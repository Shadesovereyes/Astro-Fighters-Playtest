"""Karate stance strikes (Christopher 2026-10-20: every ability used from a stance must look right): clips that start and
end in the approved karateGuard frame (long front stance, lead hand out, rear fist chambered at the hip) instead of the
boxing guard, with the real techniques: Karate Blitz (superman punch gap closer with motion blur), Hammer Fist (overhead
swing down), Side Kick (chamber + heel thrust), Sweeping Low (rear foot sweeps along the floor) and Whirlwind Kick (the
approved spin roundhouse, entered and left from the Karate stance). The front foot stays planted through every strike
(Muay Thai rule, Christopher 2026-10-20). E/W first (W mirrors E); S/N after approval.
Run: python3 tools/kastrikes.py ; node tools/character-posed.mjs male <state> (each of STATES) ; python3 tools/stances.py --outline <state> ; python3 tools/kastrikes.py --blur (Karate Blitz motion blur fx)"""
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
APPROVED = {'karateHammerFist': 'E/W approved by user 2026-10-20 (W mirrors E); S/N to author', 'karateSideKick': 'E/W approved by user 2026-10-20 (W mirrors E); S/N to author', 'karateSweepingLow': 'E/W approved by user 2026-10-20 (W mirrors E); S/N to author'}

HIP = band(55, -60)        # rear fist chambered at the hip (the stance's hikite); near = rear arm, far = lead arm
LEAD = band(-75, -95)      # the stance's lead hand out at chest height
POSES = [pose(HEAVY, n) for n in ('lift', 'side-chamber', 'side', 'round', 'round-fold', 'lead-pivot')] + [
    flat('ka-lead-hi', (33, 42), (38, 49), 40),                    # the front leg with the body a row taller (kicks stand up on it)
    flat('ka-lead-low', (33, 44), (39, 50), 40),                   # the front knee sinking a row (punch drive, sweep)
    leg('sweep-mid', (32, 43), (35, 50), (40, 55), 'toe30k'),      # rear foot coming through low, just off the floor
    leg('sweep', (34, 43), (41, 50), (50, 55), 'blade'),
    leg('sm-load-rear', (31, 44), (37, 48), (34, 54), 'toe30k'),  # superman punch: rear knee driven forward to launch
    leg('sm-kick-rear', (31, 40), (25, 44), (19, 48), 'pointDL'), # rear leg kicked straight back in the air
    leg('sm-air-lead', (33, 40), (38, 45), (37, 51), 'toe30k'),   # lead leg tucked under the body in flight
    flat('sm-land-lead', (33, 42), (38, 49), 41),                  # lead foot lands flat, a step further on
    leg('sm-trail-rear', (31, 42), (25, 48), (21, 53), 'toe30k')]   # rear leg still trailing back, toes touching down           # leg long along the floor, foot hooked (sole forward, toes up) into the ankle

