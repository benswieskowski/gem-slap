"""
Gem Slap - A Rhythm Game
"""
from flask import Flask, render_template, jsonify, send_from_directory, make_response
import random, math, os

from game_data import (
    SCALE, NOTE_COLORS, get_color,
    PERFECT_WINDOW, GREAT_WINDOW, GOOD_WINDOW,
    PERFECT_POINTS, GREAT_POINTS, GOOD_POINTS, MISS_POINTS,
    TARGET_DESTROY_RADIUS, STANDARD_TOTAL_ORBS,
    LEVEL_BATCHES, BASS_STYLES,
    create_phrase_library,
)

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# ── Service worker must be served from root scope with no-cache headers ────────
@app.route('/service-worker.js')
def service_worker():
    response = make_response(
        send_from_directory(os.path.join(app.root_path, 'static'), 'service-worker.js')
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Service-Worker-Allowed'] = '/'
    return response


def transpose_in_scale(melody, steps):
    result = []
    for note in melody:
        try:
            idx = SCALE.index(note)
            new_idx = max(0, min(len(SCALE) - 1, idx + steps))
            result.append(SCALE[new_idx])
        except ValueError:
            result.append(note)
    return result


def generate_level(level_num, bass_style=None):
    random.seed(level_num * 77)

    # ── Flat pattern indexing over all 41 levels ───────────────────────────────
    # Single batch of 41 patterns ordered by difficulty score.
    # level_in_set runs 1–41 then cycles; used only for phrase feel selection.
    all_patterns = LEVEL_BATCHES[0]['patterns']
    total_patterns = len(all_patterns)
    pattern_idx = (level_num - 1) % total_patterns
    level_in_set = pattern_idx + 1          # 1–41
    set_num = (level_num - 1) // total_patterns

    batch = LEVEL_BATCHES[0]

    visible_at_once = 8
    total_orbs = STANDARD_TOTAL_ORBS
    bpm = 108                               # client ignores this; BPM comes from engine.js
    base_speed = 0.12
    target_time = total_orbs * 1.5         # client overwrites this with its own formula
    current_bass = bass_style if bass_style is not None else set_num % 10

    # ── Phrase feel selection ──────────────────────────────────────────────────
    # Scaled to 41-level range: chill first ~25%, chill+groove next ~35%, all after
    phrase_lib = create_phrase_library()
    suffix = f'_{visible_at_once}'
    available = {k: v for k, v in phrase_lib.items() if k.endswith(suffix)}
    if level_in_set <= 10:
        available = {k: v for k, v in available.items() if v['feel'] == 'chill'}
    elif level_in_set <= 25:
        available = {k: v for k, v in available.items() if v['feel'] in ['chill', 'groove']}
    # levels 26–41: all feels (chill, groove, funky)
    keys = list(available.keys())
    random.shuffle(keys)
    selected = (keys[:3] + keys[:3])[:3]
    theme_melody = random.choice(available[selected[0]]['melodies'])

    orbs = []
    orb_id = 0
    wave = 0
    while len(orbs) < total_orbs:
        phrase_key = selected[wave % len(selected)]
        phrase = available[phrase_key]
        beats = phrase['beats']
        if wave == 0:
            melody = theme_melody
        elif wave == 1:
            melody = transpose_in_scale(theme_melody, 2) if random.random() > 0.4 else random.choice(phrase['melodies'])
        elif wave == 2:
            root_endings = [m for m in phrase['melodies'] if m[-1] in [0, 7, 12]]
            melody = random.choice(root_endings) if root_endings and random.random() > 0.3 else transpose_in_scale(theme_melody, -1)
        else:
            melody = random.choice(phrase['melodies'])

        remaining = total_orbs - len(orbs)
        count = min(visible_at_once, remaining)
        for i in range(count):
            note = melody[i % len(melody)]
            beat = beats[i % len(beats)]
            x = max(20, min(80, random.gauss(50, 15)))
            y = max(20, min(80, random.gauss(50, 15)))
            angle = random.uniform(0, 2 * math.pi)
            speed = (0.15 + base_speed * 1.2) * random.uniform(0.7, 1.3)
            orbs.append({
                'id': orb_id, 'x': round(x, 1), 'y': round(y, 1),
                'color': get_color(note), 'note': note,
                'size': round(random.uniform(0.85, 1.15), 2),
                'driftX': round(math.cos(angle) * speed, 3),
                'driftY': round(math.sin(angle) * speed, 3),
                'phraseBeat': beat, 'wave': wave,
                'phraseName': phrase_key.replace('_', ' ').title(),
            })
            orb_id += 1
        wave += 1

    pattern = all_patterns[pattern_idx]
    targets = [{'id': i, 'x': c['x'], 'y': c['y']} for i, c in enumerate(pattern['cells'])]

    return {
        'level': level_num, 'levelInSet': level_in_set, 'setNum': set_num,
        'batchName': batch['name'],
        'orbs': orbs, 'bpm': bpm, 'bassStyle': current_bass,
        'speed': round(base_speed, 2), 'targetTime': round(target_time, 1),
        'visibleAtOnce': visible_at_once, 'totalOrbs': total_orbs,
        'timing': {'perfect': PERFECT_WINDOW, 'great': GREAT_WINDOW, 'good': GOOD_WINDOW},
        'points': {'perfect': PERFECT_POINTS, 'great': GREAT_POINTS, 'good': GOOD_POINTS, 'miss': MISS_POINTS},
        'targets': targets, 'targetDestroyRadius': TARGET_DESTROY_RADIUS,
        'patternName': pattern['name'],
    }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/level/<int:level_num>')
def get_level(level_num):
    return jsonify(generate_level(level_num))

@app.route('/api/level/<int:level_num>/bass/<int:bass_style>')
def get_level_with_bass(level_num, bass_style):
    return jsonify(generate_level(level_num, bass_style))

@app.route('/api/bass_styles')
def get_bass_styles():
    return jsonify(BASS_STYLES)

@app.route('/api/batches')
def get_batches():
    all_patterns = LEVEL_BATCHES[0]['patterns']
    return jsonify([{
        'index': 0,
        'name': LEVEL_BATCHES[0]['name'],
        'levelRange': [1, len(all_patterns)],
        'patternNames': [p['name'] for p in all_patterns],
    }])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
