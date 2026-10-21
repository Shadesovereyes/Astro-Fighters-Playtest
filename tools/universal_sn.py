"""S/N (front/back) views of the approved Universal Arts clips (Christopher 2026-10-21: Guardian Barrier, Solar Flare and
Summon Companion E/W approved). The base is the approved boxing guard's S/N view (guard.json frontal through
stances.frontal), so every clip starts and ends on the approved guard front/back frame; the ability frames override the
frontal arms (armBand: angle, forearm angle, scale, fist), as in strikes_sn.py. The target is toward the viewer in S and
away in N. Effects: the renderer draws splash fx for E/W only, so --fx paints each clip's S/N splashes into the fx sheet
after the render (an effect in front of the fighter in S sits behind the fighter in N: it only shows outside the figure).
E/W pixels are restored from HEAD after the render, so the approved side views never drift.
Run: python3 tools/universal_sn.py [state..] ; node tools/character-posed.mjs male <state> ; python3 tools/universal_sn.py --restore [state..]"""
import sys, copy, os, subprocess, json
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import load, save
import stances, strikes_sn, universal, grstrikes
R = strikes_sn.R; D = strikes_sn.D
stances.FRONT['guard'] = dict(S=stances.GA, N=stances.GN, legs=dict(foot=0, knee=(0, 0)))   # the approved boxing guard front/back view
mirror_arm = strikes_sn.mirror_arm

