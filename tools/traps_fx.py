"""Trap landing effects (Christopher 2026-10-19): one sheet per trap, played by the testbed at the target cell after the
item lands. Each frame has two layers: ground (decals under fighters: pit, caltrops, scorch) and air (blast, flash, smoke
over fighters). Pixel art drawn from primitives (palette keys, black outline), no generated pixels.
Writes production/source/fx/traps/<trap>-ground.png, <trap>-air.png (frames in one row) and traps.json (frame size,
anchor = the cell centre on the ground, fps, burst frames, linger loop for traps that stay on the field).
Also exports cloud() for the smoke in traps.py.  Run: python3 traps_fx.py"""
import json, math, os, random
from PIL import Image
R = '/home/claude/astro-fighters-playtest/'
OUT = R + 'production/source/fx/traps/'
PAL = {'#': '#000000', 'W': '#ffffff', 'a': '#adadad', 'd': '#5a5a5a', 'g': '#8a8a8a', 'G': '#c4c4c4',
       'p': '#f2e6c4', 'r': '#c8302c', 'y': '#ffe97a', 'Y': '#fff6c8', 'o': '#ff9a2e', 'O': '#e0561b',
       'b': '#6b4a2b', 'k': '#3a2a1a', 'K': '#241a10'}
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def outline(px, keep=()):
    """black outline round a set of pixels {(x,y): key}"""
    o = dict(px)
    for (x, y) in px:
        for dx, dy in N4:
            if (x + dx, y + dy) not in px: o[(x + dx, y + dy)] = '#'
    for q in keep: o[q] = px[q]
    return o

