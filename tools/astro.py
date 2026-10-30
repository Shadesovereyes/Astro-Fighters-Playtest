"""Astrological (Sign) kit animations (Christopher 2026-10-27: "begin developing Astrological kit animations"; abilities
from the Sign Kits tab of AstroFighters_Abilities, 12 signs x 8). Played from the approved boxing guard (hitReact frame 6)
and returning to it, through universal.py's spec builder. One state per ability. E/W first (W mirrors E), S/N after
approval. Effects use the sign's element colours (Christopher 2026-10-27 17:00): fire = reds/oranges/yellows (Sagittarius:
select black and purple flames), earth = earth and crystal tones, water = water and ice tones; air stays white/pale until ruled.
Run: python3 tools/astro.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/astro.py --fx <state>   (aura / motion blur after the render; splash fx are baked by the renderer)"""
import math
import sys, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universal as U
from universal import band, g, leg, kleg, LOW, BRACE, NPAL, NPAT, nfx, D
from gen import load, save
import stances

STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {'stalactiteRain': 'E/W approved by user 2026-10-30 (v2 16-frame ultimate: crystal spears rise behind the caster, shoot up, hand hurled at the target, 127e2eb5; target plays stalactiteImpaled; W mirrors E); S/N to author', 'stalactiteImpaled': 'E/W approved by user 2026-10-30 (v2 spears rain down at a slant in two volleys, stick, shatter into rubble, 127e2eb5; W mirrors E); S/N to author', 'geodeBlast': 'E/W approved by user 2026-10-29 (v1 palm slam, glowing cracks run to the target, palm whipped up, c59bb3e6; target plays geodeBlasted; W mirrors E); S/N to author', 'geodeBlasted': 'E/W approved by user 2026-10-29 (v1 crystal spike clusters burst round the feet, shards, bleed, crumble, c59bb3e6; W mirrors E); S/N to author', 'adamantineShin': 'E/W approved by user 2026-10-29 (v1 crystal sheath grows over the shin, crystal shin kick at thigh height with crack and shard burst, 2ca22687; W mirrors E); S/N to author', 'diamondCutter': 'E/W approved by user 2026-10-29 (v1 knife hand chambered behind the head, crystal grows over hand and forearm, diagonal chop with slash and shards, 2ca22687; W mirrors E); S/N to author', 'prismaticSkin': 'E/W approved by user 2026-10-29 (v1 fists at the hips, teal aura, skin crystallises teal with facets and lingers while the buff lasts, 2ca22687; W mirrors E); S/N to author', 'silicaStrike': 'E/W approved by user 2026-10-28 (v5: kneel and scoop, uppercut rises from the crouch, heavy sand trail, burst and lingering cloud, 36955ad6; W mirrors E); S/N to author', 'flowingSandParry': 'E/W approved by user 2026-10-28 (v2 converging high/low arm circles with sand trails, 8baa93ab; W mirrors E); S/N to author', 'phantomHaunted': 'E/W approved by user 2026-10-28 (v2 12-frame loop: the phantom circles the victim behind, far side, in front, near side, then rakes, 41f294d; W mirrors E); S/N to author', 'witherPalm': 'E/W approved by user 2026-10-28 (v2 glowing palms, strike streaks, teal shock rings, dust plumes, teal aura, final burst, f45f621f; W mirrors E); S/N to author', 'coffinSyndrome': 'E/W approved by user 2026-10-28 (v2 caster: palm lifts to raise the coffin behind the target, fist snaps the lid shut, 8baa93ab; target plays coffinEntombed then coffinBreakOut; W mirrors E); S/N to author', 'coffinEntombed': 'E/W approved by user 2026-10-28 (v2 coffin rises behind the target, lid shuts, pounding loop from frame 6, 8baa93ab; W mirrors E); S/N to author', 'coffinBreakOut': 'E/W approved by user 2026-10-28 (v1 lid cracks and bursts, coffin breaks apart into planks and sand, 8baa93ab; W mirrors E); S/N to author', 'phantomPlague': 'E/W approved by user 2026-10-28 (v1 shadow pool, teal-eyed shadow creature claws up and glides at the target, 4af1f46; target plays phantomHaunted; W mirrors E); S/N to author', 'sandBurial': 'E/W approved by user 2026-10-28 (v1 caster: sand flows along the floor to the target, viewed in the two-fighter scene; W mirrors E); S/N to author', 'sandBuried': 'E/W approved by user 2026-10-28 (v2 sand climbs to the neck, squeeze loop with constriction bands while the Root lasts, e32d553; W mirrors E); S/N to author', 'sandBreakFree': 'E/W approved by user 2026-10-28 (v2 column cracks, arms burst out with a roar, sand chunks blow out, back to guard, e32d553; W mirrors E); S/N to author', 'sandstorm': 'E/W approved by user 2026-10-28 (v2 caster-centred storm zone: storm rises from the feet round the caster in its eye, blasts outward; spec extra.zone, canon A7, 3b513b51; W mirrors E); S/N to author', 'sandstormCaught': 'E/W approved by user 2026-10-28 (v2 sand gusts blowing past, forearms over the eyes, loops while inside the storm, 3b513b51; W mirrors E); S/N to author', 'oakFlesh': 'E/W approved by user 2026-10-28 (v6 honey oak bark with walnut grain over body and face, moss patches, hair turned to moss, 6d538de; W mirrors E); linger keeps the look while the buff lasts; S/N to author', 'ironFist': 'E/W approved by user 2026-10-28 (v1 Shatter Punch body, earth/crystal arm swirl, crystal-white flash, teal/brown shock ring, stone chips, 5d11ccb0; W mirrors E); S/N to author', 'rootSanctuary': 'E/W approved by user 2026-10-28 (v2 roots with root hairs rise from floor cracks and arch into a dome behind the fighter, crystal buds, fdb604b; W mirrors E); linger root ring is a proposal; S/N to author', 'ironwoodKanabo': 'E/W approved by user 2026-10-28 (v2 spiked iron kanabo rises head-first from a crack in the floor and is gripped, after Christopher\'s reference, c58ee3f; W mirrors E); kanabo weapon layer, Kanabo stance idle and weapon attacks in a separate thread; S/N to author', 'planetaryPressure': 'E/W approved by user 2026-10-28 (v1 illusory planet beside the raised hand, fist hauled down, sinking gravity waves and falling dashes, target genjutsu mark in earth colours, 6ce4904; W mirrors E); S/N to author', 'materialFixation': 'E/W approved by user 2026-10-28 (v1 illusory crystal gem offered from the palm, teal eyes, fascination waves, target genjutsu mark in earth colours, 6ce4904; W mirrors E); S/N to author', 'bullRush': 'E/W approved by user 2026-10-28 (v2 sprinter set, head-down charge with arms reaching forward, dust, shoulder ram, e1f5ef2; W mirrors E); S/N to author', 'mountainStance': 'E/W approved by user 2026-10-28 (v1 double shiko stamp, wide rooted stance, earth aura, crystal shards, a651ae52; W mirrors E); S/N to author','flowDodge': 'E/W approved by user 2026-10-28 (v1 trance sway, fire aura on the beat, purple/black wisps, 4d565a4; W mirrors E); S/N to author', 'leashKick': 'E/W approved by user 2026-10-28 (v2 double pirouette in a fire ring, axe kick finish, fea7941; W mirrors E); S/N to author', 'spinningTop': 'E/W approved by user 2026-10-28 (v1 headspin, flaming V legs, fire ring at foot height, turned-over frames via 180-degree layer turn, 68b2808; W mirrors E); S/N to author', 'wispFire': 'E/W approved by user 2026-10-28 (v1 alternating palm pushes, four purple wisps, 63b132e; W mirrors E); S/N to author', 'dogma': 'E/W approved by user 2026-10-28 (v1 fingers to the temple, looping purple motes, belief waves, target genjutsu mark, 6364f3b; W mirrors E); S/N to author', 'soulPressure': 'E/W approved by user 2026-10-28 (v1 dark spirit aura, pressing palm, sinking pressure waves, target genjutsu mark, d7b92b6; W mirrors E); S/N to author', 'cauterize': 'E/W approved by user 2026-10-27 (v1 palm seared to the ribs, fire flare with purple/black licks, smoke, d84e1d7; W mirrors E); S/N to author', 'supernova': 'E/W approved by user 2026-10-27 (v2 ultimate, 16 frames at 8 fps, long trembling build-up, swelling star, flash held 3 frames, rings, 50c8b58; W mirrors E); the S and N rows share the same S turn, S/N to author', 'spotlight': 'E/W approved by user 2026-10-27 (v3 arms lowered, forward lean, cone of light from the eyes, target genjutsu mark, 50c8b58; W mirrors E); S/N to author', 'sunPalm': 'E/W approved by user 2026-10-27 (v2 arm swirl, gathering sun, white-hot flash, fire shock ring, cracks, embers, d059a89; W mirrors E); S/N to author', 'kneel': 'E/W approved by user 2026-10-27 (v1 crown of light, commanding palm, sinking gold pressure waves, target genjutsu mark; W mirrors E); S/N to author', 'kingsPosture': 'E/W approved by user 2026-10-27 (v4 E-facing double biceps in profile, golden aura, flame mane, d4e4c1e; W mirrors E); S/N to author', 'radiance': 'E/W approved by user 2026-10-27 (v4 E-facing, fists down at the sides, erupting spiky gold aura, lingering 2 px aura + motes, d4e4c1e; W mirrors E); S/N to author', 'solarLance': 'E/W approved by user 2026-10-27 (v2 arm swirl, bigger sun, thick sparking beam, shoulder backblast, gold aura, d059a89; W mirrors E); S/N to author', 'battleRoar': 'E/W approved by user 2026-10-27 (v1 big breath, lunging roar, flame mane, golden roar waves, 733e752; W mirrors E); S/N to author', 'killingIntent': 'E/W approved by user 2026-10-27 (v3 illusory demon mask over the head matching the facing, clawed crouch, 02ce6eb; W mirrors E); S/N to author', 'blindRage': 'E/W approved by user 2026-10-27 (v1 genjutsu template: one-hand seal, eye flare, crimson aura, rage waves, 0b27675; W mirrors E); S/N to author', 'genjutsuAfflicted': 'E/W approved by user 2026-10-27 (v1 genjutsu target mark, fire colours, d75144b; W mirrors E); S/N to author', 'meteor': 'E/W approved by user 2026-10-27 (v2 ultimate, 16 frames, swelling fireball + flash + thick trail, f395d5b; W mirrors E); S/N to author', 'explosiveRunes': 'E/W approved by user 2026-10-27 (v1 sowing palm sweep + fire runes, 640aaba; W mirrors E); S/N to author', 'blastWave': 'E/W approved by user 2026-10-27 (v3 S-facing roar release, dd5ab8a; W mirrors E); the S and N rows share the same S turn, their guard frames still to review', 'innerGateAdrenaline': 'E/W approved by user 2026-10-27 (v3 lingering aura, skin flush, veins, aee3dad; W mirrors E) on condition the look lingers while the ability is active; canon A5: a toggle, active until 0 HP or deactivated; S/N to author', 'machLunge': 'E/W approved by user 2026-10-27 (v5 sprint, flaming feet, fire wake, 4 afterimages, fc741f6; W mirrors E); S/N to author', 'shatterPunch': 'E/W approved by user 2026-10-27 (v3 arm swirl + impact burst, fc741f6; W mirrors E); S/N to author'}

U.POSES += [leg('ml-dip-lead', (32, 45), (38, 51), 37), leg('ml-dip-rear', (31, 45), (29, 51), 24, wrap=54, kind='toe60'),   # sprinter dip, rear heel up
            kleg('ml-fly-lead', (33, 42), (39, 46), (38, 52), 'toe30k'), kleg('ml-fly-rear', (31, 42), (25, 47), (20, 51), 'toe30k'),   # driving off the rear foot
            leg('ml-plant-lead', (33, 43), (39, 50), 41), kleg('ml-trail-rear', (31, 43), (26, 49), (22, 54), 'toe30k'),   # lead foot lands a long step on
            leg('sp-load-lead', (32, 43), (35, 51), 36), leg('sp-load-rear', (31, 43), (28, 51), 24),                # Shatter Punch: weight sat back
            leg('sp-drive-lead', (33, 43), (38, 50), 40), leg('sp-drive-rear', (32, 43), (31, 50), 27, wrap=54, kind='toe60')]  # step in, rear heel turns up

# element palettes (letters added to universal.NPAL; W/w white stay for air and highlights)
ELEMENT = {'Y': '#ffe14d', 'O': '#ff8a1c', 'R': '#d8321a',               # fire: yellow core, orange body, red edge
           'K': '#1c1024', 'P': '#9b45ff', 'p': '#55208f',                # Sagittarius: black flame with purple
           'E': '#8a6236', 'e': '#c79a5b', 'C': '#7fe3d0', 'c': '#d9fff6',  # earth: soil browns, crystal teal / glint
           'A': '#2f7fe0', 'a': '#7cc8ff', 'I': '#dff6ff',                 # water: deep and light water, ice white-blue
           'M': '#7a1016', 'm': '#2a0406'}                                 # m: near-black blood red, the fill of the Killing Intent demon                                                 # fire genjutsu: dark crimson rim of a rage wave
NPAL.update(ELEMENT)

