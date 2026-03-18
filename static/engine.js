// ═══════════════════════════════════════════════════════════════
//  engine.js — AURA stable rendering, audio & utility layer
//  Globals referenced at call-time from index.html:
//    ctx, canvasW, canvasH, orbScale, state
// ═══════════════════════════════════════════════════════════════

// ═══════════════════════════════════════
//  HELPERS
// ═══════════════════════════════════════
function rgba(r, g, b, a) { return `rgba(${Math.round(r)},${Math.round(g)},${Math.round(b)},${a})`; }

// hexToRgb with Map cache — called ~900×/frame at peak, regex is expensive
const _hexCache = new Map();
function hexToRgb(hex) {
    if (_hexCache.has(hex)) return _hexCache.get(hex);
    const r = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    const val = r ? { r: parseInt(r[1], 16), g: parseInt(r[2], 16), b: parseInt(r[3], 16) } : { r: 167, g: 139, b: 250 };
    _hexCache.set(hex, val);
    return val;
}

// Mobile detection — used to reduce particle counts and skip expensive bloom layers
const _isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) ||
    (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.userAgent)); // iPad

// Background offscreen canvas — pre-rendered once, redrawn only when canvas resizes
let _bgCanvas = null, _bgCtx = null, _bgW = 0, _bgH = 0;
function _buildBgCanvas(w, h) {
    _bgCanvas = document.createElement('canvas');
    _bgCanvas.width = w; _bgCanvas.height = h;
    _bgCtx = _bgCanvas.getContext('2d');
    const bg = _bgCtx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#07070b'); bg.addColorStop(0.5, '#09090e'); bg.addColorStop(1, '#05050a');
    _bgCtx.fillStyle = bg; _bgCtx.fillRect(0, 0, w, h);
    const vg = _bgCtx.createRadialGradient(w/2, h/2, h * 0.15, w/2, h/2, h * 0.75);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.35)');
    _bgCtx.fillStyle = vg; _bgCtx.fillRect(0, 0, w, h);
    _bgW = w; _bgH = h;
}

const _orbPathCache = new Map();
const _PATH_SKIP = 1;
let _drawFrameCount = 0;

function _buildOrbPaths(p, R, T, b) {
    const mk = (n, fn) => { const a = []; for (let i = 0; i <= n; i++) { const t = (i/n)*Math.PI*2; a.push(fn(t)); } return a; };
    const body = mk(72, a => {
        const w = Math.sin(a*4+T*1.1)*0.07 + Math.sin(a*7-T*1.5)*0.04 + Math.sin(a*3+T*0.7)*0.05;
        const r = R*(1+w*(0.6+b*0.6)); return {x:p.x+Math.cos(a)*r, y:p.y+Math.sin(a)*r};
    });
    const shells = [0,1,2].map(s => {
        const sR = R*(0.75-s*0.15), sp = T*(0.6+s*0.2)+s*1.2;
        return mk(48, a => {
            const aa = a+sp*0.3, w = Math.sin(aa*5+sp)*0.12+Math.sin(aa*3-sp*1.3)*0.08;
            const r = sR*(1+w); return {x:p.x+Math.cos(aa)*r, y:p.y+Math.sin(aa)*r};
        });
    });
    const coreR = R*(0.28+b*0.12), cp = 1+Math.sin(T*3.5)*0.08+Math.sin(T*5.5)*0.05;
    const core = mk(36, a => {
        const w = Math.sin(a*4+T*4.5)*0.18+Math.sin(a*6+T*6)*0.1+Math.sin(a*3-T*3)*0.12;
        const r = coreR*cp*(1+w*(0.35+b*0.4)); return {x:p.x+Math.cos(a)*r, y:p.y+Math.sin(a)*r};
    });
    const edge = mk(64, a => {
        const w = Math.sin(a*6+T*2.5)*0.015+Math.sin(a*10-T*3.5)*0.01;
        const r = R*(0.97+w); return {x:p.x+Math.cos(a)*r, y:p.y+Math.sin(a)*r};
    });
    return {body, shells, core, edge, coreR, corePulse:cp};
}

function _tracePath(ctx, pts) {
    ctx.beginPath();
    for (let i = 0; i < pts.length; i++) i===0 ? ctx.moveTo(pts[i].x,pts[i].y) : ctx.lineTo(pts[i].x,pts[i].y);
    ctx.closePath();
}