ST = dict(an=HIP, af=LEAD, bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead')   # karateGuard frame 0
def f(**k): return {**ST, **k}

CLIPS = {   # (ability, active frame, hitbox [x, y, w, h], damage, frames[, borrow {local frame: spec}])
 'supermanPunch': ('Karate Blitz', 3, [46, 23, 14, 8], 'light', [   # gap closer modelled on a superman punch (Christopher 2026-10-20): dip and drive the rear knee forward, leap with the rear leg kicked back and the rear fist cocked, fire the rear fist straight out in flight while the lead fist chambers at the hip (hikite, Christopher 2026-10-20), land on the lead foot a long step on, settle into the stance
     f(),
     f(an=band(20, -60), af=band(-60, -100), bob=(3, 3, 3), lean=(1, 3), root=(1, 0), ln='sm-load-rear', lf='ka-lead-low'),
     f(an=band(70, 150), af=band(-55, -95), bob=(-1, -1, -1), lean=(1, 4), root=(6, 0), ln='sm-kick-rear', lf='sm-air-lead'),
     f(an=band(-95, -95), af=HIP, bob=(-1, -1, -1), lean=(2, 6), root=(6, 0), ln='sm-kick-rear', lf='sm-air-lead'),
     f(an=band(-92, -92), af=HIP, bob=(1, 1, 1), lean=(2, 5), root=(3, 0), ln='sm-trail-rear', lf='sm-land-lead'),
     f(an=band(20, -50), af=band(-60, -100), bob=(2, 2, 2), lean=(1, 2), root=(1, 0)), f()]),
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
STATES = {'karateBlitz': ('supermanPunch',), 'karateHammerFist': ('hammerFist',), 'karateSideKick': ('sideKick',), 'karateSweepingLow': ('sweepingLow',), 'karateWhirlwind': ('whirlwindKick',)}   # one state per ability (Christopher 2026-10-20: impact frames get tuned per ability)

def spec(state, names):
    base = copy.deepcopy(BASE)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    for k in ('pointFwd', 'blade', 'toe30k', 'pointDL'): base['legs']['feet'].setdefault(k, copy.deepcopy(HEAVY['legs']['feet'][k]))
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
    if 'supermanPunch' in names: extra['airborneFrames'] = [2, 3]; extra['travel'] = {'rule': 'Karate Blitz is a gap closer: the fighter ends the clip 18 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 18}
    if borrow: extra['borrow'] = {'rule': copy.deepcopy(HEAVY['borrow']['rule']), 'frames': borrow}
    s = build(base, state, frames, status=APPROVED.get(state, STAT), newPoses=POSES + [pose(HEAVY, 'stance-lead'), pose(HEAVY, 'stance-rear')], clips=clips, events=events,
              rmRule='E: x +1 on the drive into each strike',
              intent='Karate stance strikes: Karate Blitz (lead punch, then reverse punch with the lead fist pulled back to the hip), Hammer Fist (rear fist swung over the head and down, body dropping), Side Kick (side chamber, heel thrust, torso back), Sweeping Low (sink on the front leg, rear foot sweeps along the floor and hooks) and Whirlwind Kick (the approved spin roundhouse). Every clip starts and ends in the approved Karate stance frame; the front foot stays planted.',
              extra=extra)
    s['fps'] = 12; s.pop('approved', None); s.pop('keyPoses', None)
    save(s, D + state + '.json'); print(state, i, 'frames', ' '.join(names))

BLUR = {2: 7, 3: 10, 4: 6}   # supermanPunch frame: streak length behind the figure (motion blur, neutral whites like the Prowess aura)
def blur(state='karateBlitz'):
    """after render + outline: horizontal speed streaks on the fx layer trailing behind the figure (body, arms, gi) in the flight frames"""
    from PIL import Image
    d = D + state + '/'
    lay = [Image.open(d + f).convert('RGBA') for f in ('body.png', 'arms.png', 'male-gi.png')]
    W, H = lay[0].size; fx = Image.new('RGBA', (W, H)); px = fx.load(); al = [l.load() for l in lay]
    for k, L in BLUR.items():
        for r, sign in ((0, 1), (1, -1)):   # rows E, W; the back of the figure is to the left in E, the right in W
            for y in range(64):
                xs = [x for x in range(64) if any(a[k * 64 + x, r * 64 + y][3] for a in al)]
                if not xs or y % 2: continue
                edge = min(xs) if sign > 0 else max(xs)
                n = L - (y * 7 + k) % 4   # ragged ends
                for i in range(2, 2 + n):
                    x = edge - sign * i
                    if 0 <= x < 64: px[k * 64 + x, r * 64 + y] = (255, 255, 255, 255) if i < 2 + n // 2 else (0xe3, 0xe3, 0xe3, 255)
    fx.save(d + 'fx.png'); print(state, 'motion blur', BLUR)

if __name__ == '__main__':
    if '--blur' in sys.argv: blur()
    else:
        for st, names in STATES.items(): spec(st, names)
