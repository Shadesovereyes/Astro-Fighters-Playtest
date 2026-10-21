"""Previews for the chain S/N candidates: <out>-SENW-candidate.png (every frame, one row per facing, kama and chain
layers included) and <out>-candidate.gif (the four facings side by side), 4x nearest.
usage: chain_sn_preview.py <state> <out-prefix> | chain_sn_preview.py <out-prefix> --scenes (the thrower and target in S/N
with the chain between them, both ways round)"""
import json, os, sys
from PIL import Image
A = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
LAY = ['W:behind', 'far-arm', 'body', 'male-gi', 'W:front', 'fade-hair', 'brown-eyes', 'arms', 'W:top', 'fx']
def frame(st, s, k, d):
    row = s['directions'].index(d); c = Image.new('RGBA', (96, 96), (0xc8, 0xcd, 0xd7, 255))
    for name in LAY:
        if name.startswith('W:'):
            for w in s.get('weapons') or []:
                for it in w.get('items', []):
                    p = A + st + f'/main-{it}-{name[2:]}.png'
                    if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)).crop((16, 16, 112, 112)), (0, 0))
            continue
        p = A + st + '/' + name + '.png'
        if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (16, 16))
    return c
if __name__ == '__main__' and '--scenes' not in sys.argv:
    st, out = sys.argv[1:3]; s = json.load(open(A + st + '.json')); n = s['frames']; Z = 4; C = 96 * Z; G = 6
    cols = {d: [frame(st, s, k, d).resize((C, C), Image.NEAREST) for k in range(n)] for d in ('S', 'E', 'N', 'W')}
    sheet = Image.new('RGBA', (n * (C + G) - G, 4 * (C + G) - G), 'white')
    for i, d in enumerate('SENW'):
        for k in range(n): sheet.paste(cols[d][k], (k * (C + G), i * (C + G)))
    sheet.save(out + '-SENW-candidate.png')
    fr = []
    for k in range(n):
        f = Image.new('RGBA', (4 * (C + G) - G, C), 'white')
        for i, d in enumerate('SENW'): f.paste(cols[d][k], (i * (C + G), 0))
        fr.append(f)
    fps = s.get('fps', 12)
    for c in (s.get('clips') or {}).values():
        if isinstance(c, dict) and c.get('fps'): fps = c['fps']
    fr[0].save(out + '-candidate.gif', save_all=True, append_images=fr[1:] + [fr[-1]] * 3, duration=int(1000 / fps), loop=0, disposal=2)
    print('wrote', out)

# ---- S/N scene: the thrower and the target on one vertical line, the chain drawn as the testbed draws it ----
def ev(s, k, d, key):
    for x in (s.get('events') or {}).get(d) or []:
        if x.get('frame') == k and key in x: return x[key]
    return None
def line(c, p0, p1):
    (x0, y0), (x1, y1) = p0, p1; n = max(abs(x1 - x0), abs(y1 - y0), 1); pts = []
    for i in range(n + 1):
        q = (round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n))
        if not pts or pts[-1] != q: pts.append(q)
    W, H = c.size
    for x, y in pts:
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if 0 <= x + dx < W and 0 <= y + dy < H and (x + dx, y + dy) not in pts: c.putpixel((x + dx, y + dy), (0, 0, 0, 255))
    for i, (x, y) in enumerate(pts):
        if 0 <= x < W and 0 <= y < H: c.putpixel((x, y), (255, 255, 255, 255) if i % 2 else (0xad, 0xad, 0xad, 255))
def weight(c, p):
    x, y = p
    for dy, row in enumerate(['.###.', '#aWa#', '#aaa#', '.#a#.', '..#..']):
        for dx, ch in enumerate(row):
            if ch != '.': c.putpixel((x - 2 + dx, y - 1 + dy), {'#': (0, 0, 0, 255), 'a': (0xad, 0xad, 0xad, 255), 'W': (255, 255, 255, 255)}[ch])
