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
APPROVED = {}

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

PUNCH = band(-92, -92)                  # straight arm at shoulder height
CHAMBER = band(75, -150)                # rear fist drawn back by the ear, elbow high behind
TUCK_N, TUCK_F = band(-35, 200), band(-50, 215)   # arms tucked tight to the chest for the shoulder charge
FLEX_N, FLEX_F = band(50, -20), band(40, -15)     # elbows flared back, clenched fists low beside the hips (power surge)

CLIPS = {
 'machLunge': ('Mach Lunge', 4,
  'Mach Lunge (Aries taijutsu, Priority gap closer, burns the target): from the guard the fighter dips into a sprinter crouch, then explodes off the rear foot, tucking both arms tight and lowering the lead shoulder; it rockets forward low, a yellow-orange heat streak trailing off its back and flame licks peeling off the shoulder, lands a long step on and drives the shoulder into the target with a flare of flame at the point of contact; then settles back into the guard. The fighter travels 18 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(1, 1, 1), lean=(2, 7), root=(6, 0), ln='ml-fly-rear', lf='ml-fly-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(1, 1, 1), lean=(2, 8), root=(6, 0), ln='ml-fly-rear', lf='ml-fly-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 7), root=(4, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 6), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3), root=(1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='light', rm='E: 18 px forward over the dash (travel)',
       blur={2: 5, 3: 7, 4: 4}, trail=FIRE_TRAIL, ghosts={2: (5, 10), 3: (6, 12, 18), 4: (5, 10), 5: (4,)}, ghostColors=(('#ff8a1c', '#ffe14d'), ('#d8321a', '#ff8a1c'), ('#d8321a', None)),
       fx=nfx('fire flame (reds, oranges, yellows): licks peeling off the lead shoulder in flight, a flare where the shoulder lands',
              [(2, [('flame2', [28, 23]), ('heat', [24, 27])]), (3, [('flame3', [26, 23]), ('flame1', [24, 28])]),
               (4, [('flame3', [47, 32]), ('flame1', [33, 22])]), (5, [('flame2', [49, 30]), ('embers', [46, 24])]), (6, [('embers', [48, 24])])]),
       extra={'airborneFrames': [2, 3], 'travel': {'rule': 'Mach Lunge is a gap closer: the fighter ends the clip 18 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 18}})),
 'shatterPunch': ('Shatter Punch', 4,
  'Shatter Punch (Aries taijutsu, Guard Break, can stun): from the guard the fighter sits its weight back and draws the rear fist far back beside the ear, elbow high, the lead hand reaching out to measure; holds the load a beat, then steps in and fires the rear fist dead straight through the target with the whole body behind it, rear heel turning up; a yellow-orange crack bursts out from the fist on contact and shards fly; it holds the extension a beat, then pulls back into the guard.', [
     g(),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(0, 0), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 on the step into the punch, -1 settling back',
       fx=nfx('fiery yellow-orange guard-crack burst at the fist on contact, shards flying off',
              [(4, [('shatter2', [55, 27])]), (5, [('shatter3', [55, 28]), ('shard', [52, 18]), ('shardR', [62, 30])]),
               (6, [('shard', [50, 15]), ('shardR', [62, 33]), ('shatter1', [57, 26])])]))),
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
    if x.get('ghosts'):
        from PIL import Image
        f = D + state + '/fx.png'; top = Image.open(f).convert('RGBA')   # blur + splash so far
        ghosts(state, x['ghosts'], x['ghostColors'])
        g_ = Image.open(f).convert('RGBA'); g_.alpha_composite(top); g_.save(f)   # streaks and flames stay over the afterimages
        if old: new = Image.open(f).convert('RGBA'); new.alpha_composite(old); new.save(f)

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
