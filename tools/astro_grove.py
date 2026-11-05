"""Root Sanctuary v6 zone preview (v5 22:50: more roots, fewer trees; v6 23:03: no trees) (Christopher 2026-11-05 22:32: a caster-centred AoE that raises a large root ball / mini forest,
blocking projectiles, fighters inside untargetable from outside): a wide scene on a faint hex underlay (testbed hexStep 34, pointy
hexes, rows squashed by half), the caster on the centre hex facing E, an ally inside on hex 1 west, a foe outside on hex 4 east.
From zone.from the soil spreads and roots burst up ring by ring (zone.ringFrames), climb and arch inward and knot shut into a root
ball on zone.closeFrame (crown flash); saplings and small trees sprout off it from zone.treesFrom; it stands HOLD frames (its
rounds), the foe's chakra bolt breaks on its edge, then it sinks back into the ground.
usage: astro_grove.py anim A out"""
import json, sys, os, math, random
from PIL import Image, ImageDraw
anim, A, out = sys.argv[1:4]
LAY = ['far-arm', 'body', 'skin-fx', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'arms-fx', 'fx']
sa = json.load(open(os.path.join(anim, A + '.json'))); Z = sa['zone']
radius = Z['radius']; RF = {int(k): v for k, v in Z['ringFrames'].items()}; F0 = Z['from']; CF = Z['closeFrame']; TF = Z['treesFrom']
C = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in Z['colors']]
OUTL, BODY, LIT, PALE, TEAL, CRY, WHITE, LEAF, LEAF2 = C
HS = 34; HW = HS * math.sqrt(3); R = (radius + 0.5) * HW; DH = 0.78 * R
W, H = int(2 * (R + HW * 2.2)) + 40, 210; CX = W // 2 - 20; FEET = H - 30
HOLD = int(os.environ.get('GROVE_HOLD', 26)); na = sa['frames']; SINK = 7; n = na + HOLD + SINK + 3
def cell(state, k, d, x, img):
    s = json.load(open(os.path.join(anim, state + '.json'))); row = s['directions'].index(d); k = max(0, min(k, s['frames'] - 1))
    for l in LAY:
        p = os.path.join(anim, state, l + '.png')
        if os.path.exists(p): img.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (round(x) - 32, FEET - 63))
def hxy(q, r): return CX + HW * (q + r / 2), FEET + 0.375 * HS * r
def hexes(img):
    d = ImageDraw.Draw(img)
    for q in range(-6, 7):
        for r in range(-2, 3):
            x, y = hxy(q, r); dist = max(abs(q), abs(r), abs(q + r)); col = (0x9a, 0xc8, 0xe8, 130) if dist <= radius else (0xa8, 0xae, 0xbb, 90)
            d.polygon([(x + HS * math.cos(math.radians(60 * i - 30)), y + HS * 0.5 * math.sin(math.radians(60 * i - 30))) for i in range(6)], outline=col)
rnd = random.Random(5)
NS = 84   # v5 (Christopher 22:50 "more roots less trees"): 84 rim roots (was 46) plus an inner shell of 34, thicker and more varied
STR = [(2 * math.pi * i / NS + rnd.uniform(-0.05, 0.05), rnd.uniform(0.93, 1.04), rnd.uniform(4, 11), rnd.uniform(0, 6), rnd.uniform(0.85, 1.1), (0.45 if i % 2 else -0.45) * rnd.uniform(0.6, 1.1)) for i in range(NS)]
STR += [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.7, 0.86), rnd.uniform(3.5, 7), rnd.uniform(0, 6), rnd.uniform(0.9, 1.08), rnd.uniform(-0.6, 0.6)) for _ in range(34)]
INNER = [(rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random()) * (R - HW * 0.4), rnd.uniform(12, 34), rnd.uniform(2.5, 5)) for _ in range(44)]
BUTT = [(2 * math.pi * i / 22 + rnd.uniform(-0.1, 0.1), rnd.uniform(0.45, 0.9), rnd.uniform(6, 10), rnd.uniform(14, 24)) for i in range(22)]   # buttress roots flaring out over the ground round the foot
CRAWL = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.9, 1.5), rnd.uniform(0, 6)) for _ in range(26)]   # surface roots snaking outward past the rim
TREES = []   # v6 (Christopher 23:03 "no trees for root sanctuary"): roots only
TREES.sort(key=lambda T: (T[1] == 0 and math.sin(T[0]) > 0, -T[1]))   # crown first, then the far foot ring; the near foot ring last (in front)
GLINT = [(rnd.randrange(NS), rnd.uniform(0.15, 0.9), rnd.randrange(6)) for _ in range(22)]
def grow(t):   # how far the rim roots have climbed (1 = knotted at the apex)
    if t < RF[max(RF)]: return 0.0
    return min(1.0, (t - RF[max(RF)] + 1) / (CF - RF[max(RF)] + 1))
