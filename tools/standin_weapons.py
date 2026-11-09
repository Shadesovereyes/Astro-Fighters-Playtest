"""Weapon clips for abilities that still borrowed a nearby clip (Christopher 2026-11-06, thread "Animate stand-in and
Medical abilities"). Built on tanto.py's one-hand weapon machinery (two-link IK to each authored grip, weapon layer by
character-weapon.mjs). E/W first (W mirrors E), S/N after approval. Effects white/neutral.
  viperStrike       Viper Strike, free-standing (inside the clinch / Mount it plays clinchKnife / mountKnife): from the
                    one-hand knife guard the knife hand coils low by the hip, then darts up twice like a snake's
                    fangs into the midsection, a white spark on the first bite.
  ksStanceEntry     Kyoketsu-Shoge Stance: from the boxing guard the hand drops to the hip, draws the blade, flicks it
                    up and round once and settles into the one-hand guard (oneHandGuard, the stance idle).
  macheteSlash      Machete Slash (Bandit / Bandit Thug, new machete item): from the one-hand guard the machete is
                    hauled up over the shoulder, then chopped down diagonally through the target, smear and spark,
                    follow-through low, back to the guard.
Run: python3 tools/standin_weapons.py [state] ; node tools/character-posed.mjs male <state> ;
     python3 tools/standin_weapons.py --grips <state> ; node tools/character-weapon.mjs male <state> ;
     python3 tools/standin_weapons.py --fx <state> ; Guard clips also: python3 tools/standin_weapons.py --occlude <state>"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tanto as T
from tanto import fr

T.STAT = 'CANDIDATE 2026-11-06 (E/W; W mirrors E; S/N to author after approval)'
OG = dict(grip=(43, 35), angle=10, far=(39, 24))   # the approved oneHandGuard frame
def og(**k): return fr(**{**OG, **k})
H = dict(hidden=True)
APPROVED = {'macheteSlash': 'E/W approved by user 2026-11-06 18:12 (v3 raised blade on the top slot over hair and headgear; W mirrors E); S/N to author', 'viperStrike': 'E/W approved by user 2026-11-06 17:38 (v1; W mirrors E); S/N approved by user 2026-11-09 16:51 (v1)'}

CLIPS = {
 'viperStrike': ('Viper Strike', 3, [46, 26, 14, 10], 'light', 12, 'oneHandGuard', [
    og(),
    og(grip=(38, 38), angle=-5, far=(41, 25), bob=(3, 3, 3), lean=(1, 4), ln='low-rear', lf='low-lead'),
    og(grip=(37, 39), angle=-8, far=(41, 25), bob=(3, 3, 3), lean=(1, 5), ln='low-rear', lf='low-lead'),
    og(grip=(51, 30), angle=12, far=(40, 25), bob=(2, 2, 2), lean=(2, 6), root=(3, 0), ln='lunge-rear', lf='lunge-lead',
       trail={'mode': 'thrust', 'clipBody': True, 'lines': [[-3, -8, 4], [3, -6, 3]]}),
    og(grip=(44, 33), angle=5, far=(40, 25), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    og(grip=(51, 27), angle=18, far=(40, 25), bob=(2, 2, 2), lean=(2, 6), ln='lunge-rear', lf='lunge-lead',
       trail={'mode': 'thrust', 'clipBody': True, 'lines': [[-3, -8, 4], [3, -6, 3]]}),
    og(grip=(45, 33), angle=8, lean=(1, 3), root=(-2, 0), lf='step-lead'),
    og(root=(-1, 0))]),
 'ksStanceEntry': ('Kyoketsu-Shoge Stance', 4, None, 'none', 10, 'oneHandGuard', [
    og(grip=(41, 28), angle=-90, far=(39, 24), **{}),
    og(grip=(33, 39), angle=-100, far=(39, 24), lean=(0, 1)),
    og(grip=(35, 37), angle=-40, far=(40, 24), lean=(0, 2)),
    og(grip=(44, 25), angle=70, far=(40, 24), lean=(1, 3), trail='swing'),
    og(grip=(46, 30), angle=-10, far=(40, 24), lean=(1, 3), trail='swing'),
    og(grip=(44, 34), angle=40, far=(39, 24), lean=(0, 2)),
    og(angle=55)]),   # v3: ends on the sickle idle angle (oneHandGuard itemPoses kyoketsu-shoge-sickle)
 'macheteSlash': ('Machete Slash', 3, [44, 22, 16, 18], 'heavy', 12, 'oneHandGuard', [
    og(),
    og(grip=(38, 20), angle=120, far=(42, 27), lean=(-1, 0), ln='step-rear', z={'hilt': 'front', 'blade': 'top'}),   # v3 (Christopher 17:45): the raised blade over the hair and every headgear layer
    og(grip=(36, 17), angle=135, far=(43, 28), lean=(-1, -1), ln='step-rear', z={'hilt': 'front', 'blade': 'top'}),
    og(grip=(50, 30), angle=-35, far=(38, 28), bob=(2, 2, 2), lean=(2, 6), root=(3, 0), ln='lunge-rear', lf='lunge-lead', trail='swing'),
    og(grip=(45, 39), angle=-70, far=(38, 27), bob=(2, 2, 3), lean=(2, 6), ln='lunge-rear', lf='lunge-lead', trail='swing'),
    og(grip=(44, 36), angle=-20, lean=(1, 3), root=(-2, 0), lf='step-lead'),
    og(root=(-1, 0))]),
}
ITEM = {'viperStrike': 'tanto', 'ksStanceEntry': 'kyoketsu-shoge-sickle', 'macheteSlash': 'machete'}   # v3 (Christopher 2026-11-09 17:41): the base-tier sickle with chain and ring (the hooked blade is a higher-tier variant)
HIDE = {'ksStanceEntry': [0]}   # the blade is still stowed on the hip on the first frame
INTENT = {
 'viperStrike': 'Viper Strike (general Taijutsu, Bleed), free-standing (Christopher 2026-11-06: its own clip instead of the open-palm stand-in; the approved clinch and Mount versions are knife stabs, so the standing one is too): from the one-hand knife guard the fighter coils low, knees bent, the knife hand drawn back beside the hip; it darts up off the rear foot and the point bites into the midsection, snaps back an inch and bites again higher (two fangs), then recovers to the guard. White spark on the first bite.',
 'ksStanceEntry': 'Kyoketsu-Shoge Stance entry (Christopher 2026-11-06: its own clip instead of playing the tanto idle as the act): from the boxing guard the near hand drops to the hip and draws the Kyoketsu-Shoge blade, flicks it up and round in one turn (smear) and settles into the one-hand guard, the stance idle (oneHandGuard).',
 'macheteSlash': 'Machete Slash (Bandit, Bandit Thug; reskin of Kenjutsu Slash; Christopher 2026-11-06: its own clip instead of the katana cut): from the one-hand guard the bandit hauls the machete up over the shoulder, the blade drawn in front of the head (Christopher 2026-11-06 v2 layering), weight back, then steps in and chops it down diagonally through the target (heavy smear, white spark at the blade on contact), the blade carrying through low, then back to the guard.',
}
STATES = {k: k for k in CLIPS}
T.CLIPS.update(CLIPS); T.INTENT.update(INTENT); T.STATES = STATES
T.FX['viperStrike'] = {3: 11}; T.FX['macheteSlash'] = {3: 9}

# ---------------- the Guard NPC: yari and shield (Christopher 2026-11-06 decision: "Yari spear and shield") ----------------
# yari in the near (main) hand, a wooden tate on the far forearm (off slot, body layer). Every move starts and ends on
# spearGuard, the Guard's idle: spear level at the hip, point at the foe, shield up in front of the chest.
SG = dict(grip=(40, 34), angle=4, far=(43, 26), lean=(0, 2))
def sg(sh=90, **k): d = fr(**{**SG, **k}); d['w']['shield'] = sh; return d
CLIPS.update({
 'spearGuard': ('Spear Guard', None, None, None, 6, 'loop', [
    sg(), sg(grip=(40, 33), far=(43, 25)), sg(bob=(1, 1, 2), lean=(0, 3), grip=(41, 34)), sg(grip=(40, 35), far=(43, 26))]),
 'spearThrust': ('Spear Thrust', 3, [48, 26, 16, 8], 'heavy', 12, 'spearGuard', [
    sg(),
    sg(grip=(34, 33), angle=3, far=(44, 25), lean=(0, 1), ln='step-rear'),
    sg(grip=(33, 33), angle=3, far=(44, 25), lean=(-1, 0), ln='step-rear'),
    sg(grip=(48, 30), angle=4, far=(41, 26), bob=(2, 2, 2), lean=(2, 5), root=(3, 0), ln='lunge-rear', lf='lunge-lead',
       trail={'mode': 'thrust', 'clipBody': True, 'lines': [[-3, -8, 4], [3, -6, 3], [6, -9, -1]]}),
    sg(grip=(48, 30), angle=4, far=(41, 26), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    sg(grip=(43, 33), angle=4, lean=(1, 3), root=(-2, 0), lf='step-lead'),
    sg(root=(-1, 0))]),
 'yariCut': ('Blade Strike', 3, [44, 18, 20, 18], 'light', 12, 'spearGuard', [
    sg(),
    sg(grip=(40, 24), angle=55, far=(44, 28), lean=(-1, 0), ln='step-rear'),
    sg(grip=(39, 21), angle=70, far=(44, 29), lean=(-1, -1), ln='step-rear'),
    sg(grip=(46, 30), angle=-20, far=(42, 27), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), ln='lunge-rear', lf='lunge-lead', trail='swing'),
    sg(grip=(44, 34), angle=-35, far=(42, 27), bob=(2, 2, 2), lean=(2, 5), ln='lunge-rear', lf='lunge-lead'),
    sg(grip=(41, 34), angle=0, lean=(1, 3), root=(-1, 0)),
    sg(root=(-1, 0))]),
 'shieldBlock': ('Shield Block', 2, None, 'none', 12, 'spearGuard', [
    sg(),
    sg(grip=(37, 35), far=(46, 23), bob=(2, 2, 3), lean=(1, 3), ln='low-rear', lf='low-lead', sh=95),
    sg(grip=(36, 36), far=(46, 23), bob=(3, 3, 3), lean=(0, 2), root=(-2, 0), ln='low-rear', lf='low-lead', sh=95),
    sg(grip=(36, 36), far=(46, 23), bob=(3, 3, 3), lean=(1, 3), ln='low-rear', lf='low-lead', sh=95),
    sg(grip=(38, 35), far=(45, 24), bob=(2, 2, 2), lean=(1, 3), root=(1, 0)),
    sg(root=(1, 0))]),
 'shieldBash': ('Shield Bash', 3, [46, 16, 12, 22], 'light', 12, 'spearGuard', [
    sg(),
    sg(grip=(37, 34), far=(40, 26), lean=(-1, 0), ln='step-rear'),
    sg(grip=(36, 34), far=(39, 26), lean=(-1, -1), ln='step-rear'),
    sg(grip=(40, 33), far=(50, 25), bob=(2, 2, 2), lean=(3, 7), root=(3, 0), ln='lunge-rear', lf='lunge-lead'),
    sg(grip=(40, 33), far=(50, 25), bob=(2, 2, 2), lean=(3, 7), ln='lunge-rear', lf='lunge-lead'),
    sg(grip=(40, 34), far=(45, 26), lean=(1, 3), root=(-2, 0), lf='step-lead'),
    sg(root=(-1, 0))]),
})
SHIELD = ('spearGuard', 'spearThrust', 'yariCut', 'shieldBlock', 'shieldBash')
ITEM.update({k: 'yari' for k in SHIELD})
INTENT.update({
 'spearGuard': 'Spear Guard (the Guard NPC idle; Christopher 2026-11-06: the Guard carries a yari and a shield): the yari held one-handed in the near fist, level at the hip with the point at the foe, the wooden shield (tate) on the far forearm up in front of the chest, a slow breathing bob.',
 'spearThrust': 'Spear Thrust (the Guard; reskin of Precision Thrust): from the spear guard the yari is drawn back along the hip, then driven straight out in a lunge, the shield staying up (thrust lines), held, back to the guard.',
 'yariCut': 'Blade Strike (the Guard; reskin of Kenjutsu Slash; Christopher 2026-11-06 chose the yari, so the cut is made with its blade): the yari is raised up over the shoulder, then swept down diagonally so the leaf blade slices across the target (smear), back to the spear guard.',
 'shieldBlock': 'Shield Block (the Guard; reskin of Parry, Counter): the Guard drops into a braced crouch and thrusts the shield up and forward; it takes the blow on the shield (frame 2), slides back 2 px under it and recovers to the spear guard.',
 'shieldBash': 'Shield Bash (the Guard; reskin of Hilt Bash): the shield is pulled in to the chest, then the Guard lunges and punches the shield edge-first into the foe\'s face and chest (white burst), held, back to the spear guard.',
})
STATES.update({k: k for k in SHIELD})
T.CLIPS.update(CLIPS); T.INTENT.update(INTENT)
T.FX['spearThrust'] = {3: 24}; T.FX['yariCut'] = {3: 20}

SHIELDS = ('shield-tower', 'shield-heater', 'shield-buckler')   # Christopher 2026-11-06 17:47: standing requirement, every shield clip works with every type
# v3.1 (Christopher 2026-11-06 18:10: "the eyes are in front of the shield layer"): the shield is held out in front of the face,
# so the half above the grip draws on the top slot (over hair, headgear and eyes) and the half below it on the front slot
# (under the near arm and the hand on the yari). Split at the grip: u > 0 runs up the shield (angle 90 = upright).
SHIELD_Z = {'hilt': 'front', 'blade': 'top'}
def shield_slot(state):
    s = T.load(T.D + state + '.json'); fr_ = CLIPS[state][6]
    # v2 (Christopher 2026-11-06 17:47): a shield family (tower, heater, buckler; the first is the default), all on the same
    # grips; the shield sits 2 px in front of the far fist and is wide enough to cover it, so the hand no longer pokes through
    off = {'slot': 'off', 'layer': 'body', 'item': SHIELDS[0], 'items': list(SHIELDS), 'gripKind': 'normal', 'status': T.STAT,
           'rule': 'the shield on the far forearm: grip = 2 px in front of the far fist centre (covering the fist), angle 90 = upright (its axis top to bottom), seen three-quarter; every shield type uses these grips',
           'E': [{'grip': [f['far'][0] + 2, f['far'][1]], 'angle': f['w'].get('shield', 90), 'z': SHIELD_Z} for f in fr_], 'mirror': {'W': 'E'}}
    for p_ in s['weapons'][0]['E']: p_.pop('shield', None)
    # v3 (Christopher 2026-11-06 18:05: "the layering of the shield and spear is wrong"): the shield is on the far arm, the yari in
    # the near hand, so within a depth slot the off-slot shield is drawn first and the main weapon over it. The runtime draws a
    # state's weapon items in this list order, so the off slot comes first.
    off['drawOrder'] = 'within each depth slot: off (shield) under main (yari)'
    s['weapons'] = [off] + [w for w in s['weapons'] if w.get('slot') != 'off']
    T.save(s, T.D + state + '.json')

def spec(state):
    T.spec(state, state)
    s = T.load(T.D + state + '.json'); w = s['weapons'][0]; w['items'] = [ITEM[state]]
    if state in APPROVED: s['status'] = w['status'] = APPROVED[state]
    for k in HIDE.get(state, []): w['E'][k]['hidden'] = True
    s['extra'] = s.get('extra', {}); s['extra'].pop('stance', None)
    if state == 'ksStanceEntry':
        # v2: drawn, the chain hangs free from the pommel with the ring swinging; on the last two frames the far hand takes
        # the chain as in the stance idle (oneHandGuard itemPoses kyoketsu-shoge)
        for k, ch in ((1, {'to': [-2, 12]}), (2, {'to': [3, 12]}), (3, {'to': [-6, 10]}), (4, {'to': [5, 11]}),
                      (5, {'via': [45, 26], 'droop': 5, 'to': [2, 8], 'sag': 0, 'z': 'front'}), (6, {'via': [45, 26], 'droop': 5, 'to': [0, 8], 'sag': 0, 'z': 'front'})):
            w['E'][k]['chain'] = ch
        w['E'][0]['chain'] = {'off': True}
        s['clips']['rule'] = 'stance entry: starts in the boxing guard and ends in the stance idle (next: oneHandGuard)'
        for e in s['events']['E'] + s['events']['W']:
            if e.get('effect'): e['effect'] = 'enters Kyoketsu-Shoge Stance'
    T.save(s, T.D + state + '.json')
    if state in SHIELD: shield_slot(state)

def occlude(state):
    """v3.1: the shield's top half sits over the head layers, but the near arm and the yari are nearer the viewer than the
    shield, so the top-slot shield sheets are cut away wherever the arms layer or any yari sheet has a pixel (the near arm
    and the spear then read in front of it at runtime)."""
    from PIL import Image
    d = T.D + state + '/'; n = T.load(T.D + state + '.json')['frames']; rows = len(T.load(T.D + state + '.json')['directions'])
    arms = Image.open(d + 'arms.png').convert('RGBA')
    big = Image.new('RGBA', (128 * n, 128 * rows))
    for r in range(rows):
        for k in range(n): big.alpha_composite(arms.crop((k * 64, r * 64, k * 64 + 64, r * 64 + 64)), (k * 128 + 32, r * 128 + 32))
    masks = [big] + [Image.open(d + f).convert('RGBA') for f in os.listdir(d) if f.startswith('main-yari-')]
    for sh in SHIELDS:
        f = d + 'off-%s-top.png' % sh
        if not os.path.exists(f): continue
        im = Image.open(f).convert('RGBA'); px = im.load(); mp = [m.load() for m in masks]
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if px[x, y][3] and any(m[x, y][3] for m in mp): px[x, y] = (0, 0, 0, 0)
        im.save(f)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--occlude' in a: occlude(a[a.index('--occlude') + 1]); sys.exit()
    if '--grips' in a: T.grips(a[a.index('--grips') + 1])
    elif '--fx' in a: T.fx(a[a.index('--fx') + 1])
    else:
        for st in (a or CLIPS): spec(st)
