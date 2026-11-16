"""Prajioud (Muay Thai armbands), Layer 4 arm accessory, candidate 2026-11-15.

A 2-row red cloth band round each upper arm halfway down from the shoulder (on the bicep), tied with a knot on the outer
side; every pixel sits on the upper-arm part, so the rig carries it like a shoulder piece.
Usage: python3 tools/fight-gear/build_prajioud.py [outdir]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'Paperdolls/Male'
F = 64
def mirror_w(a):
    """W must be the exact mirror of E (the posed renderer mirrors E into W)."""
    a[:, 6 * F:7 * F] = a[:, 2 * F:3 * F][:, ::-1]
    return a

def load(p): return np.array(Image.open(p).convert('RGBA'))
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)
def col(img, x, y): return None if img[y, x, 3] == 0 else '%02x%02x%02x' % tuple(img[y, x, :3])
UPPER = {'0082c8', '911eb4'}
RED = ['e8434a', 'c81e2c', '8a0f1e']

def build():
    A = load(P / 'Layer 3 - Arms/Male Arms1.png'); M = load(ROOT / 'production/source/characters/rig/male/part-map.png')
    out = np.zeros_like(A)
    for f in range(A.shape[1] // F):
        ox = f * F
        for part in UPPER:
            pts = [(x, y) for y in range(F) for x in range(F) if A[y, ox + x, 3] and col(M, ox + x, y) == part]
            if not pts: continue
            top = min(y for _, y in pts); bot = max(y for _, y in pts)
            r0 = top + max(2, (bot - top) // 2)       # on the bicep, clear of the shoulder cap (v1 sat on the cap)
            band = sorted(x for x, yy in pts if yy == r0)
            if not band or band[-1] - band[0] < 3: continue   # a far arm showing as a sliver gets no band
            cx = sum(x for x, _ in pts) / len(pts)
            outer = -1 if cx < 32 else 1
            for y in (r0, r0 + 1):
                xs = sorted(x for x, yy in pts if yy == y)
                if not xs: continue
                for x in range(xs[0], xs[-1] + 1):
                    edge = x in (xs[0], xs[-1])
                    out[y, ox + x] = hx('000000') if edge else hx(RED[0] if y == r0 else RED[1])
            # knot: a darker pixel on the outer side of the band (v1's hanging tail read as a stripe down the arm)
            xs = sorted(x for x, yy in pts if yy == r0 + 1)
            if len(xs) >= 4:
                kx = xs[1] if outer < 0 else xs[-2]
                if f in (2, 6): kx = xs[1]
                out[r0 + 1, ox + kx] = hx(RED[2]); out[r0, ox + kx] = hx(RED[1])
    return out

if __name__ == '__main__':
    o = Path(sys.argv[1]) if len(sys.argv) > 1 else P
    (o / 'Layer 4 - Shoulders and Arms accessories').mkdir(parents=True, exist_ok=True)
    Image.fromarray(mirror_w(build())).save(o / 'Layer 4 - Shoulders and Arms accessories/Prajioud.png'); print('ok')
