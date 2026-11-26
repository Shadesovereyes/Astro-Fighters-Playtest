"""Submission escapes from under a locked Mount submission (Christopher 2026-11-26, thread "Animate Muscle Out and
Submission Struggle"). CANDIDATES only, E/W.
  Muscle Out Escape (STR): brute force. Big bridge and a two-handed heave that rips the grip off / curls the arm free.
  Submission Struggle (INT): technique. Hand-fight: two-on-one peel of the choking hand / hitchhiker elbow slip.
Each has a success (hold broken, both return to the Mount idles mountBottom / mountTop) and a fail (holder re-sinks the
hold, both return to the hold loop) variant, for Cross Choke (Strangle reuses it) and Arm bar.
Frames 0-3 are identical between success and fail (the outcome is decided on the impact frame 4, held on 5).
v2: frames 0-8 are a struggle phase; the holder answers each heave/pull on its own contact frame, never before it.
usage: python3 -I escapes.py   (writes specs into the playtest repo; then render with tools/character-posed.mjs)"""
import json, copy, sys
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import build, save, load
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
CAND = 'E/W candidate v2 2026-11-26 ({}), awaiting user approval; S/N to author'
band = lambda a, e: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
CT, CH, AT, AH, MT, MB, HE = (load(D + n + '.json') for n in
    ['mountCrossChoke', 'mountCrossChokeHit', 'mountArmbar', 'mountArmbarHit', 'mountTop', 'mountBottom', 'mountHipEscape'])
