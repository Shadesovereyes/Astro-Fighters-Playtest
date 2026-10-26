"""Hide the white wrist wraps under the armor vambraces.

Arms1 carries white wraps (#ffffff near arm, #e3e3e3 far arm). With an armor's Layer 4 worn,
every wrap pixel that would still show (Arms1 wraps, and the far arm's wraps that posed states draw
on the body layer) is painted in the vambrace colour on that
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
    'plate-harness-shoulders': ('6a6f7a', '444852'),
}
PAPERDOLL = {
    'scale-coat-shoulders': 'Scale Coat Shoulders.png',
    'lamellar-shoulders': 'Lamellar Shoulders.png',
    'studded-leather-shoulders': 'Studded Leather Shoulders.png',
    'plate-harness-shoulders': 'Plate Harness Shoulders.png',
}

def rgba(h): return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)] + [255], np.uint8)

CLOTHING = {'scale-coat-shoulders': 'male-scale-coat', 'lamellar-shoulders': 'male-lamellar',
            'studded-leather-shoulders': 'male-studded-leather', 'plate-harness-shoulders': 'male-plate-harness'}

def wraps(img):
    return {side: (img[..., 3] > 0) & (img[..., :3] == rgb).all(-1) for rgb, side in WRAPS.items()}

def cover(arms_path, layer_path, colours, body_path=None, clothing_path=None):
    """Paint the wraps that would show in the composite: Arms1 wraps not under the vambrace, and in posed
    states the far arm's wraps drawn on the body layer where no clothing, near arm or vambrace covers them."""
    arms = np.array(Image.open(arms_path).convert('RGBA'))
    layer = np.array(Image.open(layer_path).convert('RGBA'))
    free = layer[..., 3] == 0
    n = 0
    for side, m in wraps(arms).items():
        m = m & free
        layer[m] = rgba(colours[0 if side == 'near' else 1]); n += int(m.sum())
    if body_path and body_path.exists():
        body = np.array(Image.open(body_path).convert('RGBA'))
        shown = free & (arms[..., 3] == 0)
        if clothing_path and clothing_path.exists():
            shown &= np.array(Image.open(clothing_path).convert('RGBA'))[..., 3] == 0
        for side, m in wraps(body).items():
            m = m & shown & (layer[..., 3] == 0)
            layer[m] = rgba(colours[1]); n += int(m.sum())
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
                if (d / f'{name}.png').exists():
                    print(d.name, name, cover(d / 'arms.png', d / f'{name}.png', colours, d / 'body.png', d / f'{CLOTHING[name]}.png'))