# per state: {frame: overrides}, S semantics as strikes_sn: R/L arm = (angle, forearm angle or None, scale, fist[, elbowAt]),
# angles screen-clockwise from straight down, the forearm angle absolute (not relative to the upper arm) (R is the viewer's left in S); NR/NL explicit back view (default: the S arm mirrored)
SEAL = dict(R=(18, 205, 1, 'front'), L=(-18, 155, 1, 'front'))   # both open hands pressed together upright in front of the chin
SN = {
 'guardianBarrier': {1: SEAL,
                     2: dict(R=(165, 175, 1, 'front'), L=(-165, -175, 1, 'front')),           # both hands swept up over the head
                     3: dict(R=(110, 105, 1, 'front'), L=(-110, -105, 1, 'front')),           # out and down in a wide arc
                     4: dict(R=(60, 55, 1, 'front'), L=(-60, -55, 1, 'front')),
                     5: dict(R=(60, 55, 1, 'front'), L=(-60, -55, 1, 'front')),
                     6: dict(R=(25, 175, 1, 'up'), L=(-25, -175, 1, 'up'))},                # hands coming back in to the guard
 'solarFlare': {1: dict(R=(120, 205, 0.5, 'front'), L=(-120, -205, 0.5, 'front')),           # open hands up in front of the forehead, palms out
                2: dict(R=(130, 210, 0.5, 'front'), L=(-130, -210, 0.5, 'front')),
                3: dict(R=(125, 140, 1, 'front'), L=(-125, -140, 1, 'front')),               # the hands snap apart
                4: dict(R=(125, 140, 1, 'front'), L=(-125, -140, 1, 'front')),
                5: dict(R=(25, 175, 1, 'up'), L=(-25, -175, 1, 'up'))},
 'summonCompanion': {1: SEAL, 2: SEAL,
                     **{k: dict(R=(-14, None, 1, 'front'), L=(-28, -8, 1, 'up')) for k in (3, 4, 5)},   # near palm slapped down on the ground in front, far hand braced on the thigh
                     6: dict(R=(20, 175, 1, 'up'), L=(-20, -175, 1, 'up'))},
}
# S/N splashes per state: (frame, pattern, at S, at N); at = bottom-left (x, bottom row); None = not drawn in that view;
# 'behind' patterns in N only show outside the figure (the effect is between the fighter and the target)
FX_SN = {
 'guardianBarrier': [(2, 'spark', [30, 6], [30, 6]), (3, 'dome1', [4, 62], [4, 62]), (4, 'dome2', [4, 62], [4, 62]), (5, 'dome3', [4, 62], [4, 62]),
                     (6, 'dome3', [4, 62], [4, 62]), (7, 'dome4', [4, 62], [4, 62])],
 'solarFlare': [(2, 'star3', [28, 15], [28, 15]), (3, 'star6', [25, 18], [25, 18]), (4, 'star9', [22, 21], [22, 21]), (5, 'star3', [28, 15], [28, 15])],
 'summonCompanion': [(2, 'spark', [30, 30], None), (3, 'dust', [28, 63], [28, 60]), (4, 'puffBig', [26, 63], [26, 60]), (5, 'puffHuge', [20, 63], [20, 60]), (6, 'puffHuge2', [19, 63], [19, 60])],
}
BEHIND_N = {'solarFlare', 'summonCompanion'}   # the flash and the summoning smoke are in front of the fighter: behind the body seen from the back
# trap and cast clips (Christopher 2026-10-19/16: E/W approved, S/N to author); the thrown item is toward the viewer in S
AIM_S = (70, None, 0.45, 'front')   # far hand points at the target, toward the viewer
SN.update({
 'cast': {1: dict(R=(10, 195, 1, 'up'), L=(-10, 165, 1, 'up')),
          **{k: dict(R=(-20, 205, 0.8, 'front'), L=(20, -205, 0.8, 'front')) for k in (2, 3, 4)},     # the seal in front of the chest
          5: dict(R=(-88, None, 0.45, 'front'), L=(-20, 190, 1, 'up')), 6: dict(R=(-88, None, 0.45, 'front'), L=(-20, 190, 1, 'up')),   # the palm driven out at the viewer
          7: dict(R=(20, 175, 1, 'up'))},
 'trapThrow': {1: dict(R=(12, 20, 1, 'up')), 2: dict(R=(22, 15, 1, 'up')),                          # the hand drops to the pouch
               3: dict(R=(150, 175, 1, 'up'), L=AIM_S), 4: dict(R=(165, 185, 1, 'up'), L=AIM_S),    # cocked high behind the head, far hand aims
               5: dict(R=(130, 110, 0.75, 'up'), L=(-20, -10, 1, 'up')),                          # the arm whips over
               6: dict(R=(-88, None, 0.45, 'front'), L=(-20, -10, 1, 'up')),                       # release, arm out at the target
               7: dict(R=(-40, -50, 0.8, 'up'), L=(-15, 170, 1, 'up')), 8: dict(R=(20, 170, 1, 'up'))},
 'trapScatter': {1: dict(R=(12, 20, 1, 'up')), 2: dict(R=(22, 15, 1, 'up')),
                 3: dict(R=(30, 30, 0.7, 'up'), L=(-35, -35, 1, 'up')),                            # swings back low, crouched
                 4: dict(R=(-10, -10, 0.8, 'up'), L=(-35, -35, 1, 'up')),                          # swings through
                 5: dict(R=(-60, None, 0.5, 'front'), L=(-20, -10, 1, 'up')), 6: dict(R=(-75, None, 0.45, 'front'), L=(-20, -10, 1, 'up')),   # flings open-handed at the viewer
                 7: dict(R=(20, 165, 1, 'up'))},
 'smokeDrop': {1: dict(R=(22, 15, 1, 'up')), 2: dict(R=(165, 180, 1, 'up')),                        # pellet from the pouch, raised overhead
               3: dict(R=(-8, None, 0.9, 'up')), 4: dict(R=(-8, None, 0.9, 'up'))},                 # slammed down in front of the feet
})
CAST_FX = [(2, 'spark', [30, 28], [30, 28]), (3, 'orb', [29, 29], [29, 29]), (4, 'orbBig', [28, 30], [28, 30]), (5, 'release', 'hand', 'hand'), (6, 'spark', 'hand', 'hand')]   # 'hand': centred on the near hand
FX_SN.update({'cast': CAST_FX,
              'smokeDrop': [(3, 'fall', [26, 56], [36, 56]), (4, 'puff', [23, 63], [23, 63]), (5, 'cloudA', [14, 63], [14, 63]), (6, 'cloudB', [8, 63], [8, 63]),
                            (7, 'cloudC', [4, 63], [4, 63]), (8, 'cloudC', [4, 62], [4, 62]), (8, 'wispL', [0, 20], [0, 20]), (8, 'wispR', [52, 16], [52, 16])]})
