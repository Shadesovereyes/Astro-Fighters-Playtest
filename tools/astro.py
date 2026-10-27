"""Astrological (Sign) kit animations (Christopher 2026-10-27: "begin developing Astrological kit animations"; abilities
from the Sign Kits tab of AstroFighters_Abilities, 12 signs x 8). Played from the approved boxing guard (hitReact frame 6)
and returning to it, through universal.py's spec builder. One state per ability. E/W first (W mirrors E), S/N after
approval. Effects use the sign's element colours (Christopher 2026-10-27 17:00): fire = reds/oranges/yellows (Sagittarius:
select black and purple flames), earth = earth and crystal tones, water = water and ice tones; air stays white/pale until ruled.
Run: python3 tools/astro.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/astro.py --fx <state>   (aura / motion blur after the render; splash fx are baked by the renderer)"""
import sys, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universal as U
from universal import band, g, leg, kleg, LOW, BRACE, NPAL, NPAT, nfx, D
from gen import load, save
import stances

STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {'blastWave': 'E/W approved by user 2026-10-27 (v3 S-facing roar release, dd5ab8a; W mirrors E); the S and N rows share the same S turn, their guard frames still to review', 'innerGateAdrenaline': 'E/W approved by user 2026-10-27 (v3 lingering aura, skin flush, veins, aee3dad; W mirrors E) on condition the look lingers while the ability is active; canon A5: a toggle, active until 0 HP or deactivated; S/N to author', 'machLunge': 'E/W approved by user 2026-10-27 (v5 sprint, flaming feet, fire wake, 4 afterimages, fc741f6; W mirrors E); S/N to author', 'shatterPunch': 'E/W approved by user 2026-10-27 (v3 arm swirl + impact burst, fc741f6; W mirrors E); S/N to author'}

U.POSES += [leg('ml-dip-lead', (32, 45), (38, 51), 37), leg('ml-dip-rear', (31, 45), (29, 51), 24, wrap=54, kind='toe60'),   # sprinter dip, rear heel up
            kleg('ml-fly-lead', (33, 42), (39, 46), (38, 52), 'toe30k'), kleg('ml-fly-rear', (31, 42), (25, 47), (20, 51), 'toe30k'),   # driving off the rear foot
            leg('ml-plant-lead', (33, 43), (39, 50), 41), kleg('ml-trail-rear', (31, 43), (26, 49), (22, 54), 'toe30k'),   # lead foot lands a long step on
            leg('sp-load-lead', (32, 43), (35, 51), 36), leg('sp-load-rear', (31, 43), (28, 51), 24),                # Shatter Punch: weight sat back
            leg('sp-drive-lead', (33, 43), (38, 50), 40), leg('sp-drive-rear', (32, 43), (31, 50), 27, wrap=54, kind='toe60')]  # step in, rear heel turns up

# element palettes (letters added to universal.NPAL; W/w white stay for air and highlights)
ELEMENT = {'Y': '#ffe14d', 'O': '#ff8a1c', 'R': '#d8321a',               # fire: yellow core, orange body, red edge
           'K': '#1c1024', 'P': '#9b45ff', 'p': '#55208f',                # Sagittarius: black flame with purple
           'E': '#8a6236', 'e': '#c79a5b', 'C': '#7fe3d0', 'c': '#d9fff6',  # earth: soil browns, crystal teal / glint
           'A': '#2f7fe0', 'a': '#7cc8ff', 'I': '#dff6ff'}                 # water: deep and light water, ice white-blue
NPAL.update(ELEMENT)
# fire fx patterns: flame licks (red edge, orange body, yellow core), a fire-sign guard-crack, embers
NPAT.update({
    'flame1': ['.R.', 'ROR', '.Y.'], 'flame2': ['..R..', '.RO..', '.OYR.', 'ROYOR', '.RRR.'],
    'flame3': ['...R...', '..RO...', '.ROO.R.', '.OYYRO.', 'ROYYYOR', '.ROYOR.', '..RRR..'],
    'shatter1': ['O...O', '.Y.Y.', '..W..', '.Y.Y.', 'O...O'],
    'shatter2': ['R.....R', '.O...O.', '..YYY..', '.YYWYY.', '..YYY..', '.O...O.', 'R.....R'],
    'shatter3': ['R...R...R', '.O..O..O.', '..Y.Y.Y..', '...YWY...', 'OYYWWWYYO', '...YWY...', '..Y.Y.Y..', '.O..O..O.', 'R...R...R'],
    'shard': ['O.', '.R'], 'shardR': ['.O', 'R.'],
    'heat': ['O.Y.O', '.R.R.'], 'embers': ['.O..R', 'R..O.', '..Y..'],
    # Explosive Runes: rune circles seen flat on the ground (ellipse with a glyph stroke), hot as written, lit, smouldering
    'runeHot': ['...YWY...', '.YW.O.WY.', 'YW.OYO.WY', '.YW.O.WY.', '...YWY...'], 'runeLit': ['...OYO...', '.OR.Y.RO.', 'OR.YOY.RO', '.OR.Y.RO.', '...OYO...'],
    'runeDim': ['...R.R...', '.R..O..R.', 'R..O.O..R', '.R..O..R.', '...R.R...'], 'fireLine': ['.R.O.', 'OYROY'],
})
FIRE_AURA = ('#ffb12e', '#e0401c')   # orange next to the body, red outside
FIRE_TRAIL = {(255, 255, 255): (0xff, 0xd2, 0x3f), (0xe3, 0xe3, 0xe3): (0xff, 0x7a, 0x1c)}   # motion-blur streak recoloured: yellow inner half, orange tail

