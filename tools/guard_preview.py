"""Guard set preview (E): every Guard clip with each shield type, composited in the runtime's order: per depth slot the
weapon items in the spec's list order (the off-slot shield first, the main yari over it; Christopher 2026-11-06 18:05).
usage: guard_preview.py <animDir> <out> [--gif state]"""
import sys, os, json
from PIL import Image
anim, out = sys.argv[1:3]
GIF = sys.argv[sys.argv.index('--gif') + 1] if '--gif' in sys.argv else 'spearThrust'
CLIPS = ('spearGuard', 'spearThrust', 'yariCut', 'shieldBlock', 'shieldBash')
SHIELDS = ('shield-tower', 'shield-heater', 'shield-buckler')
LOOK = ('far-arm', 'body', 'male-gi'), ('fade-hair', 'brown-eyes', 'arms')
def cell(st, k, shield, x):
    sp = json.load(open(os.path.join(anim, st + '.json'))); row = sp['directions'].index('E')
    items = [(w['slot'], shield if w['slot'] == 'off' else w['items'][0]) for w in sp['weapons']]
    c = Image.new('RGBA', (128, 128), (0xc8, 0xcd, 0xd7, 255))
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
    return c.crop((20, 24, 108, 104))
def seq(st, shield):
    sp = json.load(open(os.path.join(anim, st + '.json'))); x = 0; r = []
    for k in range(sp['frames']): x += sp['rootMotion']['E'][k][0]; r.append(cell(st, k, shield, x))
    return r
S = 3; rows = []
for sh in SHIELDS:
    fr = [f for st in CLIPS for f in seq(st, sh)]
    rows.append(fr)
cw, ch = rows[0][0].size
strip = Image.new('RGBA', (len(rows[0]) * (cw * S + 3), len(rows) * (ch * S + 3)), 'white')
for i, r in enumerate(rows):
    for k, f in enumerate(r): strip.paste(f.resize((cw * S, ch * S), Image.NEAREST), (k * (cw * S + 3), i * (ch * S + 3)))
strip.save(out + '-E-candidate.png')
g = [seq(GIF, sh) for sh in SHIELDS]; frames = []
for k in range(len(g[0])):
    f = Image.new('RGBA', (3 * (cw * 4 + 4), ch * 4), 'white')
    for i in range(3): f.paste(g[i][k].resize((cw * 4, ch * 4), Image.NEAREST), (i * (cw * 4 + 4), 0))
    frames.append(f)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:] + [frames[-1]] * 3, duration=83, loop=0, disposal=2)
print('wrote', out, strip.size)
