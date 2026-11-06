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
APPROVED = {'darkCommunion': 'E/W approved by user 2026-11-06 18:04 (v2 violet eyes, shadow pools, black flames, tendrils on the ally; W mirrors E); S/N to author', 'darkCommuned': 'E/W approved by user 2026-11-06 18:04 (v2; W mirrors E); S/N to author', 'cellularRecovery': 'E/W approved by user 2026-11-06 17:48 (v2 health crosses; W mirrors E); S/N to author; also needs a self-cast clip', 'cellRecovered': 'E/W approved by user 2026-11-06 17:48 (v2; W mirrors E); S/N to author', 'palmHealing': 'E/W approved by user 2026-11-06 17:48 (v2 health crosses; W mirrors E); S/N to author; also needs a self-cast clip', 'palmHealed': 'E/W approved by user 2026-11-06 17:48 (v2; W mirrors E); S/N to author', 'boxUppercut': A % '17:35', 'boxHaymaker': A % '17:35', 'boxBodyShot': A % '17:35', 'wildSwing': A % '17:35', 'clinchEntry': A % '17:36'}

DRIVE = dict(ln='sp-drive-rear', lf='sp-drive-lead')
from universal import leg as _leg
import universal as _U
_U.POSES += [_leg('tp-lead', (34, 49), (41, 52), 39), _leg('tp-rear', (31, 49), (28, 54), 23, wrap=54, kind='toe60')]   # Shoulder Charge v3: lineman's three-point set, knees deep
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

 'cheapShot': ('Cheap Shot', 4,
  'Cheap Shot (Bandit, reskin of Haymaker) v4 (Christopher 2026-11-06 17:50: complete rework, drop low and punch up into the groin): the fighter drops suddenly low, knees deep, under the opponent\'s guard, the lead hand staying up at the face and the rear fist sunk down by the knee; it springs up off the crouch and drives the rear fist in a short rising punch up into the groin (white burst below the belt), holds it a beat, then rises back into the guard.',
  [g(),
   g(an=band(-10, -60), bob=(5, 5, 5), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
   g(an=band(12, -20), bob=(13, 13, 13), lean=(3, 10), root=(3, 0), ln='tp-rear', lf='tp-lead'),
   g(an=band(5, -55), bob=(13, 13, 13), lean=(3, 10), root=(2, 0), ln='tp-rear', lf='tp-lead'),
   g(an=band(-14, -96), bob=(13, 13, 13), lean=(3, 9), root=(1, 0), ln='tp-rear', lf='tp-lead'),
   g(an=band(-16, -102), bob=(13, 13, 13), lean=(3, 9), ln='tp-rear', lf='tp-lead'),
   g(an=RECOVER, bob=(4, 4, 4), lean=(1, 3), root=(-3, 0), ln='ml-dip-rear', lf='ml-dip-lead'),
   g(root=(-3, 0))],
  [None, 'squint', 'strain', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 40, 12, 8], damage='heavy', rm='E: +3 +2 +1 dropping in under the guard, -3 -3 back (net 0)',
       extra=tgt('Cheap Shot', 4, 'groinHit'),
       anchored={4: [('star9', 'hand', 1, -1)], 5: [('star3', 'hand', 2, -2)]})),

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

 'knuckleHaymaker': ('Knuckle Haymaker', 7,
  'Knuckle Haymaker (Bandit Thug, reskin of Haymaker) v3 (Christopher 2026-11-06: not a fan of the v2 duster look, and the animation did not match the description): a controlled, brutal brass-knuckle hook, the opposite of the sloppy Wild Swing. The rear fist wears a thin knuckle-duster, a 1 px steel band across the knuckles with a white glint, outlined. The thug raises its open lead palm in front of the chest and slams the iron fist into it twice as a threat, the fist pulled well back between smacks, a small grey spark each time; then it plants and throws one short, tight hook to the jaw: the elbow comes up level with the shoulder and the fist arrives from the side with no wind-up loop and no overswing; on contact the iron rings with grey metal sparks and a white burst; it snaps straight back into the guard.',
  [g(),
   g(af=band(-70, -160, fistKind='palm'), bob=(1, 1, 2), lean=(-1, -1)),
   g(an=band(-45, -125), af=band(-70, -160, fistKind='palm'), bob=(1, 1, 2), lean=(1, 2)),
   g(af=band(-70, -160, fistKind='palm'), bob=(1, 1, 2), lean=(-1, -1)),
   g(an=band(-45, -125), af=band(-70, -160, fistKind='palm'), bob=(1, 1, 2), lean=(1, 2)),
   g(an=band(-70, -185), bob=(2, 2, 2), lean=(0, 1), **LOAD),
   g(an=band(-110, -150), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **DRIVE),
   g(an=band(-110, -80), bob=(2, 2, 2), lean=(2, 6), root=(1, 0), **DRIVE),
   g(an=band(-110, -80), bob=(2, 2, 2), lean=(2, 6), **DRIVE),
   g(an=RECOVER, bob=(1, 1, 2), lean=(1, 3), root=(-2, 0)),
   g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 14, 14, 10], damage='heavy', rm='E: +1 +1 the planted hook, -2 back (net 0)',
       extra=tgt('Knuckle Haymaker', 7),
       anchored={k: [('knux', 'hand', -1, 0)] + v for k, v in {0: [], 1: [], 2: [('mSpark', 'hand', 1, 0)], 3: [], 4: [('mSpark', 'hand', 1, 0)], 5: [], 6: [('knuxGlint', 'hand', 0, -2)],
                 7: [('star9', 'hand', 2, 0), ('mShards', 'hand', 3, -1)], 8: [('mShards', 'hand', 5, 2)], 9: [], 10: []}.items()})),

 'shoulderCharge': ('Shoulder Charge', 7,
  'Shoulder Charge (Bandit Thug, reskin of Iron Mountain, needs a run-up) v3 (Christopher 2026-11-06: drop into a three-point stance, then rush the target like a football player): from the guard the fighter drops into a lineman\'s three-point stance, knees deep, back flat, the near fist planted on the floor in front of the lead foot and the far arm cocked back along the hip; it holds the set a beat, grit spitting off the planted fist, then explodes off the line: three short driving strides with the head and lead shoulder low, arms pumping, dust off every step; it drives the shoulder into the opponent\'s chest like a tackle (white burst, dust), holds the drive a beat and steps back into the guard.',
  [g(),
   g(an=band(-25, 205), af=band(-40, 215), bob=(5, 5, 5), lean=(2, 8), ln='ml-dip-rear', lf='ml-dip-lead'),
   g(an=band(-22, -18), af=band(50, 40), bob=(12, 12, 12), lean=(4, 17), ln='tp-rear', lf='tp-lead'),
   g(an=band(-22, -18), af=band(50, 40), bob=(12, 12, 12), lean=(4, 17), ln='tp-rear', lf='tp-lead')] + [
   g(an=band(-55 + 30 * (k % 2), -70 + 30 * (k % 2)), af=band(-25 - 30 * (k % 2), -40 - 30 * (k % 2)), bob=(astro.SPRINT_DY[k] + 5,) * 3, lean=(3, 16), root=(5, 0),
     ln='sr-' + astro.SPRINT_LEGS[k], lf='sr-' + astro.SPRINT_LEGS[(k + 4) % 8]) for k in range(3)] + [
   g(an=astro.TUCK_N, af=astro.TUCK_F, bob=(6, 6, 6), lean=(3, 13), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
   g(an=astro.TUCK_N, af=astro.TUCK_F, bob=(6, 6, 6), lean=(3, 13), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
   g(an=band(-25, 208), af=band(-45, 220), bob=(2, 2, 3), lean=(1, 4), root=(-10, 0)),
   g(root=(-9, 0))],
  [None, 'squint', 'strain', 'strain', 'strain', 'strain', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 26, 12, 14], damage='heavy', rm='E: +5 +5 +5 the strides, +3 +1 the tackle, -10 -9 back to the guard (net 0)',
       extra=tgt('Shoulder Charge', 7),
       anchored={3: [('dust', 'hand', 2, 1)], 4: [('dust', 'feet', -8, -2)], 5: [('dust', 'feet', -8, -2)], 6: [('dust', 'feet', -8, -2)],
                 7: [('star9', 'head', 8, 8), ('dust', 'feet', 4, -2)], 8: [('star3', 'head', 9, 6)]})),

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

# ---------------- self-cast versions (Christopher 2026-11-06 17:48: Palm Healing and Cellular Recovery approved, "it also needs a cast on self animation") ----------------
CHEST = band(-18, 195, fistKind='palm')   # near palm laid flat on its own chest
def _selfx(d): return {k: [(n, 'head', dx, dy) for (n, dx, dy) in v] for k, v in d.items()}
CLIPS.update({
 'palmHealingSelf': ('Palm Healing (self)', 4,
  'Palm Healing cast on self (Medical; Christopher 2026-11-06: the approved Palm Healing also needs a cast-on-self clip): the fighter brings both open hands together in a seal, eyes closing, green medical chakra kindling between the palms; it lays the near palm flat on its own chest, the glow pooling under it and pulsing in (the heal lands on frame 4, the first pulse), a thin green aura round the body; small green health crosses swell and shrink as they rise off the chest; it lowers the hand and settles back into the guard.',
  [g(),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=CHEST, af=band(-35, -120), bob=(1, 1, 2), lean=(0, 1)),
   g(an=CHEST, af=band(-35, -120), bob=(1, 1, 2), lean=(-1, 0)),
   g(an=CHEST, af=band(-35, -120), bob=(1, 1, 2), lean=(-1, 0)),
   g(an=CHEST, af=band(-35, -120), bob=(1, 1, 2), lean=(-1, 0)),
   g(an=CHEST, af=band(-35, -120), bob=(1, 1, 2), lean=(-1, 0)),
   g(an=band(-40, -110), bob=(1, 1, 2), lean=(0, 1)),
   g()],
  [None, 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None],
  [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
  dict(fps=10, react=True, auraColors=MED_AURA, rm='in place',
       anchored={1: [('orbMed', 'hand', 0, -2)], 2: [('orbBigMed', 'hand', 0, -2), ('sparkMed', 'hand', 3, -6)],
                 **_selfx({3: [('palmGlowMed', 4, 13)], 4: [('palmGlowMed', 4, 13), ('star6Med', 4, 13), ('healX1', 7, 9)],
                           5: [('palmGlowMed', 4, 13), ('vRingMed', 1, 13), ('healX2', 7, 6), ('healX1', -4, 9)],
                           6: [('palmGlowMed', 4, 13), ('vRing2Med', 1, 13), ('healX3', 7, 2), ('healX2', -5, 5), ('healX1', 2, 8)],
                           7: [('palmGlowMed', 4, 13), ('moteFMed', 0, 6), ('healX2', 7, -3), ('healX3', -5, 1), ('healX2', 2, 4)],
                           8: [('healX1', 7, -7), ('healX2', -5, -3), ('healX3', 2, 0)], 9: [('healX1', -5, -7), ('healX1', 2, -4)]})})),
 'cellularRecoverySelf': ('Cellular Recovery (self)', 3,
  'Cellular Recovery cast on self v2 (Medical, Regen 3 rounds; Christopher 2026-11-06 18:03: must differ from self-cast Palm Healing: "green ring pulses of energy rising through the body from the feet to the head multiple times"): the fighter presses its open hands together in a seal, eyes closing, green chakra kindling; it opens both palms down at its sides and a green ring of energy wraps its ankles (frame 3, the heal) and rises up through the body to the head, where it bursts into motes; a second and a third ring follow three frames apart, the back of each ring passing behind the body and the front over it, health crosses drifting up in their wake, a thin green aura round it; it settles back into the guard.',
  [g(),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   g(an=SEAL_N, af=SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
   *[g(an=band(-6, -6, fistKind='palm'), af=band(-12, -12, fistKind='palm'), bob=(1, 1, 1) if k % 2 else (1, 0, 1), lean=(0, 0)) for k in range(12)],
   g()],
  [None, 'closed', 'closed'] + ['closed'] * 12 + [None],
  [0, 1, 1] + [1] * 12 + [0],
  dict(fps=10, react=True, auraColors=MED_AURA, rm='in place',
       anchored={1: [('orbMed', 'hand', 0, -2)], 2: [('orbBigMed', 'hand', 0, -2), ('sparkMed', 'hand', 3, -6)]})),
})

# v2 body rings: the back arc is drawn behind the fighter, the front arc and the sides over it, so each ring reads as wrapping the body
astro.NPAT['bodyRingB'] = ['.......lllllllll.......', '....llLL.......LLll....', '..lL...............Ll..', '.......................', '.......................', '.......................', '.......................']
astro.NPAT['bodyRingF'] = ['.......................', '.......................', '.......................', 'DlL.................LlD', 'DlLL...............LLlD', '.DDlLLL.........LLLlDD.', '...DDDlLLLLLLLLLlDDD...']
astro.NPAT['bodyRingBurst'] = ['l...L...l', '.l..l..l.', '..L...L..', '.l..l..l.', 'l...L...l']
_an = CLIPS['cellularRecoverySelf'][-1]['anchored']
for w0 in (3, 6, 9):                       # three rings, three frames apart, each climbing feet to head over six frames
    for n, dy in enumerate((-2, -11, -20, -29, -38, -46)):
        f = w0 + n
        if f > 14: break
        _an.setdefault(f, []).extend([('bodyRingB', 'feet', 0, dy, {'behind': True}), ('bodyRingF', 'feet', 0, dy)])
    if w0 + 6 <= 14: _an.setdefault(w0 + 6, []).extend([('bodyRingBurst', 'head', 0, -6), ('moteFMed', 'head', -5, -9), ('moteFMed', 'head', 5, -8)])
for f, xs in {4: [('healX1', 'head', 8, 26)], 5: [('healX2', 'head', 8, 20), ('healX1', 'head', -7, 28)], 6: [('healX3', 'head', 8, 13), ('healX2', 'head', -7, 22)],
              7: [('healX2', 'head', 8, 6), ('healX3', 'head', -7, 15), ('healX1', 'head', 3, 30)], 8: [('healX1', 'head', 8, 0), ('healX2', 'head', -7, 8), ('healX2', 'head', 3, 24)],
              9: [('healX1', 'head', -7, 2), ('healX3', 'head', 3, 17)], 10: [('healX2', 'head', 8, 22), ('healX2', 'head', 3, 10)], 11: [('healX3', 'head', 8, 15), ('healX1', 'head', -7, 26)],
              12: [('healX2', 'head', 8, 8), ('healX2', 'head', -7, 19)], 13: [('healX1', 'head', 8, 2), ('healX3', 'head', -7, 12)], 14: [('healX1', 'head', -7, 5)]}.items():
    _an.setdefault(f, []).extend(xs)

# Dark Communion v2 (Christopher 2026-11-06 17:46: "needs more dramatic fx more sinister"; still a heal): the caster's eyes
# burn violet in the seal, a shadow pool opens under its feet with black-violet wisps curling up out of it, the palm laid on the
# ally burns with black Sagittarius flame; on the ally a shadow pool spreads underfoot, black tendrils crawl up its legs and
# body as the dark chakra knits it, violet motes rise and black flame flickers off it
astro.NPAT['tendril1'] = ['.K', 'Kp', 'pK', 'K.']
astro.NPAT['tendril2'] = ['..K', '.Kp', 'KpK', 'pK.', 'Kp.', '.K.']
astro.NPAT['tendril3'] = ['...K', '..Kp', '.KpK', 'KpP.', 'pK..', 'Kp..', '.pK.', '..K.']

def _ell(w, h):   # a flat pool: black heart, violet rim
    rows = []
    for y in range(h):
        r = ''
        for x in range(w):
            d = ((x - (w - 1) / 2) / (w / 2)) ** 2 + ((y - (h - 1) / 2) / (h / 2)) ** 2
            r += 'K' if d < 0.45 else ('p' if d < 0.8 else ('P' if d < 1.0 else '.'))
        rows.append(r)
    return rows
astro.NPAT['dcPool1'] = _ell(15, 3); astro.NPAT['dcPool2'] = _ell(23, 5); astro.NPAT['dcPool3'] = _ell(31, 7)
astro.NPAT['dcFlameA'] = ['..P...', '.Pp...', '.pK.P.', 'PpKPp.', 'pKKpK.', 'pKKKp.', '.KKKpP', 'PpKKKp', 'pKKKKp', 'pKKKKp', '.pKKp.', '..pp..']
astro.NPAT['dcFlameB'] = ['....P.', '...pP.', '.P.Kp.', '.pPKp.', '.pKKpP', 'PKKKKp', 'pKKKp.', 'pKKKpP', 'pKKKKp', 'pKKKKp', '.pKKp.', '..pp..']
astro.NPAT['dcFlameS'] = ['.P..', 'Pp..', 'pKP.', 'pKKp', 'pKKp', '.pp.']
_DC = CLIPS['darkCommunion'][-1]['anchored']
B = {'behind': True}
for k, v in {1: [('eyeP', 'eye', 0, 0), ('dcPool1', 'feet', 0, 0)],
             2: [('eyeP', 'eye', 0, 0), ('dcPool2', 'feet', 0, 0), ('dcFlameS', 'feet', -9, -4, B), ('spWisp', 'feet', 8, -6)],
             3: [('eyeP', 'eye', 0, 0), ('dcPool3', 'feet', 0, 0), ('dcFlameA', 'feet', -10, -8, B), ('dcFlameS', 'feet', 9, -4, B), ('pflame1', 'hand', 1, -3)],
             4: [('eyeP', 'eye', 0, 0), ('dcPool3', 'feet', 0, 0), ('dcFlameB', 'feet', -10, -12, B), ('dcFlameA', 'feet', 10, -8, B), ('pflame2', 'hand', 1, -4), ('pwisp', 'feet', -6, -30)],
             5: [('eyeP', 'eye', 0, 0), ('dcPool3', 'feet', 0, 0), ('dcFlameA', 'feet', -11, -16, B), ('dcFlameB', 'feet', 10, -12, B), ('pflame1', 'hand', 2, -5), ('pwisp2', 'feet', 5, -34)],
             6: [('eyeP', 'eye', 0, 0), ('dcPool3', 'feet', 0, 0), ('dcFlameB', 'feet', -10, -14, B), ('dcFlameA', 'feet', 11, -16, B), ('pflame2', 'hand', 1, -4)],
             7: [('eyeP', 'eye', 0, 0), ('dcPool2', 'feet', 0, 0), ('dcFlameS', 'feet', -9, -10, B), ('pflame1', 'hand', 1, -3)],
             8: [('dcPool1', 'feet', 0, 0)], 9: [('dcPool1', 'feet', 0, 0)]}.items():
    _DC[k] = _DC.get(k, []) + v
_DD = CLIPS['darkCommuned'][-1]['anchored']
for k, v in {0: [('dcPool1', 'feet', 0, 0), ('pflame1', 'head', 3, 12)],
             1: [('dcPool2', 'feet', 0, 0), ('tendril2', 'feet', -5, -5), ('tendril2', 'feet', 5, -4), ('pflame2', 'head', 3, 11), ('dcFlameS', 'feet', 0, -4, B)],
             2: [('dcPool2', 'feet', 0, 0), ('tendril3', 'feet', -5, -8), ('tendril3', 'feet', 6, -7), ('tendril2', 'head', -4, 16), ('tendril2', 'head', 5, 18), ('moteP', 'head', 6, 4), ('dcFlameA', 'feet', -1, -8, B)],
             3: [('dcPool2', 'feet', 0, 0), ('tendril3', 'feet', -5, -14), ('tendril3', 'feet', 6, -12), ('tendril3', 'head', -4, 12), ('tendril2', 'head', 5, 10), ('pflame2', 'head', 5, 6), ('moteP', 'head', -6, 0), ('dcFlameB', 'feet', 0, -12, B)],
             4: [('dcPool1', 'feet', 0, 0), ('tendril2', 'feet', -5, -10), ('tendril2', 'feet', 6, -6), ('moteP', 'head', 4, -4), ('pflame1', 'head', -3, 2)],
             5: [('dcPool1', 'feet', 0, 0), ('tendril1', 'feet', -5, -4), ('moteP', 'head', -3, -6)]}.items():
    _DD[k] = _DD.get(k, []) + v
CLIPS['darkCommunion'][-1]['auraColors'] = CLIPS['darkCommuned'][-1]['auraColors'] = ('#9b45ff', '#1c1024')   # v2: black-violet aura
CLIPS['darkCommunion'] = (CLIPS['darkCommunion'][0], CLIPS['darkCommunion'][1], CLIPS['darkCommunion'][2].replace('(Medical,', '(Medical; v2 2026-11-06: darker and more sinister, burning violet eyes, a shadow pool with black-violet wisps, black flame on the palm;', 1)) + CLIPS['darkCommunion'][3:]

# Knuckle Haymaker v3: the thin knuckle-duster band on the rear fist, a glint off it and grey metal sparks on the hit
astro.NPAT['knux'] = ['#####', '#WFF#', '#####']   # v3: a thin 1 px steel band across the knuckles, glint at the front, outlined
astro.NPAT['mSpark'] = ['F.W', '.W.', 'W.F']
astro.NPAT['knuxGlint'] = ['.W.', 'WWW', '.W.']
astro.NPAT['mShards'] = ['F...F', '.W.W.', '..W..', '.W.F.', 'F...W']

# Cheap Shot target (Christopher 2026-11-06 18:01: "on impact back up holding their groin in pain"): its own target state
CLIPS['groinHit'] = ('Cheap Shot', 0,
  'groinHit (target of Cheap Shot): frame 0 is the rising fist landing below the belt; the hips jerk back, the fighter doubles over with both hands clamped to the groin, knees knocking in, and backs up two shuffling steps in pain; it hangs there hunched a beat, then straightens, still wincing, back into the guard.',
  [g(an=band(-12, -62), af=band(-18, -58), bob=(4, 5, 5), lean=(-2, 5), root=(-2, 0), **LOW),
   g(an=band(-10, -60), af=band(-16, -56), bob=(6, 7, 7), lean=(-2, 7), root=(-1, 0), **LOW),
   g(an=band(-10, -60), af=band(-16, -56), bob=(6, 7, 7), lean=(-2, 8), **LOW),
   g(an=band(-10, -60), af=band(-16, -56), bob=(6, 7, 7), lean=(-2, 8), **LOW),
   g(an=band(-12, -62), af=band(-18, -58), bob=(5, 6, 6), lean=(-2, 7), **LOW),
   g(an=band(-30, -70), af=band(-40, -90), bob=(3, 3, 4), lean=(-1, 4)),
   g(an=RECOVER, bob=(1, 1, 2), lean=(0, 2)),
   g()],
  ['pain', 'pain', 'pain', 'pain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=10, react=True, rm='E: -2 -1 backing up (net -3, as hitReact)',
       anchored={0: [('star6', 'hand', 0, -1)], 1: [('star3', 'hand', 0, -1)]}))
APPROVED['groinHit'] = STAT
astro.CLIPS.update(CLIPS)
astro.APPROVED.update({k: APPROVED.get(k, STAT) for k in CLIPS})

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--scene':   # astro_scene.py with this file's patterns registered
        import runpy; sys.argv = ['astro_scene.py'] + a[1:]; runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'astro_scene.py'), run_name='__main__'); sys.exit()
    if '--fx' in a: astro.fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): astro.spec(st)
