"""
AURA - Game Data
All level patterns, musical phrases, scoring constants, and note config.
"""

# ═══════════════════════════════════════════════════════════════
# SCORING & TIMING
# ═══════════════════════════════════════════════════════════════
PERFECT_WINDOW = 130
GREAT_WINDOW = 250
GOOD_WINDOW = 400
PERFECT_POINTS = 100
GREAT_POINTS = 60
GOOD_POINTS = 30
MISS_POINTS = 10

TARGET_DESTROY_RADIUS = 22
STANDARD_TOTAL_ORBS = 20

# ═══════════════════════════════════════════════════════════════
# MUSIC
# ═══════════════════════════════════════════════════════════════
SCALE = [-5, -2, 0, 3, 5, 7, 10, 12, 15, 17, 19, 22]

# Full visible spectrum from red (low) to violet (high), skipping blue
# (reserved for crystals). Arc follows the natural light spectrum:
# red → orange → gold → yellow-green → green → magenta → purple → violet.
# The jump from green to magenta skips blue intentionally.
# All 6 actually-played notes (0,3,5,7,10,12) get a distinct vivid hue.
# Full visible spectrum, red (low) → violet (high).
# Blue is now included — crystals are white diamonds, no longer blue.
# Yellow-green compressed to one clean emerald so blue gets its own slot.
# Arc: vivid red → warm orange → emerald → electric cyan-blue → indigo → violet
#
# All 6 actually-played notes (0,3,5,7,10,12) map to a distinct vivid hue.
NOTE_COLORS = {
    -5: '#F03028',   # vivid red (rarely played)
    -2: '#F03028',   # vivid red (rarely played)
     0: '#F03028',   # vivid red
     3: '#F57828',   # warm orange
     5: '#28D858',   # emerald green
     7: '#18C8F8',   # electric cyan-blue
    10: '#5038E8',   # electric indigo
    12: '#A020E0',   # vivid violet
    15: '#A020E0',   # violet (rarely played)
    17: '#A020E0',   # violet (rarely played)
    19: '#A020E0',   # violet (rarely played)
    22: '#A020E0',   # violet (rarely played)
}

def get_color(note):
    return NOTE_COLORS.get(note, '#F5A200')