GH = load(D + 'mountBottomGarroteHit.json')
PAT = {k: GH['fx']['patterns'][k] for k in ('hitStar', 'strain', 'puff', 'speck', 'lines', 'tug', 'shift')}
BRIDGE = [p for p in HE['legs']['poses'] if p['name'] in ('bridge-near', 'bridge-far')]
IMPACT = 9
NFR = 16
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
    """v2 (Christopher 2026-11-26 10:58: more fx / more animation to illustrate the struggle and the muscling):
    a 9-frame struggle phase (repeated heaves or peels, the holder answering each one on its contact frame, a trembling
    stalemate), impact on frame 9 held on 10, 5 recovery frames. Frames 0-8 are shared by success and fail.
    Each entry: (bottom frames, top frames, bottom fx, top fx); fx = {frame: [(pattern, [x, y]), ...]}."""
    T = {}
    S, ST, SW, SH, TG, SF, PF, SP, LN, VL, VR, CV = 'strain', 'hitStar', 'sweat', 'shake', 'tug', 'swish', 'puff', 'speck', 'lines', 'vibeL', 'vibeR', 'chevron'
    # bottom E coords: face ~[6,49]; choke grip ~[14,41]; arm bar fist ~[22,30]; hips ~[30,58]; planted feet ~[47,58]
    # top E coords: face ~[46,20] in the choke lean, ~[38,16] sitting back in the arm bar
    # ---------------- Muscle Out Escape vs Cross Choke ----------------
    g1 = F(cb, an=band(-64, -162), af=band(-60, -160), expr='squint')
    ld = lambda l, a: F(cb, ln='bridge-near', lf='bridge-far', lean=l, an=band(-68 - a, -150 + a), af=band(-64 - a, -148 + a), expr='squint')
    pre_b = [cb, g1, ld((1, 0), 0), ld((3, 2), 8), F(g1, lean=(0, 0)), ld((2, 1), 4), ld((4, 3), 14), ld((4, 3), 16), ld((4, 3), 13)]
    up = lambda d, l=(2, 13), a=0: F(ct, bob=(15 - d, 15 - d, 16 - d), lean=l, an=band(11 + a, -41 - a), af=band(7 + a, -49 - a))
    pre_t = [ct, ct, ct, up(2), up(-1, (2, 16), 2), ct, up(3, (2, 12), 3), up(3, (2, 12), 4), up(2, (2, 13), 3)]
    fb = {1: [(S, [6, 49])], 2: [(S, [6, 49])], 3: [(PF, [47, 58])], 4: [(SW, [10, 46])], 5: [(S, [6, 49])],
          6: [(PF, [47, 58]), (S, [5, 48])], 7: [(SW, [9, 45])], 8: [(S, [6, 49]), (SW, [10, 47])]}
    ft = {3: [(VR, [52, 42])], 4: [(S, [55, 28])], 6: [(VR, [52, 43]), (VR, [55, 41]), (S, [55, 28])], 7: [(VR, [52, 43]), (VR, [55, 41]), (SW, [52, 22])], 8: [(VR, [52, 42]), (S, [55, 28])]}
    heave = F(cb, ln='bridge-near', lf='bridge-far', lean=(4, 3), an=band(-86, -92), af=band(-82, -88), expr='squint')
    T['moChokeOk'] = (
        pre_b + [heave, heave, F(mb, an=band(-80, -110), af=band(-74, -104), expr='squint'),
                 F(mb, an=band(-74, -136), af=band(-66, -126)), F(mb, an=band(-72, -144), af=band(-63, -134)), mb, mb],
        pre_t + [F(mt, bob=(10, 9, 10), lean=(-1, -3), an=band(-112, -150), af=band(-100, -135), expr='squint'),
                 F(mt, bob=(9, 8, 9), lean=(-1, -3), an=band(-114, -152), af=band(-102, -137), expr='squint'),
                 F(mt, bob=(9, 9, 10), lean=(0, 0), an=band(-90, -120), af=band(-80, -70)),
                 F(mt, bob=(10, 9, 10), lean=(0, 3), an=band(-35, -130), af=band(-48, -32)),
                 F(mt, bob=(10, 10, 11), lean=(0, 4), an=band(-22, -142), af=band(-42, -27)), mt, mt],
        {**fb, **{9: [(PF, [47, 58]), (PF, [38, 59])], 10: [(SP, [45, 58]), (SP, [51, 59])]}},
        {**ft, **{9: [(ST, [48, 42]), (LN, [40, 6])], 10: [(SW, [44, 16])]}})
    T['moChokeFail'] = (
        pre_b + [F(heave, an=band(-78, -120), af=band(-74, -116)), F(heave, an=band(-78, -122), af=band(-74, -118)),
                 F(cb, an=band(-62, -166), af=band(-58, -164), expr='pain'),
                 F(cb, expr='pain'), F(cb, expr='pain'), F(cb, expr='squint'), cb],
        pre_t + [F(ct, bob=(13, 13, 14), lean=(2, 15), an=band(13, -38), af=band(9, -46)),
                 F(ct, bob=(13, 13, 14), lean=(2, 15), an=band(13, -38), af=band(9, -46)),
                 F(ct, bob=(16, 16, 17), lean=(2, 16), an=band(13, -36), af=band(9, -44)),
                 F(ct, bob=(16, 16, 17), lean=(2, 15)), F(ct, bob=(15, 15, 16)), ct, ct],
        {**fb, **{9: [(PF, [47, 58])], 11: [(S, [6, 49]), (SW, [4, 44])], 12: [(S, [7, 50])], 13: [(SW, [3, 45])]}},
        {**ft, **{9: [(TG, [48, 44])], 11: [(TG, [47, 45])]}})
    # ---------------- Submission Struggle vs Cross Choke ----------------
    tw = lambda a, l=(0, 0), legs=('lying-near', 'lying-far'), e=None: F(cb, ln=legs[0], lf=legs[1], lean=l, an=band(-56 + a, -164 + a), af=band(-60 + a, -176 + a), expr=e)
    BN = ('bridge-near', 'lying-far')
    pre_b = [cb, tw(0), tw(8), tw(2, e='squint'), tw(4, (1, 0), BN), tw(14, (1, 0), BN), tw(12, (3, 0), BN), tw(20, (3, 0), BN, 'squint'), tw(22, (3, 0), BN, 'squint')]
    pull = lambda a, l=(2, 14): F(ct, lean=l, an=band(11 - a, -41 + a), af=band(7, -49))
    pre_t = [ct, ct, pull(3), F(ct, bob=(16, 16, 17), lean=(2, 15)), ct, pull(5), F(ct, lean=(2, 15)), pull(8, (2, 15)), pull(9, (2, 15))]
    fb = {3: [(S, [6, 49])], 4: [(SF, [38, 44])], 6: [(SF, [39, 44])], 7: [(S, [6, 49])], 8: [(SW, [10, 46])]}

    ft = {1: [(CV, [51, 47])], 2: [(CV, [51, 48])], 3: [(TG, [48, 44])], 5: [(CV, [51, 48])], 7: [(CV, [51, 49]), (S, [55, 28])], 8: [(CV, [51, 50]), (SW, [52, 22])]}
    peel = F(cb, ln='bridge-near', lean=(2, 0), an=band(-18, -110), af=band(-14, -104))
    T['ssChokeOk'] = (
        pre_b + [peel, peel, F(mb, an=band(-40, -120), af=band(-36, -112)),
                 F(mb, an=band(-60, -142), af=band(-52, -134)), F(mb, an=band(-66, -146), af=band(-56, -137)), mb, mb],
        pre_t + [F(ct, bob=(16, 16, 17), lean=(2, 15), an=band(2, -12), af=band(7, -49)),
                 F(ct, bob=(16, 16, 17), lean=(2, 15), an=band(2, -12), af=band(7, -49)),
                 F(mt, bob=(13, 13, 14), lean=(1, 10), an=band(-4, -60), af=band(-20, -40)),
                 F(mt, bob=(11, 11, 12), lean=(0, 6), an=band(-12, -130), af=band(-36, -28)),
                 F(mt, bob=(10, 10, 11), lean=(0, 5), an=band(-14, -142), af=band(-38, -26)), mt, mt],
        {**fb, **{9: [(SF, [38, 44])], 10: [(SP, [20, 50])]}},
        {**ft, **{9: [(ST, [48, 42])]}})
    T['ssChokeFail'] = (
        pre_b + [F(peel, an=band(-40, -136), af=band(-42, -144)), F(peel, an=band(-46, -146), af=band(-48, -152), expr='pain'),
                 F(cb, an=band(-58, -168), af=band(-56, -168), expr='pain'),
                 F(cb, expr='pain'), F(cb, expr='pain'), F(cb, expr='squint'), cb],
        pre_t + [F(ct, bob=(16, 16, 17), lean=(2, 16), an=band(12, -38), af=band(8, -46)),
                 F(ct, bob=(16, 16, 17), lean=(2, 16), an=band(12, -38), af=band(8, -46)),
                 F(ct, bob=(16, 16, 17), lean=(2, 15)), F(ct, bob=(15, 15, 16), lean=(2, 15)), F(ct, bob=(15, 15, 16)), ct, ct],
        {**fb, **{11: [(S, [6, 49])], 12: [(S, [7, 50]), (SW, [4, 44])]}},
        {**ft, **{9: [(TG, [48, 44])], 10: [(TG, [47, 45])]}})
    # ---------------- Muscle Out Escape vs Arm bar ----------------
    cl = lambda e_, l=(0, 0), legs=('lying-near', 'lying-far'), x='squint': F(ab, ln=legs[0], lf=legs[1], lean=l, an=band(-80, e_), af=band(-70, e_ - 12), expr=x)
    BB2 = ('bridge-near', 'bridge-far')
    pre_b = [ab, F(ab, af=band(-66, -96), expr='squint'), cl(-88, (1, 0), BB2), cl(-100, (3, 2), BB2), cl(-84, (1, 0), BB2, 'pain'),
             cl(-92, (2, 1), BB2), cl(-106, (4, 3), BB2), cl(-108, (4, 3), BB2), cl(-104, (4, 3), BB2)]
    yk = lambda l, a=0: F(at, lean=l, an=band(-62 - a, -62 - a), af=band(-58 - a, -58 - a))
    pre_t = [at, at, at, yk((0, -1), 6), yk((-2, -9), -2), at, yk((0, 0), 8), yk((0, 1), 9), yk((0, 0), 8)]
    fb = {1: [(S, [6, 49])], 2: [(S, [6, 49])], 3: [(PF, [47, 58])], 4: [(SW, [10, 46]), (S, [6, 49])], 5: [(S, [6, 49])],
          6: [(PF, [47, 58])], 7: [(SW, [9, 45])], 8: [(S, [6, 49])]}
    ft = {3: [(VR, [47, 36])], 4: [(S, [39, 22])], 6: [(VR, [47, 35]), (S, [39, 22])], 7: [(VR, [47, 36]), (VR, [50, 34]), (SW, [31, 17])], 8: [(VR, [47, 36]), (S, [39, 22])]}
    curl = F(ab, ln='bridge-near', lf='bridge-far', lean=(4, 3), an=band(-58, -162), af=band(-54, -152), expr='squint')
    T['moArmbarOk'] = (
        pre_b + [curl, curl, F(mb, an=band(-62, -158), af=band(-56, -146), expr='squint'),
                 F(mb, an=band(-68, -152), af=band(-58, -142)), F(mb, an=band(-69, -151), af=band(-59, -141)), mb, mb],
        pre_t + [F(at, bob=(12, 12, 13), lean=(1, 6), an=band(-40, -20), af=band(-36, -18), expr='squint'),
                 F(at, bob=(12, 12, 13), lean=(1, 7), an=band(-38, -18), af=band(-34, -16), expr='squint'),
                 F(mt, bob=(11, 11, 12), lean=(1, 6), an=band(-24, -80), af=band(-38, -24)),
                 F(mt, bob=(10, 10, 11), lean=(0, 5), an=band(-18, -130), af=band(-40, -25)),
                 F(mt, bob=(10, 10, 11), lean=(0, 4), an=band(-16, -142), af=band(-40, -25)), mt, mt],
        {**fb, **{9: [(PF, [47, 58]), (PF, [38, 59])], 10: [(SP, [45, 58]), (SP, [51, 59])]}},
        {**ft, **{9: [(ST, [40, 36]), (LN, [30, 8])], 10: [(SW, [31, 18])]}})
    T['moArmbarFail'] = (
        pre_b + [F(curl, an=band(-78, -108), af=band(-70, -116)), F(curl, an=band(-78, -96), af=band(-70, -108)),
                 F(ab, an=band(-78, -84), af=band(-44, -70), expr='pain'),
                 F(ab, expr='pain'), F(ab, expr='pain'), F(ab, expr='squint'), ab],
        pre_t + [F(at, bob=(10, 10, 11), lean=(-1, -5), an=band(-74, -74), af=band(-70, -70)),
                 F(at, bob=(10, 10, 11), lean=(-1, -6), an=band(-72, -72), af=band(-68, -68)),
                 F(at, lean=(-2, -9)), F(at, lean=(-1, -6)), F(at, lean=(-1, -5)), at, at],
        {**fb, **{9: [(PF, [47, 58])], 11: [(S, [6, 49]), (SW, [4, 44])], 12: [(S, [7, 50])]}},
        {**ft, **{9: [(TG, [42, 36])], 11: [(TG, [41, 37])]}})
    # ---------------- Submission Struggle vs Arm bar (hitchhiker) ----------------
    hh = lambda e_, af_, l=(0, 0), legs=BN, x=None: F(ab, ln=legs[0], lf=legs[1], lean=l, an=band(-78, e_), af=af_, expr=x)
    AF0 = ab['af']
    pre_b = [ab, hh(-84, AF0, (0, 0), ('lying-near', 'lying-far')), hh(-86, AF0, (1, 0)), hh(-88, band(-30, -40), (1, 0)), hh(-90, band(-14, -16), (2, 0)),
             hh(-86, band(-14, -16), (1, 0), x='squint'), hh(-94, band(-8, -10), (3, 1)), hh(-98, band(-8, -10), (3, 1), x='squint'), hh(-100, band(-6, -8), (3, 1), x='squint')]
    pre_t = [at, at, at, at, F(at, lean=(-2, -8)), F(at, lean=(-2, -9), an=band(-64, -64)), at, F(at, lean=(-1, -6)), F(at, lean=(-2, -7), an=band(-63, -63))]
    fb = {2: [(SF, [38, 44])], 4: [(SF, [39, 44])], 5: [(S, [6, 49])], 6: [(SF, [40, 44])], 7: [(S, [6, 49])], 8: [(SW, [10, 46])]}

    ft = {1: [(SF, [45, 32])], 3: [(CV, [41, 42])], 4: [(TG, [40, 36])], 5: [(S, [39, 22])], 6: [(CV, [41, 43])], 8: [(TG, [40, 36]), (SW, [31, 17])]}
    slip = F(ab, ln='bridge-near', lean=(2, 1), an=band(-52, -158), af=band(-8, -10))
    T['ssArmbarOk'] = (
        pre_b + [slip, slip, F(mb, an=band(-58, -156), af=band(-30, -70)),
                 F(mb, an=band(-66, -152), af=band(-50, -120)), F(mb, an=band(-68, -151), af=band(-55, -130)), mb, mb],
        pre_t + [F(at, bob=(9, 9, 10), lean=(-3, -11), an=band(-74, -100), af=band(-70, -96), expr='squint'),
                 F(at, bob=(9, 9, 10), lean=(-3, -11), an=band(-74, -100), af=band(-70, -96), expr='squint'),
                 F(mt, bob=(9, 9, 10), lean=(-1, -4), an=band(-46, -90), af=band(-50, -60)),
                 F(mt, bob=(10, 10, 11), lean=(0, 2), an=band(-24, -136), af=band(-42, -28)),
                 F(mt, bob=(10, 10, 11), lean=(0, 3), an=band(-20, -142), af=band(-41, -26)), mt, mt],
        {**fb, **{9: [(SF, [38, 44])], 10: [(SP, [24, 32])]}},
        {**ft, **{9: [(ST, [42, 36])]}})
    T['ssArmbarFail'] = (
        pre_b + [F(slip, an=band(-78, -100)), F(slip, an=band(-78, -88), expr='pain'),
                 F(ab, af=band(-24, -40), expr='pain'),
                 F(ab, expr='pain'), F(ab, expr='pain'), F(ab, expr='squint'), ab],
        pre_t + [F(at, lean=(-2, -10), an=band(-64, -64), af=band(-60, -60)),
                 F(at, lean=(-2, -11), an=band(-66, -66), af=band(-62, -62)),
                 F(at, lean=(-2, -9)), F(at, lean=(-1, -6)), F(at, lean=(-1, -5)), at, at],
        {**fb, **{11: [(S, [6, 49])], 12: [(S, [7, 50]), (SW, [4, 44])]}},
        {**ft, **{9: [(TG, [42, 36])], 10: [(TG, [41, 37])]}})
    return T

