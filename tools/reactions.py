"""Reaction band defender clips (Christopher 2026-11-26 18:48: "the actual player animations need to differ depending on if
an ability is slipped checked, parried, caught, or a critical ... respect weather the ability was a punch, kick ... as well as
if the strike was high mid or low"; 18:50: the animations should make the arena words unnecessary, the combat log keeps them).

One state per reaction x weapon x height. Each is a target state: frame 0 is the attacker's impact frame (the defender holds
its plain guard until then, ANIMATION_RULES 2026-11-04), played from the approved guard and returning to it. E/W first
(W mirrors E), S/N after approval. Effects white/neutral. Torso shear capped at 4 px (head dx - pelvis dx).

Heights (testbed table): high = Jab-Cross, Haymaker, Uppercut, Hammer Fist, Judo Chop, Elbow Strike, Karate Blitz, Sumo Palm;
mid = Body Shot, Knee Strikes, Teep Kick, Side Kick, Roundhouse Kick; low = Calf Kick, Sweeping Low.

  slipHigh          straight punch, high, middle third: head rolls down and in under the punch, knees bend, rolls back up
  parryHigh         hook, high: lead forearm snaps up to meet the arm at the temple and turns it out, head pulled away
  parryMid          hook / knee, mid: rear forearm sweeps down across the belly, knocking the strike down past the hip
  parryTeep         teep / side kick, mid: rear hand scoops the sole aside and down, half step back
  parryKickMid      roundhouse, mid: lead arm meets the shin and rakes it past, body turning back away from it
  checkHigh         any punch, high, shallow: gloves locked to the brow, chin tucked, jolted back a pixel
  checkMid          any punch, mid, shallow: elbows clamped to the ribs, body crunched over them
  checkKickMid      any kick, mid, shallow: lead knee lifted to the elbow, shin covering the ribs, jolted back
  checkLow          calf kick / sweep, low, shallow: lead knee lifted and turned out, shin meets shin
  catchKickMid      roundhouse, mid, deep: rear arm cradles the shin, lead arm clamps over, held, shoved away
  catchKickLow      calf kick, low, deep: sinks, rear hand scoops the calf, holds it, throws it down
  critHigh          true critical, high: head snapped back, arms flung, two stagger steps, then the guard
  critMid           true critical, mid punch / knee: folds over both hands on the belly, knees sag
  critKickMid       true critical, mid kick: lifted off the floor sideways, folds and nearly drops to a knee
  critLow           true critical, low: lead knee buckles, body drops, arms out for balance, limps back up
Attacker clips (the kick is held while the defender has it): muayThaiRoundCaught, muayThaiCalfCaught (in mtstrikes.py).

Run: python3 tools/reactions.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import astro
import universal as _U
from universal import band, g, kleg
from standins import RECOVER
def _low(name, hip):
    """leg pose `name` re-hipped to row `hip` (feet kept, knee takes half the drop), looked up in the new poses or the base spec's"""
    src = next((q for q in _U.POSES + _U.HR['legs']['poses'] if q['name'] == name), None)
    if src is None: return name
    d = hip - src['hipRow']
    if d == 0: return name
    nm = '%s@%d' % (name, hip)
    if not any(q['name'] == nm for q in _U.POSES): _U.POSES.append(dict(src, name=nm, hipRow=hip, kneeRow=src['kneeRow'] + (d + 1) // 2))
    return nm
def gl(**k):
    hip = 41 + k.get('bob', (0,))[0]
    for s_ in ('ln', 'lf'):
        k.setdefault(s_, _U.GUARD[s_]); k[s_] = _low(k[s_], hip)
    return g(**k)

STAT = 'CANDIDATE 2026-11-26 v1.1 (E/W; W mirrors E; S/N to author after approval)'
LOWL = dict(ln='guard-low-rear', lf='guard-low-lead')
_U.POSES += [kleg('chk-lo', (33, 42), (39, 44), (39, 51), 'toe30k'),     # shin check: lead knee up and turned out, shin vertical at calf height
             kleg('chk-hi', (33, 42), (40, 36), (40, 45), 'toe30k'),     # knee to the elbow: lead knee high, shin covering the ribs
             kleg('chk-lo-n', (31, 42), (37, 44), (37, 51), 'toe30k'),   # v1.1 near-leg shin check (drawn in front of the body: layering)
             kleg('chk-hi-n', (31, 42), (38, 36), (38, 45), 'toe30k'),   # v1.1 near-leg knee to the elbow
             kleg('crit-buckle', (32, 42), (37, 51), (33, 55), 'toe30k')]  # lead knee folding forward toward the floor, heel coming up behind it
PLANT = 'hk-plant'

# critical burst (Christopher 2026-11-26 19:14: "more red/noticeable not a star"): a jagged red-orange impact burst with a
# hot yellow core and a dark-red rim, then a broken red shock ring as it expands
import math as _m
def _burst(R=9, r=3.5, n=8, jitter=(1.0, .8, 1.15, .75, 1.0, .9, 1.1, .8, .95), hollow=0.0, rot=0.3):
    W = 2 * R + 3; c = W / 2 - .5
    pts = [(c + (R * jitter[i % len(jitter)] if i % 2 == 0 else r) * _m.cos(rot + _m.pi * i / n), c + (R * jitter[i % len(jitter)] if i % 2 == 0 else r) * _m.sin(rot + _m.pi * i / n)) for i in range(2 * n)]
    def inside(x, y):
        s_ = False
        for i in range(len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): s_ = not s_
        return s_
    gr = [['.'] * W for _ in range(W)]
    for y in range(W):
        for x in range(W):
            d = _m.hypot(x - c, y - c)
            if inside(x, y) and not (hollow and d < R * hollow): gr[y][x] = 'Y' if d < r * .5 else 'O' if d < r else 'R' if d < r * 1.7 else 'M'
    out = [r_[:] for r_ in gr]
    for y in range(W):
        for x in range(W):
            if gr[y][x] == '.' and any(0 <= x + dx < W and 0 <= y + dy < W and gr[y + dy][x + dx] != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y][x] = '#'
    return [''.join(r_) for r_ in out]
astro.NPAT['critA'] = _burst()
astro.NPAT['critB'] = _burst(R=11, r=6, hollow=.55, rot=0.0)
astro.NPAT['critC'] = [r_.replace('R', 'M').replace('O', 'M') for r_ in _burst(R=12, r=7, hollow=.7, rot=.2)]
def R(state, intent, frames, faces, fps=12, rm='E: in place', fx=None):
    return (state, 0, intent, frames, faces, None, dict(fps=fps, react=True, rm=rm, anchored=fx or {}))

CLIPS = {
 'slipHigh': R('Slip (high)',
  'slipHigh (reaction: slip, straight punch at the head): frame 0 is the punch arriving; the head is already rolling down and in under it, knees bending, gloves staying home at the face; it rolls through to the low point a frame later and comes back up on the far side of the punch into the guard. No contact, no impact fx.',
  [gl(bob=(5, 8, 6), lean=(2, 6), **LOWL), gl(bob=(6, 9, 7), lean=(2, 6), **LOWL), gl(bob=(5, 7, 6), lean=(1, 5), **LOWL),
   gl(bob=(2, 3, 3), lean=(0, 3)), g()],
  ['squint', 'squint', None, None, None]),

 'parryHigh': R('Parry (high)',
  'parryHigh (reaction: parry, hook at the head): frame 0 is the hook arriving; the lead forearm has snapped up beside the head to meet the arm, head pulled back off it, a small white tick where the forearms meet; the forearm turns the hook out forward and drops back into the guard.',
  [g(af=band(-125, -175), bob=(1, 1, 1), lean=(0, 0)), g(af=band(-110, -135), bob=(1, 1, 1), lean=(0, 1)),
   g(af=band(-80, -150), lean=(0, 2)), g()],
  ['squint', None, None, None], fx={0: [('spark', 'farhand', 0, -2)]}),

 'parryMid': R('Parry (mid)',
  'parryMid (reaction: parry, hook or knee to the body): frame 0 is the strike arriving at the ribs; the rear forearm is already sweeping down across the belly into it (white tick at the forearm) and knocks it down past the hip, the hips drawn back; the hand comes back up into the guard.',
  [g(an=band(-45, -30), bob=(2, 2, 2), lean=(-1, 2)), g(an=band(5, 15), bob=(2, 2, 2), lean=(-1, 2)),
   g(an=band(-25, -100), bob=(1, 1, 2), lean=(0, 2)), g()],
  ['squint', None, None, None], fx={0: [('spark', 'hand', 0, 0)]}),

 'parryTeep': R('Parry (teep)',
  'parryTeep (reaction: parry, teep or side kick): frame 0 is the sole arriving at the belly; the rear hand has dropped to meet it and scoops it aside and down (white tick at the palm), the fighter taking a half step back off the line; it steps back in to its tile and comes up into the guard.',
  [g(an=band(-55, -75, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), root=(-1, 0)),
   g(an=band(-20, -10, fistKind='palm'), bob=(2, 2, 2), lean=(-1, 1), root=(-1, 0)),
   g(an=band(5, -60), bob=(1, 1, 2), lean=(0, 2)), g(an=RECOVER, root=(1, 0)), g(root=(1, 0))],
  ['squint', None, None, None, None], rm='E: -1 -1 the half step back, +1 +1 back in (net 0)', fx={0: [('spark', 'hand', 1, 0)]}),

 'parryKickMid': R('Parry (kick)',
  'parryKickMid (reaction: parry, roundhouse to the body): frame 0 is the shin arriving at the ribs; the rear forearm is down and out in front of the ribs to meet it (white tick) and rakes it on past behind, the body turning back away from the kick; the arm swings back up into the guard.',
  [g(an=band(-50, -20), bob=(1, 1, 2), lean=(-1, 1), root=(-1, 0)), g(an=band(25, 45), bob=(1, 1, 2), lean=(-2, 0)),
   g(an=band(-10, -80), lean=(0, 1)), g(root=(1, 0))],
  ['squint', 'squint', None, None], rm='E: -1 turning off it, +1 back (net 0)', fx={0: [('spark', 'hand', 0, 0)]}),

 'checkHigh': R('Check (high)',
  'checkHigh (reaction: check, punch at the head, shallow): frame 0 is the punch landing on the gloves; both gloves are locked to the brow, chin tucked behind them, eyes shut, and the fighter is jolted back a pixel; it holds the shell a beat and opens back into the guard. Damage to poise only, so no stars.',
  [g(an=band(-28, 192), af=band(-38, 196), bob=(2, 3, 3), lean=(0, 1), root=(-1, 0)), g(an=band(-28, 192), af=band(-38, 196), bob=(2, 3, 3), lean=(0, 1)),
   g(an=band(-25, 200), af=band(-42, 210), bob=(1, 2, 2), lean=(0, 2)), g(root=(1, 0))],
  ['closed', 'squint', None, None], rm='E: -1 jolted, +1 back (net 0)', fx={0: [('spark', 'hand', 2, -2)]}),

 'checkMid': R('Check (mid)',
  'checkMid (reaction: check, punch to the body, shallow): frame 0 is the punch landing on the arms; both elbows are clamped down over the ribs, forearms up, the body crunched over them and jolted back a pixel; it holds a beat and opens back into the guard.',
  [g(an=band(-30, -165), af=band(-40, -170), bob=(3, 4, 4), lean=(-1, 3), root=(-1, 0)), g(an=band(-30, -165), af=band(-40, -170), bob=(3, 4, 4), lean=(-1, 3)),
   g(bob=(2, 2, 3), lean=(0, 2)), g(root=(1, 0))],
  ['strain', 'squint', None, None], rm='E: -1 jolted, +1 back (net 0)', fx={0: [('spark', 'hand', 2, 3)]}),

 'checkKickMid': R('Check (kick)',
  'checkKickMid (reaction: check, kick to the body, shallow): frame 0 is the kick landing on the raised leg; v1.1: the near (rear) knee is up to the elbow, shin covering the ribs, standing on the lead leg (drawn in front of the body), and is jolted back a pixel; the knee holds a beat and the foot comes back down into the guard.',
  [gl(an=band(-25, -160), bob=(0, 0, 1), lean=(-1, 1), root=(-1, 0), lf='stance-lead', ln='chk-hi-n'),
   gl(an=band(-25, -160), bob=(0, 0, 1), lean=(-1, 1), lf='stance-lead', ln='chk-hi-n'),
   gl(bob=(0, 0, 1), lean=(0, 2), lf='stance-lead', ln='chk-lo-n'), g(root=(1, 0))],
  ['strain', 'squint', None, None], rm='E: -1 jolted, +1 back (net 0)', fx={0: [('spark', 'farhand', 2, 4)]}),

 'checkLow': R('Check (low)',
  'checkLow (reaction: check, kick at the leg, shallow): frame 0 is shin meeting shin; v1.1: the near (rear) knee is lifted and turned out so the kick lands on the shin, not the calf (white tick at the shin), the hands staying up; the foot comes straight back down into the guard.',
  [gl(bob=(0, 0, 1), lean=(-1, 1), root=(-1, 0), lf='stance-lead', ln='chk-lo-n'), gl(bob=(0, 0, 1), lean=(0, 1), lf='stance-lead', ln='chk-lo-n'),
   g(root=(1, 0))],
  ['squint', None, None], rm='E: -1 jolted, +1 back (net 0)', fx={0: [('spark', 'feet', 9, -8)]}),

 'catchKickMid': R('Catch (kick)',
  'catchKickMid (reaction: catch, roundhouse to the body, deep): frame 0 is the shin arriving at the ribs; the rear arm drops under it and cradles the shin, the lead arm clamps over the top, the body absorbing it a pixel back; it holds the trapped leg four frames (the kicker hops on one leg), then shoves it away with both hands and comes back into the guard.',
  [g(an=band(-40, -115), af=band(-90, -40), bob=(2, 2, 2), lean=(-1, 1), root=(-1, 0)),
   g(an=band(-40, -115), af=band(-90, -40), bob=(2, 2, 2), lean=(-1, 1)),
   g(an=band(-40, -115), af=band(-90, -40), bob=(1, 1, 2), lean=(0, 2)),
   g(an=band(-40, -115), af=band(-90, -40), bob=(2, 2, 2), lean=(-1, 1)),
   g(an=band(-40, -115), af=band(-90, -40), bob=(1, 1, 2), lean=(0, 2)),
   g(an=band(-82, -90), af=band(-92, -92), bob=(1, 1, 1), lean=(1, 4), root=(1, 0)),
   g(an=RECOVER, lean=(0, 2)), g()],
  ['strain', 'strain', 'strain', 'strain', 'strain', 'strain', 'squint', None], fps=10,
  rm='E: -1 absorbing it, +1 on the shove (net 0)', fx={0: [('spark', 'hand', 0, -1)]}),

 'catchKickLow': R('Catch (low)',
  'catchKickLow (reaction: catch, kick at the leg, deep): frame 0 is the shin arriving at the calf; the fighter has sunk low and the rear hand scoops the calf at the knee, the lead hand up; it holds the leg three frames, throws it down past the hip and rises into the guard.',
  [gl(an=band(-15, -45, fistKind='palm'), bob=(4, 5, 5), lean=(1, 5), **LOWL), gl(an=band(-15, -45, fistKind='palm'), bob=(4, 5, 5), lean=(1, 5), **LOWL),
   gl(an=band(-15, -45, fistKind='palm'), bob=(4, 5, 5), lean=(1, 5), **LOWL), gl(an=band(15, 10), bob=(3, 4, 4), lean=(0, 3), **LOWL),
   gl(an=RECOVER, bob=(2, 2, 3), lean=(0, 2)), g()],
  ['strain', 'strain', 'strain', 'strain', 'squint', None], fps=10, fx={0: [('spark', 'hand', 0, 0)]}),

 'critHigh': R('Critical (high)',
  'critHigh (true critical, head): frame 0 is the blow landing flush; the head snaps back, the arms fly out and down loose, a big white burst at the face; the fighter staggers back two steps on loose knees, hangs dazed a beat, and pulls the hands back up into the guard.',
  [g(an=band(45, 60), af=band(55, 70), bob=(1, 0, 1), lean=(1, -3), root=(-3, 0)),
   g(an=band(50, 40), af=band(60, 45), bob=(2, 1, 2), lean=(1, -3), root=(-2, 0), ln='im-step-rear', lf='im-step-lead'),
   gl(an=band(35, 20), af=band(40, 25), bob=(4, 4, 4), lean=(0, -2), root=(-1, 0), **LOWL),
   gl(an=band(25, 10), af=band(30, 15), bob=(4, 5, 5), lean=(0, 1), **LOWL),
   gl(an=band(20, 5), af=band(25, 10), bob=(4, 5, 5), lean=(0, 2), **LOWL),
   g(an=band(-10, -60), af=band(-20, -70), bob=(3, 3, 3), lean=(0, 2), root=(2, 0)),
   g(an=RECOVER, bob=(2, 2, 2), lean=(0, 2), root=(2, 0)), g(root=(2, 0))],
  ['pain', 'pain', 'pain', 'closed', 'closed', 'squint', 'squint', None], fps=10,
  rm='E: -3 -2 -1 the stagger back, +2 +2 +2 stepping back in (net 0)', fx={0: [('critA', 'head', -2, 2)], 1: [('critB', 'head', -1, 2)], 2: [('critC', 'head', 0, 2)]}),

 'critMid': R('Critical (mid)',
  'critMid (true critical, body punch or knee): frame 0 is the blow sinking in; the fighter folds over it, both hands clamped to the belly, a big white burst at the ribs; the knees sag and it backs a step bent double, hangs there a beat, then straightens wincing into the guard.',
  [gl(an=band(-15, -75), af=band(-20, -70), bob=(4, 6, 5), lean=(-2, 2), root=(-2, 0), **LOWL),
   gl(an=band(-12, -72), af=band(-18, -66), bob=(5, 8, 6), lean=(-2, 2), root=(-1, 0), **LOWL),
   gl(an=band(-12, -72), af=band(-18, -66), bob=(5, 8, 6), lean=(-2, 2), **LOWL),
   gl(an=band(-12, -72), af=band(-18, -66), bob=(5, 7, 6), lean=(-2, 2), **LOWL),
   gl(an=band(-25, -95), af=band(-35, -100), bob=(3, 3, 4), lean=(-1, 2)),
   g(an=RECOVER, bob=(1, 1, 2), lean=(0, 2), root=(2, 0)), g(root=(1, 0))],
  ['pain', 'pain', 'pain', 'pain', 'squint', 'squint', None], fps=10,
  rm='E: -2 -1 backing off bent double, +2 +1 back in (net 0)', fx={0: [('critA', 'head', 2, 13)], 1: [('critB', 'head', 2, 14)], 2: [('critC', 'head', 2, 14)]}),

 'critKickMid': R('Critical (kick)',
  'critKickMid (true critical, kick to the body): frame 0 is the shin landing flush; the fighter is lifted clear of the floor and carried back folding over it, both hands on the ribs, a big white burst at the side; it lands, drops nearly to one knee, hangs a beat, and climbs back up into the guard.',
  [g(an=band(-10, -70), af=band(-15, -65), bob=(0, 1, 1), lean=(-2, 2), root=(-3, 0), ln='hk-drop', lf='ml-dip-lead'),
   g(an=band(-10, -70), af=band(-15, -65), bob=(-1, 0, 0), lean=(-2, 1), root=(-2, 0), ln='hk-drop', lf='ml-dip-lead'),
   gl(an=band(-12, -72), af=band(-18, -66), bob=(6, 8, 7), lean=(-2, 2), root=(-1, 0), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-12, -72), af=band(-18, -66), bob=(7, 9, 8), lean=(-2, 2), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-12, -72), af=band(-18, -66), bob=(7, 9, 8), lean=(-2, 2), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-25, -95), af=band(-35, -100), bob=(4, 4, 5), lean=(-1, 2), **LOWL),
   g(an=RECOVER, bob=(2, 2, 2), lean=(0, 2), root=(3, 0)), g(root=(3, 0))],
  ['pain', 'pain', 'pain', 'pain', 'pain', 'strain', 'squint', None], fps=10,
  rm='E: -3 -2 -1 lifted and carried back, +3 +3 back in (net 0)', fx={0: [('critA', 'head', 2, 14)], 1: [('critB', 'head', 2, 14)], 2: [('critC', 'head', 2, 14), ('dust', 'feet', 0, -2)]}),

 'critLow': R('Critical (low)',
  'critLow (true critical, leg kick): frame 0 is the shin landing flush on the lead calf; the lead knee buckles forward toward the floor, the body drops, the arms fly out for balance, a white burst at the calf; it hangs on the buckled leg a beat, then limps back up onto it into the guard.',
  [gl(an=band(-60, -40), af=band(-95, -70), bob=(4, 4, 4), lean=(0, 2), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-55, -30), af=band(-100, -60), bob=(6, 6, 6), lean=(0, 3), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-50, -40), af=band(-95, -70), bob=(6, 7, 6), lean=(0, 3), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-40, -80), af=band(-60, -110), bob=(5, 6, 6), lean=(0, 3), ln='guard-low-rear', lf='crit-buckle'),
   gl(an=band(-30, -100), af=band(-45, -140), bob=(3, 3, 4), lean=(0, 2), **LOWL),
   g(an=RECOVER, bob=(2, 2, 2), lean=(0, 2)), g()],
  ['pain', 'pain', 'pain', 'strain', 'squint', 'squint', None], fps=10, fx={0: [('critA', 'feet', 9, -10)], 1: [('critB', 'feet', 9, -9)], 2: [('critC', 'feet', 9, -9)]}),
}
astro.CLIPS.update(CLIPS)
astro.APPROVED.update({k: STAT for k in CLIPS})

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--fx' in a:
        for st in (a[a.index('--fx') + 1:] or [k for k in CLIPS if CLIPS[k][-1]['anchored']]): astro.fx(st)
        sys.exit()
    for st in (a or CLIPS):
        if st in CLIPS: astro.spec(st)

