"""Add the stowed-weapon layers to a male posed-animation spec.

Each stowed sheet is a rigid component (rig part pelvis or torso, tools/character-rig.mjs), so its clothing entry
only needs the outline; it is never shaded as a far side (it is drawn on its own runtime slot, behind the body or
over the clothing). clipToFrame: on a fighter lying down the yumi can reach past the 64x64 cell, so those pixels
are dropped instead of failing the render.
Usage: python3 tools/stowed-weapons/add_state_config.py <state> [<state> ...]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'
STOWED = ['katana-stowed-front', 'katana-stowed-back', 'yumi-stowed-front', 'yumi-stowed-back',
          'kyoketsu-shoge-stowed-front', 'kyoketsu-shoge-stowed-back',
          'tanto-stowed-front', 'tanto-stowed-back']

def add(state):
    p = ANIM / f'{state}.json'
    spec = json.loads(p.read_text())
    cl = spec.get('clothing')
    if not cl or 'layers' not in cl: return False
    for name in STOWED:
        cl[name] = {'outline': '#000000', 'farShade': {'#000000': '#000000'}, 'clipToFrame': True,
                    'rule': 'stowed weapon: a rigid piece that rides its rig part (katana, cord and tanto: pelvis, yumi: torso)'}
        if name not in cl['layers']: cl['layers'].append(name)
    p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')
    return True

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, add(s))
