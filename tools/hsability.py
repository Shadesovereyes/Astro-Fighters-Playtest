"""Horse Stance as an ability (Christopher 2026-10-20: "treat it like Wrestler's Prowess, where the animation plays with a
subtle aura and then returns to the karate stance"): a one-shot power-up from the approved karateGuard frame. The lead
hand draws back to the hip as both feet slide into the straddle, the fighter sinks into the Horse Stance with both fists
chambered and roots there while a white/neutral aura swells and fades, then rises and steps back into the Karate stance.
One state (karateHorseStance). E/W first (W mirrors E), S/N after approval.
Run: python3 tools/hsability.py ; node tools/character-posed.mjs male karateHorseStance ; python3 tools/stances.py --outline karateHorseStance ; python3 tools/hsability.py --aura"""
import sys, copy
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
import grstrikes
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
KARATE = load(D + 'karateGuard.json')
def band(a, e): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
def leg(name, hip, knee, foot, wrap=56, kind='flat'):
    return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1], 'footX': foot, 'wrapRow': wrap, 'foot': kind}
STATE = 'karateHorseStance'
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'

HIP, LEAD = band(55, -60), band(-75, -95)   # karateGuard: rear fist chambered at the hip, lead hand out at chest height
POSES = [leg('hs-near', (31, 45), (38, 50), 35), leg('hs-far', (30, 45), (36, 50), 30),          # the approved horseStance straddle
         leg('hs-step-rear', (31, 44), (33, 50), 26), leg('hs-step-lead', (32, 44), (38, 50), 37)]   # halfway: rear foot sliding up, lead foot drawing back
KA = dict(an=HIP, af=LEAD, bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead')   # karateGuard frame 0
STEP = dict(an=HIP, bob=(4, 4, 4), lean=(0, 1), root=(0, 0), ln='hs-step-rear', lf='hs-step-lead')
HS = dict(an=HIP, af=HIP, lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far')
FRAMES = [KA,
          {**STEP, 'af': band(10, -70)},              # lead hand drawing back, feet sliding into the straddle
          {**HS, 'bob': (6, 6, 6)},                   # sinks into the Horse Stance, both fists at the hips
          {**HS, 'bob': (7, 7, 7)},                   # roots a row deeper as the aura rises
          {**HS, 'bob': (7, 7, 7)},
          {**HS, 'bob': (7, 8, 7)},                   # breath: head settles a row
          {**HS, 'bob': (7, 7, 7)},
          {**HS, 'bob': (6, 6, 6)},
          {**STEP, 'af': band(-40, -85)},             # rises and steps back, lead hand going out
          KA]
AURA = [0, 0, 1, 2, 3, 2, 1, 0, 0, 0]   # aura ring width per frame, same swell as Wrestler's Prowess
ACTIVE = 4

def spec():
    base = copy.deepcopy(KARATE); base.pop('frontal', None); base['directions'] = ['E', 'W']
    n = len(FRAMES)
    ev = [{'frame': k, 'clip': STATE, 'type': 'startup' if k < ACTIVE else 'active' if k == ACTIVE else 'recovery'} for k in range(n)]
    ev[ACTIVE].update(move='Horse Stance', buff=True)
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E)', 'E': ev, 'W': [dict(e) for e in ev]}
    clips = {'rule': 'starts and ends in the approved karateGuard frame and returns to that idle (next: karateGuard)',
             STATE: {'frames': list(range(n)), 'fps': 10, 'next': 'karateGuard', 'ability': 'Horse Stance'}}
    s = build(base, STATE, [dict(src=0, **f) for f in FRAMES], status=STAT, newPoses=POSES, clips=clips, events=events, rmRule='in place',
              intent="Horse Stance (power-up) from the Karate stance (Christopher 2026-10-20: played like Wrestler's Prowess, with a subtle aura, then back to the Karate stance): the lead hand draws back to the hip as the feet slide into a deep straddle; the fighter sinks into the Horse Stance, both fists chambered at the hips and the back upright, and roots there while a white/neutral aura swells and fades; then rises and steps back into the Karate stance.",
              extra={'stance': base.get('stance')})
    s['fps'] = 10; s.pop('approved', None); s.pop('keyPoses', None)
    save(s, D + STATE + '.json'); print(STATE, n, 'frames')

if __name__ == '__main__':
    if '--aura' in sys.argv:
        grstrikes.CLIPS[STATE] = (None,) * 9 + (AURA,); grstrikes.aura(STATE)
    else: spec()