def strand_pt(th, sc, s, sway, wob, i, tw=0.0):
    bx, by = CX + R * sc * math.cos(th), FEET + 0.5 * R * sc * math.sin(th)
    ax, ay = CX + sway, FEET - DH
    cx_, cy_ = CX + R * sc * 0.98 * math.cos(th + tw), FEET + 0.49 * R * sc * math.sin(th + tw) - DH * 1.12   # tw twists each root round the ball, so neighbours cross and weave
    x = (1 - s) ** 2 * bx + 2 * (1 - s) * s * cx_ + s * s * ax; y = (1 - s) ** 2 * by + 2 * (1 - s) * s * cy_ + s * s * ay
    return x + math.sin(s * 11 + wob) * 2.2 * (1 - s), y + math.cos(s * 9 + wob) * 1.2
def grove(img, t, part, alpha, hfac):
    lay = Image.new('RGBA', img.size); d = ImageDraw.Draw(lay); f = grow(t); sway = math.sin(t / 4) * 1.5 if t > CF else 0
    def a_(c, a=255): return c + (int(a * alpha),)
    if part == 'back' and t >= F0:   # the soil spreading over the zone, roots crawling over it
        rr = min(R, HW * (0.5 + (t - F0) * 0.75 + 0.5))
        d.ellipse((CX - rr, FEET - rr * 0.5, CX + rr, FEET + rr * 0.5), fill=a_(OUTL, 230)); d.ellipse((CX - rr * 0.94, FEET - rr * 0.45, CX + rr * 0.94, FEET + rr * 0.45), fill=a_(BODY, 220)); d.ellipse((CX - rr * 0.7, FEET - rr * 0.3, CX + rr * 0.7, FEET + rr * 0.3), fill=a_((0x6e, 0x4c, 0x2a), 200))
        if f > 0:   # the root ball's dark inner shell behind the fighters gives it mass
            hh = DH * f * hfac; d.pieslice((CX - R, FEET - hh, CX + R, FEET + hh), 180, 360, fill=a_((0x3a, 0x26, 0x16), int(150 * min(1, f * 1.3))))
        for i, (th, sc, w, wob, _, _t) in enumerate(STR[::2]):
            x0, y0 = CX + rr * 0.95 * math.cos(th), FEET + rr * 0.47 * math.sin(th)
            d.line((CX + rr * 0.3 * math.cos(th + 0.4), FEET + rr * 0.15 * math.sin(th + 0.4), x0, y0), fill=a_(OUTL, 200), width=2)
    for th, rd, L, w in INNER:   # rootlets bursting up out of the inner hexes
        ring = min(radius, int(rd / HW + 0.5))
        if t < RF.get(ring, F0) or part != ('back' if math.sin(th) < 0 else 'front'): continue
        k = min(1, (t - RF.get(ring, F0) + 1) / 2) * hfac; x0, y0 = CX + rd * math.cos(th), FEET + 0.5 * rd * math.sin(th)
        pts = [(x0 + math.sin(u * 5 + th) * 2, y0 - L * k * u) for u in [j / 6 for j in range(7)]]
        d.line(pts, fill=a_(OUTL), width=int(w) + 2); d.line(pts, fill=a_(BODY), width=int(w)); d.line([(x + 1, y) for x, y in pts[:-1]], fill=a_(LIT), width=1)
    if t >= RF[max(RF)]:   # buttress roots flaring out over the ground and roots crawling past the rim
        kk = min(1.0, (t - RF[max(RF)] + 1) / 3) * hfac
        for th, ht, w, out in BUTT:
            if (math.sin(th) > 0) != (part == 'front'): continue
            x0, y0 = CX + R * 0.97 * math.cos(th), FEET + 0.485 * R * math.sin(th) - DH * ht * 0.35 * kk
            x1, y1 = CX + (R + out * kk) * math.cos(th), FEET + 0.5 * (R + out * kk) * math.sin(th)
            pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * (x1 - (x1 - x0) * 0.1) + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * (y1 - 2) + u * u * y1) for u in [j / 8 for j in range(9)]]
            d.line(pts, fill=a_(OUTL), width=int(w) + 2, joint='curve'); d.line(pts, fill=a_(BODY), width=int(w), joint='curve'); d.line([(x, y - 1) for x, y in pts[:-2]], fill=a_(LIT, 210), width=1)
        for th, ln, ph in CRAWL:
            if (math.sin(th) > 0) != (part == 'front'): continue
            pts = []
            for j in range(10):
                u = j / 9; rr2 = R * (0.95 + (ln - 0.95) * u * kk); a2 = th + math.sin(u * 4 + ph) * 0.08
                pts.append((CX + rr2 * math.cos(a2), FEET + 0.5 * rr2 * math.sin(a2)))
            d.line(pts, fill=a_(OUTL, 230), width=4); d.line(pts, fill=a_(BODY, 230), width=2)
    if f > 0:
        for i, (th, sc, w, wob, sp, tw) in enumerate(STR):
            front = math.sin(th) > 0.05
            if front != (part == 'front'): continue
            if front and i % 4 in (1, 2): continue   # gaps in the front wall so the fighters inside stay readable
            m = max(2, int(40 * f * sp)); top = min(1.0, f * sp)
            pts = [strand_pt(th, sc, top * j / m, sway, wob, i, tw) for j in range(m + 1)]
            pts = [(x, FEET - (FEET - y) * hfac) for x, y in pts]
            ww = max(2, int(w * (1.15 - 0.5 * top)))
            d.line(pts, fill=a_(OUTL, 255 if not front else 235), width=ww + 2, joint='curve'); d.line(pts, fill=a_(BODY, 255 if not front else 225), width=ww, joint='curve')
            d.line([(x - 1, y) for x, y in pts], fill=a_(LIT if not front else PALE, 200), width=1)
            for j in range(3, m, 5):   # root hairs fraying off
                x, y = pts[j]; dx = 3 if j % 2 else -3; d.line((x, y, x + dx, y - 2), fill=a_(LIT, 200), width=1)
    if part == 'front' and t >= CF:
        for si, s, ph in GLINT:   # crystal glints in the bark
            if (t + ph) % 6 > 2: continue
            th, sc, w, wob, sp, tw = STR[si]; x, y = strand_pt(th, sc, s, sway, wob, si, tw); y = FEET - (FEET - y) * hfac
            d.point([(x, y)], fill=a_(WHITE)); d.point([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)], fill=a_(CRY))
        for th, s, th_h, cr, t0 in TREES:   # saplings and small trees sprouting off the shell and round its foot
            if t < t0: continue
            g_ = min(1, (t - t0 + 1) / 3) * hfac
            if s > 0: x, y = strand_pt(th, 1.0, s, sway, 0, 0); y = FEET - (FEET - y) * hfac
            else: x, y = CX + (R + 6) * math.cos(th), FEET + 0.5 * (R + 6) * math.sin(th)
            h_ = th_h * g_; d.line((x, y, x, y - h_), fill=a_(OUTL), width=4); d.line((x, y, x, y - h_), fill=a_(BODY), width=2)
            r_ = cr * g_
            for ox, oy, rr_, col in ((0, -h_ - r_ * 0.6, r_, LEAF), (-r_ * 0.6, -h_ - r_ * 0.2, r_ * 0.75, LEAF), (r_ * 0.6, -h_ - r_ * 0.25, r_ * 0.7, LEAF2), (-r_ * 0.15, -h_ - r_ * 0.9, r_ * 0.5, LEAF2)):
                d.ellipse((x + ox - rr_ - 1, y + oy - rr_ - 1, x + ox + rr_ + 1, y + oy + rr_ + 1), fill=a_(OUTL))
            for ox, oy, rr_, col in ((0, -h_ - r_ * 0.6, r_, LEAF), (-r_ * 0.6, -h_ - r_ * 0.2, r_ * 0.75, LEAF), (r_ * 0.6, -h_ - r_ * 0.25, r_ * 0.7, LEAF2), (-r_ * 0.15, -h_ - r_ * 0.9, r_ * 0.5, LEAF2)):
                d.ellipse((x + ox - rr_, y + oy - rr_, x + ox + rr_, y + oy + rr_), fill=a_(col))
            if (t + int(th * 3)) % 5 == 0: d.point([(x - r_ * 0.3, y - h_ - r_)], fill=a_(CRY))
        if CF <= t < CF + 4:   # the crown flash as the canopy knots shut
            k = t - CF; L = [22, 16, 10, 6][k]; ax, ay = CX + sway, FEET - DH * hfac
            for dx, dy in ((1, 0), (0, 1), (0.7, 0.7), (0.7, -0.7)):
                for sgn in (1, -1):
                    ll = L if dx in (0, 1) else L * 0.6
                    d.line((ax, ay, ax + sgn * dx * ll, ay + sgn * dy * ll), fill=a_(WHITE if k < 2 else CRY), width=3 if k == 0 else 2 if k == 1 else 1)
            rr_ = [9, 6, 4, 2][k]; d.ellipse((ax - rr_, ay - rr_, ax + rr_, ay + rr_), fill=a_(WHITE if k < 2 else CRY))
    img.alpha_composite(lay)
