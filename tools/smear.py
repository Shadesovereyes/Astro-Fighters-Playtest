"""Smear frames for fast strikes (Christopher 2026-11-16: "introduce smear frames/motion blur for abilities meant to
seem fast").

A smear frame shows the striking limb's path: on frame k the limb is also drawn at in-between poses from frame k-1
towards k, behind the real limb and outside the body's silhouette. The in-between poses are rendered through the rig
(a temporary state whose frame k-1 holds the interpolated limb), so every layer (body, arms, gloves, shorts, Gi, hair,
armour) smears with the fighter's own look (ANIMATION_RULES: own look). Smear pixels are drawn flat: interior outline
pixels are dropped and only the smear's outer edge keeps an outline, so the path reads as one fast shape.

Usage: python3 tools/smear.py <state> <k>:<limbs>[,...] [--steps 0.35,0.7]
  limbs: arm-near arm-far leg-near leg-far joined with '+', e.g. muayThaiJabCross 5:arm-far
Writes the smear into the state's E and W layer sheets in place (run after render, gloves and close_seams).
"""
import copy, json, math, subprocess, sys, shutil
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ANIM = ROOT / 'production/source/characters/anim/male'
F = 64
DITHER = 0.5

LONG = False
def lerp_angle(a, b, t):
    d = (b - a + 180) % 360 - 180
    if LONG: d = d - 360 if d > 0 else d + 360
    return a + d * t

def lerp_arm(a, b, t):
    if a.get('construction') != 'band' or b.get('construction') != 'band': return copy.deepcopy(b if t > 0.5 else a)
    out = copy.deepcopy(b)
    out['angle'] = round(lerp_angle(a['angle'], b['angle'], t), 1)
    if 'elbow' in a and 'elbow' in b:
        out['elbow'] = dict(b['elbow'], angle=round(lerp_angle(a['elbow']['angle'], b['elbow']['angle'], t), 1),
                            at=round(a['elbow']['at'] + (b['elbow']['at'] - a['elbow']['at']) * t))
    for key in ('scale',):
        if key in a and key in b: out[key] = a[key] + (b[key] - a[key]) * t
    return out

def lerp_pose(a, b, t, name):
    out = copy.deepcopy(b); out['name'] = name
    for key, v in b.items():
        if key in a and isinstance(v, (int, float)) and isinstance(a[key], (int, float)) and key != 'name':
            out[key] = round(a[key] + (v - a[key]) * t)
        elif key in a and isinstance(v, list) and isinstance(a[key], list) and len(v) == len(a[key]) and all(isinstance(q, (int, float)) for q in v + a[key]):
            out[key] = [round(p + (q - p) * t) for p, q in zip(a[key], v)]
    # mixed constructions: footX/wrapRow (line) vs ankle (band): fall back to the target's own fields
    return out

def temp_spec(spec, k, limbs, t, tag):
    s = copy.deepcopy(spec); s['state'] = tag
    for limb in limbs:
        kind, side = limb.split('-')
        if kind == 'arm':
            arr = s['arms'][side]; arr[k - 1] = lerp_arm(spec['arms'][side][k - 1], spec['arms'][side][k], t)
        else:
            poses = s['legs']['poses']; arr = s['legs'][side]
            a, b = poses[spec['legs'][side][k - 1]], poses[spec['legs'][side][k]]
            poses.append(lerp_pose(a, b, t, f'smear-{side}-{k}-{t}')); arr[k - 1] = len(poses) - 1
    return s

