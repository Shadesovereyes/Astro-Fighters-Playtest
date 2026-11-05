"""Stalactite Rain v3 resolution preview (Christopher 2026-11-05 22:11: the ultimate treatment): the cast round, then the
eruption round, at the real AoE size (radius 3 round the aimed hex, testbed hexStep 34, pointy hexes, rows squashed by half).
Round 1: the caster (5 hexes west of the aimed hex, facing E) plays A. Round 2: it plays zone.release (the hurl with no spears rising behind it) and crystal
spears rain out of the sky at a slant from the caster's side onto every hex within the radius, ring by ring from the centre
(extra.rain): each hex tinted crystal teal, each spear streaking down, stabbing in with dust and a glint, standing a beat, then
shattering into rubble. Fighters on hexes 0, 1, 3 east and 2 west (inside) face the caster and play B from the frame the first
spear lands on their hex; one on hex 4 east stays outside in its guard.
usage: astro_rain.py anim A B out"""
import json, sys, os, math, random
from PIL import Image, ImageDraw
sys.path.insert(0, os.environ.get('ASTRO_TOOLS', '/home/claude/astro-fighters-playtest/tools'))
import astro
anim, A, B, out = sys.argv[1:5]
LAY = ['far-arm', 'body', 'skin-fx', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'arms-fx', 'fx']
sa = json.load(open(os.path.join(anim, A + '.json'))); sb = json.load(open(os.path.join(anim, B + '.json'))); Z = sa['rain']
radius = Z['radius']; COL = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in Z['colors']]
HS = 34; HW = HS * math.sqrt(3); CQ = -5
W, H = int(HW * 10.5) + 40, 170; CX = int(HW * 6) + 20; FEET = H - 30
def hxy(q, r): return CX + HW * (q + r / 2), FEET + 0.375 * HS * r
def cell(state, k, d, x, img, y=FEET):
    s = json.load(open(os.path.join(anim, state + '.json'))); row = s['directions'].index(d); k = max(0, min(k, s['frames'] - 1))
    for l in LAY:
        p = os.path.join(anim, state, l + '.png')
        if os.path.exists(p): img.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (round(x) - 32, round(y) - 63))
