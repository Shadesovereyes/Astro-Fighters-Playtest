"""Universal Arts animations (Christopher 2026-10-20: "lets move onto universal art animations"; abilities from the
Universal Arts tab of AstroFighters_Abilities). Played from the approved boxing guard (hitReact frame 6 settles into it)
and returning to it. One state per ability. E/W first (W mirrors E), S/N after approval. Effects white/neutral.
Run: python3 tools/universal.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/universal.py --aura <state>"""
import sys, copy
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grstrikes
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
HR_FX = load(D + 'clinchSweepingShoulderHit.json')['fx']
HR = load(D + 'hitReact.json'); HR.pop('frontal', None); HR['directions'] = ['E', 'W']
HR['legs']['feet'].update({k: v for k, v in load(D + 'heavyAttack.json')['legs']['feet'].items() if k not in HR['legs']['feet']})   # kick feet
_JC = load(D + 'judoChop.json')['arms']['band']; HR['arms']['band'].update({k: _JC[k] for k in ('palmUp', 'palmDown', 'palmHeel')})   # open-hand shapes (palm seals, palm thrusts)
HR['arms']['band']['fingerGun'] = {'use': 'finger gun (Chakra Bullet): index finger pointing along the arm, thumb up, the other fingers curled', 'anchor': [0, 1],
                                   'rows': ['.Lm....', 'LLLLLLm', 'LLLms..', 'msDs...']}
def band(a, e, **k): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
CLOSED = load(D + 'downed.json')['expressions']['shapes']['closed']
def h(k, side): return copy.deepcopy(HR['arms'][side][k])
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {s_: 'E/W approved by user 2026-10-21 (v1; W mirrors E); S/N to author' for s_ in ('guardianBarrier', 'solarFlare', 'summonCompanion')}
APPROVED['chakraBullet'] = 'E/W approved by user 2026-10-21 (v2, 870541e; W mirrors E); S/N to author'
APPROVED['recompose'] = 'E/W approved by user 2026-10-21 (v5, one exaggerated pump per arm, 026b272; W mirrors E); S/N to author (v3 approval withdrawn by user: needs further development)'
APPROVED['catchBreath'] = 'E/W approved by user 2026-10-21 (v2, two slow deep breaths; W mirrors E); S/N approved by user 2026-10-21 (v1, c70e4d7)'
APPROVED.update(chargeChakra='E/W approved by user 2026-10-21 (v4 meditative hold, 9622256; W mirrors E); S/N to author', **{s_: 'E/W approved by user 2026-10-21 (v3 chakra flowing up the drainer\'s arms, 9622256; W mirrors E); S/N to author' for s_ in ('chakraDrain', 'chakraDrained')})
UNUSED = 'UNUSED (Christopher 2026-10-21): shelved, not offered anywhere and no further animation work until its use is decided; E/W v1 draft kept for reference'
APPROVED.update(ironMountain=UNUSED, heavenlyKick=UNUSED)

G_N, G_F = h(6, 'near'), h(6, 'far')                     # guard arms
GUARD = dict(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), ln='stance-rear', lf='stance-lead', root=(0, 0))
def g(**k): return dict(src=6, **{**GUARD, **k})
LOW = dict(ln='guard-low-rear', lf='guard-low-lead')
def leg(name, hip, knee, foot, wrap=56, kind='flat'):
    return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'footX': foot, 'wrapRow': wrap, 'foot': kind}
POSES = [leg('cb-brace-lead', (32, 45), (38, 51), 37), leg('cb-brace-rear', (31, 45), (31, 51), 25)]   # knees bent deep and pushed forward over the feet
POSES += [leg('im-step-lead', (33, 43), (38, 50), 41), leg('im-step-rear', (31, 43), (28, 51), 24)]   # Iron Mountain: lead foot stamps a stride forward
def kleg(name, hip, knee, ankle, foot): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'ankle': list(ankle), 'foot': foot}
POSES += [kleg('hk-swing', (34, 41), (40, 43), (46, 43), 'pointFwd'),     # Heavenly Kick: rear leg swinging up straight in front
          kleg('hk-rise', (34, 40), (40, 33), (45, 25), 'pointUR'),       # straight leg at the top, sole rising under the chin
          kleg('hk-drop', (34, 41), (38, 47), (34, 53), 'toe30k'),        # leg coming back down, knee soft
          {'name': 'hk-plant', 'construction': 'band', 'hipX': 32, 'hipRow': 42, 'kneeX': 34, 'kneeRow': 50, 'footX': 35, 'wrapRow': 56, 'foot': 'flat'}]   # standing leg
