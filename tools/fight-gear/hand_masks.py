"""Exact fist masks for every arm, 2026-11-16: band arms (raised / punching, drawn from arms.band fist patterns) and
reference arms (moved from the Arms1 / Body1 sheets, whose hands below the wrist wrap are recoloured for the run).

The renderer draws a band arm's hand from the fist patterns (arms.band.fist, fistUp, fistFront, palmUp, palmDown).
This renders the state once more with those patterns' skin symbols swapped for marker colours, reads which arms.png /
body.png pixels came out as markers, saves the masks, and restores every committed output. glove_states.py uses the
masks where they exist, so a fist is never mistaken for a foreshortened forearm (muayThaiElbow S, 2026-11-16).
Usage: python3 tools/fight-gear/hand_masks.py <state> [...]   -> .git/fight-gear-hand-masks/<state>.npz (never tracked)
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / 'production/source/characters/anim/male'
MARK = {'L': ('1', '#01fe01'), 'm': ('2', '#02fe02'), 's': ('3', '#03fe03'), 'd': ('4', '#04fe04'), 'D': ('5', '#05fe05')}
MASKS = ROOT / '.git/fight-gear-hand-masks'   # inside .git: never tracked
TONE = {MARK[k][1]: i for i, k in enumerate(['L', 'm', 's', 'd', 'D'])}
WMARK = {'W': ('6', '#06fe06'), 'w': ('7', '#07fe07')}     # wrist wraps -> glove cuff (mask values 5, 6)
TONE.update({'#06fe06': 5, '#07fe07': 6})

def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)

def mark(spec):
    if 'palette' not in spec: return False      # (character-animate states: no palette; gloves fall back to the heuristic)
    hit = True
    for name in ('fist', 'fistUp', 'fistFront', 'palmUp', 'palmDown', 'palmHeel', 'fingerGun', 'fingerPoint'):
        f = spec.get('arms', {}).get('band', {}).get(name)
        if f: f['rows'] = [''.join(MARK[c][0] if c in MARK else c for c in r) for r in f['rows']]
    for k, (sym, hexc) in list(MARK.items()) + list(WMARK.items()): spec['palette'][sym] = hexc
    band = spec.get('arms', {}).get('band', {})
    if band.get('pattern', {}).get('wrap'):
        band['pattern']['wrap'] = ''.join(WMARK[c][0] if c in WMARK else c for c in band['pattern']['wrap'])
    fm = spec.get('farShade', {}).get('map')
    if fm is not None:
        order = ['1', '2', '3', '4', '5']
        for i, s in enumerate(order): fm[s] = order[min(i + 1, 4)]
        fm['6'] = '7'; fm['7'] = '7'
    return hit

SHEETS = [ROOT / 'Paperdolls/Male/Layer 3 - Arms/Male Arms1.png', ROOT / 'Paperdolls/Male/Layer 1 - Base Body/Male Base Body1.png']
PARTMAP = ROOT / 'production/source/characters/rig/male/part-map.png'
FOREARM = {(70, 240, 240), (240, 50, 230)}
SKINHEX = {'f6a35b': 'L', 'c87845': 'm', '9e4a31': 's', '70241d': 'd', '3f0505': 'D'}
WRAPHEX = {'ffffff', 'e3e3e3'}

def mark_sheet(path):
    """Recolour the reference hands (forearm-hand pixels below each arm's wrist wrap) in marker colours."""
    a = np.array(Image.open(path).convert('RGBA')); m = np.array(Image.open(PARTMAP).convert('RGBA'))
    for f in range(a.shape[1] // 64):
        ox = f * 64
        for side in ((70, 240, 240), (240, 50, 230)):
            pts = [(x, y) for y in range(64) for x in range(64) if a[y, ox + x, 3] and tuple(m[y, ox + x, :3]) == side]
            wr = [y for x, y in pts if '%02x%02x%02x' % tuple(a[y, ox + x, :3]) in WRAPHEX]
            if not wr: continue
            below = max(wr)
            for x, y in pts:
                h = '%02x%02x%02x' % tuple(a[y, ox + x, :3])
                if h in WRAPHEX:
                    c = WMARK['W' if h == 'ffffff' else 'w'][1]; a[y, ox + x, :3] = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
                    continue
                if y > below and h in SKINHEX:
                    c = MARK[SKINHEX[h]][1]; a[y, ox + x, :3] = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    Image.fromarray(a).save(path)

def run(state):
    p = ANIM / f'{state}.json'
    spec_text = p.read_text(); spec = json.loads(spec_text)
    if not mark(spec): return False
    sd = ANIM / state   # snapshot the state dir: the marker render must leave the working copy exactly as it was
    before = {q: q.read_bytes() for q in sd.iterdir() if q.is_file()}
    p.write_text(json.dumps(spec, indent=2))
    saved = {sh: sh.read_bytes() for sh in SHEETS}
    for sh in SHEETS: mark_sheet(sh)
    try:
        r = subprocess.run(['node', 'tools/character-posed.mjs', 'male', state], cwd=ROOT, capture_output=True, text=True)
        if r.returncode: print('render failed', state, r.stderr.strip().splitlines()[-1:]); return False
        anim = json.loads((ANIM / state / 'animation.json').read_text())
        masks = {}
        for layer in ('arms', 'body'):
            a = np.array(Image.open(ANIM / state / anim['layers'][layer]).convert('RGBA'))
            m = np.full(a.shape[:2], -1, np.int8)
            for hexc, t in TONE.items():
                rgb = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
                m[(a[..., 3] > 0) & (a[..., 0] == rgb[0]) & (a[..., 1] == rgb[1]) & (a[..., 2] == rgb[2])] = t
            masks[layer] = m
    finally:
        for sh, data in saved.items(): sh.write_bytes(data)
        p.write_text(spec_text)
        for q in sd.iterdir():
            if q.is_file() and q not in before: q.unlink()
        for q, data in before.items(): q.write_bytes(data)
    MASKS.mkdir(parents=True, exist_ok=True); np.savez_compressed(MASKS / f'{state}.npz', **masks)
    return True

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, run(s))
