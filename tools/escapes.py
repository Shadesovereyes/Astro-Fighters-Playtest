"""Submission escapes from under a locked Mount submission (Christopher 2026-11-26, thread "Animate Muscle Out and
Submission Struggle"). CANDIDATES only, E/W.
  Muscle Out Escape (STR): brute force. Big bridge and a two-handed heave that rips the grip off / curls the arm free.
  Submission Struggle (INT): technique. Hand-fight: two-on-one peel of the choking hand / hitchhiker elbow slip.
Each has a success (hold broken, both return to the Mount idles mountBottom / mountTop) and a fail (holder re-sinks the
hold, both return to the hold loop) variant, for Cross Choke (Strangle reuses it) and Arm bar.
Frames 0-3 are identical between success and fail (the outcome is decided on the impact frame 4, held on 5).
The holder holds the plain hold pose until frame 4 (impact-frame rule, 2026-11-04).
usage: python3 -I escapes.py   (writes specs into the playtest repo; then render with tools/character-posed.mjs)"""
import json, copy, sys
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import build, save, load
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
CAND = 'E/W candidate 2026-11-26 ({}), awaiting user approval; S/N to author'
band = lambda a, e: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
CT, CH, AT, AH, MT, MB, HE = (load(D + n + '.json') for n in
    ['mountCrossChoke', 'mountCrossChokeHit', 'mountArmbar', 'mountArmbarHit', 'mountTop', 'mountBottom', 'mountHipEscape'])
GH = load(D + 'mountBottomGarroteHit.json')
PAT = {k: GH['fx']['patterns'][k] for k in ('hitStar', 'strain', 'puff', 'speck', 'lines', 'tug', 'shift')}
BRIDGE = [p for p in HE['legs']['poses'] if p['name'] in ('bridge-near', 'bridge-far')]
IMPACT = 4
LY = (270, 10, 0, True)

def fr(spec, k):
    """frame k of an approved spec as a frame dict (lying bottom or kneeling top)"""
    P = [p['name'] for p in spec['legs']['poses']]
    br = spec.get('bodyRotation') or {}
    ex = (spec.get('expressions') or {}).get('frames', {}).get('E')
    d = dict(bob=(spec['bob']['dy'][k], spec['bob']['head'][k], spec['bob']['arms'][k]),
             lean=(spec['lean']['dx']['pelvis'][k], spec['lean']['dx']['head'][k]),
             ln=P[spec['legs']['near'][k]], lf=P[spec['legs']['far'][k]],
             an=copy.deepcopy(spec['arms']['near'][k]), af=copy.deepcopy(spec['arms']['far'][k]),
             expr=ex[k] if ex else None)
    if br: d['rot'] = (br['angle'][k], br['dx'][k], br['dy'][k], br['groundSnap'][k])
    else: d['rot'] = (0, 0, 0, False)
    return d

def F(base, **k): d = copy.deepcopy(base); d.update(k); return d

# ---------------- frame tables ----------------
# bottom (escaper) faces W in the pair; top (holder) faces E. Lying arm bands: -90 points up at the sky,
# around 0 points along the body toward the feet / the top fighter's hips.
cb, ct = fr(CH, 8), fr(CT, 8)          # cross choke hold
ab, at = fr(AH, 10), fr(AT, 10)        # arm bar hold
mb, mt = fr(MB, 0), fr(MT, 0)          # Mount idles (success end)

