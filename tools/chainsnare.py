"""Kyoketsu-Shoge grapple (Christopher 2026-10-19): Kusari Chain Snare + Chain Yank, standing rig, E/W.
Thrower: chainSnare (twirl overhead, throw the weight with the off hand, chain runs out to the target) -> chainHold (loop,
chain held taut from the off hand); chainYank (haul the chain back to the hip) -> chainHold.
Target: snared (loop, chain coiled twice around the chest pinning the arms); chainYanked (dragged forward a stumbling
step) -> snared. The chain between the two fighters is drawn by the testbed from the thrower's chainHand anchor (events)
to the target's coil anchor (events), because the range varies.
Run: python3 chainsnare.py  (specs) ; render with character-posed ; then python3 chainsnare.py --weapons ; character-weapon."""
import sys, copy, json, math
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
from PIL import Image
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
CAST = load(D + 'cast.json')
band = lambda a, e, **k: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def tf(src=0, **k): return dict(src=src, **k)
STAT = 'E/W candidate 2026-10-19 ({}), awaiting user approval; S/N to author'
KN = band(-20, -50, fistKind='forward')       # oneHandGuard near arm: kama held low and forward
KF = band(-38, 232)                            # oneHandGuard far arm: off hand raised (holds the chain)
GL = dict(ln='guard-low-rear', lf='guard-low-lead'); ST = dict(ln='stance-rear', lf='stance-lead')

# ---------- thrower: chainSnare ----------
OUT = band(-92, -90)                           # off arm straight out at the target, chain running from the fist
sn = [tf(0, an=KN, af=KF, bob=(1, 1, 1), lean=(0, 2), root=(0, 0), **ST),
      tf(0, an=KN, af=band(-55, -120), bob=(1, 1, 1), lean=(0, 1), root=(0, 0), **ST),           # off hand in front of the chest, weight whirled low
      tf(0, an=KN, af=band(-70, -160), bob=(2, 2, 2), lean=(-1, 0), root=(0, 0), **GL),          # wrist cocked up, weight swung up behind the hand
      tf(0, an=KN, af=band(-100, -105), bob=(2, 2, 2), lean=(1, 3), root=(1, 0), **GL),          # throw
      tf(0, an=KN, af=OUT, bob=(1, 1, 1), lean=(1, 4), root=(1, 0), **GL),                       # release
      tf(0, an=KN, af=OUT, bob=(1, 1, 1), lean=(1, 4), root=(0, 0), **GL),
      tf(0, an=KN, af=band(-85, -85), bob=(1, 1, 1), lean=(0, 3), root=(-1, 0), **ST),
      tf(0, an=KN, af=band(-82, -80), bob=(1, 1, 1), lean=(0, 2), root=(-1, 0), **ST)]
HOLD = [tf(0, an=KN, af=band(-82, -80), bob=(1, 1, 1), lean=(0, 2), root=(0, 0), **ST),
        tf(0, an=KN, af=band(-80, -78), bob=(1, 1, 1), lean=(0, 1), root=(0, 0), **ST),
        tf(0, an=KN, af=band(-82, -80), bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
        tf(0, an=KN, af=band(-84, -82), bob=(2, 1, 2), lean=(0, 2), root=(0, 0), **ST)]
YANK = [tf(0, an=KN, af=band(-82, -80), bob=(1, 1, 1), lean=(0, 2), root=(0, 0), **ST),
        tf(0, an=KN, af=band(-90, -95), bob=(2, 2, 2), lean=(1, 3), root=(0, 0), **GL),          # reach along the chain
        tf(0, an=KN, af=band(-45, -40), bob=(2, 2, 2), lean=(-1, -2), root=(-1, 0), **GL),       # haul
        tf(0, an=KN, af=band(-10, 30), bob=(2, 2, 2), lean=(-2, -4), root=(-1, 0), **GL),        # chain hand at the hip
        tf(0, an=KN, af=band(-10, 30), bob=(2, 2, 2), lean=(-2, -4), root=(0, 0), **GL),
        tf(0, an=KN, af=band(-50, -60), bob=(1, 1, 1), lean=(0, 0), root=(1, 0), **ST),
        tf(0, an=KN, af=band(-82, -80), bob=(1, 1, 1), lean=(0, 2), root=(1, 0), **ST)]

# ---------- target: snared / chainYanked ----------
PN, PF = band(-6, -4), band(-10, -8)          # arms pinned to the sides by the coils
SNR = [tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(0, -1), root=(0, 0), **ST),
       tf(0, an=band(-8, -6), af=band(-12, -10), bob=(1, 1, 1), lean=(1, -1), root=(0, 0), **ST),   # strains against the coils
       tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(0, -1), root=(0, 0), **ST),
       tf(0, an=band(-4, -2), af=band(-8, -6), bob=(2, 2, 2), lean=(-1, -2), root=(0, 0), **ST)]
