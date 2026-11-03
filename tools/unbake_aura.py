"""Christopher 2026-11-03 19:28: all auras follow the outline of the hair. Clips whose aura was baked into fx.png round the base
figure (body, arms, gi) by grstrikes.aura / universal_sn.sn_aura get it taken back out: the same rings are recomputed on every
row and the pixels there that still hold an aura colour are cleared; the clip's spec json and animation.json get the runtime
`aura` record (the testbed grows it round the fighter's own silhouette). usage: unbake_aura.py <state> <widths csv> <inner> <outer>"""
import json, os, sys
from PIL import Image, ImageFilter
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
RULE = ('Runtime aura (Christopher 2026-11-03: all auras follow the outline of the hair): on frame k, when widths[k] > 0, the testbed grows the silhouette of every drawn layer '
        'except fx (body, clothing or armour, arms, shoulders, hair or helmet, eyes, weapons) by widths[k] rings of 1 px (4-neighbour / 3x3 max growth); ring 0 in colors[0], '
        'the others in colors[1]; the outermost ring only on pixels where (x + y + k) is even (flicker); drawn behind the fighter, only outside its silhouette')
def unbake(state, widths, cols):
    d = D + state + '/'; fx = Image.open(d + 'fx.png').convert('RGBA'); px = fx.load(); W, H = fx.size
    lay = [Image.open(d + f).convert('RGBA') for f in ('body.png', 'arms.png', 'male-gi.png') if os.path.exists(d + f)]
    rgb = {tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in cols}; n = 0
    for k, wd in enumerate(widths):
        if not wd: continue
        for r in range(H // 64):
            box = (k * 64, r * 64, k * 64 + 64, r * 64 + 64); m = Image.new('L', (64, 64))
            for l in lay: m.paste(255, (0, 0), l.crop(box).getchannel('A').point(lambda v: 255 if v else 0))
            g = m
            for _ in range(wd): g = g.filter(ImageFilter.MaxFilter(3))
            gp, mp = g.load(), m.load()
            for y in range(64):
                for x in range(64):
                    q = px[box[0] + x, box[1] + y]
                    if gp[x, y] and not mp[x, y] and q[3] and q[:3] in rgb: px[box[0] + x, box[1] + y] = (0, 0, 0, 0); n += 1
    fx.save(d + 'fx.png')
    rec = {'rule': RULE, 'widths': list(widths), 'colors': list(cols)}
    for f in (D + state + '.json', d + 'animation.json'):
        if os.path.exists(f): j = json.load(open(f)); j['aura'] = rec; json.dump(j, open(f, 'w'), indent=2)
    print(state, 'unbaked', n, 'px')
if __name__ == '__main__':
    st, w, a, b = sys.argv[1:5]; unbake(st, [int(v) for v in w.split(',')], (a, b))
