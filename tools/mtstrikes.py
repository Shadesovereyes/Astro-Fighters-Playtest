"""Muay Thai stance strikes (Christopher 2026-10-20: every ability used from a stance must look right): states
(the renderer caps a state at 16 frames) whose clips start and end in the approved muayThaiGuard frame (MT legs, lead heel up) instead of the
boxing guard, and replace the stand-ins with the real techniques (roundhouse, teep, knee, elbow, uppercut).
E/W first (W mirrors E); S/N after approval.
Run: python3 tools/mtstrikes.py ; node tools/character-posed.mjs male <state> (each of STATES)"""
import sys, copy, json
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
BASE = load(D + 'muayThaiGuard.json')
HEAVY, LIGHT = load(D + 'heavyAttack.json'), load(D + 'lightAttack.json')
def band(a, e): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
def leg(name, hip, knee, ankle, foot): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'ankle': list(ankle), 'foot': foot}
def pose(spec, name): return copy.deepcopy(next(p for p in spec['legs']['poses'] if p['name'] == name))
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'

GN, GF = band(-20, 212), band(-45, 222)          # the approved Muay Thai guard arms (near = rear hand, far = lead hand)
POSES = [pose(LIGHT, 'cross-lead'), pose(LIGHT, 'cross-rear')] + [pose(HEAVY, n) for n in ('lift', 'chamber', 'round-fold', 'low-kick', 'low-recoil', 'lead-pivot')] + [
    {**pose(HEAVY, 'lead-pivot'), 'name': 'mt-pivot', 'wrapRow': 54, 'foot': 'toe60'},   # support foot up on the ball, turning out
    {**pose(BASE, 'mt-lead'), 'name': 'mt-lead-flat', 'wrapRow': 56, 'foot': 'flat'},   # lead foot planted flat for punches (Christopher 2026-10-20)
    leg('mt-round', (34, 40), (42, 35), (51, 30), 'pointFwd'),     # rear shin swung through at rib height, leg nearly straight
    leg('teep-chamber', (34, 40), (40, 34), (40, 42), 'toe30k'),   # knee pulled to the chest, shin hanging under it
    leg('teep', (35, 40), (44, 37), (52, 37), 'blade'),            # leg pushed out level, sole flat to the target
    leg('mt-knee', (35, 40), (46, 33), (40, 43), 'toe30k')]        # knee driven up and through, heel tucked to the seat

ST = dict(an=GN, af=GF, bob=(1, 1, 2), lean=(0, 2), root=(0, 0), ln='mt-rear', lf='mt-lead')   # muayThaiGuard frame 0
def f(**k): return {**ST, **k}
def p(**k): return {**ST, 'lf': 'mt-lead-flat', **k}   # strike frames: the lead heel comes down and stays down until the clip returns to the stance (Christopher 2026-10-20, punches and near-leg kicks)

