"""Moves from the approved Guard (Christopher 2026-11-26, thread "Animate new grappling escapes and transitions").
CANDIDATES only, E/W. The guard player (W, lying) and the fighter in the guard (E, kneeling) as in guardBottom/guardTop.
  scissorSweep  Jiu-Jitsu Scissor Sweep: Guard bottom -> Mount top. The guard player pulls the collar, shin across the
                belly, chops the knee; the top fighter tips back onto his back; the sweeper sits up into Mount.
Rules: the target holds the plain guardTop idle until the impact frame; impact frame held, no smear, impact fx.
usage: python3 -I guardmoves.py   (writes specs into the playtest repo; render with tools/character-posed.mjs)"""
import json, copy, sys
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import build, save, load
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
CAND = 'E/W APPROVED by user 2026-11-26 19:14 ET (v1) ({}); S/N to author'
APPROVED = {'by': 'Christopher', 'at': '2026-11-26 19:14 ET (v1)', 'directions': ['E', 'W']}
band = lambda a, e: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
GT, GB, MT, MB = (load(D + n + '.json') for n in ('guardTop', 'guardBottom', 'mountTop', 'mountBottom'))
GH = load(D + 'mountBottomGarroteHit.json')
PAT = {k: GH['fx']['patterns'][k] for k in ('hitStar', 'strain', 'puff', 'speck', 'lines', 'tug', 'shift', 'dustBig')}
PAT['sweat'] = ['.#.', '#b#', '#W#', '.#.']
PAT['swish'] = ['..###.', '.#WWW#', '#W##..', '.#WWW#', '..###.']
FXPAL = {'W': '#ffffff', 'w': '#e3e3e3', '#': '#000000', 'b': '#bfe3ff'}
LIE = (270, 10, 0, True)

def fr(spec, k=0):
    P = [p['name'] for p in spec['legs']['poses']]
    br = spec.get('bodyRotation') or {}
    ex = (spec.get('expressions') or {}).get('frames', {}).get('E')
    d = dict(bob=(spec['bob']['dy'][k], spec['bob']['head'][k], spec['bob']['arms'][k]),
             lean=(spec['lean']['dx']['pelvis'][k], spec['lean']['dx']['head'][k]),
             ln=P[spec['legs']['near'][k]], lf=P[spec['legs']['far'][k]],
             an=copy.deepcopy(spec['arms']['near'][k]), af=copy.deepcopy(spec['arms']['far'][k]), expr=ex[k] if ex else None, root=(0, 0))
    d['rot'] = (br['angle'][k], br['dx'][k], br['dy'][k], br['groundSnap'][k]) if br else (0, 0, 0, False)
    return d
def F(base, **k): d = copy.deepcopy(base); d.update(k); return d
def poses(spec, *names): return [copy.deepcopy(p) for p in spec['legs']['poses'] if p['name'] in names]
def withx(s):
    s = copy.deepcopy(s)
    if not s.get('expressions'): s['expressions'] = copy.deepcopy(MB['expressions'])
    s['legs']['feet'].update({k: v for k, v in MT['legs']['feet'].items() if k not in s['legs']['feet']})
    return s
def fxrec(d, rule, top=False):
    r = {'rule': rule, 'frames': [{'frame': k, 'splash': [{'pattern': p, 'at': at_} for p, at_ in v]} for k, v in sorted(d.items())],
         'palette': FXPAL, 'patterns': PAT}
    if top: r['top'] = True
    return r
P = lambda name, hx, hr, kx, kr, ax, ar, foot: {'name': name, 'construction': 'band', 'hipX': hx, 'hipRow': hr, 'kneeX': kx, 'kneeRow': kr, 'ankle': [ax, ar], 'foot': foot}

