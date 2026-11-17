"""Boxing boots paperdoll sheet (Layer 2 clothing), 2026-11-16 (Christopher: "boxing gear should have shoes").

High-top boots in the trunks' blue, drawn on the approved Gi's ankle wrap and shoe (rows 56-63, every direction) and
carried up the body's shin to row 53, with a white trim row at the top of the shaft. The posed renderer draws them as a
trouser-less garment (trouser.none): the shaft takes the wrap rows (legRows.wrap 53), the foot the shoe colour.
Usage: python3 tools/fight-gear/build_boots.py [outdir]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'Paperdolls/Male'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else P
F, TOP, TRIM, WRAP = 64, 52, 53, 56
BOOT = ['#3b6fe0', '#2f5fcf', '#1d3c94', '#10225c', '#0a1640']   # light .. deepest
TRIMC = ['#ffffff', '#e3e3e8', '#a8a8b4']
SKIN = {'f6a35b': 0, 'c87845': 1, '9e4a31': 2, '70241d': 3, '3f0505': 4}
GIW = {'fefefc': 0, 'dadad9': 1, 'adadad': 2}
SHOE = {'3b2014': 2}
def hx(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255]
def load(p): return np.array(Image.open(p).convert('RGBA'))
GI = load(P / 'Layer 2 - Clothing/Male Gi.png')
BODY = load(P / 'Layer 1 - Base Body/Male Base Body1.png')
BMAP = load(ROOT / 'production/source/characters/rig/male/part-map.png')
LEG = {'f58230', 'aa6e28', '808000', '000080'}

def c(img, x, y): return None if img[y, x, 3] == 0 else '%02x%02x%02x' % tuple(img[y, x, :3])

NEARSHIN = {'R': 'aa6e28', 'L': '000080'}
RIG = __import__('json').loads((ROOT / 'production/source/characters/rig/male/rig.json').read_text())
out = np.zeros_like(GI)
for f in range(8):
    ox = f * F
    near = RIG['frames'][f]['nearSide'] if RIG['frames'][f]['direction'] in ('E', 'W') else None
    # profile views: the posed renderer copies this ankle block onto EACH posed leg, so it must hold the near leg
    # only (a far heel or far shin sliver here would be drawn twice, the doubling in the E/W walk)
    legset = {NEARSHIN[near]} if near else LEG
    for y in range(TOP, F):
        for x in range(F):
            X = ox + x
            if y >= WRAP:
                g = c(GI, X, y)
                if g is None:
                    if near: continue
                    b = c(BODY, X, y)   # body foot/heel the Gi sheet does not cover (far heel in E)
                    if b is None: continue
                    out[y, X] = hx('#000000') if b in ('000000', '030101') else hx(BOOT[min(4, SKIN.get(b, 1) + 1)])
                    continue
                if g in ('030101', '000000'): out[y, X] = hx('#000000')
                elif g in GIW: out[y, X] = hx(BOOT[GIW[g] + 1])
                elif g in SHOE: out[y, X] = hx(BOOT[2])
                else: out[y, X] = hx(BOOT[2])
            else:
                b = c(BODY, X, y)
                if b is None or c(BMAP, X, y) not in legset and b not in ('000000', '030101'): continue
                if b in ('000000', '030101'):
                    # keep only the leg's own outline (side edges of the shin)
                    if any(c(BMAP, X + dx, y) in legset for dx in (-1, 1) if 0 <= x + dx < F): out[y, X] = hx('#000000')
                    continue
                t = SKIN.get(b, 1)
                if y == TOP: out[y, X] = hx('#000000')
                elif y == TRIM: out[y, X] = hx(TRIMC[min(2, t)])
                else: out[y, X] = hx(BOOT[min(4, t + 1)])
# clean outline (Christopher 21:58: heel looked strange): the Gi shoe carries a 2px heel/toe outline and a black seam
# where wrap meets shoe; on a bright boot those read as a black slab. Keep black only on the silhouette edge (a
# transparent 4-neighbour); every other black pixel takes its neighbour's boot colour. Then a light sole row.
for f in range(8):
    ox = f * F
    fr = out[:, ox:ox + F]
    for _ in range(3):
        op = fr[..., 3] > 0
        blk = op & (fr[..., :3].sum(-1) == 0)
        ch = False
        for y in range(TOP + 1, F):
            for x in range(F):
                if not blk[y, x]: continue
                nb = [(y + dy, x + dx) for dy, dx in ((1, 0), (0, -1), (0, 1), (-1, 0))]
                if any(not (0 <= yy < F and 0 <= xx < F) or not op[yy, xx] for yy, xx in nb if yy < F): continue
                if y == F - 1: continue
                src = [fr[yy, xx] for yy, xx in nb if 0 <= yy < F and 0 <= xx < F and op[yy, xx] and not blk[yy, xx]]
                if not src: continue
                fr[y, x] = src[0]; ch = True
        if not ch: break
    if RIG['frames'][f]['direction'] == 'E':
        # profile heel flush with the shaft's back line (the Gi shoe heel sits 2px behind it), 1px heel counter at the sole
        back = min(x for x in range(F) if fr[58, x, 3] > 0)
        for y in range(WRAP, F):
            lim = back if y <= 60 else back - 1 if y < F - 1 else back
            fr[y, :lim] = 0
            if y < F - 1 and fr[y, lim, 3] > 0: fr[y, lim] = hx('#000000')
    for _ in range(2):   # outline spurs (a black pixel with at most one opaque 4-neighbour)
        op = fr[..., 3] > 0
        blk = op & (fr[..., :3].sum(-1) == 0)
        for y in range(TOP + 1, F):
            for x in range(F):
                if blk[y, x] and sum(0 <= y + dy < F and 0 <= x + dx < F and op[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))) <= 1:
                    fr[y, x] = 0
    op = fr[..., 3] > 0
    blk = op & (fr[..., :3].sum(-1) == 0)
    for x in range(F):
        ys = [y for y in range(WRAP, F) if op[y, x] and not blk[y, x]]
        if ys and ys[-1] >= 60: fr[ys[-1], x] = hx(TRIMC[2])
# W is the exact mirror of E (posed renderer requirement), SW of SE, NW of NE
ORDER = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
for a, b in (('E', 'W'), ('SE', 'SW'), ('NE', 'NW')):
    i, j = ORDER.index(a) * F, ORDER.index(b) * F
    out[:, j:j + F] = out[:, i:i + F][:, ::-1]
Image.fromarray(out).save(OUT / 'Layer 2 - Clothing/Male Boxing Boots.png')
print('wrote', OUT / 'Layer 2 - Clothing/Male Boxing Boots.png')