def _mane(r0, n, seed, front=False):   # a lion's mane of flame round the head: tongues of uneven length radiating from a ring, red tips, orange body, yellow root
    import random
    rnd = random.Random(seed); R = r0 + n + 2; g_ = [['.'] * (2 * R + 1) for _ in range(2 * R + 1)]
    for t in range(48):
        a = 2 * math.pi * t / 48; L = n + rnd.randint(-1, 2) if math.sin(a) < 0.5 else max(1, n // 2)   # the mane hangs long at the back and top, short under the chin
        if not front and math.cos(a) > 0.6 and math.sin(a) > -0.3: L = max(1, L // 2)   # short in front of the face (front: symmetric, seen face-on)
        for d in range(r0, r0 + L + 1):
            x, y = round(R + d * math.cos(a)), round(R - d * math.sin(a) * 1.1)
            if 0 <= x <= 2 * R and 0 <= y <= 2 * R:
                q = (d - r0) / max(1, L); g_[y][x] = 'Y' if q < 0.35 else 'O' if q < 0.75 else 'R'
    return [''.join(row) for row in g_]

def _sun(rad, rays=0):   # a small sun: white-hot heart, gold body, orange rim, with rays poking out of it every 45 degrees
    R = rad + rays; g_ = [['.'] * (2 * R + 1) for _ in range(2 * R + 1)]
    for y in range(-R, R + 1):
        for x in range(-R, R + 1):
            d = (x * x + y * y) ** 0.5
            if d <= rad: g_[y + R][x + R] = 'W' if d < rad * 0.4 else 'Y' if d < rad - 0.9 else 'O'
            elif rays and (x == 0 or y == 0 or abs(x) == abs(y)) and d <= R + 0.5: g_[y + R][x + R] = 'Y' if d < rad + rays / 2 else 'R'
    return [''.join(q) for q in g_]

def _halo(n, cx=35, cy=5, rx=7, ry=2, motes=3):   # motes circling over the head, a full turn every n frames: bright in front of the head, dark crimson behind
    out = []
    for k in range(n):
        pts = [('dotM', [round(cx + rx * math.cos(t)), round(cy + ry * math.sin(t)) + 1]) for t in [2 * math.pi * (j + k / n) / 16 for j in range(0, 16, 2)]]   # a faint dotted crimson ring, turning with the motes
        for m in range(motes):
            a = 2 * math.pi * (k / n + m / motes); x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
            pts.append(('moteF' if math.sin(a) > 0 else 'moteB', [round(x) - 1, round(y) + 1]))
        out.append((k, pts))
    return out

def _jag(r, w, cols):   # a jagged ')' wave of killing intent: the rage arc with every other row kicked out a pixel (it reads as a shudder, not a ripple)
    a = _arc(r, w, cols); return [('.' + q[:-1]) if i % 2 else q for i, q in enumerate(a)]

def _sag(h, d, cols, gap=1):   # a flat dome-shaped wave bearing down (the middle high, the ends low) h px either side of centre, d px deep; cols run top -> bottom
    rows = [['.'] * (2 * h + 1) for _ in range(d + len(cols))]
    for dx in range(-h, h + 1):
        if dx % gap: continue
        y = round(d * (dx / h) ** 2)
        for i, c in enumerate(cols): rows[y + i][dx + h] = c
    return [''.join(q) for q in rows]

def _arc(r, w, cols, gap=1):   # a ')' rage wave r px either side of centre, bowing w px toward the target; cols run tip -> leading edge; gap > 1 breaks it up
    rows = []
    for dy in range(-r, r + 1):
        x = round(w * (1 - (dy / r) ** 2)); row = ['.'] * (w + len(cols))
        if dy % gap == 0:
            for i, c in enumerate(cols): row[x + i] = c
        rows.append(''.join(row).rstrip('.') or '.')
    n = max(map(len, rows)); return [q.ljust(n, '.') for q in rows]
# fire fx patterns: flame licks (red edge, orange body, yellow core), a fire-sign guard-crack, embers
NPAT.update({
    'flame1': ['.R.', 'ROR', '.Y.'], 'flame2': ['..R..', '.RO..', '.OYR.', 'ROYOR', '.RRR.'],
    'flame3': ['...R...', '..RO...', '.ROO.R.', '.OYYRO.', 'ROYYYOR', '.ROYOR.', '..RRR..'],
    'shatter1': ['O...O', '.Y.Y.', '..W..', '.Y.Y.', 'O...O'],
    'shatter2': ['R.....R', '.O...O.', '..YYY..', '.YYWYY.', '..YYY..', '.O...O.', 'R.....R'],
    'shatter3': ['R...R...R', '.O..O..O.', '..Y.Y.Y..', '...YWY...', 'OYYWWWYYO', '...YWY...', '..Y.Y.Y..', '.O..O..O.', 'R...R...R'],
    'shard': ['O.', '.R'], 'shardR': ['.O', 'R.'],
    'heat': ['O.Y.O', '.R.R.'], 'embers': ['.O..R', 'R..O.', '..Y..'],
    # Explosive Runes: rune circles seen flat on the ground (ellipse with a glyph stroke), hot as written, lit, smouldering
    'runeHot': ['...YWY...', '.YW.O.WY.', 'YW.OYO.WY', '.YW.O.WY.', '...YWY...'], 'runeLit': ['...OYO...', '.OR.Y.RO.', 'OR.YOY.RO', '.OR.Y.RO.', '...OYO...'],
    'rage1': _arc(4, 2, 'RO'), 'rage2': _arc(7, 3, 'MRO'), 'rage3': _arc(10, 4, 'MRY'), 'rage4': _arc(13, 5, 'MRO'),
    'rage4d': _arc(13, 5, 'MR', gap=2), 'rage5d': _arc(15, 6, 'M', gap=3),
    'oni': ['M.................M', 'MM...............MM', '.MM.............MM.', '.MmM...MMMMM...MmM.', '..MmMMMmmmmmMMMmM..', '..MmmmmmmmmmmmmmM..', '.MmmmmmmmmmmmmmmmM.', '.MmmRRmmmmmmmRRmmM.', 'MmmmmYRmmmmmRYmmmmM', 'MmmmmmmmmmmmmmmmmmM', 'MmmmmmmmMmMmmmmmmmM', '.MmmmmmmmmmmmmmmmM.', '.MmRmRmRmRmRmRmRmM.', '.MmmRYRYRYRYRYRmmM.', '..MmmRmRmRmRmRmmM..', '...MmmmmmmmmmmmM...', '....MMmmmmmmmMM....', '......MMMMMMM......'],   # Killing Intent: a horned demon face looming behind the fighter, glowing eyes and a fanged grin
    'oniFaint': ['M.................M', 'MM...............MM', '.MM.............MM.', '.M.M...MMMMM...M.M.', '..M.MMM.....MMM.M..', '..M.............M..', '.M...............M.', '.M...............M.', 'M.................M', 'M.................M', 'M.......M.M.......M', '.M...............M.', '.M...............M.', '.M...............M.', '..M.............M..', '...M...........M...', '....MM.......MM....', '......MMMMMMM......'], 'oniEyes': ['...................', '...................', '...................', '...................', '...................', '...................', '...................', '....RR.......RR....', '.....YR.....RY.....', '...................', '...................', '...................', '...R.R.R.R.R.R.R...', '....RYRYRYRYRYR....', '.....R.R.R.R.R.....', '...................', '...................', '...................'],
    'dread': ['M..M.M..M.M', '.MmMmMmMmM.'],   # dark pressure pooling at the feet
    'oniMask': ['..R...............', '..RR..............', '...RR.............', '...RMR............', '....RMRRRRRR......', '....RmmmmmmmRR....', '...RmmmmmmmmmmR...', '...RmmmmmRRRRRmR..', '...RmmmmmmmYWYmmR.', '...RmmmmmmmmRmmmmR', '...RmmmmmmmmmmmmRR', '...RmmmmmmmmmmMR..', '...RmmmmmmmWmWmWR.', '....RmmmmmmmmmmmR.', '....RmmmmmmmWmWR..', '.....RRmmmmmmRR...', '.......RRRRRR.....'],   # Killing Intent v3: the illusory demon mask, in profile facing E (mirrored for W): horn sweeping back, brow ridge, glowing eye, snout and fangs
    'ki1': _jag(5, 2, 'MR'), 'ki2': _jag(9, 3, 'MRO'), 'ki3': _jag(13, 4, 'MRO'), 'ki4': _jag(16, 5, 'MR'),
    'mane1': _mane(7, 2, 1), 'mane2': _mane(7, 4, 2), 'mane3': _mane(7, 6, 3), 'mane3b': _mane(7, 6, 4), 'mane4': _mane(7, 7, 5),
    **{'S' + k: _mane(7, n, sd, front=True) for k, n, sd in (('mane1', 2, 1), ('mane2', 4, 2), ('mane3', 6, 3), ('mane3b', 6, 4), ('mane4', 7, 5))},
    'sunOrb1': ['.Y.', 'YWY', '.Y.'], 'sunOrb2': ['..O..', '.YWY.', 'OWWWO', '.YWY.', '..O..'],
    'lightMote': ['.Y.', 'YWY', '.O.'],   # Radiance: a mote of light drifting up off the body
    'sunOrb4': _sun(3, 3), 'sunOrb5': _sun(4, 4),
    'sunOrb3': ['...Y...', '..OYO..', '.OYWYO.', 'YYWWWYY', '.OYWYO.', '..OYO..', '...Y...'],
    'sunBurst1': ['....Y....', '.Y..Y..Y.', '..YYWYY..', '..YWWWY..', 'YYWWWWWYY', '..YWWWY..', '..YYWYY..', '.Y..Y..Y.', '....Y....'],
    'sunBurst2': ['R....O....R', '.O...Y...O.', '..Y.OYO.Y..', '...OY.YO...', '.OYY...YYO.', 'OY.......YO', '.OYY...YYO.', '...OY.YO...', '..Y.OYO.Y..', '.O...Y...O.', 'R....O....R'],
    'sunBurst3': ['R.....R.....R', '.............', '..O.......O..', '.....R.R.....', '...R.....R...', '.............', 'R...........R', '.............', '...R.....R...', '.....R.R.....', '..O.......O..', '.............', 'R.....R.....R'],
    'roar1': _arc(5, 2, 'YW'), 'roar2': _arc(9, 3, 'OYW'), 'roar3': _arc(13, 4, 'ROY'), 'roar3d': _arc(15, 5, 'RO', gap=2),
    'moteF': ['.Y.', 'YOR', '.R.'], 'moteB': ['.M.', 'MRM', '.M.'], 'dotM': ['M'],
    'eyeGlint': ['.R.', 'RYR', '.R.'], 'eyeFlare': ['..R..', '.ROR.', 'ROYWO', '.ROR.', '..R..'], 'rageWisp': ['M.R', '.R.', 'RO.'],
    'eyeGold': ['.Y.', 'YWY', '.Y.'], 'eyeGoldF': ['..O..', '.OYO.', 'OYWYO', '.OYO.', '..O..'],   # Leo genjutsu: the eyes kindle gold
    'crown1': ['....Y....', '.Y..O..Y.', '.YOYOYOY.', '.ROROROR.'], 'crown2': ['Y...Y...Y', 'YY.YOY.YY', 'YOYOYOYOY', 'OYYYYYYYO', '.ROROROR.'],
    'crown3': ['Y...W...Y', 'YY.YWY.YY', 'YOYOYOYOY', 'OYYWYWYYO', '.ROROROR.'],   # Kneel: an illusory crown of light over the head
    'press1': _sag(5, 2, 'YO'), 'press2': _sag(8, 3, 'WYO'), 'press3': _sag(11, 4, 'YOR'), 'press3d': _sag(13, 4, 'OR', gap=2),   # Kneel: golden pressure bearing down
    'runeDim': ['...R.R...', '.R..O..R.', 'R..O.O..R', '.R..O..R.', '...R.R...'], 'fireLine': ['.R.O.', 'OYROY'],
})
FIRE_AURA = ('#ffb12e', '#e0401c')   # orange next to the body, red outside
FIRE_TRAIL = {(255, 255, 255): (0xff, 0xd2, 0x3f), (0xe3, 0xe3, 0xe3): (0xff, 0x7a, 0x1c)}   # motion-blur streak recoloured: yellow inner half, orange tail

SPRINT = load(D + 'sprint.json')   # the approved sprint: stride, lean and swept-back arms reused by Mach Lunge
SPRINT_LEGS = [p['name'] for p in SPRINT['legs']['poses']]
U.POSES += [{**p, 'name': 'sr-' + p['name']} for p in SPRINT['legs']['poses']]
SPRINT_N, SPRINT_F, SPRINT_DY = SPRINT['arms']['near'], SPRINT['arms']['far'], SPRINT['bob']['dy']
def _foot(p):   # bottom-left anchor for a flame burst at a sprint foot: on the floor when planted, at the raised foot otherwise
    q = SPRINT['legs']['poses'][SPRINT_LEGS.index(p)]
    return [q['footX'] - 3, 63 if q['wrapRow'] >= 56 else q['wrapRow'] + 6]
def _burst(p, k):   # a big flame on each foot, plus a lick trailing off the back of a planted foot; alternating shapes flicker
    at = _foot(p); big = ('flame3', 'flame2')[k % 2]
    return [(big, at)] + ([('flame2' if k % 2 else 'flame1', [at[0] - 5, 63])] if at[1] == 63 else [])
FIRE_WAKE = [[('flame3', [14, 63]), ('flame2', [7, 63]), ('flame3', [1, 63]), ('flame2', [18, 46]), ('flame1', [10, 40]), ('embers', [4, 34])],   # a stream of fire left behind along the
             [('flame2', [15, 63]), ('flame3', [8, 63]), ('flame2', [2, 63]), ('flame1', [17, 44]), ('flame2', [9, 42]), ('embers', [3, 30])]]   # ground and in the air behind the runner, flickering
FOOT_FLAMES = [_burst(SPRINT_LEGS[k], k) + _burst(SPRINT_LEGS[(k + 4) % 8], k + 1) for k in range(6)]
PUNCH = band(-92, -92)                  # straight arm at shoulder height
CHAMBER = band(75, -150)                # rear fist drawn back by the ear, elbow high behind
TUCK_N, TUCK_F = band(-35, 200), band(-50, 215)   # arms tucked tight to the chest for the shoulder charge
PU_S = (35, -15, 1, 'up')                      # Radiance v3 (S view): fist clenched and driven down at the side, elbow bent out
KP_S, KP_S2 = (92, 182, 1, 'up'), (97, 192, 1, 'up')   # King's Posture v3 (S view): front double biceps, upper arm level out to the side, fist curled up by the head (KP_S2 the squeeze)
KP_EN, KP_EF = band(-90, -170), band(92, 172)    # King's Posture v4 (E view, no turn): double biceps in profile, near upper arm level forward and far one level back, both fists curled up by the head
KP_EN2, KP_EF2 = band(-96, -178), band(98, 178)  # the squeeze on the peak frame
FLEX_N, FLEX_F = band(50, -20), band(40, -15)     # elbows flared back, clenched fists low beside the hips (power surge)

HEAVY = load(D + 'heavyAttack.json')   # Sagittarius Leash Kick: the approved side/heel kick legs and the spinPivot pirouette
U.POSES += [{**p, 'name': 'lk-' + p['name']} for p in HEAVY['legs']['poses'] if p['name'] in ('lift', 'side-chamber', 'side', 'lead-pivot')]
NPAT.update({'pflame1': ['.K.', 'KPK', '.p.'], 'pflame2': ['..K..', '.KP..', '.PpK.', 'KPpPK', '.KKK.'],   # Sagittarius: select black and purple flames
             'pembers': ['.P..K', 'K..P.', '..p..'],
             'pwisp': ['...pP...', 'K.pPPPW.', 'KpPPWWWP', '.KpPPPW.', '...pP...'], 'pwisp2': ['K..pP...', '.KpPPPW.', 'KpPPWWWP', '..pPPPW.', 'K..pP...'],   # Wisp Fire: a small purple flame flying toward the facing, white-hot head, black tail
             'pspark': ['P.p', '.W.', 'p.P'],
             'dog1': _arc(4, 2, 'WP'), 'dog2': _arc(7, 3, 'WPp'), 'dog3': _arc(10, 3, 'PpK'), 'dog3d': _arc(12, 4, 'pK', gap=2),   # Dogma: purple waves of belief looping out
             'eyeP': ['.P.', 'PWP', '.P.'], 'eyePF': ['..p..', '.pPp.', 'pPWPp', '.pPp.', '..p..'], 'moteP': ['.P.', 'PWP', '.p.'], 'moteK': ['.p.', 'pKp', '.p.'], 'dotP': ['p'],
             'sp1': _sag(5, 2, 'Pp'), 'sp2': _sag(8, 3, 'WPp'), 'sp3': _sag(11, 4, 'PpK'), 'sp3d': _sag(13, 4, 'pK', gap=2),   # Soul Pressure: a heavy blanket of spirit bearing down
             'spWisp': ['K.p', '.p.', 'pP.'],
             'crack1': ['K.....K', '.K...K.', '.EKEKE.'], 'crack2': ['K...........K', '.KK.......KK.', '...KK.K.KK...', '....EKKKE....'],   # Taurus: cracks stamped into the floor
             'dust1': ['..e.e..', '.eEeEe.', 'eEeEeEe', '.EeEeE.'], 'dust2': ['e...e.e...e', '.e.eEeEe.e.', '..eEeEeEe..', '.eEeEeEeEe.'], 'rocks': ['K...E', '.E.K.', 'E...K'],
             'cryst': ['.c.', 'cCc', '.C.'], 'crystT': ['c', 'C', 'C'],
             'kanabo': ['...jjj...', '..jhhij..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', '..ihjji..', '...hji...', '...ijj...', '...jhj...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...jhj...', '..j...j..', '..j...j..', '...jjj...'],   # Ironwood Kanabo v2 (Christopher 2026-10-28 reference): dark iron club, spike rows both sides, studs, rounded cap, tapered cone, cord-wrapped grip, ring pommel
             'smoke1': ['.g.', 'g.w', '.w.', 'w..'], 'smoke2': ['..g', '.w.', 'g..', '.w.', '..g']})   # Cauterize: a wisp of smoke off the sealed wound
U.POSES += [U.kleg('lk-axe-top', (34, 39), (38, 31), (41, 22), 'pointUR'),    # Leash Kick v2 axe kick: straight leg raised high, heel above the head
            U.kleg('lk-axe-chop', (34, 40), (41, 38), (48, 37), 'pointFwd'),   # heel chopping down through shoulder height
            U.kleg('lk-axe-down', (34, 41), (40, 46), (45, 52), 'toe30k')]     # driven down, foot about to land in front
TUCK_SPIN_N, TUCK_SPIN_F = band(-20, 212), band(-45, 222)   # arms tucked tight for the pirouette (as the Whirlwind Kick)
U.POSES += [kleg('st-vn', (33, 42), (40, 49), (46, 55), 'pointDR'), kleg('st-vf', (31, 42), (24, 49), (18, 55), 'pointDL'),   # Spinning Top (drawn upright, then turned over): legs flung wide in a V
            kleg('st-tn', (33, 42), (41, 48), (37, 41), 'pointUL'), kleg('st-tf', (31, 42), (38, 49), (33, 42), 'pointUL'),   # knees tucked (turned over: knees bent over the face, entering and leaving the spin)
            kleg('st-nn', (33, 42), (34, 50), (34, 57), 'toe30k'), kleg('st-nf', (31, 42), (30, 50), (30, 57), 'toe30k')]       # legs swept together (the V seen edge-on mid-turn)
ST_V, ST_N, ST_T = dict(ln='st-vn', lf='st-vf'), dict(ln='st-nn', lf='st-nf'), dict(ln='st-tn', lf='st-tf')
ST_AN, ST_AF = band(-135, -170), band(140, 172)   # (upright) hands up beside the head: turned over they brace on the floor by the head
def _loop(k, n=8, rx=7, ry=2, dy=-10, motes=3):   # Dogma: purple motes looping round over the head (anchored to the head), a full turn every n frames, with a faint dotted ring
    pts = [('dotP', 'head', round(rx * math.cos(t)), round(ry * math.sin(t)) + dy) for t in [2 * math.pi * (j + k / n) / 16 for j in range(0, 16, 2)]]
    for m in range(motes):
        a = 2 * math.pi * (k / n + m / motes)
        pts.append(('moteP' if math.sin(a) > 0 else 'moteK', 'head', round(rx * math.cos(a)), round(ry * math.sin(a)) + dy))
    return pts
U.POSES += [kleg('ms-lift-lead', (33, 41), (40, 36), (40, 45), 'toe30k'), kleg('ms-lift-rear', (31, 42), (36, 37), (34, 46), 'toe30k'),
            leg('ms-wide-lead', (33, 45), (40, 51), 43), leg('ms-wide-rear', (30, 45), (23, 51), 20)]   # the deep, wide rooted stance   # Mountain Stance: a knee raised high before the stamp (sumo shiko)
EARTH_RECOLOR = {'#ffe14d': '#d9fff6', '#ff8a1c': '#7fe3d0', '#d8321a': '#8a6236'}   # Taurus: fire helpers drawn in crystal glint, crystal teal and soil brown
DUST_TRAIL = {(255, 255, 255): (0xc7, 0x9a, 0x5b), (0xe3, 0xe3, 0xe3): (0x8a, 0x62, 0x36)}   # Bull Rush: motion streak recoloured to kicked-up dust
def _dustkick(p, k):   # Bull Rush: a burst of dust and grit at each sprint foot instead of flames
    at = _foot(p)
    return [(('dust2', 'dust1')[k % 2], at)] + ([('rocks', [at[0] - 6, 60])] if at[1] == 63 else [])
DUST_WAKE = [[('dust2', [12, 63]), ('dust1', [4, 62]), ('dust1', [16, 58])], [('dust1', [13, 63]), ('dust2', [5, 63]), ('rocks', [10, 56])]]
SPIN = lambda d, f: {'state': 'spinPivot', 'dir': d, 'frame': f, 'dx': 2}

NPAL.update({'T': '#3a9e8f', 'i': '#24252b', 'j': '#4a4c55', 'h': '#9a9da8', 'u': '#a08a62', 'v': '#6e5c3e'})   # i/j/h: kanabo iron (dark, mid, highlight); u/v: its cord wrap   # earth: deep crystal teal (the shaded facet of a gem)
def _dome(f, rx=21, ry=55, crystals=False):   # Root Sanctuary: two gnarled roots growing up from the floor either side and arching over the head; f = how far they have grown (1 = met overhead)
    h, w = ry + 2, 2 * rx + 9; cx, base = w // 2, ry + 1
    rows = [['.'] * w for _ in range(h)]
    def put(x, y, c):
        if 0 <= x < w and 0 <= y < h and (rows[y][x] == '.' or c in 'KC'): rows[y][x] = c
    for side in (1, -1):
        for i in range(161):
            t = i / 160 * f * math.pi / 2
            x = cx + side * round(rx * math.cos(t) + 1.6 * math.sin(t * 13)); y = base - round(ry * math.sin(t))
            put(x + side, y, 'K'); put(x, y, 'E'); put(x - side, y, 'E'); put(x - 2 * side, y, 'e')
            if i % 23 == 11: put(x - side, y, 'K')
            if i % 31 == 7: put(x - 2 * side, y, 'K')
            if i % 4 == 2 and i > 4:   # v2 (Christopher 2026-10-28: more root hairs): fine 1 px hairs fraying off both edges, alternating up and down
                up = (i // 4) % 2; ln = 2 + (i // 4) % 3
                for j in range(1, ln + 1): put(x + side * (1 + j), y - (j if up else -j) // 2 - (j > 1 and up), 'e' if j < ln else 'u')
                if i % 8 == 2:
                    for j in range(1, 3): put(x - side * (2 + j), y + j, 'e')
        for t0, ln in ((0.12, 4), (0.45, 3), (0.85, 3)):   # rootlets kicking out sideways
            if t0 <= f * math.pi / 2:
                x = cx + side * round(rx * math.cos(t0) + 1.6 * math.sin(t0 * 13)); y = base - round(ry * math.sin(t0))
                for j in range(1, ln + 1): put(x + side * j, y - j // 2, 'E')
                put(x + side * (ln + 1), y - ln // 2 - 1, 'e'); put(x + side * (ln + 1), y - ln // 2 + 1, 'e'); put(x + side * (ln - 1), y - ln // 2 + 1, 'u')   # hairs on the rootlet tips
        for j in range(1, 6): put(cx + side * (rx + 1 + j), base - (j > 3), 'E')   # roots spreading along the floor
        if crystals:
            for t0 in (0.3, 0.7, 1.1):
                x = cx + side * round(rx * math.cos(t0) + 1.6 * math.sin(t0 * 13)); y = base - round(ry * math.sin(t0))
                put(x - 2 * side, y, 'C'); put(x - 2 * side, y - 1, 'c')
    return [''.join(r) for r in rows]
SANCT_DY = -(55 + 1) / 2   # sits the dome's base row on the floor under the feet
NPAT.update({**{'sanct%d' % n: _dome(n / 100) for n in (20, 45, 70, 90)}, 'sanct100': _dome(1.0, crystals=True), 'sanctBare': _dome(1.0),
             'leafC': ['.c.', 'cCT', '.T.'],
             'eyeC': ['.C.', 'CcC', '.C.'], 'eyeCF': ['..C..', '.CcC.', 'CcWcC', '.CcC.', '..C..'],   # Taurus genjutsu: the eyes kindle crystal teal
             'gem1': ['.c.', 'cCT', '.T.'], 'gem2': ['..W..', '.cCC.', 'cCcCT', '.CCT.', '..T..'],
             'gem3': ['...W...', '..cCC..', '.cCcCC.', 'cCcWCCT', '.CCCCT.', '..CTT..', '...T...'],   # Material Fixation: an illusory crystal gem, the object of the obsession
             'glint': ['..c..', '..W..', 'cWWWc', '..W..', '..c..'], 'glit': ['c.W', '.c.', 'W.c'],
             'fix1': _arc(4, 2, 'cC'), 'fix2': _arc(7, 3, 'WcC'), 'fix3': _arc(10, 3, 'cCT'), 'fix3d': _arc(12, 4, 'CT', gap=2),
             'planet1': ['.e.', 'eEE', '.EK'], 'planet2': ['...ee....', '..eeEE...', 'CcCEEECCc', '..EEEK...', '...EK....'],
             'planet3': ['....eee....', '...eeeEE...', '..eeEEEEE..', 'cCCeEEEECCc', '..EEEEEEK..', '...EEEKK...', '....KKK....'],   # Planetary Pressure: an illusory planet, soil brown with a crystal ring
             'gp1': _sag(5, 2, 'eE'), 'gp2': _sag(8, 3, 'cCE'), 'gp3': _sag(11, 4, 'eEK'), 'gp3d': _sag(13, 4, 'EK', gap=2),
             'gline': ['e', '.', 'E', 'E', '.', 'K']})   # gravity: dashes falling on the target

NPAL.update({'S': '#e6c27a', 's': '#9c7434', 'Z': '#fff0c4'})   # Virgo: sand (body, shade, sunlit grain)
def _sandcloud(w, h, dens, seed, cone=False):   # a cloud of sand grains: dense sandy core, dark grains thinning out to the edge; cone: a fan opening toward the facing
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            dx, dy = (x - (w - 1) / 2) / (w / 2), (y - (h - 1) / 2) / (h / 2)
            if cone: dx, dy = x / w, abs(dy) / max(0.15, x / w)
            d = (dx * dx + dy * dy) ** 0.5 if not cone else dy
            if d < 1 and rnd.random() < dens * (1.2 - d):
                rows[y][x] = 'Z' if d < 0.35 and rnd.random() < 0.4 else 'S' if d < 0.65 else 's'
    return [''.join(r) for r in rows]
NPAT.update({'sandH': ['.S.', 'SsS', '.s.'], 'sandTrk': ['S', 's', '.', 'S', '.', 's', '.', '.', 'S'], 'sandPuff': ['..s.Z..s', '.sSsSsS.', 'sSsZsSsS', 'ssSSSSss'],   # Virgo: a fistful of sand, grains trickling, sand scooped off the floor
             'sandSpray': _sandcloud(9, 9, 0.8, 1, cone=True), 'sandBurst': _sandcloud(11, 13, 0.85, 2), 'sandCloud': _sandcloud(13, 17, 0.6, 3), 'sandCloud2': _sandcloud(13, 19, 0.35, 4),   # Silica Strike: sand flung into the face, bursting and drifting
             'hglass': ['vvvvvvvvv', '.c.....c.', '.cZSSSSc.', '..cSSSc..', '...cSc...', '....S....', '...c.c...', '..c.S.c..', '.c..S..c.', '.c.SSS.c.', 'vvvvvvvvv'],
             'hglass2': ['vvvvvvvvv', '.c.....c.', '.c.....c.', '..cZSSc..', '...cSc...', '....S....', '...cSc...', '..c.S.c..', '.c.SSS.c.', '.cSSSSSc.', 'vvvvvvvvv'],   # Flowing Sand Parry: an illusory hourglass beside the head, sand running through it
             'grains': ['Z...S', '..s..', 'S...Z'], 'sandArc': _arc(5, 2, 'sSZ'), 'sandArc2': _arc(7, 3, 'sS', gap=2),
             'vital': ['..c..', '.cWc.', 'cWWWc', '.cWc.', '..c..'], 'vital2': ['c...c...c', '.c..c..c.', '..cCWCc..', '..CWWWC..', 'ccWWWWWcc', '..CWWWC..', '..cCWCc..', '.c..c..c.', 'c...c...c'], 'wither': ['v.u', '.v.', 'u.v'], 'wither2': ['u..v.', '.v..u', 'v.u..', '..v.u']})   # Wither Palm: a teal flash at each vital point struck, dull dust of the strength draining out

def _whirl(h, r0, r1, phase, seed, arms=3, shards=0):   # Sandstorm: a sand tornado h px tall, r0 wide at the foot opening to r1 at the top, streaks spiralling round it;
    import random                                        # returns (front, back): the front half is drawn over the fighter, the back half only where it is not drawn
    rnd = random.Random(seed); w = 2 * r1 + 3; cx = r1 + 1
    fr = [['.'] * w for _ in range(h + 4)]; bk = [['.'] * w for _ in range(h + 4)]
    for y in range(h):
        t = 1 - y / max(1, h - 1); rx = r0 + (r1 - r0) * t; ry = max(1.0, rx * 0.2)
        for j in range(arms):
            for u in range(7):
                if y % 2 and arms == 2 and h > 20: continue   # the big storm: every other row, so the fighter shows through
                a = phase + y * 0.3 + j * 2 * math.pi / arms + u * 0.13
                X = round(cx + rx * math.cos(a)); Y = round(y + 2 + ry * math.sin(a))
                if not (0 <= X < w and 0 <= Y < h + 4) or rnd.random() < 0.25: continue
                front = math.sin(a) > 0
                c = ('Z' if u > 4 else 'S' if u > 1 else 's') if front else ('S' if u > 4 else 's')
                (fr if front else bk)[Y][X] = c
    for _ in range(shards):   # shrapnel caught in the storm: crystal chips and grit
        a = rnd.random() * 2 * math.pi; y = rnd.randint(2, h - 2); rx = r0 + (r1 - r0) * (1 - y / h)
        X = round(cx + rx * math.cos(a)); Y = round(y + 2 + rx * 0.2 * math.sin(a))
        if 0 <= X < w and 0 <= Y < h + 4: (fr if math.sin(a) > 0 else bk)[Y][X] = rnd.choice('CcK')
    return [''.join(r) for r in fr], [''.join(r) for r in bk]

def _mound(hgt, w=26, seed=0, coffin=False):   # Sand Burial: a heap of sand round the legs, hgt px high; coffin: closed up over the chest, with darker squeeze bands
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(hgt)]
    for y in range(hgt):
        f = y / max(1, hgt - 1); half = (w / 2) * (0.55 + 0.45 * f) if not coffin else (w / 2) * (0.3 + 0.7 * math.sin(min(1, 0.25 + f) * math.pi / 2) ** 0.5)   # coffin: a rounded dome closing over the shoulders
        for x in range(w):
            if abs(x - (w - 1) / 2) <= half - (rnd.random() < 0.5 and y < 2):
                edge = abs(x - (w - 1) / 2) > half - 1.5 or y == 0
                rows[y][x] = 's' if edge else ('Z' if rnd.random() < 0.08 else 's' if rnd.random() < 0.18 or (coffin and (y + abs(x - w // 2) // 3) % 7 == 3) else 'S')
    return [''.join(r) for r in rows]
NPAT.update({**{'mound%d' % n: _mound(n, seed=n) for n in (6, 14, 18)}, 'coffin26': _mound(26, w=28, seed=26, coffin=True), 'coffin30': _mound(30, w=28, seed=30, coffin=True),
             **{'storm%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(52, 6, 18, k * math.pi / 2, k, arms=2, shards=8))},
             **{'whirl%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(12, 3, 7, k * math.pi / 2, 10 + k, arms=2))},
             'sandStream': ['..s..S..s.Z..S', '.SsS.sSs.SsS.s', 'sSsSsSsSsSsSsS'], 'sandRise': ['.S.s', 's.Z.', '.S.s', 'S..s']})   # Sand Burial: sand flowing along the floor toward the target, sand rising

def _gust(w, h, phase, seed, n=9):   # Sandstorm v2 target: streaks of sand blowing across the fighter; returns (front, back)
    import random
    rnd = random.Random(seed); fr = [['.'] * w for _ in range(h)]; bk = [['.'] * w for _ in range(h)]
    for i in range(n):
        y = rnd.randint(1, h - 2); L = rnd.randint(4, 9); x0 = (rnd.randint(0, w - 1) + phase * 9) % w; q = fr if i % 2 == 0 else bk
        for u in range(L):
            X = (x0 + u) % w; Y = y + (1 if u > L // 2 and i % 3 == 0 else 0)
            q[min(h - 1, Y)][X] = 'Z' if u == L - 1 else 'S' if u > L // 3 else 's'
            if i % 2 == 0 and 0 < u < L - 1: q[min(h - 1, Y + 1)][X] = 's'
    for _ in range(3):
        y = rnd.randint(2, h - 3); x = (rnd.randint(0, w - 1) + phase * 9) % w; (fr if rnd.random() < 0.5 else bk)[y][x] = rnd.choice('CcK')
    return [''.join(r) for r in fr], [''.join(r) for r in bk]
NPAT.update({**{'eye%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(50, 15, 22, k * math.pi / 2, 30 + k, arms=4, shards=14))},   # Sandstorm v2: the storm round the caster, wide at the foot so the fighter stands in its eye
             **{'eyeMid%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(30, 15, 19, k * math.pi / 2, 40 + k, arms=4, shards=6))},
             **{'eyeLow%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(12, 14, 16, k * math.pi / 2, 50 + k, arms=3))},
             **{'gust%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _gust(34, 40, k, 60 + k, n=18))},
             'stormRing': _whirl(12, 14, 16, 0, 50, arms=2)[0], 'sandSprayL': [r[::-1] for r in NPAT['sandSpray']]})
U.POSES += [leg('ss-kneel-lead', (33, 50), (41, 49), 42), U.kleg('ss-kneel-rear', (31, 50), (29, 55), (20, 55), 'toe30k')]   # Silica Strike v2: down on the rear knee, lead foot flat in front, thigh level
NPAT.update({'sandSprayUp': [''.join(r[y] for r in NPAT['sandSpray'][::-1]) for y in range(len(NPAT['sandSpray'][0]))][::-1]})
def _ring(r, ch='c', ch2='C', gap=0):   # Wither Palm v2: a thin shock ring of radius r (flattened a little), every other pixel when gap
    w = 2 * r + 1; h = 2 * round(r * 0.8) + 1; rows = [['.'] * w for _ in range(h)]
    for k in range(int(8 * r)):
        a = 2 * math.pi * k / (8 * r); x = round(r + r * math.cos(a)); y = round((h - 1) / 2 + (h - 1) / 2 * math.sin(a))
        if gap and k % 2: continue
        rows[y][x] = ch if math.sin(a) < 0.3 else ch2
    return [''.join(q) for q in rows]
NPAT.update({'palmGlow': ['..ccc..', '.cC.Cc.', 'cC...Cc', 'c.....c', 'cC...Cc', '.cC.Cc.', '..ccc..'], 'streak': ['CCcc.c..c', '.ccc.c...'], 'vRing': _ring(5), 'vRing2': _ring(7), 'vRing3': _ring(9, gap=1),
             'witherPlume': ['..u.v..', '.uvuvu.', 'vuuvvuv', '.vuvuv.', '..v.u..', '...u...', '..v....'], 'witherBurst': ['u...v...u', '.vu.u.uv.', 'u.vuvuv.u', '.uvvuvvu.', 'vuuvuvuuv', '.uvvuvvu.', 'u.vuvuv.u', '.vu.v.uv.', 'u...u...v']})   # Wither Palm v2: palm glow, strike streak, dust plumes
def _coffin(w, h, seed, lid=False, crack=0):   # Coffin Syndrome v2: an upright coffin, a box of packed sand outlined in crystal teal; lid: the front lid (a darker seam band, two teal studs); crack: 1-2 crack lines across the lid
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        sh = 0.62 + 0.38 * min(1, y / (h * 0.22)) if y < h * 0.22 else 1 - 0.3 * (y - h * 0.22) / (h * 0.78)   # wide at the shoulders, tapering to the foot
        half = (w - 1) / 2 * sh
        for x in range(w):
            dx = abs(x - (w - 1) / 2)
            if dx > half: continue
            edge = dx > half - 1 or y in (0, h - 1)
            rows[y][x] = 'C' if edge else ('c' if edge and rnd.random() < 0.2 else 'Z' if rnd.random() < 0.06 else 's' if rnd.random() < 0.25 else 'S')
            if lid and not edge and (abs(dx - half + 3) < 0.6 or y in (3, h - 4)): rows[y][x] = 's'
    if lid:
        for y in (h // 4, 3 * h // 4): rows[y][w // 2] = 'c'
    for c_ in range(crack):   # cracks zigzagging across the lid
        y0 = h // 3 + c_ * h // 4; x = 2
        while x < w - 2:
            if rows[y0][x] != '.': rows[y0][x] = 'K'
            x += 1; y0 += rnd.choice((-1, 0, 1)) if 2 < y0 < h - 3 else 0
    return [''.join(r) for r in rows]
def _squash(pat, w):   # the lid seen swinging round on its hinge: the same lid squeezed to w columns
    W = len(pat[0]); return [''.join(r[min(W - 1, int(x * W / w))] for x in range(w)) for r in pat]
NPAT.update({'cofBack': _coffin(32, 56, 1), 'cofLid': _coffin(32, 56, 2, lid=True), 'cofLidCrack': _coffin(32, 56, 2, lid=True, crack=1), 'cofLidCrack2': _coffin(32, 56, 2, lid=True, crack=2)})
NPAT.update({'cofLid1': _squash(NPAT['cofLid'], 9), 'cofLid2': _squash(NPAT['cofLid'], 20), 'cofBackLow': _coffin(32, 56, 1)[14:], 'cofBackLow2': _coffin(32, 56, 1)[30:],
             'plank': ['CCCCCCC', 'CsSsSsC', 'CCCCCCC'], 'plankV': ['CCC', 'CSC', 'CsC', 'CSC', 'CsC', 'CCC']})
NPAL.update({'X': '#120d16', 'x': '#3a2f40'})   # Virgo genjutsu: the phantom's shadow (near-black, smoky edge)
def _scale(pat, f):   # nearest-neighbour enlargement of a pattern by f (Virgo genjutsu v1: the phantom and the coffin drawn bigger)
    h, w = len(pat), len(pat[0]); H, W = round(h * f), round(w * f)
    return [''.join(pat[min(h - 1, int(y / f))][min(w - 1, int(x / f))] for x in range(W)) for y in range(H)]
NPAT.update({'wraith0': ['....xxxx.....', '...xXXXXx....', '..xXXXXXXx...', '..xXXCXCXx...', '..xXXXXXXXx..', '...xXXXXXXXx.', '..xXXXXXXXXXx', '.xXXXXXXX.xXX', '.xXXXXXXX...X', 'xXXXXXXXx....', 'xXXXXXXXx....', '.xXXXXXXx....', '.xXXXXXx.....', '..xXXXXx.....', '..xXXXx......', '...xXx.x.....', '...x.x..x....', '....x........'],   # Phantom Plague: a hunched shadow creature with teal eyes, a clawed arm reaching forward, a wispy tail
             'wraithRise': ['....xxxx.....', '...xXXXXx....', '..xXXXXXXx...', '..xXXCXCXx...', '..xXXXXXXXx..', '...xXXXXXXXx.', '..xXXXXXXXXXx', '.xXXXXXXX.xXX', '.xXXXXXXX...X'], 'shadowPool': ['..xxxxxxx..', '.xXXXXXXXx.', 'xXXXXXXXXXx', '.xxXXXXXxx.'], 'shadowPool2': ['....xxxxx....', '.xxXXXXXXXxx.', 'xXXXXXXXXXXXx', '.xxXXXXXXXxx.'],
             'coffinUp': ['..CCC..', '.CsssC.', 'CsssssC', 'CssWssC', 'CsWWWsC', 'CssWssC', 'CsssssC', 'CsssssC', 'CsssssC', '.CsssC.', '.CsssC.', '.CsssC.', '..CsC..', '..CCC..'],   # Coffin Syndrome: an illusory coffin (crystal-teal outline, sand), standing, then slammed flat
             'coffinFlat': ['..CCCCCCCCCC...', '.CsssWsssssssC.', 'CsssWWWsssssssC', '.CsssWsssssssC.', '..CCCCCCCCCC...'],
             'cs1': _sag(5, 2, 'Ss'), 'cs2': _sag(8, 3, 'ZSs'), 'cs3': _sag(11, 4, 'SsK'), 'cs3d': _sag(13, 4, 'sK', gap=2)})   # Coffin Syndrome: sand pressure bearing down on the buried
NPAT.update({'wraith': _scale(NPAT['wraith0'], 1.6), 'wraithRise': _scale(NPAT['wraithRise'], 1.6), 'coffinUp': _scale(NPAT['coffinUp'], 1.5), 'coffinFlat': _scale(NPAT['coffinFlat'], 1.4)})
NPAT.update({'sandBurstL': _sandcloud(15, 17, 0.85, 5), 'sandCloudL': _sandcloud(17, 21, 0.6, 6), 'sandCloudL2': _sandcloud(17, 23, 0.35, 7), 'sandSprayUpL': _scale(NPAT['sandSprayUp'], 1.5), 'sandSprayL2': _scale(NPAT['sandSpray'], 1.4)})   # Silica Strike v5 (Christopher 19:28: more fx): bigger burst, cloud and spray
U.POSES += [kleg('as-lift', (34, 41), (39, 45), (37, 52), 'toe30k'), kleg('as-chamber', (34, 40), (41, 38), (39, 46), 'toe30k'),   # Capricorn Adamantine Shin: knee lifted, then chambered high
            kleg('as-kick', (34, 41), (42, 44), (51, 45), 'pointFwd'), kleg('as-kick2', (34, 41), (42, 45), (52, 47), 'pointFwd'),     # the shin swung through level at the opponent's thigh, then driving through
            kleg('as-recoil', (34, 41), (39, 46), (35, 52), 'toe30k')]
AS_SEG = {'as-lift': ((39, 45), (37, 52)), 'as-chamber': ((41, 38), (39, 46)), 'as-kick': ((42, 44), (51, 45)), 'as-kick2': ((42, 45), (52, 47)), 'as-recoil': ((39, 46), (35, 52))}   # E knee -> ankle of each kick pose (crystal sheath)
def _spikes(w, h, n, seed, lean=0, widths=(3, 4, 5)):   # Capricorn Geode Blast: a cluster of n crystal spikes erupting from the floor, w wide, the tallest h high: each spike a pointed prism, glint c on its lit (left) face, body C, deep teal T on its shaded face and outline
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for i in range(n):
        sw = rnd.choice(widths); sh = max(4, round(h * rnd.uniform(0.45, 1.0)) if i else h); x0 = round((w - sw) * (i + 0.5) / n + rnd.uniform(-1.5, 1.5)); x0 = max(0, min(w - sw, x0))
        tip = sw // 2
        for yy in range(sh):
            y = h - 1 - yy; f = yy / max(1, sh - 1); shift = round(lean * f * 2)
            half = sw / 2 if f < 0.7 else (sw / 2) * (1 - f) / 0.3 + 0.5
            for xx in range(sw):
                if abs(xx + 0.5 - sw / 2) > half: continue
                X = x0 + xx + shift
                if not 0 <= X < w: continue
                edge = xx == 0 or xx == sw - 1 or abs(xx + 0.5 - sw / 2) > half - 1
                rows[y][X] = 'T' if (edge and xx >= tip) or xx > tip else 'c' if xx < tip and (edge or yy % 4 == 1) else 'C'
    return [''.join(q) for q in rows]
NPAT.update({'geoBack': _spikes(34, 30, 6, 11), 'geoFrontL': _spikes(16, 22, 3, 12, lean=-1), 'geoFrontR': _spikes(16, 24, 3, 15, lean=1), 'geoSmall': _spikes(24, 10, 5, 13), 'geoSmallB': _spikes(28, 12, 5, 14),
             'geoBack2': _spikes(34, 30, 6, 11)[10:], 'geoFrontL2': _spikes(16, 22, 3, 12, lean=-1)[8:], 'geoFrontR2': _spikes(16, 24, 3, 15, lean=1)[8:], 'rubble': ['..T.c..T..', '.TCcT.cCT.', 'TCcCTTCcCT'],
             'bloodN': ['M.', '.m', 'M.'], 'shardFly': ['c...T', '.C.C.', 'T...c'],
             'crackGlow': ['C.....C', '.C...C.', '.cCcCc.'], 'crackRun': ['C.........K', '.KC....K.C.', '...KCKC.K..']})
NPAL.update({'G': '#8c8478', 'H': '#b3aa9a', 'N': '#544c42'})   # Capricorn Mausoleum: tomb stone (mid, lit, dark mortar)
def _slab(w, h, seed, arch=False, seam=True):   # Mausoleum: a wall of dressed stone blocks w x h (courses 6 px high, joints staggered), lit top/left edge H, dark right edge and mortar N, a crystal-teal seam glowing in one joint; arch: the top rounded like a tomb's headstone
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    seamRow = rnd.randrange(6, max(7, h - 4), 6) if seam and h > 8 else -1
    for y in range(h):
        for x in range(w):
            if arch:
                r = w / 2; top = r - math.sqrt(max(0, r * r - (x + 0.5 - r) ** 2))
                if y < top * 0.6: continue
            course = y // 6; jx = (x + (3 if course % 2 else 0) + seed) % 9
            ch = 'G'
            if y % 6 == 5 or jx == 0: ch = 'N'
            if (x + y * 3 + seed) % 11 == 0: ch = 'H' if ch == 'G' else ch
            if x == 0 or (arch and y < 3) or y == 0: ch = 'H'
            if x == w - 1: ch = 'N'
            if y == seamRow and 0 < x < w - 1: ch = 'C' if x % 3 else 'c'
            rows[y][x] = ch
    return [''.join(q) for q in rows]
def _pillar(w, h, seed):   # Mausoleum v2: a fluted stone pillar w wide, h high, with a wider capital and base (2 px each side), lit left edge H, dark right edge N, a crystal-teal seam ringing it a third of the way up
    rows = []
    for y in range(h):
        if y < 3 or y >= h - 3: rows.append('H' + 'G' * (w + 2) + 'N' if y in (0, h - 3) else 'H' + ''.join('N' if (x + seed) % 5 == 0 else 'G' for x in range(w + 2)) + 'N'); continue
        mid = ''.join('N' if x % 3 == 2 else 'H' if x % 3 == 0 and (y + seed) % 7 else 'G' for x in range(w - 2))
        if y == round(h * 0.66): mid = ''.join('C' if x % 2 else 'c' for x in range(w - 2))
        rows.append('.' + 'H' + mid + 'N' + '.')
    return rows
def _roof(w, h):   # Mausoleum v2: the roof slab dropped on the pillars: a low pediment (triangle) over a thick lintel, crystal-teal seam along the lintel
    rows = []
    for y in range(h):
        if y < h - 5:
            half = round((w / 2) * (y + 1) / (h - 5)); row = ['.'] * w
            for x in range(w // 2 - half, w // 2 + half): row[x] = 'H' if x < w // 2 else 'G'
            if half: row[w // 2 - half] = 'H'; row[min(w - 1, w // 2 + half - 1)] = 'N'
            rows.append(''.join(row))
        else:
            yy = y - (h - 5); rows.append('N' * w if yy in (0, 4) else ''.join('C' if x % 3 else 'c' for x in range(w)) if yy == 2 else 'H' + 'G' * (w - 2) + 'N')
    return rows
NPAT.update({'pillar': _pillar(7, 55, 1), 'roof': _roof(40, 9)})
NPAT.update({**{'pillar%d' % n: NPAT['pillar'][-round(55 * n / 3):] for n in (1, 2)}})
NPAT.update({'tombBack': _slab(30, 54, 3, arch=True), 'tombFront': _slab(30, 20, 5)})
NPAT.update({'stalBack': _spikes(44, 58, 5, 21, widths=(7, 8, 9)), 'stalFrontL': _spikes(18, 34, 2, 22, lean=-1, widths=(6, 7)), 'stalFrontR': _spikes(18, 38, 2, 23, lean=1, widths=(6, 7, 8)), 'stalTips': _spikes(30, 8, 6, 24), 'stalTipsS': _spikes(12, 5, 3, 25)})   # Capricorn Stalactite Rain: giant crystal spears
NPAT.update({'stalBack2': NPAT['stalBack'][20:], 'stalFrontL2': NPAT['stalFrontL'][12:], 'stalFrontR2': NPAT['stalFrontR'][14:]})
def _spear(L, ux, uy, w=5):   # Stalactite Rain v2: one crystal spear L px long pointing along (ux, uy) (tip at that end), w px thick, tapering to the point over its last third; glint c down one side, deep teal T down the other and at the butt
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n; px_, py_ = -uy, ux
    pts = {}
    for i in range(L * 3):
        t = i / 3; f = t / L; half = (w / 2) * (1 if f < 0.66 else max(0.15, (1 - f) / 0.34))
        for j in range(-w * 2, w * 2 + 1):
            o = j / 4
            if abs(o) > half: continue
            x, y = round(t * ux + o * px_), round(t * uy + o * py_)
            ch = 'c' if o < -half + 1 else 'T' if o > half - 1 or t < 1 else 'C'
            if (x, y) not in pts or ch == 'C': pts[(x, y)] = ch
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]; x0, y0 = min(xs), min(ys)
    rows = [['.'] * (max(xs) - x0 + 1) for _ in range(max(ys) - y0 + 1)]
    for (x, y), ch in pts.items(): rows[y - y0][x - x0] = ch
    return [''.join(q) for q in rows]
NPAT.update({'spearUp': _spear(40, 0, -1, 7), 'spearUpS': _spear(30, -0.1, -1, 6), 'spearFall': _spear(30, -0.55, 1, 6), 'spearFallS': _spear(24, -0.45, 1, 5), 'spearStreak': ['c', 'C', '.', 'c', '.', '.', 'c']})
NPAT.update({'spearUp1': NPAT['spearUp'][-12:], 'spearUp2': NPAT['spearUp'][-26:], 'spearUpS1': NPAT['spearUpS'][-9:], 'spearUpS2': NPAT['spearUpS'][-20:]})
NPAT.update({**{'tombBack%d' % n: NPAT['tombBack'][-round(54 * n / 3):] for n in (1, 2)}, **{'tombFront%d' % n: NPAT['tombFront'][-round(20 * n / 3):] for n in (1, 2)}})
NPAT.update({'gemShard': ['.c.', 'cCT', '.T.'], 'gemShard2': ['..c..', '.cCc.', 'cCCTT', '.CTT.', '..T..'], 'gemSpark': ['c.c', '.W.', 'c.c'],   # Capricorn: crystal shards and glints
             'gemBurst': _ring(5, 'c', 'C'), 'gemBurst2': _ring(8, 'C', 'T', gap=1), 'gemCrack': ['T...T', '.T.T.', '..W..', '.T.T.', 'T...T'],
             'slash': ['......cW', '....cWc.', '..cWc...', 'cWc.....', 'c.......'], 'slash2': ['.........cWW', '.......cWWc.', '.....cWWc...', '...cWWc.....', '.cWWc.......', 'cWc.........']})
NPAT.update({'wraithM': [r[::-1] for r in NPAT['wraith']]})   # Phantom Plague v2: the phantom turned round, facing back at the victim as it passes in front
NPAT.update({'clawMark': ['C...C...C....', '.C...C...C...', '..C...C...C..', '...C...C...C.', '....c...c...c'], 'clawMark2': ['..........', 'c...c...c.', '.c...c...c.'[:10], '..c...c...']})   # Phantom Plague target: three teal claw marks raked down past the victim

def _column(h, w, phase, tight, cracks=0, seed=0):   # Sand Burial v2 (Christopher 2026-10-28: sand up to the target's neck, squeezing it): a column of sand from the neck down,
    import random                                     # rounded over the shoulders, pinched in by tight (0-1), dark constriction bands winding round it (phase), cracks before the break
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]; c0 = (w - 1) / 2
    for y in range(h):
        sh = min(1.0, 0.45 + y / 6)   # narrow at the neck, out over the shoulders
        half = (w / 2) * sh * (1 - tight * 0.26 * math.sin(math.pi * min(1, y / (h * 0.7))))
        for x in range(w):
            dx = abs(x - c0)
            if dx > half: continue
            edge = dx > half - 1.3 or y == 0
            band_ = (y + round((x - c0) * 0.6) + phase * 2) % 7 == 0
            rows[y][x] = 's' if edge else ('v' if band_ and tight > 0.5 else 's' if band_ else 'Z' if rnd.random() < 0.07 else 's' if rnd.random() < 0.12 else 'S')
    for k in range(cracks):   # jagged dark cracks splitting the sand
        x = round(c0 + (k - (cracks - 1) / 2) * w / (cracks + 1)); y = rnd.randint(1, 4)
        while y < h - 2:
            if 0 <= x < w and rows[y][x] != '.': rows[y][x] = 'K'
            y += 1; x += rnd.choice((-1, 0, 0, 1))
    return [''.join(r) for r in rows]

def _shatter(R, seed, chunks=14):   # Sand Burial break free: chunks of packed sand blown outward in a ring R px out, grains between
    import random
    rnd = random.Random(seed); n = 2 * R + 5; rows = [['.'] * n for _ in range(n)]; c = n // 2
    for i in range(chunks):
        a = 2 * math.pi * (i + rnd.random() * 0.5) / chunks; r = R + rnd.randint(-3, 2)
        x, y = round(c + r * math.cos(a)), round(c + r * math.sin(a))
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            if 0 <= x + dx < n and 0 <= y + dy < n: rows[y + dy][x + dx] = 's' if (dx + dy) == 2 else 'S'
        for _ in range(3):
            q = r - rnd.randint(2, 6); X, Y = round(c + q * math.cos(a + rnd.uniform(-0.2, 0.2))), round(c + q * math.sin(a + rnd.uniform(-0.2, 0.2)))
            if 0 <= X < n and 0 <= Y < n: rows[Y][X] = rnd.choice('SsZ')
    return [''.join(r) for r in rows]
NPAT.update({**{'col%d' % k: _column(52, 24, k, (0.4, 1.0, 0.6, 1.0)[k], seed=k) for k in range(4)}, 'colRise': _column(52, 24, 0, 0.0, seed=9),
             'colCrack1': _column(52, 24, 1, 1.0, cracks=2, seed=11), 'colCrack2': _column(52, 24, 2, 1.0, cracks=4, seed=12),
             'shatter12': _shatter(12, 1), 'shatter18': _shatter(18, 2), 'shatter23': _shatter(23, 3, chunks=18)})   # Sand Burial v2: the neck-high column squeezing, cracking, blown apart

CLIPS = {
 'machLunge': ('Mach Lunge', 9,
  'Mach Lunge (Aries taijutsu, Priority gap closer, burns the target), v4 (Christopher 2026-10-27: the sprint instead of a single hop, flames around the feet; afterimages for speed): from the guard the fighter dips, then breaks into the approved sprint (the same stride, lean and swept-back arms), flames bursting around the feet at every step, a stream of fire and four fire-tinted afterimages trailing behind; on the last stride it tucks both arms tight, plants the lead foot and drives the lead shoulder into the target with a flare of flame at the point of contact; then settles back into the guard. The fighter travels 40 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead')] + [
     g(an=SPRINT_N[k], af=SPRINT_F[k], bob=(SPRINT_DY[k],) * 3, lean=(1, 8), root=(6, 0), ln='sr-' + SPRINT_LEGS[k], lf='sr-' + SPRINT_LEGS[(k + 4) % 8]) for k in range(6)] + [
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 7), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 6), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3)),
     g()],
  [None, 'squint'] + ['squint'] * 6 + ['squint', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='light', rm='E: 6 px a stride through the sprint (as the sprint), +3 and +1 into the shoulder check; 40 px in all (travel)',
       ghosts={k: (5, 10, 15, 20) for k in range(2, 8)} | {8: (5, 10, 15), 9: (4, 8), 10: (3,)}, ghostColors=(('#ffe14d', '#ff8a1c'), ('#ff8a1c', '#ffe14d'), ('#d8321a', '#ff8a1c'), ('#d8321a', None)),
       blur={k: 9 for k in range(2, 8)} | {8: 7, 9: 4}, trail=FIRE_TRAIL,
       fx=nfx('fire flame (reds, oranges, yellows): flames bursting around the feet at every stride, a stream of fire trailing behind, a flare where the shoulder lands',
              [(k, FOOT_FLAMES[k - 2] + FIRE_WAKE[k % 2]) for k in range(2, 8)] + [(8, [('flame3', [47, 32]), ('flame1', [40, 63])] + FIRE_WAKE[0][:3]), (9, [('flame3', [48, 31]), ('embers', [45, 24])]), (10, [('embers', [48, 24])])]),
       extra={'airborneFrames': [5], 'travel': {'rule': 'Mach Lunge is a gap closer: the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}})),
 'shatterPunch': ('Shatter Punch', 5,
  'Shatter Punch (Aries taijutsu, Guard Break, can stun), v3 (Christopher 2026-10-27: swirling fx around the winding arm, a more dramatic impact): from the guard the fighter sits its weight back and draws the rear fist far back beside the ear, elbow high, the lead hand reaching out to measure; flame swirls up around the cocked arm, winding tighter and brighter over three held frames; then it steps in and fires the rear fist dead straight through the target with the whole body behind it, rear heel turning up; on contact a white-hot flash bursts at the fist, a ring of fire shock blasts outward, jagged cracks shoot off and shards and embers scatter, the punch held through a hit-stop; then it pulls back into the guard.', [
     g(),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(0, 0), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 on the step into the punch, -1 settling back',
       swirl={1: (0, 0.35), 2: (100, 0.6), 3: (210, 0.85), 4: (320, 1.0)},   # frame: (phase degrees, strength)
       impact={5: 0, 6: 1, 7: 2, 8: 3})),   # frame: stage of the burst (flash, shock ring, spread, fade)
 'blastWave': ('Blast Wave', 5,
  'Blast Wave (Aries ninjutsu, fire AoE: a small burst of fire that breaks the speed of sound), v2 (Christopher 2026-10-27: turn the fighter to face S for the release, gesture like a power-up scream): from the guard the fighter turns to face the viewer (every facing turns S for the cast), sinks into the knees with both fists pulled in low in front of the belly, head dipped, embers gathering; then it throws its head back with a roar, chest out, both fists clenched and driven down and out to the sides, elbows flared, and the wave releases: a spiked fire aura bursts out round it and sonic-boom rings blast outward, white-hot, then yellow, orange and red as they widen and break up; it holds the roar, then settles back into the guard and turns back to its facing.', [
     g(),
     g(an=band(-30, -120), af=band(-35, -125), bob=(1, 1, 2), lean=(0, 1), **LOW),
     g(), g(bob=(3, 3, 3), **LOW), g(bob=(3, 3, 3), **LOW), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(),
     g()],
  [None, 'squint', None, 'strain', 'strain', 'roar', 'roar', 'roar', None, None],
  None,
  dict(fps=10, front={2: dict(R=stances.GA['R'], L=stances.GA['L']),
                      3: dict(R=(12, -25, 0.85, 'up'), L=(-12, 25, 0.85, 'up')),        # fists pulled in low in front of the belly
                      4: dict(R=(12, -25, 0.85, 'up'), L=(-12, 25, 0.85, 'up')),        # held still (v3: no twitch between held frames)
                      5: dict(R=(42, -5, 1, 'up'), L=(-42, 5, 1, 'up')),                # fists clenched, driven down and out, elbows flared
                      6: dict(R=(42, -5, 1, 'up'), L=(-42, 5, 1, 'up')),
                      7: dict(R=(42, -5, 1, 'up'), L=(-42, 5, 1, 'up')),
                      8: dict(R=stances.GA['R'], L=stances.GA['L'])},
       burst={3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5})),   # frame: stage (embers gathering 0-1, release 2, rings out 3-4, fading 5)
 'explosiveRunes': ('Explosive Runes', 4,
  'Explosive Runes (Aries ninjutsu, trap: glowing rune traps that detonate when a foe comes near): from the guard the fighter makes the tiger seal at the chin, a fire spark kindling between the hands; then it drops low on bent knees and sweeps the near open palm, facing the floor, low and forward over the ground like sowing seed; fire falls from the palm and burns glowing rune circles into the floor ahead, nearest first, the fire line running on past the edge to the rest, each flaring bright as it is written, embers lifting off them; the fighter rises back into the guard and the runes settle to a low smouldering glow (the testbed then draws the placed runes on their tiles until they detonate).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-20, -25, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 7), **BRACE),       # palm swept low, facing the floor
     g(an=band(-45, -45, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 7), **BRACE),       # sweeping on forward over the ground
     g(an=band(-65, -60, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 6), **BRACE),       # arm out, the last rune written
     g(an=band(-30, -90), af=band(-40, -100), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, fx=nfx('fire runes: a spark at the seal, fire running along the ground from the palm, three glowing rune circles burned into the floor ahead, flaring as they are written, then smouldering',
              [(1, [('flame1', [35, 31])]), (2, [('flame2', [34, 32])]),
               (3, [('flame2', [41, 63]), ('fireLine', [44, 63]), ('embers', [38, 50])]),
               (4, [('fireLine', [42, 63]), ('runeHot', [43, 63]), ('flame1', [46, 59]), ('embers', [42, 47]), ('flame1', [44, 54])]),
               (5, [('runeLit', [43, 63]), ('fireLine', [51, 63]), ('runeHot', [54, 63]), ('embers', [45, 57]), ('embers', [48, 42]), ('flame1', [52, 52])]),
               (6, [('runeLit', [43, 63]), ('runeLit', [54, 63]), ('fireLine', [62, 63]), ('embers', [56, 57]), ('embers', [44, 56])]),
               (7, [('runeDim', [43, 63]), ('runeDim', [54, 63])])]))),
 'meteor': ('Meteor', 10,
  'Meteor (Aries ninjutsu ultimate, charge: a giant fireball called down from the sky that blankets a wide zone next round), v2 (Christopher 2026-10-27: an ultimate needs a more dramatic animation, more frames than a typical ability): from the guard the fighter makes the seal and sinks deep, straining, embers lifting off the ground all round it; a spiked fire aura flares up and grows; then it raises the near open palm high to the sky and the fireball forms above it, swelling frame by frame until it is too big for the sky to hold, white-hot at the core, roiling orange with a red rim and flames licking off it, the aura blazing; at the peak the fighter hurls the arm forward and up with a burst of light, holds the throw through a hit-stop as the meteor tears up and away trailing a thick tail of fire, embers raining back down; the glow fades from the sky and the fighter settles back into the guard (the testbed drops the meteor on the zone the next round).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=band(-120, -150, fistKind='palm'), bob=(2, 2, 2), lean=(0, -1), **LOW)] + [
     g(an=band(-130, -150, fistKind='palm'), bob=(2, 2, 2), lean=(-1, -2), **LOW) for _ in range(4)] + [
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **LOW),   # hurled forward and up
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-80, -110, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-50, -120), af=band(-50, -130), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'pain', 'pain', 'pain', 'squint'] + ['squint'] * 4 + ['squint', 'squint', 'squint', None, None, None],
  None,
  dict(fps=10, rm='E: +1 into the throw, -1 settling back',
       burst={2: 0, 3: 1, 4: 2, 5: 3, 6: 3, 7: 3, 8: 2, 9: 2, 10: 3, 11: 4, 12: 5}, burstEvery=True,   # embers rising, spiked aura flaring and blazing, then fading
       meteor={5: ('form', 2), 6: ('form', 4), 7: ('form', 7), 8: ('form', 9), 9: ('form', 11),
               10: ('flash', 0), 11: ('fly', 0), 12: ('fly', 1), 13: ('trail', 2), 14: ('trail', 3)})),
 'blindRage': ('Blind Rage', 4,
  'Blind Rage (Aries genjutsu, mental debuff: the caster projects its fury into the target\'s mind so it sees everyone as an enemy; Confusion 1 round, INT save DC 12; range Zone of Awareness), the genjutsu template: from the guard the fighter raises the near hand with two fingers up in front of the eyes and fixes the target, the far hand staying in guard; the eyes kindle red, then flare white-hot, a dark crimson aura flickering up round it with rage wisps rising off the head; it holds the stare while red rage waves pulse out from its eyes toward the target one after another, each wider than the last, orange at the core and dark crimson at the rim, breaking up as they travel; the glow dies out of the eyes and the hand drops back into the guard (the testbed then marks the confused target).', [
     g(),
     g(an=band(-40, -160, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#d8321a', '#7a1016'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Confusion ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       fx=nfx('fire genjutsu: the eyes kindle red then flare, rage wisps off the head, red rage waves pulsing out from the eyes toward the target, widening and breaking up',
              [(2, [('eyeGlint', [38, 17])]),
               (3, [('eyeFlare', [37, 18]), ('rageWisp', [30, 7]), ('rageWisp', [35, 8])]),
               (4, [('eyeFlare', [37, 18]), ('rage1', [42, 19]), ('rageWisp', [32, 6]), ('rageWisp', [27, 9])]),
               (5, [('eyeFlare', [37, 18]), ('rage2', [45, 22]), ('rage1', [42, 19]), ('rageWisp', [29, 5]), ('rageWisp', [35, 7])]),
               (6, [('eyeGlint', [38, 17]), ('rage4', [51, 28]), ('rage2', [45, 22]), ('rageWisp', [31, 4])]),
               (7, [('rage5d', [56, 30]), ('rage3', [50, 25])]),
               (8, [('rage4d', [57, 28])])]))),
 'killingIntent': ('Killing Intent', 3,
  'Killing Intent (Aries genjutsu, mental debuff: the caster focuses its bloodlust and projects it onto the foe, freezing it with fear; Stun 1 round, STR save DC 13; range Zone of Awareness), v3 (Christopher 2026-10-27: keep the demon, but as an illusory demon mask that appears over the caster\'s head, matching its facing; the body more aggressive): from the guard the fighter coils down low, hands drawn back, a near-black blood-red aura seeping up; then it surges forward a step into a wide predatory crouch, chest driven forward, both hands thrown out in front like claws, and an illusory demon mask flickers into being over its head in profile, then solidifies, horn sweeping back, eye and fangs blazing; it holds the crouch trembling with fury, dark pressure pooling at its feet, while jagged waves of killing intent roll out of the mask\'s jaws toward the target, each bigger than the last; then the mask breaks up and fades, the aura drains away and the fighter steps back into the guard (the target takes the genjutsu mark, genjutsuAfflicted, for the Stun).', [
     g(),
     g(an=band(-25, -70), af=band(-15, -60), bob=(3, 3, 3), lean=(0, -1), **LOW),          # coil: down low, hands drawn back
     g(an=band(-25, -70), af=band(-15, -60), bob=(4, 4, 4), lean=(0, -1), **LOW),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(2, 0), **BRACE),   # surge: a step in, claws thrown out
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), **BRACE),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(1, 0), **BRACE),   # trembling with fury
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(-1, 0), **BRACE),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(1, 0), **BRACE),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(-1, 0), **BRACE),
     g(an=band(-40, -100), af=band(-35, -100), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', None, None],
  [0, 1, 2, 4, 4, 4, 4, 4, 3, 1, 0],
  dict(fps=10, rm='E: +2 surging in on frame 3, a 1 px tremble on frames 5-8, -2 back on the last frame', auraColors=('#7a1016', '#2a0406'),
       extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Stun ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       mask={2: 'faint', 3: 'flare', 4: 'full', 5: 'full', 6: 'flare', 7: 'full', 8: 'flicker'},
       maskWaves={4: [('ki1', 1, 5)], 5: [('ki2', 3, 9), ('ki1', 0, 5)], 6: [('ki3', 7, 13), ('ki2', 3, 9)], 7: [('ki4', 11, 16), ('ki3', 7, 13)], 8: [('ki4', 15, 16)]},
       fx=nfx('dark pressure pooling at the feet of the crouch',
              [(3, [('dread', [26, 63])]), (4, [('dread', [27, 63])]), (5, [('dread', [26, 63])]), (6, [('dread', [27, 63])]), (7, [('dread', [26, 63])]), (8, [('dread', [27, 63])])]))),
 'genjutsuAfflicted': ('Under Genjutsu', 0,
  'Under Genjutsu (target status, Christopher 2026-10-27: every genjutsu marks its target with an effect showing it is under a genjutsu): the shared looping state the testbed plays on a fighter for as long as any genjutsu holds it, in place of its idle; the guard sags, the hands dropped a little, and the fighter sways slowly on its feet, entranced: the eyes glow the caster\'s element colour, a thin flickering aura in that colour clings to the outline, and three glowing motes circle slowly over the head like a halo, bright passing in front of the head and dark passing behind it; fire version (Aries, Leo, Sagittarius casters: crimson and orange); the testbed recolours it for the other elements.', [
     g(an=band(-15, -105), af=band(-20, -110), bob=(1, 1, 2), lean=(0, 2)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(1, 1, 2), lean=(0, 2)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 3), lean=(0, 0)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 3), lean=(0, 0)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1))],
  ['entranced'] * 8,
  [1] * 8,
  dict(fps=6, auraColors=('#d8321a', '#7a1016'), shapes={'entranced': {'E': [[0, 1, '#d8321a'], [1, 1, '#d8321a'], [0, 2, '#ff8a1c'], [1, 2, '#ff3a1a']], 'S': [[0, 2, '#ff3a1a'], [1, 2, '#ff8a1c'], [5, 2, '#ff8a1c'], [6, 2, '#ff3a1a']]}},
       extra={'loop': True, 'genjutsuMark': {'rule': 'Christopher 2026-10-27: every genjutsu target shows it is under a genjutsu. The testbed plays genjutsuAfflicted on loop in place of the target\'s idle (and draws its halo motes, aura and eye glow over any other state it plays) for as long as a genjutsu holds it; clears when the genjutsu ends', 'element': 'fire', 'recolor': {'rule': 'swap the fire colours for the caster sign\'s element: fire as drawn', 'sagittarius': {'#ffe14d': '#c9a0ff', '#ff8a1c': '#9b45ff', '#d8321a': '#55208f', '#7a1016': '#1c1024', '#ff3a1a': '#9b45ff'}, 'earth': {'#ffe14d': '#d9fff6', '#ff8a1c': '#7fe3d0', '#d8321a': '#c79a5b', '#7a1016': '#8a6236', '#ff3a1a': '#7fe3d0'}, 'water': {'#ffe14d': '#dff6ff', '#ff8a1c': '#7cc8ff', '#d8321a': '#2f7fe0', '#7a1016': '#1b4f99', '#ff3a1a': '#7cc8ff'}, 'air': {'#ffe14d': '#ffffff', '#ff8a1c': '#e3e3e3', '#d8321a': '#b8b8c8', '#7a1016': '#8a8a9a', '#ff3a1a': '#e3e3e3'}}}},
       fx=nfx('the genjutsu mark: three glowing motes circling slowly over the head (one turn per loop), bright in front of the head, dark crimson behind it', _halo(8)))),
 'kingsPosture': ('King\'s Posture', 3,
  'King\'s Posture (Leo taijutsu stance buff: a regal guard, FORT +30% for 3 rounds, holds firm), v4 (Christopher 2026-10-27: see it E facing; v3 turned to the viewer for a front double biceps): the fighter keeps its facing; from the guard it throws both upper arms up level, the near one forward and the far one back, and curls both fists up beside the head in a double biceps flex seen in profile, chest out, teeth clenched, squeezing the flex harder on the peak frame; a golden aura flares round it and a lion\'s mane of flame bursts up behind and round its head, blazing, as it holds the pose; then the mane settles to a proud glow and it drops back into the guard (the testbed keeps the buff, not the mane).', [
     g(),
     g(an=band(-60, -150), af=band(55, 150), bob=(0, 0, 0), lean=(0, 0)),
     g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)), g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)),
     g(an=KP_EN2, af=KP_EF2, bob=(0, -1, 0), lean=(0, -1)),
     g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)), g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-60, -150), af=band(55, 150), bob=(0, 0, 0), lean=(0, 0)),
     g()],
  [None, None, 'strain', 'strain', 'strain', 'strain', 'strain', None, None],
  [0, 0, 1, 3, 2, 2, 2, 1, 0],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'),
       anchored={2: [('mane1', 'head', 0, 0, {'behind': True})], 3: [('mane3', 'head', 0, -1, {'behind': True})], 4: [('mane4', 'head', 0, -1, {'behind': True})],
                 5: [('mane3b', 'head', 0, -1, {'behind': True})], 6: [('mane2', 'head', 0, 0, {'behind': True})], 7: [('mane1', 'head', 0, 0, {'behind': True, 'alpha': {'R': 140, 'O': 170}})]})),
 'sunPalm': ('Sun Palm', 4,
  'Sun Palm (Leo taijutsu strike: channels radiant energy into the palm, scorching whoever it touches, Burn 2 rounds): from the guard the fighter draws the rear hand back low beside the hip, palm open and turned forward, and a small sun kindles in it, white-hot at the heart, swelling and throwing out rays over two held frames while flame swirls up round the arm (v2, Christopher 2026-10-27: more fx); then it steps in and drives the open palm straight out at chest height, and the sun bursts on contact in a white-hot flash and a white-gold starburst with rays flashing out, a fire shock ring blasting out with cracks, then a broken ring of flame, flame licks and scattering embers; it settles back into the guard.', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='medium', rm='E: +2 stepping into the palm, -2 settling back',
       swirl={1: (0, 0.5), 2: (120, 0.8), 3: (240, 1.0)},   # v2: flame swirling round the drawn-back arm as the sun gathers
       impact={4: 0, 5: 1, 6: 2, 7: 3},                      # v2: white-hot flash, fire shock ring, cracks and embers on contact
       anchored={1: [('sunOrb3', 'hand', 0, 0)], 2: [('sunOrb4', 'hand', 0, 0)], 3: [('sunOrb5', 'hand', 0, 0), ('embers', 'hand', 0, -8)],
                 4: [('sunBurst2', 'hand', 3, 0), ('sunOrb4', 'hand', 2, 0)], 5: [('sunBurst3', 'hand', 4, 0), ('sunBurst1', 'hand', 3, 0)],
                 6: [('sunBurst3', 'hand', 6, 0, {'alpha': {'R': 150, 'O': 180}}), ('flame3', 'hand', 4, -4), ('flame2', 'hand', 7, 3), ('embers', 'hand', 2, -7)], 7: [('embers', 'hand', 6, -4), ('flame2', 'hand', 5, -2), ('embers', 'hand', 9, 3)]})),
 'battleRoar': ('Battle Roar', 3,
  'Battle Roar (Leo taijutsu debuff: an intimidating war cry that makes the foe second-guess itself, Slow 2 rounds, STR save DC 12): from the guard the fighter draws in a huge breath, rising, chest swelling, head back and fists pulled down to its sides; then it lunges its chest forward and roars at the foe, mouth wide, both hands flung down and back with fingers spread, and a lion\'s mane of flame bursts up round its head while golden roar waves blast out of its mouth one after another, widening as they go; it holds the roar, the mane blazing, then the mane dies down and it settles back into the guard.', [
     g(),
     g(an=band(10, -40), af=band(5, -40), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(10, -40), af=band(5, -40), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), root=(1, 0), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(-30, -100), af=band(-30, -105), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'roarE', 'roarE', 'roarE', 'roarE', None, None],
  [0, 0, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, hitbox=[44, 10, 16, 18], damage='light', rm='E: +1 lunging into the roar, -1 settling back', auraColors=('#ffe14d', '#ff8a1c'),
       shapes={'roarE': {'E': [[0, 0, '#000000'], [1, 0, '#000000'], [1, 4, '#000000'], [2, 4, '#000000'], [1, 5, '#70241d'], [2, 5, '#70241d']]}},
       anchored={3: [('mane3', 'head', -1, -1, {'behind': True}), ('roar1', 'head', 9, 2)],
                 4: [('mane4', 'head', -1, -1, {'behind': True}), ('roar2', 'head', 12, 2), ('roar1', 'head', 9, 2)],
                 5: [('mane3b', 'head', -1, -1, {'behind': True}), ('roar3', 'head', 17, 2), ('roar2', 'head', 12, 2)],
                 6: [('mane2', 'head', -1, 0, {'behind': True}), ('roar3d', 'head', 22, 2), ('roar2', 'head', 15, 2)],
                 7: [('mane1', 'head', -1, 0, {'behind': True, 'alpha': {'R': 140, 'O': 170}})]})),
 'innerGateAdrenaline': ('Inner Gate: Adrenaline', 4,
  'Inner Gate: Adrenaline (Aries taijutsu buff: AGI and STR up, the fighter burns itself): from the guard the fighter clenches, curls the fists in front of the belly and sinks, straining, eyes squeezed; then the gate bursts open: it stands up tall, chest thrown out and both fists driven down and back, and an orange-red aura flares around the whole body with flame licks rising off the shoulders and head; the aura pulses once, the flames keep licking (the self-burn), then the fighter drops back into the guard still powered up: the aura lingers, the skin stays flushed red and the veins stand out on the arms, neck and temple, embers drifting off it (the testbed keeps that look for as long as the gate stays open: until 0 HP or the player deactivates it).', [
     g(),
     g(an=band(-30, -120), af=band(-35, -125), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-20, -100), af=band(-25, -105), bob=(3, 3, 4), lean=(0, 3), **LOW),
     g(an=band(-20, -100), af=band(-25, -105), bob=(3, 3, 4), lean=(0, 3), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=FLEX_N, af=FLEX_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=FLEX_N, af=FLEX_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-25, 205), af=band(-40, 215), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'pain', 'pain', 'squint', 'squint', 'squint', None, None],
  [0, 0, 0, 1, 3, 2, 3, 2, 2],
  dict(fps=10, auraColors=FIRE_AURA, tint={3: 70, 4: 150, 5: 140, 6: 150, 7: 140, 8: 140}, veins=(4, 5, 6, 7, 8),
       extra={'linger': {'rule': 'Inner Gate: Adrenaline (Christopher 2026-10-27: lingering aura, tinted skin, raised veins): the clip ends still powered up (aura 2 px, red skin tint, veins); while the ability is active (canon A5, Christopher 2026-10-27: a toggle, on until the fighter reaches 0 HP or deactivates it; the self Burn ticks every round meanwhile) the testbed keeps drawing the fighter with a 2 px orange-red aura flickering on its outer ring, the skin tint (fx red #ff3a1a at alpha 140 over skin pixels) and the veins, on every state it plays', 'aura': 2, 'auraColors': ['#ffb12e', '#e0401c'], 'tint': ['#ff3a1a', 140], 'veins': '#7a140c'}}, fx=nfx('red-orange-yellow flame licks rising off the shoulders and head as the gate opens (self-burn), embers drifting after',
              [(4, [('flame2', [31, 8]), ('flame2', [25, 26]), ('flame2', [39, 26])]), (5, [('flame3', [30, 8]), ('flame3', [23, 26]), ('flame2', [40, 25])]),
               (6, [('flame2', [32, 7]), ('flame2', [24, 25]), ('flame3', [38, 26])]), (7, [('embers', [31, 7])]), (8, [('embers', [30, 5])])]))),
 'solarLance': ('Solar Lance', 5,
  'Solar Lance (Leo ninjutsu, ranged: a focused beam of solar fire): from the guard the fighter makes the tiger seal at the chin, a spark of sunlight kindling between the hands; then it draws the near hand back low beside the hip, palm open, and a small sun gathers in it, white-hot and swelling over two held frames; then it steps in and thrusts two fingers straight out at shoulder height, and a lance of solar fire bursts from the fingertips toward the target, a white-hot core inside yellow, orange and a red rim, sparks spitting off its edges, a starburst flaring at the fingers and a backblast of flame off the shoulder, a gold aura flaring round the fighter (v2, Christopher 2026-10-27: more fx: flame swirling round the arm as the sun gathers, a thicker beam, sparks, backblast); the beam holds through a hit-stop, then narrows, flickers and breaks up into embers, and the fighter settles back into the guard (the testbed draws the beam on to the target from the release point).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 4), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 3, 3, 2, 1, 0, 0],
  dict(fps=10, release=[57, 20], rm='E: +2 stepping into the thrust, -2 settling back', auraColors=('#ffe14d', '#ff8a1c'),
       swirl={2: (0, 0.5), 3: (120, 0.8), 4: (240, 1.0)},   # v2 (Christopher 2026-10-27: more fx): flame swirling round the drawn-back arm
       extra={'beam': {'rule': 'Solar Lance is a beam, not a projectile: on frames 5-8 the testbed draws the beam from the release point to the target (white core, yellow, orange, red rim; width 4, 4, 3, 2 px half-height, the last frame broken up), the clip itself draws it to the edge of the cell', 'frames': [5, 6, 7, 8], 'colors': ['#ffffff', '#ffe14d', '#ff8a1c', '#d8321a']}},
       anchored={1: [('sunOrb2', 'hand', 0, -1)], 2: [('sunOrb3', 'hand', 0, 0)], 3: [('sunOrb4', 'hand', 0, 0)], 4: [('sunOrb5', 'hand', 0, 0), ('embers', 'hand', 0, -8)],
                 5: [('sunBurst2', 'hand', 1, 0), ('flame3', 'hand', -27, -2), ('flame2', 'hand', -30, 4)], 6: [('sunBurst1', 'hand', 1, 0), ('flame2', 'hand', -28, -2), ('embers', 'hand', -32, 2)],
                 7: [('sunOrb3', 'hand', 1, 0), ('embers', 'hand', -29, -3)], 8: [('sunOrb2', 'hand', 1, 0)], 9: [('embers', 'hand', 6, -3), ('embers', 'hand', 12, 2)]},
       beam={5: (5, 'fire'), 6: (5, 'fire'), 7: (4, 'fire'), 8: (3, 'fade')})),
 'radiance': ('Radiance', 3,
  'Radiance (Leo ninjutsu stance buff: the fighter focuses its regal aura and it strengthens it as it radiates from the body, STR +10% for 3 rounds), v4 (Christopher 2026-10-27: see it E facing; v3 turned to the viewer, after a power-up reference: fists clenched at the sides, a towering spiky aura erupting from the ground): the fighter keeps its facing; from the guard it makes the seal at the chin, eyes closed; then it sinks into its stance and drives both clenched fists down beside the hips, elbows flared back, straining; a towering aura of golden light erupts from the ground round it, white-hot at the core, pale gold and gold through the body, orange at the tips of tall jagged spikes fanning up and out, a ring of light flaring on the floor at its feet; the aura roars and flickers as it holds the yell, then settles, the fighter rises back into the guard still radiant: a 2 px gold aura and motes of light drifting up off the body (the testbed keeps that look on every state until the buff ends).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, -1), **LOW) for _ in range(6)],
     g(),
     g(), g()],
  [None, 'closed', 'strain', 'roar', 'roar', 'roar', 'strain', 'strain', None, None, None],
  [0, 1, 1, 2, 3, 3, 3, 2, 2, 2, 2],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'),
       extra={'linger': {'rule': 'Radiance (Christopher 2026-10-27: a lingering aura for the duration of the ability): the clip ends still radiant; for the 3 rounds the buff lasts the testbed keeps drawing the fighter with a 2 px gold aura flickering on its outer ring and two or three gold motes drifting up off the shoulders and head, on every state it plays (the erupting aura is only in the cast); clears when the buff ends', 'aura': 2, 'auraColors': ['#ffe14d', '#ff8a1c'], 'motes': {'pattern': 'lightMote', 'colors': ['#ffffff', '#ffe14d', '#ff8a1c'], 'perFrame': 3}}},
       anchored={1: [('sunOrb1', 'hand', 0, -1)], 9: [('lightMote', 'head', -6, 4), ('lightMote', 'head', 7, 10), ('lightMote', 'head', 2, -9)], 10: [('lightMote', 'head', -7, 0), ('lightMote', 'head', 6, 6), ('lightMote', 'head', -2, -11)]},
       flare={'every': True, 2: 0, 3: 2, 4: 3, 5: 3, 6: 3, 7: 2, 8: 1})),
 'supernova': ('Supernova', 6,
  'Supernova (Leo ninjutsu ultimate: the fighter channels its inner light and releases an instant blinding detonation round itself, wide AoE on self, Blind 1 round), the Leo ultimate (longer and more dramatic, like Meteor), v2 (Christopher 2026-10-27: more build-up, the apex lasts longer; 16 frames, the cap, at 8 fps): from the guard the fighter makes the seal and sinks deeper and deeper over five frames, trembling, straining, while motes of light stream in toward it from all round and a gold aura swells; it turns to face the viewer (every facing turns S for the release, as Blast Wave) with the seal pressed to the chest and a star kindling at its heart, swelling and blazing over two frames, the whole body beginning to glow; then it throws its arms out wide and the light detonates: a white flash swallows the fighter and the whole cell and pulses, held over three frames, then a ring of light blasts outward, white, then yellow, orange and red as it widens and breaks up, a second ring behind it and sun rays scattering, embers raining down; the glow drains off the body, it brings the hands back in and turns back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 2), root=(1, 0), **BRACE),
     g(bob=(2, 2, 2), root=(-1, 0), **LOW),
     g(bob=(1, 1, 1), **LOW),
     g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)),
     g(),
     g()],
  [None, 'squint', 'pain', 'pain', 'pain', 'pain', 'strain', 'strain', 'roar', 'roar', 'roar', 'roar', 'roar', 'squint', None, None],
  [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1, 0],
  dict(fps=8, auraColors=('#ffe14d', '#ff8a1c'),
       front={6: dict(R=(-20, 205, 0.8, 'front'), L=(20, -205, 0.8, 'front')), 7: dict(R=(-20, 205, 0.8, 'front'), L=(20, -205, 0.8, 'front')),   # the seal pressed to the chest, facing the viewer
              **{k: dict(R=(110, 105, 1, 'front'), L=(-110, -105, 1, 'front')) for k in (8, 9, 10, 11, 12, 13)},   # arms thrown out wide
              14: dict(R=stances.GA['R'], L=stances.GA['L'])},
       gather={1: 0, 2: 1, 3: 2, 4: 3, 5: 3},
       nova={6: 'core', 7: 'core2', 8: 'flash', 9: 'flash2', 10: 'flash', 11: 0, 12: 1, 13: 2, 14: 4})),
 'leashKick': ('Leash Kick', 10,
  'Leash Kick (Sagittarius taijutsu strike, Physical 12, Live Tier A: the fighter pirouettes violently before throwing out a heel kick at blazing speed): from the guard the fighter tucks both arms tight and whips round in two full pirouettes on the lead foot (the approved spin pivot, twice), a ring of fire whirling round its legs that grows with each turn, black and purple flames flickering in it; v2 (Christopher 2026-10-27: the kick more of an axe kick): coming out of the second turn it swings the rear leg up straight in front, high over its head, torso leaning back, then chops the heel straight down onto the target, a streak of fire following the heel down; flame bursts off the heel as it lands on the target\'s head and shoulder, purple and black licks trailing along the leg, embers scattering at the floor; the leg sets down and it steps back into the guard.', [
     g(),
     g(an=TUCK_SPIN_N, af=TUCK_SPIN_F, bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=TUCK_SPIN_N, af=TUCK_SPIN_F, bob=(1, 1, 1), lean=(0, 0)) for _ in range(6)],
     g(an=band(10, -40), af=band(-60, -80), bob=(1, 1, 1), lean=(0, -1), ln='hk-swing', lf='lk-lead-pivot'),
     g(an=band(30, -20), af=band(-80, -100), bob=(0, 0, 1), lean=(-1, -5), ln='lk-axe-top', lf='lk-lead-pivot'),
     g(an=band(10, -40), af=band(-60, -80), bob=(1, 1, 2), lean=(1, 3), root=(1, 0), ln='lk-axe-chop', lf='lk-lead-pivot'),
     g(an=band(0, -50), af=band(-50, -70), bob=(2, 2, 3), lean=(1, 5), ln='lk-axe-down', lf='lk-lead-pivot'),
     g(bob=(1, 1, 1), lean=(0, 1), root=(-1, 0), ln='hk-drop'),
     g()],
  [None, 'squint'] + ['squint'] * 7 + ['squint', 'squint', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 18, 14, 24], damage='medium', rm='E: +1 chopping down, -1 setting down',
       extra={'borrow': {'rule': copy.deepcopy(HEAVY['borrow']['rule']) + '; Leash Kick spins twice (E -> S, W, N, then S, W, N again)',
                         'frames': {'2': SPIN('S', 0), '3': SPIN('W', 0), '4': SPIN('N', 1), '5': SPIN('S', 0), '6': SPIN('W', 0), '7': SPIN('N', 1)}}},
       spinFire={2: (0, 130, 0), 3: (0, 250, 0), 4: (0, 360, 1), 5: (0, 360, 1), 6: (0, 360, 2), 7: (0, 360, 2), 8: (0, 360, 3)},
       fx=nfx('Sagittarius fire (reds, oranges, yellows with select black and purple flames): flame bursting off the heel on contact, purple and black licks trailing back along the leg',
              [(9, [('pflame1', [41, 22]), ('flame1', [38, 26])]),
               (10, [('flame2', [47, 41]), ('flame1', [46, 34]), ('pflame2', [42, 30]), ('flame1', [40, 25])]),
               (11, [('flame3', [43, 56]), ('pflame2', [48, 54]), ('flame2', [44, 47]), ('pembers', [50, 46]), ('embers', [38, 50])]),
               (12, [('embers', [44, 60]), ('pembers', [49, 58])])]))),
 'spinningTop': ('Spinning Top', 6,
  'Spinning Top (Sagittarius taijutsu strike, Physical 8, Melee, target Chakra -15: the fighter spins on its head while twirling its legs in a wide V fast enough to ignite the air): from the guard the fighter drops into a crouch and dives forward onto its hands and head, kicking its legs up together; turned upside down on its head with both hands braced on the floor beside it, it throws its legs open into a wide V and spins, the V flashing open and closed as it turns (open, edge-on, open from behind, edge-on), the air at its whirling feet catching fire: flames streaming off both feet, a ring of fire whirling round the V at foot height with black and purple licks in it, sparks round its head on the floor; it snaps the legs together, rolls back down into the crouch and rises into the guard.', [
     g(),
     g(an=band(-40, -80), af=band(-30, -70), bob=(2, 2, 3), lean=(1, 4), **LOW),
     g(an=band(-25, -40), af=band(-15, -35), bob=(3, 3, 3), lean=(2, 6), **BRACE),
     g(an=ST_AN, af=ST_AF, bob=(0, 0, 0), lean=(0, 0), **ST_T),
     *[g(an=ST_AN, af=ST_AF, bob=(0, 0, 0), lean=(0, 0), **(ST_V if k % 2 == 0 else ST_N)) for k in range(9)],
     g(an=ST_AN, af=ST_AF, bob=(0, 0, 0), lean=(0, 0), **ST_T),
     g(an=band(-25, -40), af=band(-15, -35), bob=(3, 3, 3), lean=(1, 4), **BRACE),
     g()],
  [None, None, 'squint'] + ['squint'] * 11 + ['squint', None],
  None,
  dict(fps=12, hitbox=[14, 0, 36, 40], damage='light', rm='none (spins in place)',
       invert={3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0, 9: 0, 10: 1, 11: 1, 12: 0, 13: 0},
       topFire={3: 0, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 1, 13: 0})),
 'wispFire': ('Wisp Fire', 4,
  'Wisp Fire (Sagittarius ninjutsu, Elemental 10, Ranged, target Chakra -20: the caster conjures a barrage of small purple flames that sap the chakra from the foe with each hit): from the guard the fighter makes the seal at the chin, a purple spark kindling between the hands; it opens the near hand palm up at the chest and small purple and black flames flicker alight and circle it, a dim purple aura breathing round the fighter; then it pushes the palms out at the target one after the other, near, far, near, far, and with each push a wisp of purple flame with a white-hot head and a black tail flies off toward the target, four in a stream; the last wisp leaves a puff of purple sparks at the palm and the fighter settles back into the guard (the testbed flies the four wisps on to the target from the release point).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -95, fistKind='palm'), af=band(-50, -110), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -95, fistKind='palm'), af=band(-50, -110), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), af=band(-88, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), af=band(-88, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-45, -110), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', None, None, 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, release=[56, 22], rm='E: +1 into the pushes, -1 settling back', auraColors=('#9b45ff', '#55208f'),
       extra={'projectile': {'rule': 'Wisp Fire is a barrage: on frames 4, 5, 6 and 7 the testbed launches one small purple wisp (pwisp, white-hot head, purple body, black tail) from the release point to the target, four in all; each that lands puffs purple sparks and pulls a few chakra-blue motes out of the target (Chakra -20 over the barrage)', 'frames': [4, 5, 6, 7], 'count': 4, 'pattern': 'pwisp', 'colors': ['#ffffff', '#9b45ff', '#55208f', '#1c1024']}},
       anchored={1: [('pspark', 'hand', 0, -2), ('pflame1', 'hand', 0, -6)],
                 2: [('pflame2', 'hand', -1, -5), ('pflame1', 'hand', -6, -1), ('pflame1', 'hand', 5, 1)],
                 3: [('pflame2', 'hand', 4, -5), ('pflame2', 'hand', -5, -2), ('pflame1', 'hand', 2, 3), ('pembers', 'hand', 0, -10)],
                 4: [('pspark', 'hand', 1, 0), ('pwisp', 'feet', 22, -42), ('pflame1', 'feet', 2, -30)],
                 5: [('pspark', 'hand', 1, 0), ('pwisp2', 'feet', 22, -41), ('pwisp', 'feet', 28, -44)],
                 6: [('pspark', 'hand', 1, 0), ('pwisp', 'feet', 22, -42), ('pwisp2', 'feet', 28, -40)],
                 7: [('pspark', 'hand', 1, 0), ('pwisp2', 'feet', 22, -41), ('pwisp', 'feet', 28, -44), ('pembers', 'hand', -3, -5)],
                 8: [('pembers', 'hand', 2, -3)]})),
 'cauterize': ('Cauterize', 4,
  'Cauterize (Sagittarius ninjutsu, self heal 15: the fighter channels its inner fire to seal its own wounds shut): from the guard the fighter makes the seal at the chin, then presses the open near palm flat against its own ribs, the far fist clenched low; it grits its teeth as the palm heats up, then fire flares out from under the hand, orange and yellow with black and purple licks, embers spitting and a warm aura flaring round the body; it holds the burn through the strain, the flame dying to a glow as heat shimmers rise; then it takes the hand away with a breath, a wisp of smoke curling up off the sealed wound and a few warm motes rising, and settles back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(25, -60, fistKind='palm'), af=band(-20, -60), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(25, -60, fistKind='palm'), af=band(-15, -50), bob=(2, 2, 2), lean=(0, 2)),
     g(an=band(25, -60, fistKind='palm'), af=band(-15, -50), bob=(2, 2, 3), lean=(-1, 3)),
     g(an=band(25, -60, fistKind='palm'), af=band(-15, -50), bob=(2, 2, 3), lean=(-1, 3)),
     g(an=band(25, -60, fistKind='palm'), af=band(-20, -60), bob=(2, 2, 2), lean=(0, 2)),
     g(an=band(-5, -70, fistKind='palm'), af=band(-25, -70), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-35, -100), af=band(-30, -95), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'squint', None, None, None],
  [0, 0, 0, 1, 2, 2, 1, 0, 0, 0],
  dict(fps=8, auraColors=FIRE_AURA,
       anchored={2: [('heat', 'hand', 0, -4)],
                 3: [('flame1', 'hand', 0, -3), ('embers', 'hand', 2, -7)],
                 4: [('flame3', 'hand', 0, -4), ('pflame1', 'hand', -3, -2), ('embers', 'hand', 4, -9), ('pembers', 'hand', -4, -10)],
                 5: [('flame2', 'hand', 1, -3), ('pflame2', 'hand', -3, -4), ('embers', 'hand', 3, -10)],
                 6: [('flame1', 'hand', 0, -2), ('heat', 'hand', 0, -6), ('heat', 'hand', -2, -11), ('pembers', 'hand', 3, -9)],
                 7: [('smoke1', 'hand', 0, -4), ('heat', 'hand', 1, -9), ('lightMote', 'head', -6, 6), ('lightMote', 'head', 7, 10)],
                 8: [('smoke2', 'hand', 0, -8), ('lightMote', 'head', -7, 0), ('lightMote', 'head', 6, 3)]})),
 'dogma': ('Dogma', 4,
  'Dogma (Sagittarius genjutsu, debuff: the caster projects its own beliefs into the foe\'s mind on a constant loop until it cannot tell its own thoughts from the caster\'s; Confusion 2 rounds, INT save DC 13; range Zone of Awareness): from the guard the fighter lifts two fingers to its temple, eyes narrowing, and its own conviction starts to loop: purple motes circling over its head on a dotted ring, the eyes kindling purple then flaring white-hot; then it thrusts the two fingers out at the target, and purple waves of belief roll out from the eyes one after another, white at the core, purple and black at the rim, each one wider, the loop over its head still turning; the motes and the glow fade and the hand drops back into the guard (the target takes the genjutsu mark, genjutsuAfflicted in Sagittarius colours, for the Confusion).', [
     g(),
     g(an=band(-115, -195, fistKind='point'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     *[g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(5)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#9b45ff', '#1c1024'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (Sagittarius colours, genjutsuMark.recolor.sagittarius) and keeps it until the Confusion ends', 'state': 'genjutsuAfflicted', 'element': 'sagittarius'}},
       anchored={1: _loop(0)[:4],
                 2: _loop(1) + [('eyeP', 'eye', 0, 0)],
                 3: _loop(2) + [('eyePF', 'eye', 0, 0)],
                 4: _loop(3) + [('eyePF', 'eye', 0, 0), ('dog1', 'eye', 6, 0)],
                 5: _loop(4) + [('eyePF', 'eye', 0, 0), ('dog2', 'eye', 10, 1), ('dog1', 'eye', 6, 0)],
                 6: _loop(5) + [('eyePF', 'eye', 0, 0), ('dog3', 'eye', 15, 2), ('dog2', 'eye', 10, 1), ('dog1', 'eye', 6, 0)],
                 7: _loop(6) + [('eyeP', 'eye', 0, 0), ('dog3d', 'eye', 20, 3), ('dog3', 'eye', 15, 2), ('dog2', 'eye', 10, 1)],
                 8: [it for it in _loop(7) if it[0] != 'dotP'] + [('dog3d', 'eye', 21, 3)],
                 9: [it for it in _loop(0) if it[0] == 'moteP']})),
 'soulPressure': ('Soul Pressure', 4,
  'Soul Pressure (Sagittarius genjutsu, debuff: the caster blankets the foe\'s mind with its spiritual energy, silencing its innermost thoughts; Silence 3 rounds, STR save DC 12; range Zone of Awareness): from the guard the fighter lowers its hands and closes its eyes, gathering itself, and a heavy aura of dark purple and black spirit-flame rises round it, wisps curling up off the shoulders; its eyes snap open, burning purple, and it extends the open near palm toward the target and presses it slowly down, the far hand low at its side, as heavy dome-shaped waves of spirit pressure roll out toward the target, bearing down and sinking as they travel, purple at the crown and black at the rim; it holds the press, then the aura settles and it returns to the guard (the target takes the genjutsu mark, genjutsuAfflicted in Sagittarius colours, for the Silence).', [
     g(),
     g(an=band(-20, -50), af=band(-10, -40), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-10, -30), af=band(-5, -25), bob=(2, 2, 2), lean=(0, 0)),
     g(an=band(-90, -100, fistKind='palm'), af=band(-5, -25), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-75, -65, fistKind='palm'), af=band(-5, -25), bob=(1, 1, 2), lean=(1, 2)),
     g(an=band(-65, -55, fistKind='palm'), af=band(-5, -25), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-65, -55, fistKind='palm'), af=band(-5, -25), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-65, -55, fistKind='palm'), af=band(-5, -25), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-40, -110), af=band(-25, -90), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, 'closed', 'closed', None, 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 2, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#55208f', '#1c1024'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (Sagittarius colours, genjutsuMark.recolor.sagittarius) and keeps it until the Silence ends', 'state': 'genjutsuAfflicted', 'element': 'sagittarius'}},
       anchored={1: [('spWisp', 'head', -6, 12)],
                 2: [('spWisp', 'head', -7, 10), ('spWisp', 'head', 6, 12), ('pflame1', 'head', -1, -9)],
                 3: [('eyePF', 'eye', 0, 0), ('pflame2', 'head', -1, -10), ('spWisp', 'head', -8, 8), ('spWisp', 'head', 7, 10)],
                 4: [('eyePF', 'eye', 0, 0), ('pflame2', 'head', 0, -10), ('sp1', 'feet', 14, -30), ('spWisp', 'head', -7, 6)],
                 5: [('eyePF', 'eye', 0, 0), ('pflame1', 'head', 0, -9), ('sp2', 'feet', 19, -24), ('sp1', 'feet', 14, -30), ('spWisp', 'head', 7, 8)],
                 6: [('eyePF', 'eye', 0, 0), ('pflame2', 'head', 0, -10), ('sp3', 'feet', 24, -17), ('sp2', 'feet', 19, -24), ('spWisp', 'head', -7, 5)],
                 7: [('eyeP', 'eye', 0, 0), ('sp3d', 'feet', 27, -10), ('spWisp', 'head', 6, 4)],
                 8: [('spWisp', 'head', -6, 2, {'alpha': {'K': 140, 'p': 140, 'P': 160}})]})),
 'mountainStance': ('Mountain Stance', 3,
  'Mountain Stance (Taurus taijutsu stance buff, FORT +30% 3 rounds: the fighter stamps its feet into the ground, demonstrating its unshakeable resolve): from the guard the fighter drops its hands and lifts the lead knee high, then stamps the foot down hard into the floor (sumo shiko), cracks splitting out from the heel, dust and stones jumping; it shifts onto that leg, lifts the rear knee and stamps again; then it sinks into a deep, wide stance with the fists pulled back to the hips, elbows back, and an earthen aura settles round it, brown with flecks of crystal glinting in it and small teal crystal shards pushing up out of the cracks; it holds, rooted, then rises back into the guard.', [
     g(),
     g(an=band(15, -40), af=band(5, -35), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -80), af=band(40, -20), bob=(0, 0, 0), lean=(0, -1), lf='ms-lift-lead'),
     g(an=band(20, -30), af=band(10, -30), bob=(3, 3, 3), lean=(1, 2), ln='ms-wide-rear', lf='ms-wide-lead'),
     g(an=band(40, -20), af=band(-30, -80), bob=(1, 1, 1), lean=(0, 1), ln='ms-lift-rear', lf='ms-wide-lead'),
     g(an=band(20, -30), af=band(10, -30), bob=(3, 3, 3), lean=(1, 2), ln='ms-wide-rear', lf='ms-wide-lead'),
     *[g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), ln='ms-wide-rear', lf='ms-wide-lead') for _ in range(4)],
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, None, 'squint', 'strain', 'squint', 'strain', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'),
       anchored={3: [('crack1', 'feet', 9, -1), ('dust2', 'feet', 6, -3), ('rocks', 'feet', 10, -8)],
                 4: [('crack1', 'feet', 9, -1), ('dust1', 'feet', 7, -5), ('rocks', 'feet', 12, -12)],
                 5: [('crack2', 'feet', 0, -1), ('dust2', 'feet', -6, -3), ('dust1', 'feet', 7, -6), ('rocks', 'feet', -10, -9)],
                 6: [('crack2', 'feet', 0, -1), ('crystT', 'feet', -9, -3), ('crystT', 'feet', 10, -3), ('dust1', 'feet', -7, -6), ('cryst', 'head', -9, 14)],
                 7: [('crack2', 'feet', 0, -1), ('crystT', 'feet', -9, -3), ('crystT', 'feet', 10, -3), ('cryst', 'feet', 13, -5), ('cryst', 'head', 9, 8)],
                 8: [('crack2', 'feet', 0, -1), ('crystT', 'feet', -9, -3), ('crystT', 'feet', 10, -3), ('cryst', 'feet', -13, -5), ('cryst', 'head', -8, 4)],
                 9: [('crack2', 'feet', 0, -1, {'alpha': {'E': 160, 'K': 160}}), ('crystT', 'feet', 10, -3, {'alpha': {'c': 150, 'C': 150}}), ('cryst', 'head', 9, 2)],
                 10: [('crack1', 'feet', 0, -1, {'alpha': {'E': 110, 'K': 110}})]})),
 'ironFist': ('Iron Fist', 5,
  'Iron Fist (Taurus taijutsu strike, Physical 16, can Slow 1 round: the fighter focuses its iron will into its fist before punching): from the guard the fighter sits its weight back and draws the rear fist back beside the ear, elbow high, the lead hand out to measure; crystal and earth swirl round the cocked arm, a ring of soil-brown grit with teal crystal at its head winding tighter over three held frames, crystal glints sparking on the knuckles; then it steps in and drives the fist dead straight through the target, rear heel turning up; on contact a crystal-white flash bursts at the fist, a shock ring of teal and brown blasts out, cracks shoot off, stone chips and crystal shards scatter and dust puffs; then it pulls back into the guard.', [
     g(),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(0, 0), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 on the step into the punch, -1 settling back',
       swirl={1: (0, 0.35), 2: (100, 0.6), 3: (210, 0.85), 4: (320, 1.0)},
       impact={5: 0, 6: 1, 7: 2, 8: 3}, recolor=EARTH_RECOLOR, keepFx=True,
       anchored={3: [('cryst', 'hand', 0, 0)], 4: [('cryst', 'hand', 1, -1), ('crystT', 'hand', -3, 2)],
                 6: [('dust1', 'hand', -2, 6), ('rocks', 'hand', 6, -6)], 7: [('dust2', 'hand', 2, 7), ('rocks', 'hand', 9, 4)]})),
 'bullRush': ('Bull Rush', 11,
  'Bull Rush (Taurus taijutsu gap closer, Physical 14, Melee (Reach +4m), Priority, movement credit +6: the fighter adopts a sprinter\'s stance before charging with reckless abandon into its opponent): from the guard the fighter drops into a low sprinter\'s set, knees deep, body pitched forward, arms hanging low, and paws the ground with the rear foot, grit spitting back; then it bursts into the approved sprint head down, both arms reaching forward ahead of it (v2, Christopher 2026-10-28: arms forward, not swept back), dust and stones exploding off the floor at every stride and a cloud of dust boiling up behind it, the motion streak in dust browns; on the last stride it tucks both arms tight, drops its head and rams the lead shoulder through the target like a bull, a burst of rock chips and dust and a few teal crystal shards at the point of impact; then it straightens back into the guard. The fighter travels 40 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=band(-20, -30), af=band(-25, -35), bob=(4, 4, 4), lean=(2, 9), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=band(-20, -30), af=band(-25, -35), bob=(4, 4, 4), lean=(2, 10), ln='ml-dip-rear', lf='ml-dip-lead')] + [
     g(an=band(-70 + 6 * (k % 2), -80 + 6 * (k % 2)), af=band(-76 + 6 * ((k + 1) % 2), -86 + 6 * ((k + 1) % 2)), bob=(SPRINT_DY[k] + 1,) * 3, lean=(1, 10), root=(6, 0), ln='sr-' + SPRINT_LEGS[k], lf='sr-' + SPRINT_LEGS[(k + 4) % 8]) for k in range(6)] + [   # v2 (Christopher 2026-10-28): arms reaching forward through the sprint, not swept back
     g(an=TUCK_N, af=TUCK_F, bob=(3, 3, 3), lean=(2, 9), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 8), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3)),
     g()],
  [None, 'squint', 'strain', 'strain'] + ['strain'] * 6 + ['strain', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='medium', rm='E: 6 px a stride through the sprint, +3 and +1 into the ram; 40 px in all (travel)',
       blur={k: 9 for k in range(4, 10)} | {10: 7, 11: 4}, trail=DUST_TRAIL,
       fx=nfx('earth (soil browns with teal crystal): grit pawed back, dust and stones bursting off the floor at every stride, a cloud of dust behind, rock chips and crystal shards where the shoulder lands',
              [(3, [('dust1', [14, 63]), ('rocks', [9, 59])])] + [(k, _dustkick(SPRINT_LEGS[k - 4], k) + _dustkick(SPRINT_LEGS[(k + 0) % 8], k + 1) + DUST_WAKE[k % 2]) for k in range(4, 10)] +
              [(10, [('rocks', [48, 30]), ('dust2', [44, 36]), ('cryst', [50, 25]), ('dust1', [38, 63])] + DUST_WAKE[0][:2]), (11, [('rocks', [50, 27]), ('crystT', [47, 22]), ('dust1', [46, 34])]), (12, [('dust1', [46, 63])])]),
       extra={'travel': {'rule': 'Bull Rush is a gap closer: the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}})),
 'oakFlesh': ('Oak Flesh', 4,
  'Oak Flesh (Taurus ninjutsu self buff, FORT +50% 3 rounds: the fighter steadies itself and focuses its will to harden its skin): from the guard the fighter makes the seal at the chin and sinks a little into its knees, eyes closing, an earthen aura rising round it; then it drives its fists down beside its hips, elbows back, and its skin hardens into oak (v2, Christopher 2026-10-28: the bark more opaque, about 88%): a warm honey-gold oak spreads over all its skin, streaked with dark walnut grain (face included) and patched with moss, its hair turning to moss, and dark wood grain stands out down the arms and neck, wood chips and dust shaken off it and teal crystal glints flashing on the hardened skin; it holds, unmoving, then rises back into the guard still clad in bark (the spec asks the testbed to keep the bark tint and grain while the buff lasts).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 3), lean=(0, 0), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'closed', 'closed', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'), tint={3: 80, 4: 160, 5: 225, 6: 225, 7: 225, 8: 225, 9: 225}, veins=(4, 5, 6, 7, 8, 9), tintColors=((0xd8, 0xa2, 0x48), (0x1e, 0x10, 0x08), (0x4a, 0x2c, 0x18), (0x7d, 0x86, 0x3c)), hairTo={'frames': [4, 5, 6, 7, 8, 9], 'map': {'#3f0505': '#2f3812', '#702219': '#55602a', '#70241d': '#55602a', '#9e4a31': '#7d863c'}},
       extra={'linger': {'rule': 'Oak Flesh (FORT +50% 3 rounds): the clip ends with the skin hardened into oak; while the buff lasts the testbed keeps drawing the fighter with the bark tint (honey oak #d8a248 at alpha 225 over skin pixels, with dark walnut grain streaks #4a2c18 (over the face too) and patches of moss #7d863c off the face, the hair turned to moss (hair ramp #3f0505/#702219/#70241d/#9e4a31 -> #2f3812/#55602a/#55602a/#7d863c), deep grain #1e1008; v2 more opaque, v3 grain streaks so it reads on the darkest skin tone, v4 honey oak instead of the v3 grey, which read as zombie skin, v5 honey oak + walnut grain + moss combined, v6 grain on the face and moss hair; Christopher 2026-10-28) and the deep wood grain (#1e1008), on every state it plays; clears when the buff ends', 'tint': ['#d8a248', 225], 'veins': '#1e1008', 'streak': ['#4a2c18', '(x + floor(y / 3)) % 3 == 0, skin pixels off the face'], 'hair': {'#3f0505': '#2f3812', '#702219': '#55602a', '#70241d': '#55602a', '#9e4a31': '#7d863c'}, 'moss': ['#7d863c', '(floor(x / 2) * 5 + floor(y / 2) * 11) % 7 == 0, skin pixels off the face']}},
       anchored={4: [('rocks', 'head', -8, 20), ('dust1', 'feet', -6, -2), ('dust1', 'feet', 7, -2)],
                 5: [('cryst', 'head', 6, 16), ('rocks', 'head', 8, 26), ('crystT', 'head', -7, 22)],
                 6: [('cryst', 'head', -6, 24), ('crystT', 'head', 7, 12)],
                 7: [('cryst', 'head', 5, 28)]})),
 'ironwoodKanabo': ('Ironwood Kanabo', 6,
  'Ironwood Kanabo (Taurus ninjutsu, STR +20% 3 rounds, unlocks the Kanabo weapon style kit: the fighter materialises its iron will into a towering studded club), v2 (Christopher 2026-10-28: the club rises from the earth; redesigned after his reference): from the guard the fighter makes the seal at the chin, then sweeps both palms down low, facing the floor, and the ground in front of it cracks, dust and stones jumping; it draws its palms up and the club rises out of the crack head first: a long dark iron kanabo with rows of spikes down both sides and studs between them, a rounded cap, a tapered cone neck, a cord-wrapped grip and an iron ring at the pommel; as the grip clears the floor the fighter closes its near fist round it and lifts it free, dust and stone shaking off; then it returns to the guard (a kanabo weapon layer and Kanabo stance idle are the next step for holding it).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -45, fistKind='palm'), af=band(-35, -50, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-30, -45, fistKind='palm'), af=band(-35, -50, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-45, -80, fistKind='palm'), af=band(-50, -85, fistKind='palm'), bob=(2, 2, 2), lean=(1, 2), **LOW),
     g(an=band(-60, -110, fistKind='palm'), af=band(-65, -115, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-55, -70), af=band(-40, -100), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-55, -70), af=band(-40, -100), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-40, -110), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', None, None, None, None],
  [0, 0, 1, 1, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'),
       extra={'weapon': {'rule': 'Ironwood Kanabo summons the Kanabo (Taurus): the cast draws the club as fx (rising from the floor, then in the near fist); holding it afterwards needs a kanabo weapon layer and a Kanabo stance idle (to author once the cast is approved)', 'item': 'kanabo'}},
       kanaboRise={3: 8, 4: 20, 5: 32, 6: 'grip', 7: 'grip'},
       anchored={2: [('crack1', 'feet', 13, -1), ('dust1', 'feet', 13, -3), ('rocks', 'feet', 17, -8)],
                 3: [('crack2', 'feet', 13, -1), ('dust2', 'feet', 13, -3), ('rocks', 'feet', 9, -10), ('rocks', 'feet', 18, -14)],
                 4: [('crack2', 'feet', 13, -1), ('dust2', 'feet', 13, -2), ('rocks', 'feet', 17, -24)],
                 5: [('crack2', 'feet', 13, -1), ('dust1', 'feet', 13, -2), ('rocks', 'feet', 9, -30)],
                 6: [('crack1', 'feet', 13, -1), ('dust1', 'feet', 13, -2), ('rocks', 'hand', 3, 12)],
                 7: [('crack1', 'feet', 13, -1, {'alpha': {'K': 130, 'E': 130}})]})),
 'rootSanctuary': ('Root Sanctuary', 5,
  'Root Sanctuary (Taurus ninjutsu self buff, FORT +20% 2 rounds: the fighter forms a rooted earthen sanctuary around itself, reinforcing its body), v2 (Christopher 2026-10-28: more root hairs on the rising roots): from the guard the fighter makes the seal at the chin and sinks into its knees, eyes closing, an earthen aura rising round it; then it drives both fists down beside its hips and the floor cracks open either side of it: two gnarled roots burst up out of the cracks, rootlets kicking out sideways and runners spreading along the floor, and climb either side of the fighter, arching inward over its head until they meet in a dome, teal crystal budding along them as they close; it holds inside the sanctuary, unmoving, crystal glinting, then the roots sink back into the floor and it rises back into the guard (the spec proposes a faint ring of roots at the feet while the buff lasts).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     *[g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW) for _ in range(7)],
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'),
       extra={'linger': {'rule': 'Root Sanctuary (FORT +20% 2 rounds), proposal: while the buff lasts the testbed draws a faint ring of roots on the floor round the fighter (the crack2 floor pattern in soil browns, alpha 150, behind the fighter); clears when the buff ends', 'pattern': 'crack2', 'alpha': 150}},
       anchored={3: [('crack2', 'feet', 0, -1), ('sanct20', 'feet', 0, SANCT_DY, {'behind': True}), ('dust1', 'feet', -14, -3), ('dust1', 'feet', 14, -3), ('rocks', 'feet', 16, -8)],
                 4: [('crack2', 'feet', 0, -1), ('sanct45', 'feet', 0, SANCT_DY, {'behind': True}), ('dust2', 'feet', 14, -3), ('rocks', 'feet', -17, -10)],
                 5: [('crack2', 'feet', 0, -1), ('sanct70', 'feet', 0, SANCT_DY, {'behind': True}), ('dust1', 'feet', -15, -4)],
                 6: [('crack2', 'feet', 0, -1), ('sanct90', 'feet', 0, SANCT_DY, {'behind': True}), ('cryst', 'feet', 12, -24)],
                 7: [('crack2', 'feet', 0, -1), ('sanct100', 'feet', 0, SANCT_DY, {'behind': True}), ('glint', 'head', 0, -10), ('cryst', 'feet', -13, -30)],
                 8: [('crack2', 'feet', 0, -1), ('sanct100', 'feet', 0, SANCT_DY, {'behind': True}), ('cryst', 'feet', 13, -18), ('glit', 'head', -9, -4)],
                 9: [('crack2', 'feet', 0, -1, {'alpha': {'E': 170, 'K': 170}}), ('sanct70', 'feet', 0, SANCT_DY, {'behind': True, 'alpha': {'E': 170, 'e': 170, 'K': 170}}), ('dust1', 'feet', 14, -3)],
                 10: [('crack1', 'feet', 0, -1, {'alpha': {'E': 120, 'K': 120}}), ('sanct20', 'feet', 0, SANCT_DY, {'behind': True, 'alpha': {'E': 110, 'e': 110, 'K': 110}})]})),
 'materialFixation': ('Material Fixation', 4,
  'Material Fixation (Taurus genjutsu, mental debuff: the caster forces an obsession on the foe, so it drops everything and loses focus on the fight; Disarm 3 rounds, INT save DC 12; range ~12 m): from the guard the fighter opens the near hand palm up in front of its chest, the far hand low, and an illusory crystal gem forms out of a glint in the palm, growing and faceting, teal with a white highlight and sparkling; its eyes kindle crystal teal; it lifts the palm and offers the gem out toward the target, and the gem\'s image drifts off the palm toward the foe trailing glitter while waves of crystal-teal fascination roll out from the eyes, each one wider; the gem fades out of sight near the target, the glow dies and the hand drops back into the guard (the target takes the genjutsu mark, genjutsuAfflicted in earth colours, for the Disarm).', [
     g(),
     g(an=band(-40, -100, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-40, -100, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-55, -95, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=band(-80, -90, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(1, 3)) for _ in range(4)],
     g(an=band(-50, -110), af=band(-25, -90), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (earth colours, genjutsuMark.recolor.earth) and keeps it until the Disarm ends', 'state': 'genjutsuAfflicted', 'element': 'earth'}},
       anchored={1: [('gem1', 'hand', 1, -4)],
                 2: [('gem2', 'hand', 1, -5), ('glit', 'hand', -3, -9), ('eyeC', 'eye', 0, 0)],
                 3: [('gem3', 'hand', 1, -6), ('glint', 'hand', 4, -11), ('eyeCF', 'eye', 0, 0)],
                 4: [('gem3', 'hand', 5, -5), ('glit', 'hand', 0, -4), ('eyeCF', 'eye', 0, 0), ('fix1', 'eye', 6, 0)],
                 5: [('gem2', 'hand', 11, -4), ('glit', 'hand', 5, -3), ('glit', 'hand', 0, -6, {'alpha': {'c': 150, 'W': 170}}), ('eyeCF', 'eye', 0, 0), ('fix2', 'eye', 10, 1), ('fix1', 'eye', 6, 0)],
                 6: [('gem2', 'hand', 17, -3, {'alpha': {'c': 190, 'C': 190, 'T': 190, 'W': 210}}), ('glit', 'hand', 11, -2), ('eyeCF', 'eye', 0, 0), ('fix3', 'eye', 15, 2), ('fix2', 'eye', 10, 1), ('fix1', 'eye', 6, 0)],
                 7: [('gem1', 'hand', 22, -2, {'alpha': {'c': 140, 'C': 140, 'T': 140}}), ('glit', 'hand', 17, -1, {'alpha': {'c': 140, 'W': 150}}), ('eyeC', 'eye', 0, 0), ('fix3d', 'eye', 20, 3), ('fix3', 'eye', 15, 2)],
                 8: [('fix3d', 'eye', 21, 3, {'alpha': {'C': 140, 'T': 140}})]})),
 'planetaryPressure': ('Planetary Pressure', 4,
  'Planetary Pressure (Taurus genjutsu, mental debuff: the caster exerts its will on the foe\'s mind so it perceives gravity as twice as strong; Slow 2 rounds, STR save DC 13; range ~12 m): from the guard the fighter raises the near hand high, palm up, and an illusory planet forms just in front of it, soil brown with a ring of teal crystal, swelling over two frames while the eyes kindle crystal teal; then it closes the hand into a fist and drags it down hard in front of itself, sinking into its knees as if hauling the weight down, and the planet collapses into heavy dome-shaped waves of gravity that roll out toward the target, bearing down and sinking as they travel, with dashes of gravity falling over the target; it holds the pull, then rises back into the guard (the target takes the genjutsu mark, genjutsuAfflicted in earth colours, for the Slow).', [
     g(),
     g(an=band(-110, -150, fistKind='palm'), af=band(-20, -70), bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-120, -150, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-120, -150, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-90, -60), af=band(-5, -40), bob=(2, 2, 2), lean=(1, 3), **LOW),
     *[g(an=band(-60, -40), af=band(-5, -40), bob=(3, 3, 3), lean=(1, 4), **LOW) for _ in range(3)],
     g(an=band(-40, -110), af=band(-25, -90), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, None, 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (earth colours, genjutsuMark.recolor.earth) and keeps it until the Slow ends', 'state': 'genjutsuAfflicted', 'element': 'earth'}},
       anchored={1: [('planet1', 'hand', 4, 1)],
                 2: [('planet2', 'hand', 6, 2), ('eyeC', 'eye', 0, 0)],
                 3: [('planet3', 'hand', 7, 3), ('glit', 'hand', 12, -2), ('eyeCF', 'eye', 0, 0)],
                 4: [('planet2', 'hand', 2, 0, {'alpha': {'e': 170, 'E': 170, 'K': 170, 'C': 190, 'c': 190}}), ('eyeCF', 'eye', 0, 0), ('gp1', 'feet', 14, -30)],
                 5: [('eyeCF', 'eye', 0, 0), ('gp2', 'feet', 19, -24), ('gp1', 'feet', 14, -30), ('gline', 'feet', 22, -38), ('gline', 'feet', 28, -34)],
                 6: [('eyeCF', 'eye', 0, 0), ('gp3', 'feet', 24, -17), ('gp2', 'feet', 19, -24), ('gline', 'feet', 22, -32), ('gline', 'feet', 28, -28), ('gline', 'feet', 25, -40)],
                 7: [('eyeC', 'eye', 0, 0), ('gp3d', 'feet', 27, -10), ('gline', 'feet', 25, -34), ('gline', 'feet', 29, -22)],
                 8: [('gline', 'feet', 27, -28, {'alpha': {'e': 120, 'E': 120, 'K': 120}})]})),
 'silicaStrike': ('Silica Strike', 5,
  'Silica Strike (Virgo taijutsu, Physical 8, Blind 3 rounds INT save DC 12: the fighter grabs a fistful of sand before striking at its opponent\'s face), v2 (Christopher 2026-10-28: the caster really bends down, almost taking a knee, then rises into an uppercut with the sand fx; v4 19:25: the uppercut rises from the crouched position; v5 19:28: more fx): from the guard the fighter drops down onto the rear knee, the lead foot planted flat in front, and sweeps the near hand along the floor, scooping, sand puffing up round the fingers; it closes the fist on a handful and draws it back low beside the hip, sand trickling; then, still kneeling, it starts the uppercut from the hip and rises out of the crouch with it, legs straightening as the fist rips up and out at the opponent\'s chin, arm reaching well out in front, the sand bursting up off the fist into the face, a burst of sand hanging there in a drifting cloud; it settles back into the guard.', [
     g(),
     g(an=band(-20, -25, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 6), **BRACE),   # dropping toward the floor
     g(an=band(-25, -40, fistKind='palm'), af=band(-20, -150), bob=(9, 10, 10), lean=(1, 8), ln='ss-kneel-rear', lf='ss-kneel-lead'),   # on the rear knee, palm sweeping the floor
     g(an=band(-5, -30), af=band(-20, -150), bob=(9, 10, 10), lean=(1, 7), ln='ss-kneel-rear', lf='ss-kneel-lead'),                    # fist closed on a handful
     g(an=band(25, -20), af=band(-40, -130), bob=(9, 10, 10), lean=(1, 4), ln='ss-kneel-rear', lf='ss-kneel-lead'),                    # fist drawn back low by the hip, coiled
     g(an=band(-35, -120), af=band(-30, -120), bob=(8, 9, 9), lean=(1, 4), ln='ss-kneel-rear', lf='ss-kneel-lead'),                    # v4: the uppercut starts from the kneel, fist swinging up from the hip
     g(an=band(-55, -130), af=band(-20, -100), bob=(4, 5, 5), lean=(1, 3), root=(1, 0), **LOW),                                          # rising out of the crouch with the fist, legs driving up
     g(an=band(-112, -128), bob=(0, -1, 0), lean=(1, 2), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),   # at the top of the uppercut, arm reaching up and out, the sand bursting off the fist into the face
     g(an=band(-112, -128), bob=(0, -1, 0), lean=(1, 2), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 2), root=(-2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'roar', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 14, 14, 10], damage='light', rm='E: +1 rising, +3 stepping into the uppercut, -4 settling back',
       anchored={2: [('sandPuff', 'hand', 2, 1), ('sandPuff', 'feet', 14, -1)], 3: [('sandPuff', 'hand', 1, 0), ('sandH', 'hand', 0, -1), ('grains', 'feet', 13, -4)],
                 4: [('sandH', 'hand', 0, -1), ('sandTrk', 'hand', 0, 5), ('grains', 'hand', 3, 3)],
                 5: [('sandH', 'hand', 0, -1), ('sandTrk', 'hand', -1, 5), ('grains', 'hand', -4, 6), ('sandPuff', 'feet', 12, -1), ('grains', 'feet', 9, -6)],
                 6: [('sandH', 'hand', 0, -1), ('sandSprayUp', 'hand', 0, -4), ('sandTrk', 'hand', -1, 7), ('grains', 'hand', -5, 9), ('sandPuff', 'feet', 13, -1)],
                 7: [('sandSprayUp', 'hand', 1, -3), ('sandBurst', 'hand', 5, -2, {'alpha': {'S': 215, 's': 205, 'Z': 225}}), ('sandSpray', 'hand', 7, 1), ('grains', 'hand', -3, 6), ('grains', 'hand', 6, 4)],
                 8: [('sandBurstL', 'hand', 5, -3, {'alpha': {'S': 235, 's': 225, 'Z': 240}}), ('sandCloud', 'hand', 7, -2, {'alpha': {'S': 190, 's': 180, 'Z': 200}}), ('grains', 'hand', -4, 7)],
                 9: [('sandCloudL', 'head', 12, -1, {'alpha': {'S': 175, 's': 165, 'Z': 185}}), ('grains', 'head', 6, 12), ('grains', 'head', 16, 10)],
                 10: [('sandCloudL2', 'head', 13, 0, {'alpha': {'S': 120, 's': 110, 'Z': 130}}), ('grains', 'head', 10, 14)]})),
 'flowingSandParry': ('Flowing Sand Parry', 6,
  'Flowing Sand Parry (Virgo taijutsu stance, counter, AGI +20% 1 round: the fighter loosens its muscles and begins to flow like sand in an hourglass while time seems to slow and its senses heighten), v2 (Christopher 2026-10-28: one arm makes a large sweeping circle over the head, the other the same down near the knees, like swinging them in converging circles): from the guard the fighter lets its arms hang loose, eyes closing, sand trickling from its fingertips; then the near arm swings up in front and round in a wide circle over its head and down behind, while the fighter sinking deep on bent knees so the far arm swings the opposite way in a low circle down by the knees, both open hands trailing streams of sand along their paths; an illusory hourglass forms beside its head and grains hang still in the air as time slows; the two circles converge in front of it, the high hand coming down and the low hand coming up until the open palms meet before the chest in the parry, eyes snapping open crystal teal, the sand trails closing into a ring; the hourglass turns, the grains fall, and it settles back into the guard (the testbed keeps the stance for the counter).', [
     g(),
     g(an=band(-10, -30, fistKind='palm'), af=band(10, -20, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-80, -95, fistKind='palm'), af=band(45, 40, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-135, -150, fistKind='palm'), af=band(15, 10, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-175, -180, fistKind='palm'), af=band(-20, -20, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(150, 150, fistKind='palm'), af=band(-50, -45, fistKind='palm'), bob=(4, 5, 5), lean=(0, 2), **BRACE),
     g(an=band(110, 105, fistKind='palm'), af=band(-30, -25, fistKind='palm'), bob=(4, 5, 5), lean=(0, 2), **BRACE),
     g(an=band(60, 50, fistKind='palm'), af=band(5, 5, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-20, -40, fistKind='palm'), af=band(35, 35, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-75, -120, fistKind='palm'), af=band(-20, -45, fistKind='palm'), bob=(3, 4, 4), lean=(0, 0), **LOW),
     g(an=band(-60, -125, fistKind='palm'), af=band(-55, -75, fistKind='palm'), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),   # the parry: the circles converge, palms meeting before the chest
     g(an=band(-60, -125, fistKind='palm'), af=band(-55, -75, fistKind='palm'), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-40, -110), af=band(-50, -120), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None, None, None],
  [0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#e6c27a', '#b08d4e'), rm='sways 1 px back and forward (net 0)',
       trails={'near': range(2, 11), 'far': range(2, 11), 'len': 3}, farLayer=True,
       anchored={1: [('sandTrk', 'hand', 0, 3)],
                 3: [('hglass', 'head', -12, -1, {'alpha': {'s': 150, 'S': 160, 'Z': 170}})],
                 **{k: [('hglass', 'head', -12, -1), ('grains', 'head', -9, 6), ('grains', 'head', 10, 16), ('grains', 'feet', -10, -20)] for k in (4, 5, 6)},
                 **{k: [('hglass2', 'head', -12, -1), ('grains', 'head', -9, 6), ('grains', 'head', 10, 16), ('grains', 'feet', -10, -20)] for k in (7, 8, 9)},
                 10: [('hglass2', 'head', -12, -1), ('eyeCF', 'eye', 0, 0), ('grains', 'head', -9, 6), ('grains', 'head', 10, 16), ('grains', 'feet', -10, -20)],
                 11: [('hglass', 'head', -12, -1, {'alpha': {'s': 140, 'S': 140, 'Z': 150}}), ('eyeC', 'eye', 0, 0), ('grains', 'head', -9, 9), ('grains', 'head', 10, 20)],
                 12: [('grains', 'head', -9, 14, {'alpha': {'S': 130, 's': 120, 'Z': 140}}), ('grains', 'feet', 10, -8, {'alpha': {'S': 130, 's': 120, 'Z': 140}})]})),
 'witherPalm': ('Wither Palm', 2,
  'Wither Palm (Virgo taijutsu strike, Physical 12, target Stamina -15: with clinical precision the fighter throws a series of palm strikes at its opponent\'s vital points): from the guard the fighter draws the near open hand back by the hip, then steps in and fires five quick open-palm strikes, alternating hands and changing height, chest, throat, ribs, solar plexus and a last near palm to the chest; each lands with a crystal-teal flash on the vital point struck, a thin teal shock ring snapping out from it and a plume of dull, dry dust as the strength drains out of the foe, the last one a big flash with a double ring and a burst of withered dust that drifts down; v2 (Christopher 2026-10-28: the animation is good, it needs more fx): the open hands glow crystal teal from the draw-back on, trailing a faint teal streak on each strike, and a thin teal aura clings to the fighter through the flurry; it holds a beat, the dust falling, then settles back into the guard.', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),   # chest
     g(an=band(-40, -110), af=band(-100, -96, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),   # throat
     g(an=band(-75, -72, fistKind='palm'), af=band(-40, -120), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),   # ribs
     g(an=band(-40, -110), af=band(-85, -85, fistKind='palm'), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),   # solar plexus
     g(an=band(-92, -92, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(2, 5), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),   # the last, full extension
     g(an=band(-92, -92, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-3, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 1, 1, 2, 2, 1, 0],
  dict(fps=12, auraColors=('#7fe3d0', '#3a9e8f'), hitbox=[44, 18, 14, 14], damage='light', rm='E: +2 stepping into the strikes, +1 on the last, -3 settling back',
       anchored={1: [('palmGlow', 'hand', 0, 0), ('palmGlow', 'farhand', 0, 0, {'alpha': {'C': 150, 'c': 170}})],
                 2: [('palmGlow', 'farhand', 0, 0), ('vital', 'hand', 2, 0), ('vRing', 'hand', 3, 0), ('witherPlume', 'hand', 1, 7), ('streak', 'hand', -6, 0)],
                 3: [('palmGlow', 'hand', 0, 0), ('vital', 'farhand', 2, 0), ('vRing', 'farhand', 3, 0), ('witherPlume', 'farhand', 1, 7), ('wither', 'hand', 0, 6), ('streak', 'farhand', -6, 0)],
                 4: [('palmGlow', 'farhand', 0, 0), ('vital', 'hand', 2, 0), ('vRing', 'hand', 3, 0), ('witherPlume', 'hand', 1, 7), ('wither', 'farhand', 3, 5), ('streak', 'hand', -6, 0)],
                 5: [('palmGlow', 'hand', 0, 0), ('vital', 'farhand', 2, 0), ('vRing', 'farhand', 3, 0), ('witherPlume', 'farhand', 1, 7), ('wither', 'hand', 1, 4), ('streak', 'farhand', -6, 0)],
                 6: [('vital2', 'hand', 3, 0), ('vRing2', 'hand', 3, 0), ('witherBurst', 'hand', 4, 3), ('wither2', 'hand', 2, 6), ('streak', 'hand', -7, 0)],
                 7: [('vital', 'hand', 3, 0, {'alpha': {'c': 150, 'W': 170}}), ('vRing3', 'hand', 3, 0, {'alpha': {'c': 170, 'C': 150}}), ('witherBurst', 'hand', 4, 8, {'alpha': {'u': 200, 'v': 200}}), ('wither2', 'hand', 2, 9), ('wither', 'hand', -2, 13)],
                 8: [('witherPlume', 'hand', 3, 13, {'alpha': {'u': 150, 'v': 150}}), ('wither', 'hand', 2, 17, {'alpha': {'u': 130, 'v': 130}}), ('wither', 'hand', 6, 19, {'alpha': {'u': 110, 'v': 110}})]})),
 'sandBurial': ('Sand Burial', 5,
  'Sand Burial (Virgo ninjutsu, Elemental 22, single target in the Zone of Awareness, Root 2 rounds STR DC 13, 2x poise damage: the caster commands the sand round its opponent to envelop and crush it): from the guard the fighter makes the seal at the chin and sinks, sand grains lifting off the floor round its feet and a sandy aura rising; it sweeps both open palms low and forward over the ground and sand streams away along the floor toward the target; then it lifts the near hand palm up, drawing the sand up round the foe, and clenches it into a fist, squeezing, arm trembling, as the sand closes and crushes; it holds the squeeze, then drops back into the guard. On the target (the testbed plays sandBuried on it from the active frame; v2, Christopher 2026-10-28): sand heaps up round its legs and climbs to its neck, pinning its arms, and the column squeezes it, looping, until the Root ends, when it breaks free (sandBreakFree).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-40, -45, fistKind='palm'), af=band(-30, -55, fistKind='palm'), bob=(4, 5, 5), lean=(1, 7), **BRACE),   # palms swept low over the ground
     g(an=band(-120, -150, fistKind='palm'), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 1), **LOW),                     # palm up, drawing the sand up
     g(an=band(-115, -155), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 2), **LOW),                                        # clenched: crush
     g(an=band(-115, -155), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 2), root=(1, 0), **LOW),
     g(an=band(-115, -155), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 2), root=(-1, 0), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'closed', 'squint', 'squint', 'strain', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#e6c27a', '#9c7434'), rm='a 1 px tremble on frames 6-7 (net 0)',
       extra={'targetState': {'rule': 'Sand Burial: on the active frame the testbed plays sandBuried on the target (frames 0-3 once: sand heaps up and climbs to the neck; then frames 4-7 on loop, the column squeezing) until the Root ends, then sandBreakFree once (v2, Christopher 2026-10-28)', 'state': 'sandBuried', 'loopFrom': 4}},
       anchored={2: [('sandRise', 'feet', -8, -4), ('sandRise', 'feet', 9, -6)],
                 3: [('sandStream', 'feet', 14, -1), ('sandRise', 'hand', 0, -3), ('grains', 'feet', -9, -8)],
                 4: [('sandStream', 'feet', 18, -1, {'alpha': {'s': 170, 'S': 170, 'Z': 190}}), ('whirl0F', 'hand', 0, -2), ('grains', 'hand', 2, 5)],
                 5: [('whirl1F', 'hand', 0, -1), ('sandH', 'hand', 0, 0), ('grains', 'hand', 3, 6)],
                 6: [('whirl2F', 'hand', 0, -1), ('grains', 'hand', -3, 6)], 7: [('whirl3F', 'hand', 0, -1, {'alpha': {'s': 150, 'S': 150, 'Z': 170}})]})),
 'sandBuried': ('Sand Buried', 3,
  'Sand Buried (target state of Sand Burial, Root 2 rounds, 2x poise damage), v2 (Christopher 2026-10-28: the sand comes up to the target\'s neck and visibly squeezes it; a break-free animation when it ends): sand heaps up round the fighter\'s feet, flinching, then climbs its legs and body, pinning its arms to its sides, until only the head sticks out of a column of packed sand; the column squeezes, pinching in round the body with dark constriction bands winding round it, the face twisting in pain, grains spurting out at the neck on each squeeze; it keeps squeezing, frames 4-7 on loop, until the Root ends, when the testbed plays sandBreakFree.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 2), lean=(0, 0))],
  ['pain', 'pain', 'pain', 'strain', 'strain', 'pain', 'strain', 'pain'],
  None,
  dict(fps=8, extra={'loop': True, 'loopFrom': 4, 'breakFree': {'rule': 'Sand Burial v2: when the Root ends (or the target is freed) the testbed plays sandBreakFree once, then the idle', 'state': 'sandBreakFree'}},
       anchored={0: [('mound6', 'feet', 0, -3), ('grains', 'feet', -10, -9), ('grains', 'feet', 10, -12)],
                 1: [('mound18', 'feet', 0, -9), ('sandRise', 'feet', -11, -21), ('sandRise', 'feet', 11, -23)],
                 2: [('coffin30', 'feet', 0, -15), ('grains', 'head', -9, 8)],
                 3: [('colRise', 'head', 0, 32), ('grains', 'head', 9, 4)],
                 4: [('col0', 'head', 0, 32)],
                 5: [('col1', 'head', 0, 32), ('grains', 'head', -7, 5), ('grains', 'head', 7, 4)],
                 6: [('col2', 'head', 0, 32)],
                 7: [('col3', 'head', 0, 32), ('grains', 'head', 8, 5), ('grains', 'head', -8, 4)]})),
 'sandBreakFree': ('Sand Break Free', 2,
  'Sand Break Free (target state, Sand Burial v2: plays once when the Root ends): buried to the neck in the squeezing sand, the fighter strains, and cracks split the packed column, spreading; then it bursts its arms up and out with a roar and the sand blows apart, chunks of packed sand flying out in a ring and grains spraying, the column collapsing to a low heap round its feet; the chunks fall and scatter, the heap slumps flat and the fighter drops back into its guard.', [
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0), root=(1, 0)),
     g(an=band(-135, -175), af=band(120, 175), bob=(0, 0, 0), lean=(0, -1), root=(-1, 0)),
     g(an=band(-130, -170), af=band(115, 170), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-80, -150), af=band(60, 120), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-50, -120), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1)),
     g(),
     g()],
  ['strain', 'strain', 'roar', 'roar', 'squint', 'squint', None, None],
  None,
  dict(fps=10, rm='a 1 px shudder on frames 1-2 (net 0)',
       anchored={0: [('colCrack1', 'head', 0, 32)], 1: [('colCrack2', 'head', 0, 32), ('grains', 'head', -8, 5), ('grains', 'head', 8, 3)],
                 2: [('shatter12', 'head', 0, 20), ('mound14', 'feet', 0, -7)],
                 3: [('shatter18', 'head', 0, 22), ('mound14', 'feet', 0, -7)],
                 4: [('shatter23', 'head', 0, 26, {'alpha': {'S': 190, 's': 180, 'Z': 200}}), ('mound6', 'feet', 0, -3)],
                 5: [('mound6', 'feet', 0, -3, {'alpha': {'S': 170, 's': 160, 'Z': 170}}), ('grains', 'feet', -12, -3), ('grains', 'feet', 12, -2)],
                 6: [('sandPuff', 'feet', -9, -1, {'alpha': {'S': 130, 's': 120, 'Z': 130}}), ('sandPuff', 'feet', 9, -1, {'alpha': {'S': 130, 's': 120, 'Z': 130}})]})),
 'sandstorm': ('Sandstorm', 6,
  'Sandstorm (Virgo ninjutsu), v2 (Christopher 2026-10-28: a user-centred AoE; a hazardous storm round the user that deals light damage, lowers the accuracy of anyone inside and keeps every projectile that is not an ultimate from entering): from the guard the fighter makes the seal, then sinks low with both fists driven down beside the hips; sand lifts off the floor round its feet and starts to turn, a low ring of sand spinning round its legs; it rises and raises the near hand high, palm up, circling it, and the storm climbs with it, round the waist, then the chest, until a sand tornado stands round the whole fighter with the fighter calm in its eye, crystal and grit shrapnel caught in the streaks, the front half drawn over the fighter (part see-through) and the back half behind it; it sweeps the open hand out and down and the storm blasts outward, sand spraying off both sides; it settles back into the guard with a thin ring of storm still turning round it. The testbed then draws the storm over the whole AoE for as long as it lasts (extra.zone).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-115, -140, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-122, -150, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-110, -132, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-122, -150, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-110, -132, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-40, -40, fistKind='palm'), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-40, -40, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'strain', 'strain', 'squint', 'squint', 'closed', 'closed', 'closed', 'strain', 'squint', None],
  [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 2, 1],
  dict(fps=10, auraColors=('#e6c27a', '#9c7434'),
       extra={'zone': {'rule': 'Sandstorm v2 (Christopher 2026-10-28): AoE centred on the caster\'s hex (selfCentered, no aim point), placeholder radius 2 for 3 rounds; the testbed draws the storm (stormRing pattern turning, sand streaks and grit) over every hex of the AoE, following the caster if it moves; each round every other fighter inside takes light Elemental damage (placeholder 4) and an accuracy penalty while inside (placeholder -20% hit chance, Claude\'s reading: the caster in the eye is not penalised); a Projectile that is not an ultimate cannot enter: it stops at the first AoE hex on its line and breaks up in a sandPuff; ultimates pass through', 'pattern': 'stormRing', 'radius': 2, 'rounds': 3, 'selfCentered': True, 'blocksProjectiles': 'non-ultimate'},
              'targetState': {'rule': 'Sandstorm v2: every other fighter inside the AoE plays sandstormCaught on loop while it stays inside', 'state': 'sandstormCaught'}},
       anchored={1: [('sandRise', 'feet', -10, -6), ('sandRise', 'feet', 10, -6)],
                 2: [('eyeLow0B', 'feet', 0, -8, {'behind': True}), ('eyeLow0F', 'feet', 0, -8)],
                 3: [('eyeLow1B', 'feet', 0, -8, {'behind': True}), ('eyeLow1F', 'feet', 0, -8), ('grains', 'feet', 12, -14)],
                 4: [('eyeMid2B', 'feet', 0, -16, {'behind': True}), ('eyeMid2F', 'feet', 0, -16, {'alpha': {'s': 190, 'S': 190, 'Z': 210}})],
                 5: [('eyeMid3B', 'feet', 0, -16, {'behind': True}), ('eyeMid3F', 'feet', 0, -16, {'alpha': {'s': 190, 'S': 190, 'Z': 210}}), ('grains', 'feet', -13, -26)],
                 **{6 + k: [('eye%dB' % k, 'feet', 0, -26, {'behind': True}), ('eye%dF' % k, 'feet', 0, -26, {'alpha': {'s': 170, 'S': 170, 'Z': 200, 'C': 220, 'c': 220, 'K': 220}})] for k in range(3)},
                 9: [('eye3B', 'feet', 0, -26, {'behind': True}), ('eye3F', 'feet', 0, -26, {'alpha': {'s': 130, 'S': 130, 'Z': 160}}), ('sandSpray', 'feet', 20, -20), ('sandSprayL', 'feet', -20, -20)],
                 10: [('sandCloud2', 'feet', 22, -18), ('sandCloud2', 'feet', -22, -18), ('eyeLow2B', 'feet', 0, -8, {'behind': True}), ('eyeLow2F', 'feet', 0, -8, {'alpha': {'s': 140, 'S': 140, 'Z': 160}})],
                 11: [('eyeLow3B', 'feet', 0, -8, {'behind': True}), ('eyeLow3F', 'feet', 0, -8, {'alpha': {'s': 110, 'S': 110, 'Z': 130}})]})),
 'sandstormCaught': ('Caught in Sandstorm', 0,
  'Caught in Sandstorm (target state of Sandstorm v2, plays while the fighter stays inside the storm: light damage each round, lowered accuracy): sand streaks and grit blow across the fighter in the direction the storm turns, crystal and grit shrapnel flicking past, some in front of it and some behind; the fighter throws its forearms up over its eyes and flinches, swaying, squinting through the sand (loops, one gust every two frames).', [
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -2), root=(-1, 0)),
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -2), root=(1, 0))],
  ['pain', 'pain', 'pain', 'pain'],
  None,
  dict(fps=10, extra={'loop': True},
       anchored={k: [('gust%dB' % k, 'feet', 0, -22, {'behind': True}), ('gust%dF' % k, 'feet', 0, -22, {'alpha': {'s': 200, 'S': 200, 'Z': 220}})] for k in range(4)})),
 'phantomPlague': ('Phantom Plague', 5,
  'Phantom Plague (Virgo genjutsu, mental summon / DoT: images of a shadowy creature that only the caster and the victim see haunt the victim across the field, dealing damage and ignoring stealth; Psychosomatic 3 rounds 4/tick, INT save DC 12; range Zone of Awareness): from the guard the fighter lifts two fingers before its eyes, which kindle crystal teal, and its shadow pools out dark across the floor; it sinks low and points down into the pool, and a hunched shadow creature with teal eyes claws up out of it behind the fighter, rising to its full height; then the fighter thrusts the pointing hand at the target and the creature glides forward past it, clawed arm reaching, fading as it goes; the glow dies and the fighter steps back into the guard. The testbed then draws the phantom (wraith pattern) hovering beside the target, following it everywhere, even in stealth, and lashing at it on each tick; the target takes genjutsuAfflicted in earth colours.', [
     g(),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-30, -50, fistKind='point'), af=band(-20, -60), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g(an=band(-30, -50, fistKind='point'), af=band(-20, -60), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g(an=band(-90, -90, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     g(an=band(-90, -90, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-90, -90, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-50, -120), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#3a2f40', '#7fe3d0'), rm='E: +1 into the point, -1 settling back',
       extra={'targetState': {'rule': 'Phantom Plague (Christopher 2026-10-28: the target needs an animation for the duration): on the active frame the target starts phantomHaunted on loop in place of its idle and keeps it until the Psychosomatic ends; the genjutsu mark (genjutsuAfflicted halo, aura and eye glow, earth colours) is drawn over it as on any other state', 'state': 'phantomHaunted', 'element': 'earth', 'mark': 'genjutsuAfflicted'},
              'summon': {'rule': 'Phantom Plague: while the Psychosomatic lasts the testbed draws the phantom (pattern wraith, palette X/x/C, about 70% opacity, bobbing 1 px) hovering just behind the target and following it every move; it stays visible on a target in stealth (ignores stealth, drawn only for the caster and the victim); on each 4/tick it lunges 3 px and the target flinches', 'pattern': 'wraith'}},
       anchored={1: [('eyeC', 'eye', 0, 0)], 2: [('eyeCF', 'eye', 0, 0), ('shadowPool', 'feet', -2, -1)],
                 3: [('eyeCF', 'eye', 0, 0), ('shadowPool2', 'feet', -3, -1), ('wraithRise', 'feet', -13, -7, {'behind': True})],
                 4: [('eyeCF', 'eye', 0, 0), ('shadowPool2', 'feet', -3, -1), ('wraith', 'feet', -14, -20, {'behind': True})],
                 5: [('eyeCF', 'eye', 0, 0), ('shadowPool', 'feet', 0, -1), ('wraith', 'feet', 4, -22, {'alpha': {'X': 230, 'x': 172, 'C': 255}})],
                 6: [('eyeC', 'eye', 0, 0), ('wraith', 'feet', 13, -23, {'alpha': {'X': 215, 'x': 161, 'C': 255}})],
                 7: [('wraith', 'feet', 20, -24, {'alpha': {'X': 175, 'x': 131, 'C': 215}})], 8: [('wraith', 'feet', 25, -24, {'alpha': {'X': 120, 'x': 90, 'C': 160}})]})),
 'phantomHaunted': ('Haunted by the Phantom', 0,
  'Haunted by the Phantom (target state of Phantom Plague; Psychosomatic 3 rounds 4/tick), v2 (Christopher 2026-10-28: the phantom circles the opponent before hitting): the victim hunches low and wary, forearms raised before its face, while the hunched shadow creature with teal eyes, part see-through, circles round it: from behind it drifts past the far side (fainter, behind the victim), round in front (turned to face it), back across the near side over the victim and round behind again; then it leans in over the victim\'s shoulder and rakes its clawed arm down past it, three teal claw marks flashing, the victim flinching forward, wincing, and it draws back behind (loops; the testbed lines the rake up with each 4/tick and draws the genjutsu mark over it).', [
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-60, -150), af=band(-65, -155), bob=(3, 3, 3), lean=(1, 5), root=(1, 0), **LOW),
     g(an=band(-60, -150), af=band(-65, -155), bob=(3, 3, 3), lean=(1, 4), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), root=(-1, 0), **LOW)],
  ['squint'] * 9 + ['pain', 'pain', 'squint'],
  None,
  dict(fps=8, extra={'loop': True},
       anchored={0: [('wraith', 'feet', -13, -22, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})],
                 1: [('wraith', 'feet', -8, -23, {'behind': True, 'alpha': {'X': 120, 'x': 90, 'C': 200}})],
                 2: [('wraith', 'feet', 0, -24, {'behind': True, 'alpha': {'X': 120, 'x': 90, 'C': 200}})],
                 3: [('wraithM', 'feet', 8, -24, {'behind': True, 'alpha': {'X': 120, 'x': 90, 'C': 200}})],
                 4: [('wraithM', 'feet', 14, -23, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})],
                 5: [('wraithM', 'feet', 9, -22, {'alpha': {'X': 150, 'x': 110, 'C': 255}})],
                 6: [('wraith', 'feet', 1, -22, {'alpha': {'X': 150, 'x': 110, 'C': 255}})],
                 7: [('wraith', 'feet', -7, -23, {'alpha': {'X': 150, 'x': 110, 'C': 255}})],
                 8: [('wraith', 'feet', -12, -24, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})],
                 9: [('wraith', 'feet', -7, -24, {'alpha': {'X': 160, 'x': 120, 'C': 255}}), ('clawMark', 'head', 3, 12)],
                 10: [('wraith', 'feet', -9, -23, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}}), ('clawMark2', 'head', 3, 14)],
                 11: [('wraith', 'feet', -12, -22, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})]})),
 'coffinSyndrome': ('Coffin Syndrome', 4,
  'Coffin Syndrome (Virgo genjutsu, mental debuff: the caster projects images of being buried alive on its opponent until panic scrambles its mind; Confusion 1 round, STR save DC 13; range Zone of Awareness), v2 (Christopher 2026-10-28: an actual coffin rises up behind the target and encloses it, with a break-out animation): from the guard the fighter raises the near hand palm up before its chest, eyes kindling crystal teal, and slowly lifts it, summoning the coffin up out of the floor behind the target; then it turns the hand over and snaps it shut into a fist, slamming the lid closed on the target; it holds the fist, sand motes drifting off it, then the glow dies and it returns to the guard. The target plays coffinEntombed from the active frame (the coffin rises behind it, the lid swings shut over it, it pounds on the lid inside) until the Confusion ends, then coffinBreakOut once; the genjutsu mark (earth colours) is drawn over both.', [
     g(),
     g(an=band(-60, -100, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-70, -110, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-90, -135, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-110, -155, fistKind='palm'), bob=(0, 0, 1), lean=(0, -2)),
     g(an=band(-110, -155, fistKind='palm'), bob=(0, 0, 1), lean=(0, -2)),
     g(an=band(-92, -92), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),     # the hand snaps shut: the lid slams
     g(an=band(-92, -92), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-92, -92), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-50, -120), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'strain', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e6c27a', '#7fe3d0'),
       extra={'targetState': {'rule': 'Coffin Syndrome v2 (Christopher 2026-10-28): from the active frame (the caster\'s palm starts to lift, frame 2) the target plays coffinEntombed: intro frames 0-5 once (the coffin rises behind it, the lid closes on frame 5, lined up with the caster\'s fist on frame 6), then frames 6-9 on loop until the Confusion ends; then coffinBreakOut once, back to its guard. The genjutsu mark (genjutsuAfflicted halo, aura, eye glow, earth colours) is drawn over it throughout', 'state': 'coffinEntombed', 'loopFrom': 6, 'element': 'earth', 'mark': 'genjutsuAfflicted', 'breakFree': 'coffinBreakOut'}},
       anchored={1: [('eyeC', 'eye', 0, 0)], 2: [('eyeCF', 'eye', 0, 0), ('grains', 'hand', 0, -4)], 3: [('eyeCF', 'eye', 0, 0), ('sandRise', 'hand', 0, -5)],
                 4: [('eyeCF', 'eye', 0, 0), ('sandRise', 'hand', 0, -6), ('grains', 'hand', 3, -9)], 5: [('eyeCF', 'eye', 0, 0), ('sandRise', 'hand', 1, -6)],
                 6: [('eyeCF', 'eye', 0, 0), ('sandPuff', 'hand', 2, 0), ('vRing', 'hand', 2, 0)], 7: [('eyeCF', 'eye', 0, 0), ('sandTrk', 'hand', 0, 5)],
                 8: [('eyeC', 'eye', 0, 0), ('grains', 'hand', 0, 6, {'alpha': {'S': 140, 's': 130, 'Z': 150}})]})),
 'coffinEntombed': ('Entombed', 0,
  'Entombed (target state of Coffin Syndrome v2, Confusion 1 round): an illusory coffin, a box of packed sand outlined in crystal teal, rises up out of the floor close behind the fighter, sand pouring off it, and stands upright over it; the lid swings round from the hinge at its back edge and slams shut over the fighter in front, a puff of sand and a teal ring bursting off it; inside, the fighter (seen faintly through the illusion) pounds on the lid with both palms, panicking, and the coffin shudders with each blow, sand trickling from its seams (loops from frame 6 until the Confusion ends; then coffinBreakOut).', [
     g(),
     g(bob=(1, 1, 2), lean=(-1, -2)),
     g(an=band(-60, -140), af=band(-70, -150), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-60, -140), af=band(-70, -150), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-50, -155, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-50, -155, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-55, -140, fistKind='palm'), af=band(-45, -150, fistKind='palm'), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-55, -140, fistKind='palm'), af=band(-45, -150, fistKind='palm'), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0))],
  [None, 'squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain'],
  None,
  dict(fps=10, extra={'loop': True, 'loopFrom': 6},
       anchored={0: [('cofBack', 'feet', -2, 24, {'behind': True}), ('sandPuff', 'feet', -10, -1), ('sandPuff', 'feet', 8, -1)],
                 1: [('cofBack', 'feet', -2, 4, {'behind': True}), ('grains', 'feet', -14, -8), ('sandTrk', 'feet', 9, -10)],
                 2: [('cofBack', 'feet', -2, -27, {'behind': True}), ('sandTrk', 'feet', -14, -16), ('grains', 'feet', 12, -20)],
                 3: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLid1', 'feet', -13, -27)],
                 4: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLid2', 'feet', -7, -27, {'alpha': {'s': 210, 'S': 210, 'Z': 220}})],
                 5: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLid', 'feet', -2, -27, {'alpha': {'s': 190, 'S': 190, 'Z': 200}}), ('sandPuff', 'feet', 13, -40), ('sandPuff', 'feet', -14, -12), ('vRing2', 'feet', 0, -28, {'alpha': {'c': 200, 'C': 180}})],
                 **{6 + k: [('cofBack', 'feet', -2 + d, -27, {'behind': True}), ('cofLid', 'feet', -2 + d, -27, {'alpha': {'s': 185, 'S': 185, 'Z': 195}}), ('sandTrk', 'feet', 12 + d, -30 + 6 * k)] + ([('grains', 'feet', -13, -44)] if k % 2 == 0 else [])
                    for k, d in enumerate((1, 0, -1, 0))}})),
 'coffinBreakOut': ('Coffin Break Out', 2,
  'Coffin Break Out (target state of Coffin Syndrome v2: plays once when the Confusion ends): inside the shut coffin the fighter strains, and cracks split the lid, spreading; then it bursts the lid open with both arms thrown out and a roar, and the coffin breaks apart into teal-edged planks and clumps of sand flying outward, the back of it crumbling into the floor; the pieces fade as they fall and the fighter shakes itself back into the guard.', [
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(an=band(-135, -175), af=band(120, 175), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-130, -170), af=band(115, 170), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-80, -150), af=band(60, 120), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-50, -120), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  ['pain', 'strain', 'roar', 'roar', 'squint', None, None],
  [0, 1, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e6c27a', '#7fe3d0'),
       anchored={0: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLidCrack', 'feet', -2, -27, {'alpha': {'s': 190, 'S': 190, 'Z': 210}})],
                 1: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLidCrack2', 'feet', -2, -27, {'alpha': {'s': 190, 'S': 190, 'Z': 210}}), ('grains', 'feet', 12, -36)],
                 2: [('cofBackLow', 'feet', -2, -20, {'behind': True}), ('plank', 'feet', 15, -40), ('plankV', 'feet', -16, -34), ('plank', 'feet', 13, -14), ('sandBurst', 'feet', 0, -30, {'alpha': {'S': 200, 's': 190, 'Z': 210}}), ('sandPuff', 'feet', -14, -12)],
                 3: [('cofBackLow2', 'feet', -2, -12, {'behind': True}), ('plank', 'feet', 21, -36), ('plankV', 'feet', -22, -28), ('plank', 'feet', 19, -8), ('sandCloud', 'feet', 0, -28, {'alpha': {'S': 150, 's': 140, 'Z': 160}})],
                 4: [('mound6', 'feet', -2, -3), ('plank', 'feet', 24, -26, {'alpha': {'C': 150, 'c': 150, 's': 120, 'S': 120}}), ('plankV', 'feet', -25, -16, {'alpha': {'C': 150, 'c': 150, 's': 120, 'S': 120}}), ('sandCloud2', 'feet', 0, -24, {'alpha': {'S': 110, 's': 100, 'Z': 120}})],
                 5: [('grains', 'feet', -8, -4, {'alpha': {'S': 120, 's': 110, 'Z': 130}}), ('grains', 'feet', 10, -5, {'alpha': {'S': 120, 's': 110, 'Z': 130}})]})),
 'adamantineShin': ('Adamantine Shin', 4,
  'Adamantine Shin (Capricorn taijutsu strike, Physical 16, Guard Break, 1.5x poise damage, Bleed 2 rounds 3/tick: a bone-hard shin that cracks structure): from the guard the fighter lifts the near knee and crystal starts to grow over the shin from the ankle up, teal facets with white glints; it chambers the knee high as the crystal sheath closes over the whole shin, a glint flashing on it; then it pivots on the lead foot and snaps the crystal shin through level at the opponent\'s thigh, a crystal-white burst, a teal shock ring and a cross-shaped crack flashing at the point of impact and crystal shards and grit flying off; it drives through, recoils the leg and sets it down, the crystal flaking away, back into the guard.', [
     g(),
     g(an=band(10, -60), af=band(-60, -90), bob=(1, 1, 1), lean=(0, 0), ln='as-lift', lf='lk-lead-pivot'),
     g(an=band(15, -50), af=band(-65, -95), bob=(0, 0, 1), lean=(0, -1), ln='as-chamber', lf='lk-lead-pivot'),
     g(an=band(15, -50), af=band(-65, -95), bob=(0, 0, 1), lean=(0, -1), ln='as-chamber', lf='lk-lead-pivot'),
     g(an=band(40, -20), af=band(-80, -100), bob=(1, 1, 1), lean=(-1, -3), root=(1, 0), ln='as-kick', lf='lk-lead-pivot'),
     g(an=band(40, -20), af=band(-80, -100), bob=(1, 1, 1), lean=(-1, -3), ln='as-kick2', lf='lk-lead-pivot'),
     g(an=band(20, -40), af=band(-65, -90), bob=(1, 1, 2), lean=(0, -1), ln='as-recoil', lf='lk-lead-pivot'),
     g(bob=(1, 1, 1), lean=(0, 0), root=(-1, 0)),
     g()],
  [None, 'squint', 'strain', 'strain', 'roar', 'strain', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 38, 14, 12], damage='heavy', rm='E: +1 into the kick, -1 setting down',
       crystal={'shin': {1: ('as-lift', 0.35, 235), 2: ('as-chamber', 0.75, 245), 3: ('as-chamber', 1.0, 255), 4: ('as-kick', 1.0, 255), 5: ('as-kick2', 1.0, 255), 6: ('as-recoil', 0.8, 190)}},
       anchored={1: [('gemSpark', 'feet', 2, -12)], 3: [('gemSpark', 'head', 6, 26), ('gemShard', 'feet', 9, -18)],
                 4: [('gemBurst', 'head', 24, 28), ('gemCrack', 'head', 24, 28), ('gemShard2', 'head', 27, 21), ('gemSpark', 'head', 28, 33)],
                 5: [('gemBurst2', 'head', 25, 29), ('gemCrack', 'head', 25, 29), ('gemShard2', 'head', 29, 22), ('gemShard2', 'head', 28, 36), ('gemShard', 'head', 31, 29), ('rocks', 'head', 23, 37), ('gemSpark', 'head', 21, 20)],
                 6: [('gemShard', 'head', 30, 35), ('gemShard', 'head', 31, 25), ('gemShard', 'head', 27, 41), ('dust1', 'feet', 10, -3)], 7: [('gemShard', 'feet', 12, -2)]})),
 'diamondCutter': ('Diamond Cutter', 5,
  'Diamond Cutter (Capricorn taijutsu strike, True damage 14, bypasses poise and mitigation: the fighter focuses its resolve into its hand, hardening it until it crystallises, then throws an unguardable chop): from the guard the fighter draws the near hand up open above its ear, elbow high behind, , knife-edge forward, eyes narrowing; crystal grows over the hand and forearm from the fingertips back, teal facets with white glints, over three held frames, a glint flashing on the edge; then it steps in and brings the crystal knife-hand chopping down and through on a diagonal, a bright white-and-teal slash line cutting the air along its path, and on contact a thin slash of light and a spray of crystal shards; it holds the follow-through low, the crystal flaking off, and returns to the guard.', [
     g(),
     g(an=band(70, -170, fistKind='palm'), af=band(-70, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-110, -110, fistKind='palm'), af=band(-30, -80), bob=(1, 1, 2), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-65, -55, fistKind='palm'), af=band(20, -60), bob=(2, 2, 3), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-60, -50, fistKind='palm'), af=band(20, -60), bob=(2, 2, 3), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -90), af=band(-30, -100), bob=(1, 1, 2), lean=(1, 2), root=(-2, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'roar', 'strain', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[44, 22, 14, 14], damage='medium', rm='E: +2 stepping into the chop, -2 settling back',
       crystal={'arm': {2: (0.2, 235), 3: (0.4, 250), 4: (0.6, 255), 5: (0.6, 255), 6: (0.6, 255), 7: (0.6, 230), 8: (0.3, 150)}},
       anchored={3: [('gemSpark', 'head', -9, -5)], 4: [('gemSpark', 'head', -8, -7), ('cryst', 'head', -12, 0)],
                 5: [('slash', 'hand', -2, 1)],
                 6: [('slash2', 'hand', -3, -5), ('gemShard2', 'hand', 5, 2), ('gemSpark', 'hand', 3, -3)],
                 7: [('gemShard', 'hand', 6, 4), ('gemShard', 'hand', 2, 8), ('cryst', 'hand', 8, -2)], 8: [('crystT', 'hand', 3, 5)]})),
 'prismaticSkin': ('Prismatic Skin', 4,
  'Prismatic Skin (Capricorn taijutsu stance buff, FORT +50% 2 rounds: by focusing its resolve the fighter\'s skin crystallises over, granting enhanced durability): from the guard the fighter drops its fists to its hips, elbows back, and tenses, sinking a little, eyes squeezed; a crystal-teal aura rises round it and crystal spreads over all its skin, pale teal with white facet lines and deep teal facets, glints flashing on the shoulders and forearms and small crystal shards popping off; it holds, glittering, then rises back into the guard still crystallised (the testbed keeps the crystal skin while the buff lasts).', [
     g(),
     g(an=band(15, -40), af=band(5, -35), bob=(1, 1, 1), lean=(0, 0)),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'strain', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#3a9e8f'), tint={2: 90, 3: 160, 4: 205, 5: 205, 6: 205, 7: 205, 8: 205}, veins=(), tintColors=((0x7f, 0xe3, 0xd0), (0x3a, 0x9e, 0x8f), (0xf0, 0xff, 0xfc), (0x2c, 0x80, 0x74)),
       extra={'linger': {'rule': 'Prismatic Skin (FORT +50% 2 rounds): the clip ends with the skin crystallised; while the buff lasts the testbed keeps drawing the fighter with the crystal tint (crystal teal #7fe3d0 at alpha 205 over skin pixels, white facet streaks #f0fffc and deep teal facet patches #2c8074 off the face), as Oak Flesh does', 'tint': '#7fe3d0', 'alpha': 205, 'streak': '#f0fffc', 'facet': '#2c8074'}},
       anchored={3: [('gemSpark', 'head', -7, 14), ('gemShard', 'head', 8, 18)],
                 4: [('gemSpark', 'head', 7, 12), ('gemShard', 'head', -8, 22), ('cryst', 'head', 9, 26)],
                 5: [('gemSpark', 'head', -6, 20), ('cryst', 'head', 7, 16)], 6: [('gemSpark', 'head', 6, 24)], 7: [('cryst', 'head', -6, 18)]})),
 'geodeBlast': ('Geode Blast', 5,
  'Geode Blast (Capricorn ninjutsu, Elemental 18, AoE in the Zone of Awareness, Bleed 2 rounds 3/tick: the fighter calls the minerals in the earth to burst from the ground, sending shrapnel over a wide area): from the guard the fighter makes the seal at the chin and sinks, an earthen aura rising with crystal glints in it; it drops and slams the near palm flat on the floor, cracks glowing teal running away from the hand along the ground toward the target; then it whips the palm up, open, and clenches it into a fist before its face, and at the target the ground splits and clusters of jagged crystal spikes burst up out of it, shards spraying out (the target plays geodeBlasted); it holds the fist, then drops back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-35, -40, fistKind='palm'), af=band(-30, -100), bob=(5, 6, 6), lean=(1, 8), **BRACE),   # palm slammed flat on the floor
     g(an=band(-35, -40, fistKind='palm'), af=band(-30, -100), bob=(5, 6, 6), lean=(1, 8), **BRACE),
     g(an=band(-120, -150, fistKind='palm'), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 1), **LOW),    # the palm whipped up: the geodes burst at the target
     g(an=band(-115, -155), af=band(-30, -100), bob=(1, 1, 1), lean=(0, 0), **LOW),                       # clenched into a fist overhead
     g(an=band(-115, -155), af=band(-30, -100), bob=(1, 1, 1), lean=(0, 0), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'roar', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'),
       extra={'targetState': {'rule': 'Geode Blast: on the active frame (the palm whips up, frame 5) the testbed plays geodeBlasted once on every fighter in the blast (crystal spikes burst up round it, shards spray, it flinches and bleeds), then its idle', 'state': 'geodeBlasted', 'loopFrom': None, 'element': 'earth'}},
       anchored={2: [('cryst', 'head', -9, 12), ('cryst', 'head', 9, 18)],
                 3: [('crack1', 'feet', 14, -1), ('crackGlow', 'feet', 14, -2), ('dust1', 'feet', 15, -4), ('rocks', 'feet', 12, -8)],
                 4: [('crack2', 'feet', 16, -1), ('crackRun', 'feet', 24, -1), ('dust1', 'feet', 20, -3), ('gemSpark', 'feet', 14, -6)],
                 5: [('crackRun', 'feet', 26, -1, {'alpha': {'C': 170, 'K': 170}}), ('gemSpark', 'hand', 0, -3)],
                 6: [('gemSpark', 'hand', 0, -2), ('cryst', 'hand', 3, 4)], 7: [('cryst', 'hand', -2, 5)]})),
 'geodeBlasted': ('Geode Blasted', 1,
  'Geode Blasted (target state of Geode Blast, plays once): the floor under the fighter cracks, glowing teal; clusters of jagged crystal spikes burst up out of it round its feet, in front and behind, shards and grit spraying out, and the fighter flinches back with its guard up over its face, small cuts bleeding (Bleed); the spikes stand a beat, then crack and crumble into rubble, and the fighter drops back into its guard.', [
     g(bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(0, 0, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(0, 0, 1), lean=(-1, -3)),
     g(an=band(-55, -150), af=band(-45, -140), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 2), lean=(0, -1), root=(1, 0)),
     g()],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'squint', None],
  None,
  dict(fps=10, rm='E: -1 flinching back, +1 recovering',
       anchored={0: [('crack2', 'feet', 0, -1), ('crackGlow', 'feet', 0, -2)],
                 1: [('geoSmallB', 'feet', -2, -6, {'behind': True}), ('geoSmall', 'feet', 3, -5), ('rocks', 'feet', -10, -12), ('rocks', 'feet', 11, -10)],
                 2: [('geoBack', 'feet', -2, -15, {'behind': True}), ('geoFrontL', 'feet', -8, -11), ('geoFrontR', 'feet', 9, -12), ('shardFly', 'head', -10, 18), ('shardFly', 'head', 11, 14), ('gemShard', 'head', -12, 6), ('bloodN', 'head', 3, 14)],
                 3: [('geoBack', 'feet', -2, -15, {'behind': True}), ('geoFrontL', 'feet', -8, -11), ('geoFrontR', 'feet', 9, -12), ('shardFly', 'head', -14, 10), ('shardFly', 'head', 14, 6), ('gemShard', 'head', -15, -2), ('gemShard', 'head', 15, 0), ('bloodN', 'head', 4, 16), ('bloodN', 'head', -3, 22)],
                 4: [('geoBack2', 'feet', -2, -10, {'behind': True, 'alpha': {'C': 200, 'c': 200, 'T': 200}}), ('geoFrontL2', 'feet', -8, -7, {'alpha': {'C': 200, 'c': 200, 'T': 200}}), ('geoFrontR2', 'feet', 9, -8, {'alpha': {'C': 200, 'c': 200, 'T': 200}}), ('gemShard', 'head', -16, 14), ('gemShard', 'head', 16, 18), ('bloodN', 'head', 4, 18)],
                 5: [('rubble', 'feet', -7, -2), ('rubble', 'feet', 8, -2), ('dust1', 'feet', 0, -3)]})),
 'mausoleum': ('Mausoleum', 2,
  'Mausoleum (Capricorn ninjutsu, Elemental 6, Terrain, Wall 2 rounds, Root 1 round STR save DC 14: the fighter calls up entombing walls that root the foe), v2 (Christopher 2026-10-29: needs a rework; Claude\'s reading: a small tomb built round the target): from the guard the fighter makes the seal at the chin and sinks, an earthen aura rising; it sweeps both open palms down low over the floor and heaves them up, palms up, as if lifting a great weight, and at the target two fluted stone pillars, ringed with glowing crystal teal, grind up out of the ground on either side of it; then it pushes both palms forward and down together and a stone roof, a pediment over a thick lintel, drops onto the pillars, sealing the target in its tomb (the target plays mausoleumSealed); it holds, arms trembling, then drops back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-40, -45, fistKind='palm'), af=band(-30, -55, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), **BRACE),   # palms swept low over the floor: the pillars start to rise
     g(an=band(-90, -150, fistKind='palm'), af=band(-80, -145, fistKind='palm'), bob=(3, 3, 3), lean=(0, 2), **LOW),     # heaving them up, palms up
     g(an=band(-120, -160, fistKind='palm'), af=band(-110, -155, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-120, -160, fistKind='palm'), af=band(-110, -155, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-92, -92, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), root=(1, 0), **LOW),   # both palms pushed forward and down: the roof drops
     g(an=band(-75, -70, fistKind='palm'), af=band(-72, -68, fistKind='palm'), bob=(3, 3, 3), lean=(1, 4), **LOW),
     g(an=band(-75, -70, fistKind='palm'), af=band(-72, -68, fistKind='palm'), bob=(3, 3, 4), lean=(1, 4), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'strain', 'strain', 'roar', 'strain', 'strain', 'strain', 'strain', None, None],
  [0, 1, 2, 2, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#b3aa9a', '#8a6236'), rm='E: +1 pushing the palms forward, -1 settling back',
       extra={'targetState': {'rule': 'Mausoleum v2: from the active frame (frame 2, the palms sweep low) the target plays mausoleumSealed: frames 0-5 once (cracks, the two pillars grind up either side, the roof drops onto them as the caster pushes, frame 5), then frames 6-9 on loop (it shoves at the front pillar) until the Root ends; the tomb is terrain for 2 rounds: while it stands the testbed keeps drawing the pillars and roof round that hex', 'state': 'mausoleumSealed', 'loopFrom': 6, 'element': 'earth', 'wallRounds': 2}},
       anchored={2: [('crack1', 'feet', 10, -1), ('dust1', 'feet', 12, -3)],
                 3: [('dust2', 'feet', 12, -3), ('rocks', 'feet', 14, -8), ('cryst', 'hand', 0, -3)],
                 4: [('rocks', 'hand', 2, -4), ('cryst', 'hand', -3, -6)], 5: [('gemSpark', 'hand', 0, -3)],
                 6: [('gemSpark', 'hand', 2, 0)], 7: [('dust1', 'feet', 8, -3)]})),
 'mausoleumSealed': ('Sealed in the Mausoleum', 1,
  'Sealed in the Mausoleum (target state of Mausoleum v2, Root 1 round): the floor cracks under the fighter and two fluted stone pillars, ringed with glowing crystal teal, grind up out of the ground on either side of it, dust spilling off them; it looks up as a stone roof, a pediment over a thick lintel, drops out of the air onto the pillars with a burst of dust, sealing it in; then (looping until the Root ends) it shoves at the front pillar with both palms, straining, grit trickling down from the lintel.', [
     g(bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-80, -85, fistKind='palm'), af=band(-75, -80, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), **BRACE),
     g(an=band(-82, -86, fistKind='palm'), af=band(-77, -82, fistKind='palm'), bob=(1, 1, 1), lean=(1, 4), **BRACE),
     g(an=band(-80, -85, fistKind='palm'), af=band(-75, -80, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), **BRACE),
     g(an=band(-82, -86, fistKind='palm'), af=band(-77, -82, fistKind='palm'), bob=(1, 1, 2), lean=(1, 4), **BRACE)],
  ['squint', 'pain', 'pain', 'squint', 'squint', 'pain', 'strain', 'strain', 'strain', 'strain'],
  None,
  dict(fps=8, extra={'loop': True, 'loopFrom': 6},
       anchored={0: [('crack2', 'feet', 0, -1), ('dust1', 'feet', -12, -3), ('dust1', 'feet', 12, -3)],
                 1: [('pillar1', 'feet', -14, -8.5), ('pillar1', 'feet', 14, -8.5), ('dust2', 'feet', -14, -3), ('dust2', 'feet', 14, -3)],
                 2: [('pillar2', 'feet', -14, -18.0), ('pillar2', 'feet', 14, -18.0), ('dust1', 'feet', -18, -14), ('dust1', 'feet', 18, -12)],
                 3: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('rocks', 'feet', -16, -40), ('dust1', 'feet', 15, -50)],
                 4: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('roof', 'feet', 0, -74)],
                 5: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('roof', 'feet', 0, -59), ('dust2', 'feet', -16, -53), ('dust2', 'feet', 16, -53), ('rocks', 'feet', 20, -44)],
                 6: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('roof', 'feet', 0, -59)], 7: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('roof', 'feet', 0, -59), ('grains', 'feet', 10, -48)], 8: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('roof', 'feet', 0, -59)], 9: [('pillar', 'feet', -14, -27.0), ('pillar', 'feet', 14, -27.0), ('roof', 'feet', 0, -59), ('grains', 'feet', -9, -46)]})),
 'stalactiteRain': ('Stalactite Rain', 10,
  'Stalactite Rain (Capricorn ninjutsu ultimate, charge, Elemental 30, wide AoE: the fighter channels its chakra through the earth, forming giant spear-like crystal formations), v2 (Christopher 2026-10-29: the crystal spears rise from behind the caster, then rain down on the target): from the guard the fighter makes the seal and sinks deep, straining, an earthen aura flaring with crystal glints; it slams both open palms down at the floor and the ground cracks behind it, glowing teal, and giant crystal spears grind up out of the earth behind it, point first, growing over three frames until they tower over its head; it heaves both palms up and the spears tear free of the ground and shoot up into the sky; then it hurls the near hand forward and down at the target, and the spears rain down out of the sky onto the target zone (the target plays stalactiteImpaled); it holds the throw, then settles back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE)] + [
     g(an=band(-35, -40, fistKind='palm'), af=band(-30, -45, fistKind='palm'), bob=(5, 6, 6), lean=(1, 7), **BRACE) for _ in range(4)] + [   # both palms slammed down: the spears grow behind
     g(an=band(-110, -150, fistKind='palm'), af=band(-100, -145, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), **LOW),   # heaving up: the spears tear free
     g(an=band(-160, -176, fistKind='palm'), af=band(-155, -174, fistKind='palm'), bob=(0, -1, 0), lean=(0, -1)),        # arms up: the spears shoot into the sky
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **LOW),        # hurled forward and down at the target: the spears rain down
     g(an=band(-100, -105, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-100, -105, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-80, -110, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'strain', 'strain', 'strain', 'strain', 'roar', 'roar', 'strain', 'strain', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'), rm='E: +1 into the throw, -1 settling back',
       extra={'targetState': {'rule': 'Stalactite Rain v2 (ultimate, charge): on the active frame (frame 10, the throw) the testbed plays stalactiteImpaled once on every fighter in the zone (crystal spears rain down out of the sky and stab into the ground round it, then shatter), then its idle', 'state': 'stalactiteImpaled', 'loopFrom': None, 'element': 'earth'}},
       anchored={2: [('cryst', 'head', -9, 12), ('cryst', 'head', 9, 16)],
                 3: [('cryst', 'head', -10, 18), ('gemSpark', 'head', 10, 10), ('crack1', 'feet', -14, -1)],
                 4: [('crack2', 'feet', -14, -1), ('crackGlow', 'feet', -14, -2), ('spearUpS1', 'feet', -11, -4.0, {'behind': True}), ('spearUp1', 'feet', -19, -5.5, {'behind': True}), ('rocks', 'feet', -14, -8)],
                 5: [('crack2', 'feet', -14, -1), ('spearUpS2', 'feet', -11, -9.5, {'behind': True}), ('spearUp2', 'feet', -19, -12.5, {'behind': True}), ('dust1', 'feet', -14, -3)],
                 6: [('crack2', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0, {'behind': True}), ('spearUp', 'feet', -19, -20.0, {'behind': True}), ('dust1', 'feet', -20, -3), ('gemSpark', 'feet', -19, -40)],
                 7: [('crack2', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0, {'behind': True}), ('spearUp', 'feet', -19, -20.0, {'behind': True}), ('gemSpark', 'feet', -12, -30), ('gemSpark', 'feet', -21, -36)],
                 8: [('crack2', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0 - 10, {'behind': True}), ('spearUp', 'feet', -19, -20.0 - 12, {'behind': True}), ('rocks', 'feet', -14, -6), ('dust2', 'feet', -14, -3)],
                 9: [('crack1', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0 - 30, {'behind': True}), ('spearUp', 'feet', -19, -20.0 - 34, {'behind': True}), ('spearStreak', 'feet', -11, -10), ('spearStreak', 'feet', -19, -14)],
                 10: [('spearStreak', 'feet', -12, -48), ('spearStreak', 'feet', -19, -52), ('gemSpark', 'hand', 2, -2)],
                 11: [('gemSpark', 'hand', 2, -3)], 12: [('cryst', 'hand', 3, -2)]})),
 'stalactiteImpaled': ('Stalactite Rain Struck', 2,
  'Stalactite Rain Struck (target state of Stalactite Rain v2, plays once): crystal glints flash in the sky over the fighter and it looks up; then giant crystal spears rain down out of the sky at a slant from the caster\'s side and stab deep into the ground all round it, in front and behind, dust and grit bursting off each impact, and it is jolted in pain, shards spraying; a second volley drives in; the spears stand embedded a beat, crack and shatter, crystal chunks and shards bursting outward and raining down into rubble, and the fighter staggers and drops back into its guard.', [
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-20, -60), af=band(-15, -55), bob=(0, -1, 0), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-20, -60), af=band(-15, -55), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(-25, -70), af=band(-20, -65), bob=(0, 0, 0), lean=(-1, -2)),
     g(an=band(-40, -110), af=band(-35, -105), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-40, -120), af=band(-35, -115), bob=(2, 2, 3), lean=(1, 2), root=(1, 0), **LOW),
     g()],
  ['squint', 'pain', 'roar', 'pain', 'pain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=10, rm='E: -1 jolted back, +1 recovering',
       anchored={0: [('gemSpark', 'head', 10, -6), ('gemSpark', 'head', -6, -8), ('spearStreak', 'head', 14, -8)],
                 1: [('spearFall', 'head', 12, 0), ('spearFallS', 'head', -4, -2), ('spearStreak', 'head', 20, -8)],
                 2: [('spearFall', 'feet', 11, -10, {'behind': True}), ('spearFallS', 'feet', -10, -8), ('dust2', 'feet', 9, -3), ('dust1', 'feet', -12, -3), ('gemShard2', 'head', 14, 10), ('bloodN', 'head', 3, 16), ('spearFall', 'head', 8, -6)],
                 3: [('spearFall', 'feet', 11, -10, {'behind': True}), ('spearFallS', 'feet', -10, -8), ('spearFall', 'feet', 2, -11, {'behind': True}), ('spearFallS', 'feet', 17, -8), ('dust2', 'feet', 0, -3), ('shardFly', 'head', -15, 4), ('shardFly', 'head', 16, 2)],
                 4: [('spearFall', 'feet', 11, -10, {'behind': True}), ('spearFallS', 'feet', -10, -8), ('spearFall', 'feet', 2, -11, {'behind': True}), ('spearFallS', 'feet', 17, -8), ('gemCrack', 'feet', 10, -18), ('gemCrack', 'feet', -9, -14)],
                 5: [('gemBurst2', 'feet', 2, -12), ('gemShard2', 'head', -16, 8), ('gemShard2', 'head', 16, 12), ('gemShard', 'head', -6, -4), ('gemShard', 'head', 8, -6), ('rubble', 'feet', -9, -2), ('rubble', 'feet', 10, -2)],
                 6: [('rubble', 'feet', -9, -2), ('rubble', 'feet', 9, -2), ('gemShard', 'head', -17, 18), ('gemShard', 'head', 17, 22), ('dust2', 'feet', 0, -3)],
                 7: [('rubble', 'feet', -9, -2), ('rubble', 'feet', 9, -2), ('gemShard', 'feet', -16, -4), ('gemShard', 'feet', 15, -3)]})),
 'flowDodge': ('Flow Dodge', 3,
  'Flow Dodge (Sagittarius taijutsu stance buff: the fighter enters a dance-like trance and begins to swing and sway to its own rhythm): from the guard the fighter shakes its arms loose and lets the guard drop low and easy, eyes half closed, catching a beat; then it sways to its own rhythm: rocking back and forward on its feet and dipping on the knees, shoulders rolling, the loose hands swinging opposite to the hips, a flickering fire aura breathing round it on the beat with a few black and purple wisps rising off the shoulders; on the last beat it snaps its eyes open and settles into a loose, low guard (the testbed keeps the stance).', [
     g(),
     g(an=band(-10, -40), af=band(-20, -50), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(15, -30), af=band(-35, -70), bob=(2, 2, 3), lean=(-1, -6), root=(-2, 0), **LOW),
     g(an=band(5, -40), af=band(-25, -60), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-35, -70), af=band(10, -30), bob=(2, 2, 3), lean=(1, 7), root=(2, 0), **LOW),
     g(an=band(-25, -60), af=band(0, -40), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(15, -30), af=band(-35, -70), bob=(2, 2, 3), lean=(-1, -6), root=(-2, 0), **LOW),
     g(an=band(5, -40), af=band(-25, -60), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-35, -70), af=band(10, -30), bob=(2, 2, 3), lean=(1, 7), root=(2, 0), **LOW),
     g(an=band(-40, -110), af=band(-50, -120), bob=(2, 2, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None],
  [0, 0, 1, 2, 1, 2, 1, 2, 1, 1, 0],
  dict(fps=8, auraColors=FIRE_AURA, rm='sways 2 px back and forward on the beat (net 0)',
       anchored={3: [('pflame2', 'head', -7, 10), ('flame2', 'head', 6, 12)], 4: [('pembers', 'head', -7, 1)], 5: [('flame2', 'head', -7, 11), ('pflame2', 'head', 6, 10)],
                 6: [('pembers', 'head', 6, 0)], 7: [('pflame2', 'head', -7, 10), ('flame2', 'head', 6, 12)], 8: [('pembers', 'head', -6, 0), ('embers', 'head', 6, 3)]})),
 'spotlight': ('Spotlight', 4,
  'Spotlight (Leo genjutsu, mental debuff: the caster projects its own inner radiance into the foe\'s mind\'s eye, Blind 1 round, INT save DC 12; range Zone of Awareness), v3 (Christopher 2026-10-27: lower the arms, the cone of light pours from the eyes; v3 lean forward a little): from the guard the fighter lets both arms drop to its sides, leans forward a little toward the target and fixes it; its eyes kindle gold, then blaze white-hot, and a cone of light pours out of the eyes toward the target, pale gold and widening, brighter at the core, growing over three frames and holding; the light dies back into the eyes and the fighter brings its hands back up into the guard (the target takes the genjutsu mark, genjutsuAfflicted, for the Blind).', [
     g(),
     g(an=band(-30, -60), af=band(-20, -45), bob=(1, 1, 1), lean=(1, 2)),
     *[g(an=band(-8, -15), af=band(4, -8), bob=(1, 1, 1), lean=(1, 4)) for _ in range(5)],
     g(an=band(-30, -60), af=band(-20, -45), bob=(0, 0, 1), lean=(0, 1)),
     g()],
  [None, None, 'squint', None, None, None, None, None, None],
  [0, 0, 1, 1, 1, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Blind ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       anchored={1: [('eyeGold', 'eye', 0, 0)], 2: [('eyeGold', 'eye', 0, 0)], 3: [('eyeGoldF', 'eye', 0, 0)],
                 4: [('eyeGoldF', 'eye', 0, 0)], 5: [('eyeGoldF', 'eye', 0, 0)], 6: [('eyeGold', 'eye', 0, 0)], 7: [('eyeGold', 'eye', 0, 0, {'alpha': {'Y': 140, 'W': 160}})]},
       cone={'from': 'eye', 3: (12, 1.0), 4: (20, 1.0), 5: (30, 1.0), 6: (30, 0.5)})),
 'kneel': ('Kneel', 4,
  'Kneel (Leo genjutsu, mental debuff: the caster projects its regal presence and imposes it on the foe\'s will, Stun 1 round, STR save DC 14; range Zone of Awareness): from the guard the fighter draws itself up tall, chin lifted, and raises the near hand high, palm out; its eyes kindle gold and an illusory crown of light forms over its head, the lion\'s mane of flame flaring behind it; then it brings the open palm down hard in front of it, palm to the floor, commanding the foe to kneel, the far fist at the hip, and heavy dome-shaped waves of golden pressure roll out toward the target, bearing down and sinking toward the floor as they travel; it holds the command, the crown blazing, then the crown and mane fade and it returns to the guard (the target takes the genjutsu mark, genjutsuAfflicted, for the Stun).', [
     g(),
     g(an=band(-110, -150, fistKind='palm'), af=band(-20, -70), bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-140, -170, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-100, -80, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-40, -110), af=band(-25, -90), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Stun ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       anchored={1: [('eyeGold', 'eye', 0, 0), ('crown1', 'head', 0, -7)],
                 2: [('eyeGold', 'eye', 0, 0), ('mane1', 'head', -1, 0, {'behind': True}), ('crown2', 'head', 0, -8)],
                 3: [('eyeGoldF', 'eye', 0, 0), ('mane3', 'head', -1, -1, {'behind': True}), ('crown2', 'head', 0, -8)],
                 4: [('eyeGoldF', 'eye', 0, 0), ('mane4', 'head', -1, -1, {'behind': True}), ('press1', 'feet', 14, -30), ('crown3', 'head', 0, -8)],
                 5: [('eyeGoldF', 'eye', 0, 0), ('mane3b', 'head', -1, -1, {'behind': True}), ('press2', 'feet', 19, -24), ('press1', 'feet', 14, -30), ('crown3', 'head', 0, -8)],
                 6: [('eyeGoldF', 'eye', 0, 0), ('mane3', 'head', -1, -1, {'behind': True}), ('press3', 'feet', 24, -17), ('press2', 'feet', 19, -24), ('crown3', 'head', 0, -8)],
                 7: [('eyeGold', 'eye', 0, 0), ('mane2', 'head', -1, 0, {'behind': True}), ('press3d', 'feet', 27, -10), ('crown2', 'head', 0, -8, {'alpha': {'Y': 170, 'O': 170, 'W': 200, 'R': 150}})],
                 8: [('crown1', 'head', 0, -7, {'alpha': {'Y': 110, 'O': 110, 'W': 140, 'R': 100}})]})),
}