def tables():
    T = {}
    # --- Muscle Out Escape vs Cross Choke: grab both wrists, load the bridge, explode up and shove the arms off
    pre_b = [cb,
             F(cb, an=band(-64, -162), af=band(-60, -160), expr='squint'),
             F(cb, ln='bridge-near', lf='bridge-far', lean=(1, 0), an=band(-68, -150), af=band(-64, -148), expr='squint'),
             F(cb, ln='bridge-near', lf='bridge-far', lean=(2, 1), an=band(-72, -140), af=band(-68, -138), expr='squint')]
    pre_t = [ct, ct, ct, ct]
    heave = F(cb, ln='bridge-near', lf='bridge-far', lean=(4, 3), an=band(-86, -92), af=band(-82, -88), expr='squint')
    T['moChokeOk'] = (
        pre_b + [heave, heave,
                 F(mb, an=band(-80, -110), af=band(-74, -104), expr='squint'),
                 F(mb, an=band(-74, -136), af=band(-66, -126)), mb, mb],
        pre_t + [F(mt, bob=(10, 9, 10), lean=(-1, -3), an=band(-112, -150), af=band(-100, -135), expr='squint'),
                 F(mt, bob=(9, 8, 9), lean=(-1, -3), an=band(-114, -152), af=band(-102, -137), expr='squint'),
                 F(mt, bob=(9, 9, 10), lean=(0, 0), an=band(-90, -120), af=band(-80, -70)),
                 F(mt, bob=(10, 9, 10), lean=(0, 3), an=band(-35, -130), af=band(-48, -32)), mt, mt])
    T['moChokeFail'] = (
        pre_b + [F(heave, an=band(-78, -120), af=band(-74, -116)), F(heave, an=band(-78, -122), af=band(-74, -118)),
                 F(cb, an=band(-62, -166), af=band(-58, -164), expr='pain'),
                 F(cb, expr='pain'), F(cb, expr='pain'), cb],
        pre_t + [F(ct, bob=(13, 13, 14), lean=(2, 15), an=band(13, -38), af=band(9, -46)),
                 F(ct, bob=(13, 13, 14), lean=(2, 15), an=band(13, -38), af=band(9, -46)),
                 F(ct, bob=(16, 16, 17), lean=(2, 16), an=band(13, -36), af=band(9, -44)),
                 F(ct, bob=(16, 16, 17), lean=(2, 15)), ct, ct])
    # --- Submission Struggle vs Cross Choke: tuck the chin, two-on-one on the near wrist, turn the hips, peel it off
    pre_b = [cb,
             F(cb, an=band(-56, -164), af=band(-60, -176)),
             F(cb, ln='bridge-near', an=band(-50, -150), af=band(-52, -158), lean=(1, 0)),
             F(cb, ln='bridge-near', an=band(-44, -138), af=band(-46, -146), lean=(2, 0))]
    peel = F(cb, ln='bridge-near', lean=(2, 0), an=band(-18, -110), af=band(-14, -104))
    T['ssChokeOk'] = (
        pre_b + [peel, peel,
                 F(mb, an=band(-40, -120), af=band(-36, -112)),
                 F(mb, an=band(-60, -142), af=band(-52, -134)), mb, mb],
        pre_t + [F(ct, bob=(16, 16, 17), lean=(2, 15), an=band(2, -12), af=band(7, -49)),
                 F(ct, bob=(16, 16, 17), lean=(2, 15), an=band(2, -12), af=band(7, -49)),
                 F(mt, bob=(13, 13, 14), lean=(1, 10), an=band(-4, -60), af=band(-20, -40)),
                 F(mt, bob=(11, 11, 12), lean=(0, 6), an=band(-12, -130), af=band(-36, -28)), mt, mt])
    T['ssChokeFail'] = (
        pre_b + [F(peel, an=band(-40, -136), af=band(-42, -144)), F(peel, an=band(-46, -146), af=band(-48, -152), expr='pain'),
                 F(cb, an=band(-58, -168), af=band(-56, -168), expr='pain'),
                 F(cb, expr='pain'), F(cb, expr='squint'), cb],
        pre_t + [F(ct, bob=(16, 16, 17), lean=(2, 16), an=band(12, -38), af=band(8, -46)),
                 F(ct, bob=(16, 16, 17), lean=(2, 16), an=band(12, -38), af=band(8, -46)),
                 F(ct, bob=(16, 16, 17), lean=(2, 15)),
                 F(ct, bob=(15, 15, 16), lean=(2, 15)), ct, ct])
    # --- Muscle Out Escape vs Arm bar: clasp the trapped forearm with the free hand, bridge, curl it out by force
    pre_b = [ab,
             F(ab, af=band(-66, -96), expr='squint'),
             F(ab, ln='bridge-near', lf='bridge-far', lean=(1, 0), an=band(-80, -88), af=band(-70, -100), expr='squint'),
             F(ab, ln='bridge-near', lf='bridge-far', lean=(2, 1), an=band(-80, -98), af=band(-72, -110), expr='squint')]
    pre_t = [at, at, at, at]
    curl = F(ab, ln='bridge-near', lf='bridge-far', lean=(4, 3), an=band(-58, -162), af=band(-54, -152), expr='squint')
    T['moArmbarOk'] = (
        pre_b + [curl, curl,
                 F(mb, an=band(-62, -158), af=band(-56, -146), expr='squint'),
                 F(mb, an=band(-68, -152), af=band(-58, -142)), mb, mb],
        pre_t + [F(at, bob=(12, 12, 13), lean=(1, 6), an=band(-40, -20), af=band(-36, -18), expr='squint'),
                 F(at, bob=(12, 12, 13), lean=(1, 7), an=band(-38, -18), af=band(-34, -16), expr='squint'),
                 F(mt, bob=(11, 11, 12), lean=(1, 6), an=band(-24, -80), af=band(-38, -24)),
                 F(mt, bob=(10, 10, 11), lean=(0, 5), an=band(-18, -130), af=band(-40, -25)), mt, mt])
    T['moArmbarFail'] = (
        pre_b + [F(curl, an=band(-78, -108), af=band(-70, -116)), F(curl, an=band(-78, -96), af=band(-70, -108)),
                 F(ab, an=band(-78, -84), af=band(-44, -70), expr='pain'),
                 F(ab, expr='pain'), F(ab, expr='pain'), ab],
        pre_t + [F(at, bob=(10, 10, 11), lean=(-1, -5), an=band(-74, -74), af=band(-70, -70)),
                 F(at, bob=(10, 10, 11), lean=(-1, -6), an=band(-72, -72), af=band(-68, -68)),
                 F(at, lean=(-2, -9)), F(at, lean=(-1, -6)), at, at])
    # --- Submission Struggle vs Arm bar: hitchhiker. Turn the thumb and hips, free hand frames the hip, elbow slips out
    pre_b = [ab,
             F(ab, ln='bridge-near', lean=(1, 0), an=band(-78, -86)),
             F(ab, ln='bridge-near', lean=(2, 0), an=band(-80, -90), af=band(-14, -16)),
             F(ab, ln='bridge-near', lean=(2, 1), an=band(-78, -98), af=band(-8, -10))]
    slip = F(ab, ln='bridge-near', lean=(2, 1), an=band(-52, -158), af=band(-8, -10))
    T['ssArmbarOk'] = (
        pre_b + [slip, slip,
                 F(mb, an=band(-58, -156), af=band(-30, -70)),
                 F(mb, an=band(-66, -152), af=band(-50, -120)), mb, mb],
        pre_t + [F(at, bob=(9, 9, 10), lean=(-3, -11), an=band(-74, -100), af=band(-70, -96), expr='squint'),
                 F(at, bob=(9, 9, 10), lean=(-3, -11), an=band(-74, -100), af=band(-70, -96), expr='squint'),
                 F(mt, bob=(9, 9, 10), lean=(-1, -4), an=band(-46, -90), af=band(-50, -60)),
                 F(mt, bob=(10, 10, 11), lean=(0, 2), an=band(-24, -136), af=band(-42, -28)), mt, mt])
    T['ssArmbarFail'] = (
        pre_b + [F(slip, an=band(-78, -100)), F(slip, an=band(-78, -88), expr='pain'),
                 F(ab, af=band(-24, -40), expr='pain'),
                 F(ab, expr='pain'), F(ab, expr='squint'), ab],
        pre_t + [F(at, lean=(-2, -10), an=band(-64, -64), af=band(-60, -60)),
                 F(at, lean=(-2, -11), an=band(-66, -66), af=band(-62, -62)),
                 F(at, lean=(-2, -9)), F(at, lean=(-1, -6)), at, at])
    return T

