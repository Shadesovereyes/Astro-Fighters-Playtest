"""S/N (front/back) views of the approved stance strikes (Christopher 2026-10-20: E/W approved for Muay Thai, Karate Hammer
Fist / Side Kick / Sweeping Low, Judo Chop, Sumo Palm, Wrestler's Prowess). Each state's S/N base is its stance's approved
S/N view (stances.frontal), so every clip starts and ends on the approved stance front/back frame; the strike frames then
override the frontal arms (armBand: angle, forearm angle, scale, fist), the body twist and the kicking leg (legBand with
the approved kick-chain poses from heavyAttack, plus a few new ones). The target is toward the viewer in S and away in N.
E/W pixels are restored from HEAD after the render, so the approved side views never drift.
Run: python3 tools/strikes_sn.py [state..] ; node tools/character-posed.mjs male <state> ; python3 tools/strikes_sn.py --restore [state..]"""
import sys, copy, os, subprocess, io
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import load, save
import stances
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
HEAVY = load(D + 'heavyAttack.json')
STANCE = {'muayThai': 'muayThaiGuard', 'karate': 'karateGuard', 'judo': 'judoGuard', 'wrestling': 'wrestlingGuard'}
def stance_of(st): return next(v for k, v in STANCE.items() if st.startswith(k))
def mir(a): return None if a is None else ((-a) % 360 if (-a) % 360 <= 180 else (-a) % 360 - 360)
def mirror_arm(t):   # the same arm shape seen from behind: angles mirrored (N pivots are swapped by the template)
    a, e, sc, fist, *rest = t; return (-a, mir(e), sc, fist, *rest)
def leg(name, sec, hip, knee, ankle, foot): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'ankle': list(ankle), 'foot': foot, 'section': sec}
NEWLEGS = {   # S poses (N mirrored x -> 64 - x); rows at body dy 0, shifted by the frame's dy
    'mtround-R': ((30, 39), (36, 35), (45, 32), 'pointUR'),   # rib-height roundhouse: shin swung across at rib height, out past the far side (knee and foot on E's rows)
    'tchamber-L': ((34, 39), (33, 34), (33, 41), 'sFoot'),    # teep: far (lead) knee to the chest
    'teep-L': ((34, 39), (33, 36), (33, 40), 'sSole'),        # teep: the sole pushed out at the viewer, leg foreshortened
    'sweepmid-R': ((30, 40), (30, 47), (32, 53), 'sFoot'),    # sweep: rear foot coming through low
    'sweep-R': ((30, 40), (31, 47), (35, 54), 'sSole'),       # sweep: sole hooking across in front of the lead foot
    'smkick-R': ((30, 39), (29, 44), (29, 47), 'sFoot'),      # superman punch: rear leg kicked back away from the viewer, foreshortened behind the body
    'smair-L': ((34, 39), (35, 45), (35, 50), 'sFoot'),       # superman punch: lead leg tucked under the body in flight
}
NEWLEGS_N = {   # back-view poses that are not the S pose mirrored (as given, no x flip)
    'mtround-R': ((34, 39), (39, 35), (46, 32), 'pointUR'),   # seen from behind the rib-height shin swings out past the near side, visible beside the trunk (as heavyAttack's N round)
}
def legpose(spec, d, key, side, dy):
    if key in NEWLEGS:
        hip, knee, ank, foot = NEWLEGS_N[key] if d == 'N' and key in NEWLEGS_N else NEWLEGS[key]
        m = (lambda x: x) if d == 'S' or key in NEWLEGS_N else (lambda x: 64 - x)
        n = '%s-%s-d%d' % (d, key, dy)   # always rebuilt (the committed spec may hold an older version of the pose)
        spec['legs']['poses'] = [p for p in spec['legs']['poses'] if p['name'] != n]
        spec['legs']['poses'].append(leg(n, d, (m(hip[0]), hip[1] + dy), (m(knee[0]), knee[1] + dy), (m(ank[0]), ank[1] + dy), foot))
        return n
    n = '%s-%s-%s' % (d, key, side)   # approved heavyAttack kick-chain pose
    if n not in [p['name'] for p in spec['legs']['poses']]:
        spec['legs']['poses'].append(copy.deepcopy(next(p for p in HEAVY['legs']['poses'] if p['name'] == n)))
    return n

