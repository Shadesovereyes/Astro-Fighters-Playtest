"""Martial stance idles (Christopher 2026-10-19): one looping combat idle per martial stance; Boxing keeps the approved
guard. Built on the approved guard spec (E/W first, W mirrors E; S/N to author after approval).
Run: python3 tools/stances.py ; node tools/character-posed.mjs male <state> (each)"""
import sys, copy, json
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
GUARD = load(D + 'guard.json')
PALM = {k: v for k, v in load(D + 'mountPalm.json')['arms']['band'].items() if k in ('palmUp', 'palmDown')}
def band(a, e, **k): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def leg(name, hip, knee, foot, wrap=56, kind='flat', hipX=None):
    return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1],
            'footX': foot, 'wrapRow': wrap, 'foot': kind}
STAT = 'CANDIDATE 2026-10-19 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {s: 'E/W approved by user 2026-10-19 (W mirrors E); S/N to author' for s in ('karateGuard', 'judoGuard', 'muayThaiGuard', 'horseStance', 'jiuJitsuGuard', 'wrestlingGuard')}

STANCES = {}
def stance(state, ability, fps, intent, frames, poses):
    STANCES[state] = (ability, fps, intent, frames, poses)

# Muay Thai: tall and square, weight on the rear leg, lead heel up and the lead knee tapping, long high guard
MT = [leg('mt-lead', (32, 41), (36, 48), 38, 54, 'toe60'), {'name': 'mt-lead-up', 'construction': 'band', 'hipX': 33, 'hipRow': 41, 'kneeX': 40, 'kneeRow': 42, 'ankle': [39, 50], 'foot': 'toe30k'},
      leg('mt-rear', (31, 41), (29, 49), 25)]
mt_n, mt_f = band(-20, 212), band(-45, 222)   # the boxing guard's hands-up arms (Christopher 2026-10-19)
stance('muayThaiGuard', 'Muay Thai Stance', 6,
       'Muay Thai stance idle: tall and square, weight sitting on the rear leg, the lead heel off the ground and the lead knee lifting high once per loop; the boxing hands-up guard rocking on its own half-length rhythm, out of sync with the leg (Christopher 2026-10-19).',
       [dict(an=band(-20 + dn, 212 + dn), af=band(-45 + df, 222 + df), bob=(dy, dy, ab), lean=(0, 2), root=(0, 0), ln='mt-rear', lf=lf)
        for (dn, df, ab), (dy, lf) in zip([(0, 0, 2), (2, -3, 1), (4, -5, 1), (2, -3, 2)] * 2,
                                          [(1, 'mt-lead'), (1, 'mt-lead'), (1, 'mt-lead'), (1, 'mt-lead-up'), (1, 'mt-lead-up'), (2, 'mt-lead'), (2, 'mt-lead'), (1, 'mt-lead')])], MT)