POSES += [leg('duel-lead', (32, 42), (34, 50), 35), leg('duel-rear', (31, 42), (30, 50), 28)]   # pistol-duel stance: feet drawn close, side-on, legs straight
FXP, FXPAL = HR_FX['patterns'], HR_FX['palette']
BRACE = dict(ln='cb-brace-rear', lf='cb-brace-lead')   # the hands brace on the thighs
SEAL_N, SEAL_F = band(-48, -150, fistKind='palm'), band(-60, -146, fistKind='palm')   # tiger seal: both open hands pressed together upright in front of the chin, fingers up
RC_MID, RC_PUSH, RC_BACK, RC_RACK = band(-25, -65), band(-60, -40), band(0, -75), band(38, -95)   # Recompose (exaggerated, v5): fist on its way down, driven far down and forward, hauled back, racked well past the ribs
MED_N, MED_F = band(-8, -75, fistKind='palm'), band(-12, -80, fistKind='palm')   # meditative hold: forearms level, open hands palm up resting in front of the belly (Charge Chakra v4)

# ---------- ninjutsu fx patterns (white/neutral; d/g = neutral greys for shadow techniques) ----------
CHAKRA = ('#4f8dff', '#23407e')   # the testbed chakra bar: --chakra #4f8dff, gradient from #23407e (Christopher 2026-10-21: chakra auras match the bar)
NPAL = {'#': '#000000', 'W': '#ffffff', 'w': '#e3e3e3', 'g': '#9a9a9a', 'd': '#4a4a4a', 'B': CHAKRA[0], 'b': CHAKRA[1]}
def grid(w, h): return [['.'] * w for _ in range(h)]
def rows(gr): return [''.join(r) for r in gr]
def dome(rx, ry, frac=1.0, dotted=False):
    """upper half of an ellipse (the barrier bubble) rx by ry, white ring with a light-grey inner ring; frac = how much of
    the arc has grown from the ground up (both sides together)"""
    import math
    gr = grid(2 * rx + 1, ry + 1)
    for t in range(0, 1801):
        a = math.pi * t / 1800                   # 0 = right foot of the dome, pi = left
        if min(a, math.pi - a) > frac * math.pi / 2: continue
        for k, c in ((0, 'W'), (1, 'w')):
            x = round(rx + (rx - k) * math.cos(a)); y = round(ry - (ry - k) * math.sin(a))
            if 0 <= y <= ry and (not dotted or (x + y) % 2 == 0): gr[y][x] = c if gr[y][x] in '.w' else gr[y][x]
    return rows(gr)
def star(r):
    gr = grid(2 * r + 1, 2 * r + 1)
    for i in range(-r, r + 1):
        gr[r][r + i] = gr[r + i][r] = 'W' if abs(i) < r else 'w'
        if abs(i) <= r * 2 // 3: gr[r + i][r + i] = gr[r + i][r - i] = 'W' if abs(i) < r // 2 else 'w'
    for y in (r - 1, r, r + 1):
        for x in (r - 1, r, r + 1): gr[y][x] = 'W'
    return rows(gr)
def blob(rx, ry, dots=False):
    gr = grid(2 * rx + 1, 2 * ry + 1)
    for y in range(2 * ry + 1):
        for x in range(2 * rx + 1):
            d = ((x - rx) / rx) ** 2 + ((y - ry) / ry) ** 2
            if d <= 1 and (not dots or (x + y) % 2 == 0): gr[y][x] = 'W' if d < 0.45 else 'w'
    return rows(gr)
GHOST = ['...ggg...', '..g.g.g..', '.g.g.g.g.', '..g.g.g..', '.g.g.g.g.', 'g.g.g.g.g', '.g.g.g.g.', 'g.g.g.g.g', '.g.g.g.g.', 'g.g...g.g', '.g.....g.']
def strip(n, c='d', h=2): return [c * n] * h
NPAT = {'spark': ['.w.', 'wWw', '.w.'], 'orb': ['.ww.', 'wWWw', 'wWWw', '.ww.'], 'orbBig': ['..w..', '.wWw.', 'wWWWw', '.wWw.', '..w..'],
        'release': ['..w....', '.wW.w..', 'wWWWWw.', '.wW.w..', '..w....'], 'wisp': ['.w.', 'wWw', '.w.'], 'wisp2': ['w.w', '.W.'],
        'star3': star(3), 'star6': star(6), 'star9': star(9),
        'dome1': dome(27, 58, 0.35), 'dome2': dome(27, 58, 0.75), 'dome3': dome(27, 58), 'dome4': dome(27, 58, dotted=True),
        'shadow1': strip(6), 'shadow2': strip(14), 'shadow3': strip(24), 'shadowTip': ['dd.', 'ddd'],
        'shroud1': ['.g.g.', 'g.g.g'],
        'puffBig': ['....wwww....', '..wwWWWWww..', '.wWWWwwWWWw.', 'wWWwwwwwwWWw', 'wWwwwwwwwwWw', '.wwwwwwwwww.', '..wwwwwwww..'],
        'puffRing': ['..w..w..w..', '.w.......w.', 'w.........w', '.w.......w.', '..w..w..w..'],
        'ghost1': [r[2:7] for r in GHOST[::2]], 'ghost2': GHOST[:-2], 'ghost3': GHOST, 'puffHuge': blob(11, 8), 'puffHuge2': blob(12, 9, dots=True), 'dust': ['..w..w..', '.wWwwWw.', 'wWwwwwWw'],
        'bspark': ['.b.', 'bBb', '.b.'], 'borb': ['.bb.', 'bBBb', 'bBBb', '.bb.'], 'borbBig': ['..b..', '.bBb.', 'bBWBb', '.bBb.', '..b..'],
        'brelease': ['..b.....', '.bB.b...', 'bBWWBBb.', '.bB.b...', '..b.....'], 'bwisp': ['.b.', 'bBb', '.b.'], 'bwisp2': ['b.b', '.B.']}