# baked fx (white/neutral): strain (veins), sweat drops, shake marks at the straining grip, tug marks on a pull, shift
# marks on a hip turn, dust puffs from the planted bridge, hit star / tug on the impact frame. Bottom fx draw with the
# bottom fighter; the holder's fx are drawn over both fighters (fx.top).
FXPAL = {'W': '#ffffff', 'w': '#e3e3e3', '#': '#000000', 'b': '#bfe3ff'}
PAT['sweat'] = ['.#.', '#b#', '#W#', '.#.']
PAT['shake'] = ['#...#', '.....', '#...#', '.....', '#...#']
PAT['vibeL'] = ['.#W', '#W.', '#W.', '.#W', '#W.', '#W.', '.#W']        # vibration arcs either side of a straining grip
PAT['vibeR'] = [r[::-1] for r in PAT['vibeL']]
PAT['chevron'] = ['#W#...#W#', '.#W#.#W#.', '..#W#W#..', '...#W#...']  # pull mark: the wrist being dragged down
PAT['swish'] = ['..###.', '.#WWW#', '#W##..', '.#WWW#', '..###.']     # hip-turn motion mark
def fxrec(d, rule, top=False):
    r = {'rule': rule, 'frames': [{'frame': k, 'splash': [{'pattern': p, 'at': at_} for p, at_ in v]} for k, v in sorted(d.items())],
         'palette': FXPAL, 'patterns': PAT}
    if top: r['top'] = True
    return r

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
        B, Tt, FB, FT = T[key]
        n = len(B); assert n == len(Tt) == NFR, (key, n, len(Tt))
        move = 'Muscle Out Escape' if mo else 'Submission Struggle'
        hold = 'Cross Choke / Strangle' if kind == 'Choke' else 'Arm bar'
        nb, nt = ('mountBottom', 'mountTop') if ok else (HOLDLOOP[kind][3] + '@hold', HOLDLOOP[kind][2] + '@hold')
        e = [{'frame': i, 'type': 'startup' if i < IMPACT else 'active' if i == IMPACT else 'recovery'} for i in range(n)]
        e[IMPACT].update({'move': move, 'damage': 'none', 'effect': ('submission broken: hold ends, both back in the Mount' if ok else 'escape fails: the hold sinks back in')})
        e[IMPACT]['impactHold'] = 2
        for i in range(1, IMPACT): e[i]['struggle'] = True
        ev = {'rule': 'per-frame gameplay data per facing; frames 1-8 are the struggle (shared by success and fail), frame 9 is the impact (grip breaks or re-sinks), held on frame 10', 'E': e, 'W': copy.deepcopy(e)}
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
                         us: {'frames': list(range(n)), 'fps': 10, 'next': nb}},
                  events=ev, rmRule='in place', rotRule='quarter turns only: lying (270) throughout',
                  fx=fxrec(FB, f'{move} vs {hold}: effort fx on the struggle frames (strain, sweat, shake/tug/shift marks, bridge dust)'))
        BT = copy.deepcopy(BT); BT.setdefault('expressions', copy.deepcopy(MB['expressions']))
        t = build(BT, ts, Tt, status=CAND.format(f'holder side of {move} vs {hold}, {"success" if ok else "fail"}'),
                  intent=f'The holder keeps the plain {hold} hold pose until the impact frame 4, then ' +
                         ('loses the grip and rocks off balance, re-basing into the Mount (mountTop).' if ok else 're-sinks the hold and settles back into the hold loop.'),
                  pair=pair(us, 'self'),
                  clips={'rule': f'plays on the holder when the mounted fighter plays {us}',
                         ts: {'frames': list(range(n)), 'fps': 10, 'next': nt}},
                  events=None, rmRule='in place', fx=fxrec(FT, 'the holder answers each heave/pull on its contact frame; hit star where the grip breaks (success) or tug where it re-sinks (fail)', top=True))
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
