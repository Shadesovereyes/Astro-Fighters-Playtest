"""Judo and Wrestling stance strikes (Christopher 2026-10-20: every ability used from a stance must look right): clips that
start and end in the approved judoGuard / wrestlingGuard frame instead of the boxing guard, with the real techniques:
Judo Chop (open knife hand raised by the ear and chopped down onto the neck), standing Sumo Palm (near then far open-hand
thrust, heel of the palm leading, from the wrestling crouch) and Wrestler's Prowess (power-up: rises out of the crouch,
flexes both arms, stamps back down into the stance). Feet stay planted. One state per ability. E/W first (W mirrors E).
Run: python3 tools/grstrikes.py ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ; python3 tools/grstrikes.py --aura (Prowess fx)"""
import sys, copy
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
JUDO, WREST = load(D + 'judoGuard.json'), load(D + 'wrestlingGuard.json')
def band(a, e, **k): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def leg(name, hip, knee, foot, wrap=56, kind='flat'):
    return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'footX': foot, 'wrapRow': wrap, 'foot': kind}
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {'judoChop': 'E/W approved by user 2026-10-20 (W mirrors E); S/N to author', 'wrestlingSumoPalm': 'E/W approved by user 2026-10-20 (W mirrors E); S/N to author', 'wrestlingProwess': 'E/W approved by user 2026-10-20 (W mirrors E); S/N to author'}
P, H = dict(fistKind='palm'), dict(fistKind='heel')
PALM_HEEL = {'use': 'open hand, heel of the palm leading a straight thrust, fingers together and up (standing Sumo Palm)', 'anchor': [0, 4],
             'rows': ['.Lm.', 'LLm.', 'LLm.', 'LLLm', 'LLLm', 'mLLs', '.sDs']}

# Judo: judoGuard frame 0; near = rear hand (lapel), far = lead hand (sleeve)
JST = dict(an=band(-55, -88, **P), af=band(-72, -96, **P), bob=(1, 1, 2), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead')
def j(**k): return {**JST, **k}
JPOSES = [leg('ju-lead-low', (32, 43), (37, 50), 39), leg('ju-rear-low', (31, 43), (29, 51), 24)]   # knees sink a row into the chop
# Wrestling: wrestlingGuard frame 0
WST = dict(an=band(-45, -105, **P), af=band(-35, -70, **P), bob=(6, 6, 7), lean=(2, 10), root=(0, 0), ln='wr-rear', lf='wr-lead')
def w(**k): return {**WST, **k}
WPOSES = [leg('wr-rise-lead', (33, 44), (38, 50), 38), leg('wr-rise-rear', (31, 44), (30, 51), 23),   # half out of the crouch
          leg('wr-tall-lead', (32, 42), (36, 50), 38), leg('wr-tall-rear', (31, 42), (29, 50), 23)]   # standing tall, same feet
RISE, TALL = dict(bob=(3, 3, 4), lean=(1, 5), ln='wr-rise-rear', lf='wr-rise-lead'), dict(bob=(1, 1, 1), lean=(0, 1), ln='wr-tall-rear', lf='wr-tall-lead')

CLIPS = {   # state: (ability, stance state, base, poses, active frame, hitbox [x, y, w, h], damage, intent, frames)
 'judoChop': ('Judo Chop', 'judoGuard', JUDO, JPOSES, 3, [42, 22, 12, 10], 'light',
  'Judo Chop from the Judo stance: the rear open hand rises to beside the ear, palm in, then chops down and forward with the edge of the hand onto the side of the neck while the lead hand draws back to the chest and the knees sink; then back to the Judo stance.', [
     j(), j(an=band(140, 190, **P), af=band(-60, -100, **P), bob=(1, 1, 1), lean=(0, 1)),
     j(an=band(-175, -165, **P), af=band(-30, -80, **P), bob=(1, 1, 1), lean=(1, 2)),
     j(an=band(-100, -50, **P), af=band(10, -60, **P), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), ln='ju-rear-low', lf='ju-lead-low'),
     j(an=band(-95, -45, **P), af=band(10, -60, **P), bob=(2, 2, 2), lean=(1, 4), ln='ju-rear-low', lf='ju-lead-low'),
     j(an=band(-60, -90, **P), af=band(-50, -90, **P), bob=(1, 1, 2), lean=(0, 3)), j()]),
 'wrestlingSumoPalm': ('Sumo Palm', 'wrestlingGuard', WREST, WPOSES, 2, [44, 26, 12, 8], 'heavy',
  'Standing Sumo Palm from the Wrestling stance (tsuppari): the near open hand draws back to the chest and drives straight out at chest height with the heel of the palm leading, fingers up; it pulls back as the far hand drives out the same way; the crouch rises a little so the thrusts run level, then sinks back into the Wrestling stance.', [
     w(), w(an=band(-20, -150, **H), bob=(5, 5, 6), lean=(2, 8)),
     w(an=band(-88, -88, **H), af=band(-20, -130, **P), bob=(5, 5, 5), lean=(2, 8), root=(1, 0)),
     w(an=band(-30, -140, **H), af=band(-30, -150, **H), bob=(5, 5, 6), lean=(2, 8)),
     w(an=band(-35, -130, **P), af=band(-95, -95, **H), bob=(5, 5, 5), lean=(3, 9), root=(1, 0)),
     w(an=band(-40, -110, **P), af=band(-35, -100, **P), bob=(6, 6, 6), lean=(2, 9)), w()]),
 'wrestlingProwess': ("Wrestler's Prowess", 'wrestlingGuard', WREST, WPOSES, 4, None, None,
  "Wrestler's Prowess (power-up) from the Wrestling stance (Christopher 2026-10-20: a downward chest press with a bulking effect and an aura): the wrestler comes half out of the crouch, hunches over, brings both fists together in front of the chest and presses them down in front of the belly, crunching the chest; the arms thicken as he bulks up and holds the press with a shudder while an aura swells around him in pulses, then he sinks back into the Wrestling stance as the aura fades.", [
     w(),
     w(an=band(-40, -85, **P), af=band(-30, -70, **P), **RISE),
     w(an=band(-85, -150), af=band(-80, -155), bob=(3, 3, 3), lean=(1, 5), ln='wr-rise-rear', lf='wr-rise-lead'),
     w(an=band(-62, -8, band={'thickness': 5}), af=band(-58, -4, band={'thickness': 5}), bob=(4, 4, 4), lean=(1, 6), ln='wr-rise-rear', lf='wr-rise-lead'),
     w(an=band(-62, -8, band={'thickness': 6}), af=band(-58, -4, band={'thickness': 6}), bob=(4, 4, 5), lean=(1, 6), ln='wr-rise-rear', lf='wr-rise-lead'),
     w(an=band(-62, -8, band={'thickness': 6}), af=band(-58, -4, band={'thickness': 6}), bob=(3, 4, 4), lean=(1, 6), ln='wr-rise-rear', lf='wr-rise-lead'),
     w(an=band(-62, -8, band={'thickness': 6}), af=band(-58, -4, band={'thickness': 6}), bob=(4, 4, 5), lean=(1, 6), ln='wr-rise-rear', lf='wr-rise-lead'),
     w(an=band(-40, -40, **P, band={'thickness': 5}), af=band(-32, -45, **P, band={'thickness': 5}), **RISE),
     w(bob=(7, 8, 7), lean=(2, 10), ln='wr-rear-low', lf='wr-lead-low'), w()],
     [0, 0, 0, 1, 2, 3, 2, 1, 0, 0]),   # aura ring width per frame (fx layer, drawn after render by aura())
}