function easeInOutCubic(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

function toScreen(orb) { return { x: (orb.x / 100) * canvasW, y: (orb.y / 100) * canvasH }; }

function getBrightness(orb, time) {
    if (!state.measureMs || state.measureMs <= 0) return { brightness: 0.15, dist: 500 };
    const measureMs = state.measureMs, beatMs = measureMs / 4;
    const phraseBeat = orb.phraseBeat || 1, targetMs = (phraseBeat - 1) * beatMs;
    const elapsed = ((time - state.beatTime) % measureMs + measureMs) % measureMs;
    let dist = elapsed - targetMs;
    if (dist > measureMs / 2) dist -= measureMs;
    if (dist < -measureMs / 2) dist += measureMs;
    const distAbs = Math.abs(dist), sigma = beatMs * 0.5;
    const gaussian = Math.exp(-(distAbs * distAbs) / (2 * sigma * sigma));
    return { brightness: 0.12 + 0.88 * gaussian, dist: distAbs };
}

// ═══════════════════════════════════════
//  PENTATONIC HARMONY SYSTEM
// ═══════════════════════════════════════
const PENTATONIC = [0, 3, 5, 7, 10]; // C minor pentatonic: C Eb F G Bb
// All music styles use C minor pentatonic so orb/crystal tones
// always harmonise with the background music regardless of style.

function snapToPentatonic(note) {
    const octave = Math.floor(note / 12);
    const degree = ((note % 12) + 12) % 12;
    let closest = PENTATONIC[0], minDist = 99;
    for (const p of PENTATONIC) {
        const d = Math.min(Math.abs(degree - p), 12 - Math.abs(degree - p));
        if (d < minDist) { minDist = d; closest = p; }
    }
    let result = octave * 12 + closest;
    if (note < 0 && closest > 6) result -= 12;
    return result;
}

const PENTATONIC_SCALE = [];
for (let oct = -1; oct <= 4; oct++) {
    for (const p of PENTATONIC) PENTATONIC_SCALE.push(oct * 12 + p);
}

// ═══════════════════════════════════════
//  CONSTANTS
// ═══════════════════════════════════════

const CRYSTAL_PALETTE = [
    { main: '#E8F2FF', light: '#FFFFFF', mid: '#F4F8FF', dark: '#B0C8E8', glow: '#FFFFFF' },
    { main: '#EAF0FF', light: '#FFFFFF', mid: '#F6F9FF', dark: '#B4CCEC', glow: '#FFFFFF' },
    { main: '#E6EEFF', light: '#FFFFFF', mid: '#F2F6FF', dark: '#ACBEE0', glow: '#FFFFFF' },
    { main: '#ECF2FF', light: '#FFFFFF', mid: '#F6F9FF', dark: '#B8CCEC', glow: '#FFFFFF' },
    { main: '#E4F0FF', light: '#FFFFFF', mid: '#F0F6FF', dark: '#ACCAE8', glow: '#FFFFFF' },
    { main: '#EEF4FF', light: '#FFFFFF', mid: '#F8FBFF', dark: '#BCCEF0', glow: '#FFFFFF' },
    { main: '#E2ECFF', light: '#FFFFFF', mid: '#F0F6FF', dark: '#A8C0E0', glow: '#FFFFFF' },
];

const SHARD_COLORS = [
    { main: '#FF2840', light: '#FF90A0' },
    { main: '#FF6018', light: '#FFB070' },
    { main: '#F5C800', light: '#FFE870' },
    { main: '#28C858', light: '#80EEA8' },
    { main: '#18C8E0', light: '#80EEF8' },
    { main: '#A020E0', light: '#D080F8' },
    { main: '#E018A0', light: '#F880CC' },
    { main: '#F07820', light: '#FFB870' },
];

const WARM_RELEASE = ['#C41E3A','#D4380D','#E86420','#F07B18','#FAAB0C','#FFC107','#FFD43B','#FFF5C0'];

// Active bass style names in rotation order
const BASS_NAMES = ["Golden Hour","Neon Pulse","Candy Flip","Guardia Festival","Prism","Bright Flash","Pharaoh Rush","Snake Slither","Dawnbreak","Fourside Funk"];

// ═══════════════════════════════════════
//  AUDIO ENGINE
// ═══════════════════════════════════════
class Audio {
    constructor() {
        this.ctx = null; this.ready = false; this.beatOn = true;
        this.beatInt = null; this.beat = 0; this.bassStyle = 0;
        this.bassFilter = null; this.bassGain = null;
        this.master = null;
        this._distCurve = null;
        this._activeNodes = 0;
        this._MAX_ACTIVE = 150;
        this._beatBpm = 0;
        this._beatCb = null;
        this._intentPlaying = false;
        this._needsResume = false;
        this._schedAt    = null;
        this._stepDur    = 0;
        this._nextStep   = 0;
        this._nextStepTime = 0;
        this._loopCount  = 0;
    }

    async init() {
        if (this.ready) return;
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (this.ctx.state === 'suspended') await this.ctx.resume();

        this.master = this.ctx.createGain();
        this.master.gain.value = 0.78;
        this.limiter = this.ctx.createDynamicsCompressor();
        this.limiter.threshold.value = -3;
        this.limiter.knee.value       = 2;
        this.limiter.ratio.value      = 20;
        this.limiter.attack.value     = 0.002;
        this.limiter.release.value    = 0.18;
        this.master.connect(this.limiter);
        this.limiter.connect(this.ctx.destination);

        this.musicOut = this.ctx.createGain();
        this.musicOut.gain.value = 0.82;
        this.musicOut.connect(this.ctx.destination);

        this.bassFilter = this.ctx.createBiquadFilter();
        this.bassFilter.type = 'lowpass'; this.bassFilter.frequency.value = 500; this.bassFilter.Q.value = 0.7;
        this.bassGain = this.ctx.createGain(); this.bassGain.gain.value = 0.44;
        this.bassFilter.connect(this.bassGain); this.bassGain.connect(this.musicOut);

        this.drumGain = this.ctx.createGain(); this.drumGain.gain.value = 0.38;
        this.drumGain.connect(this.musicOut);

        this.hihatGain = this.ctx.createGain(); this.hihatGain.gain.value = 0.26;
        this.hihatGain.connect(this.musicOut);

        this.chordFilter = this.ctx.createBiquadFilter();
        this.chordFilter.type = 'lowpass'; this.chordFilter.frequency.value = 1500; this.chordFilter.Q.value = 0.7;
        this.chordGain = this.ctx.createGain(); this.chordGain.gain.value = 0.38;
        this.chordFilter.connect(this.chordGain); this.chordGain.connect(this.musicOut);

        this.texGain = this.ctx.createGain(); this.texGain.gain.value = 0.10;
        this.texGain.connect(this.musicOut);

        this._distCurve = this._makeDistCurve(20);
        this._createReverb();

        const b = this.ctx.createBuffer(1, 1, 22050);
        const s = this.ctx.createBufferSource(); s.buffer = b;
        s.connect(this.ctx.destination); s.start(0);

        this._setupVisibilityHandler();
        this.ready = true;
    }

    _createReverb() {
        const sr  = this.ctx.sampleRate;
        const len = Math.floor(sr * 1.4);
        const ir  = this.ctx.createBuffer(2, len, sr);
        const earlyMs = Math.floor(sr * 0.03);
        for (let ch = 0; ch < 2; ch++) {
            const d = ir.getChannelData(ch);
            for (let i = 0; i < len; i++) {
                const norm  = i / len;
                const decay = Math.pow(1 - norm, 2.2);
                const airAbs = 1 - norm * 0.35;
                const early = i < earlyMs ? 1 + (1 - i / earlyMs) * 0.6 : 1;
                d[i] = (Math.random() * 2 - 1) * decay * airAbs * early;
            }
        }
        this.reverb = this.ctx.createConvolver();
        this.reverb.buffer = ir;

        this.reverbGain = this.ctx.createGain();
        this.reverbGain.gain.value = 0.14;
        this.reverb.connect(this.reverbGain);
        this.reverbGain.connect(this.musicOut);

        this.hihatRevSend = this.ctx.createGain(); this.hihatRevSend.gain.value = 0.28;
        this.hihatGain.connect(this.hihatRevSend); this.hihatRevSend.connect(this.reverb);

        this.chordRevSend = this.ctx.createGain(); this.chordRevSend.gain.value = 0.22;
        this.chordGain.connect(this.chordRevSend); this.chordRevSend.connect(this.reverb);

        this.texRevSend = this.ctx.createGain(); this.texRevSend.gain.value = 0.35;
        this.texGain.connect(this.texRevSend); this.texRevSend.connect(this.reverb);
    }

    _setupVisibilityHandler() {
        document.addEventListener('visibilitychange', () => {
            if (!this.ctx || !document.hidden) return;
            if (this.beatInt) { clearTimeout(this.beatInt); this.beatInt = null; }
        });

        const markNeedsResume = () => { this._needsResume = true; };
        document.addEventListener('visibilitychange', () => { if (!document.hidden) markNeedsResume(); });
        window.addEventListener('pageshow', markNeedsResume);
        window.addEventListener('focus', markNeedsResume);

        const gestureResume = () => {
            if (!this.ctx) return;
            const afterResume = () => {
                if (this._intentPlaying && this._beatBpm > 0 && !this.beatInt) {
                    this._restartBeat();
                }
                this._needsResume = false;
            };
            if (this.ctx.state === 'suspended' || this.ctx.state === 'interrupted') {
                this.ctx.resume().then(afterResume).catch(() => {});
            } else if (this.ctx.state === 'running') {
                if (this._intentPlaying && this._beatBpm > 0 && !this.beatInt) {
                    afterResume();
                } else if (this._needsResume) {
                    this._needsResume = false;
                }
            }
        };

        document.addEventListener('touchstart', gestureResume, { passive: true });
        document.addEventListener('click', gestureResume);
    }

    _startScheduler() {
        const LOOKAHEAD   = 0.08;
        const INTERVAL_MS = 20;
        this._stepDur     = 60 / (this._beatBpm * 4);
        this._nextStep    = 0;
        this._loopCount   = 0;
        this._nextStepTime = this.ctx.currentTime + 0.01;

        const tick = () => {
            if (!this._intentPlaying) return;
            while (this._nextStepTime < this.ctx.currentTime + LOOKAHEAD) {
                this._fireStep(this._nextStep, this._nextStepTime);
                this._nextStep++;
                if (this._nextStep >= 32) { this._nextStep = 0; this._loopCount++; }
                this._nextStepTime += this._stepDur;
            }
            this.beatInt = setTimeout(tick, INTERVAL_MS);
        };
        tick();
    }

    _restartBeat() {
        if (!this.ready || this.beatInt) return;
        this._startScheduler();
    }

    async unlock() {
        if (!this.ctx) await this.init();
        else if (this.ctx.state === 'suspended') await this.ctx.resume();
    }

    _scheduleCleanup(nodes, duration) {
        this._activeNodes += nodes.length;
        const cleanupMs = Math.ceil((duration + 0.15) * 1000);
        setTimeout(() => {
            nodes.forEach(n => { try { n.disconnect(); } catch(e) {} });
            this._activeNodes -= nodes.length;
        }, cleanupMs);
    }

    _canPlay() { return this.ready && this.ctx && this.ctx.state === 'running' && this._activeNodes < this._MAX_ACTIVE; }

    startBeat(bpm, cb) {
        this.stopBeat();
        this._beatBpm = bpm; this._beatCb = cb;
        this._intentPlaying = true;
        const start = performance.now();
        if (cb) cb(start);
        this._startScheduler();
    }

    stopBeat() {
        if (this.beatInt) { clearTimeout(this.beatInt); this.beatInt = null; }
        this._intentPlaying = false;
    }

    setBassStyle(style) { this.bassStyle = style % 47; }

    getBpm(style) {
        const BPMS = [108, 0, 126, 130, 0, 138, 132, 0, 0, 0,
                      110, 124, 120, 128, 118, 122, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 125, 0, 132, 0,
                      116, 0, 0, 0, 0, 0, 132];
        return BPMS[(style % 47)] || 130;
    }

    _fireStep(step, when) {
        if (!this._canPlay() || !this.beatOn) return;
        const s = this.bassStyle || 0;

        const SWING = [0.12, 0, 0.1, 0, 0, 0, 0, 0, 0, 0,
                       0.16, 0, 0.14, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0.08, 0, 0, 0, 0, 0, 0];
        const swingFrac = SWING[s] || 0;
        const scheduledAt = (swingFrac > 0 && step % 2 === 1)
            ? when + this._stepDur * swingFrac
            : when;
        this._schedAt = scheduledAt;

        const dr = this.getSubPattern(s)[step];
        if (dr) this.subDrone(dr[0], dr[1], dr[2]);
        const cp = this.getPadPattern(s)[step];
        if (cp) {
            if (cp[2] === 's') this.chordStab(cp[0], cp[1]);
            else this.warblePad(cp[0], cp[1]);
        }
        const pp = this.getPercPattern(s);
        if (pp.k[step]) this.kick808(pp.k[step]);
        if (pp.s[step]) this.tapeSnap(pp.s[step]);
        if (pp.h && pp.h[step]) this.hihat(Math.abs(pp.h[step]), pp.h[step] < 0);
        if (pp.t && pp.t[step]) this.texGrain(pp.t[step]);

        this._schedAt = null;
        this.beat = step;
    }

    playStep(step) { this._fireStep(step, this.ctx ? this.ctx.currentTime : 0); }

    getSubPattern(style) {
        const S = {
            // 00 · Fourside Funk (108 bpm)
            0: [[0,.58,.20],null,[0,.20,.08],null,[12,.52,.16],null,[7,.44,.14],null,
                [0,.54,.20],null,[10,.20,.08],null,[10,.48,.16],[9,.22,.10],[7,.36,.14],[0,.16,.06],
                [0,.56,.20],null,[0,.22,.08],null,[12,.50,.16],[12,.18,.06],[7,.42,.14],null,
                [0,.52,.20],null,[9,.22,.08],null,[7,.46,.16],null,[12,.38,.14],[0,.18,.06]],
            // 02 · Snake Slither (126 bpm)
            2: [[0,.58,.20],null,[0,.22,.08],null,[10,.50,.18],null,[11,.20,.08],null,
                [0,.54,.20],null,null,[7,.20,.08],[5,.48,.18],null,[4,.22,.10],[5,.16,.06],
                [0,.56,.20],null,[0,.20,.08],null,[7,.52,.18],null,[8,.22,.08],null,
                [0,.50,.20],null,null,[3,.18,.08],[7,.46,.18],[8,.18,.08],[7,.36,.16],null],
            // 03 · Guardia Festival (130 bpm)
            3: [[0,.52,.20],null,[3,.34,.14],null,[7,.48,.18],null,[10,.30,.12],null,
                [12,.50,.18],null,[10,.22,.10],null,[7,.46,.18],null,[5,.24,.12],[3,.16,.08],
                [0,.50,.20],null,[3,.32,.14],null,[7,.46,.18],null,[10,.28,.12],null,
                [12,.48,.18],null,[9,.20,.10],null,[7,.44,.18],[5,.20,.10],[3,.34,.14],null],
            // 05 · Bright Flash (138 bpm)
            5: [[0,.52,.20],null,[3,.32,.14],null,[7,.48,.18],null,[10,.28,.12],null,
                [12,.50,.18],null,[10,.22,.10],null,[7,.46,.18],null,[3,.26,.12],[0,.16,.06],
                [0,.50,.20],null,[3,.30,.14],null,[7,.46,.18],null,[12,.48,.20],null,
                [15,.46,.18],null,[12,.22,.10],[10,.18,.08],[7,.42,.18],null,[5,.24,.12],[7,.16,.06]],
            // 06 · Pharaoh Rush (144 bpm)
            6: [[0,.60,.18],null,null,null,[1,.44,.14],null,[4,.50,.16],null,
                [5,.56,.18],null,null,null,[7,.52,.16],null,[8,.28,.10],[7,.18,.06],
                [0,.58,.18],null,null,[1,.18,.08],[4,.52,.16],null,[5,.56,.18],null,
                [7,.54,.16],null,[8,.24,.10],null,[5,.50,.16],[4,.22,.10],[1,.44,.14],[0,.16,.06]],
            // 10 · Golden Hour (110 bpm)
            10:[[0,.66,.20],null,[0,.24,.08],null,[7,.54,.16],null,[3,.44,.14],null,
                [8,.64,.20],null,[8,.22,.08],null,[0,.52,.16],null,[3,.44,.14],[7,.20,.08],
                [3,.64,.20],null,[3,.22,.08],null,[10,.52,.16],null,[7,.40,.14],null,
                [7,.62,.20],null,[7,.22,.08],null,[2,.50,.16],null,[5,.38,.14],[10,.18,.08]],
            // 11 · Candy Flip (124 bpm)
            11:[[0,.68,.18],null,[0,.26,.08],null,[3,.56,.16],null,[7,.46,.14],null,
                [10,.66,.18],null,[10,.26,.08],null,[2,.54,.16],null,[5,.44,.14],[7,.20,.08],
                [8,.66,.18],null,[8,.24,.08],null,[3,.54,.16],null,[0,.44,.14],null,
                [7,.64,.18],null,[7,.22,.08],null,[11,.52,.16],null,[2,.40,.14],[5,.20,.08]],
            // 12 · Dawnbreak (120 bpm)
            12:[[0,.64,.20],null,[0,.24,.08],null,[7,.52,.18],null,[3,.36,.14],null,
                [8,.62,.20],null,[8,.22,.08],null,[3,.50,.16],null,[0,.40,.14],[7,.20,.08],
                [5,.64,.20],null,[5,.22,.08],null,[0,.52,.18],null,[3,.38,.14],null,
                [7,.62,.20],null,[7,.22,.08],null,[2,.50,.16],null,[0,.36,.14],[11,.18,.08]],
            // 13 · Prism (128 bpm)
            13:[[7,.68,.16],null,[7,.26,.08],null,[10,.56,.14],null,[5,.36,.12],null,
                [8,.64,.16],null,[8,.24,.08],null,[3,.52,.14],null,[0,.40,.12],[3,.20,.08],
                [10,.62,.16],null,[10,.24,.08],null,[5,.50,.14],null,[2,.36,.12],null,
                [0,.60,.16],null,[0,.24,.08],null,[7,.48,.14],null,[3,.38,.12],[7,.18,.08]],
            // 14 · Neon Pulse (118 bpm)
            14:[[7,.62,.18],null,[7,.22,.08],null,[10,.50,.18],null,[2,.28,.10],null,
                [0,.56,.20],null,[0,.20,.08],null,[7,.48,.18],null,[4,.32,.12],null,
                [5,.60,.18],null,[5,.18,.08],null,[0,.44,.16],[8,.22,.08],null,null,
                [10,.54,.18],null,[3,.38,.14],null,[5,.46,.18],null,[2,.28,.10],[7,.16,.06]],
            // 15 · Chrome Machine (122 bpm) — Daft Punk: filtered French house,
            //   robotic bass loop with octave punch on bar 2. "Around the World" DNA.
            //   Notes: root→5th→4th groove, then octave leap as the hook.
            15:[[0,.64,.22],null,[0,.28,.10],null,[7,.56,.18],null,[5,.40,.14],null,
                [0,.60,.20],null,[10,.24,.10],[7,.18,.08],[5,.52,.18],null,[3,.26,.12],[0,.16,.08],
                [0,.62,.22],null,[0,.26,.10],null,[7,.54,.18],null,[10,.40,.14],null,
                [12,.58,.20],null,[10,.22,.10],[7,.16,.08],[5,.50,.18],[3,.20,.10],[7,.42,.16],null],
            // 36 · Psycho Groove (125 bpm) — Talking Heads "Burning Down the House"/
            //   "Once in a Lifetime"/"Psycho Killer":
            //   Tina Weymouth's nervous REPEATING FIGURE — same root hits, then sudden leaps.
            //   Very staccato (.10 dur) — opposite of the long-held notes in Radio Silence.
            //   KEY MOVE: clusters of 0-0-0 repeated quickly, then a sudden angular leap to 5 or 7.
            //   The repetition IS the point — paranoid, insistent, you can't escape the riff.
            36:[[0,.64,.10],null,[0,.26,.08],[0,.18,.06],[5,.56,.10],null,[0,.22,.08],null,
                [0,.60,.12],null,null,[7,.24,.08],[0,.52,.10],[0,.18,.06],[3,.48,.10],null,
                [0,.62,.10],null,[0,.24,.08],[0,.16,.06],[5,.54,.10],null,[0,.20,.08],null,
                [0,.58,.12],[3,.20,.08],null,[7,.22,.08],[0,.50,.10],[0,.18,.06],[5,.44,.10],null],
            // 38 · Ghost Train (132 bpm) — The Specials / Madness / Toots and the Maytals:
            //   KEY MOVE: WALKING CHROMATIC SKA BASS. Roots on the beats, chromatic passing
            //   notes on the 16th note between them. Very active, very staccato (.08-.10).
            //   Ska bass is the skeleton that holds the offbeat guitar skank together.
            //   Uses -2 and 3 as chromatic connectors — chromatic passing tones are
            //   the ska bassist's signature (they learned from jazz walking bass lines).
            38:[[0,.66,.10],null,[-2,.26,.08],null,[0,.58,.10],null,[3,.22,.08],[5,.16,.06],
                [7,.62,.10],null,[5,.22,.08],[3,.16,.06],[0,.54,.10],[-2,.18,.06],[0,.48,.08],null,
                [0,.64,.10],null,[-2,.24,.08],null,[0,.56,.10],[3,.20,.08],[5,.36,.10],null,
                [7,.60,.10],[5,.20,.08],[3,.22,.08],null,[0,.52,.10],[-2,.18,.06],[0,.42,.10],null],
            // 40 · Hook, Line & Sinker (116 bpm) — Motown / James Jamerson:
            //   Jamerson never stopped moving — his bass lines were almost purely 16th notes.
            //   KEY MOVE: bass fills EVERY SINGLE PHRASE with constant melodic motion.
            //   Uses 0/3/5/7 (minor pentatonic) with chromatic passing tone -2 woven in.
            //   Medium note lengths (.10-.12) — Jamerson played with "The Hook" (one finger)
            //   getting a fat legato tone. Very different from cumbia's long-short seesaw.
            40:[[0,.64,.10],[3,.30,.08],[5,.50,.10],[3,.22,.08],[0,.56,.12],[3,.20,.08],[5,.44,.10],null,
                [7,.58,.12],[5,.22,.08],[3,.48,.10],[0,.18,.06],[5,.52,.10],[-2,.20,.08],[0,.42,.10],null,
                [0,.62,.10],[3,.28,.08],[5,.48,.10],[7,.20,.08],[5,.54,.12],[3,.22,.08],[0,.44,.10],null,
                [7,.56,.12],[10,.22,.08],[7,.46,.10],[5,.18,.06],[3,.50,.10],[0,.20,.08],[5,.38,.10],null],
            // 46 · Purple Haze (132 bpm) — Prince / Minneapolis Sound LinnDrum:
            //   KEY MOVE: bass uses note 10 (b7) as a constant tension partner to root (0).
            //   Extremely staccato (.08) — the LinnDrum era bass was punchy and short.
            //   Lots of space (nulls) — the DRUMS carry the density, bass punctuates.
            //   Uses 0/5/7/10 only — Prince's purple minor-pentatonic signature.
            46:[[0,.70,.08],null,null,null,[10,.28,.06],null,[0,.60,.08],null,
                [5,.64,.08],null,[3,.22,.06],null,[0,.56,.08],[10,.18,.06],[7,.48,.08],null,
                [0,.68,.08],null,null,[10,.24,.06],[0,.58,.08],null,null,null,
                [7,.62,.08],null,[5,.20,.06],null,[0,.54,.08],[10,.18,.06],[7,.40,.08],null],
        };
        return S[style] || S[0];
    }

    getPadPattern(style) {
        const P = {
            // 00 · Fourside Funk (108 bpm)
            0: [[[0,3,7,10],.36],null,null,null,null,null,null,null,
                null,null,null,null,[[10,14,17],.24,'s'],null,null,null,
                [[0,3,7,10],.34],null,null,null,null,null,null,null,
                [[9,12,16,19],.26],null,null,null,null,null,null,null],
            // 02 · Snake Slither (126 bpm)
            2: [[[0,7,12],.44,'s'],null,null,null,null,null,null,null,
                [[0,7],.36,'s'],null,null,null,[[5,12],.28,'s'],null,null,null,
                [[0,7,12],.42,'s'],null,null,null,null,[[7,14],.30,'s'],null,null,
                [[0,5,7],.34,'s'],null,null,null,null,null,[[3,7,10],.26,'s'],null],
            // 03 · Guardia Festival (130 bpm)
            3: [[[0,3,7,10],.40,'s'],null,null,null,null,null,[[7,10,14],.30,'s'],null,
                [[0,3,7],.36,'s'],null,null,null,[[5,10,12],.26,'s'],null,null,null,
                [[0,3,7,10],.38,'s'],null,null,null,null,null,[[7,10,14],.28,'s'],null,
                [[0,3,7],.34,'s'],null,null,null,[[9,12,16],.26,'s'],null,null,null],
            // 05 · Bright Flash (138 bpm)
            5: [[[0,7,12],.42,'s'],null,null,null,null,null,[[3,7,10],.32,'s'],null,
                [[0,7,12],.40,'s'],null,null,null,null,[[5,10,12],.28,'s'],null,null,
                [[0,7,12],.40,'s'],null,null,null,null,null,[[7,12,15],.30,'s'],null,
                [[3,10,15],.38,'s'],null,null,null,null,null,[[0,7,12],.36,'s'],null],
            // 06 · Pharaoh Rush (144 bpm)
            6: [[[0,7],.46,'s'],null,null,null,null,null,[[4,8],.34,'s'],null,
                [[5,8,12],.40,'s'],null,null,null,null,[[7,10],.30,'s'],null,null,
                [[0,7],.44,'s'],null,null,null,[[1,8],.32,'s'],null,null,null,
                [[5,8,12],.38,'s'],null,null,null,null,null,[[0,5,8],.34,'s'],null],
            // 10 · Golden Hour (110 bpm)
            10:[[[0,3,7,10],.46],null,null,null,null,null,null,null,
                [[-4,0,3,7],.36,'s'],null,null,null,null,null,null,null,
                [[3,7,10,14],.44],null,null,null,null,null,null,null,
                [[7,11,14,17],.32,'s'],null,null,null,
                [[0,3,7],.38,'s'],null,null,null],
            // 11 · Candy Flip (124 bpm)
            11:[[[0,3,7],.48,'s'],null,null,null,null,null,null,null,
                [[-2,2,5],.40,'s'],null,null,null,null,null,null,null,
                [[-4,0,3],.44,'s'],null,null,null,null,null,null,null,
                [[7,11,14],.36,'s'],null,null,null,
                [[0,3,7],.40,'s'],null,null,null],
            // 12 · Dawnbreak (120 bpm)
            12:[[[0,3,7,10],.46],null,null,null,null,null,null,null,
                [[-4,0,3,7],.36,'s'],null,null,null,null,null,null,null,
                [[5,8,12,15],.44],null,null,null,null,null,null,null,
                [[7,12,14,17],.34,'s'],null,null,null,
                [[0,3,7],.36,'s'],null,null,null],
            // 13 · Prism (128 bpm)
            13:[[[7,10,14],.44,'s'],null,null,null,null,null,null,null,
                [[-4,0,3],.40,'s'],null,null,null,null,null,null,null,
                [[-2,2,5,8],.42,'s'],null,null,null,null,null,null,null,
                [[0,3,7],.36,'s'],null,null,null,
                [[7,10,14],.38,'s'],null,null,null],
            // 14 · Neon Pulse (118 bpm)
            14:[[[7,10,14,17],.40,'s'],null,null,null,[[7,10,14],.36,'s'],null,null,null,
                null,null,null,null,[[0,4,7,10],.34,'s'],null,null,null,
                [[5,8,12,15],.38,'s'],null,null,null,[[5,8,12],.32,'s'],null,null,null,
                null,null,null,null,[[-2,2,5,8],.30,'s'],null,null,null],
            // 15 · Chrome Machine — French house chord stabs: punchy Cm7 on beat 1,
            //   staccato hits echo on off-beats. Bright, filtered, euphoric.
            15:[[[0,3,7,10],.46,'s'],null,null,null,null,null,[[7,10,14],.34,'s'],null,
                [[5,8,12],.40,'s'],null,null,null,[[3,7,10],.30,'s'],null,null,null,
                [[0,3,7,10],.44,'s'],null,null,null,null,null,[[10,14,17],.34,'s'],null,
                [[7,10,14],.38,'s'],null,null,null,null,null,[[0,3,7],.36,'s'],null],
            // 36 · Psycho Groove — angular post-punk chord stabs on unexpected beats.
            //   [0,7] = power chord, raw and unambiguous. Stabs land on beat 2 (not 1!) —
            //   the opposite of where you expect them, creating nervous rhythmic displacement.
            //   [5,10] = power chord up a 4th = Talking Heads' TV-on-the-Radio tension.
            36:[null,null,null,null,[[0,7],.40,'s'],null,null,null,
                null,null,null,null,null,null,null,null,
                [[0,7],.38,'s'],null,null,null,null,null,[[5,10],.30,'s'],null,
                null,null,null,null,[[0,7],.34,'s'],null,null,null],
            // 38 · Ghost Train — SKA UPSTROKE STABS. The guitar skank lands on the 8th-note
            //   upbeats: steps 2, 6, 10, 14, 18, 22, 26, 30 — BETWEEN the beats, not on them.
            //   This is the most rhythmically unique pad placement in the entire collection.
            //   [0,7,12] bright major = ska was upbeat and major-key (different from reggae's minors).
            38:[null,null,[[0,7,12],.36,'s'],null,null,null,[[5,10,14],.30,'s'],null,
                null,null,[[0,7,12],.34,'s'],null,null,null,[[3,7,10],.28,'s'],null,
                null,null,[[0,7,12],.36,'s'],null,null,null,[[5,10,14],.30,'s'],null,
                null,null,[[7,12,17],.32,'s'],null,null,null,[[0,7,12],.26,'s'],null],
            // 40 · Hook, Line & Sinker — Motown horn stabs that punch between bass phrases.
            //   [0,7,12] on beat 1 = the downbeat stab. [3,7,10] = iii = Motown's warm turnaround.
            //   [5,10,14] = IV = the big lift that Motown arrangements always built toward.
            //   Short staccato stabs (classic Motown horn section was punchy, not sustained).
            40:[[[0,7,12],.42,'s'],null,null,null,null,null,null,null,
                [[3,7,10],.34,'s'],null,null,null,null,null,null,null,
                [[0,7,12],.40,'s'],null,null,null,null,null,null,null,
                [[5,10,14],.36,'s'],null,null,null,[[3,7,10],.28,'s'],null,null,null],
            // 46 · Purple Haze — two sparse stabs per two bars. Everything else is drums.
            //   [0,7,12] tight major = Prince's clean bright chord. [5,10,12] = ambiguous IV/V.
            //   Long silence between stabs = the Minneapolis Sound breathing room.
            46:[[[0,7,12],.42,'s'],null,null,null,null,null,null,null,
                null,null,null,null,[[5,10,12],.34,'s'],null,null,null,
                [[0,7,12],.40,'s'],null,null,null,null,null,null,null,
                null,null,null,null,[[0,7,12],.30,'s'],null,null,null],
        };
        return P[style] || P[0];
    }

    getPercPattern(style) {
        const R = {
            // 00 · Fourside Funk (108 bpm)
            0: { k:[.72,0,0,0,0,0,.32,0,.62,0,.20,0,0,0,.26,0,
                    .72,0,.16,0,0,0,.32,0,.62,0,.20,0,0,0,.26,.14],
                 s:[0,0,0,0,.54,0,0,.14,0,0,0,0,.52,0,0,.12,
                    0,0,0,0,.54,0,0,.14,0,0,0,0,.52,0,0,.16],
                 h:[.30,.14,.22,.14,.30,.14,-.34,.14,.30,.14,.22,.14,.30,.14,-.34,.14,
                    .30,.14,.22,.14,.30,.14,-.34,.14,.30,.14,.22,.14,.30,.14,-.34,.14],
                 t:[0,0,.04,0,0,.04,0,0,0,0,.04,0,0,0,.04,0,
                    0,0,.04,0,0,.04,0,0,0,0,.04,0,0,.04,0,0] },
            // 02 · Snake Slither (126 bpm)
            2: { k:[.70,0,0,0,0,0,.30,0,.58,0,.20,0,0,0,.28,0,
                    .70,0,.16,0,0,0,.30,0,.58,0,.20,0,0,0,.28,.14],
                 s:[0,0,0,0,.52,0,0,.14,0,0,0,0,.50,0,0,.12,
                    0,0,0,0,.52,0,.12,.14,0,0,0,0,.50,0,0,.16],
                 h:[.28,.12,.20,.12,.28,.12,-.32,.12,.28,.12,.20,.12,.28,.12,-.32,.12,
                    .28,.12,.20,.12,.28,.12,-.32,.12,.28,.12,.20,.12,.28,.12,-.32,.12],
                 t:[0,0,0,.04,0,0,.04,0,0,0,0,.04,0,0,.04,0,
                    0,0,0,.04,0,0,.04,0,0,0,0,.04,0,0,.04,.04] },
            // 03 · Guardia Festival (130 bpm)
            3: { k:[.64,0,0,0,0,0,.28,0,.52,0,.18,0,0,0,.22,0,
                    .64,0,0,0,0,0,.28,0,.52,0,.18,0,0,0,.22,.12],
                 s:[0,0,0,0,.50,0,0,.12,0,0,0,0,.48,0,0,.10,
                    0,0,0,0,.50,0,0,.12,0,0,0,0,.48,0,0,.14],
                 h:[.28,.12,.20,.12,.28,.12,-.32,.12,.28,.12,.20,.12,.28,.12,-.32,.12,
                    .28,.12,.20,.12,.28,.12,-.32,.12,.28,.12,.20,.12,.28,.12,-.32,.12],
                 t:[0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,
                    0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04] },
            // 05 · Bright Flash (138 bpm)
            5: { k:[.70,0,0,0,0,0,.32,0,.58,0,.20,0,0,0,.26,0,
                    .70,0,.16,0,0,0,.32,0,.58,0,.20,0,0,0,.26,.14],
                 s:[0,0,0,0,.52,0,0,.14,0,0,0,0,.50,0,0,.12,
                    0,0,0,0,.52,0,.14,0,0,0,0,0,.50,0,0,.16],
                 h:[.28,0,.20,0,.28,0,-.32,0,.28,0,.20,0,.28,0,-.30,0,
                    .28,0,.20,0,.28,0,-.32,0,.28,0,.20,0,.28,0,-.30,0],
                 t:[0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,
                    0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04] },
            // 06 · Pharaoh Rush (144 bpm)
            6: { k:[.76,0,0,0,.36,0,0,0,.64,0,.20,0,.24,0,0,0,
                    .74,0,0,0,.36,0,.18,0,.62,0,.20,0,.24,0,.16,0],
                 s:[0,0,0,0,.58,0,0,.16,0,0,0,0,.56,0,.14,0,
                    0,0,0,0,.58,0,.16,0,0,0,0,0,.56,0,.14,.18],
                 h:[.34,.18,.26,.18,.34,.18,-.38,.18,.34,.18,.26,.18,.34,.18,-.38,.18,
                    .34,.18,.26,.18,.34,.18,-.38,.18,.34,.18,.26,.18,.34,.18,-.38,.18],
                 t:[0,0,.04,0,.04,0,.04,0,0,0,.04,0,.04,0,.04,0,
                    0,0,.04,0,.04,0,.04,0,0,0,.04,0,.04,0,.04,0] },
            // 10 · Golden Hour (110 bpm)
            10:{ k:[.72,0,0,0,.28,0,.26,0,.62,0,0,0,.24,0,.22,0,
                    .70,0,0,0,.26,0,.24,0,.60,0,0,0,.22,0,.20,0],
                 s:[0,0,0,0,.50,0,0,.14,0,0,0,0,.46,0,.12,0,
                    0,0,0,0,.48,0,0,.14,0,0,0,0,.44,0,.12,.16],
                 h:[.28,0,-.32,0,.28,0,-.32,0,.28,0,-.32,0,.28,0,-.32,0,
                    .28,0,-.32,0,.28,0,-.32,0,.28,0,-.32,0,.28,0,-.32,0],
                 t:[0,0,.05,0,.05,0,0,0,0,0,.05,0,.05,0,0,0,
                    0,0,.05,0,.05,0,0,0,0,0,.05,0,.05,0,0,0] },
            // 11 · Candy Flip (124 bpm)
            11:{ k:[.74,0,0,0,.28,0,.26,0,.64,0,0,0,.24,0,.22,0,
                    .72,0,0,0,.28,0,.24,0,.62,0,.18,0,.22,0,0,0],
                 s:[0,0,0,0,.56,0,.16,0,0,0,0,0,.52,0,.14,0,
                    0,0,0,0,.54,0,.16,0,0,0,0,0,.50,0,.14,.18],
                 h:[.28,.22,.28,.22,.28,.22,-.34,.22,.28,.22,.28,.22,.28,.22,-.34,.22,
                    .28,.22,.28,.22,.28,.22,-.34,.22,.28,.22,.28,.22,.28,.22,-.34,.22],
                 t:[0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,
                    0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04] },
            // 12 · Dawnbreak (120 bpm)
            12:{ k:[.70,0,0,0,0,0,.28,0,.60,0,0,0,0,0,.26,0,
                    .70,0,0,0,0,0,.26,0,.58,0,0,0,0,0,.24,0],
                 s:[0,0,0,0,.46,0,0,.12,0,0,0,0,.44,0,.10,0,
                    0,0,0,0,.44,0,0,.12,0,0,0,0,.42,0,.10,.14],
                 h:[.22,0,-.28,0,.22,0,-.28,0,.22,0,-.28,0,.22,0,-.28,0,
                    .22,0,-.28,0,.22,0,-.28,0,.22,0,-.28,0,.22,0,-.28,0],
                 t:[0,0,.05,0,0,0,.05,0,0,0,.05,0,0,0,.05,0,
                    0,0,.05,0,0,0,.05,0,0,0,.05,0,0,0,.05,0] },
            // 13 · Prism (128 bpm)
            13:{ k:[.72,0,0,0,.26,0,.24,0,.64,0,0,0,.22,0,.20,0,
                    .70,0,0,0,.26,0,.22,0,.62,0,.18,0,.22,0,0,0],
                 s:[0,0,.14,0,.54,0,.16,0,0,0,.14,0,.50,0,.14,0,
                    0,0,.16,0,.52,0,.16,0,0,0,.14,0,.48,0,.14,.12],
                 h:[.30,.18,.26,.18,.30,.18,-.34,.18,.30,.18,.26,.18,.30,.18,-.34,.18,
                    .30,.18,.26,.18,.30,.18,-.34,.18,.30,.18,.26,.18,.30,.18,-.34,.18],
                 t:[0,.03,0,.03,0,.03,0,.03,0,.03,0,.03,0,.03,0,.03,
                    0,.03,0,.03,0,.03,0,.03,0,.03,0,.03,0,.03,0,.03] },
            // 14 · Neon Pulse (118 bpm)
            14:{ k:[.68,0,0,0,.24,0,0,0,.58,0,.18,0,.20,0,0,0,
                    .66,0,0,0,.24,0,.16,0,.56,0,.18,0,.20,0,0,0],
                 s:[0,0,0,0,.52,0,0,.14,0,0,0,0,.48,0,.12,0,
                    0,0,0,0,.50,0,0,.12,0,0,0,0,.46,0,.12,.16],
                 h:[.28,.14,.22,.14,.28,.14,-.32,.14,.28,.14,.22,.14,.28,.14,-.32,.14,
                    .28,.14,.22,.14,.28,.14,-.32,.14,.28,.14,.22,.14,.28,.14,-.32,.14],
                 t:[0,0,.04,0,.04,0,.04,0,0,0,.04,0,.04,0,.04,0,
                    0,0,.04,0,.04,0,.04,0,0,0,.04,0,.04,0,.04,0] },
            // 15 · Chrome Machine — 4-on-the-floor kick (every beat, no exceptions),
            //   tight 16th hihat (every step, all the same velocity = robotic),
            //   snare on 2&4 with ghost, no texture grain (pure machine precision).
            15:{ k:[.78,0,0,.20,0,0,0,0,.72,0,.18,0,0,0,0,0,
                    .78,0,0,.20,0,0,0,0,.72,0,.18,0,0,0,.20,0],
                 s:[0,0,0,0,.56,0,0,.14,0,0,0,0,.54,0,0,.12,
                    0,0,0,0,.56,0,0,.16,0,0,0,0,.54,0,0,.12],
                 h:[.30,.30,.30,.30,.30,.30,-.36,.30,.30,.30,.30,.30,.30,.30,-.36,.30,
                    .30,.30,.30,.30,.30,.30,-.36,.30,.30,.30,.30,.30,.30,.30,-.36,.30],
                 t:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] },
            // 36 · Psycho Groove — Chris Frantz: nervous post-punk precision.
            //   Kick on 1 and 3, with an EXTRA kick on &3 — the Talking Heads push that
            //   makes every bar feel like it's tipping forward into the next one.
            //   Snare on 2 and 4 with a very light ghost — Frantz was clean, not funky.
            //   16th hihats alternating closed/open — the post-punk shimmer.
            //   Zero texture grain — angular and dry, the sonic opposite of Lagos Express.
            36:{ k:[.72,0,0,0,0,0,.24,0,.64,0,.24,0,0,0,0,0,
                    .70,0,0,0,0,0,.22,0,.62,0,.22,0,0,0,.18,0],
                 s:[0,0,0,0,.54,0,0,.10,0,0,0,0,.50,0,.08,0,
                    0,0,0,0,.52,0,0,.12,0,0,0,0,.50,0,.08,.10],
                 h:[.26,.14,-.30,.14,.26,.14,-.30,.14,.26,.14,-.30,.14,.26,.14,-.30,.14,
                    .26,.14,-.30,.14,.26,.14,-.30,.14,.26,.14,-.30,.14,.26,.14,-.30,.14],
                 t:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] },
            // 38 · Ghost Train — the most rhythmically distinctive hihat in the collection.
            //   Hihat plays ONLY on 8th-note upbeats (steps 2,6,10,14,18,22,26,30) — NEVER
            //   on the beats themselves. This is unique among all 39 styles.
            //   Kick on 1 and 3, snare HARD on 2 and 4 (ska was a dance music, snare big).
            //   Light texture grain on the beat only = the warmth of a ska record.
            38:{ k:[.68,0,0,0,0,0,.20,0,.60,0,0,0,0,0,.18,0,
                    .66,0,0,0,0,0,.18,0,.58,0,0,0,0,0,.16,0],
                 s:[0,0,0,0,.60,0,0,0,0,0,0,0,.58,0,0,0,
                    0,0,0,0,.60,0,0,0,0,0,0,0,.58,0,0,.12],
                 h:[0,.32,0,0,0,.32,0,0,0,.32,0,0,0,.32,0,0,
                    0,.32,0,0,0,.32,0,0,0,.32,0,0,0,.32,0,0],
                 t:[.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,
                    .04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0,.04,0] },
            // 40 · Hook, Line & Sinker — Benny Benjamin / Uriel Jones Motown kit.
            //   KICK: 1 and 3, clean (Motown was 1-and-3 like the Beatles but heavier).
            //   SNARE: the LOUDEST in the collection (.68) — Motown snare was a crack of thunder.
            //   Plus ghost notes on the 8th subdivisions (Benjamin played a constant ghost bed).
            //   16th hihats, all identical velocity (.24) = strict Motown timekeeping.
            //   Texture grain on EVERY 16th at .06 = the tambourine that was on every Motown record.
            40:{ k:[.74,0,0,0,0,0,0,0,.66,0,0,0,0,0,0,0,
                    .72,0,0,0,0,0,0,0,.64,0,0,0,0,0,0,0],
                 s:[0,0,.20,0,.68,0,.20,0,0,0,.20,0,.64,0,.20,0,
                    0,0,.22,0,.68,0,.20,0,0,0,.20,0,.64,0,.20,.14],
                 h:[.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,
                    .24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24,.24],
                 t:[.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,
                    .06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06,.06] },
            // 46 · Purple Haze — LinnDrum / Prince: the most relentless open-hihat track here.
            //   KICK: 1 (.76), &2 (.28), 3 (.66) — Prince's signature triplet-push feel.
            //   SNARE: 2 and 4 only, VERY HARD (.64) — the LinnDrum snare crack.
            //   HIHAT: ALL OPEN on every single 16th, identical velocity (.26) — the Prince
            //   shimmer that defines "I Would Die 4 U"/"Let's Go Crazy". Completely
            //   uniform = it sounds like an electric shaker, not a drummer.
            //   ZERO texture grain — the LinnDrum was cold, bright, and completely dry.
            46:{ k:[.76,0,0,0,0,0,.28,0,.66,0,0,0,0,0,.22,0,
                    .74,0,0,0,0,0,.26,0,.64,0,0,0,0,0,.20,0],
                 s:[0,0,0,0,.64,0,0,0,0,0,0,0,.62,0,0,0,
                    0,0,0,0,.64,0,0,0,0,0,0,0,.62,0,0,0],
                 h:[-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,
                    -.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26,-.26],
                 t:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] },
        };
        return R[style] || R[0];
    }

    getMelodyPattern() { return new Array(16).fill(null); }

    subDrone(semitone, velocity, duration) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const freq = 65.41 * Math.pow(2, semitone / 12);
        const dur = duration + 0.25;
        const nodes = [];
        const osc = this.ctx.createOscillator(); osc.type = 'triangle'; osc.frequency.value = freq;
        const g1 = this.ctx.createGain(); g1.gain.value = 0.45;
        osc.connect(g1); nodes.push(osc, g1);
        const oct = this.ctx.createOscillator(); oct.type = 'sine'; oct.frequency.value = freq * 2;
        const g2 = this.ctx.createGain(); g2.gain.value = 0.3;
        oct.connect(g2); nodes.push(oct, g2);
        const h3 = this.ctx.createOscillator(); h3.type = 'sine'; h3.frequency.value = freq * 3;
        const g3 = this.ctx.createGain(); g3.gain.value = 0.12;
        h3.connect(g3); nodes.push(h3, g3);
        const env = this.ctx.createGain();
        env.gain.setValueAtTime(0, t);
        env.gain.linearRampToValueAtTime(velocity * 0.40, t + 0.04);
        env.gain.setValueAtTime(velocity * 0.40, t + duration * 0.55);
        env.gain.exponentialRampToValueAtTime(0.001, t + dur);
        g1.connect(env); g2.connect(env); g3.connect(env);
        env.connect(this.bassFilter);
        nodes.push(env);
        [osc, oct, h3].forEach(o => { o.start(t); o.stop(t + dur); });
        this._scheduleCleanup(nodes, dur);
    }

    kick808(vel) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const osc = this.ctx.createOscillator(); osc.type = 'sine';
        osc.frequency.setValueAtTime(55 + vel * 15, t);
        osc.frequency.exponentialRampToValueAtTime(28, t + 0.2);
        const env = this.ctx.createGain();
        env.gain.setValueAtTime(0, t);
        env.gain.linearRampToValueAtTime(vel * 0.6, t + 0.006);
        env.gain.exponentialRampToValueAtTime(vel * 0.2, t + 0.08);
        env.gain.exponentialRampToValueAtTime(0.001, t + 0.45);
        osc.connect(env); env.connect(this.drumGain);
        const click = this.ctx.createOscillator(); click.type = 'triangle';
        click.frequency.setValueAtTime(300 + vel * 60, t);
        click.frequency.exponentialRampToValueAtTime(120, t + 0.025);
        const clickEnv = this.ctx.createGain();
        clickEnv.gain.setValueAtTime(vel * 0.35, t);
        clickEnv.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
        click.connect(clickEnv); clickEnv.connect(this.drumGain);
        osc.start(t); osc.stop(t + 0.5);
        click.start(t); click.stop(t + 0.06);
        this._scheduleCleanup([osc, env, click, clickEnv], 0.5);
    }

    tapeSnap(vel) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const bufLen = Math.floor(this.ctx.sampleRate * 0.04);
        const buf = this.ctx.createBuffer(1, bufLen, this.ctx.sampleRate);
        const ch = buf.getChannelData(0);
        for (let i = 0; i < bufLen; i++) ch[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufLen * 0.2));
        const noise = this.ctx.createBufferSource(); noise.buffer = buf;
        const filt = this.ctx.createBiquadFilter(); filt.type = 'lowpass'; filt.frequency.value = 400; filt.Q.value = 0.8;
        const env = this.ctx.createGain();
        env.gain.setValueAtTime(vel * 0.35, t);
        env.gain.exponentialRampToValueAtTime(0.001, t + 0.05);
        const body = this.ctx.createOscillator(); body.type = 'sine';
        body.frequency.setValueAtTime(180, t); body.frequency.exponentialRampToValueAtTime(100, t + 0.02);
        const bEnv = this.ctx.createGain();
        bEnv.gain.setValueAtTime(vel * 0.12, t); bEnv.gain.exponentialRampToValueAtTime(0.001, t + 0.03);
        noise.connect(filt); filt.connect(env); env.connect(this.drumGain);
        body.connect(bEnv); bEnv.connect(this.drumGain);
        noise.start(t); noise.stop(t + 0.06); body.start(t); body.stop(t + 0.04);
        this._scheduleCleanup([noise, filt, env, body, bEnv], 0.07);
    }

    hihat(vel, open = false) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const dur = open ? 0.14 : 0.04;
        const bufLen = Math.floor(this.ctx.sampleRate * dur);
        const buf = this.ctx.createBuffer(1, bufLen, this.ctx.sampleRate);
        const ch = buf.getChannelData(0);
        const decayRate = open ? 0.38 : 0.1;
        for (let i = 0; i < bufLen; i++) ch[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufLen * decayRate));
        const noise = this.ctx.createBufferSource(); noise.buffer = buf;
        const noiseFilt = this.ctx.createBiquadFilter();
        noiseFilt.type = 'highpass';
        noiseFilt.frequency.value = open ? 6000 : 8500;
        noiseFilt.Q.value = 0.5;
        const noiseEnv = this.ctx.createGain();
        noiseEnv.gain.setValueAtTime(vel * 0.30, t);
        noiseEnv.gain.exponentialRampToValueAtTime(0.001, t + dur);
        noise.connect(noiseFilt); noiseFilt.connect(noiseEnv); noiseEnv.connect(this.hihatGain);
        const metal = this.ctx.createOscillator(); metal.type = 'square';
        metal.frequency.value = open ? 3200 : 4800;
        const metalFilt = this.ctx.createBiquadFilter();
        metalFilt.type = 'bandpass';
        metalFilt.frequency.value = open ? 3500 : 5200;
        metalFilt.Q.value = 3.5;
        const metalEnv = this.ctx.createGain();
        metalEnv.gain.setValueAtTime(vel * 0.07, t);
        metalEnv.gain.exponentialRampToValueAtTime(0.001, t + (open ? 0.06 : 0.015));
        metal.connect(metalFilt); metalFilt.connect(metalEnv); metalEnv.connect(this.hihatGain);
        const bright = this.ctx.createOscillator(); bright.type = 'sine';
        bright.frequency.value = open ? 7800 : 10200;
        const brightEnv = this.ctx.createGain();
        brightEnv.gain.setValueAtTime(vel * 0.04, t);
        brightEnv.gain.exponentialRampToValueAtTime(0.001, t + (open ? 0.04 : 0.01));
        bright.connect(brightEnv); brightEnv.connect(this.hihatGain);
        noise.start(t); noise.stop(t + dur + 0.01);
        metal.start(t); metal.stop(t + (open ? 0.07 : 0.02));
        bright.start(t); bright.stop(t + (open ? 0.05 : 0.015));
        this._scheduleCleanup([noise, noiseFilt, noiseEnv, metal, metalFilt, metalEnv, bright, brightEnv], dur + 0.02);
    }

    texGrain(vel) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const bufLen = Math.floor(this.ctx.sampleRate * 0.1);
        const buf = this.ctx.createBuffer(1, bufLen, this.ctx.sampleRate);
        const ch = buf.getChannelData(0);
        for (let i = 0; i < bufLen; i++) ch[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufLen * 0.5));
        const noise = this.ctx.createBufferSource(); noise.buffer = buf;
        const filt = this.ctx.createBiquadFilter(); filt.type = 'bandpass'; filt.frequency.value = 500; filt.Q.value = 0.5;
        const env = this.ctx.createGain();
        env.gain.setValueAtTime(0, t); env.gain.linearRampToValueAtTime(vel, t + 0.02);
        env.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
        noise.connect(filt); filt.connect(env); env.connect(this.texGain);
        noise.start(t); noise.stop(t + 0.12);
        this._scheduleCleanup([noise, filt, env], 0.12);
    }

    warblePad(semitones, vel) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const baseFreq = 130.81;
        const dur = 2.0;
        const nodes = [];
        const mixer = this.ctx.createGain(); mixer.gain.value = 1;
        mixer.connect(this.chordFilter);
        nodes.push(mixer);
        semitones.forEach(semi => {
            const freq = baseFreq * Math.pow(2, semi / 12);
            const o1 = this.ctx.createOscillator(); o1.type = 'triangle'; o1.frequency.value = freq;
            const o2 = this.ctx.createOscillator(); o2.type = 'sine'; o2.frequency.value = freq * 1.005;
            const o3 = this.ctx.createOscillator(); o3.type = 'sine'; o3.frequency.value = freq * 0.995;
            const o4 = this.ctx.createOscillator(); o4.type = 'sine'; o4.frequency.value = freq * 2;
            const noteVol = vel * 0.22 / Math.max(3, semitones.length);
            const g = this.ctx.createGain();
            g.gain.setValueAtTime(0, t);
            g.gain.linearRampToValueAtTime(noteVol, t + 0.2);
            g.gain.setValueAtTime(noteVol, t + dur * 0.5);
            g.gain.exponentialRampToValueAtTime(0.001, t + dur);
            const g4 = this.ctx.createGain();
            g4.gain.setValueAtTime(0, t);
            g4.gain.linearRampToValueAtTime(noteVol * 0.35, t + 0.15);
            g4.gain.exponentialRampToValueAtTime(0.001, t + dur * 0.6);
            o1.connect(g); o2.connect(g); o3.connect(g); g.connect(mixer);
            o4.connect(g4); g4.connect(mixer);
            [o1, o2, o3, o4].forEach(o => { o.start(t); o.stop(t + dur + 0.05); });
            nodes.push(o1, o2, o3, o4, g, g4);
        });
        this._scheduleCleanup(nodes, dur + 0.1);
    }

    chordStab(semitones, vel) {
        if (!this._canPlay()) return;
        const t = this._schedAt ?? this.ctx.currentTime;
        const baseFreq = 130.81;
        const dur = 0.20;
        const nodes = [];
        const mixer = this.ctx.createGain(); mixer.gain.value = 1;
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass'; filter.frequency.value = 2400; filter.Q.value = 1.0;
        mixer.connect(filter); filter.connect(this.chordGain);
        nodes.push(mixer, filter);
        semitones.forEach(semi => {
            const freq = baseFreq * Math.pow(2, semi / 12);
            const o1 = this.ctx.createOscillator(); o1.type = 'triangle'; o1.frequency.value = freq;
            const o2 = this.ctx.createOscillator(); o2.type = 'sine'; o2.frequency.value = freq * 2;
            const noteVol = vel * 0.28 / Math.max(3, semitones.length);
            const g = this.ctx.createGain();
            g.gain.setValueAtTime(0, t);
            g.gain.linearRampToValueAtTime(noteVol, t + 0.005);
            g.gain.exponentialRampToValueAtTime(noteVol * 0.25, t + 0.06);
            g.gain.exponentialRampToValueAtTime(0.001, t + dur);
            const g2 = this.ctx.createGain();
            g2.gain.setValueAtTime(0, t);
            g2.gain.linearRampToValueAtTime(noteVol * 0.22, t + 0.003);
            g2.gain.exponentialRampToValueAtTime(0.001, t + dur * 0.5);
            o1.connect(g); g.connect(mixer);
            o2.connect(g2); g2.connect(mixer);
            o1.start(t); o1.stop(t + dur + 0.05);
            o2.start(t); o2.stop(t + dur * 0.5 + 0.05);
            nodes.push(o1, o2, g, g2);
        });
        this._scheduleCleanup(nodes, dur + 0.1);
    }

    playBass(step) { this.playStep(step); }

    _makeDistCurve(amount) {
        const s = 256, c = new Float32Array(s);
        for (let i = 0; i < s; i++) { const x = (i * 2) / s - 1; c[i] = (Math.PI + amount) * x / (Math.PI + amount * Math.abs(x)); }
        return c;
    }

    tone(note, dur = 1.1, vol = 0.25) {
        if (!this._canPlay()) return;
        note = snapToPentatonic(note);
        while (note < -3) note += 12;
        const freq = 261.63 * Math.pow(2, note / 12);
        const t = this.ctx.currentTime;
        const partials = [
            { ratio: 1,     type: 'triangle', amp: 0.42, decayMul: 1.0  },
            { ratio: 0.997, type: 'triangle', amp: 0.22, decayMul: 0.95 },
            { ratio: 1.004, type: 'triangle', amp: 0.22, decayMul: 0.90 },
            { ratio: 2,     type: 'sine',     amp: 0.16, decayMul: 0.55 },
            { ratio: 2.76,  type: 'sine',     amp: 0.05, decayMul: 0.40 },
            { ratio: 0.5,   type: 'triangle', amp: 0.12, decayMul: 0.75 },
        ];
        const mixer = this.ctx.createGain(); mixer.gain.value = 1;
        const filterFloor = Math.max(700, freq * 3);
        const filterMid = Math.max(1200, freq * 4);
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass'; filter.Q.value = 1.2;
        filter.frequency.setValueAtTime(5500 + vol * 3000, t);
        filter.frequency.exponentialRampToValueAtTime(filterMid, t + dur * 0.4);
        filter.frequency.exponentialRampToValueAtTime(filterFloor, t + dur);
        mixer.connect(filter); filter.connect(this.master);
        const nodes = [mixer, filter];
        partials.forEach(p => {
            const osc = this.ctx.createOscillator(); osc.type = p.type;
            const bendFreq = freq * p.ratio * 1.009;
            osc.frequency.setValueAtTime(bendFreq, t);
            osc.frequency.exponentialRampToValueAtTime(freq * p.ratio, t + 0.03);
            const g = this.ctx.createGain();
            const peakVol = vol * p.amp;
            g.gain.setValueAtTime(0, t);
            g.gain.linearRampToValueAtTime(peakVol, t + 0.003);
            g.gain.exponentialRampToValueAtTime(peakVol * 0.45, t + 0.07);
            g.gain.exponentialRampToValueAtTime(0.001, t + dur * p.decayMul);
            osc.connect(g); g.connect(mixer);
            const stopTime = dur * p.decayMul + 0.1;
            osc.start(t); osc.stop(t + stopTime);
            nodes.push(osc, g);
        });
        const bloomFreq = freq * 1.5;
        const bloom = this.ctx.createOscillator(); bloom.type = 'sine'; bloom.frequency.value = bloomFreq;
        const bloomEnv = this.ctx.createGain();
        const bloomPeak = vol * 0.08;
        bloomEnv.gain.setValueAtTime(0, t);
        bloomEnv.gain.setValueAtTime(0, t + 0.04);
        bloomEnv.gain.linearRampToValueAtTime(bloomPeak, t + 0.12);
        bloomEnv.gain.setValueAtTime(bloomPeak, t + 0.25);
        bloomEnv.gain.exponentialRampToValueAtTime(0.001, t + dur * 0.7);
        bloom.connect(bloomEnv); bloomEnv.connect(mixer);
        bloom.start(t); bloom.stop(t + dur * 0.7 + 0.1);
        nodes.push(bloom, bloomEnv);
        this._scheduleCleanup(nodes, dur + 0.15);
    }

    shockwaveSound(strength) {
        if (!this._canPlay() || !this.beatOn) return;
        const t = this.ctx.currentTime;
        const vol = Math.min(0.38, 0.14 + strength * 0.24);
        const baseSemi = snapToPentatonic(Math.round(strength * 5) - 12);
        const bodyFreq = 65.41 * Math.pow(2, baseSemi / 12);
        const thud = this.ctx.createOscillator(); thud.type = 'sine';
        thud.frequency.setValueAtTime(bodyFreq * 1.3, t);
        thud.frequency.exponentialRampToValueAtTime(bodyFreq * 0.4, t + 0.22);
        const thudEnv = this.ctx.createGain();
        thudEnv.gain.setValueAtTime(vol, t);
        thudEnv.gain.linearRampToValueAtTime(vol * 0.6, t + 0.015);
        thudEnv.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
        thud.connect(thudEnv).connect(this.master);
        thud.start(t); thud.stop(t + 0.35);
        const bufSize = Math.floor(this.ctx.sampleRate * 0.1);
        const buf = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const ch = buf.getChannelData(0);
        for (let i = 0; i < bufSize; i++) ch[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufSize * 0.12));
        const noise = this.ctx.createBufferSource(); noise.buffer = buf;
        const nEnv = this.ctx.createGain();
        nEnv.gain.setValueAtTime(vol * 0.14, t);
        nEnv.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
        const nFilt = this.ctx.createBiquadFilter();
        nFilt.type = 'lowpass'; nFilt.frequency.value = 450;
        noise.connect(nFilt).connect(nEnv).connect(this.master);
        noise.start(t); noise.stop(t + 0.15);
        this._scheduleCleanup([thud, thudEnv, noise, nEnv, nFilt], 0.35);
    }

    crystalShatter(index, total) {
        if (!this.ready || !this.ctx || this.ctx.state !== 'running') return;
        const t = this.ctx.currentTime;
        const progress = index / Math.max(1, total - 1);
        const scale = [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24];
        const noteIdx = Math.min(scale.length - 1, Math.floor(progress * scale.length));
        const baseNote = scale[noteIdx];
        const freq = 261.63 * Math.pow(2, baseNote / 12);
        const vol = 0.30 + progress * 0.10;
        const allNodes = [];

        const crackLen = Math.floor(this.ctx.sampleRate * 0.006);
        const crackBuf = this.ctx.createBuffer(1, crackLen, this.ctx.sampleRate);
        const cd = crackBuf.getChannelData(0);
        for (let i = 0; i < crackLen; i++) cd[i] = (Math.random() * 2 - 1) * Math.exp(-i / (crackLen * 0.08));
        const crackSrc = this.ctx.createBufferSource(); crackSrc.buffer = crackBuf;
        const cFilt = this.ctx.createBiquadFilter(); cFilt.type = 'highpass';
        cFilt.frequency.value = 3000 + progress * 2500; cFilt.Q.value = 0.6;
        const cGain = this.ctx.createGain(); cGain.gain.value = vol * 1.6;
        crackSrc.connect(cFilt).connect(cGain).connect(this.master);
        crackSrc.start(t); crackSrc.stop(t + 0.01);
        allNodes.push(crackSrc, cFilt, cGain);

        const partials = [
            { ratio: 1,    gain: 0.38, dur: 0.08, type: 'triangle' },
            { ratio: 2.76, gain: 0.16, dur: 0.05, type: 'sine' },
            { ratio: 5.4,  gain: 0.08, dur: 0.03, type: 'sine' },
        ];
        partials.forEach(p => {
            const osc = this.ctx.createOscillator(); osc.type = p.type; osc.frequency.value = freq * p.ratio;
            const env = this.ctx.createGain();
            env.gain.setValueAtTime(vol * p.gain, t);
            env.gain.exponentialRampToValueAtTime(0.001, t + p.dur);
            osc.connect(env).connect(this.master);
            osc.start(t); osc.stop(t + p.dur + 0.01);
            allNodes.push(osc, env);
        });

        const thud = this.ctx.createOscillator(); thud.type = 'sine';
        thud.frequency.setValueAtTime(freq * 0.5, t);
        thud.frequency.exponentialRampToValueAtTime(40, t + 0.035);
        const thudEnv = this.ctx.createGain();
        thudEnv.gain.setValueAtTime(vol * 0.35, t);
        thudEnv.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
        thud.connect(thudEnv).connect(this.master);
        thud.start(t); thud.stop(t + 0.05);
        allNodes.push(thud, thudEnv);

        const fragCount = 10 + Math.floor(progress * 3);
        const fragMultipliers = [6.2, 5.1, 4.3, 3.7, 3.1, 2.6, 2.2, 1.9];
        for (let i = 0; i < fragCount; i++) {
            const delay = 0.005 + Math.pow(i / fragCount, 1.8) * 0.38;
            const baseMulti = fragMultipliers[i % fragMultipliers.length];
            const fFreq = freq * baseMulti * (0.93 + Math.random() * 0.14);
            const fOsc = this.ctx.createOscillator(); fOsc.type = 'sine'; fOsc.frequency.value = fFreq;
            const fEnv = this.ctx.createGain();
            const fVol = vol * (0.14 - i * 0.007) * (1 + progress * 0.3);
            fEnv.gain.setValueAtTime(0, t + delay);
            fEnv.gain.linearRampToValueAtTime(Math.max(0.003, fVol), t + delay + 0.001);
            fEnv.gain.exponentialRampToValueAtTime(0.001, t + delay + 0.022);
            fOsc.connect(fEnv).connect(this.master);
            fOsc.start(t + delay); fOsc.stop(t + delay + 0.030);
            allNodes.push(fOsc, fEnv);
        }

        const dustCount = 4 + (progress > 0.5 ? 1 : 0);
        for (let i = 0; i < dustCount; i++) {
            const delay = 0.025 + i * 0.055;
            const dFreq = freq * (8 + i * 1.8);
            const dOsc = this.ctx.createOscillator(); dOsc.type = 'sine'; dOsc.frequency.value = dFreq;
            const dEnv = this.ctx.createGain();
            dEnv.gain.setValueAtTime(0, t + delay);
            dEnv.gain.linearRampToValueAtTime(vol * 0.032, t + delay + 0.001);
            dEnv.gain.exponentialRampToValueAtTime(0.001, t + delay + 0.09);
            dOsc.connect(dEnv).connect(this.master);
            dOsc.start(t + delay); dOsc.stop(t + delay + 0.10);
            allNodes.push(dOsc, dEnv);
        }

        setTimeout(() => {
            allNodes.forEach(n => { try { n.disconnect(); } catch(e) {} });
        }, 700);
    }

    crystalsClear() {
        if (!this.ready || !this.ctx || this.ctx.state !== 'running') return;
        const t = this.ctx.currentTime;
        const allNodes = [];
        const ROOT = 261.63;

        const crackLen = Math.floor(this.ctx.sampleRate * 0.006);
        const crackBuf = this.ctx.createBuffer(1, crackLen, this.ctx.sampleRate);
        const cd = crackBuf.getChannelData(0);
        for (let i = 0; i < crackLen; i++) cd[i] = (Math.random() * 2 - 1) * Math.exp(-i / (crackLen * 0.06));
        const crackSrc = this.ctx.createBufferSource(); crackSrc.buffer = crackBuf;
        const cFilt = this.ctx.createBiquadFilter(); cFilt.type = 'highpass';
        cFilt.frequency.value = 5500; cFilt.Q.value = 0.5;
        const cGain = this.ctx.createGain(); cGain.gain.value = 0.14;
        crackSrc.connect(cFilt).connect(cGain).connect(this.master);
        crackSrc.start(t); crackSrc.stop(t + 0.008);
        allNodes.push(crackSrc, cFilt, cGain);

        [0, 3, 5, 7, 10, 12].forEach((semis, i) => {
            const delay = i * 0.068;
            const freq  = ROOT * Math.pow(2, semis / 12);
            const decay = 0.32 - i * 0.008;
            const osc = this.ctx.createOscillator(); osc.type = 'sine';
            osc.frequency.value = freq;
            const env = this.ctx.createGain();
            env.gain.setValueAtTime(0, t + delay);
            env.gain.linearRampToValueAtTime(0.10 + i * 0.008, t + delay + 0.004);
            env.gain.exponentialRampToValueAtTime(0.001, t + delay + decay);
            osc.connect(env).connect(this.master);
            osc.start(t + delay); osc.stop(t + delay + decay + 0.01);
            allNodes.push(osc, env);
            [3.1, 5.4, 7.8].forEach((mult, j) => {
                const sDelay = delay + 0.002 + j * 0.006;
                const sFreq  = freq * mult * (0.97 + Math.random() * 0.06);
                const sDur   = 0.055 + j * 0.018;
                const sOsc = this.ctx.createOscillator(); sOsc.type = 'sine'; sOsc.frequency.value = sFreq;
                const sEnv = this.ctx.createGain();
                sEnv.gain.setValueAtTime(0, t + sDelay);
                sEnv.gain.linearRampToValueAtTime(0.020 - j * 0.004, t + sDelay + 0.001);
                sEnv.gain.exponentialRampToValueAtTime(0.001, t + sDelay + sDur);
                sOsc.connect(sEnv).connect(this.master);
                sOsc.start(t + sDelay); sOsc.stop(t + sDelay + sDur + 0.005);
                allNodes.push(sOsc, sEnv);
            });
        });

        const SSCALE = [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24];
        for (let i = 0; i < 28; i++) {
            const delay  = 0.05 + Math.pow(i / 27, 1.4) * 0.85;
            const semis  = SSCALE[i % SSCALE.length];
            const octave = Math.floor(i / SSCALE.length);
            const freq   = ROOT * Math.pow(2, (semis + octave * 12) / 12);
            const dur    = 0.08 + Math.random() * 0.10;
            const gVol   = 0.024 * Math.max(0.3, 1 - i * 0.022);
            const dOsc = this.ctx.createOscillator(); dOsc.type = 'sine'; dOsc.frequency.value = freq;
            const dEnv = this.ctx.createGain();
            dEnv.gain.setValueAtTime(0, t + delay);
            dEnv.gain.linearRampToValueAtTime(gVol, t + delay + 0.001);
            dEnv.gain.exponentialRampToValueAtTime(0.001, t + delay + dur);
            dOsc.connect(dEnv).connect(this.master);
            dOsc.start(t + delay); dOsc.stop(t + delay + dur + 0.005);
            allNodes.push(dOsc, dEnv);
        }

        setTimeout(() => {
            allNodes.forEach(n => { try { n.disconnect(); } catch(e) {} });
        }, Math.ceil(1.05 * 1000 + 150));
    }

    success() { [0, 3, 7, 10].forEach((n, i) => setTimeout(() => this.tone(n, 0.5, 0.14), i * 80)); }

    fail() {
        if (!this.ready || !this.ctx || this.ctx.state !== 'running') return;
        const t = this.ctx.currentTime;
        this.tone(2, 0.20, 0.13);
        setTimeout(() => this.tone(-2, 0.26, 0.11), 130);
        const osc = this.ctx.createOscillator(); osc.type = 'sine';
        osc.frequency.setValueAtTime(90, t);
        osc.frequency.exponentialRampToValueAtTime(38, t + 0.22);
        const env = this.ctx.createGain();
        env.gain.setValueAtTime(0, t);
        env.gain.linearRampToValueAtTime(0.09, t + 0.008);
        env.gain.exponentialRampToValueAtTime(0.001, t + 0.28);
        osc.connect(env); env.connect(this.master);
        osc.start(t); osc.stop(t + 0.32);
        this._scheduleCleanup([osc, env], 0.32);
    }

    countClick(accent = false) {
        if (!this._canPlay() || !this.beatOn) return;
        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator(); osc.type = 'triangle'; osc.frequency.setValueAtTime(accent ? 1200 : 900, t); osc.frequency.exponentialRampToValueAtTime(accent ? 800 : 600, t + 0.03);
        const env = this.ctx.createGain(); env.gain.setValueAtTime(accent ? 0.4 : 0.25, t); env.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
        const filter = this.ctx.createBiquadFilter(); filter.type = 'bandpass'; filter.frequency.value = 1000; filter.Q.value = 2;
        osc.connect(filter); filter.connect(env); env.connect(this.master); osc.start(t); osc.stop(t + 0.1);
        this._scheduleCleanup([osc, env, filter], 0.1);
    }
}

