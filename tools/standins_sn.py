"""S/N (front/back) views of the approved stand-in replacement clips (Christopher 2026-11-06: E/W approved; S/N after
approval). Same machinery as universal_sn.py: the base is the approved boxing guard's S/N view, the ability frames override
the frontal arms (R = near/rear arm, the viewer's left in S; L = far/lead arm; (angle, forearm angle or None, scale, fist)),
the target is toward the viewer in S and away in N; impact splashes in front of the fighter only show outside the figure in N.
Run: python3 tools/standins_sn.py [state..] ; node tools/character-posed.mjs male <state> ; python3 tools/standins_sn.py --restore [state..] ;
     python3 tools/stances.py --outline <state> ; preview: python3 /mnt/project-files/hex-sprites/tools/dir4.py <animDir> <state> <out>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standins, astro   # registers the stand-in clips and their fx patterns
import universal_sn as U
G = U.stances.GA
AIM = (70, None, 0.45, 'front')            # lead hand reaching out at the target (toward the viewer), measuring
COCK = (155, 178, 1, 'up')                 # rear fist cocked high behind the head
SN = {
 'boxUppercut': {1: dict(R=(25, 150, 1, 'up')),                  # rear fist dropped to the hip, palm up
                 2: dict(R=(-5, 185, 1, 'up')),                   # driving up close to the body
                 3: dict(R=(-30, 192, 0.9, 'up')), 4: dict(R=(-30, 192, 0.9, 'up')),   # under the chin of the target, toward the viewer
                 5: dict(R=(-5, 195, 1, 'up'))},
 'boxHaymaker': {1: dict(R=COCK, L=AIM), 2: dict(R=(165, 185, 1, 'up'), L=AIM),              # loaded behind the head, lead hand measuring
                 3: dict(R=(130, 110, 0.8, 'up'), L=(-30, 175, 1, 'up')),                  # the loop comes over the top
                 4: dict(R=(-55, -70, 0.8, 'up'), L=(-30, 175, 1, 'up')),                  # lands at the jaw, fist across in front
                 5: dict(R=(-35, -20, 1, 'up'), L=(-30, 175, 1, 'up')),                    # carries on through and down across the body
                 6: dict(R=(20, 190, 1, 'up'))},
 'boxBodyShot': {1: dict(R=(25, 200, 1, 'up'), L=(-25, 165, 1, 'up')),                     # level change, rear glove covering the ducked head
                 2: dict(R=(25, 200, 1, 'up'), L=(-75, -30, 1, 'up')),                     # lead elbow swings out wide
                 3: dict(R=(25, 200, 1, 'up'), L=(-70, 40, 0.8, 'up')), 4: dict(R=(25, 200, 1, 'up'), L=(-70, 40, 0.8, 'up')),   # hooks in at belly height
                 5: dict(L=(-30, 160, 1, 'up'))},
 'wildSwing': {1: dict(R=(160, 175, 1, 'up'), L=(-45, -70, 1, 'up')),                      # rears way back, guard thrown open
               2: dict(R=(110, 75, 1, 'up'), L=(-35, -40, 1, 'up')),                       # flinging round flat
               3: dict(R=(-65, -85, 0.85, 'up'), L=(-25, -30, 1, 'up')),                   # lands at the head
               4: dict(R=(-45, -25, 1, 'up'), L=(-15, -20, 1, 'up')),                      # overswings across the body
               5: dict(R=(-25, -15, 1, 'up'), L=(-10, -30, 1, 'up')),
               6: dict(R=(20, 190, 1, 'up'), L=(-20, 170, 1, 'up'))},
 'clinchEntry': {1: dict(R=(-35, None, 0.45, 'front'), L=(35, None, 0.45, 'front')),      # both open hands shooting out at the neck, toward the viewer
                 2: dict(R=(-50, None, 0.3, 'front'), L=(50, None, 0.3, 'front')),
                 3: dict(R=(-140, None, 0.4, 'up'), L=(140, None, 0.4, 'up')),             # closed behind the target's head (in front of the face): collar tie
                 4: dict(R=(-110, None, 0.4, 'up'), L=(110, None, 0.4, 'up')),             # pulled down
                 5: dict(R=(15, 185, 1, 'up'), L=(-15, 175, 1, 'up'))},
}
FX_SN = {
 'boxUppercut': [(3, 'star6', 'hand', 'hand'), (4, 'star3', 'hand', 'hand')],
 'boxHaymaker': [(4, 'star9', 'hand', 'hand')],
 'boxBodyShot': [(3, 'star6', [36, 42], [22, 42]), (4, 'star3', [37, 41], [23, 41])],
 'wildSwing': [(3, 'star9', 'hand', 'hand'), (4, 'dust', [24, 63], [24, 63]), (5, 'dust', [20, 63], [20, 63])],
}

# ---------------- Medical (Palm Healing, Cellular Recovery, their self-casts, Dark Communion and the ally states) ----------------
# the anchored splashes (astro.anchored, E/W only) are drawn on rows S and N by sn_anchored below: anchors found on that row's
# render (head, near hand, feet, eyes); dx stays lateral (mirrored in N); an effect at the hand (in front of the fighter, toward
# the target or between the palms) only shows outside the figure in N. Auras stay runtime records (never baked).
SEALM = dict(R=(-20, 205, 0.8, 'front'), L=(20, -205, 0.8, 'front'))      # open hands pressed together in front of the chest
PALM_OUT = dict(R=(-45, None, 0.4, 'front'), L=(-15, 170, 1, 'up'))        # near palm laid on the ally's chest, toward the viewer
PALM_MID = dict(R=(-40, None, 0.6, 'front'), L=(-15, 170, 1, 'up'))
PALM_OWN = dict(R=(-55, 170, 0.75, 'front'), L=(-25, -20, 1, 'up'))        # near palm flat on its own chest
SIDES = dict(R=(12, 8, 1, 'front'), L=(-12, -8, 1, 'front'))               # both palms open down at the sides
EASE = dict(R=(-30, 150, 0.85, 'up'), L=(-15, -30, 1, 'up'))               # healed: guard eased, near hand drifting to the warm spot
BACK = dict(R=(15, 185, 1, 'up'), L=(-15, 175, 1, 'up'))
SN.update({
 'palmHealing': {1: SEALM, 2: SEALM, 3: PALM_MID, 4: PALM_OUT, 5: PALM_OUT, 6: PALM_OUT, 7: PALM_OUT, 8: BACK},
 'darkCommunion': {1: SEALM, 2: SEALM, 3: PALM_MID, 4: PALM_OUT, 5: PALM_OUT, 6: PALM_OUT, 7: PALM_OUT, 8: BACK},
 'cellularRecovery': {1: SEALM, 2: SEALM, 3: SEALM, 4: dict(R=(-20, 160, 0.8, 'front'), L=(-15, 170, 1, 'up')), 5: PALM_OUT, 6: PALM_OUT, 7: BACK},
 'palmHealingSelf': {1: SEALM, 2: SEALM, **{k: PALM_OWN for k in (3, 4, 5, 6, 7)}, 8: BACK},
 'cellularRecoverySelf': {1: SEALM, 2: SEALM, **{k: SIDES for k in range(3, 15)}},
 'palmHealed': {1: EASE, 2: EASE, 3: EASE, 4: BACK},
 'darkCommuned': {1: EASE, 2: EASE, 3: EASE, 4: BACK},
 'cellRecovered': {1: dict(R=(20, 175, 1, 'up'), L=(-20, 165, 1, 'up')), 2: dict(R=(20, 175, 1, 'up'), L=(-20, 165, 1, 'up')), 3: dict(R=(20, 175, 1, 'up'), L=(-20, 165, 1, 'up'))},
})
MEDICAL = ('palmHealing', 'darkCommunion', 'cellularRecovery', 'palmHealingSelf', 'cellularRecoverySelf', 'palmHealed', 'darkCommuned', 'cellRecovered')
N_BEHIND = {'palmHealingSelf': {'palmGlowMed', 'star6Med', 'vRingMed', 'vRing2Med'}}   # on its own chest: in front of the body, so hidden by the back in N
U.sn_aura = lambda *a, **k: None   # auras are runtime records (Christopher 2026-11-03): never baked into the fx sheet

def sn_anchored(state):
    """astro.anchored on rows S (0) and N (2), from the clip's anchored table"""
    from PIL import Image
    d = astro.D + state + '/'; f = d + 'fx.png'; spec = astro.load(astro.D + state + '.json')
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    if fx.height < body.height:
        n4 = Image.new('RGBA', body.size); n4.paste(fx.crop((0, 0, fx.width, 64)), (0, 64)); n4.paste(fx.crop((0, 64, fx.width, 128)), (0, 192)); fx = n4
    for row in (0, 2): fx.paste(Image.new('RGBA', (fx.width, 64)), (0, row * 64))
    lays = [Image.open(d + n).convert('RGBA').load() for n in astro.FIG_LAYERS if os.path.exists(d + n)]
    arms = Image.open(d + 'arms.png').convert('RGBA'); bp = lays[0]; px = fx.load()
    eyes = Image.open(d + 'brown-eyes.png').convert('RGBA').load() if os.path.exists(d + 'brown-eyes.png') else None
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    table = astro.CLIPS[state][6].get('anchored') or {}
    for k, items in table.items():
        for r, v in ((0, 'S'), (2, 'N')):
            sg = 1 if v == 'S' else -1
            opq = [(x, y) for y in range(64) for x in range(64) if bp[k * 64 + x, r * 64 + y][3]]
            top = min(y for _, y in opq); head = [x for x, y in opq if y <= top + 9]
            hx, hy = U.hand(spec, v, k, arms)
            ey = [(x, y) for y in range(64) for x in range(64) if eyes and eyes[k * 64 + x, r * 64 + y][3] and eyes[k * 64 + x, r * 64 + y][:3] != (0, 0, 0)] if eyes else []
            A = {'head': ((min(head) + max(head)) / 2, top + 6), 'hand': (hx, hy), 'farhand': (64 - hx, hy), 'feet': ((min(x for x, _ in opq) + max(x for x, _ in opq)) / 2, 63)}
            for item in items:
                name, an, dx, dy = item[:4]; opts = dict(item[4]) if len(item) > 4 else {}
                pat = astro.NPAT[name]; h, w = len(pat), len(pat[0])
                if an == 'eye':   # burning eyes: in S on both eyes, in N none (the face is turned away)
                    if v == 'N' or not ey: continue
                    xs = sorted(set(x for x, _ in ey)); cy = sum(y for _, y in ey) / len(ey)
                    pts = [(min(xs) + 0.5, cy), (max(xs) - 0.5, cy)]
                else:
                    pts = [A[an]]
                    if v == 'N' and (an in ('hand', 'farhand') or name in N_BEHIND.get(state, ())): opts['behind'] = True
                for ax, ay in pts:
                    x0 = round(ax + (0 if an == 'eye' else sg * dx) - (w - 1) / 2); y0 = round(ay + dy - (h - 1) / 2)
                    for yy, line in enumerate(pat):
                        for xx, ch in enumerate(line if sg > 0 else line[::-1]):
                            if ch == '.': continue
                            X, Y = x0 + xx, y0 + yy
                            if not (0 <= X < 64 and 0 <= Y < 64): continue
                            if opts.get('behind') and any(L[k * 64 + X, r * 64 + Y][3] for L in lays): continue
                            px[k * 64 + X, r * 64 + Y] = hexc(astro.NPAL[ch], opts.get('alpha', {}).get(ch, 255))
    fx.save(f); print(state, 'S/N anchored', sorted(table))
U.SN.update(SN); U.FX_SN.update(FX_SN); U.BEHIND_N |= set(SN)
U.SNAP = '/tmp/standins_sn_ew/'
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SN)
    for s in args:
        if '--restore' in sys.argv:
            U.restore(s)
            if s in MEDICAL: sn_anchored(s)
            else: U.fx(s)
        else: U.sn(s)
