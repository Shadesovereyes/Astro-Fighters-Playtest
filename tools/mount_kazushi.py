"""Kazushi (Jiu-Jitsu, Mount only, top or bottom; Christopher 2026-10-20) and Cord Garrote (Kyoketsu-Shoge, Mount, both
positions, Maintained Submission) as paired Mount clips, built like tools mountmoves.py (Cross Choke, Hip Escape).
Targets hold the plain Mount idle until the impact frame (ANIMATION_RULES 2026-11-04). E/W first, S/N after approval.
Run: python3 tools/mount_kazushi.py ; node tools/character-posed.mjs male <state> ; pairpreview.py ... --cell 80 --x0 4"""
import sys, os, copy
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'production/source/characters/anim/male/')
T = load(D + 'mountTop.json'); Bt = load(D + 'mountBottom.json'); H = load(D + 'clinchSweepingShoulderHit.json')
band = lambda a, e: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
LAY = ['mountBottom body, clothing, hair, eyes', 'mountTop body, clothing, hair, eyes, far arm', 'mountBottom arms', 'mountTop arms']
STAT = 'CANDIDATE 2026-11-06 ({}) (E/W; W mirrors E; S/N to author after approval)'
patterns = dict(H['fx']['patterns'], hitStar=['..#..', '#.#.#', '.#W#.', '#.#.#', '..#..'], strain=['#.#', '...', '#.#'],
                tug=['W.W', '.W.'], shift=['W..', '.W.', 'W..'],
                kzMark=['###', '#W#', '#W#', '#W#', '#W#', '###', '#W#', '###'])   # Kazushi: off-balance exclamation mark over the target's head (Christopher 2026-11-06 18:16)

def events(F, active, move, effect):
    e = [{'frame': i, 'type': 'startup' if i < active[0] else 'active' if i in active else 'recovery'} for i in range(F)]
    for a in active: e[a].update({'move': move, 'effect': effect})
    return {'rule': 'per-frame gameplay data per facing (provisional); impact frame = first active frame (ANIMATION_RULES 2026-11-04)', 'E': e, 'W': copy.deepcopy(e), 'tactical': {'rule': 'no displacement: the pair stays in Mount on its cells'}}

def make(state, base, frames, *, partner, status, intent, clips, ev=None, fx=None, expr=None, newPoses=(), rule='', rm='in place', order=None, weapons=None):
    p = {'rule': rule, 'partner': partner, 'partnerDx': 2, 'layering': order or LAY, 'mountLayering': {'fromFrame': 0, 'order': order or LAY, **({'bottomArmsOver': True} if order else {})}}
    s = build(base, state, frames, status=STAT.format(status), intent=intent, newPoses=newPoses, pair=p, clips=clips, events=ev, fx=fx, rmRule=rm)
    if expr is not None:
        s['expressions'] = copy.deepcopy(Bt['expressions']); s['expressions']['frames'] = {'E': expr}
    if fx: s['fx']['palette'] = H['fx']['palette']; s['fx']['patterns'] = patterns
    if weapons: s['weapons'] = weapons
    else: s.pop('weapons', None)
    save(s, D + state + '.json')

def tf(src=0, **k): return dict(src=src, **k)
Tx = copy.deepcopy(T); Tx['expressions'] = copy.deepcopy(Bt['expressions'])
Bk = copy.deepcopy(Bt); Bk['legs']['feet'] = load(D + 'mountHipEscape.json')['legs']['feet']   # the bridge feet (pointDL) from the approved Hip Escape

# ================= Kazushi from the top (Jiu-Jitsu, Mount only, 2 slots: break the mounted fighter's posture) =================
# the top fighter sinks, both hands grab the collar and near sleeve, then jerks them across and up while its hips slide the
# other way: the mounted fighter's shoulders are dragged off the mat and twisted (impact frame 3), then dropped back
kt = [tf(0), tf(1, bob=(12, 12, 13), lean=(1, 8), an=band(-30, -60), af=band(-26, -56)),
      tf(2, bob=(14, 14, 15), lean=(2, 12), an=band(0, -45), af=band(4, -48)),
      tf(3, bob=(11, 11, 12), lean=(-1, 1), an=band(-10, -150), af=band(-6, -145), root=(-2, 0)),
      tf(0, bob=(11, 11, 12), lean=(-1, 1), an=band(-12, -152), af=band(-8, -147)),
      tf(1, bob=(12, 12, 13), lean=(0, 5), an=band(-20, -90), af=band(-24, -60), root=(2, 0)),
      tf(2), tf(3)]