# Karate: long front stance, lead hand out at chest height, rear fist chambered at the hip (hikite)
KA = [leg('ka-lead', (33, 43), (38, 49), 40), leg('ka-rear', (31, 43), (27, 50), 21)]
stance('karateGuard', 'Karate Stance', 6,
       'Karate stance idle: long front stance, lead knee bent over the foot and the rear leg long behind; the lead arm extended at chest height toward the opponent, the rear fist chambered at the hip; slow breathing settle.',
       [dict(an=band(55, -60), af=band(-75, -95), bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead'),
        dict(an=band(55, -60), af=band(-75, -95), bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead'),
        dict(an=band(55, -60), af=band(-73, -93), bob=(3, 3, 3), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead'),
        dict(an=band(55, -60), af=band(-73, -93), bob=(3, 3, 4), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead')], KA)

# Horse Stance: deep straddle, back upright, both fists chambered at the hips
HS = [leg('hs-near', (31, 45), (38, 50), 35), leg('hs-far', (30, 45), (36, 50), 30)]
stance('horseStance', 'Horse Stance', 4,
       'Horse Stance idle: deep straddle with the knees bent out over the feet and the back upright; both fists chambered at the hips; slow, rooted breathing.',
       [dict(an=band(55, -60), af=band(55, -60), bob=(6, 6, 6), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far'),
        dict(an=band(55, -60), af=band(55, -60), bob=(6, 6, 6), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far'),
        dict(an=band(55, -60), af=band(55, -60), bob=(6, 7, 7), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far'),
        dict(an=band(55, -60), af=band(55, -60), bob=(6, 7, 7), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far')], HS)

# Judo: upright natural stance, both open hands out at chest height hunting for the lapel and sleeve grip
JU = [leg('ju-lead', (32, 42), (36, 50), 39), leg('ju-rear', (31, 42), (29, 50), 24)]   # wider (Christopher 2026-10-19)
P = dict(fistKind='palm')
stance('judoGuard', 'Judo Stance', 6,
       'Judo stance idle: upright natural stance, knees soft; both hands open and out at chest height, the lead hand reaching for the sleeve and the rear hand for the lapel, pawing in and out.',
       [dict(an=band(-55, -88, **P), af=band(-72, -96, **P), bob=(1, 1, 2), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead'),
        dict(an=band(-55, -88, **P), af=band(-78, -100, **P), bob=(1, 1, 1), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead'),
        dict(an=band(-60, -92, **P), af=band(-72, -96, **P), bob=(2, 2, 2), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead'),
        dict(an=band(-55, -88, **P), af=band(-72, -96, **P), bob=(2, 2, 3), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead')], JU)

# Jiu-Jitsu: crouched and leaning in, elbows tight to the ribs, open hands forward to frame and grab
JJ = [leg('jj-lead', (33, 46), (38, 51), 38), leg('jj-rear', (31, 46), (30, 52), 24)]
stance('jiuJitsuGuard', 'Jiu-Jitsu Stance', 6,
       'Jiu-Jitsu stance idle: crouched with the hips back and the head forward, elbows tight to the ribs and both open hands out in front to frame and grab; small weight shifts.',
       [dict(an=band(-40, -85, **P), af=band(-12, -38, **P), bob=(5, 5, 5), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead'),
        dict(an=band(-40, -85, **P), af=band(-12, -38, **P), bob=(5, 5, 6), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead'),
        dict(an=band(-45, -90, **P), af=band(-14, -42, **P), bob=(6, 6, 6), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead'),
        dict(an=band(-45, -90, **P), af=band(-14, -42, **P), bob=(6, 6, 7), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead')], JJ)

# Wrestling: deep sprawl-ready crouch, chest over the lead knee, hands low and forward hand-fighting
WR = [leg('wr-lead', (33, 47), (39, 51), 38), leg('wr-rear', (31, 47), (31, 52), 23),
      leg('wr-lead-low', (33, 48), (39, 52), 38), leg('wr-rear-low', (31, 48), (31, 53), 23)]
stance('wrestlingGuard', 'Wrestling Stance', 6,
       'Wrestling stance idle: deep crouch with the chest over the lead knee and the rear leg driving behind; the off hand forward and away from the body with the elbow bent, the lead hand lower, both open hands leaning forward (redone like Jiu-Jitsu, Christopher 2026-10-19).',
       [dict(an=band(-45, -105, **P), af=band(-35, -70, **P), bob=b, lean=(2, 10), root=(0, 0), ln='wr-rear' + lo, lf='wr-lead' + lo)
        for b, lo in (((6, 6, 7), ''), ((6, 6, 6), ''), ((7, 8, 7), '-low'), ((7, 8, 8), '-low'))], WR)   # guard-style bob: body, head a beat deeper, arms a frame behind, whole arms riding it (Christopher 2026-10-19)

def specs(only=None):
    base = copy.deepcopy(GUARD)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    base['arms']['band'].update(copy.deepcopy(PALM))
    for f, v in load(D + 'clinchKnee.json')['legs']['feet'].items(): base['legs']['feet'].setdefault(f, copy.deepcopy(v))   # toe30k etc. for a lifted lead leg
    for st, (ab, fps, intent, frames, poses) in STANCES.items():
        if only and st not in only: continue
        s = build(base, st, [dict(src=0, **f) for f in frames], status=APPROVED.get(st, STAT), intent=intent, newPoses=poses,
                  clips={'rule': 'martial stance idle: loops while that stance is active; attacks of the style start and end in the guard', st: {'frames': list(range(len(frames))), 'fps': fps, 'loop': True}},
                  rmRule='in place', extra={'stance': ab})
        s['fps'] = fps; s.pop('approved', None); s.pop('keyPoses', None)
        if st in ('judoGuard', 'jiuJitsuGuard', 'wrestlingGuard'):   # Christopher 2026-10-19: open hands angled forward, fingers leaning toward the opponent
            s['arms']['band']['palmUp'] = {'use': 'open hand angled forward, fingers leaning toward the opponent (judo grip hunt)', 'anchor': [0, 4],
                                           'rows': ['...Lm', '..LLm', '.LLLm', 'LLLLm', 'LLLms', 'mLLs.', '.sDs.']}
        save(s, D + st + '.json')
    print(' '.join(STANCES))


def outline(states=None):
    """after render: close the outline where an open hand's fingertips or a joint meet empty space (renderer QC
    'unoutlinedEdges'); the black pixel goes on the arms layer, or the body layer when the edge pixel is body"""
    from PIL import Image
    for st in states or STANCES:
        b = Image.open(D + st + '/body.png').convert('RGBA'); a = Image.open(D + st + '/arms.png').convert('RGBA')
        W, H = b.size; n = 0
        for oy in range(0, H, 64):
            for ox in range(0, W, 64):
                fig = {}
                for lay, im in (('body', b), ('arms', a)):
                    for y in range(64):
                        for x in range(64):
                            p = im.getpixel((ox + x, oy + y))
                            if p[3] == 255: fig[(x, y)] = (lay, p[:3])
                for (x, y), (lay, c) in list(fig.items()):
                    if c == (0, 0, 0): continue
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        q = (x + dx, y + dy)
                        if q not in fig and 0 <= q[0] < 64 and 0 <= q[1] < 64:
                            (a if lay == 'arms' else b).putpixel((ox + q[0], oy + q[1]), (0, 0, 0, 255)); fig[q] = (lay, (0, 0, 0)); n += 1
        b.save(D + st + '/body.png'); a.save(D + st + '/arms.png'); print(st, 'outline +', n)

# ---------- S/N (frontal views), after E/W approval (all six approved 2026-10-19) ----------
# arm: (angle, elbow angle or None, scale, fist) seen from the front (S) or behind (N); R = the character's right (rear)
# hand, on the viewer's left in S. Legs: 'plant' keeps the reference legs (bob rows dropped); crouched stances use
# band legs authored per view (hipRow = 40 + body bob; the ankle stays planted so the knee takes the bob).
GA = {'R': (10, 192, 1, 'up'), 'L': (-10, 168, 1, 'up')}                   # the approved boxing guard (S)
GN = {'R': (-12, None, 1, 'up'), 'L': (12, None, 1, 'up')}                 # its back view: upper arms only
MT_S = {'R': (55, 198, 1, 'up'), 'L': (-55, 162, 1, 'up')}                # Muay Thai: elbows out, gloves high at the cheeks
MT_N = {'R': (-55, 162, 1, 'up'), 'L': (55, 198, 1, 'up')}
CHAMBER_S = {'R': (14, -12, 0.85, 'up'), 'L': (-14, 12, 0.85, 'up')}      # fists pulled back to the hips
CHAMBER_N = {'R': (-18, None, 1, 'up'), 'L': (18, None, 1, 'up')}
FRONT = {
    'muayThaiGuard': dict(S=MT_S, N=MT_N, legs=dict(hip=(29, 35), knee=(25, 39), ankle=(26, 38)), lift={'L': ('mt-lead-up',)}),
    'karateGuard': dict(S={'R': CHAMBER_S['R'], 'L': (88, None, 0.45, 'front')}, N={'R': CHAMBER_N['R'], 'L': (-15, None, 1, 'up')}, legs='plant'),
    'horseStance': dict(S=CHAMBER_S, N=CHAMBER_N, legs=dict(hip=(27, 37), knee=(20, 44), ankle=(21, 43), kneeDy=3)),
    'judoGuard': dict(S={'R': (-20, None, 0.4, 'front'), 'L': (20, None, 0.4, 'front')}, N={'R': (-14, None, 1, 'up'), 'L': (14, None, 1, 'up')}, legs=dict(hip=(29, 35), knee=(25, 39), ankle=(23, 41), stagger=3)),
    'jiuJitsuGuard': dict(S={'R': (-20, None, 0.4, 'front'), 'L': (8, None, 0.6, 'front')}, N={'R': (-14, None, 1, 'up'), 'L': (10, None, 1, 'up')}, legs=dict(hip=(29, 35), knee=(24, 40), ankle=(23, 41), stagger=4)),
    'wrestlingGuard': dict(S={'R': (-20, None, 0.4, 'front'), 'L': (8, None, 0.6, 'front')}, N={'R': (-16, None, 1, 'up'), 'L': (12, None, 1, 'up')}, legs=dict(hip=(29, 35), knee=(22, 42), ankle=(22, 42), stagger=4)),
}

def frontal(st, spec):
    """S and N views on the guard's frontal template, one arm and leg set per stance (constant pose, the body bob
    from the E spec carries it)."""
    F = spec['frames']; cfg = FRONT[st]; fr = copy.deepcopy(GUARD['frontal']); dy = spec['bob']['dy']
    HA = load(D + 'heavyAttack.json')['legs']; spec['legs']['sections'] = copy.deepcopy(HA['sections'])
    for f, v in HA['feet'].items(): spec['legs']['feet'].setdefault(f, copy.deepcopy(v))
    rep = lambda v: [copy.deepcopy(v) for _ in range(F)]
    names = [q['name'] for q in spec['legs']['poses']]
    for d in ('S', 'N'):
        v = fr['views'][d]
        for key in ('handDy', 'hipDx', 'footDx'): v[key] = {'R': [0] * F, 'L': [0] * F}
        v['twist'] = {'pelvis': [0] * F, 'shoulders': [0] * F, 'head': [0] * F}
        v['legPose'] = {'R': ['plant'] * F, 'L': ['plant'] * F}
        for sd in ('R', 'L'):
            a, e, sc, fist = cfg[d][sd]; ab = v['armBand'][sd]
            ab['angle'] = [a] * F; ab['elbow'] = rep({'at': 7, 'angle': e} if e is not None else None)
            ab['scale'] = [sc] * F; ab['fist'] = [fist] * F; ab['pivotDx'] = [0] * F
            if d == 'N' and e is None: ab['showTo'] = 7
            elif d == 'N': ab.pop('showTo', None)
        sides = {'R': [False] * F, 'L': [False] * F}; pose = {'R': [None] * F, 'L': [None] * F}
        mx = (lambda x: x) if d == 'S' else (lambda x: 64 - x)
        def add(name, hip, knee, ankle, foot='sFoot'):
            if name not in names:
                spec['legs']['poses'].append({'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0],
                                              'kneeRow': knee[1], 'ankle': list(ankle), 'foot': foot, 'section': d}); names.append(name)
        L = cfg['legs']
        if isinstance(L, dict):   # crouched: both legs band legs, knees out over the feet
            for k in range(F):
                for i, sd in enumerate(('R', 'L')):
                    b = dy[k]; n = '%s-%s-%s%d' % (d, st, sd, b)
                    kr = 40 + b + L['kneeDy'] if 'kneeDy' in L else 46 + b // 2 + 2
                    back = (sd == 'R') == (d == 'S')   # the foot further from the viewer (rear foot in S, lead foot in N) sits higher: stagger depth
                    ar = 60 - (L.get('stagger', 0) if back else 0)
                    add(n, (mx(L['hip'][i]), 40 + b), (mx(L['knee'][i]), min(kr, ar - 4)), (mx(L['ankle'][i]), ar))
                    sides[sd][k] = True; pose[sd][k] = n
            v['bobRows'] = list(range(42, 42 + max(dy) + 2))
        for sd, lifted in (cfg.get('lift') or {}).items():   # the lead knee lift (Muay Thai): band leg on those frames
            far = [spec['legs']['poses'][i]['name'] for i in spec['legs']['far']]
            for k in range(F):
                if far[k] in lifted:
                    b = dy[k]; n = '%s-%s-lift%s%d' % (d, st, sd, b); x = mx(L['hip'][1] if isinstance(L, dict) else 35)
                    add(n, (x, 40 + b), (x - (1 if d == 'S' else -1), 42 + b), (x - (1 if d == 'S' else -1), 50 + b))   # knee up toward the viewer, shin hanging
                    sides[sd][k] = True; pose[sd][k] = n
        if any(sides['R']) or any(sides['L']):
            v['legBand'] = {'sides': sides, 'pose': pose, 'z': {'R': [2] * F, 'L': [2] * F}, 'offset': {'R': 0, 'L': 0}}
    fr['legLift'] = {'R': [0] * F, 'L': [0] * F}
    spec['frontal'] = fr; spec['directions'] = ['S', 'E', 'N', 'W']
    if any(cfg['S'][sd][3] == 'front' for sd in 'RL') and st != 'karateGuard':   # open hand, palm to the viewer (grappling stances seen from the front)
        spec['arms']['band']['fistFront'] = {'use': 'open hand seen from the front, palm toward the viewer, fingers up (grappling stance S view)', 'anchor': [2, 4],
                                            'rows': ['mLmL.', 'LLLLm', 'LLLLm', 'mLLLs', '.sDs.']}
    for g in ('S', 'N'): spec['clothing']['sash']['sway'][g] = (GUARD['clothing']['sash']['sway'][g] * F)[:F]
    spec['rootMotion']['S'] = [[0, 0]] * F; spec['rootMotion']['N'] = [[0, 0]] * F
    return spec

def specs4(only=None):
    """E/W specs plus S/N (status: S/N candidates)"""
    specs(only)
    for st in STANCES:
        if only and st not in only: continue
        sp = frontal(st, load(D + st + '.json'))
        for k in ('handDy', 'legRows', 'legRepeatRows', 'armRows', 'armRepeatRows'): pass
        sp['status'] = sp['status'].replace('S/N to author', 'S/N CANDIDATE 2026-10-19')
        save(sp, D + st + '.json')

if __name__ == '__main__':
    if '--four' in sys.argv: specs4([a for a in sys.argv[1:] if a != '--four'] or None); sys.exit()
    if '--outline' in sys.argv: outline([a for a in sys.argv[1:] if a != '--outline'] or None)
    else: specs(sys.argv[1:] or None)