def pat(name, flip=False, a=255):
    rows = astro.NPAT[name]; im = Image.new('RGBA', (len(rows[0]), len(rows))); px = im.load()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and c in astro.NPAL: px[x, y] = tuple(int(astro.NPAL[c][i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
def stamp(img, name, cx, cy, flip=False, a=255):
    p = pat(name, flip, a); img.alpha_composite(p, (round(cx - p.width / 2), round(cy - p.height / 2)))
ZONE = [(q, r) for q in range(-radius, radius + 1) for r in range(-radius, radius + 1) if max(abs(q), abs(r), abs(q + r)) <= radius]
def dist(q, r): return max(abs(q), abs(r), abs(q + r))
na = sa['frames']; R1 = na; GAP = 4; T2 = R1 + GAP; REL = Z.get('release'); HURL = list(range(json.load(open(os.path.join(anim, REL + '.json')))['frames'])) if REL else [9, 10, 11, 12]; L0 = T2 + 3; RING = 2
rnd = random.Random(11); SPEARS = []
for q, r in ZONE:
    x, y = hxy(q, r); n_ = 1 + (rnd.random() < 0.6)
    for j in range(n_):
        SPEARS.append((x + rnd.uniform(-HS * 0.6, HS * 0.6), y + rnd.uniform(-3, 3), L0 + RING * dist(q, r) + rnd.randrange(2), rnd.random() < 0.35, r))
FALL, STAND, BREAK = 3, 5, 3
def spears(img, t, back):
    for x, y, tl, small, r in SPEARS:
        if (y < FEET - 1) != back: continue
        k = t - (tl - FALL)
        if k < 0 or k >= FALL + STAND + BREAK: continue
        name = 'spearFallS' if small else 'spearFall'; L = len(astro.NPAT[name]); ux, uy = 0.55 / math.hypot(0.55, 1), 1 / math.hypot(0.55, 1)
        if k < FALL:   # streaking down at a slant from the caster's side (upper left)
            f = (k + 1) / FALL; d = (1 - f) * 120
            tx, ty = x - ux * d, y - uy * d; stamp(img, name, tx - ux * L * 0.35, ty - uy * L * 0.5, flip=True)
            for s_ in range(1, 4): stamp(img, 'spearStreak', tx - ux * (L * 0.6 + 9 * s_), ty - uy * (L * 0.9 + 9 * s_), a=200 - 50 * s_)
        elif k < FALL + STAND:   # embedded: the tip driven 5 px into the floor
            stamp(img, name, x - ux * L * 0.32, y - uy * L * 0.45, flip=True)
            if k == FALL: stamp(img, 'dust2', x, y - 3); stamp(img, 'gemSpark', x + 3, y - 10)
            elif k == FALL + 1: stamp(img, 'dust1', x, y - 3)
        else:   # cracks and shatters into rubble
            kb = k - FALL - STAND
            if kb == 0: stamp(img, 'gemBurst2', x - 4, y - 10); stamp(img, 'gemShard2', x - 12, y - 18); stamp(img, 'gemShard2', x + 6, y - 20)
            elif kb == 1: stamp(img, 'gemShard', x - 14, y - 8); stamp(img, 'gemShard', x + 9, y - 10); stamp(img, 'rubble', x, y - 1)
            else: stamp(img, 'rubble', x, y - 1, a=150)
def tint(img, t):
    if t < L0 - 1: return
    fade = 1.0 if t < L0 + RING * radius + FALL + STAND + BREAK else max(0, 1 - (t - (L0 + RING * radius + FALL + STAND + BREAK)) / 5)
    lay = Image.new('RGBA', img.size); d = ImageDraw.Draw(lay)
    for q, r in ZONE:
        if t < L0 - 1 + RING * dist(q, r): continue
        x, y = hxy(q, r); poly = [(x + (HS - 1) * math.cos(math.radians(60 * i - 30)), y + (HS - 1) * 0.5 * math.sin(math.radians(60 * i - 30))) for i in range(6)]
        d.polygon(poly, fill=COL[1] + (int(64 * fade),), outline=COL[3] + (int(170 * fade),))
    img.alpha_composite(lay)
def hexes(img):
    d = ImageDraw.Draw(img)
    for q in range(-7, 6):
        for r in range(-2, 3):
            x, y = hxy(q, r); col = (0x9a, 0xc8, 0xe8, 130) if dist(q, r) <= radius else (0xa8, 0xae, 0xbb, 90)
            d.polygon([(x + HS * math.cos(math.radians(60 * i - 30)), y + HS * 0.5 * math.sin(math.radians(60 * i - 30))) for i in range(6)], outline=col)
GUYS = [(0, 'W'), (1, 'W'), (3, 'W'), (4, 'W'), (-2, 'W')]
nb = sb['frames']; n = L0 + RING * radius + FALL + STAND + BREAK + 10; frames = []
for t in range(n):
    img = Image.new('RGBA', (W, H), (0xc8, 0xcd, 0xd7, 255)); hexes(img); tint(img, t); spears(img, t, True)
    if t < R1: cell(A, t, 'E', hxy(CQ, 0)[0], img)
    elif T2 <= t < T2 + len(HURL): cell(REL or A, HURL[t - T2], 'E', hxy(CQ, 0)[0], img)
    else: cell('guard', 0, 'E', hxy(CQ, 0)[0], img)
    for h, d in GUYS:
        k0 = L0 - FALL + 3 + RING * dist(h, 0) if dist(h, 0) <= radius else None   # the first spear on the hex lands: B's frame 2 (the stab) then
        if k0 is not None and t >= k0 - 2 and t - (k0 - 2) < nb: cell(B, t - (k0 - 2), d, hxy(h, 0)[0], img)
        else: cell('guard', 0, d, hxy(h, 0)[0], img)
    spears(img, t, False)
    big = img.resize((W * 2, H * 2), Image.NEAREST); dr = ImageDraw.Draw(big)
    lab = 'Round 1/2: cast (charge)' if t < T2 else 'Round 2/2: the spears rain down'
    dr.rectangle((8, 8, 8 + 7 * len(lab) + 10, 26), fill=(30, 34, 44)); dr.text((14, 11), lab, fill=(127, 227, 208))
    frames.append(big)
fps = sa.get('fps', 10)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
KEY = [6, 9, T2 + 1, L0 + 1, L0 + 4, L0 + RING * 2 + 3, L0 + RING * 3 + 6, n - 4]
sheet = Image.new('RGBA', (W * 2 * 2 + 16, (H * 2 + 8) * 4), 'white')
for i, k in enumerate(KEY): sheet.paste(frames[min(k, n - 1)], ((i % 2) * (W * 2 + 16), (i // 2) * (H * 2 + 8)))
sheet.save(out + '-E-candidate.png'); print('wrote', out, n, (W, H))
