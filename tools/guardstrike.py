"""Ground Strike from the top of the Guard (move list 2026-11-26, thread "Animate new grappling escapes and transitions (part 2)").
CANDIDATE v1, E/W. The fighter in the guard (E, kneeling, guardTop) postures up out of the wrist control, cocks the near
fist and drives a straight punch down into the guard player's face (W, lying, guardBottom); both return to the Guard idle.
Rules: the guard player holds the plain guardBottom idle until the impact frame; the impact frame is held (impactHold 2),
has no smear and carries a hit star at the contact point.
usage: python3 -I guardstrike.py ['{json overrides}']   (writes specs into the playtest repo; render with tools/character-posed.mjs)"""
import copy, sys, json
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
sys.path.insert(0, '/home/claude/astro-fighters-playtest/tools')
from gen import build, save, load
from guardmoves import fr, F, band, withx, fxrec, D, GT, GB
CAND = 'E/W candidate v1 2026-11-27 ({}), awaiting user approval; S/N to author'
IMPACT = 3

def frames(V):
    g = lambda k, d: tuple(V.get(k, d))
    t = [fr(GT, k) for k in range(4)]
    b = [fr(GB, k) for k in range(4)]
    t0, b0 = t[0], b[0]
    cock = dict(bob=g('cb', (8, 7, 8)), lean=g('cl', (-1, -3)), an=band(*g('ca', (130, -170))), af=band(*g('cf', (-40, -60))))
    hit = dict(bob=g('hb', (13, 14, 17)), lean=g('hl', (2, 12)), an=band(*g('ha', (-50, -52))), af=band(*g('hf', (-34, -70))), expr='squint')
    rx = V.get('rx', 7)   # per-frame root step: the hips drive forward on the punch and settle back
    T = [t0,
         F(t0, bob=g('pb', (9, 8, 9)), lean=g('pl', (-1, -2)), an=band(*g('pa', (-60, -120))), af=band(-38, -70)),  # 1 postures up, breaks the wrist grip
         F(t0, **cock),                                                                                      # 2 fist cocked high
         F(t0, root=(rx, 0), **hit),                                                                         # 3 IMPACT: straight punch down to the face
         F(t0, **hit),                                                                                       # 4 impact held
         F(t0, bob=g('rb', (10, 10, 11)), lean=g('rl', (1, 4)), an=band(*g('ra', (-60, -120))), af=band(-36, -72), root=(-rx, 0)),  # 5 fist comes back
         F(t0, bob=(10, 10, 10), lean=(0, 2), an=band(-36, -72), af=band(-36, -76)),                         # 6 back on the wrists
         t[1], t[2], t[3]]
    pain = dict(lean=g('bl', (0, -2)), an=band(*g('ba', (-168, -172))), af=band(*g('bf', (-150, -160))), expr='pain')
    B = [b0, b[1], b[2],
         F(b0, **pain),                                                                                      # 3 IMPACT: head snaps back
         F(b0, **pain),                                                                                      # 4 held
         F(b0, lean=(0, -1), an=band(-56, -110), af=band(-48, -100), expr='squint'),                         # 5 hands come back up
         F(b0, an=band(-46, -80), af=band(-40, -70), expr='squint'),
         b[1], b[2], b[3]]
    return T, B

def run(V=None):
    V = V or {}
    T, B = frames(V)
    n = len(T); assert n == len(B)
    e = [{'frame': i, 'type': 'startup' if i < IMPACT else 'active' if i == IMPACT else 'recovery'} for i in range(n)]
    e[IMPACT].update({'move': 'Ground Strike', 'damage': 'strike', 'effect': 'punch from the top of the Guard; position unchanged (Guard)', 'impactHold': 2})
    ev = {'rule': 'per-frame gameplay data per facing; frame 3 is the impact (fist on the face), held on frame 4', 'E': e, 'W': copy.deepcopy(e)}
    lay = ['guardBottom far-arm', 'guardTop far-arm, body, clothing, hair, eyes', 'guardBottom body, clothing, hair, eyes', 'guardTop arms', 'guardBottom arms']
    pair = {'rule': 'paired Guard strike: the fighter in the guard (E) punches the guard player (W); the position does not change',
            'partnerDx': 12, 'layering': lay, 'mountLayering': {'fromFrame': 0, 'order': lay, 'bottomOver': True}}
    bx, by = V.get('fxB', [6, 52])
    fxB = {IMPACT: [('hitStar', [bx, by])], IMPACT + 1: [('hitStar', [bx, by])], IMPACT + 2: [('strain', [bx + 1, by - 2])]}
    t = build(withx(GT), 'guardGroundStrike', T, status=CAND.format('Ground Strike: Guard top, position unchanged'),
              intent='Ground Strike from the top of the Guard: postures up out of the wrist control, cocks the near fist high and on the impact frame 3 drives a straight punch down into the guard player\'s face (held on frame 4), brings the fist back and settles onto the wrists in the guardTop idle.',
              pair=dict(pair, partner='guardGroundStrikeHit', top='self'),
              clips={'rule': 'plays from guardTop; the guard player plays guardGroundStrikeHit on the same frames; returns to guardTop', 'guardGroundStrike': {'frames': list(range(n)), 'fps': 12, 'next': 'guardTop'}},
              events=ev, rmRule='in place', rotRule='kneeling upright throughout',
              fx=None)
    b = build(withx(GB), 'guardGroundStrikeHit', B, status=CAND.format('struck from the top of the Guard, position unchanged'),
              intent='The guard player, struck: holds the approved guardBottom idle until the impact frame 3, the head snaps back with the hands thrown up (held on frame 4), then the hands come back to the grips and it settles in the guardBottom idle. Legs stay locked around the waist.',
              pair=dict(pair, partner='guardGroundStrike', top='partner'),
              clips={'rule': 'plays on the guard player when the top fighter plays guardGroundStrike; returns to guardBottom', 'guardGroundStrikeHit': {'frames': list(range(n)), 'fps': 12, 'next': 'guardBottom'}},
              events=None, rmRule='in place', rotRule='quarter turns only: flat on the back (270) throughout',
              fx=fxrec(fxB, 'hit star at the face where the fist lands on the impact frame and the held frame (white, no element), strain lines as the head recovers'))
    save(t, D + 'guardGroundStrike.json'); save(b, D + 'guardGroundStrikeHit.json')
    return ['guardGroundStrike', 'guardGroundStrikeHit']

if __name__ == '__main__':
    print(' '.join(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else None)))
