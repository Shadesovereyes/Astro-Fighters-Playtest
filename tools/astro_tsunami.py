"""Tsunami v2 zone preview (Christopher 2026-11-03: more dramatic, it is an ultimate): a wide scene on a faint hex underlay
(testbed hexStep 34), the caster on hex 0 facing E, targets on hexes 2 and 3 facing W. From the active frame the giant wave
NPAT wTsunamiBig (spec extra.zone) rolls from just behind the caster across the AoE over crossMs (10 fps frames), rising from
60% to full height in the first quarter, foam streaming off the lip; each target plays tsunamiStruck when the front reaches
it; at the far edge the wave crashes and a flood sheet drains over floodMs.
usage: astro_tsunami.py anim out [radius]"""
import json, sys, os, math
from PIL import Image, ImageDraw
sys.path.insert(0, os.environ.get('ASTRO_TOOLS', '/home/claude/astro-fighters-playtest/tools'))
import astro
anim, out = sys.argv[1:3]; radius = int(sys.argv[3]) if len(sys.argv) > 3 else 3
LAY = ['far-arm', 'body', 'skin-fx', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'arms-fx', 'fx']
HS = 34; HW = HS * math.sqrt(3); W = int(HW * (radius + 2.5)) + 40; H = 150; FEET = H - 12; X0 = 40
def spec(s): return json.load(open(os.path.join(anim, s + '.json')))
def cell(state, k, d, x, img, lay=LAY):
    s = spec(state); row = s['directions'].index(d); k = max(0, min(k, s['frames'] - 1))
    for l in lay:
        p = os.path.join(anim, state, l + '.png')
        if os.path.exists(p): img.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (int(x) - 32, FEET - 63))
def hexc(c, a=255): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
ALPHA = {'W': 235, 'I': 225, 'a': 215, 'A': 205, 'n': 195}
def stamp(img, pat, x0, y0, alpha=ALPHA, fade=1.0):
    lay = Image.new('RGBA', img.size); px = lay.load()
    for yy, row in enumerate(pat):
        for xx, ch in enumerate(row):
            X, Y = int(x0 + xx), int(y0 + yy)
            if ch != '.' and 0 <= X < img.size[0] and 0 <= Y < img.size[1]: px[X, Y] = hexc(astro.NPAL[ch], int(alpha.get(ch, 220) * fade))
    img.alpha_composite(lay)
sa = spec('tsunami'); z = sa['zone']; act = z['startFrame']; na = sa['frames']; rm = sa['rootMotion']['E']
cross = round(z['crossMs'] / 100); flood = round(z['floodMs'] / 100)
tx = [X0 + HW * 2, X0 + HW * 3]; edge = X0 + HW * (radius + 0.5)
big = astro.NPAT['wTsunamiBig']; bw = len(big[0])
def front(t): return X0 - 20 + (edge - (X0 - 20)) * (t - act) / cross
hitT = [next(t for t in range(act, act + cross + 1) if front(t) >= x - 10) for x in tx]
nb = spec('tsunamiStruck')['frames']; n = max(na, max(hitT) + nb, act + cross + 3 + flood) + 2
frames = []
for t in range(n):
    c = Image.new('RGBA', (W, H), (0xc8, 0xcd, 0xd7, 255)); d = ImageDraw.Draw(c)
    for q in range(0, radius + 2):
        cx = X0 + HW * q; col = (0x8a, 0xb8, 0xe0, 110) if q <= radius else (0xa8, 0xae, 0xbb, 80)
        d.polygon([(cx - HW / 2, FEET), (cx, FEET - 8), (cx + HW / 2, FEET), (cx, FEET + 8)], outline=col)
    ka = min(t, na - 1); xa = X0 + sum(rm[q][0] for q in range(ka + 1))
    if act + cross + 3 <= t < act + cross + 3 + flood:   # the flood sheet draining off the crossed hexes
        f = 1 - (t - act - cross - 3) / flood; d2 = Image.new('RGBA', c.size); dd = ImageDraw.Draw(d2)
        dd.rectangle([X0 - 30, FEET - 3, edge, FEET + 4], fill=(0x2f, 0x7f, 0xe0, int(115 * f)))
        for gx in range(int(X0 - 26), int(edge), 9): dd.point((gx + (t * 3) % 9, FEET - 1), fill=(255, 255, 255, int(220 * f)))
        c.alpha_composite(d2)
    cell('tsunami', ka, 'E', xa, c)
    for x, ht in zip(tx, hitT):
        kb = t - ht
        if kb < 0: cell('hitReact', 0, 'W', x, c, LAY[:-1])
        else: cell('tsunamiStruck', min(kb, nb - 1), 'W', x, c)
    if act <= t <= act + cross:   # the giant wave rolling across the AoE
        u = (t - act) / cross; sc = 0.6 + 0.4 * min(1, u * 4); p = astro._sq(big, sc, sc)
        fx_ = front(t); stamp(c, p, fx_ - len(p[0]) + 8, FEET - len(p) + 1)
        stamp(c, astro.NPAT['wFoamL'], fx_ - 30, FEET - len(p) - 6)
    elif act + cross < t <= act + cross + 3:   # the crash at the far edge
        k = t - act - cross; p = astro._sq(big, 1, 1 - 0.3 * k)
        stamp(c, p, edge - len(p[0]) + 8, FEET - len(p) + 1, fade=1 - 0.25 * k)
        sp = astro.NPAT['wSplashXL']; stamp(c, sp, edge - len(sp[0]) // 2, FEET - len(sp) - 4 * k)
        stamp(c, astro.NPAT['wDropsL'], edge - 30, FEET - 60 + 8 * k)
    frames.append(c.resize((W * 3, H * 3), Image.NEAREST))
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=100, loop=0, disposal=2)
KEY = list(range(act - 2, min(n, act + 16)))
sheet = Image.new('RGBA', (W * 3 * 2 + 16, (H * 3 + 8) * ((len(KEY) + 1) // 2)), 'white')
for i, q in enumerate(KEY): sheet.paste(frames[q], ((i % 2) * (W * 3 + 16), (i // 2) * (H * 3 + 8)))
sheet.save(out + '-E-candidate.png'); print('wrote', out, n, hitT)