BEHIND_N |= {'cast', 'trapThrow', 'trapScatter'}
BEHIND_N_FRAMES = {'smokeDrop': {3, 4}}   # the pellet and first puff are in front of the fighter; the cloud swallows him
HELD = {'trapThrow': ((2, 3, 4, 5), ['tagKunai', 'pelletFlash', 'pelletSmoke', 'stake'], 'pelletSmoke'), 'trapScatter': ((2, 3, 4), ['caltrops'], 'caltrops'),
        'smokeDrop': ((1, 2), ['pelletSmoke'], 'pelletSmoke')}   # frames, the items (fx-<item>.png), the item in fx.png
# focus arts (Catch Breath v2, Recompose v3: S/N drafted at Christopher's request 2026-10-21, before their E/W verdicts)
REST = dict(R=(6, 200, 0.75, 'up'), L=(-6, -200, 0.75, 'up'))          # hands lowered and relaxed in front of the belly
OUT = dict(R=(4, 195, 0.7, 'up'), L=(-4, -195, 0.7, 'up'))             # breath out: hands sink a little lower
PUMP = dict(R=(-8, 5, 0.75, 'up'), L=(8, -5, 0.75, 'up'))           # fists pushed down and forward, at the viewer
RACK = dict(R=(35, 195, 0.85, 'up'), L=(-35, -195, 0.85, 'up'))    # racked back: elbows out behind the ribs, fists up by the chest
SN.update({'catchBreath': {1: REST, 2: REST, 3: REST, 4: REST, 5: OUT, 6: OUT, 7: REST, 8: REST, 9: OUT},
           'recompose': {}})
# Recompose v5 (Christopher 2026-10-21: one arm after the other, one big pump each, over more frames): per arm (R near, L far in S)
# v4 (Christopher 2026-10-21: v3 S/N needed further development): the push comes at the viewer as a foreshortened fist,
# knuckles on, low in front of the belly; the haul back flares the elbow out and up to the side (an elbow driving back
# seen from the front), the fist ending by the shoulder
# v5 (Christopher 2026-10-21: v4 read as raising the arms, not tucking them in): the rack pulls the elbow back and tucks
# it tight against the ribs, upper arm hanging close to the body and the forearm foreshortened forward, fist low by the chest
RC = {'mid': (-6, 10, 0.8, 'up'), 'push': (-22, None, 0.5, 'front'), 'back': (4, 170, 0.8, 'up'), 'rack': (1, 192, 0.7, 'up'), 'guard': stances.GA['R']}
RCL = lambda k: (-RC[k][0], None if RC[k][1] is None else -RC[k][1], *RC[k][2:]) if k != 'guard' else stances.GA['L']
SEQ = [(n, 'guard') for n in ('mid', 'push', 'push', 'back', 'rack', 'rack')] + [('rack', f) for f in ('mid', 'push', 'push', 'back', 'rack', 'rack')] + [('rack', 'rack')]
for k, (n, f) in enumerate(SEQ, 1): SN['recompose'][k] = dict(R=RC[n], L=RCL(f))
CLOSED_FIST_FRONT = {'recompose'}
CLOSED_S = [[0, 1, '#70241d'], [1, 1, '#70241d'], [5, 1, '#70241d'], [6, 1, '#70241d'], [0, 2, '#000000'], [1, 2, '#000000'], [5, 2, '#000000'], [6, 2, '#000000']]   # both lids shut, lash line below
# Gloom Shroud v2, Earth Wall v2, Shadow Possession v2 (Christopher 2026-10-21: E/W approved, S/N to author)
CROSS = dict(R=(70, 222, 1, 'up'), L=(-70, 138, 1, 'up'))         # forearms crossed in front of the face
LOWP = dict(R=(-10, None, 0.9, 'front'), L=(10, None, 0.9, 'front'))   # both palms low at the ground in front
POINT = (55, None, 0.75, 'up')                                  # near arm thrust straight out at the target (toward the viewer in S)
SN.update({
 'gloomShroud': {1: SEAL, **{k: CROSS for k in (2, 3, 4, 5)}, 6: dict(R=(20, 180, 1, 'up'), L=(-20, -180, 1, 'up'))},
 'earthWall': {1: LOWP, 2: LOWP,
               3: dict(R=(40, 170, 0.8, 'front'), L=(-40, -170, 0.8, 'front')),        # palms lifting past the chest
               4: dict(R=(110, 160, 1, 'front'), L=(-110, -160, 1, 'front')),          # head height
               5: dict(R=(165, 175, 1, 'front'), L=(-165, -175, 1, 'front')),          # overhead
               6: dict(R=(25, 175, 1, 'up'), L=(-25, -175, 1, 'up'))},
 'shadowPossession': {1: dict(R=(35, 120, 0.9, 'up')), **{k: dict(R=POINT) for k in (2, 3, 4, 5)}, 6: dict(R=(20, 175, 1, 'up'))},
})
FX_SN.update({
 'earthWall': [(2, 'dust', [24, 63], [24, 60]), (3, 'dust', [24, 63], [24, 60]), (3, 'spark', [30, 57], [30, 54]), (4, 'dust', [22, 63], [22, 60]),
               (4, 'spark', [36, 55], [36, 52]), (5, 'shroud1', [26, 63], [26, 60])],
 'shadowPossession': [(2, 'shadow1', [29, 63], [29, 63]), (3, 'shadow2', [25, 63], [25, 63]), (4, 'shadow3', [20, 63], [20, 63]),
                      (5, 'shadow3', [20, 63], [20, 63]), (6, 'shadow2', [25, 63], [25, 63])],   # the shadow pools out flat from under the feet
})
BEHIND_N |= {'earthWall'}
SN_APPROVED = {'catchBreath': 'S/N approved by user 2026-10-21 (v1, c70e4d7)'}

