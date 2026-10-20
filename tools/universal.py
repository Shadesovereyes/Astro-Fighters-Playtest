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
HR = load(D + 'hitReact.json'); HR.pop('frontal', None); HR['directions'] = ['E', 'W']
def band(a, e, **k): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def h(k, side): return copy.deepcopy(HR['arms'][side][k])
STAT = 'CANDIDATE 2026-10-20 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {}

G_N, G_F = h(6, 'near'), h(6, 'far')                     # guard arms
GUARD = dict(an=G_N, af=G_F, bob=(1, 1, 2), lean=(0, 2), ln='stance-rear', lf='stance-lead', root=(0, 0))
def g(**k): return dict(src=6, **{**GUARD, **k})
LOW = dict(ln='guard-low-rear', lf='guard-low-lead')
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
}

def spec(state):
    ab, act, intent, fr, ex, _ = CLIPS[state]
    n = len(fr)
    ev = [{'frame': k, 'clip': state, 'type': 'startup' if k < act else 'active' if k == act else 'recovery'} for k in range(n)]
    ev[act].update(move=ab, buff=True)
    events = {'rule': 'per-frame gameplay data per facing (W mirrors E)', 'E': ev, 'W': [dict(e) for e in ev]}
    clips = {'rule': 'starts and ends in the approved guard frame and returns to that idle (next: guard)',
             state: {'frames': list(range(n)), 'fps': 10, 'next': 'guard', 'ability': ab}}
    s = build(HR, state, fr, status=APPROVED.get(state, STAT), clips=clips, events=events, rmRule='in place', intent=intent)
    s['fps'] = 10; s.pop('approved', None); s.pop('keyPoses', None); s.pop('fx', None)
    s['expressions'] = copy.deepcopy(HR['expressions']); s['expressions']['frames'] = {'E': ex}
    save(s, D + state + '.json'); print(state, n, 'frames')

def aura(state):
    grstrikes.CLIPS[state] = (None,) * 9 + (CLIPS[state][5],); grstrikes.aura(state)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--aura' in a: aura(a[a.index('--aura') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
