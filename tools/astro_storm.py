"""Caster-centred storm at its real AoE size (Scorpio Blizzard v3, Christopher 2026-11-04 21:10: caster-centred AoE, radius 3, the fx must show it).
A wide scene on a faint hex underlay (testbed hexStep 34, pointy hexes, rows squashed by half), the caster on the centre hex facing E; fighters on
hexes 1, 2, 3 east and 2 west (inside) face the caster, one on hex 4 east stays outside in its guard. From the zone's 'from' frame the storm races
outward ring by ring (zone.ringFrames), then rages round the caster (calm eye) and fades over the last 4 frames; each fighter inside plays B from the
frame the front reaches its hex (frames 0-3 once, then loopFrom on loop).
usage: astro_storm.py anim A B out"""
import json, sys, os, math, random
from PIL import Image, ImageDraw
anim, A, B, out = sys.argv[1:5]
LAY = ['far-arm', 'body', 'skin-fx', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'arms-fx', 'fx']
sa = json.load(open(os.path.join(anim, A + '.json'))); sb = json.load(open(os.path.join(anim, B + '.json'))); Z = sa['zone']
radius = Z['radius']; RF = {int(k): v for k, v in Z['ringFrames'].items()}; F0 = Z['from']; EYE = Z.get('eye', 20)
COL = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in Z['colors']]
HS = 34; HW = HS * math.sqrt(3); R = (radius + 0.5) * HW
W, H = int(2 * (R + HW)) + 40, 150; CX = W // 2; FEET = H - 26
def cell(state, k, d, x, img):
    s = json.load(open(os.path.join(anim, state + '.json'))); row = s['directions'].index(d); k = min(k, s['frames'] - 1)
    for l in LAY:
        p = os.path.join(anim, state, l + '.png')
        if os.path.exists(p): img.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (round(x) - 32, FEET - 63))
def hexes(img):
    d = ImageDraw.Draw(img)
    for q in range(-5, 6):
        for r in range(-2, 3):
            x = CX + HW * (q + r / 2); y = FEET + 0.75 * HS * r
            dist = max(abs(q), abs(r), abs(q + r)); col = (0x9a, 0xc8, 0xe8, 130) if dist <= radius else (0xa8, 0xae, 0xbb, 90)
            d.polygon([(x + HS * math.cos(math.radians(60 * i - 30)), y + HS * 0.5 * math.sin(math.radians(60 * i - 30))) for i in range(6)], outline=col)
rnd = random.Random(7)
P = [(rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random()), rnd.uniform(2, 50) * rnd.random() ** 0.6, rnd.choice((0, 0, 1, 1, 1, 2, 2, 3)), rnd.uniform(0.7, 1.3)) for _ in range(3600)]
HZ = [(rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random()), rnd.uniform(0, 44)) for _ in range(7000)]
def front_at(t):   # the storm front's radius in px: ring h reached on RF[h] (the outer edge of ring h is (h + 0.5) hex widths out)
    if t < F0: return 0
    pts = [(F0 - 1, EYE)] + [(RF[h], (h + 0.5) * HW) for h in sorted(RF)]
    for (t0, r0), (t1, r1) in zip(pts, pts[1:]):
        if t <= t1: return r0 + (r1 - r0) * (t - t0) / (t1 - t0)
    return R
def storm(img, t, part, fade):
    fr = front_at(t)
    if not fr: return
    lay = Image.new('RGBA', img.size); px = lay.load()
    def put(x, y, c, a):
        x, y = round(x), round(y)
        if 0 <= x < W and 0 <= y < H and px[x, y][3] < a: px[x, y] = c + (int(a * fade),)
    if part == 'back':   # ice-white haze and floor frost over the whole disc
        for a, u, h in HZ:
            d = EYE + u * (fr - EYE); x, y = CX + d * math.cos(a), FEET + 0.5 * d * math.sin(a) - h * (0.3 + 0.7 * min(1, d / 60))
            if (math.sin(a) < 0) == (h > 6): put(x, y, COL[0] if h % 5 < 1 else COL[1], 110 if h > 4 else 160)
    for a0, u, h, ci, sp in P:
        d = EYE + u * (fr - EYE); a = a0 + t * 0.16 * sp * (60 / max(60, d)) * 2   # inner snow whirls faster
        if (math.sin(a) < 0) != (part == 'back'): continue
        x, y = CX + d * math.cos(a), FEET + 0.5 * d * math.sin(a) - h * min(1, d / 50)
        tx, ty = -math.sin(a), 0.5 * math.cos(a)   # tangent: the streak trails behind the flake
        for s_ in range(3):
            put(x - tx * s_ * 1.5, y - ty * s_ * 1.5, COL[min(3, ci + s_)], 235 - 40 * s_)
    if part == 'front' and fr < R:   # the churning white front at the leading edge
        for i in range(int(fr * 14)):
            a = 2 * math.pi * i / int(fr * 14); j = rnd.uniform(-5, 4); h = rnd.uniform(0, 46)
            put(CX + (fr + j) * math.cos(a), FEET + 0.5 * (fr + j) * math.sin(a) - h, COL[0] if rnd.random() < 0.6 else COL[1], 230)
    img.alpha_composite(lay)
na, nb = sa['frames'], sb['frames']; lf = sb.get('loopFrom', 0); HOLD = int(os.environ.get('STORM_HOLD', 24)); n = na + HOLD + 5; frames = []   # v3.1: the storm lingers HOLD frames past the clip (standing in for the zone's rounds), then fades
GUYS = [(1, 'W'), (2, 'W'), (3, 'W'), (4, 'W'), (-2, 'E')]
for t in range(n):
    img = Image.new('RGBA', (W, H), (0xc8, 0xcd, 0xd7, 255)); hexes(img)
    fade = 1.0 if t < na + HOLD else max(0.0, (na + HOLD + 4 - t) / 5)
    storm(img, t, 'back', fade)
    cell(A, min(t, na - 1), 'E', CX, img)
    for h, d in GUYS:
        x = CX + HW * h; k0 = RF.get(abs(h))
        if k0 is not None and t >= k0:
            k = t - k0; k = k if k < nb else lf + (k - lf) % (nb - lf); cell(B, k, d, x, img)
        else: cell('guard', 0, d, x, img)
    storm(img, t, 'front', fade)
    frames.append(img.resize((W * 2, H * 2), Image.NEAREST))
fps = sa.get('fps', 10)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
KEY = [F0 - 1, F0, F0 + 2, na, na + HOLD // 2, na + HOLD + 3]
sheet = Image.new('RGBA', (W * 2 * 2 + 16, (H * 2 + 8) * 3), 'white')
for i, k in enumerate(KEY): sheet.paste(frames[min(k, n - 1)], ((i % 2) * (W * 2 + 16), (i // 2) * (H * 2 + 8)))
sheet.save(out + '-E-candidate.png'); print('wrote', out, n, (W, H), 'R', round(R))
