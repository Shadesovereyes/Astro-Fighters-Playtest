"""Muay Thai shorts and Boxing trunks paperdoll sheets (Layer 2 clothing), candidates 2026-11-15.

The garment is cut from the approved Gi sheet's silhouette (which already covers the hip under the arm in every
direction): the Gi rows from the waistband down to the hem, with the hanging sash removed, recoloured in satin
tones that follow the Gi's own shading. The torso above the waistband stays bare. Every new edge gets a 1px black
outline. Muay Thai shorts are short and flared; Boxing trunks reach just above the knee and add high boots.
Usage: python3 tools/fight-gear/build_shorts.py [outdir]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'Paperdolls/Male'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else P
F = 64
ORDER = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
BACK = {'NE', 'N', 'NW'}

def load(p): return np.array(Image.open(p).convert('RGBA'))
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)
def col(img, x, y): return None if img[y, x, 3] == 0 else '%02x%02x%02x' % tuple(img[y, x, :3])

GI = load(P / 'Layer 2 - Clothing/Male Gi.png')
BODY = load(P / 'Layer 1 - Base Body/Male Base Body1.png')
GIMAP = load(ROOT / 'production/source/characters/rig/male/overlays/male-gi.png')
K = hx('000000')
SASH = {'9c0909'}
OUTL = {'030101', '000000'}
# Gi tone -> tone index 0 (highlight) .. 3 (deep)
GTONE = {'f8eee0': 0, 'fefefc': 0, 'ddcdb4': 1, 'dadad9': 1, 'a9977d': 2, 'adadad': 2, '726250': 3}
LEGPART = {'f58230', 'aa6e28', '808000', '000080'}   # thigh / shin parts on the gi map
PELVIS = 'ffe119'

BMAP = load(ROOT / 'production/source/characters/rig/male/part-map.png')
def leg_gap(ox):
    """Column of the body's gap between the two thighs (first row it appears, rows 39-46)."""
    for y in range(39, 47):
        xs = [x for x in range(F) if col(BMAP, ox + x, y) in ('f58230', '808000', 'aa6e28', '000080')]
        if not xs: continue
        lo, hi = min(xs), max(xs)
        gap = [x for x in range(lo, hi + 1) if BODY[y, ox + x, 3] == 0 or (col(BMAP, ox + x, y) is None)]
        if gap: return gap[len(gap) // 2]
    return None

def build(spec):
    out = np.zeros_like(GI)
    for f, d in enumerate(ORDER):
        ox = f * F
        # 1. garment region: gi pixels from the waist row to the hem row, sash dropped
        reg = {}
        for y in range(spec['waist'], spec['hem'] + 1):
            for x in range(F):
                c = col(GI, ox + x, y)
                if c is None: continue
                part = col(GIMAP, ox + x, y)
                if part == '3cb44b' and y < spec['waist']: continue
                if c in SASH: reg[(x, y)] = None          # filled from neighbours below
                elif c in OUTL: reg[(x, y)] = 'K'
                else: reg[(x, y)] = GTONE.get(c, 1)
        # sash pixels and the sash's own outline inside the garment take the neighbouring tone
        for (x, y), t in list(reg.items()):
            if t is None:
                reg[(x, y)] = 1
        # drop the sash's outline lines that sat inside the trousers: black pixels with garment on both sides in a row
        for (x, y), t in list(reg.items()):
            if t == 'K':
                l, r = reg.get((x - 1, y)), reg.get((x + 1, y))
                u, dn = reg.get((x, y - 1)), reg.get((x, y + 1))
                if l not in (None, 'K') and r not in (None, 'K') and spec['clean'](d, x, y): reg[(x, y)] = 1
        # 2. flare: muay thai legs widen outward on the last rows
        if spec.get('flare'):
            add = {}
            for y in range(spec['hem'] - spec['flare'] + 1, spec['hem'] + 1):
                xs = sorted(x for (x, yy) in reg if yy == y)
                if not xs: continue
                lo, hi = xs[0], xs[-1]
                if d in ('S', 'N', 'SE', 'SW', 'NE', 'NW'):
                    add[(lo - 1, y)] = 'K'; add[(hi + 1, y)] = 'K'
                    reg[(lo, y)] = 2; reg[(hi, y)] = 2
                else:
                    add[(lo - 1, y)] = 'K'; reg[(lo, y)] = 2
            reg.update(add)
        # 3. hem outline row
        hy = spec['hem'] + 1
        xs = [x for (x, y) in reg if y == spec['hem']]
        for x in xs:
            reg[(x, hy)] = 'K'
        # leg split: the body's own gap between the thighs becomes a seam line up to the crotch, and the hem
        # opens there, so the garment reads as two legs, not a skirt
        if d not in ('E', 'W'):
            gx = leg_gap(ox)
            if gx is not None:
                for y in range(spec['crotch'], hy + 1):
                    if (gx, y) in reg: reg[(gx, y)] = 'K'
                for y in range(spec['hem'] - 1, hy + 1):
                    for x in (gx,):
                        if y >= spec['hem']: reg.pop((x, y), None)
                    for x in (gx - 1, gx + 1):
                        if (x, y) in reg and y >= spec['hem']: reg[(x, y)] = 'K'
        # 4. paint
        pal = spec['pal']
        for (x, y), t in reg.items():
            if not (0 <= x < F and 0 <= y < F): continue
            if t == 'K': out[y, ox + x] = K; continue
            band = spec['waist'] <= y < spec['waist'] + spec['band']
            if band:
                tone = pal['band'][min(t, 2)]
                if y == spec['waist']: tone = pal['band'][2] if t != 0 else pal['band'][1]
                out[y, ox + x] = hx(tone)
            else:
                out[y, ox + x] = hx(pal['cloth'][t])
        # 5. top outline of the waistband across the torso
        for x in range(F):
            if reg.get((x, spec['waist'])) not in (None, 'K') and BODY[spec['waist'] - 1, ox + x, 3] and col(BODY, ox + x, spec['waist'] - 1) != '000000':
                pass
        spec.get('extra', lambda *a: None)(out, ox, d, reg)
    return out

def clean_default(d, x, y): return True

# Muay Thai: red satin, gold waistband with dark "lettering" dots
def mt_extra(out, ox, d, reg):
    w = MT['waist'] + 1
    if d in BACK: return
    xs = sorted(x for (x, y) in reg if y == w and reg[(x, y)] != 'K')
    for i, x in enumerate(xs[1:-1]):
        if i % 2 == 0: out[w, ox + x] = hx('7a0f1c')

MT = dict(crotch=38, waist=33, band=3, hem=41, flare=2, clean=clean_default,
          pal=dict(cloth=['ef4a52', 'c81e2c', '8a0f1e', '520812'], band=['ffd75e', 'd9a42e', '8f6516']),
          extra=mt_extra)

def bx_extra(out, ox, d, reg):
    # white side stripe on the outer edge of each trunk leg, rows below the band
    for y in range(BX['waist'] + BX['band'], BX['hem'] + 1):
        xs = sorted(x for (x, yy) in reg if yy == y and reg[(x, yy)] != 'K')
        if not xs: continue
        if d in ('S', 'N'):
            for x in (xs[0], xs[-1]): out[y, ox + x] = hx('ffffff') if d == 'S' else hx('d8d8e0')
        elif d in ('E', 'W'):
            pass
        else:
            x = xs[0] if d in ('SW', 'NE') else xs[-1]
            out[y, ox + x] = hx('e8e8f0')
    # red stripe through the white waistband
    y = BX['waist'] + 1
    for x in range(F):
        if reg.get((x, y)) not in (None, 'K'): out[y, ox + x] = hx('c81e2c')

BX = dict(crotch=39, waist=32, band=3, hem=44, flare=0, clean=clean_default,
          pal=dict(cloth=['5b8ef0', '2f5fcf', '1d3c94', '10225c'], band=['ffffff', 'e3e3e8', 'a8a8b4']),
          extra=bx_extra)

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'Layer 2 - Clothing').mkdir(parents=True, exist_ok=True)
    Image.fromarray(build(MT)).save(OUT / 'Layer 2 - Clothing/Male Muay Thai Shorts.png')
    Image.fromarray(build(BX)).save(OUT / 'Layer 2 - Clothing/Male Boxing Trunks.png')
    print('ok')
