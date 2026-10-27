"""Astrological (Sign) kit animations (Christopher 2026-10-27: "begin developing Astrological kit animations"; abilities
from the Sign Kits tab of AstroFighters_Abilities, 12 signs x 8). Played from the approved boxing guard (hitReact frame 6)
and returning to it, through universal.py's spec builder. One state per ability. E/W first (W mirrors E), S/N after
approval. Effects white/neutral (element flavour is carried by shape, not colour).
Run: python3 tools/astro.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/astro.py --fx <state>   (aura / motion blur after the render; splash fx are baked by the renderer)"""
import sys, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universal as U
from universal import band, g, leg, kleg, LOW, BRACE, NPAL, NPAT, nfx, D
from gen import load, save

STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {}

U.POSES += [leg('ml-dip-lead', (32, 45), (38, 51), 37), leg('ml-dip-rear', (31, 45), (29, 51), 24, wrap=54, kind='toe60'),   # sprinter dip, rear heel up
            kleg('ml-fly-lead', (33, 42), (39, 46), (38, 52), 'toe30k'), kleg('ml-fly-rear', (31, 42), (25, 47), (20, 51), 'toe30k'),   # driving off the rear foot
            leg('ml-plant-lead', (33, 43), (39, 50), 41), kleg('ml-trail-rear', (31, 43), (26, 49), (22, 54), 'toe30k'),   # lead foot lands a long step on
            leg('sp-load-lead', (32, 43), (35, 51), 36), leg('sp-load-rear', (31, 43), (28, 51), 24),                # Shatter Punch: weight sat back
            leg('sp-drive-lead', (33, 43), (38, 50), 40), leg('sp-drive-rear', (32, 43), (31, 50), 27, wrap=54, kind='toe60')]  # step in, rear heel turns up

# fx patterns (white/neutral): flame licks for the fire signs, cracks for guard breaks
NPAT.update({
    'flame1': ['.w.', 'wWw', '.W.'], 'flame2': ['..w..', '.wW..', '.WWw.', 'wWWWw', '.www.'],
    'flame3': ['...w...', '..wW...', '.wWW.w.', '.WWWwW.', 'wWWWWWw', '.wWWWw.', '..www..'],
    'shatter1': ['W...W', '.W.W.', '..W..', '.W.W.', 'W...W'],
    'shatter2': ['w.....w', '.W...W.', '..WWW..', '.WWWWW.', '..WWW..', '.W...W.', 'w.....w'],
    'shatter3': ['w...w...w', '.w..W..w.', '..W.W.W..', '...WWW...', 'WWWW.WWWW', '...WWW...', '..W.W.W..', '.w..W..w.', 'w...w...w'],
    'shard': ['w.', '.w'], 'shardR': ['.w', 'w.'],
    'heat': ['w.w.w', '.w.w.'], 'embers': ['.w..w', 'w..w.', '..w..'],
})

PUNCH = band(-92, -92)                  # straight arm at shoulder height
CHAMBER = band(75, -150)                # rear fist drawn back by the ear, elbow high behind
TUCK_N, TUCK_F = band(-35, 200), band(-50, 215)   # arms tucked tight to the chest for the shoulder charge
FLEX_N, FLEX_F = band(50, -20), band(40, -15)     # elbows flared back, clenched fists low beside the hips (power surge)