// ═══════════════════════════════════════
//  PARTICLE CLASSES
// ═══════════════════════════════════════
class Mote {
    constructor(w, h) { this.w = w; this.h = h; this.reset(true); }
    reset(init = false) { this.x = Math.random() * this.w; this.y = init ? Math.random() * this.h : this.h + 10; this.size = 0.5 + Math.random() * 1.5; this.speed = 0.1 + Math.random() * 0.25; this.drift = (Math.random() - 0.5) * 0.2; this.alpha = 0.03 + Math.random() * 0.08; this.phase = Math.random() * Math.PI * 2; }
    update() { this.y -= this.speed; this.x += this.drift + Math.sin(this.phase) * 0.1; this.phase += 0.008; if (this.y < -10) this.reset(); }
    draw(ctx) { const a = this.alpha * (0.6 + Math.sin(this.phase * 2) * 0.4); ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2); ctx.fillStyle = `rgba(255,255,255,${a})`; ctx.fill(); }
}

class Burst {
    constructor(x, y, color) { this.x = x; this.y = y; this.color = color; const angle = Math.random() * Math.PI * 2, speed = 1 + Math.random() * 3; this.vx = Math.cos(angle) * speed; this.vy = Math.sin(angle) * speed; this.life = 1; this.size = 2 + Math.random() * 3; }
    update() { this.x += this.vx; this.y += this.vy; this.vx *= 0.96; this.vy *= 0.96; this.life -= 0.025; }
    draw(ctx) { if (this.life <= 0) return; const rgb = hexToRgb(this.color); ctx.beginPath(); ctx.arc(this.x, this.y, this.size * this.life, 0, Math.PI * 2); ctx.fillStyle = `rgba(${rgb.r},${rgb.g},${rgb.b},${this.life * 0.5})`; ctx.fill(); }
}

