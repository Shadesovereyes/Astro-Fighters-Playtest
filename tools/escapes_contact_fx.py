"""Contact-point fx for the submission escapes (Christopher 2026-11-26 19:14: "the fx seem random and don't illustrate
what's happening"). One fx language, drawn ONLY at the hand-to-wrist contact point, measured per frame from the holder's
rendered arms layer (forward-most hand pixels), drawn over both fighters (fx.top):
  Submission Struggle (technique): a white grip ring pulses on each tug, growing with the effort (r7 < r9 < r11).
  Muscle Out Escape (force): the same grip ring on each heave, larger (r9/r11) and jittered 1px (arcs read as noise on the gi).
  Impact frame 9: hit star at the contact (success) / a small ring as the grip re-sinks (fail).
No other fx (no strain dots, sweat, leg, hip or chevron marks); the bodies carry the rest.
usage: python3 -I escapes_contact_fx.py <holderState> <style ring|vibe> <ok 1|0>   (then re-render the holder state)"""
import json, sys, os
from PIL import Image
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
st, style, ok = sys.argv[1], sys.argv[2], sys.argv[3] == '1'
EFFORT = {'ring': {2: 1, 5: 2, 7: 3, 8: 2}, 'vibe': {3: 2, 6: 3, 7: 2, 8: 3}}
RING = {1: ['..###..', '.#WWW#.', '#W...W#', '#W...W#', '#W...W#', '.#WWW#.', '..###..'],
        2: ['...###...', '..#WWW#..', '.#W...W#.', '#W.....W#', '#W.....W#', '#W.....W#', '.#W...W#.', '..#WWW#..', '...###...'],
        3: ['....###....', '..##WWW##..', '.#WW...WW#.', '.#W.....W#.', '#W.......W#', '#W.......W#', '#W.......W#', '.#W.....W#.', '.#WW...WW#.', '..##WWW##..', '....###....']}
ARC = ['.#W', '#W.', '#W.', '#W.', '.#W']
STAR = ['..#..', '#.#.#', '.#W#.', '#.#.#', '..#..']
s = json.load(open(D + st + '.json'))
arms = Image.open(os.path.join(D, st, 'arms.png')).convert('RGBA')
row = s['directions'].index('E')
def contact(k):
    px = arms.load(); pts = [(x, y) for y in range(64) for x in range(64) if px[k * 64 + x, row * 64 + y][3] > 0]
    # choke: the hands are the lowest-forward point (at the neck); arm bar: the forward-most point (on the wrist)
    sc = (lambda p: p[0] + p[1]) if 'Choke' in st else (lambda p: p[0])
    m = max(sc(p) for p in pts); near = [p for p in pts if sc(p) >= m - 2]
    return round(sum(p[0] for p in near) / len(near)) - 1, round(sum(p[1] for p in near) / len(near))
import math
def _grid(R, pts):
    n = 2 * R + 1; g = [['.'] * n for _ in range(n)]
    for x, y in pts:
        if 0 <= x < n and 0 <= y < n: g[y][x] = 'W'
    for y in range(n):                               # 1px black outline around the white pixels
        for x in range(n):
            if g[y][x] == '.' and any(0 <= x + dx < n and 0 <= y + dy < n and g[y + dy][x + dx] == 'W' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = '#'
    return [''.join(r) for r in g]
def _arc(cx, cy, r, a0, a1, step=4):
    return {(round(cx + r * math.cos(math.radians(a))), round(cy + r * math.sin(math.radians(a)))) for a in range(a0, a1, step)}
GAPS = [(15, 45), (105, 132), (195, 228), (285, 312)]   # where the ring cracks
def _cracked(R=6, r=4):
    keep = set()
    for i in range(len(GAPS)):
        a0 = GAPS[i][1]; a1 = GAPS[(i + 1) % len(GAPS)][0] + (360 if i == len(GAPS) - 1 else 0)
        keep |= _arc(R, R, r, a0, a1)
    for a0, a1 in GAPS:                              # crack lines poke out of each break
        m = math.radians((a0 + a1) / 2); keep |= {(round(R + (r + 1) * math.cos(m)), round(R + (r + 1) * math.sin(m)))}
    return _grid(R, keep)
def _shards(R, rad, n, span):
    """n ring fragments flung outward to radius rad, each an arc of +-span degrees (0 = single pixel)"""
    pts = set()
    for i in range(n):
        m = i * 360 / n + 22
        pts |= _arc(R, R, rad, int(m - span), int(m + span) + 1, 3) if span else _arc(R, R, rad, int(m), int(m) + 1)
    return _grid(R, pts)
def _split(shift):
    # the full r11 grip ring split into 4 arcs along its diagonals, each pushed outward by `shift` px
    src = RING[3]; c = 5; pts = set()
    for y, r in enumerate(src):
        for x, ch in enumerate(r):
            if ch != 'W': continue
            dx, dy = x - c, y - c
            if abs(dx) == abs(dy) or abs(abs(dx) - abs(dy)) == 1 and min(abs(dx), abs(dy)) >= 3: continue
            ox, oy = ((0, -1) if dy < 0 else (0, 1)) if abs(dy) > abs(dx) else ((-1, 0) if dx < 0 else (1, 0))
            pts.add((x + 2 + ox * shift, y + 2 + oy * shift))
    return _grid(7, pts)
SHATTER = {'shatter1': _split(2), 'shatter2': _shards(8, 7, 8, 12), 'shatter3': _shards(11, 10, 8, 0)}
pats = {'star': STAR, **SHATTER, 'arcL': ARC, 'arcR': [r[::-1] for r in ARC], **{f'ring{n}': p for n, p in RING.items()}}
frames = []
def put(k, name, cx, cy):
    p = pats[name]; return {'pattern': name, 'at': [cx - len(p[0]) // 2, cy + len(p) // 2]}   # 'at' = bottom-left
for k, n in EFFORT[style].items():
    cx, cy = contact(k)
    if style == 'ring': frames.append({'frame': k, 'splash': [put(k, f'ring{n}', cx, cy)]})
    else: frames.append({'frame': k, 'splash': [put(k, f'ring{n}', cx + (1 if k % 2 else -1), cy)]})   # force: bigger rings, jittered 1px
cx, cy = contact(8)   # the impact lands where the grip was on the last struggle frame
# Christopher 2026-11-27 12:20 ET: success = the ring breaks and shatters; fail = the ring stays whole.
if ok:
    for k, name in ((9, 'shatter1'), (10, 'shatter2'), (11, 'shatter3')):
        frames.append({'frame': k, 'splash': [put(k, name, cx, cy)]})
else:
    for k, n in ((9, 3), (10, 3), (11, 2)):      # holds whole on the grip, then tightens back down as the hold sinks in
        frames.append({'frame': k, 'splash': [put(k, f'ring{n}', *contact(k))]})
s['fx'] = {'rule': __doc__.split('\n')[1].strip() and 'contact-point fx only (2026-11-26 19:14): ' + ('grip ring pulses on each tug' if style == 'ring' else 'vibration arcs at the straining grip on each heave') + '; impact ' + ('hit star' if ok else 'small ring as the grip re-sinks'),
           'top': True, 'frames': frames, 'palette': {'W': '#ffffff', 'w': '#e3e3e3', '#': '#000000'}, 'patterns': pats}
json.dump(s, open(D + st + '.json', 'w'), indent=2); open(D + st + '.json', 'a').write('\n')
print(st, [(f['frame'], f['splash'][0]['pattern'], f['splash'][0]['at']) for f in frames])
