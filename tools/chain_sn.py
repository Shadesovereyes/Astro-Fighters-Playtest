"""S/N (front/back) views of the approved Kyoketsu-Shoge chain states (Christopher 2026-10-21: "i want ... the N/S chain
animations developed"). E/W are approved (2026-10-19, tools/chainsnare.py); this adds S and N rows as candidates.
Thrower states (chainSnare, chainHold, chainYank, chainRecall) start from the kama idle's approved S/N view (oneHandGuard:
kama low in the right hand with the blade toward the viewer, the left fist up holding the chain); the snared states
(snared, chainYanked, snaredStruggle, snareBreak) start from the guard's approved S/N view. In S the other fighter is
toward the viewer (below on screen), in N away from the viewer (above), so a throw, a hold or a haul is a foreshortened
arm toward or away from the viewer, as the S/N punches are. Every S/N frame interprets its E frame (same rows for the
fists, the weight and the coils by projection). E/W pixels are restored from HEAD after the render.
Coils (snared states) are painted after the render over the fighter's actual silhouette, two bands round the chest
and upper arms; the chain anchors (events chainHand / coil) are measured on the rendered fists.
Run: python3 tools/chain_sn.py [state..]   (spec, render with character-posed and character-weapon, restore E/W, fx)"""
import sys, copy, os, subprocess, io, json, math
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import load, save
from PIL import Image
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
OHG = load(D + 'oneHandGuard.json'); GUARD = load(D + 'guard.json')
THROWER = ('chainSnare', 'chainHold', 'chainYank', 'chainRecall')
HELD = ('snared', 'chainYanked', 'snaredStruggle', 'snareBreak')
STATES = THROWER + HELD

def mir(a): return None if a is None else ((-a) % 360 if (-a) % 360 <= 180 else (-a) % 360 - 360)
def mirror_arm(t):   # the same arm seen from behind: angles mirrored (the N pivots swap sides)
    a, e, *rest = t; return (-a, mir(e), *rest)

# arm tuples (S semantics): (upper-arm angle, forearm angle or None, scale, fist kind[, elbow at[, fistDy]])
# R pivot is screen left in S (positive = outward), L screen right (positive = inward)
KAMA_R = (0, None, 0.62, 'front')                 # the kama hand low at the right hip, blade toward the viewer (kama idle)
CHAIN_L = (0, 178, 0.6, 'up', 9)                  # the chain fist up at the left shoulder (kama idle)
OUT = (82, None, 0.45, 'front')                   # off arm straight out at the viewer, chain running from the fist
HOLD = lambda d=0: (72 + d, None, 0.5, 'front')   # the chain held taut toward the viewer at chest height
PIN_R, PIN_L = (3, 357, 1, 'front', 7, 2), (-3, 3, 1, 'front', 7, 2)   # arms pinned to the sides by the coils (exhausted's hanging arms, tighter)
GUARD_R, GUARD_L = (10, 192, 1, 'up'), (-10, 168, 1, 'up')
TW = lambda p, s, h: (p, s, h)

