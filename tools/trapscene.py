"""Preview of each trap as the testbed would play it: thrower facing E on the left, a target facing W at the trap's cell
on the right; the item flies from the thrower's release event to the cell (drawn here the way the testbed is asked to),
then the landing sheet plays there (ground layer under the fighters, air layer over). 3x nearest.
usage: trapscene.py <out-dir>   (run traps.py, render, traps.py --items <item>, render, traps_fx.py first)"""
import json, os, sys, math
from PIL import Image
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
import traps
A = traps.D; FXD = traps.FXD
LAY = ['far-arm', 'body', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'fx', 'impact-fx']
S = {}
def spec(st):
    if st not in S: S[st] = json.load(open(A + st + '.json'))
    return S[st]
def fighter(c, st, k, d, ox, oy, alpha=1.0):
    s = spec(st); row = s['directions'].index(d); k %= s['frames']
    for name in LAY:
        p = A + st + '/' + name + '.png'
        if os.path.exists(p):
            im = Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64))
            if alpha < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
            c.alpha_composite(im, (ox, oy))
PAL = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for k, v in traps.PAL.items()}
def pat(c, rows, x, y, flip=False):
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row[::-1] if flip else row):
            if ch != '.' and 0 <= x + xx < c.width and 0 <= y + yy < c.height: c.putpixel((x + xx, y + yy), PAL[ch])
CW, H = 290, 100; TX, TY = 4, H - 72; GX = 170
FL = 6                      # flight ticks
SINGLE = ['.#.#.', '#a#a#', '.#a#.', '#a#a#', '.#.#.']

def scene(trap, out):
    clip, item, sheet = traps.TRAPS[trap]
    M = json.load(open(FXD + 'traps.json')); m = M[sheet]
    s = spec(clip); n = s['frames']
    rel = next(e for e in s['events']['E'] if 'release' in e); rk, rp = rel['frame'], rel['release']
    land = rk + FL; burst = m['burst']; dmg = burst.get('damage', burst.get('blind'))
    gseq = list(range(m['frames']))
    if 'linger' in m: gseq = [k for k in gseq if k not in m['linger']['frames'] and k not in m['linger'].get('then', [])] + m['linger']['frames'] * 3 + m['linger'].get('then', [])
    total = land + len(gseq) + 4
    ground = Image.open(FXD + sheet + '-ground.png').convert('RGBA'); air = Image.open(FXD + sheet + '-air.png').convert('RGBA')
    fw, fh = m['frameSize']; ax, ay = m['anchor']
    cell = (GX + 32, TY + 63)
    imgs = []; root = [0, 0]
    for t in range(total):
        c = Image.new('RGBA', (CW, H), (0xc8, 0xcd, 0xd7, 255))
        g = gseq[t - land] if land <= t < land + len(gseq) else None
        if g is not None: c.alpha_composite(ground.crop((g * fw, 0, g * fw + fw, fh)), (cell[0] - ax, cell[1] - ay))
        if t < n: root = [root[0] + s['rootMotion']['E'][t][0], root[1] + s['rootMotion']['E'][t][1]]
        fighter(c, clip if t < n else 'guard', t if t < n else (t - n) // 2, 'E', TX + root[0], TY + root[1])
        hit = land + dmg if dmg is not None else None
        if hit is not None and hit <= t < hit + 7: fighter(c, 'hitReact', t - hit, 'W', GX, TY)
        else: fighter(c, 'guard', t // 2, 'W', GX, TY)
        if rk < t <= land:      # in flight
            f = (t - rk) / FL; x0, y0 = TX + root[0] + rp[0], TY + root[1] + rp[1]
            hgt = (0.15 if item == 'tagKunai' else 0.35) * (cell[0] - x0)
            x = x0 + (cell[0] - x0) * f; y = y0 + (cell[1] - 4 - y0) * f - hgt * 4 * f * (1 - f)
            if item == 'caltrops':
                for j, sp in enumerate((-9, -3, 3, 9)): pat(c, SINGLE, round(x + sp * f) - 2, round(y + sp * f * 0.4) - 2)
            elif t < land: pat(c, traps.ITEMS[item], round(x) - len(traps.ITEMS[item][0]) // 2, round(y) - 2)
        if g is not None: c.alpha_composite(air.crop((g * fw, 0, g * fw + fw, fh)), (cell[0] - ax, cell[1] - ay))
        imgs.append(c.resize((CW * 3, H * 3), Image.NEAREST))
    save(imgs, out)

def drop_scene(out):
    s = spec('smokeDrop'); n = s['frames']; imgs = []; root = [0, 0]
    for t in range(n + 8):
        c = Image.new('RGBA', (CW // 2, H), (0xc8, 0xcd, 0xd7, 255))
        if t < n: fighter(c, 'smokeDrop', t, 'E', 30, TY)
        else:
            fighter(c, 'guard', (t - n) // 2, 'E', 30, TY, alpha=0.35)       # Stealth: the testbed's own faded look
        imgs.append(c.resize((CW // 2 * 3, H * 3), Image.NEAREST))
    save(imgs, out)

def save(imgs, out):
    imgs[0].save(out + '.gif', save_all=True, append_images=imgs[1:] + [imgs[-1]] * 6, duration=83, loop=0, disposal=2)
    N = min(12, len(imgs)); pick = [imgs[round(i * (len(imgs) - 1) / (N - 1))] for i in range(N)]; w, h = pick[0].size
    sheet = Image.new('RGBA', (w * 2 + 4, (h + 4) * ((len(pick) + 1) // 2)), 'white')
    for i, im in enumerate(pick): sheet.paste(im, ((i % 2) * (w + 4), (i // 2) * (h + 4)))
    sheet.save(out + '-frames.png'); print('wrote', out)

if __name__ == '__main__':
    o = sys.argv[1]; only = sys.argv[2:]
    for trap, slug in (('Explosive Tag', 'explosive-tag'), ('Flash Bomb', 'flash-bomb'), ('Smoke Screen', 'smoke-screen'), ('Spike Pit', 'spike-pit'), ('Caltrops', 'caltrops')):
        if not only or slug in only: scene(trap, os.path.join(o, slug + '-candidate'))
    if not only or 'smoke-bomb' in only: drop_scene(os.path.join(o, 'smoke-bomb-candidate'))