def create_phrase_library():
    library = {}
    library['sigh_6']     = {'beats': [1, 1.5, 2.5, 3, 4, 4.5],             'feel': 'chill',  'melodies': [[0,3,5,3,0,0],[0,0,3,5,3,0],[0,3,0,3,5,0],[0,5,3,0,0,0],[3,5,3,0,0,0]]}
    library['float_6']    = {'beats': [1, 2, 2.5, 3.5, 4, 4.5],             'feel': 'chill',  'melodies': [[7,5,7,5,7,7],[7,7,5,7,10,7],[5,7,5,7,5,7],[7,10,7,5,7,7],[7,5,3,5,7,7]]}
    library['dream_6']    = {'beats': [1, 1.5, 2.5, 3, 4, 4.5],             'feel': 'chill',  'melodies': [[0,5,7,5,0,0],[0,3,7,3,0,0],[0,0,5,7,5,0],[7,5,0,5,7,7],[0,5,0,5,7,0]]}
    library['wave_6']     = {'beats': [1, 2, 3, 3.5, 4, 4.5],               'feel': 'chill',  'melodies': [[0,3,5,7,5,0],[0,5,7,5,3,0],[7,5,3,5,7,7],[0,3,5,3,0,0],[3,5,7,5,3,3]]}
    library['pocket_6']   = {'beats': [1, 1.5, 2.5, 3, 4, 4.5],             'feel': 'groove', 'melodies': [[0,0,7,5,3,0],[0,0,7,0,5,0],[0,7,0,7,5,0],[0,0,10,7,5,0],[0,3,0,7,5,0]]}
    library['strut_6']    = {'beats': [1, 2, 2.5, 3.5, 4, 4.5],             'feel': 'groove', 'melodies': [[7,7,10,7,5,7],[7,10,7,7,5,7],[7,5,7,10,7,7],[7,7,5,7,10,7],[5,7,7,10,7,7]]}
    library['bounce_6']   = {'beats': [1, 1.5, 2.5, 3, 4, 4.5],             'feel': 'groove', 'melodies': [[0,3,0,3,7,0],[0,7,0,7,10,7],[7,0,7,0,7,7],[0,5,0,7,5,0],[3,0,3,7,5,0]]}
    library['swagger_6']  = {'beats': [1, 2, 2.5, 3.5, 4, 4.5],             'feel': 'groove', 'melodies': [[0,0,7,10,7,0],[7,10,7,5,7,7],[0,3,7,7,5,0],[0,0,5,7,5,0],[3,5,7,7,5,3]]}
    library['punch_6']    = {'beats': [1, 1.5, 2, 3, 3.5, 4.5],             'feel': 'funky',  'melodies': [[0,7,10,7,0,0],[0,0,7,12,7,0],[0,7,0,10,7,0],[7,12,7,5,7,7],[0,10,7,0,0,0]]}
    library['attack_6']   = {'beats': [1, 1.5, 2.5, 3, 3.5, 4.5],           'feel': 'funky',  'melodies': [[0,3,7,10,12,7],[7,10,12,10,7,7],[0,7,12,7,0,0],[0,0,10,12,10,7],[3,7,10,7,3,3]]}
    library['fire_6']     = {'beats': [1, 2, 2.5, 3, 4, 4.5],               'feel': 'funky',  'melodies': [[7,12,7,12,7,7],[0,12,0,12,7,0],[7,10,12,12,10,7],[0,7,12,10,7,0],[12,7,12,7,0,0]]}
    library['edge_6']     = {'beats': [1, 1.5, 2, 3.5, 4, 4.5],             'feel': 'funky',  'melodies': [[10,7,10,7,0,0],[7,10,7,10,7,7],[0,10,0,10,7,0],[10,12,10,7,0,0],[0,0,10,7,5,0]]}
    library['journey_8']  = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],    'feel': 'chill',  'melodies': [[0,3,5,7,7,5,3,0],[0,0,3,5,7,5,3,0],[0,3,5,7,5,3,0,0],[0,5,7,5,0,5,7,7],[7,5,3,0,0,3,5,7]]}
    library['horizon_8']  = {'beats': [1, 1.5, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'chill',  'melodies': [[7,5,7,10,7,5,7,7],[7,7,5,7,10,7,5,7],[0,5,7,7,5,0,0,0],[7,10,7,7,5,7,7,7],[0,0,5,7,5,0,0,0]]}
    library['funk_8']     = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],    'feel': 'groove', 'melodies': [[0,0,7,0,0,10,7,7],[0,0,7,5,0,0,7,0],[7,10,7,7,5,7,7,7],[0,3,0,3,5,7,5,0],[0,7,0,7,10,7,0,0]]}
    library['soul_8']     = {'beats': [1, 1.5, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'groove', 'melodies': [[7,10,7,5,7,10,12,7],[7,7,10,7,5,7,7,7],[0,3,7,7,10,7,5,0],[0,0,7,10,7,5,0,0],[3,5,7,7,5,3,0,0]]}
    library['blaze_8']    = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],    'feel': 'funky',  'melodies': [[0,7,12,7,0,7,12,12],[7,10,12,12,10,7,5,7],[0,0,7,10,12,10,7,0],[0,7,0,7,12,12,7,0],[12,7,12,7,0,0,7,7]]}
    library['storm_8']    = {'beats': [1, 1.5, 2, 3, 3.5, 4, 4.25, 4.5],   'feel': 'funky',  'melodies': [[7,10,12,10,7,10,12,7],[0,7,10,12,12,10,7,0],[7,12,7,7,12,7,5,7],[0,0,7,12,7,0,0,0],[10,7,10,12,10,7,7,7]]}
    library['legend_9']   = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'chill',  'melodies': [[0,0,3,5,7,5,3,0,0],[0,3,5,7,7,5,3,5,7],[7,5,7,5,7,5,7,7,7],[0,5,7,5,0,5,7,5,0],[0,3,5,7,7,7,5,3,0]]}
    library['cosmos_9']   = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'chill',  'melodies': [[7,10,7,5,7,10,7,5,7],[0,7,0,7,0,7,5,0,0],[7,7,10,7,7,5,7,7,7],[0,5,7,10,7,5,0,0,0],[0,0,7,10,7,0,0,7,7]]}
    library['triumph_9']  = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'groove', 'melodies': [[0,0,7,5,0,0,7,10,7],[7,10,7,7,10,12,10,7,7],[0,3,0,5,0,7,10,7,0],[7,7,10,12,12,10,7,7,7],[0,7,0,7,5,7,10,7,7]]}
    library['glory_9']    = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'groove', 'melodies': [[0,0,3,7,10,7,3,0,0],[7,10,7,5,7,10,12,7,7],[0,3,5,7,7,7,5,3,0],[0,7,0,7,12,7,0,0,0],[3,5,7,5,3,5,7,5,3]]}
    library['inferno_9']  = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'funky',  'melodies': [[0,7,12,7,0,7,12,12,12],[7,10,12,12,10,7,10,12,7],[0,0,7,10,12,12,10,7,0],[12,7,12,7,12,7,0,0,0],[0,7,0,7,12,12,12,7,0]]}
    library['phoenix_9']  = {'beats': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.25, 4.5], 'feel': 'funky',  'melodies': [[0,3,7,10,12,12,12,10,7],[7,12,7,12,7,12,10,7,7],[0,0,10,12,10,0,0,7,7],[7,10,12,10,7,10,12,12,12],[0,7,12,0,7,12,7,0,0]]}
    return library


