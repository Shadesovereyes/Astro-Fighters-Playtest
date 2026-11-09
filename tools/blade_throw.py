"""Blade Throw (Kyoketsu-Shoge; range 3, 5 Physical + Bleed). v2 (Christopher 2026-11-06 20:33: "blade throw should not be
usable in clinch and the rope should be a chain"): a standing throw from the Kyoketsu-Shoge Stance idle (oneHandGuard); the
clinch version (clinchBladeThrow) is retired. The near hand raises the blade and cocks it behind the head, slings it forward
(release frame 3); the arm stays out while the testbed flies the blade on its steel chain from the chainHand anchor to the
target (impact frame 5, as Kusari Chain Snare), the chain is yanked (6) and the blade caught back in the fist (7), back to
the guard. E/W first (W mirrors E); S/N after approval.
Run: python3 tools/blade_throw.py ; node tools/character-posed.mjs male bladeThrow ; python3 tools/blade_throw.py --grips ;
     node tools/character-weapon.mjs male bladeThrow ; preview: python3 tools/blade_throw.py --scene <out>"""
import sys, os, copy, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
import tanto as T
from tanto import fr
from gen import load, save
D = T.D
ST = 'bladeThrow'
T.STAT = 'CANDIDATE 2026-11-06 v2 (standing, from the Kyoketsu-Shoge Stance idle; not usable in the clinch) (E/W; W mirrors E; S/N to author after approval)'
OG = dict(grip=(43, 35), angle=10, far=(39, 24))
def og(**k): return fr(**{**OG, **k})
REL, IMP, REC, CATCH = 3, 5, 6, 7
HIDDEN = (3, 4, 5, 6)   # the blade is out on its chain (testbed-drawn from chainHand)
FR = [
    og(),
    og(grip=(38, 24), angle=110, far=(41, 26), lean=(-1, 0), ln='step-rear'),
    og(grip=(31, 16), angle=160, far=(43, 27), lean=(-1, -1), ln='step-rear', z='behind'),
    og(grip=(51, 24), angle=15, far=(38, 27), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), ln='lunge-rear', lf='lunge-lead'),
    og(grip=(52, 27), angle=0, far=(38, 27), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    og(grip=(52, 27), angle=0, far=(38, 27), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    og(grip=(42, 29), angle=0, far=(39, 26), lean=(0, 2), root=(-1, 0)),
    og(grip=(44, 32), angle=30, far=(39, 25), lean=(0, 2)),
    og(root=(-1, 0))]
T.CLIPS[ST] = ('Blade Throw', IMP, None, 'light', 12, 'oneHandGuard', FR)
T.INTENT[ST] = ('Kyoketsu-Shoge Blade Throw, standing (Christopher 2026-11-06 20:33: not usable in the clinch; the cord is a steel chain): '
                'from the one-hand guard the near hand raises the blade and cocks it behind the head (frames 1-2), slings it forward (release frame 3); '
                'the arm stays out while the blade flies on its chain to the target (impact frame 5), yanks it back (6), catches it (7) and returns to the guard (8).')

def spec():
    T.spec(ST, ST)
    s = load(D + ST + '.json'); w = s['weapons'][0]
    w['items'] = ['kyoketsu-shoge']
    w['rule'] = ('per frame: grip = near fist centre (snapped to the rendered fist); frames 3-6 hidden: the blade and its steel chain are out at the target, '
                 'drawn by the testbed from chainHand; while held the chain is wound in the fist (noWeight)')
    for k, p in enumerate(w['E']):
        if k in HIDDEN: p['hidden'] = True; p['omit'] = True; p['chain'] = {'off': True}   # v2.1 (Christopher 2026-11-09: the blade still showed in the hand): omit = not drawn at all
        else: p['chain'] = {'via': [p['grip'][0], p['grip'][1] + 1], 'droop': 0, 'z': 'front', 'to': [0, 1], 'noWeight': True}
    s['extra'] = {'stance': 'Kyoketsu-Shoge Stance', 'notInClinch': True}
    s['clips']['rule'] = 'plays from the Kyoketsu-Shoge Stance idle (oneHandGuard) and returns to it; never from the clinch or Mount; a target within 3 tiles plays hitReact on the impact frame'
    ev = [{'frame': i, 'clip': ST, 'type': 'startup' if i < REL else 'active' if REL <= i <= IMP else 'recovery'} for i in range(len(FR))]
    ev[REL].update({'move': 'bladeThrow', 'release': None, 'rule': 'the blade leaves the fist at chainHand and flies to the target on its chain (testbed-drawn, as Kusari Chain Snare)'})
    ev[IMP].update({'move': 'Blade Throw', 'impact': True, 'effect': '5 Physical; Bleed 2 (AGI DC12, 3 rds)', 'rule': 'impact frame: the target plays hitReact on this frame, never before (ANIMATION_RULES 2026-11-04)'})
    ev[REC].update({'recall': True, 'rule': 'the chain is yanked: the testbed flies the blade back from the target to chainHand, arriving on frame 7'})
    ev[CATCH].update({'catch': True})
    s['events'] = {'rule': 'per-frame gameplay data per facing (provisional); chainHand = near fist centre while the chain is out; impact frame 5', 'E': ev, 'W': copy.deepcopy(ev),
                   'tactical': {'rule': 'no displacement; range 3; not usable while clinched, Grappled or in Mount'}}
    save(s, D + ST + '.json'); print('ok')

if '--grips' in sys.argv:
    T.grips(ST)
    s = load(D + ST + '.json')
    for k, p in enumerate(s['weapons'][0]['E']):
        g = p['grip']
        if 'via' in p.get('chain', {}): p['chain']['via'] = [g[0], g[1] + 1]
        s['events']['E'][k]['chainHand'] = list(g); s['events']['W'][k]['chainHand'] = [63 - g[0], g[1]]
    s['events']['E'][REL]['release'] = list(s['events']['E'][REL]['chainHand']); s['events']['W'][REL]['release'] = list(s['events']['W'][REL]['chainHand'])
    save(s, D + ST + '.json'); print('grips', [p['grip'] for p in s['weapons'][0]['E']])
elif '--scene' not in sys.argv:
    spec()

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
    # v2.1 (Christopher 2026-11-09): the flying object read as the weight. It is the blade: a full-size tanto, point leading
    # toward the target, the chain fixed to its pommel; on the recall it is hauled back pommel first, point still at the target.
    KN = ['.###.#########..', '#ttt#WWWWWWWWW##', '#ttt#aaaaaaaaa#.', '.###.#########..']
    PAL = {'#': (0, 0, 0, 255), 't': (0x3b, 0x20, 0x14, 255), 'a': (0xad, 0xad, 0xad, 255), 'W': (255, 255, 255, 255)}
    def knife(c, x, y, back=False):   # (x, y) = the pommel, where the chain is fixed
        for j, r in enumerate(KN):
            for i, ch in enumerate(r):
                if ch != '.': put(c, x + i, y - 1 + j, PAL[ch])
    HX, TX = 4, 4 + 72
    bt = sp(ST); ev = bt['events']['E']
    frames, durs = [], []
    seq = list(range(len(FR)))
    for k in seq:
        c = Image.new('RGBA', (CW, H), (0xc8, 0xcd, 0xd7, 255))
        hit = k - IMP
        tst, tk = ('hitReact', hit) if 0 <= hit < sp('hitReact')['frames'] else ('guard', k)
        for name in ['far-arm', 'body'] + LOOK['t'] + ['arms']: lay(c, tst, name, tk, 'W', TX)
        lay(c, ST, 'far-arm', k, 'E', HX); lay(c, ST, 'W:behind', k, 'E', HX)
        for name in ['body'] + LOOK['h']: lay(c, ST, name, k, 'E', HX)
        lay(c, ST, 'W:front', k, 'E', HX); lay(c, ST, 'arms', k, 'E', HX); lay(c, ST, 'W:top', k, 'E', HX)
        h = ev[k].get('chainHand'); hp = (HX + h[0], h[1]); tgt = (TX + 26 - len(KN[0]) + 3, 31)
        f = {REL: 0.12, 4: 0.55, IMP: 1.0, REC: 0.5}.get(k)
        if f is not None:   # the blade arcs slightly (peak ARC px above the straight line); the chain follows it
            ARC = -5
            kp = (round(hp[0] + (tgt[0] - hp[0]) * f), round(hp[1] + (tgt[1] - hp[1]) * f + ARC * 4 * f * (1 - f)))
            cord(c, hp, kp, sag=ARC * f if k != REC else ARC * f + 2); knife(c, kp[0], kp[1])
        frames.append(c.resize((CW * SC, H * SC), Image.NEAREST)); durs.append({2: 160, IMP: 200}.get(k, 83))
    frames += [frames[-1]] * 1; durs += [500]
    frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=durs, loop=0, disposal=2)
    st = Image.new('RGBA', (len(seq) * (CW * SC + 5), H * SC), 'white')
    for i in range(len(seq)): st.paste(frames[i], (i * (CW * SC + 5), 0))
    st.save(out + '-E-candidate.png'); print('wrote', out)
