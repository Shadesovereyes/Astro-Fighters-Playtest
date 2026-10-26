"""Hide the white wrist wraps under the armor vambraces.

Arms1 carries white wraps (#ffffff near arm, #e3e3e3 far arm). With an armor's Layer 4 worn,
every wrap pixel the vambrace does not already cover is painted in the vambrace colour on that
armor's Layer 4 sheet, so no wrap shows in any pose. Only the armor sheets are written.
Usage: python3 tools/armor-classes/cover_wraps.py <dir with arms.png> [...]   (rendered states)
       python3 tools/armor-classes/cover_wraps.py --paperdoll
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WRAPS = {(255, 255, 255): 'near', (227, 227, 227): 'far'}
# vambrace colour per armor: (near wrap, far wrap)
VAMBRACE = {
    'scale-coat-shoulders': ('7a4a26', '4a2a14'),
    'lamellar-shoulders': ('6c7282', '3d4050'),
    'studded-leather-shoulders': ('4e3022', '2f1b12'),
}
PAPERDOLL = {
    'scale-coat-shoulders': 'Scale Coat Shoulders.png',
    'lamellar-shoulders': 'Lamellar Shoulders.png',
    'studded-leather-shoulders': 'Studded Leather Shoulders.png',
}

def rgba(h): return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)

def cover(arms_path, layer_path, colours):
    arms = np.array(Image.open(arms_path).convert('RGBA'))
    layer = np.array(Image.open(layer_path).convert('RGBA'))
    n = 0
    for rgb, side in WRAPS.items():
        mask = (arms[..., 3] > 0) & (arms[..., :3] == rgb).all(-1) & (layer[..., 3] == 0)
        layer[mask] = rgba(colours[0 if side == 'near' else 1]); n += int(mask.sum())
    Image.fromarray(layer).save(layer_path)
    return n

if __name__ == '__main__':
    if sys.argv[1:] == ['--paperdoll']:
        arms = ROOT / 'Paperdolls/Male/Layer 3 - Arms/Male Arms1.png'
        for name, file in PAPERDOLL.items():
            print(name, cover(arms, ROOT / 'Paperdolls/Male/Layer 4 - Shoulders and Arms accessories' / file, VAMBRACE[name]))
    else:
        for d in map(Path, sys.argv[1:]):
            for name, colours in VAMBRACE.items():
                if (d / f'{name}.png').exists(): print(d.name, name, cover(d / 'arms.png', d / f'{name}.png', colours))
