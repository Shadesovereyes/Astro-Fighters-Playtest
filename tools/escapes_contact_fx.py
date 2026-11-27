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
pats = {'star': STAR, 'arcL': ARC, 'arcR': [r[::-1] for r in ARC], **{f'ring{n}': p for n, p in RING.items()}}
frames = []
def put(k, name, cx, cy):
    p = pats[name]; return {'pattern': name, 'at': [cx - len(p[0]) // 2, cy + len(p) // 2]}   # 'at' = bottom-left
for k, n in EFFORT[style].items():
    cx, cy = contact(k)
    if style == 'ring': frames.append({'frame': k, 'splash': [put(k, f'ring{n}', cx, cy)]})
    else: frames.append({'frame': k, 'splash': [put(k, f'ring{n}', cx + (1 if k % 2 else -1), cy)]})   # force: bigger rings, jittered 1px
cx, cy = contact(8)   # the impact lands where the grip was on the last struggle frame
frames.append({'frame': 9, 'splash': [put(9, 'star' if ok else 'ring1', cx, cy)]})
s['fx'] = {'rule': __doc__.split('\n')[1].strip() and 'contact-point fx only (2026-11-26 19:14): ' + ('grip ring pulses on each tug' if style == 'ring' else 'vibration arcs at the straining grip on each heave') + '; impact ' + ('hit star' if ok else 'small ring as the grip re-sinks'),
           'top': True, 'frames': frames, 'palette': {'W': '#ffffff', 'w': '#e3e3e3', '#': '#000000'}, 'patterns': pats}
json.dump(s, open(D + st + '.json', 'w'), indent=2); open(D + st + '.json', 'a').write('\n')
print(st, [(f['frame'], f['splash'][0]['pattern'], f['splash'][0]['at']) for f in frames])
