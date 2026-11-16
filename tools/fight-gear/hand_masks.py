"""Exact fist masks for band arms (the raised / punching arms the renderer builds from arms.band), 2026-11-16.

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

def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)

def mark(spec):
    if 'palette' not in spec: return False
    hit = False
    for name in ('fist', 'fistUp', 'fistFront', 'palmUp', 'palmDown'):
        f = spec.get('arms', {}).get('band', {}).get(name)
        if f: f['rows'] = [''.join(MARK[c][0] if c in MARK else c for c in r) for r in f['rows']]; hit = True
    for k, (sym, hexc) in MARK.items(): spec['palette'][sym] = hexc
    fm = spec.get('farShade', {}).get('map')
    if fm is not None:
        order = ['1', '2', '3', '4', '5']
        for i, s in enumerate(order): fm[s] = order[min(i + 1, 4)]
    return hit

def run(state):
    p = ANIM / f'{state}.json'
    spec = json.loads(p.read_text())
    if not mark(spec): return False
    p.write_text(json.dumps(spec, indent=2))
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
        git('checkout', '-q', '--', str(p), str(ANIM / state)); git('clean', '-fq', str(ANIM / state))
    MASKS.mkdir(parents=True, exist_ok=True); np.savez_compressed(MASKS / f'{state}.npz', **masks)
    return True

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, run(s))
