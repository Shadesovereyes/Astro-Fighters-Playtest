"""Thai gloves and Boxing gloves (Layer 4 arm accessories), candidates 2026-11-15.

Paperdoll: every Arms1 pixel from the top of the wrist wrap down (wrap = cuff, hand = glove), recoloured by the
skin tone it replaces; the rig carries it on the forearm-hand part like a vambrace. grow() then pads the glove
outward (Boxing: 1px of leather plus a new outline, Thai: a new outline only), and is run on the paperdoll and on
every rendered state's glove sheet, so a glove reads bigger than the bare fist in every pose.
Usage: python3 tools/fight-gear/build_gloves.py [outdir]            paperdoll sheets
       python3 tools/fight-gear/build_gloves.py --grow <state dir>... pad rendered glove sheets in place
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'Paperdolls/Male'
F = 64
def load(p): return np.array(Image.open(p).convert('RGBA'))
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)
def col(img, x, y): return None if img[y, x, 3] == 0 else '%02x%02x%02x' % tuple(img[y, x, :3])

SKIN = {'f6a35b': 0, 'c87845': 1, '9e4a31': 2, '70241d': 3, '3f0505': 3}
WRAP = {'ffffff': 0, 'e3e3e3': 1}
GLOVES = {
    'boxing-gloves': dict(file='Boxing Gloves.png', grow=1,
        glove=['#ff6a5c', '#d42a2a', '#8e1418', '#560a0e'], cuff=['#d42a2a', '#ffffff']),
    'thai-gloves': dict(file='Thai Gloves.png', grow=1,
        glove=['#6a6a7a', '#3e3e4a', '#26262e', '#18181e'], cuff=['#ffd75e', '#d9a42e']),
}

def paperdoll(g):
    A = load(P / 'Layer 3 - Arms/Male Arms1.png')
    out = np.zeros_like(A)
    W, H = A.shape[1], A.shape[0]
    for f in range(W // F):
        ox = f * F
        # each arm column-cluster: wrap top row found per connected arm (left half / right half of the frame by x)
        seen_wrap = {}
        for y in range(H):
            for x in range(F):
                if col(A, ox + x, y) in WRAP:
                    side = 0 if x < 32 else 1
                    seen_wrap.setdefault(side, y)
        for y in range(H):
            for x in range(F):
                c = col(A, ox + x, y)
                if c is None: continue
                side = 0 if x < 32 else 1
                top = seen_wrap.get(side)
                if top is None or y < top - (0 if c in WRAP else 0): continue
                # outline row above the wrap (where the arm meets the cuff) stays the arm's
                if c == '000000': out[y, ox + x] = hx('000000')
                elif c in WRAP: out[y, ox + x] = hx(g['cuff'][WRAP[c]])
                else: out[y, ox + x] = hx(g['glove'][SKIN.get(c, 1)])
    return out

def grow(img, g):
    """Pad the glove (rows below its cuff) outward by g['grow'] px of leather and a fresh outline."""
    a = img.copy()
    H, W = a.shape[:2]
    cuffs = {tuple(hx(c)[:3]) for c in g['cuff']}
    gl = [tuple(hx(c)[:3]) for c in g['glove']]
    def is_glove(y, x): return a[y, x, 3] and tuple(a[y, x, :3]) in gl
    for step in range(g['grow']):
        add = []
        for y in range(H):
            for x in range(W):
                if a[y, x, 3] and tuple(a[y, x, :3]) == (0, 0, 0):
                    # outline pixel touching glove leather becomes leather (the glove swells)
                    if any(0 <= y + dy < H and 0 <= x + dx < W and is_glove(y + dy, x + dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        add.append((y, x))
        for y, x in add: a[y, x] = hx(g['glove'][2])
    # fresh outline round all leather and cuff
    ring = []
    for y in range(H):
        for x in range(W):
            if a[y, x, 3]: continue
            if (x // F) != ((x + 1) // F) and False: pass
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and nx // F == x // F and a[ny, nx, 3] and tuple(a[ny, nx, :3]) != (0, 0, 0):
                    ring.append((y, x)); break
    for y, x in ring: a[y, x] = hx('000000')
    return a

if __name__ == '__main__':
    if sys.argv[1:2] == ['--grow']:
        for d in sys.argv[2:]:
            for name, g in GLOVES.items():
                p = Path(d) / f'{name}.png'
                if p.exists(): Image.fromarray(grow(load(p), g)).save(p)
        sys.exit()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else P
    (out / 'Layer 4 - Shoulders and Arms accessories').mkdir(parents=True, exist_ok=True)
    for name, g in GLOVES.items():
        Image.fromarray(grow(paperdoll(g), g)).save(out / 'Layer 4 - Shoulders and Arms accessories' / g['file'])
    print('ok')
