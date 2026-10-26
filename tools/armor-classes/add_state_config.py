"""Add the Scale Coat and Lamellar clothing entries to a male posed-animation spec.

Each new layer copies the spec's male-blue-armor / blue-armor-shoulders entry (same
registration rules) with the stand-in colours swapped for the armor's own.
Usage: python3 tools/armor-classes/add_state_config.py <state> [<state> ...]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'

# stand-in colour -> armor colour (blue armor: white highlight, grey trouser, blue, dark blue)
SWAP = {
    'male-scale-coat': {'#ffffff': '#7a7f99', '#adadad': '#4e526a', '#434da0': '#b0802e', '#332b6f': '#4a2a14'},
    'male-studded-leather': {'#ffffff': '#4c4448', '#adadad': '#332d30', '#434da0': '#4e3022', '#332b6f': '#2f1b12'},
    # profile leg rows below the kusazuri are the steel shin splints
    'male-lamellar': {'#ffffff': '#a7adbb', '#adadad': '#6c7282', '#434da0': '#6c7282', '#332b6f': '#241f2a'},
}
SHOULDER_SWAP = {
    'scale-coat-shoulders': {'#ffffff': '#a8703e', '#adadad': '#7a4a26', '#434da0': '#7a4a26', '#332b6f': '#4a2a14'},
    'studded-leather-shoulders': {'#ffffff': '#6e4630', '#adadad': '#4e3022', '#434da0': '#4e3022', '#332b6f': '#2f1b12'},
    'lamellar-shoulders': {'#ffffff': '#a7adbb', '#adadad': '#6c7282', '#434da0': '#6c7282', '#332b6f': '#3d4050'},
}
# one step darker for the far side
FAR = {
    'male-scale-coat': {'#e2b65a': '#b0802e', '#b0802e': '#6e4618', '#6e4618': '#6e4618', '#a8703e': '#7a4a26', '#7a4a26': '#4a2a14',
                        '#4a2a14': '#4a2a14', '#7a7f99': '#4e526a', '#4e526a': '#30324a', '#30324a': '#30324a', '#000000': '#000000'},
    'male-lamellar': {'#a7adbb': '#6c7282', '#6c7282': '#3d4050', '#3d4050': '#3d4050', '#b02a2a': '#6e1414', '#6e1414': '#6e1414',
                      '#6fb09a': '#3e7a66', '#3e7a66': '#3e7a66', '#c43a30': '#7e1c18', '#7e1c18': '#7e1c18', '#5a5266': '#3a3442',
                      '#3a3442': '#241f2a', '#241f2a': '#241f2a', '#000000': '#000000'},
    'male-studded-leather': {'#6e4630': '#4e3022', '#4e3022': '#2f1b12', '#2f1b12': '#2f1b12', '#c48a58': '#6e4630', '#9a6040': '#6a3e26',
                             '#6a3e26': '#6a3e26', '#7b4b30': '#4f2f1d', '#4f2f1d': '#4f2f1d', '#b8bcc4': '#6c7282', '#4c4448': '#332d30',
                             '#332d30': '#1f1b1d', '#1f1b1d': '#1f1b1d', '#000000': '#000000'},
}
def nudge(h): return h[:5] + '%02x' % (int(h[5:], 16) ^ 1)
for name in ('male-scale-coat', 'male-lamellar', 'male-studded-leather'):
    FAR[name].update({nudge(k): nudge(v) for k, v in FAR[name].items() if k != '#000000'})
FAR['scale-coat-shoulders'] = FAR['male-scale-coat']
FAR['lamellar-shoulders'] = FAR['male-lamellar']
FAR['studded-leather-shoulders'] = FAR['male-studded-leather']

def swap(v, table):
    if isinstance(v, str): return table.get(v.lower(), v)
    if isinstance(v, list): return [swap(x, table) for x in v]
    if isinstance(v, dict): return {k: swap(x, table) for k, x in v.items()}
    return v

def add(state):
    p = ANIM / f'{state}.json'
    spec = json.loads(p.read_text())
    cl = spec.get('clothing')
    if not cl or 'male-blue-armor' not in cl: return False
    for name, table in SWAP.items():
        e = swap(cl['male-blue-armor'], table); e['farShade'] = FAR[name]; cl[name] = e
    for name, table in SHOULDER_SWAP.items():
        if 'blue-armor-shoulders' in cl:
            e = swap(cl['blue-armor-shoulders'], table); e['farShade'] = FAR[name]; cl[name] = e
    layers = cl['layers']
    for name in ['male-scale-coat', 'male-lamellar', 'male-studded-leather', 'scale-coat-shoulders', 'lamellar-shoulders', 'studded-leather-shoulders']:
        if name in cl and name not in layers: layers.append(name)
    p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')
    return True

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, add(s))
