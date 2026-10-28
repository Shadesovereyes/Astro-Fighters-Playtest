"""Tantojutsu techniques (Christopher 2026-10-27: develop animations for the Tantojutsu abilities): two grip stances and
one state per ability, each starting and ending in its own grip's guard instead of the stand-ins the testbed used
(both grips -> oneHandGuard, Thrust Cut -> oneHandLight stab1 + swipe, Defang -> swipe, Blade Pass -> stab2,
Scissors -> unarmed block, Elbow Hook -> stab1).
  tantoForwardGuard   Forward Grip Stance idle: mobile and attacking, knife hand out at chest height with the point
                      at the foe, live hand up by the chest, light bounce on the balls of the feet.
  tantoReverseGuard   Reverse Grip Stance idle: defensive, lower stance with the weight back; the knife hand held high
                      in front of the chest with the blade (edge out) lying along the forearm, live hand forward.
  tantoThrustCut      Thrust Cut (Tsuki-Uchi): chamber, lunge and thrust, then a draw-cut raking down and back.
  tantoDefang         Defang (Defang the Snake): a short rising cut into the attacker's wrist, white spark at the tip.
  tantoBladePass      Blade Pass (Hubud-Lubud), Forward Grip: the live hand checks and traps, the knife hand passes over
                      the top and cuts down across.
  tantoBladePassReverse  Blade Pass from the Reverse Grip: the same pass, hammer-fist cut with the blade below the fist.
  tantoScissors       Scissors (Gunting): the live hand checks the blow while the reverse-grip blade sweeps across the
                      attacking arm (an X), white spark on the contact frame.
  tantoElbowHook      Elbow Hook: cross-block with the knife forearm, the live hand cups the foe's elbow and pulls him
                      in as the body steps forward (the testbed then enters the clinch).
E/W first (W mirrors E); S/N after approval. Arms are solved by two-link IK to each authored hand target.
Run: python3 tools/tanto.py ; for each state: node tools/character-posed.mjs male <state> ;
     python3 tools/tanto.py --grips <state> ; node tools/character-weapon.mjs male <state> ; python3 tools/tanto.py --fx <state>"""
import sys, copy, json, math
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
from PIL import Image
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
BASE = load(D + 'oneHandGuard.json')
PALMS = load(D + 'wrestlingSumoPalm.json')['arms']['band']
STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
UA, FA = 8, 7

def flat(name, hip, knee, foot, wrap=56, kind='flat'): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'footX': foot, 'wrapRow': wrap, 'foot': kind}
POSES = [flat('lunge-lead', (33, 44), (39, 50), 42), flat('lunge-rear', (31, 44), (27, 50), 21, wrap=54, kind='toe60'),
         flat('step-lead', (33, 43), (38, 50), 40), flat('step-rear', (31, 43), (28, 50), 23),
         flat('bounce-rear', (31, 42), (28, 50), 25, wrap=54, kind='toe60'),
         flat('low-lead', (32, 44), (37, 51), 38), flat('low-rear', (31, 44), (28, 51), 23)]

def ik(sx, sy, hx, hy, kind='forward'):
    """two-link arm from the shoulder pivot to the fist centre; segment angle a points along (-sin a, cos a) (0 = down,
    -90 = forward); the elbow hangs below the shoulder-hand line"""
    dx, dy = hx - sx, hy - sy; r = min(math.hypot(dx, dy), UA + FA - 0.05); r = max(r, abs(UA - FA) + 0.05)
    phi = math.atan2(-dx, dy)
    al = math.acos((UA * UA + r * r - FA * FA) / (2 * UA * r)); be = math.acos((FA * FA + r * r - UA * UA) / (2 * FA * r))
    best = None
    for s in (1, -1):
        ua, fa = phi + s * al, phi - s * be
        ey = sy + UA * math.cos(ua)
        if best is None or ey > best[0]: best = (ey, ua, fa)
    a = {'construction': 'band', 'angle': round(math.degrees(best[1]), 1), 'elbow': {'at': 8, 'angle': round(math.degrees(best[2]), 1)}}
    if kind: a['fistKind'] = kind
    return a