# baked fx (white/neutral): hitStar on the impact frame at the grip, strain on loading frames, dust under the bridge
FXPAL = {'W': '#ffffff', 'w': '#e3e3e3', '#': '#000000'}
GRIP = {'Choke': [11, 44], 'Armbar': [20, 34]}       # bottom spec E coords (head at the left in E)
def fx_bottom(kind, hold, mo, ok):
    fr_ = []
    if mo:
        fr_ += [{'frame': 3, 'splash': [{'pattern': 'strain', 'at': [6, 49]}]}]
        fr_ += [{'frame': IMPACT, 'splash': [{'pattern': 'puff', 'at': [47, 58]}]},
                {'frame': IMPACT + 1, 'splash': [{'pattern': 'speck', 'at': [45, 58]}, {'pattern': 'speck', 'at': [51, 59]}]}]
    if not ok:
        fr_ += [{'frame': 6, 'splash': [{'pattern': 'strain', 'at': [6, 49]}]}, {'frame': 7, 'splash': [{'pattern': 'strain', 'at': [7, 50]}]}]
    return {'rule': f'{"Muscle Out Escape" if mo else "Submission Struggle"} vs {hold}: '
                    + ('strain while loading the bridge, dust puffs under the hips on the heave; ' if mo else '')
                    + ('the holder\'s side carries the impact star on frame 4' if ok else 'strain marks as the hold sinks back in'),
            'frames': fr_, 'palette': FXPAL, 'patterns': PAT}