TRAIL_FROM = 0.0
def fist_trail(state, k, side='near', segs=((None, (0.25, 0.5, 0.75, 1.0)), (None, (0.25, 0.5, 0.75, 1.0))), solid=0.5, onto=False):
    """Hooks and swings (haymaker, hook, uppercut, elbow, body shot): the fist leaves a tapered ribbon along its real
    path, drawn on the inserted smear frame k (the frame before the impact, see insert_smear). Path: the rig's fist at
    in-between poses of the two spec moves leading into the inserted frame (spec frames k-2 -> k-1 and k-1 -> k, where
    k-1/k are the ORIGINAL spec indices of the frames around the insert), found exactly with hand_masks. The ribbon
    is painted per layer in that layer's own fist colours (bare skin on arms/body, leather on each glove sheet), widens
    from a point to the fist's own height, the older half dithered, outlined only against empty space, and never
    covers the figure (own-look and impact rules, Christopher 2026-11-16/17)."""
    spec = json.loads((ANIM / f'{state}.json').read_text())
    d = ANIM / state; anim = layers_of(d); rows = anim['sheetLayout']['rows']
    sys.path.insert(0, str(ROOT / 'tools/fight-gear'))
    import hand_masks, glove_states
    sheets = {n: np.array(Image.open(d / f).convert('RGBA')) for n, f in anim['layers'].items() if (d / f).exists()}
    lay = 'arms' if side == 'near' else 'body'
    path = {dn: [] for dn in ('E', 'W')}   # per direction: [(t_global, cx, cy, {layer: (mid rgb, light rgb)}, half)]
    tags = []
    # onto=True: the trail goes on an existing pre-impact frame k (path spec k-1 -> k), no insert needed
    jobs = [(k, (0.0, 0.2, 0.4, 0.6, 0.8, 1.0))] if onto else [(k - 1, ts) for ts in [segs[0][1]]] + [(k, [t * 0.55 for t in segs[1][1]])]
    order = 0
    for kk, ts in jobs:
        for t in ts:
            tag = f'zzTrail{order}{state}'; order += 1; tags.append(tag)
            (ANIM / f'{tag}.json').write_text(json.dumps(temp_spec(spec, kk, [f'arm-{side}'], t, tag)))
            r = subprocess.run(['node', 'tools/character-posed.mjs', 'male', tag], cwd=ROOT, capture_output=True, text=True)
            if r.returncode: raise SystemExit(r.stderr[-800:])
            hand_masks.run(tag)
            if any(n.endswith('gloves') for n in sheets): glove_states.run(ANIM / tag)
            m = np.load(hand_masks.MASKS / f'{tag}.npz')[lay]
            ta = layers_of(ANIM / tag)
            tl = {n: np.array(Image.open(ANIM / tag / ta['layers'][n]).convert('RGBA')) for n in sheets if n in ta['layers'] and (ANIM / tag / ta['layers'][n]).exists()}
            for di, dn in enumerate(rows):
                if dn not in path: continue
                y0, x0 = di * F, (kk - 1) * F
                hm = (m[y0:y0 + F, x0:x0 + F] >= 0) & (m[y0:y0 + F, x0:x0 + F] <= 4)
                ys, xs = np.nonzero(hm)
                if not len(ys): continue
                cols = {}
                for n, a in tl.items():
                    c = a[y0:y0 + F, x0:x0 + F]
                    if n == lay: blob = hm; px = c[hm]
                    elif n.endswith('gloves'):
                        g = c[..., 3] > 0
                        near = np.zeros_like(g)
                        for yy, xx in zip(ys, xs): near[max(0, yy - 4):yy + 5, max(0, xx - 4):xx + 5] = True
                        blob = g & near; px = c[blob]
                    else: continue
                    px = [tuple(int(v) for v in p[:3]) for p in px if p[3] and tuple(int(v) for v in p[:3]) != (0, 0, 0)]
                    if not px: continue
                    if n.endswith('gloves'):   # leather only (the cuff is not part of the swinging fist)
                        from build_gloves import GLOVES
                        gl = [tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) for h in GLOVES[n]['glove']]
                        mid, light = gl[1], gl[0]
                    else:
                        lum = sorted(set(px), key=lambda q: -sum(q)); mid = max(set(px), key=px.count); light = lum[0]
                    # each look's band follows its own fist: the centre and size of that layer's fist (the glove is
                    # bigger than the hand), so the trail is the fist stretched along its path, not a band off the wrist
                    by_, bx_ = np.nonzero(blob)
                    cols[n] = (mid, light, len(px), bx_.mean(), by_.mean(), math.sqrt(blob.sum() / math.pi))
                path[dn].append((len(path[dn]), xs.mean(), ys.mean(), cols, (ys.max() - ys.min() + 1) / 2))
    for tag in tags:
        shutil.rmtree(ANIM / tag, ignore_errors=True); (ANIM / f'{tag}.json').unlink(missing_ok=True)
        (hand_masks.MASKS / f'{tag}.npz').unlink(missing_ok=True)
    for di, dn in enumerate(rows):
        pts = path.get(dn)
        if not pts or len(pts) < 2: continue
        y0, x0 = di * F, k * F
        cur = np.zeros((F, F), bool)
        # a near fist swings in front of the body: its trail may cross torso and head, stopping only at what is drawn
        # in front of the body (the arm itself, gloves, armbands); a far fist's trail stays outside the figure
        # the band reaches the fist itself: it may cover the swinging forearm (it is blurred in the swing), only the
        # fist (its glove, or the bare hand from the frame's hand mask) stays on top
        for n, a in sheets.items():
            if side == 'far' or n.endswith('gloves'): cur |= a[y0:y0 + F, x0:x0 + F, 3] > 0
        hmk = hand_masks.MASKS / f'{state}.npz'
        if hmk.exists() and side == 'near':
            mk = np.load(hmk)[lay]
            if mk.shape[1] > x0:   # mask of the original sheet (column k is the same frame when trailing onto it)
                hand = (mk[y0:y0 + F, x0:x0 + F] >= 0) & (mk[y0:y0 + F, x0:x0 + F] <= 4)
                for dy, dx in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): cur |= np.roll(np.roll(hand, dy, 0), dx, 1)
        n_ = len(pts)
        for n in list(sheets):
            if n.endswith('trail') or not any(n in p[3] for p in pts): continue
            grow = 0.5 if n.endswith('gloves') else 0
            acc = np.zeros((F, F, 4), np.uint8); tmap = np.full((F, F), -1.0)
            # dense samples along the polyline; the ribbon reaches the in-between fist (last point)
            for i in range(n_ - 1):
                (_, ax, ay, ac, ah), (_, bx, by, bc, bh) = pts[i], pts[i + 1]
                cols = bc.get(n) or ac.get(n)
                if not cols or n not in ac or n not in bc: continue
                mid, light = cols[0], cols[1]
                ax, ay, ah = ac[n][3], ac[n][4], ac[n][5]; bx, by, bh = bc[n][3], bc[n][4], bc[n][5]
                for u in np.linspace(0, 1, 12, endpoint=False):
                    tg = (i + u) / (n_ - 1)
                    cx, cy = ax + (bx - ax) * u, ay + (by - ay) * u
                    hw = 0.5 + (ah + (bh - ah) * u - 0.5) * tg ** 0.8
                    for yy in range(int(cy - hw - 1), int(cy + hw + 2)):
                        for xx in range(int(cx - hw - 1), int(cx + hw + 2)):
                            if not (0 <= xx < F and 0 <= yy < F): continue
                            dd = math.hypot(xx - cx, yy - cy)
                            if dd > hw: continue
                            if tg >= tmap[yy, xx]:
                                tmap[yy, xx] = tg
                                acc[yy, xx, :3] = light if (yy < cy - hw * 0.35) else mid
                                acc[yy, xx, 3] = 255
            dith = (tmap >= 0) & (tmap < solid) & ((np.add.outer(np.arange(F), np.arange(F)) % 2) == 1)
            acc[dith] = 0
            body = acc[..., 3] > 0
            outl = np.zeros((F, F), bool)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                sh_ = np.roll(np.roll(body, dy, 0), dx, 1)
                outl |= sh_ & ~body & ~cur
            # the trail goes on its own sheet per look ('trail' = bare fist, '<glove>-trail'), drawn above the head items
            # (hair, mongkol, headgear), since a near fist passes in front of the head; the testbed draws the one that
            # matches the equipped gloves
            tn = 'trail' if n == lay else f'{n}-trail'
            if tn not in sheets:
                sheets[tn] = np.zeros_like(sheets[n]); anim['layers'][tn] = f'{tn}.png'
            tgt = sheets[tn][y0:y0 + F, x0:x0 + F]
            put = body & ~cur & (tgt[..., 3] == 0)
            tgt[put] = acc[put]
            ob = outl & (tmap < 0) & (tgt[..., 3] == 0)
            # outline only around the solid (newer) part, so the dithered tail stays soft
            near_solid = np.zeros((F, F), bool)
            sol = body & (tmap >= solid)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)): near_solid |= np.roll(np.roll(sol, dy, 0), dx, 1)
            ob &= near_solid
            tgt[ob] = (0, 0, 0, 255)
    for n, a in sheets.items(): Image.fromarray(a).save(d / anim['layers'][n])
    (d / 'animation.json').write_text(json.dumps(anim, indent=2))
    print(state, 'fist trail on', k)

