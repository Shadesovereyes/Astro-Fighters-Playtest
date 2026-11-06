"""Own clips for the abilities that still borrowed a nearby clip (Christopher 2026-11-06: "lets fix the 16 that are
borrowing a nearby one"). Played from the approved boxing guard and returning to it, through astro.py's spec builder
(universal.py underneath). One state per ability. E/W first (W mirrors E), S/N after approval. Effects white/neutral
(plain martial technique, no element). Targets hold their guard until the impact frame (ANIMATION_RULES 2026-11-04).

Not authored here, because the move can never be used free-standing, so its stand-in never plays:
  Headbutt (noFree: clinch or Mount bottom only; clinchHeadbutt / mountBottomHeadbutt are approved)
  Dirty Boxing (req STANDING grapple = the tie; clinchDirtyBoxing is approved)

Run: python3 tools/standins.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/standins.py --fx <state>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import astro
from universal import band, g, LOW

STAT = 'CANDIDATE 2026-11-06 (E/W; W mirrors E; S/N to author after approval)'
A = 'E/W approved by user 2026-11-06 %s (v1; W mirrors E); S/N to author'
APPROVED = {'boxUppercut': A % '17:35', 'boxHaymaker': A % '17:35', 'boxBodyShot': A % '17:35', 'wildSwing': A % '17:35', 'clinchEntry': A % '17:36'}

DRIVE = dict(ln='sp-drive-rear', lf='sp-drive-lead')
LOAD = dict(ln='sp-load-rear', lf='sp-load-lead')
GUARD_N = band(-20, 212)   # the approved guard's rear (near) arm
RECOVER = band(-55, 230)

def tgt(ab, act, state='hitReact'):
    return {'targetState': {'rule': '%s: on the impact frame (%d, the active frame) and not before, the target plays %s once, then its idle; before it the target holds its plain guard' % (ab, act, state), 'state': state}}

CLIPS = {
 'boxUppercut': ('Uppercut', 3,
  'Uppercut (Boxing, free-standing; inside the clinch it plays clinchUppercut): from the guard the fighter dips at the knees and drops the rear fist to the hip, palm turned up; it drives up off the rear foot and the fist rises close to the body straight up under the chin, elbow tucked, the lead hand guarding the face; it holds a beat on contact (a white snap at the fist) and settles back into the guard.',
  [g(),
   g(an=band(8, -70), af=band(-60, -130), bob=(3, 3, 3), lean=(1, 3), **LOW),
   g(an=band(-35, -140), af=band(-58, -128), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **DRIVE),
   g(an=band(-72, -165), af=band(-55, -125), bob=(0, 0, 1), lean=(2, 3), root=(1, 0), **DRIVE),
   g(an=band(-72, -165), af=band(-55, -125), bob=(0, 0, 1), lean=(2, 3), **DRIVE),
   g(an=RECOVER, bob=(1, 1, 2), lean=(1, 3), root=(-1, 0)),
   g(root=(-1, 0))],
  [None, 'squint', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 14, 12, 10], damage='heavy', rm='E: +1 +1 driving up into it, -1 -1 settling back (net 0)',
       extra=tgt('Uppercut', 3),
       anchored={3: [('star6', 'hand', 1, -2)], 4: [('star3', 'hand', 2, -3)]})),

 'boxHaymaker': ('Haymaker', 4,
  'Haymaker (Boxing, Guard Break): a big telegraphed loaded punch. From the guard the fighter sits back on the rear leg and swings the rear fist far back and up behind the head, the lead hand reaching out to measure; it holds the load a beat, then hurls the fist round in a wide looping arc over the top, the whole body turning through behind it, rear heel up; it lands at the jaw with a big white burst, the arm carries on through and down across the body, and the fighter pulls back into the guard.',
  [g(),
   g(an=band(55, -160), af=band(-80, -100), bob=(1, 1, 1), lean=(-1, -2), **LOAD),
   g(an=band(72, -178), af=band(-82, -98), bob=(1, 1, 1), lean=(-1, -3), **LOAD),
   g(an=band(-125, -115), af=band(-30, 215), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), **DRIVE),
   g(an=band(-95, -112), af=band(20, -150), bob=(2, 2, 2), lean=(2, 7), root=(1, 0), **DRIVE),
   g(an=band(-45, -40), af=band(20, -150), bob=(3, 3, 3), lean=(2, 7), **DRIVE),
   g(an=RECOVER, bob=(1, 1, 2), lean=(1, 3), root=(-2, 0)),
   g(root=(-1, 0))],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 15, 14, 10], damage='heavy', rm='E: +2 +1 swinging through, -2 -1 back to the guard (net 0)',
       extra=tgt('Haymaker', 4),
       anchored={4: [('star9', 'hand', 1, -1)]})),

 'boxBodyShot': ('Body Shot', 3,
  'Body Shot (Boxing, drains stamina; inside the clinch it plays clinchBodyShot): a level change and a lead hook to the liver. From the guard the fighter drops its level, knees bending and head ducked behind the rear glove; it steps in at that height and whips the lead fist round in a short hook into the opponent\'s side under the ribs (a white thud at the fist), holds the dig a beat and comes back up into the guard. A lead-hand dig, unlike Kidney Shot\'s feint and rear hook.',
  [g(),
   g(af=band(-20, -95), an=band(-35, -160), bob=(4, 4, 4), lean=(2, 6), **LOW),
   g(af=band(-30, -40), an=band(-35, -160), bob=(4, 4, 4), lean=(2, 7), root=(2, 0), **DRIVE),
   g(af=band(-88, -62), an=band(-35, -160), bob=(5, 5, 5), lean=(2, 9), root=(1, 0), **DRIVE),
   g(af=band(-88, -62), an=band(-35, -160), bob=(5, 5, 5), lean=(2, 9), **DRIVE),
   g(af=band(-40, -110), bob=(2, 2, 3), lean=(1, 4), root=(-2, 0)),
   g(root=(-1, 0))],
  [None, 'squint', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 30, 12, 8], damage='light', rm='E: +2 +1 stepping in low, -2 -1 back up (net 0)',
       extra=tgt('Body Shot', 3),
       anchored={3: [('star6', 'farhand', 1, 0)], 4: [('star3', 'farhand', 2, 1)]})),

 'cheapShot': ('Cheap Shot', 5,
  'Cheap Shot (Bandit, reskin of Haymaker) v2 (Christopher 2026-11-06: a low blow that lands below the belt): the fighter lets its guard drop as if easing off, hands low and loose, head turned half away; then it ducks in sharply, knees bending, and drives the rear fist low and straight into the groin below the belt (white burst at belt height), holds the dig a beat with a nasty grin, and pulls back into the guard.',
  [g(),
   g(an=band(10, -25), af=band(0, -40), bob=(0, 0, 1), lean=(-1, -1)),
   g(an=band(12, -20), af=band(2, -35), bob=(0, 0, 1), lean=(-1, -1)),
   g(an=band(15, -60), af=band(-40, -120), bob=(3, 3, 3), lean=(1, 4), **LOW),
   g(an=band(-25, -55), af=band(-45, -130), bob=(5, 5, 5), lean=(2, 8), root=(2, 0), **DRIVE),
   g(an=band(-40, -30), af=band(-45, -130), bob=(6, 6, 6), lean=(2, 9), root=(1, 0), **DRIVE),
   g(an=band(-40, -30), af=band(-45, -130), bob=(6, 6, 6), lean=(2, 9), **DRIVE),
   g(an=RECOVER, bob=(2, 2, 3), lean=(1, 3), root=(-2, 0)),
   g(root=(-1, 0))],
  [None, None, None, 'squint', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 40, 12, 8], damage='heavy', rm='E: +2 +1 ducking in, -2 -1 back (net 0)',
       extra=tgt('Cheap Shot', 5),
       anchored={5: [('star9', 'hand', 1, 0)], 6: [('star3', 'hand', 2, -2)]})),

 'wildSwing': ('Wild Swing', 3,
  'Wild Swing (Street Thug, reskin of Haymaker): a sloppy brawler\'s haymaker. The fighter rears way back, the rear fist cocked far behind it and the guard thrown open; it lurches forward and flings the arm round in a huge flat arc, landing at the head (white burst), and overswings: the arm carries on across the body, the weight pitches forward and it stumbles a step before hauling itself back into the guard.',
  [g(),
   g(an=band(80, -120), af=band(-40, -60), bob=(0, 0, 1), lean=(-2, -4), **LOAD),
   g(an=band(-130, -150), af=band(-20, -40), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), **DRIVE),
   g(an=band(-95, -105), af=band(10, -30), bob=(2, 2, 2), lean=(3, 8), root=(2, 0), **DRIVE),
   g(an=band(-30, -15), af=band(15, -20), bob=(4, 4, 4), lean=(3, 10), root=(2, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
   g(an=band(-10, -30), af=band(0, -40), bob=(3, 3, 3), lean=(2, 7), ln='ml-trail-rear', lf='ml-plant-lead'),
   g(an=RECOVER, bob=(1, 1, 2), lean=(1, 3), root=(-3, 0)),
   g(root=(-3, 0))],
  [None, 'squint', 'strain', 'strain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 15, 14, 10], damage='heavy', rm='E: +2 +2 lurching in, +2 the stumble, -3 -3 back (net 0)',
       extra=tgt('Wild Swing', 3),
       anchored={3: [('star9', 'hand', 1, 0)], 4: [('dust', 'feet', 6, -2)], 5: [('dust', 'feet', 2, -2)]})),

 'knuckleHaymaker': ('Knuckle Haymaker', 5,
  'Knuckle Haymaker (Bandit Thug, reskin of Haymaker) v2 (Christopher 2026-11-06: it read too like Wild Swing): a controlled, brutal brass-knuckle punch, the opposite of the sloppy Wild Swing. The rear fist wears an iron knuckle-duster the whole clip (grey band over the knuckles, glinting); the thug first smacks the iron into its own open lead palm twice as a threat, then plants, keeps its balance and throws one short, tight hook to the jaw with no wind-up loop and no overswing; on contact the iron rings with grey metal sparks and a white burst; it snaps straight back into the guard.',
  [g(),
   g(an=band(-55, -120), af=band(-70, -100, fistKind='palm'), bob=(1, 1, 2), lean=(0, 2)),
   g(an=band(-65, -110), af=band(-70, -100, fistKind='palm'), bob=(1, 1, 2), lean=(0, 2)),
   g(an=band(-55, -120), af=band(-70, -100, fistKind='palm'), bob=(1, 1, 2), lean=(0, 2)),
   g(an=band(-10, -150), af=band(-45, -125), bob=(2, 2, 2), lean=(1, 3), **LOAD),
   g(an=band(-92, -108), af=band(-45, -125), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), **DRIVE),
   g(an=band(-92, -108), af=band(-45, -125), bob=(2, 2, 2), lean=(2, 5), **DRIVE),
   g(an=RECOVER, bob=(1, 1, 2), lean=(1, 3), root=(-2, 0)),
   g()],
  [None, 'squint', None, 'squint', 'squint', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 16, 14, 10], damage='heavy', rm='E: +2 the planted hook, -2 back (net 0)',
       extra=tgt('Knuckle Haymaker', 5),
       anchored={k: [('knux', 'hand', -1, 0)] + v for k, v in {0: [], 1: [], 2: [('knuxGlint', 'hand', 0, -3)], 3: [], 4: [('knuxGlint', 'hand', 0, -3)],
                 5: [('star9', 'hand', 2, 0), ('mShards', 'hand', 3, -1)], 6: [('mShards', 'hand', 5, 2)], 7: [], 8: []}.items()})),

 'shoulderCharge': ('Shoulder Charge', 4,
  'Shoulder Charge (Bandit Thug, reskin of Iron Mountain, needs a run-up) v2 (Christopher 2026-11-06: dip lower): the fighter drops low, knees deep, dips its head and lowers the lead shoulder, arms tucked in; it drives forward two hard strides and rams the shoulder into the opponent\'s chest (white burst, dust off the feet), holds the drive a beat and steps back into the guard.',
  [g(),
   g(an=band(15, -60), af=band(-5, -75), bob=(6, 6, 6), lean=(3, 10), ln='ml-dip-rear', lf='ml-dip-lead'),
   g(an=band(15, -60), af=band(-5, -75), bob=(5, 5, 5), lean=(3, 12), root=(3, 0), ln='sr-push-off', lf='sr-knee-drive'),
   g(an=band(15, -60), af=band(-5, -75), bob=(5, 5, 5), lean=(3, 12), root=(3, 0), ln='sr-knee-drive', lf='sr-push-off'),
   g(an=band(10, -55), af=band(-10, -70), bob=(6, 6, 6), lean=(3, 12), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
   g(an=band(10, -55), af=band(-10, -70), bob=(6, 6, 6), lean=(3, 12), ln='ml-trail-rear', lf='ml-plant-lead'),
   g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3), root=(-5, 0)),
   g(root=(-4, 0))],
  [None, 'squint', 'strain', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 28, 12, 14], damage='heavy', rm='E: +3 +3 the strides, +3 the ram, -5 -4 back to the guard (net 0)',
       extra=tgt('Shoulder Charge', 4),
       anchored={2: [('dust', 'feet', -8, -2)], 3: [('dust', 'feet', -8, -2)], 4: [('star9', 'head', 8, 8), ('dust', 'feet', 4, -2)], 5: [('star3', 'head', 9, 6)]})),

 'clinchEntry': ('Clinch', 3,
  'Clinch entry (Martial shared; Grab is the NPC reskin): from the guard the fighter steps in and shoots both open hands out at the opponent\'s neck; on the impact frame the hands close behind the head in a collar tie and pull down. When the grab lands the testbed forms the clinch pair from that frame (clinchHold / clinchHeld); when it misses the fighter lets go and steps back into the guard.',
  [g(),
   g(an=band(-60, -95, fistKind='palm'), af=band(-70, -105, fistKind='palm'), bob=(1, 1, 2), lean=(2, 5), root=(2, 0), **DRIVE),
   g(an=band(-88, -110, fistKind='palm'), af=band(-92, -118, fistKind='palm'), bob=(1, 1, 2), lean=(2, 6), root=(2, 0), **DRIVE),
   g(an=band(-88, -150), af=band(-92, -155), bob=(2, 2, 2), lean=(2, 7), root=(1, 0), **DRIVE),
   g(an=band(-75, -140), af=band(-80, -145), bob=(2, 2, 3), lean=(2, 6), **DRIVE),
   g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3), root=(-3, 0)),
   g(root=(-2, 0))],
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 14, 14, 16], damage='light', rm='E: +2 +2 +1 stepping in, -3 -2 back on a miss (net 0)',
       extra={'targetState': {'rule': 'Clinch: on the impact frame (3) and not before, a landed grab forms the clinch pair (holder clinchHold, held clinchHeld); a missed or resisted grab plays the rest of this clip back to the guard and the target keeps its guard', 'state': 'clinchHeld', 'onHit': {'self': 'clinchHold', 'target': 'clinchHeld'}}})),
}

# ---------------- Medical (Christopher 2026-11-06: "then move on to the medical") ----------------
# Healing chakra is drawn in soft medical green (proposal: no colour ruling yet), from the palette already in use
# (#b8ffc8 / #39e75f / #14a03c); Dark Communion, the cultist reskin of Palm Healing, in the Sagittarius dark purples.
from universal import SEAL_N, SEAL_F
def _re(pat, m): return [''.join(m.get(ch, ch) for ch in r) for r in pat]
GREEN = {'c': 'l', 'C': 'L', 'Y': 'l', 'O': 'L', 'R': 'D', 'W': 'l', 'w': 'L'}
DARK = {'c': 'Q', 'C': 'P', 'Y': 'Q', 'O': 'P', 'R': 'p', 'W': 'Q', 'w': 'P'}
for nm in ('palmGlow', 'vRing', 'vRing2', 'moteF', 'spark', 'star6', 'orb', 'orbBig'):
    astro.NPAT[nm + 'Med'] = _re(astro.NPAT[nm], GREEN); astro.NPAT[nm + 'Dark'] = _re(astro.NPAT[nm], DARK)
MED_AURA, DARK_AURA = ('#b8ffc8', '#39e75f'), ('#c9a0ff', '#55208f')
PALM_ON = band(-88, -92, fistKind='palm')   # open palm laid flat on the ally's chest, arm level
PALM_TGT = band(-60, -40)                    # healed fighter: guard eased, near hand drifting to the warm spot

def _heal(ab, k, tgt, aura):
    m = 'Med' if k == 'Med' else 'Dark'
    return (ab, 4,
  ('%s (Medical, single ally in reach): the fighter brings both open hands together in a seal, eyes closing, and %s chakra kindles between the palms; it steps in and lays the near palm flat on the ally\'s chest, the glow pooling there and pulsing as the chakra flows in (the heal lands on frame 4, the first pulse), a thin %s aura round the caster while it channels; it lifts the palm away and steps back into the guard (the ally plays %s).') % (ab, 'green medical' if k == 'Med' else 'dark violet', 'green' if k == 'Med' else 'violet', tgt),
  [g(),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=band(-70, -80, fistKind='palm'), af=band(-45, -120), bob=(1, 1, 2), lean=(1, 3), root=(2, 0), **DRIVE),
   g(an=PALM_ON, af=band(-45, -120), bob=(1, 1, 2), lean=(1, 4), root=(1, 0), **DRIVE),
   g(an=PALM_ON, af=band(-45, -120), bob=(1, 1, 2), lean=(1, 4), **DRIVE),
   g(an=PALM_ON, af=band(-45, -120), bob=(1, 1, 2), lean=(1, 4), **DRIVE),
   g(an=PALM_ON, af=band(-45, -120), bob=(1, 1, 2), lean=(1, 4), **DRIVE),
   g(an=band(-40, -110), bob=(1, 1, 2), lean=(1, 3), root=(-2, 0)),
   g(root=(-1, 0))],
  [None, 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None],
  [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
  dict(fps=10, react=True, auraColors=aura, rm='E: +2 +1 stepping in to lay the palm on, -2 -1 back (net 0)',
       extra={'targetState': {'rule': '%s: on frame 4 (the palm lands and the first pulse flows in) and not before, the ally plays %s once, then its idle' % (ab, tgt), 'state': tgt}},
       anchored={1: [('orb' + m, 'hand', 0, -2)], 2: [('orbBig' + m, 'hand', 0, -2), ('spark' + m, 'hand', 3, -6)],
                 3: [('palmGlow' + m, 'hand', 1, 0)], 4: [('palmGlow' + m, 'hand', 2, 0), ('star6' + m, 'hand', 3, 0)],
                 5: [('palmGlow' + m, 'hand', 2, 0), ('vRing' + m, 'hand', 3, 0)], 6: [('palmGlow' + m, 'hand', 2, 0), ('vRing2' + m, 'hand', 3, 0)],
                 7: [('palmGlow' + m, 'hand', 2, 0), ('moteF' + m, 'hand', 0, -6)], 8: [('moteF' + m, 'hand', 0, -6)]}))

def _healed(ab, k, src):
    m = 'Med' if k == 'Med' else 'Dark'
    return (ab, 0,
  '%s (target of %s): frame 0 is the palm landing on its chest; the %s glow spreads from the spot, motes drift up off it, the guard eases and the shoulders drop as the hurt goes out of it, a thin aura round the body for three pulses, then it settles back into the guard.' % (ab, src, 'green' if k == 'Med' else 'violet'),
  [g(bob=(1, 1, 2), lean=(0, 1)),
   g(an=PALM_TGT, bob=(0, 0, 1), lean=(-1, 0)),
   g(an=PALM_TGT, bob=(0, 0, 1), lean=(-1, -1)),
   g(an=PALM_TGT, bob=(0, 0, 1), lean=(-1, -1)),
   g(an=band(-40, -110), bob=(1, 1, 2), lean=(0, 1)),
   g()],
  ['closed', 'closed', 'closed', None, None, None],
  [1, 1, 1, 1, 0, 0],
  dict(fps=8, react=True, auraColors=MED_AURA if k == 'Med' else DARK_AURA, rm='in place',
       anchored={0: [('vRing' + m, 'head', 0, 12)], 1: [('vRing2' + m, 'head', 0, 12), ('moteF' + m, 'head', 2, 4)],
                 2: [('moteF' + m, 'head', -2, 0), ('moteF' + m, 'head', 4, 6)], 3: [('moteF' + m, 'head', 1, -4)]}))

# Palm Healing v2 (Christopher 2026-11-06 17:39: "give palm healing more fx like small green pulsing Health crosses"):
# small green health crosses that swell and shrink as they drift up off the palm and, on the ally, off the chest
astro.NPAT['healX1'] = ['.L.', 'LlL', '.L.']
astro.NPAT['healX2'] = ['.DLD.', 'DLlLD', 'LlllL', 'DLlLD', '.DLD.']
astro.NPAT['healX3'] = ['..DDD..', '..DlD..', 'DDDlDDD', 'DllllLD', 'DDDlDDD', '..DlD..', '..DDD..']
HEAL_X = {4: [('healX2', 'hand', 2, -7), ('healX1', 'hand', -3, -3)],
          5: [('healX3', 'hand', 3, -10), ('healX2', 'hand', -4, -7), ('healX1', 'hand', 6, -3)],
          6: [('healX2', 'hand', 4, -14), ('healX3', 'hand', -4, -11), ('healX2', 'hand', 7, -7)],
          7: [('healX1', 'hand', 4, -18), ('healX2', 'hand', -5, -15), ('healX3', 'hand', 7, -11)],
          8: [('healX1', 'hand', -5, -19), ('healX1', 'hand', 7, -15)]}
HEALED_X = {0: [('healX1', 'head', 4, 10)],
            1: [('healX2', 'head', 5, 6), ('healX1', 'head', -5, 12)],
            2: [('healX3', 'head', 6, 2), ('healX2', 'head', -6, 8), ('healX1', 'head', 1, 14)],
            3: [('healX2', 'head', 6, -3), ('healX3', 'head', -6, 3), ('healX2', 'head', 1, 9)],
            4: [('healX1', 'head', 6, -7), ('healX2', 'head', -6, -2), ('healX3', 'head', 1, 4)],
            5: [('healX1', 'head', -6, -6), ('healX1', 'head', 1, -1)]}
def _addx(clip, xs):
    an = clip[-1]['anchored']
    for k, v in xs.items(): an[k] = an.get(k, []) + v
    return clip

CLIPS.update({
 'palmHealing': _addx(_heal('Palm Healing', 'Med', 'palmHealed', MED_AURA), HEAL_X),
 'palmHealed': _addx(_healed('Palm Healed', 'Med', 'Palm Healing'), HEALED_X),
 'darkCommunion': _heal('Dark Communion', 'Dark', 'darkCommuned', DARK_AURA),
 'darkCommuned': _healed('Dark Communed', 'Dark', 'Dark Communion'),
})

# Cellular Recovery (renamed from Cellular Activation, Christopher 2026-11-06 17:39, canon amendment) v2: the same pulsing
# green health crosses as Palm Healing, swelling round the orb as it gathers and rising off the ally as the cells knit
CELL_X = {2: [('healX1', 'hand', 5, -6)], 3: [('healX2', 'hand', -5, -7), ('healX1', 'hand', 6, -9)],
          4: [('healX3', 'hand', 4, -9), ('healX2', 'hand', -5, -10)], 5: [('healX1', 'hand', 2, -13), ('healX2', 'hand', -4, -14)]}
CELLED_X = {0: [('healX2', 'head', 6, 12)],
            1: [('healX3', 'head', 6, 8), ('healX1', 'head', -6, 16)],
            2: [('healX2', 'head', 7, 3), ('healX2', 'head', -6, 11), ('healX1', 'head', 2, 20)],
            3: [('healX1', 'head', 7, -2), ('healX3', 'head', -6, 6), ('healX2', 'head', 2, 15)],
            4: [('healX2', 'head', -6, 1), ('healX3', 'head', 2, 9)],
            5: [('healX1', 'head', -6, -4), ('healX1', 'head', 2, 3)]}

CLIPS.update({
 'cellularRecovery': ('Cellular Recovery', 5,
  'Cellular Recovery (renamed from Cellular Activation 2026-11-06; v2 adds pulsing green health crosses) (Medical, single ally up to 6 tiles, Regen 3 rounds): the fighter presses its open hands together in a seal, eyes closing, and a green medical orb swells between them; it opens the near palm toward the ally and sends the orb flying (projectile orbBigMed, frames 5-6, the testbed flies it to the ally and pops vRingMed there); the ally plays cellRecovered. A thin green aura round the caster while it gathers.',
  [g(),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=band(-30, -110, fistKind='palm'), af=band(-45, -120), bob=(1, 1, 2), lean=(0, 2)),
   g(an=band(-90, -95, fistKind='palm'), af=band(-45, -120), bob=(1, 1, 2), lean=(1, 4), root=(1, 0), **DRIVE),
   g(an=band(-90, -95, fistKind='palm'), af=band(-45, -120), bob=(1, 1, 2), lean=(1, 4), **DRIVE),
   g(an=band(-40, -110), bob=(1, 1, 2), lean=(1, 3), root=(-1, 0)),
   g()],
  [None, 'closed', 'closed', 'closed', None, None, None, None, None],
  [0, 1, 1, 1, 1, 0, 0, 0, 0],
  dict(fps=10, release=[50, 24], auraColors=MED_AURA, rm='E: +1 sending it, -1 back (net 0)',
       extra={'projectile': {'rule': 'Cellular Recovery: from frame 5 the testbed flies NPAT orbBigMed from the near hand to the ally at chest height, then draws vRingMed on it; the ally plays cellRecovered on arrival (the impact frame), not before', 'from': 'hand', 'frame': 5, 'pattern': 'orbBigMed', 'hit': 'vRingMed'},
              'targetState': {'rule': 'Cellular Recovery: when the orb reaches the ally and not before, the ally plays cellRecovered once, then its idle', 'state': 'cellRecovered'}},
       anchored={1: [('orbMed', 'hand', 0, -2)], 2: [('orbBigMed', 'hand', 0, -2)], 3: [('orbBigMed', 'hand', 0, -2), ('sparkMed', 'hand', 3, -7)],
                 4: [('orbBigMed', 'hand', 2, 0)], 5: [('star6Med', 'hand', 3, 0)]})),
 'cellRecovered': ('Cell Recovered', 0,
  'Cell Recovered (target of Cellular Recovery): frame 0 is the orb arriving: it bursts into a green ring round the chest; a pulse ring opens on the floor under the feet and green motes spiral up the body as the cells knit, a thin green aura round the fighter, the guard easing a little; it settles back into the guard (the Regen status keeps a faint aura while it lasts: proposal).',
  [g(bob=(1, 1, 2), lean=(0, 1)),
   g(bob=(0, 0, 1), lean=(-1, 0)),
   g(bob=(0, 0, 1), lean=(-1, 0)),
   g(bob=(0, 0, 1), lean=(-1, 0)),
   g(bob=(1, 1, 2), lean=(0, 1)),
   g()],
  [None, 'closed', 'closed', None, None, None],
  [1, 1, 1, 1, 0, 0],
  dict(fps=8, react=True, auraColors=MED_AURA, rm='in place',
       anchored={0: [('vRing2Med', 'head', 0, 14)], 1: [('vRingMed', 'feet', 0, -2), ('moteFMed', 'head', -5, 20)],
                 2: [('vRing2Med', 'feet', 0, -2), ('moteFMed', 'head', 5, 12), ('moteFMed', 'head', -4, 22)],
                 3: [('moteFMed', 'head', -4, 4), ('moteFMed', 'head', 4, 14)], 4: [('moteFMed', 'head', 2, -2)]})),
})

_addx(CLIPS['cellularRecovery'], CELL_X); _addx(CLIPS['cellRecovered'], CELLED_X)

# Knuckle Haymaker v2: the iron knuckle-duster on the rear fist, a glint off it and grey metal sparks on the hit
astro.NPAT['knux'] = ['.###.', '#FWF#', '#FFF#', '.###.']
astro.NPAT['knuxGlint'] = ['.W.', 'WWW', '.W.']
astro.NPAT['mShards'] = ['F...F', '.W.W.', '..W..', '.W.F.', 'F...W']
astro.CLIPS.update(CLIPS)
astro.APPROVED.update({k: APPROVED.get(k, STAT) for k in CLIPS})

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--scene':   # astro_scene.py with this file's patterns registered
        import runpy; sys.argv = ['astro_scene.py'] + a[1:]; runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'astro_scene.py'), run_name='__main__'); sys.exit()
    if '--fx' in a: astro.fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): astro.spec(st)
