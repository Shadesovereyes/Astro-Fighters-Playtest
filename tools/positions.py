"""New grappling positions (Christopher 2026-11-26, thread "Animate new grappling escapes and transitions"):
Guard, Side Control, Back Control, Back Clinch. Paired 4-frame idles, E/W CANDIDATES v1. Nothing wired into the testbed.
Each pair: the controlling fighter (top / taker / holder) faces E and is the pair's 'self'; the partner faces W.
Back positions: the victim faces away from the taker (faceFlip on every frame), so both look the same way.
usage: python3 -I positions.py  (writes specs into the playtest repo; render with tools/character-posed.mjs)"""
import json, copy, sys
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import build, save, load
D = '/home/claude/astro-fighters-playtest/production/source/characters/anim/male/'
CAND = 'E/W candidate v1 2026-11-26 ({}), awaiting user approval; S/N to author'
band = lambda a, e: {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}}
P = lambda name, hx, hr, kx, kr, ax, ar, foot: {'name': name, 'construction': 'band', 'hipX': hx, 'hipRow': hr, 'kneeX': kx, 'kneeRow': kr, 'ankle': [ax, ar], 'foot': foot}
MT, MB, CH, CD = (load(D + n + '.json') for n in ('mountTop', 'mountBottom', 'clinchHold', 'clinchHeld'))
def withx(s):
    s = copy.deepcopy(s)
    if not s.get('expressions'): s['expressions'] = copy.deepcopy(MB['expressions'])
    s['legs']['feet'].update({k: v for k, v in MT['legs']['feet'].items() if k not in s['legs']['feet']})
    return s
MT, MB, CH, CD = map(withx, (MT, MB, CH, CD))

def fr(spec, k=0):
    P_ = [p['name'] for p in spec['legs']['poses']]
    br = spec.get('bodyRotation') or {}
    ex = (spec.get('expressions') or {}).get('frames', {}).get('E')
    d = dict(bob=(spec['bob']['dy'][k], spec['bob']['head'][k], spec['bob']['arms'][k]),
             lean=(spec['lean']['dx']['pelvis'][k], spec['lean']['dx']['head'][k]),
             ln=P_[spec['legs']['near'][k]], lf=P_[spec['legs']['far'][k]],
             an=copy.deepcopy(spec['arms']['near'][k]), af=copy.deepcopy(spec['arms']['far'][k]), expr=ex[k] if ex else None, root=(0, 0))
    d['rot'] = (br['angle'][k], br['dx'][k], br['dy'][k], br['groundSnap'][k]) if br else (0, 0, 0, False)
    return d
def F(base, **k): d = copy.deepcopy(base); d.update(k); return d
def breathe(f, amp=((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 0, 1)), arms=None):
    """4-frame idle: a slow breath on the head/arms bob; optional per-frame arm angle nudges"""
    out = []
    for k, (a, b, c) in enumerate(amp):
        bb = f['bob']; g = F(f, bob=(bb[0] + a, bb[1] + b, bb[2] + c))
        if arms:
            dn, df = arms[k]
            g['an'] = band(f['an']['angle'] + dn, f['an']['elbow']['angle']); g['af'] = band(f['af']['angle'] + df, f['af']['elbow']['angle'])
        out.append(g)
    return out

# layering, back to front (pair.layering strings follow the existing clips' wording)
L_GUARD = ['guardBottom far-arm (gripping the far collar, behind the top fighter)', 'guardTop far-arm, body, clothing, hair, eyes', 'guardBottom body, clothing, hair, eyes (its legs wrap over the top fighter\'s hips)', 'guardTop arms', 'guardBottom arms']
L_SIDE = ['sideControlTop far-arm, body, clothing, hair, eyes (on the far side of the bottom fighter)', 'sideControlTop arms (crossface and underhook, behind the bottom fighter)', 'sideControlBottom far-arm, body, clothing, hair, eyes (its bent knees in front of the top fighter\'s hips)', 'sideControlBottom arms (the near arm wrapped over the top fighter\'s shoulder)']
L_BACK = lambda a, b: [f'{a} far-arm, body, clothing, hair, eyes (behind)', f'{b} far-arm, body, clothing, hair, eyes', f'{b} arms', f'{a} arms (wrapped in front)']

