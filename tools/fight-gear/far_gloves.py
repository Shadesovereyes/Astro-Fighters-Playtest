"""Add the far glove to states whose far arm is drawn on its own sheet (arms.farLayer -> far-arm.png), 2026-11-23.

glove_states.py looked for fists on arms.png and body.png only, so a far hand on far-arm.png stayed bare (Christopher
2026-11-23: "only one hand has a glove in the mount palm frames"). glove_states.py now covers far-arm.png for new
states; this patches already-built states in place without touching their other glove pixels: hand_masks.py renders
the far-arm hand mask, each final sheet cell is matched to its source render cell by coverage (smear in-betweens and
held impact frames reshape the sheet after the render), and the far glove is painted onto '<glove>-far' where the
body and near arm do not cover it.
Usage: python3 tools/fight-gear/far_gloves.py <state> [...]
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import hand_masks
from glove_states import masked_fists, paint, F
from build_gloves import GLOVES

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'

def match_mask(sheet_alpha, src_alpha, src_mask, thr=0.6):
    """Mask laid out like the final sheet: each cell takes the source cell (same row, any column, shifted up to 3 px)
    whose coverage best matches; cells with no good match (IoU < 0.6) stay unmasked."""
    H, W = sheet_alpha.shape; out = np.full((H, W), -1, np.int8); hits = 0
    for fy in range(0, H, F):
        for fx in range(0, W, F):
            a = sheet_alpha[fy:fy + F, fx:fx + F]
            if not a.any(): continue
            best = (0, None)
            for sx in range(0, src_alpha.shape[1], F):
                b0 = src_alpha[fy:fy + F, sx:sx + F]
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        b = np.roll(np.roll(b0, dy, 0), dx, 1)
                        iou = (a & b).sum() / max(1, (a | b).sum())
                        if iou > best[0]: best = (iou, (sx, dx, dy))
            if best[0] < thr: continue
            sx, dx, dy = best[1]; hits += 1
            out[fy:fy + F, fx:fx + F] = np.roll(np.roll(src_mask[fy:fy + F, sx:sx + F], dy, 0), dx, 1)
    return out, hits

def run(state, thr=0.6):
    d = ANIM / state; anim = json.loads((d / 'animation.json').read_text()); L = anim['layers']
    if 'far-arm' not in L or not (d / L['far-arm']).exists(): return 'no far arm'
    if not hand_masks.run(state): return 'no mask'
    z = np.load(ROOT / '.git/fight-gear-hand-masks' / f'{state}.npz')
    if 'far-arm' not in z.files: return 'no far-arm mask'
    farm = np.array(Image.open(d / L['far-arm']).convert('RGBA'))
    cover = np.maximum(np.array(Image.open(d / L['body']).convert('RGBA')), np.array(Image.open(d / L['arms']).convert('RGBA')))
    mk, hits = match_mask(farm[..., 3] > 0, z["far-arm-alpha"], z["far-arm"], thr)
    H, W = farm.shape[:2]; added = {}
    for name, g in GLOVES.items():
        p = d / f'{name}-far.png'
        if not p.exists(): continue
        old = np.array(Image.open(p).convert('RGBA'))
        if old.shape != farm.shape: return f'shape mismatch {old.shape} {farm.shape}'
        new = np.zeros_like(old)
        for fy in range(0, H, F):
            for fx in range(0, W, F):
                found = masked_fists(farm, mk, fx, fy)   # far hands and far wrist wraps (cuffs)
                if found: paint(new, fx, fy, found, g, mask=cover)
        put = (new[..., 3] > 0) & (old[..., 3] == 0)
        old[put] = new[put]; added[name] = int(put.sum())
        Image.fromarray(old).save(p)
    return f'cells matched {hits}, px added {added}'

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, run(s))
