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
def band(a, e, **k): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def h(k, side): return copy.deepcopy(HR['arms'][side][k])
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {}

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
FXP, FXPAL = HR_FX['patterns'], HR_FX['palette']
BRACE = dict(ln='cb-brace-rear', lf='cb-brace-lead')   # the hands brace on the thighs
SEAL_N, SEAL_F = band(-48, -150, fistKind='palm'), band(-60, -146, fistKind='palm')   # tiger seal: both open hands pressed together upright in front of the chin, fingers up

CLIPS = {   # state: (ability, active frame, intent, frames, expressions, aura widths)
 'chargeChakra': ('Charge Chakra', 4,
  'Charge Chakra (free focus action, recover chakra): from the guard the fighter sinks into the knees and brings both hands together in a seal in front of the chest, eyes narrowed; holding the seal, a white/neutral aura swells around the whole body in a slow pulse as the chest rises with the breath, then fades; the hands part and come back up into the guard.', [
     g(),
     g(an=band(-5, -140), af=band(-25, -145), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 0), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 0), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(2, 3, 3), lean=(0, -1), **LOW),     # in-breath: chest lifts, head a row higher
     g(an=SEAL_N, af=SEAL_F, bob=(2, 3, 3), lean=(0, -1), **LOW),
     g(an=SEAL_N, af=SEAL_F, bob=(3, 3, 3), lean=(0, 0), **LOW),
     g(an=band(-5, -140), af=band(-25, -145), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 3, 3, 2, 1, 0]),
 'catchBreath': ('Catch Breath', 3,
  'Catch Breath (free focus action, recover stamina): from the guard the fighter drops both hands, bends forward at the hips and braces both hands on the thighs above the knees, head hanging; two big heaving breaths (shoulders and head rise on the in-breath, sink on the out-breath), then straightens back up into the guard.', [
     g(),
     g(an=band(-10, -60), af=band(-20, -70), bob=(2, 2, 2), lean=(0, 4), **LOW),
     g(an=band(-8, 0), af=band(-14, -4), bob=(5, 6, 6), lean=(0, 10), **BRACE),
     g(an=band(-8, 0), af=band(-14, -4), bob=(5, 5, 5), lean=(0, 10), **BRACE),   # in-breath: shoulders and head lift
     g(an=band(-8, 0), af=band(-14, -4), bob=(5, 7, 6), lean=(0, 11), **BRACE),   # out-breath: head hangs
     g(an=band(-8, 0), af=band(-14, -4), bob=(5, 5, 5), lean=(0, 10), **BRACE),
     g(an=band(-8, 0), af=band(-14, -4), bob=(5, 7, 6), lean=(0, 11), **BRACE),
     g(an=band(-10, -60), af=band(-20, -70), bob=(2, 2, 2), lean=(0, 4), **LOW),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None),
 'recompose': ('Recompose', 6,
  'Recompose (free focus action, recover poise, steady the guard): from the guard the fighter lets both arms drop loose and shakes them out, rolls the shoulders and stands tall on a deep breath in, then brings both hands back up and snaps into a tight guard with a sharp exhale; a thin white/neutral pulse marks the reset, then the guard settles.', [
     g(),
     g(an=band(6, -20), af=band(0, -25), bob=(1, 2, 3), lean=(0, 1)),          # arms drop loose
     g(an=band(10, -10), af=band(4, -15), bob=(1, 1, 1), lean=(0, 1)),         # shake: hands swing out
     g(an=band(2, -30), af=band(-4, -35), bob=(1, 2, 3), lean=(0, 1)),         # shake: hands swing back
     g(an=band(4, -15), af=band(-2, -20), bob=(0, 0, 0), lean=(0, 0), ln='stance-rear', lf='stance-lead'),   # stands tall on the in-breath, shoulders up
     g(an=band(-30, -110, fistKind='palm'), af=band(-45, -120, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),   # hands come back up
     g(an=G_N, af=G_F, bob=(2, 2, 2), lean=(0, 3), **LOW),                     # snaps into the guard, chin tucked
     g(an=G_N, af=G_F, bob=(2, 2, 2), lean=(0, 3), **LOW),
     g()],
  [None, None, None, None, 'squint', None, None, None, None],
  [0, 0, 0, 0, 0, 0, 1, 1, 0]),
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
           {'frame': 2, 'splash': [{'pattern': 'puff', 'at': [38, 59]}]},
           {'frame': 3, 'splash': [{'pattern': 'lines', 'at': [44, 19]}, {'pattern': 'puff', 'at': [44, 59]}]},
           {'frame': 4, 'splash': [{'pattern': 'speck', 'at': [46, 60]}]}]})),
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
}

def spec(state):
    ab, act, intent, fr, ex, _, *more = CLIPS[state]
    x = more[0] if more else {}
    n = len(fr)
    ev = [{'frame': k, 'clip': state, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'} for k in range(n)]
    if x.get('hitbox'): ev[act].update(move=ab, hitbox=x['hitbox'], damage=x['damage'])
    else: ev[act].update(move=ab, buff=True)
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E: x -> 64 - x - w); hitboxes provisional', 'E': ev,
              'W': [{**e, 'hitbox': [64 - e['hitbox'][0] - e['hitbox'][2]] + e['hitbox'][1:]} if 'hitbox' in e else dict(e) for e in ev]}
    clips = {'rule': 'starts and ends in the approved guard frame and returns to that idle (next: guard)',
             state: {'frames': list(range(n)), 'fps': 10, 'next': 'guard', 'ability': ab}}
    s = build(HR, state, fr, status=APPROVED.get(state, STAT), newPoses=POSES, clips=clips, events=events, rmRule=x.get('rm', 'in place'), intent=intent, fx=x.get('fx'))
    s['fps'] = clips[state]['fps'] = x.get('fps', 10); s.pop('approved', None); s.pop('keyPoses', None)
    if not x.get('fx'): s.pop('fx', None)
    s['expressions'] = copy.deepcopy(HR['expressions']); s['expressions']['frames'] = {'E': ex}
    save(s, D + state + '.json'); print(state, n, 'frames')

def aura(state):
    grstrikes.CLIPS[state] = (None,) * 9 + (CLIPS[state][5],); grstrikes.aura(state)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--aura' in a: aura(a[a.index('--aura') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
