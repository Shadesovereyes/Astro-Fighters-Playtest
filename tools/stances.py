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
# Legs (second pass, Christopher 2026-10-20: the band legs and trouser seat read wide and blocky): the reference
# trouser legs and pelvis as in the approved S/N views (guard, block, weave, the kick chain), bent with the approved
# vocabulary only: every leg drops the body bob's rows from the thigh (a crouching thigh foreshortens toward the
# viewer), footDx spreads the feet (a shear from the hip to the foot), the knee variant pushes each knee out (dx at
# the knee, 0 at hip and ankle), and the far foot (rear in S, lead in N) drops 'stagger' more rows so it sits higher.
# foot: feet spread px per side; knee: knee dx per side (R, L in S); farKnee: extra knee dx on the far leg.
CROUCH_ROWS = [49, 53, 47, 52, 45, 54, 48, 51, 46, 55, 44]   # thigh and shin rows alternately, so the knee stays mid-leg
NEAR_ROWS = [47, 45, 49, 43, 48, 53, 46, 44, 52, 42]   # a knee coming toward the viewer: mostly thigh rows
HIPS = (26, 36)   # Muay Thai lead knee lift (band leg) hip columns
GR_N = lambda r, l: {'R': (-r, None, 1, 'up'), 'L': (l, None, 1, 'up')}          # back view: elbows bent out to the sides
def GR_S(r, l, a=14): return {'R': (-a, None, r, 'front'), 'L': (a, None, l, 'front')}   # two open hands in front of the shoulders
FRONT = {
    'muayThaiGuard': dict(S=MT_S, N=MT_N, legs=dict(foot=1, knee=(1, 1)), lift={'L': ('mt-lead-up',)}),
    'karateGuard': dict(S={'R': CHAMBER_S['R'], 'L': (68, None, 0.42, 'front')}, N={'R': CHAMBER_N['R'], 'L': (10, None, 1, 'up')},
                        legs=dict(foot=0, knee=(0, 0), near=2, far=0, nearKnee=1, stagger=4), blade=1),   # staggered like the grappling stances, no knee flare (Christopher 2026-10-20)
    'horseStance': dict(S=CHAMBER_S, N=CHAMBER_N, legs=dict(foot=2, knee=(6, 6))),
    'judoGuard': dict(S=GR_S(0.25, 0.28), N=GR_N(32, 32), legs=dict(foot=0, knee=(0, 0), near=1, far=0, nearKnee=1, stagger=2), lean=(1, 0), blade=1, headUp=1),
    'jiuJitsuGuard': dict(S=GR_S(0.25, 0.6), N=GR_N(30, 38), legs=dict(foot=0, knee=(0, 0), near=1, far=-1, nearKnee=1, stagger=3), lean=(2, 0), rise=3, blade=1, headUp=1),
    'wrestlingGuard': dict(S={'R': (40, 0, 0.7, 'front'), 'L': (-40, 0, 0.7, 'front')}, N=GR_N(40, 40), legs=dict(foot=0, knee=(0, 0), near=0, far=-1, nearKnee=0, stagger=3), lean=(1, 0), rise=3, blade=1, headUp=1),
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
        mx = (lambda x: x) if d == 'S' else (lambda x: 62 - x)
        def add(name, hip, knee, ankle, foot='sFoot'):
            if name not in names:
                spec['legs']['poses'].append({'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0],
                                              'kneeRow': knee[1], 'ankle': list(ankle), 'foot': foot, 'section': d, 'crease': True}); names.append(name)
        L = cfg['legs']; sg = 1 if d == 'S' else -1; mb = max(dy)
        farSd = 'R' if d == 'S' else 'L'
        v['legPose'] = {sd: ['far' if sd == farSd and L.get('stagger') else 'plant'] * F for sd in 'RL'}
        v['legPoseRows'] = {'plant': [], 'far': CROUCH_ROWS[mb:mb + L.get('stagger', 0)]}
        v['bobRows'] = CROUCH_ROWS[:mb]
        v['hipDx'] = {'R': [0] * F, 'L': [0] * F}
        v['footDx'] = {'R': [-sg * L['foot']] * F, 'L': [sg * L['foot']] * F}
        v['legPivot'] = 39; v['footFrom'] = {'R': 56, 'L': 56}
        pv = fr.setdefault('partVariants', {}); vs = []
        for i, sd in enumerate('RL'):
            kd = L['knee'][i] + (L.get('farKnee', 0) if sd == farSd else 0)
            if kd:
                out = (-1 if sd == 'R' else 1) * sg   # two overlapping knee shears (peaks at rows 46 and 51) round the knee off
                for j, (dk, kr) in enumerate(((kd - kd // 2, 46), (kd // 2, 51))):
                    if dk: n = '%s-%s-knee%s%d' % (d, st, sd, j); pv[n] = {'knee': {'side': sd, 'dx': out * dk, 'rows': [41, kr, 57]}}; vs.append(n)
        if L.get('near'):   # staggered stance seen head-on (Christopher 2026-10-20: wrestling read as a sumo straddle)
            # feet about shoulder width, legs near vertical like the approved guard; the near leg's knee comes toward the
            # viewer, so its crouch rows come out of the thigh; the far leg stays long and straight, tucked toward the
            # centre behind the near leg, its foot 'stagger' rows higher; knees only slightly out, peaking above the
            # knee so the trouser bottoms do not flare
            nearSd = 'L' if d == 'S' else 'R'; b0 = mb - cfg.get('rise', 0); vs = []
            v['crouch'] = -cfg.get('rise', 0); v['bobRows'] = {nearSd: NEAR_ROWS[:mb], farSd: CROUCH_ROWS[:mb]}
            v['legPoseRows']['far'] = CROUCH_ROWS[b0:b0 + L['stagger']]
            out = lambda sd, n: (-1 if sd == 'R' else 1) * sg * n
            v['footDx'] = {nearSd: [out(nearSd, L['near'])] * F, farSd: [out(farSd, L['far'])] * F}
            for sd, kd in ((nearSd, L['nearKnee']), (farSd, L.get('farKnee', 0))):
                if kd: n = '%s-%s-knee%s' % (d, st, sd); pv[n] = {'knee': {'side': sd, 'dx': out(sd, kd), 'rows': [41, 47, 56]}}; vs.append(n)
        v['variants'] = {str(k): list(vs) for k in range(F)}
        if cfg.get('rise') and not L.get('near'):   # the view's body sits this many rows higher than E's deep crouch (Christopher 2026-10-20: legs too squashed)
            v['crouch'] = -cfg['rise']; v['bobRows'] = CROUCH_ROWS[:mb - cfg['rise']]
            v['legPoseRows']['far'] = CROUCH_ROWS[mb - cfg['rise']:mb - cfg['rise'] + L.get('stagger', 0)]
        td, hd = cfg.get('lean', (0, 0))
        if td: v['torsoDrop'] = td
        if hd: v['headDy'] = (v.get('headDy') or 0) + hd + (1 if d == 'N' else 0)
        if cfg.get('headUp'):   # the head keeps its place on the neck through the bob (Christopher 2026-10-20: head tucked into the body)
            hb = spec['bob'].get('head') or dy; v['headDy'] = [(v.get('headDy') or 0) - (hb[k] - dy[k]) for k in range(F)]
        bl = cfg.get('blade', 0)
        if bl: v['twist'] = {'pelvis': [0] * F, 'shoulders': [-bl if d == 'S' else bl] * F, 'head': [-bl if d == 'S' else bl] * F}
        for sd, lifted in (cfg.get('lift') or {}).items():   # the lead knee lift (Muay Thai): band leg on those frames
            far = [spec['legs']['poses'][i]['name'] for i in spec['legs']['far']]
            for k in range(F):
                if far[k] in lifted:
                    b = dy[k]; n = '%s-%s-lift%s%d' % (d, st, sd, b); x = mx(HIPS[1])
                    add(n, (x, 40 + b), (x - (1 if d == 'S' else -1), 42 + b), (x - (1 if d == 'S' else -1), 50 + b))   # knee up toward the viewer, shin hanging
                    sides[sd][k] = True; pose[sd][k] = n
        if any(sides['R']) or any(sides['L']):
            v['legBand'] = {'sides': sides, 'pose': pose, 'z': {'R': [2] * F, 'L': [2] * F}, 'offset': {'R': 0, 'L': 0}}
    fr['legLift'] = {'R': [0] * F, 'L': [0] * F}
    spec['frontal'] = fr; spec['directions'] = ['S', 'E', 'N', 'W']
    if st == 'karateGuard':   # the lead fist punching toward the viewer, large in the middle of the chest
        spec['arms']['band']['fistFront'] = {'use': 'karate lead fist seen knuckles-on, held out toward the viewer in the middle of the chest (S view)', 'anchor': [2, 2],
                                            'rows': ['.mLm.', 'mLLLm', 'mLLLs', 'sLLms', '.sDs.']}   # small solid fist, no finger lines (Christopher 2026-10-20)
    elif any(cfg['S'][sd][3] == 'front' for sd in 'RL'):   # open hand, palm to the viewer (grappling stances seen from the front)
        spec['arms']['band']['fistFront'] = {'use': 'open hand seen from the front, palm toward the viewer, fingers up (grappling stance S view)', 'anchor': [2, 4],
                                            'rows': ['mLmL.', 'LLLLm', 'LLLLm', 'mLLLs', '.sDs.']}
    for g in ('S', 'N'): spec['clothing']['sash']['sway'][g] = (GUARD['clothing']['sash']['sway'][g] * F)[:F]
    spec['rootMotion']['S'] = [[0, 0]] * F; spec['rootMotion']['N'] = [[0, 0]] * F
    return spec

SN_APPROVED = {'karateGuard': 'S/N approved by user 2026-10-20 (v7, 5351ccd)'}

def specs4(only=None):
    """E/W specs plus S/N (status: S/N candidates)"""
    specs(only)
    for st in STANCES:
        if only and st not in only: continue
        sp = frontal(st, load(D + st + '.json'))
        for k in ('handDy', 'legRows', 'legRepeatRows', 'armRows', 'armRepeatRows'): pass
        sp['status'] = sp['status'].replace('S/N to author', SN_APPROVED.get(st, 'S/N CANDIDATE 2026-10-19'))
        save(sp, D + st + '.json')

if __name__ == '__main__':
    if '--four' in sys.argv: specs4([a for a in sys.argv[1:] if a != '--four'] or None); sys.exit()
    if '--outline' in sys.argv: outline([a for a in sys.argv[1:] if a != '--outline'] or None)
    else: specs(sys.argv[1:] or None)