SNAP = '/tmp/universal_sn_ew/'   # the E/W sheets as they were before the S/N render (a freshly rebuilt E/W clip is not in HEAD yet)

def sn(state):
    import shutil
    cur = load(D + state + '.json')   # a freshly rebuilt E/W spec (no frontal) is the base; otherwise the committed one, so reruns start clean
    spec = cur if 'frontal' not in cur else json.loads(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + os.path.relpath(D + state + '.json', R)]))
    snap = SNAP + state + '/'; shutil.rmtree(snap, ignore_errors=True)
    if 'frontal' not in cur: shutil.copytree(D + state, snap, ignore=lambda d_, fs: [f for f in fs if not f.endswith('.png')])
    spec = stances.frontal('guard', spec); fr = spec['frontal']; F = spec['frames']
    hb = spec['bob'].get('head') or spec['bob']['dy']
    if min(hb) < 0:   # a head lifted above the guard height (the breath in) would leave the frame at the afro's top row: it stays at row 0
        for d in ('S', 'N'):
            v = fr['views'][d]; h0 = v.get('headDy') or 0
            v['headDy'] = [(h0[k] if isinstance(h0, list) else h0) + max(0, -hb[k]) for k in range(F)]
    for d in ('S', 'N'):
        ab = fr['views'][d]['armBand']
        for k, o in SN[state].items():
            for sd in 'RL':
                t = o.get('N' + sd) if d == 'N' and ('N' + sd) in o else (o.get(sd) if d == 'S' else (mirror_arm(o[sd]) if sd in o else None))
                if t is None: continue
                a, e, sc, fist, *eat = t; b = ab[sd]
                b['angle'][k] = a; b['scale'][k] = sc; b['fist'][k] = fist
                b['elbow'][k] = {'at': eat[0] if eat else 7, 'angle': e} if e is not None else None
                if d == 'N':   # back view: upper arm only when straight and pointing away
                    sh = b.get('showTo'); sh = sh if isinstance(sh, list) else [sh] * F
                    sh[k] = 7 if e is None and sc < 1 else None; b['showTo'] = sh
    if any(o.get(sd, (0, 0, 0, ''))[3] == 'front' for o in SN[state].values() for sd in 'RL'):   # open hand, palm toward the viewer
        spec['arms']['band']['fistFront'] = {'use': 'open hand seen from the front, palm toward the viewer, fingers up (Universal Arts S view)', 'anchor': [2, 4],
                                            'rows': ['mLmL.', 'LLLLm', 'LLLLm', 'mLLLs', '.sDs.']}
        if state in CLOSED_FIST_FRONT:   # a fist at the viewer, knuckles on (the approved karate S fist)
            spec['arms']['band']['fistFront'] = {'use': 'fist seen knuckles-on, pushed toward the viewer (S view)', 'anchor': [2, 2], 'rows': ['.mLm.', 'mLLLm', 'mLLLs', 'sLLms', '.sDs.']}
    if 'expressions' in spec:
        for n, sh in universal.HR['expressions']['shapes'].items():   # the S face shapes (squint, pain) from the approved hitReact
            if 'S' in sh and n in spec['expressions']['shapes']: spec['expressions']['shapes'][n].setdefault('S', copy.deepcopy(sh['S']))
        if 'closed' in spec['expressions']['shapes']: spec['expressions']['shapes']['closed'].setdefault('S', copy.deepcopy(CLOSED_S))
        ex = spec['expressions']['frames']['E']; spec['expressions']['frames']['S'] = [x if x in spec['expressions']['shapes'] and 'S' in spec['expressions']['shapes'][x] else None for x in ex]
    spec['status'] = spec['status'].replace('S/N to author after approval', 'S/N to author').replace('S/N to author', SN_APPROVED.get(state, 'S/N CANDIDATE 2026-10-21 (v1)'))
    save(spec, D + state + '.json'); print(state, 'S/N', F, 'frames')

