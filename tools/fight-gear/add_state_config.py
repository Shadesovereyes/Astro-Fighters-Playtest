"""Add the fight-gear clothing entries (Muay Thai shorts, Boxing trunks) to male posed-animation specs.

Shorts are drawn like the Gi trousers in the profile poses (rows authored on the posed leg) but end at trouser.hem,
a fixed number of rows above the knee; no wrap, shoe, gap fill or under-arm jacket (the torso is bare).
Usage: python3 tools/fight-gear/add_state_config.py <state> [<state> ...]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'

SHORTS = {
    'male-muay-thai-shorts': dict(hem=41, back=2, front=1,
        tones=['#ef4a52', '#c81e2c', '#8a0f1e', '#520812'], band=['#ffd75e', '#d9a42e', '#8f6516', '#7a0f1c']),
    'male-boxing-trunks': dict(hem=44, back=1, front=1,
        tones=['#5b8ef0', '#2f5fcf', '#1d3c94', '#10225c'], band=['#ffffff', '#e3e3e8', '#a8a8b4', '#c81e2c', '#d8d8e0', '#e8e8f0']),
}

def entry(name):
    g = SHORTS[name]; t = g['tones']
    far = {t[0]: t[1], t[1]: t[2], t[2]: t[3], t[3]: t[3], '#000000': '#000000'}
    b = g['band']
    for i, c in enumerate(b): far.setdefault(c, b[min(i + 1, 2)] if i < 3 else c)
    return {
        'outline': '#000000',
        'rule': 'fight-gear shorts (2026-11-15): profile trouser rows end at hem, rows above the posed knee; legs below are bare',
        'legRows': {'wrap': 56, 'foot': 59},
        'trouser': {'hem': g['hem'], 'back': g['back'], 'front': g['front'], 'thighFront': 'f', 'shinFront': 'd',
                    'colours': {'a': '#000000', 'b': t[0], 'c': t[1], 'd': t[2], 'f': t[1]}},
        'farShade': far,
    }

# Boxing boots (2026-11-16): a trouser-less garment (trouser.none) whose shaft is the wrap rows from row 53 and whose
# foot is the shoe colour; tones match build_boots.py
BOOTS = {'male-boxing-boots': {
    'outline': '#000000', 'shoe': '#1d3c94',
    'rule': 'fight-gear boxing boots (2026-11-16): no cloth on the leg (trouser.none); the shaft takes the wrap rows from legRows.wrap, the foot the shoe colour',
    'legRows': {'wrap': 53, 'foot': 59},
    'wrap': {'margin': 0, 'pattern': 'i', 'fill': 'h', 'colours': {'a': '#000000', 'i': '#10225c', 'h': '#2f5fcf'}},
    'trouser': {'none': True, 'back': 0, 'front': 0, 'thighFront': 'a', 'shinFront': 'a', 'colours': {'a': '#000000'}},
    'farShade': {'#3b6fe0': '#2f5fcf', '#2f5fcf': '#1d3c94', '#1d3c94': '#10225c', '#10225c': '#0a1640', '#0a1640': '#0a1640',
                 '#ffffff': '#e3e3e8', '#e3e3e8': '#a8a8b4', '#a8a8b4': '#a8a8b4', '#000000': '#000000'}}}

sys.path.insert(0, str(Path(__file__).parent))
from build_gloves import GLOVES
HEADS = ['mongkol', 'boxing-headgear']

def glove_entry(name):
    g = GLOVES[name]['glove']; c = GLOVES[name]['cuff']
    far = {g[0]: g[1], g[1]: g[2], g[2]: g[3], g[3]: g[3], c[0]: c[1], c[1]: c[1], '#000000': '#000000'}
    return {'outline': '#000000', 'farShade': far,
            'rule': 'fight-gear gloves: Layer 4 piece on the forearm-hand part (like a vambrace); padded by build_gloves.py --grow after rendering'}

def add(state):
    p = ANIM / f'{state}.json'
    spec = json.loads(p.read_text())
    cl = spec.get('clothing')
    if not cl or 'male-gi' not in cl: return False
    for name in SHORTS:
        cl[name] = entry(name)
        if name not in cl['layers']: cl['layers'].append(name)
    for name, e in BOOTS.items():
        cl[name] = json.loads(json.dumps(e))
        if name not in cl['layers']: cl['layers'].append(name)
    if 'blue-armor-shoulders' in cl:
        e = json.loads(json.dumps(cl['blue-armor-shoulders']))
        e['farShade'] = {'#e8434a': '#c81e2c', '#c81e2c': '#8a0f1e', '#8a0f1e': '#8a0f1e', '#000000': '#000000'}
        cl['prajioud'] = e
        if 'prajioud' not in cl['layers']: cl['layers'].append('prajioud')
    ov = spec.get('overlays', {}).get('layers')
    if ov is not None:
        for name in HEADS:
            if name not in ov: ov.insert(ov.index('brown-eyes') if 'brown-eyes' in ov else len(ov), name)
    for name in GLOVES:            # gloves are drawn from the rendered fists (glove_states.py), not by the rig
        cl.pop(name, None)
        if name in cl['layers']: cl['layers'].remove(name)
    p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')
    return True

HEADS = ['mongkol', 'boxing-headgear']
NEW_LAYERS = list(SHORTS) + list(BOOTS) + ['prajioud'] + HEADS

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, add(s))
