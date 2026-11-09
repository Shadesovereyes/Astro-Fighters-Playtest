"""The Guard after its shield is knocked away (Christopher 2026-11-09 16:51: "spear and shield kit approved, need animations
for shield disarm and idle and attack animations for spear without shield post disarm"). Built on standin_weapons.py /
tanto.py (two-link IK to each hand target, yari on the main slot); E/W first (W mirrors E), S/N after approval.
  shieldDisarmed       target reaction when a Disarm lands on a shield bearer (impact-frame rule: frame 0 is the impact):
                       the shield is torn off the far forearm with a white spark, flies up and back over the shoulder,
                       tumbles down behind the Guard and tips flat; the Guard staggers back a step, brings the free hand onto the shaft and settles
                       into the two-handed spear guard. The shield is off the fighter from frame 0 (hidden pose: no fist).
  spearTwoHandGuard    idle without the shield: yari held in both hands, near fist forward on the shaft, far fist back at
                       the hip about 8 px down the shaft, point level at the foe; slow breathing bob.
  spearTwoHandThrust   Spear Thrust without the shield: both hands draw the spear back along the hip, then a lunge drives
                       it straight out (thrust lines), held, back to the two-handed guard.
  spearTwoHandCut      Blade Strike without the shield: the spear is lifted over the near shoulder (blade over the head
                       layers), then both hands sweep the leaf blade down diagonally across the target, back to the guard.
Run: python3 tools/guard_bare.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/guard_bare.py --grips <state> ;
     node tools/character-weapon.mjs male <state> ; python3 tools/guard_bare.py --fx <state>"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]; sys.argv = sys.argv[:1]
import standin_weapons as SW, tanto as T
from tanto import fr
from PIL import Image

STAT = 'E/W approved by user 2026-11-09 17:47 (v1.1; W mirrors E); S/N to author'
HAND = 8   # near fist to far fist along the shaft
def tw(grip, angle, hand=HAND, **k):
    """both hands on the yari: the far fist sits `hand` px back down the shaft from the near fist"""
    t = math.radians(angle); far = (round(grip[0] - hand * math.cos(t)), round(grip[1] + hand * math.sin(t)))
    return fr(grip=grip, angle=angle, far=far, fk='forward', **k)
G2 = dict(grip=(43, 34), angle=8, lean=(0, 2))   # the two-handed guard frame
def g2(**k): return tw(**{**G2, **k})
RAISE = {'hilt': 'front', 'blade': 'top'}

CLIPS = {
 'spearTwoHandGuard': ('Spear Guard (two-handed)', None, None, None, 6, 'loop', [
    g2(), g2(grip=(43, 33)), g2(grip=(43, 34), bob=(1, 1, 2), lean=(0, 3), angle=7), g2(grip=(43, 35), angle=9)]),
 'spearTwoHandThrust': ('Spear Thrust', 3, [48, 26, 16, 8], 'heavy', 12, 'spearTwoHandGuard', [
    g2(),
    tw((37, 34), 6, ln='step-rear', lean=(0, 1)),
    tw((35, 34), 6, ln='step-rear', lean=(-1, 0)),
    tw((50, 31), 5, bob=(2, 2, 2), lean=(2, 5), root=(3, 0), ln='lunge-rear', lf='lunge-lead',
       trail={'mode': 'thrust', 'clipBody': True, 'lines': [[-3, -8, 4], [3, -6, 3], [6, -9, -1]]}),
    tw((50, 31), 5, bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    tw((45, 33), 7, lean=(1, 3), root=(-2, 0), lf='step-lead'),
    g2(root=(-1, 0))]),
 'spearTwoHandCut': ('Blade Strike', 3, [44, 18, 20, 18], 'light', 12, 'spearTwoHandGuard', [
    g2(),
    tw((41, 26), 50, lean=(-1, 0), ln='step-rear', z=RAISE),
    tw((40, 23), 66, lean=(-1, -1), ln='step-rear', z=RAISE),
    tw((48, 31), -22, bob=(2, 2, 2), lean=(2, 5), root=(2, 0), ln='lunge-rear', lf='lunge-lead', trail='swing'),
    tw((46, 35), -34, bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    tw((44, 34), -4, lean=(1, 3), root=(-1, 0)),
    g2(root=(-1, 0))]),
 # target reaction: frame 0 is the impact (the shield is struck off); the far arm is flung open, the body jolts back
 'shieldDisarmed': ('Disarmed (shield)', 0, None, 'none', 10, 'spearTwoHandGuard', [
    SW.sg(far=(40, 21), lean=(-1, -1), bob=(1, 1, 1), root=(-1, 0)),
    SW.sg(grip=(39, 35), far=(36, 23), lean=(-2, -2), bob=(1, 1, 1), root=(-1, 0), ln='step-rear'),
    SW.sg(grip=(39, 35), far=(37, 27), lean=(-1, -1), bob=(2, 2, 2), ln='step-rear'),
    tw((41, 35), 6, lean=(0, 1), bob=(2, 2, 2), root=(1, 0)),
    tw((42, 34), 7, lean=(0, 2), root=(1, 0)),
    g2()]),
}
# the shield's flight, per frame of shieldDisarmed (E, body-frame px; angle 90 = upright; ws = widthScale: a shield
# lying flat on the floor is seen edge-on, so its band is thinner; z: in front of the body while still on the arm, behind
# it once it is flying): v1.1 the blow knocks it up and back over the Guard's shoulder (so it never crosses the yari), it
# tumbles down behind the Guard, lands on its rim behind the rear foot and tips flat
FLIGHT = [((44, 20), 115, 1, 'front'), ((38, 12), 150, 1, 'behind'), ((29, 22), 205, 1, 'behind'), ((24, 42), 245, 1, 'behind'),
          ((22, 56), 190, 0.7, 'behind'), ((22, 60), 180, 0.4, 'behind')]
FLIGHT_SH = {'shield-tower': 1, 'shield-heater': 1, 'shield-buckler': 1}

INTENT = {
 'spearTwoHandGuard': 'Spear Guard without the shield (Christopher 2026-11-09: idle for the Guard after its shield is disarmed): the yari in both hands, the near fist forward on the shaft and the far fist back at the hip about a hand\'s width down it, the point level at the foe; a slow breathing bob. Every shieldless spear move starts and ends here.',
 'spearTwoHandThrust': 'Spear Thrust without the shield (Christopher 2026-11-09): from the two-handed guard both hands draw the yari back along the hip, weight on the rear leg, then a lunge drives it straight out at the foe (thrust lines), held, back to the guard.',
 'spearTwoHandCut': 'Blade Strike without the shield (Christopher 2026-11-09; reskin of Kenjutsu Slash, made with the yari blade): both hands lift the yari over the near shoulder, the blade passing over the head layers, then step in and sweep the leaf blade down diagonally across the target (smear), back to the two-handed guard.',
 'shieldDisarmed': 'Shield disarmed (Christopher 2026-11-09: target reaction when a Disarm lands on a shield bearer; impact-frame rule, frame 0 is the impact): the shield is torn off the far forearm with a white spark, the far arm flung open and the Guard jolted back a step; the blow knocks the shield up and back over the shoulder; it tumbles down behind the Guard, lands on its rim behind the rear foot and tips flat on the floor; the Guard brings the free hand onto the yari shaft and settles into the two-handed spear guard (next: spearTwoHandGuard).',
}
STATES = {k: k for k in CLIPS}
SW.ITEM.update({k: 'yari' for k in CLIPS}); SW.CLIPS.update(CLIPS); SW.INTENT.update(INTENT); SW.STATES.update(STATES)
T.CLIPS.update(CLIPS); T.INTENT.update(INTENT); T.STATES = SW.STATES
T.FX['spearTwoHandThrust'] = {3: 24}; T.FX['spearTwoHandCut'] = {3: 20}
T.STAT = STAT

def spec(state):
    SW.spec(state)
    s = T.load(T.D + state + '.json')
    s['status'] = STAT
    for w in s['weapons']: w['status'] = STAT
    s['extra'] = {'npc': 'Guard', 'loadout': 'yari only (the shield was disarmed)'}
    if state == 'shieldDisarmed':
        SW.shield_slot(state)   # the shield family on the off slot, then the flight overrides the grips
        s = T.load(T.D + state + '.json'); off = next(w for w in s['weapons'] if w.get('slot') == 'off')
        off['status'] = STAT
        off['rule'] = 'the shield is off the fighter from the impact frame: free poses (hidden, no fist to register to) flying up and back over the shoulder and tumbling to the floor behind the rear foot; every shield type takes the same flight'
        off['E'] = [{'grip': list(g), 'angle': a, 'z': z, 'hidden': True, **({'widthScale': ws} if ws != 1 else {})} for g, a, ws, z in FLIGHT]
        s['clips']['rule'] = 'target reaction: plays when a Disarm lands on a shield bearer (impact-frame rule: frame 0 is the impact), then the Guard idles in spearTwoHandGuard and uses the two-handed spear moves; the shield stays off for the rest of the fight (Christopher 2026-11-09 17:47); the testbed leaves it lying on the tile (last frame of the off slot) as a floor prop'
        ev = [{'frame': k, 'clip': 'shieldDisarmed', 'type': 'impact' if k == 0 else 'recovery'} for k in range(s['frames'])]
        ev[0]['effect'] = 'Disarm on a shield bearer: the shield is knocked away; Shield Bash and Shield Block are unavailable and Spear Thrust / Blade Strike play the two-handed clips (Christopher 2026-11-09 17:47: for the rest of the fight; shield first, then weapon; up to three disarms, each harder)'
        s['events'] = {'rule': 'per-frame data (W mirrors E)', 'E': ev, 'W': [dict(e) for e in ev]}
        s['status'] = STAT
        for w in s['weapons']: w['status'] = STAT
    T.save(s, T.D + state + '.json')

SPARK = T.SPARK
def fx(state):
    if state != 'shieldDisarmed': return T.fx(state)
    s = T.load(T.D + state + '.json'); n = s['frames']; dirs = s['directions']
    out = Image.new('RGBA', (64 * n, 64 * len(dirs)), (0, 0, 0, 0))
    for k, c in ((0, (44, 22)),):   # the spark where the shield is struck off the forearm
        for di, d in enumerate(dirs):
            cc = (63 - c[0], c[1]) if d == 'W' else c
            px = {(cc[0] - 3 + i, cc[1] - 3 + j) for j, r in enumerate(SPARK) for i, ch in enumerate(r) if ch == 'W'}
            for (x, y) in px:
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + ox, y + oy)
                    if q not in px: out.putpixel((k * 64 + q[0], di * 64 + q[1]), (0, 0, 0, 255))
            for (x, y) in px: out.putpixel((k * 64 + x, di * 64 + y), (255, 255, 255, 255))
    out.save(T.D + state + '/fx.png')
    a = json.load(open(T.D + state + '/animation.json')); a['layers']['fx'] = 'fx.png'
    open(T.D + state + '/animation.json', 'w').write(json.dumps(a, indent=2) + '\n')

if __name__ == '__main__':
    a = args
    if '--grips' in a: T.grips(a[a.index('--grips') + 1])
    elif '--fx' in a: fx(a[a.index('--fx') + 1])
    else:
        for st in (a or CLIPS): spec(st)