kb = [tf(0), tf(1), tf(2),
      tf(3, lean=(3, 6), root=(1, 0), an=band(-20, -60), af=band(-120, -150)),
      tf(0, lean=(3, 6), an=band(-22, -62), af=band(-125, -152)),
      tf(1, lean=(1, 2), root=(-1, 0), an=band(-50, -120), af=band(-80, -145)),
      tf(2), tf(3)]
kx = [None, None, None, 'pain', 'pain', 'squint', None, None]
fx_k = {'rule': 'white tug marks at the collar on the jerk (impact frame 3), off-balance strain by the mounted fighter\'s head, and from the impact frame the Kazushi exclamation mark over its head (drawn over both fighters)', 'top': True, 'frames': [
    {'frame': 3, 'splash': [{'pattern': 'tug', 'at': [12, 46]}, {'pattern': 'strain', 'at': [5, 49]}, {'pattern': 'kzMark', 'at': [5, 45]}]},
    {'frame': 4, 'splash': [{'pattern': 'shift', 'at': [4, 48]}, {'pattern': 'kzMark', 'at': [5, 45]}]},
    {'frame': 5, 'splash': [{'pattern': 'kzMark', 'at': [5, 47]}]}, {'frame': 6, 'splash': [{'pattern': 'kzMark', 'at': [5, 47]}]}, {'frame': 7, 'splash': [{'pattern': 'kzMark', 'at': [5, 47]}]}]}
make('mountKazushi', T, kt, partner='mountKazushiHit', status='Kazushi from the top of Mount, paired with mountKazushiHit',
     intent='Jiu-Jitsu Kazushi from the top (Christopher 2026-10-20: Mount only, top or bottom; boosts the next Jiu-Jitsu technique this round): from the mountTop idle the top fighter sinks low and both hands grab the collar and near sleeve, then jerks them up and across toward its own chest while its hips slide back 2 px, dragging the mounted fighter\'s shoulders off the mat and twisting it off balance (impact frame 3); it holds the tilt a beat and settles back into mountTop.',
     clips={'rule': 'plays from mountTop; the mounted fighter plays mountKazushiHit on the same frames; returns to mountTop', 'mountKazushi': {'frames': list(range(8)), 'fps': 12, 'next': 'mountTop'}},
     ev=events(8, [3], 'Kazushi', 'Kazushi mark: +3 DC to the next Jiu-Jitsu technique this round (placeholder)'),
     rule='paired Mount move: top (E) breaks posture, bottom (W) is pulled off balance', rm='per-frame step (screen px): the top fighter slides 2 px back on the jerk and 2 px forward again (net 0)')
make('mountKazushiHit', Bt, kb, partner='mountKazushi', status='mounted side of Kazushi, paired with mountKazushi',
     intent="The mounted fighter's side of top Kazushi: it lies in the plain mountBottom idle until the impact frame (3), when its shoulders are dragged up and twisted toward the top fighter, the near arm pulled across and the far arm flung out for the mat; it holds a beat and settles back into mountBottom.",
     clips={'rule': 'plays on the mounted fighter when the top plays mountKazushi; returns to mountBottom', 'mountKazushiHit': {'frames': list(range(8)), 'fps': 12, 'next': 'mountBottom'}},
     fx=fx_k, expr=kx, rule='paired Mount move: top (E) breaks posture, bottom (W) is pulled off balance')

