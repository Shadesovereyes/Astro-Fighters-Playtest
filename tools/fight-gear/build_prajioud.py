"""Prajioud (Muay Thai armbands), Layer 4 arm accessory, candidate 2026-11-15.

A 2-row red cloth band round each upper arm a third of the way down from the shoulder, tied on the outer side with
a short hanging tail; every pixel sits on the upper-arm part, so the rig carries it like a shoulder piece.
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
            r0 = top + max(2, (bot - top) // 3)
            cx = sum(x for x, _ in pts) / len(pts)
            outer = -1 if cx < 32 else 1
            for y in (r0, r0 + 1):
                xs = sorted(x for x, yy in pts if yy == y)
                if not xs: continue
                for x in range(xs[0], xs[-1] + 1):
                    edge = x in (xs[0], xs[-1])
                    out[y, ox + x] = hx('000000') if edge else hx(RED[0] if y == r0 else RED[1])
            # tail on the outer side, hanging two rows
            xs = sorted(x for x, yy in pts if yy == r0 + 1)
            if xs and f not in (2, 6):
                tx = xs[0] if outer < 0 else xs[-1]
                for y in (r0 + 2, r0 + 3):
                    out[y, ox + tx] = hx(RED[2]); out[y, ox + tx + outer] = hx('000000')
                out[r0 + 4, ox + tx] = hx('000000')
            elif xs:   # profile: knot shows as a darker pixel at the band's back
                out[r0 + 1, ox + xs[1]] = hx(RED[2])
    return out

if __name__ == '__main__':
    o = Path(sys.argv[1]) if len(sys.argv) > 1 else P
    (o / 'Layer 4 - Shoulders and Arms accessories').mkdir(parents=True, exist_ok=True)
    Image.fromarray(mirror_w(build())).save(o / 'Layer 4 - Shoulders and Arms accessories/Prajioud.png'); print('ok')
