"""Author the new hair styles for the male paperdoll (Layer 5, hair slot).

Canon hair pack (Core Systems doc, Request 04): locs tied, locs loose, wrapped headscarf, modern topknot,
braided side; plus afro puff, bantu knots, ronin ponytail and flat-top (Christopher, 2026-10-27: build all).
Direct pixel authoring on the male head: per frame the head silhouette (Body1 head part) and the eye rows
give the brow line. Each style is a stack of parts painted in order; every part gets its own 1px black
outline (inside its mask), so a bun or knot keeps its edge where it overlaps the scalp. Eyes and the face
below the brow are never covered. Hair uses the creator's HAIR_KEY colours (base #3f0505, light #70241d /
#702219, top light #9e4a31) so the hair colour ramp recolours it; cloth and cord use their own colours.
W mirrors E exactly (the posed renderer checks it). Diagonal frames reuse the S/N stamps shifted to the head.
Usage: python3 tools/hair-styles/build_hair.py [outdir]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'armor-classes'))
from build_helmets import head_info, ORDER, F, P   # noqa: E402
from build_armor import BODY   # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else P / 'Layer 5 - Hair'
BACKS = {'N', 'NE', 'NW'}
SIDES = {'E', 'W'}

def hx(h): return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
C = {'#': hx('000000'), 'o': hx('3f0505'), '+': hx('70241d'), '-': hx('702219'), '*': hx('9e4a31'),
     # wrapped headscarf: indigo cloth
     'c': hx('34407a'), 'C': hx('5868a8'), 'd': hx('222a52'),
     # cords / ties: brass-gold
     't': hx('c8963a'), 'T': hx('7a5418')}

class Head:
    def __init__(self, f):
        self.f, self.d = f, ORDER[f]
        self.ox, self.head, self.eyes, self.top, self.brow, self.span, self.fr = head_info(f)
        self.lo, self.hi = self.span[self.brow]
        self.cx = (self.lo + self.hi) // 2
        self.back = self.d in BACKS
        self.side = self.d in SIDES
        self.front = not self.back and not self.side
        # back of the head in profile (E authored facing right; W is mirrored later)
        self.nape = self.lo
        # face: head pixels below the brow, inside the outline, in front and profile views
        self.face = set()
        if not self.back:
            for (x, y) in self.head:
                if y > self.brow and self.span[y][0] < x < self.span[y][1]:
                    if self.front or x > self.lo + 3:
                        self.face.add((x, y))

def ellipse(cx, cy, rx, ry):
    return {(x, y) for y in range(cy - ry, cy + ry + 1) for x in range(cx - rx, cx + rx + 1)
            if ((x - cx) / (rx + .5)) ** 2 + ((y - cy) / (ry + .5)) ** 2 <= 1}

def rect(x0, y0, x1, y1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}

def strand(pts, w):
    """Thick polyline through pts [(x, y), ...], w pixels wide (horizontal), one row per step."""
    m = set()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(y1 - y0), abs(x1 - x0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
            m |= {(x + k - w // 2, y) for k in range(w)}
    return m

def cap(h, pad=1, guard_to=None, guard_w=2, raise_top=1):
    """Hair over the scalp down to the brow, plus side guards (front), back of the head (profile/back)."""
    m = set()
    for y in range(h.top - raise_top, h.brow + 1):
        lo, hi = h.span[max(y, h.top)]
        lo, hi = lo - pad, hi + pad
        if y < h.top: lo, hi = lo + 2, hi - 2
        elif y == h.top and pad: lo, hi = lo + 1, hi - 1
        m |= rect(lo, y, hi, y)
    if guard_to:
        for y in range(h.brow + 1, guard_to + 1):
            if y not in h.span: continue
            lo, hi = h.span[y][0] - pad, h.span[y][1] + pad
            if h.back: m |= rect(lo, y, hi, y)
            elif h.side: m |= rect(lo, y, lo + guard_w + 2, y)
            else: m |= rect(lo, y, lo + guard_w - 1, y) | rect(hi - guard_w + 1, y, hi, y)
    return m

# ---- textures: (x, y, h, part) -> colour key ----------------------------------------------------
def tex_locs(x, y, h, m):
    # vertical ropes: dark seam every third column, a lit stripe beside it, beads of light down each rope
    k = (x - h.cx) % 3
    if k == 0: return 'o' if y % 2 else '#'
    if k == 1: return '+' if (y + x) % 3 else '*'
    return 'o'

def tex_locs_flat(x, y, h, m):
    # ropes lying across the scalp in profile (front-to-back)
    k = (y - h.top) % 3
    if k == 0: return 'o' if x % 2 else '#'
    if k == 1: return '+' if (x + y) % 3 else '*'
    return 'o'

def tex_curl(x, y, h, m):
    n = (x * 7 + y * 13 + (x * y) % 5) % 9
    return '#' if n == 0 else '+' if n in (2, 5) else '*' if n == 7 and y < h.top + 2 else 'o'

def tex_smooth(x, y, h, m):
    # slicked back: long streaks, light on top
    if y <= h.top: return '+' if x % 4 else '*'
    return '+' if (x + 2 * y) % 5 == 0 else 'o'

def tex_cornrow(x, y, h, m):
    k = ((y - h.top) if h.side else (x - h.cx)) % 3
    return '#' if k == 0 else '+' if k == 1 else 'o'

def tex_cloth(x, y, h, m):
    if y == h.brow: return 'd'                      # rolled edge
    if (x + y) % 4 == 0: return 'd'                 # wrap folds
    return 'C' if y <= h.top + 1 else 'c'

def tex_coil(x, y, h, m, centre):
    cx, cy = centre
    if (x, y) == (cx, cy): return '*'
    if (x - cx, y - cy) in ((1, 0), (0, -1)): return '+'
    if (x - cx, y - cy) == (-1, 1): return '#'
    return 'o'

def tex_braid(x, y, h, m):
    # three-strand plait: diagonal lit links
    return '+' if (x + y) % 3 == 0 else '*' if (x - y) % 6 == 0 else 'o'

def tex_tie(x, y, h, m): return 't' if (x + y) % 2 else 'T'

def tex_solid(key): return lambda x, y, h, m: key

# ---- painting -----------------------------------------------------------------------------------
def paint(canvas, h, mask, tex, outline=True, face_ok=False):
    mask = {p for p in mask if 0 <= p[0] < F and 0 <= p[1] < F} - h.eyes
    if not face_ok: mask -= h.face
    edge = {(x, y) for (x, y) in mask if any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    for (x, y) in mask:
        canvas[(x, y)] = '#' if outline and (x, y) in edge else tex(x, y, h, mask)

FADE_BANDS = ['o', 'o', '+', '+', '*']   # dark under the hair, stepping lighter row by row into the skin

def band_fade(canvas, h, start):
    """Faded sides and back: solid colour bands (no dither) stepping from the hair's base to its top light, one
    band per row, so the short hair grades smoothly into the skin. Front views fade only the temples (never the
    forehead or face); profile views fade the back and side of the head, not the face."""
    for (x, y) in h.head:
        k = y - start
        if k < 0 or k >= len(FADE_BANDS) or (x, y) in canvas or (x, y) in h.eyes or (x, y) in h.face: continue
        lo, hi = h.span[y]
        if h.front and lo + 1 < x < hi - 1: continue
        if h.side and x > hi - 4: continue
        canvas[(x, y)] = FADE_BANDS[k]

# ---- styles -------------------------------------------------------------------------------------
def locs_tied(h, cv):
    paint(cv, h, cap(h, 1, h.brow + 3, 2), tex_locs_flat if h.side else tex_locs)
    bx = h.cx - (1 if h.side else 0)
    by = h.top - 4
    # loc ends spilling from the bundle and falling down the back
    if h.side:
        paint(cv, h, strand([(bx - 3, by), (h.nape - 1, by + 4), (h.nape - 2, h.brow + 7)], 3), tex_locs)
    elif h.back:
        paint(cv, h, strand([(h.cx - 2, by + 1), (h.cx - 2, h.brow + 8)], 3) | strand([(h.cx + 2, by + 1), (h.cx + 2, h.brow + 7)], 3), tex_locs)
    else:
        paint(cv, h, strand([(bx - 3, by - 1), (bx - 5, by + 3)], 2) | strand([(bx + 3, by - 1), (bx + 5, by + 3)], 2), tex_locs)
    paint(cv, h, ellipse(bx, by, 3, 3), tex_locs)
    paint(cv, h, rect(bx - 2, h.top - 1, bx + 2, h.top - 1), tex_tie, outline=False)

def rope(cv, h, pts, face=None):
    """One loc: a 2px rope along pts with its own 1px outline (cutting into ropes painted before it), a lit
    left strand, a ridge notch every third row and a tapered 1px tip."""
    body = strand(pts, 2)
    tip = max(y for _, y in body)
    tx = min(x for x, y in body if y == tip)
    body = {(x, y) for (x, y) in body if y < tip} | {(tx, tip)}
    ring = {(x + dx, y + dy) for (x, y) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - body
    face = h.face if face is None else face
    # nothing rises above the scalp line: the crown stays a smooth dome
    keep = lambda p: 0 <= p[0] < F and h.top - 1 <= p[1] < F and p not in h.eyes and p not in face
    for p in ring:
        if keep(p): cv[p] = '#'
    for (x, y) in body:
        if not keep((x, y)): continue
        left = (x - 1, y) not in body
        if y == tip: cv[(x, y)] = 'o'
        elif (y - pts[0][1]) % 3 == 2: cv[(x, y)] = '#' if not left else 'o'     # ridge between twists
        else: cv[(x, y)] = ('*' if (y - pts[0][1]) % 3 == 0 else '+') if left else 'o'

def locs_loose(h, cv):
    """Loose locs fall from the whole crown and fan outward: no tie or gathered point in any facing.
    Ropes are painted back to front, so the outer and rear locs sit behind the ones nearer the viewer."""
    paint(cv, h, cap(h, 1, h.brow + 2, 2), tex_locs)
    b, t, lo, hi, cx = h.brow, h.top, h.lo, h.hi, h.cx
    if h.side:
        ropes = [[(lo + 1, t + 2), (lo - 4, b + 4), (lo - 6, b + 9)],             # rear, splayed out
                 [(lo + 3, t), (lo - 2, b + 3), (lo - 4, b + 11)],
                 [(cx - 1, t), (lo, b + 2), (lo - 2, b + 12)],
                 [(cx + 1, t), (lo + 2, b + 1), (lo + 1, b + 10)],
                 [(hi - 3, t), (lo + 4, b), (lo + 3, b + 11)],
                 # locs falling forward over the cheek (the eye stays clear)
                 [(hi - 4, t), (lo + 6, b + 1), (lo + 5, b + 11)],
                 [(hi - 2, t), (hi - 4, b + 1), (hi - 5, b + 9)],
                 [(cx + 3, t), (hi - 2, t + 1), (hi - 1, b - 1)]]              # short loc over the brow
    elif h.back:
        xs = list(range(lo - 1, hi + 2, 3))
        ends = [b + 8, b + 11, b + 10, b + 12, b + 10, b + 11, b + 9]
        ropes = []
        for i, x in enumerate(xs):
            splay = (x - cx) // 4                                   # hang close to the head, only a slight flare
            ropes.append([(cx + (x - cx) // 2, t), (x, b + 3), (x + splay, ends[i % len(ends)])])
    else:
        ropes = [[(cx - 2, t), (lo - 2, b + 2), (lo - 3, b + 8)],                 # outer locs, behind
                 [(cx + 2, t), (hi + 2, b + 2), (hi + 3, b + 8)],
                 [(cx - 1, t), (lo - 1, b + 1), (lo - 2, b + 11)],
                 [(cx + 1, t), (hi + 1, b + 1), (hi + 2, b + 11)],
                 [(cx - 3, t), (lo, b), (lo, b + 12)],                              # inner locs hug the cheek
                 [(cx + 3, t), (hi, b), (hi, b + 12)],
                 [(cx - 2, t), (cx - 4, b - 1)],                               # short locs over the forehead
                 [(cx + 2, t), (cx + 4, b - 1)],
                 [(cx, t), (cx + 1, b - 1)]]
    # in profile the locs may lie over the cheek and jaw; only the eye and the nose/mouth edge stay uncovered
    face = {(x, y) for (x, y) in h.face if x >= min(ex for ex, _ in h.eyes) - (0 if h.fr else -1)} if h.side and h.eyes else None
    for pts in ropes: rope(cv, h, pts, face)
    if h.front:
        # no gaps (Christopher 2026-10-28): every clear pixel between the outermost locs, on each row they cover, is
        # filled with the locs behind (base colour, a dark seam every third column); the body below is never covered
        rows = {}
        for (x, y) in cv: rows.setdefault(y, []).append(x)
        for y, xs in rows.items():
            if y <= b: continue
            for x in range(min(xs), max(xs) + 1):
                if (x, y) in cv or (x, y) in h.face or (x, y) in h.eyes or BODY[y, h.ox + x, 3]: continue
                cv[(x, y)] = '#' if (x - cx) % 3 == 0 else 'o'

def headscarf(h, cv):
    paint(cv, h, cap(h, 1, h.brow + 4 if h.back else h.brow + 2, 2), tex_cloth)
    if h.side:
        kx, ky = h.nape - 1, h.top + 3
        paint(cv, h, strand([(kx, ky), (kx - 1, ky + 5), (kx - 1, ky + 9)], 2) | strand([(kx + 1, ky), (kx + 1, ky + 7)], 2), tex_cloth)
        paint(cv, h, ellipse(kx, ky, 2, 2), tex_cloth)
    elif h.back:
        kx, ky = h.cx, h.top + 3
        paint(cv, h, strand([(kx - 1, ky), (kx - 3, ky + 10)], 2) | strand([(kx + 1, ky), (kx + 2, ky + 8)], 2), tex_cloth)
        paint(cv, h, ellipse(kx, ky, 2, 2), tex_cloth)
    else:
        # front fold: the wrap crosses over at the forehead
        for i in range(3):
            cv[(h.cx - 1 + i, h.top + i)] = 'd'
            cv[(h.cx + 1 - i, h.top + i)] = 'd' if i != 1 else 'C'

def headband(h, cv):
    """Headband (a Head item drawn OVER the hair, Christopher 2026-10-28): a cloth band round the forehead, 1px out
    from the head, knotted at the back with two tails. P = cloth, Q = its shade (each colour variant swaps them)."""
    r0 = h.top
    band = set()
    for y in range(r0, r0 + 4):
        lo, hi = h.span[max(y, h.top)]
        band |= rect(lo - 1, y, hi + 1, y)
    tex = lambda x, y, hh, m: 'P' if y == r0 + 1 else 'Q'
    tails = lambda x, y, hh, m: 'Q' if (x + y) % 3 == 0 else 'P'
    if h.side:
        kx, ky = h.lo - 1, r0 + 1
        paint(cv, h, strand([(kx - 1, ky + 1), (kx - 4, ky + 5), (kx - 5, ky + 10)], 2) | strand([(kx, ky + 2), (kx - 2, ky + 7), (kx - 2, ky + 12)], 2), tails)
        paint(cv, h, band, tex)
        paint(cv, h, ellipse(kx, ky + 1, 2, 2), tails)
    elif h.back:
        paint(cv, h, band, tex)
        kx, ky = h.cx, r0 + 2
        paint(cv, h, strand([(kx - 1, ky + 1), (kx - 3, ky + 7), (kx - 4, ky + 12)], 2) | strand([(kx + 1, ky + 1), (kx + 2, ky + 6), (kx + 3, ky + 11)], 2), tails)
        paint(cv, h, ellipse(kx, ky, 2, 1), tails)
    else:
        # tails peek out past the head on one side, behind the band
        paint(cv, h, strand([(h.hi + 1, r0 + 3), (h.hi + 3, r0 + 7), (h.hi + 4, r0 + 10)], 2), tails)
        paint(cv, h, band, tex)

HEADBANDS = {'White': {'P': hx('ecebe6'), 'Q': hx('b9bcc8')}, 'Red': {'P': hx('c43a30'), 'Q': hx('7e1c18')},
             'Blue': {'P': hx('3d5bbd'), 'Q': hx('232f72')}}

def topknot(h, cv):
    band_fade(cv, h, h.top + 2)
    top = cap(h, 0, None, raise_top=1)
    top = {(x, y) for (x, y) in top if y <= h.top + (2 if h.back else 1)}
    if h.side: top |= rect(h.lo + 1, h.top + 1, h.lo + 4, h.top + 2)
    kx = h.cx - (1 if h.side else 0)
    paint(cv, h, top, tex_smooth)
    paint(cv, h, ellipse(kx, h.top - 4, 2, 2), tex_smooth)
    paint(cv, h, rect(kx - 1, h.top - 2, kx + 1, h.top - 2), tex_tie, outline=False)

def braided_side(h, cv):
    # cornrows cover the whole scalp down to the nape (never a shaved back)
    paint(cv, h, cap(h, 0, h.brow + 7 if h.back else h.brow + 6 if h.side else h.brow + 1, 3 if h.side else 1, raise_top=0), tex_cornrow)
    if h.side:
        paint(cv, h, strand([(h.nape + 1, h.brow + 2), (h.nape - 1, h.brow + 7), (h.nape - 1, h.brow + 14)], 3), tex_braid)
        paint(cv, h, rect(h.nape - 2, h.brow + 14, h.nape, h.brow + 14), tex_tie, outline=False)
    elif h.back:
        # character's left = viewer's left from behind
        paint(cv, h, strand([(h.lo + 2, h.brow + 1), (h.lo, h.brow + 8), (h.lo - 1, h.brow + 15)], 3), tex_braid)
        paint(cv, h, rect(h.lo - 3, h.brow + 15, h.lo - 1, h.brow + 15), tex_tie, outline=False)
    else:
        # over the character's left shoulder = viewer's right from the front
        paint(cv, h, strand([(h.hi, h.brow + 1), (h.hi + 1, h.brow + 6), (h.hi + 2, h.brow + 15)], 3), tex_braid)
        paint(cv, h, rect(h.hi + 1, h.brow + 15, h.hi + 3, h.brow + 15), tex_tie, outline=False)

def afro_puff(h, cv):
    paint(cv, h, cap(h, 0, h.brow + 1, 1, raise_top=0), tex_curl)
    px = h.cx - (1 if h.side else 0)
    paint(cv, h, ellipse(px, h.top - 4, 5, 3), tex_curl)
    paint(cv, h, rect(px - 2, h.top - 1, px + 2, h.top - 1), tex_tie, outline=False)

BANTU = {'front': [(-4, 1), (0, -1), (4, 1)], 'side': [(-4, 2), (-1, -1), (3, 0), (-5, 6)],
         'back': [(-4, 1), (0, -1), (4, 1), (-3, 5), (3, 5)]}

def bantu(h, cv):
    paint(cv, h, cap(h, 0, h.brow + 1 if not h.front else None, 1, raise_top=0), tex_cornrow if h.side else tex_curl)
    view = 'side' if h.side else 'back' if h.back else 'front'
    for dx, dy in sorted(BANTU[view], key=lambda p: -p[1]):   # lower knots first, crown knot on top
        c = (h.cx + dx, h.top + dy)
        paint(cv, h, ellipse(c[0], c[1], 2, 2), lambda x, y, hh, m, c=c: tex_coil(x, y, hh, m, c))

def tex_swept(target):
    """Slicked-back hair: streaks radiating to the tie point, sheen on the upper-left of the crown."""
    import math
    def t(x, y, h, m):
        tx, ty = target(h)
        a = math.atan2(y - ty, x - tx)
        band = int(a * 9) % 3
        lo, hi = h.span[max(min(y, h.brow), h.top)]
        if y <= h.top + 1 and x <= (lo + hi) // 2 and band != 0: return '*'
        return '#' if band == 0 and y > h.top else '+' if band == 1 else 'o'
    return t

def tail(cv, h, pts, widths):
    """Tapered ponytail: rows along pts with the given widths (one per row), 1px outline outside, a lit left edge,
    a dark strand line down the middle, the tip split in two."""
    body, rows = set(), []
    path = [p for p in sorted(strand(pts, 1), key=lambda q: q[1])]
    seen = {}
    for x, y in path: seen.setdefault(y, x)
    for i, (y, x) in enumerate(sorted(seen.items(), key=lambda q: q[0])):
        w = widths[min(i, len(widths) - 1)]
        xs = [x - (w - 1) // 2 + k for k in range(w)]
        if i == len(seen) - 1 and w >= 2: xs = [xs[0], xs[-1]]        # split tip
        rows.append((y, xs)); body |= {(xx, y) for xx in xs}
    ring = {(x + dx, y + dy) for (x, y) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - body
    ok = lambda p: 0 <= p[0] < F and 0 <= p[1] < F and p not in h.eyes and p not in h.face
    for p in ring:
        if ok(p): cv[p] = '#'
    for i, (y, xs) in enumerate(rows):
        for j, x in enumerate(xs):
            if not ok((x, y)): continue
            mid = len(xs) // 2
            cv[(x, y)] = ('*' if i < 3 else '+') if j == 0 else '#' if (j == mid and len(xs) >= 4 and 1 < i < len(rows) - 2) else 'o'

def ponytail(h, cv):
    b = h.brow
    if h.side:
        tie = (h.nape, b + 3)
        paint(cv, h, cap(h, 1, b + 3, 2), tex_swept(lambda hh: (hh.nape, hh.brow + 3)))
        tail(cv, h, [(h.nape - 1, b + 4), (h.nape - 2, b + 8), (h.nape - 2, b + 13), (h.nape - 1, b + 15)], [4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2])
        paint(cv, h, rect(tie[0] - 1, tie[1] - 1, tie[0] + 1, tie[1]), tex_tie, outline=False)
    elif h.back:
        paint(cv, h, cap(h, 1, b + 4, 2), tex_swept(lambda hh: (hh.cx, hh.brow + 5)))
        tail(cv, h, [(h.cx, b + 6), (h.cx, b + 10), (h.cx + 1, b + 15)], [4, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2])
        paint(cv, h, rect(h.cx - 2, b + 5, h.cx + 1, b + 5), tex_tie, outline=False)
    else:
        paint(cv, h, cap(h, 1, b + 2, 2), tex_swept(lambda hh: (hh.cx, hh.top - 8)))
        # two thin loose wisps at the temples, the left one longer
        for pts in ([(h.lo, b), (h.lo - 1, b + 4), (h.lo, b + 7)], [(h.hi, b), (h.hi + 1, b + 5)]):
            m = strand(pts, 1)
            ring = {(x + dx, y) for (x, y) in m for dx in (-1, 1)} - m
            for p in ring:
                if p not in h.face and p not in h.eyes and p not in cv: cv[p] = '#'
            for p in m:
                if p not in h.face and p not in h.eyes: cv[p] = '+'

def flat_top(h, cv):
    band_fade(cv, h, h.top + 2)
    lo, hi = h.span[h.top + 2]
    block = rect(lo, h.top - 4, hi, h.top + 1)
    if h.side: block |= rect(lo, h.top + 1, lo + 3, h.brow)
    elif h.back: block |= rect(lo, h.top + 1, hi, h.top + 3)
    else: block |= rect(lo, h.top + 1, lo + 1, h.brow) | rect(hi - 1, h.top + 1, hi, h.brow)
    paint(cv, h, block, lambda x, y, hh, m: '*' if y == h.top - 3 and x % 3 else tex_curl(x, y, hh, m))

STYLES = [('locs-tied', 'Locs Tied', locs_tied, True), ('locs-loose', 'Locs Loose', locs_loose, True),
          ('headscarf', 'Wrapped Headscarf', headscarf, True), ('topknot', 'Modern Topknot', topknot, False),
          ('braided-side', 'Braided Side', braided_side, True), ('afro-puff', 'Afro Puff', afro_puff, False),
          ('bantu-knots', 'Bantu Knots', bantu, False), ('ponytail', 'Ronin Ponytail', ponytail, True),
          ('flat-top', 'Flat Top', flat_top, False)]

def build(fn, colours=None):
    out = np.zeros((F, F * 8, 4), np.uint8)
    for f, d in enumerate(ORDER):
        if d == 'W': continue
        h = Head(f)
        cv = {}
        fn(h, cv)
        for (x, y), k in cv.items():
            if 0 <= x < F and 0 <= y < F: out[y, h.ox + x] = (colours or {}).get(k) or C[k]
    e, w = ORDER.index('E') * F, ORDER.index('W') * F
    out[:, w:w + F] = out[:, e:e + F][:, ::-1]
    return out

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, name, fn, _ in STYLES:
        Image.fromarray(build(fn)).save(OUT / f'{name}.png')
        print('wrote', name)
    for colour, pal in HEADBANDS.items():
        Image.fromarray(build(headband, pal)).save(OUT / f'Headband {colour}.png')
        print('wrote Headband', colour)
