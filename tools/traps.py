"""Trap throwing (Christopher 2026-10-19), standing rig, E/W.
Thrower clips (built on the approved cast spec, guard in and out):
  trapThrow   overhand lob from the hip pouch: Explosive Tag, Flash Bomb, Smoke Screen, Spike Pit
  trapScatter underhand fling of a handful: Caltrops (bandit reskin Scatter Nails)
  smokeDrop   pellet slammed down at the feet, smoke swallows the fighter: Smoke Bomb (bandit reskin Smoke Escape)
The item rides in the near fist (fx layer) until the release frame (event release = fist); the testbed draws the item in
flight from there to the target cell and plays the trap's landing sheet (production/source/fx/traps/) at that cell.
Run: python3 traps.py ; node tools/character-posed.mjs male <state> (each) ; python3 traps.py --items ; render again."""
import sys, copy, json, math, os
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
from PIL import Image
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
FXD = R + 'production/source/fx/traps/'
CAST = load(D + 'cast.json')
band = lambda a, e, **k: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def tf(src=6, **k): return dict(src=src, **k)
STAT = 'E/W candidate 2026-10-19 ({}), awaiting user approval; S/N to author'
G_N, G_F = CAST['arms']['near'][0], CAST['arms']['far'][0]
GL = dict(ln='guard-low-rear', lf='guard-low-lead'); ST = dict(ln='stance-rear', lf='stance-lead')
AIM = band(-70, -105)                          # far hand points the way at the target while the near arm throws

# ---------- palette and item patterns (fx, drawn over the fighter) ----------
PAL = {'#': '#000000', 'W': '#ffffff', 'a': '#adadad', 'd': '#5a5a5a', 'g': '#8a8a8a', 'G': '#c4c4c4',
       'p': '#f2e6c4', 'r': '#c8302c', 'y': '#ffe97a', 'o': '#ff9a2e', 'b': '#6b4a2b', 'k': '#3a2a1a'}
ITEMS = {
    'pelletSmoke': ['.##.', '#Gg#', '#gd#', '.##.'],
    'pelletFlash': ['.##.', '#Wy#', '#yy#', '.##.'],
    'tagKunai':    ['pp......', 'rp......', 'pp.####.', '#a#aaaW#', '.#.####.'],
    'stake':       ['.##....', '#dd###.', '#ddaaW#', '.##.##.'],
    'caltrops':    ['.#.#...', '#a#a##.', '.#a#a#.', '#a#a#a#', '.#.#.#.'],
}
TRAPS = {   # ability -> (thrower clip, item in hand, landing sheet)
    'Explosive Tag': ('trapThrow', 'tagKunai', 'explosiveTag'),
    'Flash Bomb': ('trapThrow', 'pelletFlash', 'flashBomb'),
    'Smoke Screen': ('trapThrow', 'pelletSmoke', 'smokeScreen'),
    'Spike Pit': ('trapThrow', 'stake', 'spikePit'),
    'Caltrops': ('trapScatter', 'caltrops', 'caltrops'),
    'Scatter Nails': ('trapScatter', 'caltrops', 'caltrops'),
    'Smoke Bomb': ('smokeDrop', 'pelletSmoke', None),
    'Smoke Escape': ('smokeDrop', 'pelletSmoke', None),
}

# ---------- thrower clips ----------
POUCH = band(22, 8)                            # near hand down at the back hip, in the pouch
THROW = [tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
         tf(an=band(10, 30), af=G_F, bob=(1, 1, 1), lean=(0, 1), root=(0, 0), **ST),         # hand drops to the pouch
         tf(an=POUCH, af=G_F, bob=(2, 2, 2), lean=(-1, 0), root=(0, 0), **GL),               # draws the trap
         tf(an=band(120, 165), af=AIM, bob=(2, 2, 2), lean=(-1, -3), root=(-1, 0), **GL),    # cocked high behind the head, far hand aims
         tf(an=band(160, 200), af=AIM, bob=(2, 2, 2), lean=(-1, -3), root=(0, 0), **GL),
         tf(an=band(-150, -125), af=band(-50, -70), bob=(1, 1, 1), lean=(1, 3), root=(1, 0), **ST),   # arm whips over
         tf(an=band(-110, -100), af=band(-30, 210), bob=(1, 1, 1), lean=(1, 4), root=(1, 0), **ST),   # release, arm out at the target
         tf(an=band(-65, -55), af=band(-30, 210), bob=(1, 1, 2), lean=(1, 3), root=(0, 0), **ST),     # follow-through
         tf(an=band(-40, -120), af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(-1, 0), **ST),
         tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST)]
THROW_REL, THROW_HOLD = 6, (2, 3, 4, 5)