YKD = [tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(0, -1), root=(0, 0), **ST),
       tf(0, an=PN, af=PF, bob=(2, 2, 2), lean=(1, 3), root=(2, 0), **GL),            # jerked forward at the chest
       tf(0, an=PN, af=PF, bob=(3, 3, 3), lean=(2, 5), root=(3, 0), **GL),            # stumbling, off balance
       tf(0, an=PN, af=PF, bob=(2, 2, 2), lean=(2, 4), root=(3, 0), **ST),
       tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(1, 1), root=(1, 0), **ST),
       tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(0, -1), root=(0, 0), **ST)]

# chain coils (fx, drawn over the fighter so the arms read pinned): two loops round the chest/upper arms, links alternate
# white and steel with a black outline; COIL = the front of the upper coil, where the chain from the thrower attaches
CP = {'#': '#000000', 'W': '#ffffff', 'a': '#adadad'}
CPAT = {'coil': ['.############.', '#aWaWaWaWaWaWa#', '.############.']}
def coil_fx(frames):
    out = []
    for k, f in enumerate(frames):
        dy = f['bob'][2]; dx = round(f['lean'][1] * 0.5)
        out.append({'frame': k, 'splash': [{'pattern': 'coil', 'at': [25 + dx, 26 + dy]}, {'pattern': 'coil', 'at': [25 + dx, 31 + dy]}]})
    return out
def coil_anchor(f): return [39 + round(f['lean'][1] * 0.5), 27 + f['bob'][2]]

def ev(frames, move, active, extra):
    e = []
    for k, f in enumerate(frames):
        d = {'frame': k, 'type': 'startup' if k < active else 'active' if k == active else 'recovery'}
        if k == active: d['move'] = move
        d.update(extra(k, f)); e.append(d)
    return e
mirror = lambda E: [{**d, **{key: [63 - d[key][0], d[key][1]] for key in ('chainHand', 'coil', 'release') if key in d}} for d in E]

def specs():
    def mk(name, frames, fps, nxt, why, intent, events=None, fx=None, expr=None):
        s = build(CAST, name, frames, status=STAT.format(why), intent=intent,
                  clips={'rule': 'Kyoketsu-Shoge grapple (Kusari Chain Snare / Chain Yank)', name: {'frames': list(range(len(frames))), 'fps': fps, **({'next': nxt} if nxt else {'loop': True})}},
                  events=events, fx=fx, rmRule='per-frame step (screen px)')
        s.pop('keyPoses', None)
        if expr: s['expressions'] = copy.deepcopy(CAST['expressions']); s['expressions']['frames'] = {'E': expr}
        else: s.pop('expressions', None)
        save(s, D + name + '.json')
    mk('chainSnare', sn, 12, 'chainHold', 'Kusari Chain Snare throw',
       'Kusari Chain Snare (Kyoketsu-Shoge, ranged grapple): from the kama idle the off hand whirls the weight low in front of the chest, swings it up behind the cocked wrist and slings it at the target; the arm ends straight out with the chain running from the fist to the target, then settles into chainHold. The flying weight and the chain to the target are drawn by the testbed from the chainHand anchor (event release on frame 4); on a hit the target plays snared.')
    mk('chainHold', HOLD, 6, None, 'Kusari Chain Snare hold',
       'Held snare: the thrower keeps the chain taut from the off hand (straight out at chest height), kama low in the other hand, tugging 1 px as the loop breathes. The testbed draws the chain from chainHand to the target\'s coil anchor.')
    mk('chainYank', YANK, 12, 'chainHold', 'Chain Yank',
       'Chain Yank (follow-up): the thrower reaches along the chain, then hauls it back to the hip leaning away (frame 2-3, event pull on frame 2); the target plays chainYanked and is pulled into melee range; the thrower recovers to chainHold with the grapple maintained.')
    fxs = lambda fr, rule: {'rule': rule, 'top': True, 'palette': CP, 'patterns': CPAT, 'frames': coil_fx(fr)}
    mk('snared', SNR, 6, None, 'snared by the chain',
       'Snared (Kusari Chain Snare target, Grapple 2rd): the chain is wrapped twice round the chest and upper arms, pinning them to the sides; the fighter strains against it (arms push out 1-2 px, body leans back from the pull). Coils are an fx layer over the fighter; the chain from the thrower attaches at the coil anchor (events).',
       events={'rule': 'per-frame gameplay data per facing; coil = where the chain from the thrower attaches', 'E': ev(SNR, 'snared', 0, lambda k, f: {'coil': coil_anchor(f)})},
       fx=fxs(SNR, 'chain coils round the chest and upper arms, over the fighter'), expr=['squint'] * 4)
    mk('chainYanked', YKD, 12, 'snared', 'pulled by Chain Yank',
       'Chain Yanked (Chain Yank target): jerked forward at the chest by the chain, a stumbling step toward the thrower (root motion 2, 3, 3, 1 px; the testbed moves the fighter into melee range over these frames), then upright again in snared.',
       events={'rule': 'per-frame gameplay data per facing; coil = where the chain from the thrower attaches', 'E': ev(YKD, 'chainYanked', 1, lambda k, f: {'coil': coil_anchor(f)})},
       fx=fxs(YKD, 'chain coils round the chest and upper arms, over the fighter'), expr=['squint', 'pain', 'pain', 'squint', 'squint', 'squint'])
    for n in ('snared', 'chainYanked'):
        s = load(D + n + '.json'); s['events']['W'] = mirror(s['events']['E']); save(s, D + n + '.json')