def scissor():
    IMPACT = 2
    t0, b0 = fr(GT), fr(GB)            # approved Guard idle frame 0
    mt, mb = fr(MT), fr(MB)            # Mount idles (the end, roles swapped)
    # sweeper legs (lying frame, see positions.py): knee shield = near shin across the belly, chop = far leg flat on the floor at the knees
    sw = [P('shield-near', 31, 40, 44, 45, 41, 55, 'pointDL'),
          P('chop-far', 30, 40, 36, 48, 36, 58, 'pointDL'),
          P('kick-near', 31, 40, 47, 46, 49, 55, 'pointDR'),
          P('sit-near', 33, 52, 40, 48, 43, 56, 'toe30k'), P('sit-far', 31, 52, 37, 49, 40, 57, 'toe30k')]
    # top fighter (E): kneel -> tipped back -> flat on the back (270, head W) -> mountBottom
    T = [t0,                                                                     # 0 guard idle
         t0,                                                                     # 1 still the idle (no reaction before impact)
         F(t0, lean=(1, 4), an=band(-52, -80), af=band(-58, -86), expr='pain'),  # 2 IMPACT: collar yanked forward, knee chopped
         F(t0, lean=(1, 4), an=band(-52, -80), af=band(-58, -86), expr='pain'),  # 3 impact held
         F(t0, bob=(12, 12, 13), lean=(-2, -7), an=band(-120, -150), af=band(-110, -140), expr='pain'),   # 4 tipping back, arms flung
         F(mb, rot=(270, 4, 6, False), an=band(-150, -160), af=band(-140, -150), expr='pain'),           # 5 mid-fall (quarter turn)
         F(mb, rot=LIE, an=band(-110, -150), af=band(-100, -140), expr='pain'),                           # 6 lands flat, dust
         F(mb, an=band(-90, -150), af=band(-80, -140)),                                                    # 7
         F(mb, an=band(-74, -150), af=band(-64, -140)),                                                    # 8
         fr(MB, 0), fr(MB, 1), fr(MB, 2)]
    # guard player (W): grip + shrimp -> knee shield + chop -> scissor -> sit up -> kneel astride (mountTop)
    B = [b0,
         F(b0, ln='shield-near', lf='cg-far', an=band(-46, -100), af=band(-40, -90), root=(-1, 0), expr='squint'),   # 1 shrimp out, shin in
         F(b0, ln='shield-near', lf='chop-far', an=band(-20, -40), af=band(-14, -30), expr='squint'),               # 2 IMPACT: pull + chop
         F(b0, ln='shield-near', lf='chop-far', an=band(-20, -40), af=band(-14, -30), expr='squint'),               # 3 held
         F(b0, ln='kick-near', lf='chop-far', an=band(-10, -30), af=band(-6, -24), expr='squint'),                  # 4 scissor: shin lifts, chop sweeps
         F(b0, ln='kick-near', lf='lying-far', an=band(-60, -110), af=band(-54, -100)),                             # 5 follows the fall
         F(mt, rot=(0, 0, 0, True), bob=(12, 12, 12), lean=(-1, 2), ln='sit-near', lf='sit-far', an=band(-60, -90), af=band(-54, -84), root=(3, 0)),  # 6 sits up
         F(mt, bob=(11, 11, 12), lean=(0, 4), an=band(-40, -120), af=band(-50, -90), root=(4, 0)),           # 7 comes up to the knees
         F(mt, root=(3, 0)),                                                                                 # 8 astride
         fr(MT, 0), fr(MT, 1), fr(MT, 2)]
    return T, B, IMPACT, sw

