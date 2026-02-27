"""
AURA - Game Data
All level patterns, musical phrases, scoring constants, and note config.

71 levels total: 30 new shapes (sorted easy→hard) + 41 original shapes (sorted easy→hard)
New shapes use up to 12 crystals.
Original shapes: removed % Percent, ∞ Infinity, Whole Note, Repeat Sign,
                 Treble Clef, Bass Clef, Star (was hexagon), Cygnus, Gemini.
Fixed: Turtle — fourth back leg added at (74, 66)
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
    # Z-shape: 3-dot top bar (right) + 4-dot diagonal + 3-dot bottom bar (left)
    # Diagonal starts 8.2 units from top bar end, ends 8.2 units above bottom bar
    # — near-zero visible gap on small screens
    {'name': 'Lightning Bolt', 'cells': [
        {'x': 54, 'y': 26}, {'x': 64, 'y': 26}, {'x': 72, 'y': 26},
        {'x': 70, 'y': 34}, {'x': 62, 'y': 42}, {'x': 54, 'y': 50}, {'x': 46, 'y': 58},
        {'x': 28, 'y': 66}, {'x': 38, 'y': 66}, {'x': 46, 'y': 66},
    ]},

    # 2 · Bullseye · 9 crystals
    # Center + inner ring at 45° (diamond) + outer ring at 0° (cardinal cross)
    # The 45° offset between rings is what makes it read as bullseye/target
    # rather than two nested diamonds
    {'name': 'Bullseye', 'cells': [
        {'x': 50, 'y': 50},
        {'x': 40, 'y': 40}, {'x': 60, 'y': 40}, {'x': 60, 'y': 60}, {'x': 40, 'y': 60},
        {'x': 50, 'y': 26}, {'x': 74, 'y': 50}, {'x': 50, 'y': 74}, {'x': 26, 'y': 50},
    ]},

    # 3 · Eye · 9 crystals
    # Almond outline + pupil. Extreme points pulled to x=28/72 for small-screen safety
    {'name': 'Eye', 'cells': [
        {'x': 28, 'y': 50},
        {'x': 38, 'y': 38}, {'x': 50, 'y': 30}, {'x': 62, 'y': 38},
        {'x': 72, 'y': 50},
        {'x': 62, 'y': 62}, {'x': 50, 'y': 70}, {'x': 38, 'y': 62},
        {'x': 50, 'y': 50},
    ]},

    # 4 · Crescent · 10 crystals
    # Outer arc (6 dots, right-bulging) + inner arc (4 dots, offset left)
    # Key fixes: outer always right of inner at every y; tips 10 units apart
    # (the bottom point 48,74 was left of inner 50,68 — backwards, now corrected)
    {'name': 'Crescent', 'cells': [
        {'x': 52, 'y': 24}, {'x': 64, 'y': 28}, {'x': 74, 'y': 42},  # outer arc top
        {'x': 76, 'y': 56}, {'x': 66, 'y': 70}, {'x': 52, 'y': 76},  # outer arc bottom
        {'x': 44, 'y': 30}, {'x': 36, 'y': 44},                       # inner arc top
        {'x': 36, 'y': 58}, {'x': 44, 'y': 70},                       # inner arc bottom
    ]},

    # 5 · Compass · score 5.617 · 9 crystals
    # Cardinal points at dist=26, diagonal at dist=17 (ratio 1.53:1)
    # Reads as 4-pointed compass star, not octagon
    {'name': 'Compass', 'cells': [
        {'x': 50, 'y': 24}, {'x': 76, 'y': 50}, {'x': 50, 'y': 76}, {'x': 24, 'y': 50},  # cardinal (far)
        {'x': 62, 'y': 38}, {'x': 62, 'y': 62}, {'x': 38, 'y': 62}, {'x': 38, 'y': 38},  # diagonal (near)
        {'x': 50, 'y': 50},  # center
    ]},

    # 6 · Arch · score 5.678 · 9 crystals
    # Two vertical columns + curved top — doorway arch
    {'name': 'Arch', 'cells': [
        {'x': 30, 'y': 72}, {'x': 30, 'y': 60}, {'x': 30, 'y': 48},
        {'x': 38, 'y': 36}, {'x': 50, 'y': 28}, {'x': 62, 'y': 36},
        {'x': 70, 'y': 48}, {'x': 70, 'y': 60}, {'x': 70, 'y': 72},
    ]},

    # 7 · Bowtie · 10 crystals
    # 4 outer corners + 4 diagonal midpoints + 2-dot horizontal knot at center
    # The knot pair (44,50)+(56,50) reads as the tied center of the bow
    # Corners fan outward on diagonals — clearly different from Hourglass (which has
    # flat horizontal bars + vertical diagonals — this has NO horizontal/vertical edges)
    # All gaps 12–14.4u (16–19px edge-to-edge)
    {'name': 'Bowtie', 'cells': [
        {'x': 26, 'y': 30}, {'x': 74, 'y': 30},  # top corners
        {'x': 38, 'y': 38}, {'x': 62, 'y': 38},  # upper diagonal midpoints
        {'x': 44, 'y': 50}, {'x': 56, 'y': 50},  # center knot
        {'x': 38, 'y': 62}, {'x': 62, 'y': 62},  # lower diagonal midpoints
        {'x': 26, 'y': 70}, {'x': 74, 'y': 70},  # bottom corners
    ]},

    # 8 · Parabola · 12 crystals
    # Bowl: vertex at bottom, 4 spreading arm pairs, 3-dot rim at top
    # Old design had arm→rim gap of 16.5u (25px). New: 4 arm pairs bring the
    # outermost arm dots (26,32) close to rim ends (36,24) — max gap 14.4u (19px)
    # All gaps ≤14.4u. Distinguishable from Arch: Arch has straight vertical legs;
    # this has continuously curving arms with a closed top rim (reads as bowl/cup)
    {'name': 'Parabola', 'cells': [
        {'x': 50, 'y': 76},                        # vertex
        {'x': 44, 'y': 68}, {'x': 56, 'y': 68},   # spread 12
        {'x': 36, 'y': 58}, {'x': 64, 'y': 58},   # spread 28
        {'x': 28, 'y': 46}, {'x': 72, 'y': 46},   # spread 44
        {'x': 26, 'y': 32}, {'x': 74, 'y': 32},   # outer arm ends (bridge to rim)
        {'x': 36, 'y': 24}, {'x': 50, 'y': 24}, {'x': 64, 'y': 24},  # 3-dot rim
    ]},

    # 9 · Hourglass · score 5.726 · 11 crystals
    # Top and bottom bars now have 3 dots each — clearly reads as lines, not just corners
    {'name': 'Hourglass', 'cells': [
        {'x': 26, 'y': 24}, {'x': 50, 'y': 24}, {'x': 74, 'y': 24},  # top bar (3 dots)
        {'x': 38, 'y': 36}, {'x': 62, 'y': 36},                        # upper inner
        {'x': 50, 'y': 50},                                              # center pinch
        {'x': 38, 'y': 64}, {'x': 62, 'y': 64},                        # lower inner
        {'x': 26, 'y': 76}, {'x': 50, 'y': 76}, {'x': 74, 'y': 76},  # bottom bar (3 dots)
    ]},

    # 10 · Magnet · 11 crystals
    # 3-dot crown arc + 3 arm levels + single pole ends
    # Old: single crown dot read as sharp apex, shoulder→arm gap was 16.1u (24px)
    # New: crown arc (38,24)+(50,20)+(62,24) shows smooth horseshoe curve;
    #      max gap drops to 14.1u (18px) — all gaps ≤14.1u
    # Clearly distinct from Arch: Arch has straight vertical columns + single-dot
    # curve; Magnet has 3-dot arc top + 3-level arms + open pole ends at bottom
    {'name': 'Magnet', 'cells': [
        {'x': 38, 'y': 24}, {'x': 50, 'y': 20}, {'x': 62, 'y': 24},  # 3-dot crown arc
        {'x': 30, 'y': 32}, {'x': 70, 'y': 32},                        # shoulders
        {'x': 28, 'y': 46}, {'x': 72, 'y': 46},                        # upper arms
        {'x': 28, 'y': 60}, {'x': 72, 'y': 60},                        # lower arms
        {'x': 28, 'y': 72}, {'x': 72, 'y': 72},                        # pole ends
    ]},

    # 11 · Trident · score 6.034 · 10 crystals
    # Handle + crossbar + three prongs rising from it
    {'name': 'Trident', 'cells': [
        {'x': 50, 'y': 74}, {'x': 50, 'y': 62},
        {'x': 36, 'y': 52}, {'x': 50, 'y': 52}, {'x': 64, 'y': 52},
        {'x': 36, 'y': 40}, {'x': 36, 'y': 28},
        {'x': 64, 'y': 40}, {'x': 64, 'y': 28},
        {'x': 50, 'y': 40}, {'x': 50, 'y': 28},
    ]},

    # 12 · Pawn · 12 crystals
    # Head(3) → collar-max(2) → neck-pinch(2) → base-flare(2) → flat-base(3)
    # Old: neck dots on centerline left base corners disconnected (18.9u gap).
    # New: side-boundary dots all the way down — silhouette reads collar→neck→flare.
    # All side gaps ≤11.7u. Base 16u spacing (24px edge-to-edge) — acceptable.
    {'name': 'Pawn', 'cells': [
        {'x': 50, 'y': 24},                        # head top
        {'x': 40, 'y': 30}, {'x': 60, 'y': 30},   # head sides
        {'x': 36, 'y': 40}, {'x': 64, 'y': 40},   # collar (widest point)
        {'x': 42, 'y': 50}, {'x': 58, 'y': 50},   # neck (narrower)
        {'x': 36, 'y': 60}, {'x': 64, 'y': 60},   # base flare (widens again)
        {'x': 34, 'y': 70}, {'x': 50, 'y': 70}, {'x': 66, 'y': 70},  # flat base
    ]},

    # 13 · Martini · 12 crystals
    # 3-dot rim + converging sides + single-dot apex + 1 stem dot + 3-dot base
    # Old: 2-dot rim at x=28/72 read as 2 isolated points (108px gap, no midpoint).
    # Old: base 2 dots with 48px gap — also borderline.
    # New: rim (34,26)+(50,26)+(66,26) = 16u spacing (24px) ✓
    # New: base (36,74)+(50,74)+(64,74) = 14u spacing (18px) ✓
    # Width pulled from 44u → 32u — fully safe on small phone.
    {'name': 'Martini', 'cells': [
        {'x': 34, 'y': 26}, {'x': 50, 'y': 26}, {'x': 66, 'y': 26},  # 3-dot rim
        {'x': 40, 'y': 36}, {'x': 60, 'y': 36},                        # upper sides
        {'x': 44, 'y': 46}, {'x': 56, 'y': 46},                        # lower sides
        {'x': 50, 'y': 56},                                              # apex
        {'x': 50, 'y': 66},                                              # stem
        {'x': 36, 'y': 74}, {'x': 50, 'y': 74}, {'x': 64, 'y': 74},  # 3-dot base
    ]},

    # 14 · Rocket · 11 crystals
    # Nose → cone(2) → body(2+2) → fin-shoulder(2) → fin-tip(2)
    # Old: exhaust dot (50,70) was 22u from both fin tips — completely disconnected.
    # Old: fin tips at x=28/72 = 44u wide — near screen edge on small phone.
    # New: no center exhaust dot; fins are 2-dot swept-back triangles on each side.
    # Fin shape: body(40,56)→shoulder(30,64)→tip(36,74) — clean backward-swept fin.
    # All gaps ≤12.8u. Width reduced from 44u → 40u.
    {'name': 'Rocket', 'cells': [
        {'x': 50, 'y': 24},                        # nose tip
        {'x': 42, 'y': 32}, {'x': 58, 'y': 32},   # nose cone
        {'x': 40, 'y': 44}, {'x': 60, 'y': 44},   # body top
        {'x': 40, 'y': 56}, {'x': 60, 'y': 56},   # body bottom
        {'x': 30, 'y': 64}, {'x': 70, 'y': 64},   # fin shoulders (sweep out)
        {'x': 36, 'y': 74}, {'x': 64, 'y': 74},   # fin tips
    ]},

    # 15 · Peace Sign · 12 crystals
    # 8-dot circle (r=22) + 4 internal line dots
    # Old: 6-dot circle had 23–28u gaps (46–60px) — every segment disconnected.
    # The right side (70,36)→(70,64) was 28u = 60px — two completely isolated dots.
    # New: 8 evenly-spaced circle dots at 17.1u (27px) each — readable as a circle.
    # Internal: upper stem (50,38) bridges circle-top→center; lower diags (40,62)+(60,62)
    # each terminate just 7.2u from their circle anchor points — very tight connection.
    {'name': 'Peace Sign', 'cells': [
        {'x': 50, 'y': 28}, {'x': 66, 'y': 34}, {'x': 72, 'y': 50},  # circle top-right
        {'x': 66, 'y': 66}, {'x': 50, 'y': 72}, {'x': 34, 'y': 66},  # circle bottom
        {'x': 28, 'y': 50}, {'x': 34, 'y': 34},                        # circle left
        {'x': 50, 'y': 38}, {'x': 50, 'y': 50},                        # vertical stem
        {'x': 40, 'y': 62}, {'x': 60, 'y': 62},                        # lower diagonals
    ]},

    # 16 · Ice Cream Cone · 11 crystals
    # 5-dot scoop arc + 3-dot waffle junction + 2 cone mid-dots + tip
    # Old: 4 near-duplicate dots at y=56-58 (6.3u apart = clutter), no cone sides,
    #      18.9u crown gaps, 48px gap from scoop-base to tip.
    # New: clean arc r≈20 → waffle line (signals scoop/cone boundary) → swept cone sides.
    # All gaps ≤16.1u. Width narrowed from 44u → 40u.
    {'name': 'Ice Cream Cone', 'cells': [
        {'x': 50, 'y': 28}, {'x': 62, 'y': 32}, {'x': 70, 'y': 46},  # right scoop arc
        {'x': 38, 'y': 32}, {'x': 30, 'y': 46},                        # left scoop arc
        {'x': 34, 'y': 56}, {'x': 50, 'y': 56}, {'x': 66, 'y': 56},  # waffle junction line
        {'x': 40, 'y': 67}, {'x': 60, 'y': 67},                        # cone sides
        {'x': 50, 'y': 76},                                              # cone tip
    ]},

    # 17 · Flame · 10 crystals
    # Shape logic was fine (all gaps ≤15.2u). Only issue: width was 44u (x=28–72).
    # Narrowed widest row from (28,56)+(72,56) → (30,56)+(70,56) = 40u wide.
    # All gaps ≤14.1u. Tapers cleanly from wide base through curved sides to tip.
    {'name': 'Flame', 'cells': [
        {'x': 50, 'y': 72}, {'x': 38, 'y': 66}, {'x': 62, 'y': 66},  # base
        {'x': 30, 'y': 56}, {'x': 70, 'y': 56},                        # widest (40u)
        {'x': 34, 'y': 44}, {'x': 66, 'y': 44},                        # mid taper
        {'x': 40, 'y': 34}, {'x': 60, 'y': 34},                        # upper taper
        {'x': 50, 'y': 24},                                              # tip
    ]},

    # 18 · Mountain · 12 crystals
    # Two symmetric peaks + valley + fully connected slopes.
    # Old: asymmetric peaks (y=34 vs y=24), two floating dots not on any slope,
    #      base gap 30px, width 56u.
    # New: peaks symmetric at y=40, valley dot at (50,58), outer slopes via
    #      mid at y=54, inner slopes via mid at y=50, all gaps ≤16.1u, width 48u.
    {'name': 'Mountain', 'cells': [
        {'x': 26, 'y': 70}, {'x': 38, 'y': 70}, {'x': 50, 'y': 70},  # base
        {'x': 62, 'y': 70}, {'x': 74, 'y': 70},
        {'x': 28, 'y': 54}, {'x': 32, 'y': 40},                        # left outer slope
        {'x': 40, 'y': 50}, {'x': 50, 'y': 58},                        # left inner → valley
        {'x': 60, 'y': 50}, {'x': 68, 'y': 40}, {'x': 72, 'y': 54},  # right inner + outer
    ]},

    # 19 · Heart · 12 crystals
    # Two-bump top + V-point bottom.
    # Old: bump-to-outer-side gap was 18.9u (33px) and outer points x=26/74 = 48u wide.
    # New: added bridge dot (30,36)/(70,36) between bump and outer — gap drops to 8–10u.
    #      Outer tightened from x=26/74 → x=28/72 = 44u wide.
    # All gaps ≤16.1u.
    {'name': 'Heart', 'cells': [
        {'x': 36, 'y': 28}, {'x': 50, 'y': 36}, {'x': 64, 'y': 28},  # top bumps + dip
        {'x': 30, 'y': 36}, {'x': 70, 'y': 36},                        # bridge dots (new)
        {'x': 28, 'y': 44}, {'x': 72, 'y': 44},                        # outer sides
        {'x': 28, 'y': 58}, {'x': 72, 'y': 58},                        # lower sides
        {'x': 38, 'y': 68}, {'x': 62, 'y': 68},                        # lower curve
        {'x': 50, 'y': 76},                                              # tip
    ]},

    # 20 · Mushroom · 12 crystals
    # 7-dot dome + 1 dome-base midpoint + 2+2 stem.
    # Old: dome base (30,58)→(70,58) = 40u = 96px edge-to-edge (critical gap),
    #      crown-to-shoulder 19u, width 52u.
    # New: dome narrowed (30–70 = 40u wide), dome-base midpoint (50,56) closes the
    #      40u gap into 2×16u ✓, crown gaps 12.6u ✓. Stem as proper rectangle.
    {'name': 'Mushroom', 'cells': [
        {'x': 50, 'y': 26},                                              # dome crown
        {'x': 38, 'y': 30}, {'x': 30, 'y': 42}, {'x': 34, 'y': 56},  # left dome arc
        {'x': 62, 'y': 30}, {'x': 70, 'y': 42}, {'x': 66, 'y': 56},  # right dome arc
        {'x': 50, 'y': 56},                                              # dome-base midpoint
        {'x': 42, 'y': 64}, {'x': 58, 'y': 64},                        # stem top
        {'x': 44, 'y': 74}, {'x': 56, 'y': 74},                        # stem bottom
    ]},

    # 21 · Bell · 11 crystals
    # Two dome chains + 3-dot bell-mouth opening + clapper beneath center
    # Old: width 50u (x=24–74), bell mouth 40u = 96px gap, clapper floated 21.5u
    #      from either base — disconnected from everything.
    # New: width 44u, opening (34,68)+(50,68)+(66,68) each 16u ✓,
    #      clapper (50,76) hangs 8u below opening center ✓. All gaps ≤16.1u.
    {'name': 'Bell', 'cells': [
        {'x': 50, 'y': 24},                                              # crown
        {'x': 38, 'y': 28}, {'x': 28, 'y': 40}, {'x': 30, 'y': 56}, {'x': 34, 'y': 68},  # left dome
        {'x': 62, 'y': 28}, {'x': 72, 'y': 40}, {'x': 70, 'y': 56}, {'x': 66, 'y': 68},  # right dome
        {'x': 50, 'y': 68},                                              # opening midpoint
        {'x': 50, 'y': 76},                                              # clapper
    ]},

    # 22 · UFO · 12 crystals
    # Dome (3) + inner disk row (3) + outer disk row (3) + bottom rim (3)
    # Old: outer disk (28,56)+(72,56) = 44u = 108px gap — 2 floating isolated dots.
    #      Width 44u (x=28–72).
    # New: outer disk narrowed to x=30/70 and midpoint (50,56) added → 20u gaps ✓.
    #      Width 40u. The 4-row layered structure now clearly reads as flying saucer.
    {'name': 'UFO', 'cells': [
        {'x': 40, 'y': 44}, {'x': 50, 'y': 38}, {'x': 60, 'y': 44},  # dome
        {'x': 38, 'y': 50}, {'x': 50, 'y': 48}, {'x': 62, 'y': 50},  # inner disk
        {'x': 30, 'y': 56}, {'x': 50, 'y': 56}, {'x': 70, 'y': 56},  # outer disk (midpoint added)
        {'x': 34, 'y': 64}, {'x': 50, 'y': 66}, {'x': 66, 'y': 64},  # bottom rim
    ]},

    # 23 · Cactus · 11 crystals
    # Trunk (5) + left arm (3) + right arm (3) — perfectly symmetric
    # Old: left arm exited trunk at y=56, right at y=52 (asymmetric);
    #      left tip y=44, right tip y=40 (asymmetric); arms only 8u wide.
    # New: both arms exit trunk at y=48 (shared trunk dot), both 3 dots wide
    #      horizontally (50→38→30 and 50→62→70), both tips turn up to y=36.
    #      All gaps 8–12u ✓. Perfectly symmetric.
    {'name': 'Cactus', 'cells': [
        {'x': 50, 'y': 72}, {'x': 50, 'y': 60}, {'x': 50, 'y': 48},  # trunk bottom
        {'x': 50, 'y': 36}, {'x': 50, 'y': 24},                        # trunk top
        {'x': 38, 'y': 48}, {'x': 30, 'y': 48}, {'x': 30, 'y': 36},  # left arm
        {'x': 62, 'y': 48}, {'x': 70, 'y': 48}, {'x': 70, 'y': 36},  # right arm
    ]},

    # 24 · Thumbs Up · 12 crystals
    # 8-dot closed fist outline + 4-dot thumb (2 dots wide at tip)
    # Old: thumb was a single-dot-wide line indistinguishable from fist edge;
    #      (52,48)→(34,40) junction gap 19.7u; fist bottom gap 18.1u.
    # New: fist is a clean closed loop (38,74)→(52,74)→(64,70)→(66,58)→(64,50)
    #      →(52,50)→(40,50)→(34,60)→back, all gaps ≤14.6u ✓.
    #      Thumb branches from (40,50) upward-left: (34,40)→(32,28)→(38,24)+(46,24)
    #      — 2-dot-wide tip reads as a thumb, not a fist edge. Width 34u ✓.
    {'name': 'Thumbs Up', 'cells': [
        {'x': 38, 'y': 74}, {'x': 52, 'y': 74},                        # fist base
        {'x': 64, 'y': 70}, {'x': 66, 'y': 58}, {'x': 64, 'y': 50},  # fist right side
        {'x': 52, 'y': 50}, {'x': 40, 'y': 50},                        # fist top
        {'x': 34, 'y': 60},                                              # fist left side
        {'x': 34, 'y': 40}, {'x': 32, 'y': 28},                        # thumb shaft
        {'x': 38, 'y': 24}, {'x': 46, 'y': 24},                        # thumb tip (2 wide)
    ]},

    # 25 · Anchor · 12 crystals
    # 8-dot ring + shaft-at-crossbar + 2 crossbar arms + tip
    # Old: no shaft dot where shaft meets crossbar; crossbar (30,64)+(70,64)
    #      = 40u = 96px gap; hook-tip gaps 22.4u each — hooks were 2 floating dots.
    # New: (50,64) shaft-at-crossbar added — shaft now reads as continuous;
    #      crossbar arms tightened to x=38/62 (12u from center each);
    #      (38,64)→(50,74) = 15.6u ✓ and (62,64)→(50,74) = 15.6u ✓.
    #      Classic anchor silhouette: ring→shaft→crossbar→tip. All gaps ≤15.6u.
    {'name': 'Anchor', 'cells': [
        {'x': 50, 'y': 24},                                              # ring top
        {'x': 64, 'y': 30}, {'x': 70, 'y': 44}, {'x': 62, 'y': 56},  # ring right
        {'x': 50, 'y': 60},                                              # ring bottom
        {'x': 38, 'y': 56}, {'x': 30, 'y': 44}, {'x': 36, 'y': 30},  # ring left
        {'x': 50, 'y': 64},                                              # shaft meets crossbar
        {'x': 38, 'y': 64}, {'x': 62, 'y': 64},                        # crossbar arms
        {'x': 50, 'y': 74},                                              # tip
    ]},

    # 26 · Pyramid · 11 crystals
    # Apex + row2(2) + row3(3) + base(5) — four horizontal tiers, narrowed
    # Old: width 56u (x=22–78), all slope gaps 17–20u (27–36px) — every slope
    #      dot read as isolated; the layered structure was invisible.
    # New: width 44u (x=28–72), slopes 15.2–16.1u ✓. Rows evenly spaced 14u.
    #      Each outer slope: apex→row2→row3→base, all gaps ≤16.1u.
    {'name': 'Pyramid', 'cells': [
        {'x': 50, 'y': 24},                                              # apex
        {'x': 42, 'y': 38}, {'x': 58, 'y': 38},                        # row 2
        {'x': 34, 'y': 52}, {'x': 50, 'y': 52}, {'x': 66, 'y': 52},  # row 3
        {'x': 28, 'y': 66}, {'x': 38, 'y': 66}, {'x': 50, 'y': 66},  # base
        {'x': 62, 'y': 66}, {'x': 72, 'y': 66},
    ]},

    # 27 · Fork · score 7.238 · 12 crystals
    # Handle + three tines spreading at top
    {'name': 'Fork', 'cells': [
        {'x': 50, 'y': 74}, {'x': 50, 'y': 64}, {'x': 50, 'y': 54},
        {'x': 40, 'y': 44}, {'x': 50, 'y': 44}, {'x': 60, 'y': 44},
        {'x': 36, 'y': 34}, {'x': 34, 'y': 24},
        {'x': 50, 'y': 34}, {'x': 50, 'y': 24},
        {'x': 64, 'y': 34}, {'x': 66, 'y': 24},
    ]},

    # 28 · Saturn · 12 crystals
    # 6-dot planet oval + 6-dot diagonal ring passing through it
    # Old: ring was 4 dots in no coherent sequence — (38,34)→(62,64) = 38.4u = 91px,
    #      completely disconnected. Width 50u.
    # New: planet is a compact 6-dot oval (gaps 12.2–16.1u ✓, width 28u).
    #      Ring is a 6-dot diagonal line lower-left→upper-right passing through the
    #      planet center — gaps all 8.2–11.7u ✓. Width 48u total.
    #      The ring's diagonal direction clearly differs from the oval's rounded shape.
    {'name': 'Saturn', 'cells': [
        {'x': 50, 'y': 36}, {'x': 62, 'y': 44}, {'x': 64, 'y': 56},  # planet right arc
        {'x': 50, 'y': 64}, {'x': 38, 'y': 56}, {'x': 36, 'y': 44},  # planet left arc
        {'x': 26, 'y': 62}, {'x': 36, 'y': 56}, {'x': 46, 'y': 50},  # ring left section
        {'x': 54, 'y': 48}, {'x': 64, 'y': 42}, {'x': 74, 'y': 36},  # ring right section
    ]},

    # 29 · Happy Face · 12 crystals
    # 7-dot circle (r=18, center 50,44) + 2 eyes + 3-dot smile arc below circle
    # Old: 7-dot circle with all gaps 19.7–28u (35–60px) — every segment broken.
    #      Width 52u. Bottom circle gap 28u = 60px = single worst gap in any shape.
    # New: circle r=18 has uniform 13.9u gaps ✓; smile arc sits just below circle
    #      (38,66)+(50,72)+(62,66) — circle lower-dots only 9.1u from smile ends
    #      (3px clearance), visually bridging the intentionally-omitted circle bottom.
    #      Eyes (40,40)+(60,40) are comfortably inside circle. Width 36u ✓.
    {'name': 'Happy Face', 'cells': [
        {'x': 50, 'y': 26}, {'x': 63, 'y': 31}, {'x': 68, 'y': 44},  # circle top-right
        {'x': 63, 'y': 57}, {'x': 37, 'y': 57},                        # circle lower
        {'x': 32, 'y': 44}, {'x': 37, 'y': 31},                        # circle left
        {'x': 40, 'y': 40}, {'x': 60, 'y': 40},                        # eyes
        {'x': 38, 'y': 66}, {'x': 50, 'y': 72}, {'x': 62, 'y': 66},  # smile arc
    ]},

    # 30 · Eiffel Tower · 12 crystals
    # Same 12-dot design, scaled from 56u → 48u wide.
    # Old: width 56u (x=22–78) — too wide for small phone.
    # New: all coords scaled inward: legs x=26/74, intermediate rows proportionally
    #      adjusted. All slope gaps 7.8–13.0u ✓. Arch detail 15.2u ✓.
    #      The tapered silhouette with arch cutout at the base is unmistakable.
    {'name': 'Eiffel Tower', 'cells': [
        {'x': 50, 'y': 24},                                              # pinnacle
        {'x': 45, 'y': 34}, {'x': 55, 'y': 34},                        # upper taper
        {'x': 41, 'y': 46}, {'x': 59, 'y': 46},                        # mid taper
        {'x': 36, 'y': 58}, {'x': 50, 'y': 64}, {'x': 64, 'y': 58},  # arch level
        {'x': 31, 'y': 70}, {'x': 69, 'y': 70},                        # leg shoulders
        {'x': 26, 'y': 76}, {'x': 74, 'y': 76},                        # leg bases
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
    # Fixed: back-right leg added at (74, 66)
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
# Single flat batch — 71 levels total in difficulty order.
# Server: level N → ORDERED_PATTERNS[(N-1) % 71]
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
