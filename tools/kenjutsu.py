"""Kenjutsu stance techniques (Christopher 2026-10-27: the Kenjutsu style animations still need development): one state
per ability, each starting and ending in the approved two-handed katana stance (twoHandGuard, chudan) instead of the
stand-ins the testbed used (Parry -> unarmed block, Hilt Bash -> katana side cut, Precision Thrust -> katana up cut).
  kenjutsuParry   Parry: the blade swings up from chudan to stand near-vertical in front of the body, the strike
                  glances off the upper blade with a white spark, held, then back to chudan.
  kenjutsuHiltBash  Hilt Bash: blade drawn up beside the head, both hands drive the pommel straight into the foe's face
                  with a step in, white impact burst at the pommel, then back to chudan.
  kenjutsuThrust  Precision Thrust: hands chamber at the near hip with the blade level, then a lunge drives the point
                  straight out (morote-zuki) with thrust speed lines, hold, recover to chudan.
E/W first (W mirrors E); S/N after approval. Arms are solved by two-link IK to the authored grip (near hand at the guard,
far hand down the hilt at the pommel end).
Run: python3 tools/kenjutsu.py ; node tools/character-posed.mjs male <state> ; python3 tools/kenjutsu.py --grips <state> ;
     node tools/character-weapon.mjs male <state> ; python3 tools/kenjutsu.py --fx <state>"""
import sys, copy, json, math
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
from PIL import Image
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
BASE = load(D + 'twoHandGuard.json')
LIGHT = load(D + 'katanaLight.json')
STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
UA, FA, HILT = 8, 7, 5.5   # upper arm and forearm reach (band pivot to fist centre), near fist to far fist along the hilt

def flat(name, hip, knee, foot, wrap=56, kind='flat'): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'footX': foot, 'wrapRow': wrap, 'foot': kind}
POSES = [flat('lunge-lead', (33, 44), (39, 50), 42), flat('lunge-rear', (31, 44), (27, 50), 21, wrap=54, kind='toe60'),
         flat('step-lead', (33, 43), (38, 50), 40), flat('step-rear', (31, 43), (28, 50), 23)]

def ik(sx, sy, hx, hy):
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
    return {'construction': 'band', 'angle': round(math.degrees(best[1]), 1), 'elbow': {'at': 8, 'angle': round(math.degrees(best[2]), 1)}, 'fistKind': 'forward'}

def fr(grip, angle, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), ln='stance-rear', lf='stance-lead', trail=None, z='front'):
    sx, sy = 32 + lean[1] * 0.5, 23 + bob[2]
    t = math.radians(angle); far = (grip[0] - HILT * math.cos(t), grip[1] + HILT * math.sin(t))
    w = {'grip': list(grip), 'angle': angle, 'z': z}
    if trail: w['trail'] = trail
    return dict(src=0, an=ik(sx, sy, grip[0], grip[1]), af=ik(sx, sy, *far), bob=bob, lean=lean, root=root, ln=ln, lf=lf, w=w)

