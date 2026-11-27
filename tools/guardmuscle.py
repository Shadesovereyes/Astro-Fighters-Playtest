"""Muscle Out from the Guard (Christopher 2026-11-26 rulings: Muscle Out moves the defender ONE step back; Guard -> Free).
CANDIDATE v1, E/W. The guard player (W, lying, guardBottom) shoves the fighter in the guard (E, kneeling, guardTop) off:
foot on the hip + both hands on the chest, then both get back to their feet in the unarmed guard (Free).
Rules: the top fighter holds the plain guardTop idle until the impact frame; impact frame held, no smear, impact fx.
usage: python3 -I guardmuscle.py   (writes specs into the playtest repo; render with tools/character-posed.mjs)"""
import copy, sys
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import build, save, load
import guardmoves as gm
from guardmoves import fr, F, band, P, poses, withx, fxrec, D, GT, GB, MT, MB
CAND = 'E/W candidate v3 2026-11-27 ({}), awaiting user approval; S/N to author'
G = load(D + 'guard.json')
IMPACT = 2

def frames(V=None):
    V = V or {}
    g = lambda k, d: V.get(k, d)
    t0, b0, s0 = fr(GT), fr(GB), fr(G)
    s1, s2 = fr(G, 1), fr(G, 2)
    # top (E): kneeling in the guard -> shoved back -> stumbles up to the guard
    T = [t0, t0,
         F(t0, bob=(5, 5, 5), lean=(-3, -7), an=band(-100, -130), af=band(-110, -140), root=(-4, 0), expr='pain'),  # 2 IMPACT: both feet drive into the hips, lifted off the knees
         F(t0, bob=(5, 5, 5), lean=(-3, -7), an=band(-100, -130), af=band(-110, -140), expr='pain'),  # 3 held
         F(t0, bob=(8, 7, 8), lean=(-3, -6), an=band(-100, -130), af=band(-110, -140), root=(-5, 0), expr='pain', ln='up-near', lf='kneel-far'),  # 4 knocked back, a foot comes up
         F(s0, bob=(5, 4, 5), lean=(-2, -3), ln='guard-low-rear', lf='guard-low-lead', an=band(-60, -100), af=band(-70, -110), root=(-2, 0)),      # 5 stumbling up
         F(s0, bob=(3, 3, 3), lean=(-1, -1), ln='guard-low-rear', lf='guard-low-lead', root=(-2, 0)),  # 6 catches balance
         s1, s2, s0, s1, s2]
    # bottom (W): lying -> foot on the hip, hands frame -> shove -> sits up -> technical stand-up -> guard
    B = [b0,
         F(b0, ln='hip-near', lf='hip-far', an=band(*g('fa', (-44, -70))), af=band(*g('ff', (-40, -66))), expr='squint'),     # 1 legs open, foot to the hip, frames
         F(b0, ln='push-near', lf='push-far', an=band(*g('pa', (-40, -46))), af=band(*g('pf', (-36, -42))), expr='squint'),  # 2 IMPACT shove
         F(b0, ln='push-near', lf='push-far', an=band(*g('pa', (-40, -46))), af=band(*g('pf', (-36, -42))), expr='squint'),  # 3 held
         F(fr(MT), rot=(0, 0, 0, True), bob=tuple(V.get('b4', (12, 12, 17))), lean=tuple(V.get('l4', (0, -5))), ln='sit-near', lf='sit-far', an=band(*V.get('post', (25, 15))), af=band(-60, -90), root=(-9, 0)),   # 4 sits up, the back hand posts down behind the hips (Christopher 2026-11-27: no raised arm)
         F(fr(MT), rot=(0, 0, 0, True), bob=(10, 10, 10), lean=tuple(V.get('l5', (0, -4))), ln='kneel-near', lf='sit-far', an=band(*V.get('post5', V.get('post', (25, 15)))), af=band(-50, -90), root=(-2, 0)),   # 5 technical stand-up: post + knee
         F(s0, bob=(5, 5, 5), lean=(-1, 0), ln='guard-low-rear', lf='guard-low-lead', an=band(-60, -100), af=band(-70, -110), root=(-3, 0)),               # 6 rising, hands come up
         F(s0, bob=(3, 3, 3), ln='guard-low-rear', lf='guard-low-lead'),
         s0, s1, s2, s0]
    for b in B[6:]: b['expr'] = None
    return T, B

