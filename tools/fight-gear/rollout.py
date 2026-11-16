"""Render the fight-gear layers into male states, keeping every approved output untouched.

Like tools/armor-classes/rollout.py: each state gets the fight-gear spec entries, is rendered, and only the new
fight-gear sheets (and their animation.json layer entries) are kept; then the gloves are drawn from the state's
own fists (hand_masks.py exact band-arm fists, then glove_states.py).
Usage: python3 tools/fight-gear/rollout.py [state ...]   (default: every state)
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'
sys.path.insert(0, str(Path(__file__).parent))
from add_state_config import add, NEW_LAYERS
import glove_states, hand_masks

def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)

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
    keep = {n: (ANIM / state / f'{n}.png').read_bytes() for n in NEW_LAYERS if (ANIM / state / f'{n}.png').exists()}
    git('checkout', '-q', '--', str(ANIM / state)); git('clean', '-fq', str(ANIM / state))
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
    for s in states:
        if s not in errors: hand_masks.run(s); glove_states.run(ANIM / s)