G = dict(grip=(44, 33), angle=40)   # the approved chudan guard frame
CLIPS = {
 # Parry (Counter, self): the blade swings up to stand near-vertical in front of the body, edge out, tip slightly back;
 # the weight settles onto the rear leg and the incoming blow glances off the upper blade (spark), then back to chudan
 'parry': ('Parry', 3, None, 'none', 10, [
    fr(**G),
    fr((45, 29), 75, bob=(1, 1, 1), lean=(0, 1)),
    fr((45, 27), 102, bob=(2, 2, 2), lean=(-1, -1), ln='step-rear'),
    fr((44, 28), 108, bob=(2, 2, 2), lean=(-1, -2), ln='step-rear'),
    fr((45, 27), 103, bob=(2, 2, 2), lean=(-1, -1), ln='step-rear'),
    fr((45, 29), 75, bob=(1, 1, 1), lean=(0, 1)),
    fr(**G)]),
 # Hilt Bash (guard break + stun): blade drawn up beside the head, then both hands drive the pommel into the face
 'hiltBash': ('Hilt Bash', 3, [48, 20, 12, 12], 'heavy', 12, [
    fr(**G),
    fr((41, 27), 100, bob=(1, 1, 1), lean=(0, 0)),
    fr((43, 24), 115, bob=(1, 1, 1), lean=(1, 3), root=(1, 0), lf='step-lead'),
    fr((50, 23), 128, bob=(2, 2, 2), lean=(2, 5), root=(2, 0), ln='lunge-rear', lf='lunge-lead'),
    fr((50, 23), 126, bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    fr((46, 27), 90, bob=(1, 1, 2), lean=(1, 3), root=(-2, 0), lf='step-lead'),
    fr(**G, root=(-1, 0))]),
 # Precision Thrust (true damage, guard break): chamber at the near hip with the blade level, lunge, point straight out
 'thrust': ('Precision Thrust', 3, [52, 26, 12, 6], 'heavy', 12, [
    fr(**G),
    fr((39, 33), 8, bob=(2, 2, 2), lean=(-1, 0)),
    fr((40, 32), 5, bob=(2, 2, 2), lean=(0, 1), root=(1, 0), lf='step-lead'),
    fr((50, 30), 2, bob=(3, 3, 3), lean=(2, 5), root=(3, 0), ln='lunge-rear', lf='lunge-lead',
       trail={'mode': 'thrust', 'clipBody': True, 'lines': [[-4, -6, 10], [4, -4, 8], [7, -9, 1]]}),
    fr((50, 30), 2, bob=(3, 3, 3), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    fr((46, 32), 20, bob=(2, 2, 2), lean=(1, 3), root=(-2, 0), lf='step-lead'),
    fr(**G, root=(-2, 0))]),
}
STATES = {'kenjutsuParry': 'parry', 'kenjutsuHiltBash': 'hiltBash', 'kenjutsuThrust': 'thrust'}

def spec(state, c):
    base = copy.deepcopy(BASE)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    ab, act, hb, dmg, fps, frames = CLIPS[c]
    n = len(frames)
    clips = {'rule': 'Kenjutsu techniques: each clip starts and ends in the approved two-handed stance frame and returns to that idle (next: twoHandGuard)',
             c: {'frames': list(range(n)), 'fps': fps, 'next': 'twoHandGuard', 'ability': ab}}
    ev = []
    for k in range(n):
        e = {'frame': k, 'clip': c, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'}
        if k == act:
            e['move'] = ab
            if hb: e.update(hitbox=hb, damage=dmg)
            else: e['effect'] = 'deflect (Counter: the next hostile ability against the caster deals 0)'
        ev.append(e)
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
              'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    s = build(base, state, [{k: v for k, v in f.items() if k != 'w'} for f in frames], status=STAT, newPoses=POSES, clips=clips, events=events,
              rmRule='E: the step in moves the body forward, the recovery steps back to the start (sum 0)',
              intent=CLIPS_INTENT[c], extra={'stance': 'Kenjutsu Stance'})
    s['fps'] = fps; s.pop('approved', None); s.pop('keyPoses', None)
    w = copy.deepcopy(BASE['weapons'][0])
    w['status'] = STAT; w['E'] = [f['w'] for f in frames]; w['mirror'] = {'W': 'E'}
    for k in ('S', 'N', 'projectionRule'): w.pop(k, None)
    s['weapons'] = [w]
    assert sum(r[0] for r in s['rootMotion']['E']) == 0, state
    save(s, D + state + '.json'); print(state, n, 'frames')

CLIPS_INTENT = {
 'parry': 'Kenjutsu Parry (Counter), user 2026-10-27: from chudan the blade swings up to stand near-vertical in front of the body (edge out, tip slightly back), the weight settles onto the rear leg; the incoming blow glances off the upper blade (white spark on the contact frame), held, then the blade lowers back to chudan.',
 'hiltBash': 'Kenjutsu Hilt Bash (guard break, stun), user 2026-10-27: from chudan the blade is drawn up beside the head, then a step in drives both hands forward so the pommel (kashira) leads into the foe\'s face (white impact burst at the pommel), hold, step back to chudan.',
 'thrust': 'Kenjutsu Precision Thrust (true damage, guard break), user 2026-10-27: from chudan the hands chamber at the near hip with the blade level, then a lunge on the lead leg drives the point straight out at chest height (morote-zuki) with speed lines along the blade, hold, recover back to chudan.',
}

def grips(state):
    """snap each authored grip to the nearest rendered fist pixel so the hilt registers in the hand (character-weapon --check)"""
    s = json.load(open(D + state + '.json')); arms = Image.open(D + state + '/arms.png').convert('RGBA')
    row = s['directions'].index('E')
    for k, p in enumerate(s['weapons'][0]['E']):
        x, y = p['grip']; best = None
        for yy in range(y - 4, y + 5):
            for xx in range(x - 4, x + 5):
                if 0 <= xx < 64 and 0 <= yy < 64 and arms.getpixel((k * 64 + xx, row * 64 + yy))[3] == 255 and arms.getpixel((k * 64 + xx, row * 64 + yy))[:3] != (0, 0, 0):
                    d = (xx - x) ** 2 + (yy - y) ** 2
                    if best is None or d < best[0]: best = (d, xx, yy)
        if best: p['grip'] = [best[1], best[2]]
    save(s, D + state + '.json')

# white/neutral FX (fx.png, 64 px frames): a four-point spark with a black outline
SPARK = ['...W...', '...W...', '..WWW..', 'WWWWWWW', '..WWW..', '...W...', '...W...']
BURST = ['W..W..W', '.W.W.W.', '..WWW..', 'WWWWWWW', '..WWW..', '.W.W.W.', 'W..W..W']
FX = {'kenjutsuParry': {3: ('spark', 'blade', 14)}, 'kenjutsuHiltBash': {3: ('burst', 'pommel', 0)}}
def fx(state):
    s = json.load(open(D + state + '.json')); n = s['frames']; dirs = s['directions']
    out = Image.new('RGBA', (64 * n, 64 * len(dirs)), (0, 0, 0, 0))
    for k, (kind, at, u) in FX.get(state, {}).items():
        p = s['weapons'][0]['E'][k]; t = math.radians(p['angle'])
        if at == 'pommel': u = -8.5
        cx, cy = p['grip'][0] + 0.5 + u * math.cos(t), p['grip'][1] + 0.5 - u * math.sin(t)
        if at == 'blade': cx += 3   # the blow lands on the blade's forward edge
        pat = SPARK if kind == 'spark' else BURST
        for di, d in enumerate(dirs):
            px = set()
            for j, r in enumerate(pat):
                for i, ch in enumerate(r):
                    if ch == 'W':
                        x = int(cx) - 3 + i; px.add((63 - x if d == 'W' else x, int(cy) - 3 + j))
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
        for st, c in STATES.items(): spec(st, c)