# ═══════════════════════════════════════════════════════════════
# BATCH 0: ANIMALS — simple silhouettes, 8–10 crystals each
#
# Each animal chosen for one unmistakable visual signature:
# tail fork (fish), M-wings (bird), tall ears (rabbit), S-neck (swan),
# 4-wing symmetry (butterfly), shell+legs top-down (turtle),
# forked flukes (whale), spiral shell (snail),
# raised V-claws (crab), 8-leg radial (spider).
#
# Coordinates in 22–78% playfield range.
# Crystal counts: 8 → 9 → 9 → 9 → 10 → 10 → 10 → 10 → 10 → 10
# ═══════════════════════════════════════════════════════════════
ANIMAL_PATTERNS = [

    # ── 1. Fish — 8 crystals ─────────────────────────────────
    # Facing left. Signature: oval body + forked tail V on the right.
    {'name': 'Fish', 'cells': [
        {'x': 26, 'y': 50},   # mouth tip
        {'x': 36, 'y': 43},   # eye
        {'x': 48, 'y': 36},   # body — upper arc
        {'x': 62, 'y': 40},   # body — upper right
        {'x': 48, 'y': 64},   # body — lower arc
        {'x': 62, 'y': 60},   # body — lower right
        {'x': 74, 'y': 38},   # tail — upper fork
        {'x': 74, 'y': 62},   # tail — lower fork
    ]},

    # ── 2. Bird — 9 crystals ─────────────────────────────────
    # In flight. Signature: M-shaped wings — the universal bird silhouette.
    {'name': 'Bird', 'cells': [
        {'x': 24, 'y': 44},   # left wing — outer tip
        {'x': 35, 'y': 30},   # left wing — apex of M
        {'x': 43, 'y': 40},   # left wing — inner valley of M
        {'x': 50, 'y': 46},   # body center
        {'x': 57, 'y': 40},   # right wing — inner valley of M
        {'x': 65, 'y': 30},   # right wing — apex of M
        {'x': 76, 'y': 44},   # right wing — outer tip
        {'x': 44, 'y': 66},   # tail — left feather
        {'x': 56, 'y': 66},   # tail — right feather
    ]},

    # ── 3. Rabbit — 9 crystals ───────────────────────────────
    # Sitting. Signature: two tall narrow parallel ears — unmistakable.
    {'name': 'Rabbit', 'cells': [
        {'x': 40, 'y': 24},   # left ear — top
        {'x': 42, 'y': 36},   # left ear — base
        {'x': 58, 'y': 36},   # right ear — base
        {'x': 60, 'y': 24},   # right ear — top
        {'x': 50, 'y': 48},   # head
        {'x': 50, 'y': 64},   # body
        {'x': 36, 'y': 74},   # left foot
        {'x': 64, 'y': 74},   # right foot
        {'x': 68, 'y': 60},   # fluffy tail
    ]},

    # ── 4. Swan — 9 crystals ─────────────────────────────────
    # Facing right. Signature: long S-curve neck descending into oval body.
    {'name': 'Swan', 'cells': [
        {'x': 68, 'y': 26},   # head
        {'x': 62, 'y': 34},   # neck — upper curve
        {'x': 54, 'y': 42},   # neck — mid curve
        {'x': 46, 'y': 50},   # neck base / body join
        {'x': 30, 'y': 52},   # body — left (widest)
        {'x': 34, 'y': 62},   # body — lower left
        {'x': 48, 'y': 68},   # body — bottom center
        {'x': 62, 'y': 64},   # body — tail
        {'x': 50, 'y': 56},   # wing highlight
    ]},

    # ── 5. Butterfly — 10 crystals ───────────────────────────
    # Wings spread. Signature: 4 distinct wings + narrow body. Bilateral.
    {'name': 'Butterfly', 'cells': [
        {'x': 26, 'y': 38},   # upper left wing — outer
        {'x': 36, 'y': 26},   # upper left wing — top
        {'x': 64, 'y': 26},   # upper right wing — top
        {'x': 74, 'y': 38},   # upper right wing — outer
        {'x': 40, 'y': 46},   # upper left — inner pinch
        {'x': 60, 'y': 46},   # upper right — inner pinch
        {'x': 50, 'y': 42},   # body — upper waist
        {'x': 50, 'y': 60},   # body — lower
        {'x': 32, 'y': 64},   # lower left wing
        {'x': 68, 'y': 64},   # lower right wing
    ]},

    # ── 6. Turtle — 10 crystals ──────────────────────────────
    # Top-down. Signature: oval shell outline + 4 legs poking out.
    {'name': 'Turtle', 'cells': [
        {'x': 50, 'y': 28},   # head
        {'x': 38, 'y': 36},   # shell — upper left
        {'x': 62, 'y': 36},   # shell — upper right
        {'x': 30, 'y': 54},   # shell — left
        {'x': 70, 'y': 54},   # shell — right
        {'x': 38, 'y': 68},   # shell — lower left
        {'x': 62, 'y': 68},   # shell — lower right
        {'x': 24, 'y': 40},   # front left leg
        {'x': 76, 'y': 40},   # front right leg
        {'x': 26, 'y': 66},   # back left leg
    ]},

    # ── 7. Whale — 10 crystals ───────────────────────────────
    # Swimming left to right. Signature: massive body + forked tail flukes.
    {'name': 'Whale', 'cells': [
        {'x': 24, 'y': 50},   # head tip
        {'x': 26, 'y': 58},   # jaw
        {'x': 32, 'y': 42},   # eye
        {'x': 42, 'y': 32},   # body — upper left
        {'x': 56, 'y': 28},   # body — dorsal peak
        {'x': 68, 'y': 32},   # body — upper right
        {'x': 44, 'y': 58},   # body — lower left
        {'x': 60, 'y': 60},   # body — lower right
        {'x': 76, 'y': 38},   # tail fluke — upper
        {'x': 76, 'y': 62},   # tail fluke — lower
    ]},

    # ── 8. Snail — 10 crystals ───────────────────────────────
    # Moving left. Signature: circular shell arc + horizontal foot + antenna.
    {'name': 'Snail', 'cells': [
        {'x': 64, 'y': 28},   # shell — top
        {'x': 76, 'y': 44},   # shell — right
        {'x': 74, 'y': 60},   # shell — lower right
        {'x': 62, 'y': 70},   # shell — bottom
        {'x': 50, 'y': 64},   # shell — left arc
        {'x': 60, 'y': 50},   # shell — inner whorl
        {'x': 42, 'y': 72},   # foot — right
        {'x': 30, 'y': 70},   # foot — left
        {'x': 26, 'y': 60},   # head
        {'x': 24, 'y': 48},   # antenna
    ]},

    # ── 9. Crab — 10 crystals ────────────────────────────────
    # Facing forward. Signature: wide body + two large claws raised in V.
    {'name': 'Crab', 'cells': [
        {'x': 22, 'y': 28},   # left claw — pincer tip
        {'x': 28, 'y': 40},   # left claw — base
        {'x': 36, 'y': 50},   # left arm
        {'x': 44, 'y': 58},   # body — left
        {'x': 50, 'y': 54},   # body — center
        {'x': 56, 'y': 58},   # body — right
        {'x': 64, 'y': 50},   # right arm
        {'x': 72, 'y': 40},   # right claw — base
        {'x': 78, 'y': 28},   # right claw — pincer tip
        {'x': 50, 'y': 72},   # legs / body base
    ]},

    # ── 10. Spider — 10 crystals ─────────────────────────────
    # Top-down. Signature: 2 body segments + 4 legs per side splayed out.
    {'name': 'Spider', 'cells': [
        {'x': 50, 'y': 38},   # head
        {'x': 50, 'y': 58},   # abdomen
        {'x': 34, 'y': 28},   # left upper leg — outer
        {'x': 24, 'y': 36},   # left upper leg — far
        {'x': 30, 'y': 52},   # left lower leg — outer
        {'x': 22, 'y': 62},   # left lower leg — far
        {'x': 66, 'y': 28},   # right upper leg — outer
        {'x': 76, 'y': 36},   # right upper leg — far
        {'x': 70, 'y': 52},   # right lower leg — outer
        {'x': 78, 'y': 62},   # right lower leg — far
    ]},
]


