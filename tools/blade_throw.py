"""Blade Throw (Kyoketsu-Shoge; Grappling only: thrown from the clinch hold, never while Grappled or in Mount; range 3,
5 Physical + Bleed). The holder keeps the collar tie with the far hand, drops the near hand, cocks the tanto back over its
shoulder and slings it on its chain past the held fighter's head; the flying tanto and the chain to the target are drawn
by the testbed from the chainHand anchor (release event), like Kusari Chain Snare; the cord is yanked and the tanto caught
back in the fist, which returns to the neck. The held fighter keeps its clinchHeld idle (it is not the target).
E/W first (W mirrors E); S/N after approval.
Run: python3 tools/blade_throw.py ; node tools/character-posed.mjs male clinchBladeThrow ; python3 tools/blade_throw.py --grips ;
     node tools/character-weapon.mjs male clinchBladeThrow ; preview: python3 tools/blade_throw.py --scene <out>"""
import sys, os, copy, json
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'production/source/characters/anim/male/')
K = load(D + 'clinchKnife.json')
band = lambda a, e: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
def tf(src=0, **k): return dict(src=src, **k)
TEST = '--test' in sys.argv
if TEST:
    A = [(-82, -118), (-30, 210), (-150, -230), (-170, -250), (-130, -200), (-100, -105), (-92, -90), (-60, -120), (-40, -120), (-120, -60)]
    fr = [tf(0, an=band(a, e)) for a, e in A]
    s = build(K, 'zzBT', fr, status='x', intent='x', clips={'rule': 'x', 'zzBT': {'frames': list(range(10)), 'fps': 12}})
    s.pop('weapons', None); save(s, D + 'zzBT.json'); sys.exit()

# near arm per frame (far arm keeps the collar tie from clinchKnife frame 0); lean back on the cock, forward on the sling
NEAR = [(-82, -118), (-30, 210), (-150, -230), (-170, -250), (-100, -105), (-92, -90), (-92, -90), (-60, -120), (-40, -120), (-82, -118)]
LEAN = [None, None, (-1, -2), (-1, -3), (1, 3), (1, 3), (1, 2), (0, 1), None, None]
fr = []
for k, (a, e) in enumerate(NEAR):
    f = tf(0, an=band(a, e))
    if LEAN[k]: f['lean'] = LEAN[k]
    fr.append(f)
REL, IMP, REC, CATCH = 4, 6, 7, 8
ev = [{'frame': i, 'type': 'startup' if i < REL else 'active' if i in (REL, IMP) else 'recovery'} for i in range(10)]
ev[REL].update({'move': 'bladeThrow', 'release': None, 'rule': 'the tanto leaves the fist at chainHand and flies to the target on its cord (testbed-drawn, as Kusari Chain Snare)'})
ev[IMP].update({'move': 'Blade Throw', 'impact': True, 'effect': '5 Physical; Bleed 2 (AGI DC12, 3 rds)', 'rule': 'impact frame: the target plays hitReact on this frame, never before (ANIMATION_RULES 2026-11-04)'})
ev[REC].update({'recall': True, 'rule': 'the cord is yanked: the testbed flies the tanto back from the target to chainHand, arriving on frame 8'})
ev[CATCH].update({'catch': True})
events = {'rule': 'per-frame gameplay data per facing (provisional); chainHand = near fist centre while the cord is out; impact frame 6', 'E': ev, 'W': copy.deepcopy(ev),
          'tactical': {'rule': 'no displacement: the clinch pair stays on its cells; range 3 (Zone of Awareness 1/3 approximated as 3 tiles)'}}
s = build(K, 'clinchBladeThrow', fr, status='CANDIDATE 2026-11-06 (Blade Throw from the clinch hold, partner keeps clinchHeld) (E/W; W mirrors E; S/N to author after approval)',
          intent=('Kyoketsu-Shoge Blade Throw (Grappling only): from clinchHold the far hand keeps the collar tie; the near hand drops off the neck with the tanto, '
                  'swings it up and cocks it behind the head (frames 2-3), then slings it forward over the held fighter\'s head (release frame 4). The arm stays out while the '
                  'tanto flies on its chain to the target (impact frame 6), yanks it back (7), catches it (8) and returns to the neck (9).'),
          clips={'rule': 'plays from clinchHold and returns to it; the held partner keeps its clinchHeld idle; a target within 3 tiles plays hitReact on the impact frame',
                 'clinchBladeThrow': {'frames': list(range(10)), 'fps': 12, 'next': 'clinchHold'}}, events=events)
s['pair'] = dict(K['pair'], partner='clinchHeld')
s['weapons'] = [{'slot': 'main', 'layer': 'arms', 'items': ['kyoketsu-shoge'], 'status': s['status'],
                 'rule': 'per frame: grip = near fist centre (snapped to the rendered fist); frames 4-7 hidden: the tanto and its cord are out at the target, drawn by the testbed from chainHand; the cord is wound in the fist when held (noWeight)',
                 'depthRule': 'front: over body and clothing, under the arms layer', 'E': [], 'mirror': {'W': 'E'}}]
ANG = [60, 70, 150, 170, None, None, None, None, 40, 60]
for k in range(10):
    p = {'grip': [48, 23], 'angle': ANG[k] if ANG[k] is not None else 0, 'z': 'front'}
    if ANG[k] is None: p['hidden'] = True; p['chain'] = {'off': True}
    else: p['chain'] = {'via': [48, 24], 'droop': 0, 'z': 'front', 'to': [0, 1], 'noWeight': True}
    s['weapons'][0]['E'].append(p)
if not TEST and '--grips' not in sys.argv and '--scene' not in sys.argv: save(s, D + 'clinchBladeThrow.json'); print('ok')

