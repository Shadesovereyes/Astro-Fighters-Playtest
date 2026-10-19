"""Preview of the Kyoketsu-Shoge grapple as the testbed would play it: thrower facing E on the left, target facing W at
range on the right; the chain between them (thrower chainHand event -> target coil event) is drawn here the way the
testbed is asked to draw it (1 px links, white/steel alternating, black outline). 3x nearest.
usage: chainscene.py <out-prefix>"""
import json, os, sys
from PIL import Image
A = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
LAY = ['W:behind', 'far-arm', 'body', 'male-gi', 'W:front', 'fade-hair', 'brown-eyes', 'arms', 'W:top', 'fx']
S = {}
def spec(st):
    if st not in S: S[st] = json.load(open(A + st + '.json'))
    return S[st]
def layer(st, name, k, d):
    s = spec(st); row = s['directions'].index(d)
    if name.startswith('W:'):
        out = []
        for w in (s.get('weapons') or []):
            for it in w.get('items', []):
                p = A + st + f'/main-{it}-{name[2:]}.png'
                if os.path.exists(p): out.append((Image.open(p).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)), -32))
        return out
    p = A + st + '/' + name + '.png'
    return [(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), 0)] if os.path.exists(p) else []
def ev(st, k, d, key):
    e = (spec(st).get('events') or {}).get(d) or []
    for x in e:
        if x.get('frame') == k and key in x: return x[key]
    return None
CW, H = 200, 64
def line(c, p0, p1):
    (x0, y0), (x1, y1) = p0, p1; n = max(abs(x1 - x0), abs(y1 - y0), 1); pts = []
    for i in range(n + 1):
        q = (round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n))
        if not pts or pts[-1] != q: pts.append(q)
    for x, y in pts:
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if 0 <= x + dx < CW and 0 <= y + dy < H and (x + dx, y + dy) not in pts: c.putpixel((x + dx, y + dy), (0, 0, 0, 255))
    for i, (x, y) in enumerate(pts):
        if 0 <= x < CW and 0 <= y < H: c.putpixel((x, y), (255, 255, 255, 255) if i % 2 else (0xad, 0xad, 0xad, 255))
def weight(c, p):
    x, y = p
    for dy, row in enumerate(['.###.', '#aWa#', '#aaa#', '.#a#.', '..#..']):
        for dx, ch in enumerate(row):
            if ch != '.' and 0 <= x - 2 + dx < CW and 0 <= y - 1 + dy < H: c.putpixel((x - 2 + dx, y - 1 + dy), {'#': (0, 0, 0, 255), 'a': (0xad, 0xad, 0xad, 255), 'W': (255, 255, 255, 255)}[ch])
def scene(seq, out):
    imgs = []; tx = 8; gx = 120; troot = [0, 0]; groot = [0, 0]
    for (ts, tk, gs, gk, extra) in seq:
        rm = spec(ts)['rootMotion']['E'][tk]; troot = [troot[0] + rm[0], troot[1] + rm[1]]
        rg = spec(gs)['rootMotion']['W'][gk]; groot = [groot[0] + rg[0], groot[1] + rg[1]]
        gx += extra.get('pull', 0)
        c = Image.new('RGBA', (CW, H), (0xc8, 0xcd, 0xd7, 255))
        for st, k, d, ox, r in ((gs, gk, 'W', gx, groot), (ts, tk, 'E', tx, troot)):
            for name in LAY:
                for im, off in layer(st, name, k, d): c.alpha_composite(im, (ox + r[0] + off, r[1] + off))
        h = ev(ts, tk, 'E', 'chainHand'); co = ev(gs, gk, 'W', 'coil')
        if h:
            hp = (tx + troot[0] + h[0], troot[1] + h[1])
            if 'fly' in extra:      # the weight in flight toward the target
                gp = (gx + groot[0] + 32, 30); f = extra['fly']; tip = (round(hp[0] + (gp[0] - hp[0]) * f), round(hp[1] + (gp[1] - hp[1]) * f) - 3)
                line(c, hp, tip); weight(c, tip)
            elif co:
                line(c, hp, (gx + groot[0] + co[0], groot[1] + co[1]))
        imgs.append(c.resize((CW * 3, H * 3), Image.NEAREST))
    imgs[0].save(out + '.gif', save_all=True, append_images=imgs[1:], duration=[x[4].get('ms', 90) for x in seq], loop=0, disposal=2)
    sheet = Image.new('RGBA', (CW * 3, H * 3 * len(imgs)), 'white')
    for i, im in enumerate(imgs): sheet.paste(im, (0, i * H * 3))
    sheet.save(out + '-frames.png'); print('wrote', out)

if __name__ == '__main__':
    o = sys.argv[1]
    G = [0, 1, 2, 3]
    snare = [('chainSnare', k, 'guard', G[k % 4], {'fly': {4: 0.45, 5: 0.9}[k]} if k in (4, 5) else {}) for k in range(6)]
    snare += [('chainSnare', k, 'snared', (k - 6) % 4, {}) for k in (6, 7)]
    snare += [('chainHold', k % 4, 'snared', k % 4, {'ms': 160}) for k in range(8)]
    scene(snare, o + 'kusari-chain-snare-candidate')
    pull = {1: -15, 2: -22, 3: -18}
    yank = [('chainYank', k, 'chainYanked', k if k < 6 else 5, {'pull': pull.get(k, 0)}) for k in range(7)]
    yank += [('chainHold', k % 4, 'snared', k % 4, {'ms': 160}) for k in range(8)]
    scene(yank, o + 'chain-yank-candidate')