PROJ_T = na + 8
frames = []
for t in range(n):
    img = Image.new('RGBA', (W, H), (0xc8, 0xcd, 0xd7, 255)); hexes(img)
    if t < na + HOLD: alpha, hfac = 1.0, 1.0
    else: u = (t - na - HOLD) / SINK; alpha, hfac = max(0.0, 1 - u * 0.9), max(0.0, 1 - u)
    if hfac <= 0: alpha = 0
    grove(img, t, 'back', alpha, max(0.01, hfac))
    cell(A, min(t, na - 1), 'E', CX, img)
    cell('guard', 0, 'E', hxy(-1, 0)[0], img)   # an ally inside
    cell('guard', 0, 'W', hxy(4, 0)[0], img)    # a foe outside: it cannot target anyone inside; its bolt breaks on the roots
    grove(img, t, 'front', alpha, max(0.01, hfac))
    d = ImageDraw.Draw(img); k = t - PROJ_T; ex = CX + R * 0.98
    if 0 <= k < 6 and t < na + HOLD:
        x0 = hxy(4, 0)[0] - 10; x = x0 - (x0 - ex) * min(1, (k + 1) / 4); y = FEET - 34
        if k < 4: d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(255, 255, 255, 255)); d.line((x + 4, y, x + 14, y), fill=(0x9e, 0xd8, 0xff, 200), width=2)
        else:
            for a in range(0, 360, 45): d.line((ex, y, ex + math.cos(math.radians(a)) * (4 + 3 * (k - 4)), y + math.sin(math.radians(a)) * (4 + 3 * (k - 4))), fill=(255, 255, 255, 220) if k == 4 else (0xc7, 0x9a, 0x5b, 200), width=1)
    big = img.resize((W * 2, H * 2), Image.NEAREST); dr = ImageDraw.Draw(big)
    lab = 'cast' if t < na else ('the sanctuary stands (2 rounds): bolts break on it, no one outside can target those inside' if t < na + HOLD else 'the rounds end: it sinks back into the ground')
    dr.rectangle((8, 8, 8 + 6 * len(lab) + 12, 26), fill=(30, 34, 44)); dr.text((14, 11), lab, fill=(0xc7, 0x9a, 0x5b))
    frames.append(big)
fps = sa.get('fps', 10)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
KEY = [5, 7, 9, 10, 13, PROJ_T + 4, na + HOLD + 3, n - 1]
sheet = Image.new('RGBA', (W * 2 * 2 + 16, (H * 2 + 8) * 4), 'white')
for i, k in enumerate(KEY): sheet.paste(frames[min(k, n - 1)], ((i % 2) * (W * 2 + 16), (i // 2) * (H * 2 + 8)))
sheet.save(out + '-E-candidate.png'); print('wrote', out, n, (W, H), 'R', round(R))