# ═══════════════════════════════════════════════════════════════
# BATCH 1: MATH SYMBOLS — 8–10 crystals per level
#
# All coordinates in the 22–78% playfield range.
# Cell count: 8 → 9 → 9 → 7 → 8 → 7 → 10 → 9 → 9 → 10
# ═══════════════════════════════════════════════════════════════
MATH_PATTERNS = [

    # ── 1. Δ  Delta — 8 crystals ─────────────────────────────
    {'name': 'Δ  Delta', 'cells': [
        {'x': 50, 'y': 25},   # apex
        {'x': 38, 'y': 42},   # left edge — upper midpoint
        {'x': 62, 'y': 42},   # right edge — upper midpoint
        {'x': 29, 'y': 58},   # left edge — lower midpoint
        {'x': 71, 'y': 58},   # right edge — lower midpoint
        {'x': 26, 'y': 74},   # bottom-left corner
        {'x': 50, 'y': 74},   # bottom-center
        {'x': 74, 'y': 74},   # bottom-right corner
    ]},

    # ── 2. +  Plus — 9 crystals ──────────────────────────────
    {'name': '+  Plus', 'cells': [
        {'x': 50, 'y': 25},   # top arm — far
        {'x': 50, 'y': 37},   # top arm — near
        {'x': 25, 'y': 50},   # left arm — far
        {'x': 37, 'y': 50},   # left arm — near
        {'x': 50, 'y': 50},   # center
        {'x': 63, 'y': 50},   # right arm — near
        {'x': 75, 'y': 50},   # right arm — far
        {'x': 50, 'y': 63},   # bottom arm — near
        {'x': 50, 'y': 75},   # bottom arm — far
    ]},

    # ── 3. ×  Times — 9 crystals ─────────────────────────────
    {'name': '×  Times', 'cells': [
        {'x': 28, 'y': 26},   # top-left arm — far
        {'x': 39, 'y': 37},   # top-left arm — near
        {'x': 61, 'y': 37},   # top-right arm — near
        {'x': 72, 'y': 26},   # top-right arm — far
        {'x': 50, 'y': 50},   # center
        {'x': 39, 'y': 63},   # bottom-left arm — near
        {'x': 28, 'y': 74},   # bottom-left arm — far
        {'x': 61, 'y': 63},   # bottom-right arm — near
        {'x': 72, 'y': 74},   # bottom-right arm — far
    ]},

    # ── 4. θ  Theta — 9 crystals ─────────────────────────────
    # Six crystals at 60° intervals form a clean circular outline;
    # three crystals form the horizontal bar through the center.
    # The bar endpoints sit just inside the circle edge so the
    # crossbar reads as interior, not as a separate element.
    {'name': 'θ  Theta', 'cells': [
        {'x': 50, 'y': 27},   # circle — top
        {'x': 69, 'y': 38},   # circle — upper-right
        {'x': 69, 'y': 62},   # circle — lower-right
        {'x': 50, 'y': 73},   # circle — bottom
        {'x': 31, 'y': 62},   # circle — lower-left
        {'x': 31, 'y': 38},   # circle — upper-left
        {'x': 36, 'y': 50},   # bar — left
        {'x': 50, 'y': 50},   # bar — center
        {'x': 64, 'y': 50},   # bar — right
    ]},

    # ── 5. =  Equals — 8 crystals ────────────────────────────
    {'name': '=  Equals', 'cells': [
        {'x': 25, 'y': 40},   # top bar — far left
        {'x': 42, 'y': 40},   # top bar — left-center
        {'x': 58, 'y': 40},   # top bar — right-center
        {'x': 75, 'y': 40},   # top bar — far right
        {'x': 25, 'y': 60},   # bottom bar — far left
        {'x': 42, 'y': 60},   # bottom bar — left-center
        {'x': 58, 'y': 60},   # bottom bar — right-center
        {'x': 75, 'y': 60},   # bottom bar — far right
    ]},

    # ── 6. %  Percent — 7 crystals ───────────────────────────
    # Single dot (upper-LEFT) + 5-crystal forward slash / + single dot (lower-RIGHT).
    # Slash ascends left→right (y decreases as x increases) — correct % direction.
    {'name': '%  Percent', 'cells': [
        {'x': 30, 'y': 65},   # lower-left dot
        {'x': 37, 'y': 58},   # slash — 1 (ascending)
        {'x': 43, 'y': 52},   # slash — 2
        {'x': 50, 'y': 50},   # slash — center
        {'x': 57, 'y': 44},   # slash — 4
        {'x': 63, 'y': 38},   # slash — 5
        {'x': 70, 'y': 30},   # upper-right dot
    ]},

    # ── 7. π  Pi — 10 crystals ───────────────────────────────
    {'name': 'π  Pi', 'cells': [
        {'x': 25, 'y': 30},   # bar — far left
        {'x': 42, 'y': 30},   # bar — left-center
        {'x': 58, 'y': 30},   # bar — right-center
        {'x': 75, 'y': 30},   # bar — far right
        {'x': 35, 'y': 44},   # left leg — upper
        {'x': 32, 'y': 58},   # left leg — mid (lean outward)
        {'x': 29, 'y': 72},   # left leg — lower (lean outward)
        {'x': 65, 'y': 44},   # right leg — upper
        {'x': 68, 'y': 58},   # right leg — mid (lean outward)
        {'x': 71, 'y': 72},   # right leg — lower (lean outward)
    ]},

    # ── 8. √  Root — 9 crystals ──────────────────────────────
    {'name': '√  Root', 'cells': [
        {'x': 23, 'y': 56},   # tail — small descender, left side
        {'x': 30, 'y': 64},   # notch — dropping down
        {'x': 36, 'y': 72},   # check — lowest point
        {'x': 43, 'y': 61},   # check — rising back up
        {'x': 50, 'y': 49},   # diagonal — mid-rise
        {'x': 56, 'y': 35},   # diagonal — near top
        {'x': 61, 'y': 30},   # bar — start (where stroke meets bar)
        {'x': 70, 'y': 30},   # bar — mid
        {'x': 78, 'y': 30},   # bar — end, right side
    ]},

    # ── 9. Σ  Sigma — 9 crystals ─────────────────────────────
    {'name': 'Σ  Sigma', 'cells': [
        {'x': 33, 'y': 28},   # top bar — left
        {'x': 51, 'y': 28},   # top bar — center
        {'x': 70, 'y': 28},   # top bar — right
        {'x': 54, 'y': 40},   # upper diagonal — midpoint
        {'x': 35, 'y': 50},   # center vertex — inward point (key crystal)
        {'x': 54, 'y': 60},   # lower diagonal — midpoint
        {'x': 33, 'y': 72},   # bottom bar — left
        {'x': 51, 'y': 72},   # bottom bar — center
        {'x': 70, 'y': 72},   # bottom bar — right
    ]},

    # ── 10. ∞  Infinity — 10 crystals ────────────────────────
    # Two complete oval loops sharing a center crossing point.
    # Both loops fully traced with top and bottom arc points.
    {'name': '∞  Infinity', 'cells': [
        {'x': 25, 'y': 50},   # far-left extreme
        {'x': 31, 'y': 37},   # left loop — upper-left
        {'x': 42, 'y': 30},   # left loop — top
        {'x': 31, 'y': 63},   # left loop — lower-left
        {'x': 42, 'y': 70},   # left loop — bottom
        {'x': 50, 'y': 50},   # center crossing point
        {'x': 58, 'y': 30},   # right loop — top
        {'x': 69, 'y': 37},   # right loop — upper-right
        {'x': 58, 'y': 70},   # right loop — bottom
        {'x': 69, 'y': 63},   # right loop — lower-right
    ]},
]


