"""Draw the fight-gear gloves onto rendered male states from the state's own fists (candidates 2026-11-15).

Fists are posed differently in every clip (band arms, frontal arms, the far arm drawn on body.png), so the gloves are
found from the rendered pixels instead of carried by the rig: each wrist wrap (white run) splits its arm into a
forearm and a hand; the small skin piece beyond the wrap is the fist. The fist becomes the glove (padded outward by
the glove's grow and re-outlined), the wrap becomes the cuff. The near arm (arms.png) is drawn over a far glove
(found on body.png). Band-arm fists come exactly from tools/fight-gear/hand_masks.py when its masks exist
(the heuristic mistook a raised fist for a forearm in muayThaiElbow S). Writes <glove>.png into each state and lists it in animation.json.
Usage: python3 tools/fight-gear/glove_states.py <state dir> [...]
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from build_gloves import GLOVES, SKIN, hx

F = 64
WRAPC = {(255, 255, 255), (227, 227, 227), (173, 173, 173)}
BLACK = (0, 0, 0)
N8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
N4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def comps(points):
    pts, seen, out = set(points), set(), []
    for p in points:
        if p in seen: continue
        c, st = [], [p]; seen.add(p)
        while st:
            x, y = st.pop(); c.append((x, y))
            for dx, dy in N8:
                q = (x + dx, y + dy)
                if q in pts and q not in seen: seen.add(q); st.append(q)
        out.append(c)
    return out

def split_by_axis(wc, arm):
    """The wrap does not cut the arm in two (it shows on one edge only): split the arm across its own axis at the
    wrap; the side that ends within a few px of the wrap is the hand."""
    cx = sum(x for x, _ in wc) / len(wc); cy = sum(y for _, y in wc) / len(wc)
    near = [(x, y) for (x, y) in arm if (x - cx) ** 2 + (y - cy) ** 2 <= 64] + list(wc)
    mx = sum(x for x, _ in near) / len(near); my = sum(y for _, y in near) / len(near)
    sxx = sum((x - mx) ** 2 for x, _ in near); syy = sum((y - my) ** 2 for _, y in near); sxy = sum((x - mx) * (y - my) for x, y in near)
    ang = 0.5 * np.arctan2(2 * sxy, sxx - syy); ux, uy = np.cos(ang), np.sin(ang)
    pr = lambda p: (p[0] - cx) * ux + (p[1] - cy) * uy
    pe = lambda p: abs(-(p[0] - cx) * uy + (p[1] - cy) * ux)
    wp = [pr(p) for p in wc]; lo, hi = min(wp), max(wp)
    plus = [p for p in arm if pr(p) > hi]; minus = [p for p in arm if pr(p) < lo]
    far_plus = sum(1 for p in plus if pr(p) > hi + 6); far_minus = sum(1 for p in minus if pr(p) < lo - 6)
    if far_plus == far_minus: return None
    side = minus if far_plus > far_minus else plus
    edge = lo if far_plus > far_minus else hi
    hand = {p for p in side if abs(pr(p) - edge) <= 5.5 and pe(p) <= 3.5}
    return hand if 4 <= len(hand) <= 26 else None

def masked_fists(img, mask, fx, fy):
    """Fists known exactly from hand_masks.py: mask 0-4 = hand (skin tone), 5-6 = wrist wrap (glove cuff). Every
    visible wrist wrap becomes cuff, even when its fist is hidden, so a bare wrap never shows under a glove."""
    px = {}
    for y in range(F):
        for x in range(F):
            a = img[fy + y, fx + x]
            if a[3]: px[(x, y)] = tuple(int(v) for v in a[:3])
    cell = lambda x, y: int(mask[fy + y, fx + x])
    hand = [(x, y) for (x, y) in px if 0 <= cell(x, y) <= 4]
    cuffs = {(x, y) for (x, y) in px if cell(x, y) >= 5}
    out = []
    for hc in comps(hand):
        hs = set(hc)
        outl = {(x + dx, y + dy) for (x, y) in hs for dx, dy in N8 if px.get((x + dx, y + dy)) == BLACK}
        out.append((hs, outl, set(), px, {p: cell(*p) for p in hs}))
    if cuffs:
        out.append((set(), set(), cuffs, {p: ((255, 255, 255) if cell(*p) == 5 else (227, 227, 227)) for p in cuffs}, {}))
    return out

def fists(img, fx, fy, body=False):
    """[(hand pixels, outline pixels, cuff pixels)] for one frame cell."""
    px = {}
    for y in range(F):
        for x in range(F):
            a = img[fy + y, fx + x]
            if a[3]: px[(x, y)] = tuple(int(v) for v in a[:3])
    wrap = [p for p, c in px.items() if c in WRAPC]
    skin = [p for p, c in px.items() if c not in WRAPC and c != BLACK]
    scomp = comps(skin); owner = {}
    for i, c in enumerate(scomp):
        for p in c: owner[p] = i
    out = []
    for wc in comps(wrap):
        if body and (len(wc) > 14 or min(y for _, y in wc) >= 46): continue      # briefs / ankle wraps
        # skin pieces touching the wrap, or separated from it only by an outline row (the fist's own outline)
        adj = {owner[(x + dx, y + dy)] for (x, y) in wc for dx, dy in N8 if (x + dx, y + dy) in owner}
        adj |= {owner[(x + 2 * dx, y + 2 * dy)] for (x, y) in wc for dx, dy in N8
                if px.get((x + dx, y + dy)) == BLACK and (x + 2 * dx, y + 2 * dy) in owner}
        if not adj: continue
        sizes = sorted((len(scomp[i]), i) for i in adj)
        n, i = sizes[0]
        if n > 26 or (len(sizes) == 1 and n > 16):
            if body: continue
            hand = split_by_axis(wc, set().union(*(scomp[j] for j in adj)))
            if not hand: continue
        else:
            hand = set(scomp[i])
        outl = {(x + dx, y + dy) for (x, y) in hand for dx, dy in N8 if px.get((x + dx, y + dy)) == BLACK}
        out.append((hand, outl, set(wc), px))
    return out

def align_to_cuff(glove_px, hand, cuffs):
    """A straight (horizontal) forearm ends in a vertical wrap stripe: the glove is centred on that stripe's rows, so
    it sits on the forearm's line instead of following the band hand's raised knuckles (Christopher 2026-11-17: the
    cross glove looked rotated upward, not aligned with the forearm). Returns the row shift (0 when not straight)."""
    near = {q for q in cuffs if any(abs(q[0] - x) + abs(q[1] - y) <= 2 for (x, y) in hand)}
    if len(near) < 3: return 0
    xs = [x for x, _ in near]; ys = [y for _, y in near]
    if max(xs) - min(xs) > 2 or max(ys) - min(ys) < 2: return 0
    gy = [y for _, y in glove_px]
    dy = round((min(ys) + max(ys)) / 2 - (min(gy) + max(gy)) / 2)
    return dy if abs(dy) <= 2 else 0

def paint(layer, fx, fy, found, g, mask=None):
    H = W = F
    cell = {}
    allcuff = set().union(*[item[2] for item in found]) if found else set()
    for item in found:
        hand, outl, cuff, px = item[:4]
        tone = item[4] if len(item) > 4 else None
        for p in hand: cell[p] = hx(g['glove'][min(3, tone[p])] if tone else g['glove'][SKIN.get('%02x%02x%02x' % px[p], 1)])
        for p in cuff: cell[p] = hx(g['cuff'][0 if px[p] == (255, 255, 255) else 1])
        for p in outl:
            if p not in cell: cell[p] = hx('000000')
        glove = set(hand)
        # swell: outline touching the leather becomes leather, g['grow'] times
        for _ in range(g['grow']):
            ring = {(x + dx, y + dy) for (x, y) in glove for dx, dy in N4}
            for q in ring - glove - cuff:
                if 0 <= q[0] < W and 0 <= q[1] < H:
                    cell[q] = hx(g['glove'][2]); glove.add(q)
        dy = align_to_cuff(glove, hand, allcuff) if hand else 0
        if dy:
            moved = {(x, y + dy): cell[(x, y)] for (x, y) in glove if (x, y) in cell}
            for q in glove | {q for q in outl if q in cell and not cell[q][:3].any()}: cell.pop(q, None)
            glove = {q for q in moved if 0 <= q[1] < H}
            cell.update({q: c for q, c in moved.items() if 0 <= q[1] < H})
        # fresh outline round leather and cuff
        for (x, y) in list(glove | cuff):
            for dx, dy in N4:
                q = (x + dx, y + dy)
                if 0 <= q[0] < W and 0 <= q[1] < H and q not in cell: cell[q] = hx('000000')
        # a 1px knuckle highlight on the leather's top-front pixel row
    for (x, y), c in cell.items():
        if mask is not None and mask[fy + y, fx + x, 3]: continue
        layer[fy + y, fx + x] = c

def run(d):
    d = Path(d)
    anim = json.loads((d / 'animation.json').read_text())
    arms = np.array(Image.open(d / anim['layers']['arms']).convert('RGBA'))
    body = np.array(Image.open(d / anim['layers']['body']).convert('RGBA'))
    H, W = arms.shape[:2]
    mp = Path(__file__).resolve().parents[2] / '.git/fight-gear-hand-masks' / f'{d.name}.npz'
    masks = dict(np.load(mp)) if mp.exists() else {}
    # Far hands (drawn on body.png, behind the torso) get their own '<glove>-far' sheet, which the game draws between
    # the body and the clothing, so shorts, trunks, the Gi or armour hide a far glove the way they hide the far hand;
    # near hands (arms.png) stay on '<glove>' above the arms.
    for name, g in GLOVES.items():
        layers = {'body': np.zeros_like(arms), 'arms': np.zeros_like(arms)}
        for fy in range(0, H, F):
            for fx in range(0, W, F):
                for img, key, m in ((body, 'body', arms), (arms, 'arms', None)):
                    mk = masks.get(key)
                    exact = masked_fists(img, mk, fx, fy) if mk is not None else None   # masks mark every hand the renderer drew
                    paint(layers[key], fx, fy, exact if exact is not None else fists(img, fx, fy, body=(key == 'body')), g, mask=m)
        Image.fromarray(layers['arms']).save(d / f'{name}.png')
        Image.fromarray(layers['body']).save(d / f'{name}-far.png')
        anim['layers'][name] = f'{name}.png'
        anim['layers'][f'{name}-far'] = f'{name}-far.png'
    (d / 'animation.json').write_text(json.dumps(anim, indent=2, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    for d in sys.argv[1:]: run(d); print('ok', d)
