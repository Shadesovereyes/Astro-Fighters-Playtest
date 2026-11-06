"""Guard set S/N preview: one Guard clip in S, E, N, W (rows) with each shield type (columns), as a gif.
usage: guard_sn_preview.py <animDir> <state> <out>
Based on guard_preview.py (E): every Guard clip with each shield type, composited in the runtime's order: per depth slot the
weapon items in the spec's list order (the off-slot shield first, the main yari over it; Christopher 2026-11-06 18:05).
usage: guard_preview.py <animDir> <out> [--gif state]"""
import sys, os, json
from PIL import Image
anim, ST, out = sys.argv[1:4]
CLIPS = ('spearGuard', 'spearThrust', 'yariCut', 'shieldBlock', 'shieldBash')
SHIELDS = ('shield-tower', 'shield-heater', 'shield-buckler')
LOOK = ('far-arm', 'body', 'male-gi'), ('arms', 'fade-hair', 'brown-eyes')   # the testbed's slot order: front weapons before the arms, hair and eyes after them, top last
def cell(st, k, shield, x, d='E'):
    sp = json.load(open(os.path.join(anim, st + '.json'))); row = sp['directions'].index(d)
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
def seq(st, shield, d):
    sp = json.load(open(os.path.join(anim, st + '.json'))); x = 0; r = []
    for k in range(sp['frames']): x += sp['rootMotion'][d][k][0]; r.append(cell(st, k, shield, x, d))
    return r
g = {(d, sh): seq(ST, sh, d) for d in 'SENW' for sh in SHIELDS}
cw, ch = g[('S', SHIELDS[0])][0].size; n = len(g[('S', SHIELDS[0])]); frames = []
for k in range(n):
    f = Image.new('RGBA', (3 * (cw * 3 + 4), 4 * (ch * 3 + 4)), 'white')
    for j, d in enumerate('SENW'):
        for i, sh in enumerate(SHIELDS): f.paste(g[(d, sh)][k].resize((cw * 3, ch * 3), Image.NEAREST), (i * (cw * 3 + 4), j * (ch * 3 + 4)))
    frames.append(f)
fps = json.load(open(os.path.join(anim, ST + '.json'))).get('fps', 12)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:] + [frames[-1]] * 2, duration=int(1000 / fps), loop=0, disposal=2)
strip = Image.new('RGBA', (n * (f.width + 6), f.height), 'white')
for k, fr_ in enumerate(frames): strip.paste(fr_, (k * (f.width + 6), 0))
strip.save(out + '-SENW-candidate.png'); print('wrote', out)
