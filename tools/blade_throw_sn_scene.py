"""S/N scene preview for Blade Throw: thrower + target stacked (S: target toward the viewer, below; N: target away, above),
the tanto flying point-first on its chain from chainHand (frames 3-6), as the E scene in blade_throw.py --scene."""
import sys, os, json
from PIL import Image
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
ST = 'bladeThrow'; IMP, REL, REC = 5, 3, 6
H_LOOK = ['male-gi', 'fade-hair', 'brown-eyes']; T_LOOK = ['male-blue-armor', 'blue-armor-shoulders', 'afro-hair', 'brown-eyes']
SP = {}
def sp(st):
    if st not in SP: SP[st] = json.load(open(D + st + '.json'))
    return SP[st]
def lay(c, st, name, k, d, ox, oy):
    s = sp(st); row = s['directions'].index(d); k %= s['frames']
    if name.startswith('W:'):
        for w in s.get('weapons') or []:
            for it in w.get('items', []):
                p = D + st + f'/main-{it}-{name[2:]}.png'
                if os.path.exists(p):
                    t = Image.new('RGBA', c.size); t.paste(Image.open(p).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)), (ox - 32, oy - 32)); c.alpha_composite(t)
        return
    p = D + st + '/' + name + '.png'
    if os.path.exists(p):
        t = Image.new('RGBA', c.size); t.paste(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (ox, oy)); c.alpha_composite(t)
def put(c, x, y, col):
    if 0 <= x < c.width and 0 <= y < c.height: c.putpixel((x, y), col)
def cord(c, p0, p1, sag=0):
    (x0, y0), (x1, y1) = p0, p1; n = max(abs(x1 - x0), abs(y1 - y0), 1); pts = []
    for i in range(n + 1):
        t = i / n; q = (round(x0 + (x1 - x0) * t + sag * 4 * t * (1 - t)), round(y0 + (y1 - y0) * t))
        if not pts or pts[-1] != q: pts.append(q)
    for x, y in pts:
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (x + dx, y + dy) not in pts: put(c, x + dx, y + dy, (0, 0, 0, 255))
    for i, (x, y) in enumerate(pts): put(c, x, y, (255, 255, 255, 255) if i % 2 else (0xad, 0xad, 0xad, 255))
KN = ['.###.#########..', '#ttt#WWWWWWWWW##', '#ttt#aaaaaaaaa#.', '.###.#########..']
PAL = {'#': (0, 0, 0, 255), 't': (0x3b, 0x20, 0x14, 255), 'a': (0xad, 0xad, 0xad, 255), 'W': (255, 255, 255, 255)}
def knife(c, x, y, down):   # (x, y) = pommel; the blade runs down (S, toward the viewer) or up (N, away), foreshortened to 10 px
    rows = [r[:5] + r[5:][::2] for r in KN] if False else KN
    L = len(KN[0]); keep = list(range(0, 5)) + list(range(5, L, 2))   # shorten: blade foreshortened along the view axis
    for j, r in enumerate(KN):
        for n, i in enumerate(keep):
            ch = r[i]
            if ch != '.': put(c, x - 1 + j, y + (n if down else -n), PAL[ch])
def scene(view):
    W, Hh = 64, 132
    th = sp(ST); ev = th['events'][view]; out = []
    # S: thrower at top facing S, target below facing N (its back to us). N: thrower at bottom facing N, target above facing S.
    if view == 'S': TY, GY, tdir = 0, 66, 'N'
    else: TY, GY, tdir = 66, 0, 'S'
    for k in range(th['frames']):
        c = Image.new('RGBA', (W, Hh), (0xc8, 0xcd, 0xd7, 255))
        hit = k - IMP
        tst, tk = ('hitReact', hit) if 0 <= hit < sp('hitReact')['frames'] else ('guard', k)
        def target():
            for name in ['far-arm', 'body'] + T_LOOK + ['arms']: lay(c, tst, name, tk, tdir, 0, GY)
        def thrower():
            for name in ['W:behind', 'far-arm', 'body'] + H_LOOK + ['W:front', 'arms', 'W:top']: lay(c, ST, name, k, view, 0, TY)
        f = {REL: 0.12, 4: 0.55, IMP: 1.0, REC: 0.5}.get(k)
        def blade():
            if f is None: return
            h = ev[k]['chainHand']; hp = (h[0], TY + h[1])
            tgt = (32, GY + (20 if view == 'S' else 42))    # S: the target's upper back; N: its chest, seen past the thrower
            kp = (round(hp[0] + (tgt[0] - hp[0]) * f), round(hp[1] + (tgt[1] - hp[1]) * f))
            cord(c, hp, kp, sag=2 * f); knife(c, kp[0], kp[1], view == 'S')
        if view == 'S': thrower(); target(); blade()      # the target is nearer the viewer: drawn over the thrower
        else: target(); thrower(); blade()
        out.append(c)
    return out
o = sys.argv[1]; SC = 4
S, N = scene('S'), scene('N'); frames, durs = [], []
for k in range(len(S)):
    f = Image.new('RGBA', (2 * 64 + 6, 132), 'white'); f.paste(S[k], (0, 0)); f.paste(N[k], (70, 0))
    frames.append(f.resize((f.width * SC, f.height * SC), Image.NEAREST)); durs.append({2: 160, IMP: 200}.get(k, 83))
frames += [frames[-1]]; durs += [500]
frames[0].save(o + '-candidate.gif', save_all=True, append_images=frames[1:], duration=durs, loop=0, disposal=2)
n = len(S); st = Image.new('RGBA', (n * (64 * SC + 5), 2 * (132 * SC) + 5), 'white')
for k in range(n):
    st.paste(S[k].resize((64 * SC, 132 * SC), Image.NEAREST), (k * (64 * SC + 5), 0)); st.paste(N[k].resize((64 * SC, 132 * SC), Image.NEAREST), (k * (64 * SC + 5), 132 * SC + 5))
st.save(o + '-SN-candidate.png'); print('wrote', o)