FRONT_LAYERS = ('arms', 'boxing-gloves', 'thai-gloves', 'prajioud')
HAND_LAYERS = ('arms', 'boxing-gloves', 'thai-gloves', 'prajioud')
def thrust(sheets, orig, rows, k, reach=5, length=16, solid=0.7):
    """straight punch (jab, cross, palm): the fist and forearm leave afterimages behind them along the punch line,
    the nearest solid and the farther ones dithered, drawn from each layer's own pixels (gloves, wraps, armbands)"""
    for di, dname in enumerate(rows):
        if dname not in ('E', 'W'): continue
        sgn = 1 if dname == 'E' else -1
        y0, x0 = di * F, k * F
        cur = np.zeros((F, F), bool)
        for n, a in orig.items(): cur |= a[y0:y0 + F, x0:x0 + F, 3] > 0
        # the punching fist is the frontmost part of the silhouette at arm height (a far-arm punch sits on the body
        # layer, a near one on the arms layer)
        band = cur.copy(); band[34:] = False; band[:14] = False
        xs = np.where(band.any(0))[0]
        if not len(xs): continue
        front = xs.max() if sgn > 0 else xs.min()
        lo, hi = (front - reach, front) if sgn > 0 else (front, front + reach)
        ys = np.where(band[:, lo:hi + 1].any(1))[0]
        # comet: the fist's own colours stretched back along the punch line from its back edge, tapering to a point,
        # the tail dithered; drawn over the forearm and past it (each layer from its own fist pixels: glove, wrap,
        # skin), then neutral white speed lines above and below (effects rule: white/neutral)
        fy0, fy1 = int(ys.min()), int(ys.max()); h = fy1 - fy0 + 1; cy = (fy0 + fy1) / 2
        back = lo if sgn > 0 else hi
        for n in sheets:
            src = orig[n][y0:y0 + F, x0:x0 + F]; tgt = sheets[n][y0:y0 + F, x0:x0 + F]
            # per row, the fist's colour one column in from its back edge (skip outline)
            rowc = {}
            for y in range(fy0, fy1 + 1):
                xs_ = [x for x in range(lo, hi + 1) if src[y, x, 3] > 0 and int(src[y, x, :3].astype(int).sum()) > 0]
                if xs_: rowc[y] = src[y, sorted(xs_, key=lambda x: sgn * x)[min(1, len(xs_) - 1)]].copy()
            if not rowc: continue
            for dd in range(1, length + 1):
                half = (h / 2 + 0.5) * (1 - (dd / (length + 1)) ** 2.5)   # stays full-width, tapers late (exaggerated)
                X = back - sgn * dd
                if not (0 <= X < F): break
                for y, c in rowc.items():
                    if abs(y - cy) > half: continue
                    if dd > length * solid and (X + y) % 2: continue
                    if tgt[y, X, 3] and not cur[y, X]: continue
                    tgt[y, X] = c
        wl = 'body'   # neutral lines go on the body layer, which every outfit draws
        tgt = sheets[wl][y0:y0 + F, x0:x0 + F]
        for y, ln in ((fy0 - 2, length + 4), (fy0 - 4, length - 4), (fy1 + 2, length + 2), (fy1 + 4, length - 6)):
            if not (0 <= y < F): continue
            for i in range(ln):
                X = back - sgn * (2 + i)
                if not (0 <= X < F) or cur[y, X] or tgt[y, X, 3]: continue
                if i >= ln // 2 and (X + y) % 2: continue
                tgt[y, X] = (255, 255, 255, 255) if i < ln // 2 else (0xe3, 0xe3, 0xe3, 255)

