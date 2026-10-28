"""Kanabo weapon style (Christopher 2026-10-28: "ironwood kanabo approved create a separate thread for weapon attack
abilities using the kanabo"). Ironwood Kanabo (Taurus ninjutsu) summons the club and unlocks the Kanabo weapon style;
canon (Astro Fighters: Core Systems, Taurus > Ninjutsu > Ironwood Kanabo): "[TB] Summons a temporary Weapon. Changes
'Basic Attack' to 'Club Smash' (Higher Base Dmg + AoE) for 3 turns. [RT] ... Changes melee animations to slow, heavy
swings." Club Smash is the only kanabo attack canon defines.
  kanabo item     the approved Ironwood Kanabo v2 club (astro.py NPAT['kanabo'], after Christopher's reference) as a
                  rigid weapon item: one band segment per pattern row, '.' empty, so spikes stand out of the band
  kanaboGuard     held idle while the club lasts: both fists on the cord grip low in front, the club angled up and
                  forward, a slow heavy breath that dips the head of the club (from and back to this loop)
  kanaboSmash     Club Smash: heave the club up and back overhead, hang, step in and bring it down in one heavy arc into
                  the floor in front; the floor cracks, a ring of dust and stone bursts out round the impact (AoE),
                  hold, heave it back up to the guard
E/W first (W mirrors E); S/N after approval. Arms by two-link IK to the grips (kenjutsu.py): near fist at the top of the
cord grip (pattern row 26, where the cast grips it), far fist 4 px below it.
Run: python3 tools/kanabo.py ; node tools/character-posed.mjs male <state> ; python3 tools/kanabo.py --grips <state> ;
     node tools/character-weapon.mjs male <state> ; python3 tools/kanabo.py --fx <state>"""
import sys, os, copy, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import build, save
from PIL import Image
import kenjutsu as K
K.HILT = 4   # near fist to far fist along the cord grip
from kenjutsu import fr, D, BASE, POSES, grips

R = K.R
STAT = 'CANDIDATE 2026-10-28 (E/W; W mirrors E; S/N to author after approval)'

# the approved club (Ironwood Kanabo v2, astro.py NPAT['kanabo']): rows top (cap) to bottom (ring pommel), columns back
# to front in E; i/j/h iron dark/mid/highlight, u/v cord wrap
CLUB = ['...jjj...', '..jhhij..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', '..ihjji..', '...hji...', '...ijj...', '...jhj...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...jhj...', '..j...j..', '..j...j..', '...jjj...']
GRIP_ROW = 26

def item():
    segs = []
    for r, row in enumerate(CLUB):
        u0 = GRIP_ROW - r - 0.5
        name = 'cap' if r < 2 else 'head' if r < 21 else 'neck' if r < 24 else 'grip' if r < 32 else 'ring'
        segs.append({'name': f'{name}-{r}', 'from': u0, 'to': u0 + 1, 'thickness': 9, 'pattern': [row]})
    it = {'schema': 'astro-fighters-character-item/v1', 'item': 'kanabo',
          'kind': 'rigid weapon (AGENTS.md: rigid items are placed by anchor with integer offsets)',
          'status': 'design approved by user 2026-10-28 (Ironwood Kanabo v2 cast, c58ee3f); weapon layer CANDIDATE 2026-10-28',
          'construction': 'band, one segment per row of the approved Ironwood Kanabo v2 club (astro.py NPAT[\'kanabo\']); \'.\' in a cross-section is empty, so the spike rows stand out of the band; pixels are rasterised from the authored data, never rotated or resampled from an image',
          'palette': {'#': '#000000', 'i': '#24252b', 'j': '#4a4c55', 'h': '#9a9da8', 'u': '#a08a62', 'v': '#6e5c3e'},
          'paletteSource': 'astro.py NPAL: i/j/h kanabo iron (dark, mid, highlight), u/v its cord wrap (as approved in the cast)',
          'units': 'pixels along the axis from the grip point (u, positive toward the cap) and across it (v)',
          'segments': segs,
          'outline': 'every coloured pixel touching empty space gets an outline pixel (#) if it is not already one',
          'grip': 'two-handed: near fist at the top of the cord grip (row 26, where the cast grips it), far fist 4 px below',
          'trail': {'rule': 'swing smear colours, from the outer edge inward: earth dust browns (astro.py ELEMENT e/E) behind a white edge; hard alpha',
                    'bands': [{'to': 1.5, 'colour': '#ffffff'}, {'to': 3.5, 'colour': '#c79a5b'}, {'to': 99, 'colour': '#8a6236'}]}}
    save(it, R + 'production/source/characters/items/kanabo.json')