# ================= Kazushi from the bottom (Jiu-Jitsu, Mounted) =================
# the mounted fighter frames both forearms on the top fighter's hips, then bridges hard and shoves up and across:
# the top fighter is tipped forward and off its base (impact frame 3), posts and resettles
newB = [{'name': 'kz-bridge-near', 'construction': 'band', 'hipX': 32, 'hipRow': 42, 'kneeX': 39, 'kneeRow': 47, 'ankle': [36, 55], 'foot': 'pointDL'},
        {'name': 'kz-bridge-far', 'construction': 'band', 'hipX': 31, 'hipRow': 42, 'kneeX': 37, 'kneeRow': 48, 'ankle': [34, 56], 'foot': 'pointDL'}]
bb = [tf(0), tf(1, an=band(-25, -70), af=band(-20, -65)),
      tf(2, ln='kz-bridge-near', lf='kz-bridge-far', lean=(1, 1), an=band(-20, -55), af=band(-16, -50)),
      tf(3, ln='kz-bridge-near', lf='kz-bridge-far', lean=(4, 3), an=band(-8, -12), af=band(-6, -10)),
      tf(0, ln='kz-bridge-near', lf='kz-bridge-far', lean=(4, 3), an=band(-6, -10), af=band(-4, -8)),
      tf(1, lean=(1, 1), an=band(-40, -110), af=band(-35, -100)),
      tf(2), tf(3)]
bt = [tf(0), tf(1), tf(2),
      tf(3, bob=(14, 14, 15), lean=(3, 13), an=band(8, -15), af=band(12, -18), root=(3, 0)),
      tf(0, bob=(14, 14, 15), lean=(3, 14), an=band(10, -12), af=band(14, -16)),
      tf(1, bob=(12, 12, 13), lean=(1, 7), an=band(-20, -70), af=band(-30, -45), root=(-3, 0)),
      tf(2), tf(3)]
bx = [None, 'squint', 'pain', 'pain', 'pain', 'squint', None, None]
fx_bt = {'rule': 'from the impact frame (3) the Kazushi exclamation mark over the top fighter\'s head', 'top': True, 'frames': [
    {'frame': k, 'splash': [{'pattern': 'kzMark', 'at': [x, 16 if k < 5 else 15]}]} for k, x in ((3, 46), (4, 47), (5, 40), (6, 38), (7, 37))]}
btx = [None, None, None, 'pain', 'pain', 'squint', None, None]
fx_b = {'rule': 'a white shove burst at the top fighter\'s hips on the bridge (impact frame 3)', 'frames': [
    {'frame': 3, 'splash': [{'pattern': 'tug', 'at': [38, 44]}]}, {'frame': 4, 'splash': [{'pattern': 'shift', 'at': [40, 40]}]}]}
make('mountBottomKazushi', Bk, bb, partner='mountBottomKazushiHit', status='Kazushi from the bottom of Mount, paired with mountBottomKazushiHit', newPoses=newB,
     intent='Jiu-Jitsu Kazushi from the bottom (Christopher 2026-10-20: Mount only, top or bottom): from the mountBottom idle the mounted fighter frames both forearms on the top fighter\'s hips, then bridges its hips up hard and shoves up and across, tipping the top fighter forward off its base (impact frame 3); it drops back flat and returns to mountBottom.',
     clips={'rule': 'plays from mountBottom; the top fighter plays mountBottomKazushiHit; returns to mountBottom', 'mountBottomKazushi': {'frames': list(range(8)), 'fps': 12, 'next': 'mountBottom'}},
     ev=events(8, [3], 'Kazushi', 'Kazushi mark: +3 DC to the next Jiu-Jitsu technique this round (placeholder)'), expr=bx,
     rule='paired Mount move: bottom (W) bridges and shoves, top (E) is tipped off its base')