def cloud(w, h, seed, tones=('W', 'G', 'g'), puffs=None):
    """billowing smoke: overlapping round puffs (lower ones in front). Lit from the upper left on the whole silhouette
    (highlight where the upper-left is open air, shadow underneath and on the lower right), a shadow rim along the lower
    edge of each front puff where it overlaps the puffs behind, black outline round the whole. Returns pattern rows."""
    rnd = random.Random(seed); cs = []
    m = min(w, h); n = puffs or max(5, (w * h) // 90)
    for i in range(n):
        r = rnd.randint(max(2, m // 6), max(3, int(m / 3)))
        cs.append((rnd.randint(r, max(r, w - 1 - r)), rnd.randint(min(r, h - 1 - r), h - 1 - r), r))
    cs.append((w // 2, h - 1 - m // 3, m // 3))
    cs.sort(key=lambda c: c[1] + c[2])
    hi, mid, lo = tones; U = set(); rim = set(); cap = set()
    for cx, cy, r in cs:
        disk = {(x, y) for y in range(cy - r, cy + r + 1) for x in range(cx - r, cx + r + 1)
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 1 and 0 <= x < w and 0 <= y < h}
        inner = {q for q in disk if (q[0] - cx) ** 2 + (q[1] - cy) ** 2 < (r - 1) ** 2}
        rim -= inner; cap -= inner
        for (x, y) in disk - inner:
            if (x, y) not in U: continue
            if y >= cy + r // 3: rim.add((x, y))                                    # lower edge of a front puff: shadow line
            elif (x - cx) + (y - cy) < -0.8 * r and r >= m / 5: cap.add((x, y))   # its lit upper-left brow
        U |= disk
    px = {}
    for (x, y) in U:
        if (x - 2, y - 2) not in U or (x - 1, y - 3) not in U: t = hi
        elif (x + 1, y + 3) not in U or (x + 3, y + 1) not in U or y > h * 0.78: t = lo
        else: t = mid
        if (x, y) in rim and t != hi: t = lo
        elif (x, y) in cap and t == mid: t = hi
        px[(x, y)] = t
    px = outline(px)
    return [''.join(px.get((x, y), '.') for x in range(-1, w + 1)) for y in range(-1, h + 1)]

def stamp(px, rows, x0, y0, under=False):
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.' and (not under or (x0 + x, y0 + y) not in px): px[(x0 + x, y0 + y)] = ch

def disc(px, cx, cy, r, key, ry=None):
    ry = ry or r
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if ((x - cx) / r) ** 2 + ((y - cy) / ry) ** 2 <= 1: px[(x, y)] = key

def ray(px, x0, y0, ang, l0, l1, key):
    for t in range(l0, l1):
        px[(round(x0 + t * math.cos(ang)), round(y0 + t * math.sin(ang)))] = key

ITEM = {
    'tagStuck':   ['pp.', 'rp.', 'pp#', '.#a', '.#a', '..#'],
    'pellet':     ['.##.', '#Gg#', '#gd#', '.##.'],
    'pelletF':    ['.##.', '#Wy#', '#yy#', '.##.'],
    'stake':      ['.##.', '#dd#', '#da#', '.#a#', '.#a#', '..#.'],
    'caltrop':    ['.#.#.', '#a#a#', '.#a#.', '#a#a#', '.#.#.'],
    'caltropW':   ['.#.#.', '#a#W#', '.#W#.', '#a#a#', '.#.#.'],
    'spark':      ['.y.', 'yWy', '.y.'],
    'spike':      ['..#..', '.#W#.', '.#a#.', '#aad#', '#aad#'],
    'spikeT':     ['..#..', '.#W#.', '.#a#.', '.#a#.', '#aad#', '#aad#', '#aad#'],
}

def sheet(name, W, H, frames, fps, burst, linger=None, note=''):
    """frames: list of (groundpx, airpx) dicts in frame coords; anchor = (W//2, H-8)"""
    os.makedirs(OUT, exist_ok=True)
    for li, lay in enumerate(('ground', 'air')):
        im = Image.new('RGBA', (W * len(frames), H), (0, 0, 0, 0))
        for k, fr in enumerate(frames):
            for (x, y), ch in fr[li].items():
                if 0 <= x < W and 0 <= y < H:
                    c = PAL[ch]; im.putpixel((k * W + x, y), (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255))
        im.save(OUT + f'{name}-{lay}.png')
    return {'frameSize': [W, H], 'frames': len(frames), 'anchor': [W // 2, H - 8], 'fps': fps, 'burst': burst,
            **({'linger': linger} if linger else {}), 'layers': {'ground': f'{name}-ground.png (under fighters)', 'air': f'{name}-air.png (over fighters)'}, 'note': note}

# ---------------- the six traps ----------------
def explosive():
    W, H = 96, 80; ax, ay = W // 2, H - 8; F = []
    tag = lambda g: stamp(g, ITEM['tagStuck'], ax - 1, ay - 5)
    g = {}; tag(g); F.append((g, {}))
    g = {}; tag(g); a = {}; stamp(a, ITEM['spark'], ax - 3, ay - 9); stamp(a, ['.r.', 'ryr', '.r.'], ax + 1, ay - 11); F.append((g, a))
    g = {}; tag(g); a = {}; disc(a, ax, ay - 4, 8, 'W'); a = outline(a); F.append((g, a))
    def ball(r, cy, seed):
        a = {}; rows = cloud(r * 2, r * 2, seed, tones=('Y', 'y', 'o'), puffs=12); stamp(a, rows, ax - r - 1, cy - r - 1)
        for q, ch in list(a.items()):
            if ch == 'o' and (q[0] + q[1]) % 3 == 0: a[q] = 'O'
        return a
    scorch = {}; disc(scorch, ax, ay, 16, 'K', 4); disc(scorch, ax, ay, 10, 'k', 2.5)
    F.append(({}, ball(16, ay - 14, 11)))
    a = ball(22, ay - 20, 12); stamp(a, cloud(14, 10, 13, tones=('G', 'g', 'd')), ax - 30, ay - 14, under=True); stamp(a, cloud(14, 10, 14, tones=('G', 'g', 'd')), ax + 16, ay - 14, under=True)
    F.append((dict(scorch), a))
    a = {}; stamp(a, cloud(44, 34, 15, tones=('G', 'g', 'd')), ax - 22, ay - 44)
    for q, ch in list(a.items()):
        if ch == 'G' and q[1] > ay - 22 and (q[0] * 7 + q[1]) % 5 == 0: a[q] = 'o'
    F.append((dict(scorch), a))
    a = {}; stamp(a, cloud(40, 26, 16, tones=('G', 'g', 'd')), ax - 20, ay - 50); stamp(a, cloud(12, 9, 17, tones=('G', 'g', 'd')), ax - 34, ay - 20); stamp(a, cloud(10, 8, 18, tones=('G', 'g', 'd')), ax + 22, ay - 24)
    F.append((dict(scorch), a))
    a = {}; stamp(a, cloud(18, 12, 19, tones=('G', 'g', 'd')), ax - 16, ay - 58); stamp(a, cloud(12, 9, 20, tones=('G', 'g', 'd')), ax + 6, ay - 62)
    F.append((dict(scorch), a))
    F.append((dict(scorch), {}))
    return sheet('explosiveTag', W, H, F, 12, {'land': 0, 'detonate': 3, 'damage': 3},
                 note='Explosive Tag: kunai with a paper tag sticks in the ground, the tag sizzles, white flash, fireball, smoke rises, scorch mark fades with the last frame. Hit fighters play hitReact on frame 3.')

def flash():
    W, H = 112, 88; ax, ay = W // 2, H - 8; F = []; cy = ay - 20
    g = {}; stamp(g, ITEM['pelletF'], ax - 2, ay - 4); F.append((g, {}))
    a = {}; disc(a, ax, cy, 4, 'W'); stamp(a, ['y'], ax, cy); a = outline(a); F.append(({}, a))
    for r, L, n in ((10, 34, 8), (16, 44, 16)):
        a = {}
        for i in range(n):
            ang = i * 2 * math.pi / n; l = L if i % 2 == 0 else L * 2 // 3
            ray(a, ax, cy, ang, r, l, 'y'); ray(a, ax + 0.6 * math.sin(ang), cy - 0.6 * math.cos(ang), ang, r, l - 6, 'Y')
        disc(a, ax, cy, r + 3, 'Y'); disc(a, ax, cy, r, 'W'); F.append(({}, a))
    a = {}
    for i in range(16):
        ang = i * 2 * math.pi / 16 + 0.1; ray(a, ax, cy, ang, 30, 40, 'Y')
    disc(a, ax, cy, 8, 'Y'); disc(a, ax, cy, 5, 'W'); F.append(({}, a))
    rnd = random.Random(3)
    for n in (8, 4):
        a = {}
        for i in range(n):
            ang = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(14, 40)
            stamp(a, ITEM['spark'], round(ax + d * math.cos(ang)) - 1, round(cy + d * math.sin(ang) * 0.7) - 1)
        F.append(({}, a))
    return sheet('flashBomb', W, H, F, 12, {'land': 0, 'flash': 2, 'blind': 2},
                 note='Flash Bomb: pellet lands, a white star flash with yellow rays fills the area and fades to sparkles. Blinded fighters play hitReact (squint) on frame 2; the testbed may also white out the screen for one frame.')

def smoke():
    W, H = 144, 88; ax, ay = W // 2, H - 8; F = []
    g = {}; stamp(g, ITEM['pellet'], ax - 2, ay - 4); F.append((g, {}))
    for w, h, s in ((16, 10, 31), (44, 26, 32), (90, 46, 33), (132, 64, 34)):
        a = {}; stamp(a, cloud(w, h, s), ax - w // 2, ay - h + 4); F.append(({}, a))
    burst = len(F)
    for s in range(4):          # linger loop: the bank breathes, wisps drift off the top
        a = {}; stamp(a, cloud(132, 64, 34), ax - 66 + (1 if s in (1, 2) else 0), ay - 60 - (1 if s == 2 else 0))
        stamp(a, cloud(14, 9, 40 + s), ax - 52 + s * 6, ay - 70 - s, under=True); stamp(a, cloud(12, 8, 50 + s), ax + 30 - s * 4, ay - 68 - s, under=True)
        F.append(({}, a))
    for w, h, s in ((110, 46, 35), (60, 24, 36)):    # dispersal when the 2 rounds are up
        a = {}; stamp(a, cloud(w, h, s), ax - w // 2, ay - h + 2)
        for q in list(a):
            if (q[0] + q[1]) % 3 == 0 and a[q] != '#': del a[q]
        F.append(({}, a))
    return sheet('smokeScreen', W, H, F, 10, {'land': 0, 'smoke': 4}, linger={'frames': list(range(burst, burst + 4)), 'loop': True, 'fps': 6, 'rounds': 2, 'then': [burst + 4, burst + 5]},
                 note='Smoke Screen (radius 2): pellet lands, smoke billows out into a bank that covers the area; loop the linger frames while the Smoke terrain lasts (2 rounds), then play the two dispersal frames.')

def smokebomb():
    # Smoke Bomb / Smoke Escape (radius 1 round the thrower, 2 rounds; ruling 2026-10-19): the smokeDrop clip is the burst,
    # this sheet is the bank it leaves: a linger loop over the 7 cells, then the dispersal
    W, H = 112, 80; ax, ay = W // 2, H - 8; F = []
    for s in range(4):
        a = {}; stamp(a, cloud(100, 56, 61), ax - 50 + (1 if s in (1, 2) else 0), ay - 52 - (1 if s == 2 else 0))
        stamp(a, cloud(12, 8, 62 + s), ax - 40 + s * 5, ay - 62 - s, under=True); stamp(a, cloud(10, 7, 70 + s), ax + 24 - s * 4, ay - 60 - s, under=True)
        F.append(({}, a))
    for w, h, s in ((80, 36, 66), (44, 20, 67)):
        a = {}; stamp(a, cloud(w, h, s), ax - w // 2, ay - h + 2)
        for q in list(a):
            if (q[0] + q[1]) % 3 == 0 and a[q] != '#': del a[q]
        F.append(({}, a))
    return sheet('smokeBomb', W, H, F, 10, {}, linger={'frames': [0, 1, 2, 3], 'loop': True, 'fps': 6, 'rounds': 2, 'then': [4, 5]},
                 note='Smoke Bomb / Smoke Escape (radius 1 round the user): starts when the smokeDrop clip ends; loop the linger frames while the Smoke terrain lasts (2 rounds), then the two dispersal frames. Everyone inside is hidden.')

CAL_AT = [(-26, -2), (-14, 3), (-4, -5), (7, 2), (18, -3), (28, 1), (-18, -9), (12, -10), (0, 5)]
def caltrops():
    W, H = 96, 40; ax, ay = W // 2, H - 8; F = []
    for k, hop in enumerate((3, 1, 0)):
        g = {}
        for i, (dx, dy) in enumerate(CAL_AT):
            h = hop if i % 2 == k % 2 else 0
            stamp(g, ITEM['caltrop'], ax + dx - 2, ay + dy - 2 - h)
        F.append((g, {}))
    burst = len(F)
    for s in range(2):
        g = {}
        for i, (dx, dy) in enumerate(CAL_AT):
            stamp(g, ITEM['caltropW' if (i + s) % 3 == 0 else 'caltrop'], ax + dx - 2, ay + dy - 2)
        F.append((g, {}))
    return sheet('caltrops', W, H, F, 12, {'land': 0}, linger={'frames': [burst, burst + 1], 'loop': True, 'fps': 3, 'rounds': 3},
                 note='Caltrops / Scatter Nails: the handful lands, bouncing once, and lies across the cell; loop the linger frames (glints) while the hazard lasts (3 rounds). Fighters standing on it play hitReact when it bites.')

def spikepit():
    W, H = 96, 64; ax, ay = W // 2, H - 10; F = []
    g = {}; stamp(g, ITEM['stake'], ax - 2, ay - 5); F.append((g, {}))
    g = {}; stamp(g, ITEM['stake'], ax - 2, ay - 4)
    for ang, l in ((0.1, 14), (2.9, 13), (1.4, 5), (4.6, 4), (0.6, 9), (3.6, 10)):
        ray(g, ax, ay, ang, 3, l, '#')
    F.append((g, {}))
    def pit(g):
        disc(g, ax, ay, 18, 'b', 6); disc(g, ax, ay + 0.5, 16, 'k', 4.5); disc(g, ax, ay + 1, 12, 'K', 3)
        for (x, y) in [(x, y) for (x, y) in g]:
            pass
        return outline(g)
    g = pit({}); a = {}; stamp(a, cloud(16, 9, 61, tones=('p', 'G', 'g')), ax - 26, ay - 10); stamp(a, cloud(14, 8, 62, tones=('p', 'G', 'g')), ax + 12, ay - 9)
    F.append((g, a))
    SP = [(-12, 0, 'spikeT'), (-5, 1, 'spikeT'), (2, 0, 'spikeT'), (9, 1, 'spikeT'), (-9, -2, 'spike'), (5, -2, 'spike')]
    for rise in (6, 0):         # erupt overshoot then settle
        g = pit({}); a = {}
        for dx, dy, p in sorted(SP, key=lambda s: s[1]):
            rows = ITEM[p]; stamp(a, rows, ax + dx - 2, ay + dy - len(rows) - rise + 1)
        F.append((g, a))
    burst = len(F)
    for s in range(2):
        g = pit({}); a = {}
        for i, (dx, dy, p) in enumerate(sorted(SP, key=lambda s: s[1])):
            rows = [r.replace('W', 'a') if (i + s) % 2 else r for r in ITEM[p]]
            stamp(a, rows, ax + dx - 2, ay + dy - len(rows) + 1)
        F.append((g, a))
    return sheet('spikePit', W, H, F, 12, {'land': 0, 'open': 2, 'damage': 3}, linger={'frames': [burst, burst + 1], 'loop': True, 'fps': 3, 'rounds': 3},
                 note='Spike Pit: an iron stake drives into the ground, cracks run out, the ground drops into a pit and spikes spring up (overshoot, settle). Loop the linger frames (glints) for the 3 rounds; spikes are an air layer so they stand in front of a fighter in the pit.')

if __name__ == '__main__':
    meta = {'rule': 'trap landing sheets; play at the target cell when the thrown item arrives; ground layer under fighters, air layer over; anchor = cell centre on the ground (scale with the testbed hex size)',
            'status': 'approved by user 2026-10-19 (Christopher: approve and wire in the trap animations); lingering traps last their ability duration',
            'explosiveTag': explosive(), 'flashBomb': flash(), 'smokeScreen': smoke(), 'smokeBomb': smokebomb(), 'caltrops': caltrops(), 'spikePit': spikepit(),
            'abilities': {'Explosive Tag': 'explosiveTag', 'Flash Bomb': 'flashBomb', 'Smoke Screen': 'smokeScreen', 'Spike Pit': 'spikePit', 'Caltrops': 'caltrops', 'Scatter Nails': 'caltrops', 'Smoke Bomb': 'smokeBomb', 'Smoke Escape': 'smokeBomb'},
            'inFlight': {'rule': 'item drawn along the flight from the thrower release event to the cell: arc height 0.35 x distance for pellets and the stake, 0.15 for the tag kunai (spins nose-first), caltrops fan into 4 singles', 'patterns': {k: ITEM[k] for k in ('pellet', 'pelletF', 'stake', 'caltrop')}, 'palette': PAL}}
    json.dump(meta, open(OUT + 'traps.json', 'w'), indent=1); print('ok')