# ---------- after render: kama + chain (weapon layer), chainHand anchors ----------
def fist(state, k, side):
    s = load(D + state + '.json'); a = s['arms'][side][k]
    ua, fa = math.radians(a['angle']), math.radians(a['elbow']['angle'])
    lx = s['lean']['dx']['head'][k] * 0.5; dy = s['bob']['arms'][k]
    sx = 32 + lx + (2 if side == 'far' else 0)
    x = sx - 8 * math.sin(ua) - 7 * math.sin(fa); y = 23 + dy + 8 * math.cos(ua) + 7 * math.cos(fa)
    best = None
    for lay in ('arms', 'body'):
        im = Image.open(D + state + '/' + lay + '.png').convert('RGBA')
        for yy in range(int(y) - 4, int(y) + 5):
            for xx in range(int(x) - 4, int(x) + 5):
                if 0 <= xx < 64 and 0 <= yy < 64:
                    p = im.getpixel((k * 64 + xx, yy))
                    if p[3] == 255 and p[:3] != (0, 0, 0):
                        d = (xx - x) ** 2 + (yy - y) ** 2
                        if best is None or d < best[0]: best = (d, xx, yy)
    return [best[1], best[2]] if best else [round(x), round(y)]

TWIRL = {1: [3, 10], 2: [6, -10]}              # weight whirled low in front, then swung up over the hand
def weapons():
    for st, n in (('chainSnare', len(sn)), ('chainHold', len(HOLD)), ('chainYank', len(YANK))):
        s = load(D + st + '.json'); E = []; ev_ = []
        for k in range(n):
            g, h = fist(st, k, 'near'), fist(st, k, 'far')
            chain = {'via': h, 'droop': 6, 'z': 'front'}
            if st == 'chainSnare' and k in TWIRL: chain['to'] = TWIRL[k]
            elif st == 'chainSnare' and k == 0: chain.update(to=[0, 9])
            else: chain.update(to=[6, 0], noWeight=True)      # the chain leaves the fist toward the target; the testbed draws the rest
            E.append({'grip': g, 'angle': 55, 'z': 'front', 'chain': chain})
            d = {'frame': k, 'chainHand': h}
            ev_.append(d)
        s['weapons'] = [{'slot': 'main', 'layer': 'arms', 'items': ['kama'], 'status': s['status'],
                         'rule': 'per frame: grip = near fist centre (snapped to the rendered fist), angle 55 as in the kama idle; chain via = off fist; chain.to = weight offset from the off fist (noWeight: the weight is out at the target, drawn by the testbed)',
                         'depthRule': 'front: over body and clothing, under the arms layer', 'E': E, 'mirror': {'W': 'E'}}]
        base = {e['frame']: e for e in (s.get('events') or {}).get('E', [])}
        for d in ev_:
            b = base.get(d['frame'], {'frame': d['frame'], 'type': 'active' if (st == 'chainSnare' and d['frame'] == 4) or (st == 'chainYank' and d['frame'] == 2) else 'recovery' if d['frame'] > (4 if st == 'chainSnare' else 2) else 'startup'})
            b.update(d)
            if st == 'chainSnare' and d['frame'] == 4: b.update(move='kusariChainSnare', release=d['chainHand'])
            if st == 'chainYank' and d['frame'] == 2: b.update(move='chainYank', pull=True)
            base[d['frame']] = b
        E2 = [base[k] for k in range(n)]
        s['events'] = {'rule': 'per-frame gameplay data per facing; chainHand = the off fist, where the testbed starts the chain line to the target', 'E': E2, 'W': mirror(E2)}
        save(s, D + st + '.json')