# ═══════════════════════════════════════════════════════════════
# BATCH 2: MUSIC — musical symbols, easy → hard
# Cell count: 5 → 5 → 6 → 7 → 7 → 7 → 8 → 8 → 8 → 9
# ═══════════════════════════════════════════════════════════════
MUSIC_PATTERNS = [
    {'name': 'Quarter Note', 'cells': [
        {'x': 44, 'y': 68}, {'x': 51, 'y': 64},
        {'x': 53, 'y': 52}, {'x': 53, 'y': 38}, {'x': 53, 'y': 24},
    ]},
    {'name': 'Whole Note', 'cells': [
        {'x': 50, 'y': 30}, {'x': 70, 'y': 44}, {'x': 72, 'y': 60},
        {'x': 50, 'y': 70}, {'x': 28, 'y': 52},
    ]},
    {'name': 'Eighth Note', 'cells': [
        {'x': 38, 'y': 72}, {'x': 45, 'y': 68},
        {'x': 47, 'y': 56}, {'x': 47, 'y': 38},
        {'x': 61, 'y': 36}, {'x': 69, 'y': 47},
    ]},
    {'name': 'Flat', 'cells': [
        {'x': 38, 'y': 26}, {'x': 38, 'y': 40},
        {'x': 38, 'y': 54}, {'x': 38, 'y': 68},
        {'x': 52, 'y': 52}, {'x': 58, 'y': 64}, {'x': 44, 'y': 74},
    ]},
    {'name': 'Fermata', 'cells': [
        {'x': 24, 'y': 54}, {'x': 32, 'y': 36},
        {'x': 42, 'y': 27}, {'x': 58, 'y': 27},
        {'x': 68, 'y': 36}, {'x': 76, 'y': 54},
        {'x': 50, 'y': 63},
    ]},
    {'name': 'Repeat Sign', 'cells': [
        {'x': 36, 'y': 36}, {'x': 36, 'y': 56},
        {'x': 52, 'y': 26}, {'x': 52, 'y': 50}, {'x': 52, 'y': 74},
        {'x': 64, 'y': 26}, {'x': 64, 'y': 74},
    ]},
    {'name': 'Beamed Notes', 'cells': [
        {'x': 26, 'y': 74}, {'x': 33, 'y': 70},
        {'x': 35, 'y': 56}, {'x': 35, 'y': 34},
        {'x': 63, 'y': 28}, {'x': 63, 'y': 50},
        {'x': 60, 'y': 66}, {'x': 67, 'y': 62},
    ]},
    {'name': 'Sharp', 'cells': [
        {'x': 40, 'y': 27}, {'x': 37, 'y': 69},
        {'x': 56, 'y': 23}, {'x': 53, 'y': 65},
        {'x': 31, 'y': 40}, {'x': 62, 'y': 36},
        {'x': 31, 'y': 56}, {'x': 62, 'y': 52},
    ]},
    {'name': 'Bass Clef', 'cells': [
        {'x': 50, 'y': 27},
        {'x': 64, 'y': 32}, {'x': 70, 'y': 46},
        {'x': 64, 'y': 62}, {'x': 48, 'y': 70}, {'x': 32, 'y': 64},
        {'x': 74, 'y': 38}, {'x': 74, 'y': 54},
    ]},
    {'name': 'Treble Clef', 'cells': [
        {'x': 55, 'y': 76}, {'x': 43, 'y': 70},
        {'x': 37, 'y': 58}, {'x': 40, 'y': 43},
        {'x': 46, 'y': 29}, {'x': 62, 'y': 24},
        {'x': 71, 'y': 38}, {'x': 65, 'y': 54},
        {'x': 33, 'y': 51},
    ]},
]


