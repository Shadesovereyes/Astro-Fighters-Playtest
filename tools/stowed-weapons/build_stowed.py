"""Author the stowed-weapon paperdoll sheets (Christopher, 2026-10-26: equipped weapons are shown sheathed or
stowed unless their stance is active).

Direct pixel authoring on the male paperdoll, 512x64, frames S SE E NE N NW W SW. Each weapon has two sheets: a
back sheet drawn behind the body and a front sheet drawn over the clothing and under the arms.
  katana: sheathed at the left hip, hilt forward; the saya runs back and down.
  yumi: slung across the back from the right shoulder to the left hip; the string crosses the chest.
  kyoketsu-shoge: the cord coiled at the right hip with the ring hanging; the blade tucked in the belt.
  tanto: sheathed level through the sash at the small of the back, hilt out past the right hip (clear of the katana
  at the left hip and the kyoketsu-shoge blade at the front).
Lit from the east; every piece gets a 1px black outline.
Usage: python3 tools/stowed-weapons/build_stowed.py [outdir]
"""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'Paperdolls/Male/Layer 2b - Stowed Weapons'
F = 64
ORDER = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']

def hx(h): h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

C = {k: hx(v) for k, v in {
    'K': '000000',
    # katana: black lacquer saya, gold tsuba, dark wrap with pale diamonds, red sageo
    'sa0': '1e1a26', 'sa1': '3a3346', 'sa2': '5e5470', 'tsu': 'c9a24a', 'tsuD': '8a6a2a',
    'wr': '2e2218', 'wrL': 'e8dcc0', 'sg': 'b02a2b',
    # yumi: lacquered bamboo, red/white grip, pale string
    'yu0': '4a2a12', 'yu1': '6e4220', 'yu2': '9a6430', 'grp': 'c8302c', 'grpL': 'f2e6c4', 'str': 'e6dcc0', 'strD': '7a6440',
    # kyoketsu-shoge: hemp cord, steel ring and blade
    'cd0': '6e5032', 'cd1': '9a7448', 'cd2': 'c8a070', 'st0': '5a5f6b', 'st1': 'a8aeba', 'st2': 'e4e8ee',
}.items()}

