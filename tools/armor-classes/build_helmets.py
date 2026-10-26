"""Author the helmet that matches each armor weight-class outfit (Layer 5, replaces the hair).

Direct pixel authoring on the male head: per frame the head silhouette (Body1 head part) and the
eye rows give the brow line; each helmet is a dome over the head down to the brow, plus guards
(side flaps in front and diagonal views, the back half in profile, the whole back of the head in
back views), outlined 1px black, then patterned in the armor's materials. Eyes are never covered.
Usage: python3 tools/armor-classes/build_helmets.py
"""
import numpy as np
from PIL import Image
from build_armor import (ROOT, P, F, ORDER, BACK, BODY, PARTMAP, part_of, hx, K,
                         MED, HEV, STD, PLT, scale_px, lam_px)

EYES = np.array(Image.open(P / 'Layer 6 - Eyes/Brown Eyes.png').convert('RGBA'))
OUTDIR = P / 'Layer 5 - Hair'

def head_info(f):
    ox = f * F
    head = {(x, y) for y in range(F) for x in range(F) if BODY[y, ox + x, 3] and part_of(PARTMAP, ox + x, y) == 'head'}
    eyes = {(x, y) for y in range(F) for x in range(F) if EYES[y, ox + x, 3]}
    top = min(y for _, y in head)
    brow = (min(y for _, y in eyes) - 1) if eyes else 12
    span = {y: (min(x for x, yy in head if yy == y), max(x for x, yy in head if yy == y)) for y in {y for _, y in head}}
    face_right = None
    if eyes and ORDER[f] in ('E', 'W'):
        ex = sum(x for x, _ in eyes) / len(eyes)
        face_right = ex > (span[brow + 1][0] + span[brow + 1][1]) / 2
    return ox, head, eyes, top, brow, span, face_right

def shape(f, guard_to, guard_w, dome_pad=1):
    """Helmet mask: dome (head rows above the brow, padded) + guards down to guard_to."""
    ox, head, eyes, top, brow, span, face_right = head_info(f)
    d = ORDER[f]
    m = set()
    for y in range(top - 1, brow + 1):
        ref = span.get(max(y, top))
        lo, hi = ref[0] - dome_pad, ref[1] + dome_pad
        if y == top - 1: lo, hi = lo + 2, hi - 2
        elif y == top: lo, hi = lo + 1, hi - 1 if dome_pad else hi
        m |= {(x, y) for x in range(lo, hi + 1)}
    for y in range(brow + 1, guard_to + 1):
        if y not in span: continue
        lo, hi = span[y][0] - dome_pad, span[y][1] + dome_pad
        if d in BACK:
            m |= {(x, y) for x in range(lo, hi + 1)}
        elif d in ('E', 'W'):
            back_w = guard_w + 3
            m |= {(x, y) for x in (range(lo, lo + back_w) if face_right else range(hi - back_w + 1, hi + 1))}
        else:
            m |= {(x, y) for x in range(lo, lo + guard_w)} | {(x, y) for x in range(hi - guard_w + 1, hi + 1)}
    m -= eyes
    return ox, m, top, brow, span, face_right