VARS = {'S-plantR1': {'plant': {'side': 'R', 'dx': 1}}, 'S-plantR': {'plant': {'side': 'R', 'dx': 2}},   # far-leg kicks: the rear (standing) leg moves under the body
        'air0': {'bob': 0},   # airborne frames: the front/back view keeps the body at bob 0 (the afro's top row is row 0, no room to rise)
        'N-plantR1': {'plant': {'side': 'R', 'dx': -1}}, 'N-plantR': {'plant': {'side': 'R', 'dx': -2}},
        # the trunk turned into a kick (Christopher 2026-10-20: heavyAttack's rotR/rotR2 drop up to 5 torso columns and the
        # turned trunk reads paper thin): the trunk keeps its depth, losing at most 1-2 far columns with the near side in
        # place, and the side turning away (screen right in both views) becomes the shaded side plane of the chest
        'S-turn1': {'rotate': {'center': 31, 'far': 'right', 'drop': {'torso': [34], 'pelvis': [35]}, 'nearDx': 0, 'headDx': 1, 'armDx': {'R': 0, 'L': -1}}, 'shade': {'from': 34, 'far': 'right'}},
        'S-turn2': {'rotate': {'center': 31, 'far': 'right', 'drop': {'torso': [33, 34], 'pelvis': [34, 36]}, 'nearDx': 0, 'headDx': 1, 'armDx': {'R': 0, 'L': -2}}, 'shade': {'from': 32, 'far': 'right'}},
        'N-turn1': {'rotate': {'center': 31, 'far': 'right', 'drop': {'torso': [34], 'pelvis': [35]}, 'nearDx': 0, 'headDx': 1, 'armDx': {'L': 0, 'R': -1}}, 'shade': {'from': 34, 'far': 'right'}},
        'N-turn2': {'rotate': {'center': 31, 'far': 'right', 'drop': {'torso': [33, 34], 'pelvis': [34, 36]}, 'nearDx': 0, 'headDx': 1, 'armDx': {'L': 0, 'R': -2}}, 'shade': {'from': 32, 'far': 'right'}}}
