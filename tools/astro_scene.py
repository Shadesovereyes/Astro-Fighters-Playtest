"""Astro kit scene preview with root motion and an optional flown projectile (Libra Aero Palm, Feather Step).
usage: astro_scene.py anim A out [--gap G] [--target B HITFRAME] [--proj PATTERN FROMFRAME FLYFRAMES HITPATTERN] [--solo]
  caster A at the left facing E (root motion applied, so travel clips move across a wide cell);
  --target: the target stands in its guard at the right facing W and plays B once from HITFRAME;
  --proj: from FROMFRAME the NPAT pattern flies from the caster's near hand to the target chest over FLYFRAMES, then HITPATTERN pops there;
  --solo: no target (teleports / dashes)."""
import json, sys, os
from PIL import Image
sys.path.insert(0, os.environ.get('ASTRO_TOOLS', '/home/claude/astro-fighters-playtest/tools'))
import astro
a = sys.argv[1:]; anim, A, out = a[:3]; opt = a[3:]
def arg(k, n):
    return opt[opt.index(k) + 1: opt.index(k) + 1 + n] if k in opt else None
GAP = int((arg('--gap', 1) or [66])[0]); solo = '--solo' in opt
tg = arg('--target', 2)
PR = [opt[i + 1:i + 6] for i, o in enumerate(opt) if o == '--proj']   # repeatable: PATTERN FROMFRAME FLYFRAMES HITPATTERN [hand|farhand|mouth]
LAY = ['far-arm', 'body', 'skin-fx', 'male-gi', 'fade-hair', 'brown-eyes', 'arms', 'arms-fx', 'fx']
CW = GAP + 84 if not solo else max(150, GAP + 70)
def spec(s): return json.load(open(os.path.join(anim, s + '.json')))
OUT = (arg('--outfit', 1) or [None])[0]   # caster outfit, e.g. male-lamellar,lamellar-shoulders,locs-tied,purple-eyes (clothing, shoulders, hair, eyes)
def outfit(lay):
    if not OUT: return lay
    o = OUT.split(','); cl, sh, hr, ey = (o + [None] * 4)[:4]
    out = []
    for l in lay:
        if l == 'male-gi': out += [cl]
        elif l == 'fade-hair': out += []
        elif l == 'brown-eyes': out += []
        elif l == 'arms-fx': out += [l] + ([sh] if sh else [])
        else: out += [l]
        if l == 'arms' and 'arms-fx' not in lay and sh: out += [sh]
        if l == 'arms-fx' or (l == 'arms' and 'arms-fx' not in lay): out += [hr or 'fade-hair', ey or 'brown-eyes']
    return [l for l in out if l]
def runtime_aura(state, k, d, lay, x, img):   # the testbed's runtime aura (Christopher 2026-11-03 19:28: auras follow the hair outline): grown from the composited silhouette of every drawn layer but fx
    au = spec(state).get('aura'); wd = au['widths'][k] if au and k < len(au['widths']) else 0
    if not wd: return
    from PIL import ImageFilter
    row = spec(state)['directions'].index(d); m = Image.new('L', (64, 64))
    for l in lay:
        p_ = os.path.join(anim, state, l + '.png')
        if l != 'fx' and os.path.exists(p_): m.paste(255, (0, 0), Image.open(p_).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)).getchannel('A').point(lambda v: 255 if v else 0))
    out = Image.new('RGBA', (64, 64)); op = out.load(); prev = m
    for ring in range(wd):
        g_ = prev.filter(ImageFilter.MaxFilter(3)); gp, pp = g_.load(), prev.load(); c = au['colors'][0 if ring == 0 else 1]
        for yy in range(64):
            for xx in range(64):
                if gp[xx, yy] and not pp[xx, yy] and (ring < wd - 1 or (xx + yy + k) % 2 == 0): op[xx, yy] = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
        prev = g_
    img.alpha_composite(out, (x, 0))
def cell(state, k, d, x, img, lay=None, who=None):
    row = spec(state)['directions'].index(d); lay = lay or LAY
    if who == 'caster': lay = outfit(lay)
    if 'fx' in lay: runtime_aura(state, k, d, lay, x, img)
    for l in lay:
        p = os.path.join(anim, state, l + '.png')
        if os.path.exists(p): img.alpha_composite(Image.open(p).convert('RGBA').crop((k * 64, row * 64, k * 64 + 64, row * 64 + 64)), (x, 0))
def hand(state, k, d, layer='arms'):
    row = spec(state)['directions'].index(d); im = Image.open(os.path.join(anim, state, layer + '.png')).convert('RGBA').load()
    pts = [(x, y) for y in range(64) for x in range(64) if im[k * 64 + x, row * 64 + y][3]]
    return max(pts, key=lambda q: (q[0], -q[1])) if pts else (40, 24)