def spec(state):
    ab, stance, B, poses, act, hb, dmg, intent, fr, *_ = CLIPS[state]
    base = copy.deepcopy(B); base.pop('frontal', None); base['directions'] = ['E', 'W']
    base['arms']['band']['palmHeel'] = copy.deepcopy(PALM_HEEL)
    n = len(fr)
    ev = [{'frame': k, 'clip': state, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'} for k in range(n)]
    if hb: ev[act].update(move=ab, hitbox=hb, damage=dmg)
    else: ev[act].update(move=ab, buff=True)
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
              'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    clips = {'rule': f'starts and ends in the approved {stance} frame and returns to that idle (next: {stance})',
             state: {'frames': list(range(n)), 'fps': 12, 'next': stance, 'ability': ab}}
    s = build(base, state, [dict(src=0, **x) for x in fr], status=APPROVED.get(state, STAT), newPoses=poses, clips=clips, events=events,
              rmRule='E: x +1 on the drive into the strike' if hb else 'in place', intent=intent, extra={'stance': base.get('stance')})
    s['fps'] = 12; s.pop('approved', None); s.pop('keyPoses', None)
    save(s, D + state + '.json'); print(state, n, 'frames')

AURA = ('#ffffff', '#e3e3e3')   # white next to the body, light neutral grey outside (Christopher 2026-10-20: white/neutral aura; the fx palette's whites)
def aura(state):
    """after render + outline: an aura on the fx layer, `w` pixels wide around the whole figure (every layer but fx),
    inner ring white, outer rings light grey; drawn behind nothing, so it only shows outside the silhouette"""
    import os
    from PIL import Image, ImageFilter
    widths = CLIPS[state][9]; d = D + state + '/'
    lay = [Image.open(d + f).convert('RGBA') for f in sorted(os.listdir(d)) if f in ('body.png', 'arms.png', 'male-gi.png')]   # base figure + gi only: hair and armour variants would bloat it
    W, Hh = lay[0].size; fx = Image.new('RGBA', (W, Hh)); px = fx.load()
    for k, wd in enumerate(widths):
        if not wd: continue
        for r in range(Hh // 64):
            box = (k * 64, r * 64, k * 64 + 64, r * 64 + 64)
            m = Image.new('L', (64, 64))
            for l in lay: m.paste(255, (0, 0), l.crop(box).getchannel('A').point(lambda v: 255 if v else 0))
            prev = m
            for ring in range(wd):
                grown = prev.filter(ImageFilter.MaxFilter(3)); gp, pp = grown.load(), prev.load()
                c = AURA[0] if ring == 0 else AURA[1]
                for y in range(64):
                    for x in range(64):
                        if gp[x, y] and not pp[x, y] and (ring < wd - 1 or (x + y + k) % 2 == 0):   # the outermost ring flickers (every other pixel)
                            px[box[0] + x, box[1] + y] = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
                prev = grown
    fx.save(d + 'fx.png'); print(state, 'aura', widths)

if __name__ == '__main__':
    if '--aura' in sys.argv: aura('wrestlingProwess')
    else:
        for st in (sys.argv[1:] or CLIPS): spec(st)