def specs():
    out = {}
    # ---------------- Guard (closed guard) ----------------
    gl = [P('cg-near', 31, 40, 45, 49, 34, 54, 'pointDL'), P('cg-far', 30, 40, 43, 50, 32, 55, 'pointDL')]
    b = F(fr(MB), ln='cg-near', lf='cg-far', an=band(-40, -70), af=band(-36, -66), expr=None)
    t = F(fr(MT), lean=(0, 1), an=band(-30, -70), af=band(-36, -76))
    out['guard'] = dict(names=('guardTop', 'guardBottom'), base=(MT, MB), pdx=12, newB=gl,
        A=breathe(t, arms=[(0, 0), (1, 0), (1, 1), (0, 1)]), B=breathe(b, amp=((0, 0, 0), (0, 0, 0), (0, 1, 1), (0, 1, 1)), arms=[(0, 0), (-2, 0), (-2, -2), (0, -2)]),
        layering=L_GUARD, bottomOver=True,
        intentA='Guard, top (in the guard): kneeling between the guard player\'s legs, posture up, hands posted on their belly and hips; the bottom fighter\'s legs lock around the waist.',
        intentB='Guard, bottom (guard player): flat on the back, legs closed around the top fighter\'s waist (ankles crossed behind the back), both hands gripping the top fighter\'s collar/sleeves to break posture.',
        rot='bottom: laid flat on the back (270, as mountBottom)')
    # ---------------- Side Control ----------------
    tl = [P('sc-near', 33, 42, 46, 44, 45, 54, 'pointDR'), P('sc-far', 31, 42, 45, 44, 45, 54, 'pointDR')]
    bl = [P('scb-near', 32, 42, 44, 48, 36, 57, 'pointDL'), P('scb-far', 31, 42, 42, 48, 35, 57, 'pointDL')]
    t = F(fr(MT), bob=(0, 0, 0), lean=(0, 0), ln='sc-near', lf='sc-far', an=band(-100, -175), af=band(-95, -170), expr='squint', rot=(90, -10, 1, False))
    b = F(fr(MB), ln='scb-near', lf='scb-far', an=band(-85, 20), af=band(-45, -30), expr='squint')
    out['side'] = dict(names=('sideControlTop', 'sideControlBottom'), base=(MT, MB), pdx=4, newA=tl, newB=bl,
        A=breathe(t, amp=((0, 0, 0), (0, 0, 0), (0, 0, 1), (0, 0, 1)), arms=[(0, 0), (0, 0), (-2, 0), (-2, 0)]), B=breathe(b, amp=((0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)), arms=[(0, 0), (2, 0), (2, 2), (0, 2)]),
        layering=L_SIDE, bottomOver=False, topBehind=True,
        intentA='Side Control, top (Christopher\'s references 2026-11-26): on the far side of the bottom fighter, a quarter turn chest-down (90) draped across their chest, head down beside their head, hips up on the knees behind their bent legs, crossface arm under the head and the far arm underhooking.',
        intentB='Side Control, bottom: flat on the back (270), knees bent with the feet planted (in front of the top fighter\'s hips), the near arm wrapped over the top fighter\'s shoulder, face squeezed.',
        rot='top: a quarter turn chest-down (90, held above the ground on its knees); bottom: flat on the back (270)')
    # ---------------- Back Control (ground, seated, hooks in) ----------------
    al = [P('hook-near', 33, 52, 42, 51, 50, 53, 'levelR'), P('hook-far', 31, 52, 41, 51, 49, 53, 'levelR')]
    vl = [P('sitx-near', 33, 52, 43, 53, 53, 53, 'levelR'), P('sitx-far', 31, 52, 42, 53, 52, 53, 'levelR')]
    a = F(fr(MT), lean=(0, 1), an=band(-66, -112), af=band(-62, -100), rot=(0, 0, 0, True))
    v = F(fr(MT), bob=(11, 11, 11), lean=(-1, -1), ln='sitx-near', lf='sitx-far', an=band(-40, -170), af=band(-46, -160), expr='squint', rot=(0, 0, 0, True))
    out['backctl'] = dict(names=('backControlTop', 'backControlBottom'), base=(MT, MT), pdx=15, newA=al, newB=vl, flipB=True,
        A=breathe(a, amp=((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 0, 1))), B=breathe(v, amp=((0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)), arms=[(0, 0), (3, 0), (3, 3), (0, 3)]),
        layering=L_BACK('backControlTop', 'backControlBottom'), bottomOver=False,
        intentA='Back Control, taker: kneeling up behind the seated opponent, chest to their back, seat-belt grip (near arm over the shoulder across the chest, far arm under the armpit), chest glued to their back.',
        intentB='Back Control, victim: sat on the ground facing away from the taker (faceFlip), legs out, leaning back into the taker\'s chest, both hands fighting the seat-belt wrist at the chest.',
        rot='taker kneeling, victim seated (both groundSnap)')
    # ---------------- Back Clinch (standing) ----------------
    a = F(fr(CH), lean=(1, 5), bob=(3, 3, 4), an=band(-35, -70), af=band(-40, -75), ln='guard-low-rear', lf='guard-low-lead')
    v = F(fr(CD), lean=(-1, 1), bob=(2, 2, 2), an=band(-8, -50), af=band(-14, -55), ln='stance-rear', lf='stance-lead', expr='squint')
    out['backclinch'] = dict(names=('backClinchHold', 'backClinchHeld'), base=(CH, CD), pdx=12, flipB=True,
        A=breathe(a, amp=((0, 0, 0), (0, 0, 1), (1, 1, 1), (1, 0, 1))), B=breathe(v, amp=((0, 0, 0), (0, 1, 0), (1, 1, 1), (1, 0, 1)), arms=[(0, 0), (3, 0), (3, 3), (0, 3)]),
        layering=L_BACK('backClinchHold', 'backClinchHeld'), bottomOver=False,
        intentA='Back Clinch, holder: standing chest to the opponent\'s back, body lock (both arms wrapped around the waist, hands locked at the belt), head tucked beside their shoulder.',
        intentB='Back Clinch, held: standing facing away from the holder (faceFlip), base wide, both hands prying at the locked hands on the belt.',
        rot='upright')
    return out