def insert_smear(state, k, limbs, t=0.55, swing=False):
    """Insert a smear in-between frame before impact frame k (Christopher 2026-11-17: the impact frames have no smear).
    E/W: the limb at an in-between pose (rendered through the rig, every layer) with the exaggerated fist streak
    behind it; S/N: a copy of frame k-1 for now. Every layer sheet gains a column; animation.json frames, columns,
    rootMotion, clips and events shift."""
    spec = json.loads((ANIM / f'{state}.json').read_text())
    d = ANIM / state; anim = layers_of(d); rows = anim['sheetLayout']['rows']; F0 = anim['frames']
    if anim.get('smearFrames') and any(sf['before'] == k for sf in anim['smearFrames']): raise SystemExit('already inserted')
    tag = f'zzSmearIns{state}'
    (ANIM / f'{tag}.json').write_text(json.dumps(temp_spec(spec, k, limbs, t, tag)))
    r = subprocess.run(['node', 'tools/character-posed.mjs', 'male', tag], cwd=ROOT, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-800:])
    sheets_names = list(anim['layers'])
    if any(n.endswith('gloves') for n in sheets_names):
        sys.path.insert(0, str(ROOT / 'tools/fight-gear'))
        import hand_masks, glove_states
        hand_masks.run(tag); glove_states.run(ANIM / tag)
    td = ANIM / tag; ta = layers_of(td)
    new = {}
    for n, f in anim['layers'].items():
        if not (d / f).exists(): continue
        a = np.array(Image.open(d / f).convert('RGBA'))
        col = a[:, (k - 1) * F:k * F].copy()
        tf = ta['layers'].get(n)
        tmp = np.array(Image.open(td / tf).convert('RGBA'))[:, (k - 1) * F:k * F] if tf and (td / tf).exists() else np.zeros_like(col)
        for di, dn in enumerate(rows):
            if dn in ('E', 'W'): col[di * F:(di + 1) * F] = tmp[di * F:(di + 1) * F]
        new[n] = np.concatenate([a[:, :k * F], col, a[:, k * F:]], axis=1)
    orig = {n: a.copy() for n, a in new.items()}
    if any(l.startswith('arm') for l in limbs) and not swing: thrust(new, orig, rows, k)   # legs get the sweep (run) on the inserted frame
    for n, a in new.items(): Image.fromarray(a).save(d / anim['layers'][n])
    # animation.json
    sh = lambda i: i + 1 if i >= k else i
    anim['frames'] = F0 + 1
    anim['sheetLayout']['columns'] = f'frames 0\u2013{F0}'.encode().decode('unicode_escape')
    for dn, rm in anim.get('rootMotion', {}).items(): rm.insert(k, [0, 0])
    for name, c in anim.get('clips', {}).items():
        if isinstance(c, dict) and 'frames' in c:
            fr = [sh(i) for i in c['frames']]
            if k + 1 in fr: fr.insert(fr.index(k + 1), k)   # the clip holding the (shifted) impact frame gets the smear just before it
            c['frames'] = fr
    for dn, evs in anim.get('events', {}).items():
        if not isinstance(evs, list): continue
        clip = next((e.get('clip') for e in evs if e['frame'] == k), None)
        for e in evs: e['frame'] = sh(e['frame'])
        evs.insert(next(i for i, e in enumerate(evs) if e['frame'] == k + 1), {'frame': k, 'clip': clip, 'type': 'startup', 'smear': True})
    anim.setdefault('smearFrames', []).append({'before': k, 'frame': k, 'limbs': limbs, 'rule': 'smear in-between inserted before the impact frame (tools/smear.py --insert)'})
    (d / 'animation.json').write_text(json.dumps(anim, indent=2))
    shutil.rmtree(td, ignore_errors=True); (ANIM / f'{tag}.json').unlink(missing_ok=True)
    for p_ in (ROOT / '.git/fight-gear-hand-masks').glob(f'{tag}*'): p_.unlink()
    print(state, 'smear frame inserted before', k)

