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
     python3 tools/standin_weapons.py --fx <state>"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tanto as T
from tanto import fr

T.STAT = 'CANDIDATE 2026-11-06 (E/W; W mirrors E; S/N to author after approval)'
OG = dict(grip=(43, 35), angle=10, far=(39, 24))   # the approved oneHandGuard frame
def og(**k): return fr(**{**OG, **k})
H = dict(hidden=True)

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
    og(grip=(44, 34), angle=8, far=(39, 24), lean=(0, 2)),
    og()]),
 'macheteSlash': ('Machete Slash', 3, [44, 22, 16, 18], 'heavy', 12, 'oneHandGuard', [
    og(),
    og(grip=(38, 20), angle=120, far=(42, 27), lean=(-1, 0), ln='step-rear', z='behind'),
    og(grip=(36, 17), angle=135, far=(43, 28), lean=(-1, -1), ln='step-rear', z='behind'),
    og(grip=(50, 30), angle=-35, far=(38, 28), bob=(2, 2, 2), lean=(2, 6), root=(3, 0), ln='lunge-rear', lf='lunge-lead', trail='swing'),
    og(grip=(45, 39), angle=-70, far=(38, 27), bob=(2, 2, 3), lean=(2, 6), ln='lunge-rear', lf='lunge-lead', trail='swing'),
    og(grip=(44, 36), angle=-20, lean=(1, 3), root=(-2, 0), lf='step-lead'),
    og(root=(-1, 0))]),
}
ITEM = {'viperStrike': 'tanto', 'ksStanceEntry': 'tanto', 'macheteSlash': 'machete'}
HIDE = {'ksStanceEntry': [0]}   # the blade is still stowed on the hip on the first frame
INTENT = {
 'viperStrike': 'Viper Strike (general Taijutsu, Bleed), free-standing (Christopher 2026-11-06: its own clip instead of the open-palm stand-in; the approved clinch and Mount versions are knife stabs, so the standing one is too): from the one-hand knife guard the fighter coils low, knees bent, the knife hand drawn back beside the hip; it darts up off the rear foot and the point bites into the midsection, snaps back an inch and bites again higher (two fangs), then recovers to the guard. White spark on the first bite.',
 'ksStanceEntry': 'Kyoketsu-Shoge Stance entry (Christopher 2026-11-06: its own clip instead of playing the tanto idle as the act): from the boxing guard the near hand drops to the hip and draws the Kyoketsu-Shoge blade, flicks it up and round in one turn (smear) and settles into the one-hand guard, the stance idle (oneHandGuard).',
 'macheteSlash': 'Machete Slash (Bandit, Bandit Thug; reskin of Kenjutsu Slash; Christopher 2026-11-06: its own clip instead of the katana cut): from the one-hand guard the bandit hauls the machete up over the shoulder, weight back, then steps in and chops it down diagonally through the target (heavy smear, white spark at the blade on contact), the blade carrying through low, then back to the guard.',
}
STATES = {k: k for k in CLIPS}
T.CLIPS.update(CLIPS); T.INTENT.update(INTENT); T.STATES = STATES
T.FX['viperStrike'] = {3: 11}; T.FX['macheteSlash'] = {3: 9}

def spec(state):
    T.spec(state, state)
    s = T.load(T.D + state + '.json'); w = s['weapons'][0]; w['items'] = [ITEM[state]]
    for k in HIDE.get(state, []): w['E'][k]['hidden'] = True
    s['extra'] = s.get('extra', {}); s['extra'].pop('stance', None)
    if state == 'ksStanceEntry':
        s['clips']['rule'] = 'stance entry: starts in the boxing guard and ends in the stance idle (next: oneHandGuard)'
        for e in s['events']['E'] + s['events']['W']:
            if e.get('effect'): e['effect'] = 'enters Kyoketsu-Shoge Stance'
    T.save(s, T.D + state + '.json')

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--grips' in a: T.grips(a[a.index('--grips') + 1])
    elif '--fx' in a: T.fx(a[a.index('--fx') + 1])
    else:
        for st in (a or CLIPS): spec(st)