# per state: frame -> dict(R=, L=, NR=, NL=, tw=, chain=(to, weight?)) ; N defaults to the S arm mirrored
SN = {
 'chainSnare': {0: dict(chain=([0, 9], True)),
                1: dict(L=(18, None, 0.55, 'front'), chain=([-3, 7], True)),                       # off hand in front of the belly, weight whirled low
                2: dict(L=(-28, 172, 1, 'up'), NL=(28, 188, 1, 'up'), chain=([3, -9], True)),       # wrist cocked up beside the head, weight swung up over it
                3: dict(L=(55, None, 0.6, 'front'), NL=(-10, None, 1, 'up'), tw=TW(-1, -1, -1), chain=([0, 4], False)),   # throw
                4: dict(L=OUT, NL=(-15, None, 1, 'up'), tw=TW(-1, -2, -1), chain=([0, 4], False)),  # release
                5: dict(L=OUT, NL=(-15, None, 1, 'up'), tw=TW(-1, -2, -1), chain=([0, 4], False)),
                6: dict(L=HOLD(2), NL=(-14, None, 1, 'up'), tw=TW(0, -1, 0), chain=([0, 4], False)),
                7: dict(L=HOLD(), NL=(-13, None, 1, 'up'), tw=TW(0, -1, 0), chain=([0, 4], False))},
 'chainHold': {k: dict(L=HOLD(d), NL=(-13 - d // 2, None, 1, 'up'), tw=TW(0, -1, 0), chain=([0, 4], False)) for k, d in enumerate((0, 2, 0, -2))},
 'chainYank': {0: dict(L=HOLD(), NL=(-13, None, 1, 'up'), tw=TW(0, -1, 0), chain=([0, 4], False)),
               1: dict(L=(86, None, 0.42, 'front'), NL=(-18, None, 1, 'up'), tw=TW(-1, -2, -1), chain=([0, 4], False)),   # reach along the chain
               2: dict(L=(30, None, 0.7, 'front'), NL=(-4, None, 1, 'up'), tw=TW(1, 1, 1), chain=([0, 5], False)),        # haul
               3: dict(L=(-14, None, 0.85, None), NL=(14, 40, 1, 'up'), tw=TW(1, 2, 1), chain=([1, 6], False)),          # chain hand back at the hip
               4: dict(L=(-14, None, 0.85, None), NL=(14, 40, 1, 'up'), tw=TW(1, 2, 1), chain=([1, 6], False)),
               5: dict(L=(45, None, 0.6, 'front'), NL=(-8, None, 1, 'up'), tw=TW(0, 0, 0), chain=([0, 4], False)),
               6: dict(L=HOLD(), NL=(-13, None, 1, 'up'), tw=TW(0, -1, 0), chain=([0, 4], False))},
 'chainRecall': {0: dict(L=HOLD(), NL=(-13, None, 1, 'up'), tw=TW(0, -1, 0), chain=([0, 4], False)),
                 1: dict(L=(50, None, 0.6, 'front'), NL=(-8, None, 1, 'up'), chain=([1, 6], True)),       # the slack chain pulled in, weight back at the fist
                 2: dict(L=(22, 200, 0.8, 'up', 8), chain=([0, 8], True)),
                 3: dict(chain=([0, 9], True))},
 'snared': {0: dict(R=PIN_R, L=PIN_L), 1: dict(R=(5, 355, 1, 'front', 7, 2), L=(-5, 5, 1, 'front', 7, 2), tw=TW(0, 1, 0)),
            2: dict(R=PIN_R, L=PIN_L), 3: dict(R=(2, 358, 1, 'front', 7, 2), L=(-2, 2, 1, 'front', 7, 2))},
 'chainYanked': {k: dict(R=PIN_R, L=PIN_L) for k in range(6)},
 'snaredStruggle': {0: dict(R=PIN_R, L=PIN_L),
                    1: dict(R=(9, 350, 1, 'front', 7, 2), L=(-5, 5, 1, 'front', 7, 2), tw=TW(1, 2, 1)),     # heave against the coils, one way
                    2: dict(R=(11, 348, 1, 'front', 7, 2), L=(-6, 6, 1, 'front', 7, 2), tw=TW(1, 2, 1)),
                    3: dict(R=(5, 355, 1, 'front', 7, 2), L=(-9, 10, 1, 'front', 7, 2), tw=TW(-1, -2, -1)),  # twist back the other way
                    4: dict(R=(6, 354, 1, 'front', 7, 2), L=(-11, 12, 1, 'front', 7, 2), tw=TW(-1, -2, -1)),
                    5: dict(R=PIN_R, L=PIN_L), 6: dict(R=PIN_R, L=PIN_L)},
 'snareBreak': {0: dict(R=PIN_R, L=PIN_L),
                1: dict(R=(9, 350, 1, 'front', 7, 2), L=(-5, 5, 1, 'front', 7, 2), tw=TW(1, 2, 1)),
                2: dict(R=(11, 348, 1, 'front', 7, 2), L=(-6, 6, 1, 'front', 7, 2), tw=TW(1, 2, 1)),
                3: dict(R=(70, 110, 1, None), L=(-70, 250, 1, None)),            # coils burst: both arms flung out wide, free
                4: dict(R=(55, 140, 1, 'up'), L=(-55, 220, 1, 'up')),
                5: dict(R=(30, 175, 1, 'up'), L=(-30, 185, 1, 'up')),
                6: dict(R=GUARD_R, L=GUARD_L), 7: dict(R=GUARD_R, L=GUARD_L)},
}

PER_FRAME = {'angle', 'elbow', 'scale', 'fist', 'pivotDx', 'pivotDy', 'showTo'}
def resample(fr, F, F0):
    pick = lambda xs: [copy.deepcopy(xs[k % F0]) for k in range(F)]
    for d in ('S', 'N'):
        v = fr['views'][d]
        for key in ('legPose', 'handDy', 'hipDx', 'footDx', 'twist'):
            if key in v: v[key] = {s: pick(x) if isinstance(x, list) and len(x) == F0 else x for s, x in v[key].items()}
        for sd, ab in v['armBand'].items():
            for key in PER_FRAME:
                if isinstance(ab.get(key), list) and len(ab[key]) == F0: ab[key] = pick(ab[key])
        if 'variants' in v: v['variants'] = {str(k): copy.deepcopy(v['variants'].get(str(k % F0), [])) for k in range(F)}
    fr['legLift'] = {'R': [0] * F, 'L': [0] * F}

def head_spec(state):
    return json.loads(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + os.path.relpath(D + state + '.json', R)]))

def set_arm(v, sd, k, t, d):
    a, e, sc, fist, *rest = t; ab = v['armBand'][sd]
    at = rest[0] if rest else 7; fdy = rest[1] if len(rest) > 1 else None
    ab['angle'][k] = a; ab['scale'][k] = sc; ab['fist'][k] = fist
    ab['elbow'][k] = ({'at': at, 'angle': e, **({'fistDy': fdy} if fdy is not None else {})}) if e is not None else None
    if d == 'N':
        sh = ab.get('showTo'); sh = sh if isinstance(sh, list) else [sh] * len(ab['angle'])
        sh[k] = 7 if e is None else None; ab['showTo'] = sh

def spec_sn(state):
    spec = head_spec(state); F = spec['frames']; base = OHG if state in THROWER else GUARD
    fr = copy.deepcopy(base['frontal']); resample(fr, F, base['frames'])
    for key, val in base['arms']['band'].items(): spec['arms']['band'].setdefault(key, copy.deepcopy(val))
    dy = spec['bob']['dy']; mb = max(max(dy), max(spec['bob'].get('arms') or dy))
    for d in ('S', 'N'):
        v = fr['views'][d]; sg = 1 if d == 'S' else -1
        if isinstance(v.get('bobRows'), list) and len(v['bobRows']) < mb:   # room for this state's deeper bob
            v['bobRows'] = v['bobRows'] + [r for r in (49, 53, 47, 52, 45, 54, 48, 51) if r not in v['bobRows']][:mb - len(v['bobRows'])]
        for sd in 'RL':
            ab = v['armBand'][sd]
            for key in ('angle', 'scale', 'fist', 'elbow', 'pivotDx'):
                if not isinstance(ab.get(key), list): ab[key] = [copy.deepcopy(ab.get(key))] * F
        v.setdefault('twist', {'pelvis': [0] * F, 'shoulders': [0] * F, 'head': [0] * F})
        v.setdefault('hipDx', {'R': [0] * F, 'L': [0] * F})
        for k, o in SN[state].items():
            for sd in 'RL':
                t = o.get('N' + sd) if d == 'N' and ('N' + sd) in o else (o.get(sd) if d == 'S' else (mirror_arm(o[sd]) if sd in o else None))
                if d == 'N' and state in HELD and ('N' + sd) not in o and sd in o and o[sd][1] is not None and abs(mir(o[sd][1])) < 30:
                    t = (-o[sd][0], None, 1, 'up')   # arms hanging at the sides seen from behind: the upper arms beside the torso (exhausted's N)
                if t is not None: set_arm(v, sd, k, t, d)
            if 'tw' in o:
                for i, part in enumerate(('pelvis', 'shoulders', 'head')): v['twist'][part][k] += sg * o['tw'][i]
                for sd in 'RL': v['hipDx'][sd][k] += sg * o['tw'][0]
    spec['frontal'] = fr; spec['directions'] = ['S', 'E', 'N', 'W']
    sway = GUARD['clothing']['sash']['sway']
    for g in ('S', 'N'): spec['clothing']['sash']['sway'][g] = (sway[g] * F)[:F]
    # the yank's stumble toward the thrower: down the screen in S (toward the viewer), up in N
    ex = [m[0] for m in spec['rootMotion']['E']]
    spec['rootMotion']['S'] = [[0, x] for x in ex] if state == 'chainYanked' else [[0, 0]] * F
    spec['rootMotion']['N'] = [[0, -x] for x in ex] if state == 'chainYanked' else [[0, 0]] * F
    if 'expressions' in spec:
        for d in ('S', 'N'): spec['expressions']['frames'][d] = [x if x in (spec['expressions'].get('shapes', {}).get(x) or {}) or (spec['expressions'].get('shapes', {}).get(x) or {}).get(d) else None for x in spec['expressions']['frames']['E']]
    if state in THROWER:   # the kama stays as in the idle; the chain leaves the off fist (via measured after the arm render)
        w = spec['weapons'][0]; ip = OHG['weapons'][0]['itemPoses']['kama']
        for d in ('S', 'N'): w[d] = [None] * F
    spec['status'] = spec['status'].replace('S/N to author', 'S/N CANDIDATE 2026-10-21 (v1)')
    save(spec, D + state + '.json')
    return spec

# ---- measuring the render ----
ROW = {'S': 0, 'N': 2}
def layer_px(state, name, d, k, size=64):
    p = D + state + '/' + name + '.png'
    if not os.path.exists(p): return None
    im = Image.open(p).convert('RGBA'); r = ROW[d]
    return im.crop((k * size, r * size, k * size + size, r * size + size))
def fist_at(state, d, k, sd, guess):
    """the opaque non-outline arm pixel nearest the band's hand point (arms layer; N hands behind the body: body too)"""
    best = None
    for name in ('arms', 'body'):
        im = layer_px(state, name, d, k)
        if im is None: continue
        for y in range(max(0, int(guess[1]) - 5), min(64, int(guess[1]) + 6)):
            for x in range(max(0, int(guess[0]) - 5), min(64, int(guess[0]) + 6)):
                p = im.getpixel((x, y))
                if p[3] == 255 and max(p[:3]) > 60:
                    dd = (x - guess[0]) ** 2 + (y - guess[1]) ** 2
                    if best is None or dd < best[0]: best = (dd, x, y)
        if best: break
    return [best[1], best[2]] if best else [round(guess[0]), round(guess[1])]
def hand_guess(spec, d, k, sd):
    v = spec['frontal']['views'][d]; ab = v['armBand'][sd]; B = spec['arms']['band']
    sc = ab['scale'][k]; el = ab['elbow'][k]; a = math.radians(ab['angle'][k])
    arms = (spec['bob'].get('arms') or spec['bob']['dy'])[k]
    px = ab['pivot'][0] + (ab['pivotDx'][k] or 0) + v['twist']['shoulders'][k]; py = ab['pivot'][1] + arms
    hf = B['handFrom'] * sc + 1.5
    if el is None: return (px - math.sin(a) * hf, py + math.cos(a) * hf)
    at = el['at'] * sc; e = math.radians(el['angle'])
    return (px - math.sin(a) * at - math.sin(e) * (hf - at), py + math.cos(a) * at + math.cos(e) * (hf - at))

def weapons_sn(state):
    spec = load(D + state + '.json'); F = spec['frames']; w = spec['weapons'][0]; ip = OHG['weapons'][0]['itemPoses']['kama']
    ev = spec.setdefault('events', {})
    for d in ('S', 'N'):
        E = []; evd = []
        for k in range(F):
            g = fist_at(state, d, k, 'R', hand_guess(spec, d, k, 'R')); h = fist_at(state, d, k, 'L', hand_guess(spec, d, k, 'L'))
            to, weight = SN[state].get(k, {}).get('chain', ([0, 9], True))
            if d == 'N': to = [-to[0], -to[1]] if not weight else [-to[0], to[1]]
            if d == 'S':
                e = {**copy.deepcopy(ip['S'][0]), 'grip': g, 'chain': {'via': h, 'droop': 6 if weight else 2, 'to': to, 'sag': 0, 'z': 'front', **({} if weight else {'noWeight': True})}}
            else:
                e = {**copy.deepcopy(ip['N'][0]), 'grip': g, 'hidden': True, 'chain': {'via': h, 'droop': 6 if weight else 2, 'to': to, 'sag': 0, 'z': 'behind', **({} if weight else {'noWeight': True})}}
            E.append(e); evd.append({'frame': k, 'chainHand': h})
        w[d] = E
        base = {x['frame']: x for x in ev.get('E', [])}
        ev[d] = [{**{kk: vv for kk, vv in base.get(k, {'frame': k}).items() if kk not in ('chainHand', 'release', 'coil')}, **evd[k], **({'release': evd[k]['chainHand']} if 'release' in base.get(k, {}) else {})} for k in range(F)]
    w.pop('itemPoses', None)
    save(spec, D + state + '.json')

# ---- coils over the snared fighter's silhouette ----
CP = {'#': (0, 0, 0, 255), 'W': (255, 255, 255, 255), 'a': (0xad, 0xad, 0xad, 255)}
def silhouette(state, d, k):
    m = set()
    for name in ('body', 'male-gi', 'arms'):
        im = layer_px(state, name, d, k)
        if im is None: continue
        for y in range(64):
            for x in range(64):
                if im.getpixel((x, y))[3]: m.add((x, y))
    return m
def coil_rows(spec, k):
    b = spec['bob']['dy'][k]; return (26 + b, 31 + b)   # the upper coil over the chest and upper arms, the lower over the forearms and belly
def paint_coils(img, k, sil, rows, broken=False):
    for row in rows:
        xs = [x for (x, y) in sil if y == row]
        if not xs: continue
        x0, x1 = min(xs) - 1, max(xs) + 1
        for x in range(x0, x1 + 1):
            for yy, kind in ((row - 1, '#'), (row, 'link'), (row + 1, '#')):
                if x in (x0, x1) and kind == '#': continue
                c = CP['#'] if kind == '#' or x in (x0, x1) else (CP['a'] if (x - x0) % 2 else CP['W'])
                img.putpixel((k * 64 + x, ROW_FX + yy), c)
ROW_FX = 0
LINKS = {'link': ['.#.', '#a#', '.#.'], 'linkW': ['.#.', '#W#', '.#.'], 'bar': ['.###.', '#aWa#', '.###.']}
BURST = {3: [([20, 27], 'bar'), ([40, 27], 'bar'), ([30, 22], 'link'), ([33, 33], 'linkW')],   # S/N: links fly out to both sides
         4: [([14, 25], 'link'), ([47, 24], 'linkW'), ([22, 17], 'link'), ([41, 38], 'link'), ([30, 40], 'linkW')],
         5: [([8, 27], 'linkW'), ([53, 22], 'link'), ([47, 45], 'linkW'), ([13, 44], 'link')]}
def fx_sn(state):
    global ROW_FX
    spec = load(D + state + '.json'); F = spec['frames']; p = D + state + '/fx.png'
    im = Image.open(p).convert('RGBA') if os.path.exists(p) else Image.new('RGBA', (64 * F, 256))
    if im.height < 256: im = Image.new('RGBA', (64 * F, 256))
    ev = spec.setdefault('events', {})
    for d in ('S', 'N'):
        ROW_FX = ROW[d] * 64
        im.paste(Image.new('RGBA', (64 * F, 64)), (0, ROW_FX))
        evd = []
        for k in range(F):
            held = not (state == 'snareBreak' and k >= 3)
            rows = coil_rows(spec, k)
            if held:
                paint_coils(im, k, silhouette(state, d, k), rows)
                evd.append({'coil': [32 + spec['frontal']['views'][d]['twist']['shoulders'][k], rows[0]]})
            else:
                for (x, y), pat in BURST.get(k, []):
                    for dy_, r in enumerate(LINKS[pat]):
                        for dx_, ch in enumerate(r):
                            if ch != '.': im.putpixel((k * 64 + x + dx_, ROW_FX + y - len(LINKS[pat]) + 1 + dy_), CP[ch])
                evd.append({})
        base = {x['frame']: x for x in ev.get('E', [])}
        ev[d] = [{**{kk: vv for kk, vv in base.get(k, {'frame': k}).items() if kk != 'coil'}, **evd[k]} for k in range(F)]
    im.save(p)
    lay = spec.get('layers')
    save(spec, D + state + '.json')

def restore(state):
    """the approved E/W pixels from HEAD into the E and W rows of the new 4-row sheets (S, E, N, W)"""
    d = D + state + '/'
    for f in sorted(os.listdir(d)):
        if not f.endswith('.png'): continue
        rel = os.path.relpath(d + f, R)
        try: old = Image.open(io.BytesIO(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + rel], stderr=subprocess.DEVNULL))).convert('RGBA')
        except subprocess.CalledProcessError: continue
        new = Image.open(d + f).convert('RGBA'); h = old.height // 2
        if new.height < 4 * h: new = Image.new('RGBA', (old.width, 4 * h))
        for row, nrow in ((0, 1), (1, 3)):
            new.paste(Image.new('RGBA', (new.width, h)), (0, nrow * h)); new.paste(old.crop((0, row * h, old.width, row * h + h)), (0, nrow * h))
        new.save(d + f)

def run(state):
    spec_sn(state)
    subprocess.check_call(['node', R + 'tools/character-posed.mjs', 'male', state], stdout=subprocess.DEVNULL)
    if state in THROWER:
        weapons_sn(state)
        subprocess.check_call(['node', R + 'tools/character-weapon.mjs', 'male', state], stdout=subprocess.DEVNULL)
    restore(state)
    if state in HELD: fx_sn(state)
    print(state, 'S/N v1')

if __name__ == '__main__':
    for s in [a for a in sys.argv[1:] if not a.startswith('--')] or STATES: run(s)
