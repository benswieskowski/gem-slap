"""
AURA - Game Data
All level patterns, musical phrases, scoring constants, and note config.

71 levels total: 30 new shapes (sorted easy→hard) + 41 original shapes (sorted easy→hard)
New shapes use up to 12 crystals.
Original shapes: removed % Percent, ∞ Infinity, Whole Note, Repeat Sign,
                 Treble Clef, Bass Clef, Star (was hexagon), Cygnus, Gemini.
Fixed: Turtle — fourth back leg added at (74, 66)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS ASPECT RATIO — CRITICAL DESIGN RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  The game canvas is ~390pt wide × ~673pt tall (after header/footer).
  This means:
    1 x-unit = 3.90pt
    1 y-unit = 6.73pt  ← y is 1.73x TALLER per unit than x

  ⚠ DO NOT use equal Δx and Δy for diagonal steps. A step of (8,8)
    appears at 60° from horizontal (nearly vertical!), not 45°.

  For a VISUALLY balanced 45° diagonal: Δx ≈ 1.73 × Δy
  
  Canonical connected diagonal steps (crystal radius=18pt, target gap ≤15pt):
    Δ(9,5)  → dist=48.6pt, gap=12.6pt, visual angle=43.8°  ← recommended
    Δ(7,4)  → dist=38.3pt, gap= 2.3pt, visual angle=44.6°  ← tight/touching
    Δ(10,6) → dist=56.1pt, gap=20.1pt, visual angle=46.0°  ← slightly gappy

  For horizontal bars, every 9–12 x-units is ideal (35–47pt, gap 0–11pt).
  For vertical bars, every 5–7 y-units is ideal (34–47pt, gap 0–11pt).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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

NOTE_COLORS = {
    -5: '#F03028',
    -2: '#F03028',
     0: '#F03028',
     3: '#F57828',
     5: '#28D858',
     7: '#18C8F8',
    10: '#5038E8',
    12: '#A020E0',
    15: '#A020E0',
    17: '#A020E0',
    19: '#A020E0',
    22: '#A020E0',
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
# NEW SHAPES (levels 1–30) — sorted easy→hard
# score = crystals × 0.6 + normalised_spread × 0.4
# ═══════════════════════════════════════════════════════════════
NEW_PATTERNS = [

    # 1 · Lightning Bolt · 10 crystals
    # True ⚡ shape: single tip → long diagonal → short rightward kink → long diagonal → single tail
    #
    # KEY INSIGHT v3: Previous fix used step(-9,+5) = 44° from horizontal.
    # That made the bolt run nearly DIAGONALLY across the screen — wider than tall!
    # Pixel dimensions: 176pt wide × 236pt tall (aspect 1.34) — looks like a diagonal line.
    #
    # FIX: Use step(-5,+6) = 64° from horizontal (26° from vertical).
    # Each diagonal leans mostly DOWNWARD with a small leftward drift — like a real bolt.
    # New pixel dimensions: 78pt wide × 283pt tall (aspect 3.6) — clearly vertical ✓
    #
    # Layout (all diagonals use step(-5,+6) = visual 64°, gap=8.8pt):
    #   Tip:            (60,27)                          — single upper-right point
    #   Upper diagonal: (55,33)·(50,39)·(45,45)·(40,51) — 4 steps down-left
    #   Rightward kink: (40,51)·(49,51)·(58,51)         — 2 steps right (+9,0)
    #   Lower diagonal: (53,57)·(48,63)·(43,69)         — 3 steps down-left from kink-R
    #   (58,51)→(53,57) is the kink-R→first-lower-diag junction
    {'name': 'Lightning Bolt', 'cells': [
        {'x': 60, 'y': 27},
        {'x': 55, 'y': 33}, {'x': 50, 'y': 39}, {'x': 45, 'y': 45}, {'x': 40, 'y': 51},
        {'x': 49, 'y': 51}, {'x': 58, 'y': 51},
        {'x': 53, 'y': 57}, {'x': 48, 'y': 63}, {'x': 43, 'y': 69},
    ]},

    # 2 · Bullseye · 12 crystals
    # Center + inner 4-dot ring + outer 7-dot ring — three concentric tiers = target
    #
    # ASPECT RATIO KEY: For a ring to appear circular, x-radius must be 1.73× y-radius.
    #   Inner ring: rx=8 units (31pt), ry=5 units (34pt) → visually ~round ✓
    #   Outer ring: rx=14 units (55pt), ry=8 units (54pt) → visually ~round ✓
    #
    # Inner ring (4 dots, 45° rotated diamond): centers are literally touching the center
    # crystal (gap=−0.3pt) — this is intentional, making it read as a tight inner ring.
    # Outer ring uses 7 evenly-spaced dots (51.4° apart) so all edge gaps ≤15.5pt ✓
    # Inner is 45° diamond, outer is 0°-offset heptagon — clearly two separate rings.
    {'name': 'Bullseye', 'cells': [
        {'x': 50, 'y': 50},                                             # center
        {'x': 56, 'y': 54}, {'x': 44, 'y': 54},                        # inner ring (bottom)
        {'x': 44, 'y': 46}, {'x': 56, 'y': 46},                        # inner ring (top)
        {'x': 64, 'y': 50}, {'x': 59, 'y': 56}, {'x': 47, 'y': 58},  # outer ring (right arc)
        {'x': 37, 'y': 53}, {'x': 37, 'y': 47},                        # outer ring (left)
        {'x': 47, 'y': 42}, {'x': 59, 'y': 44},                        # outer ring (top arc)
    ]},

    # 3 · Eye · 12 crystals
    # Almond/lens outline with pointed left+right tips — no pupil (empty interior)
    #
    # ASPECT RATIO FIX: old design had x-span=44, y-span=40 → 172pt × 269pt (taller than wide!)
    # New design:  x-span=52 units (203pt),  y-span=18 units (121pt)  → W/H = 1.67 ✓
    # For x-span 52 units and y-span 18 units the shape is clearly wider than tall,
    # like a real eye. All arc gaps ≤11pt, all tip→arc gaps ≤5pt.
    #
    # Tips: (24,50) and (76,50) — extreme left and right points of the almond
    # Upper arc: 5 dots curving from left tip to right tip through y=41 (apex)
    # Lower arc: 5 dots curving from right tip to left tip through y=59 (nadir)
    # No pupil — the empty interior and pointed tips distinguish this from Bullseye
    {'name': 'Eye', 'cells': [
        {'x': 24, 'y': 50}, {'x': 76, 'y': 50},                        # left and right tips
        {'x': 30, 'y': 45}, {'x': 38, 'y': 42}, {'x': 50, 'y': 41},  # upper arc
        {'x': 62, 'y': 42}, {'x': 70, 'y': 45},                        # upper arc (right)
        {'x': 70, 'y': 55}, {'x': 62, 'y': 58}, {'x': 50, 'y': 59},  # lower arc
        {'x': 38, 'y': 58}, {'x': 30, 'y': 55},                        # lower arc (left)
    ]},

    # 4 · Crescent · 10 crystals
    {'name': 'Crescent', 'cells': [
        {'x': 52, 'y': 24}, {'x': 64, 'y': 28}, {'x': 74, 'y': 42},
        {'x': 76, 'y': 56}, {'x': 66, 'y': 70}, {'x': 52, 'y': 76},
        {'x': 44, 'y': 30}, {'x': 36, 'y': 44},
        {'x': 36, 'y': 58}, {'x': 44, 'y': 70},
    ]},

    # 5 · Compass · score 5.617 · 9 crystals
    {'name': 'Compass', 'cells': [
        {'x': 50, 'y': 24}, {'x': 76, 'y': 50}, {'x': 50, 'y': 76}, {'x': 24, 'y': 50},
        {'x': 62, 'y': 38}, {'x': 62, 'y': 62}, {'x': 38, 'y': 62}, {'x': 38, 'y': 38},
        {'x': 50, 'y': 50},
    ]},

    # 6 · Arch · score 5.678 · 9 crystals
    {'name': 'Arch', 'cells': [
        {'x': 30, 'y': 72}, {'x': 30, 'y': 60}, {'x': 30, 'y': 48},
        {'x': 38, 'y': 36}, {'x': 50, 'y': 28}, {'x': 62, 'y': 36},
        {'x': 70, 'y': 48}, {'x': 70, 'y': 60}, {'x': 70, 'y': 72},
    ]},

    # 7 · Bowtie · 10 crystals
    {'name': 'Bowtie', 'cells': [
        {'x': 26, 'y': 30}, {'x': 74, 'y': 30},
        {'x': 38, 'y': 38}, {'x': 62, 'y': 38},
        {'x': 44, 'y': 50}, {'x': 56, 'y': 50},
        {'x': 38, 'y': 62}, {'x': 62, 'y': 62},
        {'x': 26, 'y': 70}, {'x': 74, 'y': 70},
    ]},

    # 8 · Parabola · 12 crystals
    {'name': 'Parabola', 'cells': [
        {'x': 50, 'y': 76},
        {'x': 44, 'y': 68}, {'x': 56, 'y': 68},
        {'x': 36, 'y': 58}, {'x': 64, 'y': 58},
        {'x': 28, 'y': 46}, {'x': 72, 'y': 46},
        {'x': 26, 'y': 32}, {'x': 74, 'y': 32},
        {'x': 36, 'y': 24}, {'x': 50, 'y': 24}, {'x': 64, 'y': 24},
    ]},

    # 9 · Hourglass · score 5.726 · 11 crystals
    {'name': 'Hourglass', 'cells': [
        {'x': 26, 'y': 24}, {'x': 50, 'y': 24}, {'x': 74, 'y': 24},
        {'x': 38, 'y': 36}, {'x': 62, 'y': 36},
        {'x': 50, 'y': 50},
        {'x': 38, 'y': 64}, {'x': 62, 'y': 64},
        {'x': 26, 'y': 76}, {'x': 50, 'y': 76}, {'x': 74, 'y': 76},
    ]},

    # 10 · Magnet · 11 crystals
    {'name': 'Magnet', 'cells': [
        {'x': 38, 'y': 24}, {'x': 50, 'y': 20}, {'x': 62, 'y': 24},
        {'x': 30, 'y': 32}, {'x': 70, 'y': 32},
        {'x': 28, 'y': 46}, {'x': 72, 'y': 46},
        {'x': 28, 'y': 60}, {'x': 72, 'y': 60},
        {'x': 28, 'y': 72}, {'x': 72, 'y': 72},
    ]},

    # 11 · Trident · score 6.034 · 10 crystals
    {'name': 'Trident', 'cells': [
        {'x': 50, 'y': 74}, {'x': 50, 'y': 62},
        {'x': 36, 'y': 52}, {'x': 50, 'y': 52}, {'x': 64, 'y': 52},
        {'x': 36, 'y': 40}, {'x': 36, 'y': 28},
        {'x': 64, 'y': 40}, {'x': 64, 'y': 28},
        {'x': 50, 'y': 40}, {'x': 50, 'y': 28},
    ]},

    # 12 · Pawn · 12 crystals
    {'name': 'Pawn', 'cells': [
        {'x': 50, 'y': 24},
        {'x': 40, 'y': 30}, {'x': 60, 'y': 30},
        {'x': 36, 'y': 40}, {'x': 64, 'y': 40},
        {'x': 42, 'y': 50}, {'x': 58, 'y': 50},
        {'x': 36, 'y': 60}, {'x': 64, 'y': 60},
        {'x': 34, 'y': 70}, {'x': 50, 'y': 70}, {'x': 66, 'y': 70},
    ]},

    # 13 · Martini · 12 crystals
    {'name': 'Martini', 'cells': [
        {'x': 34, 'y': 26}, {'x': 50, 'y': 26}, {'x': 66, 'y': 26},
        {'x': 40, 'y': 36}, {'x': 60, 'y': 36},
        {'x': 44, 'y': 46}, {'x': 56, 'y': 46},
        {'x': 50, 'y': 56},
        {'x': 50, 'y': 66},
        {'x': 36, 'y': 74}, {'x': 50, 'y': 74}, {'x': 64, 'y': 74},
    ]},

    # 14 · Rocket · 11 crystals
    {'name': 'Rocket', 'cells': [
        {'x': 50, 'y': 24},
        {'x': 42, 'y': 32}, {'x': 58, 'y': 32},
        {'x': 40, 'y': 44}, {'x': 60, 'y': 44},
        {'x': 40, 'y': 56}, {'x': 60, 'y': 56},
        {'x': 30, 'y': 64}, {'x': 70, 'y': 64},
        {'x': 36, 'y': 74}, {'x': 64, 'y': 74},
    ]},

    # 15 · Peace Sign · 12 crystals
    {'name': 'Peace Sign', 'cells': [
        {'x': 50, 'y': 28}, {'x': 66, 'y': 34}, {'x': 72, 'y': 50},
        {'x': 66, 'y': 66}, {'x': 50, 'y': 72}, {'x': 34, 'y': 66},
        {'x': 28, 'y': 50}, {'x': 34, 'y': 34},
        {'x': 50, 'y': 38}, {'x': 50, 'y': 50},
        {'x': 40, 'y': 62}, {'x': 60, 'y': 62},
    ]},

    # 16 · Ice Cream Cone · 11 crystals
    {'name': 'Ice Cream Cone', 'cells': [
        {'x': 50, 'y': 28}, {'x': 62, 'y': 32}, {'x': 70, 'y': 46},
        {'x': 38, 'y': 32}, {'x': 30, 'y': 46},
        {'x': 34, 'y': 56}, {'x': 50, 'y': 56}, {'x': 66, 'y': 56},
        {'x': 40, 'y': 67}, {'x': 60, 'y': 67},
        {'x': 50, 'y': 76},
    ]},

    # 17 · Flame · 10 crystals
    {'name': 'Flame', 'cells': [
        {'x': 50, 'y': 72}, {'x': 38, 'y': 66}, {'x': 62, 'y': 66},
        {'x': 30, 'y': 56}, {'x': 70, 'y': 56},
        {'x': 34, 'y': 44}, {'x': 66, 'y': 44},
        {'x': 40, 'y': 34}, {'x': 60, 'y': 34},
        {'x': 50, 'y': 24},
    ]},

    # 18 · Mountain · 12 crystals
    {'name': 'Mountain', 'cells': [
        {'x': 26, 'y': 70}, {'x': 38, 'y': 70}, {'x': 50, 'y': 70},
        {'x': 62, 'y': 70}, {'x': 74, 'y': 70},
        {'x': 28, 'y': 54}, {'x': 32, 'y': 40},
        {'x': 40, 'y': 50}, {'x': 50, 'y': 58},
        {'x': 60, 'y': 50}, {'x': 68, 'y': 40}, {'x': 72, 'y': 54},
    ]},

    # 19 · Heart · 12 crystals
    {'name': 'Heart', 'cells': [
        {'x': 36, 'y': 28}, {'x': 50, 'y': 36}, {'x': 64, 'y': 28},
        {'x': 30, 'y': 36}, {'x': 70, 'y': 36},
        {'x': 28, 'y': 44}, {'x': 72, 'y': 44},
        {'x': 28, 'y': 58}, {'x': 72, 'y': 58},
        {'x': 38, 'y': 68}, {'x': 62, 'y': 68},
        {'x': 50, 'y': 76},
    ]},

    # 20 · Mushroom · 12 crystals
    {'name': 'Mushroom', 'cells': [
        {'x': 50, 'y': 26},
        {'x': 38, 'y': 30}, {'x': 30, 'y': 42}, {'x': 34, 'y': 56},
        {'x': 62, 'y': 30}, {'x': 70, 'y': 42}, {'x': 66, 'y': 56},
        {'x': 50, 'y': 56},
        {'x': 42, 'y': 64}, {'x': 58, 'y': 64},
        {'x': 44, 'y': 74}, {'x': 56, 'y': 74},
    ]},

    # 21 · Bell · 11 crystals
    {'name': 'Bell', 'cells': [
        {'x': 50, 'y': 24},
        {'x': 38, 'y': 28}, {'x': 28, 'y': 40}, {'x': 30, 'y': 56}, {'x': 34, 'y': 68},
        {'x': 62, 'y': 28}, {'x': 72, 'y': 40}, {'x': 70, 'y': 56}, {'x': 66, 'y': 68},
        {'x': 50, 'y': 68},
        {'x': 50, 'y': 76},
    ]},

    # 22 · UFO · 12 crystals
    {'name': 'UFO', 'cells': [
        {'x': 40, 'y': 44}, {'x': 50, 'y': 38}, {'x': 60, 'y': 44},
        {'x': 38, 'y': 50}, {'x': 50, 'y': 48}, {'x': 62, 'y': 50},
        {'x': 30, 'y': 56}, {'x': 50, 'y': 56}, {'x': 70, 'y': 56},
        {'x': 34, 'y': 64}, {'x': 50, 'y': 66}, {'x': 66, 'y': 64},
    ]},

    # 23 · Cactus · 11 crystals
    {'name': 'Cactus', 'cells': [
        {'x': 50, 'y': 72}, {'x': 50, 'y': 60}, {'x': 50, 'y': 48},
        {'x': 50, 'y': 36}, {'x': 50, 'y': 24},
        {'x': 38, 'y': 48}, {'x': 30, 'y': 48}, {'x': 30, 'y': 36},
        {'x': 62, 'y': 48}, {'x': 70, 'y': 48}, {'x': 70, 'y': 36},
    ]},

    # 24 · Thumbs Up · 12 crystals
    {'name': 'Thumbs Up', 'cells': [
        {'x': 38, 'y': 74}, {'x': 52, 'y': 74},
        {'x': 64, 'y': 70}, {'x': 66, 'y': 58}, {'x': 64, 'y': 50},
        {'x': 52, 'y': 50}, {'x': 40, 'y': 50},
        {'x': 34, 'y': 60},
        {'x': 34, 'y': 40}, {'x': 32, 'y': 28},
        {'x': 38, 'y': 24}, {'x': 46, 'y': 24},
    ]},

    # 25 · Anchor · 12 crystals
    {'name': 'Anchor', 'cells': [
        {'x': 50, 'y': 24},
        {'x': 64, 'y': 30}, {'x': 70, 'y': 44}, {'x': 62, 'y': 56},
        {'x': 50, 'y': 60},
        {'x': 38, 'y': 56}, {'x': 30, 'y': 44}, {'x': 36, 'y': 30},
        {'x': 50, 'y': 64},
        {'x': 38, 'y': 64}, {'x': 62, 'y': 64},
        {'x': 50, 'y': 74},
    ]},

    # 26 · Pyramid · 11 crystals
    {'name': 'Pyramid', 'cells': [
        {'x': 50, 'y': 24},
        {'x': 42, 'y': 38}, {'x': 58, 'y': 38},
        {'x': 34, 'y': 52}, {'x': 50, 'y': 52}, {'x': 66, 'y': 52},
        {'x': 28, 'y': 66}, {'x': 38, 'y': 66}, {'x': 50, 'y': 66},
        {'x': 62, 'y': 66}, {'x': 72, 'y': 66},
    ]},

    # 27 · Fork · score 7.238 · 12 crystals
    {'name': 'Fork', 'cells': [
        {'x': 50, 'y': 74}, {'x': 50, 'y': 64}, {'x': 50, 'y': 54},
        {'x': 40, 'y': 44}, {'x': 50, 'y': 44}, {'x': 60, 'y': 44},
        {'x': 36, 'y': 34}, {'x': 34, 'y': 24},
        {'x': 50, 'y': 34}, {'x': 50, 'y': 24},
        {'x': 64, 'y': 34}, {'x': 66, 'y': 24},
    ]},

    # 28 · Saturn · 12 crystals
    {'name': 'Saturn', 'cells': [
        {'x': 50, 'y': 36}, {'x': 62, 'y': 44}, {'x': 64, 'y': 56},
        {'x': 50, 'y': 64}, {'x': 38, 'y': 56}, {'x': 36, 'y': 44},
        {'x': 26, 'y': 62}, {'x': 36, 'y': 56}, {'x': 46, 'y': 50},
        {'x': 54, 'y': 48}, {'x': 64, 'y': 42}, {'x': 74, 'y': 36},
    ]},

    # 29 · Happy Face · 12 crystals
    {'name': 'Happy Face', 'cells': [
        {'x': 50, 'y': 26}, {'x': 63, 'y': 31}, {'x': 68, 'y': 44},
        {'x': 63, 'y': 57}, {'x': 37, 'y': 57},
        {'x': 32, 'y': 44}, {'x': 37, 'y': 31},
        {'x': 40, 'y': 40}, {'x': 60, 'y': 40},
        {'x': 38, 'y': 66}, {'x': 50, 'y': 72}, {'x': 62, 'y': 66},
    ]},

    # 30 · Eiffel Tower · 12 crystals
    {'name': 'Eiffel Tower', 'cells': [
        {'x': 50, 'y': 24},
        {'x': 45, 'y': 34}, {'x': 55, 'y': 34},
        {'x': 41, 'y': 46}, {'x': 59, 'y': 46},
        {'x': 36, 'y': 58}, {'x': 50, 'y': 64}, {'x': 64, 'y': 58},
        {'x': 31, 'y': 70}, {'x': 69, 'y': 70},
        {'x': 26, 'y': 76}, {'x': 74, 'y': 76},
    ]},
]


# ═══════════════════════════════════════════════════════════════
# ORIGINAL 41 LEVELS (levels 31–71) — sorted easy→hard
# score = crystals × 0.6 + normalised_spread × 0.4
# ═══════════════════════════════════════════════════════════════
ORIGINAL_PATTERNS = [

    # 31 · Triangle · score 1.800 · 3 crystals
    {'name': 'Triangle', 'cells': [
        {'x': 50, 'y': 36}, {'x': 38, 'y': 60}, {'x': 62, 'y': 60},
    ]},

    # 32 · Line · score 2.468 · 4 crystals
    {'name': 'Line', 'cells': [
        {'x': 25, 'y': 50}, {'x': 42, 'y': 50}, {'x': 58, 'y': 50}, {'x': 75, 'y': 50},
    ]},

    # 33 · Crux · score 2.728 · 4 crystals
    {'name': 'Crux', 'cells': [
        {'x': 55, 'y': 76}, {'x': 32, 'y': 47}, {'x': 50, 'y': 24}, {'x': 68, 'y': 39},
    ]},

    # 34 · Square · score 2.735 · 4 crystals
    {'name': 'Square', 'cells': [
        {'x': 34, 'y': 34}, {'x': 66, 'y': 34}, {'x': 34, 'y': 66}, {'x': 66, 'y': 66},
    ]},

    # 35 · Diamond · score 2.751 · 4 crystals
    {'name': 'Diamond', 'cells': [
        {'x': 50, 'y': 27}, {'x': 27, 'y': 50}, {'x': 73, 'y': 50}, {'x': 50, 'y': 73},
    ]},

    # 36 · Quarter Note · score 3.003 · 5 crystals
    {'name': 'Quarter Note', 'cells': [
        {'x': 44, 'y': 68}, {'x': 51, 'y': 64}, {'x': 53, 'y': 52},
        {'x': 53, 'y': 38}, {'x': 53, 'y': 24},
    ]},

    # 37 · Cross · score 3.046 · 5 crystals
    {'name': 'Cross', 'cells': [
        {'x': 50, 'y': 30}, {'x': 30, 'y': 50}, {'x': 50, 'y': 50},
        {'x': 70, 'y': 50}, {'x': 50, 'y': 70},
    ]},

    # 38 · Cassiopeia · score 3.145 · 5 crystals
    {'name': 'Cassiopeia', 'cells': [
        {'x': 76, 'y': 53}, {'x': 60, 'y': 66}, {'x': 51, 'y': 49},
        {'x': 36, 'y': 50}, {'x': 24, 'y': 34},
    ]},

    # 39 · Lyra · score 3.354 · 5 crystals
    {'name': 'Lyra', 'cells': [
        {'x': 69, 'y': 24}, {'x': 56, 'y': 34}, {'x': 39, 'y': 40},
        {'x': 47, 'y': 70}, {'x': 31, 'y': 76},
    ]},

    # 40 · Arrow · score 3.360 · 5 crystals
    {'name': 'Arrow', 'cells': [
        {'x': 25, 'y': 42}, {'x': 25, 'y': 58}, {'x': 50, 'y': 28},
        {'x': 50, 'y': 72}, {'x': 73, 'y': 50},
    ]},

    # 41 · Pentagon · score 3.363 · 5 crystals
    {'name': 'Pentagon', 'cells': [
        {'x': 50, 'y': 29}, {'x': 72, 'y': 45}, {'x': 64, 'y': 71},
        {'x': 36, 'y': 71}, {'x': 28, 'y': 45},
    ]},

    # 42 · Eighth Note · score 3.664 · 6 crystals
    {'name': 'Eighth Note', 'cells': [
        {'x': 38, 'y': 72}, {'x': 45, 'y': 68}, {'x': 47, 'y': 56},
        {'x': 47, 'y': 38}, {'x': 61, 'y': 36}, {'x': 69, 'y': 47},
    ]},

    # 43 · Leo · score 3.723 · 6 crystals
    {'name': 'Leo', 'cells': [
        {'x': 76, 'y': 39}, {'x': 62, 'y': 47}, {'x': 68, 'y': 52},
        {'x': 68, 'y': 61}, {'x': 40, 'y': 45}, {'x': 24, 'y': 55},
    ]},

    # 44 · Hexagon · score 4.000 · 6 crystals
    {'name': 'Hexagon', 'cells': [
        {'x': 50, 'y': 26}, {'x': 71, 'y': 38}, {'x': 71, 'y': 62},
        {'x': 50, 'y': 74}, {'x': 29, 'y': 62}, {'x': 29, 'y': 38},
    ]},

    # 45 · Flat · score 4.236 · 7 crystals
    {'name': 'Flat', 'cells': [
        {'x': 38, 'y': 26}, {'x': 38, 'y': 40}, {'x': 38, 'y': 54}, {'x': 38, 'y': 68},
        {'x': 52, 'y': 52}, {'x': 58, 'y': 64}, {'x': 44, 'y': 74},
    ]},

    # 46 · Big Dipper · score 4.346 · 7 crystals
    {'name': 'Big Dipper', 'cells': [
        {'x': 22, 'y': 54}, {'x': 28, 'y': 65}, {'x': 45, 'y': 60}, {'x': 45, 'y': 50},
        {'x': 55, 'y': 43}, {'x': 62, 'y': 36}, {'x': 78, 'y': 35},
    ]},

    # 47 · Fermata · score 4.485 · 7 crystals
    {'name': 'Fermata', 'cells': [
        {'x': 24, 'y': 54}, {'x': 32, 'y': 36}, {'x': 42, 'y': 27}, {'x': 58, 'y': 27},
        {'x': 68, 'y': 36}, {'x': 76, 'y': 54}, {'x': 50, 'y': 63},
    ]},

    # 48 · Snowflake · score 4.488 · 7 crystals
    {'name': 'Snowflake', 'cells': [
        {'x': 50, 'y': 50}, {'x': 50, 'y': 25}, {'x': 72, 'y': 38},
        {'x': 72, 'y': 62}, {'x': 50, 'y': 75}, {'x': 28, 'y': 63}, {'x': 28, 'y': 38},
    ]},

    # 49 · Corona Borealis · score 4.512 · 7 crystals
    {'name': 'Corona Borealis', 'cells': [
        {'x': 68, 'y': 31}, {'x': 76, 'y': 47}, {'x': 66, 'y': 64}, {'x': 53, 'y': 67},
        {'x': 42, 'y': 69}, {'x': 30, 'y': 63}, {'x': 24, 'y': 42},
    ]},

    # 50 · Fish · score 4.965 · 8 crystals
    {'name': 'Fish', 'cells': [
        {'x': 26, 'y': 50}, {'x': 36, 'y': 43}, {'x': 48, 'y': 36}, {'x': 62, 'y': 40},
        {'x': 48, 'y': 64}, {'x': 62, 'y': 60}, {'x': 74, 'y': 38}, {'x': 74, 'y': 62},
    ]},

    # 51 · Scorpius · score 5.012 · 8 crystals
    {'name': 'Scorpius', 'cells': [
        {'x': 70, 'y': 24}, {'x': 72, 'y': 30}, {'x': 61, 'y': 36}, {'x': 57, 'y': 38},
        {'x': 54, 'y': 42}, {'x': 47, 'y': 55}, {'x': 28, 'y': 76}, {'x': 28, 'y': 63},
    ]},

    # 52 · = Equals · score 5.014 · 8 crystals
    {'name': '= Equals', 'cells': [
        {'x': 25, 'y': 40}, {'x': 42, 'y': 40}, {'x': 58, 'y': 40}, {'x': 75, 'y': 40},
        {'x': 25, 'y': 60}, {'x': 42, 'y': 60}, {'x': 58, 'y': 60}, {'x': 75, 'y': 60},
    ]},

    # 53 · Sharp · score 5.021 · 8 crystals
    {'name': 'Sharp', 'cells': [
        {'x': 40, 'y': 27}, {'x': 37, 'y': 69}, {'x': 56, 'y': 23}, {'x': 53, 'y': 65},
        {'x': 31, 'y': 40}, {'x': 62, 'y': 36}, {'x': 31, 'y': 56}, {'x': 62, 'y': 52},
    ]},

    # 54 · Beamed Notes · score 5.082 · 8 crystals
    {'name': 'Beamed Notes', 'cells': [
        {'x': 26, 'y': 74}, {'x': 33, 'y': 70}, {'x': 35, 'y': 56}, {'x': 35, 'y': 34},
        {'x': 63, 'y': 28}, {'x': 63, 'y': 50}, {'x': 60, 'y': 66}, {'x': 67, 'y': 62},
    ]},

    # 55 · Δ Delta · score 5.173 · 8 crystals
    {'name': 'Δ Delta', 'cells': [
        {'x': 50, 'y': 25}, {'x': 38, 'y': 42}, {'x': 62, 'y': 42}, {'x': 29, 'y': 58},
        {'x': 71, 'y': 58}, {'x': 26, 'y': 74}, {'x': 50, 'y': 74}, {'x': 74, 'y': 74},
    ]},

    # 56 · Orion · score 5.447 · 9 crystals
    {'name': 'Orion', 'cells': [
        {'x': 50, 'y': 24}, {'x': 37, 'y': 31}, {'x': 56, 'y': 34}, {'x': 52, 'y': 51},
        {'x': 49, 'y': 54}, {'x': 46, 'y': 55}, {'x': 50, 'y': 65}, {'x': 42, 'y': 76},
        {'x': 63, 'y': 72},
    ]},

    # 57 · Swan · score 5.453 · 9 crystals
    {'name': 'Swan', 'cells': [
        {'x': 68, 'y': 26}, {'x': 62, 'y': 34}, {'x': 54, 'y': 42}, {'x': 46, 'y': 50},
        {'x': 30, 'y': 52}, {'x': 34, 'y': 62}, {'x': 48, 'y': 68}, {'x': 62, 'y': 64},
        {'x': 50, 'y': 56},
    ]},

    # 58 · + Plus · score 5.485 · 9 crystals
    {'name': '+ Plus', 'cells': [
        {'x': 50, 'y': 25}, {'x': 50, 'y': 37}, {'x': 25, 'y': 50}, {'x': 37, 'y': 50},
        {'x': 50, 'y': 50}, {'x': 63, 'y': 50}, {'x': 75, 'y': 50}, {'x': 50, 'y': 63},
        {'x': 50, 'y': 75},
    ]},

    # 59 · Bird · score 5.506 · 9 crystals
    {'name': 'Bird', 'cells': [
        {'x': 24, 'y': 44}, {'x': 35, 'y': 30}, {'x': 43, 'y': 40}, {'x': 50, 'y': 46},
        {'x': 57, 'y': 40}, {'x': 65, 'y': 30}, {'x': 76, 'y': 44}, {'x': 44, 'y': 66},
        {'x': 56, 'y': 66},
    ]},

    # 60 · θ Theta · score 5.542 · 9 crystals
    {'name': 'θ Theta', 'cells': [
        {'x': 50, 'y': 27}, {'x': 69, 'y': 38}, {'x': 69, 'y': 62}, {'x': 50, 'y': 73},
        {'x': 31, 'y': 62}, {'x': 31, 'y': 38}, {'x': 36, 'y': 50}, {'x': 50, 'y': 50},
        {'x': 64, 'y': 50},
    ]},

    # 61 · Rabbit · score 5.615 · 9 crystals
    {'name': 'Rabbit', 'cells': [
        {'x': 40, 'y': 24}, {'x': 42, 'y': 36}, {'x': 58, 'y': 36}, {'x': 60, 'y': 24},
        {'x': 50, 'y': 48}, {'x': 50, 'y': 64}, {'x': 36, 'y': 74}, {'x': 64, 'y': 74},
        {'x': 68, 'y': 60},
    ]},

    # 62 · √ Root · score 5.685 · 9 crystals
    {'name': '√ Root', 'cells': [
        {'x': 23, 'y': 56}, {'x': 30, 'y': 64}, {'x': 36, 'y': 72}, {'x': 43, 'y': 61},
        {'x': 50, 'y': 49}, {'x': 56, 'y': 35}, {'x': 61, 'y': 30}, {'x': 70, 'y': 30},
        {'x': 78, 'y': 30},
    ]},

    # 63 · Σ Sigma · score 5.696 · 9 crystals
    {'name': 'Σ Sigma', 'cells': [
        {'x': 33, 'y': 28}, {'x': 51, 'y': 28}, {'x': 70, 'y': 28}, {'x': 54, 'y': 40},
        {'x': 35, 'y': 50}, {'x': 54, 'y': 60}, {'x': 33, 'y': 72}, {'x': 51, 'y': 72},
        {'x': 70, 'y': 72},
    ]},

    # 64 · × Times · score 5.709 · 9 crystals
    {'name': '× Times', 'cells': [
        {'x': 28, 'y': 26}, {'x': 39, 'y': 37}, {'x': 61, 'y': 37}, {'x': 72, 'y': 26},
        {'x': 50, 'y': 50}, {'x': 39, 'y': 63}, {'x': 28, 'y': 74}, {'x': 61, 'y': 63},
        {'x': 72, 'y': 74},
    ]},

    # 65 · Butterfly · score 6.166 · 10 crystals
    {'name': 'Butterfly', 'cells': [
        {'x': 26, 'y': 38}, {'x': 36, 'y': 26}, {'x': 64, 'y': 26}, {'x': 74, 'y': 38},
        {'x': 40, 'y': 46}, {'x': 60, 'y': 46}, {'x': 50, 'y': 42}, {'x': 50, 'y': 60},
        {'x': 32, 'y': 64}, {'x': 68, 'y': 64},
    ]},

    # 66 · Crab · score 6.210 · 10 crystals
    {'name': 'Crab', 'cells': [
        {'x': 22, 'y': 28}, {'x': 28, 'y': 40}, {'x': 36, 'y': 50}, {'x': 44, 'y': 58},
        {'x': 50, 'y': 54}, {'x': 56, 'y': 58}, {'x': 64, 'y': 50}, {'x': 72, 'y': 40},
        {'x': 78, 'y': 28}, {'x': 50, 'y': 72},
    ]},

    # 67 · Snail · score 6.286 · 10 crystals
    {'name': 'Snail', 'cells': [
        {'x': 64, 'y': 28}, {'x': 76, 'y': 44}, {'x': 74, 'y': 60}, {'x': 62, 'y': 70},
        {'x': 50, 'y': 64}, {'x': 60, 'y': 50}, {'x': 42, 'y': 72}, {'x': 30, 'y': 70},
        {'x': 26, 'y': 60}, {'x': 24, 'y': 48},
    ]},

    # 68 · Whale · score 6.299 · 10 crystals
    {'name': 'Whale', 'cells': [
        {'x': 24, 'y': 50}, {'x': 26, 'y': 58}, {'x': 32, 'y': 42}, {'x': 42, 'y': 32},
        {'x': 56, 'y': 28}, {'x': 68, 'y': 32}, {'x': 44, 'y': 58}, {'x': 60, 'y': 60},
        {'x': 76, 'y': 38}, {'x': 76, 'y': 62},
    ]},

    # 69 · Spider · score 6.350 · 10 crystals
    {'name': 'Spider', 'cells': [
        {'x': 50, 'y': 38}, {'x': 50, 'y': 58}, {'x': 34, 'y': 28}, {'x': 24, 'y': 36},
        {'x': 30, 'y': 52}, {'x': 22, 'y': 62}, {'x': 66, 'y': 28}, {'x': 76, 'y': 36},
        {'x': 70, 'y': 52}, {'x': 78, 'y': 62},
    ]},

    # 70 · π Pi · score 6.377 · 10 crystals
    {'name': 'π Pi', 'cells': [
        {'x': 25, 'y': 30}, {'x': 42, 'y': 30}, {'x': 58, 'y': 30}, {'x': 75, 'y': 30},
        {'x': 35, 'y': 44}, {'x': 32, 'y': 58}, {'x': 29, 'y': 72}, {'x': 65, 'y': 44},
        {'x': 68, 'y': 58}, {'x': 71, 'y': 72},
    ]},

    # 71 · Turtle · score 6.965 · 11 crystals
    {'name': 'Turtle', 'cells': [
        {'x': 50, 'y': 28}, {'x': 38, 'y': 36}, {'x': 62, 'y': 36},
        {'x': 30, 'y': 54}, {'x': 70, 'y': 54},
        {'x': 38, 'y': 68}, {'x': 62, 'y': 68},
        {'x': 24, 'y': 40}, {'x': 76, 'y': 40},
        {'x': 26, 'y': 66}, {'x': 74, 'y': 66},
    ]},
]

ORDERED_PATTERNS = NEW_PATTERNS + ORIGINAL_PATTERNS


# ═══════════════════════════════════════════════════════════════
# LEVEL BATCHES
# ═══════════════════════════════════════════════════════════════
LEVEL_BATCHES = [
    {'name': '', 'patterns': ORDERED_PATTERNS},
]


# ═══════════════════════════════════════════════════════════════
# BASS STYLES
# ═══════════════════════════════════════════════════════════════
BASS_STYLES = {
    0: {'name': "Wily's Resolve",   'bpm': 150},
    1: {'name': 'Fourside Funk',    'bpm': 108},
    2: {'name': 'Snake Slither',    'bpm': 126},
    3: {'name': 'Pharaoh Rush',     'bpm': 144},
    4: {'name': 'Hard Corps',       'bpm': 150},
    5: {'name': 'Bright Flash',     'bpm': 138},
    6: {'name': 'Gemini Mirror',    'bpm': 132},
    7: {'name': 'Sky World',        'bpm': 148},
    8: {'name': 'Hyrule March',     'bpm': 112},
    9: {'name': 'Guardia Festival', 'bpm': 130},
}
