"""Close the seam the posed renderer leaves where a kicking leg's shorts meet the standing leg's shorts.

The near and far trouser legs are drawn as separate pieces, so on a raised or extended leg each piece keeps its own
outline and the seat (glutes) shows a black step or a notch between them (Christopher 2026-11-16: "a gap near the
glutes once the leg is extended"). A black or empty pixel with cloth at most 2 rows above AND 2 rows below in its own
column is filled with the cloth colour below it (or above), and the outline is then redrawn round the cloth.
Usage: python3 tools/fight-gear/close_seams.py <state dir> [...]   (runs on the shorts/trunks sheets in place)
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

SHEETS = ['male-muay-thai-shorts', 'male-boxing-trunks']
# waistband colours (build_shorts.py): a line under the waistband is a designed seam, never closed
BAND = {(0xff, 0xd7, 0x5e), (0xd9, 0xa4, 0x2e), (0x8f, 0x65, 0x16), (0x7a, 0x0f, 0x1c), (0xff, 0xff, 0xff), (0xe3, 0xe3, 0xe8),
        (0xa8, 0xa8, 0xb4), (0xc8, 0x1e, 0x2c), (0xd8, 0xd8, 0xe0), (0xe8, 0xe8, 0xf0)}
F = 64

def seat_clamp(a, body, rows):
    """Profile rows (E/W): the shorts' back edge stays at most 2 px (outline included) behind the body's own back
    line, so a lifted or extended leg's seat does not balloon behind the glutes (Christopher 2026-11-16: knee looks
    strange at the glutes). Standing frames already sit within that limit and do not change."""
    n = 0
    for r, d in enumerate(rows):
        if d not in ('E', 'W'): continue
        for c in range(a.shape[1] // F):
            y0, x0 = r * F, c * F
            A, B = a[y0:y0 + F, x0:x0 + F], body[y0:y0 + F, x0:x0 + F]
            for y in range(F):
                bx = np.where(B[y, :, 3] > 0)[0]
                if not len(bx): continue
                if d == 'E':
                    cut = A[y, :bx.min() - 1, 3] > 0; n += int(cut.sum()); A[y, :bx.min() - 1] = 0
                else:
                    cut = A[y, bx.max() + 2:, 3] > 0; n += int(cut.sum()); A[y, bx.max() + 2:] = 0
    return n

def close(a):
    a = a.copy()
    op = a[..., 3] > 0
    black = op & (a[..., 0] == 0) & (a[..., 1] == 0) & (a[..., 2] == 0)
    cloth = op & ~black
    H, W = op.shape
    fill = np.zeros_like(op)
    src = {}
    for y in range(H):
        cy = y % F
        for x in range(W):
            if cloth[y, x]: continue
            up = [y - d for d in (1, 2) if cy - d >= 0 and cloth[y - d, x]]
            dn = [y + d for d in (1, 2) if cy + d < F and cloth[y + d, x]]
            if up and dn and not any(tuple(a[u, x, :3]) in BAND for u in range(max(y - F, y - 4), y) if op[u, x]):
                fill[y, x] = True; src[(y, x)] = dn[0]
    for (y, x), sy in src.items(): a[y, x] = a[sy, x]
    cloth = cloth | fill
    # a black pixel left inside the cloth (3 or 4 of its 4 neighbours are cloth) is a broken seam end: fill it too
    for _ in range(2):
        add = {}
        for y in range(H):
            for x in range(W):
                if cloth[y, x] or not op[y, x]: continue
                cy, cx = y % F, x % F
                nb = [(y + dy, x + dx) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= cy + dy < F and 0 <= cx + dx < F and cloth[y + dy, x + dx]]
                if len(nb) >= 3: add[(y, x)] = max(nb, key=lambda q: q[0])
        for (y, x), q in add.items(): a[y, x] = a[q]; cloth[y, x] = True; fill[y, x] = True
    # redraw the outline: every non-cloth pixel touching cloth (4-neighbour, same cell) is black; stray black
    # pixels that no longer touch cloth are cleared
    out = np.zeros_like(op)
    for y in range(H):
        for x in range(W):
            if cloth[y, x]: continue
            cy, cx = y % F, x % F
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = cy + dy, cx + dx
                if 0 <= yy < F and 0 <= xx < F and cloth[y + dy, x + dx]: out[y, x] = True; break
    a[out & ~cloth] = (0, 0, 0, 255)
    a[~out & ~cloth] = (0, 0, 0, 0)
    return a, int(fill.sum())

def run(d):
    d = Path(d); anim = json.loads((d / 'animation.json').read_text()); n = 0
    for s in SHEETS:
        f = anim['layers'].get(s)
        if not f: continue
        a = np.array(Image.open(d / f).convert('RGBA'))
        if 'body' in anim['layers']:
            n += seat_clamp(a, np.array(Image.open(d / anim['layers']['body']).convert('RGBA')), anim['sheetLayout']['rows'])
        b, k = close(a); n += k
        Image.fromarray(b).save(d / f)
    return n

if __name__ == '__main__':
    for d in sys.argv[1:]: print(d, run(d))