class CrystalShard {
    constructor(x, y, palette, baseSize) {
        this.x = x; this.y = y;
        const shardPal = SHARD_COLORS[Math.floor(Math.random() * SHARD_COLORS.length)];
        this.color = shardPal.main; this.lightColor = shardPal.light;
        const numVerts = 3 + Math.floor(Math.random() * 2);
        const size = baseSize * (0.25 + Math.random() * 0.5);
        this.verts = [];
        const startAngle = Math.random() * Math.PI * 2;
        for (let i = 0; i < numVerts; i++) {
            const a = startAngle + (i / numVerts) * Math.PI * 2 + (Math.random() - 0.5) * 0.6;
            const r = size * (0.4 + Math.random() * 0.6);
            this.verts.push({ x: Math.cos(a) * r, y: Math.sin(a) * r });
        }
        const angle = Math.random() * Math.PI * 2;
        const speed = 3 + Math.random() * 7;
        this.vx = Math.cos(angle) * speed; this.vy = Math.sin(angle) * speed;
        this.rotation = Math.random() * Math.PI * 2;
        this.angVel = (Math.random() - 0.5) * 0.35;
        this.gravity = 0.08 + Math.random() * 0.06;
        this.life = 1; this.decay = 0.012 + Math.random() * 0.01;
        this.hasHighlight = Math.random() > 0.4;
    }
    update() {
        this.x += this.vx; this.y += this.vy; this.vy += this.gravity;
        this.vx *= 0.985; this.vy *= 0.985;
        this.rotation += this.angVel; this.angVel *= 0.995; this.life -= this.decay;
    }
    draw(ctx) {
        if (this.life <= 0) return;
        const a = this.life;
        const rgb = hexToRgb(this.color); const lrgb = hexToRgb(this.lightColor);
        ctx.save(); ctx.translate(this.x, this.y); ctx.rotate(this.rotation); ctx.globalAlpha = a;
        ctx.beginPath();
        this.verts.forEach((v, i) => i === 0 ? ctx.moveTo(v.x, v.y) : ctx.lineTo(v.x, v.y));
        ctx.closePath();
        const g = ctx.createLinearGradient(this.verts[0].x, this.verts[0].y, this.verts[1].x, this.verts[1].y);
        g.addColorStop(0, `rgba(${lrgb.r},${lrgb.g},${lrgb.b},${a * 0.9})`);
        g.addColorStop(0.5, `rgba(${rgb.r},${rgb.g},${rgb.b},${a * 0.7})`);
        g.addColorStop(1, `rgba(${rgb.r*0.6|0},${rgb.g*0.6|0},${rgb.b*0.6|0},${a * 0.5})`);
        ctx.fillStyle = g; ctx.fill();
        if (this.hasHighlight) { ctx.strokeStyle = `rgba(255,255,255,${a * 0.6})`; ctx.lineWidth = 1; ctx.stroke(); }
        if (this.verts.length >= 3) {
            ctx.beginPath();
            ctx.moveTo(this.verts[0].x * 0.3, this.verts[0].y * 0.3);
            ctx.lineTo(this.verts[1].x * 0.8, this.verts[1].y * 0.8);
            ctx.strokeStyle = `rgba(255,255,255,${a * 0.25})`; ctx.lineWidth = 0.5; ctx.stroke();
        }
        ctx.globalAlpha = 1; ctx.restore();
    }
}