def hand(spec, d, k, img):
    """the near (R) hand's centre in view d, frame k: the band arm's geometry (pivot, angles, scale, the arms' bob),
    snapped to the nearest coloured pixel of the rendered arms layer"""
    import math
    ab = spec['frontal']['views'][d]['armBand']['R']; at = lambda v: v[k] if isinstance(v, list) else v
    sc = at(ab['scale']) or 1; el = at(ab['elbow']); a = math.radians(at(ab['angle'])); px, py = ab['pivot']
    dy = (spec['bob'].get('arms') or spec['bob']['dy'])[k] + (at(ab.get('pivotDx')) and 0)
    u0 = (el['at'] if el else 12) * sc; x = px - math.sin(a) * u0; y = py + dy + math.cos(a) * u0
    if el: e = math.radians(el['angle']); x -= math.sin(e) * (12 - el['at']) * sc; y += math.cos(e) * (12 - el['at']) * sc
    row = ('S', 'E', 'N', 'W').index(d); best = None
    for yy in range(int(y) - 4, int(y) + 5):
        for xx in range(int(x) - 4, int(x) + 5):
            if 0 <= xx < 64 and 0 <= yy < 64:
                q = img.getpixel((k * 64 + xx, row * 64 + yy))
                if q[3] == 255 and q[:3] != (0, 0, 0) and (best is None or (xx - x) ** 2 + (yy - y) ** 2 < best[0]): best = ((xx - x) ** 2 + (yy - y) ** 2, xx, yy)
    return (best[1], best[2]) if best else (round(x), round(y))

def sn_aura(state, out):
    """the E/W aura (universal.CLIPS widths, grstrikes.aura rings) on rows S and N, under the splashes"""
    from PIL import Image, ImageFilter
    clip = universal.CLIPS.get(state); widths = clip[5] if clip else None
    if not widths or not any(widths): return
    cols = ((clip[6:] or [{}])[0]).get('auraColors') or grstrikes.AURA
    d = D + state + '/'; lay = [Image.open(d + f).convert('RGBA') for f in ('body.png', 'arms.png', 'male-gi.png') if os.path.exists(d + f)]
    px = out.load()
    for k, wd in enumerate(widths):
        if not wd: continue
        for r in (0, 2):
            box = (k * 64, r * 64, k * 64 + 64, r * 64 + 64); m = Image.new('L', (64, 64))
            for l in lay: m.paste(255, (0, 0), l.crop(box).getchannel('A').point(lambda v: 255 if v else 0))
            prev = m
            for ring in range(wd):
                grown = prev.filter(ImageFilter.MaxFilter(3)); gp, pp = grown.load(), prev.load(); c = cols[0] if ring == 0 else cols[1]
                for y in range(64):
                    for x in range(64):
                        if gp[x, y] and not pp[x, y] and (ring < wd - 1 or (x + y + k) % 2 == 0):
                            px[box[0] + x, box[1] + y] = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
                prev = grown