def run():
    T, B, IMPACT, sw = scissor()
    n = len(T); assert n == len(B)
    e = [{'frame': i, 'type': 'startup' if i < IMPACT else 'active' if i == IMPACT else 'recovery'} for i in range(n)]
    e[IMPACT].update({'move': 'Scissor Sweep', 'damage': 'none', 'effect': 'sweep: the guard player ends Mounting (top), the swept fighter Mounted (bottom)', 'impactHold': 2})
    ev = {'rule': 'per-frame gameplay data per facing; frame 2 is the impact (collar pull + knee chop), held on frame 3', 'E': e, 'W': copy.deepcopy(e)}
    lay = ['guardBottom far-arm', 'guardTop far-arm, body, clothing, hair, eyes', 'guardBottom body, clothing, hair, eyes', 'guardTop arms', 'guardBottom arms']
    lay2 = ['scissorSweep (swept, now bottom) far-arm, body, clothing, hair, eyes', 'scissorSweepHit... sweeper (now top) far-arm, body, clothing, hair, eyes', 'swept arms', 'sweeper arms']
    pair = {'rule': 'paired Guard sweep: the guard player (W) sweeps the fighter in the guard (E); from frame 5 the roles swap and the pair ends in Mount with the sweeper on top',
            'partnerDx': 12, 'layering': lay, 'mountLayering': {'fromFrame': 0, 'order': lay, 'bottomOver': True, 'topSwapFrom': 5, 'orderFromSwap': lay2}}
    BT = withx(GT); BT['legs']['poses'] += poses(MB, 'lying-near', 'lying-far')
    BB = withx(GB); BB['legs']['poses'] += poses(MT, 'kneel-near', 'kneel-far') + sw
    fxB = {1: [('swish', [34, 46])], 2: [('strain', [6, 49]), ('puff', [38, 58])], 3: [('strain', [6, 49])], 4: [('swish', [44, 44]), ('strain', [6, 49])], 6: [('puff', [20, 60])]}
    fxT = {2: [('hitStar', [44, 56]), ('tug', [40, 34])], 3: [('hitStar', [44, 56])], 4: [('lines', [16, 34])], 6: [('dustBig', [28, 62]), ('puff', [50, 62])], 7: [('speck', [12, 60]), ('speck', [54, 60])]}
    t = build(BT, 'guardScissorSweepHit', T, status=CAND.format('swept: Guard top -> Mount bottom'),
              intent='The fighter in the guard, swept: holds the approved guardTop idle until the impact frame 2 (collar yanked forward, near knee chopped out), tips backward over the knee shield, a quarter turn onto the back (head to the back side) and settles into the mountBottom idle under the sweeper.',
              pair=dict(pair, partner='guardScissorSweep', top='self'),
              clips={'rule': 'plays from guardTop; the guard player plays guardScissorSweep on the same frames; ends Mounted (next: mountBottom)', 'guardScissorSweepHit': {'frames': list(range(n)), 'fps': 10, 'next': 'mountBottom'}},
              events=None, rmRule='in place', rotRule='quarter turns only: kneeling (0) to frame 4, a quarter turn backward (270) from frame 5, flat from 6',
              fx=fxrec(fxT, 'impact star at the chopped knee and a tug at the yanked collar on the impact frame; speed lines on the fall; dust where the back lands', top=True))
    b = build(BB, 'guardScissorSweep', B, status=CAND.format('Jiu-Jitsu Scissor Sweep: Guard bottom -> Mount top'),
              intent='Jiu-Jitsu Scissor Sweep from the bottom of the Guard: grips the collar and sleeve and shrimps out, slides the near shin across the belly (knee shield) with the far leg flat at the knees, then on the impact frame 2 yanks the top fighter forward and chops the knee; scissors the legs as he tips back, sits up after him and comes up to the knees astride (mountTop).',
              newPoses=(), pair=dict(pair, partner='guardScissorSweepHit', top='partner'),
              clips={'rule': 'plays from guardBottom; ends Mounting (next: mountTop, same facing)', 'guardScissorSweep': {'frames': list(range(n)), 'fps': 10, 'next': 'mountTop'}},
              events=ev, rmRule='per-frame step (screen px): slides toward the swept fighter\'s hips as it sits up',
              rotRule='quarter turns only: flat on the back (270) to frame 5, sits up (0) from frame 6',
              fx=fxrec(fxB, 'effort: hip swish on the shrimp and the scissor, strain on the pull, dust under the planted hip'))
    for s in (t, b): s.pop('approved', None)
    for sp in (t, b): sp['approved'] = APPROVED
    save(t, D + 'guardScissorSweepHit.json'); save(b, D + 'guardScissorSweep.json')
    return ['guardScissorSweepHit', 'guardScissorSweep']

if __name__ == '__main__':
    print(' '.join(run()))
