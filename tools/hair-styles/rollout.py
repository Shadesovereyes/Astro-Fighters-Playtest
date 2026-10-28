"""Render the new hair styles (tools/hair-styles/build_hair.py) into every male state.

Same rules as tools/armor-classes/rollout.py: only the new hair sheets are added to each state; every
approved output already in a state (and its animation.json apart from the new layer entries) stays exactly
as committed. Posed specs list their head overlays, so the hair names are added next to long-hair first.
States that borrow frames from other states are retried until their sources have the new layers.
Usage: python3 tools/hair-styles/rollout.py [state ...]   (default: every state)
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'
HAIR = ['locs-tied', 'locs-loose', 'wrapped-headscarf', 'modern-topknot', 'braided-side',
        'afro-puff', 'bantu-knots', 'ronin-ponytail', 'flat-top',
        'headband-white', 'headband-red', 'headband-blue']

def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)

def add(state):
    p = ANIM / f'{state}.json'
    spec = json.loads(p.read_text())
    ov = spec.get('overlays', {}).get('layers')
    if ov is None or 'long-hair' not in ov: return False
    at = ov.index('long-hair') + 1
    for name in reversed(HAIR):
        if name not in ov: ov.insert(at, name)
    p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')
    return True

def tool_for(state):
    schema = json.loads((ANIM / f'{state}.json').read_text())['schema']
    return 'tools/character-posed.mjs' if 'posed' in schema else 'tools/character-animate.mjs'

def render(state):
    old_anim = json.loads((ANIM / state / 'animation.json').read_text())
    r = subprocess.run(['node', tool_for(state), 'male', state], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        git('checkout', '-q', '--', str(ANIM / state)); git('clean', '-fq', str(ANIM / state))
        return r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'failed'
    new_anim = json.loads((ANIM / state / 'animation.json').read_text())
    keep = {n: (ANIM / state / f'{n}.png').read_bytes() for n in HAIR if (ANIM / state / f'{n}.png').exists()}
    git('checkout', '-q', '--', str(ANIM / state))         # restore every approved output
    for n, data in keep.items(): (ANIM / state / f'{n}.png').write_bytes(data)
    layers = old_anim.get('layers', {})
    for n in keep: layers[n] = new_anim['layers'].get(n, f'{n}.png')
    old_anim['layers'] = layers
    (ANIM / state / 'animation.json').write_text(json.dumps(old_anim, indent=2, ensure_ascii=False) + '\n')
    return None

if __name__ == '__main__':
    states = sys.argv[1:] or sorted(p.stem for p in ANIM.glob('*.json') if (ANIM / p.stem / 'animation.json').exists())
    for s in states: add(s)
    pending, errors = list(states), {}
    while pending:
        progress, nxt = False, []
        for s in pending:
            err = render(s)
            if err: nxt.append(s); errors[s] = err
            else: progress = True; errors.pop(s, None); print('ok', s, flush=True)
        pending = nxt
        if not progress: break
    for s, e in errors.items(): print('FAILED', s, e)