# per state: {frame: overrides}, S semantics. R/L arm = (angle, forearm angle or None, scale, fist[, elbowAt]); NR/NL
# explicit back view (default: mirror of the S arm, at the back view's depth); tw = (pelvis, shoulders, head) twist
# (N negated); kick = (side, pose key); var = heavyAttack part variants (S- names, N- swapped in); z = kick leg depth
JAB_S = (88, None, 0.45, 'front'); CROSS_S = (-88, None, 0.45, 'front')
SN = {
 'muayThaiJabCross': {1: dict(L=JAB_S, NL=(-15, None, 1, 'up'), pdx={'L': -1}, tw=(-1, -2, -1)), 2: dict(L=(-40, 170, 0.85, 'up'), tw=(0, -1, 0)),
                      4: dict(R=(18, 192, 1, 'up'), tw=(0, -1, 0)), 5: dict(R=CROSS_S, NR=(15, None, 1, 'up'), pdx={'R': 1}, tw=(2, 3, 2)), 6: dict(R=(25, 190, 0.85, 'up'), tw=(1, 1, 1))},
 'muayThaiUppercut': {1: dict(R=(25, 150, 1, 'up'), tw=(0, -1, 0)), 2: dict(R=(-5, 185, 1, 'up'), tw=(1, 1, 1)), 3: dict(R=(-30, 192, 0.9, 'up'), pdx={'R': 1}, tw=(1, 2, 1)),
                      4: dict(R=(-10, 195, 1, 'up'), tw=(1, 1, 1))},
 'muayThaiCalfKick': {1: dict(lift=('R', 50), var=['S-hikeR1', 'bend1', 'S-plantL1']), 2: dict(R=(30, 15, 1, 'up'), kick=('R', 'low'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(-1, 1, 2)),
                      3: dict(lift=('R', 49), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(0, 1, 1))},
 'muayThaiRoundhouse': {1: dict(R=(25, 185, 1, 'up'), lift=('R', 50), var=['S-hikeR1', 'bend1', 'S-plantL1']),
                        2: dict(R=(35, 60, 1, 'up'), lift=('R', 40), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(1, -1, -1)),
                        3: dict(R=(70, 60, 1, 'up'), kick=('R', 'mtround-R'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn2', 'S-plantL'], tw=(1, 2, 2)),
                        4: dict(R=(70, 60, 1, 'up'), kick=('R', 'mtround-R'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn2', 'S-plantL'], tw=(1, 2, 2)),
                        5: dict(R=(30, 70, 1, 'up'), lift=('R', 40), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(0, -1, -1)),
                        6: dict(R=(25, 190, 1, 'up'), lift=('R', 50), var=['S-hikeR1', 'bend1', 'S-plantL1'])},
 'muayThaiTeep': {1: dict(lift=('L', 39), var=['bend1', 'S-plantR1']), 2: dict(kick=('L', 'teep-L'), var=['bend2', 'S-kneeR', 'S-plantR']),
                  3: dict(kick=('L', 'teep-L'), var=['bend2', 'S-kneeR', 'S-plantR']), 4: dict(lift=('L', 39), var=['bend1', 'S-plantR1'])},
 'muayThaiKnee': {1: dict(R=(25, 178, 1, 'up'), L=(-25, 182, 1, 'up'), lift=('R', 50), var=['S-hikeR1', 'bend1', 'S-plantL1']),
                  2: dict(R=(30, 170, 0.9, 'up'), L=(-30, 190, 0.9, 'up'), lift=('R', 43), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-plantL'], tw=(0, 1, 0)),
                  3: dict(R=(20, 215, 0.85, 'up'), L=(-20, 145, 0.85, 'up'), lift=('R', 40), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(1, 1, 0)),
                  4: dict(R=(20, 215, 0.85, 'up'), L=(-20, 145, 0.85, 'up'), lift=('R', 40), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(1, 1, 0)),
                  5: dict(lift=('R', 50), var=['S-hikeR1', 'bend1', 'S-plantL1'])},
 'muayThaiElbow': {1: dict(R=(45, 200, 1, 'up'), tw=(0, -1, 0)), 2: dict(R=(-70, 140, 0.8, 'up'), pdx={'R': 1}, tw=(2, 3, 2)), 3: dict(R=(-72, 138, 0.8, 'up'), pdx={'R': 1}, tw=(2, 3, 2)),
                   4: dict(R=(25, 195, 0.9, 'up'), tw=(1, 1, 1))},
 'karateHammerFist': {1: dict(R=(150, 175, 1, 'up'), tw=(0, -1, 0)), 2: dict(R=(170, 190, 1, 'up'), L=(40, None, 0.6, 'front'), tw=(0, 0, 0)),
                      3: dict(R=(-110, -10, 0.65, 'up'), L=(-14, 12, 0.85, 'up'), pdx={'R': 1}, tw=(1, 2, 1)), 4: dict(R=(-108, -8, 0.65, 'up'), L=(-14, 12, 0.85, 'up'), pdx={'R': 1}, tw=(1, 2, 1)),
                      5: dict(R=(20, -40, 0.9, 'up'), L=(50, None, 0.5, 'front'))},
 'karateBlitz': {1: dict(R=(14, -12, 0.85, 'up'), L=(-14, 12, 0.85, 'up'), tw=(0, -1, 0)),
                 2: dict(R=(60, 190, 1, 'up'), L=(-14, 12, 0.85, 'up'), kick=('R', 'smkick-R'), kz=0, kick2=('L', 'smair-L'), var=['air0'], tw=(0, -1, -1)),
                 3: dict(R=CROSS_S, NR=(15, None, 1, 'up'), L=(-14, 12, 0.85, 'up'), pdx={'R': 1}, kick=('R', 'smkick-R'), kz=0, kick2=('L', 'smair-L'), var=['air0'], tw=(2, 3, 2)),
                 4: dict(R=CROSS_S, NR=(15, None, 1, 'up'), L=(-14, 12, 0.85, 'up'), pdx={'R': 1}, tw=(1, 2, 1)),
                 5: dict(R=(14, -12, 0.85, 'up'))},
 'karateSideKick': {1: dict(kick=('R', 'lift'), var=['S-hikeR1', 'bend1', 'S-plantL1']), 2: dict(kick=('R', 'chamber'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(0, 1, 1)),
                    3: dict(kick=('R', 'snap'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn2', 'S-plantL'], tw=(1, 2, 2)), 4: dict(kick=('R', 'snap'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn2', 'S-plantL'], tw=(1, 2, 2)),
                    5: dict(kick=('R', 'chamber'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-turn1', 'S-plantL'], tw=(0, 1, 1)), 6: dict(kick=('R', 'lift'), var=['S-hikeR1', 'bend1', 'S-plantL1'])},
 'karateWhirlwind': {4: dict(R=(22, 200, 1, 'up'), L=(-30, 190, 1, 'up'), kick=('R', 'round'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-rotR2', 'S-plantL'], tw=(1, -2, -2)),   # spin frames 1-3: heavyAttack's S/N spin bodies (BORROW_SN)
                     5: dict(kick=('R', 'fold'), var=['S-hikeR', 'bend2', 'S-kneeL', 'S-rotR2', 'S-plantL'], tw=(0, -1, -1))},
 'karateSweepingLow': {2: dict(kick=('R', 'sweepmid-R'), var=['S-plantL1']), 3: dict(L=(50, None, 0.6, 'front'), kick=('R', 'sweep-R'), var=['S-turn1', 'S-plantL'], tw=(1, 1, 0)),
                       4: dict(L=(50, None, 0.6, 'front'), kick=('R', 'sweep-R'), var=['S-turn1', 'S-plantL'], tw=(1, 1, 0)), 5: dict(kick=('R', 'sweepmid-R'), var=['S-plantL1'])},
 'judoChop': {1: dict(R=(150, 195, 1, 'front'), tw=(0, -1, 0)), 2: dict(R=(170, 200, 1, 'front'), tw=(0, -1, 0)),
              3: dict(R=(-120, -30, 0.6, 'front'), L=(10, None, 0.3, 'front'), pdx={'R': 1}, tw=(1, 2, 1)), 4: dict(R=(-118, -25, 0.6, 'front'), L=(10, None, 0.3, 'front'), pdx={'R': 1}, tw=(1, 2, 1))},
 'wrestlingSumoPalm': {1: dict(R=(30, -100, 0.75, 'front', 9)), 2: dict(R=(-82, None, 0.3, 'front'), NR=(20, None, 1, 'up'), pdx={'R': 1}, tw=(1, 2, 1)),
                       3: dict(R=(30, -100, 0.75, 'front', 9), L=(-30, 100, 0.75, 'up', 10)), 4: dict(L=(82, None, 0.3, 'up'), NL=(-20, None, 1, 'up'), pdx={'L': -1}, tw=(-1, -2, -1))},
 'wrestlingProwess': {k: dict(R=(25, -85, 1, 'front', 8), L=(-25, 85, 1, 'up', 8), NR=(-50, None, 1, 'up'), NL=(50, None, 1, 'up')) for k in (3, 4, 5, 6)} | {
                      2: dict(R=(40, -60, 0.9, 'front', 8), L=(-40, 60, 0.9, 'up', 8), NR=(-45, None, 1, 'up'), NL=(45, None, 1, 'up'))},
}

# spin clips: the front/back views turn through other bodies (spinPivot frames), copied from heavyAttack's spinRoundhouse
# borrow.byDirection (heavyAttack frame -> this state's frame)
BORROW_SN = {'karateWhirlwind': {10: 1, 11: 2, 12: 3}}

# knee lifts and chambers (Christopher 2026-10-20: the guard's knee-lift logic carried into the Muay Thai abilities): the
# reference trouser leg stays in place, its hem and sock rise to E's rows by projection (hem outline on hemOut, sock the
# 3 rows below it, the shoe pointing down for 5 rows with its outline on E's toe row); a knee chambered high (up >= 13)
# keeps 4 trouser rows above the hem as the knee block and, in S, comes in front of the torso
SOCK_X = {('S', 'L'): 37, ('S', 'R'): 21, ('N', 'L'): 21, ('N', 'R'): 37}   # the sock's left outline column (output)
SAMPLE = {('S', 'L'): {'#': [36, 61], 's': [37, 61]}, ('S', 'R'): {'#': [21, 61], 's': [23, 61]},
          ('N', 'L'): {'#': [21, 61], 's': [23, 61]}, ('N', 'R'): {'#': [35, 61], 's': [37, 61]}}
FOOT_OUT = {'right': ['#sss#.', '#ssss#', '#ssss#', '#ssss#', '.#ss#.', '..##..'], 'left': ['.#sss#', '#ssss#', '#ssss#', '#ssss#', '.#ss#.', '..##..']}
def lift_variant(d, side, hemOut):
    up = 56 - hemOut; out = 'right' if (d, side) in (('S', 'L'), ('N', 'R')) else 'left'
    t = {'side': side, 'hem': 54, 'up': up, 'shoe': 60, 'keep': 4 if up >= 13 else 0,
         'foot': {'at': [SOCK_X[d, side] - (1 if out == 'left' else 0), hemOut + 4], 'sample': SAMPLE[d, side], 'rows': FOOT_OUT[out]}}
    if d == 'S' and up >= 13: t['z'] = 4
    return {'tiptoe': t}

SN_APPROVED = {s: 'S/N approved by user 2026-10-20 (v1, b24f8f0)' for s in ('karateHammerFist', 'judoChop', 'wrestlingProwess')} | {'karateBlitz': 'S/N approved by user 2026-10-20 (v2 with motion blur, c46b181)', 'karateWhirlwind': 'S/N approved by user 2026-10-20 (v1 with swing arc, 31fb396)'}

def sn(state):
    import json   # always from the committed E/W spec, so reruns start clean
    spec = json.loads(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + os.path.relpath(D + state + '.json', R)])); st = stance_of(state); F = spec['frames']
    spec = stances.frontal(st, spec); fr = spec['frontal']; dy = spec['bob']['dy']
    ov = SN[state]
    # the Muay Thai lead heel stays up (tiptoe) only on frames where E's lead foot is still on its toes (toe60); it comes
    # down flat with the strike (Christopher 2026-10-20)
    lead = [spec['legs']['poses'][i] for i in spec['legs']['far']]
    for d in ('S', 'N'):
        for k, vs in fr['views'][d]['variants'].items():
            if lead[int(k)].get('foot') != 'toe60': vs[:] = [n for n in vs if 'tiptoe' not in fr['partVariants'].get(n, {})]
    for d in ('S', 'N'):
        v = fr['views'][d]; ab = v['armBand']; sg = 1 if d == 'S' else -1
        ext = lambda rows, src: src[:len(rows) + 3] if rows == src[:len(rows)] else rows   # room for the kick variants' standing-leg bend (bend2)
        v['bobRows'] = ext(v['bobRows'], stances.CROUCH_ROWS) if isinstance(v['bobRows'], list) else {sd: ext(r, stances.NEAR_ROWS if r == stances.NEAR_ROWS[:len(r)] else stances.CROUCH_ROWS) for sd, r in v['bobRows'].items()}
        for k, o in ov.items():
            for sd in 'RL':
                t = o.get('N' + sd) if d == 'N' and ('N' + sd) in o else (o.get(sd) if d == 'S' else (mirror_arm(o[sd]) if sd in o else None))
                if t is None: continue
                a, e, sc, fist, *eat = t; b = ab[sd]
                b['angle'][k] = a; b['scale'][k] = sc; b['fist'][k] = fist
                b['elbow'][k] = {'at': eat[0] if eat else 7, 'angle': e} if e is not None else None
                if d == 'N':   # back view: per-frame showTo (upper arm only when straight and pointing away)
                    sh = b.get('showTo'); sh = sh if isinstance(sh, list) else [sh] * F
                    sh[k] = 7 if e is None else None; b['showTo'] = sh
                if 'pdx' in o and sd in o['pdx']: b['pivotDx'][k] = sg * o['pdx'][sd]
            if 'tw' in o:
                for i, part in enumerate(('pelvis', 'shoulders', 'head')): v['twist'][part][k] += sg * o['tw'][i]
                for sd in 'RL': v['hipDx'][sd][k] += sg * o['tw'][0]
            for kk in ('kick', 'kick2'):
                if kk not in o: continue
                side, key = o[kk]
                lb = v.setdefault('legBand', {'sides': {'R': [False] * F, 'L': [False] * F}, 'pose': {'R': [None] * F, 'L': [None] * F},
                                              'z': {'R': [3.5 if d == 'S' else 1.5] * F, 'L': [3.5 if d == 'S' else 1.5] * F}, 'offset': {'R': 0, 'L': 0}})
                lb['sides'][side][k] = True; lb['pose'][side][k] = legpose(spec, d, key, side, max(dy[k], 0) - 1)
                v['legPose'][side][k] = 'plant'
                if kk == 'kick' and 'kz' in o: lb['z'][side][k] = o['kz'] if d == 'S' else 3.5 - o['kz']   # behind the body in S, in front in N
            if 'var' in o:
                v['variants'][str(k)] = [n.replace('S-', d + '-', 1) for n in o['var']]
                for n in v['variants'][str(k)]:
                    if n not in fr['partVariants']: fr['partVariants'][n] = copy.deepcopy(HEAVY['frontal']['partVariants'].get(n) or VARS[n])
            if 'lift' in o:   # knee raised in front: the reference trouser leg, risen and foreshortened (stances tiptoe)
                side, hemOut = o['lift']; tv = lift_variant(d, side, hemOut); n = '%s-lift%s%d' % (d, side, hemOut)
                fr['partVariants'][n] = tv; v['variants'].setdefault(str(k), []).append(n)
    if state in BORROW_SN:
        hb = HEAVY['borrow']['byDirection']
        spec['borrow']['byDirection'] = {d: {str(BORROW_SN[state][int(k)]): copy.deepcopy(b) for k, b in hb[d].items()} for d in ('S', 'N')}
    spec['status'] = spec['status'].replace('S/N to author', SN_APPROVED.get(state, 'S/N CANDIDATE 2026-10-20'))
    save(spec, D + state + '.json'); print(state, 'S/N', F, 'frames')

def restore(state):
    """the approved E/W pixels from HEAD into the E and W rows of the new 4-row sheets (S, E, N, W)"""
    from PIL import Image
    d = D + state + '/'
    for f in sorted(os.listdir(d)):
        if not f.endswith('.png'): continue
        rel = os.path.relpath(d + f, R)
        try: old = Image.open(io.BytesIO(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + rel], stderr=subprocess.DEVNULL))).convert('RGBA')
        except subprocess.CalledProcessError: continue
        new = Image.open(d + f).convert('RGBA')
        if new.height < 256: new = Image.new('RGBA', (old.width, 256))   # a post-render layer (fx) the renderer did not rewrite
        for row, nrow in (((0, 1), (1, 3)) if old.height < 256 else ((1, 1), (3, 3))):   # old E, W (2-row E/W sheet or 4-row S, E, N, W) -> new rows E, W
            new.paste(Image.new('RGBA', (new.width, 64)), (0, nrow * 64)); new.paste(old.crop((0, row * 64, old.width, row * 64 + 64)), (0, nrow * 64))
        new.save(d + f)
    print(state, 'E/W restored from HEAD')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SN)
    for s in args: (restore if '--restore' in sys.argv else sn)(s)
