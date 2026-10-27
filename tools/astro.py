"""Astrological (Sign) kit animations (Christopher 2026-10-27: "begin developing Astrological kit animations"; abilities
from the Sign Kits tab of AstroFighters_Abilities, 12 signs x 8). Played from the approved boxing guard (hitReact frame 6)
and returning to it, through universal.py's spec builder. One state per ability. E/W first (W mirrors E), S/N after
approval. Effects use the sign's element colours (Christopher 2026-10-27 17:00): fire = reds/oranges/yellows (Sagittarius:
select black and purple flames), earth = earth and crystal tones, water = water and ice tones; air stays white/pale until ruled.
Run: python3 tools/astro.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/astro.py --fx <state>   (aura / motion blur after the render; splash fx are baked by the renderer)"""
import sys, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universal as U
from universal import band, g, leg, kleg, LOW, BRACE, NPAL, NPAT, nfx, D
from gen import load, save

STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {'machLunge': 'E/W approved by user 2026-10-27 (v5 sprint, flaming feet, fire wake, 4 afterimages, fc741f6; W mirrors E); S/N to author', 'shatterPunch': 'E/W approved by user 2026-10-27 (v3 arm swirl + impact burst, fc741f6; W mirrors E); S/N to author'}

U.POSES += [leg('ml-dip-lead', (32, 45), (38, 51), 37), leg('ml-dip-rear', (31, 45), (29, 51), 24, wrap=54, kind='toe60'),   # sprinter dip, rear heel up
            kleg('ml-fly-lead', (33, 42), (39, 46), (38, 52), 'toe30k'), kleg('ml-fly-rear', (31, 42), (25, 47), (20, 51), 'toe30k'),   # driving off the rear foot
            leg('ml-plant-lead', (33, 43), (39, 50), 41), kleg('ml-trail-rear', (31, 43), (26, 49), (22, 54), 'toe30k'),   # lead foot lands a long step on
            leg('sp-load-lead', (32, 43), (35, 51), 36), leg('sp-load-rear', (31, 43), (28, 51), 24),                # Shatter Punch: weight sat back
            leg('sp-drive-lead', (33, 43), (38, 50), 40), leg('sp-drive-rear', (32, 43), (31, 50), 27, wrap=54, kind='toe60')]  # step in, rear heel turns up

# element palettes (letters added to universal.NPAL; W/w white stay for air and highlights)
ELEMENT = {'Y': '#ffe14d', 'O': '#ff8a1c', 'R': '#d8321a',               # fire: yellow core, orange body, red edge
           'K': '#1c1024', 'P': '#9b45ff', 'p': '#55208f',                # Sagittarius: black flame with purple
           'E': '#8a6236', 'e': '#c79a5b', 'C': '#7fe3d0', 'c': '#d9fff6',  # earth: soil browns, crystal teal / glint
           'A': '#2f7fe0', 'a': '#7cc8ff', 'I': '#dff6ff'}                 # water: deep and light water, ice white-blue
NPAL.update(ELEMENT)
# fire fx patterns: flame licks (red edge, orange body, yellow core), a fire-sign guard-crack, embers
NPAT.update({
    'flame1': ['.R.', 'ROR', '.Y.'], 'flame2': ['..R..', '.RO..', '.OYR.', 'ROYOR', '.RRR.'],
    'flame3': ['...R...', '..RO...', '.ROO.R.', '.OYYRO.', 'ROYYYOR', '.ROYOR.', '..RRR..'],
    'shatter1': ['O...O', '.Y.Y.', '..W..', '.Y.Y.', 'O...O'],
    'shatter2': ['R.....R', '.O...O.', '..YYY..', '.YYWYY.', '..YYY..', '.O...O.', 'R.....R'],
    'shatter3': ['R...R...R', '.O..O..O.', '..Y.Y.Y..', '...YWY...', 'OYYWWWYYO', '...YWY...', '..Y.Y.Y..', '.O..O..O.', 'R...R...R'],
    'shard': ['O.', '.R'], 'shardR': ['.O', 'R.'],
    'heat': ['O.Y.O', '.R.R.'], 'embers': ['.O..R', 'R..O.', '..Y..'],
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
FLEX_N, FLEX_F = band(50, -20), band(40, -15)     # elbows flared back, clenched fists low beside the hips (power surge)

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
 'innerGateAdrenaline': ('Inner Gate: Adrenaline', 4,
  'Inner Gate: Adrenaline (Aries taijutsu buff: AGI and STR up, the fighter burns itself): from the guard the fighter clenches, curls the fists in front of the belly and sinks, straining, eyes squeezed; then the gate bursts open: it stands up tall, chest thrown out and both fists driven down and back, and an orange-red aura flares around the whole body with flame licks rising off the shoulders and head; the aura pulses once, the flames keep licking (the self-burn), then the fighter drops back into the guard with embers still drifting off it.', [
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
  [0, 0, 0, 1, 3, 2, 3, 1, 0],
  dict(fps=10, auraColors=FIRE_AURA, fx=nfx('red-orange-yellow flame licks rising off the shoulders and head as the gate opens (self-burn), embers drifting after',
              [(4, [('flame2', [31, 8]), ('flame2', [25, 26]), ('flame2', [39, 26])]), (5, [('flame3', [30, 8]), ('flame3', [23, 26]), ('flame2', [40, 25])]),
               (6, [('flame2', [32, 7]), ('flame2', [24, 25]), ('flame3', [38, 26])]), (7, [('embers', [31, 7])]), (8, [('embers', [30, 5])])]))),
}

def spec(state):
    U.CLIPS[state] = CLIPS[state]
    U.APPROVED[state] = APPROVED.get(state, STAT)
    U.spec(state)
    x = CLIPS[state][6]; s = load(D + state + '.json')
    for k, v in (x.get('extra') or {}).items(): s[k] = v
    save(s, D + state + '.json')

def fx(state):
    x = CLIPS[state][6]
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
    if x.get('swirl') or x.get('impact'):
        from PIL import Image
        f = D + state + '/fx.png'
        if not os.path.exists(f) or 'fx' not in load(D + state + '.json'): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f)   # no splash fx: start clean (not a stale render)
        if x.get('swirl'): swirl(state, x['swirl'])
        if x.get('impact'): impact(state, x['impact'])
    if x.get('ghosts'):
        from PIL import Image
        f = D + state + '/fx.png'; top = Image.open(f).convert('RGBA')   # blur + splash so far
        ghosts(state, x['ghosts'], x['ghostColors'])
        g_ = Image.open(f).convert('RGBA'); g_.alpha_composite(top); g_.save(f)   # streaks and flames stay over the afterimages

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

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--fx' in a: fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