# ═══════════════════════════════════════════════════════════════
# BATCH 3: GEOMETRY — easy → hard
# Cell count: 3 → 4 → 4 → 4 → 5 → 5 → 5 → 6 → 6 → 7
# ═══════════════════════════════════════════════════════════════
GEOMETRY_PATTERNS = [
    {'name': 'Triangle',  'cells': [{'x': 50, 'y': 36}, {'x': 38, 'y': 60}, {'x': 62, 'y': 60}]},
    {'name': 'Line',      'cells': [{'x': 25, 'y': 50}, {'x': 42, 'y': 50}, {'x': 58, 'y': 50}, {'x': 75, 'y': 50}]},
    {'name': 'Square',    'cells': [{'x': 34, 'y': 34}, {'x': 66, 'y': 34}, {'x': 34, 'y': 66}, {'x': 66, 'y': 66}]},
    {'name': 'Diamond',   'cells': [{'x': 50, 'y': 27}, {'x': 27, 'y': 50}, {'x': 73, 'y': 50}, {'x': 50, 'y': 73}]},
    {'name': 'Arrow',     'cells': [{'x': 25, 'y': 42}, {'x': 25, 'y': 58}, {'x': 50, 'y': 28}, {'x': 50, 'y': 72}, {'x': 73, 'y': 50}]},
    {'name': 'Cross',     'cells': [{'x': 50, 'y': 30}, {'x': 30, 'y': 50}, {'x': 50, 'y': 50}, {'x': 70, 'y': 50}, {'x': 50, 'y': 70}]},
    {'name': 'Pentagon',  'cells': [{'x': 50, 'y': 29}, {'x': 72, 'y': 45}, {'x': 64, 'y': 71}, {'x': 36, 'y': 71}, {'x': 28, 'y': 45}]},
    {'name': 'Hexagon',   'cells': [{'x': 50, 'y': 26}, {'x': 71, 'y': 38}, {'x': 71, 'y': 62}, {'x': 50, 'y': 74}, {'x': 29, 'y': 62}, {'x': 29, 'y': 38}]},
    {'name': 'Star',      'cells': [{'x': 50, 'y': 24}, {'x': 66, 'y': 41}, {'x': 73, 'y': 63}, {'x': 50, 'y': 68}, {'x': 27, 'y': 63}, {'x': 34, 'y': 41}]},
    {'name': 'Snowflake', 'cells': [{'x': 50, 'y': 50}, {'x': 50, 'y': 25}, {'x': 72, 'y': 38}, {'x': 72, 'y': 62}, {'x': 50, 'y': 75}, {'x': 28, 'y': 63}, {'x': 28, 'y': 38}]},
]