def rev_angle(arm, off):
    """reverse grip (user 2026-10-27: the blade points downward, never back into the arm): the blade leaves the
    little-finger side of the fist and points straight down, tipped `off` degrees forward (positive) or back"""
    return -90 + off

def fr(grip, angle=None, far=(39, 24), fk=None, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), ln='stance-rear', lf='stance-lead',
       trail=None, rev=None, z='front'):
    sx, sy = 32 + lean[1] * 0.5, 23 + bob[2]
    an = ik(sx, sy, *grip); af = ik(sx, sy, *far, kind=fk)
    if rev is not None: angle = rev_angle(an, rev); z = {'hilt': 'front', 'blade': 'aboveArm'}
    w = {'grip': list(grip), 'angle': angle, 'z': z}
    if trail: w['trail'] = trail   # 'swing': a crescent about the grip from the previous frame's blade angle
    return dict(src=0, an=an, af=af, bob=bob, lean=lean, root=root, ln=ln, lf=lf, w=w)

P, H = 'palm', 'heel'
FG = dict(grip=(45, 30), angle=15, far=(39, 23), lean=(0, 3))                                         # forward grip guard
RG = dict(grip=(45, 26), rev=6, far=(40, 23), fk=None, lean=(0, 2), bob=(2, 2, 2), ln='guard-low-rear', lf='guard-low-lead')   # reverse grip guard
def fg(**k): return fr(**{**FG, **k})
def rg(**k): return fr(**{**RG, **k})
def arc(a0, a1, R=27, w=7, c=(33, 24)): return {'from': a0, 'to': a1, 'center': list(c), 'radius': R, 'width': w}