def fx_top(kind, ok):
    star = 'hitStar' if ok else 'tug'
    at_ = [50, 44] if kind == 'Choke' else [42, 36]      # top spec E coords: the grip, ahead of the holder
    return {'rule': 'impact fx at the grip on the impact frame: a white hit star where the grip breaks (success) or a tug mark where it re-sinks (fail)',
            'top': True, 'frames': [{'frame': IMPACT, 'splash': [{'pattern': star, 'at': at_}]}], 'palette': FXPAL, 'patterns': PAT}

NAMES = {
    'moChokeOk': ('mountMuscleOutChoke', 'mountMuscleOutChokeHit', CH, CT, 'Choke', True, True),
    'moChokeFail': ('mountMuscleOutChokeFail', 'mountMuscleOutChokeFailHit', CH, CT, 'Choke', True, False),
    'ssChokeOk': ('mountStruggleChoke', 'mountStruggleChokeHit', CH, CT, 'Choke', False, True),
    'ssChokeFail': ('mountStruggleChokeFail', 'mountStruggleChokeFailHit', CH, CT, 'Choke', False, False),
    'moArmbarOk': ('mountMuscleOutArmbar', 'mountMuscleOutArmbarHit', AH, AT, 'Armbar', True, True),
    'moArmbarFail': ('mountMuscleOutArmbarFail', 'mountMuscleOutArmbarFailHit', AH, AT, 'Armbar', True, False),
    'ssArmbarOk': ('mountStruggleArmbar', 'mountStruggleArmbarHit', AH, AT, 'Armbar', False, True),
    'ssArmbarFail': ('mountStruggleArmbarFail', 'mountStruggleArmbarFailHit', AH, AT, 'Armbar', False, False),
}
HOLDLOOP = {'Choke': ('crossChokeHold', 'crossChokedHold', 'mountCrossChoke', 'mountCrossChokeHit'),
            'Armbar': ('armbarHold', 'armbarTrapped', 'mountArmbar', 'mountArmbarHit')}

