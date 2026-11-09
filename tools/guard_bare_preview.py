"""Preview (E/W) of the shieldless Guard set: shieldDisarmed chained into the two-handed idle, thrust and cut, composited in the
runtime's slot order (guard_preview.py), each shield type for the disarm. usage: guard_bare_preview.py <animDir> <out>"""
import sys, os, json
from PIL import Image
anim, out = sys.argv[1:3]
LOOK = ('far-arm', 'body', 'male-gi'), ('arms', 'fade-hair', 'brown-eyes')
BG = (0xc8, 0xcd, 0xd7, 255)
def cell(st, k, shield, x, d):
    sp = json.load(open(os.path.join(anim, st + '.json'))); row = sp['directions'].index(d)
    items = [(w['slot'], shield if w['slot'] == 'off' else w['items'][0]) for w in sp['weapons']]
    c = Image.new('RGBA', (128, 128), BG)
    def W(depth):
        for slot, it in items:
            p = os.path.join(anim, st, f'{slot}-{it}-{depth}.png')
            if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)), (x, 0))
    def L(n):
        p = os.path.join(anim, st, n + '.png')
        if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (32 + x, 32))
    W('behind')
    for l in LOOK[0]: L(l)
    W('front')
    for l in LOOK[1]: L(l)
    W('top'); W('trail'); L('fx')
    return c.crop((8, 24, 120, 104))
def seq(st, shield, d, x0=0):
    sp = json.load(open(os.path.join(anim, st + '.json'))); x = x0; r = []
    sgn = 1 if d == 'E' else -1
    for k in range(sp['frames']): x += sgn * sp['rootMotion']['E'][k][0]; r.append(cell(st, k, shield, x, d))
    return r
SH = ('shield-tower', 'shield-heater', 'shield-buckler')
CH = ['shieldDisarmed', 'spearTwoHandGuard', 'spearTwoHandGuard', 'spearTwoHandThrust', 'spearTwoHandGuard', 'spearTwoHandCut', 'spearTwoHandGuard']
S = 3
# strip: rows = each clip E then W (disarm per shield type)
rows = [seq('shieldDisarmed', sh, 'E') for sh in SH] + [seq('shieldDisarmed', 'shield-tower', 'W')]
for st in ('spearTwoHandGuard', 'spearTwoHandThrust', 'spearTwoHandCut'):
    rows += [seq(st, None, 'E'), seq(st, None, 'W')]
cw, ch = rows[0][0].size; m = max(len(r) for r in rows)
strip = Image.new('RGBA', (m * (cw * S + 3), len(rows) * (ch * S + 3)), 'white')
for i, r in enumerate(rows):
    for k, f in enumerate(r): strip.paste(f.resize((cw * S, ch * S), Image.NEAREST), (k * (cw * S + 3), i * (ch * S + 3)))
strip.save(out + '-EW-candidate.png')
# gif: the chain disarm -> idle -> thrust -> idle -> cut, one column per shield type, E on top, W below
cols = []
for sh in SH:
    for d in ('E', 'W'):
        fr = []
        for st in CH: fr += seq(st, sh, d)
        cols.append(fr)
frames = []
for k in range(len(cols[0])):
    f = Image.new('RGBA', (3 * (cw * 3 + 4), 2 * (ch * 3 + 4)), 'white')
    for i in range(3):
        for j in range(2): f.paste(cols[i * 2 + j][k].resize((cw * 3, ch * 3), Image.NEAREST), (i * (cw * 3 + 4), j * (ch * 3 + 4)))
    frames.append(f)
dur = []
for st in CH:
    fps = json.load(open(os.path.join(anim, st + '.json'))).get('fps', 10); n = json.load(open(os.path.join(anim, st + '.json')))['frames']
    dur += [int(1000 / fps)] * n
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=dur, loop=0, disposal=2)
print('wrote', out)
