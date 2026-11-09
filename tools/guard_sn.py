"""S/N v1 of the Guard spear-and-shield set (Christopher 2026-11-06 18:14: shield layering accepted, the spear and shield
set cleared to develop further). The yari takes tanto.py's S/N projection from the oneHandGuard frontal (a level spear points
at the viewer in S, foreshortened; hidden in front of the body in N). The shield (off slot, every type: tower, heater,
buckler) sits on the far fist in both views: S face-on (widened) on the top slot in front of both forearms,
cut away only under the yari; N behind the body, so only its rim shows outside the figure.
E/W pixels and weapon sheets are restored from HEAD afterwards.
Run: python3 tools/guard_sn.py [state..]   (does the whole loop)"""
import sys, os, json, math, subprocess, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.argv = sys.argv[:1] + [a for a in sys.argv[1:]]
args = sys.argv[1:]; sys.argv = sys.argv[:1]
import standin_weapons as SW, tanto as T
from PIL import Image
R = T.R; D = T.D
STAT = {'spearGuard': '17:30', 'spearThrust': '17:30', 'yariCut': '17:30', 'shieldBlock': '17:30', 'shieldBash': '17:30'}
FACE = {'shield-tower': 1.75, 'shield-heater': 1.7, 'shield-buckler': 1.3}   # S: the shield face-on, its full width (widthScale across the axis)
def lhand(spec, d, k):
    ab = spec['frontal']['views'][d]['armBand']['L']; at = lambda v: v[k] if isinstance(v, list) else v
    sc = at(ab['scale']) or 1; el = at(ab['elbow']); a = math.radians(at(ab['angle'])); px, py = ab['pivot']
    dy = (spec['bob'].get('arms') or spec['bob']['dy'])[k]
    u0 = (el['at'] if el else 12) * sc; x = px - math.sin(a) * u0; y = py + dy + math.cos(a) * u0
    if el: e = math.radians(el['angle']); x -= math.sin(e) * (12 - el['at']) * sc; y += math.cos(e) * (12 - el['at']) * sc
    return round(x), round(y)
def occlude_s(state):
    """S row: the face-on shield is in front of both forearms (whole shield on the top slot), cut away only under the yari"""
    d = D + state + '/'; dirs = T.load(D + state + '.json')['directions']; r = dirs.index('S')
    ys = [Image.open(d + f).convert('RGBA') for f in os.listdir(d) if f.startswith('main-yari-')]
    for sh in SW.SHIELDS:
        f = d + 'off-%s-top.png' % sh
        if not os.path.exists(f): continue
        im = Image.open(f).convert('RGBA'); px = im.load(); mp = [m.load() for m in ys]
        for y in range(r * 128, r * 128 + 128):
            for x in range(im.size[0]):
                if px[x, y][3] and any(m[x, y][3] for m in mp): px[x, y] = (0, 0, 0, 0)
        im.save(f)
def run(state):
    T.sn(state)
    s = T.load(D + state + '.json'); off = next(w for w in s['weapons'] if w.get('slot') == 'off'); E = off['E']
    off['S'] = []; off['N'] = []
    for k in range(s['frames']):
        lx, ly = lhand(s, 'S', k); ang = E[k]['angle']
        off['S'].append({'grip': [lx + 1, ly], 'angle': ang, 'z': 'top'})
        off['N'].append({'grip': [64 - lx - 1, ly], 'angle': ang, 'z': 'behind'})
    off['itemPoses'] = {it: {'S': {'widthScale': w_}} for it, w_ in FACE.items()}
    off['projectionRule'] = 'S: upright on the far fist, turned face-on (itemPoses widthScale), the whole shield on the top slot in front of both forearms, cut away only under the yari; N: behind the body, only the rim shows outside the figure'
    s['status'] = 'E/W approved by user 2026-11-06 18:14 (Guard set v3.1 layering); S/N approved by user 2026-11-09 16:26 (v1); whole spear-and-shield kit incl. tower shield v2.2 approved by user 2026-11-09 16:51; W mirrors E'
    for w in s['weapons']: w['status'] = s['status']
    T.save(s, D + state + '.json')
    sh = lambda *c: subprocess.run(c, cwd=R, check=True, capture_output=True)
    sh('node', 'tools/character-posed.mjs', 'male', state); sh('python3', 'tools/stances.py', '--outline', state)
    T.restore(state); sh('node', 'tools/character-weapon.mjs', 'male', state); occlude_s(state); T.fx(state)
    d = D + state + '/'
    for f in sorted(os.listdir(d)):   # weapon sheets and fx: the approved E/W rows from HEAD
        if not (f.startswith('main-') or f.startswith('off-') or f == 'fx.png'): continue
        try: old = Image.open(io.BytesIO(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + os.path.relpath(d + f, R)], stderr=subprocess.DEVNULL))).convert('RGBA')
        except subprocess.CalledProcessError: continue
        new = Image.open(d + f).convert('RGBA'); F = old.height // 2
        for o, n in ((0, 1), (1, 3)):
            new.paste(Image.new('RGBA', (new.width, F)), (0, n * F)); new.paste(old.crop((0, o * F, old.width, o * F + F)), (0, n * F))
        new.save(d + f)
    print(state, 'S/N done')
for st in (args or SW.SHIELD): run(st)
