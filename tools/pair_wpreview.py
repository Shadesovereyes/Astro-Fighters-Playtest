"""Pair preview with weapon layers (main-<item>-<depth>.png, 128 px cells, character at +32): front sheets after the
owner's body group, top sheets over everything. Otherwise identical to pairpreview.py.
Mechanical pair preview: composites two rendered posed-animation sheets (E holder, W partner) into
91x64 cells, applies rootMotion, scales 4x nearest, writes an E strip PNG and a 12 fps GIF.
usage: pairpreview.py <animDir> <holderState> <partnerState> <outPrefix> [--swap-from K] [--cell W]
Layer groups per frame come from the holder spec's pair.layering / pair.mountLayering (fromFrame)."""
import json, sys, os, glob
def _paste(im, w, x, y):
    t = Image.new('RGBA', im.size, (0, 0, 0, 0)); t.paste(w, (x, y)); im.alpha_composite(t)
from PIL import Image

anim, A, B, out = sys.argv[1:5]
args = sys.argv[5:]
CELL_W = int(args[args.index('--cell') + 1]) if '--cell' in args else 91
F = 64
spec = json.load(open(os.path.join(anim, A + '.json')))
specB = json.load(open(os.path.join(anim, B + '.json')))
pdx = spec['pair'].get('partnerDx', 27)
x0 = int(args[args.index('--x0') + 1]) if '--x0' in args else 0
n = spec['frames']
LOOK = {
    'A': ['male-gi', 'fade-hair', 'brown-eyes'],
    'B': ['male-red-armor', 'red-armor-shoulders', 'long-hair', 'brown-eyes'],
}

def sheet(state, layer):
    p = os.path.join(anim, state, layer + '.png')
    return Image.open(p).convert('RGBA') if os.path.exists(p) else None

def cell(state, layer, row, k):
    s = sheet(state, layer)
    if s is None: return None
    return s.crop((k * F, row * F, k * F + F, row * F + F))

def cum(motion, k):
    x = y = 0
    for i in range(k + 1):
        x += motion[i][0]; y += motion[i][1]
    return x, y

# role -> (state, row, origin x); A faces E (row 0), B faces W (row 1)
roles = {'A': (A, spec['directions'].index('E'), x0), 'B': (B, specB['directions'].index('W'), x0 + pdx)}
mA, mB = spec['rootMotion']['E'], specB['rootMotion']['W']

def groups(k):
    ml = dict(specB['pair'].get('mountLayering') or {}); ml.update(spec['pair'].get('mountLayering') or {})
    if not ml: ml = None
    elif 'bottomOverFrom' in ml and k >= ml['bottomOverFrom']: ml['bottomOver'] = True
    top = 'B' if spec['pair'].get('top') == 'partner' else 'A'
    if ml and k >= ml.get('topSwapFrom', 99): top = 'B' if top == 'A' else 'A'
    bot = 'B' if top == 'A' else 'A'
    if ml and k >= ml['fromFrame']:
        bodyset = lambda r: ['body', *LOOK[r][:-1], LOOK[r][-1]] + (['fx'] if True else [])
        if ml.get('bottomArmsOver'):
            return [(bot, ['body'] + LOOK[bot] + ['fx']), (top, ['far-arm', 'body'] + LOOK[top] + ['fx']), (top, ['arms']), (bot, ['far-arm', 'arms'])]
        if ml.get('bottomOver'):
            return [(top, ['far-arm', 'body'] + LOOK[top] + ['fx']), (bot, ['far-arm', 'body'] + LOOK[bot] + ['fx']), (top, ['arms']), (bot, ['arms'])]
        return [(bot, ['body'] + LOOK[bot] + ['fx']), (top, ['far-arm', 'body'] + LOOK[top] + ['fx']), (bot, ['far-arm', 'arms']), (top, ['arms'])]
    h, d = ('B', 'A') if k < spec['pair'].get('heldLayeringUntil', 0) else ('A', 'B')
    return [(h, ['far-arm']), (d, ['far-arm']), (h, ['body'] + LOOK[h] + ['fx']), (d, ['body'] + LOOK[d] + ['fx']), (d, ['arms']), (h, ['arms'])]

frames = []
for k in range(n):
    im = Image.new('RGBA', (CELL_W, F), (0xc8, 0xcd, 0xd7, 255))
    for role, layers in groups(k):
        st, row, ox = roles[role]
        mx, my = cum(mA if role == 'A' else mB, k)
        for l in layers:
            c = cell(st, l, row, k)
            if c is not None: im.alpha_composite(c, (ox + mx, my))
        if layers[-1] == 'arms' and 'body' not in layers:   # top weapon sheets ride on their owner's arms group (under a later, higher partner arms group)
            for wp in sorted(glob.glob(os.path.join(anim, st, 'main-*-top.png'))):
                _paste(im, Image.open(wp).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)), ox + mx - 32, my - 32)
        if 'body' in layers:
            for wp in sorted(glob.glob(os.path.join(anim, st, 'main-*-front.png'))):
                w = Image.open(wp).convert('RGBA').crop((k * 128, row * 128, k * 128 + 128, row * 128 + 128)); im.alpha_composite(w, (ox + mx - 32, my - 32)) if ox + mx >= 32 and my >= 32 else _paste(im, w, ox + mx - 32, my - 32)
    for role, sp in (('A', spec), ('B', specB)):   # fx.top: an impact flash is drawn over both fighters
        if (sp.get('fx') or {}).get('top'):
            st, row, ox = roles[role]; mx, my = cum(mA if role == 'A' else mB, k)
            c = cell(st, 'fx', row, k)
            if c is not None: im.alpha_composite(c, (ox + mx, my))
    frames.append(im.resize((CELL_W * 4, F * 4), Image.NEAREST))
gap = 5 * 4 // 4
W = len(frames) * CELL_W * 4 + (len(frames) - 1) * 5
strip = Image.new('RGBA', (W, F * 4), (255, 255, 255, 255))
for i, f in enumerate(frames): strip.paste(f, (i * (CELL_W * 4 + 5), 0))
strip.save(out + '-E-candidate.png')
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=int(1000 / spec.get('fps', 12)), loop=0, disposal=2)
print('wrote', out)
