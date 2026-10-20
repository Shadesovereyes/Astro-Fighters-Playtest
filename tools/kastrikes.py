"""Karate stance strikes (Christopher 2026-10-20: every ability used from a stance must look right): clips that start and
end in the approved karateGuard frame (long front stance, lead hand out, rear fist chambered at the hip) instead of the
boxing guard, with the real techniques: Karate Blitz (lunge punch + reverse punch with hikite), Hammer Fist (overhead
swing down), Side Kick (chamber + heel thrust), Sweeping Low (rear foot sweeps along the floor) and Whirlwind Kick (the
approved spin roundhouse, entered and left from the Karate stance). The front foot stays planted through every strike
(Muay Thai rule, Christopher 2026-10-20). E/W first (W mirrors E); S/N after approval.
Run: python3 tools/kastrikes.py ; node tools/character-posed.mjs male <state> (each of STATES)"""
import sys, copy
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
BASE = load(D + 'karateGuard.json')
HEAVY = load(D + 'heavyAttack.json')
def band(a, e): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
def leg(name, hip, knee, ankle, foot): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'ankle': list(ankle), 'foot': foot}
def flat(name, hip, knee, foot, wrap=56, kind='flat'): return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'footX': foot, 'wrapRow': wrap, 'foot': kind}
def pose(spec, name): return copy.deepcopy(next(p for p in spec['legs']['poses'] if p['name'] == name))
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'

HIP = band(55, -60)        # rear fist chambered at the hip (the stance's hikite); near = rear arm, far = lead arm
LEAD = band(-75, -95)      # the stance's lead hand out at chest height
POSES = [pose(HEAVY, n) for n in ('lift', 'side-chamber', 'side', 'round', 'round-fold', 'lead-pivot')] + [
    flat('ka-lead-hi', (33, 42), (38, 49), 40),                    # the front leg with the body a row taller (kicks stand up on it)
    flat('ka-lead-low', (33, 44), (39, 50), 40),                   # the front knee sinking a row (punch drive, sweep)
    leg('sweep-mid', (32, 43), (35, 50), (40, 55), 'toe30k'),      # rear foot coming through low, just off the floor
    leg('sweep', (34, 43), (41, 50), (50, 55), 'blade')]           # leg long along the floor, foot hooked (sole forward, toes up) into the ankle

