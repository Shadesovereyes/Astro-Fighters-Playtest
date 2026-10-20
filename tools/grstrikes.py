"""Judo and Wrestling stance strikes (Christopher 2026-10-20: every ability used from a stance must look right): clips that
start and end in the approved judoGuard / wrestlingGuard frame instead of the boxing guard, with the real techniques:
Judo Chop (open knife hand raised by the ear and chopped down onto the neck), standing Sumo Palm (near then far open-hand
thrust, heel of the palm leading, from the wrestling crouch) and Wrestler's Prowess (power-up: rises out of the crouch,
flexes both arms, stamps back down into the stance). Feet stay planted. One state per ability. E/W first (W mirrors E).
Run: python3 tools/grstrikes.py ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state>"""
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
 'wrestlingProwess': ("Wrestler's Prowess", 'wrestlingGuard', WREST, WPOSES, 3, None, None,
  "Wrestler's Prowess (power-up) from the Wrestling stance: the wrestler rises out of the crouch, chest up, and flexes both arms in a double biceps, upper arms level out front and behind with the fists curled up beside the head; holds the flex with a small shudder, then drops the hips and stamps back into the Wrestling stance.", [
     w(), w(an=band(-30, -80), af=band(-25, -60), **RISE),
     w(an=band(60, -175), af=band(-80, -165), **TALL),
     w(an=band(85, -175), af=band(-100, -160), bob=(1, 1, 0), lean=(0, 1), ln='wr-tall-rear', lf='wr-tall-lead'),
     w(an=band(85, -175), af=band(-100, -160), bob=(0, 0, 0), lean=(0, 1), ln='wr-tall-rear', lf='wr-tall-lead'),
     w(an=band(85, -175), af=band(-100, -160), bob=(1, 1, 0), lean=(0, 1), ln='wr-tall-rear', lf='wr-tall-lead'),
     w(an=band(-40, -90, **P), af=band(-30, -65, **P), **RISE),
     w(bob=(7, 8, 7), lean=(2, 10), ln='wr-rear-low', lf='wr-lead-low'), w()]),
}

def spec(state):
    ab, stance, B, poses, act, hb, dmg, intent, fr = CLIPS[state]
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
    s = build(base, state, [dict(src=0, **x) for x in fr], status=STAT, newPoses=poses, clips=clips, events=events,
              rmRule='E: x +1 on the drive into the strike' if hb else 'in place', intent=intent, extra={'stance': base.get('stance')})
    s['fps'] = 12; s.pop('approved', None); s.pop('keyPoses', None)
    save(s, D + state + '.json'); print(state, n, 'frames')

if __name__ == '__main__':
    for st in (sys.argv[1:] or CLIPS): spec(st)