def run():
    done = []
    for key, s in specs().items():
        A, B = s['names']; bA, bB = s['base']
        pair = {'rule': f'paired position idle: {A} (E, the controlling fighter) with {B} (W)' + ('; the partner faces away (faceFlip): both look E' if s.get('flipB') else '') + '; the partner pivot sits partnerDx px ahead along the facing',
                'partner': B, 'partnerDx': s['pdx'], 'top': 'self', 'layering': s['layering']}
        if s.get('bottomOver'): pair['mountLayering'] = {'fromFrame': 0, 'order': s['layering'], 'bottomOver': True}
        if s.get('flipB'): pair['victimOver'] = True
        if s.get('topBehind'): pair['topBehind'] = True
        clipsA = {'rule': f'position idle loop; the partner plays {B}', A: {'frames': [0, 1, 2, 3], 'fps': 6, 'loop': True}}
        clipsB = {'rule': f'position idle loop; the partner plays {A}', B: {'frames': [0, 1, 2, 3], 'fps': 6, 'loop': True}}
        sa = build(bA, A, s['A'], status=CAND.format(s['intentA'].split(':')[0]), intent=s['intentA'], newPoses=s.get('newA', ()), pair=pair, clips=clipsA,
                   rmRule='in place', rotRule='quarter turns only: ' + s['rot'], bobRule='a slow breath')
        pb = dict(pair, partner=A, top='partner', rule=pair['rule'])
        sb = build(bB, B, s['B'], status=CAND.format(s['intentB'].split(':')[0]), intent=s['intentB'], newPoses=s.get('newB', ()), pair=pb, clips=clipsB,
                   rmRule='in place', rotRule='quarter turns only: ' + s['rot'], bobRule='a slow breath', extra={'faceFlip': [True] * 4} if s.get('flipB') else None)
        for sp in (sa, sb): sp.pop('approved', None); sp['fps'] = 6
        save(sa, D + A + '.json'); save(sb, D + B + '.json'); done += [A, B]
    return done

if __name__ == '__main__':
    print(' '.join(run()))