def nfx(rule, frames): return {'rule': rule, 'top': True, 'palette': NPAL, 'patterns': NPAT, 'frames': [{'frame': k, 'splash': [{'pattern': p_, 'at': at} for p_, at in sp]} for k, sp in frames]}

CLIPS = {   # state: (ability, active frame, intent, frames, expressions, aura widths)
 'chargeChakra': ('Charge Chakra', 4,
  'Charge Chakra (free focus action, recover chakra): from the guard the fighter sinks into the knees and lowers both open hands, palms up, to rest in front of the belly in a meditative hold, eyes closed in focus; holding it, an aura in the chakra bar blue swells around the whole body in a slow pulse as the chest rises with the breath, then fades; the eyes open, the hands part and come back up into the guard (Christopher 2026-10-21: eyes closed, aura the colour of the chakra bar; v4: hands lowered into a meditative state, the raised seal read as a recoil).', [
     g(),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=MED_N, af=MED_F, bob=(3, 3, 3), lean=(0, 0), **LOW),
     g(an=MED_N, af=MED_F, bob=(3, 3, 3), lean=(0, 0), **LOW),
     g(an=MED_N, af=MED_F, bob=(2, 3, 3), lean=(0, -1), **LOW),     # in-breath: chest lifts, head a row higher
     g(an=MED_N, af=MED_F, bob=(2, 3, 3), lean=(0, -1), **LOW),
     g(an=MED_N, af=MED_F, bob=(3, 3, 3), lean=(0, 0), **LOW),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g()],
  [None, None, 'closed', 'closed', 'closed', 'closed', 'closed', None, None],
  [0, 0, 1, 2, 3, 3, 2, 1, 0],
  dict(auraColors=CHAKRA)),
 'catchBreath': ('Catch Breath', 2,
  'Catch Breath (free focus action, recover stamina; Christopher 2026-10-21: one or two slow deep breaths, not the exhausted pose): from the guard the hands lower a little and relax; the fighter draws a long, deep breath in, eyes closing, chest and shoulders rising and the head lifting; holds it a beat, then lets it out slowly, the shoulders sinking below the guard; a second, calmer breath; then the hands come back up into the guard.', [
     g(),
     g(an=band(-25, -105), af=band(-35, -115), bob=(1, 1, 2), lean=(0, 1)),                    # hands lower and relax
     g(an=band(-25, -108), af=band(-35, -118), bob=(1, 0, 1), lean=(0, 0)),                    # breath in begins
     g(an=band(-25, -110), af=band(-35, -120), bob=(0, -1, 0), lean=(0, -1)),                  # full breath: chest up, head up, shoulders raised
     g(an=band(-25, -110), af=band(-35, -120), bob=(0, -1, 0), lean=(0, -1)),                  # holds it
     g(an=band(-22, -104), af=band(-32, -114), bob=(1, 1, 2), lean=(0, 1)),                    # long breath out
     g(an=band(-20, -100), af=band(-30, -110), bob=(2, 2, 3), lean=(0, 2)),                    # shoulders sink, empty
     g(an=band(-25, -108), af=band(-35, -118), bob=(1, 0, 1), lean=(0, 0)),                    # second breath in
     g(an=band(-25, -108), af=band(-35, -118), bob=(1, 0, 1), lean=(0, 0)),
     g(an=band(-22, -104), af=band(-32, -114), bob=(1, 1, 2), lean=(0, 1)),                    # and out
     g()],
  [None, None, 'closed', 'closed', 'closed', 'closed', None, 'closed', 'closed', None, None],
  None,
  dict(fps=5)),
 'recompose': ('Recompose', 13,
  'Recompose (free focus action, recover poise; Christopher 2026-10-21: like Henry Cavill\'s arm "reload"; v4: the arms move one after the other; v5: one big exaggerated pump per arm, spread over more frames so it feels slower): from the guard the near fist sinks and drives far down and forward, holds, then is hauled back hard, elbow driving well past the ribs and the shoulder popping up; then the far fist does the same while the near one stays racked; both hold racked a beat, then snap back into a tight guard with a thin white pulse.', [
     g()] + [f for far in (False, True) for f in (
     g(an=RC_RACK if far else RC_MID, af=RC_MID if far else G_F, bob=(1, 1, 1), lean=(0, 1)),                  # the fist on its way down and forward
     g(an=RC_RACK if far else RC_PUSH, af=RC_PUSH if far else G_F, bob=(1, 1, 2), lean=(0, 2)),                # pushed far out
     g(an=RC_RACK if far else RC_PUSH, af=RC_PUSH if far else G_F, bob=(2, 2, 2), lean=(0, 3)),                # held, leaning into it
     g(an=RC_RACK if far else RC_BACK, af=RC_BACK if far else G_F, bob=(1, 1, 1), lean=(0, 1)),                # hauled back
     g(an=RC_RACK, af=RC_RACK if far else G_F, bob=(1, 0, -1), lean=(0, -1)),                                  # racked: elbow well past the ribs, shoulder up
     g(an=RC_RACK, af=RC_RACK if far else G_F, bob=(1, 0, 0), lean=(0, 0)))] + [
     g(an=RC_RACK, af=RC_RACK, bob=(1, 0, 0), lean=(0, 0)),                                   # both held racked a beat
     g(an=G_N, af=G_F, bob=(2, 2, 2), lean=(0, 3), **LOW),                                    # snaps into the guard
     g()],
  [None] * 16,
  [0] * 14 + [1, 0],
  dict(fps=10)),
 'ironMountain': ('Iron Mountain', 3,
  'Iron Mountain (guard-break strike, bajiquan stamp and reinforced elbow): from the guard the fighter folds the rear arm level with the fist back at the chest and the lead fist tucked to the chest behind it, coils back a row, then stamps the lead foot a stride forward and drives the point of the folded elbow and the shoulder behind it into the guard with the whole body behind it, rooted like a mountain; a stamp of dust at the lead foot and impact lines at the elbow; then draws back into the guard.', [
     g(),
     g(an=band(-60, 110), af=band(-20, -150), bob=(2, 2, 2), lean=(0, -1), **LOW),                       # coil: lead arm folded, rear palm on the lead fist
     g(an=band(-75, 100), af=band(-20, -150), bob=(3, 3, 3), lean=(1, 4), ln='im-step-rear', lf='im-step-lead', root=(2, 0)),   # stamp and drive
     g(an=band(-88, 92), af=band(-20, -150), bob=(3, 3, 3), lean=(2, 6), ln='im-step-rear', lf='im-step-lead', root=(2, 0)),   # elbow and shoulder impact
     g(an=band(-88, 92), af=band(-20, -150), bob=(3, 3, 3), lean=(2, 6), ln='im-step-rear', lf='im-step-lead'),
     g(an=band(-40, -120), af=band(-60, -130), bob=(2, 2, 2), lean=(1, 4), ln='im-step-rear', lf='im-step-lead', root=(-2, 0)),
     g(an=G_N, af=G_F, bob=(2, 2, 2), lean=(0, 2), **LOW, root=(-2, 0)),
     g()],
  [None, None, 'squint', 'squint', 'squint', None, None, None],
  None,
  dict(fps=12, hitbox=[42, 18, 12, 16], damage='heavy', rm='E: x +2, +2 on the stamp and drive, back -2, -2 into the guard',
       fx={'rule': 'white/neutral: impact lines off the lead elbow on the hit; a dust stamp at the lead foot', 'palette': FXPAL, 'patterns': FXP, 'frames': [
           {'frame': 2, 'splash': [{'pattern': 'puff', 'at': [36, 63]}]},
           {'frame': 3, 'splash': [{'pattern': 'lines', 'at': [44, 19]}, {'pattern': 'puff', 'at': [42, 63]}]},
           {'frame': 4, 'splash': [{'pattern': 'speck', 'at': [46, 63]}]}]})),
 'heavenlyKick': ('Heavenly Kick', 3,
  'Heavenly Kick (rising kick that can stun): from the guard the fighter shifts onto the lead leg and swings the rear leg up straight in front of the body, toes up, the sole rising under the chin to head height while the torso leans back and the rear arm swings down and back for balance; impact lines at the foot on the hit; the leg drops back down and the fighter settles into the guard.', [
     g(),
     g(bob=(1, 1, 1), lean=(0, 0), ln='hk-swing', lf='hk-plant', an=band(10, -40)),
     g(bob=(0, 0, 1), lean=(0, -3), ln='hk-rise', lf='hk-plant', an=band(30, 10)),
     g(bob=(0, 0, 1), lean=(1, -5), ln='hk-rise', lf='hk-plant', an=band(40, 20), root=(1, 0)),
     g(bob=(0, 0, 1), lean=(1, -4), ln='hk-rise', lf='hk-plant', an=band(40, 20)),
     g(bob=(1, 1, 1), lean=(0, -1), ln='hk-drop', lf='hk-plant', an=band(10, -40), root=(-1, 0)),
     g(bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, None, None, 'squint', None, None, None, None],
  None,
  dict(fps=12, hitbox=[42, 16, 12, 14], damage='heavy', rm='E: x +1 on the hit, back -1 as the leg drops',
       fx={'rule': 'white/neutral impact lines above the rising foot on the hit', 'palette': FXPAL, 'patterns': FXP, 'frames': [
           {'frame': 3, 'splash': [{'pattern': 'lines', 'at': [40, 12]}]}]})),
 'guardianBarrier': ('Guardian Barrier', 4,
  'Guardian Barrier (ally buff, Fortified): from the guard the fighter makes the seal at the chest, sweeps both open hands up over the head and then out and down in a wide arc, tracing the bubble; a white/neutral dome grows from the ground up around the fighter, holds, then thins to a dotted shell as the hands come back to the guard (the testbed draws the ally field itself).', [
     g(),
     g(an=SEAL_N, af=SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-160, -175, fistKind='palm'), af=band(-150, -170, fistKind='palm'), bob=(0, 0, 0), lean=(0, 0), ln='stance-rear', lf='stance-lead'),
     g(an=band(-120, -110, fistKind='palm'), af=band(-110, -100, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-60, -50, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-70, -60, fistKind='palm'), af=band(-60, -50, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-40, -100), af=band(-50, -110), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(),
     g()],
  [None, 'squint', None, None, None, None, None, None, None],
  None,
  dict(fx=nfx('white/neutral bubble: a dome grows from the ground up around the fighter as the hands trace it, holds, then thins to a dotted shell',
              [(2, [('spark', [36, 6])]), (3, [('dome1', [4, 62])]), (4, [('dome2', [4, 62])]), (5, [('dome3', [4, 62])]), (6, [('dome3', [4, 62])]), (7, [('dome4', [4, 62])])]))),
 'solarFlare': ('Solar Flare', 3,
  'Solar Flare (ranged debuff, Blind): from the guard the fighter brings both open hands up in front of the forehead, palms out and fingers spread, eyes shut; the hands snap apart and a white starburst flashes from between them, swelling and fading; then back to the guard.', [
     g(),
     g(an=band(-110, -150, fistKind='palm'), af=band(-105, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-118, -160, fistKind='palm'), af=band(-112, -160, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-105, -115, fistKind='palm'), af=band(-140, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-105, -115, fistKind='palm'), af=band(-140, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-60, -120), af=band(-80, -140), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=12, fx=nfx('white/neutral starburst from between the hands at the forehead; the blind itself is drawn on the target by the testbed',
              [(2, [('star3', [41, 15])]), (3, [('star6', [38, 18])]), (4, [('star9', [35, 21])]), (5, [('star3', [41, 15])])]))),
 'chakraBullet': ('Chakra Bullet', 7,
  'Chakra Bullet (basic chakra projectile; Christopher 2026-10-21: pistol-duel stance, finger gun, aura gathers to the fingertip and fires): from the guard the fighter draws the feet together side-on, tucks the far hand into the small of the back and raises the near arm straight out at shoulder height, hand shaped into a finger gun; an aura in the chakra bar blue swells around the body, then draws in to an orb at the fingertip, which fires with a burst and a small kick of recoil; the spell draws the bullet from the release frame; then back to the guard.', [
     g(),
     g(an=band(-55, -55, fistKind='gun'), af=band(20, -80), bob=(1, 1, 1), lean=(0, 0), ln='duel-rear', lf='duel-lead'),
     g(an=band(-90, -90, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -1), ln='duel-rear', lf='duel-lead'),
     g(an=band(-90, -90, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -1), ln='duel-rear', lf='duel-lead'),
     g(an=band(-90, -90, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -1), ln='duel-rear', lf='duel-lead'),
     g(an=band(-90, -90, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -1), ln='duel-rear', lf='duel-lead'),
     g(an=band(-90, -90, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -1), ln='duel-rear', lf='duel-lead'),
     g(an=band(-100, -100, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -2), ln='duel-rear', lf='duel-lead'),   # fires: recoil kicks the hand up
     g(an=band(-94, -94, fistKind='gun'), af=band(20, -80), bob=(0, 0, 0), lean=(0, -1), ln='duel-rear', lf='duel-lead'),
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None, None],
  [0, 0, 1, 2, 3, 2, 1, 0, 0, 0, 0],
  dict(fps=10, release=[57, 20], auraColors=CHAKRA,
       fx=nfx('chakra bar blue: the aura (drawn by aura()) swells, then draws into an orb at the fingertip that fires with a burst',
              [(5, [('borb', [55, 24])]), (6, [('borbBig', [55, 25])]), (7, [('brelease', [57, 22])]), (8, [('bspark', [61, 22])])]))),
 'chakraDrain': ('Chakra Drain', 3,
  'Chakra Drain (debuff, steals chakra; Christopher 2026-10-21: plays like a short grapple, the chakra aura leaving the target in the chakra bar blue): the fighter steps in and grabs the target in a collar tie, both hands on the neck and shoulder, pulls them in and holds while wisps of chakra-blue light stream off the target into the gripping hands and flow up through both arms into the body, the drainer glowing faintly blue as it arrives (Christopher 2026-10-21 v3: the chakra flows out of the target through the arms of the user); then shoves them off and steps back into the guard. Pairs with chakraDrained on the target.', [
     g(),
     g(an=band(-70, -100, fistKind='palm'), af=band(-75, -105, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), root=(4, 0)),   # steps in, hands reaching
     g(an=band(-80, -80, fistKind='palm'), af=band(-84, -84, fistKind='palm'), bob=(1, 1, 1), lean=(1, 4), root=(4, 0)),      # grabs
     g(an=band(-72, -95, fistKind='palm'), af=band(-78, -98, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),            # pulls in, holds
     g(an=band(-72, -95, fistKind='palm'), af=band(-78, -98, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-72, -95, fistKind='palm'), af=band(-78, -98, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-88, -88, fistKind='palm'), af=band(-90, -90, fistKind='palm'), bob=(1, 1, 1), lean=(1, 5)),                    # shoves off
     g(an=band(-60, -120), af=G_F, bob=(1, 1, 2), lean=(0, 2), root=(-4, 0)),
     g(root=(-4, 0))],
  [None, None, 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 0, 0, 0, 1, 1, 0, 0, 0],
  dict(fps=10, auraColors=CHAKRA, flow=(3, 4, 5), hitbox=[44, 20, 10, 10], damage='light', rm='E: x +4, +4 stepping in to the tie, back -4, -4',
       fx=nfx('chakra bar blue wisps streaming off the target (in front) into the gripping hands while the tie holds',
              [(3, [('bwisp', [58, 22]), ('bwisp2', [54, 26])]), (4, [('bwisp2', [56, 21]), ('bwisp', [51, 25]), ('bspark', [60, 27])]), (5, [('bwisp', [53, 22]), ('bwisp2', [49, 26])])]))),
 'chakraDrained': ('Chakra Drain (target)', 3,
  'Chakra Drain, the target\'s side (pairs with chakraDrain): caught in the collar tie the target is jerked in, head snapped forward and guard broken, and sags in the grip while a chakra-blue aura bleeds off them and away toward the drainer; shoved off, they stumble back and recover into the guard.', [
     dict(src=6, an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), ln='stance-rear', lf='stance-lead', root=(0, 0)),
     dict(src=6, an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), ln='stance-rear', lf='stance-lead', root=(0, 0)),
     dict(src=1, an=h(1, 'near'), af=h(1, 'far'), bob=(2, 2, 2), lean=(1, 3), ln='guard-low-rear', lf='guard-low-lead', root=(0, 0)),
     dict(src=1, an=band(-20, -60), af=band(-30, -70), bob=(3, 3, 3), lean=(1, 4), ln='guard-low-rear', lf='guard-low-lead', root=(0, 0)),
     dict(src=1, an=band(-15, -50), af=band(-25, -60), bob=(3, 4, 4), lean=(1, 5), ln='guard-low-rear', lf='guard-low-lead', root=(0, 0)),
     dict(src=1, an=band(-15, -50), af=band(-25, -60), bob=(3, 4, 4), lean=(1, 5), ln='guard-low-rear', lf='guard-low-lead', root=(0, 0)),
     dict(src=2, an=h(2, 'near'), af=h(2, 'far'), bob=(2, 2, 2), lean=(1, -3), ln='guard-low-rear', lf='guard-low-lead', root=(-2, 0)),
     dict(src=4, an=h(4, 'near'), af=h(4, 'far'), bob=(2, 2, 2), lean=(0, -1), ln='stance-rear', lf='stance-lead', root=(-1, 0)),
     dict(src=6, an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), ln='stance-rear', lf='stance-lead', root=(3, 0))],
  [None, None, 'pain', 'pain', 'pain', 'pain', 'pain', None, None],
  [0, 0, 0, 1, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=CHAKRA, react=True, rm='shoved back -2, -1, then steps back into place +3 (the drainer steps back too)')),
 'gloomShroud': ('Gloom Shroud', 4,
  'Gloom Shroud (self buff, Stealth): from the guard the fighter makes the seal, then crosses both forearms in front of the face and sinks low; a dark neutral-grey shroud wells up around the body from the ground and wraps it, then settles to a faint grey haze as the arms come down to the guard (the testbed then draws the stealth state).', [
     g(),
     g(an=SEAL_N, af=SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-130, -190), af=band(-120, -185), bob=(3, 3, 3), lean=(0, 2), **LOW),
     g(an=band(-130, -190), af=band(-120, -185), bob=(4, 4, 4), lean=(0, 3), **BRACE),
     g(an=band(-130, -190), af=band(-120, -185), bob=(4, 4, 4), lean=(0, 3), **BRACE),
     g(an=band(-130, -190), af=band(-120, -185), bob=(4, 4, 4), lean=(0, 3), **BRACE),
     g(an=band(-60, -130), af=band(-60, -140), bob=(3, 3, 3), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 0, 1, 2, 3, 1, 0],
  dict(auraColors=('#4a4a4a', '#9a9a9a'), opacity={
      'rule': 'Stealth (Christopher 2026-10-21): the caster turns invisible to everyone but its own player, who sees it see-through. Multiply the whole composited fighter (every layer, fx included) by self[k] when drawn for its own side and by others[k] for any other viewer; after the clip the Stealth state holds the last value (self 0.4, others 0) until Stealth ends.',
      'self': [1, 1, 1, 1, 1, 0.85, 0.6, 0.4], 'others': [1, 1, 1, 1, 1, 0.7, 0.3, 0]})),
 'earthWall': ('Earth Wall', 3,
  'Earth Wall (terrain: raise a stone barricade): from the guard the fighter raises both fists over the head, then drops low and slams both open palms down in front of the body, toward the ground, with the knees deep; a burst of dust kicks up at the ground in front where the wall rises (the wall itself is the terrain prop); then rises back into the guard.', [
     g(),
     g(an=band(-165, -175), af=band(-160, -170), bob=(0, 0, 0), lean=(0, -1), ln='stance-rear', lf='stance-lead'),
     g(an=band(-110, -100, fistKind='palm'), af=band(-100, -95, fistKind='palm'), bob=(2, 2, 2), lean=(1, 2)),
     g(an=band(-40, -25, fistKind='palm'), af=band(-34, -20, fistKind='palm'), bob=(5, 6, 6), lean=(0, 8), **BRACE),
     g(an=band(-40, -25, fistKind='palm'), af=band(-34, -20, fistKind='palm'), bob=(5, 6, 6), lean=(0, 8), **BRACE),
     g(an=band(-30, -90), af=band(-40, -100), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g()],
  [None, None, None, 'squint', 'squint', None, None],
  None,
  dict(fps=12, fx=nfx('white/neutral dust kicked up at the ground in front where the wall rises',
              [(3, [('dust', [44, 63])]), (4, [('dust', [46, 63]), ('spark', [52, 59])]), (5, [('shroud1', [48, 63])])]))),
 'shadowPossession': ('Shadow Possession', 3,
  'Shadow Possession (grapple: pin the foe\'s shadow): from the guard the fighter makes the seal at the chest and sinks low on bent knees, eyes narrowed and holding still; the fighter\'s shadow stretches out flat along the ground toward the target as a dark neutral-grey band, holds, then the hands part back into the guard (the testbed draws the shadow onward to the target and the root on both).', [
     g(),
     g(an=SEAL_N, af=SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-5, -140), af=band(-25, -145), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, fx=nfx('a dark neutral-grey shadow band stretching from the feet along the ground toward the target, edge of frame onward drawn by the testbed',
              [(2, [('shadow1', [38, 63])]), (3, [('shadow2', [38, 63])]), (4, [('shadow3', [38, 63])]), (5, [('shadow3', [38, 63])]), (6, [('shadow2', [38, 63])])]))),
 'summonCompanion': ('Summon Companion', 3,
  'Summon Companion (calls a Guardian-tier creature): from the guard the fighter makes the seal at the chest, then drops low on bent knees and slaps the open near palm down onto the ground in front; a big white/neutral smoke puff bursts up where the hand lands and spreads into a ring as it clears (the companion itself is placed by the testbed inside the puff); then rises back into the guard.', [
     g(),
     g(an=SEAL_N, af=SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-40, -25, fistKind='palm'), af=band(-20, -150), bob=(5, 6, 6), lean=(0, 8), **BRACE),
     g(an=band(-40, -25, fistKind='palm'), af=band(-20, -150), bob=(5, 6, 6), lean=(0, 8), **BRACE),
     g(an=band(-40, -25, fistKind='palm'), af=band(-20, -150), bob=(5, 6, 6), lean=(0, 8), **BRACE),
     g(an=band(-30, -90), af=band(-40, -100), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g()],
  [None, 'squint', 'squint', None, None, None, None, None],
  None,
  dict(fx=nfx('white/neutral summoning smoke: a spark at the seal, a big puff bursting up where the palm hits the ground in front, spreading into a ring as it clears',
              [(2, [('spark', [36, 30])]), (3, [('dust', [44, 63])]), (4, [('puffBig', [44, 63])]), (5, [('puffHuge', [40, 63])]), (6, [('puffHuge2', [39, 63])])]))),
 'phantomHaunt': ('Phantom Haunt', 3,
  'Phantom Haunt (genjutsu: a phantom only caster and victim see): from the guard the fighter raises the near hand with two fingers up in front of the eyes, fixes the target with narrowed eyes and holds still while the far hand stays in guard; a faint dotted pale-grey phantom slips out of the fighter and drifts away toward the target, growing as it goes (the testbed then draws it hounding the victim); the hand drops back into the guard.', [
     g(),
     g(an=band(-120, -160, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-120, -165, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-120, -165, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-120, -165, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-120, -165, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fx=nfx('a faint dotted pale-grey phantom slipping out of the fighter and drifting toward the target, growing as it goes',
              [(2, [('ghost1', [40, 32])]), (3, [('ghost2', [44, 36])]), (4, [('ghost3', [49, 38])]), (5, [('ghost3', [54, 38])])]))),
}

def spec(state):
    ab, act, intent, fr, ex, _, *more = CLIPS[state]
    x = more[0] if more else {}
    n = len(fr)
    ev = [{'frame': k, 'clip': state, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'} for k in range(n)]
    if x.get('react'): ev[act].update(react=True)
    elif x.get('release'): ev[act].update(move=ab, release=x['release'])
    elif x.get('hitbox'): ev[act].update(move=ab, hitbox=x['hitbox'], damage=x['damage'])
    else: ev[act].update(move=ab, buff=True)
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
              'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else {**e, 'release': [64 - e['release'][0], e['release'][1]]} if 'release' in e else dict(e) for e in ev]}
    clips = {'rule': 'starts and ends in the approved guard frame and returns to that idle (next: guard)',
             state: {'frames': list(range(n)), 'fps': 10, 'next': 'guard', 'ability': ab}}
    s = build(HR, state, fr, status=APPROVED.get(state, STAT), newPoses=POSES, clips=clips, events=events, rmRule=x.get('rm', 'in place'), intent=intent, fx=x.get('fx'))
    s['fps'] = clips[state]['fps'] = x.get('fps', 10); s.pop('approved', None); s.pop('keyPoses', None)
    if state == 'chargeChakra':   # meditative hold: the open hand lies flat, palm up, fingers forward (not the upright grip-hunt hand)
        s['arms']['band']['palmUp'] = {'use': 'open hand resting flat, palm up, fingers pointing forward (Charge Chakra meditative hold)', 'anchor': [0, 1], 'rows': ['.mLLLLm', 'mLLLLLL', '.sDDDsm']}
    if not x.get('fx'): s.pop('fx', None)
    if x.get('opacity'): s['opacity'] = x['opacity']
    s['expressions'] = copy.deepcopy(HR['expressions']); s['expressions']['frames'] = {'E': ex}
    s['expressions']['shapes']['closed'] = copy.deepcopy(CLOSED)   # eyes shut (focus)
    save(s, D + state + '.json'); print(state, n, 'frames')

def aura(state):
    x = (CLIPS[state][6:] or [{}])[0]; keep = grstrikes.AURA
    if x.get('auraColors'): grstrikes.AURA = x['auraColors']   # shadow techniques: dark neutral grey inside, mid grey outside
    from PIL import Image
    f = D + state + '/fx.png'; old = Image.open(f).convert('RGBA') if x.get('fx') and os.path.exists(f) else None   # the clip's own splash fx (rendered just before)
    grstrikes.CLIPS[state] = (None,) * 9 + (CLIPS[state][5],); grstrikes.aura(state); grstrikes.AURA = keep
    if old:
        new = Image.open(f).convert('RGBA'); new.alpha_composite(old); new.save(f)   # splash fx over the aura

def opacity(state):
    """copy the spec's per-frame whole-fighter opacity (stealth fade) into the rendered animation.json"""
    a = load(D + state + '/animation.json'); a['opacity'] = load(D + state + '.json')['opacity']; save(a, D + state + '/animation.json'); print(state, 'opacity')

def flow(state):
    """after --aura: the drained chakra running up the drainer's arms (Christopher 2026-10-21): on each grip frame the
    arm pixels from the hand back toward the shoulder turn chakra blue in bands that travel toward the shoulder, reaching
    the hands, then the elbows, then the whole arm (fx layer, over the arms)"""
    from PIL import Image
    x = CLIPS[state][6]; d = D + state + '/'; f = d + 'fx.png'
    fx = Image.open(f).convert('RGBA'); hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    lite, mid = hexc('#9cc0ff'), hexc(CHAKRA[0])
    arms = [Image.open(d + n).convert('RGBA') for n in ('arms.png', 'far-arm.png') if os.path.exists(d + n)]
    spec_ = load(D + state + '.json'); dirs = spec_['directions']
    for step, k in enumerate(x['flow']):
        reach = (5, 10, 64)[min(step, 2)]
        for d_ in ('E', 'W'):
            r = dirs.index(d_); sg = 1 if d_ == 'E' else -1
            for a in arms:
                pts = [(X, Y) for Y in range(64) for X in range(64) if (q := a.getpixel((k * 64 + X, r * 64 + Y)))[3] and q[:3] != (0, 0, 0)]
                if not pts: continue
                tip = max(sg * X for X, _ in pts)
                for X, Y in pts:
                    u = tip - sg * X   # distance back from the hand
                    if u > reach: continue
                    fx.putpixel((k * 64 + X, r * 64 + Y), lite if (u + 2 * step) % 4 < 2 else mid)
    fx.save(f); print(state, 'arm flow', x['flow'])

if __name__ == '__main__':
    if '--opacity' in sys.argv[1:]: opacity(sys.argv[sys.argv.index('--opacity') + 1]); sys.exit()
    if '--flow' in sys.argv[1:]: flow(sys.argv[sys.argv.index('--flow') + 1]); sys.exit()
    a = sys.argv[1:]
    if '--aura' in a: aura(a[a.index('--aura') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