def run(only=None):
    T = tables()
    out = []
    for key, (us, ts, BB, BT, kind, mo, ok) in NAMES.items():
        if only and key not in only: continue
        B, Tt = T[key]
        n = len(B); assert n == len(Tt) == 10, (key, n, len(Tt))
        move = 'Muscle Out Escape' if mo else 'Submission Struggle'
        hold = 'Cross Choke / Strangle' if kind == 'Choke' else 'Arm bar'
        nb, nt = ('mountBottom', 'mountTop') if ok else (HOLDLOOP[kind][3] + '@hold', HOLDLOOP[kind][2] + '@hold')
        e = [{'frame': i, 'type': 'startup' if i < IMPACT else 'active' if i == IMPACT else 'recovery'} for i in range(n)]
        e[IMPACT].update({'move': move, 'damage': 'none', 'effect': ('submission broken: hold ends, both back in the Mount' if ok else 'escape fails: the hold sinks back in')})
        e[IMPACT]['impactHold'] = 2
        ev = {'rule': 'per-frame gameplay data per facing; frame 4 is the impact (grip breaks or re-sinks), held on frame 5', 'E': e, 'W': copy.deepcopy(e)}
        lay = copy.deepcopy(BB['pair'])
        pair = lambda partner, top: dict({k: v for k, v in lay.items() if k not in ('partner', 'rule', 'top')},
                                         rule=f'paired Mount escape: the mounted fighter (W) escapes {hold}; the top fighter (E) holds it; frames 0-3 shared by success and fail',
                                         partner=partner, top=top)
        BB = copy.deepcopy(BB); BB['legs']['feet'].update({k: v for k, v in HE['legs']['feet'].items() if k not in BB['legs']['feet']})
        u = build(BB, us, B, status=CAND.format(f'{move} from under {hold}, {"success" if ok else "fail"}'),
                  intent=(f'{move} ({"STR, brute force" if mo else "INT, technique"}) from under a locked {hold}, {"success" if ok else "fail"}. ' +
                          {('Choke', True): 'Grabs both choking wrists, loads a big bridge and heaves straight up, ripping the grip off the neck.',
                           ('Choke', False): 'Tucks the chin, two-on-one on the near choking wrist, turns the hips and peels the hand off the collar.',
                           ('Armbar', True): 'Clasps the trapped forearm with the free hand, bridges and curls the straight arm out by force.',
                           ('Armbar', False): 'Hitchhiker: turns the thumb and hips, frames the holder\'s hip with the free hand and slips the elbow out.'}[(kind, mo)] +
                          (' Ends Mounted (mountBottom).' if ok else ' The holder re-sinks it; ends back in the hold loop.')),
                  newPoses=BRIDGE, pair=pair(ts, 'partner'),
                  clips={'rule': f'plays from the {HOLDLOOP[kind][1]} loop; the holder plays {ts} on the same frames',
                         us: {'frames': list(range(n)), 'fps': 12, 'next': nb}},
                  events=ev, rmRule='in place', rotRule='quarter turns only: lying (270) throughout',
                  fx=fx_bottom(kind, hold, mo, ok))
        BT = copy.deepcopy(BT); BT.setdefault('expressions', copy.deepcopy(MB['expressions']))
        t = build(BT, ts, Tt, status=CAND.format(f'holder side of {move} vs {hold}, {"success" if ok else "fail"}'),
                  intent=f'The holder keeps the plain {hold} hold pose until the impact frame 4, then ' +
                         ('loses the grip and rocks off balance, re-basing into the Mount (mountTop).' if ok else 're-sinks the hold and settles back into the hold loop.'),
                  pair=pair(us, 'self'),
                  clips={'rule': f'plays on the holder when the mounted fighter plays {us}',
                         ts: {'frames': list(range(n)), 'fps': 12, 'next': nt}},
                  events=None, rmRule='in place', fx=fx_top(kind, ok))
        for s in (u, t):
            s.pop('approved', None); s.pop('extension', None)
            s['expressions'] = copy.deepcopy(MB['expressions']) if s is u else copy.deepcopy(s.get('expressions') or MB['expressions'])
        u['expressions']['frames'] = {'E': [f.get('expr') for f in B]}
        t['expressions']['frames'] = {'E': [f.get('expr') for f in Tt]}
        if not any(f.get('expr') for f in Tt): t.pop('expressions')
        save(u, D + us + '.json'); save(t, D + ts + '.json'); out += [us, ts]
    return out

if __name__ == '__main__':
    print(' '.join(run(sys.argv[1:] or None)))