CLIPS = {
 'fgd': ('Forward Grip Stance', None, None, None, 6, 'loop', [
    fg(lean=(0, 2), grip=(44, 30)), fg(lean=(1, 3), grip=(45, 30)), fg(lean=(1, 5), grip=(47, 30), bob=(1, 1, 2)), fg(lean=(1, 3), grip=(45, 30))]),
 'rgd': ('Reverse Grip Stance', None, None, None, 5, 'loop', [
    rg(), rg(bob=(2, 2, 2), grip=(45, 25)), rg(bob=(3, 3, 3)), rg(bob=(3, 3, 3), grip=(45, 27))]),
 # Thrust Cut (Tsuki-Uchi): chamber, lunge and thrust, then the edge is drawn down and back through the target
 'thrustCut': ('Thrust Cut', 3, [48, 24, 14, 8], 'heavy', 12, 'tantoForwardGuard', [
    fg(),
    fg(grip=(38, 31), angle=5, far=(43, 25), lean=(0, 1)),
    fg(grip=(41, 30), angle=3, far=(42, 25), lean=(1, 3), root=(1, 0), lf='step-lead'),
    fg(grip=(51, 28), angle=2, far=(38, 26), bob=(2, 2, 2), lean=(2, 5), root=(3, 0), ln='lunge-rear', lf='lunge-lead',
       trail={'mode': 'thrust', 'clipBody': True, 'lines': [[-3, -8, 4], [3, -6, 3], [6, -9, -1]]}),
    fg(grip=(51, 28), angle=2, far=(38, 26), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    fg(grip=(48, 33), angle=-22, far=(38, 26), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    fg(grip=(44, 37), angle=-42, far=(38, 25), bob=(2, 2, 2), lean=(1, 3), root=(-1, 0), lf='step-lead', trail=arc(-6, -44, R=28)),
    fg(grip=(43, 33), angle=5, root=(-2, 0)),
    fg(root=(-1, 0))]),
 # Defang (Defang the Snake): the blade dips, then a short rising cut meets the attacking wrist (spark at the tip)
 'defang': ('Defang', 2, [50, 18, 12, 14], 'light', 12, 'tantoForwardGuard', [
    fg(),
    fg(grip=(42, 33), angle=-30, far=(39, 22), lean=(0, 2)),
    fg(grip=(49, 27), angle=35, far=(39, 22), lean=(1, 4), root=(2, 0), lf='step-lead', trail=arc(-38, 9, R=26)),
    fg(grip=(48, 25), angle=48, far=(39, 22), lean=(1, 4), lf='step-lead'),
    fg(grip=(46, 28), angle=25, lean=(0, 3), root=(-1, 0)),
    fg(root=(-1, 0))]),
 # Blade Pass (Hubud-Lubud): the live hand taps the foe's arm up, the knife hand passes over it while the live hand
 # traps it down, then the blade cuts down across the trapped arm
 'bladePass': ('Blade Pass', 3, [46, 22, 14, 14], 'light', 12, 'tantoForwardGuard', [
    fg(),
    fg(grip=(40, 30), angle=30, far=(46, 25), fk=P, lean=(0, 3)),
    fg(grip=(44, 23), angle=62, far=(46, 29), fk=P, lean=(1, 3)),
    fg(grip=(50, 30), angle=-16, far=(45, 31), fk=P, lean=(2, 5), root=(1, 0), lf='step-lead', trail=arc(31, -18, R=28)),
    fg(grip=(50, 30), angle=-16, far=(41, 27), lean=(2, 5), lf='step-lead'),
    fg(grip=(46, 31), angle=8, root=(-1, 0)),
    fg()]),
 'bladePassRev': ('Blade Pass', 3, [46, 22, 14, 14], 'light', 12, 'tantoReverseGuard', [
    rg(),
    rg(grip=(40, 21), far=(47, 25)),
    rg(grip=(42, 19), far=(46, 29), lean=(0, 1)),
    rg(grip=(48, 28), rev=None, angle=-55, z={'hilt': 'front', 'blade': 'aboveArm'}, far=(45, 31), lean=(1, 3), root=(1, 0), ln='low-rear', lf='step-lead', trail='swing'),
    rg(grip=(48, 28), rev=None, angle=-55, z={'hilt': 'front', 'blade': 'aboveArm'}, far=(41, 27), fk=None, lean=(1, 3), ln='low-rear', lf='step-lead'),
    rg(grip=(43, 24), root=(-1, 0)),
    rg()]),
 # Scissors (Gunting, Counter): the live hand checks the blow high while the reverse-grip blade sweeps across the
 # attacking arm in an X (spark), the knife hand carries on out and down, then back to the reverse guard
 'scissors': ('Scissors', 2, None, 'none', 12, 'tantoReverseGuard', [
    rg(),
    rg(grip=(39, 20), far=(47, 24), lean=(-1, -1), ln='step-rear'),
    rg(grip=(47, 22), rev=25, far=(46, 24), lean=(-1, 0), ln='step-rear'),
    rg(grip=(47, 29), rev=None, angle=-62, z={'hilt': 'front', 'blade': 'aboveArm'}, far=(45, 25), lean=(0, 1), ln='step-rear', trail='swing'),
    rg(grip=(47, 29), rev=None, angle=-62, z={'hilt': 'front', 'blade': 'aboveArm'}, far=(45, 26), lean=(0, 1), ln='step-rear'),
    rg(grip=(43, 24), far=(46, 28)),
    rg()]),
 # Elbow Hook: the knife forearm cross-blocks high, the live hand reaches over and cups the foe's elbow, then pulls it
 # in to the hip as the body steps forward (the testbed enters the clinch after this clip)
 'elbowHook': ('Elbow Hook', 3, [46, 20, 14, 14], 'light', 12, 'tantoReverseGuard', [
    rg(),
    rg(grip=(43, 17), rev=15, far=(42, 27), lean=(-1, 0)),
    rg(grip=(44, 18), rev=15, far=(50, 22), fk=P, lean=(2, 6), root=(2, 0), ln='step-rear', lf='step-lead'),
    rg(grip=(44, 22), rev=15, far=(41, 31), fk=None, lean=(-1, 0), root=(1, 0), ln='step-rear', lf='step-lead'),
    rg(grip=(44, 22), rev=15, far=(40, 31), fk=None, lean=(0, 1), ln='step-rear', lf='step-lead'),
    rg(grip=(42, 22), root=(-2, 0)),
    rg(root=(-1, 0))]),
}
STATES = {'tantoForwardGuard': 'fgd', 'tantoReverseGuard': 'rgd', 'tantoThrustCut': 'thrustCut', 'tantoDefang': 'defang',
          'tantoBladePass': 'bladePass', 'tantoBladePassReverse': 'bladePassRev', 'tantoScissors': 'scissors', 'tantoElbowHook': 'elbowHook'}
INTENT = {
 'fgd': 'Tantojutsu Forward Grip Stance idle (attack, mobility), user 2026-10-27: the tanto held in the forward (hammer) grip with the knife hand out at chest height and the point toward the foe, the live hand up by the chest, both feet planted, the body rocking forward and back over them (user 2026-10-27: no raised heel).',
 'rgd': 'Tantojutsu Reverse Grip Stance idle (defence, counters), user 2026-10-27: a lower stance with the weight back; the knife hand held high in front of the chest in the reverse (ice-pick) grip, the blade pointing straight down out of the little-finger side of the fist, clear of the forearm (user 2026-10-27); the live fist up by the chin; a slow breathing bob.',
 'thrustCut': 'Tantojutsu Thrust Cut (Tsuki-Uchi), user 2026-10-27: from the forward grip the knife hand chambers at the hip, a lunge drives the point straight out (thrust lines), then the edge is drawn down and back through the target (draw-cut smear) as the feet recover to the forward guard.',
 'defang': 'Tantojutsu Defang (Defang the Snake), user 2026-10-27: from the forward grip the point dips, then a short rising cut with a half step meets the attacking wrist (white spark at the tip), follow-through and back to the forward guard.',
 'bladePass': 'Tantojutsu Blade Pass (Hubud-Lubud) from the forward grip, user 2026-10-27: the live hand taps the foe\'s arm up, the knife hand passes over it while the live hand traps it down, then the blade cuts down across the trapped arm (smear), back to the forward guard.',
 'bladePassRev': 'Tantojutsu Blade Pass (Hubud-Lubud) from the reverse grip, user 2026-10-27: the live hand taps the foe\'s arm up, the knife hand passes over it while the live hand traps it down, then a hammer-fist cut drives the blade below the fist down across the trapped arm (smear), back to the reverse guard.',
 'scissors': 'Tantojutsu Scissors (Gunting, Counter), user 2026-10-27: from the reverse grip the weight rocks back as the live hand checks the incoming blow high and the knife hand sweeps the reverse-grip blade across the attacking arm, the two forearms crossing like scissors (white spark on contact), the blade carries on out and down, then back to the reverse guard.',
 'elbowHook': 'Tantojutsu Elbow Hook, user 2026-10-27: from the reverse grip the knife forearm cross-blocks high, the live hand reaches over and cups the foe\'s elbow, then pulls it in to the hip as the body steps forward; the ruling of 2026-10-27 takes the pair into the clinch after the clip (not Prone).',
}

def spec(state, c):
    base = copy.deepcopy(BASE)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    for k in ('palmUp', 'palmDown', 'palmHeel'): base['arms']['band'][k] = copy.deepcopy(PALMS[k])
    ab, act, hb, dmg, fps, nxt, frames = CLIPS[c]
    n = len(frames)
    if nxt == 'loop':
        clips = {'rule': 'loops while the %s is active; every move from this grip ends here' % ab, state: {'frames': list(range(n)), 'fps': fps, 'loop': True}}
        events = None
    else:
        clips = {'rule': 'Tantojutsu techniques: each clip starts and ends in its grip\'s guard frame and returns to that idle (next: %s)' % nxt,
                 c: {'frames': list(range(n)), 'fps': fps, 'next': nxt, 'ability': ab}}
        ev = []
        for k in range(n):
            e = {'frame': k, 'clip': c, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'}
            if k == act:
                e['move'] = ab
                if hb: e.update(hitbox=hb, damage=dmg)
                else: e['effect'] = 'counter (the blow is checked and the attacking arm is cut: riposte)'
            ev.append(e)
        if c == 'thrustCut': ev[6].update(type='active', move='Thrust Cut (draw-cut)', hitbox=[44, 30, 14, 12], damage='light')
        events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
                  'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    s = build(base, state, [{k: v for k, v in f.items() if k != 'w'} for f in frames], status=STAT, newPoses=POSES, clips=clips, events=events,
              rmRule='E: a step in moves the body forward, the recovery steps back to the start (sum 0)',
              intent=INTENT[c], extra={'stance': 'Reverse Grip Stance' if nxt == 'tantoReverseGuard' or c == 'rgd' else 'Forward Grip Stance'})
    s['fps'] = fps; s.pop('approved', None); s.pop('keyPoses', None)
    w = copy.deepcopy(BASE['weapons'][0])
    w['status'] = STAT; w['items'] = ['tanto']; w['E'] = [copy.deepcopy(f['w']) for f in frames]; w['mirror'] = {'W': 'E'}
    for k, p in enumerate(w['E']):
        if p.get('trail') == 'swing':
            a0 = w['E'][k - 1]['angle']
            while a0 - p['angle'] > 180: a0 -= 360
            while p['angle'] - a0 > 180: a0 += 360
            p['trail'] = {'from': a0, 'to': p['angle'], 'width': 5}
    w['grip'] = 'reverse (blade below the little finger, pointing down, clear of the forearm)' if c in ('rgd', 'bladePassRev', 'scissors', 'elbowHook') else 'forward'
    for k in ('S', 'N', 'projectionRule', 'itemPoses', 'itemStatus', 'viewRule'): w.pop(k, None)
    s['weapons'] = [w]
    assert sum(r[0] for r in s['rootMotion']['E']) == 0, state
    save(s, D + state + '.json'); print(state, n, 'frames')

def grips(state):
    """snap each authored grip to the nearest rendered fist pixel so the hilt registers in the hand (character-weapon --check)"""
    s = json.load(open(D + state + '.json')); arms = Image.open(D + state + '/arms.png').convert('RGBA')
    for d in [d for d in ('E', 'S') if d in s['directions'] and d in s['weapons'][0]]:
      row = s['directions'].index(d)
      for k, p in enumerate(s['weapons'][0][d]):
        x, y = p['grip']; best = None
        for yy in range(y - 4, y + 5):
            for xx in range(x - 4, x + 5):
                if 0 <= xx < 64 and 0 <= yy < 64 and arms.getpixel((k * 64 + xx, row * 64 + yy))[3] == 255 and arms.getpixel((k * 64 + xx, row * 64 + yy))[:3] != (0, 0, 0):
                    q = (xx - x) ** 2 + (yy - y) ** 2
                    if best is None or q < best[0]: best = (q, xx, yy)
        if best: p['grip'] = [best[1], best[2]]
    save(s, D + state + '.json')

# white/neutral FX (fx.png, 64 px frames): a four-point spark with a black outline, at a point along the blade
SPARK = ['...W...', '...W...', '..WWW..', 'WWWWWWW', '..WWW..', '...W...', '...W...']
FX = {'tantoDefang': {2: 10}, 'tantoScissors': {2: 7}}
def fx(state):
    s = json.load(open(D + state + '.json')); n = s['frames']; dirs = s['directions']
    out = Image.new('RGBA', (64 * n, 64 * len(dirs)), (0, 0, 0, 0))
    for k, u in FX.get(state, {}).items():
        p = s['weapons'][0]['E'][k]; t = math.radians(p['angle'])
        cx, cy = p['grip'][0] + 0.5 + u * math.cos(t), p['grip'][1] + 0.5 - u * math.sin(t)
        for di, d in enumerate(dirs):
            if d not in ('E', 'W'): continue
            c = ((63 - int(cx)) if d == 'W' else int(cx), int(cy))
            px = {(c[0] - 3 + i, c[1] - 3 + j) for j, r in enumerate(SPARK) for i, ch in enumerate(r) if ch == 'W'}
            for (x, y) in px:
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + ox, y + oy)
                    if q not in px and 0 <= q[0] < 64 and 0 <= q[1] < 64: out.putpixel((k * 64 + q[0], di * 64 + q[1]), (0, 0, 0, 255))
            for (x, y) in px:
                if 0 <= x < 64 and 0 <= y < 64: out.putpixel((k * 64 + x, di * 64 + y), (255, 255, 255, 255))
    out.save(D + state + '/fx.png')
    a = json.load(open(D + state + '/animation.json')); a['layers']['fx'] = 'fx.png'
    open(D + state + '/animation.json', 'w').write(json.dumps(a, indent=2) + '\n')

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--grips': grips(sys.argv[2])
    elif len(sys.argv) > 2 and sys.argv[1] == '--fx': fx(sys.argv[2])
    else:
        only = sys.argv[1:]
        for st, c in STATES.items():
            if not only or st in only: spec(st, c)