if __name__ == '__main__' and not ({'--struggle', '--recall-weapons'} & set(sys.argv)):
    weapons() if '--weapons' in sys.argv else specs()
    print('ok')
# approved by Christopher 2026-10-19: relabel after regenerating
if __name__ == '__main__' and not ({'--struggle', '--recall-weapons'} & set(sys.argv)):
    for _st in ('chainSnare', 'chainHold', 'chainYank', 'snared', 'chainYanked'):
        _s = load(D + _st + '.json'); _s['status'] = _s['status'].replace('E/W candidate 2026-10-19', 'E/W approved by user 2026-10-19').replace(', awaiting user approval', '')
        for _w in _s.get('weapons', []): _w['status'] = _s['status']
        save(_s, D + _st + '.json')

# ---------- Struggle (Christopher 2026-10-19): a snared fighter cannot strike; its clinch strikes become Struggle, an
# escape check whose DC drops each attempt. Fail: snaredStruggle -> snared. Success: snareBreak -> guard (thrower: chainRecall).
STAT2 = 'E/W candidate 2026-10-19 ({}), awaiting user approval; S/N to author'
G_N, G_F = CAST['arms']['near'][0], CAST['arms']['far'][0]
STR = [tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(0, -1), root=(0, 0), **ST),
       tf(0, an=band(-14, -10), af=band(-4, 0), bob=(2, 2, 2), lean=(1, 2), root=(0, 0), **GL),       # heave forward against the coils
       tf(0, an=band(-16, -12), af=band(-2, 2), bob=(3, 3, 3), lean=(1, 3), root=(0, 0), **GL),
       tf(0, an=band(-2, 2), af=band(-16, -12), bob=(2, 2, 2), lean=(-1, -3), root=(0, 0), **GL),     # twist back the other way
       tf(0, an=band(0, 4), af=band(-18, -14), bob=(2, 2, 2), lean=(-1, -3), root=(0, 0), **GL),
       tf(0, an=PN, af=PF, bob=(1, 1, 1), lean=(0, -1), root=(0, 0), **ST),                           # the coils hold
       tf(0, an=PN, af=PF, bob=(2, 1, 1), lean=(0, -1), root=(0, 0), **ST)]