def stamp(img, name, cx, cy, alpha=255):
    pat = astro.NPAT[name]; h, w = len(pat), len(pat[0]); x0, y0 = round(cx - (w - 1) / 2), round(cy - (h - 1) / 2); px = img.load()
    for yy, row in enumerate(pat):
        for xx, ch in enumerate(row):
            if ch != '.' and 0 <= x0 + xx < img.size[0] and 0 <= y0 + yy < img.size[1]:
                c = astro.NPAL[ch]; px[x0 + xx, y0 + yy] = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (alpha,)
GUARD = os.environ.get('SCENE_GUARD', 'guard')   # 2026-11-04: the plain boxing guard (hitReact frame 0 is the recoil pose, which read as the target reacting before the impact)
sa = spec(A); na = sa['frames']; rm = sa['rootMotion']['E']
n = na + 4
if tg: B, hit = tg[0], int(tg[1]); nb = spec(B)['frames']; n = max(n, hit + nb + 2)
frames = []
for t in range(n):
    c = Image.new('RGBA', (CW, 64), (0xc8, 0xcd, 0xd7, 255)); ka = min(t, na - 1)
    xa = 4 + sum(rm[q][0] for q in range(ka + 1))
    if sa.get('clones') and t < na:   # runtime copies of the caster (Mirage Clone, Phantom Legion v2): its own outfit, as the testbed draws them
        me = Image.new('RGBA', (64, 64)); cell(A, ka, 'E', 0, me, [l for l in LAY if l not in ('fx', 'skin-fx', 'arms-fx')], who='caster'); mp_ = me.load()
        for it in sorted(sa['clones']['frames'].get(str(ka), []), key=lambda t_: -abs(t_[0])):
            dx, al = it[0], it[1]; wash = it[2] if len(it) > 2 else 0.35; rim = tuple(int(it[3][i:i + 2], 16) for i in (1, 3, 5)) if len(it) > 3 and it[3] else None
            lay_ = Image.new('RGBA', (64, 64)); lp = lay_.load()
            for yy in range(64):
                for xx in range(64):
                    q = mp_[xx, yy]; X = xx + dx
                    if not q[3] or not (0 <= X < 64) or mp_[X, yy][3]: continue
                    edge = rim and any(not (0 <= xx + ex < 64 and 0 <= yy + ey < 64) or not mp_[xx + ex, yy + ey][3] for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    lp[X, yy] = (rim if edge else tuple(round(q[i] * (1 - wash) + (233, 238, 244)[i] * wash) for i in range(3))) + (al,)
            c.alpha_composite(lay_, (xa, 0))
    cell(A, ka, 'E', xa, c, who='caster')
    if tg and not solo:
        kb = t - hit
        if 0 <= kb < nb and '--legion' in opt and spec(B).get('legion'):   # Phantom Beset: copies of the caster (its own outfit) drawn behind the target, as the testbed does
            lg = spec(B)['legion']; items = lg['frames'].get(str(kb), [])
            tgt = Image.new('RGBA', (64, 64)); cell(B, kb, 'W', 0, tgt, LAY[:-1]); tp = tgt.load()
            for dx, al in sorted(items, key=lambda t: -abs(t[0])):
                cp_ = Image.new('RGBA', (64, 64)); cell(lg['src'], lg['srcFrame'], 'E' if dx > 0 else 'W', 0, cp_, [l for l in LAY if l not in ('fx', 'skin-fx', 'arms-fx')], who='caster'); q_ = cp_.load()
                lay_ = Image.new('RGBA', (64, 64)); lp = lay_.load()
                for yy in range(64):
                    for xx in range(64):
                        q = q_[xx, yy]; X = xx - dx   # the target faces W here: dx toward its facing is -x
                        if not q[3] or not (0 <= X < 64) or tp[X, yy][3]: continue
                        edge = any(not (0 <= xx + ex < 64 and 0 <= yy + ey < 64) or not q_[xx + ex, yy + ey][3] for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                        lp[X, yy] = ((0x39, 0xe7, 0x5f) if edge else tuple(round(q[i] * 0.65 + (233, 238, 244)[i] * 0.35) for i in range(3))) + (al,)
                c.alpha_composite(lay_, (4 + GAP, 0))
        if 0 <= kb < nb: cell(B, kb, 'W', 4 + GAP, c)
        elif kb < 0: cell(GUARD, 0, 'W', 4 + GAP, c, LAY[:-1])   # before the hit: the target in a plain guard, no fx (v2: B's frame 0 showed its fx before the cast landed)
        else: cell(B, nb - 1, 'W', 4 + GAP, c) if B != 'hitReact' else cell('hitReact', 6, 'W', 4 + GAP, c)
    mk = arg('--mark', 1)   # the genjutsu mark over the target from the hit on, recoloured for the element (as the testbed draws it)
    if mk and tg and t >= hit:
        gs = spec('genjutsuAfflicted'); rc = {tuple(int(a[i:i + 2], 16) for i in (1, 3, 5)): tuple(int(b[i:i + 2], 16) for i in (1, 3, 5)) for a, b in gs['genjutsuMark']['recolor'][mk[0]].items() if a.startswith('#')}
        row = gs['directions'].index('W'); kk = (t - hit) % gs['frames']
        for l in ('fx', 'skin-fx'):
            pth = os.path.join(anim, 'genjutsuAfflicted', l + '.png')
            if not os.path.exists(pth): continue
            m = Image.open(pth).convert('RGBA').crop((kk * 64, row * 64, kk * 64 + 64, row * 64 + 64)); mp = m.load()
            for yy in range(64):
                for xx in range(64):
                    q = mp[xx, yy]
                    if q[3] and q[:3] in rc: mp[xx, yy] = rc[q[:3]] + (q[3],)
            c.alpha_composite(m, (4 + GAP, 0))
    for pr in PR:
        pat, f0, nf, hp = pr[0], int(pr[1]), int(pr[2]), pr[3]; lay = 'far-arm' if len(pr) > 4 and pr[4] == 'farhand' and os.path.exists(os.path.join(anim, A, 'far-arm.png')) else 'arms'
        hx, hy = hand(A, f0, 'E', lay)
        if len(pr) > 4 and pr[4] == 'mouth':   # Howling Blast v2: from the mouth (eye centre, 3 px down, a few px ahead)
            ex_ = astro._eye(A, f0, spec(A)['directions'].index('E')); hx, hy = (ex_[0], ex_[1] + 3) if ex_ else (hx, hy)
        sx, sy = 4 + sum(rm[q][0] for q in range(f0 + 1)) + hx + 6, hy; ex, ey = 4 + GAP + 26, 24
        if f0 <= t < f0 + nf:
            u = (t - f0 + 1) / nf; stamp(c, pat, sx + (ex - sx) * u, sy + (ey - sy) * u)
        elif f0 + nf <= t < f0 + nf + 2: stamp(c, hp, ex, ey, 255 if t == f0 + nf else 150)
    st = sa.get('stream') if '--stream' in opt and tg else None   # Hydro Cannon Palm v2: the testbed's stream from the palm to the target
    if st and t < na and (ka in st['frames'] or ka == st.get('tailFrame')):
        hx, hy = hand(A, ka, 'E'); sx = xa + hx + 1; ex = 4 + GAP + 22; T = st['tile']
        early = ka < st.get('reachFrame', -1); ex_full = ex
        if early: ex = sx + round((ex - sx) * float(st.get('travel', {}).get(str(ka), 0.5)))   # the stream front still travelling (impact-frame rule: no hit until reachFrame; v5 travel fractions per frame)
        xs = list(range(sx, ex, T)); tail = ka == st.get('tailFrame')
        for i, x0 in enumerate(xs):
            if tail and i < len(xs) * 2 // 3: continue
            pat = astro.NPAT[st['tail'] if tail else st['tiles'][(ka + i) % 4]]; ph, pw = len(pat), len(pat[0])
            tile = Image.new('RGBA', (pw, ph)); tp = tile.load()
            for yy, row in enumerate(pat):
                for xx, ch in enumerate(row):
                    if ch != '.' and x0 + xx < ex: c_ = astro.NPAL[ch]; tp[xx, yy] = tuple(int(c_[j:j + 2], 16) for j in (1, 3, 5)) + (255,)
            c.alpha_composite(tile, (x0, hy - ph // 2))
        if early: stamp(c, st.get('front', 'wSplashS'), ex, hy)
        elif not tail:
            h0 = st.get('reachFrame', st['frames'][0]); hp = astro.NPAT[st['hit'][(ka - h0) % 4]]; stamp(c, st['hit'][(ka - h0) % 4], ex + (len(hp[0]) - 1) / 2, hy)
    frames.append(c.resize((CW * 4, 256), Image.NEAREST))
fps = sa.get('fps', 10)
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
KEY = list(range(min(n, 12)))
sheet = Image.new('RGBA', (CW * 4 * 2 + 16, 264 * ((len(KEY) + 1) // 2)), 'white')
for i, f in enumerate(frames[q] for q in KEY): sheet.paste(f, ((i % 2) * (CW * 4 + 16), (i // 2) * 264))
sheet.save(out + '-E-candidate.png'); print('wrote', out, n)