def run(V=None):
    V = V or {}
    T, B = frames(V)
    n = len(T); assert n == len(B)
    mo = [P('hip-near', 31, 40, *V.get('hk', [46, 42]), *V.get('ha', [44, 49]), 'pointDL'), P('push-near', 31, 40, *V.get('pk', [42, 46]), *V.get('pa2', [51, 51]), 'pointDL'), P('push-far', 30, 40, *V.get('fk', [41, 47]), *V.get('fa2', [50, 52]), 'pointDL'),
          P('up-near', 33, 52, 40, 48, 41, 57, 'levelR'), P('hip-far', 30, 40, *V.get('hk2', [45, 43]), *V.get('ha2', [43, 50]), 'pointDL')]
    e = [{'frame': i, 'type': 'startup' if i < IMPACT else 'active' if i == IMPACT else 'recovery'} for i in range(n)]
    e[IMPACT].update({'move': 'Muscle Out', 'damage': 'none', 'effect': 'escape one step back: Guard -> Free (both fighters stand in the guard)', 'impactHold': 2})
    ev = {'rule': 'per-frame gameplay data per facing; frame 2 is the impact (foot on the hip + two-hand shove), held on frame 3', 'E': e, 'W': copy.deepcopy(e)}
    lay = ['guardBottom far-arm', 'guardTop far-arm, body, clothing, hair, eyes', 'guardBottom body, clothing, hair, eyes', 'guardTop arms', 'guardBottom arms']
    lay2 = ['guardMuscleOutHit far-arm, body', 'guardMuscleOut far-arm, body', 'guardMuscleOutHit arms', 'guardMuscleOut arms']
    pair = {'rule': 'paired Guard escape: the guard player (W) shoves the fighter in the guard (E) off; from frame 4 they separate and both stand (Free)',
            'partnerDx': 12, 'layering': lay, 'mountLayering': {'fromFrame': 0, 'order': lay, 'bottomOver': True, 'untilFrame': 3, 'orderAfter': lay2}}
    BT = withx(GT); BT['legs']['poses'] += poses(MT, 'kneel-near', 'kneel-far') + poses(G, 'guard-low-lead', 'guard-low-rear', 'stance-lead', 'stance-rear') + [mo[3]]
    BB = withx(GB); BB['legs']['poses'] += poses(MT, 'kneel-near', 'kneel-far') + poses(G, 'guard-low-lead', 'guard-low-rear', 'stance-lead', 'stance-rear') + [p for p in gm.scissor()[3] if p['name'].startswith('sit')] + mo[:3] + mo[4:]
    for s in (BT, BB):
        seen = set(); s['legs']['poses'] = [p for p in s['legs']['poses'] if not (p['name'] in seen or seen.add(p['name']))]
    fxB = {1: [('swish', [40, 40])], 2: [('strain', [6, 49])], 3: [('strain', [6, 49])], 4: [('puff', [26, 60])], 5: [('puff', [36, 60])]}
    fxT = {2: [('hitStar', [35, 45]), ('shift', [22, 34])], 3: [('hitStar', [35, 45])], 4: [('lines', [44, 34])], 5: [('dustBig', [30, 62])], 6: [('speck', [20, 60])]}
    t = build(BT, 'guardMuscleOutHit', T, status=CAND.format('shoved out of the Guard: Guard top -> Free'),
              intent='The fighter in the guard, muscled out: holds the approved guardTop idle until the impact frame 2 (foot on the hip, both hands on the chest), is shoved back off the knees, a foot comes up, stumbles backward to the feet and settles into the unarmed guard.',
              pair=dict(pair, partner='guardMuscleOut', top='self'),
              clips={'rule': 'plays from guardTop; the guard player plays guardMuscleOut on the same frames; ends Free (next: guard)', 'guardMuscleOutHit': {'frames': list(range(n)), 'fps': 10, 'next': 'guard'}},
              events=None, rmRule='per-frame step (screen px): driven backward away from the guard player on frames 4-6',
              rotRule='upright throughout (kneeling to standing)',
              fx=fxrec(fxT, 'impact star at the hip/chest on the impact frame and a shift jolt; speed lines on the shove; dust as the feet land', top=True))
    b = build(BB, 'guardMuscleOut', B, status=CAND.format('Muscle Out: Guard bottom -> Free'),
              intent='Muscle Out from the bottom of the Guard (STR power escape, one step back = Free): chambers both knees and plants both feet on the top fighter\'s hips (hands framing), then on the impact frame 2 kicks both legs out straight and hard, lifting him off his knees and driving him back (Christopher 2026-11-27: push hard off him with the legs); sits up behind a posted hand and does a technical stand-up into the unarmed guard.',
              newPoses=(), pair=dict(pair, partner='guardMuscleOutHit', top='partner'),
              clips={'rule': 'plays from guardBottom; ends Free (next: guard, same facing)', 'guardMuscleOut': {'frames': list(range(n)), 'fps': 10, 'next': 'guard'}},
              events=ev, rmRule='per-frame step (screen px): scoots back as it sits up', rotRule='quarter turns only: flat on the back (270) to frame 3, upright (0) from frame 4',
              fx=fxrec(fxB, 'effort: hip swish as the foot comes up, strain on the shove, dust under the post and the stand-up'))
    for s in (t, b): s.pop('approved', None)
    save(t, D + 'guardMuscleOutHit.json'); save(b, D + 'guardMuscleOut.json')
    return ['guardMuscleOutHit', 'guardMuscleOut']

if __name__ == '__main__':
    import json
    print(' '.join(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else None)))
