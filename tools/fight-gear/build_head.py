"""Mongkol (Muay Thai head rope) and Boxing headgear, Layer 5 head items, candidates 2026-11-15.

Mongkol: the approved Headband sheet's band recoloured as a twisted white/red/gold rope, its knot tails cut short
so they stick out behind like the mongkol's tail. Worn over the hair like the headbands.
Boxing headgear: the approved Molded Leather Cap recoloured in red leather, with its ear flaps carried down the
cheeks as padded cheek guards (rows to 19, then an outline). Worn in the helmet slot (hides the hair).
Usage: python3 tools/fight-gear/build_head.py [outdir]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'Paperdolls/Male/Layer 5 - Hair'
F = 64
def mirror_w(a):
    """W must be the exact mirror of E (the posed renderer mirrors E into W)."""
    a[:, 6 * F:7 * F] = a[:, 2 * F:3 * F][:, ::-1]
    return a

def load(p): return np.array(Image.open(p).convert('RGBA'))
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)
def col(img, x, y): return None if img[y, x, 3] == 0 else '%02x%02x%02x' % tuple(img[y, x, :3])

ROPE = ['f4efe2', 'f4efe2', 'c81e2c']

def mongkol():
    src = load(P / 'Headband Red.png'); out = src.copy()
    H, W = src.shape[:2]
    for y in range(H):
        for x in range(W):
            c = col(src, x, y)
            if c is None: continue
            back = (x // F) in (3, 4, 5)
            if y > (13 if back else 16): out[y, x] = 0; continue          # tail cut short (behind the head in back views)
            if c != '000000':
                t = ROPE[(x + y) % 3] if c == 'c43a30' else {'f4efe2': 'c9c1ae', 'c81e2c': '8a0f1e', 'd9a42e': '8f6516'}[ROPE[(x + y) % 3]]
                out[y, x] = hx(t)
    # close the cut tail with an outline end
    for x in range(W):
        for yy in (13, 16):
            if out[yy, x, 3] and not out[yy + 1, x, 3] and yy > 12: out[yy, x] = hx('000000')
    return out

LEATHER = {'4e3022': 'b0201f', '6e4630': 'd8403a', '2f1b12': '6e0f12', 'c48a58': 'ff8a70'}

def headgear():
    src = load(P / 'Molded Leather Cap.png'); out = np.zeros_like(src)
    H, W = src.shape[:2]
    for y in range(H):
        for x in range(W):
            c = col(src, x, y)
            if c is None: continue
            out[y, x] = hx('000000') if c == '000000' else hx(LEATHER.get(c, 'b0201f'))
    for f in range(W // F):
        ox = f * F
        # ear flaps: runs of cap pixels on row 14; carry them down as cheek guards to row 19
        row = [x for x in range(F) if src[14, ox + x, 3]]
        runs, cur = [], []
        for x in row:
            if cur and x != cur[-1] + 1: runs.append(cur); cur = []
            cur.append(x)
        if cur: runs.append(cur)
        for r in runs:
            lo, hi = r[0], r[-1]
            if hi - lo < 1: continue
            for y in range(15, 20):
                for x in range(lo, hi + 1):
                    edge = x in (lo, hi)
                    out[y, ox + x] = hx('000000') if edge else hx('d8403a' if x == lo + 1 else 'b0201f')
            for x in range(lo, hi + 1): out[20, ox + x] = hx('000000')
            # padding: widen the guard 1px toward the face where the flap is a bare outline pair
            if hi - lo == 1:
                inward = 1 if (lo % F) < 32 else -1
                for y in range(13, 20):
                    xi = (hi if inward > 0 else lo)
                    out[y, ox + xi] = hx('b0201f'); out[y, ox + xi + inward] = hx('000000')
                for x in range(min(lo, lo + inward), max(hi, hi + inward) + 1): out[20, ox + x] = hx('000000')
    # back views: a dark lacing seam down the middle of the back pad
    for f in (3, 4, 5):
        ox = f * F
        xs = [x for x in range(F) if out[14, ox + x, 3] and tuple(out[14, ox + x, :3]) != (0, 0, 0)]
        if xs:
            cx = (xs[0] + xs[-1]) // 2
            for y in range(11, 20):
                if out[y, ox + cx, 3] and tuple(out[y, ox + cx, :3]) != (0, 0, 0): out[y, ox + cx] = hx('6e0f12' if y % 2 else 'f4efe2')
    return out

if __name__ == '__main__':
    o = Path(sys.argv[1]) if len(sys.argv) > 1 else P
    o.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mirror_w(mongkol())).save(o / 'Mongkol.png')
    Image.fromarray(mirror_w(headgear())).save(o / 'Boxing Headgear.png')
    print('ok')