def spec(state):
    U.CLIPS[state] = CLIPS[state]
    U.APPROVED[state] = APPROVED.get(state, STAT)
    U.spec(state)
    x = CLIPS[state][6]; s = load(D + state + '.json')
    for k, v in (x.get('extra') or {}).items(): s[k] = v
    if x.get('farLayer'): s['arms']['farLayer'] = True   # the far arm in its own far-arm sheet (Flowing Sand Parry v2: its hand is tracked for the sand trail)
    if x.get('shapes'): s['expressions']['shapes'].update(copy.deepcopy(x['shapes']))
    if x.get('front') or {'roar', 'strain'} & set(CLIPS[state][4]):   # roar/strain faces (S shapes used by the turn, E for all)
        s['expressions']['shapes']['roar'] = {'E': copy.deepcopy(s['expressions']['shapes']['pain']['E']),
            'S': [[0, 1, '#000000'], [1, 1, '#000000'], [5, 1, '#000000'], [6, 1, '#000000'], [2, 3, '#000000'], [3, 3, '#000000'], [4, 3, '#000000'], [2, 4, '#000000'], [3, 4, '#70241d'], [4, 4, '#000000']]}   # eyes squeezed, mouth open in a yell (mid-face, clear of the chin)
        s['expressions']['shapes']['strain'] = {'E': copy.deepcopy(s['expressions']['shapes']['pain']['E']),
            'S': [[0, 1, '#000000'], [1, 1, '#000000'], [5, 1, '#000000'], [6, 1, '#000000'], [2, 4, '#000000'], [3, 4, '#000000'], [4, 4, '#000000']]}   # eyes squeezed, teeth clenched
    if x.get('front'):   # the fighter turns to face S for part of the clip (Blast Wave v2): every facing plays the S frames there
        s['facingOverride'] = {'rule': 'Christopher 2026-10-27: the fighter turns to face S (toward the viewer) for these frames whatever its facing; every row holds the S frame there (the rows are copied after the render), then it turns back', 'frames': sorted(x['front']), 'to': 'S'}
    save(s, D + state + '.json')
    if x.get('front'):
        import universal_sn as USN
        USN.SN[state] = x['front']; USN.sn(state)