class EnergyMote {
    constructor(x, y) {
        this.x = x; this.y = y;
        this.warmColor = WARM_RELEASE[Math.floor(Math.random() * WARM_RELEASE.length)];
        const angle = Math.random() * Math.PI * 2;
        const speed = 0.8 + Math.random() * 2.5;
        this.vx = Math.cos(angle) * speed; this.vy = Math.sin(angle) * speed - 0.8;
        this.life = 1; this.size = 2 + Math.random() * 4;
        this.decay = 0.01 + Math.random() * 0.008; this.phase = Math.random() * Math.PI * 2;
    }
    update() {
        this.x += this.vx; this.y += this.vy; this.vy -= 0.03;
        this.vx *= 0.98; this.vy *= 0.985; this.life -= this.decay; this.phase += 0.1;
    }
    draw(ctx) {
        if (this.life <= 0) return;
        const rgb = hexToRgb(this.warmColor); const a = this.life * 0.8;
        const r = this.size * (0.5 + this.life * 0.5);
        const wobble = Math.sin(this.phase) * r * 0.15;
        ctx.beginPath(); ctx.arc(this.x + wobble, this.y, r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${rgb.r},${rgb.g},${rgb.b},${a * 0.7})`; ctx.fill();
        ctx.beginPath(); ctx.arc(this.x + wobble, this.y, r * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${a * 0.8})`; ctx.fill();
    }
}

