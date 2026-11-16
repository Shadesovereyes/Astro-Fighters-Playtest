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
HI, MID, DK = 'd8403a', 'b0201f', '6e0f12'
HEAD = (230, 25, 75)

def headgear_v1():
    """v1 (S and N approved 2026-11-16): the Molded Leather Cap in red leather with its ear flaps carried down the cheeks."""
    src = load(P / 'Molded Leather Cap.png'); out = np.zeros_like(src)
    H, W = src.shape[:2]
    for y in range(H):
        for x in range(W):
            c = col(src, x, y)
            if c is None: continue
            out[y, x] = hx('000000') if c == '000000' else hx(LEATHER.get(c, 'b0201f'))
    for f in range(W // F):
        ox = f * F
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
            if hi - lo == 1:
                inward = 1 if (lo % F) < 32 else -1
                for y in range(13, 20):
                    xi = (hi if inward > 0 else lo)
                    out[y, ox + xi] = hx('b0201f'); out[y, ox + xi + inward] = hx('000000')
                for x in range(min(lo, lo + inward), max(hi, hi + inward) + 1): out[20, ox + x] = hx('000000')
    for f in (3, 4, 5):
        ox = f * F
        xs = [x for x in range(F) if out[14, ox + x, 3] and tuple(out[14, ox + x, :3]) != (0, 0, 0)]
        if xs:
            cx = (xs[0] + xs[-1]) // 2
            for y in range(11, 20):
                if out[y, ox + cx, 3] and tuple(out[y, ox + cx, :3]) != (0, 0, 0): out[y, ox + cx] = hx('6e0f12' if y % 2 else 'f4efe2')
    return out

def headgear():
    """v2 (2026-11-16): S and N kept from v1 (approved); the side and 3/4 views are rebuilt from the head itself so the
    gear frames the ears and face and never sits in front of the face: it covers the head except the face (from one
    px behind the eyes to the head's front edge, brow to chin), with a black rim round the face opening, and adds one
    px of padding only on top and at the back of the head."""
    out = headgear_v1()
    B = load(ROOT / 'Paperdolls/Male/Layer 1 - Base Body/Male Base Body1.png')
    M = load(ROOT / 'production/source/characters/rig/male/part-map.png')
    E = load(ROOT / 'Paperdolls/Male/Layer 6 - Eyes/Brown Eyes.png')
    for f in (1, 2, 3, 5, 6, 7):
        ox = f * F
        out[:, ox:ox + F] = 0
        head = {(x, y) for y in range(22) for x in range(F) if B[y, ox + x, 3] and tuple(M[y, ox + x, :3]) == HEAD}
        eyes = [(x, y) for y in range(F) for x in range(F) if E[y, ox + x, 3]]
        hx0 = min(x for x, _ in head); hx1 = max(x for x, _ in head); hcx = (hx0 + hx1) / 2
        ex = [x for x, _ in eyes]; ey0 = min(y for _, y in eyes)
        front = 1 if sum(ex) / len(ex) > hcx else -1                 # the side the face looks to
        edge = (min(ex) - 1) if front > 0 else (max(ex) + 1)         # the face starts one px behind the eyes
        brow, chin = ey0 - 2, 19
        def is_face(x, y): return brow <= y <= chin and ((x >= edge) if front > 0 else (x <= edge))
        gear = {p for p in head if not is_face(*p) and p[1] <= chin}
        # padding: one px outward on top and at the back only (never in front of the face)
        pad = set()
        for (x, y) in gear:
            for dx, dy in ((0, -1), (-front, 0)):
                q = (x + dx, y + dy)
                if q not in head and 0 <= q[0] < F and q[1] >= 0: pad.add(q)
        gear |= pad
        top = min(y for _, y in gear)
        for (x, y) in gear:
            out[y, ox + x] = hx(HI if y <= top + 1 else (DK if (x - hcx) * front < -3 and y > brow else MID))
        # black outline: gear pixels that border empty space or the face opening
        for (x, y) in gear:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in gear and (q not in head or is_face(*q) or q[1] > chin):
                    out[y, ox + x] = hx('000000'); break
        # ear opening (Christopher 2026-11-16): a 2x2 hole over the ear, midway along the side panel at eye height,
        # ringed in black, so the ear shows through the side panel
        side = sorted(x for (x, y) in gear if y == ey0 + 1 and tuple(out[y, ox + x, :3]) != (0, 0, 0))
        if len(side) >= 3:
            ex_ = side[len(side) // 2] - (1 if front > 0 else 0)
            hole = {(ex_ + dx, ey0 + 1 + dy) for dx in (0, 1) for dy in (0, 1)}
            for (x, y) in hole:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        q = (x + dx, y + dy)
                        if q in gear and q not in hole: out[q[1], ox + q[0]] = hx('000000')
            for (x, y) in hole: out[y, ox + x] = 0
        # lower edge: close the cheek guards and back pad one row under the chin row
        for x in range(F):
            if out[chin, ox + x, 3] and tuple(out[chin, ox + x, :3]) != (0, 0, 0) and (x, chin + 1) not in gear:
                out[chin + 1, ox + x] = hx('000000')
    return out

if __name__ == '__main__':
    o = Path(sys.argv[1]) if len(sys.argv) > 1 else P
    o.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mirror_w(mongkol())).save(o / 'Mongkol.png')
    Image.fromarray(mirror_w(headgear())).save(o / 'Boxing Headgear.png')
    print('ok')