make('mountBottomKazushiHit', Tx, bt, partner='mountBottomKazushi', status='top side of bottom Kazushi, paired with mountBottomKazushi',
     intent="The top fighter's side of bottom Kazushi: it kneels in the plain mountTop idle until the impact frame (3), when the bridge pitches it forward 3 px over the mounted fighter's head, chest dropping and both hands shooting down to post on the mat; it rocks back up and resettles into mountTop.",
     clips={'rule': 'plays on the top fighter when the bottom plays mountBottomKazushi; returns to mountTop', 'mountBottomKazushiHit': {'frames': list(range(8)), 'fps': 12, 'next': 'mountTop'}},
     expr=btx, fx=fx_bt, rule='paired Mount move: bottom (W) bridges and shoves, top (E) is tipped off its base', rm='per-frame step (screen px): pitched 3 px forward on the impact frame and back (net 0)')

LINGER = {'rule': 'Kazushi (Christopher 2026-11-06 18:16: an exclamation mark over the target\'s head that lingers for the duration of the Kazushi effect): the clip ends with kzMark over the target\'s head; while the caster\'s Kazushi mark is up (the rest of the round, or until the next Jiu-Jitsu technique spends it) the testbed keeps drawing NPAT kzMark 2 px above the top of the target\'s head on every state it plays, bobbing 1 px every 4 frames; it clears when the mark is spent or expires', 'mark': {'pattern': 'kzMark', 'palette': {'W': '#ffffff', '#': '#000000'}, 'anchor': 'headTop', 'gap': 2, 'bob': [0, 0, 0, 0, -1, -1, -1, -1], 'on': 'target', 'while': 'Kazushi'}}
for _st in ('mountKazushiHit', 'mountBottomKazushiHit'):
    _s = load(D + _st + '.json'); _s.setdefault('extra', {})['linger'] = LINGER; save(_s, D + _st + '.json')
if __name__ == '__main__': print('ok')

# ================= Cord Garrote (Kyoketsu-Shoge; Mount, both positions; Maintained Submission) =================
# The blade stays hidden in the near fist (chainOnly) and the hemp cord runs taut from it to the far fist (chain.via),
# across the throat. Grips are snapped afterwards to the rendered fists: garrote_grips(state).
import json as _json
from PIL import Image as _Image
cc = load(D + 'mountCrossChoke.json'); ch = load(D + 'mountCrossChokeHit.json')
def _fr(spec, k):   # one frame of an approved spec as a tf() override
    return dict(src=0, bob=(spec['bob']['dy'][k], spec['bob']['head'][k], spec['bob']['arms'][k]), lean=(spec['lean']['dx']['pelvis'][k], spec['lean']['dx']['head'][k]),
                an=spec['arms']['near'][k], af=spec['arms']['far'][k])
gt = [tf(0), tf(1, bob=(10, 10, 11), lean=(0, 3), an=band(-75, -100), af=band(-70, -95)),
      _fr(cc, 2), _fr(cc, 3)] + [dict(_fr(cc, k), lean=(1, cc['lean']['dx']['head'][k] - 3)) for k in (4, 5, 6, 7)]
gb = [tf(0), tf(1), tf(2)] + [_fr(ch, k) for k in (3, 4, 5, 6, 7)]
gx = [None, None, None, 'pain', 'squint', 'pain', 'squint', 'pain']
fx_g = {'rule': "strain marks by the mounted fighter's face from the impact frame (3) while the cord squeezes", 'frames': [
    {'frame': 3, 'splash': [{'pattern': 'strain', 'at': [7, 50]}]}, {'frame': 5, 'splash': [{'pattern': 'strain', 'at': [6, 49]}]}, {'frame': 7, 'splash': [{'pattern': 'strain', 'at': [7, 50]}]}]}
HIGH = ['mountBottom body, clothing, hair, eyes', 'mountTop body, clothing, hair, eyes, far arm', 'mountTop arms', 'mountBottom arms (highest: the hands at the cord)']
def wrec(state):
    return [{'slot': 'main', 'layer': 'arms', 'items': ['kyoketsu-shoge'], 'status': STAT.format(state), 'rule': 'per frame: grip = near fist centre (snapped to the rendered fist); chainOnly: the blade is closed in the fist; chain.via = far fist centre, so the hemp cord runs taut between the fists across the throat; noWeight: the ring end is wound round the far hand',
             'depthRule': 'front: over body and clothing, under the arms layer (the fists close over the cord)', 'E': [{'grip': [44, 40], 'angle': -60, 'z': 'front', 'chainOnly': True, 'chain': {'via': [40, 40], 'droop': 0, 'z': 'front', 'to': [0, 1], 'noWeight': True}} for _ in range(8)], 'mirror': {'W': 'E'}}]