SPARK = [  # impact fx stages (white / light grey, grey rim for contrast; effects rule): a star on the contact, then a burst
    ["....g....",
     "..g.w.g..",
     "...gwg...",
     ".g.wWw.g.",
     "gwwWWWwwg",
     ".g.wWw.g.",
     "...gwg...",
     "..g.w.g..",
     "....g...."],
    [".....w.....",
     ".a...a...a.",
     "..a.....a..",
     "...........",
     "...........",
     "wa.......aw",
     "...........",
     "...........",
     "..a.....a..",
     ".a...a...a.",
     ".....w....."]]
def half_pop(stage):
    """Half pop (Christopher 2026-11-17: an edge-on shock ring at the contact with rays fanning forward, white/neutral;
    then "less visible, not transparent, just less dense"): offsets (dx forward of the contact, dy) -> colour key.
    Every pixel is opaque; density comes from gaps: a broken ring (only its arcs above and below the contact and its
    front tip), single-pixel rays with a gap, a 3 px flash. Stage 0 on the impact frame, stage 1 (ring opened, rays
    flown out) on the held copy."""
    out = {}
    def put(x, y, c):
        q = (int(round(x)), int(round(y)))
        if out.get(q) != 'W': out[q] = c
    ox, rx, ry = ((1, 1.0, 3.0), (1, 1.5, 4.5))[stage]
    for i in range(96):
        t = 2 * np.pi * i / 96; ct, st = np.cos(t), np.sin(t)
        if ct < -0.2 or (abs(st) < 0.75 and ct < 0.9): continue   # keep the upper/lower arcs and the front tip
        put(ox + rx * ct, ry * st, 'W' if ct > 0.5 else 'a')
    rays = ((-55, 3), (0, 4), (55, 3)) if stage == 0 else ((-60, 4), (-25, 5), (0, 6), (25, 5), (60, 4))
    r0 = 2 if stage == 0 else 3
    for ang, ln in rays:
        t = np.radians(ang)
        for j in range(ln):
            if stage == 1 and j == 1: continue   # a gap: the ray breaks off the contact
            r = r0 + j; f = j / max(1, ln - 1)
            put(r * np.cos(t), r * np.sin(t), 'W' if f < 0.5 else ('a' if f < 0.9 else 'g'))
    if stage == 0:
        for q in ((0, 0), (0, -1), (0, 1)): out[q] = 'W'   # flash on the contact
    return out