def scene(seq, out, thrower_dir):
    """thrower_dir S: thrower on top facing the viewer, target below with its back to the viewer; N: the reverse"""
    td, gd = thrower_dir, 'N' if thrower_dir == 'S' else 'S'
    TY, GY = (0, 58) if td == 'S' else (58, 0)
    imgs = []; gy = GY
    for (ts, tk, gs, gk, extra) in seq:
        T, G = json.load(open(A + ts + '.json')), json.load(open(A + gs + '.json'))
        gy += extra.get('pull', 0) * (-1 if td == 'S' else 1)
        c = Image.new('RGBA', (96, 160), (0xc8, 0xcd, 0xd7, 255))
        order = ((gs, G, gk, gd, gy), (ts, T, tk, td, TY)) if td == 'S' else ((ts, T, tk, td, TY), (gs, G, gk, gd, gy))
        for st, s, k, d, y in order: c.alpha_composite(frame(st, s, k, d).convert('RGBA'), (0, y), )
        h = ev(T, tk, td, 'chainHand'); co = ev(G, gk, gd, 'coil')
        if h:
            hp = (16 + h[0], 16 + TY + h[1])
            if 'fly' in extra:
                gp = (48, 16 + gy + 30); f = extra['fly']; tip = (round(hp[0] + (gp[0] - hp[0]) * f), round(hp[1] + (gp[1] - hp[1]) * f))
                line(c, hp, tip); weight(c, tip)
            elif co: line(c, hp, (16 + co[0], 16 + gy + co[1]))
        imgs.append(c.resize((96 * 3, 160 * 3), Image.NEAREST))
    return imgs
def frame(st, s, k, d):   # (redefined: transparent background for the scene)
    row = s['directions'].index(d); c = Image.new('RGBA', (96, 96))
    for name in LAY:
        if name.startswith('W:'):
            for w in s.get('weapons') or []:
                for it in w.get('items', []):
                    p = A + st + f'/main-{it}-{name[2:]}.png'
                    if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)).crop((16, 16, 112, 112)), (0, 0))
            continue
        p = A + st + '/' + name + '.png'
        if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (16, 16))
    return c
def scenes(out):
    G = [0, 1, 2, 3]
    snare = [('chainSnare', k, 'guard', G[k % 4], {'fly': {4: 0.45, 5: 0.9}[k]} if k in (4, 5) else {}) for k in range(6)]
    snare += [('chainSnare', k, 'snared', (k - 6) % 4, {}) for k in (6, 7)] + [('chainHold', k % 4, 'snared', k % 4, {'ms': 160}) for k in range(8)]
    pull = {1: -6, 2: -9, 3: -7}
    yank = [('chainYank', k, 'chainYanked', k if k < 6 else 5, {'pull': pull.get(k, 0)}) for k in range(7)] + [('chainHold', k % 4, 'snared', k % 4, {'ms': 160}) for k in range(8)]
    strug = [('chainHold', k % 4, 'snaredStruggle', k, {}) for k in range(7)] + [('chainHold', k % 4, 'snared', k % 4, {'ms': 160}) for k in range(4)]
    brk = [('chainHold', k % 4, 'snareBreak', k, {}) for k in range(3)] + [('chainRecall', min(k - 3, 3), 'snareBreak', k, {}) for k in range(3, 8)]
    for name, seq in (('kusari-chain-snare', snare), ('chain-yank', yank), ('struggle', strug), ('snare-break', brk)):
        a, b = scene(seq, out, 'S'), scene(seq, out, 'N'); fr = []
        for x, y in zip(a, b):
            f = Image.new('RGBA', (x.width * 2 + 8, x.height), 'white'); f.paste(x, (0, 0)); f.paste(y, (x.width + 8, 0)); fr.append(f)
        fr[0].save(out + name + '-SN-scene-candidate.gif', save_all=True, append_images=fr[1:], duration=[q[4].get('ms', 90) for q in seq], loop=0, disposal=2)
        sheet = Image.new('RGBA', (fr[0].width * min(len(fr), 8), fr[0].height * ((len(fr) + 7) // 8)), 'white')
        for i, f in enumerate(fr): sheet.paste(f, ((i % 8) * f.width, (i // 8) * f.height))
        sheet.save(out + name + '-SN-scene-frames.png'); print('wrote', out + name)
if __name__ == '__main__' and '--scenes' in sys.argv: scenes(sys.argv[1])