class CrystalDustP {
    constructor(x, y, palette) {
        this.x = x + (Math.random() - 0.5) * 20; this.y = y + (Math.random() - 0.5) * 20;
        const dustPal = SHARD_COLORS[Math.floor(Math.random() * SHARD_COLORS.length)];
        this.color = Math.random() > 0.5 ? dustPal.light : dustPal.main;
        const angle = Math.random() * Math.PI * 2;
        const speed = 0.3 + Math.random() * 1.2;
        this.vx = Math.cos(angle) * speed; this.vy = Math.sin(angle) * speed - 0.3;
        this.life = 1; this.size = 0.5 + Math.random() * 1.5;
        this.decay = 0.008 + Math.random() * 0.006;
        this.twinkleSpeed = 3 + Math.random() * 5; this.twinklePhase = Math.random() * Math.PI * 2;
    }
    update() {
        this.x += this.vx; this.y += this.vy; this.vy -= 0.008;
        this.vx *= 0.995; this.life -= this.decay; this.twinklePhase += this.twinkleSpeed * 0.016;
    }
    draw(ctx) {
        if (this.life <= 0) return;
        const twinkle = 0.3 + Math.sin(this.twinklePhase) * 0.7;
        const a = this.life * twinkle; const rgb = hexToRgb(this.color); const r = this.size * this.life;
        ctx.beginPath(); ctx.arc(this.x, this.y, r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${rgb.r},${rgb.g},${rgb.b},${a})`; ctx.fill();
        if (twinkle > 0.7 && r > 0.5) {
            const sparkR = r * 3;
            ctx.beginPath(); ctx.moveTo(this.x - sparkR, this.y); ctx.lineTo(this.x + sparkR, this.y);
            ctx.strokeStyle = `rgba(255,255,255,${a * 0.3})`; ctx.lineWidth = 0.5; ctx.stroke();
            ctx.beginPath(); ctx.moveTo(this.x, this.y - sparkR); ctx.lineTo(this.x, this.y + sparkR); ctx.stroke();
        }
    }
}

// ═══════════════════════════════════════════════════════════════
//  DRAW CRYSTAL
// ═══════════════════════════════════════════════════════════════
function drawCrystal(target, now) {
    const palette = CRYSTAL_PALETTE[target.id % CRYSTAL_PALETTE.length];
    const lrgb = hexToRgb(palette.light);
    const drgb = hexToRgb(palette.dark);
    const SPECTRAL = ['#FF2840', '#FF7820', '#F5D200', '#28C858', '#18C8E0', '#A020E0'];

    if (!target.alive) {
        if (target.destroyTime && now - target.destroyTime < 600) {
            const age = now - target.destroyTime; const p = age / 600;
            const px = (target.x / 100) * canvasW; const py = (target.y / 100) * canvasH;
            const baseR = 18 * orbScale;
            const ringR = baseR * (1 + p * 4); const ringA = Math.pow(1 - p, 2.5) * 0.55;
            ctx.beginPath(); ctx.arc(px, py, ringR, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(255,255,255,${ringA})`;
            ctx.lineWidth = 2.5 * (1 - p); ctx.stroke();
            if (p < 0.4) {
                const fa = (1 - p / 0.4) * 0.4;
                const fg = ctx.createRadialGradient(px, py, 0, px, py, baseR * (2 + p * 3));
                fg.addColorStop(0, `rgba(255,255,255,${fa})`);
                fg.addColorStop(0.4, `rgba(210,235,255,${fa * 0.5})`);
                fg.addColorStop(1, `rgba(255,255,255,0)`);
                ctx.fillStyle = fg; ctx.beginPath(); ctx.arc(px, py, baseR * (2 + p * 3), 0, Math.PI * 2); ctx.fill();
            }
        }
        return;
    }

    const px = (target.x / 100) * canvasW; const py = (target.y / 100) * canvasH;
    const T = now / 1000; const baseR = 18 * orbScale;
    const breathe = 1 + Math.sin(T * 1.5 + target.id * 1.7) * 0.05;
    const R = baseR * breathe;
    const aliveCount = state.targets.filter(t => t.alive).length;
    const urgency = 1 - (aliveCount - 1) / Math.max(1, state.totalTargets - 1);
    const tremor = urgency * Math.sin(T * 15 + target.id * 4.3) * 1.2 * orbScale;
    const cx = px + tremor; const cy = py;
    const rot = T * 0.15 + target.id * 1.1;
    const numSides = 6;

    const getVertex = (i, r) => {
        const a = rot + (i / numSides) * Math.PI * 2 - Math.PI / 2;
        return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
    };

    const glowR = R * 4.5;
    const glow = ctx.createRadialGradient(cx, cy, R * 0.3, cx, cy, glowR);
    glow.addColorStop(0, `rgba(220,235,255,${0.14 + urgency * 0.08})`);
    glow.addColorStop(0.3, `rgba(200,220,255,${0.05 + urgency * 0.04})`);
    glow.addColorStop(1, `rgba(180,210,255,0)`);
    ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(cx, cy, glowR, 0, Math.PI * 2); ctx.fill();

    for (let i = 0; i < numSides; i++) {
        const v1 = getVertex(i, R * 1.12);
        const v2 = getVertex(i + 1, R * 1.12);
        const hue = ((i / numSides) * 360 + T * 18 + target.id * 60) % 360;
        ctx.beginPath(); ctx.moveTo(v1.x, v1.y); ctx.lineTo(v2.x, v2.y);
        ctx.strokeStyle = `hsla(${hue},100%,70%,${0.20 + urgency * 0.15})`;
        ctx.lineWidth = 1.4; ctx.stroke();
    }

    for (let i = 0; i < numSides; i++) {
        const v1 = getVertex(i, R * 1.1); const v2 = getVertex(i + 1, R * 1.1);
        const facetAngle = rot + ((i + 0.5) / numSides) * Math.PI * 2 - Math.PI / 2;
        const lightDot = Math.cos(facetAngle + 0.5) * 0.5 + 0.5;
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(v1.x, v1.y); ctx.lineTo(v2.x, v2.y); ctx.closePath();
        const facetGrad = ctx.createLinearGradient(cx, cy, (v1.x + v2.x) / 2, (v1.y + v2.y) / 2);
        const bodyA = 0.45 + urgency * 0.15;
        facetGrad.addColorStop(0, `rgba(255,255,255,${bodyA * (0.6 + lightDot * 0.4)})`);
        facetGrad.addColorStop(0.5, `rgba(${lrgb.r},${lrgb.g},${lrgb.b},${bodyA * (0.4 + lightDot * 0.3)})`);
        facetGrad.addColorStop(1, `rgba(${drgb.r},${drgb.g},${drgb.b},${bodyA * (0.15 + lightDot * 0.2)})`);
        ctx.fillStyle = facetGrad; ctx.fill();
    }

    ctx.beginPath();
    for (let i = 0; i <= numSides; i++) { const v = getVertex(i, R * 1.1); i === 0 ? ctx.moveTo(v.x, v.y) : ctx.lineTo(v.x, v.y); }
    ctx.closePath();
    ctx.strokeStyle = `rgba(255,255,255,${0.75 + urgency * 0.22})`;
    ctx.lineWidth = 1.5; ctx.stroke();

    for (let i = 0; i < numSides; i++) {
        const v = getVertex(i, R * 1.1);
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(v.x, v.y);
        ctx.strokeStyle = `rgba(200,220,255,${0.13 + urgency * 0.08})`;
        ctx.lineWidth = 0.8; ctx.stroke();
    }

    const tensionPulse = 1 + Math.sin(T * (2.5 + urgency * 4) + target.id * 2) * (0.15 + urgency * 0.2);
    const tensionR = R * 0.5 * tensionPulse; const tensionA = 0.18 + urgency * 0.28;
    const tGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, tensionR * 2);
    tGrad.addColorStop(0, `rgba(255,240,200,${tensionA * 0.9})`);
    tGrad.addColorStop(0.3, `rgba(255,200,140,${tensionA * 0.5})`);
    tGrad.addColorStop(0.6, `rgba(255,140,80,${tensionA * 0.18})`);
    tGrad.addColorStop(1, `rgba(255,80,40,0)`);
    ctx.fillStyle = tGrad; ctx.beginPath(); ctx.arc(cx, cy, tensionR * 2, 0, Math.PI * 2); ctx.fill();

    const coreR = R * 0.2; const corePulse = 1 + Math.sin(T * 3.5 + target.id * 2.5) * 0.12;
    const coreGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, coreR * corePulse * 2.5);
    coreGrad.addColorStop(0, `rgba(255,255,255,${0.95 + urgency * 0.05})`);
    coreGrad.addColorStop(0.2, `rgba(240,248,255,0.75)`);
    coreGrad.addColorStop(0.5, `rgba(210,230,255,0.28)`);
    coreGrad.addColorStop(1, `rgba(180,210,255,0)`);
    ctx.fillStyle = coreGrad; ctx.beginPath(); ctx.arc(cx, cy, coreR * corePulse * 2.5, 0, Math.PI * 2); ctx.fill();

    for (let i = 0; i < numSides; i++) {
        const v = getVertex(i, R * 1.15);
        const sparkle = Math.sin(T * 4 + i * 1.8 + target.id) * 0.5 + 0.5;
        if (sparkle > 0.55) {
            const sa = (sparkle - 0.55) * 2.2 * 0.65;
            const sr = 2.8 * orbScale;
            const specRgb = hexToRgb(SPECTRAL[i % SPECTRAL.length]);
            ctx.beginPath(); ctx.moveTo(v.x - sr * 2.5, v.y); ctx.lineTo(v.x + sr * 2.5, v.y);
            ctx.strokeStyle = `rgba(${specRgb.r},${specRgb.g},${specRgb.b},${sa * 0.85})`;
            ctx.lineWidth = 0.9; ctx.stroke();
            ctx.beginPath(); ctx.moveTo(v.x, v.y - sr * 2.5); ctx.lineTo(v.x, v.y + sr * 2.5); ctx.stroke();
            ctx.beginPath(); ctx.arc(v.x, v.y, sr * 0.65, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255,255,255,${sa})`; ctx.fill();
            const bloom = ctx.createRadialGradient(v.x, v.y, 0, v.x, v.y, sr * 3.5);
            bloom.addColorStop(0, `rgba(255,255,255,${sa * 0.8})`);
            bloom.addColorStop(0.35, `rgba(${specRgb.r},${specRgb.g},${specRgb.b},${sa * 0.35})`);
            bloom.addColorStop(1, `rgba(${specRgb.r},${specRgb.g},${specRgb.b},0)`);
            ctx.fillStyle = bloom; ctx.beginPath(); ctx.arc(v.x, v.y, sr * 3.5, 0, Math.PI * 2); ctx.fill();
        }
    }

    for (let i = 0; i < 3; i++) {
        const angle = T * (0.4 + i * 0.15) + i * (Math.PI * 2 / 3) + target.id * 0.8;
        const orbit = R * 1.8;
        const mx = cx + Math.cos(angle) * orbit; const my = cy + Math.sin(angle) * orbit;
        const ma = 0.28 + Math.sin(T * 2.5 + i * 2) * 0.15; const ms = 1.4 * orbScale;
        const moteHue = ((i * 120 + T * 30 + target.id * 40) % 360);
        ctx.save(); ctx.translate(mx, my); ctx.rotate(T * 2 + i);
        ctx.beginPath();
        ctx.moveTo(0, -ms); ctx.lineTo(ms * 0.6, 0); ctx.lineTo(0, ms); ctx.lineTo(-ms * 0.6, 0);
        ctx.closePath();
        ctx.fillStyle = `hsla(${moteHue},100%,72%,${ma})`;
        ctx.fill(); ctx.restore();
    }
}

function drawCrystalConnections(now) {
    const alive = state.targets.filter(t => t.alive);
    if (alive.length < 2) return;
    const T = now / 1000;
    for (let i = 0; i < alive.length; i++) {
        for (let j = i + 1; j < alive.length; j++) {
            const a = alive[i], b = alive[j];
            const dist = Math.hypot(a.x - b.x, a.y - b.y);
            if (dist > 45) continue;
            const ax = (a.x / 100) * canvasW, ay = (a.y / 100) * canvasH;
            const bx = (b.x / 100) * canvasW, by = (b.y / 100) * canvasH;
            const alpha = 0.06 + Math.sin(T * 0.8 + i + j) * 0.025;
            ctx.beginPath(); ctx.moveTo(ax, ay);
            const midX = (ax + bx) / 2 + Math.sin(T * 2 + i * 3) * 3;
            const midY = (ay + by) / 2 + Math.cos(T * 2.5 + j * 2) * 3;
            ctx.lineTo(midX, midY); ctx.lineTo(bx, by);
            ctx.strokeStyle = `rgba(200,220,255,${alpha})`;
            ctx.lineWidth = 1; ctx.stroke();
        }
    }
}

// ═══════════════════════════════════════════════════════════════
//  DRAW ORB
// ═══════════════════════════════════════════════════════════════
function drawOrb(orb, now) {
    const p = toScreen(orb);
    const { brightness } = getBrightness(orb, now);
    const baseR = 40 * (orb.size || 1) * orbScale;
    const rgb = hexToRgb(orb.color);
    if (isNaN(p.x) || isNaN(p.y) || baseR <= 0) return;

    const spawnAge = orb.spawnTime ? (now - orb.spawnTime) : 1000;
    const spawnFade = Math.min(1, spawnAge / 600);
    const spawnEase = spawnFade < 0.5 ? 4*spawnFade*spawnFade*spawnFade : 1 - Math.pow(-2*spawnFade+2,3)/2;
    const b = brightness * spawnEase;
    const t = now / 1000, T = t + orb.id * 3.7;
    const breathe = 1 + Math.sin(T*0.5)*0.03 + Math.sin(T*0.9)*0.02;
    const sizeScale = 0.32 + b * 0.68;
    const R = baseR * sizeScale * breathe * spawnEase;
    if (R < 1) return;

    const hue = T*0.25 + b*2;
    const iR = Math.min(255, rgb.r + Math.sin(hue)*30      + b*50);
    const iG = Math.min(255, rgb.g + Math.sin(hue+2.1)*25  + b*30);
    const iB = Math.min(255, rgb.b + Math.sin(hue+4.2)*35  + b*20);
    const hR = Math.min(255, 100 + rgb.r*0.4  + b*155);
    const hG = Math.min(255, 110 + rgb.g*0.35 + b*145);
    const hB = Math.min(255, 130 + rgb.b*0.3  + b*125);
    const wR = Math.min(255, rgb.r*1.2+40), wG = Math.min(255, rgb.g*0.9+20), wB = Math.min(255, rgb.b*0.7);

    ctx.globalAlpha = spawnEase;

    const shockE = orb.shockEnergy || 0;
    if (shockE > 0.15 && spawnEase > 0.3) {
        const trailStrength = Math.min(1, shockE/2.5);
        const trailCount = Math.min(6, Math.ceil(shockE*2));
        const svx = (orb.shockVx||0)*(canvasW/100), svy = (orb.shockVy||0)*(canvasH/100);
        for (let i = 1; i <= trailCount; i++) {
            const frac = i/(trailCount+1);
            const tx = p.x-svx*i*2.5, ty = p.y-svy*i*2.5;
            const ta = trailStrength*(1-frac)*0.3*spawnEase, tr = R*(0.65-frac*0.12);
            if (tr > 1 && ta > 0.005) {
                const tg = ctx.createRadialGradient(tx,ty,0,tx,ty,tr);
                tg.addColorStop(0,   rgba(rgb.r,rgb.g,rgb.b, ta*0.9));
                tg.addColorStop(0.4, rgba(rgb.r,rgb.g,rgb.b, ta*0.35));
                tg.addColorStop(1,   rgba(rgb.r,rgb.g,rgb.b, 0));
                ctx.fillStyle=tg; ctx.beginPath(); ctx.arc(tx,ty,tr,0,Math.PI*2); ctx.fill();
            }
        }
    }
    if (orb.shockFlash && spawnEase > 0.3) {
        const flashAge = now - orb.shockFlash;
        if (flashAge < 280) {
            const fp = flashAge/280, fa = (1-fp*fp)*0.5*spawnEase, fr = R*(1.1+fp*0.5);
            const fg = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,fr);
            fg.addColorStop(0,    `rgba(255,255,255,${fa})`);
            fg.addColorStop(0.35, `rgba(255,255,255,${fa*0.35})`);
            fg.addColorStop(1,    'rgba(255,255,255,0)');
            ctx.fillStyle=fg; ctx.beginPath(); ctx.arc(p.x,p.y,fr,0,Math.PI*2); ctx.fill();
        }
    }

    const atmoR = baseR*(2.0+b*0.8);
    const ag = ctx.createRadialGradient(p.x,p.y,R*0.5,p.x,p.y,atmoR);
    ag.addColorStop(0,    rgba(iR,iG,iB,       0.12+b*0.25));
    ag.addColorStop(0.35, rgba(rgb.r,rgb.g,rgb.b, 0.06+b*0.14));
    ag.addColorStop(0.65, rgba(rgb.r,rgb.g,rgb.b, 0.02+b*0.06));
    ag.addColorStop(1,    rgba(rgb.r,rgb.g,rgb.b, 0));
    ctx.fillStyle=ag; ctx.beginPath(); ctx.arc(p.x,p.y,atmoR,0,Math.PI*2); ctx.fill();

    const coronaR = R*(1.15+b*0.1);
    const cg = ctx.createRadialGradient(p.x,p.y,R*0.85,p.x,p.y,coronaR);
    cg.addColorStop(0,   rgba(iR,iG,iB,       0));
    cg.addColorStop(0.4, rgba(iR,iG,iB,       0.15+b*0.35));
    cg.addColorStop(0.7, rgba(wR,wG,wB,       0.08+b*0.2));
    cg.addColorStop(1,   rgba(rgb.r,rgb.g,rgb.b, 0));
    ctx.fillStyle=cg; ctx.beginPath(); ctx.arc(p.x,p.y,coronaR,0,Math.PI*2); ctx.fill();

    _drawFrameCount++;
    let cached = _orbPathCache.get(orb.id);
    if (!cached || (_drawFrameCount - cached.stamp) >= _PATH_SKIP) {
        cached = { ..._buildOrbPaths(p, R, T, b), stamp: _drawFrameCount };
        _orbPathCache.set(orb.id, cached);
    }
    const { body, shells, core, edge, coreR, corePulse } = cached;

    const bdg = ctx.createRadialGradient(
        p.x+Math.sin(T*0.4)*R*0.12, p.y+Math.cos(T*0.35)*R*0.12, R*0.1, p.x,p.y,R);
    bdg.addColorStop(0,    rgba(hR,hG,hB,       0.35+b*0.45));
    bdg.addColorStop(0.25, rgba(iR,iG,iB,       0.25+b*0.35));
    bdg.addColorStop(0.5,  rgba(rgb.r,rgb.g,rgb.b, 0.15+b*0.25));
    bdg.addColorStop(0.75, rgba(rgb.r,rgb.g,rgb.b, 0.08+b*0.15));
    bdg.addColorStop(1,    rgba(rgb.r,rgb.g,rgb.b, 0.02+b*0.05));
    ctx.fillStyle=bdg; _tracePath(ctx,body); ctx.fill();

    for (let s = 0; s < 3; s++) {
        const sR = R*(0.75-s*0.15), sp = T*(0.6+s*0.2)+s*1.2, sa = (0.12+b*0.22)*(1-s*0.2);
        const sg = ctx.createRadialGradient(p.x+Math.cos(sp)*sR*0.2, p.y+Math.sin(sp)*sR*0.2, 0, p.x,p.y,sR);
        sg.addColorStop(0,   rgba(hR,hG,hB,       sa*1.3));
        sg.addColorStop(0.35,rgba(iR,iG,iB,       sa*0.9));
        sg.addColorStop(0.7, rgba(rgb.r,rgb.g,rgb.b, sa*0.4));
        sg.addColorStop(1,   rgba(rgb.r,rgb.g,rgb.b, 0));
        ctx.fillStyle=sg; _tracePath(ctx,shells[s]); ctx.fill();
    }

    const coreAlpha = 0.4+b*0.55;
    const chg = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,coreR*2.5*corePulse);
    chg.addColorStop(0,    rgba(255,255,255,     coreAlpha*0.8));
    chg.addColorStop(0.15, rgba(hR,hG,hB,        coreAlpha*0.65));
    chg.addColorStop(0.4,  rgba(iR,iG,iB,        coreAlpha*0.35));
    chg.addColorStop(0.7,  rgba(rgb.r,rgb.g,rgb.b, coreAlpha*0.12));
    chg.addColorStop(1,    rgba(rgb.r,rgb.g,rgb.b, 0));
    ctx.fillStyle=chg; ctx.beginPath(); ctx.arc(p.x,p.y,coreR*2.5*corePulse,0,Math.PI*2); ctx.fill();

    const crg = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,coreR*corePulse);
    crg.addColorStop(0,   rgba(255,255,255,     coreAlpha));
    crg.addColorStop(0.3, rgba(hR,hG,hB,        coreAlpha*0.85));
    crg.addColorStop(0.6, rgba(iR,iG,iB,        coreAlpha*0.5));
    crg.addColorStop(1,   rgba(rgb.r,rgb.g,rgb.b, 0));
    ctx.fillStyle=crg; _tracePath(ctx,core); ctx.fill();

    const numMotes = 10 + Math.floor(b * 16);
    for (let i = 0; i < numMotes; i++) {
        const golden = i*2.39996323, moteOrbit = R*(0.2+(i/numMotes)*0.7);
        const motePhase = T*(0.15+(i%7)*0.06)+golden, wobble = Math.sin(T*1.5+i*0.9)*4;
        const mx = p.x+Math.cos(motePhase)*moteOrbit+Math.cos(motePhase+1.57)*wobble;
        const my = p.y+Math.sin(motePhase)*moteOrbit+Math.sin(motePhase+1.57)*wobble;
        const moteSize  = (0.8+b*1.8)*(0.5+Math.sin(T*4+i*2)*0.4);
        const moteAlpha = (0.25+b*0.55)*(0.5+Math.sin(T*3+i*1.5)*0.4);
        const mg = ctx.createRadialGradient(mx,my,0,mx,my,moteSize*2.5);
        mg.addColorStop(0,    rgba(255,255,255, moteAlpha));
        mg.addColorStop(0.35, rgba(hR,hG,hB,   moteAlpha*0.6));
        mg.addColorStop(0.7,  rgba(iR,iG,iB,   moteAlpha*0.25));
        mg.addColorStop(1,    rgba(rgb.r,rgb.g,rgb.b, 0));
        ctx.fillStyle=mg; ctx.beginPath(); ctx.arc(mx,my,moteSize*2.5,0,Math.PI*2); ctx.fill();
    }

    if (b > 0.08) {
        _tracePath(ctx, edge);
        ctx.strokeStyle=rgba(iR,iG,iB, (b-0.08)*0.4); ctx.lineWidth=1+b*0.8; ctx.stroke();
    }

    if (b > 0.55) {
        const peak = (b-0.55)/0.45, peakPulse = 0.65+Math.sin(T*9)*0.35;
        const bloomR = R*(1.4+peak*0.4);
        const blg = ctx.createRadialGradient(p.x,p.y,R*0.3,p.x,p.y,bloomR);
        blg.addColorStop(0,   rgba(hR,hG,hB,       peak*0.4*peakPulse));
        blg.addColorStop(0.3, rgba(iR,iG,iB,       peak*0.25*peakPulse));
        blg.addColorStop(0.6, rgba(rgb.r,rgb.g,rgb.b, peak*0.12*peakPulse));
        blg.addColorStop(1,   rgba(rgb.r,rgb.g,rgb.b, 0));
        ctx.fillStyle=blg; ctx.beginPath(); ctx.arc(p.x,p.y,bloomR,0,Math.PI*2); ctx.fill();

        {
            for (let ring = 0; ring < 3; ring++) {
                const ringR = R*(1.03+peak*(0.06+ring*0.045)), rp = Math.sin(T*7+ring*2.1)*0.5+0.5;
                ctx.beginPath();
                for (let i = 0; i <= 48; i++) {
                    const a=(i/48)*Math.PI*2, w=Math.sin(a*5+T*5+ring)*0.025*peak, r=ringR*(1+w);
                    i===0 ? ctx.moveTo(p.x+Math.cos(a)*r,p.y+Math.sin(a)*r)
                           : ctx.lineTo(p.x+Math.cos(a)*r,p.y+Math.sin(a)*r);
                }
                ctx.closePath();
                ctx.strokeStyle=rgba(hR,hG,hB, peak*0.6*rp*(1-ring*0.25));
                ctx.lineWidth=2.5+peak*2-ring*0.6; ctx.stroke();
            }
            const burstCount = 8+Math.floor(peak*10);
            for (let i = 0; i < burstCount; i++) {
                const ba = T*1.2+i*(Math.PI*2/burstCount);
                const bd = R*(0.85+peak*0.3+Math.sin(T*5+i*2.3)*0.08);
                const bx = p.x+Math.cos(ba)*bd, by = p.y+Math.sin(ba)*bd;
                const bs = 2.5+peak*4, bA = peak*0.7*(0.5+Math.sin(T*8+i*2.7)*0.5);
                const bgg = ctx.createRadialGradient(bx,by,0,bx,by,bs*2);
                bgg.addColorStop(0,    rgba(255,255,255, bA));
                bgg.addColorStop(0.25, rgba(hR,hG,hB,   bA*0.7));
                bgg.addColorStop(0.6,  rgba(iR,iG,iB,   bA*0.3));
                bgg.addColorStop(1,    rgba(rgb.r,rgb.g,rgb.b, 0));
                ctx.fillStyle=bgg; ctx.beginPath(); ctx.arc(bx,by,bs*2,0,Math.PI*2); ctx.fill();
            }
            if (peak > 0.6) {
                const mp = (peak-0.6)/0.4, brillR = coreR*(2+mp);
                const brg = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,brillR);
                brg.addColorStop(0,   rgba(255,255,255, mp*0.7*peakPulse));
                brg.addColorStop(0.2, rgba(hR,hG,hB,   mp*0.5*peakPulse));
                brg.addColorStop(0.5, rgba(iR,iG,iB,   mp*0.25*peakPulse));
                brg.addColorStop(1,   rgba(rgb.r,rgb.g,rgb.b, 0));
                ctx.fillStyle=brg; ctx.beginPath(); ctx.arc(p.x,p.y,brillR,0,Math.PI*2); ctx.fill();
            }
        }
    }
    ctx.globalAlpha = 1;
}
