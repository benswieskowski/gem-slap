"""
Gem Slap - Game Data
All level patterns, musical phrases, scoring constants, and note config.

52 levels total (down from 71 — 19 removed).

Removed levels:
  Cross, Delta, Parabola, Crux, Eighth Note, Sharp, Beamed Notes,
  Cassiopeia, Lyra, Corona Borealis, Scorpius, Swan,
  Compass, Arch, Rocket, Trident, Anchor, Peace Sign, Thumbs Up
"""

PERFECT_WINDOW = 130
GREAT_WINDOW = 250
GOOD_WINDOW = 400
PERFECT_POINTS = 100
GREAT_POINTS = 60
GOOD_POINTS = 30
MISS_POINTS = 10

TARGET_DESTROY_RADIUS = 22
STANDARD_TOTAL_ORBS = 20

SCALE = [-5, -2, 0, 3, 5, 7, 10, 12, 15, 17, 19, 22]

NOTE_COLORS = {
    -5: '#F03028', -2: '#F03028', 0: '#F03028', 3: '#F57828',
    5: '#28D858', 7: '#18C8F8', 10: '#5038E8', 12: '#A020E0',
    15: '#A020E0', 17: '#A020E0', 19: '#A020E0', 22: '#A020E0',
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


# 52 levels — removed: Cross, Delta, Parabola, Crux, Eighth Note, Sharp,
# Beamed Notes, Cassiopeia, Lyra, Corona Borealis, Scorpius, Swan,
# Compass, Arch, Rocket, Trident, Anchor, Peace Sign, Thumbs Up
ORDERED_PATTERNS = [
    # SHAPES — 12 levels (removed: Cross, Delta, Parabola)
    {'name': 'Triangle',    'cells': [{'x':50,'y':36},{'x':38,'y':60},{'x':62,'y':60}]},
    {'name': 'Line',        'cells': [{'x':25,'y':50},{'x':42,'y':50},{'x':58,'y':50},{'x':75,'y':50}]},
    {'name': 'Square',      'cells': [{'x':34,'y':34},{'x':66,'y':34},{'x':34,'y':66},{'x':66,'y':66}]},
    {'name': 'Diamond',     'cells': [{'x':50,'y':27},{'x':27,'y':50},{'x':73,'y':50},{'x':50,'y':73}]},
    {'name': 'Arrow',       'cells': [{'x':24,'y':50},{'x':35,'y':50},{'x':46,'y':50},{'x':57,'y':50},{'x':68,'y':50},{'x':59,'y':45},{'x':50,'y':40},{'x':59,'y':55},{'x':50,'y':60}]},
    {'name': 'Pentagon',    'cells': [{'x':50,'y':29},{'x':72,'y':45},{'x':64,'y':71},{'x':36,'y':71},{'x':28,'y':45}]},
    {'name': 'Hexagon',     'cells': [{'x':50,'y':26},{'x':71,'y':38},{'x':71,'y':62},{'x':50,'y':74},{'x':29,'y':62},{'x':29,'y':38}]},
    {'name': '= Equals',    'cells': [{'x':25,'y':40},{'x':42,'y':40},{'x':58,'y':40},{'x':75,'y':40},{'x':25,'y':60},{'x':42,'y':60},{'x':58,'y':60},{'x':75,'y':60}]},
    {'name': '+ Plus',      'cells': [{'x':50,'y':25},{'x':50,'y':37},{'x':25,'y':50},{'x':37,'y':50},{'x':50,'y':50},{'x':63,'y':50},{'x':75,'y':50},{'x':50,'y':63},{'x':50,'y':75}]},
    {'name': 'Bowtie',      'cells': [{'x':26,'y':30},{'x':74,'y':30},{'x':38,'y':38},{'x':62,'y':38},{'x':44,'y':50},{'x':56,'y':50},{'x':38,'y':62},{'x':62,'y':62},{'x':26,'y':70},{'x':74,'y':70}]},
    {'name': 'Hourglass',   'cells': [{'x':26,'y':24},{'x':50,'y':24},{'x':74,'y':24},{'x':38,'y':36},{'x':62,'y':36},{'x':50,'y':50},{'x':38,'y':64},{'x':62,'y':64},{'x':26,'y':76},{'x':50,'y':76},{'x':74,'y':76}]},
    {'name': 'Pyramid',     'cells': [{'x':50,'y':24},{'x':42,'y':38},{'x':58,'y':38},{'x':34,'y':52},{'x':50,'y':52},{'x':66,'y':52},{'x':28,'y':66},{'x':38,'y':66},{'x':50,'y':66},{'x':62,'y':66},{'x':72,'y':66}]},

    # SYMBOLS — 8 levels (removed: Crux, Eighth Note, Sharp, Beamed Notes)
    # 13 · Hockey Stick · 5 crystals
    # Shaft: 3 vertical dots at x=44 (Δy=10, 31pt gaps — reads as a clean rod).
    # Blade: turns right at the heel with Δ(9,4) then Δ(9,3) — both connected,
    # blade runs nearly horizontal (only 3 y-units of drop over 18 x-units).
    {'name': 'Hockey Stick','cells': [{'x':44,'y':26},{'x':44,'y':36},{'x':44,'y':46},{'x':53,'y':50},{'x':62,'y':53}]},
    {'name': 'Flat',        'cells': [{'x':38,'y':26},{'x':38,'y':40},{'x':38,'y':54},{'x':38,'y':68},{'x':52,'y':52},{'x':58,'y':64},{'x':44,'y':74}]},
    {'name': 'Fermata',     'cells': [{'x':24,'y':54},{'x':32,'y':36},{'x':42,'y':27},{'x':58,'y':27},{'x':68,'y':36},{'x':76,'y':54},{'x':50,'y':63}]},
    {'name': 'θ Theta',     'cells': [{'x':50,'y':27},{'x':69,'y':38},{'x':69,'y':62},{'x':50,'y':73},{'x':31,'y':62},{'x':31,'y':38},{'x':36,'y':50},{'x':50,'y':50},{'x':64,'y':50}]},
    {'name': '√ Root',      'cells': [{'x':23,'y':56},{'x':30,'y':64},{'x':36,'y':72},{'x':43,'y':61},{'x':50,'y':49},{'x':56,'y':35},{'x':61,'y':30},{'x':70,'y':30},{'x':78,'y':30}]},
    {'name': 'Σ Sigma',     'cells': [{'x':33,'y':28},{'x':51,'y':28},{'x':70,'y':28},{'x':54,'y':40},{'x':35,'y':50},{'x':54,'y':60},{'x':33,'y':72},{'x':51,'y':72},{'x':70,'y':72}]},
    {'name': 'X',            'cells': [{'x':28,'y':26},{'x':39,'y':37},{'x':61,'y':37},{'x':72,'y':26},{'x':50,'y':50},{'x':39,'y':63},{'x':28,'y':74},{'x':61,'y':63},{'x':72,'y':74}]},
    {'name': 'π Pi',        'cells': [{'x':25,'y':30},{'x':42,'y':30},{'x':58,'y':30},{'x':75,'y':30},{'x':35,'y':44},{'x':32,'y':58},{'x':29,'y':72},{'x':65,'y':44},{'x':68,'y':58},{'x':71,'y':72}]},

    # SPACE — 5 levels (removed: Cassiopeia, Lyra, Corona Borealis, Scorpius, Swan)
    {'name': 'Dog',         'cells': [{'x':44,'y':28},{'x':50,'y':36},{'x':62,'y':39},{'x':32,'y':40},{'x':46,'y':50},{'x':44,'y':62}]},
    {'name': 'Big Dipper',  'cells': [{'x':22,'y':54},{'x':28,'y':65},{'x':45,'y':60},{'x':45,'y':50},{'x':55,'y':43},{'x':62,'y':36},{'x':78,'y':35}]},
    {'name': 'Snowflake',   'cells': [{'x':63,'y':50},{'x':57,'y':57},{'x':43,'y':57},{'x':37,'y':50},{'x':43,'y':43},{'x':57,'y':43},{'x':76,'y':50},{'x':64,'y':64},{'x':36,'y':64},{'x':24,'y':50},{'x':36,'y':36},{'x':64,'y':36}]},
    {'name': 'Orion',       'cells': [{'x':50,'y':24},{'x':37,'y':31},{'x':56,'y':34},{'x':52,'y':51},{'x':49,'y':54},{'x':46,'y':55},{'x':50,'y':65},{'x':42,'y':76},{'x':63,'y':72}]},
    {'name': 'Crescent',    'cells': [{'x':50,'y':32},{'x':50,'y':68},{'x':59,'y':38},{'x':61,'y':44},{'x':62,'y':50},{'x':61,'y':56},{'x':59,'y':62},{'x':52,'y':38},{'x':53,'y':44},{'x':53,'y':50},{'x':53,'y':56},{'x':52,'y':62}]},

    # ANIMALS — 9 levels (none removed)
    # Fish — 12 crystals. Facing right.
    # Forked tail (24,46)+(24,62) → junction (32,54) → oval body upper arc
    # (38,48)→(50,44)→(62,48) and lower arc (38,60)→(50,64)→(62,60) → nose (70,54).
    # Dorsal fin spikes up (50,36)→(48,28) from the body's widest point.
    {'name': 'Fish',        'cells': [{'x':24,'y':46},{'x':24,'y':62},{'x':32,'y':54},{'x':38,'y':48},{'x':38,'y':60},{'x':50,'y':44},{'x':50,'y':64},{'x':62,'y':48},{'x':62,'y':60},{'x':70,'y':54},{'x':50,'y':36},{'x':48,'y':28}]},
    {'name': 'Bird',        'cells': [{'x':24,'y':44},{'x':35,'y':30},{'x':43,'y':40},{'x':50,'y':46},{'x':57,'y':40},{'x':65,'y':30},{'x':76,'y':44},{'x':44,'y':66},{'x':56,'y':66}]},
    {'name': 'Rabbit',      'cells': [{'x':40,'y':24},{'x':42,'y':36},{'x':58,'y':36},{'x':60,'y':24},{'x':50,'y':48},{'x':50,'y':64},{'x':36,'y':74},{'x':64,'y':74},{'x':68,'y':60}]},
    # Butterfly — 12 crystals, facing forward, wings spread.
    # Body: vertical chain (50,26)→(50,36)→(50,46)→(50,56), Δy=10 each (gap 31pt).
    # Upper wings attach at head+thorax: inner points (40,30)/(60,30), tips (26,26)/(74,26).
    # Lower wings (smaller) attach at base: inner (38,62)/(62,62), tips (28,70)/(72,70).
    # Upper wings noticeably wider/higher than lower — correct butterfly silhouette.
    {'name': 'Butterfly',   'cells': [{'x':50,'y':26},{'x':50,'y':36},{'x':50,'y':46},{'x':50,'y':56},{'x':40,'y':30},{'x':26,'y':26},{'x':60,'y':30},{'x':74,'y':26},{'x':38,'y':62},{'x':28,'y':70},{'x':62,'y':62},{'x':72,'y':70}]},
    # Crab — 12 crystals, top-down view.
    # Wide 3x2 body: row1 (40,44)-(50,44)-(60,44), row2 (40,54)-(50,54)-(60,54).
    # Body cols connect vertically at gap 31pt; rows touch at gap 3pt.
    # Left claw arm (30,49) sits at mid-height, connects to both left body cols
    # and forks into two pincer tips (22,43)/(22,55) — gap 44.8pt between them.
    # Right claw mirrors exactly. Fully symmetric. Centered at (50,49).
    {'name': 'Crab',        'cells': [{'x':40,'y':44},{'x':50,'y':44},{'x':60,'y':44},{'x':40,'y':54},{'x':50,'y':54},{'x':60,'y':54},{'x':30,'y':49},{'x':22,'y':43},{'x':22,'y':55},{'x':70,'y':49},{'x':78,'y':43},{'x':78,'y':55}]},
    # Snail — 12 crystals, facing left.
    # Shell: 5-point partial hex ring (proven snowflake geometry) + center whorl.
    # Opening on the left (lower-left ring point is where body exits).
    # Body chain: neck→body→head flows left in tight 3-5pt steps.
    # Head: two eyestalk antennae (touching at base, 3pt gap) + foot trailing down.
    {'name': 'Snail',       'cells': [{'x':58,'y':42},{'x':71,'y':42},{'x':65,'y':49},{'x':51,'y':49},{'x':51,'y':35},{'x':65,'y':35},{'x':42,'y':52},{'x':32,'y':54},{'x':22,'y':54},{'x':16,'y':48},{'x':26,'y':48},{'x':18,'y':62}]},
    # Whale — 12 crystals, side profile facing right.
    # Tail: upper fluke (22,44), lower fluke (22,58), base (32,52). Flukes 58pt apart.
    # Top arc: (42,44)→(54,40)→(66,44)→mouth_upper (74,48). Arches up over midpoint.
    # Bottom arc: (42,56)→(54,56)→mouth_lower (70,58). Flat belly.
    # Dorsal fin tip (54,30) above top_mid — 31pt gap, reads as spike.
    # Pectoral fin (54,66) below belly — small triangular limb.
    {'name': 'Whale',       'cells': [{'x':22,'y':44},{'x':22,'y':58},{'x':32,'y':52},{'x':42,'y':44},{'x':54,'y':40},{'x':66,'y':44},{'x':42,'y':56},{'x':54,'y':56},{'x':54,'y':30},{'x':74,'y':48},{'x':70,'y':58},{'x':54,'y':66}]},
    # Spider — 12 crystals, top-down view. Perfectly left-right symmetric.
    # Body: 2x2 block (42,48)-(58,48)-(42,58)-(58,58). Left col at x=42, right at x=58.
    # Left legs at x=32 (Δx=10 from body edge): LL1(32,40), LL2(32,52), LL3(32,64).
    #   Each isolated from neighbours (Δy=12, gap 44.8pt). All connect to body (gap 11-30pt).
    # Right legs mirror exactly at x=68.
    # Front leg extensions at (20,34)/(80,34): connected to LL1/RL1 (gap 25.8pt),
    #   isolated from everything else. Creates bent front legs — classic spider silhouette.
    {'name': 'Spider',      'cells': [{'x':42,'y':48},{'x':58,'y':48},{'x':42,'y':58},{'x':58,'y':58},{'x':20,'y':34},{'x':80,'y':34},{'x':32,'y':40},{'x':68,'y':40},{'x':32,'y':52},{'x':68,'y':52},{'x':32,'y':64},{'x':68,'y':64}]},
    {'name': 'Turtle',      'cells': [{'x':50,'y':28},{'x':38,'y':36},{'x':62,'y':36},{'x':30,'y':54},{'x':70,'y':54},{'x':38,'y':68},{'x':62,'y':68},{'x':24,'y':40},{'x':76,'y':40},{'x':26,'y':66},{'x':74,'y':66}]},

    # OBJECTS — 12 levels (removed: Compass, Arch, Rocket, Trident, Anchor)
    {'name': 'Lightning Bolt','cells': [{'x':60,'y':27},{'x':55,'y':33},{'x':50,'y':39},{'x':45,'y':45},{'x':40,'y':51},{'x':49,'y':51},{'x':58,'y':51},{'x':53,'y':57},{'x':48,'y':63},{'x':43,'y':69}]},
    # Bell — 12 crystals, front view.
    # Handle (50,24)→crown (50,32); crown shoulders (42,36)/(58,36) form dome top pair (gap 26.4pt).
    # Two symmetric arcs: crown→shoulder→mouth→rim, each step verified connected.
    # Mouth at x=28/72 (wide flare), rim at x=30/70 (curves slightly back in).
    # Clapper: free-floating 2-crystal chain (50,52)→(50,62) inside bell body.
    # Floats clear of all arc crystals (min gap 43pt) — reads as interior clapper.
    {'name': 'Bell',          'cells': [{'x':50,'y':24},{'x':50,'y':32},{'x':42,'y':36},{'x':58,'y':36},{'x':32,'y':42},{'x':68,'y':42},{'x':28,'y':52},{'x':72,'y':52},{'x':30,'y':60},{'x':70,'y':60},{'x':50,'y':52},{'x':50,'y':62}]},
    {'name': 'Cactus',        'cells': [{'x':50,'y':72},{'x':50,'y':60},{'x':50,'y':48},{'x':50,'y':36},{'x':50,'y':24},{'x':38,'y':48},{'x':30,'y':48},{'x':30,'y':36},{'x':62,'y':48},{'x':70,'y':48},{'x':70,'y':36}]},
    {'name': 'Ice Cream Cone','cells': [{'x':50,'y':28},{'x':62,'y':32},{'x':70,'y':46},{'x':38,'y':32},{'x':30,'y':46},{'x':34,'y':56},{'x':50,'y':56},{'x':66,'y':56},{'x':40,'y':67},{'x':60,'y':67},{'x':50,'y':76}]},
    {'name': 'Magnet',        'cells': [{'x':38,'y':24},{'x':50,'y':20},{'x':62,'y':24},{'x':30,'y':32},{'x':70,'y':32},{'x':28,'y':46},{'x':72,'y':46},{'x':28,'y':60},{'x':72,'y':60},{'x':28,'y':72},{'x':72,'y':72}]},
    {'name': 'Fork',          'cells': [{'x':50,'y':74},{'x':50,'y':64},{'x':50,'y':54},{'x':40,'y':44},{'x':50,'y':44},{'x':60,'y':44},{'x':36,'y':34},{'x':34,'y':24},{'x':50,'y':34},{'x':50,'y':24},{'x':64,'y':34},{'x':66,'y':24}]},
    {'name': 'Martini',       'cells': [{'x':34,'y':26},{'x':50,'y':26},{'x':66,'y':26},{'x':40,'y':36},{'x':60,'y':36},{'x':44,'y':46},{'x':56,'y':46},{'x':50,'y':56},{'x':50,'y':66},{'x':36,'y':74},{'x':50,'y':74},{'x':64,'y':74}]},
    # Mushroom — 12 crystals, front view.
    # Cap: crown (50,28) + cap_center (50,36) bridge the dome to the stem.
    #   Upper shoulders (36,32)/(64,32) hang off the crown.
    #   Wing tips (26,38)/(74,38) extend wide — overhang reads clearly vs narrow stem.
    # Stem: tight 2×3 block (44-56 × 44-64), gap 10.8pt horizontal, 31.3pt vertical.
    #   cap_center bridges to stem top at gap 22.7pt.
    {'name': 'Mushroom',      'cells': [{'x':50,'y':28},{'x':50,'y':36},{'x':36,'y':32},{'x':64,'y':32},{'x':26,'y':38},{'x':74,'y':38},{'x':44,'y':44},{'x':56,'y':44},{'x':44,'y':54},{'x':56,'y':54},{'x':44,'y':64},{'x':56,'y':64}]},
    {'name': 'Pawn',          'cells': [{'x':50,'y':24},{'x':40,'y':30},{'x':60,'y':30},{'x':36,'y':40},{'x':64,'y':40},{'x':42,'y':50},{'x':58,'y':50},{'x':36,'y':60},{'x':64,'y':60},{'x':34,'y':70},{'x':50,'y':70},{'x':66,'y':70}]},
    # Saturn — 12 crystals, 3/4-view. Planet body + tilted elliptical ring.
    # Planet: 2x2 solid block (46,46)-(54,46)-(46,54)-(54,54). All 6 pairs connected.
    # Ring: 8-crystal fully-connected ellipse tilted ~10° (right side higher).
    #   Spans x=26-74. Arc clockwise: left-tip→top-arc(3)→right-tip→bottom-arc(3)→back.
    #   Connects to planet at top-center (gap 6-9pt) and bottom-center (gap -5pt).
    #   Ring tips (26,48)/(74,48) clear of planet (43pt+). No non-consecutive ring pairs touch.
    {'name': 'Saturn',        'cells': [{'x':46,'y':46},{'x':54,'y':46},{'x':46,'y':54},{'x':54,'y':54},{'x':26,'y':48},{'x':36,'y':42},{'x':51,'y':40},{'x':66,'y':42},{'x':74,'y':48},{'x':64,'y':56},{'x':50,'y':58},{'x':34,'y':56}]},
    # UFO — 12 crystals.
    # Dome (3): tight cap (50,28)+(44,32)+(56,32), all touching (-0.3pt row, 10.8pt pair).
    #   Bridges to saucer top-center (10.7pt) and top-left/right (22.7pt).
    # Saucer (8): fully-connected ellipse x=26-74. Top trio at y=38-40 (12.7pt apart),
    #   wide tips at (26,46)/(74,46), bottom arc at y=52-54. All 8 consecutive gaps <28pt.
    # Beam (1): (50,64) hangs 31.3pt below saucer bottom — single tractor beam.
    {'name': 'UFO',           'cells': [{'x':50,'y':28},{'x':44,'y':32},{'x':56,'y':32},{'x':38,'y':40},{'x':50,'y':38},{'x':62,'y':40},{'x':74,'y':46},{'x':66,'y':52},{'x':50,'y':54},{'x':34,'y':52},{'x':26,'y':46},{'x':50,'y':64}]},
    {'name': 'Eiffel Tower',  'cells': [{'x':50,'y':24},{'x':45,'y':34},{'x':55,'y':34},{'x':41,'y':46},{'x':59,'y':46},{'x':36,'y':58},{'x':50,'y':64},{'x':64,'y':58},{'x':31,'y':70},{'x':69,'y':70},{'x':26,'y':76},{'x':74,'y':76}]},

    # MISC — 6 levels (removed: Peace Sign, Thumbs Up)
    # Flame — 12 crystals.
    # Outline: 10-crystal teardrop ring, pointed tip at (50,26), widens to base at y=60-66.
    # All 10 consecutive outline gaps verified (10-33pt). Left-right symmetric.
    # Inner core: iU (50,36) merges with outline at y=32 (-0.3pt, touching),
    #   bridges down to iM (50,46) which reaches both wide sides at gap 32pt.
    # Dense connected top, sparser connected base — reads as a real flame shape.
    {'name': 'Flame',      'cells': [{'x':50,'y':26},{'x':56,'y':32},{'x':62,'y':40},{'x':66,'y':50},{'x':62,'y':60},{'x':50,'y':66},{'x':38,'y':60},{'x':34,'y':50},{'x':38,'y':40},{'x':44,'y':32},{'x':50,'y':36},{'x':50,'y':46}]},
    {'name': 'Eye',        'cells': [{'x':24,'y':50},{'x':76,'y':50},{'x':30,'y':45},{'x':38,'y':42},{'x':50,'y':41},{'x':62,'y':42},{'x':70,'y':45},{'x':70,'y':55},{'x':62,'y':58},{'x':50,'y':59},{'x':38,'y':58},{'x':30,'y':55}]},
    # Bullseye — 12 crystals. Two interleaved hexagonal rings, no center dot.
    # Inner ring (6): proven Snowflake hex geometry, all gaps 14-18pt.
    # Outer ring (6): rotated 30° from inner, visual radius 90pt.
    #   Outer points fall BETWEEN inner points angularly — reads as concentric rings,
    #   not spokes (which is what 0° alignment produces in Snowflake).
    # Each inner connects to its 2 adjacent outer (12-18pt). Outer isolated from each other (51-58pt).
    # Perfectly symmetric, centered at (50,50).
    {'name': 'Bullseye',   'cells': [{'x':63,'y':50},{'x':57,'y':57},{'x':43,'y':57},{'x':37,'y':50},{'x':43,'y':43},{'x':57,'y':43},{'x':70,'y':57},{'x':50,'y':63},{'x':30,'y':57},{'x':30,'y':43},{'x':50,'y':37},{'x':70,'y':43}]},
    # Mountain — 12 crystals, front silhouette. Left-right symmetric, centered at (50,50).
    # Peak (50,26) + snow cap band (42,34)↔(58,34) — all 3 at gap 26pt, forms distinct cap.
    # Left ridgeline: snL→(34,42)→(27,51)→(24,61). Steps Δ(8,8)/Δ(7,9)/Δ(3,10) all verified.
    # Right ridgeline mirrors exactly.
    # Base: rL3(24,61)→(38,66)→(50,66)→(62,66)→rR3(76,61). Base crystals touching (10.8pt).
    {'name': 'Mountain',   'cells': [{'x':50,'y':26},{'x':42,'y':34},{'x':58,'y':34},{'x':34,'y':42},{'x':66,'y':42},{'x':27,'y':51},{'x':73,'y':51},{'x':24,'y':61},{'x':76,'y':61},{'x':38,'y':66},{'x':50,'y':66},{'x':62,'y':66}]},
    {'name': 'Heart',      'cells': [{'x':36,'y':28},{'x':50,'y':36},{'x':64,'y':28},{'x':30,'y':36},{'x':70,'y':36},{'x':28,'y':44},{'x':72,'y':44},{'x':28,'y':58},{'x':72,'y':58},{'x':38,'y':68},{'x':62,'y':68},{'x':50,'y':76}]},
    {'name': 'Happy Face', 'cells': [{'x':40,'y':37},{'x':60,'y':37},{'x':26,'y':50},{'x':30,'y':54},{'x':34,'y':58},{'x':39,'y':62},{'x':46,'y':65},{'x':54,'y':65},{'x':61,'y':62},{'x':66,'y':58},{'x':70,'y':54},{'x':74,'y':50}]},
]

LEVEL_BATCHES = [
    {'name': '', 'patterns': ORDERED_PATTERNS},
]

BASS_STYLES = {
     0: {'name': 'Fourside Funk',    'bpm': 108},
     2: {'name': 'Snake Slither',    'bpm': 126},
     3: {'name': 'Guardia Festival', 'bpm': 130},
     5: {'name': 'Bright Flash',     'bpm': 138},
     6: {'name': 'Pharaoh Rush',     'bpm': 132},
    10: {'name': 'Golden Hour',      'bpm': 110},
    11: {'name': 'Candy Flip',       'bpm': 124},
    12: {'name': 'Dawnbreak',        'bpm': 120},
    13: {'name': 'Prism',            'bpm': 128},
    14: {'name': 'Neon Pulse',       'bpm': 118},
}

# BPM arc: 110→118→124→130→128→138→132→126→120→108
STYLE_ORDER = [10, 14, 11, 3, 13, 5, 6, 2, 12, 0]
