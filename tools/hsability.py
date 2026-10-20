"""Horse Stance as an ability (Christopher 2026-10-20: "treat it like Wrestler's Prowess, where the animation plays with a
subtle aura and then returns to the karate stance"): a one-shot power-up from the approved karateGuard frame. The lead
hand draws back to the hip as both feet slide into the straddle, the fighter sinks into the Horse Stance with both fists
chambered and roots there while a white/neutral aura swells and fades, then rises and steps back into the Karate stance.
One state (karateHorseStance). E/W first (W mirrors E), S/N after approval.
Run: python3 tools/hsability.py ; node tools/character-posed.mjs male karateHorseStance ; python3 tools/stances.py --outline karateHorseStance ; python3 tools/hsability.py --aura"""
import sys, copy
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grstrikes, stances
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

# ---------- S/N ----------
# Base: the approved karateGuard front/back view (stances.frontal) on every frame. The horse frames swap the legs for the
# straddle seen head-on: the reference trouser legs with row drops only, each leg sheared out from the hip to the foot
# (footDx, a straight line, no kink) plus a small knee push peaking at the knee row so the shin stands near vertical over
# the foot and the trouser bottoms hang straight (Christopher 2026-10-20: the idle's low knee shear flared the hem).
# Both legs drop the same crouch rows, the body squares to the viewer (no blade twist) and both fists chamber at the hips.
HS_SN = dict(foot=4, knee=1, kneeRow=49)
STEP_SN = dict(foot=2, knee=0, kneeRow=49)
LEGS_SN = {1: STEP_SN, 2: HS_SN, 3: HS_SN, 4: HS_SN, 5: HS_SN, 6: HS_SN, 7: HS_SN, 8: STEP_SN}
HIP_S = {'R': (14, -12, 0.6, 'up'), 'L': (-14, 12, 0.6, 'up')}   # fists at the hips on E's fist rows (projection: E fist rows 35-39)
ARM_SN = {'S': {1: {'L': (30, None, 0.6, 'front')}, 8: {'L': (40, None, 0.55, 'front')}, **{k: {'R': HIP_S['R'], 'L': HIP_S['L']} for k in range(2, 8)}},
          'N': {1: {'L': (14, None, 1, 'up')}, 8: {'L': (12, None, 1, 'up')}, **{k: {'L': stances.CHAMBER_N['L']} for k in range(2, 8)}}}

def sn():
    import json, subprocess, os
    sp = json.loads(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + os.path.relpath(D + STATE + '.json', R)]))
    sp = stances.frontal('karateGuard', sp); fr = sp['frontal']; F = sp['frames']; pv = fr['partVariants']
    for d in ('S', 'N'):
        v = fr['views'][d]; sg = 1 if d == 'S' else -1; ab = v['armBand']
        base = v['bobRows']; v['bobRowsAt'] = [None] * F
        v['legPoseRows']['far'] = stances.CROUCH_ROWS[3:7]   # karateGuard's own stagger rows (its deepest bob is 3)
        for k, L in LEGS_SN.items():
            v['bobRowsAt'][k] = stances.CROUCH_ROWS   # both legs crouch alike
            v['legPose']['R'][k] = v['legPose']['L'][k] = 'plant'
            v['footDx']['R'][k] = -sg * L['foot']; v['footDx']['L'][k] = sg * L['foot']
            vs = []
            for sd in 'RL':
                if L['knee']:
                    n = '%s-hs-knee%s%d' % (d, sd, L['knee']); pv[n] = {'knee': {'side': sd, 'dx': (-1 if sd == 'R' else 1) * sg * L['knee'], 'rows': [41, L['kneeRow'], 57]}}; vs.append(n)
            v['variants'][str(k)] = vs
            for part in v['twist']: v['twist'][part][k] = 0
        v['bobRowsAt'] = [r if r is not None else base for r in v['bobRowsAt']]
        for k, arms in ARM_SN[d].items():
            for sd, (a, e, sc, fist) in arms.items():
                b = ab[sd]; b['angle'][k] = a; b['scale'][k] = sc; b['fist'][k] = fist; b['elbow'][k] = {'at': 7, 'angle': e} if e is not None else None
                if d == 'N':
                    sh = b.get('showTo'); sh = sh if isinstance(sh, list) else [sh] * F; sh[k] = 7 if e is None else None; b['showTo'] = sh
    sp['status'] = sp['status'].replace('S/N to author after approval', 'S/N CANDIDATE 2026-10-20')
    save(sp, D + STATE + '.json'); print(STATE, 'S/N', F, 'frames')

if __name__ == '__main__':
    if '--sn' in sys.argv: sn(); sys.exit()
    if '--restore' in sys.argv:
        import strikes_sn; strikes_sn.restore(STATE); sys.exit()
    if '--aura' in sys.argv:
        grstrikes.CLIPS[STATE] = (None,) * 9 + (AURA,); grstrikes.aura(STATE)
    else: spec()