make('mountGarrote', T, gt, partner='mountGarroteHit', status='Cord Garrote from the top of Mount, paired with mountGarroteHit',
     intent='Kyoketsu-Shoge Cord Garrote from the top (Positional Rules: Both; Maintained Submission): from the mountTop idle the top fighter draws the hemp cord taut between its fists in front of its chest, drops it over the mounted fighter\'s head and sinks onto it, the cord biting across the throat on the impact frame (3); frames 4-7 loop while the submission is held, the fists hauling back.',
     clips={'rule': 'plays from mountTop; the mounted fighter plays mountGarroteHit; loops garroteHold while the Maintained Submission holds, then mountTop',
            'mountGarrote': {'frames': [0, 1, 2, 3], 'fps': 12, 'next': 'garroteHold'}, 'garroteHold': {'frames': [4, 5, 6, 7], 'fps': 6, 'loop': True, 'next': 'mountTop'}},
     ev=events(8, [3], 'Cord Garrote', '10 Physical; Silence 1rd (FORT or STR DC12); no Focus 1rd; Maintained Submission'),
     rule='paired Mount move: top (E) garrotes, bottom (W) is choked; the mounted fighter\'s arms are the highest layer', order=HIGH, weapons=wrec('mountGarrote'))
make('mountGarroteHit', Bt, gb, partner='mountGarrote', status='mounted side of Cord Garrote, paired with mountGarrote',
     intent="The mounted fighter's side of the top Cord Garrote: it lies in the plain mountBottom idle until the cord bites (impact frame 3), then both hands claw up at the cord on the throat on the highest layer, straining; frames 4-7 loop (garrotedHold) while the submission holds.",
     clips={'rule': 'plays on the mounted fighter when the top plays mountGarrote; loops garrotedHold, then mountBottom',
            'mountGarroteHit': {'frames': [0, 1, 2, 3], 'fps': 12, 'next': 'garrotedHold'}, 'garrotedHold': {'frames': [4, 5, 6, 7], 'fps': 6, 'loop': True, 'next': 'mountBottom'}},
     fx=fx_g, expr=gx, rule='paired Mount move: top (E) garrotes, bottom (W) is choked', order=HIGH)

def tips(state, k, row=0):
    im = _Image.open(D + state + '/arms.png').convert('RGBA'); px = im.load()
    pts = [(x, y) for y in range(64) for x in range(64) if px[k * 64 + x, row * 64 + y][3] and px[k * 64 + x, row * 64 + y][:3] != (0, 0, 0)]
    x, y = max(pts, key=lambda q: (q[0], -q[1])); return [x - 1, y]
# side-on the far fist sits right behind the near one, so the cord is drawn as a loop: from the near fist down round the
# mounted fighter's throat and back up into the fist. LOOP[k] = (via offset from the fist, to offset from via, droop)
LOOP = {0: None, 1: ((-4, 3), (4, -3), 2), 2: ((-1, 5), (2, -5), 1)}
def garrote_grips(state, top=True):
    s = _json.load(open(D + state + '.json')); w = s['weapons'][0]; row = s['directions'].index('E')
    for k, p in enumerate(w['E']):
        n = tips(state, k, row); p['grip'] = n
        lp = LOOP.get(k, ((-1, 4), (2, -4), 1))
        if lp is None: p['chain'] = {'via': [n[0], n[1] + 1], 'droop': 0, 'z': 'front', 'to': [0, 2], 'noWeight': True}   # wound in the fist
        else: p['chain'] = {'via': [n[0] + lp[0][0], n[1] + lp[0][1]], 'droop': lp[2], 'z': 'front', 'to': list(lp[1]), 'noWeight': True}
    save(s, D + state + '.json')

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[1] == '--grips': garrote_grips(sys.argv[2])