class Sheet:
    def __init__(self): self.a = np.zeros((F, F * 8, 4), np.uint8)
    def px(self, f, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < F and 0 <= y < F: self.a[y, f * F + x] = C[c]
    def get(self, f, x, y):
        return self.a[y, f * F + x]

def thick_line(sh, f, p0, p1, w, ramp, light=(1, -1)):
    """A rod from p0 to p1, w pixels wide; ramp dark->light across the rod by the side facing the light (east/north)."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    if nx * light[0] + ny * light[1] < 0: nx, ny = -nx, -ny
    for y in range(F):
        for x in range(F):
            px, py = x + .5 - x0, y + .5 - y0
            t = px * ux + py * uy
            d = px * nx + py * ny
            if -0.3 <= t <= L + 0.3 and abs(d) <= w / 2:
                k = (d / (w / 2) + 1) / 2 if w > 1.2 else 0.5
                sh.px(f, x, y, ramp[min(len(ramp) - 1, int(k * len(ramp)))])

NO_OUTLINE = ('str', 'strD')   # strings and cords stay 1px, with no outline
def outline(sh):
    a = sh.a; o = a.copy()
    skip = {C[c] for c in NO_OUTLINE}
    for f in range(8):
        for y in range(F):
            for x in range(F):
                X = f * F + x
                if a[y, X, 3]: continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < F and 0 <= ny < F and a[ny, f * F + nx, 3] and tuple(a[ny, f * F + nx]) != C['K'] and tuple(a[ny, f * F + nx]) not in skip:
                        o[y, X] = C['K']; break
    sh.a = o

# ---------- katana ----------
# per facing: tsuba point, hilt end, saya end, which layer the hilt / saya go on
KATANA = {   # lengths match the drawn katana (twoHandGuard: about 33px hilt to tip): saya ~24px, hilt ~7px
    'S':  dict(tsuba=(38, 34), hilt=(34, 29), saya=(51, 48), hilt_on='front', saya_on='back'),
    'SE': dict(tsuba=(38, 34), hilt=(35, 29), saya=(53, 46), hilt_on='front', saya_on='back'),
    'E':  dict(tsuba=(36, 34), hilt=(43, 30), saya=(13, 43), hilt_on='front', saya_on='back'),
    'NE': dict(tsuba=(30, 34), hilt=(35, 30), saya=(12, 47), hilt_on='back', saya_on='front'),
    'N':  dict(tsuba=(28, 34), hilt=(32, 30), saya=(14, 50), hilt_on='back', saya_on='front'),
    'NW': dict(tsuba=(29, 34), hilt=(24, 30), saya=(46, 49), hilt_on='back', saya_on='front'),
    'W':  dict(tsuba=(28, 34), hilt=(21, 30), saya=(51, 43), hilt_on='front', saya_on='front'),
    'SW': dict(tsuba=(36, 34), hilt=(30, 30), saya=(55, 43), hilt_on='front', saya_on='front'),
}
def katana(front, back):
    for f, d in enumerate(ORDER):
        k = KATANA[d]
        sh_s = front if k['saya_on'] == 'front' else back
        sh_h = front if k['hilt_on'] == 'front' else back
        thick_line(sh_s, f, k['tsuba'], k['saya'], 2.2, ['sa0', 'sa1', 'sa2'])
        # kojiri: a lighter cap on the saya end
        sh_s.px(f, *k['saya'], 'sa2')
        # sageo: the red cord wound near the mouth of the saya
        tx, ty = k['tsuba']; sx, sy = k['saya']; L = math.hypot(sx - tx, sy - ty)
        sh_s.px(f, tx + (sx - tx) * 2.5 / L, ty + (sy - ty) * 2.5 / L, 'sg')
        thick_line(sh_h, f, k['tsuba'], k['hilt'], 2.0, ['wr', 'wr', 'wrL'])
        hx_, hy = k['hilt']; L2 = math.hypot(hx_ - tx, hy - ty)
        for t in (1.5, 3.0, 4.5):
            sh_h.px(f, tx + (hx_ - tx) * t / L2, ty + (hy - ty) * t / L2, 'wrL')
        sh_h.px(f, *k['hilt'], 'tsuD')
        # tsuba: a 3px guard across the blade line
        nx, ny = -(hy - ty) / L2, (hx_ - tx) / L2
        for s in (-1, 0, 1):
            sh_h.px(f, tx + nx * s, ty + ny * s, 'tsu' if s >= 0 else 'tsuD')

# ---------- yumi ----------
# per facing: top tip, bottom tip, bulge (how far the bow bows out, signed), bow layer, chest-string segment (front)
YUMI = {
    'S':  dict(top=(21, 8), bot=(44, 52), bulge=-3, on='back', chest=((27, 19), (37, 36))),
    'SE': dict(top=(22, 8), bot=(44, 51), bulge=-3, on='back', chest=((29, 19), (38, 35))),
    'E':  dict(top=(26, 7), bot=(30, 53), bulge=-3, on='back', chest=((36, 20), (36, 33))),
    'NE': dict(top=(40, 8), bot=(22, 51), bulge=3, on='front', chest=None),
    'N':  dict(top=(43, 8), bot=(20, 52), bulge=3, on='front', chest=None),
    'NW': dict(top=(42, 8), bot=(21, 51), bulge=3, on='front', chest=None),
    'W':  dict(top=(37, 7), bot=(33, 53), bulge=3, on='back', chest=((27, 20), (27, 33))),
    'SW': dict(top=(20, 8), bot=(42, 51), bulge=-3, on='back', chest=((26, 19), (35, 35))),
}
def yumi(front, back):
    for f, d in enumerate(ORDER):
        y = YUMI[d]; sh = front if y['on'] == 'front' else back
        (x0, y0), (x1, y1) = y['top'], y['bot']
        L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        pts = []
        for i in range(0, 61):
            t = i / 60
            # asymmetric yumi: the grip sits a third of the way up from the bottom, the curve peaks above it
            b = y['bulge'] * math.sin(math.pi * t) * (1.0 + 0.25 * math.sin(2 * math.pi * t))
            pts.append((x0 + (x1 - x0) * t + nx * b, y0 + (y1 - y0) * t + ny * b))
        # string: the chord, on the inside of the curve
        for i in range(0, 41):
            t = i / 40; sh.px(f, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 'str')
        for i in range(len(pts) - 1):
            thick_line(sh, f, pts[i], pts[i + 1], 1.6, ['yu0', 'yu1', 'yu2'])
        # grip wrap
        for t in (0.62, 0.66, 0.70):
            gx = x0 + (x1 - x0) * t + nx * y['bulge'] * math.sin(math.pi * t) * 1.1
            gy = y0 + (y1 - y0) * t + ny * y['bulge'] * math.sin(math.pi * t) * 1.1
            sh.px(f, gx, gy, 'grp' if t != 0.66 else 'grpL')
        sh.px(f, x0, y0, 'yu2'); sh.px(f, x1, y1, 'yu2')
        if y['chest']:
            (a, b), (c, e) = y['chest']
            n = int(max(abs(c - a), abs(e - b))) + 1
            for i in range(n): front.px(f, a + (c - a) * i / (n - 1), b + (e - b) * i / (n - 1), 'strD')

# ---------- kyoketsu-shoge ----------
# per facing: coil centre (cord loops hanging from the belt), ring below it, blade grip point in the belt, layers
KYO = {
    'S':  dict(coil=(25, 37), on='front', blade=((34, 33), (35, 27)), blade_on='front'),
    'SE': dict(coil=(26, 37), on='front', blade=((35, 33), (36, 27)), blade_on='front'),
    'E':  dict(coil=(32, 37), on='front', blade=((36, 33), (39, 28)), blade_on='front'),
    'NE': dict(coil=(37, 37), on='front', blade=((33, 33), (35, 28)), blade_on='back'),
    'N':  dict(coil=(38, 37), on='front', blade=((29, 33), (28, 27)), blade_on='back'),
    'NW': dict(coil=(37, 37), on='front', blade=((29, 33), (27, 28)), blade_on='back'),
    'W':  dict(coil=(31, 37), on='back', blade=((28, 33), (24, 28)), blade_on='front'),
    'SW': dict(coil=(26, 37), on='front', blade=((33, 33), (32, 27)), blade_on='front'),
}
def kyoketsu(front, back):
    for f, d in enumerate(ORDER):
        k = KYO[d]; sh = front if k['on'] == 'front' else back
        cx, cy = k['coil']
        # a hank of cord: three flat loops stacked down from the belt, lit on the east side
        for j, (oy, rx) in enumerate(((0, 3.4), (2, 3.6), (4, 3.2))):
            for i in range(64):
                a = i / 64 * 2 * math.pi
                x, y = cx + rx * math.cos(a), cy - 2 + oy + 1.3 * math.sin(a)
                sh.px(f, x, y, 'cd2' if math.cos(a) > 0.4 else 'cd1' if math.cos(a) > -0.4 else 'cd0')
        # the iron ring hangs below the coil (a 5x5 ring, lit on the east side)
        RING = ['.aab.', 'a...b', 'a...b', 'a...b', '.aab.']
        for j, line in enumerate(RING):
            for i, ch in enumerate(line):
                if ch != '.': sh.px(f, cx - 1 + i, cy + 4 + j, 'st1' if ch == 'a' else 'st2')
        # blade tucked in the belt: grip in the belt, blade up, the hook a pixel off the spine
        sb = front if k['blade_on'] == 'front' else back
        (bx, by), (tx, ty) = k['blade']
        thick_line(sb, f, (bx, by), (tx, ty), 1.6, ['st0', 'st1', 'st2'])
        sb.px(f, bx, by, 'cd0'); sb.px(f, tx, ty, 'st2')
        sb.px(f, bx + (tx - bx) * 0.5 + (1 if tx >= bx else -1), by + (ty - by) * 0.5, 'st1')

# ---------- tanto ----------
# per facing: hilt end (kashira), mouth of the saya (where the hilt meets it), saya end, layer. Seen from the side the
# level blade runs mostly in depth, so it shows as a short stub out of the back; S/N show its length across the back
TANTO = {
    'S':  dict(hilt=(15, 33), mouth=(20, 34), saya=(31, 35), on='back'),
    'SE': dict(hilt=(17, 33), mouth=(21, 34), saya=(29, 35), on='back'),
    'E':  dict(hilt=(22, 32), mouth=(24, 33), saya=(29, 35), on='back'),
    'NE': dict(hilt=(42, 33), mouth=(38, 34), saya=(28, 35), on='front'),
    'N':  dict(hilt=(47, 33), mouth=(42, 34), saya=(31, 35), on='front'),
    'NW': dict(hilt=(45, 33), mouth=(41, 34), saya=(31, 35), on='front'),
    'W':  dict(hilt=(41, 32), mouth=(39, 33), saya=(34, 35), on='back'),
    'SW': dict(hilt=(20, 33), mouth=(24, 34), saya=(34, 35), on='back'),
}
def tanto(front, back):
    for f, d in enumerate(ORDER):
        t = TANTO[d]; sh = front if t['on'] == 'front' else back
        thick_line(sh, f, t['mouth'], t['saya'], 1.8, ['sa0', 'sa1', 'sa2'])
        sh.px(f, *t['saya'], 'sa2')
        thick_line(sh, f, t['hilt'], t['mouth'], 1.8, ['wr', 'wr', 'wrL'])
        (hx_, hy), (mx, my) = t['hilt'], t['mouth']; L = math.hypot(mx - hx_, my - hy) or 1
        for u in (1.5, 3.0):
            if u < L - 0.5: sh.px(f, hx_ + (mx - hx_) * u / L, hy + (my - hy) * u / L, 'wrL')
        sh.px(f, hx_, hy, 'tsuD'); sh.px(f, mx, my, 'tsu')

WEAPONS = {'katana': katana, 'yumi': yumi, 'kyoketsu-shoge': kyoketsu, 'tanto': tanto}
NAMES = {'katana': 'Katana', 'yumi': 'Yumi', 'kyoketsu-shoge': 'Kyoketsu-Shoge', 'tanto': 'Tanto'}

def build():
    out = {}
    for key, fn in WEAPONS.items():
        front, back = Sheet(), Sheet()
        fn(front, back)
        outline(front); outline(back)
        out[key] = (front.a, back.a)
    return out

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for key, (front, back) in build().items():
        Image.fromarray(front).save(OUT / f'{NAMES[key]} Stowed Front.png')
        Image.fromarray(back).save(OUT / f'{NAMES[key]} Stowed Back.png')
        print('wrote', key)
