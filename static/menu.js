// ═══════════════════════════════════════════════════════════════════════════════
//  menu.js — Menu, Level Select, Achievements, Stats, Progress
//
//  Globals used from index.html (game script):
//    loadProgress, saveProgress, state, audio, loadLevel, startCountdown,
//    resetGameUI, $
//  Globals used from engine.js:
//    (none directly)
// ═══════════════════════════════════════════════════════════════════════════════

    // ═══════════════════════════════════════
    //  MENU
    // ═══════════════════════════════════════

    const ACHIEVEMENTS = [

        // ── STARTER ──────────────────────────────────────────────────────────
        { id: 'first_blood',     icon: '✦',  name: 'First Blood',      desc: 'Complete your first level',
          check: p => (p.highestLevel||0) >= 2 },
        { id: 'committed',       icon: '📅', name: 'Committed',         desc: 'Play on 3 different days',
          check: p => (p.daysPlayed||[]).length >= 3 },
        { id: 'dedicated',       icon: '⏱', name: 'Dedicated',         desc: 'Spend 30 minutes playing',
          check: p => (p.totalPlaySecs||0) >= 1800 },

        // ── STREAKS ───────────────────────────────────────────────────────────
        { id: 'hat_trick',       icon: '🔱', name: 'Hat Trick',         desc: 'Gold 3 levels in a row',
          check: p => (p.goldStreak||0) >= 3 },
        { id: 'golden_run',      icon: '👑', name: 'Golden Run',         desc: 'Gold 5 levels in a row',
          check: p => (p.goldStreak||0) >= 5 },
        { id: 'unstoppable',     icon: '🌊', name: 'Unstoppable',        desc: 'Gold 10 levels in a row',
          check: p => (p.goldStreak||0) >= 10 },
        { id: 'on_fire',         icon: '🔥', name: 'On Fire',            desc: 'Gold 3 levels in a single session',
          check: p => (p.sessionGolds||0) >= 3 },

        // ── SKILL ────────────────────────────────────────────────────────────
        { id: 'chain_reaction',  icon: '💥', name: 'Chain Reaction',     desc: 'Break 2 crystals with a single orb hit',
          check: p => !!(p.achFlags||{}).chainReaction },
        { id: 'clockwork',       icon: '🎯', name: 'Clockwork',           desc: 'Gold the same level 3 separate times',
          check: p => Object.values(p.goldPerLevel||{}).some(n => n >= 3) },
        { id: 'wrecking_ball',   icon: '⚡', name: 'Wrecking Ball',       desc: 'Break all crystals in under 8 seconds',
          check: p => !!(p.achFlags||{}).wreckingBall },
        { id: 'orbs_to_spare',   icon: '🌀', name: 'Orbs to Spare',       desc: 'Complete a level with 4 or more orbs unused',
          check: p => !!(p.achFlags||{}).orbsSpare },
        { id: 'last_crystal',    icon: '🎱', name: 'Last Crystal',        desc: 'Break the final crystal with your last orb',
          check: p => !!(p.achFlags||{}).lastCrystal },

        // ── COMPLETIONIST ────────────────────────────────────────────────────
        { id: 'cartographer',    icon: '🗺️', name: 'Cartographer',       desc: 'Complete all 50 levels',
          check: p => (p.highestLevel||0) >= 50 },
        { id: 'bronze_age',      icon: '🥉', name: 'Bronze Age',          desc: 'Bronze or better on every level',
          check: p => {
              const tiers = p.bestTiers || {};
              return Array.from({length:50},(_,i)=>i+1).every(n => tiers[n] && tiers[n] !== 'none');
          }},
        { id: 'silver_lining',   icon: '🥈', name: 'Silver Lining',       desc: 'Silver or better on every level',
          check: p => {
              const tiers = p.bestTiers || {};
              return Array.from({length:50},(_,i)=>i+1).every(n => tiers[n] === 'silver' || tiers[n] === 'gold');
          }},
        { id: 'all_that_glitters', icon: '🥇', name: 'All That Glitters', desc: 'Gold on every single level',
          check: p => {
              const tiers = p.bestTiers || {};
              return Array.from({length:50},(_,i)=>i+1).every(n => tiers[n] === 'gold');
          }},

        // ── GOLD QUANTITY ────────────────────────────────────────────────────
        { id: 'golden_touch',    icon: '✨', name: 'Golden Touch',        desc: 'Earn 10 gold medals',
          check: p => (p.totalGolds||0) >= 10 },
        { id: 'gold_rush',       icon: '🏅', name: 'Gold Rush',            desc: 'Earn 25 gold medals',
          check: p => (p.totalGolds||0) >= 25 },
        { id: 'gold_standard',   icon: '🌟', name: 'Gold Standard',        desc: 'Earn 50 gold medals',
          check: p => (p.totalGolds||0) >= 50 },
        { id: 'midas',           icon: '👑', name: 'Midas',                desc: 'Earn 100 gold medals',
          check: p => (p.totalGolds||0) >= 100 },

        // ── VOLUME ───────────────────────────────────────────────────────────
        { id: 'century',         icon: '💯', name: 'Century',              desc: 'Complete 100 levels',
          check: p => (p.totalClears||0) >= 100 },
        { id: 'five_hundred',    icon: '🚀', name: 'Five Hundred',          desc: 'Complete 500 levels',
          check: p => (p.totalClears||0) >= 500 },
        { id: 'thousandaire',    icon: '🌌', name: 'Thousandaire',          desc: 'Complete 1000 levels',
          check: p => (p.totalClears||0) >= 1000 },
        { id: 'legend',          icon: '🔥', name: 'Legend',                desc: 'Hit 10,000 orbs',
          check: p => (p.totalOrbsHit||0) >= 10000 },

    ];

    function getMenuProgress() { return loadProgress(); }

    const BATCH_NAMES = ['Awakening','Emergence','Ascension','Transcendence','Infinity','Revelation','Zenith','Eclipse','Nexus','Apex'];

    function buildMedalGrid(p) {
        const container = document.getElementById('mp-medal-grid');
        container.innerHTML = '';
        const highest = p.highestLevel || 1;
        const tiers = p.bestTiers || {};
        // Show up to highest level reached + a few locked, grouped in batches of 10
        const showUpTo = Math.ceil(highest / 10) * 10;
        for (let batch = 0; batch < Math.ceil(showUpTo / 10); batch++) {
            const lbl = document.createElement('div');
            lbl.className = 'medal-batch-label';
            lbl.textContent = BATCH_NAMES[batch] || `Batch ${batch+1}`;
            container.appendChild(lbl);
            const grid = document.createElement('div');
            grid.className = 'medal-grid';
            for (let i = 0; i < 10; i++) {
                const lvl = batch * 10 + i + 1;
                const cell = document.createElement('div');
                cell.className = 'medal-cell';
                const em = document.createElement('div');
                const tier = tiers[lvl];
                if (lvl > highest) { em.className = 'medal-emoji locked'; em.textContent = '◆'; }
                else if (!tier || tier === 'none') { em.className = 'medal-emoji cleared'; em.textContent = '◆'; }
                else {
                    em.className = 'medal-emoji';
                    em.textContent = tier === 'gold' ? '🥇' : tier === 'silver' ? '🥈' : '🥉';
                }
                cell.appendChild(em);
                grid.appendChild(cell);
            }
            container.appendChild(grid);
        }
    }

    function buildStats(p) {
        const tiers = p.bestTiers || {};
        const times = p.bestTimes || {};
        const goldCount   = Object.values(tiers).filter(t=>t==='gold').length;
        const silverCount = Object.values(tiers).filter(t=>t==='silver').length;
        const bronzeCount = Object.values(tiers).filter(t=>t==='bronze').length;
        const allTimes    = Object.values(times);
        const fastestTime = allTimes.length ? Math.min(...allTimes) : null;
        const totalSecs   = p.totalPlaySecs || 0;
        const hours = totalSecs >= 3600 ? `${(totalSecs/3600).toFixed(1)}h` : `${Math.floor(totalSecs/60)}m`;
        document.getElementById('ms-orbs').textContent    = (p.totalOrbsHit||0).toLocaleString();
        document.getElementById('ms-time').textContent    = hours;
        document.getElementById('ms-levels').textContent  = (p.totalClears||0);
        document.getElementById('ms-sessions').textContent= (p.sessions||0);
        document.getElementById('ms-gold').textContent    = goldCount;
        document.getElementById('ms-silver').textContent  = silverCount;
        document.getElementById('ms-bronze').textContent  = bronzeCount;
        document.getElementById('ms-best-time').textContent = fastestTime != null ? `${fastestTime.toFixed(1)}s` : '—';
    }

    function buildAchievements(p) {
        const list = document.getElementById('ach-list');
        list.innerHTML = '';
        ACHIEVEMENTS.forEach(ach => {
            const unlocked = ach.check(p);
            const item = document.createElement('div');
            item.className = `ach-item${unlocked ? '' : ' locked'}`;
            item.innerHTML = `
                <div class="ach-icon">${ach.icon}</div>
                <div class="ach-text">
                    <div class="ach-name">${ach.name}</div>
                    <div class="ach-desc">${ach.desc}</div>
                </div>
                <div class="ach-check">✓</div>`;
            list.appendChild(item);
        });
    }

    function openMenu() {
        const p = getMenuProgress();
        document.getElementById('mp-level-num').textContent = p.highestLevel || 1;
        buildMedalGrid(p);
        buildStats(p);
        buildAchievements(p);
        document.getElementById('menu-overlay').classList.add('show');
        document.getElementById('menu-panel').classList.add('show');
        // (level select button needs no reset state)
    }

    function closeMenu() {
        document.getElementById('menu-overlay').classList.remove('show');
        document.getElementById('menu-panel').classList.remove('show');
    }

    // Tab switching
    document.querySelectorAll('.menu-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.menu-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.menu-pane').forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(`mpane-${tab.dataset.tab}`).classList.add('active');
        });
    });

    // Open via menu button (upper right) or logo tap
    function toggleMenu() {
        if (document.getElementById('menu-panel').classList.contains('show')) closeMenu();
        else openMenu();
    }
    document.getElementById('menu-btn').addEventListener('click', toggleMenu);
    document.getElementById('intro-menu-btn').addEventListener('click', () => { toggleMenu(); });
    document.getElementById('gs-logo').addEventListener('click', toggleMenu);

    // Close via overlay or X
    document.getElementById('menu-overlay').addEventListener('click', closeMenu);
    document.getElementById('menu-close').addEventListener('click', closeMenu);

    // ── LEVEL SELECT ──────────────────────────────────────────────────────────
    let _lsSelectedLevel = null;

    function medalEmoji(tier) {
        return tier === 'gold' ? '🥇' : tier === 'silver' ? '🥈' : tier === 'bronze' ? '🥉' : null;
    }

    function openLevelSelect() {
        _lsSelectedLevel = null;
        const panel  = document.getElementById('ls-panel');
        const footer = document.getElementById('ls-footer');
        const overlay = document.getElementById('ls-overlay');
        // Reset
        footer.classList.remove('show');
        document.getElementById('ls-scroll').innerHTML = '';
        buildLevelSelect();
        // Step 1: make display:flex (via .animating) so transition can play
        panel.classList.add('animating');
        overlay.classList.add('show');
        // Step 2: on next frame, add .show to trigger the slide-up transition
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                panel.classList.add('show');
            });
        });

    }

    function closeLevelSelect() {
        _lsSelectedLevel = null;
        const panel  = document.getElementById('ls-panel');
        const footer = document.getElementById('ls-footer');
        const overlay = document.getElementById('ls-overlay');
        footer.classList.remove('show');
        overlay.classList.remove('show');
        panel.classList.remove('show'); // triggers slide-down transition
        // After transition: remove .animating → display:none (physically cannot render)
        const cleanup = () => {
            panel.classList.remove('animating');
            panel.removeEventListener('transitionend', cleanup);
            document.getElementById('ls-scroll').innerHTML = '';
        };
        panel.addEventListener('transitionend', cleanup);
        // Safety fallback in case transitionend doesn't fire (e.g. tab hidden)
        setTimeout(cleanup, 500);
    }

    function selectLsCard(lvl, cardEl) {
        // Deselect previous
        document.querySelectorAll('.ls-card.selected').forEach(c => c.classList.remove('selected'));
        _lsSelectedLevel = lvl;
        cardEl.classList.add('selected');

        // Populate footer
        const p = loadProgress();
        const name  = (p.levelNames || {})[lvl] || `Level ${lvl}`;
        const tier  = (p.bestTiers || {})[lvl] || null;
        const time  = (p.bestTimes || {})[lvl] || null;
        const medal = tier && tier !== 'none' ? medalEmoji(tier) : null;

        document.getElementById('ls-footer-name').textContent = `Level ${lvl}: ${name}`;
        let meta = '';
        if (medal && time != null) meta = `${medal} Best: ${time.toFixed(1)}s`;
        else if (time != null) meta = `Best: ${time.toFixed(1)}s`;
        else meta = 'Not yet completed';
        document.getElementById('ls-footer-meta').textContent = meta;
        document.getElementById('ls-footer').classList.add('show');
    }

    function buildLevelSelect() {
        const p = loadProgress();
        const highest = p.highestLevel || 1;
        const tiers   = p.bestTiers || {};
        const times   = p.bestTimes || {};
        const names   = p.levelNames || {};

        const showUpTo = Math.max(10, Math.ceil(highest / 10) * 10);
        const scroll = document.getElementById('ls-scroll');
        scroll.innerHTML = '';

        for (let batch = 0; batch < Math.ceil(showUpTo / 10); batch++) {
            const lbl = document.createElement('div');
            lbl.className = 'ls-batch-label';
            lbl.textContent = BATCH_NAMES[batch] || `Batch ${batch + 1}`;
            scroll.appendChild(lbl);

            const grid = document.createElement('div');
            grid.className = 'ls-grid';

            for (let i = 0; i < 10; i++) {
                const lvl    = batch * 10 + i + 1;
                const locked = lvl > highest;
                const tier   = tiers[lvl] || null;
                const time   = times[lvl] || null;
                const name   = names[lvl] || null;
                const medal  = tier && tier !== 'none' ? medalEmoji(tier) : null;

                const card = document.createElement('div');
                card.className = 'ls-card'
                    + (locked  ? ' locked'  : '')
                    ;
                card.dataset.level = lvl;

                // Medal indicator: emoji or dim dot
                const medalEl = medal
                    ? `<span class="ls-medal-icon">${medal}</span>`
                    : `<span class="ls-medal-dot ${locked ? 'locked' : (tier === 'none' || !tier) ? 'cleared' : ''}"></span>`;

                card.innerHTML = `
                    <div class="ls-card-top">
                        <div class="ls-card-num">Level ${lvl}</div>
                        ${medalEl}
                    </div>
                    <div class="ls-card-name${name ? '' : ' unknown'}">${name || (locked ? '🔒' : '—')}</div>
                    <div class="ls-card-time${medal ? ' ' + tier : ''}">${time != null ? time.toFixed(1) + 's' : ''}</div>`;

                if (!locked) {
                    card.addEventListener('click', () => selectLsCard(lvl, card));
                }
                grid.appendChild(card);
            }
            scroll.appendChild(grid);
        }

        // Reset button at very bottom
        const resetWrap = document.createElement('div');
        resetWrap.className = 'ls-reset-wrap';
        const resetBtn = document.createElement('button');
        resetBtn.className = 'ls-reset-btn';
        resetBtn.textContent = 'Reset All Progress';
        resetBtn._confirming = false;
        resetBtn.addEventListener('click', function() {
            if (!this._confirming) {
                this._confirming = true;
                this.classList.add('confirming');
                this.textContent = 'Tap again to confirm';
                this._confirmTimer = setTimeout(() => {
                    this._confirming = false;
                    this.classList.remove('confirming');
                    this.textContent = 'Reset All Progress';
                }, 3000);
            } else {
                clearTimeout(this._confirmTimer);
                try { localStorage.removeItem('gs_progress'); } catch {}
                // resetGameUI first — kills ls-panel display:none immediately,
                // no race with the close animation
                resetGameUI();
                closeLevelSelect(); closeMenu();
                setTimeout(async () => { await loadLevel(1); startCountdown(); }, 50);
            }
        });
        resetWrap.appendChild(resetBtn);
        scroll.appendChild(resetWrap);
    }

    // Play button — handles both: game already running, and launching from home screen
    document.getElementById('ls-play-btn').addEventListener('click', async () => {
        if (!_lsSelectedLevel) return;
        const lvl = _lsSelectedLevel;
        saveProgress({ resumeLevel: lvl });
        closeLevelSelect();
        closeMenu();
        if (state.started) resetGameUI();
        if (!state.started) {
            // Game hasn't started yet — full startup path
            state.started = true;
            introState.running = false;
            await audio.init();
            resize();
            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('intro-menu-btn').style.display = 'none';
        } else {
            audio.stopBeat();
        }
        await loadLevel(lvl);
        startCountdown();
    });

    document.getElementById('menu-reset-btn').addEventListener('click', openLevelSelect);
    document.getElementById('ls-close').addEventListener('click', closeLevelSelect);
    document.getElementById('ls-overlay').addEventListener('click', closeLevelSelect);

    // ═══════════════════════════════════════════════════════════════════════
    //  ACHIEVEMENT TOAST SYSTEM
    //
    //  checkAndToastAchievements(prevP, newP)
    //    Called after every saveProgress in showFloatingEnd.
    //    Diffs the two snapshots to find achievements that flipped from
    //    locked → unlocked in this exact save, then queues them.
    //
    //  Queue: multiple achievements can unlock simultaneously (e.g. Hat Trick
    //    + Golden Touch on the same gold). They show one at a time, 600ms apart.
    // ═══════════════════════════════════════════════════════════════════════

    const _toastQueue  = [];
    let   _toastActive = false;

    function checkAndToastAchievements(prevP, newP) {
        ACHIEVEMENTS.forEach(ach => {
            const wasUnlocked = ach.check(prevP);
            const nowUnlocked = ach.check(newP);
            if (!wasUnlocked && nowUnlocked) {
                _toastQueue.push(ach);
            }
        });
        if (!_toastActive) _drainToastQueue();
    }

    function _drainToastQueue() {
        if (_toastQueue.length === 0) { _toastActive = false; return; }
        _toastActive = true;
        const ach = _toastQueue.shift();
        _showToast(ach, () => {
            // 600ms gap between consecutive toasts
            setTimeout(_drainToastQueue, 600);
        });
    }

    function _showToast(ach, onDone) {
        const el    = document.getElementById('ach-toast');
        const icon  = document.getElementById('ach-toast-icon');
        const name  = document.getElementById('ach-toast-name');
        const desc  = document.getElementById('ach-toast-desc');
        if (!el) { onDone(); return; }

        // Populate
        icon.textContent = ach.icon;
        name.textContent = ach.name;
        desc.textContent = ach.desc;

        // Reset to hidden state instantly (no transition), then trigger show
        el.classList.remove('show', 'hide');
        el.style.transition = 'none';
        // Force reflow so removing classes takes effect before we add 'show'
        void el.offsetHeight;
        el.style.transition = '';

        // Drop in
        requestAnimationFrame(() => {
            el.classList.add('show');
        });

        // Hold for 2.8s then exit
        const HOLD_MS = 4500;
        setTimeout(() => {
            el.classList.remove('show');
            el.classList.add('hide');
            // After exit transition (~300ms), clean up and call onDone
            setTimeout(() => {
                el.classList.remove('hide');
                onDone();
            }, 320);
        }, HOLD_MS);
    }