BRK = STR[:3] + [
       tf(0, an=band(-60, -110), af=band(25, 60), bob=(2, 2, 2), lean=(0, 2), root=(0, 0), **GL),     # coils burst: arms fling free
       tf(0, an=band(-55, -120), af=band(20, 70), bob=(1, 1, 1), lean=(0, 1), root=(0, 0), **ST),
       tf(0, an=band(-30, -150), af=band(-20, 200), bob=(1, 1, 1), lean=(0, 2), root=(0, 0), **ST),
       tf(0, an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
       tf(0, an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST)]
RCL = [tf(0, an=KN, af=band(-82, -80), bob=(1, 1, 1), lean=(0, 2), root=(0, 0), **ST),
       tf(0, an=KN, af=band(-75, -95), bob=(1, 1, 1), lean=(0, 1), root=(-1, 0), **ST),              # the chain goes slack, recalled hand over hand
       tf(0, an=KN, af=band(-55, -120), bob=(1, 1, 1), lean=(0, 1), root=(0, 0), **ST),
       tf(0, an=KN, af=KF, bob=(1, 1, 1), lean=(0, 2), root=(0, 0), **ST)]
LINK = {'link': ['.#.', '#a#', '.#.'], 'linkW': ['.#.', '#W#', '.#.'], 'bar': ['.###.', '#aWa#', '.###.']}
def break_fx():
    fr = coil_fx(BRK[:3])
    bursts = {3: [([22, 27], 'bar'), ([37, 25], 'bar'), ([28, 22], 'link'), ([33, 34], 'linkW')],
              4: [([16, 24], 'link'), ([44, 22], 'linkW'), ([24, 16], 'link'), ([40, 38], 'link'), ([30, 40], 'linkW')],
              5: [([10, 26], 'linkW'), ([50, 20], 'link'), ([46, 44], 'linkW')]}
    for k, ps in bursts.items(): fr.append({'frame': k, 'splash': [{'pattern': p, 'at': a} for a, p in ps]})
    return fr
def struggle_specs():
    pat = dict(CPAT, **LINK)
    def mk(name, frames, fps, nxt, why, intent, fx=None, expr=None, events=None):
        s = build(CAST, name, frames, status=STAT2.format(why), intent=intent,
                  clips={'rule': 'Kyoketsu-Shoge grapple: Struggle (escape from Kusari Chain Snare)', name: {'frames': list(range(len(frames))), 'fps': fps, 'next': nxt}},
                  events=events, fx=fx, rmRule='per-frame step (screen px)')
        s.pop('keyPoses', None)
        if expr: s['expressions'] = copy.deepcopy(CAST['expressions']); s['expressions']['frames'] = {'E': expr}
        else: s.pop('expressions', None)
        save(s, D + name + '.json')
    mk('snaredStruggle', STR, 12, 'snared', 'Struggle, failed',
       'Struggle that fails: the snared fighter heaves forward against the coils, twists back the other way, and the chain holds; back to snared. Coils follow the body (fx over the fighter).',
       fx={'rule': 'chain coils round the chest and upper arms, over the fighter', 'top': True, 'palette': CP, 'patterns': pat, 'frames': coil_fx(STR)},
       expr=['squint', 'pain', 'pain', 'pain', 'pain', 'squint', 'squint'],
       events={'rule': 'per-frame gameplay data per facing; coil = where the chain from the thrower attaches', 'E': ev(STR, 'struggle', 2, lambda k, f: {'coil': coil_anchor(f)})})
    mk('snareBreak', BRK, 12, 'guard', 'Struggle, breaks the snare',
       'Struggle that succeeds: the same heave, then the coils burst apart (chain links fly off), the arms fling free and come back up into the guard. The thrower plays chainRecall.',
       fx={'rule': 'coils over the fighter while they hold (frames 0-2); on the burst (frame 3) the coils break into links that fly outward and fall away', 'top': True, 'palette': CP, 'patterns': pat, 'frames': break_fx()},
       expr=['squint', 'pain', 'pain', None, None, None, None, None],
       events={'rule': 'per-frame gameplay data per facing; coil = where the chain from the thrower attaches until it breaks (frame 3, event snareBroken)', 'E': ev(BRK, 'snareBroken', 3, lambda k, f: {'coil': coil_anchor(f)} if k < 3 else {})})
    mk('chainRecall', RCL, 10, 'oneHandGuard', 'chain recalled after the snare breaks',
       'Thrower when the snare is broken: the chain goes slack and is pulled back in, the off hand returns to the kama idle (oneHandGuard). The testbed draws the slack chain shortening to the fist over frames 0-2.')
    for n in ('snaredStruggle', 'snareBreak'):
        s = load(D + n + '.json'); s['events']['W'] = mirror(s['events']['E']); save(s, D + n + '.json')
def recall_weapons():
    s = load(D + 'chainRecall.json'); E = []; e2 = []
    for k in range(len(RCL)):
        g, h = fist('chainRecall', k, 'near'), fist('chainRecall', k, 'far')
        to = {0: [6, 0], 1: [4, 6], 2: [2, 8], 3: [0, 9]}[k]
        E.append({'grip': g, 'angle': 55, 'z': 'front', 'chain': {'via': h, 'droop': 6, 'z': 'front', 'to': to, **({'noWeight': True} if k == 0 else {})}})
        e2.append({'frame': k, 'type': 'recovery', 'chainHand': h})
    s['weapons'] = [{'slot': 'main', 'layer': 'arms', 'items': ['kama'], 'status': s['status'], 'rule': 'as chainHold; the weight is back at the off fist from frame 1', 'depthRule': 'front', 'E': E, 'mirror': {'W': 'E'}}]
    s['events'] = {'rule': 'chainHand = the off fist; the testbed shortens the slack chain to it over frames 0-2', 'E': e2, 'W': mirror(e2)}
    save(s, D + 'chainRecall.json')
if __name__ == '__main__' and '--struggle' in sys.argv: struggle_specs()
if __name__ == '__main__' and '--recall-weapons' in sys.argv: recall_weapons()