SCAT = [tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
        tf(an=band(10, 30), af=G_F, bob=(1, 1, 1), lean=(0, 1), root=(0, 0), **ST),
        tf(an=POUCH, af=G_F, bob=(2, 2, 2), lean=(-1, 0), root=(0, 0), **GL),                # grabs a handful
        tf(an=band(45, 35), af=band(-45, -60), bob=(3, 3, 3), lean=(-1, -2), root=(-1, 0), **GL),     # swings back low, crouched
        tf(an=band(-20, -35), af=band(-45, -60), bob=(3, 3, 3), lean=(1, 2), root=(1, 0), **GL),      # swings through
        tf(an=band(-80, -90, fistKind='palm'), af=band(-30, 210), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **GL),   # flings open-handed
        tf(an=band(-95, -105, fistKind='palm'), af=band(-30, 210), bob=(1, 1, 1), lean=(1, 3), root=(0, 0), **ST),
        tf(an=band(-45, -110), af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(-1, 0), **ST),
        tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST)]
SCAT_REL, SCAT_HOLD = 5, (2, 3, 4)

DROP = [tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
        tf(an=POUCH, af=G_F, bob=(2, 2, 2), lean=(-1, 0), root=(0, 0), **GL),                # pellet from the pouch
        tf(an=band(150, 175), af=G_F, bob=(2, 2, 2), lean=(-1, -1), root=(0, 0), **GL),      # raised overhead
        tf(an=band(-70, -40), af=band(-20, 30), bob=(5, 5, 5), lean=(1, 4), root=(0, 0), **GL),       # slammed down in front of the feet, crouching
        tf(an=band(-55, -25), af=band(-20, 30), bob=(5, 5, 5), lean=(1, 4), root=(0, 0), **GL),
        tf(an=G_N, af=G_F, bob=(3, 3, 3), lean=(0, 1), root=(0, 0), **GL),
        tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
        tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST),
        tf(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), **ST)]
DROP_REL, DROP_HOLD = 3, (1, 2)

from traps_fx import cloud

def drop_fx():
    """smoke from the pellet at the feet: a puff, then a cloud that swallows the fighter and thins (Stealth from frame 5)"""
    pats = {'puff': cloud(16, 9, 1), 'cloudA': cloud(34, 24, 2), 'cloudB': cloud(46, 44, 3),
            'cloudC': cloud(54, 56, 4), 'wispL': cloud(12, 9, 5), 'wispR': cloud(10, 8, 6),
            'fall': ['.#.', '#g#', '.#.', '...', '.#.', '...', '.#.']}
    fr = [{'frame': 3, 'splash': [{'pattern': 'fall', 'at': [40, 56]}]},
          {'frame': 4, 'splash': [{'pattern': 'puff', 'at': [32, 63]}]},
          {'frame': 5, 'splash': [{'pattern': 'cloudA', 'at': [16, 63]}]},
          {'frame': 6, 'splash': [{'pattern': 'cloudB', 'at': [8, 63]}]},
          {'frame': 7, 'splash': [{'pattern': 'cloudC', 'at': [4, 63]}]},
          {'frame': 8, 'splash': [{'pattern': 'cloudC', 'at': [4, 62]}, {'pattern': 'wispL', 'at': [0, 20]}, {'pattern': 'wispR', 'at': [52, 16]}]}]
    return pats, fr

def ev(F, rel, move, trap_note):
    return [{'frame': k, 'type': 'startup' if k < rel else 'active' if k == rel else 'recovery',
             **({'move': move, 'traps': trap_note} if k == rel else {})} for k in range(F)]

def specs():
    def mk(name, frames, fps, why, intent, rel, move, traps, fx=None, expr=None):
        s = build(CAST, name, frames, status=STAT.format(why), intent=intent,
                  clips={'rule': 'trap throwing (thrower); the landing effect is a separate sheet in production/source/fx/traps', name: {'frames': list(range(len(frames))), 'fps': fps, 'next': 'guard'}},
                  events={'rule': 'per-frame gameplay data per facing; release = where the item leaves the hand (filled by traps.py --items)', 'E': ev(len(frames), rel, move, traps), 'W': ev(len(frames), rel, move, traps)},
                  fx=fx, rmRule='per-frame step (screen px)')
        s.pop('keyPoses', None)
        s['expressions'] = copy.deepcopy(CAST['expressions']); s['expressions']['frames'] = {'E': expr or [None] * len(frames)}
        if not any(expr or []): s.pop('expressions')
        save(s, D + name + '.json')
    mk('trapThrow', THROW, 12, 'trap throw, overhand lob',
       'Trap throw (Explosive Tag, Flash Bomb, Smoke Screen, Spike Pit): from the guard the near hand drops to the pouch at the back hip and draws the trap, cocks it high behind the head while the far hand points at the target cell, then whips the arm over and lets go with the arm out at the target (frame 6, event release); follow-through and back to the guard. The item rides in the fist (fx) on frames 2-5; the testbed flies it from release to the target cell and plays the landing sheet there.',
       THROW_REL, 'trapThrow', ['Explosive Tag', 'Flash Bomb', 'Smoke Screen', 'Spike Pit'],
       expr=[None, None, None, 'squint', 'squint', None, None, None, None, None])
    mk('trapScatter', SCAT, 12, 'trap scatter, underhand fling',
       'Trap scatter (Caltrops; bandit Scatter Nails): the near hand grabs a handful from the pouch, swings back low in a crouch and flings it underhand, the hand opening at the release (frame 5, event release) so the caltrops fan out over the target cell; back to the guard.',
       SCAT_REL, 'trapScatter', ['Caltrops', 'Scatter Nails'], expr=[None, None, None, 'squint', 'squint', None, None, None, None])
    pats, fr = drop_fx()
    mk('smokeDrop', DROP, 12, 'smoke bomb dropped at the feet',
       'Smoke Bomb (self; bandit Smoke Escape): a pellet from the pouch is raised overhead and slammed down at the feet in a crouch (frame 3, event release); it bursts into a puff that grows into a cloud swallowing the fighter, who is in Stealth from frame 5 (the testbed fades the fighter under the cloud and keeps its own Stealth look afterwards).',
       DROP_REL, 'smokeBomb', ['Smoke Bomb', 'Smoke Escape'],
       fx={'rule': 'smoke from the pellet at the feet, over the fighter', 'top': True, 'palette': PAL, 'patterns': pats, 'frames': fr},
       expr=[None, None, 'squint', 'squint', 'squint', 'squint', None, None, None])