SPARK_C = {'W': (255, 255, 255, 255), 'w': (255, 255, 255, 255), 'a': (0xe3, 0xe3, 0xe3, 255), 'g': (0xa8, 0xa8, 0xb4, 255)}

def impact_hold(state, k):
    """Rule (Christopher 2026-11-17): the impact frame lasts longer and shows impact fx. The impact column is
    duplicated (held for two ticks); the fx layer gets a hit spark at the contact point: a tight star on the impact
    frame, a burst of rays on the held copy. Contact = the frontmost silhouette pixel inside the event hitbox rows."""
    d = ANIM / state; anim = layers_of(d); rows = anim['sheetLayout']['rows']; F0 = anim['frames']
    sheets = {n: np.array(Image.open(d / f).convert('RGBA')) for n, f in anim['layers'].items() if (d / f).exists()}
    H = sheets['body'].shape[0]
    for n, a in list(sheets.items()):
        sheets[n] = np.concatenate([a[:, :(k + 1) * F], a[:, k * F:(k + 1) * F], a[:, (k + 1) * F:]], axis=1)
    for di, dn in enumerate(rows):
        evs = anim['events'].get(dn) if isinstance(anim.get('events'), dict) else None
        ev = next((e for e in (evs or []) if e['frame'] == k and e.get('hitbox')), None)
        if not ev: continue
        hx_, hy, hw, hh = ev['hitbox']
        y0 = di * F
        cur = np.zeros((F, F), bool)
        for n, a in sheets.items():
            if n != 'fx': cur |= a[y0:y0 + F, k * F:(k + 1) * F, 3] > 0
        east = hx_ >= 32
        # contact = the striking fist/foot itself, measured on the bare figure (body + arms, no gear): its front is the
        # frontmost pixel in the hitbox rows, its centreline the middle of its rows (outline included) within 3 px of
        # that front, kept at half-pixel precision (Christopher 2026-11-17: centre the pop on the fist's centreline).
        # Gloves stand proud of the fist: their extra reach per glove layer is recorded so the pop touches the glove.
        def front(names):
            m = np.zeros((F, F), bool)
            for n in names:
                if n in sheets: m |= sheets[n][y0:y0 + F, k * F:(k + 1) * F, 3] > 0
            xs = np.where(m[hy:hy + hh].any(0))[0]
            return (m, int(xs.max()) if east else int(xs.min())) if len(xs) else (m, None)
        bare, fx_ = front(('body', 'arms'))
        if fx_ is None: continue
        # the fist's rows: the unbroken run of rows near the front that holds the frontmost hitbox pixel (the hitbox
        # rows may cut the fist, so the run is followed past them)
        near = (bare[:, max(0, fx_ - 3):fx_ + 1] if east else bare[:, fx_:fx_ + 4]).any(1)
        seed = hy + int(np.where(bare[hy:hy + hh, fx_])[0][0])
        top = bot = seed
        while top > 0 and near[top - 1]: top -= 1
        while bot < F - 1 and near[bot + 1]: bot += 1
        cy = (top + bot) / 2
        reach = {}
        for g in [n for n in sheets if n.endswith('gloves')]:
            _, gx = front(('body', 'arms', g))
            if gx is not None and gx != fx_: reach[g] = abs(gx - fx_)
        rec = {'dir': dn, 'frame': k, 'held': k + 1, 'x': fx_ + (1 if east else -1), 'y': float(cy), 'facing': 1 if east else -1, 'style': 'halfPop'}
        if reach: rec['gearReach'] = reach
        anim.setdefault('impactFx', []).append(rec)
    for n, a in sheets.items(): Image.fromarray(a).save(d / anim['layers'][n])
    sh = lambda i: i + 1 if i > k else i
    anim['frames'] = F0 + 1
    anim['sheetLayout']['columns'] = 'frames 0\u2013%d' % F0
    anim['sheetLayout']['columns'] = anim['sheetLayout']['columns'].encode().decode('unicode_escape')
    for dn, rm in anim.get('rootMotion', {}).items(): rm.insert(k + 1, [0, 0])
    for rec in anim.get('impactFx', []) + anim.get('impactHolds', []):   # records of later impacts move with the insert
        if rec['frame'] > k: rec['frame'] += 1; rec['held'] += 1
    for name, c in anim.get('clips', {}).items():
        if isinstance(c, dict) and 'frames' in c:
            fr = [sh(i) for i in c['frames']]
            if k in fr: fr.insert(fr.index(k) + 1, k + 1)
            c['frames'] = fr
    for dn, evs in anim.get('events', {}).items():
        if not isinstance(evs, list): continue
        e0 = next((e for e in evs if e['frame'] == k), None)
        for e in evs: e['frame'] = sh(e['frame'])
        if e0: evs.insert(evs.index(e0) + 1, {'frame': k + 1, 'clip': e0.get('clip'), 'type': 'impactHold'})
    anim.setdefault('impactHolds', []).append({'frame': k, 'held': k + 1, 'rule': 'impact frame held one extra tick with impact fx (tools/smear.py --impact)'})
    (d / 'animation.json').write_text(json.dumps(anim, indent=2))
    print(state, 'impact held + fx at', k)