# ---- attacker clips while the defender holds the kick (Muay Thai stance; the testbed swaps them in for a catch) ----
import mtstrikes as _M
_f, _p, _b = _M.f, _M.p, _M.band
_M.CLIPS['roundCaught'] = ('Roundhouse Kick', 3, [44, 28, 14, 10], 'heavy', [   # roundhouse to the impact, then the shin is trapped 4 frames (arms flailing for balance on the standing leg), shoved off, back to the stance
    _f(), _p(an=_b(-5, 190), bob=(0, 0, 1), lean=(0, 1), ln='lift', lf='lead-pivot'),
    _p(an=_b(30, 40), bob=(0, 0, 1), lean=(1, -1), ln='round-fold', lf='lead-pivot'),
    _p(an=_b(40, 30), af=_b(-60, 200), bob=(0, 0, 1), lean=(1, -4), root=(1, 0), ln='mt-round', lf='lead-pivot'),
    _p(an=_b(70, 100), af=_b(-100, 170), bob=(0, 0, 0), lean=(0, -4), ln='mt-round', lf='lead-pivot'),
    _p(an=_b(55, 60), af=_b(-60, 220), bob=(0, 0, 1), lean=(1, -3), ln='mt-round', lf='lead-pivot'),
    _p(an=_b(75, 110), af=_b(-110, 160), bob=(0, 0, 0), lean=(0, -4), ln='mt-round', lf='lead-pivot'),
    _p(an=_b(55, 60), af=_b(-60, 220), bob=(0, 0, 1), lean=(1, -3), ln='mt-round', lf='lead-pivot'),
    _p(an=_b(60, 90), af=_b(-30, 160), bob=(0, 0, 1), lean=(-1, -4), root=(-2, 0), ln='round-fold', lf='lead-pivot'),
    _p(an=_b(-10, 200), ln='lift'), _f(root=(1, 0))])