ST = dict(an=HIP, af=LEAD, bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead')   # karateGuard frame 0
def f(**k): return {**ST, **k}

CLIPS = {   # (ability, active frame, hitbox [x, y, w, h], damage, frames[, borrow {local frame: spec}])
 'leadPunch': ('Karate Blitz', 2, [44, 27, 12, 6], 'light', [   # lead fist snaps back, then drives straight out as the front knee sinks
     f(), f(af=band(-55, -140), lean=(0, 2)),
     f(af=band(-92, -92), bob=(3, 3, 3), lean=(1, 3), root=(1, 0), lf='ka-lead-low'), f(af=band(-80, -100))]),
 'reversePunch': ('Karate Blitz', 2, [44, 27, 12, 6], 'light', [   # gyaku-zuki: rear fist from the hip, lead fist pulled back to its hip (hikite), hips square
     f(an=band(10, -40), af=band(-40, -80), lean=(1, 2)),
     f(an=band(-60, -75), af=band(25, -40), bob=(3, 3, 3), lean=(1, 3), lf='ka-lead-low'),
     f(an=band(-92, -92), af=band(55, -60), bob=(3, 3, 3), lean=(2, 4), root=(1, 0), lf='ka-lead-low'),
     f(an=band(20, -50), af=band(-60, -100), lean=(1, 2)), f()]),
 'hammerFist': ('Hammer Fist', 3, [42, 26, 12, 14], 'heavy', [   # rear fist swung up over the head, then down onto the target; the body drops into it
     f(), f(an=band(150, 175), af=band(-70, -110), bob=(1, 1, 1), lean=(0, 0)),
     f(an=band(-150, -130), af=band(-30, -70), bob=(2, 2, 2), lean=(1, 2)),
     f(an=band(-95, -55), af=band(45, -60), bob=(3, 3, 3), lean=(2, 4), root=(1, 0), lf='ka-lead-low'),
     f(an=band(-90, -45), af=band(55, -60), bob=(3, 3, 3), lean=(2, 4), lf='ka-lead-low'),
     f(an=band(10, -50), af=band(-60, -100), lean=(1, 2)), f()]),
 'sideKick': ('Side Kick', 3, [46, 34, 12, 10], 'heavy', [   # rear knee up and across into the side chamber, heel thrust out, torso leaning well back
     f(), f(bob=(1, 1, 1), lean=(0, 0), ln='lift', lf='ka-lead-hi'),
     f(af=band(-60, -80), bob=(0, 0, 1), lean=(0, -2), ln='side-chamber', lf='lead-pivot'),
     f(af=band(-55, -70), bob=(0, 0, 1), lean=(1, -5), root=(1, 0), ln='side', lf='lead-pivot'),
     f(af=band(-55, -70), bob=(0, 0, 1), lean=(1, -5), ln='side', lf='lead-pivot'),
     f(af=band(-60, -80), bob=(0, 0, 1), lean=(0, -2), ln='side-chamber', lf='lead-pivot'),
     f(bob=(1, 1, 1), ln='lift', lf='ka-lead-hi'), f()]),
 'sweepingLow': ('Sweeping Low', 3, [40, 50, 18, 8], 'heavy', [   # sink on the front leg, the rear foot sweeps forward along the floor and hooks the ankle
     f(), f(bob=(3, 3, 3), lean=(0, 1), lf='ka-lead-low'),
     f(af=band(-50, -70), bob=(3, 3, 3), lean=(1, 0), ln='sweep-mid', lf='ka-lead-low'),
     f(af=band(10, -50), bob=(3, 3, 3), lean=(1, -2), root=(1, 0), ln='sweep', lf='ka-lead-low'),
     f(af=band(10, -50), bob=(3, 3, 3), lean=(1, -2), ln='sweep', lf='ka-lead-low'),
     f(bob=(3, 3, 3), lean=(0, 0), ln='sweep-mid', lf='ka-lead-low'), f()]),
 'whirlwindKick': ('Whirlwind Kick', 4, [44, 20, 16, 12], 'heavy', [   # the approved spin roundhouse (spin frames borrowed from spinPivot), entered and left from the Karate stance
     f(), f(an=band(-20, 212), af=band(-45, 222), bob=(1, 1, 1), lean=(0, 0), ln='stance-rear', lf='stance-lead'),
     f(an=band(-20, 212), af=band(-45, 222), bob=(1, 1, 1), lean=(0, 0), ln='stance-rear', lf='stance-lead'),
     f(an=band(-20, 212), af=band(-45, 222), bob=(1, 1, 1), lean=(0, 0), ln='stance-rear', lf='stance-lead'),
     f(an=band(25, 20), af=band(-45, 222), bob=(0, 0, 0), lean=(0, -6), ln='round', lf='stance-lead'),
     f(an=band(25, 20), af=band(-45, 222), bob=(0, 0, 0), lean=(0, -3), ln='round-fold', lf='stance-lead'), f()],
     {1: ('S', 0, 2), 2: ('W', 0, 2), 3: ('N', 1, 2)}),
}
STATES = {'karateBlitz': ('leadPunch', 'reversePunch'), 'karateHammerFist': ('hammerFist',), 'karateSideKick': ('sideKick',), 'karateSweepingLow': ('sweepingLow',), 'karateWhirlwind': ('whirlwindKick',)}   # one state per ability (Christopher 2026-10-20: impact frames get tuned per ability)

def spec(state, names):
    base = copy.deepcopy(BASE)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    for k in ('pointFwd', 'blade', 'toe30k'): base['legs']['feet'].setdefault(k, copy.deepcopy(HEAVY['legs']['feet'][k]))
    frames, clips, ev, borrow, i = [], {'rule': 'Karate strikes: each clip starts and ends in the approved karateGuard frame and returns to that idle (next: karateGuard)'}, [], {}, 0
    for c in names:
        ab, act, hb, dmg, fr, *bw = CLIPS[c]
        n = len(fr); clips[c] = {'frames': list(range(i, i + n)), 'fps': 12, 'next': 'karateGuard', 'ability': ab}
        for k in range(n):
            e = {'frame': i + k, 'clip': c, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'}
            if k == act: e.update(move=ab, hitbox=hb, damage=dmg)
            ev.append(e)
        for k, (d, sf, dx) in (bw[0] if bw else {}).items(): borrow[str(i + k)] = {'state': 'spinPivot', 'dir': d, 'frame': sf, 'dx': dx}
        frames += [dict(src=0, **x) for x in fr]; i += n
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
              'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    extra = {'stance': 'Karate Stance'}
    if borrow: extra['borrow'] = {'rule': copy.deepcopy(HEAVY['borrow']['rule']), 'frames': borrow}
    s = build(base, state, frames, status=STAT, newPoses=POSES + [pose(HEAVY, 'stance-lead'), pose(HEAVY, 'stance-rear')], clips=clips, events=events,
              rmRule='E: x +1 on the drive into each strike',
              intent='Karate stance strikes: Karate Blitz (lead punch, then reverse punch with the lead fist pulled back to the hip), Hammer Fist (rear fist swung over the head and down, body dropping), Side Kick (side chamber, heel thrust, torso back), Sweeping Low (sink on the front leg, rear foot sweeps along the floor and hooks) and Whirlwind Kick (the approved spin roundhouse). Every clip starts and ends in the approved Karate stance frame; the front foot stays planted.',
              extra=extra)
    s['fps'] = 12; s.pop('approved', None); s.pop('keyPoses', None)
    save(s, D + state + '.json'); print(state, i, 'frames', ' '.join(names))

if __name__ == '__main__':
    for st, names in STATES.items(): spec(st, names)