# ---------- after render: item in the fist (fx), release anchors ----------
def fist(state, k, side='near'):
    s = load(D + state + '.json'); a = s['arms'][side][k]
    ua, fa = math.radians(a['angle']), math.radians(a['elbow']['angle'])
    lx = s['lean']['dx']['head'][k] * 0.5; dy = s['bob']['arms'][k]
    sx = 32 + lx + (2 if side == 'far' else 0)
    x = sx - 8 * math.sin(ua) - 7 * math.sin(fa); y = 23 + dy + 8 * math.cos(ua) + 7 * math.cos(fa)
    best = None
    for lay in ('arms', 'body'):
        im = Image.open(D + state + '/' + lay + '.png').convert('RGBA')
        for yy in range(int(y) - 4, int(y) + 5):
            for xx in range(int(x) - 4, int(x) + 5):
                if 0 <= xx < 64 and 0 <= yy < 64:
                    p = im.getpixel((k * 64 + xx, yy))
                    if p[3] == 255 and p[:3] != (0, 0, 0):
                        d = (xx - x) ** 2 + (yy - y) ** 2
                        if best is None or d < best[0]: best = (d, xx, yy)
    return [best[1], best[2]] if best else [round(x), round(y)]

def items(variant=None):
    """variant: which item the preview shows in hand; the shipped specs carry the clip's default item"""
    for st, hold, rel, item in (('trapThrow', THROW_HOLD, THROW_REL, variant or 'pelletSmoke'), ('trapScatter', SCAT_HOLD, SCAT_REL, 'caltrops'), ('smokeDrop', DROP_HOLD, DROP_REL, 'pelletSmoke')):
        s = load(D + st + '.json')
        fx = s.get('fx') or {'rule': '', 'top': True, 'palette': PAL, 'patterns': {}, 'frames': []}
        base_rule = fx['rule'].split('; ', 1)[-1] if fx['rule'].startswith('item in') else fx['rule']
        fx['rule'] = 'item in the near fist until the release frame' + ('; ' + base_rule if base_rule else '')
        fx['palette'] = PAL; fx['patterns'].update({k: v for k, v in ITEMS.items()})
        frames = {f['frame']: f for f in fx['frames']}
        for f in frames.values(): f['splash'] = [sp for sp in f.get('splash', []) if sp['pattern'] not in ITEMS]
        for k in hold:
            x, y = fist(st, k); rows = ITEMS[item]; w, h = len(rows[0]), len(rows)
            frames.setdefault(k, {'frame': k, 'splash': []})['splash'].append({'pattern': item, 'at': [x - w // 2, y + h // 2]})
        fx['frames'] = [frames[k] for k in sorted(frames) if frames[k].get('splash') or frames[k].get('smear')]
        s['fx'] = fx
        relp = fist(st, rel) if st != 'smokeDrop' else [fist(st, rel)[0], 62]
        for d in ('E', 'W'):
            for e in s['events'][d]:
                if e['frame'] == rel: e['release'] = relp if d == 'E' else [63 - relp[0], relp[1]]
        s['events']['heldItem'] = {'rule': 'item drawn in the fist on these frames (fx); the testbed swaps the pattern per trap', 'frames': list(hold), 'byTrap': {t: v[1] for t, v in TRAPS.items() if v[0] == st}}
        save(s, D + st + '.json')

if __name__ == '__main__':
    if '--items' in sys.argv: items(sys.argv[sys.argv.index('--items') + 1] if len(sys.argv) > sys.argv.index('--items') + 1 else None)
    else: specs()
    print('ok')
