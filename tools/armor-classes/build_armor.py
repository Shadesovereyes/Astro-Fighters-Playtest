"""Author the Medium (Scale Coat) and Heavy (Lamellar) armor paperdoll sheets.

Direct pixel authoring on the male paperdoll: the stand-in Blue Armor sheet supplies the
registered silhouette (torso, belt, trousers, boots) and its rig part map says which body
part each pixel sits on; this script repaints those regions with each armor's pattern and
adds the extra plates (skirt flare, shoulder plates) with a 1px black outline.
Usage: python3 tools/armor-classes/build_armor.py [outdir]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'Paperdolls/Male'
RIG = ROOT / 'production/source/characters/rig/male'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else P
F = 64
ORDER = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
BACK = {'NE', 'N', 'NW'}

def load(p):
    return np.array(Image.open(p).convert('RGBA'))

def hx(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)

BASE = load(P / 'Layer 2 - Clothing/Male Blue Armor.png')
BASE_SH = load(P / 'Layer 4 - Shoulders and Arms accessories/Blue Armor Shoulders.png')
BODY = load(P / 'Layer 1 - Base Body/Male Base Body1.png')
ARMS = load(P / 'Layer 3 - Arms/Male Arms1.png')
PARTMAP = load(RIG / 'part-map.png')
OVMAP = load(RIG / 'overlays/male-blue-armor.png')
SHMAP = load(RIG / 'overlays/blue-armor-shoulders.png')
PART = {'3cb44b': 'torso', 'ffe119': 'pelvis', 'f58230': 'R-thigh', 'aa6e28': 'R-shin-foot',
        '808000': 'L-thigh', '000080': 'L-shin-foot', 'ffa0c8': 'sash',
        '0082c8': 'R-upper-arm', '46f0f0': 'R-forearm-hand', '911eb4': 'L-upper-arm', 'f032e6': 'L-forearm-hand',
        'e6194b': 'head'}

def part_of(m, x, y):
    if m[y, x, 3] == 0: return None
    return PART.get('%02x%02x%02x' % tuple(m[y, x, :3]))

def col(img, x, y):
    if img[y, x, 3] == 0: return None
    return '%02x%02x%02x' % tuple(img[y, x, :3])

K = hx('000000')
BLUE, DARK, WHITE, GREY = '434da0', '332b6f', 'ffffff', 'adadad'

def outline_new(img, ox, added):
    """Black 1px outline around added pixels, on transparent cells only."""
    for (x, y) in list(added):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < F and 0 <= ny < F and img[ny, ox + nx, 3] == 0:
                img[ny, ox + nx] = K

def frame_info(f):
    ox = f * F
    pix = {}
    for y in range(F):
        for x in range(F):
            c = col(BASE, ox + x, y)
            if c: pix[(x, y)] = (c, part_of(OVMAP, ox + x, y))
    return ox, pix

# ---------------------------------------------------------------- Medium: Scale Coat
MED = dict(
    sh=hx('e2b65a'), sm=hx('b0802e'), sd=hx('6e4618'),          # brass scales: highlight, mid, shadow
    lh=hx('a8703e'), lm=hx('7a4a26'), ld=hx('4a2a14'),          # leather
    ch=hx('7a7f99'), cm=hx('4e526a'), cd=hx('30324a'),          # slate trousers
)

def scale_px(x, y, top, pal, back=False):
    """Brass scales, 3 wide x 2 tall, staggered rows; each scale lit on its upper-left."""
    r = (y - top) // 2
    cx = (x + (r % 2) * 2) % 4
    ry = (y - top) % 2
    if cx == 3: return pal['sd']
    if ry == 0: return pal['sh'] if (cx == 0 and not back) else pal['sm']
    return pal['sm'] if cx == 0 else pal['sd'] if cx == 2 else pal['sm']

LEGS = ('pelvis', 'R-thigh', 'L-thigh', 'R-shin-foot', 'L-shin-foot')

def skirt_colour(c):
    """Skirt pixels use their own colours (blue channel nudged by one) so the rig can split the skirt
    off as the swinging 'sash' part; on screen they are the same colours."""
    c = c.copy(); c[2] ^= 1; return c

def skirt_colours(pal_values):
    return sorted({'%02x%02x%02x' % tuple(skirt_colour(v)[:3]) for v in pal_values})

def build_medium():
    out = np.zeros_like(BASE)
    for f, d in enumerate(ORDER):
        ox, pix = frame_info(f)
        top = min(y for (x, y), (c, p) in pix.items() if p == 'torso')
        skirt_to = 44
        for (x, y), (c, p) in pix.items():
            if c == '000000': out[y, ox + x] = K; continue
            if p == 'torso':
                out[y, ox + x] = scale_px(x, y, top, MED, d in BACK)
            elif p == 'sash':
                out[y, ox + x] = MED['lh'] if c == WHITE else MED['lm'] if c == BLUE else MED['ld']
            elif p in LEGS and y <= skirt_to:
                # coat skirt: scales down to mid-thigh with a dark hem row
                out[y, ox + x] = skirt_colour(MED['sd'] if y == skirt_to else scale_px(x, y, top, MED, d in BACK))
            elif p and 'shin' in p and (c in (BLUE, DARK) or (c == WHITE and y >= 54)):
                out[y, ox + x] = MED['lm'] if c == BLUE else MED['ld'] if c == DARK else MED['lh']
            else:
                out[y, ox + x] = MED['cm'] if c == GREY else MED['ch'] if c == WHITE else MED['cd']
        for (x, y), (c, p) in pix.items():
            if y == skirt_to + 1 and p in LEGS and c != '000000':
                out[y, ox + x] = K
    return out

def build_medium_shoulders():
    out = np.zeros_like(BASE_SH)
    for f in range(8):
        ox = f * F
        for y in range(F):
            for x in range(F):
                c = col(BASE_SH, ox + x, y)
                if not c: continue
                p = part_of(SHMAP, ox + x, y)
                if p and 'upper' in p: continue  # the stand-in shoulder caps give way to the pauldrons below
                if c == '000000': out[y, ox + x] = K
                else: out[y, ox + x] = MED['lh'] if c == WHITE else MED['lm'] if c in (BLUE, GREY) else MED['ld']
        # small scale pauldron capping each shoulder, one pixel clear of the bracer
        bracer = {(x, y) for y in range(F) for x in range(F) if out[y, ox + x, 3]}
        d = ORDER[f]
        added = set()
        for side in ('R-upper-arm', 'L-upper-arm'):
            pts = [(x, y) for y in range(F) for x in range(F) if ARMS[y, ox + x, 3] and part_of(PARTMAP, ox + x, y) == side]
            if not pts: continue
            top = min(y for _, y in pts) - 1
            xs = [x for x, _ in pts]; x0, x1 = min(xs), max(xs)
            if d in ('E', 'W'): x0 -= 1; x1 += 1
            elif (x0 + x1) / 2 < 32: x0 -= 1
            else: x1 += 1
            for y in range(top, top + 5):
                if any((x + dx, y + dy) in bracer for x in range(x0, x1 + 1) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): break
                for x in range(x0, x1 + 1):
                    added.add((x, y)); out[y, ox + x] = scale_px(x, y, top + 1, MED, d in BACK)
        for (x, y) in added:
            if any((x + dx, y + dy) not in added for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y, ox + x] = K
    return out

# ---------------------------------------------------------------- Heavy: Lamellar
HEV = dict(
    ph=hx('a7adbb'), pm=hx('6c7282'), pd=hx('3d4050'),          # dark steel plates
    lc=hx('b02a2a'), ld=hx('6e1414'),                           # crimson lacing
    th=hx('6fb09a'), tm=hx('3e7a66'),                           # verdigris copper trim
    cm=hx('3a3442'), cd=hx('241f2a'), ch=hx('5a5266'),          # under-cloth
    bc=hx('c43a30'), bd=hx('7e1c18'),                           # cord belt (own colours: the rig splits the belt by colour)
)

def lam_px(x, y, top, pal, back=False):
    """Lamellar: 3-row bands = one lacing row + two plate rows; plates 2 wide with dark seams."""
    ry = (y - top) % 3
    if ry == 0: return pal['ld'] if (x % 3 == 1) else pal['lc']
    seam = (x + ((y - top) // 3) % 2) % 3 == 2
    if seam: return pal['pd']
    if ry == 1: return pal['ph'] if not back else pal['pm']
    return pal['pm']

def build_heavy():
    out = np.zeros_like(BASE)
    for f, d in enumerate(ORDER):
        ox, pix = frame_info(f)
        top = min(y for (x, y), (c, p) in pix.items() if p == 'torso')
        knee = 45   # the skirt ends above the shins: shin pixels taken into the swinging skirt leave the frame in deep stances
        skirt = set()
        for (x, y), (c, p) in pix.items():
            if c == '000000': out[y, ox + x] = K; continue
            if p == 'torso':
                # verdigris copper collar on the top rows
                out[y, ox + x] = HEV['th'] if y <= top + 1 else lam_px(x, y, top, HEV, d in BACK)
            elif p == 'sash':
                out[y, ox + x] = HEV['bc'] if c in (BLUE, WHITE) else HEV['bd']
            elif p in LEGS and y <= knee:
                out[y, ox + x] = lam_px(x, y, top, HEV, d in BACK); skirt.add((x, y))
            elif p and 'shin' in p and (c in (BLUE, DARK) or (c == WHITE and y >= 54)):
                out[y, ox + x] = HEV['cd'] if c == DARK else HEV['cm']
            elif p and 'shin' in p:
                # suneate: steel shin splints over the trouser leg
                out[y, ox + x] = HEV['ph'] if x % 2 == 0 else HEV['pm']
            else:
                out[y, ox + x] = HEV['cm'] if c == GREY else HEV['ch'] if c == WHITE else HEV['cd']
        # kusazuri flare: the skirt widens by 1px past the hips on each outer side
        added = set()
        for y in range(37, knee + 1):
            xs = [x for (x, yy) in skirt if yy == y]
            if not xs: continue
            for x, step in ((min(xs), -1), (max(xs), 1)):
                ex = x + step          # current outline pixel
                nx = ex + step         # new outline position
                if (ex, y) in pix and pix[(ex, y)][0] == '000000' and 0 <= nx < F and out[y, ox + nx, 3] == 0:
                    out[y, ox + ex] = lam_px(ex, y, top, HEV, d in BACK); skirt.add((ex, y)); added.add((ex, y))
        outline_new(out, ox, added)
        # hem: dark lacing row at the knee, outline under it
        for (x, y) in list(skirt):
            if y == knee: out[y, ox + x] = HEV['ld']
        for (x, y), (c, p) in pix.items():
            if y == knee + 1 and p in LEGS and c != '000000' and (x, knee) in skirt:
                out[y, ox + x] = K
        for (x, y) in skirt:
            out[y, ox + x] = skirt_colour(out[y, ox + x])
    return out

def build_heavy_shoulders():
    """Sode: wide lamellar plates over each upper arm, plus steel kote on the forearms."""
    out = np.zeros_like(BASE_SH)
    for f, d in enumerate(ORDER):
        ox = f * F
        # forearm guards from the stand-in bracers
        for y in range(F):
            for x in range(F):
                c = col(BASE_SH, ox + x, y)
                if not c: continue
                p = part_of(SHMAP, ox + x, y)
                if p and 'upper' in p: continue
                out[y, ox + x] = K if c == '000000' else HEV['ph'] if c == WHITE else HEV['pm'] if c in (BLUE, GREY) else HEV['pd']
        # sode: a rectangular lamellar plate hanging from each shoulder, kept one pixel clear of the kote
        # so the rig keeps it a separate piece that follows the upper arm
        kote = {(x, y) for y in range(F) for x in range(F) if out[y, ox + x, 3]}
        added = set()
        for side in ('R-upper-arm', 'L-upper-arm'):
            pts = [(x, y) for y in range(F) for x in range(F) if ARMS[y, ox + x, 3] and part_of(PARTMAP, ox + x, y) == side]
            if not pts: continue
            top = min(y for _, y in pts) - 1
            xs = [x for x, _ in pts]
            x0, x1 = min(xs), max(xs)
            outward = -1 if (x0 + x1) / 2 < 32 else 1
            if d in ('E', 'W'):
                x0 -= 1; x1 += 1
            elif outward < 0: x0 -= 2
            else: x1 += 2
            rect = set()
            for y in range(top, top + 9):
                for x in range(x0, x1 + 1):
                    rect.add((x, y))
            clear = {(x, y) for (x, y) in rect if not any((x + dx, y + dy) in kote for dx in (-1, 0, 1) for dy in (-1, 0, 1))}
            # keep only full rows from the top down until the first row that would touch the kote
            rows = []
            for y in range(top, top + 9):
                row = {(x, yy) for (x, yy) in rect if yy == y}
                if row <= clear: rows.append(y)
                else: break
            for y in rows:
                for x in range(x0, x1 + 1):
                    added.add((x, y))
                    first = y == rows[0]
                    out[y, ox + x] = HEV['th'] if first else lam_px(x, y, rows[0] + 1, HEV, d in BACK)
        edge = {(x, y) for (x, y) in added if any((x + dx, y + dy) not in added for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
        for (x, y) in edge: out[y, ox + x] = K
    return out

# ---------------------------------------------------------------- Medium option B: Studded Leather
# From Christopher's reference (2026-10-26): riveted leather cuirass with a shoulder harness, buckled belt,
# side tassets open at the front (full panel at the back), long riveted bracers, dark trousers with a thigh
# strap, strapped knee boots.
STD = dict(
    lh=hx('6e4630'), lm=hx('4e3022'), ld=hx('2f1b12'),          # dark leather
    sh=hx('9a6040'), sd=hx('6a3e26'),                           # harness straps, a step redder and lighter
    bb=hx('7b4b30'), bd=hx('4f2f1d'),                           # belt (own colours: the rig splits the belt by colour)
    rv=hx('c48a58'), st=hx('b8bcc4'),                           # copper rivets, steel buckles
    ch=hx('4c4448'), cm=hx('332d30'), cd=hx('1f1b1d'),          # dark cloth
)

def stud_px(x, y, top, pal, back=False):
    """Riveted leather, used on the tassets: smooth leather, a dark rim row and a rivet line above it."""
    r = (y - top) % 4
    if r == 2 and x % 3 == 0: return pal['rv']
    return pal['lm']

def molded_px(x, y, top, waist, cx, pal, back=False, profile=False):
    """Molded leather cuirass: two lit chest plates (upper left lit), a dark centre seam,
    a shadowed lower belly, and rivets only along the outer edge and the chest line."""
    dx = x - cx
    if not profile and not back and dx == 0: return pal['ld']                       # centre seam
    if y >= waist - 2: return pal['ld'] if y == waist - 1 else pal['lm']            # belly shadow
    if y == top + 5 and not profile and abs(dx) % 3 == 1: return pal['rv']          # chest rivet line
    lit = (y - top) <= 3 and ((-4 <= dx <= -2) or (1 <= dx <= 2)) if not profile else (y - top) <= 3 and dx <= 0
    if back: lit = (y - top) <= 2 and dx <= -1
    return pal['lh'] if lit else pal['lm']

def build_studded():
    out = np.zeros_like(BASE)
    for f, d in enumerate(ORDER):
        ox, pix = frame_info(f)
        torso = [(x, y) for (x, y), (c, p) in pix.items() if p == 'torso' and c != '000000']
        top = min(y for _, y in torso)
        cx = round(sum(x for x, _ in torso) / len(torso))
        back, profile = d in BACK, d in ('E', 'W')
        skirt_to = 41
        waist = max(y for _, y in torso) + 1
        straps = {cx + 1} if profile else {cx - 3, cx + 3}
        for (x, y), (c, p) in pix.items():
            if c == '000000': out[y, ox + x] = K; continue
            if p == 'torso':
                if y <= top: out[y, ox + x] = STD['cd']                       # undershirt collar
                elif x in straps:
                    out[y, ox + x] = STD['st'] if (y == top + 3 and not back) else STD['sh']
                else:
                    edge = any(pix.get((x + ex, y), ('', ''))[0] == '000000' for ex in (-1, 1))
                    out[y, ox + x] = STD['rv'] if (edge and (y - top) % 3 == 1 and y < waist - 2) else molded_px(x, y, top, waist, cx, STD, back, profile)
            elif p == 'sash':
                out[y, ox + x] = STD['bb'] if c in (BLUE, WHITE) else STD['bd']
            elif p in LEGS and y <= skirt_to and (profile or back or abs(x - cx) >= 2):
                # tassets: riveted panels, open over the front of the trousers
                out[y, ox + x] = skirt_colour(STD['ld'] if y == skirt_to else stud_px(x, y, top, STD, back))
            elif p and 'shin' in p and (c in (BLUE, DARK) or (c == WHITE and y >= 54) or y >= 50):
                # knee boots: dark cuff at the top, two lighter straps
                out[y, ox + x] = STD['ld'] if y == 50 or c == DARK else STD['sh'] if y in (52, 56) else STD['lm']
            elif p in LEGS and y == 45:
                out[y, ox + x] = STD['sh']                                    # thigh strap
            else:
                out[y, ox + x] = STD['cm'] if c == GREY else STD['ch'] if c == WHITE else STD['cd']
        for (x, y), (c, p) in pix.items():
            if y == skirt_to + 1 and p in LEGS and c != '000000' and out[skirt_to, ox + x, 3] and tuple(out[skirt_to, ox + x, :3]) == tuple(skirt_colour(STD['ld'])[:3]):
                out[y, ox + x] = K
    return out

def build_studded_shoulders():
    """Two-tier riveted leather pauldrons and long riveted bracers."""
    out = np.zeros_like(BASE_SH)
    for f, d in enumerate(ORDER):
        ox = f * F
        for y in range(F):
            for x in range(F):
                c = col(BASE_SH, ox + x, y)
                if not c: continue
                p = part_of(SHMAP, ox + x, y)
                if p and 'upper' in p: continue
                if c == '000000': out[y, ox + x] = K
                else: out[y, ox + x] = STD['rv'] if (y % 3 == 1 and x % 2 == 0 and c != DARK) else STD['lm'] if c in (BLUE, GREY, WHITE) else STD['ld']
        bracer = {(x, y) for y in range(F) for x in range(F) if out[y, ox + x, 3]}
        added = set()
        for side in ('R-upper-arm', 'L-upper-arm'):
            pts = [(x, y) for y in range(F) for x in range(F) if ARMS[y, ox + x, 3] and part_of(PARTMAP, ox + x, y) == side]
            if not pts: continue
            top = min(y for _, y in pts) - 1
            xs = [x for x, _ in pts]; x0, x1 = min(xs), max(xs)
            if d in ('E', 'W'): x0 -= 1; x1 += 1
            elif (x0 + x1) / 2 < 32: x0 -= 2
            else: x1 += 2
            # molded cap: rounded on the outer top corner and along the lower rim, lit on its upper left
            outer_left = d in ('E', 'W') or (x0 + x1) / 2 < 32
            shape = [(2, 0), (1, 0), (0, 0), (0, 0), (1, 1)]   # (cut on the outer side, cut on the inner side) per row
            if d in ('E', 'W'): shape = [(1, 1), (0, 0), (0, 0), (0, 0), (1, 1)]
            rows = []
            for i, (co, ci) in enumerate(shape):
                y = top + i
                lo, hi = (x0 + co, x1 - ci) if outer_left else (x0 + ci, x1 - co)
                if any((x + dx, y + dy) in bracer for x in range(lo, hi + 1) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): break
                rows.append((y, lo, hi))
            for i, (y, lo, hi) in enumerate(rows):
                for x in range(lo, hi + 1):
                    added.add((x, y))
                    u = (x - lo) / max(1, hi - lo)
                    if i == len(rows) - 2 and len(rows) > 3: c = STD['rv'] if (x - lo) % 3 == 1 else STD['ld']   # rivets on the rim
                    elif i <= 1 and u <= 0.5: c = STD['lh']
                    else: c = STD['lm']
                    out[y, ox + x] = c
        for (x, y) in added:
            if any((x + dx, y + dy) not in added for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y, ox + x] = K
    return out

# ---------------------------------------------------------------- Heavy option B: Plate Harness
# From Christopher's plate reference (2026-10-26): steel breastplate with a centre ridge and a mail collar,
# leather harness and buckled belt, steel tassets either side of a quilted leather apron, plate legs with
# knee rondels, strapped sabatons, big layered round pauldrons, steel vambraces.
PLT = dict(
    sh=hx('a2a7b2'), sm=hx('6a6f7a'), sd=hx('444852'), sx=hx('2c2f36'),   # dark gunmetal steel
    hl=hx('7a4a2e'), hd=hx('4e2e1c'),                                   # leather harness
    bb=hx('7b4b31'), bd=hx('4f2f1e'),                                   # belt (own colours for the rig's belt split)
    ql=hx('5a4030'), qd=hx('3e2a1e'),                                   # quilted apron
    ml=hx('4a4c52'), md=hx('2a2b30'),                                   # mail
)

def plate_px(x, y, top, waist, cx, back=False, profile=False):
    """Breastplate: lit upper left, a bright centre ridge (front), a darker fauld band above the belt."""
    dx = x - cx
    if y >= waist - 2: return PLT['sd'] if y == waist - 1 else PLT['sm']
    if not profile and not back and dx == 0: return PLT['sh']
    if profile: lit = (y - top) <= 4 and dx <= 0
    elif back: lit = (y - top) <= 3 and dx <= -1
    else: lit = (y - top) <= 4 and -4 <= dx <= -1
    if not profile and not back and dx == 1: return PLT['sd']           # shadow side of the ridge
    return PLT['sh'] if lit and (y - top) <= 1 else PLT['sm'] if not lit else hx('868b96')

def tasset_px(y, top):
    return PLT['sd'] if (y - top) % 3 == 2 else PLT['sh'] if (y - top) % 3 == 0 else PLT['sm']

def build_plate():
    out = np.zeros_like(BASE)
    for f, d in enumerate(ORDER):
        ox, pix = frame_info(f)
        torso = [(x, y) for (x, y), (c, p) in pix.items() if p == 'torso' and c != '000000']
        top = min(y for _, y in torso)
        waist = max(y for _, y in torso) + 1
        cx = round(sum(x for x, _ in torso) / len(torso))
        back, profile = d in BACK, d in ('E', 'W')
        skirt_to, knee = 43, 46
        straps = {cx + 1} if profile else {cx - 3, cx + 3}
        skirt = set()
        for (x, y), (c, p) in pix.items():
            if c == '000000': out[y, ox + x] = K; continue
            if p == 'torso':
                if y <= top: out[y, ox + x] = PLT['md'] if x % 2 else PLT['ml']              # mail collar
                elif x in straps and y <= top + 6:
                    out[y, ox + x] = PLT['sh'] if (y == top + 3 and not back) else PLT['hl']
                else: out[y, ox + x] = plate_px(x, y, top, waist, cx, back, profile)
            elif p == 'sash':
                out[y, ox + x] = PLT['bb'] if c in (BLUE, WHITE) else PLT['bd']
            elif p in LEGS and y <= skirt_to:
                if not profile and abs(x - cx) <= 2:
                    # quilted leather apron
                    out[y, ox + x] = PLT['qd'] if (x + y) % 3 == 0 or (x - y) % 3 == 0 else PLT['ql']
                else:
                    out[y, ox + x] = tasset_px(y, waist)
                skirt.add((x, y))
            elif p in LEGS and y <= knee:
                # cuisses and poleyn: knee row lighter, a rondel on the outer knee
                out[y, ox + x] = PLT['sh'] if y == knee else PLT['sm'] if x % 3 else hx('868b96')
            elif p and 'shin' in p and y >= 56:
                out[y, ox + x] = PLT['hl'] if y == 57 else PLT['sd'] if c == DARK else PLT['sm']   # sabatons
            elif p and 'shin' in p:
                out[y, ox + x] = PLT['sh'] if c == WHITE else PLT['sm'] if c == GREY else PLT['sd']  # greaves
            else:
                out[y, ox + x] = PLT['sm'] if c == GREY else PLT['sh'] if c == WHITE else PLT['sd']
        for (x, y), (c, p) in pix.items():
            if y == skirt_to + 1 and p in LEGS and c != '000000' and (x, skirt_to) in skirt:
                out[y, ox + x] = K
        for (x, y) in skirt:
            out[y, ox + x] = skirt_colour(out[y, ox + x])
    return out

def build_plate_shoulders():
    """Large round layered pauldrons (three lames) and steel vambraces."""
    out = np.zeros_like(BASE_SH)
    for f, d in enumerate(ORDER):
        ox = f * F
        for y in range(F):
            for x in range(F):
                c = col(BASE_SH, ox + x, y)
                if not c: continue
                p = part_of(SHMAP, ox + x, y)
                if p and 'upper' in p: continue
                out[y, ox + x] = K if c == '000000' else PLT['sh'] if c == WHITE else PLT['sm'] if c in (BLUE, GREY) else PLT['sd']
        bracer = {(x, y) for y in range(F) for x in range(F) if out[y, ox + x, 3]}
        added = set()
        for side in ('R-upper-arm', 'L-upper-arm'):
            pts = [(x, y) for y in range(F) for x in range(F) if ARMS[y, ox + x, 3] and part_of(PARTMAP, ox + x, y) == side]
            if not pts: continue
            top = min(y for _, y in pts) - 2
            xs = [x for x, _ in pts]; x0, x1 = min(xs), max(xs)
            outer_left = d in ('E', 'W') or (x0 + x1) / 2 < 32
            if d in ('E', 'W'): x0 -= 1; x1 += 1
            elif outer_left: x0 -= 3
            else: x1 += 3
            shape = [(3, 1), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1)]
            if d in ('E', 'W'): shape = [(2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1)]
            rows = []
            for i, (co, ci) in enumerate(shape):
                y = top + i
                lo, hi = (x0 + co, x1 - ci) if outer_left else (x0 + ci, x1 - co)
                if any((x + dx, y + dy) in bracer for x in range(lo, hi + 1) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): break
                rows.append((y, lo, hi))
            for i, (y, lo, hi) in enumerate(rows):
                for x in range(lo, hi + 1):
                    added.add((x, y))
                    u = (x - lo) / max(1, hi - lo)
                    lit = u <= 0.45 if outer_left else u >= 0.55
                    if i in (2, 4): c = PLT['sd']                                  # lame edges
                    elif i == 1 and lit: c = PLT['sh']
                    elif lit and i < 4: c = hx('868b96')
                    else: c = PLT['sm']
                    out[y, ox + x] = c
        for (x, y) in added:
            if any((x + dx, y + dy) not in added for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y, ox + x] = K
    return out

if __name__ == '__main__':
    if '--skirt-colours' in sys.argv:
        print('medium', skirt_colours([MED[k] for k in ('sh', 'sm', 'sd')]))
        print('studded', skirt_colours([STD[k] for k in ('lh', 'lm', 'ld', 'rv')]))
        print('plate', skirt_colours([PLT[k] for k in ('sh', 'sm', 'sd', 'ql', 'qd')]))
        print('heavy', skirt_colours([HEV[k] for k in ('ph', 'pm', 'pd', 'lc', 'ld')]))
        sys.exit()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'Layer 2 - Clothing').mkdir(parents=True, exist_ok=True)
    (OUT / 'Layer 4 - Shoulders and Arms accessories').mkdir(parents=True, exist_ok=True)
    Image.fromarray(build_medium()).save(OUT / 'Layer 2 - Clothing/Male Scale Coat.png')
    Image.fromarray(build_medium_shoulders()).save(OUT / 'Layer 4 - Shoulders and Arms accessories/Scale Coat Shoulders.png')
    Image.fromarray(build_studded()).save(OUT / 'Layer 2 - Clothing/Male Studded Leather.png')
    Image.fromarray(build_studded_shoulders()).save(OUT / 'Layer 4 - Shoulders and Arms accessories/Studded Leather Shoulders.png')
    Image.fromarray(build_plate()).save(OUT / 'Layer 2 - Clothing/Male Plate Harness.png')
    Image.fromarray(build_plate_shoulders()).save(OUT / 'Layer 4 - Shoulders and Arms accessories/Plate Harness Shoulders.png')
    Image.fromarray(build_heavy()).save(OUT / 'Layer 2 - Clothing/Male Lamellar.png')
    Image.fromarray(build_heavy_shoulders()).save(OUT / 'Layer 4 - Shoulders and Arms accessories/Lamellar Shoulders.png')
    # then: python3 tools/armor-classes/cover_wraps.py --paperdoll (vambraces hide the white wrist wraps)
