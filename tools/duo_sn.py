"""S/N pair preview for an attacker clip and its target's clip: left scene, the attacker faces S (toward the viewer) with
the target in front of it facing N; right scene, the attacker faces N with the target beyond it facing S. The nearer fighter
is drawn over. Layers gi/fade hair/brown eyes (attacker), red armour/long hair (target); 4x nearest.
usage: duo_sn.py <animDir> <attacker> <target> <out> [--gap N]"""
import json, sys, os
from PIL import Image
anim, A, T, out = sys.argv[1:5]; a = sys.argv[5:]
GAP = int(a[a.index('--gap') + 1]) if '--gap' in a else 14
LA = ['far-arm', 'body', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'fx']
LT = ['far-arm', 'body', 'male-red-armor', 'red-armor-shoulders', 'long-hair', 'brown-eyes', 'arms', 'fx']
def cells(st, d, lay):
    s = json.load(open(os.path.join(anim, st + '.json'))); row = s['directions'].index(d); res = []
    for k in range(s['frames']):
        c = Image.new('RGBA', (64, 64))
        for l in lay:
            p = os.path.join(anim, st, l + '.png')
            if os.path.exists(p): c.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)))
        res.append(c)
    return res, s.get('fps', 10)
AS, fps = cells(A, 'S', LA); TN, _ = cells(T, 'N', LT); AN, _ = cells(A, 'N', LA); TS, _ = cells(T, 'S', LT)
H = 64 + GAP + 8; frames = []
for k in range(len(AS)):
    f = Image.new('RGBA', (2 * 72 + 4, H), (0xc8, 0xcd, 0xd7, 255)); t = min(k, len(TN) - 1)
    f.alpha_composite(AS[k], (4, 4)); f.alpha_composite(TN[t], (4, 4 + GAP))          # S scene: target nearer, over
    f.alpha_composite(TS[t], (76, 4)); f.alpha_composite(AN[k], (76, 4 + GAP))        # N scene: attacker nearer, over
    frames.append(f.resize((f.width * 4, H * 4), Image.NEAREST))
w = frames[0].width; strip = Image.new('RGBA', (len(frames) * (w + 5) - 5, H * 4), 'white')
for k, f in enumerate(frames): strip.paste(f, (k * (w + 5), 0))
strip.save(out + '-SN-candidate.png')
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:] + [frames[-1]] * 4, duration=int(1000 / fps), loop=0, disposal=2)
print('wrote', out)