CLIPS = {   # (clip, ability, active frame, hitbox [x, y, w, h], damage, frames)
 'jab': ('Jab-Cross', 1, [44, 26, 12, 6], 'light', [
     f(), p(af=band(-93, -93), lean=(0, 3), root=(1, 0)), p(af=band(-50, 235)), f()]),
 'cross': ('Jab-Cross', 1, [44, 26, 12, 6], 'light', [
     p(an=band(-8, 205), lean=(0, 3)), p(an=band(-92, -92), bob=(2, 2, 2), lean=(1, 5), root=(1, 0), ln='cross-rear', lf='cross-lead'), p(an=band(-55, 230), lean=(0, 3)), f()]),
 'calfKick': ('Calf Kick', 2, [42, 46, 16, 10], 'heavy', [
     p(lean=(0, 1)), p(bob=(0, 0, 1), lean=(0, 0), ln='lift'),
     p(an=band(25, 20), bob=(0, 0, 1), lean=(1, -2), root=(1, 0), ln='low-kick', lf='lead-pivot'),
     p(bob=(0, 0, 1), lean=(0, -1), ln='low-recoil', lf='lead-pivot'), f()]),
 'roundhouse': ('Roundhouse Kick', 3, [44, 28, 14, 10], 'heavy', [   # rear arm swings down and back as the hip turns over; lead hand stays up
     f(), p(an=band(-5, 190), bob=(0, 0, 1), lean=(0, 1), ln='lift', lf='lead-pivot'),
     p(an=band(30, 40), bob=(0, 0, 1), lean=(1, -1), ln='round-fold', lf='lead-pivot'),
     p(an=band(40, 30), af=band(-60, 200), bob=(0, 0, 1), lean=(1, -4), root=(1, 0), ln='mt-round', lf='lead-pivot'),
     p(an=band(40, 30), af=band(-60, 200), bob=(0, 0, 1), lean=(1, -4), ln='mt-round', lf='lead-pivot'),
     p(an=band(10, 60), bob=(0, 0, 1), lean=(0, -1), ln='round-fold', lf='lead-pivot'), p(an=band(-10, 200), ln='lift'), f()]),
 'teep': ('Teep Kick', 2, [46, 34, 12, 10], 'heavy', [   # knee to the chest, hips pushed through, torso leaning back
     f(), p(bob=(0, 0, 1), lean=(0, 0), ln='teep-chamber'),
     p(bob=(0, 0, 1), lean=(2, -3), root=(1, 0), ln='teep'), p(bob=(0, 0, 1), lean=(2, -3), ln='teep'),
     p(bob=(0, 0, 1), lean=(0, 0), ln='teep-chamber'), f()]),
 'knee': ('Knee Strikes', 3, [44, 32, 10, 10], 'heavy', [   # hands reach up and pull down as the rear knee drives up, lead foot planted
     f(), p(an=band(-75, -120), af=band(-85, -125), bob=(0, 0, 1), lean=(1, 3), ln='lift'),
     p(an=band(-70, -100), af=band(-80, -110), bob=(0, 0, 1), lean=(2, 1), root=(1, 0), ln='chamber'),
     p(an=band(-55, -70), af=band(-65, -85), bob=(0, 0, 0), lean=(3, -1), ln='mt-knee'),
     p(an=band(-55, -70), af=band(-65, -85), bob=(0, 0, 0), lean=(3, -1), ln='mt-knee'),
     p(an=band(-40, 230), af=GF, bob=(0, 0, 1), lean=(1, 1), ln='lift'), f()]),
 'elbow': ('Elbow Strike', 2, [42, 22, 10, 8], 'heavy', [   # rear elbow carried level across, forearm folded back to the head
     f(), p(an=band(-55, -155), lean=(1, 3)),
     f(an=band(-105, 95), bob=(2, 2, 2), lean=(1, 3), root=(1, 0), ln='cross-rear', lf='cross-lead'),
     f(an=band(-103, 97), bob=(2, 2, 2), lean=(1, 3), ln='cross-rear', lf='cross-lead'),
     p(an=band(-55, 230), lean=(0, 3)), f()]),
 'uppercut': ('Uppercut', 3, [42, 20, 10, 10], 'heavy', [   # knees dip and the rear fist drops, then the body rises through it
     f(), p(an=band(-5, 200), bob=(2, 2, 2), lean=(1, 3)),
     f(an=band(-40, -150), bob=(1, 1, 1), lean=(1, 3), ln='cross-rear', lf='cross-lead'),
     f(an=band(-62, -162), bob=(1, 0, 1), lean=(1, 2), root=(1, 0), ln='cross-rear', lf='cross-lead'),
     p(an=band(-70, -140), bob=(1, 1, 1), lean=(1, 3)), f()]),
}

STATES = {'muayThaiPunch': ('jab', 'cross', 'uppercut'), 'muayThaiKick': ('calfKick', 'roundhouse'), 'muayThaiTeepKnee': ('teep', 'knee'), 'muayThaiElbow': ('elbow',)}

def spec(state, names):
    base = copy.deepcopy(BASE)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    for k in ('pointFwd', 'blade', 'toe30k'): base['legs']['feet'].setdefault(k, copy.deepcopy(HEAVY['legs']['feet'][k]))
    frames, clips, ev, i = [], {'rule': 'Muay Thai strikes: each clip starts and ends in the approved muayThaiGuard frame and returns to that idle (next: muayThaiGuard)'}, [], 0
    for c in names:
        ab, act, hb, dmg, fr = CLIPS[c]
        n = len(fr); clips[c] = {'frames': list(range(i, i + n)), 'fps': 12, 'next': 'muayThaiGuard', 'ability': ab}
        for k in range(n):
            e = {'frame': i + k, 'clip': c, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'}
            if k == act: e.update(move=ab, hitbox=hb, damage=dmg)
            ev.append(e)
        frames += [dict(src=0, **x) for x in fr]; i += n
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
              'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    s = build(base, state, frames, status=STAT, newPoses=POSES, clips=clips, events=events, rmRule='E: x +1 on the step into each strike',
              intent='Muay Thai stance strikes: Jab-Cross, Calf Kick, Roundhouse (rear shin swung through at rib height, rear arm swinging down and back), Teep (knee to the chest then a flat-soled push, torso back), Knee (hands reach and pull down, rear knee driven up, lead foot planted), Elbow (rear elbow level across, forearm folded) and Uppercut (dip then rise). Every clip starts and ends in the approved Muay Thai guard frame.',
              extra={'stance': 'Muay Thai Stance'})
    s['fps'] = 12; s.pop('approved', None); s.pop('keyPoses', None)
    save(s, D + state + '.json'); print(state, i, 'frames', ' '.join(names))

if __name__ == '__main__':
    for st, names in STATES.items(): spec(st, names)