def layers_of(d):
    return json.loads((d / 'animation.json').read_text())

def run(state, jobs, steps=tuple(round(0.1 * i, 2) for i in range(1, 10))):
    spec = json.loads((ANIM / f'{state}.json').read_text())
    d = ANIM / state; anim = layers_of(d); rows = anim['sheetLayout']['rows']
    sheets = {n: np.array(Image.open(d / f).convert('RGBA')) for n, f in anim['layers'].items() if (d / f).exists()}
    orig = {n: a.copy() for n, a in sheets.items()}
    tmp_dirs = []
    for k, limbs in jobs:
        if limbs[0] == 'thrust':
            thrust(sheets, orig, rows, k); continue
        smear = {n: [] for n in sheets}
        for i, t in enumerate(steps):
            tag = f'zzSmear{i}{state}'
            (ANIM / f'{tag}.json').write_text(json.dumps(temp_spec(spec, k, limbs, t, tag)))
            r = subprocess.run(['node', 'tools/character-posed.mjs', 'male', tag], cwd=ROOT, capture_output=True, text=True)
            if r.returncode: raise SystemExit(r.stderr[-800:])
            if any(n.endswith('gloves') for n in sheets):
                sys.path.insert(0, str(ROOT / 'tools/fight-gear'))
                import hand_masks, glove_states
                hand_masks.run(tag); glove_states.run(ANIM / tag)
            td = ANIM / tag; ta = layers_of(td); tmp_dirs.append(tag)
            for n in sheets:
                f = ta['layers'].get(n)
                smear[n].append(np.array(Image.open(td / f).convert('RGBA')) if f and (td / f).exists() else None)
        for di, dname in enumerate(rows):
            if dname not in ('E', 'W'): continue
            col = k if dname == 'E' else k   # W mirrors E frame for frame
            y0, x0 = di * F, col * F
            cur = np.zeros((F, F), bool)
            for n, a in orig.items(): cur |= a[y0:y0 + F, x0:x0 + F, 3] > 0
            prev = {n: orig[n][y0:y0 + F, (k - 1) * F:k * F] for n in orig}
            # a near arm swings in front of the body: its smear may cross the torso and head (arms and glove layers
            # only), stopping only at what is drawn in front of the body in frame k
            near_arm = 'arm-near' in limbs
            front = np.zeros((F, F), bool)
            for n in FRONT_LAYERS:
                if n in orig: front |= orig[n][y0:y0 + F, x0:x0 + F, 3] > 0
            # the smear: per layer, in-between pixels that moved (differ from the real frame k-1) and lie outside the
            # real frame k silhouette; later steps (closer to k) draw over earlier ones
            add = {}; tmap = np.full((F, F), -1.0)
            for n in sheets:
                acc = np.zeros((F, F, 4), np.uint8)
                for s, t in zip(smear[n], steps):
                    if s is None: continue
                    c = s[y0:y0 + F, (k - 1) * F:k * F]
                    moved = (c[..., 3] > 0) & ((c != prev[n]).any(-1))
                    m = moved & ~(front if n in FRONT_LAYERS and near_arm else cur)
                    acc[m] = c[m]; tmap[m] = np.maximum(tmap[m], t)
                add[n] = acc
            # motion blur: the older half of the path (t below DITHER) is dithered (every other pixel), the newer half
            # solid, so the smear fades out behind the limb
            dith = (tmap >= 0) & (tmap < DITHER * max(steps)) & ((np.add.outer(np.arange(F), np.arange(F)) % 2) == 1)
            for n in add: add[n][dith] = 0
            union = np.zeros((F, F), bool)
            for n, acc in add.items(): union |= acc[..., 3] > 0
            # flat smear: black pixels inside the union lose their outline (take a neighbour's colour); the union's outer
            # edge keeps black where it touches empty space
            for n, acc in add.items():
                blk = (acc[..., 3] > 0) & (acc[..., :3].sum(-1) == 0)
                for y, x in zip(*np.where(blk)):
                    edge = any(not (0 <= y + dy < F and 0 <= x + dx < F) or not (union[y + dy, x + dx] or cur[y + dy, x + dx])
                               for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if edge: continue
                    nb = [acc[y + dy, x + dx] for dy, dx in ((0, -1), (0, 1), (-1, 0), (1, 0)) if 0 <= y + dy < F and 0 <= x + dx < F
                          and acc[y + dy, x + dx, 3] > 0 and acc[y + dy, x + dx, :3].sum() > 0]
                    if nb: acc[y, x] = nb[0]
                    else: acc[y, x] = 0
                tgt = sheets[n][y0:y0 + F, x0:x0 + F]
                m = (acc[..., 3] > 0) & (tgt[..., 3] == 0)
                tgt[m] = acc[m]
    for n, a in sheets.items(): Image.fromarray(a).save(d / anim['layers'][n])
    for tag in set(tmp_dirs):
        shutil.rmtree(ANIM / tag, ignore_errors=True); (ANIM / f'{tag}.json').unlink(missing_ok=True)
        for p in (ROOT / '.git/fight-gear-hand-masks').glob(f'{tag}*'): p.unlink()
    print(state, 'smear', jobs)

if __name__ == '__main__' and '--trail' in sys.argv:
    # smear.py <state> --trail k[:far]   (k = the inserted smear frame; run after --insert ... with a :nothrust limb)
    state = sys.argv[1]; j = sys.argv[sys.argv.index('--trail') + 1].split(':')
    fist_trail(state, int(j[0]), j[1] if len(j) > 1 else 'near', onto='onto' in j); sys.exit()
if __name__ == '__main__' and '--impact' in sys.argv:
    state = sys.argv[1]
    for k in sorted((int(x) for x in sys.argv[sys.argv.index('--impact') + 1].split(',')), reverse=True): impact_hold(state, k)
    sys.exit()
if __name__ == '__main__' and '--insert' in sys.argv:
    # smear.py <state> --insert k:limbs[,k2:limbs] (impact frames of the ORIGINAL clip; inserted from the last back)
    state = sys.argv[1]; jobs = sys.argv[sys.argv.index('--insert') + 1].split(',')
    for j in sorted(jobs, key=lambda j: -int(j.split(':')[0])):
        k, l, *t = j.split(':'); insert_smear(state, int(k), l.split('+'), *(float(x) for x in t), swing='--swing' in sys.argv)   # k:limbs[:t]
    sys.exit()
if __name__ == '__main__':
    state = sys.argv[1]; jobs = []
    for j in sys.argv[2].split(','):
        k, l, *opt = j.split(':'); jobs.append((int(k), l.split('+')))
        if 'long' in opt: LONG = True
    if '--steps' in sys.argv: run(state, jobs, tuple(float(x) for x in sys.argv[sys.argv.index('--steps') + 1].split(',')))
    else: run(state, jobs)