def fx(state):
    x = CLIPS[state][6]
    if x.get('invert'): invert(state, x['invert'])
    if CLIPS[state][5]: U.CLIPS[state] = CLIPS[state]; U.aura(state)
    if x.get('blur'):
        from PIL import Image
        import kastrikes
        f = D + state + '/fx.png'; old = Image.open(f).convert('RGBA') if os.path.exists(f) else None
        kastrikes.BLUR = x['blur']; kastrikes.blur(state)
        if x.get('trail'):
            b = Image.open(f).convert('RGBA'); px = b.load()
            for yy in range(b.size[1]):
                for xx in range(b.size[0]):
                    q = px[xx, yy]
                    if q[3] and q[:3] in x['trail']: px[xx, yy] = x['trail'][q[:3]] + (255,)
            b.save(f)
        if old: new = Image.open(f).convert('RGBA'); new.alpha_composite(old); new.save(f)
    if x.get('front'): face_front(state, sorted(x['front']))
    if x.get('front') and CLIPS[state][5]: U.aura(state)   # the aura again, round the turned (S) figure
    if x.get('burst'):
        if x.get('burstEvery'):   # the spiked aura drawn on each facing's own row (the fighter keeps its facing)
            for i, r_ in enumerate(load(D + state + '.json')['directions']): burst(state, x['burst'], row=r_, spread=False, clean=i == 0)
        else: burst(state, x['burst'])
    if x.get('tint'): flush(state, x['tint'], x.get('veins', ()), *x.get('tintColors', ()))
    if x.get('hairTo'): hair_to(state, x['hairTo'])
    if x.get('meteor'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        meteor(state, x['meteor'])
    if x.get('swirl') or x.get('impact') or x.get('blast'):
        from PIL import Image
        f = D + state + '/fx.png'
        if not os.path.exists(f) or 'fx' not in load(D + state + '.json'): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f)   # no splash fx: start clean (not a stale render)
        if x.get('swirl'): swirl(state, x['swirl'])
        if x.get('impact'): impact(state, x['impact'])
        if x.get('blast'): blast(state, x['blast'])
    if x.get('anchored'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_) or ('fx' not in load(D + state + '.json') and not CLIPS[state][5] and not x.get('keepFx')): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)   # clean start unless the aura was just drawn (keepFx: keep the arm swirl / impact drawn above; Sun Palm's approved render predates it)
        anchored(state, x['anchored'])
        if x.get('crystal'): crystalize(state, x['crystal'])
        if x.get('trails'): trails(state, x['trails'])
        if x.get('front'):   # turned frames: every row shows the E row's fx (drawn round the same S figure)
            fx_ = Image.open(f_).convert('RGBA'); dirs_ = load(D + state + '.json')['directions']; re_ = dirs_.index('E')
            for k in x['front']:
                cell = fx_.crop((k * 64, re_ * 64, k * 64 + 64, re_ * 64 + 64))
                for r_ in range(len(dirs_)):
                    if r_ != re_: fx_.paste(cell, (k * 64, r_ * 64))
            fx_.save(f_)
    if x.get('mask'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        mask(state, x['mask'], x.get('maskWaves'))
    if x.get('spinFire'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        spinFire(state, x['spinFire'])
    if x.get('kanaboRise'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        kanaboRise(state, x['kanaboRise'])
    if x.get('topFire'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_) or 'fx' not in load(D + state + '.json'): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        topFire(state, x['topFire'])
    if any(x.get(n) for n in ('rays', 'beam', 'cone', 'gather', 'nova', 'flare')):   # Leo sunlight fx, drawn over what is already there
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_) or ('fx' not in load(D + state + '.json') and not CLIPS[state][5] and not x.get('anchored')): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        for n in ('gather', 'nova', 'flare', 'rays', 'beam', 'cone'):
            if x.get(n): globals()[n](state, x[n])
    if x.get('ghosts'):
        from PIL import Image
        f = D + state + '/fx.png'; top = Image.open(f).convert('RGBA')   # blur + splash so far
        ghosts(state, x['ghosts'], x['ghostColors'])
        g_ = Image.open(f).convert('RGBA'); g_.alpha_composite(top); g_.save(f)   # streaks and flames stay over the afterimages
    if x.get('recolor'):   # fire-drawn helpers (swirl, impact) re-coloured for another element: {'#rrggbb': '#rrggbb'}
        from PIL import Image
        f_ = D + state + '/fx.png'; im = Image.open(f_).convert('RGBA'); px = im.load()
        m = {_hexc(a)[:3]: _hexc(b)[:3] for a, b in x['recolor'].items()}
        for yy in range(im.size[1]):
            for xx in range(im.size[0]):
                q = px[xx, yy]
                if q[3] and q[:3] in m: px[xx, yy] = m[q[:3]] + (q[3],)
        im.save(f_); print(state, 'recolor', len(m))

def invert(state, frames):
    """Spinning Top: the rig has no upside-down pose, so these frames are drawn upright (hands up by the head, legs down in
    a V) and every figure layer's cell is turned over (rotated 180 degrees: two quarter turns) after the render, the head
    set on the floor. A 180 turn also mirrors the facing, so each row takes the opposite row's cell (it then faces its own
    way); frames = {k: back} with back=1 taking its own row's cell instead (seen from behind mid-spin), or {k: (1, -90)}
    for a quarter turn (the dive onto the head and the roll back out: the body laid flat, head toward the facing, on the
    floor; W turns the other way). Runs once per render
    (a marker holds the turned body.png's hash)."""
    from PIL import Image
    import hashlib
    d = D + state + '/'; mk = d + '.inverted'
    h_ = lambda: hashlib.md5(open(d + 'body.png', 'rb').read()).hexdigest()
    if os.path.exists(mk) and open(mk).read() == h_(): return
    dirs = load(D + state + '.json')['directions']; body = Image.open(d + 'body.png').convert('RGBA')
    shift = {}
    for k, back in frames.items():
        for r in range(len(dirs)):
            back_, deg = back if isinstance(back, tuple) else (back, 180)
            if deg != 180 and dirs[r] == 'W': deg = -deg
            src = r if back_ else (len(dirs) - 1 - r if set(dirs) == {'E', 'W'} else r)
            b = body.crop((k * 64, src * 64, k * 64 + 64, src * 64 + 64)).rotate(deg); bb = b.getbbox()
            dx = 0 if deg == 180 else 32 - (bb[0] + bb[2]) // 2
            shift[k, r] = (src, deg, dx, 63 - bb[3] + 1)   # the lowest body row (the head's top when turned over) rests on row 63
    for f in os.listdir(d):
        if not f.endswith('.png') or f == 'fx.png': continue
        im = Image.open(d + f).convert('RGBA'); src_im = im.copy()
        for (k, r), (src, deg, dx, dy) in shift.items():
            cell = src_im.crop((k * 64, src * 64, k * 64 + 64, src * 64 + 64)).rotate(deg)
            out = Image.new('RGBA', (64, 64)); out.paste(cell, (dx, dy))
            im.paste(out, (k * 64, r * 64))
        im.save(d + f)
    open(mk, 'w').write(h_()); print(state, 'invert', sorted(frames))

def _arm(state, k, r, layer='arms.png'):
    from PIL import Image
    a = Image.open(D + state + '/' + layer).convert('RGBA').load()
    return [(x, y) for y in range(64) for x in range(64) if a[k * 64 + x, r * 64 + y][3]]

def swirl(state, frames):
    """Shatter Punch wind-up (Christopher 2026-10-27): fire swirling round the cocked arm. A tilted ellipse round the
    arm's pixels; a comet of flame runs round it, its head yellow, body orange, tail red, longer and doubled as the
    load builds; the half behind the arm hides behind the figure, the front half draws over it"""
    import math
    from PIL import Image
    f = D + state + '/fx.png'; fx = Image.open(f).convert('RGBA'); px = fx.load()
    lay = [Image.open(D + state + '/' + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png', 'far-arm.png') if os.path.exists(D + state + '/' + n)]
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    Y, O, R_ = hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    dirs = load(D + state + '.json')['directions']
    for k, (ph, st) in frames.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            pts = _arm(state, k, r)
            if not pts: continue
            cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
            rx = (max(x for x, _ in pts) - min(x for x, _ in pts)) / 2 + 3; ry = (max(y for _, y in pts) - min(y for _, y in pts)) / 2 + 3
            for ring, (dr, sweep) in enumerate(((0, 300 * st), (2, 200 * st))):
                if ring and st < 0.6: continue
                for t in range(int(sweep * 4)):
                    u = t / (sweep * 4)   # 0 tail .. 1 head
                    th = math.radians(ph + (180 if ring else 0) + t / 4)
                    x = round(cx + sg * (rx + dr) * math.cos(th)); y = round(cy + (ry * 0.7 + dr) * math.sin(th))
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    behind = math.sin(th) < 0
                    if behind and any(L[k * 64 + x, r * 64 + y][3] for L in lay): continue
                    if u < 0.35 and (x + y) % 2: continue   # dithered tail
                    px[k * 64 + x, r * 64 + y] = Y if u > 0.8 else O if u > 0.4 else R_
            # sparks thrown off the swirl
            for i in range(int(4 * st)):
                th = math.radians(ph + 90 * i + 45)
                x = round(cx + sg * (rx + 3) * math.cos(th)); y = round(cy + (ry * 0.7 + 3) * math.sin(th))
                if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, r * 64 + y] = Y
    fx.save(f); print(state, 'arm swirl', list(frames))

def impact(state, frames):
    """Shatter Punch contact (Christopher 2026-10-27: more dramatic): stage 0 a big white-hot flash star at the fist with
    jagged cracks; 1 a fire shock ring blasting out, cracks reaching further, shards; 2 the ring wider and broken,
    shards and embers scattering; 3 embers fading. All drawn on top at the fist (the arms layer's far tip)"""
    import math
    from PIL import Image
    f = D + state + '/fx.png'; fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    dirs = load(D + state + '.json')['directions']
    def put(k, r, x, y, c):
        if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, r * 64 + y] = c
    first = min(frames)
    for k, stage in frames.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            pts = _arm(state, first, r)
            tip = max(pts, key=lambda p: sg * p[0]); fx0, fy = tip[0] + sg * 2, tip[1]
            P = lambda dx, dy, c: put(k, r, fx0 + sg * dx, fy + dy, c)
            cracks = [(0, -1), (1, -2), (2, -1), (1, 1), (2, 2), (-1, 2), (-1, -2), (3, 0)]   # crack directions (x forward, y)
            if stage == 0:
                for i in range(-9, 10):   # the flash star: long horizontal and vertical spikes, shorter diagonals
                    c = W_ if abs(i) < 4 else Y if abs(i) < 7 else O if abs(i) < 9 else R_
                    P(i, 0, c); P(0, i, c); P(i, 1 if abs(i) < 5 else 0, c); P(1 if abs(i) < 5 else 0, i, c)
                    if abs(i) < 7: P(i, i, c if abs(i) < 3 else O); P(i, -i, c if abs(i) < 3 else O)
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if abs(dx) + abs(dy) < 5: P(dx, dy, W_ if abs(dx) + abs(dy) < 3 else Y)
            if stage in (1, 2):
                rad = (7, 11)[stage - 1]
                for t in range(0, 360, 4):   # the shock ring, an upright ellipse (seen side-on)
                    if stage == 2 and (t // 20) % 3 == 0: continue   # breaking up
                    th = math.radians(t)
                    P(round(rad * 0.55 * math.cos(th)), round(rad * 1.3 * math.sin(th)), O if stage == 1 else R_)
                    P(round((rad - 1) * 0.55 * math.cos(th)), round((rad - 1) * 1.3 * math.sin(th)), Y if stage == 1 else O)
                for dx, dy in cracks:   # jagged cracks shooting off
                    L = (8, 12)[stage - 1]
                    for i in range(2, L):
                        jx = (i % 3 == 0) * (1 if dy >= 0 else -1)
                        P(round(dx * i / 2) + jx, round(dy * i / 2), Y if i < L // 2 else O)
                for i, (dx, dy) in enumerate(cracks):   # shards flung out past the cracks
                    d = (11, 16)[stage - 1]
                    sx, sy = round(dx * d / 2), round(dy * d / 2)
                    P(sx, sy, O); P(sx + 1, sy + 1, R_)
                if stage == 1:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2): P(dx, dy, W_ if dx == dy == 0 else Y)
            if stage == 3:
                for i, (dx, dy) in enumerate(cracks):
                    if i % 2: continue
                    P(round(dx * 8), round(dy * 8) - 1, O); P(round(dx * 6) + 1, round(dy * 6) - 2, R_)
                P(-1, -6, Y); P(3, 5, O)
    fx.save(f); print(state, 'impact', frames)

def blast(state, frames):
    """Blast Wave (fire burst breaking the sound barrier): from the palms (the arms layer's far tip on the first frame) a
    cone of flame fans forward and sonic-boom arcs ')' ripple outward through it, each stage one arc further, the
    nearest white-hot, then yellow, orange, red; stage 3 leaves only the last broken arc and embers"""
    import math, random
    from PIL import Image
    f = D + state + '/fx.png'; fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    dirs = load(D + state + '.json')['directions']; first = min(frames)
    lay = [Image.open(D + state + '/' + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png', 'far-arm.png') if os.path.exists(D + state + '/' + n)]
    for k, stage in frames.items():
        rnd = random.Random(k)
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            pts = _arm(state, first, r); tip = max(pts, key=lambda p: sg * p[0]); x0, y0 = tip[0] + sg, tip[1]
            def P(dx, dy, c):
                x, y = x0 + sg * dx, y0 + dy
                if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, r * 64 + y] = c
            if stage < 3:   # the flame cone: dithered fire fanning out, hotter near the palms
                L = (7, 11, 13)[stage]
                for dx in range(0, L):
                    h = 1 + dx * 2 // 3
                    for dy in range(-h, h + 1):
                        if rnd.random() < (0.9 if dx < 3 else 0.55 - 0.03 * dx): P(dx, dy, ramp[min(3, (dx * 4) // (L + 1) + (abs(dy) > h - 1))])
            for j in range(stage + 1):   # the sonic boom: rings bursting out round the whole fighter, oldest widest
                rx = 9 + 8 * (stage - j); ry = round(rx * 0.75); c = ramp[min(3, stage - j + (stage == 3))]
                for t in range(0, 360, 2):
                    if (stage - j) >= 2 and (t // 12) % 3 == 0: continue   # the outer ring breaks up
                    th = math.radians(t); x = round(32 + rx * math.cos(th)); y = round(34 + ry * math.sin(th))
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    if math.sin(th) < 0 and any(L[k * 64 + x, r * 64 + y][3] for L in lay): continue   # far half behind the figure
                    px[k * 64 + x, r * 64 + y] = c
            if stage >= 2:
                for i in range(6): P(rnd.randint(4, 16), rnd.randint(-10, 10), (O, R_, Y)[i % 3])
    fx.save(f); print(state, 'blast', frames)

SKIN = {(0xf6, 0xa3, 0x5b), (0xc8, 0x78, 0x45), (0x9e, 0x4a, 0x31)}   # the rig's skin ramp (L, m, s)
def flush(state, tint, veins, col=(0xff, 0x3a, 0x1a), vcol=(0x7a, 0x14, 0x0c), streak=None, moss=None):   # col/vcol: tint and vein colours (Oak Flesh: bark brown, dark grain); streak: bark grain streak colour (Oak Flesh v3)
    """Inner Gate (Christopher 2026-10-27): the skin flushes red (a translucent red over every skin pixel, alpha per frame)
    and veins stand out on the forearms, upper arms, neck and temple (dark red broken lines, interior skin pixels only).
    Written as two extra layers so clothing, armour and hair still cover it: skin-fx.png (body + far arm skin, drawn just
    above body.png / far-arm.png) and arms-fx.png (near arm skin, drawn just above arms.png)"""
    from PIL import Image
    d = D + state + '/'
    dirs = load(D + state + '.json')['directions']
    for src, out in ((('body.png', 'far-arm.png'), 'skin-fx.png'), (('arms.png',), 'arms-fx.png')):
        lays = [Image.open(d + n).convert('RGBA') for n in src if os.path.exists(d + n)]
        if not lays: continue
        img = Image.new('RGBA', lays[0].size); px = img.load(); lays = [L.load() for L in lays]
        for k, al in tint.items():
            for fd in dirs:
                r = dirs.index(fd)
                skin = {(x, y) for L in lays for y in range(64) for x in range(64) if (q := L[k * 64 + x, r * 64 + y])[3] and q[:3] in SKIN}
                for (x, y) in skin: px[k * 64 + x, r * 64 + y] = tuple(col) + (al,)
                if streak:   # Oak Flesh v3 (Christopher 2026-10-28: read on the darkest skin tone): wavy vertical grain streaks over the bark, face clear
                    ty = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                    for (x, y) in skin:
                        if (x + y // 3) % 3 == 0: px[k * 64 + x, r * 64 + y] = tuple(streak) + (al,)   # v6: streaks run over the face too
                if moss:   # Oak Flesh v5 (Christopher 2026-10-28: all three colours combined): 2 px patches of moss on the bark, face clear
                    ty = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                    for (x, y) in skin:
                        if not (ty + 2 < y < ty + 11) and ((x // 2) * 5 + (y // 2) * 11) % 7 == 0: px[k * 64 + x, r * 64 + y] = tuple(moss) + (al,)
                if k not in veins or not skin: continue
                top_y = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                for (x, y) in skin:
                    if top_y + 2 < y < top_y + 11:   # head: a short vein at the temple only, the face stays clean
                        if y in (top_y + 3, top_y + 4) and (x + y) % 3 == 0 and (x - 1, y) in skin and (x + 1, y) in skin: px[k * 64 + x, r * 64 + y] = tuple(vcol) + (255,)
                        continue
                    across = ((x - 1, y) in skin and (x + 1, y) in skin and (x - 2, y) not in skin | {(x, y)}) or ((x, y - 1) in skin and (x, y + 1) in skin)
                    # a vein runs down the middle of each limb's cross-section (arms, neck), broken every few pixels
                    mid = (x - 1, y) in skin and (x + 1, y) in skin if (x, y - 1) in skin and (x, y + 1) in skin else (x, y - 1) in skin and (x, y + 1) in skin
                    if mid and (x * 3 + y) % 5 != 0: px[k * 64 + x, r * 64 + y] = tuple(vcol) + (255,)
        img.save(d + out)
    print(state, 'flush', list(tint), 'veins', list(veins))

HAIR_LAYERS = ('afro-hair', 'afro-puff', 'bantu-knots', 'braided-side', 'fade-hair', 'flat-top', 'locs-loose', 'locs-tied', 'long-hair', 'modern-topknot', 'ronin-ponytail')
def hair_to(state, spec):   # Oak Flesh v6 (Christopher 2026-10-28: change the hair to the moss): every hair style's base ramp swapped on the given frames
    from PIL import Image
    d = D + state + '/'; m = {_hexc(a)[:3]: _hexc(b)[:3] for a, b in spec['map'].items()}
    for n in HAIR_LAYERS:
        f = d + n + '.png'
        if not os.path.exists(f): continue
        im = Image.open(f).convert('RGBA'); px = im.load()
        for k in spec['frames']:
            for yy in range(im.size[1]):
                for xx in range(k * 64, k * 64 + 64):
                    q = px[xx, yy]
                    if q[3] and q[:3] in m: px[xx, yy] = m[q[:3]] + (q[3],)
        im.save(f)
    print(state, 'hair', spec['frames'])

def face_front(state, frames):
    """every row takes the S row's frame on the turned frames (all layers), so each facing turns to the viewer there"""
    from PIL import Image
    d = D + state + '/'; dirs = load(D + state + '.json')['directions']; rs = dirs.index('S')
    for n in sorted(os.listdir(d)):
        if not n.endswith('.png') or n == 'fx.png': continue
        im = Image.open(d + n).convert('RGBA')
        if im.height < 64 * len(dirs): continue
        for k in frames:
            cell = im.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
            for r in range(len(dirs)):
                if r != rs: im.paste(cell, (k * 64, r * 64))
        im.save(d + n)
    print(state, 'S frames on every row', frames)

def burst(state, frames, row='S', spread=True, clean=True):
    """Blast Wave v2 (facing S): embers gathering round the crouched fighter (stages 0-1), then the release: a spiked fire
    aura round the whole figure (inner yellow glow, flame spikes radiating out, longer at the release) and sonic-boom rings
    blasting out round it, white-hot, then yellow, orange, red as they widen and break up (stages 2-5). Drawn on the S row
    and copied to every row (all rows show the S frame there)"""
    import math, random
    from PIL import Image, ImageFilter
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']; rs = dirs.index(row)
    base = Image.open(d + 'body.png'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) and ('fx' in load(D + state + '.json') or not clean) else Image.new('RGBA', base.size)   # no splash fx: start clean
    if fx.size != base.size: n_ = Image.new('RGBA', base.size); n_.paste(fx, (0, 0)); fx = n_
    px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    lay = [Image.open(d + n).convert('RGBA') for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png', 'far-arm.png') if os.path.exists(d + n)]
    for k, st in frames.items():
        rnd = random.Random(k * 7)
        box = (k * 64, rs * 64, k * 64 + 64, rs * 64 + 64)
        m = Image.new('L', (64, 64))
        for L in lay: m.paste(255, (0, 0), L.crop(box).getchannel('A').point(lambda v: 255 if v else 0))
        fig = m.load(); pts = [(x, y) for y in range(64) for x in range(64) if fig[x, y]]
        cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
        def P(x, y, c, over=False):
            if 0 <= x < 64 and 0 <= y < 64 and (over or not fig[x, y]): px[box[0] + x, box[1] + y] = c
        if st <= 1:   # embers drawn in toward the fighter
            for i in range(10 + 6 * st):
                th = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(14, 24) - 5 * st
                P(round(cx + rr * math.cos(th)), round(cy + rr * 1.2 * math.sin(th)), (Y, O, R_)[i % 3])
            g1 = m.filter(ImageFilter.MaxFilter(3)).load()
            for (x, y) in [(x, y) for y in range(64) for x in range(64) if g1[x, y] and not fig[x, y]]:
                if (x + y + k) % 2 == 0 or st: P(x, y, O if st else R_)
            continue
        # spiked fire aura: glow rings, then flame spikes out of the silhouette
        grow = [m]
        for i in range(3): grow.append(grow[-1].filter(ImageFilter.MaxFilter(3)))
        G = [g.load() for g in grow]; wd = (3, 3, 2, 1)[st - 2]
        for y in range(64):
            for x in range(64):
                for i in range(1, wd + 1):
                    if G[i][x, y] and not G[i - 1][x, y]: P(x, y, (Y, O, R_)[min(2, i - 1)]); break
        L0 = (10, 8, 5, 3)[st - 2]
        for t in range(0, 360, 12):
            th = math.radians(t + (k * 5)); L = L0 + rnd.randint(-2, 3)
            # start at the silhouette edge in that direction
            r0 = 0
            while r0 < 40:
                x, y = round(cx + r0 * math.sin(th)), round(cy - r0 * math.cos(th))
                if not (0 <= x < 64 and 0 <= y < 64) or not fig[x, y]: break
                r0 += 1
            for i in range(L):
                u = i / L; w = 1 if u < 0.6 else 0
                x, y = cx + (r0 + i) * math.sin(th), cy - (r0 + i) * math.cos(th)
                c = Y if u < 0.35 else O if u < 0.7 else R_
                P(round(x), round(y), c)
                if w: P(round(x + math.cos(th)), round(y + math.sin(th)), c)
        # sonic-boom rings round the fighter
        for j in range(st - 1):
            age = st - 2 - j; rx = 12 + 9 * age; ry = round(rx * 0.8); c = ramp[min(3, age + (st == 5))]
            for t in range(0, 360, 2):
                if age >= 2 and (t // 12) % 3 == 0: continue
                th = math.radians(t)
                P(round(cx + rx * math.cos(th)), round(cy + 4 + ry * math.sin(th)), c)
        if st == 2:   # the white-hot release flash at the chest
            for i in range(-3, 4): P(round(cx) + i, round(cy) - 6, W_ if abs(i) < 2 else Y, over=False)
    for k in (frames if spread else ()):   # every row shows the S frame here
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(f); print(state, 'burst', frames)

def meteor(state, frames):
    """Meteor: a fireball forming above the raised hands ('form', radius), roiling (yellow core, orange body, red rim,
    flame licks off the top); then hurled ('fly', step): it streaks up and away toward the target's side of the sky with a
    tapering fire trail back to the hands, leaving embers ('trail')"""
    import math, random
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    def ball(k, r, cx, cy, rad, sg, rnd):
        for y in range(-rad - 3, rad + 1):
            for x in range(-rad - 1, rad + 2):
                dd = (x * x + y * y) ** 0.5
                X, Y_ = cx + sg * x, cy + y
                if not (0 <= X < 64 and 0 <= Y_ < 64): continue
                if dd <= rad:
                    c = W_ if dd < rad * 0.3 else Y if dd < rad * 0.6 else O if dd < rad - 0.8 else R_
                    if rad >= 4 and Y is c and rnd.random() < 0.2: c = O   # roiling
                    px[k * 64 + X, r * 64 + Y_] = c
                elif y < 0 and dd <= rad + 2 and rnd.random() < 0.35: px[k * 64 + X, r * 64 + Y_] = R_ if rnd.random() < 0.5 else O   # licks off the top
    for k, (kind, n) in frames.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1; rnd = random.Random(k * 13 + r)
            pts = _arm(state, 3, r); top = min(pts, key=lambda p: p[1]); hx = top[0]; hy = top[1]   # the raised palm (frame 3)
            if kind == 'form': ball(k, r, hx + sg, hy - min(n, 5) - 1, n, 1, rnd)   # big ones run off the top of the frame: too big for the sky
            elif kind == 'flash':   # the launch: the fireball at its biggest, lit white, light rays out from it
                ball(k, r, hx + sg * 3, hy - 6, 11, 1, rnd)
                for t in range(0, 360, 30):
                    th = math.radians(t)
                    for i in range(12, 20):
                        X, Y_ = round(hx + sg * 3 + i * math.cos(th)), round(hy - 6 + i * math.sin(th))
                        if 0 <= X < 64 and 0 <= Y_ < 64: px[k * 64 + X, r * 64 + Y_] = Y if i < 16 else O
            else:
                cx = hx + sg * (10 + 11 * n); cy = max(1, hy - 4 - 4 * n); rad = max(3, 9 - 2 * n)
                for t in range(0, 60):   # the trail back toward the hands, tapering
                    u = t / 60; tx = round(hx + sg * 4 + (cx - hx - sg * 4) * u); ty = round(hy + 4 + (cy - hy - 4) * u)
                    w = int(u * (5 if kind == 'fly' else 3))
                    for dy in range(-w, w + 1):
                        X, Y_ = tx, ty + dy
                        if 0 <= X < 64 and 0 <= Y_ < 64 and (kind != 'trail' or rnd.random() < 0.3) and rnd.random() < 0.4 + 0.5 * u:
                            px[k * 64 + X, r * 64 + Y_] = R_ if u < 0.4 else O if u < 0.75 else Y
                if kind == 'fly': ball(k, r, cx, cy, rad, sg, rnd)
                for i in range(8 + 6 * n):   # embers shed along the way, raining back down
                    X = hx + sg * rnd.randint(-6, 30); Y_ = rnd.randint(2, 20 + 10 * n)
                    if 0 <= X < 64: px[k * 64 + X, r * 64 + Y_] = (O, R_, Y)[i % 3]
    fx.save(f); print(state, 'meteor', list(frames))

def trails(state, t):   # Flowing Sand Parry v2: streams of sand following each open hand along its circle; t = {'near': frames, 'far': frames, 'len': n}
    """the hand of each arm (the arm pixel farthest from the chest) is found on every frame; on the listed frames a sand stream is
    drawn back along the hand's path through the last len frames (bent outward from the chest, so the stream follows the circle)"""
    from PIL import Image
    import random
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']; n = load(D + state + '.json')['frames']
    body = Image.open(d + 'body.png').convert('RGBA').load(); fx = Image.open(f).convert('RGBA'); px = fx.load()
    lay = {'near': Image.open(d + 'arms.png').convert('RGBA').load(), 'far': Image.open(d + 'far-arm.png').convert('RGBA').load()}
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    for r, fd in enumerate(dirs):
        if fd not in ('E', 'W'): continue
        for side in ('near', 'far'):
            tips = []
            for k in range(n):
                opq = [(x, y) for y in range(64) for x in range(64) if body[k * 64 + x, r * 64 + y][3]]
                top = min(y for _, y in opq); hx = sum(x for x, y in opq if y <= top + 9) / max(1, sum(1 for x, y in opq if y <= top + 9))
                chest = (hx, top + 17); L = lay[side]
                arm = [(x, y) for y in range(64) for x in range(64) if L[k * 64 + x, r * 64 + y][3]]
                tips.append((max(arm, key=lambda q: (q[0] - chest[0]) ** 2 + (q[1] - chest[1]) ** 2) if arm else None, chest))
            rnd = random.Random(r * 7 + (side == 'far'))
            for k in t[side]:
                pts = [tips[q] for q in range(max(0, k - t['len']), k + 1) if tips[q][0]]
                for i in range(len(pts) - 1):
                    (x0, y0), c0 = pts[i]; (x1, y1), _ = pts[i + 1]; age = len(pts) - 1 - i   # 1 = the newest stretch
                    a0 = math.atan2(y0 - c0[1], x0 - c0[0]); a1 = math.atan2(y1 - c0[1], x1 - c0[0])
                    if a1 - a0 > math.pi: a1 -= 2 * math.pi
                    if a0 - a1 > math.pi: a1 += 2 * math.pi
                    r0 = math.hypot(x0 - c0[0], y0 - c0[1]); r1 = math.hypot(x1 - c0[0], y1 - c0[1])
                    for u in range(13):
                        q = u / 12; a = a0 + (a1 - a0) * q; rr = r0 + (r1 - r0) * q
                        X = round(c0[0] + rr * math.cos(a)); Y = round(c0[1] + rr * math.sin(a))
                        if not (0 <= X < 64 and 0 <= Y < 64) or rnd.random() < 0.15 * age: continue
                        if any(L_[k * 64 + X, r * 64 + Y][3] for L_ in (body, lay['near'], lay['far'])) and side == 'far': continue   # the far arm's stream passes behind the body
                        ch = 'Z' if rnd.random() < 0.15 else 'S' if age == 1 else 's'
                        px[k * 64 + X, r * 64 + Y] = hexc(NPAL[ch], 255 if age == 1 else 200 if age == 2 else 150)
                        if age < 3:   # the newer stretches two pixels thick, the second one outward from the chest
                            X2 = round(c0[0] + (rr + 1) * math.cos(a)); Y2 = round(c0[1] + (rr + 1) * math.sin(a))
                            if (X2, Y2) != (X, Y) and 0 <= X2 < 64 and 0 <= Y2 < 64 and not (side == 'far' and any(L_[k * 64 + X2, r * 64 + Y2][3] for L_ in (body, lay['near'], lay['far']))): px[k * 64 + X2, r * 64 + Y2] = hexc(NPAL['s'], 210 if age == 1 else 160)
    fx.save(f); print(state, 'trails')

def crystalize(state, spec):   # Capricorn: crystal growing over the fighter. spec = {'shin': {frame: (pose, cover, alpha)}, 'arm': {frame: (cover, alpha)}}
    """shin: the near (kicking) leg's pixels within 2.5 px of its knee -> ankle line (AS_SEG, E coords, mirrored for W),
    covered from the ankle up by cover (0-1); arm: the near arm's skin (arms.png), covered from the hand (furthest from the shoulder) back.
    Crystal: teal body C, glint c facet lines, deep teal T on the edges and every fifth diagonal (the gem's shaded facets)"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    px = fx.load(); lays = [Image.open(d + n).convert('RGBA').load() for n in ('body.png', 'male-gi.png') if os.path.exists(d + n)]
    ap = Image.open(d + 'arms.png').convert('RGBA').load()
    C_, c_, T_ = _hexc(NPAL['C'])[:3], _hexc(NPAL['c'])[:3], _hexc(NPAL['T'])[:3]
    def paint(pts, al, k, r):
        for (x, y) in pts:
            edge = any((x + a, y + b) not in pts for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            col = T_ if edge or (x - y) % 5 == 0 else c_ if (x + y) % 4 == 0 else C_
            px[k * 64 + x, r * 64 + y] = col + (al,)
    for k, (pose, cov, al) in (spec.get('shin') or {}).items():
        (kx, ky), (ax_, ay_) = AS_SEG[pose]
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'
            pts = set()
            for y in range(64):
                for x in range(64):
                    if not any(L[k * 64 + x, r * 64 + y][3] for L in lays): continue
                    ex = 63 - x if flip else x
                    vx, vy = ax_ - kx, ay_ - ky; L2 = vx * vx + vy * vy
                    t = max(0, min(1.25, ((ex - kx) * vx + (y - ky) * vy) / L2))
                    if math.hypot(ex - (kx + t * vx), y - (ky + t * vy)) <= 2.5 and t >= 1 - cov: pts.add((x, y))
            paint(pts, al, k, r)
    for k, (cov, al) in (spec.get('arm') or {}).items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'
            arm = [(x, y) for y in range(64) for x in range(64) if ap[k * 64 + x, r * 64 + y][3]]
            if not arm: continue
            sh = min(arm, key=lambda q: abs(q[1] - 22) * 4 + abs(q[0] - 32))   # the shoulder: crystal grows from the hand (the skin furthest from it) back
            skin = [(x, y) for (x, y) in arm if ap[k * 64 + x, r * 64 + y][:3] in SKIN]
            skin.sort(key=lambda q: -math.hypot(q[0] - sh[0], q[1] - sh[1]))
            paint(set(skin[:round(len(skin) * cov)]), al, k, r)
    fx.save(f); print(state, 'crystalize', sorted(spec.get('shin') or {}), sorted(spec.get('arm') or {}))

def anchored(state, frames):
    """Splash fx placed on the fighter itself, so they ride every pose and root step: frames = {frame: [(pattern, anchor,
    dx, dy, opts)]}; anchor 'head' (centre of the head found in body.png), 'hand' (tip of the near arm, the arms layer's
    most forward pixel), 'farhand' (the same on the far arm), 'feet' (floor under the body); dx is toward the facing (mirrored for W, pattern flipped);
    the pattern is centred on the anchor; opts: 'behind' (only where the fighter is not drawn), {'alpha': {letter: a}}"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    lays = [Image.open(d + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'far-arm.png', 'male-gi.png', 'fade-hair.png') if os.path.exists(d + n)]
    px = fx.load(); bp = lays[0]; ap = Image.open(d + 'arms.png').convert('RGBA').load()
    fp = Image.open(d + 'far-arm.png').convert('RGBA').load() if os.path.exists(d + 'far-arm.png') else None
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    for k, items in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1
            opq = [(x, y) for y in range(64) for x in range(64) if bp[k * 64 + x, r * 64 + y][3]]
            top = min(y for _, y in opq); head = [x for x, y in opq if y <= top + 9]
            arm = [(x, y) for y in range(64) for x in range(64) if ap[k * 64 + x, r * 64 + y][3]]
            tip = (max if not flip else min)(arm, key=lambda q: (q[0], -q[1])) if arm else ((max(head), top + 8))
            farm = [(x, y) for y in range(64) for x in range(64) if fp and fp[k * 64 + x, r * 64 + y][3]]   # the far arm's most forward pixel (Wither Palm: the far palm's strikes)
            ftip = (max if not flip else min)(farm, key=lambda q: (q[0], -q[1])) if farm else tip
            anchors = {'head': ((min(head) + max(head)) / 2, top + 6), 'hand': tip, 'farhand': ftip, 'feet': ((min(x for x, _ in opq) + max(x for x, _ in opq)) / 2, 63), 'eye': _eye(state, k, r) or (max(head) - 2 if not flip else min(head) + 2, top + 5)}
            for item in items:
                name, an, dx, dy = item[:4]; opts = item[4] if len(item) > 4 else {}
                pat = NPAT[name]; h, w = len(pat), len(pat[0]); ax, ay = anchors[an]
                x0 = round(ax + sg * dx - (w - 1) / 2); y0 = round(ay + dy - (h - 1) / 2)
                for yy, row in enumerate(pat):
                    for xx, ch in enumerate(row[::-1] if flip else row):
                        if ch == '.': continue
                        X, Y = x0 + xx, y0 + yy
                        if not (0 <= X < 64 and 0 <= Y < 64): continue
                        if opts.get('behind') and any(L[k * 64 + X, r * 64 + Y][3] for L in lays): continue
                        px[k * 64 + X, r * 64 + Y] = hexc(NPAL[ch], opts.get('alpha', {}).get(ch, 255))
    fx.save(f); print(state, 'anchored', list(frames))

def mask(state, frames, waves=None):
    """Killing Intent v3 (Christopher 2026-10-27): an illusory demon mask appears over the caster's head, in profile matching
    its facing ('faint' outline only, 'full' translucent fill, 'flare' eye and fangs blazing, 'flicker' breaking up); placed
    from the head found in body.png each frame so it rides the lunge; the killing-intent waves roll out from the mask's mouth"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    px = fx.load(); bp = body.load()
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    def stamp(k, r, pat, x0, y0, flip, recol=None, alpha=None, skip=None):
        for yy, row in enumerate(pat):
            if skip and yy % 2 == skip - 1: continue
            for xx, ch in enumerate(row[::-1] if flip else row):
                if ch == '.': continue
                ch = (recol or {}).get(ch, ch)
                if ch == '.': continue
                X, Y = x0 + xx, y0 + yy
                if 0 <= X < 64 and 0 <= Y < 64: px[k * 64 + X, r * 64 + Y] = hexc(NPAL[ch], (alpha or {}).get(ch, 255))
    for k, stage in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            opq = [(x, y) for y in range(64) for x in range(64) if bp[k * 64 + x, r * 64 + y][3]]
            if not opq: continue
            top = min(y for _, y in opq); head = [x for x, y in opq if y <= top + 9]; L, R_ = min(head), max(head)
            flip = fd == 'W'; x0 = R_ + 3 - 17 if flip else L - 3; y0 = top - 4
            pat = NPAT['oniMask']
            if stage == 'faint': stamp(k, r, pat, x0, y0, flip, recol={'m': '.', 'M': '.', 'Y': '.', 'W': '.'}, alpha={'R': 150})
            elif stage == 'flicker': stamp(k, r, pat, x0, y0, flip, alpha={'m': 110, 'R': 170}, skip=1)
            else: stamp(k, r, pat, x0, y0, flip, alpha={'m': 175}, recol={'R': 'O', 'Y': 'W'} if stage == 'flare' else None)   # translucent fill: an illusion, the face shows faintly through
            for name, dx, dy in (waves or {}).get(k, ()):   # waves anchored at the mask's snout, bottom-left like nfx
                w = NPAT[name]; wx = (L - 3 + 18 + dx) if not flip else (R_ + 3 - 17 - dx - len(w[0]))
                stamp(k, r, w, wx, top + 9 + dy - len(w) + 1, flip)
    fx.save(f); print(state, 'mask', list(frames))

def ghosts(state, offs, cols):
    """after the blur: afterimages (Christopher 2026-10-27: onion/afterimage effects to exaggerate the speed). On each
    dash frame the figure's own silhouette is stamped again 4-18 px behind it on the fx layer, nearest first: an edge of
    solid colour with a dithered fill, fading out (orange/yellow, then red/orange, then a bare red edge); drawn only where
    the figure itself is not, so the real fighter stays on top"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'
    lay = [Image.open(d + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'far-arm.png', 'male-gi.png', 'fade-hair.png') if os.path.exists(d + n)]
    fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    dirs = load(D + state + '.json')['directions']
    for k, os_ in offs.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            fig = {(x, y) for y in range(64) for x in range(64) if any(a[k * 64 + x, r * 64 + y][3] for a in lay)}
            for i, o in sorted(enumerate(os_), key=lambda t: -t[0]):   # farthest first, nearest drawn over it
                edge, fill = cols[min(i, len(cols) - 1)]
                for (x, y) in fig:
                    X = x - sg * o
                    if not (0 <= X < 64) or (X, y) in fig: continue
                    rim = any((x + dx, y + dy) not in fig for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if rim: px[k * 64 + X, r * 64 + y] = hexc(edge)
                    elif fill and (X + y) % 2 == 0: px[k * 64 + X, r * 64 + y] = hexc(fill)
    fx.save(f); print(state, 'afterimages', offs)

def _eye(state, k, r):   # centre of the eye pixels (brown-eyes layer) in one cell
    from PIL import Image
    f = D + state + '/brown-eyes.png'
    if not os.path.exists(f): return None
    e = Image.open(f).convert('RGBA').load(); pts = [(x, y) for y in range(64) for x in range(64) if e[k * 64 + x, r * 64 + y][3]]
    return (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)) if pts else None

# ---- Leo ninjutsu / genjutsu (sunlight: white-hot core, gold, orange, red rim) ----
FIG_LAYERS = ('body.png', 'arms.png', 'far-arm.png', 'male-gi.png', 'fade-hair.png')
def _hexc(c, a=255): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def _open_fx(state, aura=False):   # the fx layer drawn so far this pass (fx() starts it clean when nothing else drew)
    from PIL import Image
    d = D + state + '/'; size = Image.open(d + 'body.png').size; fx = Image.open(d + 'fx.png').convert('RGBA')
    if fx.size != size: n_ = Image.new('RGBA', size); n_.paste(fx, (0, 0)); fx = n_
    return fx
def _fig(state, k, r):   # the figure's opaque pixels in one cell
    from PIL import Image
    d = D + state + '/'; lays = [Image.open(d + n).convert('RGBA').load() for n in FIG_LAYERS if os.path.exists(d + n)]
    return {(x, y) for y in range(64) for x in range(64) if any(L[k * 64 + x, r * 64 + y][3] for L in lays)}
def _tip(state, k, r, flip):   # the near hand: the arms layer's most forward pixel
    pts = _arm(state, k, r)
    return (min if flip else max)(pts, key=lambda q: (q[0], -q[1])) if pts else None

def rays(state, frames, aura=False):
    """Radiance: rays of sunlight bursting from the whole body, long and short in turn, turning slowly (frames = {k: (length, phase deg)});
    each ray starts a pixel off the silhouette edge, white at the root, then gold, orange, a red tip; drawn only outside the figure"""
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    W_, Y, O, R_ = (255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O']), _hexc(ELEMENT['R'])
    for k, (L0, ph) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); cx = sum(x for x, _ in fig) / len(fig); cy = sum(y for _, y in fig) / len(fig) - 4
            for i in range(16):
                th = math.radians(ph + 22.5 * i); L = L0 if i % 2 == 0 else max(2, L0 * 3 // 5)
                r0 = 0
                while r0 < 40 and (round(cx + r0 * math.cos(th)), round(cy - r0 * math.sin(th))) in fig: r0 += 1
                for j in range(L):
                    u = j / max(1, L - 1); c = W_ if u < 0.2 else Y if u < 0.55 else O if u < 0.85 else R_
                    for w in ((0, 0.6) if i % 2 == 0 and u < 0.6 else (0,)):   # the long rays are two pixels thick at the root
                        x = round(cx + (r0 + 2 + j) * math.cos(th) - w * math.sin(th)); y = round(cy - (r0 + 2 + j) * math.sin(th) * 1.1 - w * math.cos(th))
                        if 0 <= x < 64 and 0 <= y < 64 and (x, y) not in fig: px[k * 64 + x, r * 64 + y] = c
    fx.save(D + state + '/fx.png'); print(state, 'rays', list(frames))

def flare(state, frames, aura=False):
    """Radiance v3 (Christopher 2026-10-27, power-up reference): facing S, a towering aura of light erupting from the ground round
    the fighter (frames = {k: stage 0-3}): a glow hugging the body, white at the core, pale gold, gold, then tall jagged spikes
    fanning up and out with orange tips, longest straight up, and a ring of light flaring on the floor at the feet; drawn
    only outside the figure on the S row, then copied to every row (all rows show the S frame there)"""
    import random
    from PIL import ImageFilter, Image
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    W_, P_, Y, O = (255, 255, 255, 255), (255, 243, 176, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O'])
    every = isinstance(frames, dict) and frames.get('every')   # v4 (E-facing): drawn round each row's own figure, no turn
    if every: frames = {k: v for k, v in frames.items() if k != 'every'}
    for k, st, rs in [(k, st, r_) for k, st in frames.items() for r_ in (range(len(dirs)) if every else [dirs.index('S')])]:
        fig = _fig(state, k, rs); rnd = random.Random(k * 23)
        m = Image.new('L', (64, 64)); mp = m.load()
        for (x, y) in fig: mp[x, y] = 255
        cx = sum(x for x, _ in fig) / len(fig); top = min(y for _, y in fig); foot = max(y for _, y in fig)
        def P(x, y, c):
            x, y = round(x), round(y)
            if 0 <= x < 64 and 0 <= y < 64 and (x, y) not in fig: px[k * 64 + x, rs * 64 + y] = c
        g = [m]
        for i in range(4): g.append(g[-1].filter(ImageFilter.MaxFilter(3)))
        G = [q.load() for q in g]; wd = (1, 2, 3, 4)[st]
        if st >= 2:   # v3: the aura's body, a translucent mass of pale light filling round the fighter under the spikes
            vol = m.filter(ImageFilter.MaxFilter((0, 0, 9, 13)[st])).filter(ImageFilter.MaxFilter(5)).load()
            for y in range(64):
                for x in range(64):
                    if vol[x, y] and y < 62: P(x, y, (255, 246, 200, 150) if (x + y + k) % 3 else (255, 225, 77, 170))
        for y in range(64):   # the glow hugging the body: white, pale gold, gold, orange outward
            for x in range(64):
                for i in range(1, wd + 1):
                    if G[i][x, y] and not G[i - 1][x, y]: P(x, y, (W_, P_, Y, O)[min(3, i - 1 + (st < 2))]); break
        if st >= 1:   # the spikes: rays from the feet, each starting where it leaves the glow, fanning up and out, longest straight up
            L0 = (0, 8, 14, 17)[st]; ox, oy = cx, foot - 14; edge = G[min(wd, 4)] if st < 2 else vol
            for t in range(-100, 101, 4):
                a = math.radians(t + rnd.uniform(-1.5, 1.5)); ddx, ddy = math.sin(a), -math.cos(a) * 1.3
                d = 90   # from far outside, walk in toward the hips until the glow is hit: the spike roots there
                while d > 0:
                    xs, ys = ox + d * ddx, oy + d * ddy
                    if 0 <= round(xs) < 64 and 0 <= round(ys) < 64 and edge[round(xs), round(ys)]: break
                    d -= 0.5
                L = L0 * (0.55 + 0.45 * math.cos(a)) + rnd.randint(-3, 4) + (3 if abs(t) > 75 else 0)
                n = math.hypot(ddx, ddy); ux, uy = ddx / n, ddy / n
                for j in range(1, int(L)):
                    u = j / max(1, L - 1)
                    x, y = xs + j * ux, ys + j * uy
                    c = W_ if u < 0.25 else P_ if u < 0.5 else Y if u < 0.78 else O
                    P(x, y, c)
                    if u < 0.5: P(x - uy, y + ux, c)
            rx = (0, 16, 24, 26)[st]   # the ring of light flaring on the floor
            for tt in range(0, 360, 3):
                th = math.radians(tt); x, y = cx + rx * math.cos(th), 62 + 2 * math.sin(th)
                P(x, y, Y if math.sin(th) > 0 else O)
                if tt % 9 == 0: P(x, y - 1, P_)
        if every: continue
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(D + state + '/fx.png'); print(state, 'flare', list(frames))

def beam(state, frames, aura=False):
    """Solar Lance: a beam of solar fire from the near fingertips to the edge of the cell (frames = {k: (half-height, 'fire'|'fade')}):
    white-hot core, gold, orange, red rim; the rim flickers; 'fade' breaks it up into embers"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    ramp = [(255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O']), _hexc(ELEMENT['R'])]
    for k, (w, kind) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1; rnd = random.Random(k * 31 + r)
            tip = _tip(state, k, r, flip)
            if not tip: continue
            x0, y0 = tip[0] + sg * 2, tip[1]
            for i in range(64):
                x = x0 + sg * i
                if not 0 <= x < 64: break
                ww = min(w, 1 + i // 2)   # the beam flares out of the fingers over the first few pixels
                for dy in range(-ww, ww + 1):
                    lvl = min(3, round(abs(dy) * 3 / max(1, ww)))
                    if abs(dy) == ww and rnd.random() < 0.3: continue   # flickering rim
                    if kind == 'fade':
                        if rnd.random() < 0.55: continue
                        lvl = min(3, lvl + 1)
                    y = y0 + dy
                    if 0 <= y < 64: px[k * 64 + x, r * 64 + y] = ramp[lvl]
                if kind == 'fire' and i > 2 and rnd.random() < 0.35:   # sparks spitting off the beam's edges
                    y = y0 + rnd.choice((-1, 1)) * (ww + rnd.randint(2, 4))
                    if 0 <= y < 64: px[k * 64 + x, r * 64 + y] = ramp[rnd.randint(1, 2)]
    fx.save(D + state + '/fx.png'); print(state, 'beam', list(frames))

def cone(state, frames, aura=False):
    """Spotlight: a cone of pale gold light pouring from the open palm (v2: from the eyes) toward the target (frames = {k: (length, strength)}),
    widening as it goes, a bright core line near the palm, dithered and translucent so the scene shows through"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    src = frames.get('from', 'hand'); frames = {k: v for k, v in frames.items() if k != 'from'}   # v2: 'eye' pours it from the eyes
    for k, (L, st) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1; rnd = random.Random(k * 17 + r)
            tip = _eye(state, k, r) if src == 'eye' else _tip(state, k, r, flip)
            if not tip: continue
            x0, y0 = round(tip[0]) + sg * 2, round(tip[1])
            for i in range(L):
                x = x0 + sg * i
                if not 0 <= x < 64: break
                h = 1 + i * 0.5
                for dy in range(-round(h), round(h) + 1):
                    y = y0 + dy
                    if not 0 <= y < 64: continue
                    q = abs(dy) / max(1, h)
                    if q > 0.85: c = _hexc(ELEMENT['O'], round(200 * st))                          # the cone's edge
                    elif i < 8 and q < 0.3: c = _hexc('#ffffff', round(230 * st))                   # hot core line near the palm
                    elif (x + y) % 2 == 0 or q < 0.4: c = _hexc(ELEMENT['Y'], round((150 if q < 0.4 else 110) * st))
                    else: continue
                    if i > L - 4 and rnd.random() < 0.5: continue   # ragged leading edge
                    px[k * 64 + x, r * 64 + y] = c
    fx.save(D + state + '/fx.png'); print(state, 'cone', list(frames))

def gather(state, frames, aura=False):
    """Supernova wind-up: motes of light streaming in toward the fighter from all round, closing in and thickening by stage (0-3)"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    cols = [(255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O'])]
    for k, st in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); cx = sum(x for x, _ in fig) / len(fig); cy = sum(y for _, y in fig) / len(fig)
            rnd = random.Random(k * 11 + r)
            for i in range(16 + 6 * st):
                th = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(15, 27) - 3 * st
                x, y = cx + rr * math.cos(th), cy + rr * 1.15 * math.sin(th)
                for j in range(3):   # a short streak pointing in toward the fighter, bright head inward
                    X, Y_ = round(x - j * math.cos(th)), round(y - j * 1.15 * math.sin(th))
                    if 0 <= X < 64 and 0 <= Y_ < 64 and (X, Y_) not in fig: px[k * 64 + X, r * 64 + Y_] = cols[min(2, 2 - j + (j == 0 and st < 2))]
    fx.save(D + state + '/fx.png'); print(state, 'gather', list(frames))

def spinFire(state, frames):
    """Leash Kick: a ring of fire whirling round the legs through the pirouette (frames = {k: (start, end degrees swept, stage 0-3)}):
    a flat ellipse at knee-to-hip height swept further each frame, thicker each turn (stage 2 doubled), black and purple
    licks flickering in it every few degrees (Sagittarius); its far half hides behind the figure; stage 3 breaks up as the kick fires"""
    from PIL import Image
    f_ = D + state + '/fx.png'; fx = Image.open(f_).convert('RGBA'); px = fx.load(); dirs = load(D + state + '.json')['directions']
    Y, O, R_, P, K = (_hexc(ELEMENT[c]) for c in 'YORPK')
    for k, (a0, a1, st) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); sg = -1 if fd == 'W' else 1
            cx = sum(x for x, _ in fig) / len(fig); cy = 46
            rx, ry = 13 + 2 * min(st, 2), 4 + (st >= 2)
            for ring in range(1 + (st >= 1) + (st >= 2)):
                for t in range(a0 * 2, a1 * 2):
                    th = math.radians(t / 2); x = round(cx + sg * (rx + ring) * math.cos(th)); y = round(cy + (ry + ring) * math.sin(th) - ring)
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    if st == 3 and (x + y + t) % 3: continue
                    if math.sin(th) < 0 and (x, y) in fig: continue
                    deg = t // 2; c = (Y, O, R_)[ring] if ring < 3 else R_
                    if deg % 40 < 6: c = P if ring == 0 else K   # Sagittarius: purple and black licks in the ring
                    px[k * 64 + x, r * 64 + y] = c
                    if deg % 30 == 0 and st >= 1 and y - 2 >= 0: px[k * 64 + x, r * 64 + y - 1] = O; px[k * 64 + x, r * 64 + y - 2] = R_ if deg % 60 else P   # tongues of flame licking up
    fx.save(f_); print(state, 'spinFire', list(frames))

def topFire(state, frames):
    """Spinning Top (turned over, spinning on the head): frames = {k: stage} (0 entry / exit embers, 1 a ring half swept,
    2 the full whirl). The feet are the highest figure pixels (one per side of the V when it is open); flames burst off
    each foot (alternating shapes so they flicker, a black/purple flame every other frame), a flat ring of fire whirls
    round the legs at foot height (yellow, orange, red rings with purple and black licks, its far half behind the legs,
    the swept part advancing each frame), and sparks scatter on the floor round the head"""
    from PIL import Image
    f_ = D + state + '/fx.png'; fx = Image.open(f_).convert('RGBA'); px = fx.load(); dirs = load(D + state + '.json')['directions']
    Y, O, R_, P, K = (_hexc(ELEMENT[c]) for c in 'YORPK')
    def stamp(k, r, name, cx, cy, flip):
        pat = NPAT[name]; h, w = len(pat), len(pat[0]); x0, y0 = round(cx - (w - 1) / 2), round(cy - (h - 1) / 2)
        for yy, row in enumerate(pat):
            for xx, ch in enumerate(row[::-1] if flip else row):
                X, Y_ = x0 + xx, y0 + yy
                if ch != '.' and 0 <= X < 64 and 0 <= Y_ < 64: px[k * 64 + X, r * 64 + Y_] = _hexc(NPAL[ch])
    for k, st in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); flip = fd == 'W'; sg = -1 if flip else 1
            cx = (min(x for x, _ in fig) + max(x for x, _ in fig)) / 2; top = min(y for _, y in fig)
            l = [q for q in fig if q[0] < cx - 4]; rr = [q for q in fig if q[0] > cx + 4]
            wide = l and rr and min(y for _, y in l) < top + 4 and min(y for _, y in rr) < top + 4
            feet = [min(l, key=lambda q: q[1]), min(rr, key=lambda q: q[1])] if wide else [min(fig, key=lambda q: q[1])]
            if st == 0:
                for fx_, fy in feet: stamp(k, r, 'embers', fx_, fy - 2, flip)
                stamp(k, r, 'embers', cx - 7, 60, flip); continue
            cy = top + 5; rx, ry = (17 if wide else 12), 3
            sweep = 200 if st == 1 else 360; a0 = (k * 97) % 360
            for ring in range(3):
                for t in range(sweep * 2):
                    th = math.radians(a0 + t / 2); x = round(cx + sg * (rx + ring) * math.cos(th)); y = round(cy + (ry + ring) * math.sin(th) - ring)
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    if math.sin(th) < 0 and (x, y) in fig: continue
                    if st == 1 and t < sweep and (x + y + t) % 2: continue   # the tail of a part-swept ring breaks up
                    deg = int(a0 + t / 2); c = (Y, O, R_)[ring]
                    if deg % 45 < 6: c = P if ring == 0 else K
                    px[k * 64 + x, r * 64 + y] = c
                    if deg % 36 == 0 and y - 2 >= 0: px[k * 64 + x, r * 64 + y - 1] = O; px[k * 64 + x, r * 64 + y - 2] = R_ if deg % 72 else P   # tongues licking up off the ring
            for i, (fx_, fy) in enumerate(feet):
                stamp(k, r, ('flame3', 'flame2')[(k + i) % 2] if (k + i) % 3 else 'pflame2', fx_, fy - 3, flip)
            stamp(k, r, 'embers' if k % 2 else 'pembers', cx + 8, 60, flip); stamp(k, r, 'pembers' if k % 2 else 'embers', cx - 8, 60, flip)   # sparks on the floor round the head
    fx.save(f_); print(state, 'topFire', list(frames))

def kanaboRise(state, frames):
    """Ironwood Kanabo v2 (Christopher 2026-10-28: the club rises from the earth): frames = {k: rows} the club's height
    above the floor, head first, out of a crack in front of the fighter (only the part above row 62 shows), or
    {k: 'grip'} the whole club with its grip in the near fist (the arms layer's foremost pixel)"""
    from PIL import Image
    f_ = D + state + '/fx.png'; fx = Image.open(f_).convert('RGBA'); px = fx.load(); dirs = load(D + state + '.json')['directions']
    pat = NPAT['kanabo']; H, Wd = len(pat), len(pat[0]); GRIP = 26   # pattern row held in the fist
    for k, v in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1
            fig = _fig(state, k, r); cx = (min(x for x, _ in fig) + max(x for x, _ in fig)) / 2
            if v == 'grip':
                tip = _tip(state, k, r, flip); x0 = tip[0] - Wd // 2 - sg; y0 = tip[1] - GRIP; floor = 63
            else:
                x0 = round(cx + sg * 13 - Wd / 2); y0 = 63 - v; floor = 62
            for yy, row in enumerate(pat):
                for xx, ch in enumerate(row[::-1] if flip else row):
                    X, Y_ = x0 + xx, y0 + yy
                    if ch != '.' and 0 <= X < 64 and 0 <= Y_ <= floor: px[k * 64 + X, r * 64 + Y_] = _hexc(NPAL[ch])
    fx.save(f_); print(state, 'kanaboRise', frames)

def nova(state, frames, aura=False):
    """Supernova release, facing S (every row shows the S frame here): 'core' a star kindling at the chest and the body glowing;
    'flash' a white flash swallowing the fighter and the whole cell; stages 0-4 the rings of light blasting out (white, gold,
    orange, red as they widen and break up), sun rays scattering and the glow draining off the body, embers raining down"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']; rs = dirs.index('S')
    W_, Y, O, R_ = (255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O']), _hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    for k, st in frames.items():
        fig = _fig(state, k, rs); cx = sum(x for x, _ in fig) / len(fig); cy = sum(y for _, y in fig) / len(fig) - 10   # the heart
        rnd = random.Random(k * 5)
        def P(x, y, c, over=False):
            x, y = round(x), round(y)
            if 0 <= x < 64 and 0 <= y < 64 and (over or (x, y) not in fig): px[k * 64 + x, rs * 64 + y] = c
        glow = {'core': 90, 'core2': 140, 'flash': 215, 'flash2': 235, 0: 150, 1: 100, 2: 60, 3: 30, 4: 0}[st]
        for (x, y) in fig:   # the body glowing white-gold (blinding at the flash)
            if glow: P(x, y, (255, 250, 220, glow), over=True)
        if st in ('core', 'core2'):   # v2: core2 the star swollen and blazing, rays flickering off it
            n_ = 5 if st == 'core' else 8
            for i in range(-n_, n_ + 1):
                c = W_ if abs(i) < 2 + (st == 'core2') else Y if abs(i) < n_ - 1 else O
                P(cx + i, cy, c, True); P(cx, cy + i, c, True)
                if abs(i) < n_ // 2 + 1: P(cx + i, cy + i, Y, True); P(cx + i, cy - i, Y, True)
            if st == 'core2':
                for i in range(8):
                    th = math.radians(i * 45 + 22); 
                    for d in range(10, 14): P(cx + d * math.cos(th), cy + d * math.sin(th), Y if d < 12 else O)
        elif st in ('flash', 'flash2'):   # v2: flash2 the flash pulsing bigger on the held apex
            sc = 1.0 if st == 'flash' else 1.2
            for y in range(64):
                for x in range(64):
                    dd = math.hypot(x - cx, (y - cy) * 0.9) / sc
                    if dd < 14: c = (255, 255, 255, 255)
                    elif dd < 24: c = (255, 245, 190, 235)
                    elif dd < 34: c = _hexc(ELEMENT['Y'], 190)
                    elif dd < 42: c = _hexc(ELEMENT['O'], 140 if (x + y) % 2 == 0 else 0)
                    else: continue
                    if c[3]: P(x, y, c)
        else:
            for j in range(min(st, 2) + 1):   # the leading ring and up to two behind it
                age = st - j; rx = 20 + 10 * age; ry = rx * 0.8; c = ramp[min(3, age)]
                if rx > 52: continue
                for t in range(0, 360, 2):
                    if age >= 2 and (t // 12) % 3 == 0: continue
                    th = math.radians(t); P(cx + rx * math.cos(th), cy + 10 + ry * math.sin(th), c)
                    if age < 2: P(cx + (rx - 1) * math.cos(th), cy + 10 + (ry - 1) * math.sin(th), Y if age == 0 else O)
            if st <= 2:   # sun rays scattering out between the rings
                for i in range(12):
                    th = math.radians(i * 30 + 15 * st)
                    for d in range(8 + 6 * st, 16 + 8 * st):
                        if d % 3 != 2: P(cx + d * math.cos(th), cy + d * 0.9 * math.sin(th), Y if d < 14 + 6 * st else O)
            for i in range(6 + 4 * st):   # embers
                P(rnd.randint(2, 61), rnd.randint(2, 60), (O, R_, Y)[i % 3])
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(D + state + '/fx.png'); print(state, 'nova', list(frames))

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--fx' in a: fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