SPRINT = load(D + 'sprint.json')   # the approved sprint: stride, lean and swept-back arms reused by Mach Lunge
SPRINT_LEGS = [p['name'] for p in SPRINT['legs']['poses']]
U.POSES += [{**p, 'name': 'sr-' + p['name']} for p in SPRINT['legs']['poses']]
SPRINT_N, SPRINT_F, SPRINT_DY = SPRINT['arms']['near'], SPRINT['arms']['far'], SPRINT['bob']['dy']
def _foot(p):   # bottom-left anchor for a flame burst at a sprint foot: on the floor when planted, at the raised foot otherwise
    q = SPRINT['legs']['poses'][SPRINT_LEGS.index(p)]
    return [q['footX'] - 3, 63 if q['wrapRow'] >= 56 else q['wrapRow'] + 6]
def _burst(p, k):   # a big flame on each foot, plus a lick trailing off the back of a planted foot; alternating shapes flicker
    at = _foot(p); big = ('flame3', 'flame2')[k % 2]
    return [(big, at)] + ([('flame2' if k % 2 else 'flame1', [at[0] - 5, 63])] if at[1] == 63 else [])
FIRE_WAKE = [[('flame3', [14, 63]), ('flame2', [7, 63]), ('flame3', [1, 63]), ('flame2', [18, 46]), ('flame1', [10, 40]), ('embers', [4, 34])],   # a stream of fire left behind along the
             [('flame2', [15, 63]), ('flame3', [8, 63]), ('flame2', [2, 63]), ('flame1', [17, 44]), ('flame2', [9, 42]), ('embers', [3, 30])]]   # ground and in the air behind the runner, flickering
FOOT_FLAMES = [_burst(SPRINT_LEGS[k], k) + _burst(SPRINT_LEGS[(k + 4) % 8], k + 1) for k in range(6)]
PUNCH = band(-92, -92)                  # straight arm at shoulder height
CHAMBER = band(75, -150)                # rear fist drawn back by the ear, elbow high behind
TUCK_N, TUCK_F = band(-35, 200), band(-50, 215)   # arms tucked tight to the chest for the shoulder charge
FLEX_N, FLEX_F = band(50, -20), band(40, -15)     # elbows flared back, clenched fists low beside the hips (power surge)