# ═══════════════════════════════════════════════════════════════
# BATCH 4: CONSTELLATIONS
# Star counts: 5 → 5 → 7 → 4 → 5 → 7 → 6 → 6 → 8 → 9
# ═══════════════════════════════════════════════════════════════
CONSTELLATION_PATTERNS = [
    {'name': 'Cassiopeia',      'cells': [{'x': 76, 'y': 53}, {'x': 60, 'y': 66}, {'x': 51, 'y': 49}, {'x': 36, 'y': 50}, {'x': 24, 'y': 34}]},
    {'name': 'Cygnus',          'cells': [{'x': 31, 'y': 24}, {'x': 61, 'y': 24}, {'x': 41, 'y': 40}, {'x': 25, 'y': 58}, {'x': 75, 'y': 76}]},
    {'name': 'Corona Borealis', 'cells': [{'x': 68, 'y': 31}, {'x': 76, 'y': 47}, {'x': 66, 'y': 64}, {'x': 53, 'y': 67}, {'x': 42, 'y': 69}, {'x': 30, 'y': 63}, {'x': 24, 'y': 42}]},
    {'name': 'Crux',            'cells': [{'x': 55, 'y': 76}, {'x': 32, 'y': 47}, {'x': 50, 'y': 24}, {'x': 68, 'y': 39}]},
    {'name': 'Lyra',            'cells': [{'x': 69, 'y': 24}, {'x': 56, 'y': 34}, {'x': 39, 'y': 40}, {'x': 47, 'y': 70}, {'x': 31, 'y': 76}]},
    {'name': 'Big Dipper',      'cells': [{'x': 22, 'y': 54}, {'x': 28, 'y': 65}, {'x': 45, 'y': 60}, {'x': 45, 'y': 50}, {'x': 55, 'y': 43}, {'x': 62, 'y': 36}, {'x': 78, 'y': 35}]},
    {'name': 'Gemini',          'cells': [{'x': 31, 'y': 28}, {'x': 24, 'y': 39}, {'x': 62, 'y': 47}, {'x': 39, 'y': 56}, {'x': 76, 'y': 54}, {'x': 67, 'y': 72}]},
    {'name': 'Leo',             'cells': [{'x': 76, 'y': 39}, {'x': 62, 'y': 47}, {'x': 68, 'y': 52}, {'x': 68, 'y': 61}, {'x': 40, 'y': 45}, {'x': 24, 'y': 55}]},
    {'name': 'Scorpius',        'cells': [{'x': 70, 'y': 24}, {'x': 72, 'y': 30}, {'x': 61, 'y': 36}, {'x': 57, 'y': 38}, {'x': 54, 'y': 42}, {'x': 47, 'y': 55}, {'x': 28, 'y': 76}, {'x': 28, 'y': 63}]},
    {'name': 'Orion',           'cells': [{'x': 50, 'y': 24}, {'x': 37, 'y': 31}, {'x': 56, 'y': 34}, {'x': 52, 'y': 51}, {'x': 49, 'y': 54}, {'x': 46, 'y': 55}, {'x': 50, 'y': 65}, {'x': 42, 'y': 76}, {'x': 63, 'y': 72}]},
]


