"""Render the stowed-weapon layers into every male state.

Same approach as tools/armor-classes/rollout.py: only the new stowed sheets are added to each state; every approved
output (body, arms, clothing, armor, animation.json apart from the new layer entries) is restored as committed.
States that borrow frames from other states are retried until their sources have the new layers.
Usage: python3 tools/stowed-weapons/rollout.py [state ...]   (default: every state)
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'
sys.path.insert(0, str(Path(__file__).parent))
from add_state_config import add, STOWED as NEW

def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)

def tool_for(state):
    schema = json.loads((ANIM / f'{state}.json').read_text())['schema']
    return 'tools/character-posed.mjs' if 'posed' in schema else 'tools/character-animate.mjs'

def render(state):
    old_anim = json.loads(git('show', f'HEAD:{(ANIM / state / "animation.json").relative_to(ROOT)}').stdout)
    r = subprocess.run(['node', tool_for(state), 'male', state], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        git('checkout', '-q', '--', str(ANIM / state))
        return r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'failed'
    new_anim = json.loads((ANIM / state / 'animation.json').read_text())
    keep = {n: (ANIM / state / f'{n}.png').read_bytes() for n in NEW if (ANIM / state / f'{n}.png').exists()}
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