CLIPS = {
 'machLunge': ('Mach Lunge', 9,
  'Mach Lunge (Aries taijutsu, Priority gap closer, burns the target), v4 (Christopher 2026-10-27: the sprint instead of a single hop, flames around the feet; afterimages for speed): from the guard the fighter dips, then breaks into the approved sprint (the same stride, lean and swept-back arms), flames bursting around the feet at every step, a stream of fire and four fire-tinted afterimages trailing behind; on the last stride it tucks both arms tight, plants the lead foot and drives the lead shoulder into the target with a flare of flame at the point of contact; then settles back into the guard. The fighter travels 40 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead')] + [
     g(an=SPRINT_N[k], af=SPRINT_F[k], bob=(SPRINT_DY[k],) * 3, lean=(1, 8), root=(6, 0), ln='sr-' + SPRINT_LEGS[k], lf='sr-' + SPRINT_LEGS[(k + 4) % 8]) for k in range(6)] + [
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 7), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 6), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3)),
     g()],
  [None, 'squint'] + ['squint'] * 6 + ['squint', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='light', rm='E: 6 px a stride through the sprint (as the sprint), +3 and +1 into the shoulder check; 40 px in all (travel)',
       ghosts={k: (5, 10, 15, 20) for k in range(2, 8)} | {8: (5, 10, 15), 9: (4, 8), 10: (3,)}, ghostColors=(('#ffe14d', '#ff8a1c'), ('#ff8a1c', '#ffe14d'), ('#d8321a', '#ff8a1c'), ('#d8321a', None)),
       blur={k: 9 for k in range(2, 8)} | {8: 7, 9: 4}, trail=FIRE_TRAIL,
       fx=nfx('fire flame (reds, oranges, yellows): flames bursting around the feet at every stride, a stream of fire trailing behind, a flare where the shoulder lands',
              [(k, FOOT_FLAMES[k - 2] + FIRE_WAKE[k % 2]) for k in range(2, 8)] + [(8, [('flame3', [47, 32]), ('flame1', [40, 63])] + FIRE_WAKE[0][:3]), (9, [('flame3', [48, 31]), ('embers', [45, 24])]), (10, [('embers', [48, 24])])]),
       extra={'airborneFrames': [5], 'travel': {'rule': 'Mach Lunge is a gap closer: the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}})),
 'shatterPunch': ('Shatter Punch', 5,
  'Shatter Punch (Aries taijutsu, Guard Break, can stun), v3 (Christopher 2026-10-27: swirling fx around the winding arm, a more dramatic impact): from the guard the fighter sits its weight back and draws the rear fist far back beside the ear, elbow high, the lead hand reaching out to measure; flame swirls up around the cocked arm, winding tighter and brighter over three held frames; then it steps in and fires the rear fist dead straight through the target with the whole body behind it, rear heel turning up; on contact a white-hot flash bursts at the fist, a ring of fire shock blasts outward, jagged cracks shoot off and shards and embers scatter, the punch held through a hit-stop; then it pulls back into the guard.', [
     g(),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(0, 0), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=CHAMBER, af=band(-80, -95), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 on the step into the punch, -1 settling back',
       swirl={1: (0, 0.35), 2: (100, 0.6), 3: (210, 0.85), 4: (320, 1.0)},   # frame: (phase degrees, strength)
       impact={5: 0, 6: 1, 7: 2, 8: 3})),   # frame: stage of the burst (flash, shock ring, spread, fade)
 'blastWave': ('Blast Wave', 5,
  'Blast Wave (Aries ninjutsu, fire AoE: a small burst of fire that breaks the speed of sound), v2 (Christopher 2026-10-27: turn the fighter to face S for the release, gesture like a power-up scream): from the guard the fighter turns to face the viewer (every facing turns S for the cast), sinks into the knees with both fists pulled in low in front of the belly, head dipped, embers gathering; then it throws its head back with a roar, chest out, both fists clenched and driven down and out to the sides, elbows flared, and the wave releases: a spiked fire aura bursts out round it and sonic-boom rings blast outward, white-hot, then yellow, orange and red as they widen and break up; it holds the roar, then settles back into the guard and turns back to its facing.', [
     g(),
     g(an=band(-30, -120), af=band(-35, -125), bob=(1, 1, 2), lean=(0, 1), **LOW),
     g(), g(bob=(3, 3, 3), **LOW), g(bob=(3, 3, 3), **LOW), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(),
     g()],
  [None, 'squint', None, 'strain', 'strain', 'roar', 'roar', 'roar', None, None],
  None,
  dict(fps=10, front={2: dict(R=stances.GA['R'], L=stances.GA['L']),
                      3: dict(R=(12, -25, 0.85, 'up'), L=(-12, 25, 0.85, 'up')),        # fists pulled in low in front of the belly
                      4: dict(R=(12, -25, 0.85, 'up'), L=(-12, 25, 0.85, 'up')),        # held still (v3: no twitch between held frames)
                      5: dict(R=(42, -5, 1, 'up'), L=(-42, 5, 1, 'up')),                # fists clenched, driven down and out, elbows flared
                      6: dict(R=(42, -5, 1, 'up'), L=(-42, 5, 1, 'up')),
                      7: dict(R=(42, -5, 1, 'up'), L=(-42, 5, 1, 'up')),
                      8: dict(R=stances.GA['R'], L=stances.GA['L'])},
       burst={3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5})),   # frame: stage (embers gathering 0-1, release 2, rings out 3-4, fading 5)
 'explosiveRunes': ('Explosive Runes', 4,
  'Explosive Runes (Aries ninjutsu, trap: glowing rune traps that detonate when a foe comes near): from the guard the fighter makes the tiger seal at the chin, a fire spark kindling between the hands; then it drops low on bent knees and sweeps the near open palm, facing the floor, low and forward over the ground like sowing seed; fire falls from the palm and burns glowing rune circles into the floor ahead, nearest first, the fire line running on past the edge to the rest, each flaring bright as it is written, embers lifting off them; the fighter rises back into the guard and the runes settle to a low smouldering glow (the testbed then draws the placed runes on their tiles until they detonate).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-20, -25, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 7), **BRACE),       # palm swept low, facing the floor
     g(an=band(-45, -45, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 7), **BRACE),       # sweeping on forward over the ground
     g(an=band(-65, -60, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 6), **BRACE),       # arm out, the last rune written
     g(an=band(-30, -90), af=band(-40, -100), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, fx=nfx('fire runes: a spark at the seal, fire running along the ground from the palm, three glowing rune circles burned into the floor ahead, flaring as they are written, then smouldering',
              [(1, [('flame1', [35, 31])]), (2, [('flame2', [34, 32])]),
               (3, [('flame2', [41, 63]), ('fireLine', [44, 63]), ('embers', [38, 50])]),
               (4, [('fireLine', [42, 63]), ('runeHot', [43, 63]), ('flame1', [46, 59]), ('embers', [42, 47]), ('flame1', [44, 54])]),
               (5, [('runeLit', [43, 63]), ('fireLine', [51, 63]), ('runeHot', [54, 63]), ('embers', [45, 57]), ('embers', [48, 42]), ('flame1', [52, 52])]),
               (6, [('runeLit', [43, 63]), ('runeLit', [54, 63]), ('fireLine', [62, 63]), ('embers', [56, 57]), ('embers', [44, 56])]),
               (7, [('runeDim', [43, 63]), ('runeDim', [54, 63])])]))),
 'innerGateAdrenaline': ('Inner Gate: Adrenaline', 4,
  'Inner Gate: Adrenaline (Aries taijutsu buff: AGI and STR up, the fighter burns itself): from the guard the fighter clenches, curls the fists in front of the belly and sinks, straining, eyes squeezed; then the gate bursts open: it stands up tall, chest thrown out and both fists driven down and back, and an orange-red aura flares around the whole body with flame licks rising off the shoulders and head; the aura pulses once, the flames keep licking (the self-burn), then the fighter drops back into the guard still powered up: the aura lingers, the skin stays flushed red and the veins stand out on the arms, neck and temple, embers drifting off it (the testbed keeps that look for as long as the gate stays open: until 0 HP or the player deactivates it).', [
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
  [0, 0, 0, 1, 3, 2, 3, 2, 2],
  dict(fps=10, auraColors=FIRE_AURA, tint={3: 70, 4: 150, 5: 140, 6: 150, 7: 140, 8: 140}, veins=(4, 5, 6, 7, 8),
       extra={'linger': {'rule': 'Inner Gate: Adrenaline (Christopher 2026-10-27: lingering aura, tinted skin, raised veins): the clip ends still powered up (aura 2 px, red skin tint, veins); while the ability is active (canon A5, Christopher 2026-10-27: a toggle, on until the fighter reaches 0 HP or deactivates it; the self Burn ticks every round meanwhile) the testbed keeps drawing the fighter with a 2 px orange-red aura flickering on its outer ring, the skin tint (fx red #ff3a1a at alpha 140 over skin pixels) and the veins, on every state it plays', 'aura': 2, 'auraColors': ['#ffb12e', '#e0401c'], 'tint': ['#ff3a1a', 140], 'veins': '#7a140c'}}, fx=nfx('red-orange-yellow flame licks rising off the shoulders and head as the gate opens (self-burn), embers drifting after',
              [(4, [('flame2', [31, 8]), ('flame2', [25, 26]), ('flame2', [39, 26])]), (5, [('flame3', [30, 8]), ('flame3', [23, 26]), ('flame2', [40, 25])]),
               (6, [('flame2', [32, 7]), ('flame2', [24, 25]), ('flame3', [38, 26])]), (7, [('embers', [31, 7])]), (8, [('embers', [30, 5])])]))),
}

def spec(state):
    U.CLIPS[state] = CLIPS[state]
    U.APPROVED[state] = APPROVED.get(state, STAT)
    U.spec(state)
    x = CLIPS[state][6]; s = load(D + state + '.json')
    for k, v in (x.get('extra') or {}).items(): s[k] = v
    if x.get('front'):   # the fighter turns to face S for part of the clip (Blast Wave v2): every facing plays the S frames there
        s['expressions']['shapes']['roar'] = {'E': copy.deepcopy(s['expressions']['shapes']['pain']['E']),
            'S': [[0, 1, '#000000'], [1, 1, '#000000'], [5, 1, '#000000'], [6, 1, '#000000'], [2, 3, '#000000'], [3, 3, '#000000'], [4, 3, '#000000'], [2, 4, '#000000'], [3, 4, '#70241d'], [4, 4, '#000000']]}   # eyes squeezed, mouth open in a yell (mid-face, clear of the chin)
        s['expressions']['shapes']['strain'] = {'E': copy.deepcopy(s['expressions']['shapes']['pain']['E']),
            'S': [[0, 1, '#000000'], [1, 1, '#000000'], [5, 1, '#000000'], [6, 1, '#000000'], [2, 4, '#000000'], [3, 4, '#000000'], [4, 4, '#000000']]}   # eyes squeezed, teeth clenched
        s['facingOverride'] = {'rule': 'Christopher 2026-10-27: the fighter turns to face S (toward the viewer) for these frames whatever its facing; every row holds the S frame there (the rows are copied after the render), then it turns back', 'frames': sorted(x['front']), 'to': 'S'}
    save(s, D + state + '.json')
    if x.get('front'):
        import universal_sn as USN
        USN.SN[state] = x['front']; USN.sn(state)

def fx(state):
    x = CLIPS[state][6]
    if CLIPS[state][5]: U.CLIPS[state] = CLIPS[state]; U.aura(state)
    if x.get('blur'):
        from PIL import Image
        import kastrikes
        f = D + state + '/fx.png'; old = Image.open(f).convert('RGBA') if os.path.exists(f) else None
        kastrikes.BLUR = x['blur']; kastrikes.blur(state)
        if x.get('trail'):
            b = Image.open(f).convert('RGBA'); px = b.load()
            for yy in range(b.size[1]):
                for xx in range(b.size[0]):
                    q = px[xx, yy]
                    if q[3] and q[:3] in x['trail']: px[xx, yy] = x['trail'][q[:3]] + (255,)
            b.save(f)
        if old: new = Image.open(f).convert('RGBA'); new.alpha_composite(old); new.save(f)
    if x.get('front'): face_front(state, sorted(x['front']))
    if x.get('burst'): burst(state, x['burst'])
    if x.get('tint'): flush(state, x['tint'], x.get('veins', ()))
    if x.get('swirl') or x.get('impact') or x.get('blast'):
        from PIL import Image
        f = D + state + '/fx.png'
        if not os.path.exists(f) or 'fx' not in load(D + state + '.json'): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f)   # no splash fx: start clean (not a stale render)
        if x.get('swirl'): swirl(state, x['swirl'])
        if x.get('impact'): impact(state, x['impact'])
        if x.get('blast'): blast(state, x['blast'])
    if x.get('ghosts'):
        from PIL import Image
        f = D + state + '/fx.png'; top = Image.open(f).convert('RGBA')   # blur + splash so far
        ghosts(state, x['ghosts'], x['ghostColors'])
        g_ = Image.open(f).convert('RGBA'); g_.alpha_composite(top); g_.save(f)   # streaks and flames stay over the afterimages

def _arm(state, k, r, layer='arms.png'):
    from PIL import Image
    a = Image.open(D + state + '/' + layer).convert('RGBA').load()
    return [(x, y) for y in range(64) for x in range(64) if a[k * 64 + x, r * 64 + y][3]]

def swirl(state, frames):
    """Shatter Punch wind-up (Christopher 2026-10-27): fire swirling round the cocked arm. A tilted ellipse round the
    arm's pixels; a comet of flame runs round it, its head yellow, body orange, tail red, longer and doubled as the
    load builds; the half behind the arm hides behind the figure, the front half draws over it"""
    import math
    from PIL import Image
    f = D + state + '/fx.png'; fx = Image.open(f).convert('RGBA'); px = fx.load()
    lay = [Image.open(D + state + '/' + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png', 'far-arm.png') if os.path.exists(D + state + '/' + n)]
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    Y, O, R_ = hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    dirs = load(D + state + '.json')['directions']
    for k, (ph, st) in frames.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            pts = _arm(state, k, r)
            if not pts: continue
            cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
            rx = (max(x for x, _ in pts) - min(x for x, _ in pts)) / 2 + 3; ry = (max(y for _, y in pts) - min(y for _, y in pts)) / 2 + 3
            for ring, (dr, sweep) in enumerate(((0, 300 * st), (2, 200 * st))):
                if ring and st < 0.6: continue
                for t in range(int(sweep * 4)):
                    u = t / (sweep * 4)   # 0 tail .. 1 head
                    th = math.radians(ph + (180 if ring else 0) + t / 4)
                    x = round(cx + sg * (rx + dr) * math.cos(th)); y = round(cy + (ry * 0.7 + dr) * math.sin(th))
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    behind = math.sin(th) < 0
                    if behind and any(L[k * 64 + x, r * 64 + y][3] for L in lay): continue
                    if u < 0.35 and (x + y) % 2: continue   # dithered tail
                    px[k * 64 + x, r * 64 + y] = Y if u > 0.8 else O if u > 0.4 else R_
            # sparks thrown off the swirl
            for i in range(int(4 * st)):
                th = math.radians(ph + 90 * i + 45)
                x = round(cx + sg * (rx + 3) * math.cos(th)); y = round(cy + (ry * 0.7 + 3) * math.sin(th))
                if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, r * 64 + y] = Y
    fx.save(f); print(state, 'arm swirl', list(frames))

def impact(state, frames):
    """Shatter Punch contact (Christopher 2026-10-27: more dramatic): stage 0 a big white-hot flash star at the fist with
    jagged cracks; 1 a fire shock ring blasting out, cracks reaching further, shards; 2 the ring wider and broken,
    shards and embers scattering; 3 embers fading. All drawn on top at the fist (the arms layer's far tip)"""
    import math
    from PIL import Image
    f = D + state + '/fx.png'; fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    dirs = load(D + state + '.json')['directions']
    def put(k, r, x, y, c):
        if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, r * 64 + y] = c
    first = min(frames)
    for k, stage in frames.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            pts = _arm(state, first, r)
            tip = max(pts, key=lambda p: sg * p[0]); fx0, fy = tip[0] + sg * 2, tip[1]
            P = lambda dx, dy, c: put(k, r, fx0 + sg * dx, fy + dy, c)
            cracks = [(0, -1), (1, -2), (2, -1), (1, 1), (2, 2), (-1, 2), (-1, -2), (3, 0)]   # crack directions (x forward, y)
            if stage == 0:
                for i in range(-9, 10):   # the flash star: long horizontal and vertical spikes, shorter diagonals
                    c = W_ if abs(i) < 4 else Y if abs(i) < 7 else O if abs(i) < 9 else R_
                    P(i, 0, c); P(0, i, c); P(i, 1 if abs(i) < 5 else 0, c); P(1 if abs(i) < 5 else 0, i, c)
                    if abs(i) < 7: P(i, i, c if abs(i) < 3 else O); P(i, -i, c if abs(i) < 3 else O)
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if abs(dx) + abs(dy) < 5: P(dx, dy, W_ if abs(dx) + abs(dy) < 3 else Y)
            if stage in (1, 2):
                rad = (7, 11)[stage - 1]
                for t in range(0, 360, 4):   # the shock ring, an upright ellipse (seen side-on)
                    if stage == 2 and (t // 20) % 3 == 0: continue   # breaking up
                    th = math.radians(t)
                    P(round(rad * 0.55 * math.cos(th)), round(rad * 1.3 * math.sin(th)), O if stage == 1 else R_)
                    P(round((rad - 1) * 0.55 * math.cos(th)), round((rad - 1) * 1.3 * math.sin(th)), Y if stage == 1 else O)
                for dx, dy in cracks:   # jagged cracks shooting off
                    L = (8, 12)[stage - 1]
                    for i in range(2, L):
                        jx = (i % 3 == 0) * (1 if dy >= 0 else -1)
                        P(round(dx * i / 2) + jx, round(dy * i / 2), Y if i < L // 2 else O)
                for i, (dx, dy) in enumerate(cracks):   # shards flung out past the cracks
                    d = (11, 16)[stage - 1]
                    sx, sy = round(dx * d / 2), round(dy * d / 2)
                    P(sx, sy, O); P(sx + 1, sy + 1, R_)
                if stage == 1:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2): P(dx, dy, W_ if dx == dy == 0 else Y)
            if stage == 3:
                for i, (dx, dy) in enumerate(cracks):
                    if i % 2: continue
                    P(round(dx * 8), round(dy * 8) - 1, O); P(round(dx * 6) + 1, round(dy * 6) - 2, R_)
                P(-1, -6, Y); P(3, 5, O)
    fx.save(f); print(state, 'impact', frames)

def blast(state, frames):
    """Blast Wave (fire burst breaking the sound barrier): from the palms (the arms layer's far tip on the first frame) a
    cone of flame fans forward and sonic-boom arcs ')' ripple outward through it, each stage one arc further, the
    nearest white-hot, then yellow, orange, red; stage 3 leaves only the last broken arc and embers"""
    import math, random
    from PIL import Image
    f = D + state + '/fx.png'; fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    dirs = load(D + state + '.json')['directions']; first = min(frames)
    lay = [Image.open(D + state + '/' + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png', 'far-arm.png') if os.path.exists(D + state + '/' + n)]
    for k, stage in frames.items():
        rnd = random.Random(k)
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            pts = _arm(state, first, r); tip = max(pts, key=lambda p: sg * p[0]); x0, y0 = tip[0] + sg, tip[1]
            def P(dx, dy, c):
                x, y = x0 + sg * dx, y0 + dy
                if 0 <= x < 64 and 0 <= y < 64: px[k * 64 + x, r * 64 + y] = c
            if stage < 3:   # the flame cone: dithered fire fanning out, hotter near the palms
                L = (7, 11, 13)[stage]
                for dx in range(0, L):
                    h = 1 + dx * 2 // 3
                    for dy in range(-h, h + 1):
                        if rnd.random() < (0.9 if dx < 3 else 0.55 - 0.03 * dx): P(dx, dy, ramp[min(3, (dx * 4) // (L + 1) + (abs(dy) > h - 1))])
            for j in range(stage + 1):   # the sonic boom: rings bursting out round the whole fighter, oldest widest
                rx = 9 + 8 * (stage - j); ry = round(rx * 0.75); c = ramp[min(3, stage - j + (stage == 3))]
                for t in range(0, 360, 2):
                    if (stage - j) >= 2 and (t // 12) % 3 == 0: continue   # the outer ring breaks up
                    th = math.radians(t); x = round(32 + rx * math.cos(th)); y = round(34 + ry * math.sin(th))
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    if math.sin(th) < 0 and any(L[k * 64 + x, r * 64 + y][3] for L in lay): continue   # far half behind the figure
                    px[k * 64 + x, r * 64 + y] = c
            if stage >= 2:
                for i in range(6): P(rnd.randint(4, 16), rnd.randint(-10, 10), (O, R_, Y)[i % 3])
    fx.save(f); print(state, 'blast', frames)

SKIN = {(0xf6, 0xa3, 0x5b), (0xc8, 0x78, 0x45), (0x9e, 0x4a, 0x31)}   # the rig's skin ramp (L, m, s)
def flush(state, tint, veins):
    """Inner Gate (Christopher 2026-10-27): the skin flushes red (a translucent red over every skin pixel, alpha per frame)
    and veins stand out on the forearms, upper arms, neck and temple (dark red broken lines, interior skin pixels only).
    Written as two extra layers so clothing, armour and hair still cover it: skin-fx.png (body + far arm skin, drawn just
    above body.png / far-arm.png) and arms-fx.png (near arm skin, drawn just above arms.png)"""
    from PIL import Image
    d = D + state + '/'
    dirs = load(D + state + '.json')['directions']
    for src, out in ((('body.png', 'far-arm.png'), 'skin-fx.png'), (('arms.png',), 'arms-fx.png')):
        lays = [Image.open(d + n).convert('RGBA') for n in src if os.path.exists(d + n)]
        if not lays: continue
        img = Image.new('RGBA', lays[0].size); px = img.load(); lays = [L.load() for L in lays]
        for k, al in tint.items():
            for fd in dirs:
                r = dirs.index(fd)
                skin = {(x, y) for L in lays for y in range(64) for x in range(64) if (q := L[k * 64 + x, r * 64 + y])[3] and q[:3] in SKIN}
                for (x, y) in skin: px[k * 64 + x, r * 64 + y] = (0xff, 0x3a, 0x1a, al)
                if k not in veins or not skin: continue
                top_y = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                for (x, y) in skin:
                    if top_y + 2 < y < top_y + 11:   # head: a short vein at the temple only, the face stays clean
                        if y in (top_y + 3, top_y + 4) and (x + y) % 3 == 0 and (x - 1, y) in skin and (x + 1, y) in skin: px[k * 64 + x, r * 64 + y] = (0x7a, 0x14, 0x0c, 255)
                        continue
                    across = ((x - 1, y) in skin and (x + 1, y) in skin and (x - 2, y) not in skin | {(x, y)}) or ((x, y - 1) in skin and (x, y + 1) in skin)
                    # a vein runs down the middle of each limb's cross-section (arms, neck), broken every few pixels
                    mid = (x - 1, y) in skin and (x + 1, y) in skin if (x, y - 1) in skin and (x, y + 1) in skin else (x, y - 1) in skin and (x, y + 1) in skin
                    if mid and (x * 3 + y) % 5 != 0: px[k * 64 + x, r * 64 + y] = (0x7a, 0x14, 0x0c, 255)
        img.save(d + out)
    print(state, 'flush', list(tint), 'veins', list(veins))

def face_front(state, frames):
    """every row takes the S row's frame on the turned frames (all layers), so each facing turns to the viewer there"""
    from PIL import Image
    d = D + state + '/'; dirs = load(D + state + '.json')['directions']; rs = dirs.index('S')
    for n in sorted(os.listdir(d)):
        if not n.endswith('.png') or n == 'fx.png': continue
        im = Image.open(d + n).convert('RGBA')
        if im.height < 64 * len(dirs): continue
        for k in frames:
            cell = im.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
            for r in range(len(dirs)):
                if r != rs: im.paste(cell, (k * 64, r * 64))
        im.save(d + n)
    print(state, 'S frames on every row', frames)

def burst(state, frames):
    """Blast Wave v2 (facing S): embers gathering round the crouched fighter (stages 0-1), then the release: a spiked fire
    aura round the whole figure (inner yellow glow, flame spikes radiating out, longer at the release) and sonic-boom rings
    blasting out round it, white-hot, then yellow, orange, red as they widen and break up (stages 2-5). Drawn on the S row
    and copied to every row (all rows show the S frame there)"""
    import math, random
    from PIL import Image, ImageFilter
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']; rs = dirs.index('S')
    base = Image.open(d + 'body.png'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) and 'fx' in load(D + state + '.json') else Image.new('RGBA', base.size)   # no splash fx: start clean
    if fx.size != base.size: n_ = Image.new('RGBA', base.size); n_.paste(fx, (0, 0)); fx = n_
    px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    lay = [Image.open(d + n).convert('RGBA') for n in ('body.png', 'arms.png', 'male-gi.png', 'fade-hair.png', 'far-arm.png') if os.path.exists(d + n)]
    for k, st in frames.items():
        rnd = random.Random(k * 7)
        box = (k * 64, rs * 64, k * 64 + 64, rs * 64 + 64)
        m = Image.new('L', (64, 64))
        for L in lay: m.paste(255, (0, 0), L.crop(box).getchannel('A').point(lambda v: 255 if v else 0))
        fig = m.load(); pts = [(x, y) for y in range(64) for x in range(64) if fig[x, y]]
        cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
        def P(x, y, c, over=False):
            if 0 <= x < 64 and 0 <= y < 64 and (over or not fig[x, y]): px[box[0] + x, box[1] + y] = c
        if st <= 1:   # embers drawn in toward the fighter
            for i in range(10 + 6 * st):
                th = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(14, 24) - 5 * st
                P(round(cx + rr * math.cos(th)), round(cy + rr * 1.2 * math.sin(th)), (Y, O, R_)[i % 3])
            g1 = m.filter(ImageFilter.MaxFilter(3)).load()
            for (x, y) in [(x, y) for y in range(64) for x in range(64) if g1[x, y] and not fig[x, y]]:
                if (x + y + k) % 2 == 0 or st: P(x, y, O if st else R_)
            continue
        # spiked fire aura: glow rings, then flame spikes out of the silhouette
        grow = [m]
        for i in range(3): grow.append(grow[-1].filter(ImageFilter.MaxFilter(3)))
        G = [g.load() for g in grow]; wd = (3, 3, 2, 1)[st - 2]
        for y in range(64):
            for x in range(64):
                for i in range(1, wd + 1):
                    if G[i][x, y] and not G[i - 1][x, y]: P(x, y, (Y, O, R_)[min(2, i - 1)]); break
        L0 = (10, 8, 5, 3)[st - 2]
        for t in range(0, 360, 12):
            th = math.radians(t + (k * 5)); L = L0 + rnd.randint(-2, 3)
            # start at the silhouette edge in that direction
            r0 = 0
            while r0 < 40:
                x, y = round(cx + r0 * math.sin(th)), round(cy - r0 * math.cos(th))
                if not (0 <= x < 64 and 0 <= y < 64) or not fig[x, y]: break
                r0 += 1
            for i in range(L):
                u = i / L; w = 1 if u < 0.6 else 0
                x, y = cx + (r0 + i) * math.sin(th), cy - (r0 + i) * math.cos(th)
                c = Y if u < 0.35 else O if u < 0.7 else R_
                P(round(x), round(y), c)
                if w: P(round(x + math.cos(th)), round(y + math.sin(th)), c)
        # sonic-boom rings round the fighter
        for j in range(st - 1):
            age = st - 2 - j; rx = 12 + 9 * age; ry = round(rx * 0.8); c = ramp[min(3, age + (st == 5))]
            for t in range(0, 360, 2):
                if age >= 2 and (t // 12) % 3 == 0: continue
                th = math.radians(t)
                P(round(cx + rx * math.cos(th)), round(cy + 4 + ry * math.sin(th)), c)
        if st == 2:   # the white-hot release flash at the chest
            for i in range(-3, 4): P(round(cx) + i, round(cy) - 6, W_ if abs(i) < 2 else Y, over=False)
    for k in frames:   # every row shows the S frame here
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(f); print(state, 'burst', frames)

def ghosts(state, offs, cols):
    """after the blur: afterimages (Christopher 2026-10-27: onion/afterimage effects to exaggerate the speed). On each
    dash frame the figure's own silhouette is stamped again 4-18 px behind it on the fx layer, nearest first: an edge of
    solid colour with a dithered fill, fading out (orange/yellow, then red/orange, then a bare red edge); drawn only where
    the figure itself is not, so the real fighter stays on top"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'
    lay = [Image.open(d + n).convert('RGBA').load() for n in ('body.png', 'arms.png', 'far-arm.png', 'male-gi.png', 'fade-hair.png') if os.path.exists(d + n)]
    fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    dirs = load(D + state + '.json')['directions']
    for k, os_ in offs.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1
            fig = {(x, y) for y in range(64) for x in range(64) if any(a[k * 64 + x, r * 64 + y][3] for a in lay)}
            for i, o in sorted(enumerate(os_), key=lambda t: -t[0]):   # farthest first, nearest drawn over it
                edge, fill = cols[min(i, len(cols) - 1)]
                for (x, y) in fig:
                    X = x - sg * o
                    if not (0 <= X < 64) or (X, y) in fig: continue
                    rim = any((x + dx, y + dy) not in fig for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if rim: px[k * 64 + X, r * 64 + y] = hexc(edge)
                    elif fill and (X + y) % 2 == 0: px[k * 64 + X, r * 64 + y] = hexc(fill)
    fx.save(f); print(state, 'afterimages', offs)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--fx' in a: fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