OVER = {'hilt': 'front', 'blade': 'behind'}   # club raised overhead: the head passes behind the fighter's head
G = dict(grip=(43, 35), angle=68)
SWING = lambda a0: {'from': a0, 'width': 8}
CLIPS = {
 # held idle: a slow heavy breath, the club's weight dipping its head a few degrees as the body settles
 'guard': ('Kanabo Stance', None, None, None, 5, True, [
    fr(**G, bob=(1, 1, 2), lean=(0, 2)),
    fr((43, 35), 66, bob=(1, 1, 2), lean=(0, 2)),
    fr((43, 36), 63, bob=(2, 3, 3), lean=(0, 2), ln='guard-low-rear', lf='guard-low-lead'),
    fr((43, 36), 65, bob=(2, 3, 3), lean=(0, 2), ln='guard-low-rear', lf='guard-low-lead')]),
 # Club Smash (higher damage + AoE; slow, heavy swing)
 'smash': ('Club Smash', 5, [42, 34, 22, 30], 'heavy', 10, False, [
    fr(**G),
    fr((41, 27), 100, bob=(1, 1, 1), lean=(0, 0), z=OVER),
    fr((37, 19), 148, bob=(1, 1, 0), lean=(-1, -2), ln='step-rear', z=OVER),
    fr((36, 18), 158, bob=(1, 1, 0), lean=(-1, -3), ln='step-rear', z=OVER),
    fr((44, 22), 96, bob=(1, 1, 1), lean=(1, 3), root=(2, 0), lf='step-lead', trail=SWING(158), z=OVER),
    fr((45, 37), -58, bob=(4, 4, 4), lean=(2, 6), root=(2, 0), ln='lunge-rear', lf='lunge-lead', trail=SWING(96)),
    fr((45, 37), -58, bob=(4, 4, 4), lean=(2, 6), ln='lunge-rear', lf='lunge-lead'),
    fr((45, 37), -57, bob=(3, 3, 4), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    fr((44, 31), 25, bob=(2, 2, 2), lean=(1, 3), root=(-2, 0), lf='step-lead'),
    fr((43, 33), 52, bob=(1, 1, 2), lean=(0, 2), root=(-2, 0)),
    fr(**G)]),
}
STATES = {'kanaboGuard': 'guard', 'kanaboSmash': 'smash'}
INTENT = {
 'guard': 'Kanabo Stance (held idle while the Ironwood Kanabo lasts; Christopher 2026-10-28: weapon attacks with the approved kanabo): both fists on the cord grip low in front of the belt, the long spiked iron club angled up and forward; a slow heavy breath, the body settling into a lower stance and the weight of the club dipping its head a few degrees, then rising again. Every kanabo attack starts and ends here.',
 'smash': 'Club Smash (canon: Ironwood Kanabo changes the basic attack to Club Smash, higher base damage + AoE; slow, heavy swings): from the kanabo guard the fighter heaves the club up and back over its head (the head of the club passing behind its own), hangs a beat at the top with the weight on the rear leg, then steps in and brings it down in one heavy arc (earth-dust smear) into the floor in front; the floor cracks under the head of the club and a ring of dust and stone bursts out round the impact (the AoE), held two frames as the dust settles, then it heaves the club back up to the guard.',
}

def spec(state, c):
    base = copy.deepcopy(BASE)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    ab, act, hb, dmg, fps, loop, frames = CLIPS[c]
    n = len(frames)
    if loop:
        clips = {'rule': 'loops while the Ironwood Kanabo lasts; every kanabo attack clip ends here (next: kanaboGuard)', state: {'frames': list(range(n)), 'fps': fps, 'loop': True}}
        events = None
    else:
        clips = {'rule': 'Kanabo attacks: each clip starts and ends in the kanabo guard frame and returns to that idle (next: kanaboGuard)',
                 c: {'frames': list(range(n)), 'fps': fps, 'next': 'kanaboGuard', 'ability': ab}}
        ev = []
        for k in range(n):
            e = {'frame': k, 'clip': c, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'}
            if k == act: e.update(move=ab, hitbox=hb, damage=dmg, effect='AoE: the impact hits the target and everything round the point of impact (provisional; canon: higher base damage + AoE)')
            ev.append(e)
        events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
                  'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    s = build(base, state, [{k: v for k, v in f.items() if k != 'w'} for f in frames], status=STAT, newPoses=POSES, clips=clips, events=events,
              rmRule='E: the step in moves the body forward, the recovery steps back to the start (sum 0)', intent=INTENT[c],
              extra={'stance': 'Kanabo Stance', 'weaponSource': 'Ironwood Kanabo (Taurus ninjutsu) summons the club for 3 turns'})
    s['fps'] = fps; s.pop('approved', None); s.pop('keyPoses', None)
    w = copy.deepcopy(BASE['weapons'][0])
    w['status'] = STAT; w['items'] = ['kanabo']; w['E'] = [f['w'] for f in frames]; w['mirror'] = {'W': 'E'}
    w['viewRule'] = 'E/W only for now (S/N after approval). The club is held two-handed on its cord grip; raised overhead its head passes behind the fighter\'s head (z hilt front, blade behind).'
    for k in ('S', 'N', 'projectionRule', 'itemPoses'): w.pop(k, None)
    s['weapons'] = [w]
    assert sum(r[0] for r in s['rootMotion']['E']) == 0, state
    save(s, D + state + '.json'); print(state, n, 'frames')

# ---- impact FX (fx.png, 64 px cells): earth colours as the Taurus kit (astro.py ELEMENT, NPAT) ----
PAL = {'E': (0x8a, 0x62, 0x36), 'e': (0xc7, 0x9a, 0x5b), 'K': (0x1c, 0x10, 0x24), 'C': (0x7f, 0xe3, 0xd0), 'c': (0xd9, 0xff, 0xf6)}
PAT = {'crack1': ['K.....K', '.K...K.', '.EKEKE.'], 'crack2': ['K...........K', '.KK.......KK.', '...KK.K.KK...', '....EKKKE....'],
       'dust1': ['..e.e..', '.eEeEe.', 'eEeEeEe', '.EeEeE.'], 'dust2': ['e...e.e...e', '.e.eEeEe.e.', '..eEeEeEe..', '.eEeEeEeEe.'],
       'rocks': ['K...E', '.E.K.', 'E...K'], 'cryst': ['.c.', 'cCc', '.C.'], 'crystT': ['c', 'C', 'C']}
def ring(rx, ry, dash=3):   # the AoE: a broken flat ring of dust round the impact, e outside, E inside
    W, H = 2 * rx + 1, 2 * ry + 3; g = [['.'] * W for _ in range(H)]
    for t in range(0, 360, 4):
        a = math.radians(t)
        if (t // (dash * 4)) % 2: continue
        x, y = round(rx + rx * math.cos(a)), round(ry + 1 + ry * math.sin(a))
        g[y][x] = 'e'
        if 0 <= y + 1 < H and g[y + 1][x] == '.': g[y + 1][x] = 'E'
    return [''.join(r) for r in g]
IMPACT = (57, 63)   # E: floor point under the head of the club on the impact frame (cell coordinates)
FX = {'kanaboSmash': {
    5: [('crack2', 0, 0), ('dust2', 0, -1), ('dust1', 0, -4), ('rocks', -6, -8), ('rocks', 4, -11), (ring(10, 2), 0, 1)],
    6: [('crack2', 0, 0), ('dust1', -7, -1), ('dust1', 7, -1), ('rocks', -9, -14), ('rocks', 6, -17), ('crystT', -11, -3), ('cryst', 9, -10), (ring(14, 3), 0, 2)],
    7: [('crack2', 0, 0, 170), ('dust2', 0, -2, 150), ('rocks', -10, -10), ('crystT', 11, -3), (ring(17, 3, 4), 0, 2, 140)],
    8: [('crack1', 0, 0, 130), ('dust1', -3, -1, 110)]}}

def fx(state):
    s = json.load(open(D + state + '.json')); n = s['frames']; dirs = s['directions']
    out = Image.new('RGBA', (64 * n, 64 * len(dirs)), (0, 0, 0, 0)); px = out.load()
    for k, stamps in FX.get(state, {}).items():
        for di, d in enumerate(dirs):
            for st in stamps:
                pat, dx, dy = st[:3]; a = st[3] if len(st) > 3 else 255
                rows = PAT[pat] if isinstance(pat, str) else pat
                w = len(rows[0]); x0 = IMPACT[0] + dx - w // 2; y0 = IMPACT[1] + dy - len(rows) + 1
                for j, r in enumerate(rows):
                    for i, ch in enumerate(r):
                        if ch == '.': continue
                        x, y = x0 + i, y0 + j
                        if d == 'W': x = 63 - x
                        if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, di * 64 + y] = PAL[ch] + (a,)
    out.save(D + state + '/fx.png')
    a = json.load(open(D + state + '/animation.json')); a['layers']['fx'] = 'fx.png'
    open(D + state + '/animation.json', 'w').write(json.dumps(a, indent=2) + '\n')

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--grips': grips(sys.argv[2])
    elif len(sys.argv) > 2 and sys.argv[1] == '--fx': fx(sys.argv[2])
    else:
        item()
        for st, c in STATES.items():
            if len(sys.argv) > 1 and st not in sys.argv[1:]: continue
            spec(st, c)