def fx(state):
    """the clip's S/N splashes (and the held trap item) into the fx sheets' rows S (0) and N (2); in N an effect in front
    of the fighter only shows outside the figure"""
    from PIL import Image
    d = D + state + '/'; spec = load(D + state + '.json'); sfx = spec.get('fx') or {}
    pal = {**universal.NPAL, **sfx.get('palette', {})}; pat = {**universal.NPAT, **sfx.get('patterns', {})}
    lay = [Image.open(d + n).convert('RGBA') for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png') if os.path.exists(d + n)]
    arms = Image.open(d + 'arms.png').convert('RGBA')
    held = HELD.get(state); files = [('fx.png', held[2] if held else None)] + [('fx-%s.png' % it, it) for it in (held[1] if held else [])]
    for fn, item in files:
        if fn != 'fx.png' and not os.path.exists(d + fn): continue
        out = Image.open(d + fn).convert('RGBA') if os.path.exists(d + fn) else Image.new('RGBA', lay[0].size)
        if out.height < 256: n4 = Image.new('RGBA', (out.width, 256)); n4.paste(out.crop((0, 0, out.width, 64)), (0, 64)); n4.paste(out.crop((0, 64, out.width, 128)), (0, 192)); out = n4
        for row in (0, 2): out.paste(Image.new('RGBA', (out.width, 64)), (0, row * 64))
        if fn == 'fx.png': sn_aura(state, out)
        ents = list(FX_SN.get(state, []))
        if item:
            rows_ = pat[item]; w, h = len(rows_[0]), len(rows_)
            for k in held[0]:
                (xs, ys), (xn, yn) = hand(spec, 'S', k, arms), hand(spec, 'N', k, arms)
                ents.append((k, item, [xs - w // 2, ys + h // 2], [xn - w // 2, yn + h // 2], 'held'))
        for k, p, aS, aN, *tag in ents:
            for row, at in ((0, aS), (2, aN)):
                if at is None: continue
                rows = pat[p]; h = len(rows)
                if at == 'hand': hx, hy = hand(spec, 'SN'[row // 2], k, arms); at = [hx - len(rows[0]) // 2, hy + h // 2]
                behind = row == 2 and (state in BEHIND_N or k in BEHIND_N_FRAMES.get(state, ())) and not (tag and state == 'smokeDrop')
                for y, line in enumerate(rows):
                    for x, ch in enumerate(line):
                        if ch == '.': continue
                        X, Y = at[0] + x, at[1] - (h - 1) + y
                        if not (0 <= X < 64 and 0 <= Y < 64): continue
                        if behind and not tag and any(l.getpixel((k * 64 + X, row * 64 + Y))[3] for l in lay): continue
                        c = pal[ch]; out.putpixel((k * 64 + X, row * 64 + Y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
        out.save(d + fn)
    print(state, 'S/N fx', [f for f, _ in files])

def restore(state):
    """the E/W pixels back into rows E and W: from the pre-render snapshot when sn() started from a fresh E/W spec, else from HEAD"""
    from PIL import Image
    snap = SNAP + state + '/'
    if not os.path.isdir(snap): return strikes_sn.restore(state)
    d = D + state + '/'
    for f in sorted(os.listdir(snap)):
        old = Image.open(snap + f).convert('RGBA'); new = Image.open(d + f).convert('RGBA') if os.path.exists(d + f) else Image.new('RGBA', (old.width, 256))
        if new.height < 256: new = Image.new('RGBA', (old.width, 256))
        for row, nrow in (((0, 1), (1, 3)) if old.height < 256 else ((1, 1), (3, 3))):
            new.paste(Image.new('RGBA', (new.width, 64)), (0, nrow * 64)); new.paste(old.crop((0, row * 64, old.width, row * 64 + 64)), (0, nrow * 64))
        new.save(d + f)
    print(state, 'E/W restored from the pre-render snapshot')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SN)
    for s in args:
        if '--restore' in sys.argv: restore(s); fx(s)
        else: sn(s)