CLIPS = {
 'machLunge': ('Mach Lunge', 4,
  'Mach Lunge (Aries taijutsu, Priority gap closer, burns the target): from the guard the fighter dips into a sprinter crouch, then explodes off the rear foot, tucking both arms tight and lowering the lead shoulder; it rockets forward low, a white heat streak trailing off its back and flame licks peeling off the shoulder, lands a long step on and drives the shoulder into the target with a flare of flame at the point of contact; then settles back into the guard. The fighter travels 18 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(1, 1, 1), lean=(2, 7), root=(6, 0), ln='ml-fly-rear', lf='ml-fly-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(1, 1, 1), lean=(2, 8), root=(6, 0), ln='ml-fly-rear', lf='ml-fly-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 7), root=(4, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 6), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3), root=(1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='light', rm='E: 18 px forward over the dash (travel)',
       blur={2: 8, 3: 11, 4: 6},
       fx=nfx('white/neutral flame: licks peeling off the lead shoulder in flight, a flare where the shoulder lands',
              [(2, [('flame2', [28, 23]), ('heat', [24, 27])]), (3, [('flame3', [26, 23]), ('flame1', [24, 28])]),
               (4, [('flame3', [47, 32]), ('flame1', [33, 22])]), (5, [('flame2', [49, 30]), ('embers', [46, 24])]), (6, [('embers', [48, 24])])]),
       extra={'airborneFrames': [2, 3], 'travel': {'rule': 'Mach Lunge is a gap closer: the fighter ends the clip 18 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 18}})),
 'shatterPunch': ('Shatter Punch', 4,
  'Shatter Punch (Aries taijutsu, Guard Break, can stun): from the guard the fighter sits its weight back and draws the rear fist far back beside the ear, elbow high, the lead hand reaching out to measure; holds the load a beat, then steps in and fires the rear fist dead straight through the target with the whole body behind it, rear heel turning up; a white crack bursts out from the fist on contact and shards fly; it holds the extension a beat, then pulls back into the guard.', [
     g(),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(0, 0), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 on the step into the punch, -1 settling back',
       fx=nfx('white guard-crack burst at the fist on contact, shards flying off',
              [(4, [('shatter2', [55, 27])]), (5, [('shatter3', [55, 28]), ('shard', [52, 18]), ('shardR', [62, 30])]),
               (6, [('shard', [50, 15]), ('shardR', [62, 33]), ('shatter1', [57, 26])])]))),
 'innerGateAdrenaline': ('Inner Gate: Adrenaline', 4,
  'Inner Gate: Adrenaline (Aries taijutsu buff: AGI and STR up, the fighter burns itself): from the guard the fighter clenches, curls the fists in front of the belly and sinks, straining, eyes squeezed; then the gate bursts open: it stands up tall, chest thrown out and both fists driven down and back, and a white aura flares around the whole body with flame licks rising off the shoulders and head; the aura pulses once, the flames keep licking (the self-burn), then the fighter drops back into the guard with embers still drifting off it.', [
     g(),
     g(an=band(-30, -120), af=band(-35, -125), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-20, -100), af=band(-25, -105), bob=(3, 3, 4), lean=(0, 3), **LOW),
     g(an=band(-20, -100), af=band(-25, -105), bob=(3, 3, 4), lean=(0, 3), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=FLEX_N, af=FLEX_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=FLEX_N, af=FLEX_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-25, 205), af=band(-40, 215), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'pain', 'pain', 'squint', 'squint', 'squint', None, None],
  [0, 0, 0, 1, 3, 2, 3, 1, 0],
  dict(fps=10, fx=nfx('white flame licks rising off the shoulders and head as the gate opens (self-burn), embers drifting after',
              [(4, [('flame2', [31, 8]), ('flame2', [25, 26]), ('flame2', [39, 26])]), (5, [('flame3', [30, 8]), ('flame3', [23, 26]), ('flame2', [40, 25])]),
               (6, [('flame2', [32, 7]), ('flame2', [24, 25]), ('flame3', [38, 26])]), (7, [('embers', [31, 7])]), (8, [('embers', [30, 5])])]))),
}

def spec(state):
    U.CLIPS[state] = CLIPS[state]
    U.APPROVED[state] = APPROVED.get(state, STAT)
    U.spec(state)
    x = CLIPS[state][6]; s = load(D + state + '.json')
    for k, v in (x.get('extra') or {}).items(): s[k] = v
    save(s, D + state + '.json')

def fx(state):
    x = CLIPS[state][6]
    if CLIPS[state][5]: U.CLIPS[state] = CLIPS[state]; U.aura(state)
    if x.get('blur'):
        from PIL import Image
        import kastrikes
        f = D + state + '/fx.png'; old = Image.open(f).convert('RGBA') if os.path.exists(f) else None
        kastrikes.BLUR = x['blur']; kastrikes.blur(state)
        if old: new = Image.open(f).convert('RGBA'); new.alpha_composite(old); new.save(f)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--fx' in a: fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