_M.CLIPS['calfCaught'] = ('Calf Kick', 2, [42, 46, 16, 10], 'heavy', [   # calf kick to the impact, the shin held 2 frames (arms out), thrown down so the kicker stumbles forward a step, back to the stance
    _p(lean=(0, 1)), _p(bob=(0, 0, 1), lean=(0, 0), ln='lift'),
    _p(an=_b(25, 20), bob=(0, 0, 1), lean=(1, -2), root=(1, 0), ln='low-kick', lf='lead-pivot'),
    _p(an=_b(60, 90), af=_b(-100, 170), bob=(0, 0, 1), lean=(1, -2), ln='low-kick', lf='lead-pivot'),
    _p(an=_b(50, 70), af=_b(-95, 180), bob=(0, 0, 1), lean=(1, -2), ln='low-kick', lf='lead-pivot'),
    _p(an=_b(-40, -60), af=_b(-70, -90), bob=(1, 1, 2), lean=(2, 5), root=(1, 0), ln='low-recoil', lf='lead-pivot'),
    _f(root=(-1, 0)), _f(root=(-1, 0))])
ATTACKERS = {'muayThaiRoundCaught': ('roundCaught',), 'muayThaiCalfCaught': ('calfCaught',)}
for _s in ATTACKERS: _M.APPROVED[_s] = STAT
if __name__ == '__main__':
    for _s, _n in ATTACKERS.items():
        if not sys.argv[1:] or _s in sys.argv[1:]: _M.spec(_s, _n)