if '--grips' in sys.argv:
    from fistsnap import fists
    s = load(D + 'clinchBladeThrow.json'); F = fists('clinchBladeThrow')
    for k, p in enumerate(s['weapons'][0]['E']):
        p['grip'] = list(F[k])
        if 'chain' in p: p['chain']['via'] = [F[k][0], F[k][1] + 1]
        s['events']['E'][k]['chainHand'] = list(F[k]); s['events']['W'][k]['chainHand'] = [63 - F[k][0], F[k][1]]
    s['events']['E'][REL]['release'] = list(F[REL]); s['events']['W'][REL]['release'] = [63 - F[REL][0], F[REL][1]]
    save(s, D + 'clinchBladeThrow.json'); print('grips', F)

if '--scene' in sys.argv:
    from PIL import Image
    out = sys.argv[sys.argv.index('--scene') + 1]
    CW, H, SC = 150, 64, 4
    LOOK = {'h': ['male-gi', 'fade-hair', 'brown-eyes'], 'd': ['male-red-armor', 'red-armor-shoulders', 'long-hair', 'brown-eyes'], 't': ['male-blue-armor', 'blue-armor-shoulders', 'afro-hair', 'brown-eyes']}
    SP = {}
    def sp(st):
        if st not in SP: SP[st] = load(D + st + '.json')
        return SP[st]
    def lay(c, st, name, k, d, ox):
        s = sp(st); row = s['directions'].index(d); k %= s['frames']
        if name.startswith('W:'):
            for w in s.get('weapons') or []:
                for it in w.get('items', []):
                    p = D + st + f'/main-{it}-{name[2:]}.png'
                    if os.path.exists(p):
                        t = Image.new('RGBA', c.size); t.paste(Image.open(p).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)), (ox - 32, -32)); c.alpha_composite(t)
            return
        p = D + st + '/' + name + '.png'
        if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (ox, 0))
    def put(c, x, y, col):
        if 0 <= x < CW and 0 <= y < H: c.putpixel((x, y), col)
    def cord(c, p0, p1, sag=0):
        (x0, y0), (x1, y1) = p0, p1; n = max(abs(x1 - x0), abs(y1 - y0), 1); pts = []
        for i in range(n + 1):
            t = i / n; q = (round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)))
            if not pts or pts[-1] != q: pts.append(q)
        for x, y in pts:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (x + dx, y + dy) not in pts: put(c, x + dx, y + dy, (0, 0, 0, 255))
        for i, (x, y) in enumerate(pts): put(c, x, y, (255, 255, 255, 255) if i % 2 else (0xad, 0xad, 0xad, 255))
    KN = ['.####....', '#tta#####', '#ttaWWWW#', '.####....']   # tanto in flight, point toward +x (the target)
    PAL = {'#': (0, 0, 0, 255), 't': (0x3b, 0x20, 0x14, 255), 'a': (0xad, 0xad, 0xad, 255), 'W': (255, 255, 255, 255)}
    def knife(c, x, y, back=False):
        for j, r in enumerate(KN):
            for i, ch in enumerate(r[::-1] if back else r):
                if ch != '.': put(c, x - 4 + i, y - 2 + j, PAL[ch])
    HX, DX, TX = 4, 4 + 27, 4 + 27 + 50
    bt = sp('clinchBladeThrow'); ev = bt['events']['E']
    frames, durs = [], []
    seq = list(range(10)) + [9] * 0
    for k in seq:
        c = Image.new('RGBA', (CW, H), (0xc8, 0xcd, 0xd7, 255))
        hit = k - IMP
        tst, tk = ('hitReact', hit) if 0 <= hit < sp('hitReact')['frames'] else ('guard', k)
        for name in ['far-arm', 'body'] + LOOK['t'] + ['arms']: lay(c, tst, name, tk, 'W', TX)
        lay(c, 'clinchBladeThrow', 'far-arm', k, 'E', HX); lay(c, 'clinchHeld', 'far-arm', k, 'W', DX)
        lay(c, 'clinchBladeThrow', 'W:behind', k, 'E', HX)
        for name in ['body'] + LOOK['h']: lay(c, 'clinchBladeThrow', name, k, 'E', HX)
        lay(c, 'clinchBladeThrow', 'W:front', k, 'E', HX)
        for name in ['body'] + LOOK['d']: lay(c, 'clinchHeld', name, k, 'W', DX)
        lay(c, 'clinchHeld', 'arms', k, 'W', DX); lay(c, 'clinchBladeThrow', 'arms', k, 'E', HX); lay(c, 'clinchBladeThrow', 'W:top', k, 'E', HX)
        h = ev[k].get('chainHand'); hp = (HX + h[0], h[1]); tgt = (TX + 26, 31)
        f = {REL: 0.12, 5: 0.55, IMP: 1.0, REC: 0.5}.get(k)
        if f is not None:   # the tanto arcs over the held fighter's head (peak ARC px above the straight line); the cord follows it
            ARC = -9
            kp = (round(hp[0] + (tgt[0] - hp[0]) * f), round(hp[1] + (tgt[1] - hp[1]) * f + ARC * 4 * f * (1 - f)))
            cord(c, hp, kp, sag=ARC * f if k != REC else ARC * f + 2); knife(c, kp[0], kp[1], back=(k == REC))
        frames.append(c.resize((CW * SC, H * SC), Image.NEAREST)); durs.append({3: 160, IMP: 200}.get(k, 83))
    frames += [frames[-1]] * 1; durs += [500]
    frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=durs, loop=0, disposal=2)
    st = Image.new('RGBA', (len(seq) * (CW * SC + 5), H * SC), 'white')
    for i in range(len(seq)): st.paste(frames[i], (i * (CW * SC + 5), 0))
    st.save(out + '-E-candidate.png'); print('wrote', out)