# ═══════════════════════════════════════════════════════════════
# LEVEL BATCHES
# Batch 0 = Math Symbols   (levels  1–10)
# Batch 1 = Music          (levels 11–20)
# Batch 2 = Geometry       (levels 21–30)
# Batch 3 = Constellations (levels 31–40)
# ═══════════════════════════════════════════════════════════════
LEVEL_BATCHES = [
    {'name': 'Animals',        'patterns': ANIMAL_PATTERNS},
    {'name': 'Math Symbols',   'patterns': MATH_PATTERNS},
    {'name': 'Music',          'patterns': MUSIC_PATTERNS},
    {'name': 'Geometry',       'patterns': GEOMETRY_PATTERNS},
    {'name': 'Constellations', 'patterns': CONSTELLATION_PATTERNS},
]


# ═══════════════════════════════════════════════════════════════
# BASS STYLES
# ═══════════════════════════════════════════════════════════════
BASS_STYLES = {
    0: {'name': "Wily's Resolve",   'bpm': 150},   # Mega Man 2 · Dr. Wily Stage
    1: {'name': 'Fourside Funk',    'bpm': 108},   # Earthbound · Fourside (C Dorian)
    2: {'name': 'Snake Slither',    'bpm': 126},   # Mega Man 3 · Snake Man
    3: {'name': 'Pharaoh Rush',     'bpm': 144},   # Mega Man 4 · Pharaoh Man (Hijaz)
    4: {'name': 'Hard Corps',       'bpm': 150},   # Mega Man 3 · Hard Man
    5: {'name': 'Bright Flash',     'bpm': 138},   # Mega Man 4 · Bright Man
    6: {'name': 'Gemini Mirror',    'bpm': 132},   # Mega Man 3 · Gemini Man
    7: {'name': 'Sky World',        'bpm': 148},   # Super Mario Bros 3 · Athletic
    8: {'name': 'Hyrule March',     'bpm': 112},   # Zelda / Ocarina of Time · Overworld
    9: {'name': 'Guardia Festival', 'bpm': 130},   # Chrono Trigger · Millennial Fair
}
