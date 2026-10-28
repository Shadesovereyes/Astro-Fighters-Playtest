"""Caster + target scene for a caster-centred storm zone (Sandstorm v2): like astro_duo.py, and from the active frame on a sand
storm turns round the caster across the whole scene (back half behind the fighters, front half over them, part see-through).
usage: astro_zone.py anim A B active loopFrom loops out"""
import json, sys, os, math, random
from PIL import Image, ImageDraw
anim, A, B, act, lf, loops, out = sys.argv[1:8]; act, lf, loops = int(act), int(lf), int(loops)
LAY = ['far-arm', 'body', 'skin-fx', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'arms-fx', 'fx']
CW, GAP = 150, 66
SAND = [(0xe6, 0xc2, 0x7a), (0xc8, 0x9a, 0x52), (0x9c, 0x74, 0x34)]
def cell(state, k, d, x, img):
    s = json.load(open(os.path.join(anim, state + '.json'))); row = s['directions'].index(d)
    for l in LAY:
        p = os.path.join(anim, state, l + '.png')
        if os.path.exists(p): img.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (x, 0))
rnd = random.Random(7)
streaks = [(rnd.random() * 2 * math.pi, rnd.randint(14, 62), rnd.randint(3, 7), rnd.randrange(3), rnd.random() < 0.08) for _ in range(150)]
def storm(t, front, grow):
    lay = Image.new('RGBA', (CW, 64)); px = lay.load(); cx = 36; rx = 30 + 60 * grow
    for a0, y, L, c, shard in streaks:
        a = a0 + t * 0.35 + y * 0.02; ry = 3
        for u in range(L):
            b = a + u * 0.05; f = math.sin(b) > 0
            if f != front: continue
            X = round(cx + rx * math.cos(b)); Y = round(y + ry * math.sin(b))
            if 0 <= X < CW and 0 <= Y < 64:
                col = (0x9e, 0xe6, 0xe0) if shard else SAND[(c + (u == L - 1)) % 3]
                px[X, Y] = col + (150 if front else 200,)
    return lay
sa = json.load(open(os.path.join(anim, A + '.json'))); sb = json.load(open(os.path.join(anim, B + '.json')))
na, nb = sa['frames'], sb['frames']
bseq = list(range(nb)) + list(range(lf, nb)) * loops
n = max(na, act + len(bseq)); frames = []
for t in range(n):
    c = Image.new('RGBA', (CW, 64), (0xc8, 0xcd, 0xd7, 255))
    grow = min(1, (t - act + 1) / 3) if t >= act else 0
    if grow: c.alpha_composite(storm(t, False, grow))
    ka = min(t, na - 1); xa = 4 + sum(sa['rootMotion']['E'][q][0] for q in range(ka + 1))
    cell(A, ka, 'E', xa, c)
    if t < act: cell(A, 0, 'W', 4 + GAP, c)
    else: cell(B, bseq[t - act], 'W', 4 + GAP, c)
    if grow: c.alpha_composite(storm(t, True, grow))
    k = t - act - 6   # a thrown kunai (not an ultimate) flies in from the east and breaks up at the storm's edge
    if 0 <= k < 3:
        d = ImageDraw.Draw(c); x = 146 - k * 7
        d.line([(x, 34), (x + 6, 34)], fill=(0x6a, 0x70, 0x7a)); d.point([(x - 1, 34)], fill=(0xdd, 0xe2, 0xea)); d.point([(x + 7, 33), (x + 7, 35)], fill=(0xa0, 0x30, 0x30))
    elif 3 <= k < 6:
        d = ImageDraw.Draw(c); r = 2 + (k - 3) * 2
        for q in range(14):
            a = q * 2 * math.pi / 14; X = 128 + round(r * math.cos(a)); Y = 34 + round(r * 0.8 * math.sin(a))
            if (q + k) % 3: d.point([(X, Y)], fill=SAND[q % 3])
        if k == 3: d.line([(126, 33), (130, 35)], fill=(0x6a, 0x70, 0x7a))
    frames.append(c.resize((CW * 4, 256), Image.NEAREST))
fps = sa.get('fps', 10)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
pick = list(range(0, n, 2))
sheet = Image.new('RGBA', (CW * 4 * 2 + 16, 264 * ((len(pick) + 1) // 2)), 'white')
for i, k in enumerate(pick): sheet.paste(frames[k], ((i % 2) * (CW * 4 + 16), (i // 2) * 264))
sheet.save(out + '-E-candidate.png'); print('wrote', out, n)