def outline(m):
    return {(x, y) for (x, y) in m if any((x + dx, y + dy) not in m for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}

def paint(out, ox, m, colour_at):
    edge = outline(m)
    for (x, y) in m:
        out[y, ox + x] = K if (x, y) in edge else colour_at(x, y)

def helmet(kind):
    out = np.zeros((F, F * 8, 4), np.uint8)
    for f, d in enumerate(ORDER):
        back = d in BACK
        if kind == 'scale-coat':
            # iron-rimmed cap of brass scales with scale ear flaps / neck guard
            ox, m, top, brow, span, fr = shape(f, 17, 3)
            paint(out, ox, m, lambda x, y: MED['ld'] if y == brow else scale_px(x, y, top, MED, back))
        elif kind == 'lamellar':
            # kabuto: dark-steel ribbed bowl, verdigris brow band and crest, flared lamellar neck guard
            ox, m, top, brow, span, fr = shape(f, 18, 3)
            # shikoro flare: one more pixel outward on the guard's lower rows
            for y in range(brow + 3, 19):
                xs = [x for x, yy in m if yy == y]
                if xs and not back and d not in ('E', 'W'): m |= {(min(xs) - 1, y), (max(xs) + 1, y)}
                elif xs: m |= {(min(xs) - 1, y), (max(xs) + 1, y)}
            def c(x, y):
                if y == brow: return HEV['th']
                if y > brow: return lam_px(x, y, brow + 1, HEV, back)
                return HEV['pd'] if x % 2 == 0 else (HEV['ph'] if y <= top + 1 else HEV['pm'])
            paint(out, ox, m, c)
            if not back:
                # maedate: small copper crescent crest on the brow (front and diagonals), a stub in profile
                cx = (span[brow][0] + span[brow][1]) // 2 if d not in ('E', 'W') else (span[brow][1] - 2 if fr else span[brow][0] + 2)
                crest = [(cx - 2, top - 3), (cx + 2, top - 3), (cx - 1, top - 2), (cx + 1, top - 2), (cx, top - 1)] if d not in ('E', 'W') \
                    else [(cx + (1 if fr else -1), top - 2), (cx, top - 1)]
                for (x, y) in crest: out[y, ox + x] = HEV['th']
                for (x, y) in crest:
                    for dx, dy in ((1, 0), (-1, 0), (0, -1)):
                        n = (x + dx, y + dy)
                        if n not in crest and out[n[1], ox + n[0], 3] == 0: out[n[1], ox + n[0]] = K
        elif kind == 'molded-leather':
            # leather skull cap: lit upper left, riveted brow band, short ear flaps, 1px nasal in front views
            ox, m, top, brow, span, fr = shape(f, 15, 2)
            def c(x, y):
                if y == brow: return STD['rv'] if x % 3 == 0 else STD['ld']
                if y <= top + 1 and x <= (span[max(y, top)][0] + span[max(y, top)][1]) // 2: return STD['lh']
                return STD['lm']
            paint(out, ox, m, c)
            if d in ('S', 'SE', 'SW'):
                cx = (span[brow][0] + span[brow][1]) // 2
                if (cx, brow + 1) not in head_info(f)[2]:
                    out[brow + 1, ox + cx] = STD['ld']; out[brow + 2, ox + cx] = STD['ld']
        elif kind == 'plate-harness':
            # steel bascinet: ridged dome, cheek plates to the jaw, mail aventail
            ox, m, top, brow, span, fr = shape(f, 18, 3)
            def c(x, y):
                mid = (span[max(min(y, brow), top)][0] + span[max(min(y, brow), top)][1]) // 2
                if y > brow + 4: return PLT['ml'] if (x + y) % 2 else PLT['md']           # aventail
                if y <= brow and not back and d not in ('E', 'W') and x == mid: return PLT['sh']   # ridge
                if y <= top + 2 and x < mid: return PLT['sh']
                return PLT['sm'] if y <= brow else hx('868b96') if y == brow + 1 else PLT['sm']
            paint(out, ox, m, c)
    # W mirrors E exactly (the posed renderer mirrors E for W and checks the reference frames match)
    e, w = ORDER.index('E') * F, ORDER.index('W') * F
    out[:, w:w + F] = out[:, e:e + F][:, ::-1]
    return out

if __name__ == '__main__':
    for kind, name in [('scale-coat', 'Scale Coat Helmet'), ('lamellar', 'Lamellar Kabuto'),
                       ('molded-leather', 'Molded Leather Cap'), ('plate-harness', 'Plate Bascinet')]:
        Image.fromarray(helmet(kind)).save(OUTDIR / f'{name}.png')
        print('wrote', name)
