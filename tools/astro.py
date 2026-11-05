"""Astrological (Sign) kit animations (Christopher 2026-10-27: "begin developing Astrological kit animations"; abilities
from the Sign Kits tab of AstroFighters_Abilities, 12 signs x 8). Played from the approved boxing guard (hitReact frame 6)
and returning to it, through universal.py's spec builder. One state per ability. E/W first (W mirrors E), S/N after
approval. Effects use the sign's element colours (Christopher 2026-10-27 17:00): fire = reds/oranges/yellows (Sagittarius:
select black and purple flames), earth = earth and crystal tones, water = water and ice tones; air stays white/pale until ruled.
Run: python3 tools/astro.py [state] ; node tools/character-posed.mjs male <state> ; python3 tools/stances.py --outline <state> ;
     python3 tools/astro.py --fx <state>   (aura / motion blur after the render; splash fx are baked by the renderer)"""
import math
import sys, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universal as U
from universal import band, g, leg, kleg, LOW, BRACE, NPAL, NPAT, nfx, D
from gen import load, save
import stances

STAT = 'CANDIDATE 2026-10-27 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {'slideCounter': 'E/W approved by user 2026-11-05 15:04 (v1 water slick, slides 22 px back with a wake, open-hand counter stance with water rings, 39e4d09; W mirrors E); S/N to author', 'betrayal': 'E/W approved by user 2026-11-05 14:59 (v1 palm over the heart, shadow-water waves volley frames 5-6, impact 7, 9ebd110; target plays betrayed; genjutsu mark water; W mirrors E); S/N to author', 'betrayed': 'E/W approved by user 2026-11-05 14:59 (v2.1 the target\'s own eyeless shadow silhouette, drawn at runtime (extra.shadowDouble), stabs its back three times with a shadow knife; it turns round in shock through S (frames 8, 11; awayFrames 9-10) and back; trembling loop from 13, 090c014; W mirrors E); S/N to author', 'blizzard': 'E/W approved by user 2026-11-04 22:29 (v3.2 ultimate, 16 frames: snow-vortex charge, flash, arms flung wide; caster-centred radius-3 storm (extra.zone selfCentered) races out ring by ring frames 10-12, lingers on the cast hexes for 2 rounds, diamond-dust flashes in the snow, 72a2f7d; targets play blizzardStruck; W mirrors E); S/N to author', 'blizzardStruck': 'E/W approved by user 2026-11-04 22:29 (v2 shields face, ice shards, frost crust, shiver loop from 4, 72a2f7d; W mirrors E); S/N to author', 'paranoia': 'E/W approved by user 2026-11-04 (v1 fingers to the temple, ice-blue eyes, shadow wisps, shadow-water waves volley frames 5-6, impact 7, 9ebd110; target plays paranoid; genjutsu mark water; W mirrors E); S/N to author', 'paranoid': 'E/W approved by user 2026-11-04 (v1 flinch, darting guard loop from 4 while shadow eyes open round it, 9ebd110; W mirrors E); S/N to author', 'iceShard': 'E/W approved by user 2026-11-04 (v1 seal, two-finger point, three ice darts freeze behind the target and strike its back on impact frame 6 via extra.targetFx, 2b76e70; target plays iceShardStruck; W mirrors E); S/N to author', 'iceShardStruck': 'E/W approved by user 2026-11-04 (v1 jolted forward, ice shatters off its back, 2b76e70; W mirrors E); S/N to author', 'frostArmor': 'E/W approved by user 2026-11-04 (v1 seal, braced flex, frost floor, runtime ice shell extra.iceShell drawn from the fighter outline, cracks into place frame 6, linger while the buff lasts, 2b76e70; W mirrors E); S/N to author', 'kidneyShot': 'E/W approved by user 2026-11-04 (v2 half-jab feint, dip and step in, rear hook to the flank, huge water burst with shards and double ring on impact frame 4, d1675b1; target plays kidneyStruck; W mirrors E); S/N to author', 'kidneyStruck': 'E/W approved by user 2026-11-04 (v2 buckles clutching its side, water blasts out of its back, recovers, d1675b1; W mirrors E); S/N to author', 'numbingStrike': 'E/W approved by user 2026-11-04 (v2 Numbing Strikes: four alternating two-finger strikes lead/rear/lead/rear frames 2-5, ice flashes, shards and frost rings, d1675b1; renamed Numbing Strikes (canon amendment); target plays numbed; W mirrors E); S/N to author', 'numbed': 'E/W approved by user 2026-11-04 (v2 jolts on each of the four hits, arm goes dead, frost, recovers, d1675b1; W mirrors E); S/N to author', 'shadowStep': 'E/W approved by user 2026-11-04 (v1 crouch, shadow pool spreads, sinks into it with opacity fade, pool slides 40 px, rises and fades into Stealth; extra.floorFx, travel 40, b0fde8e; W mirrors E); S/N to author', 'regression': 'E/W approved by user 2026-11-04 (v2 drop in the palm, ripples, ring waves fly to the target as a projectile volley frames 5-6, impact frame 7, f5b09c8; target plays regressed; genjutsu mark water; W mirrors E); S/N to author', 'regressed': 'E/W approved by user 2026-11-04 (v1 guard melts into a toddler stance, toddle loop from frame 4 while Slowed, e427e00; W mirrors E); S/N to author', 'pacification': 'E/W approved by user 2026-11-04 (v2 palms settle still water, lullaby lines fly to the target frames 5-6, impact frame 7, f5b09c8; target plays pacified; genjutsu mark water; W mirrors E); S/N to author', 'pacified': 'E/W approved by user 2026-11-04 (v1 eyes droop, arms fall slack, weapon drops frame 2, drowsy sway loop from frame 4, e427e00; W mirrors E); S/N to author', 'hydroCannonPalm': 'E/W approved by user 2026-11-04 (v5 six-frame water swirl round the palm, held palm thrust, fire-hose stream drawn by the testbed from extra.stream, front travels frames 7-8, touches the target on frame 9 (impact), pours four frames, 0c2f0ef; target plays hydroWaved; W mirrors E); S/N to author', 'hydroWaved': 'E/W approved by user 2026-11-04 (v2 contact frame 0 at impact, jolt, pressure wave rolls through and bursts out of the back, doubles over, recovers, 0c2f0ef; W mirrors E); S/N to author', 'viceGrip': 'E/W approved by user 2026-11-04 (v5 crab slip-in, water coats both arms, big water pincer rooted in the lowered hand, clamps round the target on frame 5 (impact), hold loops 5-7 with a water rope from each hand, far arm in far-arm sheet, 0c2f0ef; target plays viceGripped; W mirrors E); S/N to author', 'viceGripped': 'E/W approved by user 2026-11-04 (v4 frame 0 is the clamp shutting round the body, arms pinned, struggle loop from frame 2 while held, 0db0feb; W mirrors E); S/N to author', 'tidalSlam': 'E/W approved by user 2026-11-04 (v5 palms summon the wave, rides on top of it in a surfer stance, curling wave rooted behind the riding wave, flying elbow drop onto the shoulder with the crest pouring over onto the elbow, 4a65f39; lift by bodyRotation dy; target plays tidalSlammed; travel 40; W mirrors E); S/N to author', 'tidalSlammed': 'E/W approved by user 2026-11-04 (v1 crushed to one knee, water pours over it, rises, 4a65f39; W mirrors E); S/N to author', 'tsunamiCharge': 'E/W approved by user 2026-11-04 (v4 seal, rising drops and ripples, water spout widening into a vortex round the body, floor burst, shaking hold loops from frame 13, no small wave, e7e649f; then tsunami; W mirrors E); S/N to author', 'tsunami': 'E/W approved by user 2026-11-04 (v4 release: haul back, thrust bursts the vortex, giant breaking wave wTsunamiBig0-3 rolled across the AoE by the testbed from extra.zone, e7e649f; targets play tsunamiStruck; W mirrors E); S/N to author', 'tsunamiStruck': 'E/W approved by user 2026-11-04 (v2 arms up, swallowed and tumbled flat through the water, dumped to one knee, recovers, 2cb675b; with Tsunami v4; W mirrors E); S/N to author', 'waterCutter': 'E/W approved by user 2026-11-03 (v1 seal, water blade gathered along the drawn-back knife hand, level slash flings it; projectile wBladeL from frame 5, hit wCut, c432151; target plays hitReact; W mirrors E); S/N to author', 'whirlpool': 'E/W approved by user 2026-11-03 (v1 seal, low palm circles over the ground, fist wrench, c432151; targets play whirlpoolCaught then whirlpoolRelease; W mirrors E); S/N to author', 'whirlpoolCaught': 'E/W approved by user 2026-11-03 (v1 puddle churns into a whirlpool, water spirals up the legs, arms out for balance, loop from frame 4 while Rooted, c432151; W mirrors E); S/N to author', 'whirlpoolRelease': 'E/W approved by user 2026-11-03 (v1 whirlpool drains to a puddle, steps free, c432151; W mirrors E); S/N to author', 'sonicSweep': 'E/W approved by user 2026-11-03 (v2 step-in drop, long rear-leg load, sweep cracks out at ankle height, floor swoosh, vapour cone, follow-through, 06ada59; target plays sonicSwept then prone, getUp; W mirrors E); S/N to author', 'sonicSwept': 'E/W approved by user 2026-11-03 (v1 feet knocked out, laid flat on its back by a quarter turn, dust, 06ada59; W mirrors E); S/N to author', 'echoFist': 'E/W approved by user 2026-11-03 (v2 humming rings on the loaded fist, cross, crack and boom, two echo pulses with shockwave arcs through the target, 06ada59; target plays echoReverb; W mirrors E); S/N to author', 'echoReverb': 'E/W approved by user 2026-11-03 (v1 three jolts, arcs bursting out of the back, stagger, 06ada59; W mirrors E); S/N to author', 'tinnitus': 'E/W approved by user 2026-11-03 (v2 finger to the ear, green-tailed sine lines, finger points at the target, green aura rim, b81a3e0; target plays tinnitusRinging; W mirrors E); S/N to author', 'tinnitusRinging': 'E/W approved by user 2026-11-03 (v2 far hand to the far ear, near fist low, wince, sine lines, drip, b81a3e0; W mirrors E); S/N to author', 'resonanceChamber': 'E/W approved by user 2026-11-03 (v2 palms drawn apart, standing sound bars with green caps both sides, floor ring, green aura rim, b81a3e0; W mirrors E); S/N to author', 'howlingBlast': 'E/W approved by user 2026-11-03 (v2 breath, braced howl, sound shockwaves roll out of the mouth toward the target, projectile volley hw3 from the mouth, 39ea3ef; W mirrors E); S/N to author', 'mirageClone': 'E/W approved by user 2026-11-03 (v2 seal, blur, dart, indistinguishable full-colour clone 18 px ahead; extra.decoy, canon A8; 39ea3ef; W mirrors E); S/N to author', 'mirageCloneDispel': 'E/W approved by user 2026-11-03 (v1 hit flinch, pixel break-up with air puffs and green motes, 39ea3ef; W mirrors E); S/N to author', 'aeroPalm': 'E/W approved by user 2026-11-03 (v2 four palm pops each firing its own airPuck at the target, final full palm fires airSlug, green rim; W mirrors E); S/N to author', 'lagSwitch': 'E/W approved by user 2026-11-03 (v2 clock dial on the palm sweeps backward, rewind tick waves at the target; target plays lagSwitched; W mirrors E); S/N to author', 'lagSwitched': 'E/W approved by user 2026-11-03 (v2 arms dropped slack, sway, loading spinner and floor loop arrow, loop from frame 4; W mirrors E); S/N to author', 'systemCrash': 'E/W approved by user 2026-11-03 (v1 two fingers to the temple, glitch waves, 086cdc62; target plays systemCrashed; W mirrors E); S/N to author', 'systemCrashed': 'E/W approved by user 2026-11-03 (v2 arms held out front groping blind, no arm over the face, 7f38dd1b; W mirrors E); S/N to author', 'voltaicOrb': 'E/W approved by user 2026-11-03 (v1 seal, orb kindles between the palms, both palms hurl it, 43180ea3; projectile voltOrb4; targets play voltaicShocked; W mirrors E); S/N to author', 'voltaicShocked': 'E/W approved by user 2026-11-03 (v1 orb bursts into a sphere of lightning round the target, jolt, sparks, 43180ea3; W mirrors E); S/N to author', 'empField': 'E/W approved by user 2026-11-03 (v4 charge, flash, bolts and floor rings; one radius-2 field drawn by the testbed from zone.draw with the dome look, pulses outward, 0d8e1dd7; enemies play empSlowed; W mirrors E); S/N to author', 'empSlowed': 'E/W approved by user 2026-11-03 (with EMP Field v4, 0d8e1dd7; W mirrors E); S/N to author', 'lightningCutter': 'E/W approved by user 2026-11-03 (v4 sprinting uppercut to the body: electric blade sheaf wraps the knife hand carried low through the run, rips up into the torso, e9311c7d; target plays lightningImpaled; travel 40; W mirrors E); S/N to author', 'lightningImpaled': 'E/W approved by user 2026-11-03 (v3 blades punch up out of the upper back, convulses, hand rips free, staggers, e9311c7d; W mirrors E); S/N to author', 'nerveDisruptor': 'E/W approved by user 2026-10-30 (v1 static crackles over the lead fist, charged jab, spark flash, forked lightning, f5d859a8; recoloured electric green-white by user request 2026-10-30; W mirrors E); S/N to author', 'staticShell': 'E/W approved by user 2026-10-30 (v1 fists at the hips, crackling aura, arcs beside the body, shock ring at the feet, f5d859a8; recoloured electric green-white by user request 2026-10-30; W mirrors E); linger is a proposal; S/N to author', 'shockPalm': 'E/W approved by user 2026-10-30 (v1 lightning orb swells in the drawn-back palm, palm drive discharges in bolts and a shock ring, f5d859a8; recoloured electric green-white by user request 2026-10-30; W mirrors E); S/N to author', 'atlasRegret': 'E/W approved by user 2026-10-30 (v1 palms press slowly down, blazing eyes, 3c6a7d94; target plays atlasBurdened; W mirrors E); S/N to author', 'atlasBurdened': 'E/W approved by user 2026-10-30 (v3 globe settles on the shoulders, arms hang at the sides, sinks to one knee, trembling loop from frame 5, a1de2d5d; W mirrors E); S/N to author', 'atlasBurdenedWalk': 'E/W approved by user 2026-10-30 (v3 separate burdened walk under the Slow: rises from the kneel, slow hunched walk loop from frame 2, arms hanging, ends by sinking back to the kneel, a1de2d5d; W mirrors E); S/N to author', 'titansGaze': 'E/W approved by user 2026-10-30 (v2 goat\'s eye opens behind the caster\'s head, gaze beam off the fingertips, 91775e34; target plays titanGazed; W mirrors E); S/N to author', 'titanGazed': 'E/W approved by user 2026-10-30 (v2 horned stone titan rises behind the target, eyes snap open, stone crust creeps up the legs, loop from frame 7, 91775e34; W mirrors E); S/N to author', 'mausoleum': 'E/W approved by user 2026-10-30 (v3 seal opens a glyph ring, tomb erupts, fists hammer the capstone down, 4c2e0d3d; target plays mausoleumSealed then mausoleumBreakOut; W mirrors E); S/N to author', 'mausoleumSealed': 'E/W approved by user 2026-10-30 (v3 headstone, pillars, chest-high slab, capstone slam, pulsing Capricorn sigil loop, 4c2e0d3d; W mirrors E); S/N to author', 'mausoleumBreakOut': 'E/W approved by user 2026-10-30 (v2 slab bursts, whole tomb crumbles into rubble, a8121ea5; W mirrors E); S/N to author', 'stalactiteRain': 'E/W approved by user 2026-10-30 (v2 16-frame ultimate: crystal spears rise behind the caster, shoot up, hand hurled at the target, 127e2eb5; target plays stalactiteImpaled; W mirrors E); S/N to author', 'stalactiteImpaled': 'E/W approved by user 2026-10-30 (v2 spears rain down at a slant in two volleys, stick, shatter into rubble, 127e2eb5; W mirrors E); S/N to author', 'geodeBlast': 'E/W approved by user 2026-10-29 (v1 palm slam, glowing cracks run to the target, palm whipped up, c59bb3e6; target plays geodeBlasted; W mirrors E); S/N to author', 'geodeBlasted': 'E/W approved by user 2026-10-29 (v1 crystal spike clusters burst round the feet, shards, bleed, crumble, c59bb3e6; W mirrors E); S/N to author', 'adamantineShin': 'E/W approved by user 2026-10-29 (v1 crystal sheath grows over the shin, crystal shin kick at thigh height with crack and shard burst, 2ca22687; W mirrors E); S/N to author', 'diamondCutter': 'E/W approved by user 2026-10-29 (v1 knife hand chambered behind the head, crystal grows over hand and forearm, diagonal chop with slash and shards, 2ca22687; W mirrors E); S/N to author', 'prismaticSkin': 'E/W approved by user 2026-10-29 (v1 fists at the hips, teal aura, skin crystallises teal with facets and lingers while the buff lasts, 2ca22687; W mirrors E); S/N to author', 'silicaStrike': 'E/W approved by user 2026-10-28 (v5: kneel and scoop, uppercut rises from the crouch, heavy sand trail, burst and lingering cloud, 36955ad6; W mirrors E); S/N to author', 'flowingSandParry': 'E/W approved by user 2026-10-28 (v2 converging high/low arm circles with sand trails, 8baa93ab; W mirrors E); S/N to author', 'phantomHaunted': 'E/W approved by user 2026-10-28 (v2 12-frame loop: the phantom circles the victim behind, far side, in front, near side, then rakes, 41f294d; W mirrors E); S/N to author', 'witherPalm': 'E/W approved by user 2026-10-28 (v2 glowing palms, strike streaks, teal shock rings, dust plumes, teal aura, final burst, f45f621f; W mirrors E); S/N to author', 'coffinSyndrome': 'E/W approved by user 2026-10-28 (v2 caster: palm lifts to raise the coffin behind the target, fist snaps the lid shut, 8baa93ab; target plays coffinEntombed then coffinBreakOut; W mirrors E); S/N to author', 'coffinEntombed': 'E/W approved by user 2026-10-28 (v2 coffin rises behind the target, lid shuts, pounding loop from frame 6, 8baa93ab; W mirrors E); S/N to author', 'coffinBreakOut': 'E/W approved by user 2026-10-28 (v1 lid cracks and bursts, coffin breaks apart into planks and sand, 8baa93ab; W mirrors E); S/N to author', 'phantomPlague': 'E/W approved by user 2026-10-28 (v1 shadow pool, teal-eyed shadow creature claws up and glides at the target, 4af1f46; target plays phantomHaunted; W mirrors E); S/N to author', 'sandBurial': 'E/W approved by user 2026-10-28 (v1 caster: sand flows along the floor to the target, viewed in the two-fighter scene; W mirrors E); S/N to author', 'sandBuried': 'E/W approved by user 2026-10-28 (v2 sand climbs to the neck, squeeze loop with constriction bands while the Root lasts, e32d553; W mirrors E); S/N to author', 'sandBreakFree': 'E/W approved by user 2026-10-28 (v2 column cracks, arms burst out with a roar, sand chunks blow out, back to guard, e32d553; W mirrors E); S/N to author', 'sandstorm': 'E/W approved by user 2026-10-28 (v2 caster-centred storm zone: storm rises from the feet round the caster in its eye, blasts outward; spec extra.zone, canon A7, 3b513b51; W mirrors E); S/N to author', 'sandstormCaught': 'E/W approved by user 2026-10-28 (v2 sand gusts blowing past, forearms over the eyes, loops while inside the storm, 3b513b51; W mirrors E); S/N to author', 'oakFlesh': 'E/W approved by user 2026-10-28 (v6 honey oak bark with walnut grain over body and face, moss patches, hair turned to moss, 6d538de; W mirrors E); linger keeps the look while the buff lasts; S/N to author', 'ironFist': 'E/W approved by user 2026-10-28 (v1 Shatter Punch body, earth/crystal arm swirl, crystal-white flash, teal/brown shock ring, stone chips, 5d11ccb0; W mirrors E); S/N to author', 'rootSanctuary': 'E/W approved by user 2026-10-28 (v2 roots with root hairs rise from floor cracks and arch into a dome behind the fighter, crystal buds, fdb604b; W mirrors E); linger root ring is a proposal; S/N to author', 'ironwoodKanabo': 'E/W approved by user 2026-10-28 (v2 spiked iron kanabo rises head-first from a crack in the floor and is gripped, after Christopher\'s reference, c58ee3f; W mirrors E); kanabo weapon layer, Kanabo stance idle and weapon attacks in a separate thread; S/N to author', 'planetaryPressure': 'E/W approved by user 2026-10-28 (v1 illusory planet beside the raised hand, fist hauled down, sinking gravity waves and falling dashes, target genjutsu mark in earth colours, 6ce4904; W mirrors E); S/N to author', 'materialFixation': 'E/W approved by user 2026-10-28 (v1 illusory crystal gem offered from the palm, teal eyes, fascination waves, target genjutsu mark in earth colours, 6ce4904; W mirrors E); S/N to author', 'bullRush': 'E/W approved by user 2026-10-28 (v2 sprinter set, head-down charge with arms reaching forward, dust, shoulder ram, e1f5ef2; W mirrors E); S/N to author', 'mountainStance': 'E/W approved by user 2026-10-28 (v1 double shiko stamp, wide rooted stance, earth aura, crystal shards, a651ae52; W mirrors E); S/N to author','flowDodge': 'E/W approved by user 2026-10-28 (v1 trance sway, fire aura on the beat, purple/black wisps, 4d565a4; W mirrors E); S/N to author', 'leashKick': 'E/W approved by user 2026-10-28 (v2 double pirouette in a fire ring, axe kick finish, fea7941; W mirrors E); S/N to author', 'spinningTop': 'E/W approved by user 2026-10-28 (v1 headspin, flaming V legs, fire ring at foot height, turned-over frames via 180-degree layer turn, 68b2808; W mirrors E); S/N to author', 'wispFire': 'E/W approved by user 2026-10-28 (v1 alternating palm pushes, four purple wisps, 63b132e; W mirrors E); S/N to author', 'dogma': 'E/W approved by user 2026-10-28 (v1 fingers to the temple, looping purple motes, belief waves, target genjutsu mark, 6364f3b; W mirrors E); S/N to author', 'soulPressure': 'E/W approved by user 2026-10-28 (v1 dark spirit aura, pressing palm, sinking pressure waves, target genjutsu mark, d7b92b6; W mirrors E); S/N to author', 'cauterize': 'E/W approved by user 2026-10-27 (v1 palm seared to the ribs, fire flare with purple/black licks, smoke, d84e1d7; W mirrors E); S/N to author', 'supernova': 'E/W approved by user 2026-10-27 (v2 ultimate, 16 frames at 8 fps, long trembling build-up, swelling star, flash held 3 frames, rings, 50c8b58; W mirrors E); the S and N rows share the same S turn, S/N to author', 'spotlight': 'E/W approved by user 2026-10-27 (v3 arms lowered, forward lean, cone of light from the eyes, target genjutsu mark, 50c8b58; W mirrors E); S/N to author', 'sunPalm': 'E/W approved by user 2026-10-27 (v2 arm swirl, gathering sun, white-hot flash, fire shock ring, cracks, embers, d059a89; W mirrors E); S/N to author', 'kneel': 'E/W approved by user 2026-10-27 (v1 crown of light, commanding palm, sinking gold pressure waves, target genjutsu mark; W mirrors E); S/N to author', 'kingsPosture': 'E/W approved by user 2026-10-27 (v4 E-facing double biceps in profile, golden aura, flame mane, d4e4c1e; W mirrors E); S/N to author', 'radiance': 'E/W approved by user 2026-10-27 (v4 E-facing, fists down at the sides, erupting spiky gold aura, lingering 2 px aura + motes, d4e4c1e; W mirrors E); S/N to author', 'solarLance': 'E/W approved by user 2026-10-27 (v2 arm swirl, bigger sun, thick sparking beam, shoulder backblast, gold aura, d059a89; W mirrors E); S/N to author', 'battleRoar': 'E/W approved by user 2026-10-27 (v1 big breath, lunging roar, flame mane, golden roar waves, 733e752; W mirrors E); S/N to author', 'killingIntent': 'E/W approved by user 2026-10-27 (v3 illusory demon mask over the head matching the facing, clawed crouch, 02ce6eb; W mirrors E); S/N to author', 'blindRage': 'E/W approved by user 2026-10-27 (v1 genjutsu template: one-hand seal, eye flare, crimson aura, rage waves, 0b27675; W mirrors E); S/N to author', 'genjutsuAfflicted': 'E/W approved by user 2026-10-27 (v1 genjutsu target mark, fire colours, d75144b; W mirrors E); S/N to author', 'meteor': 'E/W approved by user 2026-10-27 (v2 ultimate, 16 frames, swelling fireball + flash + thick trail, f395d5b; W mirrors E); S/N to author', 'explosiveRunes': 'E/W approved by user 2026-10-27 (v1 sowing palm sweep + fire runes, 640aaba; W mirrors E); S/N to author', 'blastWave': 'E/W approved by user 2026-10-27 (v3 S-facing roar release, dd5ab8a; W mirrors E); the S and N rows share the same S turn, their guard frames still to review', 'innerGateAdrenaline': 'E/W approved by user 2026-10-27 (v3 lingering aura, skin flush, veins, aee3dad; W mirrors E) on condition the look lingers while the ability is active; canon A5: a toggle, active until 0 HP or deactivated; S/N to author', 'machLunge': 'E/W approved by user 2026-10-27 (v5 sprint, flaming feet, fire wake, 4 afterimages, fc741f6; W mirrors E); S/N to author', 'shatterPunch': 'E/W approved by user 2026-10-27 (v3 arm swirl + impact burst, fc741f6; W mirrors E); S/N to author'}

U.POSES += [leg('ml-dip-lead', (32, 45), (38, 51), 37), leg('ml-dip-rear', (31, 45), (29, 51), 24, wrap=54, kind='toe60'),   # sprinter dip, rear heel up
            kleg('ml-fly-lead', (33, 42), (39, 46), (38, 52), 'toe30k'), kleg('ml-fly-rear', (31, 42), (25, 47), (20, 51), 'toe30k'),   # driving off the rear foot
            leg('ml-plant-lead', (33, 43), (39, 50), 41), kleg('ml-trail-rear', (31, 43), (26, 49), (22, 54), 'toe30k'),   # lead foot lands a long step on
            leg('sp-load-lead', (32, 43), (35, 51), 36), leg('sp-load-rear', (31, 43), (28, 51), 24),                # Shatter Punch: weight sat back
            leg('sp-drive-lead', (33, 43), (38, 50), 40), leg('sp-drive-rear', (32, 43), (31, 50), 27, wrap=54, kind='toe60')]  # step in, rear heel turns up

# element palettes (letters added to universal.NPAL; W/w white stay for air and highlights)
ELEMENT = {'Y': '#ffe14d', 'O': '#ff8a1c', 'R': '#d8321a',               # fire: yellow core, orange body, red edge
           'K': '#1c1024', 'P': '#9b45ff', 'p': '#55208f',                # Sagittarius: black flame with purple
           'E': '#8a6236', 'e': '#c79a5b', 'C': '#7fe3d0', 'c': '#d9fff6',  # earth: soil browns, crystal teal / glint
           'A': '#2f7fe0', 'a': '#7cc8ff', 'I': '#dff6ff',                 # water: deep and light water, ice white-blue
           'M': '#7a1016', 'm': '#2a0406'}                                 # m: near-black blood red, the fill of the Killing Intent demon                                                 # fire genjutsu: dark crimson rim of a rage wave
NPAL.update(ELEMENT)

def _mane(r0, n, seed, front=False):   # a lion's mane of flame round the head: tongues of uneven length radiating from a ring, red tips, orange body, yellow root
    import random
    rnd = random.Random(seed); R = r0 + n + 2; g_ = [['.'] * (2 * R + 1) for _ in range(2 * R + 1)]
    for t in range(48):
        a = 2 * math.pi * t / 48; L = n + rnd.randint(-1, 2) if math.sin(a) < 0.5 else max(1, n // 2)   # the mane hangs long at the back and top, short under the chin
        if not front and math.cos(a) > 0.6 and math.sin(a) > -0.3: L = max(1, L // 2)   # short in front of the face (front: symmetric, seen face-on)
        for d in range(r0, r0 + L + 1):
            x, y = round(R + d * math.cos(a)), round(R - d * math.sin(a) * 1.1)
            if 0 <= x <= 2 * R and 0 <= y <= 2 * R:
                q = (d - r0) / max(1, L); g_[y][x] = 'Y' if q < 0.35 else 'O' if q < 0.75 else 'R'
    return [''.join(row) for row in g_]

def _sun(rad, rays=0):   # a small sun: white-hot heart, gold body, orange rim, with rays poking out of it every 45 degrees
    R = rad + rays; g_ = [['.'] * (2 * R + 1) for _ in range(2 * R + 1)]
    for y in range(-R, R + 1):
        for x in range(-R, R + 1):
            d = (x * x + y * y) ** 0.5
            if d <= rad: g_[y + R][x + R] = 'W' if d < rad * 0.4 else 'Y' if d < rad - 0.9 else 'O'
            elif rays and (x == 0 or y == 0 or abs(x) == abs(y)) and d <= R + 0.5: g_[y + R][x + R] = 'Y' if d < rad + rays / 2 else 'R'
    return [''.join(q) for q in g_]

def _halo(n, cx=35, cy=5, rx=7, ry=2, motes=3):   # motes circling over the head, a full turn every n frames: bright in front of the head, dark crimson behind
    out = []
    for k in range(n):
        pts = [('dotM', [round(cx + rx * math.cos(t)), round(cy + ry * math.sin(t)) + 1]) for t in [2 * math.pi * (j + k / n) / 16 for j in range(0, 16, 2)]]   # a faint dotted crimson ring, turning with the motes
        for m in range(motes):
            a = 2 * math.pi * (k / n + m / motes); x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
            pts.append(('moteF' if math.sin(a) > 0 else 'moteB', [round(x) - 1, round(y) + 1]))
        out.append((k, pts))
    return out

def _jag(r, w, cols):   # a jagged ')' wave of killing intent: the rage arc with every other row kicked out a pixel (it reads as a shudder, not a ripple)
    a = _arc(r, w, cols); return [('.' + q[:-1]) if i % 2 else q for i, q in enumerate(a)]

def _sag(h, d, cols, gap=1):   # a flat dome-shaped wave bearing down (the middle high, the ends low) h px either side of centre, d px deep; cols run top -> bottom
    rows = [['.'] * (2 * h + 1) for _ in range(d + len(cols))]
    for dx in range(-h, h + 1):
        if dx % gap: continue
        y = round(d * (dx / h) ** 2)
        for i, c in enumerate(cols): rows[y + i][dx + h] = c
    return [''.join(q) for q in rows]

def _arc(r, w, cols, gap=1):   # a ')' rage wave r px either side of centre, bowing w px toward the target; cols run tip -> leading edge; gap > 1 breaks it up
    rows = []
    for dy in range(-r, r + 1):
        x = round(w * (1 - (dy / r) ** 2)); row = ['.'] * (w + len(cols))
        if dy % gap == 0:
            for i, c in enumerate(cols): row[x + i] = c
        rows.append(''.join(row).rstrip('.') or '.')
    n = max(map(len, rows)); return [q.ljust(n, '.') for q in rows]
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
    'rage1': _arc(4, 2, 'RO'), 'rage2': _arc(7, 3, 'MRO'), 'rage3': _arc(10, 4, 'MRY'), 'rage4': _arc(13, 5, 'MRO'),
    'rage4d': _arc(13, 5, 'MR', gap=2), 'rage5d': _arc(15, 6, 'M', gap=3),
    'oni': ['M.................M', 'MM...............MM', '.MM.............MM.', '.MmM...MMMMM...MmM.', '..MmMMMmmmmmMMMmM..', '..MmmmmmmmmmmmmmM..', '.MmmmmmmmmmmmmmmmM.', '.MmmRRmmmmmmmRRmmM.', 'MmmmmYRmmmmmRYmmmmM', 'MmmmmmmmmmmmmmmmmmM', 'MmmmmmmmMmMmmmmmmmM', '.MmmmmmmmmmmmmmmmM.', '.MmRmRmRmRmRmRmRmM.', '.MmmRYRYRYRYRYRmmM.', '..MmmRmRmRmRmRmmM..', '...MmmmmmmmmmmmM...', '....MMmmmmmmmMM....', '......MMMMMMM......'],   # Killing Intent: a horned demon face looming behind the fighter, glowing eyes and a fanged grin
    'oniFaint': ['M.................M', 'MM...............MM', '.MM.............MM.', '.M.M...MMMMM...M.M.', '..M.MMM.....MMM.M..', '..M.............M..', '.M...............M.', '.M...............M.', 'M.................M', 'M.................M', 'M.......M.M.......M', '.M...............M.', '.M...............M.', '.M...............M.', '..M.............M..', '...M...........M...', '....MM.......MM....', '......MMMMMMM......'], 'oniEyes': ['...................', '...................', '...................', '...................', '...................', '...................', '...................', '....RR.......RR....', '.....YR.....RY.....', '...................', '...................', '...................', '...R.R.R.R.R.R.R...', '....RYRYRYRYRYR....', '.....R.R.R.R.R.....', '...................', '...................', '...................'],
    'dread': ['M..M.M..M.M', '.MmMmMmMmM.'],   # dark pressure pooling at the feet
    'oniMask': ['..R...............', '..RR..............', '...RR.............', '...RMR............', '....RMRRRRRR......', '....RmmmmmmmRR....', '...RmmmmmmmmmmR...', '...RmmmmmRRRRRmR..', '...RmmmmmmmYWYmmR.', '...RmmmmmmmmRmmmmR', '...RmmmmmmmmmmmmRR', '...RmmmmmmmmmmMR..', '...RmmmmmmmWmWmWR.', '....RmmmmmmmmmmmR.', '....RmmmmmmmWmWR..', '.....RRmmmmmmRR...', '.......RRRRRR.....'],   # Killing Intent v3: the illusory demon mask, in profile facing E (mirrored for W): horn sweeping back, brow ridge, glowing eye, snout and fangs
    'ki1': _jag(5, 2, 'MR'), 'ki2': _jag(9, 3, 'MRO'), 'ki3': _jag(13, 4, 'MRO'), 'ki4': _jag(16, 5, 'MR'),
    'mane1': _mane(7, 2, 1), 'mane2': _mane(7, 4, 2), 'mane3': _mane(7, 6, 3), 'mane3b': _mane(7, 6, 4), 'mane4': _mane(7, 7, 5),
    **{'S' + k: _mane(7, n, sd, front=True) for k, n, sd in (('mane1', 2, 1), ('mane2', 4, 2), ('mane3', 6, 3), ('mane3b', 6, 4), ('mane4', 7, 5))},
    'sunOrb1': ['.Y.', 'YWY', '.Y.'], 'sunOrb2': ['..O..', '.YWY.', 'OWWWO', '.YWY.', '..O..'],
    'lightMote': ['.Y.', 'YWY', '.O.'],   # Radiance: a mote of light drifting up off the body
    'sunOrb4': _sun(3, 3), 'sunOrb5': _sun(4, 4),
    'sunOrb3': ['...Y...', '..OYO..', '.OYWYO.', 'YYWWWYY', '.OYWYO.', '..OYO..', '...Y...'],
    'sunBurst1': ['....Y....', '.Y..Y..Y.', '..YYWYY..', '..YWWWY..', 'YYWWWWWYY', '..YWWWY..', '..YYWYY..', '.Y..Y..Y.', '....Y....'],
    'sunBurst2': ['R....O....R', '.O...Y...O.', '..Y.OYO.Y..', '...OY.YO...', '.OYY...YYO.', 'OY.......YO', '.OYY...YYO.', '...OY.YO...', '..Y.OYO.Y..', '.O...Y...O.', 'R....O....R'],
    'sunBurst3': ['R.....R.....R', '.............', '..O.......O..', '.....R.R.....', '...R.....R...', '.............', 'R...........R', '.............', '...R.....R...', '.....R.R.....', '..O.......O..', '.............', 'R.....R.....R'],
    'roar1': _arc(5, 2, 'YW'), 'roar2': _arc(9, 3, 'OYW'), 'roar3': _arc(13, 4, 'ROY'), 'roar3d': _arc(15, 5, 'RO', gap=2),
    'moteF': ['.Y.', 'YOR', '.R.'], 'moteB': ['.M.', 'MRM', '.M.'], 'dotM': ['M'],
    'eyeGlint': ['.R.', 'RYR', '.R.'], 'eyeFlare': ['..R..', '.ROR.', 'ROYWO', '.ROR.', '..R..'], 'rageWisp': ['M.R', '.R.', 'RO.'],
    'eyeGold': ['.Y.', 'YWY', '.Y.'], 'eyeGoldF': ['..O..', '.OYO.', 'OYWYO', '.OYO.', '..O..'],   # Leo genjutsu: the eyes kindle gold
    'crown1': ['....Y....', '.Y..O..Y.', '.YOYOYOY.', '.ROROROR.'], 'crown2': ['Y...Y...Y', 'YY.YOY.YY', 'YOYOYOYOY', 'OYYYYYYYO', '.ROROROR.'],
    'crown3': ['Y...W...Y', 'YY.YWY.YY', 'YOYOYOYOY', 'OYYWYWYYO', '.ROROROR.'],   # Kneel: an illusory crown of light over the head
    'press1': _sag(5, 2, 'YO'), 'press2': _sag(8, 3, 'WYO'), 'press3': _sag(11, 4, 'YOR'), 'press3d': _sag(13, 4, 'OR', gap=2),   # Kneel: golden pressure bearing down
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
PU_S = (35, -15, 1, 'up')                      # Radiance v3 (S view): fist clenched and driven down at the side, elbow bent out
KP_S, KP_S2 = (92, 182, 1, 'up'), (97, 192, 1, 'up')   # King's Posture v3 (S view): front double biceps, upper arm level out to the side, fist curled up by the head (KP_S2 the squeeze)
KP_EN, KP_EF = band(-90, -170), band(92, 172)    # King's Posture v4 (E view, no turn): double biceps in profile, near upper arm level forward and far one level back, both fists curled up by the head
KP_EN2, KP_EF2 = band(-96, -178), band(98, 178)  # the squeeze on the peak frame
FLEX_N, FLEX_F = band(50, -20), band(40, -15)     # elbows flared back, clenched fists low beside the hips (power surge)

HEAVY = load(D + 'heavyAttack.json')   # Sagittarius Leash Kick: the approved side/heel kick legs and the spinPivot pirouette
U.POSES += [{**p, 'name': 'lk-' + p['name']} for p in HEAVY['legs']['poses'] if p['name'] in ('lift', 'side-chamber', 'side', 'lead-pivot')]
NPAT.update({'pflame1': ['.K.', 'KPK', '.p.'], 'pflame2': ['..K..', '.KP..', '.PpK.', 'KPpPK', '.KKK.'],   # Sagittarius: select black and purple flames
             'pembers': ['.P..K', 'K..P.', '..p..'],
             'pwisp': ['...pP...', 'K.pPPPW.', 'KpPPWWWP', '.KpPPPW.', '...pP...'], 'pwisp2': ['K..pP...', '.KpPPPW.', 'KpPPWWWP', '..pPPPW.', 'K..pP...'],   # Wisp Fire: a small purple flame flying toward the facing, white-hot head, black tail
             'pspark': ['P.p', '.W.', 'p.P'],
             'dog1': _arc(4, 2, 'WP'), 'dog2': _arc(7, 3, 'WPp'), 'dog3': _arc(10, 3, 'PpK'), 'dog3d': _arc(12, 4, 'pK', gap=2),   # Dogma: purple waves of belief looping out
             'eyeP': ['.P.', 'PWP', '.P.'], 'eyePF': ['..p..', '.pPp.', 'pPWPp', '.pPp.', '..p..'], 'moteP': ['.P.', 'PWP', '.p.'], 'moteK': ['.p.', 'pKp', '.p.'], 'dotP': ['p'],
             'sp1': _sag(5, 2, 'Pp'), 'sp2': _sag(8, 3, 'WPp'), 'sp3': _sag(11, 4, 'PpK'), 'sp3d': _sag(13, 4, 'pK', gap=2),   # Soul Pressure: a heavy blanket of spirit bearing down
             'spWisp': ['K.p', '.p.', 'pP.'],
             'crack1': ['K.....K', '.K...K.', '.EKEKE.'], 'crack2': ['K...........K', '.KK.......KK.', '...KK.K.KK...', '....EKKKE....'],   # Taurus: cracks stamped into the floor
             'dust1': ['..e.e..', '.eEeEe.', 'eEeEeEe', '.EeEeE.'], 'dust2': ['e...e.e...e', '.e.eEeEe.e.', '..eEeEeEe..', '.eEeEeEeEe.'], 'rocks': ['K...E', '.E.K.', 'E...K'],
             'cryst': ['.c.', 'cCc', '.C.'], 'crystT': ['c', 'C', 'C'],
             'kanabo': ['...jjj...', '..jhhij..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', 'ijihjjij.', '..ihjhi..', '..ijjji..', '.jihjjiji', '..ihjhi..', '..ijjji..', '..ihjji..', '...hji...', '...ijj...', '...jhj...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...vuv...', '...uvu...', '...jhj...', '..j...j..', '..j...j..', '...jjj...'],   # Ironwood Kanabo v2 (Christopher 2026-10-28 reference): dark iron club, spike rows both sides, studs, rounded cap, tapered cone, cord-wrapped grip, ring pommel
             'smoke1': ['.g.', 'g.w', '.w.', 'w..'], 'smoke2': ['..g', '.w.', 'g..', '.w.', '..g']})   # Cauterize: a wisp of smoke off the sealed wound
U.POSES += [U.kleg('lk-axe-top', (34, 39), (38, 31), (41, 22), 'pointUR'),    # Leash Kick v2 axe kick: straight leg raised high, heel above the head
            U.kleg('lk-axe-chop', (34, 40), (41, 38), (48, 37), 'pointFwd'),   # heel chopping down through shoulder height
            U.kleg('lk-axe-down', (34, 41), (40, 46), (45, 52), 'toe30k')]     # driven down, foot about to land in front
TUCK_SPIN_N, TUCK_SPIN_F = band(-20, 212), band(-45, 222)   # arms tucked tight for the pirouette (as the Whirlwind Kick)
U.POSES += [kleg('st-vn', (33, 42), (40, 49), (46, 55), 'pointDR'), kleg('st-vf', (31, 42), (24, 49), (18, 55), 'pointDL'),   # Spinning Top (drawn upright, then turned over): legs flung wide in a V
            kleg('st-tn', (33, 42), (41, 48), (37, 41), 'pointUL'), kleg('st-tf', (31, 42), (38, 49), (33, 42), 'pointUL'),   # knees tucked (turned over: knees bent over the face, entering and leaving the spin)
            kleg('st-nn', (33, 42), (34, 50), (34, 57), 'toe30k'), kleg('st-nf', (31, 42), (30, 50), (30, 57), 'toe30k')]       # legs swept together (the V seen edge-on mid-turn)
ST_V, ST_N, ST_T = dict(ln='st-vn', lf='st-vf'), dict(ln='st-nn', lf='st-nf'), dict(ln='st-tn', lf='st-tf')
ST_AN, ST_AF = band(-135, -170), band(140, 172)   # (upright) hands up beside the head: turned over they brace on the floor by the head
def _loop(k, n=8, rx=7, ry=2, dy=-10, motes=3):   # Dogma: purple motes looping round over the head (anchored to the head), a full turn every n frames, with a faint dotted ring
    pts = [('dotP', 'head', round(rx * math.cos(t)), round(ry * math.sin(t)) + dy) for t in [2 * math.pi * (j + k / n) / 16 for j in range(0, 16, 2)]]
    for m in range(motes):
        a = 2 * math.pi * (k / n + m / motes)
        pts.append(('moteP' if math.sin(a) > 0 else 'moteK', 'head', round(rx * math.cos(a)), round(ry * math.sin(a)) + dy))
    return pts
U.POSES += [kleg('ms-lift-lead', (33, 41), (40, 36), (40, 45), 'toe30k'), kleg('ms-lift-rear', (31, 42), (36, 37), (34, 46), 'toe30k'),
            leg('ms-wide-lead', (33, 45), (40, 51), 43), leg('ms-wide-rear', (30, 45), (23, 51), 20)]   # the deep, wide rooted stance   # Mountain Stance: a knee raised high before the stamp (sumo shiko)
EARTH_RECOLOR = {'#ffe14d': '#d9fff6', '#ff8a1c': '#7fe3d0', '#d8321a': '#8a6236'}   # Taurus: fire helpers drawn in crystal glint, crystal teal and soil brown
DUST_TRAIL = {(255, 255, 255): (0xc7, 0x9a, 0x5b), (0xe3, 0xe3, 0xe3): (0x8a, 0x62, 0x36)}   # Bull Rush: motion streak recoloured to kicked-up dust
def _dustkick(p, k):   # Bull Rush: a burst of dust and grit at each sprint foot instead of flames
    at = _foot(p)
    return [(('dust2', 'dust1')[k % 2], at)] + ([('rocks', [at[0] - 6, 60])] if at[1] == 63 else [])
DUST_WAKE = [[('dust2', [12, 63]), ('dust1', [4, 62]), ('dust1', [16, 58])], [('dust1', [13, 63]), ('dust2', [5, 63]), ('rocks', [10, 56])]]
SPIN = lambda d, f: {'state': 'spinPivot', 'dir': d, 'frame': f, 'dx': 2}

NPAL.update({'T': '#3a9e8f', 'i': '#24252b', 'j': '#4a4c55', 'h': '#9a9da8', 'u': '#a08a62', 'v': '#6e5c3e'})   # i/j/h: kanabo iron (dark, mid, highlight); u/v: its cord wrap   # earth: deep crystal teal (the shaded facet of a gem)
def _dome(f, rx=21, ry=55, crystals=False):   # Root Sanctuary: two gnarled roots growing up from the floor either side and arching over the head; f = how far they have grown (1 = met overhead)
    h, w = ry + 2, 2 * rx + 9; cx, base = w // 2, ry + 1
    rows = [['.'] * w for _ in range(h)]
    def put(x, y, c):
        if 0 <= x < w and 0 <= y < h and (rows[y][x] == '.' or c in 'KC'): rows[y][x] = c
    for side in (1, -1):
        for i in range(161):
            t = i / 160 * f * math.pi / 2
            x = cx + side * round(rx * math.cos(t) + 1.6 * math.sin(t * 13)); y = base - round(ry * math.sin(t))
            put(x + side, y, 'K'); put(x, y, 'E'); put(x - side, y, 'E'); put(x - 2 * side, y, 'e')
            if i % 23 == 11: put(x - side, y, 'K')
            if i % 31 == 7: put(x - 2 * side, y, 'K')
            if i % 4 == 2 and i > 4:   # v2 (Christopher 2026-10-28: more root hairs): fine 1 px hairs fraying off both edges, alternating up and down
                up = (i // 4) % 2; ln = 2 + (i // 4) % 3
                for j in range(1, ln + 1): put(x + side * (1 + j), y - (j if up else -j) // 2 - (j > 1 and up), 'e' if j < ln else 'u')
                if i % 8 == 2:
                    for j in range(1, 3): put(x - side * (2 + j), y + j, 'e')
        for t0, ln in ((0.12, 4), (0.45, 3), (0.85, 3)):   # rootlets kicking out sideways
            if t0 <= f * math.pi / 2:
                x = cx + side * round(rx * math.cos(t0) + 1.6 * math.sin(t0 * 13)); y = base - round(ry * math.sin(t0))
                for j in range(1, ln + 1): put(x + side * j, y - j // 2, 'E')
                put(x + side * (ln + 1), y - ln // 2 - 1, 'e'); put(x + side * (ln + 1), y - ln // 2 + 1, 'e'); put(x + side * (ln - 1), y - ln // 2 + 1, 'u')   # hairs on the rootlet tips
        for j in range(1, 6): put(cx + side * (rx + 1 + j), base - (j > 3), 'E')   # roots spreading along the floor
        if crystals:
            for t0 in (0.3, 0.7, 1.1):
                x = cx + side * round(rx * math.cos(t0) + 1.6 * math.sin(t0 * 13)); y = base - round(ry * math.sin(t0))
                put(x - 2 * side, y, 'C'); put(x - 2 * side, y - 1, 'c')
    return [''.join(r) for r in rows]
SANCT_DY = -(55 + 1) / 2   # sits the dome's base row on the floor under the feet
NPAT.update({**{'sanct%d' % n: _dome(n / 100) for n in (20, 45, 70, 90)}, 'sanct100': _dome(1.0, crystals=True), 'sanctBare': _dome(1.0),
             'leafC': ['.c.', 'cCT', '.T.'],
             'eyeC': ['.C.', 'CcC', '.C.'], 'eyeCF': ['..C..', '.CcC.', 'CcWcC', '.CcC.', '..C..'],   # Taurus genjutsu: the eyes kindle crystal teal
             'gem1': ['.c.', 'cCT', '.T.'], 'gem2': ['..W..', '.cCC.', 'cCcCT', '.CCT.', '..T..'],
             'gem3': ['...W...', '..cCC..', '.cCcCC.', 'cCcWCCT', '.CCCCT.', '..CTT..', '...T...'],   # Material Fixation: an illusory crystal gem, the object of the obsession
             'glint': ['..c..', '..W..', 'cWWWc', '..W..', '..c..'], 'glit': ['c.W', '.c.', 'W.c'],
             'fix1': _arc(4, 2, 'cC'), 'fix2': _arc(7, 3, 'WcC'), 'fix3': _arc(10, 3, 'cCT'), 'fix3d': _arc(12, 4, 'CT', gap=2),
             'planet1': ['.e.', 'eEE', '.EK'], 'planet2': ['...ee....', '..eeEE...', 'CcCEEECCc', '..EEEK...', '...EK....'],
             'planet3': ['....eee....', '...eeeEE...', '..eeEEEEE..', 'cCCeEEEECCc', '..EEEEEEK..', '...EEEKK...', '....KKK....'],   # Planetary Pressure: an illusory planet, soil brown with a crystal ring
             'gp1': _sag(5, 2, 'eE'), 'gp2': _sag(8, 3, 'cCE'), 'gp3': _sag(11, 4, 'eEK'), 'gp3d': _sag(13, 4, 'EK', gap=2),
             'gline': ['e', '.', 'E', 'E', '.', 'K']})   # gravity: dashes falling on the target

NPAL.update({'S': '#e6c27a', 's': '#9c7434', 'Z': '#fff0c4'})   # Virgo: sand (body, shade, sunlit grain)
def _sandcloud(w, h, dens, seed, cone=False):   # a cloud of sand grains: dense sandy core, dark grains thinning out to the edge; cone: a fan opening toward the facing
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            dx, dy = (x - (w - 1) / 2) / (w / 2), (y - (h - 1) / 2) / (h / 2)
            if cone: dx, dy = x / w, abs(dy) / max(0.15, x / w)
            d = (dx * dx + dy * dy) ** 0.5 if not cone else dy
            if d < 1 and rnd.random() < dens * (1.2 - d):
                rows[y][x] = 'Z' if d < 0.35 and rnd.random() < 0.4 else 'S' if d < 0.65 else 's'
    return [''.join(r) for r in rows]
NPAT.update({'sandH': ['.S.', 'SsS', '.s.'], 'sandTrk': ['S', 's', '.', 'S', '.', 's', '.', '.', 'S'], 'sandPuff': ['..s.Z..s', '.sSsSsS.', 'sSsZsSsS', 'ssSSSSss'],   # Virgo: a fistful of sand, grains trickling, sand scooped off the floor
             'sandSpray': _sandcloud(9, 9, 0.8, 1, cone=True), 'sandBurst': _sandcloud(11, 13, 0.85, 2), 'sandCloud': _sandcloud(13, 17, 0.6, 3), 'sandCloud2': _sandcloud(13, 19, 0.35, 4),   # Silica Strike: sand flung into the face, bursting and drifting
             'hglass': ['vvvvvvvvv', '.c.....c.', '.cZSSSSc.', '..cSSSc..', '...cSc...', '....S....', '...c.c...', '..c.S.c..', '.c..S..c.', '.c.SSS.c.', 'vvvvvvvvv'],
             'hglass2': ['vvvvvvvvv', '.c.....c.', '.c.....c.', '..cZSSc..', '...cSc...', '....S....', '...cSc...', '..c.S.c..', '.c.SSS.c.', '.cSSSSSc.', 'vvvvvvvvv'],   # Flowing Sand Parry: an illusory hourglass beside the head, sand running through it
             'grains': ['Z...S', '..s..', 'S...Z'], 'sandArc': _arc(5, 2, 'sSZ'), 'sandArc2': _arc(7, 3, 'sS', gap=2),
             'vital': ['..c..', '.cWc.', 'cWWWc', '.cWc.', '..c..'], 'vital2': ['c...c...c', '.c..c..c.', '..cCWCc..', '..CWWWC..', 'ccWWWWWcc', '..CWWWC..', '..cCWCc..', '.c..c..c.', 'c...c...c'], 'wither': ['v.u', '.v.', 'u.v'], 'wither2': ['u..v.', '.v..u', 'v.u..', '..v.u']})   # Wither Palm: a teal flash at each vital point struck, dull dust of the strength draining out

def _whirl(h, r0, r1, phase, seed, arms=3, shards=0):   # Sandstorm: a sand tornado h px tall, r0 wide at the foot opening to r1 at the top, streaks spiralling round it;
    import random                                        # returns (front, back): the front half is drawn over the fighter, the back half only where it is not drawn
    rnd = random.Random(seed); w = 2 * r1 + 3; cx = r1 + 1
    fr = [['.'] * w for _ in range(h + 4)]; bk = [['.'] * w for _ in range(h + 4)]
    for y in range(h):
        t = 1 - y / max(1, h - 1); rx = r0 + (r1 - r0) * t; ry = max(1.0, rx * 0.2)
        for j in range(arms):
            for u in range(7):
                if y % 2 and arms == 2 and h > 20: continue   # the big storm: every other row, so the fighter shows through
                a = phase + y * 0.3 + j * 2 * math.pi / arms + u * 0.13
                X = round(cx + rx * math.cos(a)); Y = round(y + 2 + ry * math.sin(a))
                if not (0 <= X < w and 0 <= Y < h + 4) or rnd.random() < 0.25: continue
                front = math.sin(a) > 0
                c = ('Z' if u > 4 else 'S' if u > 1 else 's') if front else ('S' if u > 4 else 's')
                (fr if front else bk)[Y][X] = c
    for _ in range(shards):   # shrapnel caught in the storm: crystal chips and grit
        a = rnd.random() * 2 * math.pi; y = rnd.randint(2, h - 2); rx = r0 + (r1 - r0) * (1 - y / h)
        X = round(cx + rx * math.cos(a)); Y = round(y + 2 + rx * 0.2 * math.sin(a))
        if 0 <= X < w and 0 <= Y < h + 4: (fr if math.sin(a) > 0 else bk)[Y][X] = rnd.choice('CcK')
    return [''.join(r) for r in fr], [''.join(r) for r in bk]

def _mound(hgt, w=26, seed=0, coffin=False):   # Sand Burial: a heap of sand round the legs, hgt px high; coffin: closed up over the chest, with darker squeeze bands
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(hgt)]
    for y in range(hgt):
        f = y / max(1, hgt - 1); half = (w / 2) * (0.55 + 0.45 * f) if not coffin else (w / 2) * (0.3 + 0.7 * math.sin(min(1, 0.25 + f) * math.pi / 2) ** 0.5)   # coffin: a rounded dome closing over the shoulders
        for x in range(w):
            if abs(x - (w - 1) / 2) <= half - (rnd.random() < 0.5 and y < 2):
                edge = abs(x - (w - 1) / 2) > half - 1.5 or y == 0
                rows[y][x] = 's' if edge else ('Z' if rnd.random() < 0.08 else 's' if rnd.random() < 0.18 or (coffin and (y + abs(x - w // 2) // 3) % 7 == 3) else 'S')
    return [''.join(r) for r in rows]
NPAT.update({**{'mound%d' % n: _mound(n, seed=n) for n in (6, 14, 18)}, 'coffin26': _mound(26, w=28, seed=26, coffin=True), 'coffin30': _mound(30, w=28, seed=30, coffin=True),
             **{'storm%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(52, 6, 18, k * math.pi / 2, k, arms=2, shards=8))},
             **{'whirl%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(12, 3, 7, k * math.pi / 2, 10 + k, arms=2))},
             'sandStream': ['..s..S..s.Z..S', '.SsS.sSs.SsS.s', 'sSsSsSsSsSsSsS'], 'sandRise': ['.S.s', 's.Z.', '.S.s', 'S..s']})   # Sand Burial: sand flowing along the floor toward the target, sand rising

def _gust(w, h, phase, seed, n=9):   # Sandstorm v2 target: streaks of sand blowing across the fighter; returns (front, back)
    import random
    rnd = random.Random(seed); fr = [['.'] * w for _ in range(h)]; bk = [['.'] * w for _ in range(h)]
    for i in range(n):
        y = rnd.randint(1, h - 2); L = rnd.randint(4, 9); x0 = (rnd.randint(0, w - 1) + phase * 9) % w; q = fr if i % 2 == 0 else bk
        for u in range(L):
            X = (x0 + u) % w; Y = y + (1 if u > L // 2 and i % 3 == 0 else 0)
            q[min(h - 1, Y)][X] = 'Z' if u == L - 1 else 'S' if u > L // 3 else 's'
            if i % 2 == 0 and 0 < u < L - 1: q[min(h - 1, Y + 1)][X] = 's'
    for _ in range(3):
        y = rnd.randint(2, h - 3); x = (rnd.randint(0, w - 1) + phase * 9) % w; (fr if rnd.random() < 0.5 else bk)[y][x] = rnd.choice('CcK')
    return [''.join(r) for r in fr], [''.join(r) for r in bk]
NPAT.update({**{'eye%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(50, 15, 22, k * math.pi / 2, 30 + k, arms=4, shards=14))},   # Sandstorm v2: the storm round the caster, wide at the foot so the fighter stands in its eye
             **{'eyeMid%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(30, 15, 19, k * math.pi / 2, 40 + k, arms=4, shards=6))},
             **{'eyeLow%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _whirl(12, 14, 16, k * math.pi / 2, 50 + k, arms=3))},
             **{'gust%d%s' % (k, fb): q for k in range(4) for fb, q in zip('FB', _gust(34, 40, k, 60 + k, n=18))},
             'stormRing': _whirl(12, 14, 16, 0, 50, arms=2)[0], 'sandSprayL': [r[::-1] for r in NPAT['sandSpray']]})
U.POSES += [leg('ss-kneel-lead', (33, 50), (41, 49), 42), U.kleg('ss-kneel-rear', (31, 50), (29, 55), (20, 55), 'toe30k')]   # Silica Strike v2: down on the rear knee, lead foot flat in front, thigh level
U.POSES += [kleg('ar-lift-lead', (33, 44), (37, 49), (38, 54), 'toe30k'), leg('ar-plant-lead', (33, 45), (38, 51), 41),   # Burdened by the World v2: a dragging step, the lead foot barely lifts
            leg('ar-plant-rear', (31, 45), (29, 51), 26), kleg('ar-drag-rear', (31, 45), (28, 51), (24, 55), 'toe30k'),   # rear foot hauled up on its toes
            leg('ar-buckle-lead', (33, 47), (39, 51), 40), leg('ar-buckle-rear', (31, 47), (29, 53), 25)]   # the knees give
def _aw(k, hx):   # Burdened Walk: one leg's pose at walk frame k (0 heel strike, 1-3 loaded and sliding back 3 px a frame, 4 toe dragging behind, 5-7 swinging low past and forward); hips sunk 3 px
    hip = (hx, 45)
    return [leg(None, hip, (hx + 4, 51), hx + 6), leg(None, hip, (hx + 2, 51), hx + 3), leg(None, hip, (hx, 51), hx), leg(None, hip, (hx - 2, 51), hx - 4, wrap=54, kind='toe60'),
            kleg(None, hip, (hx - 3, 51), (hx - 7, 57), 'toe30k'), kleg(None, hip, (hx, 50), (hx - 2, 56), 'toe30k'), kleg(None, hip, (hx + 4, 49), (hx + 3, 55), 'toe30k'), kleg(None, hip, (hx + 6, 50), (hx + 6, 56), 'toe30k')][k]
for k_ in range(8):
    U.POSES += [{**_aw(k_, 31), 'name': 'aw-%d-near' % k_}, {**_aw(k_, 33), 'name': 'aw-%d-far' % k_}]
U.POSES += [kleg('gs-back-rear', (31, 50), (24, 55), (16, 57), 'toe30k'), kleg('gs-mid-rear', (31, 50), (34, 54), (37, 56), 'pointFwd'),   # Gemini Sonic Sweep: the rear leg stretched behind along the floor, swinging under,
            kleg('gs-front-rear', (31, 50), (40, 55), (49, 57), 'pointFwd'), leg('gs-crouch-lead', (33, 50), (40, 49), 41)]
U.POSES += [kleg('gs-far-rear', (31, 50), (41, 54), (51, 55), 'pointFwd'), kleg('gs-wide-rear', (31, 50), (22, 54), (13, 57), 'toe30k'),   # Sonic Sweep v2: follow-through past the target's ankles, and the long load behind
            kleg('sw-up-lead', (33, 43), (39, 45), (45, 47), 'pointFwd'), kleg('sw-up-rear', (31, 43), (36, 46), (42, 49), 'pointFwd'),   # Sonic Swept: both feet knocked out forward from under the fighter
            kleg('sw-hi-lead', (33, 43), (39, 41), (45, 39), 'pointUR'), kleg('sw-hi-rear', (31, 43), (37, 43), (43, 42), 'pointFwd')]                  # then sweeping out flat in front; crouched on the lead foot
LC_RUN = band(-15, -40, fistKind='palm')   # Lightning Cutter v3: the bladed knife hand carried low by the hip through the sprint
LC_RISE, LC_CUT = band(-25, -70, fistKind='palm'), band(-55, -125, fistKind='palm')   # v3: the uppercut rising, then driven up into the body
AR_SWAY_N, AR_SWAY_F = band(12, -4), band(-4, -8)   # Burdened Walk: the limp arms swing a little with the stride
AR_HANG_N, AR_HANG_F = band(6, -4), band(2, -6)        # arms hanging limp at the sides
AR_KNEEL_N, AR_KNEEL_F = band(10, 0), band(4, -4)
NPAT.update({'sandSprayUp': [''.join(r[y] for r in NPAT['sandSpray'][::-1]) for y in range(len(NPAT['sandSpray'][0]))][::-1]})
def _ring(r, ch='c', ch2='C', gap=0):   # Wither Palm v2: a thin shock ring of radius r (flattened a little), every other pixel when gap
    w = 2 * r + 1; h = 2 * round(r * 0.8) + 1; rows = [['.'] * w for _ in range(h)]
    for k in range(int(8 * r)):
        a = 2 * math.pi * k / (8 * r); x = round(r + r * math.cos(a)); y = round((h - 1) / 2 + (h - 1) / 2 * math.sin(a))
        if gap and k % 2: continue
        rows[y][x] = ch if math.sin(a) < 0.3 else ch2
    return [''.join(q) for q in rows]
NPAT.update({'palmGlow': ['..ccc..', '.cC.Cc.', 'cC...Cc', 'c.....c', 'cC...Cc', '.cC.Cc.', '..ccc..'], 'streak': ['CCcc.c..c', '.ccc.c...'], 'vRing': _ring(5), 'vRing2': _ring(7), 'vRing3': _ring(9, gap=1),
             'witherPlume': ['..u.v..', '.uvuvu.', 'vuuvvuv', '.vuvuv.', '..v.u..', '...u...', '..v....'], 'witherBurst': ['u...v...u', '.vu.u.uv.', 'u.vuvuv.u', '.uvvuvvu.', 'vuuvuvuuv', '.uvvuvvu.', 'u.vuvuv.u', '.vu.v.uv.', 'u...u...v']})   # Wither Palm v2: palm glow, strike streak, dust plumes
def _coffin(w, h, seed, lid=False, crack=0):   # Coffin Syndrome v2: an upright coffin, a box of packed sand outlined in crystal teal; lid: the front lid (a darker seam band, two teal studs); crack: 1-2 crack lines across the lid
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        sh = 0.62 + 0.38 * min(1, y / (h * 0.22)) if y < h * 0.22 else 1 - 0.3 * (y - h * 0.22) / (h * 0.78)   # wide at the shoulders, tapering to the foot
        half = (w - 1) / 2 * sh
        for x in range(w):
            dx = abs(x - (w - 1) / 2)
            if dx > half: continue
            edge = dx > half - 1 or y in (0, h - 1)
            rows[y][x] = 'C' if edge else ('c' if edge and rnd.random() < 0.2 else 'Z' if rnd.random() < 0.06 else 's' if rnd.random() < 0.25 else 'S')
            if lid and not edge and (abs(dx - half + 3) < 0.6 or y in (3, h - 4)): rows[y][x] = 's'
    if lid:
        for y in (h // 4, 3 * h // 4): rows[y][w // 2] = 'c'
    for c_ in range(crack):   # cracks zigzagging across the lid
        y0 = h // 3 + c_ * h // 4; x = 2
        while x < w - 2:
            if rows[y0][x] != '.': rows[y0][x] = 'K'
            x += 1; y0 += rnd.choice((-1, 0, 1)) if 2 < y0 < h - 3 else 0
    return [''.join(r) for r in rows]
def _squash(pat, w):   # the lid seen swinging round on its hinge: the same lid squeezed to w columns
    W = len(pat[0]); return [''.join(r[min(W - 1, int(x * W / w))] for x in range(w)) for r in pat]
NPAT.update({'cofBack': _coffin(32, 56, 1), 'cofLid': _coffin(32, 56, 2, lid=True), 'cofLidCrack': _coffin(32, 56, 2, lid=True, crack=1), 'cofLidCrack2': _coffin(32, 56, 2, lid=True, crack=2)})
NPAT.update({'cofLid1': _squash(NPAT['cofLid'], 9), 'cofLid2': _squash(NPAT['cofLid'], 20), 'cofBackLow': _coffin(32, 56, 1)[14:], 'cofBackLow2': _coffin(32, 56, 1)[30:],
             'plank': ['CCCCCCC', 'CsSsSsC', 'CCCCCCC'], 'plankV': ['CCC', 'CSC', 'CsC', 'CSC', 'CsC', 'CCC']})
NPAL.update({'X': '#120d16', 'x': '#3a2f40'})   # Virgo genjutsu: the phantom's shadow (near-black, smoky edge)
def _scale(pat, f):   # nearest-neighbour enlargement of a pattern by f (Virgo genjutsu v1: the phantom and the coffin drawn bigger)
    h, w = len(pat), len(pat[0]); H, W = round(h * f), round(w * f)
    return [''.join(pat[min(h - 1, int(y / f))][min(w - 1, int(x / f))] for x in range(W)) for y in range(H)]
NPAT.update({'wraith0': ['....xxxx.....', '...xXXXXx....', '..xXXXXXXx...', '..xXXCXCXx...', '..xXXXXXXXx..', '...xXXXXXXXx.', '..xXXXXXXXXXx', '.xXXXXXXX.xXX', '.xXXXXXXX...X', 'xXXXXXXXx....', 'xXXXXXXXx....', '.xXXXXXXx....', '.xXXXXXx.....', '..xXXXXx.....', '..xXXXx......', '...xXx.x.....', '...x.x..x....', '....x........'],   # Phantom Plague: a hunched shadow creature with teal eyes, a clawed arm reaching forward, a wispy tail
             'wraithRise': ['....xxxx.....', '...xXXXXx....', '..xXXXXXXx...', '..xXXCXCXx...', '..xXXXXXXXx..', '...xXXXXXXXx.', '..xXXXXXXXXXx', '.xXXXXXXX.xXX', '.xXXXXXXX...X'], 'shadowPool': ['..xxxxxxx..', '.xXXXXXXXx.', 'xXXXXXXXXXx', '.xxXXXXXxx.'], 'shadowPool2': ['....xxxxx....', '.xxXXXXXXXxx.', 'xXXXXXXXXXXXx', '.xxXXXXXXXxx.'],
             'coffinUp': ['..CCC..', '.CsssC.', 'CsssssC', 'CssWssC', 'CsWWWsC', 'CssWssC', 'CsssssC', 'CsssssC', 'CsssssC', '.CsssC.', '.CsssC.', '.CsssC.', '..CsC..', '..CCC..'],   # Coffin Syndrome: an illusory coffin (crystal-teal outline, sand), standing, then slammed flat
             'coffinFlat': ['..CCCCCCCCCC...', '.CsssWsssssssC.', 'CsssWWWsssssssC', '.CsssWsssssssC.', '..CCCCCCCCCC...'],
             'cs1': _sag(5, 2, 'Ss'), 'cs2': _sag(8, 3, 'ZSs'), 'cs3': _sag(11, 4, 'SsK'), 'cs3d': _sag(13, 4, 'sK', gap=2)})   # Coffin Syndrome: sand pressure bearing down on the buried
NPAT.update({'wraith': _scale(NPAT['wraith0'], 1.6), 'wraithRise': _scale(NPAT['wraithRise'], 1.6), 'coffinUp': _scale(NPAT['coffinUp'], 1.5), 'coffinFlat': _scale(NPAT['coffinFlat'], 1.4)})
NPAT.update({'sandBurstL': _sandcloud(15, 17, 0.85, 5), 'sandCloudL': _sandcloud(17, 21, 0.6, 6), 'sandCloudL2': _sandcloud(17, 23, 0.35, 7), 'sandSprayUpL': _scale(NPAT['sandSprayUp'], 1.5), 'sandSprayL2': _scale(NPAT['sandSpray'], 1.4)})   # Silica Strike v5 (Christopher 19:28: more fx): bigger burst, cloud and spray
U.POSES += [kleg('as-lift', (34, 41), (39, 45), (37, 52), 'toe30k'), kleg('as-chamber', (34, 40), (41, 38), (39, 46), 'toe30k'),   # Capricorn Adamantine Shin: knee lifted, then chambered high
            kleg('as-kick', (34, 41), (42, 44), (51, 45), 'pointFwd'), kleg('as-kick2', (34, 41), (42, 45), (52, 47), 'pointFwd'),     # the shin swung through level at the opponent's thigh, then driving through
            kleg('as-recoil', (34, 41), (39, 46), (35, 52), 'toe30k')]
AS_SEG = {'as-lift': ((39, 45), (37, 52)), 'as-chamber': ((41, 38), (39, 46)), 'as-kick': ((42, 44), (51, 45)), 'as-kick2': ((42, 45), (52, 47)), 'as-recoil': ((39, 46), (35, 52))}   # E knee -> ankle of each kick pose (crystal sheath)
def _spikes(w, h, n, seed, lean=0, widths=(3, 4, 5)):   # Capricorn Geode Blast: a cluster of n crystal spikes erupting from the floor, w wide, the tallest h high: each spike a pointed prism, glint c on its lit (left) face, body C, deep teal T on its shaded face and outline
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for i in range(n):
        sw = rnd.choice(widths); sh = max(4, round(h * rnd.uniform(0.45, 1.0)) if i else h); x0 = round((w - sw) * (i + 0.5) / n + rnd.uniform(-1.5, 1.5)); x0 = max(0, min(w - sw, x0))
        tip = sw // 2
        for yy in range(sh):
            y = h - 1 - yy; f = yy / max(1, sh - 1); shift = round(lean * f * 2)
            half = sw / 2 if f < 0.7 else (sw / 2) * (1 - f) / 0.3 + 0.5
            for xx in range(sw):
                if abs(xx + 0.5 - sw / 2) > half: continue
                X = x0 + xx + shift
                if not 0 <= X < w: continue
                edge = xx == 0 or xx == sw - 1 or abs(xx + 0.5 - sw / 2) > half - 1
                rows[y][X] = 'T' if (edge and xx >= tip) or xx > tip else 'c' if xx < tip and (edge or yy % 4 == 1) else 'C'
    return [''.join(q) for q in rows]
NPAT.update({'geoBack': _spikes(34, 30, 6, 11), 'geoFrontL': _spikes(16, 22, 3, 12, lean=-1), 'geoFrontR': _spikes(16, 24, 3, 15, lean=1), 'geoSmall': _spikes(24, 10, 5, 13), 'geoSmallB': _spikes(28, 12, 5, 14),
             'geoBack2': _spikes(34, 30, 6, 11)[10:], 'geoFrontL2': _spikes(16, 22, 3, 12, lean=-1)[8:], 'geoFrontR2': _spikes(16, 24, 3, 15, lean=1)[8:], 'rubble': ['..T.c..T..', '.TCcT.cCT.', 'TCcCTTCcCT'],
             'bloodN': ['M.', '.m', 'M.'], 'shardFly': ['c...T', '.C.C.', 'T...c'],
             'crackGlow': ['C.....C', '.C...C.', '.cCcCc.'], 'crackRun': ['C.........K', '.KC....K.C.', '...KCKC.K..']})
NPAL.update({'G': '#8c8478', 'H': '#b3aa9a', 'N': '#544c42'})   # Capricorn Mausoleum: tomb stone (mid, lit, dark mortar)
def _slab(w, h, seed, arch=False, seam=True):   # Mausoleum: a wall of dressed stone blocks w x h (courses 6 px high, joints staggered), lit top/left edge H, dark right edge and mortar N, a crystal-teal seam glowing in one joint; arch: the top rounded like a tomb's headstone
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    seamRow = rnd.randrange(6, max(7, h - 4), 6) if seam and h > 8 else -1
    for y in range(h):
        for x in range(w):
            if arch:
                r = w / 2; top = r - math.sqrt(max(0, r * r - (x + 0.5 - r) ** 2))
                if y < top * 0.6: continue
            course = y // 6; jx = (x + (3 if course % 2 else 0) + seed) % 9
            ch = 'G'
            if y % 6 == 5 or jx == 0: ch = 'N'
            if (x + y * 3 + seed) % 11 == 0: ch = 'H' if ch == 'G' else ch
            if x == 0 or (arch and y < 3) or y == 0: ch = 'H'
            if x == w - 1: ch = 'N'
            if y == seamRow and 0 < x < w - 1: ch = 'C' if x % 3 else 'c'
            rows[y][x] = ch
    return [''.join(q) for q in rows]
def _pillar(w, h, seed):   # Mausoleum v2: a fluted stone pillar w wide, h high, with a wider capital and base (2 px each side), lit left edge H, dark right edge N, a crystal-teal seam ringing it a third of the way up
    rows = []
    for y in range(h):
        if y < 3 or y >= h - 3: rows.append('H' + 'G' * (w + 2) + 'N' if y in (0, h - 3) else 'H' + ''.join('N' if (x + seed) % 5 == 0 else 'G' for x in range(w + 2)) + 'N'); continue
        mid = ''.join('N' if x % 3 == 2 else 'H' if x % 3 == 0 and (y + seed) % 7 else 'G' for x in range(w - 2))
        if y == round(h * 0.66): mid = ''.join('C' if x % 2 else 'c' for x in range(w - 2))
        rows.append('.' + 'H' + mid + 'N' + '.')
    return rows
def _roof(w, h):   # Mausoleum v2: the roof slab dropped on the pillars: a low pediment (triangle) over a thick lintel, crystal-teal seam along the lintel
    rows = []
    for y in range(h):
        if y < h - 5:
            half = round((w / 2) * (y + 1) / (h - 5)); row = ['.'] * w
            for x in range(w // 2 - half, w // 2 + half): row[x] = 'H' if x < w // 2 else 'G'
            if half: row[w // 2 - half] = 'H'; row[min(w - 1, w // 2 + half - 1)] = 'N'
            rows.append(''.join(row))
        else:
            yy = y - (h - 5); rows.append('N' * w if yy in (0, 4) else ''.join('C' if x % 3 else 'c' for x in range(w)) if yy == 2 else 'H' + 'G' * (w - 2) + 'N')
    return rows
NPAT.update({'pillar': _pillar(7, 55, 1), 'roof': _roof(40, 9)})
NPAT.update({**{'pillar%d' % n: NPAT['pillar'][-round(55 * n / 3):] for n in (1, 2)}})
def _runes(w, h, lit):   # Mausoleum v3: carved glyphs over the front slab, glowing crystal teal (lit: white-hot cores) or dim deep teal between pulses
    G = [['C.C', '.C.', 'C.C'], ['CCC', 'C..', 'CCC'], ['.C.', 'CCC', '.C.'], ['C.C', 'CCC', 'C.C'], ['CC.', '.C.', '.CC'], ['C..', 'CCC', '..C']]
    rows = [['.'] * w for _ in range(h)]; k = 0
    for gy in range(4, h - 4, 7):
        for gx in range(3, w - 4, 7):
            for yy, r in enumerate(G[k % len(G)]):
                for xx, ch in enumerate(r):
                    if ch != '.': rows[gy + yy][gx + xx] = ('W' if (xx, yy) == (1, 1) else 'c') if lit else 'T'
            k += 1
    return [''.join(q) for q in rows]
def _runering(w, h, lit):   # Mausoleum v3: a ring of glowing glyph ticks opening in the floor under the target
    rows = [['.'] * w for _ in range(h)]
    for k in range(int(4 * w)):
        a = 2 * math.pi * k / (4 * w); x = round((w - 1) / 2 + (w - 1) / 2 * math.cos(a)); y = round((h - 1) / 2 + (h - 1) / 2 * math.sin(a))
        rows[y][x] = 'C' if lit else 'T'
    for k in range(10):
        a = 2 * math.pi * k / 10; x = round((w - 1) / 2 + (w - 1) / 2 * 0.7 * math.cos(a)); y = round((h - 1) / 2 + (h - 1) / 2 * 0.6 * math.sin(a))
        rows[y][x] = 'W' if lit else 'c'
    return [''.join(q) for q in rows]
def _plume(w, h, seed):   # Mausoleum v3: a plume of stone dust (the sand cloud in earth browns and stone)
    return [r.replace('Z', 'H').replace('S', 'e').replace('s', 'E') for r in _sandcloud(w, h, 0.7, seed)]
NPAT.update({'tombSlab': _slab(26, 36, 9, seam=False), 'runesLit': _runes(26, 36, True), 'runesDim': _runes(26, 36, False), 'roofBig': _roof(46, 10),
             'ringLit': _runering(36, 7, True), 'ringDim': _runering(36, 7, False), 'plume': _plume(15, 13, 31), 'plume2': _plume(19, 15, 32), 'plumeWide': _plume(31, 11, 33)})
NPAT.update({'tombSlab1': NPAT['tombSlab'][-12:], 'tombSlab2': NPAT['tombSlab'][-24:], 'runesLit2': NPAT['runesLit'][-24:]})
def _sigil(r, lit):   # Mausoleum v3: a big carved sigil on the front slab: a ring with the goat-fish glyph of Capricorn inside (a V whose right arm curls into a hook), glowing crystal teal (lit: white-hot glyph)
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]; ring, glyph = ('c', 'W') if lit else ('T', 'C')
    for k in range(int(8 * r)):
        a = 2 * math.pi * k / (8 * r); rows[round(r + r * math.sin(a))][round(r + r * math.cos(a))] = ring
    pts = [(-4, -4), (-3, -2), (-2, 0), (-1, 2), (0, 3), (1, 1), (1, -1), (2, -3), (3, -3), (4, -2), (4, 0), (3, 2), (2, 3), (3, 4)]
    for (x, y) in pts:
        rows[r + y][r + x] = glyph
        if lit: rows[r + y][r + x + 1] = rows[r + y][r + x + 1] if rows[r + y][r + x + 1] != '.' else 'c'
    return [''.join(q) for q in rows]
NPAT.update({'sigilLit': _sigil(9, True), 'sigilDim': _sigil(9, False), 'slabGlow': [''.join('C' if ch == 'N' else '.' for ch in r) for r in NPAT['tombSlab']], 'lightBeam': ['c', 'C', 'c', 'c', '.', 'c', 'C', 'c', '.', 'c'] * 4})
def _globe(r, phase=0):   # Atlas's Regret: the illusory world on the target's shoulders: a soil-brown sphere with teal crystal seas, latitude and longitude lines in glint, a teal rim; phase turns it
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for y in range(w):
        for x in range(w):
            dx, dy = (x - r) / r, (y - r) / r; d = dx * dx + dy * dy
            if d > 1: continue
            if d > 0.8: rows[y][x] = 'C'; continue
            lon = math.asin(max(-1, min(1, dx / math.sqrt(max(1e-6, 1 - dy * dy))))) + phase
            sea = math.sin(lon * 2.3 + dy * 3) + math.cos(dy * 4.1 - lon) > 0.6
            ch = 'T' if sea else 'e' if dx < 0.2 else 'E'
            if abs(dy * r) % 5 < 0.6 or abs((lon * 6) % 3.2) < 0.25: ch = 'c'
            rows[y][x] = ch
    return [''.join(q) for q in rows]
def _titan(w, h, lit):   # Titan's Gaze: the looming face of a stone giant behind the target: a broad oval face of weathered stone (lit left, shaded right) with a heavy brow ridge, cracks, a nose ridge and a grim mouth line, two huge eyes blazing crystal teal (lit: white-hot cores)
    import random
    rnd = random.Random(7); rows = [['.'] * w for _ in range(h)]; cx, cy = (w - 1) / 2, (h - 1) / 2
    for y in range(h):
        for x in range(w):
            dx, dy = (x - cx) / (w / 2), (y - cy) / (h / 2)
            if dx * dx + dy * dy * (1.0 if dy < 0 else 0.8) > 1: continue
            edge = dx * dx + dy * dy * (1.0 if dy < 0 else 0.8) > 0.86
            rows[y][x] = 'N' if edge else 'H' if dx < -0.45 and (x + y) % 3 else 'N' if dx > 0.5 and (x + y) % 2 else 'G'
    by = round(h * 0.34)
    for x in range(round(w * 0.12), round(w * 0.88)):
        yy = by + round(2 * abs(x - cx) / (w / 2)); rows[yy][x] = 'N'; rows[yy - 1][x] = 'H'
    for ex in (round(w * 0.3), round(w * 0.7)):
        ey = by + 4
        for y in range(ey - 3, ey + 4):
            for x in range(ex - 7, ex + 8):
                dx, dy = (x - ex) / 7, (y - ey) / 3.2; d = dx * dx + dy * dy
                if d <= 1: rows[y][x] = ('W' if lit else 'c') if d < 0.22 else 'c' if d < 0.5 else 'C'
                elif d <= 1.45: rows[y][x] = 'T'
    for y in range(by + 6, round(h * 0.72)): rows[y][round(cx) - 1] = 'H'; rows[y][round(cx) + 1] = 'N'
    my = round(h * 0.8)
    for x in range(round(w * 0.36), round(w * 0.64)): rows[my + (1 if abs(x - cx) > w * 0.1 else 0)][x] = 'N'
    for _ in range(9):
        x, y = rnd.randrange(w), rnd.randrange(h)
        for t in range(rnd.randint(3, 7)):
            if 0 <= x < w and 0 <= y < h and rows[y][x] in 'GH': rows[y][x] = 'N'
            x += rnd.choice((-1, 0, 1)); y += 1
    return [''.join(q) for q in rows]
def _titan2(lit, eyes='open', seams=False):   # Titan's Gaze v2 (Christopher 2026-10-30: "needs more cool"): the head of a horned stone titan (Capricorn's goat) behind the target:
    import random                             # an angular face of weathered stone lit from the left, a scowling V brow, slit eyes blazing crystal teal with a goat's bar pupil, ram horns curling round to the sides, cracks that glow teal (seams)
    W, H = 62, 46; rnd = random.Random(11); rows = [['.'] * W for _ in range(H)]; cx = 30.5
    def put(x, y, ch):
        if 0 <= x < W and 0 <= y < H: rows[y][x] = ch
    for side in (-1, 1):   # ram horns: from the forehead corner they sweep back and out, curl down round the side and forward under themselves
        ox, oy = cx + side * 21, 15
        for i in range(0, 260):
            t = i / 259; a = math.radians(-115 + 360 * t); r = 10.5 - 6.0 * t; th = 6.0 - 3.6 * t
            px, py = ox + side * r * math.cos(a), oy + r * math.sin(a)
            for j in range(-6, 7):
                o = j / 6 * th / 2; qx, qy = round(px + side * o * math.cos(a)), round(py + o * math.sin(a))
                ridge = int(t * 26) % 2
                put(qx, qy, 'N' if abs(o) > th / 2 - 0.6 else ('H' if o < 0 else 'G') if not ridge else 'G' if o < 0 else 'N')
    def half(y):
        if y < 3: return 0
        if y < 9: return 12 + (y - 3) * 1.1
        if y < 30: return 18.5
        return max(6, 18.5 - (y - 30) * 0.85)
    for y in range(H):
        hw = half(y)
        for x in range(W):
            dx = x - cx
            if abs(dx) > hw: continue
            edge = abs(dx) > hw - 1.2 or y == 3 or y == H - 1
            rows[y][x] = 'N' if edge else ('H' if (x + y) % 3 else 'G') if dx < -8 else ('N' if (x + y) % 2 else 'G') if dx > 9 else 'G'
    for x in range(W):   # scowling V brow ridge, low in the middle
        dx = abs(x - cx)
        if dx > 17: continue
        by = 12 + round(5 * (1 - dx / 17) ** 1.5)
        put(x, by - 1, 'H'); put(x, by, 'N'); put(x, by + 1, 'N')
    for ex in (cx - 11, cx + 11):   # the eyes: slanted almonds under the brow, set wide so they blaze either side of the target's head
        for y in range(15, 24):
            for x in range(W):
                dx, dy = (x - ex) / 5.6, (y - 19.5 - (x - ex) * 0.3 * (-1 if ex > cx else 1)) / 2.6
                d = dx * dx + dy * dy
                if eyes == 'shut':
                    if d <= 1 and abs(dy) < 0.35: rows[y][x] = 'T' if lit else 'N'
                    continue
                if d <= 1: rows[y][x] = ('W' if lit else 'c') if d < 0.3 else 'c' if d < 0.6 else 'C'
                elif d <= 1.6 and rows[y][x] in 'GHN': rows[y][x] = 'T'
        if eyes != 'shut':
            for x in range(round(ex) - 2, round(ex) + 3): put(x, round(19.5 + (x - ex) * 0.3 * (-1 if ex > cx else 1)), 'K')   # goat's bar pupil
    for y in range(23, 34): put(round(cx) - 1, y, 'H'); put(round(cx) + 1, y, 'N')   # nose ridge
    put(round(cx) - 2, 34, 'N'); put(round(cx) + 2, 34, 'N')
    for x in range(round(cx) - 9, round(cx) + 10):   # grim mouth, corners turned down
        dx = abs(x - cx); my = 39 + (1 if dx > 6 else 0) + (1 if dx > 8 else 0); put(x, my, 'T' if seams and dx < 6 else 'N')
    for k in range(10):   # cracks (glowing seams when lit)
        x, y = rnd.randrange(14, 48), rnd.randrange(4, 44)
        for t in range(rnd.randint(4, 8)):
            if 0 <= x < W and 0 <= y < H and rows[y][x] in 'GH': rows[y][x] = ('C' if t % 2 else 'T') if seams else 'N'
            x += rnd.choice((-1, 0, 1)); y += 1
    return [''.join(q) for q in rows]
# ---------- Air: Aquarius lightning (Christopher 2026-10-30: electric green-white, so it is not confused with the water signs: white core, pale mint, electric green, deep green edge) ----------
NPAL.update({'l': '#b8ffc8', 'L': '#39e75f', 'D': '#14a03c'})
ELEC_RECOLOR = {'#ffe14d': '#ffffff', '#ff8a1c': '#b8ffc8', '#d8321a': '#39e75f'}   # fire swirl / impact helpers drawn as lightning
def _bolt(L, seed, amp=2, branches=1):   # a jagged lightning bolt L px long, left to right: white core, pale cyan glow pixels, a forked branch or two
    import random
    rnd = random.Random(seed); H = 2 * amp + 7; rows = [['.'] * L for _ in range(H)]; y = H // 2
    def put(x, y_, ch):
        if 0 <= x < L and 0 <= y_ < H and (rows[y_][x] == '.' or ch == 'W'): rows[y_][x] = ch
    pts = []
    for x in range(L):
        if x % 3 == 0: y = max(2, min(H - 3, y + rnd.choice((-2, -1, 1, 2))))
        pts.append((x, y)); put(x, y, 'W'); put(x, y - 1, 'l'); put(x, y + 1, 'l' if x % 2 else 'L')
    for _ in range(branches):
        x, y_ = pts[rnd.randrange(L // 4, 3 * L // 4)]; d = rnd.choice((-1, 1))
        for t in range(rnd.randint(3, 6)):
            x += 1; y_ += d if t % 2 == 0 else 0; put(x, y_, 'l' if t < 3 else 'L')
    return [''.join(q) for q in rows]
def _crackle(r, seed, n=5):   # short arcs crackling out from a point in every direction (a charged fist / palm)
    import random
    rnd = random.Random(seed); w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for k in range(n):
        a = 2 * math.pi * (k + rnd.random() * 0.6) / n; x, y = float(r), float(r)
        for t in range(r):
            a += rnd.uniform(-0.7, 0.7); x += math.cos(a); y += math.sin(a)
            xi, yi = round(x), round(y)
            if 0 <= xi < w and 0 <= yi < w: rows[yi][xi] = 'W' if t < 2 else 'l' if t < r - 2 else 'L'
    return [''.join(q) for q in rows]
def _voltOrb(r, seed):   # a ball of lightning: white-hot heart, pale cyan body, electric-blue rim, a few arcs licking off it
    import random
    rnd = random.Random(seed); R = r + 3; w = 2 * R + 1; rows = [['.'] * w for _ in range(w)]
    for y in range(w):
        for x in range(w):
            d = math.hypot(x - R, y - R)
            if d <= r: rows[y][x] = 'W' if d < r * 0.45 else 'l' if d < r - 0.8 else 'L'
    for k in range(4):
        a = rnd.uniform(0, 2 * math.pi); x, y = R + r * math.cos(a), R + r * math.sin(a)
        for t in range(3):
            a += rnd.uniform(-0.8, 0.8); x += math.cos(a); y += math.sin(a)
            if 0 <= round(x) < w and 0 <= round(y) < w: rows[round(y)][round(x)] = 'l' if t < 2 else 'L'
    return [''.join(q) for q in rows]
def _zapRing(r, seed):   # an electric shock ring: a broken ring of zigzag pale cyan and blue, white sparks on it
    import random
    rnd = random.Random(seed); w = 2 * r + 3; rows = [['.'] * w for _ in range(w)]
    for k in range(int(10 * r)):
        a = 2 * math.pi * k / (10 * r)
        if math.sin(a * 5 + seed) > 0.75: continue
        rr = r + rnd.choice((-1, 0, 0, 1)); x, y = round(r + 1 + rr * math.cos(a)), round(r + 1 + rr * math.sin(a) * 0.85)
        rows[y][x] = 'W' if rnd.random() < 0.15 else 'l' if rnd.random() < 0.6 else 'L'
    return [''.join(q) for q in rows]
NPAT.update({'bolt12': _bolt(12, 1), 'bolt12b': _bolt(12, 2), 'bolt18': _bolt(18, 3, 3, 2), 'bolt18b': _bolt(18, 4, 3, 2), 'bolt8': _bolt(8, 5, 1, 0), 'bolt8b': _bolt(8, 6, 1, 0),
             'crackle3': _crackle(3, 1, 4), 'crackle4': _crackle(4, 2), 'crackle4b': _crackle(4, 3), 'crackle6': _crackle(6, 4, 7), 'crackle6b': _crackle(6, 5, 7),
             'voltOrb2': _voltOrb(2, 1), 'voltOrb3': _voltOrb(3, 2), 'voltOrb4': _voltOrb(4, 3), 'voltOrb4b': _voltOrb(4, 4),
             'zapRing6': _zapRing(6, 1), 'zapRing9': _zapRing(9, 2), 'zapRing12': _zapRing(12, 3),
             'spark': ['.l.', 'lWl', '.l.'], 'sparkL': ['L.l', '.W.', 'l.L'], 'staticV': ['l', 'W', 'l', '.', 'L'], 'staticV2': ['.l', 'W.', '.l', 'L.']})
def _glitchWave(r, w, seed, cols='WlL', gap=0):   # System Crash: a ')' psionic wave built of 2 px data blocks, each 2-row band torn sideways by a random 0-2 px glitch offset; gap drops every gap-th band
    import random
    rnd = random.Random(seed); rows = []
    for b, dy in enumerate(range(-r, r + 1, 2)):
        if gap and b % gap == gap - 1: rows += ['.', '.']; continue
        off = rnd.choice((0, 0, 1, 2, -1)); x = max(0, round(w * (1 - (dy / r) ** 2)) + off + 1)
        for k in range(2): rows.append('.' * x + cols[:len(cols) - (k if rnd.random() < 0.3 else 0)])
    n = max(map(len, rows)); return [q.ljust(n, '.') for q in rows[:2 * r + 1]]
def _glitchBar(w, seed, h=3):   # System Crash target: a bar of corrupted pixels torn across the eyes, rows shifted against each other
    import random
    rnd = random.Random(seed); rows = []
    for y in range(h):
        off = rnd.choice((0, 1, 2)); row = ['.'] * (w + 2)
        for x in range(w):
            if rnd.random() < 0.85: row[x + off] = rnd.choice('WWllLD') if y != h // 2 else rnd.choice('WWWl')
        rows.append(''.join(row))
    return rows
def _dataBits(r, seed, n=6):   # loose 1-2 px data blocks scattered round a point (a mind overloading)
    import random
    rnd = random.Random(seed); w = 2 * r + 2; rows = [['.'] * w for _ in range(w)]
    for _ in range(n):
        x, y, c = rnd.randrange(w - 1), rnd.randrange(w - 1), rnd.choice('WlL')
        rows[y][x] = c
        if rnd.random() < 0.5: rows[y][x + 1] = c
    return [''.join(q) for q in rows]
NPAT.update({'gw1': _glitchWave(4, 2, 1, 'Wl'), 'gw2': _glitchWave(7, 3, 2), 'gw3': _glitchWave(10, 4, 3, 'lLD'), 'gw3d': _glitchWave(12, 5, 4, 'LD', gap=3),
             'gbar': _glitchBar(9, 1), 'gbarB': _glitchBar(9, 2), 'gbarC': _glitchBar(11, 3), 'gbarW': _glitchBar(7, 4, 2),
             'bits4': _dataBits(4, 1), 'bits4b': _dataBits(4, 2), 'bits6': _dataBits(6, 3, 9), 'bits6b': _dataBits(6, 4, 9),
             'scanL': ['WlllL..lL'], 'scanS': ['lLL.W'],
             'eyeG': ['.L.', 'LlL', '.L.'], 'eyeGF': ['..L..', '.LlL.', 'LlWlL', '.LlL.', '..L..']})
def _dial(r, hand, lit=True):   # Lag Switch: an illusory clock dial (12 ticks, faint dotted rim, centre pin) whose hand sweeps BACKWARD; hand = clock position 0-11, a mint trail on the side it came from
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    def put(x, y, ch, over=False):
        xi, yi = round(x), round(y)
        if 0 <= xi < w and 0 <= yi < w and (rows[yi][xi] == '.' or over): rows[yi][xi] = ch
    pos = lambda p, rr: (r + rr * math.sin(2 * math.pi * p / 12), r - rr * math.cos(2 * math.pi * p / 12))
    for t in range(48):
        if t % 4 == 2: put(*pos(t / 4, r), 'L' if lit else 'D')
    for i in range(12): put(*pos(i, r), 'W' if i % 3 == 0 and lit else 'l' if lit else 'L', True)
    for q in (0.5, 1.0, 1.5): put(*pos(hand + q, r - 2), 'L')   # trail: where the hand has just been
    for t in range(1, r - 1): put(*pos(hand, t), 'W' if t < r - 3 else 'l', True)
    put(r, r, 'W', True); return [''.join(q) for q in rows]
def _rewindWave(r, w, seed, cols='Wl', gap=0):   # Lag Switch: a ')' wave of clock ticks (every other row) with a '<' rewind chevron at its middle pointing back at the caster
    import random
    rnd = random.Random(seed); n = w + 5; rows = [['.'] * n for _ in range(2 * r + 1)]
    for i, dy in enumerate(range(-r, r + 1)):
        if gap and (i // 2) % gap == gap - 1: continue
        x = round(w * (1 - (dy / r) ** 2)) + 3; rows[i][x] = 'W' if dy % 3 == 0 and cols[0] != 'L' else cols[0] if abs(dy) < r / 2 else cols[-1]
        if rnd.random() < 0.4 and x + 1 < n: rows[i][x + 1] = cols[-1]
    c = cols[0]
    for dx, dy in ((0, 0), (1, -1), (1, 1), (2, -2), (2, 2)): rows[r + dy][w - 1 + dx] = c if dx < 2 else cols[-1]
    return [''.join(q) for q in rows]
def _buffer(phase, n=8):   # Lag Switch target: a loading spinner over the head, n dots on a small ellipse; the bright dot runs round with a fading tail
    rows = [['.'] * 9 for _ in range(7)]
    for i in range(n):
        a = 2 * math.pi * i / n; x, y = round(4 + 3.6 * math.sin(a)), round(3 - 2.6 * math.cos(a)); d = (phase - i) % n
        rows[y][x] = 'W' if d == 0 else 'l' if d == 1 else 'L' if d == 2 else 'D'
    return [''.join(q) for q in rows]
def _loopRing(rx, ry, phase):   # Lag Switch target: a looping arrow running round the floor under the feet (dotted green ring, white arrow head with a mint tail)
    rows = [['.'] * (2 * rx + 1) for _ in range(2 * ry + 1)]
    for t in range(120):
        a = 2 * math.pi * t / 120; x, y = round(rx + rx * math.cos(a)), round(ry + ry * math.sin(a))
        d = (phase * 15 - t) % 120
        rows[y][x] = 'W' if d < 3 else 'l' if d < 14 else 'L' if d < 26 else ('D' if t % 4 < 2 else rows[y][x])
    return [''.join(q) for q in rows]
# ---------- Air: Libra wind (air unruled: white / pale silver for now, Christopher 2026-10-27) ----------
NPAL.update({'f': '#e9eef4', 'F': '#a3aebb', 'q': '#39e75f'})   # v2 (Christopher 2026-11-03: silver alone may not read on every terrain, add a little of the System Crash green): the rim is electric green #39e75f
#   # wind: pale air, silver, slate rim (v1 had F/q too close to the preview ground)
def _airCol(L, r, phase):   # Aero Palm: a column of compressed air driven forward, L px long, radius r: streaming edge lines, white core dashes, vortex rings every 7 px (phase shifts them)
    H = 2 * r + 1; rows = [['.'] * L for _ in range(H)]
    for x in range(L):
        fade = x > L - 5
        if (x + phase) % 3: rows[0][x] = 'q' if fade else 'F'; rows[H - 1][x] = 'q' if fade else 'F'
        if (x + phase) % 4 < 2: rows[r][x] = 'F' if fade else 'W'
        if r > 2 and (x + phase + 2) % 5 < 2: rows[r - 2][x] = 'f'; rows[r + 2][x] = 'f'
        if (x + phase) % 7 == 0:
            for y in range(H): rows[y][x] = 'f' if 0 < y < H - 1 else 'W'
    return [''.join(q) for q in rows]
def _curl(r, a0, a1, seed=0):   # Flow Parry: a curling air current, an arc of radius r from angle a0 to a1 (degrees, 0 = toward the facing, 90 = down), dashed, hooked at the head
    w = 2 * r + 3; rows = [['.'] * w for _ in range(w)]; n = max(8, int(abs(a1 - a0) / 6))
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n); x, y = round(r + 1 + r * math.cos(a)), round(r + 1 + r * 0.7 * math.sin(a))
        if (i + seed) % 4 == 3: continue
        rows[y][x] = 'W' if i > n - 3 else 'f' if i > n / 2 else 'F'
    a = math.radians(a1); x, y = r + 1 + (r - 2) * math.cos(a), r + 1 + (r - 2) * 0.7 * math.sin(a)
    if 0 <= round(x) < w and 0 <= round(y) < w: rows[round(y)][round(x)] = 'f'
    return [''.join(q) for q in rows]
NPAT.update({'aRing3': _ring(3, 'f', 'W', 1), 'aRing5': _ring(5, 'F', 'f'), 'aRing7': _ring(7, 'q', 'F', 1),
             'airCol0': _airCol(24, 3, 0), 'airCol1': _airCol(24, 4, 3), 'airCol2': _airCol(24, 4, 6), 'airColF': [r_.replace('W', 'f').replace('F', 'q') for r_ in _airCol(24, 4, 1)],
             'airSlug': _airCol(16, 4, 0), 'airPuck': _airCol(9, 2, 1), 'airPuckS': _airCol(6, 2, 2),
             'aStreak': ['FFff.fW', '.......', '.qFff..'], 'aStreak2': ['qFfffW', '..qFf.'],
             **{'curl%d' % k_: _curl(14, -150 + 60 * k_, -40 + 60 * k_, k_) for k_ in range(6)},
             **{'curlS%d' % k_: _curl(9, 30 + 70 * k_, 140 + 70 * k_, k_) for k_ in range(6)},
             'feather': ['....qWq', '...qfWq', '..qffq.', '.qfFq..', 'qFqq...', 'q......'], 'feather2': ['qWq....', 'qWfq...', '.qffq..', '..qFfq.', '...qqFq', '......q'], 'feather3': ['.qWq', '.qfq', 'qfFq', 'qFq.', 'q...'],
             'puff': ['.f.f.', 'fWfFf', '.FfF.', '..q..'], 'eyeW': ['.F.', 'FWF', '.F.'], 'eyeWF': ['..F..', '.fWf.', 'FWWWF', '.fWf.', '..F..']})
def _howl(r, w, seed, gap=0):   # Gemini Howling Blast v2: a ')' sound shockwave rolling out of the mouth toward the target: white leading edge, silver body, green rim behind, shock spikes pushed out ahead
    import random
    rnd = random.Random(seed); rows = [['.'] * (w + 6) for _ in range(2 * r + 1)]
    for i, dy in enumerate(range(-r, r + 1)):
        if gap and i % gap == gap - 1: continue
        u = 1 - (dy / r) ** 2; x = round(w * u) + 1
        rows[i][x + 1] = 'W'; rows[i][x] = 'f' if abs(dy) < r * 0.7 else 'F'
        if u > 0.15 and x - 1 >= 0: rows[i][x - 1] = 'q' if abs(dy) > r * 0.35 else 'F'
    for k in range(max(2, r // 3)):
        dy = rnd.randint(-r + 1, r - 1); i = dy + r; x = round(w * (1 - (dy / r) ** 2)) + 3
        for e in range(2):
            if x + e < w + 6: rows[i][x + e] = 'W' if e == 0 else 'q'
    return [''.join(q) for q in rows]
NPAL.update({'k': '#1b1f27', 'o': '#3a4250'})   # Libra Singularity Sphere: the vacuum's near-black heart and its deep slate shell
def _crescent(r, t):   # Gale Slicer: a ')' blade of compressed wind, r tall-radius, t px thick at the middle tapering to points: white edge, pale air body, silver back, slate rim, two wind streaks trailing
    H = 2 * r + 1; W_ = t + 9; rows = [['.'] * W_ for _ in range(H)]
    for i, dy in enumerate(range(-r, r + 1)):
        u = 1 - (dy / r) ** 2; x1 = 7 + round(t * 0.6 * u + 1); th = max(1, round(t * u))
        for q in range(th):
            x = x1 - q
            if 0 <= x < W_: rows[i][x] = 'W' if q == 0 else 'f' if q < th - 1 else 'F'
        if 0 <= x1 + 1 < W_ and u > 0.2: rows[i][x1 + 1] = 'q' if abs(dy) > r / 3 else 'F'
        if dy in (-2, 2): 
            for x in range(0, x1 - th - 1): rows[i][x] = 'F' if x % 3 else '.'
    return [''.join(q) for q in rows]
def _boom(r, seed):   # Pressure Blast: a sonic-boom ring: a white ring broken by silver, slate dashes, and short shock spikes pushed out from it
    import random
    rnd = random.Random(seed); w = 2 * r + 7; c = r + 3; rows = [['.'] * w for _ in range(w)]
    for k in range(int(12 * r)):
        a = 2 * math.pi * k / (12 * r); x, y = round(c + r * math.cos(a)), round(c + r * 0.8 * math.sin(a))
        rows[y][x] = 'W' if k % 5 else 'F'
        x2, y2 = round(c + (r + 1) * math.cos(a)), round(c + (r + 1) * 0.8 * math.sin(a))
        if k % 3 == 0: rows[y2][x2] = 'f'
    for k in range(8):
        a = 2 * math.pi * (k + rnd.random() * 0.5) / 8
        for d in (r + 2, r + 3):
            x, y = round(c + d * math.cos(a)), round(c + d * 0.8 * math.sin(a))
            if 0 <= x < w and 0 <= y < w: rows[y][x] = 'q' if d == r + 3 else 'F'
    return [''.join(q) for q in rows]
def _vac(r, phase, front=True):   # Singularity Sphere: a vacuum sphere; front=False: the near-black disc with a slate shell (drawn behind the fighter); front=True: its white event rim and four spiral arms of air being sucked in (rotating with phase)
    R = r + 7; w = 2 * R + 1; rows = [['.'] * w for _ in range(w)]
    for y in range(w):
        for x in range(w):
            d = math.hypot(x - R, (y - R) / 0.9)
            if not front and d <= r: rows[y][x] = 'k' if d < r - 2 else 'o'
            if front and r - 0.6 <= d <= r + 0.4 and (x + y + phase) % 3: rows[y][x] = 'W' if (x + phase) % 2 else 'f'
    if front:
        for arm in range(4):
            for i in range(16):
                rr = R - i * (R - r) / 16; a = arm * math.pi / 2 + phase * 0.45 + i * 0.12
                x, y = round(R + rr * math.cos(a)), round(R + rr * 0.9 * math.sin(a))
                if 0 <= x < w and 0 <= y < w and i % 4 != 3: rows[y][x] = 'q' if i < 5 else 'F' if i < 11 else 'f'
    return [''.join(q) for q in rows]
NPAT.update({'galeBlade': _crescent(7, 4), 'galeBladeS': _crescent(5, 3), 'galeCut': ['.......W', '.....Wf.', '...Wff..', '.Wff....', 'Wq......'],
             'compress': ['.f.', 'fWf', '.f.'], 'compress2': ['..F..', '.fWf.', 'FWWWF', '.fWf.', '..F..'],
             'hw1': _howl(3, 1, 1), 'hw2': _howl(6, 2, 2), 'hw3': _howl(9, 3, 3), 'hw4': _howl(12, 4, 4), 'hw4d': _howl(13, 5, 5, gap=3), **{'hwB%d' % k_: [r_[::-1] for r_ in _howl(3 * k_, k_, k_ + 6)] for k_ in (1, 2, 3)}, 'boom4': _boom(4, 1), 'boom8': _boom(8, 2), 'boom12': _boom(12, 3), 'boom15': _boom(15, 4),
             **{'vacF%d_%d' % (r_, k_): _vac(r_, k_) for r_ in (3, 6, 10, 13) for k_ in range(4)}, **{'vacB%d' % r_: _vac(r_, 0, False) for r_ in (3, 6, 10, 13)},
             'vacSeed': ['.o.', 'okο'.replace('ο', 'o'), '.o.']})
def _scale(tilt):   # Libra Indecision: an illusory balance scale: post and base, a beam tipped by tilt px at each end, a pan hung from each end (the low pan heavier, brighter)
    W_, H = 15, 12; rows = [['.'] * W_ for _ in range(H)]; c = 7
    for y in range(2, 10): rows[y][c] = 'F'
    for x in range(5, 10): rows[10][x] = 'q'
    rows[11][4] = rows[11][10] = 'q'; rows[1][c] = 'W'
    for x in range(1, 14):
        y = round(2 + tilt * (x - c) / 6); rows[max(0, min(H - 1, y))][x] = 'W' if abs(x - c) < 2 else 'f'
    for end, sg in ((1, -1), (13, 1)):
        ye = round(2 + tilt * (end - c) / 6); low = sg * tilt > 0
        for y in range(ye + 1, ye + 4): rows[max(0, min(H - 1, y))][end + (-1 if y == ye + 1 else 0) * 0] = 'F'
        py = min(H - 1, ye + 4)
        for x in range(end - 2, end + 3):
            if 0 <= x < W_: rows[py][x] = 'W' if low else 'f'
        if 0 <= end - 2 < W_ and py - 1 >= 0: rows[py - 1][end - 2] = 'q'
        if end + 2 < W_ and py - 1 >= 0: rows[py - 1][end + 2] = 'q'
    return [''.join(q) for q in rows]
def _arcW(r, w, cols='Wf', gap=0):   # Libra genjutsu: a plain ')' wave in wind colours, dashed when gap
    rows = [['.'] * (w + 2) for _ in range(2 * r + 1)]
    for i, dy in enumerate(range(-r, r + 1)):
        if gap and i % gap == gap - 1: continue
        x = round(w * (1 - (dy / r) ** 2)); rows[i][x] = cols[0] if abs(dy) < r / 2 else cols[-1]
    return [''.join(q) for q in rows]
def _spiral(r, phase, turns=2.2):   # Libra Vertigo: a dizzy spiral of dots winding in to a white heart, turning with phase
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]; n = int(30 * turns)
    for i in range(n + 1):
        t = i / n; a = 2 * math.pi * turns * t + phase * math.pi / 3; rr = r * (1 - t)
        x, y = round(r + rr * math.cos(a)), round(r + rr * 0.8 * math.sin(a))
        if i % 3 != 2: rows[y][x] = 'q' if t < 0.3 else 'F' if t < 0.65 else 'f' if t < 0.9 else 'W'
    return [''.join(q) for q in rows]
def _motesW(phase, n=6):   # Vertigo target: wind motes reeling round over the head (a small ellipse, bright mote with a fading tail)
    rows = [['.'] * 15 for _ in range(5)]
    for i in range(n):
        a = 2 * math.pi * i / n; x, y = round(7 + 6.5 * math.cos(a)), round(2 + 2 * math.sin(a)); d = (phase - i) % n
        rows[y][x] = 'W' if d == 0 else 'f' if d == 1 else 'F' if d == 2 else 'q'
    return [''.join(q) for q in rows]
NPAT.update({**{'scale%+d' % t_: _scale(t_) for t_ in (-2, -1, 0, 1, 2)},
             'iw1': _arcW(4, 2), 'iw2': _arcW(7, 3), 'iw3': _arcW(10, 4, 'fF'), 'iw3d': _arcW(12, 5, 'Fq', gap=3),
             **{'spiral%d_%d' % (r_, k_): _spiral(r_, k_) for r_ in (3, 5, 7) for k_ in range(6)},
             **{'motesW%d' % k_: _motesW(k_) for k_ in range(6)}})
def _sweepArc(w, h, stage):   # Sonic Sweep v2: the leg's path traced on the floor as a flat swoosh, an arc bowed toward the viewer: white at the leading (front) end, silver, the green rim at the trailing tail; stage 0 just drawn, 1 the tail fading, 2 a faint dashed trace
    rows = [['.'] * w for _ in range(h + 2)]
    for x in range(w):
        t = x / (w - 1); y = round(h * (1 - (2 * t - 1) ** 2))
        if stage == 2 and x % 3: continue
        c = 'W' if t > 0.75 else 'f' if t > 0.4 else 'F' if t > 0.15 else 'q'
        if stage == 1 and t < 0.3: continue
        rows[y][x] = c
        if y + 1 < h + 2 and t > 0.3 and stage < 2: rows[y + 1][x] = 'q' if t < 0.6 else 'F'
    return [''.join(q) for q in rows]
NPAT.update({'vcone': _arcW(18, 5, 'Wf'), 'vcone2': _arcW(16, 4, 'fF', gap=4), 'floorStreak': ['......fffWW', 'qqFFFff....'], 'floorStreakL': ['WWfff......', '....ffFFFqq'],
             'boomFlat': [r_ for r_ in _boom(9, 5)[5:-5]], **{'sweepArc%d' % k_: _sweepArc(26, 6, k_) for k_ in range(3)}, 'crackV': ['..W..', '.WfW.', 'WfqfW', '.q.q.']})   # Gemini Mach Dash vapour cone, Sonic Sweep floor boom
def _sine(L, amp, per, phase, cols='Wf'):   # Gemini Tinnitus: a thin high-pitched sine line L px long
    H = 2 * amp + 1; rows = [['.'] * L for _ in range(H)]
    for x in range(L):
        y = round(amp + amp * math.sin(2 * math.pi * (x + phase) / per)); rows[y][x] = cols[0] if x < L * 0.6 else cols[-1] if len(cols) < 3 or x < L * 0.85 else cols[2]   # v2 (Christopher 2026-11-03 19:04, updated colour scheme): a third colour, the green rim, on the trailing tail
        if len(cols) > 2 and x % 4 == 1 and 0 <= y + 1 < H and rows[y + 1][x] == '.': rows[y + 1][x] = cols[2]   # green under-glint along the line
    return [''.join(q) for q in rows]
def _bars(n, h, gap, phase):   # Gemini Resonance Chamber: standing sound waves as vertical bars, tallest at the middle, pulsing with phase
    rows = [['.'] * (n * gap) for _ in range(h)]
    for i in range(n):
        hh = max(2, round(h * (0.45 + 0.55 * abs(math.cos((i + phase) * math.pi / n))))); y0 = (h - hh) // 2
        for y in range(y0, y0 + hh): rows[y][i * gap] = 'W' if y in (y0, y0 + hh - 1) else 'f' if (y + i + phase) % 2 else 'F'
        for y in (y0 - 1, y0 + hh):   # v2 (updated colour scheme): green caps beyond each bar's white ends
            if 0 <= y < h: rows[y][i * gap] = 'q'
    return [''.join(q) for q in rows]
NPAT.update({**{'sine%d' % k_: _sine(14, 2, 4, k_, 'Wfq') for k_ in range(4)}, **{'sineL%d' % k_: _sine(22, 2, 4, k_, 'fFq') for k_ in range(4)},
             **{'bars%d' % k_: _bars(5, 22, 3, k_) for k_ in range(4)}, 'drip': ['R', 'R', '.', 'M'], 'earRing': ['.W.', 'W.W', '.W.']})
NPAT.update({**{'dial%d_%d' % (r_, h_): _dial(r_, h_) for r_ in (4, 6) for h_ in range(12)}, 'dialDim': _dial(6, 1, lit=False),
             'rw1': _rewindWave(4, 2, 1), 'rw2': _rewindWave(7, 3, 2, 'Wll'), 'rw3': _rewindWave(10, 4, 3, 'lL'), 'rw3d': _rewindWave(12, 5, 4, 'LD', gap=3),
             **{'buf%d' % k_: _buffer(k_) for k_ in range(8)}, **{'loopR%d' % k_: _loopRing(11, 3, k_) for k_ in range(8)}})
def _edome(rx, ry, frac, seed, lit=True):   # EMP Field: a dome of crackling electricity round the caster: a jagged arc (white / pale cyan, blue jitter) grown from the floor up both sides to frac, a dotted inner shell
    import random
    rnd = random.Random(seed); rows = [['.'] * (2 * rx + 1) for _ in range(ry + 1)]
    for t in range(0, 1201):
        a = math.pi * t / 1200
        if min(a, math.pi - a) > frac * math.pi / 2: continue
        j = rnd.choice((-1, 0, 0, 0, 1)) if t % 9 == 0 else 0
        for k, c in ((0, 'W' if lit else 'l'), (1, 'l'), (2, 'L')):
            x = round(rx + (rx - k - j) * math.cos(a)); y = round(ry - (ry - k - j) * math.sin(a))
            if 0 <= y <= ry and 0 <= x <= 2 * rx and rows[y][x] in '.L': rows[y][x] = c
        x = round(rx + (rx - 6) * math.cos(a)); y = round(ry - (ry - 6) * math.sin(a))
        if 0 <= y <= ry and t % 14 == 0 and min(a, math.pi - a) <= frac * math.pi / 2: rows[y][x] = 'L'
    for _ in range(6 if lit else 3):   # arcs running over the shell
        a = rnd.uniform(0.15, math.pi - 0.15)
        if min(a, math.pi - a) > frac * math.pi / 2: continue
        x, y = rx + (rx - 1) * math.cos(a), ry - (ry - 1) * math.sin(a)
        for t in range(5):
            a2 = a + rnd.uniform(-1.2, 1.2) + math.pi; x += math.cos(a2) * 0.9; y -= math.sin(a2) * 0.9
            xi, yi = round(x), round(y)
            if 0 <= xi <= 2 * rx and 0 <= yi <= ry: rows[yi][xi] = 'W' if t < 2 else 'l'
    return [''.join(q) for q in rows]
def _eripple(rx, ry):   # EMP Field v2: a thin dotted pulse of the field radiating outward (one shell, mint and green)
    rows = [['.'] * (2 * rx + 1) for _ in range(ry + 1)]
    for t in range(0, 1201):
        a = math.pi * t / 1200; x = round(rx + rx * math.cos(a)); y = round(ry - ry * math.sin(a))
        if (x + y) % 3 != 2: rows[y][x] = 'l' if (x + y) % 3 == 0 else 'L'
    return [''.join(q) for q in rows]
NPAT.update({'edomeA': _edome(10, 18, 1.0, 21), 'edomeB': _edome(18, 32, 1.0, 22), 'edomeC': _edome(25, 44, 1.0, 23), 'edomeD': _edome(30, 52, 1.0, 24),
             **{'eripple%d' % k: _eripple(rx, ry) for k, (rx, ry) in enumerate(((14, 25), (19, 33), (24, 42), (29, 50)))}})
NPAT.update({**{'edome%d' % k: _edome(30, 52, f, k) for k, f in enumerate((0.25, 0.55, 0.85, 1.0))}, 'edome4': _edome(30, 52, 1.0, 9), 'edomeDim': _edome(30, 52, 1.0, 11, lit=False),
             'zapRing16': _zapRing(16, 4), 'zapRing20': _zapRing(20, 5), 'voltOrb6': _voltOrb(6, 5), 'voltOrb6b': _voltOrb(6, 6), 'voltOrb8': _voltOrb(8, 7),
             'bolt24': _bolt(24, 8, 3, 3), 'bolt24b': _bolt(24, 9, 3, 3), 'boltV': [''.join(r) for r in zip(*_bolt(20, 10, 3, 2))], 'boltV2': [''.join(r) for r in zip(*_bolt(16, 11, 2, 1))],
             'knifeArc': _crackle(5, 12, 6), 'knifeArc2': _crackle(5, 13, 6)})
def _eblade(L, seed, spread=1.0, base=0.0):   # base: turns the whole sheaf (negative = tipped up: Lightning Cutter v3 uppercut)
    return _eblade0(L, seed, spread, base)
def _eblade0(L, seed, spread, base):   # Lightning Cutter v2: a sheaf of electric blades enveloping the knife hand, pointing forward (+x): a long central blade and shorter ones fanning above and below, white cores, mint bodies, green jagged edges
    import random
    rnd = random.Random(seed); H = 21 if not base else L + 4; rows = [['.'] * (L + 2) for _ in range(H)]; cy = H // 2 if not base else H - 3
    for (ln, ang, w) in ((L, 0, 3.0), (round(L * 0.75), -0.3 * spread, 2.2), (round(L * 0.7), 0.32 * spread, 2.2), (round(L * 0.5), -0.6 * spread, 1.6), (round(L * 0.45), 0.65 * spread, 1.6)):
        for i in range(ln * 2):
            t = i / 2; f = t / ln; half = w * (1 - f) + 0.4
            y0 = cy + math.sin(ang + base) * t + (rnd.choice((-0.6, 0, 0.6)) if i % 3 == 0 else 0); x0 = math.cos(ang + base) * t
            for j in range(-4, 5):
                o = j / 2
                if abs(o) > half: continue
                x, y = round(x0), round(y0 + o)
                if 0 <= x < L + 2 and 0 <= y < H:
                    ch = 'W' if abs(o) < 0.3 and f < 0.7 else 'l' if abs(o) < half - 0.6 else 'L'
                    if rows[y][x] == '.' or ch == 'W': rows[y][x] = ch
    for _ in range(4):   # sparks crackling off the edges
        x, y = rnd.randrange(2, L), rnd.choice((0, 1, H - 2, H - 1))
        rows[y][x] = 'l'
    return [''.join(q) for q in rows]
NPAT.update({'eblade0': _eblade(18, 1), 'eblade1': _eblade(18, 2, 1.2), 'eblade2': _eblade(18, 3, 0.9), 'ebladeS': _eblade(11, 4, 0.8), 'ebladeL': _eblade(24, 5, 0.7),
             'ebladeLow': _eblade(16, 8, 0.8, 0.25), 'ebladeLow2': _eblade(16, 9, 0.9, 0.25), 'ebladeUp': _eblade(16, 10, 0.7, -0.85), 'ebladeUp2': _eblade(18, 11, 0.8, -0.95),
             'impaleUp': [r[::-1] for r in _eblade(18, 12, 0.6, -0.8)], 'impaleUp2': [r[::-1] for r in _eblade(20, 13, 0.8, -0.85)],
             'impaleOut': [r[::-1] for r in _eblade(18, 6, 0.6)], 'impaleOut2': [r[::-1] for r in _eblade(20, 7, 0.8)]})
def _ebladeAt(L, seed, spread, base, back=5):   # Lightning Cutter v4 (Christopher 2026-11-03: the blades cover the hand, not below it): the sheaf rooted `back` px behind the fingertips so it wraps the
    import random                                  # knife hand and juts past it; returns the rows plus the anchored dx/dy that put the root on the hand anchor (patterns are centred on the anchor)
    rnd = random.Random(seed); pts = {}
    for (ln, ang, w) in ((L, 0, 3.4), (round(L * 0.75), -0.3 * spread, 2.4), (round(L * 0.7), 0.32 * spread, 2.4), (round(L * 0.5), -0.6 * spread, 1.8), (round(L * 0.45), 0.65 * spread, 1.8)):
        for i in range(ln * 2):
            t = i / 2; f = t / ln; half = w * (1 - f) + 0.5
            jit = rnd.choice((-0.6, 0, 0.6)) if i % 3 == 0 else 0
            for j in range(-5, 6):
                o = j / 2
                if abs(o) > half: continue
                a = ang + base; x = round(t * math.cos(a) - (o + jit) * math.sin(a)) - back; y = round(t * math.sin(a) + (o + jit) * math.cos(a))
                ch = 'W' if abs(o) < 0.3 and f < 0.7 else 'l' if abs(o) < half - 0.6 else 'L'
                if (x, y) not in pts or ch == 'W': pts[(x, y)] = ch
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]; x0, y0 = min(xs), min(ys); w_, h_ = max(xs) - x0 + 1, max(ys) - y0 + 1
    rows = [['.'] * w_ for _ in range(h_)]
    for (x, y), ch in pts.items(): rows[y - y0][x - x0] = ch
    for _ in range(5): rows[rnd.randrange(h_)][rnd.randrange(w_)] = 'l'
    return [''.join(q) for q in rows], (w_ - 1) / 2 + x0, (h_ - 1) / 2 + y0   # dx, dy: offset of the pattern centre from the root
EB = {}
for nm, args in {'ebHand0': (15, 21, 0.9, 0.15), 'ebHand1': (15, 22, 1.1, 0.2), 'ebUp': (16, 23, 0.8, -0.9), 'ebUpS': (11, 24, 0.7, -0.9)}.items():
    NPAT[nm], dx_, dy_ = _ebladeAt(*args); EB[nm] = (round(dx_), round(dy_))
def eb(nm, alpha=None):   # anchored item: blade sheaf nm rooted on the hand
    return (nm, 'hand', EB[nm][0], EB[nm][1]) + (({'alpha': alpha},) if alpha else ())
ELEC_TRAIL = {(255, 255, 255): (0xff, 0xff, 0xff), (0xe3, 0xe3, 0xe3): (0x39, 0xe7, 0x5f)}   # Lightning Cutter: motion streak white inner half, electric green tail
ELEC_FEET = [[('spark', _foot(SPRINT_LEGS[k])), ('sparkL', [_foot(SPRINT_LEGS[(k + 4) % 8])[0], _foot(SPRINT_LEGS[(k + 4) % 8])[1]])] + ([('bolt8', [_foot(SPRINT_LEGS[k])[0] - 9, 63])] if _foot(SPRINT_LEGS[k])[1] == 63 else []) for k in range(6)]
ELEC_WAKE = [[('bolt12', [2, 58]), ('spark', [10, 40]), ('sparkL', [3, 30])], [('bolt12b', [1, 60]), ('sparkL', [12, 44]), ('spark', [4, 34])]]
def _crust(w, h, seed):   # Titan's Gaze v2: a jagged crust of stone creeping up over the target's feet and shins (it seizes up, petrified with fear)
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]; c0 = (w - 1) / 2
    tops = [max(0, round(h * 0.15 + abs(x - c0) / c0 * h * 0.35 + rnd.randint(-2, 2))) for x in range(w)]
    for x in range(w):
        for y in range(tops[x], h):
            rows[y][x] = 'N' if y == tops[x] or x in (0, w - 1) else 'H' if (x * 3 + y * 5 + seed) % 7 < 2 else 'N' if (x + 2 * y + seed) % 9 == 0 else 'G'
    return [''.join(q) for q in rows]
def _gazeEye(n):   # Titan's Gaze v2 caster: a great goat's eye opening in the air behind the caster's head (n: 0 a slit, 1 half open, 2 open and blazing)
    rows = [['.'] * 17 for _ in range(7)]; ry = (0.6, 1.8, 3.2)[n]
    for y in range(7):
        for x in range(17):
            dx, dy = (x - 8) / 8, (y - 3) / max(ry, 0.6); d = dx * dx + dy * dy
            if d <= 1: rows[y][x] = 'C' if d > 0.6 else 'c' if d > 0.25 or n < 2 else 'W'
    if n: rows[3][6:11] = ['K'] * 5
    return [''.join(q) for q in rows]
NPAT.update({**{'globe%d' % k: _globe(11, k * 0.5) for k in range(4)}, 'globeS': _globe(5), 'globeM': _globe(8),
             'titanLit': _titan(58, 44, True), 'titanDim': _titan(58, 44, False), 'sweat': ['w', 'W'], 'fearLines': ['C.....C', '.C...C.', '..C.C..']})
NPAT.update({'titan2Lit': _titan2(True, 'open', True), 'titan2Dim': _titan2(False, 'open', False), 'titan2Shut': _titan2(False, 'shut', False), 'titan2Wake': _titan2(True, 'shut', True),
             'crust1': _crust(20, 6, 3), 'crust2': _crust(22, 12, 5), 'gazeEye0': _gazeEye(0), 'gazeEye1': _gazeEye(1), 'gazeEye2': _gazeEye(2),
             'pebbles': ['G.....N', '.......', '...H...', 'N.....G'], 'pebbles2': ['...N...', 'H.....G', '.......', '..G..N.'],
             'gazeBeam': ['......c.....C.....c..W', 'C..c.C..cC.c..CcC.cWcW', '......c.....C.....c..W'], 'gazeBeam2': ['.....C......c....c..', 'c.C..c.C..c..C.c.CcC', '.....C......c....c..']})
NPAT.update({'tombBack': _slab(30, 54, 3, arch=True), 'tombFront': _slab(30, 20, 5)})
NPAT.update({'stalBack': _spikes(44, 58, 5, 21, widths=(7, 8, 9)), 'stalFrontL': _spikes(18, 34, 2, 22, lean=-1, widths=(6, 7)), 'stalFrontR': _spikes(18, 38, 2, 23, lean=1, widths=(6, 7, 8)), 'stalTips': _spikes(30, 8, 6, 24), 'stalTipsS': _spikes(12, 5, 3, 25)})   # Capricorn Stalactite Rain: giant crystal spears
NPAT.update({'stalBack2': NPAT['stalBack'][20:], 'stalFrontL2': NPAT['stalFrontL'][12:], 'stalFrontR2': NPAT['stalFrontR'][14:]})
def _spear(L, ux, uy, w=5):   # Stalactite Rain v2: one crystal spear L px long pointing along (ux, uy) (tip at that end), w px thick, tapering to the point over its last third; glint c down one side, deep teal T down the other and at the butt
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n; px_, py_ = -uy, ux
    pts = {}
    for i in range(L * 3):
        t = i / 3; f = t / L; half = (w / 2) * (1 if f < 0.66 else max(0.15, (1 - f) / 0.34))
        for j in range(-w * 2, w * 2 + 1):
            o = j / 4
            if abs(o) > half: continue
            x, y = round(t * ux + o * px_), round(t * uy + o * py_)
            ch = 'c' if o < -half + 1 else 'T' if o > half - 1 or t < 1 else 'C'
            if (x, y) not in pts or ch == 'C': pts[(x, y)] = ch
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]; x0, y0 = min(xs), min(ys)
    rows = [['.'] * (max(xs) - x0 + 1) for _ in range(max(ys) - y0 + 1)]
    for (x, y), ch in pts.items(): rows[y - y0][x - x0] = ch
    return [''.join(q) for q in rows]
NPAT.update({'spearUp': _spear(40, 0, -1, 7), 'spearUpS': _spear(30, -0.1, -1, 6), 'spearFall': _spear(30, -0.55, 1, 6), 'spearFallS': _spear(24, -0.45, 1, 5), 'spearStreak': ['c', 'C', '.', 'c', '.', '.', 'c']})
NPAT.update({'spearUp1': NPAT['spearUp'][-12:], 'spearUp2': NPAT['spearUp'][-26:], 'spearUpS1': NPAT['spearUpS'][-9:], 'spearUpS2': NPAT['spearUpS'][-20:]})
NPAT.update({**{'tombBack%d' % n: NPAT['tombBack'][-round(54 * n / 3):] for n in (1, 2)}, **{'tombFront%d' % n: NPAT['tombFront'][-round(20 * n / 3):] for n in (1, 2)}})
NPAT.update({'gemShard': ['.c.', 'cCT', '.T.'], 'gemShard2': ['..c..', '.cCc.', 'cCCTT', '.CTT.', '..T..'], 'gemSpark': ['c.c', '.W.', 'c.c'],   # Capricorn: crystal shards and glints
             'gemBurst': _ring(5, 'c', 'C'), 'gemBurst2': _ring(8, 'C', 'T', gap=1), 'gemCrack': ['T...T', '.T.T.', '..W..', '.T.T.', 'T...T'],
             'slash': ['......cW', '....cWc.', '..cWc...', 'cWc.....', 'c.......'], 'slash2': ['.........cWW', '.......cWWc.', '.....cWWc...', '...cWWc.....', '.cWWc.......', 'cWc.........']})
NPAT.update({'wraithM': [r[::-1] for r in NPAT['wraith']]})   # Phantom Plague v2: the phantom turned round, facing back at the victim as it passes in front
NPAT.update({'clawMark': ['C...C...C....', '.C...C...C...', '..C...C...C..', '...C...C...C.', '....c...c...c'], 'clawMark2': ['..........', 'c...c...c.', '.c...c...c.'[:10], '..c...c...']})   # Phantom Plague target: three teal claw marks raked down past the victim

def _column(h, w, phase, tight, cracks=0, seed=0):   # Sand Burial v2 (Christopher 2026-10-28: sand up to the target's neck, squeezing it): a column of sand from the neck down,
    import random                                     # rounded over the shoulders, pinched in by tight (0-1), dark constriction bands winding round it (phase), cracks before the break
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]; c0 = (w - 1) / 2
    for y in range(h):
        sh = min(1.0, 0.45 + y / 6)   # narrow at the neck, out over the shoulders
        half = (w / 2) * sh * (1 - tight * 0.26 * math.sin(math.pi * min(1, y / (h * 0.7))))
        for x in range(w):
            dx = abs(x - c0)
            if dx > half: continue
            edge = dx > half - 1.3 or y == 0
            band_ = (y + round((x - c0) * 0.6) + phase * 2) % 7 == 0
            rows[y][x] = 's' if edge else ('v' if band_ and tight > 0.5 else 's' if band_ else 'Z' if rnd.random() < 0.07 else 's' if rnd.random() < 0.12 else 'S')
    for k in range(cracks):   # jagged dark cracks splitting the sand
        x = round(c0 + (k - (cracks - 1) / 2) * w / (cracks + 1)); y = rnd.randint(1, 4)
        while y < h - 2:
            if 0 <= x < w and rows[y][x] != '.': rows[y][x] = 'K'
            y += 1; x += rnd.choice((-1, 0, 0, 1))
    return [''.join(r) for r in rows]

def _shatter(R, seed, chunks=14):   # Sand Burial break free: chunks of packed sand blown outward in a ring R px out, grains between
    import random
    rnd = random.Random(seed); n = 2 * R + 5; rows = [['.'] * n for _ in range(n)]; c = n // 2
    for i in range(chunks):
        a = 2 * math.pi * (i + rnd.random() * 0.5) / chunks; r = R + rnd.randint(-3, 2)
        x, y = round(c + r * math.cos(a)), round(c + r * math.sin(a))
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            if 0 <= x + dx < n and 0 <= y + dy < n: rows[y + dy][x + dx] = 's' if (dx + dy) == 2 else 'S'
        for _ in range(3):
            q = r - rnd.randint(2, 6); X, Y = round(c + q * math.cos(a + rnd.uniform(-0.2, 0.2))), round(c + q * math.sin(a + rnd.uniform(-0.2, 0.2)))
            if 0 <= X < n and 0 <= Y < n: rows[Y][X] = rnd.choice('SsZ')
    return [''.join(r) for r in rows]
NPAT.update({**{'col%d' % k: _column(52, 24, k, (0.4, 1.0, 0.6, 1.0)[k], seed=k) for k in range(4)}, 'colRise': _column(52, 24, 0, 0.0, seed=9),
             'colCrack1': _column(52, 24, 1, 1.0, cracks=2, seed=11), 'colCrack2': _column(52, 24, 2, 1.0, cracks=4, seed=12),
             'shatter12': _shatter(12, 1), 'shatter18': _shatter(18, 2), 'shatter23': _shatter(23, 3, chunks=18)})   # Sand Burial v2: the neck-high column squeezing, cracking, blown apart
def _slabcrack(n):   # Mausoleum break out: dark cracks splitting the front slab from the centre (n: 1 = two cracks, 2 = five), white glints at their heads
    rows = [['.'] * 26 for _ in range(36)]
    for a in [(-0.5, -1), (0.6, 1), (0.9, -0.6), (-0.9, 0.5), (0.1, 1)][:2 if n == 1 else 5]:
        x, y = 13.0, 18.0
        for t in range(9 + 5 * n):
            x += a[0] + (0.6 if t % 3 == 1 else -0.3 if t % 3 == 2 else 0); y += a[1]
            X, Y = round(x), round(y)
            if 0 <= X < 26 and 0 <= Y < 36: rows[Y][X] = 'K'
        if 0 <= round(x) < 26 and 0 <= round(y) < 36: rows[round(y)][round(x)] = 'W'
    return [''.join(q) for q in rows]
def _blocks(R, seed, n):   # Mausoleum break out: n blocks of dressed stone (3-5 px, lit H top-left, dark N bottom-right) blown out in a ring about R px, dust specks between
    import random
    rnd = random.Random(seed); m = 2 * R + 9; rows = [['.'] * m for _ in range(m)]; c = m // 2
    for i in range(n):
        a = 2 * math.pi * (i + rnd.random() * 0.6) / n; r = R + rnd.randint(-3, 2); bw, bh = rnd.choice((5, 6, 7)), rnd.choice((4, 5))
        x0, y0 = round(c + r * math.cos(a)) - bw // 2, round(c + r * 0.85 * math.sin(a)) - bh // 2
        for yy in range(bh):
            for xx in range(bw):
                X, Y = x0 + xx, y0 + yy
                if 0 <= X < m and 0 <= Y < m: rows[Y][X] = '#' if yy in (0, bh - 1) or xx in (0, bw - 1) else 'H' if yy == 1 or xx == 1 else 'N' if yy == bh - 2 or xx == bw - 2 else 'G'
        for _ in range(2):
            q = r - rnd.randint(3, 7); X, Y = round(c + q * math.cos(a)), round(c + q * 0.85 * math.sin(a))
            if 0 <= X < m and 0 <= Y < m: rows[Y][X] = rnd.choice('eE')
    return [''.join(q) for q in rows]
STONE = lambda pat: [r.replace('Z', 'H').replace('S', 'G').replace('s', 'N') for r in pat]   # Mausoleum break out: the sand helpers in tomb stone
NPAT.update({**{'pillarC%d' % n: NPAT['pillar'][-n:] for n in (44, 30, 16)}, **{'tombBackC%d' % n: NPAT['tombBack'][-n:] for n in (42, 28, 14)}, 'rubbleHeap': STONE(_mound(9, w=44, seed=5)), 'rubbleHeap2': STONE(_mound(6, w=46, seed=6)),
             'roofTilt': [r[2:] + '..' if i < 5 else r for i, r in enumerate(_roof(46, 10))], 'roofBlocks': _blocks(14, 44, 9)})   # Mausoleum v3 crumble (Christopher 2026-10-30: the tomb crumbles to the ground instead of disappearing)
NPAT.update({'stoneShatter12': STONE(_shatter(12, 41)), 'stoneShatter18': STONE(_shatter(18, 42, chunks=16)), 'stoneShatter23': STONE(_shatter(23, 43, chunks=18)),
             'slabCrack1': _slabcrack(1), 'slabCrack2': _slabcrack(2), 'stoneShatter12': _blocks(12, 41, 7), 'stoneShatter18': _blocks(19, 42, 8), 'stoneShatter23': _blocks(25, 43, 9)})

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
 'meteor': ('Meteor', 10,
  'Meteor (Aries ninjutsu ultimate, charge: a giant fireball called down from the sky that blankets a wide zone next round), v2 (Christopher 2026-10-27: an ultimate needs a more dramatic animation, more frames than a typical ability): from the guard the fighter makes the seal and sinks deep, straining, embers lifting off the ground all round it; a spiked fire aura flares up and grows; then it raises the near open palm high to the sky and the fireball forms above it, swelling frame by frame until it is too big for the sky to hold, white-hot at the core, roiling orange with a red rim and flames licking off it, the aura blazing; at the peak the fighter hurls the arm forward and up with a burst of light, holds the throw through a hit-stop as the meteor tears up and away trailing a thick tail of fire, embers raining back down; the glow fades from the sky and the fighter settles back into the guard (the testbed drops the meteor on the zone the next round).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=band(-120, -150, fistKind='palm'), bob=(2, 2, 2), lean=(0, -1), **LOW)] + [
     g(an=band(-130, -150, fistKind='palm'), bob=(2, 2, 2), lean=(-1, -2), **LOW) for _ in range(4)] + [
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **LOW),   # hurled forward and up
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-80, -110, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-50, -120), af=band(-50, -130), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'pain', 'pain', 'pain', 'squint'] + ['squint'] * 4 + ['squint', 'squint', 'squint', None, None, None],
  None,
  dict(fps=10, rm='E: +1 into the throw, -1 settling back',
       burst={2: 0, 3: 1, 4: 2, 5: 3, 6: 3, 7: 3, 8: 2, 9: 2, 10: 3, 11: 4, 12: 5}, burstEvery=True,   # embers rising, spiked aura flaring and blazing, then fading
       meteor={5: ('form', 2), 6: ('form', 4), 7: ('form', 7), 8: ('form', 9), 9: ('form', 11),
               10: ('flash', 0), 11: ('fly', 0), 12: ('fly', 1), 13: ('trail', 2), 14: ('trail', 3)})),
 'blindRage': ('Blind Rage', 4,
  'Blind Rage (Aries genjutsu, mental debuff: the caster projects its fury into the target\'s mind so it sees everyone as an enemy; Confusion 1 round, INT save DC 12; range Zone of Awareness), the genjutsu template: from the guard the fighter raises the near hand with two fingers up in front of the eyes and fixes the target, the far hand staying in guard; the eyes kindle red, then flare white-hot, a dark crimson aura flickering up round it with rage wisps rising off the head; it holds the stare while red rage waves pulse out from its eyes toward the target one after another, each wider than the last, orange at the core and dark crimson at the rim, breaking up as they travel; the glow dies out of the eyes and the hand drops back into the guard (the testbed then marks the confused target).', [
     g(),
     g(an=band(-40, -160, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#d8321a', '#7a1016'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Confusion ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       fx=nfx('fire genjutsu: the eyes kindle red then flare, rage wisps off the head, red rage waves pulsing out from the eyes toward the target, widening and breaking up',
              [(2, [('eyeGlint', [38, 17])]),
               (3, [('eyeFlare', [37, 18]), ('rageWisp', [30, 7]), ('rageWisp', [35, 8])]),
               (4, [('eyeFlare', [37, 18]), ('rage1', [42, 19]), ('rageWisp', [32, 6]), ('rageWisp', [27, 9])]),
               (5, [('eyeFlare', [37, 18]), ('rage2', [45, 22]), ('rage1', [42, 19]), ('rageWisp', [29, 5]), ('rageWisp', [35, 7])]),
               (6, [('eyeGlint', [38, 17]), ('rage4', [51, 28]), ('rage2', [45, 22]), ('rageWisp', [31, 4])]),
               (7, [('rage5d', [56, 30]), ('rage3', [50, 25])]),
               (8, [('rage4d', [57, 28])])]))),
 'killingIntent': ('Killing Intent', 3,
  'Killing Intent (Aries genjutsu, mental debuff: the caster focuses its bloodlust and projects it onto the foe, freezing it with fear; Stun 1 round, STR save DC 13; range Zone of Awareness), v3 (Christopher 2026-10-27: keep the demon, but as an illusory demon mask that appears over the caster\'s head, matching its facing; the body more aggressive): from the guard the fighter coils down low, hands drawn back, a near-black blood-red aura seeping up; then it surges forward a step into a wide predatory crouch, chest driven forward, both hands thrown out in front like claws, and an illusory demon mask flickers into being over its head in profile, then solidifies, horn sweeping back, eye and fangs blazing; it holds the crouch trembling with fury, dark pressure pooling at its feet, while jagged waves of killing intent roll out of the mask\'s jaws toward the target, each bigger than the last; then the mask breaks up and fades, the aura drains away and the fighter steps back into the guard (the target takes the genjutsu mark, genjutsuAfflicted, for the Stun).', [
     g(),
     g(an=band(-25, -70), af=band(-15, -60), bob=(3, 3, 3), lean=(0, -1), **LOW),          # coil: down low, hands drawn back
     g(an=band(-25, -70), af=band(-15, -60), bob=(4, 4, 4), lean=(0, -1), **LOW),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(2, 0), **BRACE),   # surge: a step in, claws thrown out
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), **BRACE),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(1, 0), **BRACE),   # trembling with fury
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(-1, 0), **BRACE),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(1, 0), **BRACE),
     g(an=band(-75, -105, fistKind='palm'), af=band(-60, -95, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), root=(-1, 0), **BRACE),
     g(an=band(-40, -100), af=band(-35, -100), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', None, None],
  [0, 1, 2, 4, 4, 4, 4, 4, 3, 1, 0],
  dict(fps=10, rm='E: +2 surging in on frame 3, a 1 px tremble on frames 5-8, -2 back on the last frame', auraColors=('#7a1016', '#2a0406'),
       extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Stun ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       mask={2: 'faint', 3: 'flare', 4: 'full', 5: 'full', 6: 'flare', 7: 'full', 8: 'flicker'},
       maskWaves={4: [('ki1', 1, 5)], 5: [('ki2', 3, 9), ('ki1', 0, 5)], 6: [('ki3', 7, 13), ('ki2', 3, 9)], 7: [('ki4', 11, 16), ('ki3', 7, 13)], 8: [('ki4', 15, 16)]},
       fx=nfx('dark pressure pooling at the feet of the crouch',
              [(3, [('dread', [26, 63])]), (4, [('dread', [27, 63])]), (5, [('dread', [26, 63])]), (6, [('dread', [27, 63])]), (7, [('dread', [26, 63])]), (8, [('dread', [27, 63])])]))),
 'genjutsuAfflicted': ('Under Genjutsu', 0,
  'Under Genjutsu (target status, Christopher 2026-10-27: every genjutsu marks its target with an effect showing it is under a genjutsu): the shared looping state the testbed plays on a fighter for as long as any genjutsu holds it, in place of its idle; the guard sags, the hands dropped a little, and the fighter sways slowly on its feet, entranced: the eyes glow the caster\'s element colour, a thin flickering aura in that colour clings to the outline, and three glowing motes circle slowly over the head like a halo, bright passing in front of the head and dark passing behind it; fire version (Aries, Leo, Sagittarius casters: crimson and orange); the testbed recolours it for the other elements.', [
     g(an=band(-15, -105), af=band(-20, -110), bob=(1, 1, 2), lean=(0, 2)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(1, 1, 2), lean=(0, 2)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 3), lean=(0, 0)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 3), lean=(0, 0)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-15, -105), af=band(-20, -110), bob=(2, 2, 2), lean=(0, 1))],
  ['entranced'] * 8,
  [1] * 8,
  dict(fps=6, auraColors=('#d8321a', '#7a1016'), shapes={'entranced': {'E': [[0, 1, '#d8321a'], [1, 1, '#d8321a'], [0, 2, '#ff8a1c'], [1, 2, '#ff3a1a']], 'S': [[0, 2, '#ff3a1a'], [1, 2, '#ff8a1c'], [5, 2, '#ff8a1c'], [6, 2, '#ff3a1a']]}},
       extra={'loop': True, 'genjutsuMark': {'rule': 'Christopher 2026-10-27: every genjutsu target shows it is under a genjutsu. The testbed plays genjutsuAfflicted on loop in place of the target\'s idle (and draws its halo motes, aura and eye glow over any other state it plays) for as long as a genjutsu holds it; clears when the genjutsu ends', 'element': 'fire', 'recolor': {'rule': 'swap the fire colours for the caster sign\'s element: fire as drawn', 'sagittarius': {'#ffe14d': '#c9a0ff', '#ff8a1c': '#9b45ff', '#d8321a': '#55208f', '#7a1016': '#1c1024', '#ff3a1a': '#9b45ff'}, 'earth': {'#ffe14d': '#d9fff6', '#ff8a1c': '#7fe3d0', '#d8321a': '#c79a5b', '#7a1016': '#8a6236', '#ff3a1a': '#7fe3d0'}, 'water': {'#ffe14d': '#dff6ff', '#ff8a1c': '#7cc8ff', '#d8321a': '#2f7fe0', '#7a1016': '#1b4f99', '#ff3a1a': '#7cc8ff'}, 'aquarius': {'#ffe14d': '#ffffff', '#ff8a1c': '#b8ffc8', '#d8321a': '#39e75f', '#7a1016': '#14a03c', '#ff3a1a': '#b8ffc8'}, 'air': {'#ffe14d': '#ffffff', '#ff8a1c': '#e9eef4', '#d8321a': '#a3aebb', '#7a1016': '#39e75f', '#ff3a1a': '#e9eef4'}}}},
       fx=nfx('the genjutsu mark: three glowing motes circling slowly over the head (one turn per loop), bright in front of the head, dark crimson behind it', _halo(8)))),
 'kingsPosture': ('King\'s Posture', 3,
  'King\'s Posture (Leo taijutsu stance buff: a regal guard, FORT +30% for 3 rounds, holds firm), v4 (Christopher 2026-10-27: see it E facing; v3 turned to the viewer for a front double biceps): the fighter keeps its facing; from the guard it throws both upper arms up level, the near one forward and the far one back, and curls both fists up beside the head in a double biceps flex seen in profile, chest out, teeth clenched, squeezing the flex harder on the peak frame; a golden aura flares round it and a lion\'s mane of flame bursts up behind and round its head, blazing, as it holds the pose; then the mane settles to a proud glow and it drops back into the guard (the testbed keeps the buff, not the mane).', [
     g(),
     g(an=band(-60, -150), af=band(55, 150), bob=(0, 0, 0), lean=(0, 0)),
     g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)), g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)),
     g(an=KP_EN2, af=KP_EF2, bob=(0, -1, 0), lean=(0, -1)),
     g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)), g(an=KP_EN, af=KP_EF, bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-60, -150), af=band(55, 150), bob=(0, 0, 0), lean=(0, 0)),
     g()],
  [None, None, 'strain', 'strain', 'strain', 'strain', 'strain', None, None],
  [0, 0, 1, 3, 2, 2, 2, 1, 0],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'),
       anchored={2: [('mane1', 'head', 0, 0, {'behind': True})], 3: [('mane3', 'head', 0, -1, {'behind': True})], 4: [('mane4', 'head', 0, -1, {'behind': True})],
                 5: [('mane3b', 'head', 0, -1, {'behind': True})], 6: [('mane2', 'head', 0, 0, {'behind': True})], 7: [('mane1', 'head', 0, 0, {'behind': True, 'alpha': {'R': 140, 'O': 170}})]})),
 'sunPalm': ('Sun Palm', 4,
  'Sun Palm (Leo taijutsu strike: channels radiant energy into the palm, scorching whoever it touches, Burn 2 rounds): from the guard the fighter draws the rear hand back low beside the hip, palm open and turned forward, and a small sun kindles in it, white-hot at the heart, swelling and throwing out rays over two held frames while flame swirls up round the arm (v2, Christopher 2026-10-27: more fx); then it steps in and drives the open palm straight out at chest height, and the sun bursts on contact in a white-hot flash and a white-gold starburst with rays flashing out, a fire shock ring blasting out with cracks, then a broken ring of flame, flame licks and scattering embers; it settles back into the guard.', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='medium', rm='E: +2 stepping into the palm, -2 settling back',
       swirl={1: (0, 0.5), 2: (120, 0.8), 3: (240, 1.0)},   # v2: flame swirling round the drawn-back arm as the sun gathers
       impact={4: 0, 5: 1, 6: 2, 7: 3},                      # v2: white-hot flash, fire shock ring, cracks and embers on contact
       anchored={1: [('sunOrb3', 'hand', 0, 0)], 2: [('sunOrb4', 'hand', 0, 0)], 3: [('sunOrb5', 'hand', 0, 0), ('embers', 'hand', 0, -8)],
                 4: [('sunBurst2', 'hand', 3, 0), ('sunOrb4', 'hand', 2, 0)], 5: [('sunBurst3', 'hand', 4, 0), ('sunBurst1', 'hand', 3, 0)],
                 6: [('sunBurst3', 'hand', 6, 0, {'alpha': {'R': 150, 'O': 180}}), ('flame3', 'hand', 4, -4), ('flame2', 'hand', 7, 3), ('embers', 'hand', 2, -7)], 7: [('embers', 'hand', 6, -4), ('flame2', 'hand', 5, -2), ('embers', 'hand', 9, 3)]})),
 'battleRoar': ('Battle Roar', 3,
  'Battle Roar (Leo taijutsu debuff: an intimidating war cry that makes the foe second-guess itself, Slow 2 rounds, STR save DC 12): from the guard the fighter draws in a huge breath, rising, chest swelling, head back and fists pulled down to its sides; then it lunges its chest forward and roars at the foe, mouth wide, both hands flung down and back with fingers spread, and a lion\'s mane of flame bursts up round its head while golden roar waves blast out of its mouth one after another, widening as they go; it holds the roar, the mane blazing, then the mane dies down and it settles back into the guard.', [
     g(),
     g(an=band(10, -40), af=band(5, -40), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(10, -40), af=band(5, -40), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), root=(1, 0), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(-30, -100), af=band(-30, -105), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'roarE', 'roarE', 'roarE', 'roarE', None, None],
  [0, 0, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, hitbox=[44, 10, 16, 18], damage='light', rm='E: +1 lunging into the roar, -1 settling back', auraColors=('#ffe14d', '#ff8a1c'),
       shapes={'roarE': {'E': [[0, 0, '#000000'], [1, 0, '#000000'], [1, 4, '#000000'], [2, 4, '#000000'], [1, 5, '#70241d'], [2, 5, '#70241d']]}},
       anchored={3: [('mane3', 'head', -1, -1, {'behind': True}), ('roar1', 'head', 9, 2)],
                 4: [('mane4', 'head', -1, -1, {'behind': True}), ('roar2', 'head', 12, 2), ('roar1', 'head', 9, 2)],
                 5: [('mane3b', 'head', -1, -1, {'behind': True}), ('roar3', 'head', 17, 2), ('roar2', 'head', 12, 2)],
                 6: [('mane2', 'head', -1, 0, {'behind': True}), ('roar3d', 'head', 22, 2), ('roar2', 'head', 15, 2)],
                 7: [('mane1', 'head', -1, 0, {'behind': True, 'alpha': {'R': 140, 'O': 170}})]})),
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
 'solarLance': ('Solar Lance', 5,
  'Solar Lance (Leo ninjutsu, ranged: a focused beam of solar fire): from the guard the fighter makes the tiger seal at the chin, a spark of sunlight kindling between the hands; then it draws the near hand back low beside the hip, palm open, and a small sun gathers in it, white-hot and swelling over two held frames; then it steps in and thrusts two fingers straight out at shoulder height, and a lance of solar fire bursts from the fingertips toward the target, a white-hot core inside yellow, orange and a red rim, sparks spitting off its edges, a starburst flaring at the fingers and a backblast of flame off the shoulder, a gold aura flaring round the fighter (v2, Christopher 2026-10-27: more fx: flame swirling round the arm as the sun gathers, a thicker beam, sparks, backblast); the beam holds through a hit-stop, then narrows, flickers and breaks up into embers, and the fighter settles back into the guard (the testbed draws the beam on to the target from the release point).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 4), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='point'), af=band(30, -160), bob=(2, 2, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 3, 3, 2, 1, 0, 0],
  dict(fps=10, release=[57, 20], rm='E: +2 stepping into the thrust, -2 settling back', auraColors=('#ffe14d', '#ff8a1c'),
       swirl={2: (0, 0.5), 3: (120, 0.8), 4: (240, 1.0)},   # v2 (Christopher 2026-10-27: more fx): flame swirling round the drawn-back arm
       extra={'beam': {'rule': 'Solar Lance is a beam, not a projectile: on frames 5-8 the testbed draws the beam from the release point to the target (white core, yellow, orange, red rim; width 4, 4, 3, 2 px half-height, the last frame broken up), the clip itself draws it to the edge of the cell', 'frames': [5, 6, 7, 8], 'colors': ['#ffffff', '#ffe14d', '#ff8a1c', '#d8321a']}},
       anchored={1: [('sunOrb2', 'hand', 0, -1)], 2: [('sunOrb3', 'hand', 0, 0)], 3: [('sunOrb4', 'hand', 0, 0)], 4: [('sunOrb5', 'hand', 0, 0), ('embers', 'hand', 0, -8)],
                 5: [('sunBurst2', 'hand', 1, 0), ('flame3', 'hand', -27, -2), ('flame2', 'hand', -30, 4)], 6: [('sunBurst1', 'hand', 1, 0), ('flame2', 'hand', -28, -2), ('embers', 'hand', -32, 2)],
                 7: [('sunOrb3', 'hand', 1, 0), ('embers', 'hand', -29, -3)], 8: [('sunOrb2', 'hand', 1, 0)], 9: [('embers', 'hand', 6, -3), ('embers', 'hand', 12, 2)]},
       beam={5: (5, 'fire'), 6: (5, 'fire'), 7: (4, 'fire'), 8: (3, 'fade')})),
 'radiance': ('Radiance', 3,
  'Radiance (Leo ninjutsu stance buff: the fighter focuses its regal aura and it strengthens it as it radiates from the body, STR +10% for 3 rounds), v4 (Christopher 2026-10-27: see it E facing; v3 turned to the viewer, after a power-up reference: fists clenched at the sides, a towering spiky aura erupting from the ground): the fighter keeps its facing; from the guard it makes the seal at the chin, eyes closed; then it sinks into its stance and drives both clenched fists down beside the hips, elbows flared back, straining; a towering aura of golden light erupts from the ground round it, white-hot at the core, pale gold and gold through the body, orange at the tips of tall jagged spikes fanning up and out, a ring of light flaring on the floor at its feet; the aura roars and flickers as it holds the yell, then settles, the fighter rises back into the guard still radiant: a 2 px gold aura and motes of light drifting up off the body (the testbed keeps that look on every state until the buff ends).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, -1), **LOW) for _ in range(6)],
     g(),
     g(), g()],
  [None, 'closed', 'strain', 'roar', 'roar', 'roar', 'strain', 'strain', None, None, None],
  [0, 1, 1, 2, 3, 3, 3, 2, 2, 2, 2],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'),
       extra={'linger': {'rule': 'Radiance (Christopher 2026-10-27: a lingering aura for the duration of the ability): the clip ends still radiant; for the 3 rounds the buff lasts the testbed keeps drawing the fighter with a 2 px gold aura flickering on its outer ring and two or three gold motes drifting up off the shoulders and head, on every state it plays (the erupting aura is only in the cast); clears when the buff ends', 'aura': 2, 'auraColors': ['#ffe14d', '#ff8a1c'], 'motes': {'pattern': 'lightMote', 'colors': ['#ffffff', '#ffe14d', '#ff8a1c'], 'perFrame': 3}}},
       anchored={1: [('sunOrb1', 'hand', 0, -1)], 9: [('lightMote', 'head', -6, 4), ('lightMote', 'head', 7, 10), ('lightMote', 'head', 2, -9)], 10: [('lightMote', 'head', -7, 0), ('lightMote', 'head', 6, 6), ('lightMote', 'head', -2, -11)]},
       flare={'every': True, 2: 0, 3: 2, 4: 3, 5: 3, 6: 3, 7: 2, 8: 1})),
 'supernova': ('Supernova', 6,
  'Supernova (Leo ninjutsu ultimate: the fighter channels its inner light and releases an instant blinding detonation round itself, wide AoE on self, Blind 1 round), the Leo ultimate (longer and more dramatic, like Meteor), v2 (Christopher 2026-10-27: more build-up, the apex lasts longer; 16 frames, the cap, at 8 fps): from the guard the fighter makes the seal and sinks deeper and deeper over five frames, trembling, straining, while motes of light stream in toward it from all round and a gold aura swells; it turns to face the viewer (every facing turns S for the release, as Blast Wave) with the seal pressed to the chest and a star kindling at its heart, swelling and blazing over two frames, the whole body beginning to glow; then it throws its arms out wide and the light detonates: a white flash swallows the fighter and the whole cell and pulses, held over three frames, then a ring of light blasts outward, white, then yellow, orange and red as it widens and breaks up, a second ring behind it and sun rays scattering, embers raining down; the glow drains off the body, it brings the hands back in and turns back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 2), root=(1, 0), **BRACE),
     g(bob=(2, 2, 2), root=(-1, 0), **LOW),
     g(bob=(1, 1, 1), **LOW),
     g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)), g(bob=(0, -1, 0)),
     g(),
     g()],
  [None, 'squint', 'pain', 'pain', 'pain', 'pain', 'strain', 'strain', 'roar', 'roar', 'roar', 'roar', 'roar', 'squint', None, None],
  [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1, 0],
  dict(fps=8, auraColors=('#ffe14d', '#ff8a1c'),
       front={6: dict(R=(-20, 205, 0.8, 'front'), L=(20, -205, 0.8, 'front')), 7: dict(R=(-20, 205, 0.8, 'front'), L=(20, -205, 0.8, 'front')),   # the seal pressed to the chest, facing the viewer
              **{k: dict(R=(110, 105, 1, 'front'), L=(-110, -105, 1, 'front')) for k in (8, 9, 10, 11, 12, 13)},   # arms thrown out wide
              14: dict(R=stances.GA['R'], L=stances.GA['L'])},
       gather={1: 0, 2: 1, 3: 2, 4: 3, 5: 3},
       nova={6: 'core', 7: 'core2', 8: 'flash', 9: 'flash2', 10: 'flash', 11: 0, 12: 1, 13: 2, 14: 4})),
 'leashKick': ('Leash Kick', 10,
  'Leash Kick (Sagittarius taijutsu strike, Physical 12, Live Tier A: the fighter pirouettes violently before throwing out a heel kick at blazing speed): from the guard the fighter tucks both arms tight and whips round in two full pirouettes on the lead foot (the approved spin pivot, twice), a ring of fire whirling round its legs that grows with each turn, black and purple flames flickering in it; v2 (Christopher 2026-10-27: the kick more of an axe kick): coming out of the second turn it swings the rear leg up straight in front, high over its head, torso leaning back, then chops the heel straight down onto the target, a streak of fire following the heel down; flame bursts off the heel as it lands on the target\'s head and shoulder, purple and black licks trailing along the leg, embers scattering at the floor; the leg sets down and it steps back into the guard.', [
     g(),
     g(an=TUCK_SPIN_N, af=TUCK_SPIN_F, bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=TUCK_SPIN_N, af=TUCK_SPIN_F, bob=(1, 1, 1), lean=(0, 0)) for _ in range(6)],
     g(an=band(10, -40), af=band(-60, -80), bob=(1, 1, 1), lean=(0, -1), ln='hk-swing', lf='lk-lead-pivot'),
     g(an=band(30, -20), af=band(-80, -100), bob=(0, 0, 1), lean=(-1, -5), ln='lk-axe-top', lf='lk-lead-pivot'),
     g(an=band(10, -40), af=band(-60, -80), bob=(1, 1, 2), lean=(1, 3), root=(1, 0), ln='lk-axe-chop', lf='lk-lead-pivot'),
     g(an=band(0, -50), af=band(-50, -70), bob=(2, 2, 3), lean=(1, 5), ln='lk-axe-down', lf='lk-lead-pivot'),
     g(bob=(1, 1, 1), lean=(0, 1), root=(-1, 0), ln='hk-drop'),
     g()],
  [None, 'squint'] + ['squint'] * 7 + ['squint', 'squint', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 18, 14, 24], damage='medium', rm='E: +1 chopping down, -1 setting down',
       extra={'borrow': {'rule': copy.deepcopy(HEAVY['borrow']['rule']) + '; Leash Kick spins twice (E -> S, W, N, then S, W, N again)',
                         'frames': {'2': SPIN('S', 0), '3': SPIN('W', 0), '4': SPIN('N', 1), '5': SPIN('S', 0), '6': SPIN('W', 0), '7': SPIN('N', 1)}}},
       spinFire={2: (0, 130, 0), 3: (0, 250, 0), 4: (0, 360, 1), 5: (0, 360, 1), 6: (0, 360, 2), 7: (0, 360, 2), 8: (0, 360, 3)},
       fx=nfx('Sagittarius fire (reds, oranges, yellows with select black and purple flames): flame bursting off the heel on contact, purple and black licks trailing back along the leg',
              [(9, [('pflame1', [41, 22]), ('flame1', [38, 26])]),
               (10, [('flame2', [47, 41]), ('flame1', [46, 34]), ('pflame2', [42, 30]), ('flame1', [40, 25])]),
               (11, [('flame3', [43, 56]), ('pflame2', [48, 54]), ('flame2', [44, 47]), ('pembers', [50, 46]), ('embers', [38, 50])]),
               (12, [('embers', [44, 60]), ('pembers', [49, 58])])]))),
 'spinningTop': ('Spinning Top', 6,
  'Spinning Top (Sagittarius taijutsu strike, Physical 8, Melee, target Chakra -15: the fighter spins on its head while twirling its legs in a wide V fast enough to ignite the air): from the guard the fighter drops into a crouch and dives forward onto its hands and head, kicking its legs up together; turned upside down on its head with both hands braced on the floor beside it, it throws its legs open into a wide V and spins, the V flashing open and closed as it turns (open, edge-on, open from behind, edge-on), the air at its whirling feet catching fire: flames streaming off both feet, a ring of fire whirling round the V at foot height with black and purple licks in it, sparks round its head on the floor; it snaps the legs together, rolls back down into the crouch and rises into the guard.', [
     g(),
     g(an=band(-40, -80), af=band(-30, -70), bob=(2, 2, 3), lean=(1, 4), **LOW),
     g(an=band(-25, -40), af=band(-15, -35), bob=(3, 3, 3), lean=(2, 6), **BRACE),
     g(an=ST_AN, af=ST_AF, bob=(0, 0, 0), lean=(0, 0), **ST_T),
     *[g(an=ST_AN, af=ST_AF, bob=(0, 0, 0), lean=(0, 0), **(ST_V if k % 2 == 0 else ST_N)) for k in range(9)],
     g(an=ST_AN, af=ST_AF, bob=(0, 0, 0), lean=(0, 0), **ST_T),
     g(an=band(-25, -40), af=band(-15, -35), bob=(3, 3, 3), lean=(1, 4), **BRACE),
     g()],
  [None, None, 'squint'] + ['squint'] * 11 + ['squint', None],
  None,
  dict(fps=12, hitbox=[14, 0, 36, 40], damage='light', rm='none (spins in place)',
       invert={3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0, 9: 0, 10: 1, 11: 1, 12: 0, 13: 0},
       topFire={3: 0, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 1, 13: 0})),
 'wispFire': ('Wisp Fire', 4,
  'Wisp Fire (Sagittarius ninjutsu, Elemental 10, Ranged, target Chakra -20: the caster conjures a barrage of small purple flames that sap the chakra from the foe with each hit): from the guard the fighter makes the seal at the chin, a purple spark kindling between the hands; it opens the near hand palm up at the chest and small purple and black flames flicker alight and circle it, a dim purple aura breathing round the fighter; then it pushes the palms out at the target one after the other, near, far, near, far, and with each push a wisp of purple flame with a white-hot head and a black tail flies off toward the target, four in a stream; the last wisp leaves a puff of purple sparks at the palm and the fighter settles back into the guard (the testbed flies the four wisps on to the target from the release point).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -95, fistKind='palm'), af=band(-50, -110), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -95, fistKind='palm'), af=band(-50, -110), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), af=band(-88, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), af=band(-88, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-45, -110), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', None, None, 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, release=[56, 22], rm='E: +1 into the pushes, -1 settling back', auraColors=('#9b45ff', '#55208f'),
       extra={'projectile': {'rule': 'Wisp Fire is a barrage: on frames 4, 5, 6 and 7 the testbed launches one small purple wisp (pwisp, white-hot head, purple body, black tail) from the release point to the target, four in all; each that lands puffs purple sparks and pulls a few chakra-blue motes out of the target (Chakra -20 over the barrage)', 'frames': [4, 5, 6, 7], 'count': 4, 'pattern': 'pwisp', 'colors': ['#ffffff', '#9b45ff', '#55208f', '#1c1024']}},
       anchored={1: [('pspark', 'hand', 0, -2), ('pflame1', 'hand', 0, -6)],
                 2: [('pflame2', 'hand', -1, -5), ('pflame1', 'hand', -6, -1), ('pflame1', 'hand', 5, 1)],
                 3: [('pflame2', 'hand', 4, -5), ('pflame2', 'hand', -5, -2), ('pflame1', 'hand', 2, 3), ('pembers', 'hand', 0, -10)],
                 4: [('pspark', 'hand', 1, 0), ('pwisp', 'feet', 22, -42), ('pflame1', 'feet', 2, -30)],
                 5: [('pspark', 'hand', 1, 0), ('pwisp2', 'feet', 22, -41), ('pwisp', 'feet', 28, -44)],
                 6: [('pspark', 'hand', 1, 0), ('pwisp', 'feet', 22, -42), ('pwisp2', 'feet', 28, -40)],
                 7: [('pspark', 'hand', 1, 0), ('pwisp2', 'feet', 22, -41), ('pwisp', 'feet', 28, -44), ('pembers', 'hand', -3, -5)],
                 8: [('pembers', 'hand', 2, -3)]})),
 'cauterize': ('Cauterize', 4,
  'Cauterize (Sagittarius ninjutsu, self heal 15: the fighter channels its inner fire to seal its own wounds shut): from the guard the fighter makes the seal at the chin, then presses the open near palm flat against its own ribs, the far fist clenched low; it grits its teeth as the palm heats up, then fire flares out from under the hand, orange and yellow with black and purple licks, embers spitting and a warm aura flaring round the body; it holds the burn through the strain, the flame dying to a glow as heat shimmers rise; then it takes the hand away with a breath, a wisp of smoke curling up off the sealed wound and a few warm motes rising, and settles back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(25, -60, fistKind='palm'), af=band(-20, -60), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(25, -60, fistKind='palm'), af=band(-15, -50), bob=(2, 2, 2), lean=(0, 2)),
     g(an=band(25, -60, fistKind='palm'), af=band(-15, -50), bob=(2, 2, 3), lean=(-1, 3)),
     g(an=band(25, -60, fistKind='palm'), af=band(-15, -50), bob=(2, 2, 3), lean=(-1, 3)),
     g(an=band(25, -60, fistKind='palm'), af=band(-20, -60), bob=(2, 2, 2), lean=(0, 2)),
     g(an=band(-5, -70, fistKind='palm'), af=band(-25, -70), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-35, -100), af=band(-30, -95), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'squint', None, None, None],
  [0, 0, 0, 1, 2, 2, 1, 0, 0, 0],
  dict(fps=8, auraColors=FIRE_AURA,
       anchored={2: [('heat', 'hand', 0, -4)],
                 3: [('flame1', 'hand', 0, -3), ('embers', 'hand', 2, -7)],
                 4: [('flame3', 'hand', 0, -4), ('pflame1', 'hand', -3, -2), ('embers', 'hand', 4, -9), ('pembers', 'hand', -4, -10)],
                 5: [('flame2', 'hand', 1, -3), ('pflame2', 'hand', -3, -4), ('embers', 'hand', 3, -10)],
                 6: [('flame1', 'hand', 0, -2), ('heat', 'hand', 0, -6), ('heat', 'hand', -2, -11), ('pembers', 'hand', 3, -9)],
                 7: [('smoke1', 'hand', 0, -4), ('heat', 'hand', 1, -9), ('lightMote', 'head', -6, 6), ('lightMote', 'head', 7, 10)],
                 8: [('smoke2', 'hand', 0, -8), ('lightMote', 'head', -7, 0), ('lightMote', 'head', 6, 3)]})),
 'dogma': ('Dogma', 4,
  'Dogma (Sagittarius genjutsu, debuff: the caster projects its own beliefs into the foe\'s mind on a constant loop until it cannot tell its own thoughts from the caster\'s; Confusion 2 rounds, INT save DC 13; range Zone of Awareness): from the guard the fighter lifts two fingers to its temple, eyes narrowing, and its own conviction starts to loop: purple motes circling over its head on a dotted ring, the eyes kindling purple then flaring white-hot; then it thrusts the two fingers out at the target, and purple waves of belief roll out from the eyes one after another, white at the core, purple and black at the rim, each one wider, the loop over its head still turning; the motes and the glow fade and the hand drops back into the guard (the target takes the genjutsu mark, genjutsuAfflicted in Sagittarius colours, for the Confusion).', [
     g(),
     g(an=band(-115, -195, fistKind='point'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     *[g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(5)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#9b45ff', '#1c1024'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (Sagittarius colours, genjutsuMark.recolor.sagittarius) and keeps it until the Confusion ends', 'state': 'genjutsuAfflicted', 'element': 'sagittarius'}},
       anchored={1: _loop(0)[:4],
                 2: _loop(1) + [('eyeP', 'eye', 0, 0)],
                 3: _loop(2) + [('eyePF', 'eye', 0, 0)],
                 4: _loop(3) + [('eyePF', 'eye', 0, 0), ('dog1', 'eye', 6, 0)],
                 5: _loop(4) + [('eyePF', 'eye', 0, 0), ('dog2', 'eye', 10, 1), ('dog1', 'eye', 6, 0)],
                 6: _loop(5) + [('eyePF', 'eye', 0, 0), ('dog3', 'eye', 15, 2), ('dog2', 'eye', 10, 1), ('dog1', 'eye', 6, 0)],
                 7: _loop(6) + [('eyeP', 'eye', 0, 0), ('dog3d', 'eye', 20, 3), ('dog3', 'eye', 15, 2), ('dog2', 'eye', 10, 1)],
                 8: [it for it in _loop(7) if it[0] != 'dotP'] + [('dog3d', 'eye', 21, 3)],
                 9: [it for it in _loop(0) if it[0] == 'moteP']})),
 'soulPressure': ('Soul Pressure', 4,
  'Soul Pressure (Sagittarius genjutsu, debuff: the caster blankets the foe\'s mind with its spiritual energy, silencing its innermost thoughts; Silence 3 rounds, STR save DC 12; range Zone of Awareness): from the guard the fighter lowers its hands and closes its eyes, gathering itself, and a heavy aura of dark purple and black spirit-flame rises round it, wisps curling up off the shoulders; its eyes snap open, burning purple, and it extends the open near palm toward the target and presses it slowly down, the far hand low at its side, as heavy dome-shaped waves of spirit pressure roll out toward the target, bearing down and sinking as they travel, purple at the crown and black at the rim; it holds the press, then the aura settles and it returns to the guard (the target takes the genjutsu mark, genjutsuAfflicted in Sagittarius colours, for the Silence).', [
     g(),
     g(an=band(-20, -50), af=band(-10, -40), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-10, -30), af=band(-5, -25), bob=(2, 2, 2), lean=(0, 0)),
     g(an=band(-90, -100, fistKind='palm'), af=band(-5, -25), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-75, -65, fistKind='palm'), af=band(-5, -25), bob=(1, 1, 2), lean=(1, 2)),
     g(an=band(-65, -55, fistKind='palm'), af=band(-5, -25), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-65, -55, fistKind='palm'), af=band(-5, -25), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-65, -55, fistKind='palm'), af=band(-5, -25), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-40, -110), af=band(-25, -90), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, 'closed', 'closed', None, 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 2, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#55208f', '#1c1024'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (Sagittarius colours, genjutsuMark.recolor.sagittarius) and keeps it until the Silence ends', 'state': 'genjutsuAfflicted', 'element': 'sagittarius'}},
       anchored={1: [('spWisp', 'head', -6, 12)],
                 2: [('spWisp', 'head', -7, 10), ('spWisp', 'head', 6, 12), ('pflame1', 'head', -1, -9)],
                 3: [('eyePF', 'eye', 0, 0), ('pflame2', 'head', -1, -10), ('spWisp', 'head', -8, 8), ('spWisp', 'head', 7, 10)],
                 4: [('eyePF', 'eye', 0, 0), ('pflame2', 'head', 0, -10), ('sp1', 'feet', 14, -30), ('spWisp', 'head', -7, 6)],
                 5: [('eyePF', 'eye', 0, 0), ('pflame1', 'head', 0, -9), ('sp2', 'feet', 19, -24), ('sp1', 'feet', 14, -30), ('spWisp', 'head', 7, 8)],
                 6: [('eyePF', 'eye', 0, 0), ('pflame2', 'head', 0, -10), ('sp3', 'feet', 24, -17), ('sp2', 'feet', 19, -24), ('spWisp', 'head', -7, 5)],
                 7: [('eyeP', 'eye', 0, 0), ('sp3d', 'feet', 27, -10), ('spWisp', 'head', 6, 4)],
                 8: [('spWisp', 'head', -6, 2, {'alpha': {'K': 140, 'p': 140, 'P': 160}})]})),
 'mountainStance': ('Mountain Stance', 3,
  'Mountain Stance (Taurus taijutsu stance buff, FORT +30% 3 rounds: the fighter stamps its feet into the ground, demonstrating its unshakeable resolve): from the guard the fighter drops its hands and lifts the lead knee high, then stamps the foot down hard into the floor (sumo shiko), cracks splitting out from the heel, dust and stones jumping; it shifts onto that leg, lifts the rear knee and stamps again; then it sinks into a deep, wide stance with the fists pulled back to the hips, elbows back, and an earthen aura settles round it, brown with flecks of crystal glinting in it and small teal crystal shards pushing up out of the cracks; it holds, rooted, then rises back into the guard.', [
     g(),
     g(an=band(15, -40), af=band(5, -35), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -80), af=band(40, -20), bob=(0, 0, 0), lean=(0, -1), lf='ms-lift-lead'),
     g(an=band(20, -30), af=band(10, -30), bob=(3, 3, 3), lean=(1, 2), ln='ms-wide-rear', lf='ms-wide-lead'),
     g(an=band(40, -20), af=band(-30, -80), bob=(1, 1, 1), lean=(0, 1), ln='ms-lift-rear', lf='ms-wide-lead'),
     g(an=band(20, -30), af=band(10, -30), bob=(3, 3, 3), lean=(1, 2), ln='ms-wide-rear', lf='ms-wide-lead'),
     *[g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), ln='ms-wide-rear', lf='ms-wide-lead') for _ in range(4)],
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, None, 'squint', 'strain', 'squint', 'strain', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'),
       anchored={3: [('crack1', 'feet', 9, -1), ('dust2', 'feet', 6, -3), ('rocks', 'feet', 10, -8)],
                 4: [('crack1', 'feet', 9, -1), ('dust1', 'feet', 7, -5), ('rocks', 'feet', 12, -12)],
                 5: [('crack2', 'feet', 0, -1), ('dust2', 'feet', -6, -3), ('dust1', 'feet', 7, -6), ('rocks', 'feet', -10, -9)],
                 6: [('crack2', 'feet', 0, -1), ('crystT', 'feet', -9, -3), ('crystT', 'feet', 10, -3), ('dust1', 'feet', -7, -6), ('cryst', 'head', -9, 14)],
                 7: [('crack2', 'feet', 0, -1), ('crystT', 'feet', -9, -3), ('crystT', 'feet', 10, -3), ('cryst', 'feet', 13, -5), ('cryst', 'head', 9, 8)],
                 8: [('crack2', 'feet', 0, -1), ('crystT', 'feet', -9, -3), ('crystT', 'feet', 10, -3), ('cryst', 'feet', -13, -5), ('cryst', 'head', -8, 4)],
                 9: [('crack2', 'feet', 0, -1, {'alpha': {'E': 160, 'K': 160}}), ('crystT', 'feet', 10, -3, {'alpha': {'c': 150, 'C': 150}}), ('cryst', 'head', 9, 2)],
                 10: [('crack1', 'feet', 0, -1, {'alpha': {'E': 110, 'K': 110}})]})),
 'ironFist': ('Iron Fist', 5,
  'Iron Fist (Taurus taijutsu strike, Physical 16, can Slow 1 round: the fighter focuses its iron will into its fist before punching): from the guard the fighter sits its weight back and draws the rear fist back beside the ear, elbow high, the lead hand out to measure; crystal and earth swirl round the cocked arm, a ring of soil-brown grit with teal crystal at its head winding tighter over three held frames, crystal glints sparking on the knuckles; then it steps in and drives the fist dead straight through the target, rear heel turning up; on contact a crystal-white flash bursts at the fist, a shock ring of teal and brown blasts out, cracks shoot off, stone chips and crystal shards scatter and dust puffs; then it pulls back into the guard.', [
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
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 on the step into the punch, -1 settling back',
       swirl={1: (0, 0.35), 2: (100, 0.6), 3: (210, 0.85), 4: (320, 1.0)},
       impact={5: 0, 6: 1, 7: 2, 8: 3}, recolor=EARTH_RECOLOR, keepFx=True,
       anchored={3: [('cryst', 'hand', 0, 0)], 4: [('cryst', 'hand', 1, -1), ('crystT', 'hand', -3, 2)],
                 6: [('dust1', 'hand', -2, 6), ('rocks', 'hand', 6, -6)], 7: [('dust2', 'hand', 2, 7), ('rocks', 'hand', 9, 4)]})),
 'bullRush': ('Bull Rush', 11,
  'Bull Rush (Taurus taijutsu gap closer, Physical 14, Melee (Reach +4m), Priority, movement credit +6: the fighter adopts a sprinter\'s stance before charging with reckless abandon into its opponent): from the guard the fighter drops into a low sprinter\'s set, knees deep, body pitched forward, arms hanging low, and paws the ground with the rear foot, grit spitting back; then it bursts into the approved sprint head down, both arms reaching forward ahead of it (v2, Christopher 2026-10-28: arms forward, not swept back), dust and stones exploding off the floor at every stride and a cloud of dust boiling up behind it, the motion streak in dust browns; on the last stride it tucks both arms tight, drops its head and rams the lead shoulder through the target like a bull, a burst of rock chips and dust and a few teal crystal shards at the point of impact; then it straightens back into the guard. The fighter travels 40 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=band(-20, -30), af=band(-25, -35), bob=(4, 4, 4), lean=(2, 9), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=band(-20, -30), af=band(-25, -35), bob=(4, 4, 4), lean=(2, 10), ln='ml-dip-rear', lf='ml-dip-lead')] + [
     g(an=band(-70 + 6 * (k % 2), -80 + 6 * (k % 2)), af=band(-76 + 6 * ((k + 1) % 2), -86 + 6 * ((k + 1) % 2)), bob=(SPRINT_DY[k] + 1,) * 3, lean=(1, 10), root=(6, 0), ln='sr-' + SPRINT_LEGS[k], lf='sr-' + SPRINT_LEGS[(k + 4) % 8]) for k in range(6)] + [   # v2 (Christopher 2026-10-28): arms reaching forward through the sprint, not swept back
     g(an=TUCK_N, af=TUCK_F, bob=(3, 3, 3), lean=(2, 9), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=TUCK_N, af=TUCK_F, bob=(2, 2, 2), lean=(2, 8), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(1, 1, 2), lean=(1, 3)),
     g()],
  [None, 'squint', 'strain', 'strain'] + ['strain'] * 6 + ['strain', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='medium', rm='E: 6 px a stride through the sprint, +3 and +1 into the ram; 40 px in all (travel)',
       blur={k: 9 for k in range(4, 10)} | {10: 7, 11: 4}, trail=DUST_TRAIL,
       fx=nfx('earth (soil browns with teal crystal): grit pawed back, dust and stones bursting off the floor at every stride, a cloud of dust behind, rock chips and crystal shards where the shoulder lands',
              [(3, [('dust1', [14, 63]), ('rocks', [9, 59])])] + [(k, _dustkick(SPRINT_LEGS[k - 4], k) + _dustkick(SPRINT_LEGS[(k + 0) % 8], k + 1) + DUST_WAKE[k % 2]) for k in range(4, 10)] +
              [(10, [('rocks', [48, 30]), ('dust2', [44, 36]), ('cryst', [50, 25]), ('dust1', [38, 63])] + DUST_WAKE[0][:2]), (11, [('rocks', [50, 27]), ('crystT', [47, 22]), ('dust1', [46, 34])]), (12, [('dust1', [46, 63])])]),
       extra={'travel': {'rule': 'Bull Rush is a gap closer: the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}})),
 'oakFlesh': ('Oak Flesh', 4,
  'Oak Flesh (Taurus ninjutsu self buff, FORT +50% 3 rounds: the fighter steadies itself and focuses its will to harden its skin): from the guard the fighter makes the seal at the chin and sinks a little into its knees, eyes closing, an earthen aura rising round it; then it drives its fists down beside its hips, elbows back, and its skin hardens into oak (v2, Christopher 2026-10-28: the bark more opaque, about 88%): a warm honey-gold oak spreads over all its skin, streaked with dark walnut grain (face included) and patched with moss, its hair turning to moss, and dark wood grain stands out down the arms and neck, wood chips and dust shaken off it and teal crystal glints flashing on the hardened skin; it holds, unmoving, then rises back into the guard still clad in bark (the spec asks the testbed to keep the bark tint and grain while the buff lasts).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 3), lean=(0, 0), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'closed', 'closed', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'), tint={3: 80, 4: 160, 5: 225, 6: 225, 7: 225, 8: 225, 9: 225}, veins=(4, 5, 6, 7, 8, 9), tintColors=((0xd8, 0xa2, 0x48), (0x1e, 0x10, 0x08), (0x4a, 0x2c, 0x18), (0x7d, 0x86, 0x3c)), hairTo={'frames': [4, 5, 6, 7, 8, 9], 'map': {'#3f0505': '#2f3812', '#702219': '#55602a', '#70241d': '#55602a', '#9e4a31': '#7d863c'}},
       extra={'linger': {'rule': 'Oak Flesh (FORT +50% 3 rounds): the clip ends with the skin hardened into oak; while the buff lasts the testbed keeps drawing the fighter with the bark tint (honey oak #d8a248 at alpha 225 over skin pixels, with dark walnut grain streaks #4a2c18 (over the face too) and patches of moss #7d863c off the face, the hair turned to moss (hair ramp #3f0505/#702219/#70241d/#9e4a31 -> #2f3812/#55602a/#55602a/#7d863c), deep grain #1e1008; v2 more opaque, v3 grain streaks so it reads on the darkest skin tone, v4 honey oak instead of the v3 grey, which read as zombie skin, v5 honey oak + walnut grain + moss combined, v6 grain on the face and moss hair; Christopher 2026-10-28) and the deep wood grain (#1e1008), on every state it plays; clears when the buff ends', 'tint': ['#d8a248', 225], 'veins': '#1e1008', 'streak': ['#4a2c18', '(x + floor(y / 3)) % 3 == 0, skin pixels off the face'], 'hair': {'#3f0505': '#2f3812', '#702219': '#55602a', '#70241d': '#55602a', '#9e4a31': '#7d863c'}, 'moss': ['#7d863c', '(floor(x / 2) * 5 + floor(y / 2) * 11) % 7 == 0, skin pixels off the face']}},
       anchored={4: [('rocks', 'head', -8, 20), ('dust1', 'feet', -6, -2), ('dust1', 'feet', 7, -2)],
                 5: [('cryst', 'head', 6, 16), ('rocks', 'head', 8, 26), ('crystT', 'head', -7, 22)],
                 6: [('cryst', 'head', -6, 24), ('crystT', 'head', 7, 12)],
                 7: [('cryst', 'head', 5, 28)]})),
 'ironwoodKanabo': ('Ironwood Kanabo', 6,
  'Ironwood Kanabo (Taurus ninjutsu, STR +20% 3 rounds, unlocks the Kanabo weapon style kit: the fighter materialises its iron will into a towering studded club), v2 (Christopher 2026-10-28: the club rises from the earth; redesigned after his reference): from the guard the fighter makes the seal at the chin, then sweeps both palms down low, facing the floor, and the ground in front of it cracks, dust and stones jumping; it draws its palms up and the club rises out of the crack head first: a long dark iron kanabo with rows of spikes down both sides and studs between them, a rounded cap, a tapered cone neck, a cord-wrapped grip and an iron ring at the pommel; as the grip clears the floor the fighter closes its near fist round it and lifts it free, dust and stone shaking off; then it returns to the guard (a kanabo weapon layer and Kanabo stance idle are the next step for holding it).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-30, -45, fistKind='palm'), af=band(-35, -50, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-30, -45, fistKind='palm'), af=band(-35, -50, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-45, -80, fistKind='palm'), af=band(-50, -85, fistKind='palm'), bob=(2, 2, 2), lean=(1, 2), **LOW),
     g(an=band(-60, -110, fistKind='palm'), af=band(-65, -115, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-55, -70), af=band(-40, -100), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-55, -70), af=band(-40, -100), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-40, -110), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', None, None, None, None],
  [0, 0, 1, 1, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'),
       extra={'weapon': {'rule': 'Ironwood Kanabo summons the Kanabo (Taurus): the cast draws the club as fx (rising from the floor, then in the near fist); holding it afterwards needs a kanabo weapon layer and a Kanabo stance idle (to author once the cast is approved)', 'item': 'kanabo'}},
       kanaboRise={3: 8, 4: 20, 5: 32, 6: 'grip', 7: 'grip'},
       anchored={2: [('crack1', 'feet', 13, -1), ('dust1', 'feet', 13, -3), ('rocks', 'feet', 17, -8)],
                 3: [('crack2', 'feet', 13, -1), ('dust2', 'feet', 13, -3), ('rocks', 'feet', 9, -10), ('rocks', 'feet', 18, -14)],
                 4: [('crack2', 'feet', 13, -1), ('dust2', 'feet', 13, -2), ('rocks', 'feet', 17, -24)],
                 5: [('crack2', 'feet', 13, -1), ('dust1', 'feet', 13, -2), ('rocks', 'feet', 9, -30)],
                 6: [('crack1', 'feet', 13, -1), ('dust1', 'feet', 13, -2), ('rocks', 'hand', 3, 12)],
                 7: [('crack1', 'feet', 13, -1, {'alpha': {'K': 130, 'E': 130}})]})),
 'rootSanctuary': ('Root Sanctuary', 5,
  'Root Sanctuary (Taurus ninjutsu self buff, FORT +20% 2 rounds: the fighter forms a rooted earthen sanctuary around itself, reinforcing its body), v2 (Christopher 2026-10-28: more root hairs on the rising roots): from the guard the fighter makes the seal at the chin and sinks into its knees, eyes closing, an earthen aura rising round it; then it drives both fists down beside its hips and the floor cracks open either side of it: two gnarled roots burst up out of the cracks, rootlets kicking out sideways and runners spreading along the floor, and climb either side of the fighter, arching inward over its head until they meet in a dome, teal crystal budding along them as they close; it holds inside the sanctuary, unmoving, crystal glinting, then the roots sink back into the floor and it rises back into the guard (the spec proposes a faint ring of roots at the feet while the buff lasts).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     *[g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW) for _ in range(7)],
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'),
       extra={'linger': {'rule': 'Root Sanctuary (FORT +20% 2 rounds), proposal: while the buff lasts the testbed draws a faint ring of roots on the floor round the fighter (the crack2 floor pattern in soil browns, alpha 150, behind the fighter); clears when the buff ends', 'pattern': 'crack2', 'alpha': 150}},
       anchored={3: [('crack2', 'feet', 0, -1), ('sanct20', 'feet', 0, SANCT_DY, {'behind': True}), ('dust1', 'feet', -14, -3), ('dust1', 'feet', 14, -3), ('rocks', 'feet', 16, -8)],
                 4: [('crack2', 'feet', 0, -1), ('sanct45', 'feet', 0, SANCT_DY, {'behind': True}), ('dust2', 'feet', 14, -3), ('rocks', 'feet', -17, -10)],
                 5: [('crack2', 'feet', 0, -1), ('sanct70', 'feet', 0, SANCT_DY, {'behind': True}), ('dust1', 'feet', -15, -4)],
                 6: [('crack2', 'feet', 0, -1), ('sanct90', 'feet', 0, SANCT_DY, {'behind': True}), ('cryst', 'feet', 12, -24)],
                 7: [('crack2', 'feet', 0, -1), ('sanct100', 'feet', 0, SANCT_DY, {'behind': True}), ('glint', 'head', 0, -10), ('cryst', 'feet', -13, -30)],
                 8: [('crack2', 'feet', 0, -1), ('sanct100', 'feet', 0, SANCT_DY, {'behind': True}), ('cryst', 'feet', 13, -18), ('glit', 'head', -9, -4)],
                 9: [('crack2', 'feet', 0, -1, {'alpha': {'E': 170, 'K': 170}}), ('sanct70', 'feet', 0, SANCT_DY, {'behind': True, 'alpha': {'E': 170, 'e': 170, 'K': 170}}), ('dust1', 'feet', 14, -3)],
                 10: [('crack1', 'feet', 0, -1, {'alpha': {'E': 120, 'K': 120}}), ('sanct20', 'feet', 0, SANCT_DY, {'behind': True, 'alpha': {'E': 110, 'e': 110, 'K': 110}})]})),
 'materialFixation': ('Material Fixation', 4,
  'Material Fixation (Taurus genjutsu, mental debuff: the caster forces an obsession on the foe, so it drops everything and loses focus on the fight; Disarm 3 rounds, INT save DC 12; range ~12 m): from the guard the fighter opens the near hand palm up in front of its chest, the far hand low, and an illusory crystal gem forms out of a glint in the palm, growing and faceting, teal with a white highlight and sparkling; its eyes kindle crystal teal; it lifts the palm and offers the gem out toward the target, and the gem\'s image drifts off the palm toward the foe trailing glitter while waves of crystal-teal fascination roll out from the eyes, each one wider; the gem fades out of sight near the target, the glow dies and the hand drops back into the guard (the target takes the genjutsu mark, genjutsuAfflicted in earth colours, for the Disarm).', [
     g(),
     g(an=band(-40, -100, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-40, -100, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-55, -95, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=band(-80, -90, fistKind='palm'), af=band(-10, -40), bob=(1, 1, 1), lean=(1, 3)) for _ in range(4)],
     g(an=band(-50, -110), af=band(-25, -90), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (earth colours, genjutsuMark.recolor.earth) and keeps it until the Disarm ends', 'state': 'genjutsuAfflicted', 'element': 'earth'}},
       anchored={1: [('gem1', 'hand', 1, -4)],
                 2: [('gem2', 'hand', 1, -5), ('glit', 'hand', -3, -9), ('eyeC', 'eye', 0, 0)],
                 3: [('gem3', 'hand', 1, -6), ('glint', 'hand', 4, -11), ('eyeCF', 'eye', 0, 0)],
                 4: [('gem3', 'hand', 5, -5), ('glit', 'hand', 0, -4), ('eyeCF', 'eye', 0, 0), ('fix1', 'eye', 6, 0)],
                 5: [('gem2', 'hand', 11, -4), ('glit', 'hand', 5, -3), ('glit', 'hand', 0, -6, {'alpha': {'c': 150, 'W': 170}}), ('eyeCF', 'eye', 0, 0), ('fix2', 'eye', 10, 1), ('fix1', 'eye', 6, 0)],
                 6: [('gem2', 'hand', 17, -3, {'alpha': {'c': 190, 'C': 190, 'T': 190, 'W': 210}}), ('glit', 'hand', 11, -2), ('eyeCF', 'eye', 0, 0), ('fix3', 'eye', 15, 2), ('fix2', 'eye', 10, 1), ('fix1', 'eye', 6, 0)],
                 7: [('gem1', 'hand', 22, -2, {'alpha': {'c': 140, 'C': 140, 'T': 140}}), ('glit', 'hand', 17, -1, {'alpha': {'c': 140, 'W': 150}}), ('eyeC', 'eye', 0, 0), ('fix3d', 'eye', 20, 3), ('fix3', 'eye', 15, 2)],
                 8: [('fix3d', 'eye', 21, 3, {'alpha': {'C': 140, 'T': 140}})]})),
 'planetaryPressure': ('Planetary Pressure', 4,
  'Planetary Pressure (Taurus genjutsu, mental debuff: the caster exerts its will on the foe\'s mind so it perceives gravity as twice as strong; Slow 2 rounds, STR save DC 13; range ~12 m): from the guard the fighter raises the near hand high, palm up, and an illusory planet forms just in front of it, soil brown with a ring of teal crystal, swelling over two frames while the eyes kindle crystal teal; then it closes the hand into a fist and drags it down hard in front of itself, sinking into its knees as if hauling the weight down, and the planet collapses into heavy dome-shaped waves of gravity that roll out toward the target, bearing down and sinking as they travel, with dashes of gravity falling over the target; it holds the pull, then rises back into the guard (the target takes the genjutsu mark, genjutsuAfflicted in earth colours, for the Slow).', [
     g(),
     g(an=band(-110, -150, fistKind='palm'), af=band(-20, -70), bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-120, -150, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-120, -150, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-90, -60), af=band(-5, -40), bob=(2, 2, 2), lean=(1, 3), **LOW),
     *[g(an=band(-60, -40), af=band(-5, -40), bob=(3, 3, 3), lean=(1, 4), **LOW) for _ in range(3)],
     g(an=band(-40, -110), af=band(-25, -90), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, None, 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#c79a5b', '#8a6236'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (earth colours, genjutsuMark.recolor.earth) and keeps it until the Slow ends', 'state': 'genjutsuAfflicted', 'element': 'earth'}},
       anchored={1: [('planet1', 'hand', 4, 1)],
                 2: [('planet2', 'hand', 6, 2), ('eyeC', 'eye', 0, 0)],
                 3: [('planet3', 'hand', 7, 3), ('glit', 'hand', 12, -2), ('eyeCF', 'eye', 0, 0)],
                 4: [('planet2', 'hand', 2, 0, {'alpha': {'e': 170, 'E': 170, 'K': 170, 'C': 190, 'c': 190}}), ('eyeCF', 'eye', 0, 0), ('gp1', 'feet', 14, -30)],
                 5: [('eyeCF', 'eye', 0, 0), ('gp2', 'feet', 19, -24), ('gp1', 'feet', 14, -30), ('gline', 'feet', 22, -38), ('gline', 'feet', 28, -34)],
                 6: [('eyeCF', 'eye', 0, 0), ('gp3', 'feet', 24, -17), ('gp2', 'feet', 19, -24), ('gline', 'feet', 22, -32), ('gline', 'feet', 28, -28), ('gline', 'feet', 25, -40)],
                 7: [('eyeC', 'eye', 0, 0), ('gp3d', 'feet', 27, -10), ('gline', 'feet', 25, -34), ('gline', 'feet', 29, -22)],
                 8: [('gline', 'feet', 27, -28, {'alpha': {'e': 120, 'E': 120, 'K': 120}})]})),
 'silicaStrike': ('Silica Strike', 5,
  'Silica Strike (Virgo taijutsu, Physical 8, Blind 3 rounds INT save DC 12: the fighter grabs a fistful of sand before striking at its opponent\'s face), v2 (Christopher 2026-10-28: the caster really bends down, almost taking a knee, then rises into an uppercut with the sand fx; v4 19:25: the uppercut rises from the crouched position; v5 19:28: more fx): from the guard the fighter drops down onto the rear knee, the lead foot planted flat in front, and sweeps the near hand along the floor, scooping, sand puffing up round the fingers; it closes the fist on a handful and draws it back low beside the hip, sand trickling; then, still kneeling, it starts the uppercut from the hip and rises out of the crouch with it, legs straightening as the fist rips up and out at the opponent\'s chin, arm reaching well out in front, the sand bursting up off the fist into the face, a burst of sand hanging there in a drifting cloud; it settles back into the guard.', [
     g(),
     g(an=band(-20, -25, fistKind='palm'), af=band(-20, -150), bob=(4, 5, 5), lean=(1, 6), **BRACE),   # dropping toward the floor
     g(an=band(-25, -40, fistKind='palm'), af=band(-20, -150), bob=(9, 10, 10), lean=(1, 8), ln='ss-kneel-rear', lf='ss-kneel-lead'),   # on the rear knee, palm sweeping the floor
     g(an=band(-5, -30), af=band(-20, -150), bob=(9, 10, 10), lean=(1, 7), ln='ss-kneel-rear', lf='ss-kneel-lead'),                    # fist closed on a handful
     g(an=band(25, -20), af=band(-40, -130), bob=(9, 10, 10), lean=(1, 4), ln='ss-kneel-rear', lf='ss-kneel-lead'),                    # fist drawn back low by the hip, coiled
     g(an=band(-35, -120), af=band(-30, -120), bob=(8, 9, 9), lean=(1, 4), ln='ss-kneel-rear', lf='ss-kneel-lead'),                    # v4: the uppercut starts from the kneel, fist swinging up from the hip
     g(an=band(-55, -130), af=band(-20, -100), bob=(4, 5, 5), lean=(1, 3), root=(1, 0), **LOW),                                          # rising out of the crouch with the fist, legs driving up
     g(an=band(-112, -128), bob=(0, -1, 0), lean=(1, 2), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),   # at the top of the uppercut, arm reaching up and out, the sand bursting off the fist into the face
     g(an=band(-112, -128), bob=(0, -1, 0), lean=(1, 2), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 2), root=(-2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'roar', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 14, 14, 10], damage='light', rm='E: +1 rising, +3 stepping into the uppercut, -4 settling back',
       anchored={2: [('sandPuff', 'hand', 2, 1), ('sandPuff', 'feet', 14, -1)], 3: [('sandPuff', 'hand', 1, 0), ('sandH', 'hand', 0, -1), ('grains', 'feet', 13, -4)],
                 4: [('sandH', 'hand', 0, -1), ('sandTrk', 'hand', 0, 5), ('grains', 'hand', 3, 3)],
                 5: [('sandH', 'hand', 0, -1), ('sandTrk', 'hand', -1, 5), ('grains', 'hand', -4, 6), ('sandPuff', 'feet', 12, -1), ('grains', 'feet', 9, -6)],
                 6: [('sandH', 'hand', 0, -1), ('sandSprayUp', 'hand', 0, -4), ('sandTrk', 'hand', -1, 7), ('grains', 'hand', -5, 9), ('sandPuff', 'feet', 13, -1)],
                 7: [('sandSprayUp', 'hand', 1, -3), ('sandBurst', 'hand', 5, -2, {'alpha': {'S': 215, 's': 205, 'Z': 225}}), ('sandSpray', 'hand', 7, 1), ('grains', 'hand', -3, 6), ('grains', 'hand', 6, 4)],
                 8: [('sandBurstL', 'hand', 5, -3, {'alpha': {'S': 235, 's': 225, 'Z': 240}}), ('sandCloud', 'hand', 7, -2, {'alpha': {'S': 190, 's': 180, 'Z': 200}}), ('grains', 'hand', -4, 7)],
                 9: [('sandCloudL', 'head', 12, -1, {'alpha': {'S': 175, 's': 165, 'Z': 185}}), ('grains', 'head', 6, 12), ('grains', 'head', 16, 10)],
                 10: [('sandCloudL2', 'head', 13, 0, {'alpha': {'S': 120, 's': 110, 'Z': 130}}), ('grains', 'head', 10, 14)]})),
 'flowingSandParry': ('Flowing Sand Parry', 6,
  'Flowing Sand Parry (Virgo taijutsu stance, counter, AGI +20% 1 round: the fighter loosens its muscles and begins to flow like sand in an hourglass while time seems to slow and its senses heighten), v2 (Christopher 2026-10-28: one arm makes a large sweeping circle over the head, the other the same down near the knees, like swinging them in converging circles): from the guard the fighter lets its arms hang loose, eyes closing, sand trickling from its fingertips; then the near arm swings up in front and round in a wide circle over its head and down behind, while the fighter sinking deep on bent knees so the far arm swings the opposite way in a low circle down by the knees, both open hands trailing streams of sand along their paths; an illusory hourglass forms beside its head and grains hang still in the air as time slows; the two circles converge in front of it, the high hand coming down and the low hand coming up until the open palms meet before the chest in the parry, eyes snapping open crystal teal, the sand trails closing into a ring; the hourglass turns, the grains fall, and it settles back into the guard (the testbed keeps the stance for the counter).', [
     g(),
     g(an=band(-10, -30, fistKind='palm'), af=band(10, -20, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-80, -95, fistKind='palm'), af=band(45, 40, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-135, -150, fistKind='palm'), af=band(15, 10, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-175, -180, fistKind='palm'), af=band(-20, -20, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(150, 150, fistKind='palm'), af=band(-50, -45, fistKind='palm'), bob=(4, 5, 5), lean=(0, 2), **BRACE),
     g(an=band(110, 105, fistKind='palm'), af=band(-30, -25, fistKind='palm'), bob=(4, 5, 5), lean=(0, 2), **BRACE),
     g(an=band(60, 50, fistKind='palm'), af=band(5, 5, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-20, -40, fistKind='palm'), af=band(35, 35, fistKind='palm'), bob=(4, 5, 5), lean=(0, 1), **BRACE),
     g(an=band(-75, -120, fistKind='palm'), af=band(-20, -45, fistKind='palm'), bob=(3, 4, 4), lean=(0, 0), **LOW),
     g(an=band(-60, -125, fistKind='palm'), af=band(-55, -75, fistKind='palm'), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),   # the parry: the circles converge, palms meeting before the chest
     g(an=band(-60, -125, fistKind='palm'), af=band(-55, -75, fistKind='palm'), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-40, -110), af=band(-50, -120), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None, None, None],
  [0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#e6c27a', '#b08d4e'), rm='sways 1 px back and forward (net 0)',
       trails={'near': range(2, 11), 'far': range(2, 11), 'len': 3}, farLayer=True,
       anchored={1: [('sandTrk', 'hand', 0, 3)],
                 3: [('hglass', 'head', -12, -1, {'alpha': {'s': 150, 'S': 160, 'Z': 170}})],
                 **{k: [('hglass', 'head', -12, -1), ('grains', 'head', -9, 6), ('grains', 'head', 10, 16), ('grains', 'feet', -10, -20)] for k in (4, 5, 6)},
                 **{k: [('hglass2', 'head', -12, -1), ('grains', 'head', -9, 6), ('grains', 'head', 10, 16), ('grains', 'feet', -10, -20)] for k in (7, 8, 9)},
                 10: [('hglass2', 'head', -12, -1), ('eyeCF', 'eye', 0, 0), ('grains', 'head', -9, 6), ('grains', 'head', 10, 16), ('grains', 'feet', -10, -20)],
                 11: [('hglass', 'head', -12, -1, {'alpha': {'s': 140, 'S': 140, 'Z': 150}}), ('eyeC', 'eye', 0, 0), ('grains', 'head', -9, 9), ('grains', 'head', 10, 20)],
                 12: [('grains', 'head', -9, 14, {'alpha': {'S': 130, 's': 120, 'Z': 140}}), ('grains', 'feet', 10, -8, {'alpha': {'S': 130, 's': 120, 'Z': 140}})]})),
 'witherPalm': ('Wither Palm', 2,
  'Wither Palm (Virgo taijutsu strike, Physical 12, target Stamina -15: with clinical precision the fighter throws a series of palm strikes at its opponent\'s vital points): from the guard the fighter draws the near open hand back by the hip, then steps in and fires five quick open-palm strikes, alternating hands and changing height, chest, throat, ribs, solar plexus and a last near palm to the chest; each lands with a crystal-teal flash on the vital point struck, a thin teal shock ring snapping out from it and a plume of dull, dry dust as the strength drains out of the foe, the last one a big flash with a double ring and a burst of withered dust that drifts down; v2 (Christopher 2026-10-28: the animation is good, it needs more fx): the open hands glow crystal teal from the draw-back on, trailing a faint teal streak on each strike, and a thin teal aura clings to the fighter through the flurry; it holds a beat, the dust falling, then settles back into the guard.', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),   # chest
     g(an=band(-40, -110), af=band(-100, -96, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),   # throat
     g(an=band(-75, -72, fistKind='palm'), af=band(-40, -120), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),   # ribs
     g(an=band(-40, -110), af=band(-85, -85, fistKind='palm'), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),   # solar plexus
     g(an=band(-92, -92, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(2, 5), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),   # the last, full extension
     g(an=band(-92, -92, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-3, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 1, 1, 2, 2, 1, 0],
  dict(fps=12, auraColors=('#7fe3d0', '#3a9e8f'), hitbox=[44, 18, 14, 14], damage='light', rm='E: +2 stepping into the strikes, +1 on the last, -3 settling back',
       anchored={1: [('palmGlow', 'hand', 0, 0), ('palmGlow', 'farhand', 0, 0, {'alpha': {'C': 150, 'c': 170}})],
                 2: [('palmGlow', 'farhand', 0, 0), ('vital', 'hand', 2, 0), ('vRing', 'hand', 3, 0), ('witherPlume', 'hand', 1, 7), ('streak', 'hand', -6, 0)],
                 3: [('palmGlow', 'hand', 0, 0), ('vital', 'farhand', 2, 0), ('vRing', 'farhand', 3, 0), ('witherPlume', 'farhand', 1, 7), ('wither', 'hand', 0, 6), ('streak', 'farhand', -6, 0)],
                 4: [('palmGlow', 'farhand', 0, 0), ('vital', 'hand', 2, 0), ('vRing', 'hand', 3, 0), ('witherPlume', 'hand', 1, 7), ('wither', 'farhand', 3, 5), ('streak', 'hand', -6, 0)],
                 5: [('palmGlow', 'hand', 0, 0), ('vital', 'farhand', 2, 0), ('vRing', 'farhand', 3, 0), ('witherPlume', 'farhand', 1, 7), ('wither', 'hand', 1, 4), ('streak', 'farhand', -6, 0)],
                 6: [('vital2', 'hand', 3, 0), ('vRing2', 'hand', 3, 0), ('witherBurst', 'hand', 4, 3), ('wither2', 'hand', 2, 6), ('streak', 'hand', -7, 0)],
                 7: [('vital', 'hand', 3, 0, {'alpha': {'c': 150, 'W': 170}}), ('vRing3', 'hand', 3, 0, {'alpha': {'c': 170, 'C': 150}}), ('witherBurst', 'hand', 4, 8, {'alpha': {'u': 200, 'v': 200}}), ('wither2', 'hand', 2, 9), ('wither', 'hand', -2, 13)],
                 8: [('witherPlume', 'hand', 3, 13, {'alpha': {'u': 150, 'v': 150}}), ('wither', 'hand', 2, 17, {'alpha': {'u': 130, 'v': 130}}), ('wither', 'hand', 6, 19, {'alpha': {'u': 110, 'v': 110}})]})),
 'sandBurial': ('Sand Burial', 5,
  'Sand Burial (Virgo ninjutsu, Elemental 22, single target in the Zone of Awareness, Root 2 rounds STR DC 13, 2x poise damage: the caster commands the sand round its opponent to envelop and crush it): from the guard the fighter makes the seal at the chin and sinks, sand grains lifting off the floor round its feet and a sandy aura rising; it sweeps both open palms low and forward over the ground and sand streams away along the floor toward the target; then it lifts the near hand palm up, drawing the sand up round the foe, and clenches it into a fist, squeezing, arm trembling, as the sand closes and crushes; it holds the squeeze, then drops back into the guard. On the target (the testbed plays sandBuried on it from the active frame; v2, Christopher 2026-10-28): sand heaps up round its legs and climbs to its neck, pinning its arms, and the column squeezes it, looping, until the Root ends, when it breaks free (sandBreakFree).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-40, -45, fistKind='palm'), af=band(-30, -55, fistKind='palm'), bob=(4, 5, 5), lean=(1, 7), **BRACE),   # palms swept low over the ground
     g(an=band(-120, -150, fistKind='palm'), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 1), **LOW),                     # palm up, drawing the sand up
     g(an=band(-115, -155), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 2), **LOW),                                        # clenched: crush
     g(an=band(-115, -155), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 2), root=(1, 0), **LOW),
     g(an=band(-115, -155), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 2), root=(-1, 0), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'closed', 'squint', 'squint', 'strain', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#e6c27a', '#9c7434'), rm='a 1 px tremble on frames 6-7 (net 0)',
       extra={'targetState': {'rule': 'Sand Burial: on the active frame the testbed plays sandBuried on the target (frames 0-3 once: sand heaps up and climbs to the neck; then frames 4-7 on loop, the column squeezing) until the Root ends, then sandBreakFree once (v2, Christopher 2026-10-28)', 'state': 'sandBuried', 'loopFrom': 4}},
       anchored={2: [('sandRise', 'feet', -8, -4), ('sandRise', 'feet', 9, -6)],
                 3: [('sandStream', 'feet', 14, -1), ('sandRise', 'hand', 0, -3), ('grains', 'feet', -9, -8)],
                 4: [('sandStream', 'feet', 18, -1, {'alpha': {'s': 170, 'S': 170, 'Z': 190}}), ('whirl0F', 'hand', 0, -2), ('grains', 'hand', 2, 5)],
                 5: [('whirl1F', 'hand', 0, -1), ('sandH', 'hand', 0, 0), ('grains', 'hand', 3, 6)],
                 6: [('whirl2F', 'hand', 0, -1), ('grains', 'hand', -3, 6)], 7: [('whirl3F', 'hand', 0, -1, {'alpha': {'s': 150, 'S': 150, 'Z': 170}})]})),
 'sandBuried': ('Sand Buried', 3,
  'Sand Buried (target state of Sand Burial, Root 2 rounds, 2x poise damage), v2 (Christopher 2026-10-28: the sand comes up to the target\'s neck and visibly squeezes it; a break-free animation when it ends): sand heaps up round the fighter\'s feet, flinching, then climbs its legs and body, pinning its arms to its sides, until only the head sticks out of a column of packed sand; the column squeezes, pinching in round the body with dark constriction bands winding round it, the face twisting in pain, grains spurting out at the neck on each squeeze; it keeps squeezing, frames 4-7 on loop, until the Root ends, when the testbed plays sandBreakFree.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 2), lean=(0, 0))],
  ['pain', 'pain', 'pain', 'strain', 'strain', 'pain', 'strain', 'pain'],
  None,
  dict(fps=8, extra={'loop': True, 'loopFrom': 4, 'breakFree': {'rule': 'Sand Burial v2: when the Root ends (or the target is freed) the testbed plays sandBreakFree once, then the idle', 'state': 'sandBreakFree'}},
       anchored={0: [('mound6', 'feet', 0, -3), ('grains', 'feet', -10, -9), ('grains', 'feet', 10, -12)],
                 1: [('mound18', 'feet', 0, -9), ('sandRise', 'feet', -11, -21), ('sandRise', 'feet', 11, -23)],
                 2: [('coffin30', 'feet', 0, -15), ('grains', 'head', -9, 8)],
                 3: [('colRise', 'head', 0, 32), ('grains', 'head', 9, 4)],
                 4: [('col0', 'head', 0, 32)],
                 5: [('col1', 'head', 0, 32), ('grains', 'head', -7, 5), ('grains', 'head', 7, 4)],
                 6: [('col2', 'head', 0, 32)],
                 7: [('col3', 'head', 0, 32), ('grains', 'head', 8, 5), ('grains', 'head', -8, 4)]})),
 'sandBreakFree': ('Sand Break Free', 2,
  'Sand Break Free (target state, Sand Burial v2: plays once when the Root ends): buried to the neck in the squeezing sand, the fighter strains, and cracks split the packed column, spreading; then it bursts its arms up and out with a roar and the sand blows apart, chunks of packed sand flying out in a ring and grains spraying, the column collapsing to a low heap round its feet; the chunks fall and scatter, the heap slumps flat and the fighter drops back into its guard.', [
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-8, -25), af=band(-4, -20), bob=(1, 1, 1), lean=(0, 0), root=(1, 0)),
     g(an=band(-135, -175), af=band(120, 175), bob=(0, 0, 0), lean=(0, -1), root=(-1, 0)),
     g(an=band(-130, -170), af=band(115, 170), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-80, -150), af=band(60, 120), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-50, -120), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1)),
     g(),
     g()],
  ['strain', 'strain', 'roar', 'roar', 'squint', 'squint', None, None],
  None,
  dict(fps=10, rm='a 1 px shudder on frames 1-2 (net 0)',
       anchored={0: [('colCrack1', 'head', 0, 32)], 1: [('colCrack2', 'head', 0, 32), ('grains', 'head', -8, 5), ('grains', 'head', 8, 3)],
                 2: [('shatter12', 'head', 0, 20), ('mound14', 'feet', 0, -7)],
                 3: [('shatter18', 'head', 0, 22), ('mound14', 'feet', 0, -7)],
                 4: [('shatter23', 'head', 0, 26, {'alpha': {'S': 190, 's': 180, 'Z': 200}}), ('mound6', 'feet', 0, -3)],
                 5: [('mound6', 'feet', 0, -3, {'alpha': {'S': 170, 's': 160, 'Z': 170}}), ('grains', 'feet', -12, -3), ('grains', 'feet', 12, -2)],
                 6: [('sandPuff', 'feet', -9, -1, {'alpha': {'S': 130, 's': 120, 'Z': 130}}), ('sandPuff', 'feet', 9, -1, {'alpha': {'S': 130, 's': 120, 'Z': 130}})]})),
 'sandstorm': ('Sandstorm', 6,
  'Sandstorm (Virgo ninjutsu), v2 (Christopher 2026-10-28: a user-centred AoE; a hazardous storm round the user that deals light damage, lowers the accuracy of anyone inside and keeps every projectile that is not an ultimate from entering): from the guard the fighter makes the seal, then sinks low with both fists driven down beside the hips; sand lifts off the floor round its feet and starts to turn, a low ring of sand spinning round its legs; it rises and raises the near hand high, palm up, circling it, and the storm climbs with it, round the waist, then the chest, until a sand tornado stands round the whole fighter with the fighter calm in its eye, crystal and grit shrapnel caught in the streaks, the front half drawn over the fighter (part see-through) and the back half behind it; it sweeps the open hand out and down and the storm blasts outward, sand spraying off both sides; it settles back into the guard with a thin ring of storm still turning round it. The testbed then draws the storm over the whole AoE for as long as it lasts (extra.zone).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-115, -140, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-122, -150, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-110, -132, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-122, -150, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-110, -132, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-40, -40, fistKind='palm'), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-40, -40, fistKind='palm'), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'strain', 'strain', 'squint', 'squint', 'closed', 'closed', 'closed', 'strain', 'squint', None],
  [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 2, 1],
  dict(fps=10, auraColors=('#e6c27a', '#9c7434'),
       extra={'zone': {'rule': 'Sandstorm v2 (Christopher 2026-10-28): AoE centred on the caster\'s hex (selfCentered, no aim point), placeholder radius 2 for 3 rounds; the testbed draws the storm (stormRing pattern turning, sand streaks and grit) over every hex of the AoE, following the caster if it moves; each round every other fighter inside takes light Elemental damage (placeholder 4) and an accuracy penalty while inside (placeholder -20% hit chance, Claude\'s reading: the caster in the eye is not penalised); a Projectile that is not an ultimate cannot enter: it stops at the first AoE hex on its line and breaks up in a sandPuff; ultimates pass through', 'pattern': 'stormRing', 'radius': 2, 'rounds': 3, 'selfCentered': True, 'blocksProjectiles': 'non-ultimate'},
              'targetState': {'rule': 'Sandstorm v2: every other fighter inside the AoE plays sandstormCaught on loop while it stays inside', 'state': 'sandstormCaught'}},
       anchored={1: [('sandRise', 'feet', -10, -6), ('sandRise', 'feet', 10, -6)],
                 2: [('eyeLow0B', 'feet', 0, -8, {'behind': True}), ('eyeLow0F', 'feet', 0, -8)],
                 3: [('eyeLow1B', 'feet', 0, -8, {'behind': True}), ('eyeLow1F', 'feet', 0, -8), ('grains', 'feet', 12, -14)],
                 4: [('eyeMid2B', 'feet', 0, -16, {'behind': True}), ('eyeMid2F', 'feet', 0, -16, {'alpha': {'s': 190, 'S': 190, 'Z': 210}})],
                 5: [('eyeMid3B', 'feet', 0, -16, {'behind': True}), ('eyeMid3F', 'feet', 0, -16, {'alpha': {'s': 190, 'S': 190, 'Z': 210}}), ('grains', 'feet', -13, -26)],
                 **{6 + k: [('eye%dB' % k, 'feet', 0, -26, {'behind': True}), ('eye%dF' % k, 'feet', 0, -26, {'alpha': {'s': 170, 'S': 170, 'Z': 200, 'C': 220, 'c': 220, 'K': 220}})] for k in range(3)},
                 9: [('eye3B', 'feet', 0, -26, {'behind': True}), ('eye3F', 'feet', 0, -26, {'alpha': {'s': 130, 'S': 130, 'Z': 160}}), ('sandSpray', 'feet', 20, -20), ('sandSprayL', 'feet', -20, -20)],
                 10: [('sandCloud2', 'feet', 22, -18), ('sandCloud2', 'feet', -22, -18), ('eyeLow2B', 'feet', 0, -8, {'behind': True}), ('eyeLow2F', 'feet', 0, -8, {'alpha': {'s': 140, 'S': 140, 'Z': 160}})],
                 11: [('eyeLow3B', 'feet', 0, -8, {'behind': True}), ('eyeLow3F', 'feet', 0, -8, {'alpha': {'s': 110, 'S': 110, 'Z': 130}})]})),
 'sandstormCaught': ('Caught in Sandstorm', 0,
  'Caught in Sandstorm (target state of Sandstorm v2, plays while the fighter stays inside the storm: light damage each round, lowered accuracy): sand streaks and grit blow across the fighter in the direction the storm turns, crystal and grit shrapnel flicking past, some in front of it and some behind; the fighter throws its forearms up over its eyes and flinches, swaying, squinting through the sand (loops, one gust every two frames).', [
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -2), root=(-1, 0)),
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-130, -175), af=band(-120, -170), bob=(1, 1, 2), lean=(0, -2), root=(1, 0))],
  ['pain', 'pain', 'pain', 'pain'],
  None,
  dict(fps=10, extra={'loop': True},
       anchored={k: [('gust%dB' % k, 'feet', 0, -22, {'behind': True}), ('gust%dF' % k, 'feet', 0, -22, {'alpha': {'s': 200, 'S': 200, 'Z': 220}})] for k in range(4)})),
 'phantomPlague': ('Phantom Plague', 5,
  'Phantom Plague (Virgo genjutsu, mental summon / DoT: images of a shadowy creature that only the caster and the victim see haunt the victim across the field, dealing damage and ignoring stealth; Psychosomatic 3 rounds 4/tick, INT save DC 12; range Zone of Awareness): from the guard the fighter lifts two fingers before its eyes, which kindle crystal teal, and its shadow pools out dark across the floor; it sinks low and points down into the pool, and a hunched shadow creature with teal eyes claws up out of it behind the fighter, rising to its full height; then the fighter thrusts the pointing hand at the target and the creature glides forward past it, clawed arm reaching, fading as it goes; the glow dies and the fighter steps back into the guard. The testbed then draws the phantom (wraith pattern) hovering beside the target, following it everywhere, even in stealth, and lashing at it on each tick; the target takes genjutsuAfflicted in earth colours.', [
     g(),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -175, fistKind='point'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-30, -50, fistKind='point'), af=band(-20, -60), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g(an=band(-30, -50, fistKind='point'), af=band(-20, -60), bob=(3, 3, 3), lean=(0, 3), **LOW),
     g(an=band(-90, -90, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     g(an=band(-90, -90, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-90, -90, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-50, -120), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#3a2f40', '#7fe3d0'), rm='E: +1 into the point, -1 settling back',
       extra={'targetState': {'rule': 'Phantom Plague (Christopher 2026-10-28: the target needs an animation for the duration): on the active frame the target starts phantomHaunted on loop in place of its idle and keeps it until the Psychosomatic ends; the genjutsu mark (genjutsuAfflicted halo, aura and eye glow, earth colours) is drawn over it as on any other state', 'state': 'phantomHaunted', 'element': 'earth', 'mark': 'genjutsuAfflicted'},
              'summon': {'rule': 'Phantom Plague: while the Psychosomatic lasts the testbed draws the phantom (pattern wraith, palette X/x/C, about 70% opacity, bobbing 1 px) hovering just behind the target and following it every move; it stays visible on a target in stealth (ignores stealth, drawn only for the caster and the victim); on each 4/tick it lunges 3 px and the target flinches', 'pattern': 'wraith'}},
       anchored={1: [('eyeC', 'eye', 0, 0)], 2: [('eyeCF', 'eye', 0, 0), ('shadowPool', 'feet', -2, -1)],
                 3: [('eyeCF', 'eye', 0, 0), ('shadowPool2', 'feet', -3, -1), ('wraithRise', 'feet', -13, -7, {'behind': True})],
                 4: [('eyeCF', 'eye', 0, 0), ('shadowPool2', 'feet', -3, -1), ('wraith', 'feet', -14, -20, {'behind': True})],
                 5: [('eyeCF', 'eye', 0, 0), ('shadowPool', 'feet', 0, -1), ('wraith', 'feet', 4, -22, {'alpha': {'X': 230, 'x': 172, 'C': 255}})],
                 6: [('eyeC', 'eye', 0, 0), ('wraith', 'feet', 13, -23, {'alpha': {'X': 215, 'x': 161, 'C': 255}})],
                 7: [('wraith', 'feet', 20, -24, {'alpha': {'X': 175, 'x': 131, 'C': 215}})], 8: [('wraith', 'feet', 25, -24, {'alpha': {'X': 120, 'x': 90, 'C': 160}})]})),
 'phantomHaunted': ('Haunted by the Phantom', 0,
  'Haunted by the Phantom (target state of Phantom Plague; Psychosomatic 3 rounds 4/tick), v2 (Christopher 2026-10-28: the phantom circles the opponent before hitting): the victim hunches low and wary, forearms raised before its face, while the hunched shadow creature with teal eyes, part see-through, circles round it: from behind it drifts past the far side (fainter, behind the victim), round in front (turned to face it), back across the near side over the victim and round behind again; then it leans in over the victim\'s shoulder and rakes its clawed arm down past it, three teal claw marks flashing, the victim flinching forward, wincing, and it draws back behind (loops; the testbed lines the rake up with each 4/tick and draws the genjutsu mark over it).', [
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-60, -150), af=band(-65, -155), bob=(3, 3, 3), lean=(1, 5), root=(1, 0), **LOW),
     g(an=band(-60, -150), af=band(-65, -155), bob=(3, 3, 3), lean=(1, 4), **LOW),
     g(an=band(-45, -140), af=band(-55, -150), bob=(2, 2, 3), lean=(0, 2), root=(-1, 0), **LOW)],
  ['squint'] * 9 + ['pain', 'pain', 'squint'],
  None,
  dict(fps=8, extra={'loop': True},
       anchored={0: [('wraith', 'feet', -13, -22, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})],
                 1: [('wraith', 'feet', -8, -23, {'behind': True, 'alpha': {'X': 120, 'x': 90, 'C': 200}})],
                 2: [('wraith', 'feet', 0, -24, {'behind': True, 'alpha': {'X': 120, 'x': 90, 'C': 200}})],
                 3: [('wraithM', 'feet', 8, -24, {'behind': True, 'alpha': {'X': 120, 'x': 90, 'C': 200}})],
                 4: [('wraithM', 'feet', 14, -23, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})],
                 5: [('wraithM', 'feet', 9, -22, {'alpha': {'X': 150, 'x': 110, 'C': 255}})],
                 6: [('wraith', 'feet', 1, -22, {'alpha': {'X': 150, 'x': 110, 'C': 255}})],
                 7: [('wraith', 'feet', -7, -23, {'alpha': {'X': 150, 'x': 110, 'C': 255}})],
                 8: [('wraith', 'feet', -12, -24, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})],
                 9: [('wraith', 'feet', -7, -24, {'alpha': {'X': 160, 'x': 120, 'C': 255}}), ('clawMark', 'head', 3, 12)],
                 10: [('wraith', 'feet', -9, -23, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}}), ('clawMark2', 'head', 3, 14)],
                 11: [('wraith', 'feet', -12, -22, {'behind': True, 'alpha': {'X': 180, 'x': 135, 'C': 255}})]})),
 'coffinSyndrome': ('Coffin Syndrome', 4,
  'Coffin Syndrome (Virgo genjutsu, mental debuff: the caster projects images of being buried alive on its opponent until panic scrambles its mind; Confusion 1 round, STR save DC 13; range Zone of Awareness), v2 (Christopher 2026-10-28: an actual coffin rises up behind the target and encloses it, with a break-out animation): from the guard the fighter raises the near hand palm up before its chest, eyes kindling crystal teal, and slowly lifts it, summoning the coffin up out of the floor behind the target; then it turns the hand over and snaps it shut into a fist, slamming the lid closed on the target; it holds the fist, sand motes drifting off it, then the glow dies and it returns to the guard. The target plays coffinEntombed from the active frame (the coffin rises behind it, the lid swings shut over it, it pounds on the lid inside) until the Confusion ends, then coffinBreakOut once; the genjutsu mark (earth colours) is drawn over both.', [
     g(),
     g(an=band(-60, -100, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-70, -110, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-90, -135, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-110, -155, fistKind='palm'), bob=(0, 0, 1), lean=(0, -2)),
     g(an=band(-110, -155, fistKind='palm'), bob=(0, 0, 1), lean=(0, -2)),
     g(an=band(-92, -92), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),     # the hand snaps shut: the lid slams
     g(an=band(-92, -92), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-92, -92), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-50, -120), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'strain', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e6c27a', '#7fe3d0'),
       extra={'targetState': {'rule': 'Coffin Syndrome v2 (Christopher 2026-10-28): from the active frame (the caster\'s palm starts to lift, frame 2) the target plays coffinEntombed: intro frames 0-5 once (the coffin rises behind it, the lid closes on frame 5, lined up with the caster\'s fist on frame 6), then frames 6-9 on loop until the Confusion ends; then coffinBreakOut once, back to its guard. The genjutsu mark (genjutsuAfflicted halo, aura, eye glow, earth colours) is drawn over it throughout', 'state': 'coffinEntombed', 'loopFrom': 6, 'element': 'earth', 'mark': 'genjutsuAfflicted', 'breakFree': 'coffinBreakOut'}},
       anchored={1: [('eyeC', 'eye', 0, 0)], 2: [('eyeCF', 'eye', 0, 0), ('grains', 'hand', 0, -4)], 3: [('eyeCF', 'eye', 0, 0), ('sandRise', 'hand', 0, -5)],
                 4: [('eyeCF', 'eye', 0, 0), ('sandRise', 'hand', 0, -6), ('grains', 'hand', 3, -9)], 5: [('eyeCF', 'eye', 0, 0), ('sandRise', 'hand', 1, -6)],
                 6: [('eyeCF', 'eye', 0, 0), ('sandPuff', 'hand', 2, 0), ('vRing', 'hand', 2, 0)], 7: [('eyeCF', 'eye', 0, 0), ('sandTrk', 'hand', 0, 5)],
                 8: [('eyeC', 'eye', 0, 0), ('grains', 'hand', 0, 6, {'alpha': {'S': 140, 's': 130, 'Z': 150}})]})),
 'coffinEntombed': ('Entombed', 0,
  'Entombed (target state of Coffin Syndrome v2, Confusion 1 round): an illusory coffin, a box of packed sand outlined in crystal teal, rises up out of the floor close behind the fighter, sand pouring off it, and stands upright over it; the lid swings round from the hinge at its back edge and slams shut over the fighter in front, a puff of sand and a teal ring bursting off it; inside, the fighter (seen faintly through the illusion) pounds on the lid with both palms, panicking, and the coffin shudders with each blow, sand trickling from its seams (loops from frame 6 until the Confusion ends; then coffinBreakOut).', [
     g(),
     g(bob=(1, 1, 2), lean=(-1, -2)),
     g(an=band(-60, -140), af=band(-70, -150), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-60, -140), af=band(-70, -150), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-50, -155, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-50, -155, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-55, -140, fistKind='palm'), af=band(-45, -150, fistKind='palm'), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-55, -140, fistKind='palm'), af=band(-45, -150, fistKind='palm'), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0))],
  [None, 'squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain'],
  None,
  dict(fps=10, extra={'loop': True, 'loopFrom': 6},
       anchored={0: [('cofBack', 'feet', -2, 24, {'behind': True}), ('sandPuff', 'feet', -10, -1), ('sandPuff', 'feet', 8, -1)],
                 1: [('cofBack', 'feet', -2, 4, {'behind': True}), ('grains', 'feet', -14, -8), ('sandTrk', 'feet', 9, -10)],
                 2: [('cofBack', 'feet', -2, -27, {'behind': True}), ('sandTrk', 'feet', -14, -16), ('grains', 'feet', 12, -20)],
                 3: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLid1', 'feet', -13, -27)],
                 4: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLid2', 'feet', -7, -27, {'alpha': {'s': 210, 'S': 210, 'Z': 220}})],
                 5: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLid', 'feet', -2, -27, {'alpha': {'s': 190, 'S': 190, 'Z': 200}}), ('sandPuff', 'feet', 13, -40), ('sandPuff', 'feet', -14, -12), ('vRing2', 'feet', 0, -28, {'alpha': {'c': 200, 'C': 180}})],
                 **{6 + k: [('cofBack', 'feet', -2 + d, -27, {'behind': True}), ('cofLid', 'feet', -2 + d, -27, {'alpha': {'s': 185, 'S': 185, 'Z': 195}}), ('sandTrk', 'feet', 12 + d, -30 + 6 * k)] + ([('grains', 'feet', -13, -44)] if k % 2 == 0 else [])
                    for k, d in enumerate((1, 0, -1, 0))}})),
 'coffinBreakOut': ('Coffin Break Out', 2,
  'Coffin Break Out (target state of Coffin Syndrome v2: plays once when the Confusion ends): inside the shut coffin the fighter strains, and cracks split the lid, spreading; then it bursts the lid open with both arms thrown out and a roar, and the coffin breaks apart into teal-edged planks and clumps of sand flying outward, the back of it crumbling into the floor; the pieces fade as they fall and the fighter shakes itself back into the guard.', [
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-45, -150, fistKind='palm'), af=band(-55, -140, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(an=band(-135, -175), af=band(120, 175), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-130, -170), af=band(115, 170), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-80, -150), af=band(60, 120), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-50, -120), af=band(-35, -105), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  ['pain', 'strain', 'roar', 'roar', 'squint', None, None],
  [0, 1, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e6c27a', '#7fe3d0'),
       anchored={0: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLidCrack', 'feet', -2, -27, {'alpha': {'s': 190, 'S': 190, 'Z': 210}})],
                 1: [('cofBack', 'feet', -2, -27, {'behind': True}), ('cofLidCrack2', 'feet', -2, -27, {'alpha': {'s': 190, 'S': 190, 'Z': 210}}), ('grains', 'feet', 12, -36)],
                 2: [('cofBackLow', 'feet', -2, -20, {'behind': True}), ('plank', 'feet', 15, -40), ('plankV', 'feet', -16, -34), ('plank', 'feet', 13, -14), ('sandBurst', 'feet', 0, -30, {'alpha': {'S': 200, 's': 190, 'Z': 210}}), ('sandPuff', 'feet', -14, -12)],
                 3: [('cofBackLow2', 'feet', -2, -12, {'behind': True}), ('plank', 'feet', 21, -36), ('plankV', 'feet', -22, -28), ('plank', 'feet', 19, -8), ('sandCloud', 'feet', 0, -28, {'alpha': {'S': 150, 's': 140, 'Z': 160}})],
                 4: [('mound6', 'feet', -2, -3), ('plank', 'feet', 24, -26, {'alpha': {'C': 150, 'c': 150, 's': 120, 'S': 120}}), ('plankV', 'feet', -25, -16, {'alpha': {'C': 150, 'c': 150, 's': 120, 'S': 120}}), ('sandCloud2', 'feet', 0, -24, {'alpha': {'S': 110, 's': 100, 'Z': 120}})],
                 5: [('grains', 'feet', -8, -4, {'alpha': {'S': 120, 's': 110, 'Z': 130}}), ('grains', 'feet', 10, -5, {'alpha': {'S': 120, 's': 110, 'Z': 130}})]})),
 'adamantineShin': ('Adamantine Shin', 4,
  'Adamantine Shin (Capricorn taijutsu strike, Physical 16, Guard Break, 1.5x poise damage, Bleed 2 rounds 3/tick: a bone-hard shin that cracks structure): from the guard the fighter lifts the near knee and crystal starts to grow over the shin from the ankle up, teal facets with white glints; it chambers the knee high as the crystal sheath closes over the whole shin, a glint flashing on it; then it pivots on the lead foot and snaps the crystal shin through level at the opponent\'s thigh, a crystal-white burst, a teal shock ring and a cross-shaped crack flashing at the point of impact and crystal shards and grit flying off; it drives through, recoils the leg and sets it down, the crystal flaking away, back into the guard.', [
     g(),
     g(an=band(10, -60), af=band(-60, -90), bob=(1, 1, 1), lean=(0, 0), ln='as-lift', lf='lk-lead-pivot'),
     g(an=band(15, -50), af=band(-65, -95), bob=(0, 0, 1), lean=(0, -1), ln='as-chamber', lf='lk-lead-pivot'),
     g(an=band(15, -50), af=band(-65, -95), bob=(0, 0, 1), lean=(0, -1), ln='as-chamber', lf='lk-lead-pivot'),
     g(an=band(40, -20), af=band(-80, -100), bob=(1, 1, 1), lean=(-1, -3), root=(1, 0), ln='as-kick', lf='lk-lead-pivot'),
     g(an=band(40, -20), af=band(-80, -100), bob=(1, 1, 1), lean=(-1, -3), ln='as-kick2', lf='lk-lead-pivot'),
     g(an=band(20, -40), af=band(-65, -90), bob=(1, 1, 2), lean=(0, -1), ln='as-recoil', lf='lk-lead-pivot'),
     g(bob=(1, 1, 1), lean=(0, 0), root=(-1, 0)),
     g()],
  [None, 'squint', 'strain', 'strain', 'roar', 'strain', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 38, 14, 12], damage='heavy', rm='E: +1 into the kick, -1 setting down',
       crystal={'shin': {1: ('as-lift', 0.35, 235), 2: ('as-chamber', 0.75, 245), 3: ('as-chamber', 1.0, 255), 4: ('as-kick', 1.0, 255), 5: ('as-kick2', 1.0, 255), 6: ('as-recoil', 0.8, 190)}},
       anchored={1: [('gemSpark', 'feet', 2, -12)], 3: [('gemSpark', 'head', 6, 26), ('gemShard', 'feet', 9, -18)],
                 4: [('gemBurst', 'head', 24, 28), ('gemCrack', 'head', 24, 28), ('gemShard2', 'head', 27, 21), ('gemSpark', 'head', 28, 33)],
                 5: [('gemBurst2', 'head', 25, 29), ('gemCrack', 'head', 25, 29), ('gemShard2', 'head', 29, 22), ('gemShard2', 'head', 28, 36), ('gemShard', 'head', 31, 29), ('rocks', 'head', 23, 37), ('gemSpark', 'head', 21, 20)],
                 6: [('gemShard', 'head', 30, 35), ('gemShard', 'head', 31, 25), ('gemShard', 'head', 27, 41), ('dust1', 'feet', 10, -3)], 7: [('gemShard', 'feet', 12, -2)]})),
 'diamondCutter': ('Diamond Cutter', 5,
  'Diamond Cutter (Capricorn taijutsu strike, True damage 14, bypasses poise and mitigation: the fighter focuses its resolve into its hand, hardening it until it crystallises, then throws an unguardable chop): from the guard the fighter draws the near hand up open above its ear, elbow high behind, , knife-edge forward, eyes narrowing; crystal grows over the hand and forearm from the fingertips back, teal facets with white glints, over three held frames, a glint flashing on the edge; then it steps in and brings the crystal knife-hand chopping down and through on a diagonal, a bright white-and-teal slash line cutting the air along its path, and on contact a thin slash of light and a spray of crystal shards; it holds the follow-through low, the crystal flaking off, and returns to the guard.', [
     g(),
     g(an=band(70, -170, fistKind='palm'), af=band(-70, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-110, -110, fistKind='palm'), af=band(-30, -80), bob=(1, 1, 2), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-65, -55, fistKind='palm'), af=band(20, -60), bob=(2, 2, 3), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-60, -50, fistKind='palm'), af=band(20, -60), bob=(2, 2, 3), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -90), af=band(-30, -100), bob=(1, 1, 2), lean=(1, 2), root=(-2, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'roar', 'strain', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[44, 22, 14, 14], damage='medium', rm='E: +2 stepping into the chop, -2 settling back',
       crystal={'arm': {2: (0.2, 235), 3: (0.4, 250), 4: (0.6, 255), 5: (0.6, 255), 6: (0.6, 255), 7: (0.6, 230), 8: (0.3, 150)}},
       anchored={3: [('gemSpark', 'head', -9, -5)], 4: [('gemSpark', 'head', -8, -7), ('cryst', 'head', -12, 0)],
                 5: [('slash', 'hand', -2, 1)],
                 6: [('slash2', 'hand', -3, -5), ('gemShard2', 'hand', 5, 2), ('gemSpark', 'hand', 3, -3)],
                 7: [('gemShard', 'hand', 6, 4), ('gemShard', 'hand', 2, 8), ('cryst', 'hand', 8, -2)], 8: [('crystT', 'hand', 3, 5)]})),
 'prismaticSkin': ('Prismatic Skin', 4,
  'Prismatic Skin (Capricorn taijutsu stance buff, FORT +50% 2 rounds: by focusing its resolve the fighter\'s skin crystallises over, granting enhanced durability): from the guard the fighter drops its fists to its hips, elbows back, and tenses, sinking a little, eyes squeezed; a crystal-teal aura rises round it and crystal spreads over all its skin, pale teal with white facet lines and deep teal facets, glints flashing on the shoulders and forearms and small crystal shards popping off; it holds, glittering, then rises back into the guard still crystallised (the testbed keeps the crystal skin while the buff lasts).', [
     g(),
     g(an=band(15, -40), af=band(5, -35), bob=(1, 1, 1), lean=(0, 0)),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'strain', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#3a9e8f'), tint={2: 90, 3: 160, 4: 205, 5: 205, 6: 205, 7: 205, 8: 205}, veins=(), tintColors=((0x7f, 0xe3, 0xd0), (0x3a, 0x9e, 0x8f), (0xf0, 0xff, 0xfc), (0x2c, 0x80, 0x74)),
       extra={'linger': {'rule': 'Prismatic Skin (FORT +50% 2 rounds): the clip ends with the skin crystallised; while the buff lasts the testbed keeps drawing the fighter with the crystal tint (crystal teal #7fe3d0 at alpha 205 over skin pixels, white facet streaks #f0fffc and deep teal facet patches #2c8074 off the face), as Oak Flesh does', 'tint': '#7fe3d0', 'alpha': 205, 'streak': '#f0fffc', 'facet': '#2c8074'}},
       anchored={3: [('gemSpark', 'head', -7, 14), ('gemShard', 'head', 8, 18)],
                 4: [('gemSpark', 'head', 7, 12), ('gemShard', 'head', -8, 22), ('cryst', 'head', 9, 26)],
                 5: [('gemSpark', 'head', -6, 20), ('cryst', 'head', 7, 16)], 6: [('gemSpark', 'head', 6, 24)], 7: [('cryst', 'head', -6, 18)]})),
 'geodeBlast': ('Geode Blast', 5,
  'Geode Blast (Capricorn ninjutsu, Elemental 18, AoE in the Zone of Awareness, Bleed 2 rounds 3/tick: the fighter calls the minerals in the earth to burst from the ground, sending shrapnel over a wide area): from the guard the fighter makes the seal at the chin and sinks, an earthen aura rising with crystal glints in it; it drops and slams the near palm flat on the floor, cracks glowing teal running away from the hand along the ground toward the target; then it whips the palm up, open, and clenches it into a fist before its face, and at the target the ground splits and clusters of jagged crystal spikes burst up out of it, shards spraying out (the target plays geodeBlasted); it holds the fist, then drops back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-35, -40, fistKind='palm'), af=band(-30, -100), bob=(5, 6, 6), lean=(1, 8), **BRACE),   # palm slammed flat on the floor
     g(an=band(-35, -40, fistKind='palm'), af=band(-30, -100), bob=(5, 6, 6), lean=(1, 8), **BRACE),
     g(an=band(-120, -150, fistKind='palm'), af=band(-30, -100), bob=(2, 2, 2), lean=(0, 1), **LOW),    # the palm whipped up: the geodes burst at the target
     g(an=band(-115, -155), af=band(-30, -100), bob=(1, 1, 1), lean=(0, 0), **LOW),                       # clenched into a fist overhead
     g(an=band(-115, -155), af=band(-30, -100), bob=(1, 1, 1), lean=(0, 0), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'roar', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'),
       extra={'targetState': {'rule': 'Geode Blast: on the active frame (the palm whips up, frame 5) the testbed plays geodeBlasted once on every fighter in the blast (crystal spikes burst up round it, shards spray, it flinches and bleeds), then its idle', 'state': 'geodeBlasted', 'loopFrom': None, 'element': 'earth'}},
       anchored={2: [('cryst', 'head', -9, 12), ('cryst', 'head', 9, 18)],
                 3: [('crack1', 'feet', 14, -1), ('crackGlow', 'feet', 14, -2), ('dust1', 'feet', 15, -4), ('rocks', 'feet', 12, -8)],
                 4: [('crack2', 'feet', 16, -1), ('crackRun', 'feet', 24, -1), ('dust1', 'feet', 20, -3), ('gemSpark', 'feet', 14, -6)],
                 5: [('crackRun', 'feet', 26, -1, {'alpha': {'C': 170, 'K': 170}}), ('gemSpark', 'hand', 0, -3)],
                 6: [('gemSpark', 'hand', 0, -2), ('cryst', 'hand', 3, 4)], 7: [('cryst', 'hand', -2, 5)]})),
 'geodeBlasted': ('Geode Blasted', 1,
  'Geode Blasted (target state of Geode Blast, plays once): the floor under the fighter cracks, glowing teal; clusters of jagged crystal spikes burst up out of it round its feet, in front and behind, shards and grit spraying out, and the fighter flinches back with its guard up over its face, small cuts bleeding (Bleed); the spikes stand a beat, then crack and crumble into rubble, and the fighter drops back into its guard.', [
     g(bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(0, 0, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(0, 0, 1), lean=(-1, -3)),
     g(an=band(-55, -150), af=band(-45, -140), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 2), lean=(0, -1), root=(1, 0)),
     g()],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'squint', None],
  None,
  dict(fps=10, rm='E: -1 flinching back, +1 recovering',
       anchored={0: [('crack2', 'feet', 0, -1), ('crackGlow', 'feet', 0, -2)],
                 1: [('geoSmallB', 'feet', -2, -6, {'behind': True}), ('geoSmall', 'feet', 3, -5), ('rocks', 'feet', -10, -12), ('rocks', 'feet', 11, -10)],
                 2: [('geoBack', 'feet', -2, -15, {'behind': True}), ('geoFrontL', 'feet', -8, -11), ('geoFrontR', 'feet', 9, -12), ('shardFly', 'head', -10, 18), ('shardFly', 'head', 11, 14), ('gemShard', 'head', -12, 6), ('bloodN', 'head', 3, 14)],
                 3: [('geoBack', 'feet', -2, -15, {'behind': True}), ('geoFrontL', 'feet', -8, -11), ('geoFrontR', 'feet', 9, -12), ('shardFly', 'head', -14, 10), ('shardFly', 'head', 14, 6), ('gemShard', 'head', -15, -2), ('gemShard', 'head', 15, 0), ('bloodN', 'head', 4, 16), ('bloodN', 'head', -3, 22)],
                 4: [('geoBack2', 'feet', -2, -10, {'behind': True, 'alpha': {'C': 200, 'c': 200, 'T': 200}}), ('geoFrontL2', 'feet', -8, -7, {'alpha': {'C': 200, 'c': 200, 'T': 200}}), ('geoFrontR2', 'feet', 9, -8, {'alpha': {'C': 200, 'c': 200, 'T': 200}}), ('gemShard', 'head', -16, 14), ('gemShard', 'head', 16, 18), ('bloodN', 'head', 4, 18)],
                 5: [('rubble', 'feet', -7, -2), ('rubble', 'feet', 8, -2), ('dust1', 'feet', 0, -3)]})),
 'mausoleum': ('Mausoleum', 1,
  'Mausoleum (Capricorn ninjutsu, Elemental 6, Terrain, Wall 2 rounds, Root 1 round STR save DC 14: the fighter calls up entombing walls that root the foe), v3 (Christopher 2026-10-30: still not cool enough; make it big): from the guard the fighter claps its palms together in the seal before its chest, eyes closing, and a ring of glowing crystal glyphs opens in the floor under the target; it sweeps both palms down low and heaves them up with a roar, and the tomb erupts round the target in plumes of stone dust: a tall arched headstone behind it, a fluted pillar either side and a carved front slab grinding up to its chest; then it raises both fists high overhead and hammers them down at the floor, and a great capstone slams down out of the sky onto the pillars with a shockwave of dust and rubble; the great Capricorn sigil carved in the front slab blazes up crystal teal, light leaking from every joint, and the fighter holds the hammer pose, then rises back into the guard (the target plays mausoleumSealed).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),                                                                    # palms clapped in the seal: the glyph ring opens
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-40, -45, fistKind='palm'), af=band(-30, -55, fistKind='palm'), bob=(4, 5, 5), lean=(1, 6), **BRACE),          # palms swept low over the floor
     g(an=band(-110, -150, fistKind='palm'), af=band(-100, -145, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), **LOW),         # heaved up: the tomb erupts
     g(an=band(-130, -160, fistKind='palm'), af=band(-120, -155, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1), **LOW),
     g(an=band(-165, -178), af=band(-160, -176), bob=(0, -1, 0), lean=(0, -1)),                                                 # both fists raised high overhead
     g(an=band(-40, -45), af=band(-35, -50), bob=(5, 6, 6), lean=(1, 8), **BRACE),                                               # hammered down at the floor: the capstone slams
     g(an=band(-40, -45), af=band(-35, -50), bob=(5, 6, 6), lean=(1, 8), **BRACE),
     g(an=band(-40, -45), af=band(-35, -50), bob=(5, 6, 7), lean=(1, 8), **BRACE),
     g(an=band(-50, -120), af=band(-40, -110), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'closed', 'closed', 'strain', 'roar', 'roar', 'strain', 'roar', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'),
       extra={'targetState': {'rule': 'Mausoleum v3: from the active frame (frame 1, the seal) the target plays mausoleumSealed: frames 0-7 once (glyph ring, the headstone, pillars and front slab erupt, the capstone slams on frame 6 as the caster hammers down, the glyphs ignite), then frames 8-11 on loop (the glyphs pulse, the target strains) until the Root ends; the tomb is terrain for 2 rounds: while it stands the testbed keeps drawing it round that hex (loop frames)', 'state': 'mausoleumSealed', 'loopFrom': 8, 'element': 'earth', 'wallRounds': 2, 'breakFree': 'mausoleumBreakOut'}},
       anchored={1: [('gemSpark', 'hand', 0, -4)],
                 3: [('crack2', 'feet', 9, -1), ('dust1', 'feet', 12, -3)],
                 4: [('plume', 'feet', 12, -6), ('rocks', 'feet', 15, -10), ('cryst', 'hand', 0, -3)],
                 5: [('dust2', 'feet', 12, -3), ('cryst', 'hand', -3, -5)],
                 6: [('gemSpark', 'hand', 0, -3), ('gemSpark', 'farhand', 0, -3)],
                 7: [('crack2', 'feet', 10, -1), ('plumeWide', 'feet', 12, -5), ('rocks', 'feet', 16, -10), ('rocks', 'feet', 6, -8)],
                 8: [('crack2', 'feet', 10, -1), ('plume', 'feet', 14, -8, {'alpha': {'e': 190, 'E': 190, 'H': 200}})],
                 9: [('crack1', 'feet', 10, -1), ('dust1', 'feet', 14, -4)]})),
 'mausoleumSealed': ('Sealed in the Mausoleum', 4,
  'Sealed in the Mausoleum (target state of Mausoleum v3, Root 1 round): a ring of glowing crystal glyphs opens in the floor under the fighter, shafts of teal light shooting up from it; the tomb erupts round it in plumes of stone dust, a tall arched headstone behind, a fluted pillar either side and a carved front slab grinding up to its chest, pinning it; it looks up as a great capstone falls out of the sky and slams onto the pillars with a shockwave of dust and rubble, jolting it; a great sigil carved in the front slab, the goat-fish of Capricorn in a ring, blazes crystal teal and light leaks from every joint of the stone, and (looping until the Root ends) it pulses while the fighter strains inside, grit trickling from the capstone.', [
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(2, 2, 3), lean=(0, 0)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(2, 2, 2), lean=(0, 0)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 2), lean=(0, -1))],
  ['squint', 'pain', 'pain', 'pain', 'squint', 'squint', 'pain', 'strain', 'strain', 'pain', 'strain', 'pain'],
  None,
  dict(fps=10, extra={'loop': True, 'loopFrom': 8, 'breakFree': {'rule': 'Mausoleum v3 (Christopher 2026-10-30: a break-free animation): when the Root ends the testbed plays mausoleumBreakOut once (the front slab is smashed and the whole tomb crumbles into rubble; Christopher 2026-10-30), then the idle', 'state': 'mausoleumBreakOut'}},
       anchored={0: [('ringDim', 'feet', 0, -1), ('crack1', 'feet', 0, -1)],
                 1: [('ringLit', 'feet', 0, -1), ('lightBeam', 'feet', -12, -20, {'alpha': {'c': 150, 'C': 170}}), ('lightBeam', 'feet', 12, -20, {'alpha': {'c': 150, 'C': 170}}), ('lightBeam', 'feet', 0, -22, {'alpha': {'c': 120, 'C': 140}}), ('tombBack1', 'feet', -2, -8.5, {'behind': True}), ('pillar1', 'feet', -16, -8.5), ('pillar1', 'feet', 16, -8.5), ('plume', 'feet', -16, -8), ('plume', 'feet', 16, -8)],
                 2: [('ringLit', 'feet', 0, -1), ('lightBeam', 'feet', -8, -24, {'alpha': {'c': 120, 'C': 140}}), ('lightBeam', 'feet', 9, -24, {'alpha': {'c': 120, 'C': 140}}), ('tombBack2', 'feet', -2, -17.5, {'behind': True}), ('pillar2', 'feet', -16, -18), ('pillar2', 'feet', 16, -18), ('tombSlab1', 'feet', 2, -5.5), ('plume2', 'feet', -17, -20), ('plume2', 'feet', 17, -18), ('rocks', 'feet', 0, -26)],
                 3: [('ringLit', 'feet', 0, -1), ('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab2', 'feet', 2, -11.5), ('plume', 'feet', -18, -44), ('plume', 'feet', 18, -40), ('rocks', 'feet', 8, -28)],
                 4: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('plumeWide', 'feet', 2, -36), ('rocks', 'feet', -6, -40)],
                 5: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('roofBig', 'feet', 0, -67)],
                 6: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('roofBig', 'feet', 0, -59.5), ('plumeWide', 'feet', -18, -52), ('plumeWide', 'feet', 18, -52), ('rocks', 'feet', -22, -44), ('rocks', 'feet', 22, -40), ('plumeWide', 'feet', 0, -4)],
                 7: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('sigilLit', 'feet', 2, -18), ('slabGlow', 'feet', 2, -17.5, {'alpha': {'C': 170}}), ('roofBig', 'feet', 0, -59.5), ('plume', 'feet', -20, -50, {'alpha': {'e': 170, 'E': 170, 'H': 180}}), ('gemBurst2', 'feet', 2, -18)],
                 8: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('sigilLit', 'feet', 2, -18), ('slabGlow', 'feet', 2, -17.5, {'alpha': {'C': 170}}), ('roofBig', 'feet', 0, -59.5)],
                 9: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('sigilLit', 'feet', 2, -18, {'alpha': {'c': 190, 'W': 200}}), ('slabGlow', 'feet', 2, -17.5, {'alpha': {'C': 110}}), ('roofBig', 'feet', 0, -59.5), ('grains', 'feet', 9, -48)],
                 10: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('sigilDim', 'feet', 2, -18), ('roofBig', 'feet', 0, -59.5)],
                 11: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('tombSlab', 'feet', 2, -17.5), ('sigilLit', 'feet', 2, -18, {'alpha': {'c': 190, 'W': 200}}), ('slabGlow', 'feet', 2, -17.5, {'alpha': {'C': 110}}), ('roofBig', 'feet', 0, -59.5), ('grains', 'feet', -8, -46)]})),
 'mausoleumBreakOut': ('Mausoleum Break Out', 3,
  'Mausoleum Break Out (target state of Mausoleum v3, plays once when the Root ends; Christopher 2026-10-30: a break-free animation, and the tomb crumbles to the ground instead of disappearing): sealed in the tomb up to its chest, the fighter strains and cracks split the front slab, spreading, the Capricorn sigil on it flickering and dying; then it drives both palms forward with a roar and the slab explodes outward, blocks of stone flying in a ring and a plume of stone dust bursting off; with its front gone the tomb gives way: cracks run up the pillars and headstone, the capstone tips and breaks apart into falling blocks, and the pillars and headstone crumble downward into a heap of rubble in a rolling cloud of dust while the fighter covers its head; the dust settles over the rubble and the fighter drops back into its guard.', [
     g(an=band(-10, -30), af=band(-8, -25), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-10, -30), af=band(-8, -25), bob=(2, 2, 2), lean=(0, 2), **BRACE),
     g(an=band(-10, -30), af=band(-8, -25), bob=(2, 2, 3), lean=(-1, -1), **BRACE),
     g(an=band(-92, -92, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 4), root=(1, 0)),
     g(an=band(-92, -92, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 4)),
     g(an=band(-60, -120), af=band(-50, -115), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-60, -155), af=band(-50, -145), bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-60, -155), af=band(-50, -145), bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-60, -155), af=band(-50, -145), bob=(2, 2, 3), lean=(0, 0), **LOW),
     g(an=band(-50, -130), af=band(-45, -125), bob=(1, 1, 2), lean=(0, 0), **LOW),
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g(),
     g()],
  ['strain', 'strain', 'pain', 'roar', 'roar', 'squint', 'pain', 'pain', 'squint', 'squint', 'squint', None, None],
  None,
  dict(fps=10, rm='E: +1 bursting out, -1 settling back',
       extra={'crumble': {'rule': 'Mausoleum v3 (Christopher 2026-10-30): the tomb does not vanish: after the front slab bursts it crumbles to the ground in this clip (frames 5-9) and leaves a heap of rubble; the wall terrain ends with it', 'rubble': 'rubbleHeap2'}},
       anchored={0: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('roofBig', 'feet', 0, -59.5), ('tombSlab', 'feet', 2, -17.5), ('sigilLit', 'feet', 2, -18, {'alpha': {'c': 190, 'W': 200}}), ('slabCrack1', 'feet', 2, -17.5)],
                 1: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('roofBig', 'feet', 0, -59.5), ('tombSlab', 'feet', 2, -17.5), ('sigilDim', 'feet', 2, -18), ('slabCrack2', 'feet', 2, -17.5), ('grains', 'feet', 6, -30)],
                 2: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('roofBig', 'feet', 0, -59.5), ('tombSlab', 'feet', 2, -17.5), ('slabCrack2', 'feet', 2, -17.5), ('gemCrack', 'feet', 2, -18), ('rocks', 'feet', 10, -34), ('rocks', 'feet', -6, -32)],
                 3: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('roofBig', 'feet', 0, -59.5), ('stoneShatter12', 'feet', 4, -18), ('plume2', 'feet', 8, -16), ('gemBurst2', 'feet', 4, -18)],
                 4: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('roofBig', 'feet', 0, -59.5), ('stoneShatter18', 'feet', 4, -16), ('plumeWide', 'feet', 6, -10, {'alpha': {'e': 190, 'E': 190, 'H': 200}})],
                 5: [('tombBack', 'feet', -2, -26.5, {'behind': True}), ('pillar', 'feet', -16, -27), ('pillar', 'feet', 16, -27), ('roofBig', 'feet', 0, -59.5), ('gemCrack', 'feet', -16, -40), ('gemCrack', 'feet', 16, -30), ('gemCrack', 'feet', -4, -48), ('stoneShatter23', 'feet', 4, -12, {'alpha': {'G': 200, 'N': 200, 'H': 200, '#': 200}}), ('rubble', 'feet', 10, -2)],
                 6: [('tombBackC42', 'feet', -2, -20.5, {'behind': True}), ('pillarC44', 'feet', -16, -21.5), ('pillarC44', 'feet', 16, -21.5), ('roofTilt', 'feet', 2, -55.5), ('gemCrack', 'feet', -16, -26), ('gemCrack', 'feet', 16, -22), ('plume', 'feet', -16, -44), ('rubble', 'feet', 10, -2)],
                 7: [('tombBackC28', 'feet', -2, -13.5, {'behind': True}), ('pillarC30', 'feet', -16, -14.5), ('pillarC30', 'feet', 16, -14.5), ('roofBlocks', 'feet', 0, -44), ('plume2', 'feet', -17, -30), ('plume2', 'feet', 17, -28), ('rubble', 'feet', 10, -2), ('rubble', 'feet', -10, -2)],
                 8: [('tombBackC14', 'feet', -2, -6.5, {'behind': True}), ('pillarC16', 'feet', -16, -7.5), ('pillarC16', 'feet', 16, -7.5), ('stoneShatter18', 'feet', 0, -24), ('plumeWide', 'feet', -10, -14), ('plumeWide', 'feet', 12, -12), ('rubbleHeap', 'feet', 0, -4)],
                 9: [('rubbleHeap', 'feet', 0, -4), ('plumeWide', 'feet', -10, -8, {'alpha': {'e': 180, 'E': 180, 'H': 190}}), ('plumeWide', 'feet', 12, -6, {'alpha': {'e': 180, 'E': 180, 'H': 190}}), ('rocks', 'feet', -20, -6), ('rocks', 'feet', 20, -4)],
                 10: [('rubbleHeap', 'feet', 0, -4, {'behind': True}), ('plume', 'feet', -14, -6, {'alpha': {'e': 130, 'E': 130, 'H': 140}}), ('plume', 'feet', 14, -6, {'alpha': {'e': 130, 'E': 130, 'H': 140}})],
                 11: [('rubbleHeap2', 'feet', 0, -2.5, {'behind': True})], 12: [('rubbleHeap2', 'feet', 0, -2.5, {'behind': True})]})),
 'stalactiteRain': ('Stalactite Rain', 10,
  'Stalactite Rain (Capricorn ninjutsu ultimate, charge, Elemental 30, wide AoE: the fighter channels its chakra through the earth, forming giant spear-like crystal formations), v2 (Christopher 2026-10-29: the crystal spears rise from behind the caster, then rain down on the target): from the guard the fighter makes the seal and sinks deep, straining, an earthen aura flaring with crystal glints; it slams both open palms down at the floor and the ground cracks behind it, glowing teal, and giant crystal spears grind up out of the earth behind it, point first, growing over three frames until they tower over its head; it heaves both palms up and the spears tear free of the ground and shoot up into the sky; then it hurls the near hand forward and down at the target, and the spears rain down out of the sky onto the target zone (the target plays stalactiteImpaled); it holds the throw, then settles back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE)] + [
     g(an=band(-35, -40, fistKind='palm'), af=band(-30, -45, fistKind='palm'), bob=(5, 6, 6), lean=(1, 7), **BRACE) for _ in range(4)] + [   # both palms slammed down: the spears grow behind
     g(an=band(-110, -150, fistKind='palm'), af=band(-100, -145, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), **LOW),   # heaving up: the spears tear free
     g(an=band(-160, -176, fistKind='palm'), af=band(-155, -174, fistKind='palm'), bob=(0, -1, 0), lean=(0, -1)),        # arms up: the spears shoot into the sky
     g(an=band(-110, -115, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **LOW),        # hurled forward and down at the target: the spears rain down
     g(an=band(-100, -105, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-100, -105, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-80, -110, fistKind='palm'), af=band(-40, 215), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'strain', 'strain', 'strain', 'strain', 'roar', 'roar', 'strain', 'strain', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'), rm='E: +1 into the throw, -1 settling back',
       extra={'targetState': {'rule': 'Stalactite Rain v2 (ultimate, charge): on the active frame (frame 10, the throw) the testbed plays stalactiteImpaled once on every fighter in the zone (crystal spears rain down out of the sky and stab into the ground round it, then shatter), then its idle', 'state': 'stalactiteImpaled', 'loopFrom': None, 'element': 'earth'}},
       anchored={2: [('cryst', 'head', -9, 12), ('cryst', 'head', 9, 16)],
                 3: [('cryst', 'head', -10, 18), ('gemSpark', 'head', 10, 10), ('crack1', 'feet', -14, -1)],
                 4: [('crack2', 'feet', -14, -1), ('crackGlow', 'feet', -14, -2), ('spearUpS1', 'feet', -11, -4.0, {'behind': True}), ('spearUp1', 'feet', -19, -5.5, {'behind': True}), ('rocks', 'feet', -14, -8)],
                 5: [('crack2', 'feet', -14, -1), ('spearUpS2', 'feet', -11, -9.5, {'behind': True}), ('spearUp2', 'feet', -19, -12.5, {'behind': True}), ('dust1', 'feet', -14, -3)],
                 6: [('crack2', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0, {'behind': True}), ('spearUp', 'feet', -19, -20.0, {'behind': True}), ('dust1', 'feet', -20, -3), ('gemSpark', 'feet', -19, -40)],
                 7: [('crack2', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0, {'behind': True}), ('spearUp', 'feet', -19, -20.0, {'behind': True}), ('gemSpark', 'feet', -12, -30), ('gemSpark', 'feet', -21, -36)],
                 8: [('crack2', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0 - 10, {'behind': True}), ('spearUp', 'feet', -19, -20.0 - 12, {'behind': True}), ('rocks', 'feet', -14, -6), ('dust2', 'feet', -14, -3)],
                 9: [('crack1', 'feet', -14, -1), ('spearUpS', 'feet', -11, -15.0 - 30, {'behind': True}), ('spearUp', 'feet', -19, -20.0 - 34, {'behind': True}), ('spearStreak', 'feet', -11, -10), ('spearStreak', 'feet', -19, -14)],
                 10: [('spearStreak', 'feet', -12, -48), ('spearStreak', 'feet', -19, -52), ('gemSpark', 'hand', 2, -2)],
                 11: [('gemSpark', 'hand', 2, -3)], 12: [('cryst', 'hand', 3, -2)]})),
 'stalactiteImpaled': ('Stalactite Rain Struck', 2,
  'Stalactite Rain Struck (target state of Stalactite Rain v2, plays once): crystal glints flash in the sky over the fighter and it looks up; then giant crystal spears rain down out of the sky at a slant from the caster\'s side and stab deep into the ground all round it, in front and behind, dust and grit bursting off each impact, and it is jolted in pain, shards spraying; a second volley drives in; the spears stand embedded a beat, crack and shatter, crystal chunks and shards bursting outward and raining down into rubble, and the fighter staggers and drops back into its guard.', [
     g(an=band(-40, -120), af=band(-35, -115), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-20, -60), af=band(-15, -55), bob=(0, -1, 0), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-20, -60), af=band(-15, -55), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(-25, -70), af=band(-20, -65), bob=(0, 0, 0), lean=(-1, -2)),
     g(an=band(-40, -110), af=band(-35, -105), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-60, -150), af=band(-50, -140), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-40, -120), af=band(-35, -115), bob=(2, 2, 3), lean=(1, 2), root=(1, 0), **LOW),
     g()],
  ['squint', 'pain', 'roar', 'pain', 'pain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=10, rm='E: -1 jolted back, +1 recovering',
       anchored={0: [('gemSpark', 'head', 10, -6), ('gemSpark', 'head', -6, -8), ('spearStreak', 'head', 14, -8)],
                 1: [('spearFall', 'head', 12, 0), ('spearFallS', 'head', -4, -2), ('spearStreak', 'head', 20, -8)],
                 2: [('spearFall', 'feet', 11, -10, {'behind': True}), ('spearFallS', 'feet', -10, -8), ('dust2', 'feet', 9, -3), ('dust1', 'feet', -12, -3), ('gemShard2', 'head', 14, 10), ('bloodN', 'head', 3, 16), ('spearFall', 'head', 8, -6)],
                 3: [('spearFall', 'feet', 11, -10, {'behind': True}), ('spearFallS', 'feet', -10, -8), ('spearFall', 'feet', 2, -11, {'behind': True}), ('spearFallS', 'feet', 17, -8), ('dust2', 'feet', 0, -3), ('shardFly', 'head', -15, 4), ('shardFly', 'head', 16, 2)],
                 4: [('spearFall', 'feet', 11, -10, {'behind': True}), ('spearFallS', 'feet', -10, -8), ('spearFall', 'feet', 2, -11, {'behind': True}), ('spearFallS', 'feet', 17, -8), ('gemCrack', 'feet', 10, -18), ('gemCrack', 'feet', -9, -14)],
                 5: [('gemBurst2', 'feet', 2, -12), ('gemShard2', 'head', -16, 8), ('gemShard2', 'head', 16, 12), ('gemShard', 'head', -6, -4), ('gemShard', 'head', 8, -6), ('rubble', 'feet', -9, -2), ('rubble', 'feet', 10, -2)],
                 6: [('rubble', 'feet', -9, -2), ('rubble', 'feet', 9, -2), ('gemShard', 'head', -17, 18), ('gemShard', 'head', 17, 22), ('dust2', 'feet', 0, -3)],
                 7: [('rubble', 'feet', -9, -2), ('rubble', 'feet', 9, -2), ('gemShard', 'feet', -16, -4), ('gemShard', 'feet', 15, -3)]})),
 'atlasRegret': ('Atlas\'s Regret', 3,
  'Atlas\'s Regret (Capricorn genjutsu, mental debuff, Slow 2 rounds STR save DC 13, ~12 m: the caster projects the weight of the world onto its opponent): from the guard the fighter raises both open hands before its chest, palms down, its eyes kindling crystal teal; then it presses them slowly down, sinking into its knees as if forcing a great weight onto the foe, the eyes blazing, and holds the press, arms trembling, before rising back into the guard. On the target (the testbed plays atlasBurdened from the active frame, with the genjutsu mark in earth colours): an illusory world, a soil-brown globe with crystal-teal seas, forms over its head and settles onto its shoulders, and it buckles into a deep crouch with both hands raised to hold it up, trembling under the weight while the Slow lasts.', [
     g(),
     g(an=band(-80, -140, fistKind='palm'), af=band(-75, -135, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-85, -145, fistKind='palm'), af=band(-80, -140, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-70, -80, fistKind='palm'), af=band(-65, -75, fistKind='palm'), bob=(3, 3, 3), lean=(1, 3), **LOW),
     g(an=band(-55, -50, fistKind='palm'), af=band(-50, -45, fistKind='palm'), bob=(4, 5, 5), lean=(1, 5), **BRACE),
     g(an=band(-55, -50, fistKind='palm'), af=band(-50, -45, fistKind='palm'), bob=(4, 5, 5), lean=(1, 5), root=(1, 0), **BRACE),
     g(an=band(-55, -50, fistKind='palm'), af=band(-50, -45, fistKind='palm'), bob=(4, 5, 6), lean=(1, 5), root=(-1, 0), **BRACE),
     g(an=band(-40, -110), af=band(-35, -105), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'strain', None, None],
  [0, 0, 1, 1, 2, 2, 2, 1, 0],
  dict(fps=10, auraColors=('#7fe3d0', '#8a6236'), rm='a 1 px tremble on frames 5-6 (net 0)',
       extra={'targetState': {'rule': 'Atlas\'s Regret: from the active frame (frame 3, the press begins) the target plays atlasBurdened: frames 0-3 once (the globe forms and settles on its shoulders, it buckles), then frames 4-7 on loop until the Slow ends, then its idle; the genjutsu mark (genjutsuAfflicted halo, aura, eye glow, earth colours) is drawn over it throughout', 'state': 'atlasBurdened', 'loopFrom': 4, 'element': 'earth', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeC', 'eye', 0, 0), ('globeS', 'hand', 4, -8, {'alpha': {'C': 150, 'c': 150, 'e': 140, 'E': 140, 'T': 150}})],
                 2: [('eyeCF', 'eye', 0, 0), ('globeS', 'hand', 4, -8)],
                 3: [('eyeCF', 'eye', 0, 0), ('globeM', 'hand', 5, -6, {'alpha': {'C': 180, 'c': 180, 'e': 160, 'E': 160, 'T': 170}})],
                 4: [('eyeCF', 'eye', 0, 0), ('gp1', 'feet', 16, -24)], 5: [('eyeCF', 'eye', 0, 0), ('gp2', 'feet', 20, -18)], 6: [('eyeC', 'eye', 0, 0), ('gp3d', 'feet', 24, -12)]})),
 'atlasBurdened': ('Burdened by the World', 2,
  'Burdened by the World (target state of Atlas\'s Regret, Slow 2 rounds), v3 (Christopher 2026-10-30: arms down by the sides; movement under the Slow gets its own walk, atlasBurdenedWalk, that ends in this kneel): an illusory world, a soil-brown globe with crystal-teal seas and glinting lines of latitude, forms out of the air over the fighter\'s head and sinks onto its shoulders; its guard drops, the arms hang limp at its sides, the knees buckle and it sinks onto one knee; then (looping while the Slow lasts) it trembles on its knee under the slowly turning globe, sweat flying off it.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 3), lean=(0, 1), **LOW),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(4, 5, 5), lean=(1, 3), **BRACE),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(7, 7, 8), lean=(1, 4), ln='ar-buckle-rear', lf='ar-buckle-lead'),
     g(an=AR_KNEEL_N, af=AR_KNEEL_F, bob=(9, 10, 10), lean=(1, 3), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=AR_KNEEL_N, af=AR_KNEEL_F, bob=(9, 10, 10), lean=(1, 3), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=AR_KNEEL_N, af=AR_KNEEL_F, bob=(10, 10, 11), lean=(1, 4), root=(1, 0), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=AR_KNEEL_N, af=AR_KNEEL_F, bob=(9, 10, 10), lean=(1, 3), root=(-1, 0), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=AR_KNEEL_N, af=AR_KNEEL_F, bob=(10, 10, 11), lean=(1, 4), ln='ss-kneel-rear', lf='ss-kneel-lead')],
  ['squint', 'pain', 'strain', 'pain', 'strain', 'strain', 'pain', 'strain', 'pain'],
  None,
  dict(fps=7, rm='in place; +1/-1 tremble in the loop (net 0)',
       extra={'loop': True, 'loopFrom': 5, 'walk': {'rule': 'Burdened by the World v3 (Christopher 2026-10-30): while the Slow lasts, any movement plays atlasBurdenedWalk (rise from the kneel once, then the burdened walk loop) instead of the walk; when the move ends the fighter plays frames 3-4 of this state (the knees give, it sinks onto its knee) and returns to this loop', 'state': 'atlasBurdenedWalk', 'loopFrom': 2, 'stop': [3, 4]}},
       anchored={0: [('globeS', 'head', 0, -12, {'alpha': {'C': 150, 'c': 150, 'e': 140, 'E': 140, 'T': 150}})],
                 1: [('globeM', 'head', 0, -14, {'alpha': {'C': 200, 'c': 200, 'e': 190, 'E': 190, 'T': 200}})],
                 2: [('globe0', 'head', -2, -10, {'behind': True}), ('dust1', 'feet', -8, -3), ('dust1', 'feet', 8, -3)],
                 3: [('globe1', 'head', -2, -10, {'behind': True}), ('sweat', 'head', 7, 0)],
                 4: [('globe2', 'head', -2, -9, {'behind': True}), ('dust2', 'feet', 0, -3)],
                 5: [('globe3', 'head', -2, -9, {'behind': True}), ('sweat', 'head', 7, 0)],
                 6: [('globe0', 'head', -2, -9, {'behind': True}), ('sweat', 'head', -7, 2), ('sweat', 'head', 9, 4)],
                 7: [('globe1', 'head', -2, -9, {'behind': True}), ('sweat', 'head', 8, -2)],
                 8: [('globe2', 'head', -2, -9, {'behind': True}), ('sweat', 'head', -8, 0), ('grains', 'feet', 0, -2)]})),
 'atlasBurdenedWalk': ('Burdened Walk', 0,
  'Burdened Walk (movement under Atlas\'s Regret, Slow 2 rounds; Christopher 2026-10-30: a separate slow, struggling walk that ends in the kneeling pose): from the kneel the fighter heaves itself up, the illusory globe still on its shoulders; then it trudges, a slow walk cycle bent forward under the weight, knees deep, arms hanging limp and swaying, short heavy strides that scuff the floor, its whole body dropping on each footfall, sweat flying; when the move ends it sinks back onto its knee (frames 3-4 of atlasBurdened).', [
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(7, 7, 8), lean=(1, 4), ln='ar-buckle-rear', lf='ar-buckle-lead'),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(5, 5, 6), lean=(1, 4), **BRACE),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(5, 5, 6), lean=(1, 5), root=(3, 0), ln='aw-0-near', lf='aw-4-far'),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(6, 6, 7), lean=(1, 5), root=(3, 0), ln='aw-1-near', lf='aw-5-far'),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(5, 5, 6), lean=(1, 5), root=(3, 0), ln='aw-2-near', lf='aw-6-far'),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(4, 5, 5), lean=(1, 5), root=(3, 0), ln='aw-3-near', lf='aw-7-far'),
     g(an=AR_SWAY_N, af=AR_SWAY_F, bob=(5, 5, 6), lean=(1, 5), root=(3, 0), ln='aw-4-near', lf='aw-0-far'),
     g(an=AR_SWAY_N, af=AR_SWAY_F, bob=(6, 6, 7), lean=(1, 5), root=(3, 0), ln='aw-5-near', lf='aw-1-far'),
     g(an=AR_SWAY_N, af=AR_SWAY_F, bob=(5, 5, 6), lean=(1, 5), root=(3, 0), ln='aw-6-near', lf='aw-2-far'),
     g(an=AR_SWAY_N, af=AR_SWAY_F, bob=(4, 5, 5), lean=(1, 5), root=(3, 0), ln='aw-7-near', lf='aw-3-far'),
  ],
  ['strain', 'pain', 'strain', 'pain', 'strain', 'strain', 'strain', 'pain', 'strain', 'strain'],
  None,
  dict(fps=6, rm='E: +3 per walk frame (frames 2-9, matching the planted foot sliding back 3 px a frame; at 6 fps it covers ground at about 3/4 of the normal walk\'s pace); the testbed paces the move along the path at this speed',
       extra={'loop': True, 'loopFrom': 2},
       anchored={0: [('globe0', 'head', -2, -9, {'behind': True}), ('sweat', 'head', 7, 0)], 1: [('globe1', 'head', -2, -10, {'behind': True}), ('sweat', 'head', -7, 2)], 2: [('globe2', 'head', -2, -10, {'behind': True}), ('dust1', 'feet', 6, -2)], 3: [('globe2', 'head', -2, -10, {'behind': True}), ('sweat', 'head', 7, 0)], 4: [('globe3', 'head', -2, -10, {'behind': True})], 5: [('globe3', 'head', -2, -10, {'behind': True}), ('grains', 'feet', -6, -2)], 6: [('globe0', 'head', -2, -10, {'behind': True}), ('dust1', 'feet', 6, -2)], 7: [('globe0', 'head', -2, -10, {'behind': True}), ('sweat', 'head', -8, 2)], 8: [('globe1', 'head', -2, -10, {'behind': True})], 9: [('globe1', 'head', -2, -10, {'behind': True}), ('grains', 'feet', -6, -2)]})),
 'titansGaze': ('Titan\'s Gaze', 4,
  'Titan\'s Gaze (Capricorn genjutsu, mental debuff, Slow 2 rounds INT save DC 12, ~12 m: the caster invokes the terrifying gaze of a giant into the mind\'s eye of its opponent, so it seizes up with fear): from the guard the fighter raises two fingers up beside its near eye, the eyes kindling and then blazing crystal teal, a stone-grey aura rising; a great slit goat\'s eye opening in the air behind its head (v2, Christopher 2026-10-30: "needs more cool"); then it thrusts the hand out at the target, two fingers pointing, a dotted beam of teal light flashing off the fingertips, and holds the stare, the eye blazing, then closing, before lowering the hand back into the guard. On the target (the testbed plays titanGazed from the active frame, with the genjutsu mark in earth colours): the horned head of a stone titan rises out of the earth behind it, its slit eyes snap open blazing teal, and the target seizes up as stone crusts over its legs, frozen and trembling while the Slow lasts.', [
     g(),
     g(an=band(-40, -170, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-40, -172, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-40, -172, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-92, -92, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     g(an=band(-92, -92, fistKind='point'), af=band(-30, -100), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-92, -92, fistKind='point'), af=band(-30, -100), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'roar', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#b3aa9a', '#3a9e8f'), rm='E: +1 thrusting the hand out, -1 settling back',
       extra={'targetState': {'rule': 'Titan\'s Gaze: from the active frame (frame 4, the hand thrusts out) the target plays titanGazed: frames 0-6 once (the horned titan rises behind it, its eyes snap open, stone creeps up the target\'s legs), then frames 7-10 on loop until the Slow ends, then its idle; the genjutsu mark (genjutsuAfflicted halo, aura, eye glow, earth colours) is drawn over it throughout', 'state': 'titanGazed', 'loopFrom': 7, 'element': 'earth', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeC', 'eye', 0, 0), ('gazeEye0', 'head', -13, -3, {'behind': True})], 2: [('eyeCF', 'eye', 0, 0), ('gemSpark', 'hand', 0, -2), ('gazeEye1', 'head', -13, -3, {'behind': True})],
                 3: [('eyeCF', 'eye', 0, 0), ('gemSpark', 'hand', 1, -3), ('gazeEye2', 'head', -13, -3, {'behind': True}), ('gemSpark', 'head', -22, -5)],
                 4: [('eyeCF', 'eye', 0, 0), ('gazeEye2', 'head', -13, -3, {'behind': True}), ('gazeBeam', 'hand', 7, 0), ('gemBurst', 'hand', 1, 0)],
                 5: [('eyeCF', 'eye', 0, 0), ('gazeEye2', 'head', -13, -3, {'behind': True}), ('gazeBeam2', 'hand', 8, 0, {'alpha': {'C': 170, 'c': 170}})],
                 6: [('eyeC', 'eye', 0, 0), ('gazeEye1', 'head', -13, -3, {'behind': True, 'alpha': {'C': 150, 'c': 150, 'K': 150}})], 7: [('gazeEye0', 'head', -13, -3, {'behind': True, 'alpha': {'C': 110, 'c': 110}})]})),
 'titanGazed': ('Under the Titan\'s Gaze', 1,
  'Under the Titan\'s Gaze (target state of Titan\'s Gaze, Slow 2 rounds), v2 (Christopher 2026-10-30: "needs more cool"): the ground cracks and rumbles at the fighter\'s feet, and the head of a horned stone titan, the goat of Capricorn, rises up out of the earth behind it in a burst of dust and falling rubble, eyes shut: an angular face of weathered stone with a scowling brow and great ram horns curling round to the sides; its eyes snap open in a flash, slit and blazing crystal teal with a goat\'s bar pupil, the cracks in its face glowing; the fighter recoils, throwing a forearm up over its eyes, then seizes up in a tight crouch as a crust of stone creeps up over its feet and shins; then (looping while the Slow lasts) it trembles, frozen, the titan\'s eyes and glowing seams pulsing over it and pebbles lifting off the ground round its feet.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-50, -150), af=band(-40, -140), bob=(2, 2, 2), lean=(0, -2), **LOW),
     g(an=band(-40, -155), af=band(-30, -148), bob=(2, 2, 3), lean=(-1, -2), **LOW),
     g(an=band(-30, -158), af=band(-25, -150), bob=(2, 2, 3), lean=(-1, -3), **LOW),
     g(an=band(-130, -165), af=band(-30, -150), bob=(1, 1, 1), lean=(-2, -6), root=(-1, 0)),
     g(an=band(-20, -160), af=band(-15, -155), bob=(3, 3, 3), lean=(-1, -3), **LOW),
     g(an=band(-20, -160), af=band(-15, -155), bob=(3, 3, 4), lean=(-1, -3), root=(1, 0), **LOW),
     g(an=band(-20, -160), af=band(-15, -155), bob=(3, 3, 3), lean=(-1, -3), **LOW),
     g(an=band(-22, -161), af=band(-17, -156), bob=(3, 3, 4), lean=(-1, -2), root=(1, 0), **LOW),
     g(an=band(-20, -160), af=band(-15, -155), bob=(3, 3, 3), lean=(-1, -3), root=(-1, 0), **LOW),
     g(an=band(-22, -161), af=band(-17, -156), bob=(3, 3, 4), lean=(-1, -2), **LOW)],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain'],
  None,
  dict(fps=8, rm='E: -1 recoiling from the flash, +1 back as it seizes up (net 0); +1/-1 tremble in the loop (net 0)', extra={'loop': True, 'loopFrom': 7},
       anchored={0: [('gemCrack', 'feet', -10, -2), ('gemCrack', 'feet', 10, -2), ('dust1', 'feet', 0, -3), ('titan2Shut', 'head', 0, 34, {'behind': True, 'alpha': {'H': 110, 'G': 110, 'N': 110, 'C': 110, 'c': 110, 'T': 110, 'K': 110, 'W': 110}})],
                 1: [('titan2Shut', 'head', 0, 22, {'behind': True, 'alpha': {'H': 170, 'G': 170, 'N': 170, 'C': 170, 'c': 170, 'T': 170, 'K': 170, 'W': 170}}), ('plume', 'feet', -17, -7, {'alpha': {'e': 190, 'E': 190, 'H': 200}}), ('plume', 'feet', 17, -7, {'alpha': {'e': 190, 'E': 190, 'H': 200}}), ('rocks', 'head', -20, 0)],
                 2: [('titan2Shut', 'head', 0, 11, {'behind': True, 'alpha': {'H': 210, 'G': 210, 'N': 210, 'C': 210, 'c': 210, 'T': 210, 'K': 210, 'W': 210}}), ('dust2', 'feet', -14, -3), ('dust2', 'feet', 14, -3), ('rocks', 'head', 20, 6), ('rocks', 'head', -22, 12)],
                 3: [('titan2Wake', 'head', 0, 4, {'behind': True, 'alpha': {'H': 220, 'G': 220, 'N': 220, 'C': 220, 'c': 220, 'T': 220, 'K': 220, 'W': 220}}), ('dust1', 'feet', -14, -3), ('rocks', 'feet', 18, -6)],
                 4: [('titan2Lit', 'head', 0, 4, {'behind': True}), ('gemBurst2', 'head', -11, 0), ('gemBurst2', 'head', 11, 0), ('fearLines', 'head', 0, -9)],
                 5: [('titan2Lit', 'head', 0, 5, {'behind': True}), ('gemBurst', 'head', -11, 1), ('gemBurst', 'head', 11, 1), ('crust1', 'feet', 0, -3), ('fearLines', 'head', 0, -9)],
                 6: [('titan2Lit', 'head', 0, 5, {'behind': True}), ('crust2', 'feet', 0, -6), ('pebbles', 'feet', 0, -14), ('sweat', 'head', 7, 1)],
                 7: [('titan2Lit', 'head', 0, 5, {'behind': True}), ('crust2', 'feet', 0, -6), ('pebbles', 'feet', 0, -16), ('sweat', 'head', -7, 2)],
                 8: [('titan2Dim', 'head', 0, 5, {'behind': True, 'alpha': {'H': 230, 'G': 230, 'N': 230, 'C': 230, 'c': 230, 'T': 230, 'K': 230, 'W': 230}}), ('crust2', 'feet', 0, -6), ('pebbles2', 'feet', 0, -19), ('fearLines', 'head', 0, -9, {'alpha': {'C': 160}})],
                 9: [('titan2Lit', 'head', 0, 5, {'behind': True}), ('crust2', 'feet', 0, -6), ('pebbles', 'feet', 1, -21), ('sweat', 'head', 7, 0)],
                 10: [('titan2Dim', 'head', 0, 5, {'behind': True, 'alpha': {'H': 230, 'G': 230, 'N': 230, 'C': 230, 'c': 230, 'T': 230, 'K': 230, 'W': 230}}), ('crust2', 'feet', 0, -6), ('pebbles2', 'feet', -1, -14), ('fearLines', 'head', 0, -9, {'alpha': {'C': 160}})]})),
 'nerveDisruptor': ('Nerve Disruptor', 3,
  'Nerve Disruptor (Aquarius taijutsu strike, Physical 10, Silence 1 round CHA save DC 12: the fighter channels its inner electrical field into a charged jab that disrupts the opponent\'s chakra flow): from the guard the fighter tightens its lead fist and static crackles over it, small arcs leaping off the knuckles and a pale green aura flickering up; then it snaps the lead jab straight out and back, fast; on contact a white-hot spark flash bursts at the fist and jagged lightning forks out from it, a broken electric ring snapping out, sparks scattering; the fist comes back into the guard still fizzing.', [
     g(),
     g(af=band(-55, -125), bob=(1, 1, 1), lean=(0, 0)),
     g(af=band(-55, -125), bob=(1, 1, 1), lean=(0, -1)),
     g(af=band(-88, -88), bob=(1, 1, 1), lean=(1, 4), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(af=band(-88, -88), bob=(1, 1, 1), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(af=band(-75, -105), bob=(1, 1, 1), lean=(1, 2)),
     g(root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 1, 2, 2, 1, 1, 0, 0],
  dict(fps=12, auraColors=('#b8ffc8', '#39e75f'), hitbox=[44, 18, 14, 10], damage='light', rm='E: +1 into the jab, -1 back',
       anchored={1: [('crackle3', 'farhand', 0, 0), ('spark', 'farhand', -3, -3)], 2: [('crackle4', 'farhand', 0, 0), ('sparkL', 'farhand', 2, 3), ('staticV', 'head', -7, 10)],
                 3: [('voltOrb2', 'farhand', 1, 0), ('bolt8', 'farhand', 6, -2), ('crackle4b', 'farhand', 1, 0)],
                 4: [('zapRing6', 'farhand', 3, 0), ('bolt12', 'farhand', 8, -3), ('bolt8b', 'farhand', 6, 4), ('spark', 'farhand', 3, 0)],
                 5: [('zapRing9', 'farhand', 12, 0, {'alpha': {'l': 170, 'L': 170}}), ('spark', 'farhand', 10, -6), ('sparkL', 'farhand', 13, 5)],
                 6: [('crackle3', 'farhand', 0, 0, {'alpha': {'l': 160, 'L': 160}})], 7: [('spark', 'farhand', 0, -2)]})),
 'staticShell': ('Static Shell', 3,
  'Static Shell (Aquarius taijutsu stance, Posture, Counter, Fortified 1 round (10): the fighter lets its inner electrical field radiate from its body as a small EMP field that disrupts the opponent\'s attacks): from the guard the fighter drops its fists to its hips and sets its feet, eyes narrowing; a crackling pale-green aura flares up round it and arcs of static dance over its shoulders, arms and legs, sparks spitting off, a broken electric ring pulsing out at its feet; then it rises back into a tight guard with the static still crackling over it (the testbed keeps a thin crackling aura and a spark or two while the stance holds).', [
     g(),
     g(an=band(15, -40), af=band(5, -35), bob=(1, 1, 1), lean=(0, 0)),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(1, 1, 2), lean=(0, 2), **LOW),
     g(), g()],
  [None, 'squint', 'strain', 'strain', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 3, 2, 2, 1, 1],
  dict(fps=10, auraColors=('#b8ffc8', '#39e75f'),
       extra={'linger': {'rule': 'Static Shell (stance): the clip ends crackling; while the stance holds the testbed keeps a 1 px pale-green aura flickering on the fighter and one or two sparks or short arcs popping on the shoulders and arms each frame, on every state it plays; clears when the stance ends', 'aura': 1, 'auraColors': ['#b8ffc8', '#39e75f'], 'motes': {'pattern': 'spark', 'colors': ['#ffffff', '#b8ffc8', '#39e75f'], 'perFrame': 2}}},
       anchored={2: [('crackle4', 'head', -11, 10), ('staticV', 'head', 11, 14), ('spark', 'head', 10, 2)],
                 3: [('crackle6', 'head', -12, 16), ('bolt8', 'head', 13, 6), ('spark', 'head', 12, 24), ('sparkL', 'head', -11, 30), ('zapRing9', 'feet', 0, -6)],
                 4: [('crackle6b', 'head', 12, 22), ('bolt8b', 'head', -13, 8), ('staticV2', 'head', -12, 26), ('staticV', 'head', 3, -9), ('spark', 'head', -12, 38), ('zapRing12', 'feet', 0, -8, {'alpha': {'l': 190, 'L': 190}})],
                 5: [('crackle4b', 'head', -11, 14), ('bolt8', 'head', 13, 18), ('sparkL', 'head', 11, 32), ('spark', 'head', -11, 36), ('zapRing12', 'feet', 0, -8, {'alpha': {'l': 120, 'L': 120, 'W': 150}})],
                 6: [('crackle4', 'head', 11, 16), ('spark', 'head', -11, 24), ('staticV', 'head', -2, -9)], 7: [('staticV', 'head', -11, 12), ('spark', 'head', 11, 26)], 8: [('sparkL', 'head', 10, 14)]})),
 'shockPalm': ('Shock Palm', 4,
  'Shock Palm (Aquarius taijutsu strike, Physical 16, Debuff: the fighter channels electrical energy into its palm, shocking whoever it touches): from the guard the fighter draws the rear hand back low beside the hip, palm open and turned forward, and a ball of lightning kindles in it, crackling and swelling over two held frames while arcs spiral up round the arm; then it steps in and drives the open palm straight out at chest height, and the charge discharges on contact in a white-hot flash, jagged bolts forking out, an electric shock ring blasting out and sparks scattering; it settles back into the guard.', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'strain', 'squint', 'squint', None, None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='medium', rm='E: +2 stepping into the palm, -2 settling back',
       swirl={1: (0, 0.5), 2: (120, 0.8), 3: (240, 1.0)}, impact={4: 0, 5: 1, 6: 2, 7: 3}, recolor=ELEC_RECOLOR, keepFx=True,
       anchored={1: [('voltOrb2', 'hand', 0, 0)], 2: [('voltOrb3', 'hand', 0, 0), ('crackle4', 'hand', 0, 0)], 3: [('voltOrb4', 'hand', 0, 0), ('crackle6', 'hand', 0, 0), ('spark', 'hand', -2, -8)],
                 4: [('voltOrb4b', 'hand', 2, 0), ('bolt12', 'hand', 9, -4), ('bolt12b', 'hand', 9, 5)],
                 5: [('bolt18', 'hand', 12, -5), ('bolt18b', 'hand', 12, 6), ('crackle6b', 'hand', 3, 0)],
                 6: [('bolt12', 'hand', 10, -7, {'alpha': {'l': 170, 'L': 170}}), ('spark', 'hand', 8, 4), ('sparkL', 'hand', 12, -2)], 7: [('spark', 'hand', 6, -4), ('sparkL', 'hand', 9, 4)]})),
 'voltaicOrb': ('Voltaic Orb', 5,
  'Voltaic Orb (Aquarius ninjutsu, Elemental 14, AoE in the Zone of Awareness: a crackling orb of lightning): from the guard the fighter makes the seal at the chin, then pulls both hands apart before its chest, palms facing, and a ball of lightning kindles between them, crackling and swelling over three frames, arcs leaping to its fingers, a pale green aura rising; then it thrusts both palms out at the target and hurls the orb, which streaks off in a flash; at the target the orb bursts into a crackling sphere of lightning (the target plays voltaicShocked); the fighter settles back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-55, -105, fistKind='palm'), af=band(-45, -140, fistKind='palm'), bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-55, -105, fistKind='palm'), af=band(-45, -140, fistKind='palm'), bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-55, -105, fistKind='palm'), af=band(-45, -140, fistKind='palm'), bob=(2, 2, 2), lean=(0, -2), **LOW),
     g(an=band(-90, -90, fistKind='palm'), af=band(-86, -86, fistKind='palm'), bob=(1, 1, 1), lean=(1, 4), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-86, -86, fistKind='palm'), bob=(1, 1, 1), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'closed', 'squint', 'squint', 'strain', 'roar', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#b8ffc8', '#39e75f'), release=[56, 26], rm='E: +1 thrusting the palms out, -1 back',
       extra={'targetState': {'rule': 'Voltaic Orb: the orb flies from the release point to the target (the testbed draws voltOrb4 streaking along the line); on arrival every fighter in the burst plays voltaicShocked once (the orb bursts into a sphere of lightning round it, it jolts, sparks), then its idle', 'state': 'voltaicShocked', 'loopFrom': None, 'element': 'air', 'projectile': 'voltOrb4'}},
       anchored={1: [('spark', 'hand', 0, -4)], 2: [('voltOrb2', 'hand', 4, 3), ('crackle3', 'hand', 4, 3)], 3: [('voltOrb3', 'hand', 4, 3), ('crackle4', 'hand', 4, 3), ('spark', 'head', -9, 10)],
                 4: [('voltOrb4', 'hand', 4, 3), ('crackle6', 'hand', 4, 3), ('sparkL', 'head', 9, 14)],
                 5: [('voltOrb4b', 'hand', 7, 0), ('bolt8', 'hand', 2, -4), ('bolt8b', 'hand', 2, 4)], 6: [('voltOrb4', 'hand', 18, 0), ('bolt12', 'hand', 8, 0, {'alpha': {'W': 170, 'l': 170, 'L': 170}})], 7: [('spark', 'hand', 2, 0)]})),
 'voltaicShocked': ('Voltaic Shocked', 1,
  'Voltaic Shocked (target state of Voltaic Orb, plays once): the orb of lightning arrives over the fighter and bursts into a crackling sphere round it, bolts forking down through it into the floor; the fighter jolts rigid, arms flung out and back, back arched, eyes squeezed, a white flash over it; it shudders as the sphere crackles and sparks scatter, then the lightning dies away and it drops back into the guard, fizzing.', [
     g(bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(30, -20), af=band(20, -15), bob=(0, -1, -1), lean=(-1, -4)),
     g(an=band(35, -15), af=band(25, -10), bob=(0, -1, -1), lean=(-1, -5), root=(-1, 0)),
     g(an=band(30, -20), af=band(20, -15), bob=(0, -1, -1), lean=(-1, -4), root=(1, 0)),
     g(an=band(35, -15), af=band(25, -10), bob=(0, -1, -1), lean=(-1, -5), root=(-1, 0)),
     g(an=band(-30, -110), af=band(-30, -120), bob=(2, 2, 2), lean=(1, 2), root=(1, 0), **LOW),
     g()],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'squint', None],
  None,
  dict(fps=10, rm='E: a 1 px shudder on frames 2-5 (net 0)',
       anchored={0: [('voltOrb6', 'head', 0, -6)],
                 1: [('voltOrb8', 'head', 0, 6, {'alpha': {'W': 200, 'l': 170, 'L': 170}}), ('zapRing12', 'head', 0, 18), ('boltV', 'head', -8, 30)],
                 2: [('zapRing16', 'head', 0, 18), ('boltV', 'head', 9, 30), ('bolt12', 'head', -14, 4), ('crackle6', 'head', 0, 12)],
                 3: [('zapRing20', 'head', 0, 20, {'alpha': {'W': 170, 'l': 170, 'L': 170}}), ('boltV2', 'head', -10, 32), ('bolt12b', 'head', 14, 10), ('crackle6b', 'head', 0, 22)],
                 4: [('crackle4', 'head', -8, 8), ('crackle4b', 'head', 8, 26), ('spark', 'head', -12, 30), ('sparkL', 'head', 12, 0)],
                 5: [('spark', 'head', 9, 12), ('sparkL', 'head', -9, 30), ('staticV', 'head', 6, -8)], 6: [('spark', 'head', -7, 20)]})),
 'lightningCutter': ('Lightning Cutter', 9,
  'Lightning Cutter (Aquarius ninjutsu, Mental 24, Melee (Reach +6m), Priority, Gap Closer: an instant piercing lightning charge), v4 (Christopher 2026-11-03: the lightning blades cover the hand, not sit below it; v3: play it as a sprinting uppercut to the body with the same fx, the striking arm kept low until the strike is in range; v2 2026-10-30: electric blades envelop the hand while it runs, the strike impales the torso): from the guard the fighter dips and draws the near hand back low as a knife hand, and a sheaf of crackling electric blades bursts out round it; then it breaks into the approved sprint at blinding speed with the bladed hand carried low beside the hip, the blades pointing forward along the floor and spitting sparks, sparks off its feet at every stride, a streak of lightning and four green afterimages trailing behind; in range it plants, dips, and rips the bladed hand up from the hip in an uppercut into the target\'s body, the blades driving up through its torso and punching out of its upper back in a burst of lightning (the target plays lightningImpaled); it holds the blow while the lightning crackles through the target, then rips the hand free and settles back into the guard. The fighter travels 40 px over the clip (the game moves it by that distance).', [
     g(),
     g(an=band(20, -40, fistKind='palm'), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead')] + [
     g(an=LC_RUN, af=SPRINT_F[k], bob=(SPRINT_DY[k],) * 3, lean=(1, 8), root=(6, 0), ln='sr-' + SPRINT_LEGS[k], lf='sr-' + SPRINT_LEGS[(k + 4) % 8]) for k in range(6)] + [
     g(an=LC_RISE, af=TUCK_F, bob=(3, 3, 3), lean=(2, 6), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=LC_CUT, af=TUCK_F, bob=(1, 1, 1), lean=(1, 2), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=LC_CUT, af=TUCK_F, bob=(1, 1, 1), lean=(1, 2), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=LC_CUT, af=TUCK_F, bob=(1, 1, 2), lean=(1, 2), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=LC_CUT, af=TUCK_F, bob=(1, 1, 1), lean=(1, 2), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -150), af=band(-45, 220), bob=(1, 1, 2), lean=(0, 1), ln='ml-trail-rear', lf='ml-plant-lead'),
     g()],
  [None, 'squint'] + ['squint'] * 6 + ['roar', 'roar', 'strain', 'strain', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[42, 20, 16, 12], damage='heavy', rm='E: 6 px a stride through the sprint (as the sprint), +3 and +1 into the thrust; 40 px in all (travel)',
       ghosts={k: (5, 10, 15, 20) for k in range(2, 8)} | {8: (5, 10, 15), 9: (4, 8), 10: (3,)}, ghostColors=(('#ffffff', '#b8ffc8'), ('#b8ffc8', '#ffffff'), ('#39e75f', '#b8ffc8'), ('#39e75f', None)),
       blur={k: 9 for k in range(2, 8)} | {8: 7, 9: 4}, trail=ELEC_TRAIL,
       fx=nfx('lightning (white, pale mint, electric green): sparks spitting off the feet at every stride, a streak of lightning trailing behind',
              [(k, ELEC_FEET[k - 2] + ELEC_WAKE[k % 2]) for k in range(2, 8)] + [(8, ELEC_WAKE[0][:2]), (9, [('spark', [4, 40])])]),
       extra={'airborneFrames': [5], 'travel': {'rule': 'Lightning Cutter is a gap closer (Reach +6 m): the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40},
              'targetState': {'rule': 'Lightning Cutter v3: on the active frame (frame 9, the bladed uppercut drives up into the body) the target plays lightningImpaled once (impaled, blades out of its back, convulsing, then the hand rips free and it staggers), then its idle', 'state': 'lightningImpaled', 'loopFrom': None, 'element': 'air'}},
       anchored={1: [eb('ebHand0'), ('crackle3', 'hand', -3, 0)], **{k: [eb(('ebHand0', 'ebHand1')[k % 2]), ('spark', 'hand', -3, (-5, 5)[k % 2])] for k in range(2, 8)},
                 8: [eb('ebUp'), ('crackle4', 'hand', -2, 0)], 9: [('voltOrb3', 'hand', 0, 0), ('zapRing9', 'hand', 2, -2)],
                 10: [('crackle6', 'hand', 0, 0), ('spark', 'hand', -3, -7)], 11: [('crackle4b', 'hand', 0, 0)], 12: [('crackle6b', 'hand', 0, 0), ('sparkL', 'hand', -2, 6)],
                 13: [eb('ebUpS', {'W': 160, 'l': 150, 'L': 140}), ('spark', 'hand', 6, 2)], 14: [('spark', 'hand', 2, -3)]})),
 'lightningImpaled': ('Lightning Impaled', 0,
  'Lightning Impaled (target state of Lightning Cutter v3, plays once): the bladed uppercut drives up into the fighter\'s body and the electric blades punch up and out through its upper back in a burst of lightning; it doubles over the hand, arms flung out, eyes squeezed, convulsing as lightning crackles through it and arcs off its body; then the hand rips free, the blades vanish, and it staggers back clutching its chest before dropping back into the guard.', [
     g(an=band(20, -30), af=band(10, -25), bob=(1, 0, 0), lean=(2, 8)),
     g(an=band(28, -20), af=band(18, -15), bob=(2, 2, 3), lean=(2, 9), root=(-1, 0)),
     g(an=band(20, -30), af=band(10, -25), bob=(2, 2, 2), lean=(2, 8), root=(1, 0)),
     g(an=band(28, -20), af=band(18, -15), bob=(2, 2, 3), lean=(2, 9), root=(-1, 0)),
     g(an=band(20, -30), af=band(10, -25), bob=(2, 2, 2), lean=(2, 8), root=(1, 0)),
     g(an=band(-60, -100), af=band(-55, -95), bob=(3, 3, 3), lean=(1, 5), root=(-2, 0), **BRACE),
     g(an=band(-60, -100), af=band(-55, -95), bob=(2, 2, 2), lean=(0, 3), **LOW),
     g(root=(2, 0))],
  ['pain', 'pain', 'pain', 'pain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=12, rm='E: 1 px convulsions on frames 1-4 (net 0), -2 staggering back as the hand rips free, +2 back onto the tile',
       anchored={0: [('impaleUp2', 'head', -14, 4), ('voltOrb4', 'head', 3, 15), ('zapRing12', 'head', -6, 15)],
                 1: [('impaleUp', 'head', -13, 5), ('bolt12', 'head', -14, 6), ('crackle6', 'head', 0, 18)],
                 2: [('impaleUp2', 'head', -14, 4), ('boltV2', 'head', 8, 26), ('crackle6b', 'head', -2, 12)],
                 3: [('impaleUp', 'head', -13, 5), ('bolt12b', 'head', -14, 24), ('crackle4', 'head', 4, 6)],
                 4: [('impaleUp2', 'head', -14, 4, {'alpha': {'W': 180, 'l': 170, 'L': 160}}), ('spark', 'head', 8, 8), ('sparkL', 'head', -9, 30)],
                 5: [('crackle4b', 'head', 3, 15), ('spark', 'head', -8, 20)], 6: [('spark', 'head', 6, 14), ('staticV', 'head', -7, 10)]})),
 'empField': ('EMP Field', 5,
  'EMP Field (Aquarius ninjutsu, Elemental 6, Wide AoE, Slow 2 rounds INT save DC 12: the fighter amplifies its inner electrical field with chakra into a dome that repulses enemies and hinders their attacks), v2 (Christopher 2026-10-30: more dramatic; the force field must radiate outward): from the guard the fighter makes the seal and sinks, a crackling green aura rising and arcs leaping off its shoulders; it crosses both forearms before its chest and the charge builds, lightning crawling over its whole body, its eyes blazing white, sparks spitting off the floor; then it throws both arms wide and down with a roar and the field detonates outward: a white flash at its chest, bolts lashing out in every direction, and the dome of crackling electricity blasts out from its body, small, then wider, then full size, with electric shock rings racing outward along the floor; the dome stands round it, crackling, and pulses of force keep radiating outward through it, ring after ring; then it fades as the fighter rises back into the guard (v4, Christopher 2026-11-03: one field only, with the look of the small dome and the radius of the large one: the clip keeps the charge, the flash, the bolts and the floor shock rings, and the testbed draws the dome itself at radius 2).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-60, -165), af=band(-55, -160), bob=(3, 3, 3), lean=(0, 1), **BRACE),
     g(an=band(-60, -165), af=band(-55, -160), bob=(3, 3, 4), lean=(0, 2), root=(1, 0), **BRACE),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(0, -1, -1), lean=(0, -2), root=(-1, 0), **LOW),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(0, -1, -1), lean=(0, -2), **LOW),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(1, 0, 0), lean=(0, -1), **LOW),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1), **LOW),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1), **LOW),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1), **LOW),
     g(an=band(35, 20, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(1, 1, 2), lean=(0, 2)),
     g(), g()],
  [None, 'closed', 'squint', 'strain', 'strain', 'roar', 'roar', 'roar', 'squint', 'squint', 'squint', 'squint', None, None, None],
  [0, 1, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#b8ffc8', '#39e75f'), rm='E: +1 bracing as the charge builds, -1 on the release',
       extra={'zone': {'rule': 'EMP Field (Wide AoE): centred on the caster\'s hex (selfCentered, Claude\'s reading of "a dome of protection"), radius 2 for 2 rounds (Christopher 2026-11-03: the field covers a radius of 2; v4 (2026-11-03: one field, the small dome\'s look at the large one\'s radius): the clip draws no dome; the testbed draws the field as a dome standing on the caster\'s floor line, half-width R = (radius + 0.5) * hexStep * sqrt(3) (the Guardian Barrier sizing) and height 0.92 R, no fill: a jagged 3 px arc (#ffffff / #b8ffc8 / #39e75f, a #14a03c dotted inner shell 6 px in), arcs crawling over the shell, growing out from the caster to R over 0.5 s, then standing with dotted pulse domes running outward from the caster every 0.6 s; preview hex-sprites/astro/aquarius/emp-field-radius2-v4, tool hex-sprites/tools/astro_field.py); v2: on the cast the field radiates outward from the caster across the AoE (rings growing hex by hex, as Explosive Tag fills its hexes ring by ring); while it lasts the testbed draws the crackling dome (edomeD / edomeDim flickering) over the AoE with an eripple pulse running outward every few frames; enemies inside on the cast take Elemental 6, save or are Slowed 2 rounds, and are pushed to the edge (repulse, placeholder 1 hex)', 'pattern': 'edomeD', 'pulse': ['eripple0', 'eripple1', 'eripple2', 'eripple3'], 'radius': 2, 'rounds': 2, 'draw': {'shape': 'dome on the floor line', 'R': '(radius + 0.5) * hexStep * sqrt(3)', 'height': 0.92, 'riseMs': 500, 'fill': None, 'rim': ['#ffffff', '#b8ffc8', '#39e75f'], 'innerShell': ['#14a03c', 6], 'pulseMs': 600}},
              'targetState': {'rule': 'EMP Field: every enemy inside the radius that fails the save plays empSlowed on loop once the field\'s growing edge has reached it, while the Slow lasts', 'state': 'empSlowed', 'loopFrom': 0, 'element': 'air'}},
       anchored={2: [('spark', 'head', -9, 12), ('sparkL', 'head', 9, 18), ('staticV', 'head', -10, 26)],
                 3: [('crackle6', 'hand', 0, 0), ('crackle4', 'head', -10, 18), ('bolt8', 'head', 11, 10), ('spark', 'feet', -10, -2), ('sparkL', 'feet', 10, -3)],
                 4: [('crackle6b', 'hand', 0, 0), ('crackle4b', 'head', 10, 24), ('bolt8b', 'head', -12, 8), ('staticV2', 'head', 0, -9), ('spark', 'feet', 11, -2), ('sparkL', 'feet', -9, -4), ('zapRing6', 'feet', 0, -2)],
                 5: [('voltOrb8', 'head', 2, 16), ('zapRing12', 'feet', 0, -5), ('bolt18', 'head', 13, 6), ('boltV', 'head', -13, 26)],
                 6: [('zapRing16', 'feet', 0, -7), ('bolt18b', 'head', -14, 2), ('bolt18', 'head', 14, 28), ('voltOrb4', 'head', 2, 16)],
                 7: [('zapRing20', 'feet', 0, -9), ('bolt12', 'head', -15, 30)],
                 8: [('zapRing20', 'feet', 0, -9, {'alpha': {'W': 120, 'l': 110, 'L': 100}}), ('spark', 'head', 10, 20)],
                 9: [('sparkL', 'head', -10, 14)], 10: [('spark', 'head', 9, 30)], 11: [('sparkL', 'head', -9, 24)], 12: [('spark', 'head', 8, 12)]})),
 'empSlowed': ('EMP Slowed', 0,
  'EMP Slowed (target state of EMP Field, loops while the Slow 2 rounds lasts): static crawls over the fighter, small arcs jumping between its shoulders, arms and knees; its guard sags and it twitches in fits, a limb jerking, as if its nerves misfire, sparks spitting off it.', [
     g(an=band(-40, -125), af=band(-35, -120), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-30, -110), af=band(-35, -120), bob=(2, 2, 3), lean=(0, 1), root=(1, 0), **LOW),
     g(an=band(-40, -125), af=band(-35, -120), bob=(2, 2, 2), lean=(0, 1), root=(-1, 0), **LOW),
     g(an=band(-40, -125), af=band(-25, -105), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(an=band(-40, -125), af=band(-35, -120), bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=band(-40, -125), af=band(-35, -120), bob=(2, 2, 2), lean=(-1, 0), **LOW)],
  ['squint', 'pain', 'squint', 'pain', 'squint', 'squint'],
  None,
  dict(fps=8, rm='E: a 1 px twitch on frames 1-2 (net 0)', extra={'loop': True, 'loopFrom': 0},
       anchored={0: [('staticV', 'head', -8, 12), ('spark', 'head', 9, 24)], 1: [('crackle4', 'head', 7, 8), ('sparkL', 'head', -9, 30)], 2: [('staticV2', 'head', 9, 18), ('spark', 'head', -7, 38)],
                 3: [('crackle4b', 'hand', 0, 0), ('spark', 'head', 8, 32)], 4: [('staticV', 'head', 8, 10), ('sparkL', 'head', -9, 20)], 5: [('crackle3', 'head', -8, 28), ('spark', 'head', 7, 2)]})),
 'systemCrash': ('System Crash', 5,
  'System Crash (Aquarius genjutsu, debuff: the caster projects a wave of intense psionic energy onto the foe\'s mind, overloading and blinding it; Blind 2 rounds, STR save DC 13; range Zone of Awareness): from the guard the fighter presses two fingers to its temple and its mind spins up: the eyes kindle electric green then flare white-hot, a green-white aura crackles up the outline and loose data blocks flicker round the head, faster each frame; then it thrusts the two fingers out at the target and the overload goes out as waves of torn data, each a ) of 2 px blocks shoved sideways by glitches, white-mint at the core and deep green at the rim, each one wider; the blocks scatter and the hand drops back into the guard (the target plays systemCrashed with the genjutsu mark in Aquarius green).', [
     g(),
     g(an=band(-115, -195, fistKind='point'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(3)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'roar', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#b8ffc8', '#39e75f'), rm='E: +1 thrusting the fingers out, -1 back',
       extra={'targetState': {'rule': 'System Crash: from the active frame the target plays systemCrashed: frames 0-4 once (the overload hits, a bar of corrupted pixels tears across its eyes, it clutches its head), then frames 5-10 on loop until the Blind ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.aquarius) is drawn over it throughout', 'state': 'systemCrashed', 'loopFrom': 5, 'element': 'aquarius', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeG', 'eye', 0, 0), ('spark', 'hand', 0, -3)],
                 2: [('eyeGF', 'eye', 0, 0), ('bits4', 'head', 0, -4), ('staticV', 'hand', 1, -6)],
                 3: [('eyeGF', 'eye', 0, 0), ('bits6', 'head', 0, -3), ('crackle3', 'hand', 0, 0), ('scanS', 'head', -12, 2)],
                 4: [('eyeGF', 'eye', 0, 0), ('bits6b', 'head', -2, -3), ('gw1', 'eye', 5, 0), ('spark', 'hand', 2, 0)],
                 5: [('eyeGF', 'eye', 0, 0), ('bits4b', 'head', -4, -5), ('gw2', 'eye', 9, 0), ('gw1', 'eye', 4, 0)],
                 6: [('eyeGF', 'eye', 0, 0), ('gw3', 'eye', 14, 0), ('gw2', 'eye', 9, 0), ('gw1', 'eye', 4, 0), ('scanL', 'head', -14, 6)],
                 7: [('eyeG', 'eye', 0, 0), ('gw3d', 'eye', 19, 0), ('gw3', 'eye', 14, 0), ('gw2', 'eye', 9, 0)],
                 8: [('gw3d', 'eye', 21, 1, {'alpha': {'L': 130, 'D': 130}}), ('bits4', 'head', -3, -6, {'alpha': {'W': 120, 'l': 120, 'L': 120}})]})),
 'systemCrashed': ('System Crashed', 0,
  'System Crashed (target state of System Crash, Blind 2 rounds): the overload hits and the fighter\'s head snaps back as a bar of corrupted pixels tears across its eyes, rows shoved against each other; it flinches, hands jerking up to the chest, then throws both arms out in front, palms open, feeling for what it can no longer see, while static and loose data blocks spit off it and stray scan lines slice past; then (looping while the Blind lasts) it staggers blind, both arms held out in front, hands groping and searching (v2, Christopher 2026-11-03: no arm over the face, arms out front for the blindness), the bar flickering and re-tearing, data blocks drifting up off the head.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(-2, -5), root=(-1, 0)),
     g(an=band(-45, -125), af=band(-40, -120), bob=(1, 1, 2), lean=(-1, -3)),
     g(an=band(-70, -100, fistKind='palm'), af=band(-60, -110, fistKind='palm'), bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-82, -95, fistKind='palm'), af=band(-75, -100, fistKind='palm'), bob=(2, 2, 3), lean=(1, 2), root=(1, 0), **LOW),
     g(an=band(-85, -92, fistKind='palm'), af=band(-80, -95, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(an=band(-85, -92, fistKind='palm'), af=band(-80, -95, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(an=band(-78, -98, fistKind='palm'), af=band(-88, -90, fistKind='palm'), bob=(2, 2, 3), lean=(1, 3), root=(1, 0), **LOW),
     g(an=band(-72, -104, fistKind='palm'), af=band(-85, -93, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), **LOW),
     g(an=band(-82, -94, fistKind='palm'), af=band(-74, -100, fistKind='palm'), bob=(2, 2, 2), lean=(-1, 1), root=(-1, 0), **LOW),
     g(an=band(-90, -88, fistKind='palm'), af=band(-70, -104, fistKind='palm'), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-85, -92, fistKind='palm'), af=band(-80, -95, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), **LOW)],
  ['pain', 'pain', 'closed', 'pain', 'closed', 'closed', 'pain', 'closed', 'closed', 'pain', 'closed'],
  None,
  dict(fps=8, rm='E: -1 head snapping back, +1 stumbling in (net 0); +1/-1 stagger in the loop (net 0)', extra={'loop': True, 'loopFrom': 5},
       anchored={0: [('gbarC', 'eye', 0, 0), ('bits6', 'head', 0, -2), ('crackle4', 'head', -6, 2)],
                 1: [('gbar', 'eye', 0, 0), ('bits6b', 'head', 0, -4), ('scanL', 'head', 8, 6), ('staticV', 'head', -10, 8)],
                 2: [('gbarB', 'eye', 1, 0), ('bits4', 'head', 2, -6), ('scanS', 'head', -12, 14), ('spark', 'head', 9, 2)],
                 3: [('gbarC', 'eye', -1, 0), ('bits6', 'head', 0, -6), ('scanL', 'head', 10, 18)],
                 4: [('gbar', 'eye', 0, 0), ('bits4b', 'head', 0, -7), ('staticV2', 'head', -9, 10)],
                 5: [('gbar', 'eye', 0, 0), ('bits4', 'head', 1, -8)],
                 6: [('gbarB', 'eye', 1, 0), ('bits4b', 'head', -1, -9), ('scanS', 'head', 10, 10)],
                 7: [('gbarW', 'eye', 0, 0), ('bits4', 'head', 0, -10, {'alpha': {'W': 170, 'l': 170, 'L': 170}})],
                 8: [('gbarC', 'eye', -1, 0), ('bits6b', 'head', 0, -6), ('spark', 'head', -9, 6)],
                 9: [('gbar', 'eye', 0, 0), ('bits4b', 'head', 1, -8), ('scanL', 'head', -12, 16)],
                 10: [('gbarB', 'eye', 0, 0), ('bits4', 'head', 0, -9)]})),
 'lagSwitch': ('Lag Switch', 6,
  'Lag Switch (Aquarius genjutsu, debuff: the caster distorts the foe\'s sense of time and traps it in a time loop; Slow 2 rounds, INT save DC 12; range Zone of Awareness): from the guard the fighter raises its near hand palm out before its face and its eyes kindle electric green; an illusory clock dial forms on the palm, ticks in white, mint and green, and the hand circles once as the dial\'s hand sweeps backward round the face, the dial growing; then it pushes the palm out at the target and the rewind goes out as waves of clock ticks, each a ) with a < rewind chevron at its heart pointing back at the caster, white-mint at the core, deep green at the rim, each one wider; the dial fades and the hand drops back into the guard (the target plays lagSwitched with the genjutsu mark in Aquarius green).', [
     g(),
     g(an=band(-100, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-115, -160, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-95, -135, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-105, -150, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'strain', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#b8ffc8', '#39e75f'), rm='E: +1 pushing the palm out, -1 back',
       extra={'targetState': {'rule': 'Lag Switch: from the active frame the target plays lagSwitched: frames 0-3 once (the rewind hits, it freezes mid-flinch, a loading spinner kindles over its head and a looping arrow runs round its feet), then frames 4-11 on loop until the Slow ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.aquarius) is drawn over it throughout', 'state': 'lagSwitched', 'loopFrom': 4, 'element': 'aquarius', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeG', 'eye', 0, 0), ('dial4_0', 'hand', 3, 0)],
                 2: [('eyeGF', 'eye', 0, 0), ('dial4_10', 'hand', 3, 0), ('spark', 'hand', -2, -6)],
                 3: [('eyeGF', 'eye', 0, 0), ('dial6_8', 'hand', 4, 0), ('bits4', 'head', 0, -5)],
                 4: [('eyeGF', 'eye', 0, 0), ('dial6_5', 'hand', 4, 0), ('scanS', 'head', -12, 4)],
                 5: [('eyeGF', 'eye', 0, 0), ('dial6_2', 'hand', 5, 0), ('rw1', 'eye', 8, 0)],
                 6: [('eyeGF', 'eye', 0, 0), ('dial6_11', 'hand', 5, 0, {'alpha': {'W': 190, 'l': 190, 'L': 160, 'D': 140}}), ('rw2', 'eye', 12, 0), ('rw1', 'eye', 7, 0)],
                 7: [('eyeG', 'eye', 0, 0), ('dialDim', 'hand', 5, 0, {'alpha': {'L': 120, 'D': 100}}), ('rw3', 'eye', 17, 0), ('rw2', 'eye', 12, 0)],
                 8: [('rw3d', 'eye', 20, 1, {'alpha': {'L': 130, 'D': 130}})]})),
 'lagSwitched': ('Lag Switched', 0,
  'Lag Switched (target state of Lag Switch, Slow 2 rounds): the rewind hits and the fighter jerks back, then freezes mid-flinch for a beat as time stalls on it: a loading spinner kindles over its head and a looping arrow starts running round the floor under its feet; its guard drops and the arms fall slack at its sides (v2, Christopher 2026-11-03: no reaching, arms dropped, keep the sway); then (looping while the Slow lasts) it is caught in the time loop: arms hanging, it sways in a step, leaving green lag afterimages behind it, freezes mid-step for two frames while a scan line stutters across it, and is snapped back to where it started, a rewind afterimage left where it had got to; it shakes its head and tries again; the spinner keeps turning and the arrow keeps running round.', [
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-55, -125), af=band(-48, -118), bob=(1, 1, 1), lean=(0, -1), root=(1, 0)),
     g(an=band(-30, -70), af=band(-25, -65), bob=(1, 1, 1), lean=(0, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 2), lean=(1, 3), root=(1, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 2), lean=(1, 4), root=(1, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 2), lean=(1, 4)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 2), lean=(1, 4)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 1), lean=(0, -1), root=(-2, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 1), lean=(0, -2)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 1), lean=(0, 0))],
  ['pain', 'pain', 'squint', 'squint', 'strain', 'strain', 'strain', 'strain', 'pain', 'closed', 'squint', 'squint'],
  None,
  dict(fps=8, rm='E: -1 jerked back, +1 recovering (net 0); loop +1 +1 stepping in, -2 snapped back (net 0)', extra={'loop': True, 'loopFrom': 4},
       ghosts={1: (2,), 4: (3,), 5: (3, 6), 6: (3, 6), 7: (3,), 8: (-3, -6), 9: (-3,)},
       ghostColors=(('#b8ffc8', '#39e75f'), ('#39e75f', None)),
       anchored={0: [('scanL', 'head', 6, 6), ('bits4', 'head', 0, -6), ('loopR0', 'feet', 0, -2)],
                 1: [('buf0', 'head', 0, -12), ('scanS', 'head', -10, 14), ('loopR1', 'feet', 0, -2)],
                 2: [('buf1', 'head', 0, -12), ('loopR2', 'feet', 0, -2)],
                 3: [('buf2', 'head', 0, -12), ('loopR3', 'feet', 0, -2)],
                 4: [('buf3', 'head', 0, -12), ('loopR4', 'feet', 0, -2)],
                 5: [('buf4', 'head', 0, -12), ('loopR5', 'feet', 0, -2)],
                 6: [('buf5', 'head', 0, -12), ('scanL', 'head', 2, 10), ('loopR6', 'feet', 0, -2)],
                 7: [('buf6', 'head', 0, -12), ('scanL', 'head', -2, 22), ('scanS', 'head', 8, 4), ('loopR7', 'feet', 0, -2)],
                 8: [('buf7', 'head', 0, -12), ('rw1', 'head', 8, 10), ('spark', 'head', -7, 4), ('loopR0', 'feet', 0, -2)],
                 9: [('buf0', 'head', 0, -12), ('loopR1', 'feet', 0, -2)],
                 10: [('buf1', 'head', 0, -12), ('loopR2', 'feet', 0, -2)],
                 11: [('buf2', 'head', 0, -12), ('loopR3', 'feet', 0, -2)]})),
 'aeroPalm': ('Aero Palm', 6,
  'Aero Palm (Libra taijutsu strike, Physical 12, Melee with Reach +6 m: the fighter throws a series of palm strikes so fast that they project a column of air that hits the opponent from range): from the guard the fighter draws the near open hand back by the hip, steps in and fires four rapid alternating palm strikes straight out at chest height, near, far, near, far, each one popping a small ring of compressed air off the palm and firing its own small column of air at the target (v2, Christopher 2026-11-03); on the fifth, full extension of the near palm the rings join into a column of air driven straight out (pale silver edges, white core, vortex rings along it); it streams on for a frame and thins away as the arm comes back and the fighter settles into the guard (spec extra.projectile has the testbed fly the air column on to the target).', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), af=band(-90, -90, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -88, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), af=band(-90, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(2, 5), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='palm'), af=band(-40, -120), bob=(1, 1, 1), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-3, 0))],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 1, 1, 2, 2, 1, 0],
  dict(fps=14, auraColors=('#e9eef4', '#a3aebb'), hitbox=[44, 18, 14, 14], damage='light', rm='E: +2 stepping into the strikes, +1 on the last, -3 settling back',
       extra={'projectile': {'rule': 'Aero Palm v2 (Christopher 2026-11-03: a projectile for each strike): every palm fires its own column of air at the target: on frames 2, 3, 4 and 5 the testbed flies NPAT airPuck from the striking palm (near, far, near, far) to the target at chest height, popping aRing3 on each hit; on frame 6 the last, full palm fires airSlug and pops aRing5', 'volley': [{'frame': 2, 'from': 'hand', 'pattern': 'airPuck', 'hit': 'aRing3'}, {'frame': 3, 'from': 'farhand', 'pattern': 'airPuck', 'hit': 'aRing3'}, {'frame': 4, 'from': 'hand', 'pattern': 'airPuck', 'hit': 'aRing3'}, {'frame': 5, 'from': 'farhand', 'pattern': 'airPuck', 'hit': 'aRing3'}, {'frame': 6, 'from': 'hand', 'pattern': 'airSlug', 'hit': 'aRing5'}]}},
       anchored={1: [('puff', 'hand', 0, 0, {'alpha': {'f': 160, 'F': 150, 'q': 140}})],
                 2: [('aRing3', 'hand', 3, 0), ('aStreak2', 'hand', -6, 0), ('airPuckS', 'hand', 9, 0)],
                 3: [('aRing3', 'farhand', 3, 0), ('aStreak2', 'farhand', -6, 0), ('airPuckS', 'farhand', 9, 0), ('aRing5', 'hand', 8, 1, {'alpha': {'F': 130, 'f': 130}})],
                 4: [('aRing3', 'hand', 3, 0), ('aStreak2', 'hand', -6, 0), ('airPuckS', 'hand', 9, 0), ('aRing5', 'farhand', 8, 0, {'alpha': {'F': 130, 'f': 130}})],
                 5: [('aRing3', 'farhand', 3, 0), ('aStreak2', 'farhand', -6, 0), ('airPuckS', 'farhand', 9, 0), ('aRing5', 'hand', 8, 1, {'alpha': {'F': 130, 'f': 130}})],
                 6: [('aRing5', 'hand', 2, 0), ('airCol1', 'hand', 14, 0), ('aStreak', 'hand', -7, 1)],
                 7: [('aRing7', 'hand', 3, 0, {'alpha': {'q': 170, 'F': 170}}), ('airCol2', 'hand', 14, 0)],
                 8: [('airColF', 'hand', 18, 0, {'alpha': {'f': 140, 'q': 120}})]})),
 'flowParry': ('Flow Parry', 8,
  'Flow Parry (Libra taijutsu posture, stance, counter, AGI +20% 1 round: the fighter quiets its mind and attunes to the air currents round it, gaining reaction time and a feeling of weightlessness): from the guard the fighter lets its hands sink, palms down, and closes its eyes; it breathes out and the arms float slowly up, open palms rising to the chest as if lifted by the air, the body light, a pale silver aura round it; air currents curl round it, sweeping in front of the body and behind it in turn, and a few small feathers rise past it; then its eyes snap open and the lead palm sweeps out and across in a soft parry trailing a curl of wind; it settles into a light, low guard.', [
     g(),
     g(an=band(-10, -30, fistKind='palm'), af=band(10, -20, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-25, -45, fistKind='palm'), af=band(-10, -30, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-45, -60, fistKind='palm'), af=band(-25, -45, fistKind='palm'), bob=(0, 0, 1), lean=(0, -1)),
     g(an=band(-60, -75, fistKind='palm'), af=band(-45, -60, fistKind='palm'), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-70, -85, fistKind='palm'), af=band(-60, -75, fistKind='palm'), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-72, -88, fistKind='palm'), af=band(-62, -78, fistKind='palm'), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-70, -85, fistKind='palm'), af=band(-60, -75, fistKind='palm'), bob=(0, 0, 0), lean=(0, -1)),
     g(an=band(-110, -130, fistKind='palm'), af=band(-50, -80, fistKind='palm'), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-55, -40, fistKind='palm'), af=band(-50, -90, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1), root=(1, 0)),
     g(an=band(-60, -110, fistKind='palm'), af=band(-50, -100, fistKind='palm'), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0), **LOW),
     g()],
  [None, 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None, None, None],
  [0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +1 into the parry, -1 back (net 0)',
       trails={'near': range(8, 11), 'far': (), 'len': 2, 'cols': 'Wfq'}, farLayer=True,
       anchored={2: [('curl0', 'head', 0, 22, {'alpha': {'F': 150, 'f': 160}}), ('feather3', 'feet', -10, -6)],
                 3: [('curl1', 'head', 0, 20), ('feather3', 'feet', -11, -11), ('feather', 'feet', 12, -4)],
                 4: [('curl2', 'head', 0, 18, {'behind': True}), ('curlS0', 'head', 0, 4), ('feather2', 'head', -12, 20), ('feather', 'feet', 13, -10)],
                 5: [('curl3', 'head', 0, 18), ('curlS1', 'head', 0, 4, {'behind': True}), ('feather2', 'head', -12, 14), ('feather3', 'feet', 12, -17)],
                 6: [('curl4', 'head', 0, 18, {'behind': True}), ('curlS2', 'head', 0, 4), ('feather', 'head', -12, 8), ('feather3', 'head', 13, 22)],
                 7: [('curl5', 'head', 0, 20), ('curlS3', 'head', 0, 4, {'behind': True}), ('feather', 'head', -13, 2), ('feather2', 'head', 13, 16)],
                 8: [('eyeWF', 'eye', 0, 0), ('aStreak2', 'hand', 2, -2), ('feather2', 'head', 13, 10)],
                 9: [('eyeW', 'eye', 0, 0), ('aRing5', 'hand', 3, 0, {'alpha': {'F': 150, 'f': 160}}), ('feather3', 'head', 14, 4)],
                 10: [('feather3', 'head', 15, -2, {'alpha': {'f': 140, 'F': 130, 'q': 120, 'W': 150}})]})),
 'featherStep': ('Feather Step', 2,
  'Feather Step (Libra taijutsu, teleport, buff, stance, AGI +20% 2 rounds, Move +5 m: the fighter dashes to a new place silently at near-instant speed): from the guard the fighter dips onto the balls of its feet and is gone: two long low strides at blurring speed, the body stretched into a string of pale silver afterimages, no dust, only a thin streak of wind; it lands soft and light 40 px on, a puff of air at its feet, and small white feathers spill out of the wake and drift down round it as it rises into the guard (spec extra.travel: the game moves the fighter by 40 px).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=SPRINT_N[1], af=SPRINT_F[1], bob=(SPRINT_DY[1],) * 3, lean=(1, 8), root=(16, 0), ln='sr-' + SPRINT_LEGS[1], lf='sr-' + SPRINT_LEGS[5]),
     g(an=SPRINT_N[5], af=SPRINT_F[5], bob=(SPRINT_DY[5],) * 3, lean=(1, 8), root=(16, 0), ln='sr-' + SPRINT_LEGS[5], lf='sr-' + SPRINT_LEGS[1]),
     g(an=band(-25, 208), af=band(-45, 220), bob=(3, 3, 3), lean=(1, 4), root=(6, 0), ln='ml-dip-rear', lf='ml-dip-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(2, 2, 2), lean=(1, 3), root=(2, 0)),
     g(an=band(-40, -110), af=band(-45, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', None, None, None],
  None,
  dict(fps=12, rm='E: +16 +16 through the blink strides, +6 +2 landing; 40 px in all (travel)',
       ghosts={2: (4, 8, 12, 16), 3: (4, 8, 12, 16), 4: (4, 8), 5: (3,)}, ghostColors=(('#ffffff', '#e9eef4'), ('#e9eef4', None), ('#a3aebb', None), ('#39e75f', None)),
       extra={'travel': {'rule': 'Feather Step is a teleport dash (Move +5 m): the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}},
       anchored={1: [('puff', 'feet', 0, -2, {'alpha': {'f': 150, 'F': 140, 'q': 120}})],
                 2: [('aStreak', 'head', -14, 14), ('aStreak2', 'feet', -14, -6)],
                 3: [('aStreak', 'head', -14, 18), ('aStreak2', 'feet', -14, -8), ('feather', 'head', -9, 8)],
                 4: [('puff', 'feet', 2, -2), ('feather2', 'head', -9, 2), ('feather3', 'feet', -10, -14)],
                 5: [('feather', 'head', -9, 12), ('feather3', 'head', 12, 4), ('feather2', 'feet', -10, -8)],
                 6: [('feather2', 'head', -9, 18), ('feather', 'head', 12, 12), ('feather3', 'feet', -10, -3)],
                 7: [('feather3', 'head', 12, 20, {'alpha': {'f': 150, 'F': 140, 'q': 120, 'W': 160}}), ('feather', 'feet', -9, -2, {'alpha': {'f': 140, 'F': 130, 'q': 110, 'W': 150}})]})),
 'galeSlicer': ('Gale Slicer', 4,
  'Gale Slicer (Libra ninjutsu, Elemental 16, Ranged, Bleed 2 rounds AGI save DC 12: the caster conjures a blade of compressed wind and hurls it at the opponent): from the guard the fighter makes the seal at the chin; air begins to curl round it; it draws the near knife hand up and back behind its head, the wind gathering and spinning round the hand into a crescent of pressed air; then it whips the knife hand down and across in a chop and the crescent blade (white edge, pale air body, silver back, slate rim) is flung off it and flies on toward the target, the hand finishing low; it settles back into the guard (spec extra.projectile has the testbed fly the blade on to the target and cut on hit).', [
     g(),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(115, 172, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-100, -100, fistKind='palm'), af=band(-30, -80), bob=(1, 1, 2), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-60, -50, fistKind='palm'), af=band(20, -60), bob=(2, 2, 3), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-60, -50, fistKind='palm'), af=band(20, -60), bob=(2, 2, 3), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -90), af=band(-30, -100), bob=(1, 1, 2), lean=(1, 2), root=(-2, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'roar', 'strain', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +2 stepping into the throw, -2 settling back',
       extra={'projectile': {'rule': 'Gale Slicer: from frame 4 the testbed flies NPAT galeBlade from the near hand to the target at chest height (fast, 2-3 frames), then draws galeCut on it', 'from': 'hand', 'frame': 4, 'pattern': 'galeBlade', 'hit': 'galeCut'}},
       anchored={1: [('curlS0', 'head', 0, 10, {'alpha': {'F': 150, 'f': 160, 'W': 170}})],
                 2: [('curlS2', 'hand', 0, 0), ('aStreak2', 'head', -10, 14)],
                 3: [('galeBladeS', 'hand', 0, 0), ('curlS4', 'hand', 0, 0), ('puff', 'hand', -3, 4)],
                 4: [('galeBlade', 'hand', 7, 0), ('aStreak', 'hand', -4, -3)],
                 5: [('aStreak2', 'hand', 3, -2, {'alpha': {'q': 160, 'F': 160, 'f': 160}})]})),
 'pressureBlast': ('Pressure Blast', 4,
  'Pressure Blast (Libra ninjutsu, Elemental 8, AoE in the Zone of Awareness: the caster focuses its chakra on the air in an area and makes it expand so fast it sets off a sonic boom): from the guard the fighter makes the seal at the chin, then pushes the near open hand out at the spot with the fingers curled in, gathering, while air streams in toward the palm; then it snaps the fingers wide open and the trapped air at the spot bursts (the targets play pressureBlasted); the hand drops back into the guard.', [
     g(),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-85, -100), af=band(-60, -120), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-88, -95), af=band(-60, -120), bob=(1, 1, 2), lean=(0, 2)),
     g(an=band(-92, -92, fistKind='palm'), af=band(-60, -120), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     g(an=band(-92, -92, fistKind='palm'), af=band(-60, -120), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'roar', 'squint', None, None],
  [0, 1, 1, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +1 snapping the hand open, -1 back',
       extra={'targetState': {'rule': 'Pressure Blast: from the active frame every fighter in the area plays pressureBlasted once', 'state': 'pressureBlasted'}},
       anchored={1: [('curlS1', 'head', 0, 10, {'alpha': {'F': 150, 'f': 160, 'W': 170}})],
                 2: [('aStreak2', 'hand', 5, -1), ('compress', 'hand', 2, 0)],
                 3: [('aStreak2', 'hand', 6, 2), ('aStreak2', 'hand', 7, -3), ('compress2', 'hand', 2, 0)],
                 4: [('boom4', 'hand', 3, 0), ('puff', 'hand', 1, 0)],
                 5: [('aRing5', 'hand', 4, 0, {'alpha': {'F': 140, 'f': 140}})]})),
 'pressureBlasted': ('Pressure Blasted', 0,
  'Pressure Blasted (target state of Pressure Blast, plays once): the air round the fighter is crushed to a white-hot point at its chest, then bursts in a sonic boom: rings of white and silver blast out from it, each wider, with shock spikes, and the fighter is slammed back a step, head snapping back, arms flung, clothes and hair blown; it rocks back in and recovers into its guard.', [
     g(),
     g(an=band(-50, -140), af=band(-40, -130), bob=(1, 1, 1), lean=(-2, -6), root=(-2, 0)),
     g(an=band(-25, -95), af=band(-15, -90), bob=(2, 2, 2), lean=(-2, -6), root=(-1, 0)),
     g(an=band(-30, -100), af=band(-20, -95), bob=(2, 2, 2), lean=(-1, -4)),
     g(an=band(-45, -115), af=band(-35, -110), bob=(1, 1, 2), lean=(0, -1), root=(2, 0)),
     g(an=band(-55, -120), af=band(-45, -120), bob=(1, 1, 2), lean=(0, 1), root=(1, 0)),
     g()],
  ['squint', 'pain', 'pain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=10, rm='E: -2 -1 slammed back, +2 +1 recovering (net 0)',
       anchored={0: [('compress2', 'head', 1, 16)],
                 1: [('boom4', 'head', 2, 16), ('compress', 'head', 2, 16)],
                 2: [('boom8', 'head', 3, 16), ('boom4', 'head', 3, 16, {'alpha': {'W': 160, 'F': 140, 'f': 140, 'q': 140}})],
                 3: [('boom12', 'head', 3, 16), ('aStreak2', 'head', -12, 2)],
                 4: [('boom15', 'head', 3, 16, {'alpha': {'W': 150, 'F': 130, 'f': 130, 'q': 120}})]})),
 'singularitySphere': ('Singularity Sphere', 6,
  'Singularity Sphere (Libra ninjutsu, Elemental 12, Wide AoE, Root 1 round STR save DC 12: the caster focuses its chakra on the air in an area and makes it collapse in on itself into a crushing vacuum): from the guard the fighter makes the seal at the chin, then holds both open palms out facing each other a hand apart; a speck of black vacuum forms between them and air streams in to it; it presses the palms slowly together, straining, the speck darkening, the air spiralling in; then it crushes the hands shut into a fist and drives it forward at the area (the targets play singularityCaught as the sphere collapses on them); it holds, trembling, and drops back into the guard.', [
     g(),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-75, -110, fistKind='palm'), af=band(-95, -70, fistKind='palm'), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-78, -105, fistKind='palm'), af=band(-92, -78, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-80, -100, fistKind='palm'), af=band(-90, -84, fistKind='palm'), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-82, -96, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-92, -92), af=band(-60, -120), bob=(2, 2, 2), lean=(1, 4), root=(1, 0), **LOW),
     g(an=band(-92, -92), af=band(-60, -120), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-92, -92), af=band(-60, -120), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'roar', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#a3aebb', '#3a4250'), rm='E: +1 driving the fist out, -1 back',
       extra={'targetState': {'rule': 'Singularity Sphere: from the active frame every fighter in the area plays singularityCaught: frames 0-3 once (the vacuum swells and swallows it), then frames 4-9 on loop while the Root lasts, then singularityRelease once', 'state': 'singularityCaught', 'loopFrom': 4, 'release': 'singularityRelease'}},
       anchored={2: [('vacSeed', 'hand', -3, 2), ('aStreak2', 'hand', 2, -5)],
                 3: [('vacB3', 'hand', -2, 2), ('vacF3_0', 'hand', -2, 2)],
                 4: [('vacB3', 'hand', -2, 1), ('vacF3_1', 'hand', -2, 1)],
                 5: [('vacB3', 'hand', -1, 1), ('vacF3_2', 'hand', -1, 1)],
                 6: [('vacSeed', 'hand', 3, 0), ('aRing5', 'hand', 3, 0, {'alpha': {'F': 150, 'f': 150}})],
                 7: [('aStreak2', 'hand', -6, -3), ('aStreak2', 'hand', -6, 3)]})),
 'singularityCaught': ('Singularity Caught', 0,
  'Singularity Caught (target state of Singularity Sphere, Root 1 round): a speck of black vacuum opens at the fighter\'s chest and swells into a sphere round it (near-black heart, slate shell behind the fighter, a white event rim and four arms of air spiralling in over it); the fighter, seen through the dark of it, is dragged in on itself, hunched, arms clamped to its body, knees buckling, feet locked; then (looping while the Root lasts) it strains against the crush, trembling, the spiral arms turning, the rim flickering.', [
     g(an=band(-50, -130), af=band(-40, -125), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(-30, -110), af=band(-25, -110), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-15, -120), af=band(-10, -120), bob=(3, 3, 3), lean=(1, 4), **LOW),
     g(an=band(-10, -125), af=band(-5, -125), bob=(3, 3, 4), lean=(1, 5), **LOW),
     g(an=band(-10, -125), af=band(-5, -125), bob=(3, 3, 4), lean=(1, 5), root=(1, 0), **LOW),
     g(an=band(-12, -122), af=band(-6, -124), bob=(3, 3, 4), lean=(1, 4), root=(-1, 0), **LOW),
     g(an=band(-10, -125), af=band(-5, -125), bob=(3, 3, 4), lean=(1, 5), **LOW),
     g(an=band(-10, -125), af=band(-5, -125), bob=(3, 3, 4), lean=(1, 5), root=(1, 0), **LOW),
     g(an=band(-12, -122), af=band(-6, -124), bob=(3, 3, 4), lean=(1, 4), root=(-1, 0), **LOW),
     g(an=band(-10, -125), af=band(-5, -125), bob=(3, 3, 4), lean=(1, 5), **LOW)],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'closed', 'pain', 'pain', 'closed', 'pain'],
  None,
  dict(fps=8, rm='E: trembling 1 px in the loop (net 0)', extra={'loop': True, 'loopFrom': 4},
       anchored={0: [('vacB3', 'head', -4, 18, {'behind': True}), ('vacF3_0', 'head', -4, 18)],
                 1: [('vacB10', 'head', -4, 20, {'behind': True}), ('vacB10', 'head', -4, 20, {'alpha': {'k': 70, 'o': 100}, 'onFig': True}), ('vacF10_1', 'head', -4, 20)],
                 2: [('vacB13', 'head', -4, 21, {'behind': True}), ('vacB13', 'head', -4, 21, {'alpha': {'k': 80, 'o': 110}, 'onFig': True}), ('vacF13_2', 'head', -4, 21)],
                 **{k_: [('vacB13', 'head', -4, 22, {'behind': True}), ('vacB13', 'head', -4, 22, {'alpha': {'k': 80 + 10 * (k_ % 2), 'o': 110}, 'onFig': True}), ('vacF13_%d' % (k_ % 4), 'head', 1, 22)] for k_ in range(3, 10)}})),
 'singularityRelease': ('Singularity Release', 0,
  'Singularity Release (target state, plays once when the Root of Singularity Sphere ends): the vacuum sphere shrinks back to a speck and pops in a puff of air, the fighter stumbles up out of its crouch gasping and back into the guard.', [
     g(an=band(-10, -125), af=band(-5, -125), bob=(3, 3, 4), lean=(1, 5), **LOW),
     g(an=band(-30, -110), af=band(-25, -110), bob=(2, 2, 3), lean=(1, 3), **LOW),
     g(an=band(-45, -115), af=band(-35, -115), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-50, -120), af=band(-40, -120), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  ['pain', 'squint', 'squint', 'squint', None],
  None,
  dict(fps=8, anchored={0: [('vacB6', 'head', -4, 20, {'behind': True}), ('vacF6_0', 'head', -4, 20)],
                        1: [('vacSeed', 'head', 1, 18), ('aRing5', 'head', 1, 18)],
                        2: [('puff', 'head', 2, 16), ('aRing7', 'head', 1, 18, {'alpha': {'q': 140, 'F': 140}})]})),
 'indecision': ('Indecision', 5,
  'Indecision (Libra genjutsu, debuff: the caster projects its own thoughts on to the opponent so it second-guesses which thoughts are its own; Silence 1 round, INT save DC 12; range Zone of Awareness): from the guard the fighter lifts the near hand palm up before its chest and its eyes kindle silver-white; an illusory balance scale, the Libra scales, forms over the palm and tips one way, then the other, then back, weighing; then the fighter pushes the open palm out at the target and the weighing goes out as pale waves of wind-white thought, each one wider; the scale fades and the hand drops back into the guard (the target plays indecisive with the genjutsu mark in air colours).', [
     g(),
     g(an=band(-60, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-65, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-65, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-65, -150, fistKind='palm'), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +1 pushing the palm out, -1 back',
       extra={'targetState': {'rule': 'Indecision: from the active frame the target plays indecisive: frames 0-2 once, then frames 3-10 on loop until the Silence ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.air) is drawn over it throughout', 'state': 'indecisive', 'loopFrom': 3, 'element': 'air', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeW', 'eye', 0, 0), ('scale+0', 'hand', 0, -8, {'alpha': {'W': 170, 'f': 160, 'F': 150, 'q': 140}})],
                 2: [('eyeWF', 'eye', 0, 0), ('scale+2', 'hand', 0, -8)],
                 3: [('eyeWF', 'eye', 0, 0), ('scale-2', 'hand', 0, -8)],
                 4: [('eyeWF', 'eye', 0, 0), ('scale+1', 'hand', 0, -8), ('iw1', 'eye', 5, 0)],
                 5: [('eyeWF', 'eye', 0, 0), ('iw2', 'eye', 9, 0), ('iw1', 'eye', 4, 0), ('scale+0', 'head', -4, -12, {'alpha': {'W': 150, 'f': 140, 'F': 130, 'q': 120}})],
                 6: [('eyeWF', 'eye', 0, 0), ('iw3', 'eye', 14, 0), ('iw2', 'eye', 9, 0), ('iw1', 'eye', 4, 0)],
                 7: [('eyeW', 'eye', 0, 0), ('iw3d', 'eye', 19, 0), ('iw3', 'eye', 14, 0), ('iw2', 'eye', 9, 0)],
                 8: [('iw3d', 'eye', 21, 1, {'alpha': {'F': 130, 'q': 130}})]})),
 'indecisive': ('Indecisive', 0,
  'Indecisive (target state of Indecision, Silence 1 round): the thought-waves hit and the fighter blinks, an illusory balance scale appearing over its head; its hands sag, unsure; then (looping while the Silence lasts) it is torn two ways: it leans in to act, the near hand reaching, while a pale afterimage of itself hangs back; then it sways back, the hand drawn in, while the afterimage leans on ahead; again with the far hand; the scale over its head tips with every change of mind.', [
     g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-40, -110), af=band(-30, -105), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-35, -100), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-80, -100, fistKind='palm'), af=band(-35, -105), bob=(1, 1, 2), lean=(1, 4)),
     g(an=band(-80, -100, fistKind='palm'), af=band(-35, -105), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-30, -95), af=band(-30, -100), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-30, -95), af=band(-30, -100), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-35, -100), af=band(-80, -95, fistKind='palm'), bob=(1, 1, 2), lean=(1, 4)),
     g(an=band(-35, -100), af=band(-80, -95, fistKind='palm'), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-30, -95), af=band(-30, -100), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-35, -100), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 0))],
  ['squint', 'closed', 'squint', 'squint', 'squint', 'pain', 'squint', 'squint', 'squint', 'pain', 'squint'],
  None,
  dict(fps=8, rm='E: sways in place (net 0)', extra={'loop': True, 'loopFrom': 3},
       ghosts={3: (3,), 4: (4,), 5: (-3,), 6: (-4,), 7: (3,), 8: (4,), 9: (-3,), 10: (-2,)}, ghostColors=(('#e9eef4', None),),
       anchored={0: [('iw2', 'eye', -4, 0, {'alpha': {'W': 160, 'f': 150}}), ('scale+0', 'head', -13, -2, {'alpha': {'W': 150, 'f': 140, 'F': 130, 'q': 120}})],
                 1: [('scale+1', 'head', -13, -2)], 2: [('scale-1', 'head', -13, -2)],
                 3: [('scale+2', 'head', -13, -2)], 4: [('scale+2', 'head', -13, -2)], 5: [('scale-2', 'head', -13, -2)], 6: [('scale-2', 'head', -13, -2)],
                 7: [('scale+2', 'head', -13, -2)], 8: [('scale+1', 'head', -13, -2)], 9: [('scale-2', 'head', -13, -2)], 10: [('scale+0', 'head', -13, -2)]})),
 'vertigo': ('Vertigo', 6,
  'Vertigo (Libra genjutsu, debuff: the caster induces vertigo in the opponent so it loses its sense of direction; Blind 2 rounds, STR save DC 13; range Zone of Awareness): from the guard the fighter raises the near index finger beside its face and its eyes kindle silver-white; it traces small circles in the air with the fingertip and a spiral of wind-white dots winds up round it, growing and turning; then it points the finger at the target and the spiral is flung out after it, turning as it goes, as widening rings; the finger drops back into the guard (the target plays vertigoSpun with the genjutsu mark in air colours).', [
     g(),
     g(an=band(-110, -150, fistKind='point'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-100, -138, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-118, -160, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-108, -172, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-96, -146, fistKind='point'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +1 pointing, -1 back',
       extra={'targetState': {'rule': 'Vertigo: from the active frame the target plays vertigoSpun: frames 0-2 once, then frames 3-10 on loop until the Blind ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.air) is drawn over it throughout', 'state': 'vertigoSpun', 'loopFrom': 3, 'element': 'air', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeW', 'eye', 0, 0), ('spiral3_0', 'hand', 0, -2)],
                 2: [('eyeWF', 'eye', 0, 0), ('spiral3_1', 'hand', 0, -2)],
                 3: [('eyeWF', 'eye', 0, 0), ('spiral5_2', 'hand', 0, -2)],
                 4: [('eyeWF', 'eye', 0, 0), ('spiral5_3', 'hand', 0, -2)],
                 5: [('eyeWF', 'eye', 0, 0), ('spiral7_4', 'hand', 1, -2)],
                 6: [('eyeWF', 'eye', 0, 0), ('spiral5_5', 'hand', 5, 0), ('iw1', 'hand', 2, 0)],
                 7: [('eyeW', 'eye', 0, 0), ('spiral3_0', 'hand', 8, 0, {'alpha': {'q': 150, 'F': 160}}), ('iw2', 'hand', 3, 0)],
                 8: [('iw3d', 'hand', 5, 0, {'alpha': {'F': 130, 'q': 130}})]})),
 'vertigoSpun': ('Vertigo Spun', 0,
  'Vertigo Spun (target state of Vertigo, Blind 2 rounds): the spiral hits and the fighter\'s head lolls, a spiral of wind-white dots turning over its head and motes reeling round it; its knees go and it throws its arms out for balance, near hand forward and far hand back, eyes squeezed shut; then (looping while the Blind lasts) it reels in a slow circle on the spot, swaying forward, across and back, stumbling a step one way and the other, the spiral turning and the motes reeling over it.', [
     g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-40, -60, fistKind='palm'), af=band(30, 15, fistKind='palm'), bob=(2, 2, 2), lean=(0, -1), **LOW),
     g(an=band(-55, -55, fistKind='palm'), af=band(40, 30, fistKind='palm'), bob=(2, 2, 3), lean=(0, 1), **LOW),
     g(an=band(-55, -55, fistKind='palm'), af=band(40, 30, fistKind='palm'), bob=(2, 2, 3), lean=(1, 5), root=(1, 0), **LOW),
     g(an=band(-45, -50, fistKind='palm'), af=band(35, 25, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-35, -45, fistKind='palm'), af=band(45, 35, fistKind='palm'), bob=(2, 2, 3), lean=(0, 0), root=(-1, 0), **LOW),
     g(an=band(-30, -40, fistKind='palm'), af=band(50, 40, fistKind='palm'), bob=(2, 2, 2), lean=(-1, -4), root=(-1, 0), **LOW),
     g(an=band(-40, -45, fistKind='palm'), af=band(45, 35, fistKind='palm'), bob=(2, 2, 3), lean=(-1, -3), **LOW),
     g(an=band(-50, -55, fistKind='palm'), af=band(40, 30, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), root=(1, 0), **LOW),
     g(an=band(-55, -60, fistKind='palm'), af=band(35, 25, fistKind='palm'), bob=(2, 2, 3), lean=(0, 2), **LOW),
     g(an=band(-55, -55, fistKind='palm'), af=band(40, 30, fistKind='palm'), bob=(2, 2, 3), lean=(0, 1), **LOW)],
  ['pain', 'closed', 'closed', 'pain', 'closed', 'closed', 'pain', 'closed', 'closed', 'pain', 'closed'],
  None,
  dict(fps=8, rm='E: reeling +1, -1, -1, +1 in the loop (net 0)', extra={'loop': True, 'loopFrom': 3},
       anchored={0: [('spiral3_0', 'head', 0, -9), ('iw2', 'eye', -4, 0, {'alpha': {'W': 160, 'f': 150}})],
                 **{k_: [('spiral5_%d' % (k_ % 6), 'head', 0, -9), ('motesW%d' % (k_ % 6), 'head', 0, -4)] for k_ in range(1, 11)}})),
 'machDash': ('Mach Dash', 2,
  'Mach Dash (Gemini taijutsu, teleport, buff, stance, Movement +15, AGI +10% 1 round: the fighter dashes fast enough to break the sound barrier): from the guard the fighter dips into the sprinter set, then breaks into the approved sprint so fast it blurs: a sonic boom ring bursts behind it on the first stride and a white vapour cone wraps the front of its body, pale afterimages streaming behind; it plants the lead foot and brakes, skidding, a last ring of sound puffing off it, and rises into the guard (spec extra.travel: the game moves the fighter by 40 px).', [
     g(),
     g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead')] + [
     g(an=SPRINT_N[k], af=SPRINT_F[k], bob=(SPRINT_DY[k],) * 3, lean=(1, 8), root=(6, 0), ln='sr-' + SPRINT_LEGS[k], lf='sr-' + SPRINT_LEGS[(k + 4) % 8]) for k in range(6)] + [
     g(an=band(-25, 208), af=band(-45, 220), bob=(2, 2, 2), lean=(-1, -3), root=(3, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-25, 208), af=band(-45, 220), bob=(2, 2, 2), lean=(0, -1), root=(1, 0), ln='ml-trail-rear', lf='ml-plant-lead'),
     g(an=band(-40, -110), af=band(-45, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint'] + ['squint'] * 6 + ['strain', 'squint', None, None],
  None,
  dict(fps=12, rm='E: 6 px a stride through the sprint, +3 +1 braking; 40 px in all (travel)',
       ghosts={k: (5, 10, 15, 20) for k in range(2, 8)} | {8: (5, 10), 9: (3,)}, ghostColors=(('#ffffff', '#e9eef4'), ('#e9eef4', None), ('#a3aebb', None), ('#39e75f', None)),
       extra={'travel': {'rule': 'Mach Dash is a teleport dash (Movement +15): the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}},
       anchored={1: [('puff', 'feet', -4, -2)],
                 2: [('boom8', 'head', -14, 18), ('vcone2', 'head', 6, 18)],
                 3: [('boom12', 'head', -18, 18, {'alpha': {'W': 160, 'F': 140, 'f': 140, 'q': 130}}), ('vcone', 'head', 7, 18)],
                 **{k_: [('vcone', 'head', 7, 18), ('aStreak', 'head', -12, 8 + 4 * (k_ % 2))] for k_ in (4, 5, 6, 7)},
                 8: [('floorStreakL', 'feet', -10, -2), ('boom4', 'head', 4, 18)],
                 9: [('puff', 'feet', 4, -2), ('aRing5', 'head', 3, 18, {'alpha': {'F': 140, 'f': 140}})]})),
 'echoFist': ('Echo Fist', 3,
  'Echo Fist (Gemini taijutsu strike, Physical 14: the fighter throws a punch that reverberates through the opponent\'s body; v2, Christopher 2026-11-03: develop the fx): from the guard the fighter sets the rear fist back by the ear, rings of sound humming and tightening round it, then steps in with a straight cross; on contact a white sonic boom bursts off the fist with a sharp crack; then the punch echoes: twice more a ring pulses out from the knuckles, each echo sending a shockwave arc rolling on through the target, wider each time; the fighter holds the fist in as the echoes ring out, then draws back into the guard (the target plays echoReverb: it jolts with each echo as the shockwave bursts out of its back).', [
     g(),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(40, -170), af=band(-70, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=PUNCH, af=band(30, -160), bob=(2, 2, 2), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(root=(-2, 0))],
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='medium', rm='E: +2 on the step into the punch, -2 settling back',
       extra={'targetState': {'rule': 'Echo Fist v2: on the hit the target plays echoReverb once (three jolts, one per echo, shockwave arcs bursting out of its back), then its idle', 'state': 'echoReverb'}},
       anchored={1: [('aRing3', 'hand', 0, 0, {'alpha': {'f': 150, 'W': 160}}), ('aRing5', 'hand', 0, 0, {'alpha': {'F': 110, 'f': 110, 'q': 100}})],
                 2: [('aRing3', 'hand', 0, 0), ('compress', 'hand', 1, 0), ('aStreak2', 'hand', 3, -3)],
                 3: [('boom4', 'hand', 3, 0), ('compress2', 'hand', 2, 0), ('crackV', 'hand', 5, -3)],
                 4: [('boom8', 'hand', 2, 0), ('hw1', 'hand', 6, 0), ('aRing3', 'hand', 2, 0)],
                 5: [('boom8', 'hand', 2, 0, {'alpha': {'W': 200, 'F': 170, 'f': 170, 'q': 160}}), ('aRing5', 'hand', 2, 0), ('hw2', 'hand', 9, 0)],
                 6: [('boom12', 'hand', 2, 0, {'alpha': {'W': 170, 'F': 150, 'f': 150, 'q': 140}}), ('aRing3', 'hand', 2, 0), ('hw3', 'hand', 13, 0)],
                 7: [('aRing5', 'hand', 4, 0, {'alpha': {'F': 110, 'f': 110, 'q': 100}}), ('hw3', 'hand', 16, 0, {'alpha': {'W': 120, 'F': 100, 'f': 100, 'q': 90}})]})),
 'echoReverb': ('Echo Reverb', 0,
  'Echo Reverb (target state of Echo Fist, v2): the cross lands in its chest and a sonic boom bursts there; the fighter jolts back, then the echoes hit: twice more it jerks as if struck again, each time a ring pulses at its chest and a shockwave arc bursts out of its back, wider each time; it staggers a step and recovers its guard.', [
     g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(-2, -5), root=(-1, 0)),
     g(an=band(-50, -120), af=band(-45, -115), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-60, -130), af=band(-50, -125), bob=(1, 1, 2), lean=(-2, -6), root=(-1, 0)),
     g(an=band(-50, -120), af=band(-45, -115), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-60, -135), af=band(-50, -130), bob=(2, 2, 2), lean=(-2, -7), root=(-1, 0)),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(-1, -3)),
     g(an=band(-45, -115), af=band(-40, -110), bob=(1, 1, 1), lean=(0, -1), root=(1, 0)),
     g(an=band(-45, -115), af=band(-40, -110), bob=(1, 1, 1), lean=(0, 0), root=(1, 0)),
     g(root=(1, 0))],
  ['pain', 'pain', 'pain', 'squint', 'pain', 'squint', 'squint', None, None],
  None,
  dict(fps=10, rm='E: -1 -1 -1 jolted back by each echo, +1 +1 +1 recovering (net 0)',
       anchored={0: [('boom8', 'head', 6, 14), ('compress2', 'head', 5, 14)],
                 1: [('aRing3', 'head', 5, 14, {'alpha': {'f': 150, 'W': 160}}), ('hwB1', 'head', -9, 14)],
                 2: [('boom8', 'head', 5, 14, {'alpha': {'W': 200, 'F': 170, 'f': 170, 'q': 160}}), ('hwB2', 'head', -11, 14)],
                 3: [('aRing3', 'head', 5, 14), ('hwB2', 'head', -15, 14, {'alpha': {'W': 150, 'F': 130, 'f': 130, 'q': 120}})],
                 4: [('boom12', 'head', 5, 14, {'alpha': {'W': 170, 'F': 150, 'f': 150, 'q': 140}}), ('hwB3', 'head', -13, 14)],
                 5: [('hwB3', 'head', -18, 14, {'alpha': {'W': 140, 'F': 120, 'f': 120, 'q': 110}}), ('aRing3', 'head', 5, 14, {'alpha': {'f': 110, 'W': 120}})],
                 6: [('puff', 'feet', -4, -2, {'alpha': {'f': 140, 'F': 130, 'q': 120, 'W': 150}})]})),
 'sonicSweep': ('Sonic Sweep', 5,
  'Sonic Sweep (Gemini taijutsu, Physical 10, Prone 1 round AGI save DC 12: the fighter sweeps its leg fast enough to break the sound barrier and knocks the opponent prone; v2, Christopher 2026-11-03: develop the animation): from the guard the fighter steps in and drops hard, planting the near hand on the floor beside the lead foot, and loads the rear leg out long behind it along the ground, coiling; then it whips the leg round under itself: the foot skims the floor, swings under the body, and cracks out flat in front at ankle height, breaking the sound barrier: a flattened sonic boom bursts off the foot with a sharp crack and a cone of vapour, the leg\'s path traced on the floor behind it as a white swoosh with a green tail, dust kicked up; the leg follows through past the target\'s ankles, the body leaning into it, then it snaps the leg back under, pushes off the planted hand and rises into the guard (the target plays sonicSwept: its feet are knocked out from under it and it drops flat on its back, then lies prone for the round and gets up).', [
     g(),
     g(an=band(-30, -60), af=band(-20, -120), bob=(2, 3, 3), lean=(1, 4), root=(2, 0), **BRACE),
     g(an=band(-20, -25, fistKind='palm'), af=band(-30, -140), bob=(9, 10, 10), lean=(1, 7), ln='gs-wide-rear', lf='gs-crouch-lead'),
     g(an=band(-20, -25, fistKind='palm'), af=band(-30, -140), bob=(10, 11, 11), lean=(1, 7), ln='gs-wide-rear', lf='gs-crouch-lead'),
     g(an=band(-15, -20, fistKind='palm'), af=band(-40, -120), bob=(9, 10, 10), lean=(1, 5), ln='gs-mid-rear', lf='gs-crouch-lead'),
     g(an=band(10, -10, fistKind='palm'), af=band(-70, -110), bob=(9, 10, 10), lean=(0, 2), root=(1, 0), ln='gs-front-rear', lf='gs-crouch-lead'),
     g(an=band(10, -10, fistKind='palm'), af=band(-80, -100), bob=(9, 10, 10), lean=(-1, 0), root=(1, 0), ln='gs-far-rear', lf='gs-crouch-lead'),
     g(an=band(10, -10, fistKind='palm'), af=band(-80, -100), bob=(9, 10, 10), lean=(-1, 0), ln='gs-far-rear', lf='gs-crouch-lead'),
     g(an=band(-15, -20, fistKind='palm'), af=band(-40, -120), bob=(9, 10, 10), lean=(1, 5), ln='gs-mid-rear', lf='gs-crouch-lead'),
     g(an=band(-55, -130), af=band(-20, -100), bob=(4, 5, 5), lean=(1, 3), root=(-2, 0), **LOW),
     g(an=band(-50, -120), af=band(-30, -110), bob=(1, 2, 2), lean=(0, 1), root=(-2, 0)),
     g()],
  [None, 'squint', 'strain', 'strain', 'strain', 'roar', 'roar', 'strain', 'squint', None, None, None],
  None,
  dict(fps=14, hitbox=[42, 52, 18, 10], damage='light', rm='E: +2 stepping in, +1 +1 into the sweep, -2 -2 rising back (net 0)',
       extra={'targetState': {'rule': 'Sonic Sweep v2: on a hit the target plays sonicSwept once (feet knocked out, drops flat on its back), then prone for the Prone round, then getUp', 'state': 'sonicSwept', 'then': ['prone', 'getUp']}},
       anchored={2: [('puff', 'hand', 0, 2), ('floorStreakL', 'feet', -14, -2, {'alpha': {'f': 150, 'F': 140, 'q': 130, 'W': 160}})],
                 3: [('floorStreakL', 'feet', -12, -2)],
                 4: [('floorStreak', 'feet', -4, -2), ('sweepArc0', 'feet', -2, -5, {'behind': True}), ('puff', 'feet', -6, -3)],
                 5: [('crackV', 'feet', 20, -4), ('boomFlat', 'feet', 18, -3), ('sweepArc0', 'feet', 4, -5), ('vcone2', 'feet', 14, -6), ('puff', 'feet', 8, -3)],
                 6: [('boom12', 'feet', 20, -6, {'alpha': {'W': 200, 'F': 170, 'f': 170, 'q': 160}}), ('sweepArc1', 'feet', 6, -5), ('vcone', 'feet', 18, -8), ('puff', 'feet', 14, -4), ('puff', 'feet', 2, -2)],
                 7: [('boom15', 'feet', 20, -8, {'alpha': {'W': 140, 'F': 120, 'f': 120, 'q': 110}}), ('sweepArc2', 'feet', 6, -5), ('puff', 'feet', 18, -6, {'alpha': {'f': 150, 'F': 140, 'q': 130, 'W': 160}})],
                 8: [('puff', 'feet', 14, -8, {'alpha': {'f': 110, 'F': 100, 'q': 90, 'W': 120}})]})),
 'sonicSwept': ('Sonic Swept', 0,
  'Sonic Swept (target state of Sonic Sweep, v2, Christopher 2026-11-03): the sweep cracks into its ankles: both feet are knocked out forward from under it, arms flung up, body tipping back; for a beat it hangs in the air, laid out flat, then drops onto its back on the floor with a thud and a puff of dust and a ring of sound, bouncing once, and lies there (the testbed then plays prone for the Prone round and getUp).', [
     g(an=band(-100, -170), af=band(-110, -175), bob=(0, 0, 0), lean=(-2, -6), ln='sw-up-rear', lf='sw-up-lead'),
     g(an=band(-130, -190), af=band(-140, -195), bob=(0, 0, 0), lean=(-2, -8), ln='sw-hi-rear', lf='sw-hi-lead'),
     g(an=band(-150, -200), af=band(-150, -200), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-150, -200), af=band(-150, -200), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-150, -200), af=band(-150, -200), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-150, -200), af=band(-150, -200), bob=(0, 0, 0), lean=(0, 0))],
  ['pain', 'pain', 'pain', 'closed', 'closed', 'closed'],
  None,
  dict(fps=10, rm='E: no travel (it drops where it stood)', invert={2: (1, 90), 3: (1, 90), 4: (1, 90), 5: (1, 90)},
       anchored={0: [('boomFlat', 'feet', 6, -3), ('puff', 'feet', 4, -2)], 1: [('puff', 'feet', 2, -3, {'alpha': {'f': 150, 'F': 140, 'q': 130, 'W': 160}})],
                 3: [('boomFlat', 'feet', 0, -2), ('puff', 'feet', -10, -3), ('puff', 'feet', 10, -3)], 4: [('puff', 'feet', -12, -5, {'alpha': {'f': 130, 'F': 120, 'q': 110, 'W': 140}}), ('puff', 'feet', 12, -5, {'alpha': {'f': 130, 'F': 120, 'q': 110, 'W': 140}})]})),
 'howlingBlast': ('Howling Blast', 3,
  'Howling Blast (Gemini ninjutsu, Elemental 8, 6 m AoE centred on the caster, Silence 1 round INT save DC 12: the caster channels chakra into its throat and releases a deafening howl): from the guard the fighter draws a huge breath, chest lifting, head back, a white glow gathering at the throat; then it lunges forward on braced legs, hands flung back, and howls (v2, Christopher 2026-11-03: the shockwaves emit outward from the mouth toward the target): sound shockwaves, \')\' arcs with a white leading edge, silver body, green rim and shock spikes, roll out of its mouth one after another toward the target, each one wider as it travels; the testbed flies them on to every target in the area; the howl dies away and it settles back into the guard.', [
     g(),
     g(an=band(10, -40), af=band(5, -40), bob=(0, -1, 0), lean=(-1, -3)),
     g(an=band(10, -40), af=band(5, -40), bob=(0, -1, 0), lean=(-1, -4)),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), root=(1, 0), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(35, 15, fistKind='palm'), af=band(30, 10, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), **BRACE),
     g(an=band(-30, -100), af=band(-30, -105), bob=(1, 1, 2), lean=(0, 2)),
     g(root=(-1, 0))],
  [None, 'squint', 'squint', 'roarE', 'roarE', 'roarE', 'roarE', None, None],
  [0, 0, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +1 lunging into the howl, -1 back',
       shapes={'roarE': {'E': [[0, 0, '#000000'], [1, 0, '#000000'], [1, 4, '#000000'], [2, 4, '#000000'], [1, 5, '#70241d'], [2, 5, '#70241d']]}},
       extra={'zone': {'rule': 'Howling Blast is a 6 m AoE centred on the caster; everyone in it is Silenced 1 round', 'shape': 'radius', 'centre': 'caster'},
              'projectile': {'rule': 'Howling Blast v2 (Christopher 2026-11-03: shockwaves emit outward from the mouth toward the target): from frames 4, 5 and 6 the testbed flies NPAT hw3 from the mouth (eye anchor, 3 px down) to each target in the area at head height over 3 frames, turned to face the target, popping boom8 on each arrival', 'volley': [{'frame': 4, 'from': 'mouth', 'pattern': 'hw3', 'hit': 'boom8'}, {'frame': 5, 'from': 'mouth', 'pattern': 'hw3', 'hit': 'boom8'}, {'frame': 6, 'from': 'mouth', 'pattern': 'hw3', 'hit': 'boom8'}]}},
       anchored={1: [('compress', 'eye', -3, 8)], 2: [('compress2', 'eye', -3, 8)],
                 3: [('hw1', 'eye', 5, 3), ('compress2', 'eye', 2, 5)],
                 4: [('hw2', 'eye', 9, 3), ('hw1', 'eye', 5, 3)],
                 5: [('hw3', 'eye', 14, 3), ('hw2', 'eye', 9, 3), ('hw1', 'eye', 5, 3)],
                 6: [('hw4', 'eye', 20, 3), ('hw3', 'eye', 14, 3), ('hw2', 'eye', 9, 3)],
                 7: [('hw4d', 'eye', 24, 3, {'alpha': {'W': 150, 'F': 130, 'f': 130, 'q': 120}}), ('hw3', 'eye', 15, 3, {'alpha': {'W': 120, 'F': 100, 'f': 100, 'q': 90}})]})),
 'mirageClone': ('Mirage Clone', 3,
  'Mirage Clone (Gemini ninjutsu, self buff, AGI +50% 2 rounds: the caster channels chakra to reach extreme speed and leaves an afterimage of itself; v2 decoy behaviour per Christopher 2026-11-03, see extra.decoy): from the guard the fighter makes the seal at the chin and blurs, vibrating in place; it darts forward and straight back faster than the eye, and where it stood an instant before its twin is left standing: for two frames the twin shimmers in, then it is an exact full-colour copy of the fighter, indistinguishable from it, in the same guard (v1 left a pale washed copy)', [
     g(),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0), root=(1, 0)),
     g(bob=(1, 1, 2), lean=(1, 4), root=(9, 0)),
     g(bob=(1, 1, 2), lean=(-1, -2), root=(-10, 0)),
     g(), g(), g()],
  [None, 'squint', 'squint', 'strain', 'strain', None, None, None],
  [0, 1, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#a3aebb'), rm='E: +1 +9 darting forward, -10 back (net 0)',
       ghosts={2: (2, -2), 3: (3, 6, 9), 4: (-3, -6)}, ghostColors=(('#ffffff', '#e9eef4'), ('#e9eef4', None), ('#39e75f', None)),
       runtimeClones=True, clones={4: [(18, 170, 0.35)], 5: [(18, 235, 0.12)], 6: [(18, 255, 0)], 7: [(18, 255, 0)]},
       extra={'decoy': {'rule': 'Mirage Clone v2 (Christopher 2026-11-03): the cast creates an indistinguishable clone of the caster on a free tile next to it (the clip shows it 18 px ahead; the testbed then draws it as its own fighter with the caster\'s exact look, no tint, no label); every hostile fighter currently targeting the caster switches its target to the clone; the clone copies every movement and attack of the caster (same clip, same facing, mirrored from the caster\'s tile offset) but deals no damage; the first damage it takes dispels it: it plays mirageCloneDispel and is removed', 'state': 'mirageCloneDispel', 'appearFrame': 6, 'offsetPx': 18}},
       anchored={1: [('aRing3', 'hand', 0, 0, {'alpha': {'f': 150, 'W': 160}})], 2: [('aStreak2', 'head', -10, 12)],
                 3: [('aStreak', 'head', -14, 14), ('aStreak2', 'feet', -14, -6)], 4: [('aStreak', 'head', 10, 14), ('puff', 'feet', 8, -2)]})),
 'mirageCloneDispel': ('Mirage Clone Dispel', 0,
  'Mirage Clone Dispel (the Mirage Clone decoy takes damage, Christopher 2026-11-03: it disappears after taking damage): the hit lands and the clone jerks back like the real fighter would, so for one beat it still reads as the caster; then it comes apart: the figure breaks up into scattered pixels from the edges in, pale silver puffs of air and green motes bursting out of it, until nothing is left; the last puffs drift up and fade (the testbed removes the clone after the last frame).', [
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -4), root=(-1, 0)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -3), root=(2, 0))],
  ['pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain'],
  None,
  dict(fps=10, rm='E: -1 -1 knocked back, +2 (net 0; nothing is drawn by then)', extra={'dispel': {'rule': 'Mirage Clone v2: the clone plays this once on the first damage it takes, then the testbed removes it', 'removeAfter': True}},
       dissolve={2: 0.22, 3: 0.5, 4: 0.78, 5: 0.94, 6: 1.0, 7: 1.0},
       anchored={0: [('boom4', 'head', 6, 12)],
                 1: [('boom8', 'head', 6, 12, {'alpha': {'W': 200, 'F': 170, 'f': 170, 'q': 160}})],
                 2: [('puff', 'head', 3, 6), ('puff', 'feet', -2, -12), ('spark', 'head', -6, 14)],
                 3: [('puff', 'head', -2, 2), ('puff', 'head', 5, 16), ('puff', 'feet', 3, -6), ('aStreak2', 'head', -2, 10)],
                 4: [('puff', 'head', 0, -2), ('puff', 'head', -5, 12), ('puff', 'feet', 0, -14), ('motesW1', 'head', 0, 4)],
                 5: [('puff', 'head', 1, -6, {'alpha': {'f': 170, 'W': 190, 'F': 150, 'q': 150}}), ('puff', 'feet', -3, -20, {'alpha': {'f': 170, 'W': 190, 'F': 150, 'q': 150}}), ('motesW2', 'head', 0, 0)],
                 6: [('puff', 'head', 0, -10, {'alpha': {'f': 110, 'W': 130, 'F': 100, 'q': 100}}), ('motesW3', 'head', 0, -4, {'alpha': {'f': 140, 'W': 160, 'F': 120, 'q': 120}})],
                 7: []})),
 'resonanceChamber': ('Resonance Chamber', 5,
  'Resonance Chamber (Gemini ninjutsu, Elemental 6, Wide AoE: the caster channels chakra into the air round it and makes it resonate at a destructive frequency): from the guard the fighter makes the seal at the chin, then presses the palms flat together before the chest, trembling, a hum of sound gathering; it draws the palms slowly apart and the air between and round it starts to ring: standing sound waves, rows of white and silver bars, pulse out on both sides of it and a ring of sound runs along the floor; it holds the palms apart, vibrating, as the waves pulse, then lets them fall into the guard (spec extra.zone: the testbed may draw the bars over the area while it hits).', [
     g(),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-70, -110, fistKind='palm'), af=band(-75, -105, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(-70, -110, fistKind='palm'), af=band(-75, -105, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0), root=(1, 0)),
     g(an=band(-70, -110, fistKind='palm'), af=band(-75, -105, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0), root=(-1, 0)),
     g(an=band(-60, -75, fistKind='palm'), af=band(-20, -90, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-60, -75, fistKind='palm'), af=band(-20, -90, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), root=(1, 0), **LOW),
     g(an=band(-60, -75, fistKind='palm'), af=band(-20, -90, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), root=(-1, 0), **LOW),
     g(an=band(-60, -75, fistKind='palm'), af=band(-20, -90, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=band(-40, -110), af=band(-30, -110), bob=(1, 1, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'closed', 'closed', 'closed', 'strain', 'strain', 'strain', 'strain', None, None],
  [0, 1, 1, 2, 2, 2, 2, 2, 2, 1, 0],
  dict(fps=10, auraColors=('#e9eef4', '#39e75f'), rm='E: trembling 1 px (net 0)',
       extra={'zone': {'rule': 'Resonance Chamber is a Wide AoE: from the active frame the testbed may draw bars0-3 pulsing over each target in the area while the hit plays (proposal)', 'shape': 'wide'}},
       anchored={2: [('aRing3', 'hand', 0, 0, {'alpha': {'f': 150, 'W': 160}})], 3: [('aRing5', 'hand', 0, 0, {'alpha': {'F': 150, 'f': 150}})], 4: [('aRing5', 'hand', 0, 0)],
                 **{k_: [('bars%d' % (k_ % 4), 'head', 16, 20), ('bars%d' % ((k_ + 2) % 4), 'head', -17, 20), ('aRing7', 'feet', 0, -2, {'alpha': {'q': 160, 'F': 160}}), ('sine%d' % (k_ % 4), 'hand', 2, -6)] for k_ in (5, 6, 7, 8)},
                 9: [('bars1', 'head', 18, 20, {'alpha': {'W': 120, 'f': 110, 'F': 100}}), ('bars3', 'head', -19, 20, {'alpha': {'W': 120, 'f': 110, 'F': 100}})]})),
 'tinnitus': ('Tinnitus', 5,
  'Tinnitus (Gemini genjutsu, mental DoT: the caster projects a mental ringing into the opponent\'s head that bleeds its mind; Bleed 3 rounds 4/tick, STR save DC 12; range ~12 m): from the guard the fighter raises the near index finger to its own ear and its eyes kindle silver-white; a thin, high ringing line wavers out beside the ear; then it flicks the finger out at the target and the ringing goes after it as thin sine-wave lines, white at the front, silver behind; the finger drops back into the guard (the target plays tinnitusRinging with the genjutsu mark in air colours).', [
     g(),
     g(an=band(-125, -200, fistKind='point'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-125, -205, fistKind='point'), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='point'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#39e75f'), rm='E: +1 flicking the finger out, -1 back',
       extra={'targetState': {'rule': 'Tinnitus: from the active frame the target plays tinnitusRinging: frames 0-2 once, then frames 3-8 on loop until the Bleed ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.air) is drawn over it throughout', 'state': 'tinnitusRinging', 'loopFrom': 3, 'element': 'air', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeW', 'eye', 0, 0)], 2: [('eyeWF', 'eye', 0, 0), ('sine0', 'head', -12, 4)], 3: [('eyeWF', 'eye', 0, 0), ('sine1', 'head', -12, 4), ('earRing', 'hand', 0, -2)],
                 4: [('eyeWF', 'eye', 0, 0), ('sine2', 'head', -12, 4), ('sine0', 'head', -12, 8)],
                 5: [('eyeWF', 'eye', 0, 0), ('sine3', 'hand', 9, 0)], 6: [('eyeWF', 'eye', 0, 0), ('sineL0', 'hand', 12, 0)],
                 7: [('eyeW', 'eye', 0, 0), ('sineL2', 'hand', 14, 1, {'alpha': {'f': 150, 'F': 140}})]})),
 'tinnitusRinging': ('Tinnitus Ringing', 0,
  'Tinnitus Ringing (target state of Tinnitus, Bleed 3 rounds): the ringing hits and the fighter flinches, then claps the far hand to its far ear, the near fist dropping low by the ribs (no hand over the face), hunched and wincing, eyes squeezed shut; thin sine-wave lines of ringing waver off both sides of its head; then (looping while the Bleed lasts) it shudders and sways under the ringing, a drop of blood running from the ear every few beats.', [
     g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-40, -100), af=band(-105, -185, fistKind='palm'), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), **LOW),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 3), lean=(1, 4), **LOW),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3), root=(1, 0), **LOW),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 3), lean=(0, 2), root=(-1, 0), **LOW),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 2), lean=(1, 4), **LOW),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 3), lean=(1, 3), root=(-1, 0), **LOW),
     g(an=band(-35, -95), af=band(-120, -200, fistKind='palm'), bob=(2, 2, 2), lean=(0, 2), root=(1, 0), **LOW)],
  ['pain', 'pain', 'closed', 'pain', 'closed', 'pain', 'closed', 'pain', 'closed'],
  None,
  dict(fps=8, rm='E: shuddering 1 px (net 0)', extra={'loop': True, 'loopFrom': 3},
       anchored={0: [('sine0', 'head', 10, 4)], 1: [('sine1', 'head', 10, 4), ('sine3', 'head', -11, 4)],
                 **{k_: [('sine%d' % (k_ % 4), 'head', 11, 3), ('sine%d' % ((k_ + 2) % 4), 'head', -12, 5)] + ([('drip', 'head', -2, 9)] if k_ in (4, 7) else []) for k_ in range(2, 9)}})),
 'phantomLegion': ('Phantom Legion', 5,
  'Phantom Legion (Gemini genjutsu, debuff: the caster forces the opponent to see many copies of it; Blind 1 round, INT save DC 12; range Zone of Awareness): from the guard the fighter makes the seal at the chin and its eyes kindle silver-white; pale washed copies of itself flicker into being, one ahead of it and one behind, then two more further out, a legion standing in guard; they shimmer and shift a pixel this way and that as if each were the real one; then they fade, the fighter lowers the seal into the guard (the target plays the genjutsu mark in air colours while the Blind lasts).', [
     g(),
     g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)),
     *[g(an=band(-120, -175, fistKind='palm'), af=band(-80, -170), bob=(1, 1, 1), lean=(0, 0)) for _ in range(6)],
     g(an=band(-40, -110), af=band(-45, -120), bob=(1, 1, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 1, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#e9eef4', '#39e75f'),
       runtimeClones=True, clones={2: [(12, 110, 0.35, '#39e75f'), (-12, 110, 0.35, '#39e75f')], 3: [(12, 180, 0.35, '#39e75f'), (-12, 180, 0.35, '#39e75f')], 4: [(12, 190, 0.35, '#39e75f'), (-12, 190, 0.35, '#39e75f'), (24, 120, 0.35, '#39e75f'), (-24, 120, 0.35, '#39e75f')],
               5: [(13, 190, 0.35, '#39e75f'), (-11, 190, 0.35, '#39e75f'), (24, 180, 0.35, '#39e75f'), (-25, 180, 0.35, '#39e75f')], 6: [(11, 190, 0.35, '#39e75f'), (-13, 190, 0.35, '#39e75f'), (25, 180, 0.35, '#39e75f'), (-23, 180, 0.35, '#39e75f')], 7: [(12, 120, 0.35, '#39e75f'), (-12, 120, 0.35, '#39e75f'), (24, 90, 0.35, '#39e75f'), (-24, 90, 0.35, '#39e75f')]},
       extra={'targetState': {'rule': 'Phantom Legion v2 target (Christopher 2026-11-03: rework the target fx): from the active frame the target plays phantomBeset: frames 0-1 once, then frames 2-9 on loop until the Blind ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.air) is drawn over it throughout', 'state': 'phantomBeset', 'loopFrom': 2, 'element': 'air', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeW', 'eye', 0, 0)], **{k_: [('eyeWF', 'eye', 0, 0)] for k_ in range(2, 7)}, 7: [('eyeW', 'eye', 0, 0)]})),
 'phantomBeset': ('Phantom Beset', 0,
  'Phantom Beset (target state of Phantom Legion, Blind 1 round; v2 target fx, Christopher 2026-11-03: rework the target fx): the copies of the caster close in round the fighter: it flinches back with its guard snapped up high, then spins its attention from one to the next, guard jerking forward at the copy in front, then leaning away from the one behind, never sure which is real; around it washed copies of the caster, each outlined in the green rim and facing it, flicker in and out in turn, two in front and two behind, one sliding into a new spot each beat; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.air: white and silver motes with a green edge) is drawn over it throughout.', [
     g(an=band(-75, -150), af=band(-70, -145), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-80, -160), af=band(-75, -150), bob=(1, 1, 2), lean=(-1, -3)),
     g(an=band(-80, -160), af=band(-75, -150), bob=(1, 1, 2), lean=(0, -1), root=(1, 0)),
     g(an=band(-70, -120), af=band(-80, -150), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-70, -120), af=band(-80, -150), bob=(1, 1, 2), lean=(1, 4), root=(1, 0)),
     g(an=band(-80, -160), af=band(-75, -150), bob=(1, 1, 2), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-80, -160), af=band(-75, -150), bob=(1, 1, 2), lean=(-1, -4), root=(-1, 0)),
     g(an=band(-70, -120), af=band(-80, -150), bob=(1, 1, 2), lean=(0, 1), root=(1, 0)),
     g(an=band(-80, -160), af=band(-75, -150), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-80, -160), af=band(-75, -150), bob=(1, 1, 2), lean=(0, 0))],
  ['pain', 'squint', 'squint', 'strain', 'strain', 'pain', 'pain', 'strain', 'squint', 'squint'],
  None,
  dict(fps=8, rm='E: -1 flinch, +1; loop +1 lunging at the front copy, -1 -1 leaning from the one behind, +1 (net 0)',
       extra={'loop': True, 'loopFrom': 2, 'mark': 'genjutsuAfflicted', 'element': 'air', 'legion': {'rule': 'Phantom Legion v2 (Christopher 2026-11-03 19:22: the copies must match the caster, whatever it wears): the testbed draws the copies at runtime from the CASTER\'s own composited sprite (every equipped layer: armour, helmet, hair, eyes, weapons; no fx), frame srcFrame of src in the row that faces the target (a copy ahead of the target, dx > 0, takes the row opposite the target\'s facing; one behind takes the same facing), washed 35% toward #e9eef4 with a 1 px #39e75f outline, at alpha, dx px along the target\'s facing, drawn behind the target; frames {k: [[dx, alpha]]}', 'src': 'phantomLegion', 'srcFrame': 0, 'frames': {0: [(14, 90), (-14, 90)], 1: [(14, 170), (-14, 170), (26, 90)],
               2: [(14, 200), (-14, 200), (26, 150), (-26, 110)], 3: [(15, 210), (-14, 170), (26, 170), (-26, 150)],
               4: [(16, 210), (-13, 140), (25, 120), (-26, 180)], 5: [(14, 150), (-16, 210), (27, 160), (-25, 120)],
               6: [(13, 120), (-16, 210), (26, 180), (-24, 150)], 7: [(15, 210), (-14, 150), (24, 130), (-27, 170)],
               8: [(14, 190), (-15, 190), (26, 170), (-26, 120)], 9: [(14, 200), (-14, 200), (26, 140), (-26, 150)]}}},
       anchored={k_: [('eyeWF' if k_ % 3 else 'eyeW', 'eye', 0, 0)] for k_ in range(10)})),
 'flowDodge': ('Flow Dodge', 3,
  'Flow Dodge (Sagittarius taijutsu stance buff: the fighter enters a dance-like trance and begins to swing and sway to its own rhythm): from the guard the fighter shakes its arms loose and lets the guard drop low and easy, eyes half closed, catching a beat; then it sways to its own rhythm: rocking back and forward on its feet and dipping on the knees, shoulders rolling, the loose hands swinging opposite to the hips, a flickering fire aura breathing round it on the beat with a few black and purple wisps rising off the shoulders; on the last beat it snaps its eyes open and settles into a loose, low guard (the testbed keeps the stance).', [
     g(),
     g(an=band(-10, -40), af=band(-20, -50), bob=(1, 1, 2), lean=(0, 0)),
     g(an=band(15, -30), af=band(-35, -70), bob=(2, 2, 3), lean=(-1, -6), root=(-2, 0), **LOW),
     g(an=band(5, -40), af=band(-25, -60), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-35, -70), af=band(10, -30), bob=(2, 2, 3), lean=(1, 7), root=(2, 0), **LOW),
     g(an=band(-25, -60), af=band(0, -40), bob=(1, 1, 1), lean=(0, 1)),
     g(an=band(15, -30), af=band(-35, -70), bob=(2, 2, 3), lean=(-1, -6), root=(-2, 0), **LOW),
     g(an=band(5, -40), af=band(-25, -60), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-35, -70), af=band(10, -30), bob=(2, 2, 3), lean=(1, 7), root=(2, 0), **LOW),
     g(an=band(-40, -110), af=band(-50, -120), bob=(2, 2, 2), lean=(0, 2)),
     g()],
  [None, 'squint', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', None, None],
  [0, 0, 1, 2, 1, 2, 1, 2, 1, 1, 0],
  dict(fps=8, auraColors=FIRE_AURA, rm='sways 2 px back and forward on the beat (net 0)',
       anchored={3: [('pflame2', 'head', -7, 10), ('flame2', 'head', 6, 12)], 4: [('pembers', 'head', -7, 1)], 5: [('flame2', 'head', -7, 11), ('pflame2', 'head', 6, 10)],
                 6: [('pembers', 'head', 6, 0)], 7: [('pflame2', 'head', -7, 10), ('flame2', 'head', 6, 12)], 8: [('pembers', 'head', -6, 0), ('embers', 'head', 6, 3)]})),
 'spotlight': ('Spotlight', 4,
  'Spotlight (Leo genjutsu, mental debuff: the caster projects its own inner radiance into the foe\'s mind\'s eye, Blind 1 round, INT save DC 12; range Zone of Awareness), v3 (Christopher 2026-10-27: lower the arms, the cone of light pours from the eyes; v3 lean forward a little): from the guard the fighter lets both arms drop to its sides, leans forward a little toward the target and fixes it; its eyes kindle gold, then blaze white-hot, and a cone of light pours out of the eyes toward the target, pale gold and widening, brighter at the core, growing over three frames and holding; the light dies back into the eyes and the fighter brings its hands back up into the guard (the target takes the genjutsu mark, genjutsuAfflicted, for the Blind).', [
     g(),
     g(an=band(-30, -60), af=band(-20, -45), bob=(1, 1, 1), lean=(1, 2)),
     *[g(an=band(-8, -15), af=band(4, -8), bob=(1, 1, 1), lean=(1, 4)) for _ in range(5)],
     g(an=band(-30, -60), af=band(-20, -45), bob=(0, 0, 1), lean=(0, 1)),
     g()],
  [None, None, 'squint', None, None, None, None, None, None],
  [0, 0, 1, 1, 1, 1, 1, 0, 0],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Blind ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       anchored={1: [('eyeGold', 'eye', 0, 0)], 2: [('eyeGold', 'eye', 0, 0)], 3: [('eyeGoldF', 'eye', 0, 0)],
                 4: [('eyeGoldF', 'eye', 0, 0)], 5: [('eyeGoldF', 'eye', 0, 0)], 6: [('eyeGold', 'eye', 0, 0)], 7: [('eyeGold', 'eye', 0, 0, {'alpha': {'Y': 140, 'W': 160}})]},
       cone={'from': 'eye', 3: (12, 1.0), 4: (20, 1.0), 5: (30, 1.0), 6: (30, 0.5)})),
 'kneel': ('Kneel', 4,
  'Kneel (Leo genjutsu, mental debuff: the caster projects its regal presence and imposes it on the foe\'s will, Stun 1 round, STR save DC 14; range Zone of Awareness): from the guard the fighter draws itself up tall, chin lifted, and raises the near hand high, palm out; its eyes kindle gold and an illusory crown of light forms over its head, the lion\'s mane of flame flaring behind it; then it brings the open palm down hard in front of it, palm to the floor, commanding the foe to kneel, the far fist at the hip, and heavy dome-shaped waves of golden pressure roll out toward the target, bearing down and sinking toward the floor as they travel; it holds the command, the crown blazing, then the crown and mane fade and it returns to the guard (the target takes the genjutsu mark, genjutsuAfflicted, for the Stun).', [
     g(),
     g(an=band(-110, -150, fistKind='palm'), af=band(-20, -70), bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-140, -170, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-100, -80, fistKind='palm'), af=band(-5, -40), bob=(0, -1, 0), lean=(0, -1)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-70, -60, fistKind='palm'), af=band(-5, -40), bob=(0, 0, 0), lean=(0, 0)),
     g(an=band(-40, -110), af=band(-25, -90), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, None, 'squint', 'squint', 'squint', 'squint', 'squint', 'squint', None, None],
  [0, 0, 1, 2, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=('#ffe14d', '#ff8a1c'), extra={'targetState': {'rule': 'Christopher 2026-10-27: every genjutsu marks its target; on the active frame the target starts genjutsuAfflicted (fire colours) and keeps it until the Stun ends', 'state': 'genjutsuAfflicted', 'element': 'fire'}},
       anchored={1: [('eyeGold', 'eye', 0, 0), ('crown1', 'head', 0, -7)],
                 2: [('eyeGold', 'eye', 0, 0), ('mane1', 'head', -1, 0, {'behind': True}), ('crown2', 'head', 0, -8)],
                 3: [('eyeGoldF', 'eye', 0, 0), ('mane3', 'head', -1, -1, {'behind': True}), ('crown2', 'head', 0, -8)],
                 4: [('eyeGoldF', 'eye', 0, 0), ('mane4', 'head', -1, -1, {'behind': True}), ('press1', 'feet', 14, -30), ('crown3', 'head', 0, -8)],
                 5: [('eyeGoldF', 'eye', 0, 0), ('mane3b', 'head', -1, -1, {'behind': True}), ('press2', 'feet', 19, -24), ('press1', 'feet', 14, -30), ('crown3', 'head', 0, -8)],
                 6: [('eyeGoldF', 'eye', 0, 0), ('mane3', 'head', -1, -1, {'behind': True}), ('press3', 'feet', 24, -17), ('press2', 'feet', 19, -24), ('crown3', 'head', 0, -8)],
                 7: [('eyeGold', 'eye', 0, 0), ('mane2', 'head', -1, 0, {'behind': True}), ('press3d', 'feet', 27, -10), ('crown2', 'head', 0, -8, {'alpha': {'Y': 170, 'O': 170, 'W': 200, 'R': 150}})],
                 8: [('crown1', 'head', 0, -7, {'alpha': {'Y': 110, 'O': 110, 'W': 140, 'R': 100}})]})),
}

# ---------- Water: Cancer (water colours: white glint W, ice white-blue I, light water a, deep water A, deep edge n) ----------
NPAL.update({'n': '#1b4f99'})
WATER_RECOLOR = {'#ffe14d': '#dff6ff', '#ff8a1c': '#7cc8ff', '#d8321a': '#2f7fe0'}   # fire swirl / impact helpers drawn as water
WATER_TRAIL = {(255, 255, 255): (0x7c, 0xc8, 0xff), (0xe3, 0xe3, 0xe3): (0x2f, 0x7f, 0xe0)}   # motion streak recoloured to a water trail
def _wOrb(r, seed):   # a ball of water: glint top-left, ice-white heart, light body, deep rim and a darker belly, a few drops spinning off it
    import random
    rnd = random.Random(seed); R = r + 3; w = 2 * R + 1; rows = [['.'] * w for _ in range(w)]
    for y in range(w):
        for x in range(w):
            d = math.hypot(x - R, y - R)
            if d <= r: rows[y][x] = 'n' if d > r - 0.9 and y > R else 'A' if d > r - 0.9 else 'a' if d > r * 0.45 or y > R else 'I'
    gx, gy = R - max(1, r // 2), R - max(1, r // 2); rows[gy][gx] = 'W'
    if r > 3: rows[gy][gx + 1] = 'W'
    for k in range(3):
        a = rnd.uniform(0, 2 * math.pi); d = r + rnd.randint(1, 2); x, y = round(R + d * math.cos(a)), round(R + d * math.sin(a))
        if 0 <= x < w and 0 <= y < w: rows[y][x] = 'a'
    return [''.join(q) for q in rows]
def _splash(w, h, seed, n=9, spread=(15, 165), dense=False):   # a crown splash: jets of water thrown up and out from the base, each a parabola of drops, white at the crest
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for k in range(n):
        a = math.radians(spread[0] + (spread[1] - spread[0]) * (k + rnd.random() * 0.5) / n); v = rnd.uniform(0.7, 1.0)
        for t in range(40):
            s = t / 39; x = w / 2 + math.cos(a) * v * (w / 2) * s; y = h - 1 - (math.sin(a) * v * h * 1.6 * s - h * 0.8 * s * s)
            if t % 3 and s > (0.8 if dense else 0.5): continue
            xi, yi = round(x), round(y)
            if 0 <= xi < w and 0 <= yi < h: rows[yi][xi] = 'W' if 0.45 < s < 0.65 else 'I' if s < 0.3 else 'a' if s < 0.8 else 'A'
            if dense and s < 0.6 and 0 <= xi + 1 < w and 0 <= yi < h and rows[yi][xi + 1] == '.': rows[yi][xi + 1] = 'a' if s < 0.4 else 'A'
    for x in range(w // 4, 3 * w // 4): rows[h - 1][x] = 'A' if x % 2 else 'a'   # the foot of the splash, a sheet of water
    return [''.join(q) for q in rows]
def _jet(L, seed, h=7):   # a jet of water spraying out to the right: a dense root that breaks into drops, deep water underneath, white spray on top
    import random
    rnd = random.Random(seed); rows = [['.'] * L for _ in range(h)]; c = h // 2
    for x in range(L):
        s = x / L; half = 1 + s * (h // 2 - 1)
        for y in range(h):
            dy = y - c
            if abs(dy) > half: continue
            if s > 0.45 and rnd.random() < s * 0.8: continue
            rows[y][x] = 'W' if dy == -round(half) and s > 0.2 else 'I' if dy < 0 else 'a' if dy < half - 0.5 else 'A'
    return [''.join(q) for q in rows]
def _drops(w, h, seed, n=10):   # loose droplets
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for _ in range(n):
        x, y = rnd.randrange(w), rnd.randrange(h - 1); rows[y][x] = rnd.choice('aaI'); rows[y + 1][x] = 'A'
    return [''.join(q) for q in rows]
def _wake(w, h):   # a floor wake rolling behind a runner: low at the back, rising to a white lip at the front (the front is the right end)
    rows = [['.'] * w for _ in range(h)]
    for x in range(w):
        top = h - 1 - round((h - 1) * (x / (w - 1)) ** 1.6)
        for y in range(top, h): rows[y][x] = 'W' if y == top and x > w * 0.6 else 'I' if y == top else 'a' if y < top + 2 else 'A' if y < h - 1 else 'n'
    return [''.join(q) for q in rows]
def _crest(h, curl=1.0, thick=2):   # a breaking wave rising behind the runner: gently sloped dark back, light face, white foaming lip hooking forward and down at the top (front = right)
    w = round(h * 0.8) + 2; r = max(1, round(h * 0.22 * curl)); W_ = w + r + 1
    rows = [['.'] * W_ for _ in range(h)]
    for y in range(h):
        s = 1 - y / (h - 1)
        x1 = round((w - 1) * (0.62 + 0.38 * s ** 1.4))
        x0 = round((w - 1) * (0.62 * s ** 1.3))
        for x in range(x0, x1 + 1):
            e = x1 - x
            rows[y][x] = 'W' if e == 0 and s > 0.6 else 'I' if e < 2 else 'a' if e < 3 + round(3 * s) else 'A' if x > x0 + 1 else 'n'
        if s > 0.85: rows[y][x0] = 'W'
    cx, cy = w - 1, r
    for t in range(80):
        th = math.pi / 2 - t / 79 * (math.pi / 2 + math.pi / 2.6)
        x, y = round(cx + r * math.cos(th)), round(cy - r * math.sin(th))
        if thick <= 2:
            for dd, ch in ((0, 'W'), (1, 'I')):
                if 0 <= x - dd < W_ and 0 <= y < h and rows[y][x - dd] == '.': rows[y][x - dd] = ch
        else:   # Tsunami: a thick curling lip, the annulus filled radially in toward the curl's centre
            for dd, ch in zip(range(thick), 'WIaaAn'):
                xx, yy = round(cx + (r - dd) * math.cos(th)), round(cy - (r - dd) * math.sin(th))
                if 0 <= xx < W_ and 0 <= yy < h and rows[yy][xx] in '.n' + ('A' if ch in 'WI' else ''): rows[yy][xx] = ch
    return [''.join(q) for q in rows]
def _sq(p, sx=1.0, sy=1.0):   # resize a pattern (nearest)
    h, w = len(p), len(p[0]); H, Wd = max(1, round(h * sy)), max(1, round(w * sx))
    return [''.join(p[min(h - 1, int(y / sy))][min(w - 1, int(x / sx))] for x in range(Wd)) for y in range(H)]
_flipx = lambda p: [q[::-1] for q in p]
NPAT.update({**{'wOrb%d' % r: _wOrb(r, 40 + r) for r in (2, 3, 4, 5)},
             'wSplash': _splash(21, 14, 3), 'wSplashL': _splash(29, 19, 5, n=12), 'wSplashS': _splash(13, 8, 7, n=6),
             'wJet': _jet(14, 2), 'wJetL': _jet(20, 4, h=9), 'wJetB': _flipx(_jet(14, 6)), 'wJetBL': _flipx(_jet(20, 8, h=9)),
             'wDrops': _drops(15, 12, 1), 'wDropsL': _drops(23, 16, 2, n=16),
             'wWake': _wake(12, 4), 'wWakeL': _wake(18, 6),
             **{'wCrest%d' % h: _crest(h, curl=min(1, h / 30)) for h in (10, 20, 30, 40, 52)}, 'wSplashXL': _splash(41, 28, 9, n=20, spread=(10, 170), dense=True), 'wSplashLD': _splash(29, 19, 5, n=14, dense=True),
             'wRing': _ring(5, 'a', 'I'), 'wRing2': _ring(8, 'a', 'I'), 'wRing3': _ring(11, 'A', 'a', gap=1),
             'wArc1': _arc(4, 2, 'Ia'), 'wArc2': _arc(6, 3, 'Ia'), 'wArc3': _arc(8, 4, 'aA'), 'wArcB2': _flipx(_arc(6, 3, 'Ia')), 'wArcB3': _flipx(_arc(8, 4, 'aA')),
             'wClaw': ['...aaIW', '.aaA...', 'aA.....', 'aA.....', 'aA.....', '.aaA...', '...aaIW'], 'wClawShut': ['..aaaIW', '.aA..II', 'aA....I', 'aA....I', '.aA..II', '..aaaIW'],   # the crab pincer: an open C of water round the hand, then snapped shut
             'wPuddle': ['..aaaaaaa..', '.aAAIAAAAa.', 'aAnnAAnnAAa', '.aAAAAAAAa.']})
_BR = CLIPS['bullRush']; _SP = CLIPS['shockPalm']
_A = lambda d: {'alpha': d}
_FADE = {'W': 150, 'I': 140, 'a': 130, 'A': 120, 'n': 110}
_CR = {'A': 215, 'n': 200, 'a': 235}   # the wave's body a little see-through
CLIPS.update({
 'tidalSlam': ('Tidal Slam', 10,
  'Tidal Slam (Cancer taijutsu gap closer, Physical 16, Melee (Reach +4m), Gap Closer: the fighter gathers a running start and gains enough momentum to slam into its opponent): from the guard the fighter drops into the low sprinter\'s set and water pools round its feet; it bursts into a head-down sprint, a wake of water rolling off its heels, and with every stride a wave builds behind it, rising taller and curling forward over its back as the run gains momentum; it tucks and slams the shoulder in, and the wave comes crashing down over the impact in a great crown splash and a jet of water bursting forward, drops raining; it settles back into the guard in a spreading puddle. Body from Bull Rush (approved), water colours; travel 40 px.',
  copy.deepcopy(_BR[3]), list(_BR[4]), None,
  dict(fps=12, hitbox=[42, 24, 14, 16], damage='medium', rm='E: as Bull Rush, 6 px a stride through the sprint, +3 and +1 into the slam; 40 px in all (travel)',
       blur={k: 9 for k in range(4, 10)} | {10: 7, 11: 4}, trail=WATER_TRAIL,
       extra={'travel': {'rule': 'Tidal Slam is a gap closer: the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40}},
       anchored={1: [('wPuddle', 'feet', 0, -1, _A(_FADE))], 2: [('wPuddle', 'feet', 0, -1), ('wDrops', 'feet', -6, -5, _A(_FADE))], 3: [('wPuddle', 'feet', -1, -1), ('wSplashS', 'feet', -6, -4)],
                 4: [('wWake', 'feet', -11, -2), ('wSplashS', 'feet', -5, -4)],
                 5: [('wWake', 'feet', -12, -2), ('wCrest10', 'feet', -10, -5, {'behind': True, 'alpha': _CR})],
                 6: [('wWakeL', 'feet', -14, -3), ('wCrest20', 'feet', -11, -10, {'behind': True, 'alpha': _CR}), ('wDrops', 'feet', -18, -14, _A(_FADE))],
                 7: [('wWakeL', 'feet', -14, -3), ('wCrest30', 'feet', -12, -15, {'behind': True, 'alpha': _CR}), ('wSplashS', 'feet', -4, -4)],
                 8: [('wWakeL', 'feet', -14, -3), ('wCrest40', 'feet', -13, -20, {'behind': True, 'alpha': _CR}), ('wDrops', 'feet', -20, -22, _A(_FADE))],
                 9: [('wWakeL', 'feet', -13, -3), ('wCrest52', 'feet', -12, -26, {'behind': True, 'alpha': _CR}), ('wSplashS', 'feet', -3, -4)],
                 10: [('wCrest40', 'feet', -4, -20, {'behind': True, 'alpha': _CR}), ('wSplashXL', 'head', 7, 2), ('wJetL', 'hand', 12, 0), ('wDropsL', 'head', 6, -6)],
                 11: [('wCrest20', 'feet', 2, -10, {'behind': True, 'alpha': _FADE}), ('wSplashLD', 'head', 9, 4), ('wSplash', 'feet', 16, -7), ('wDropsL', 'head', 12, 2), ('wJet', 'hand', 14, 0, _A(_FADE)), ('wPuddle', 'feet', 8, -1)],
                 12: [('wDropsL', 'head', 14, 10, _A(_FADE)), ('wPuddle', 'feet', 6, -1), ('wSplash', 'feet', 16, -7, _A(_FADE))],
                 13: [('wPuddle', 'feet', 2, -1, _A(_FADE))]})),
 'viceGrip': ('Vice Grip', 5,
  'Vice Grip (Cancer taijutsu, Physical 12, Melee, Grapple: using its manoeuvrability the fighter bypasses the opponent\'s guard to secure a grapple): from the guard the fighter ducks and slips in low and sideways like a crab, a slick of water skimming under its feet; out of the crouch both hands shoot in at once, one high and one low, open like a crab\'s pincers, each wrapped in a C of water; the pincers snap shut on the opponent with a splash, both hands clamped, and the fighter holds the grip as the water drips off. On success the testbed puts both fighters into the clinch with the caster holding (target plays hitReact on the clamp).',
  [g(),
   g(an=band(-40, -100), af=band(-50, -110), bob=(5, 6, 6), lean=(2, 7), root=(2, 0), ln='gs-wide-rear', lf='gs-crouch-lead'),
   g(an=band(-60, -75, fistKind='palm'), af=band(-55, -85, fistKind='palm'), bob=(9, 10, 10), lean=(2, 10), root=(3, 0), ln='gs-wide-rear', lf='gs-crouch-lead'),
   g(an=band(-108, -125, fistKind='palm'), af=band(-68, -58, fistKind='palm'), bob=(4, 5, 5), lean=(2, 7), root=(3, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(an=band(-108, -125, fistKind='palm'), af=band(-68, -58, fistKind='palm'), bob=(4, 5, 5), lean=(2, 7), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(an=band(-96, -100, fistKind='palm'), af=band(-82, -76, fistKind='palm'), bob=(3, 3, 4), lean=(1, 5), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(an=band(-96, -100, fistKind='palm'), af=band(-82, -76, fistKind='palm'), bob=(3, 3, 4), lean=(1, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(an=band(-94, -100, fistKind='palm'), af=band(-82, -78, fistKind='palm'), bob=(2, 3, 3), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead')],
  [None, 'squint', 'strain', 'strain', 'strain', 'strain', 'squint', 'squint'],
  None,
  dict(fps=10, hitbox=[42, 18, 16, 22], damage='light', rm='E: +2 +3 +3 slipping in low, +1 into the clamp (9 px; the testbed then snaps both fighters to the clinch spacing)',
       extra={'grapple': {'rule': 'Vice Grip is a Grapple: on success both fighters enter the clinch with the caster holding (testbed clinch rules apply: posOverride, noGrappled, shield bearers immune until Disarmed); the clip ends on the clamp and hands over to the clinch hold idle', 'onSuccess': 'clinch', 'holder': 'caster', 'targetState': 'hitReact'}},
       anchored={1: [('wWake', 'feet', -8, -2, _A(_FADE))], 2: [('wWakeL', 'feet', -10, -3), ('wDrops', 'feet', -12, -6, _A(_FADE))],
                 3: [('wClaw', 'hand', 1, 0), ('wClaw', 'farhand', 1, 0), ('wJetB', 'hand', -6, 0, _A(_FADE)), ('wWake', 'feet', -10, -2)],
                 4: [('wClaw', 'hand', 2, 0), ('wClaw', 'farhand', 2, 0), ('wDrops', 'hand', -3, 4, _A(_FADE))],
                 5: [('wClawShut', 'hand', 1, 0), ('wClawShut', 'farhand', 1, 0), ('wSplash', 'hand', 3, 2), ('wDrops', 'farhand', 2, 3)],
                 6: [('wClawShut', 'hand', 1, 0, _A(_FADE)), ('wClawShut', 'farhand', 1, 0, _A(_FADE)), ('wDrops', 'hand', 0, 8)],
                 7: [('wDrops', 'feet', 4, -6, _A(_FADE)), ('wPuddle', 'feet', 4, -1, _A(_FADE))]})),
 'hydroCannonPalm': ('Hydro Cannon Palm', 4,
  'Hydro Cannon Palm (Cancer taijutsu strike, Physical 14, Melee, 2 slots: the fighter slams its palm into the opponent, creating a hydrostatic pressure wave that travels through its body): from the guard the fighter draws the rear hand back low beside the hip, palm open, and a ball of water gathers and swells in it over three frames, water swirling up round the arm; then it steps in and slams the open palm into the chest: the ball bursts on contact in a white splash, a pressure ring blasts out round the palm and pressure arcs roll forward through the target, a jet of water spraying on out the far side; it settles back into the guard (the target plays hydroWaved). Body from Shock Palm (approved), water colours.',
  copy.deepcopy(_SP[3]), list(_SP[4]), None,
  dict(fps=10, hitbox=[46, 20, 14, 10], damage='heavy', rm='E: +2 stepping into the palm, -2 settling back',
       swirl={1: (0, 0.5), 2: (120, 0.8), 3: (240, 1.0)}, impact={4: 0, 5: 1, 6: 2, 7: 3}, recolor=WATER_RECOLOR, keepFx=True,
       extra={'targetState': {'rule': 'Hydro Cannon Palm: on the hit the target plays hydroWaved once (the pressure wave ripples through its body and bursts out of its back), then its idle', 'state': 'hydroWaved'}},
       anchored={1: [('wOrb2', 'hand', 0, 0)], 2: [('wOrb3', 'hand', 0, 0), ('wDrops', 'hand', 0, -4, _A(_FADE))], 3: [('wOrb4', 'hand', 0, 0), ('wSplashS', 'hand', 0, -5, _A(_FADE))],
                 4: [('wSplash', 'hand', 4, -3), ('wRing', 'hand', 2, 0), ('wArc1', 'hand', 7, 0)],
                 5: [('wRing2', 'hand', 3, 0), ('wArc2', 'hand', 10, 0), ('wDrops', 'hand', 4, -6)],
                 6: [('wRing3', 'hand', 4, 0, _A(_FADE)), ('wArc3', 'hand', 14, 0), ('wJetL', 'hand', 20, 0)],
                 7: [('wArc3', 'hand', 18, 0, _A(_FADE)), ('wDropsL', 'hand', 10, 4, _A(_FADE))]})),
 'hydroWaved': ('Hydro Waved', 0,
  'Hydro Waved (target state of Hydro Cannon Palm): the palm lands on its chest and the water bursts there; the fighter jolts back, then the hydrostatic wave rolls through it: ripples of water cross its body from the chest to the back, and burst out of its back in a jet of spray and drops; it doubles over, arms clutched to the belly, water dripping, staggers a step and recovers its guard.',
  [g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(-2, -5), root=(-1, 0)),
   g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(-2, -4)),
   g(an=band(-50, -120), af=band(-45, -115), bob=(1, 1, 2), lean=(-1, -3)),
   g(an=band(-65, -140), af=band(-55, -135), bob=(1, 1, 1), lean=(-3, -8), root=(-1, 0)),
   g(an=band(-10, -120), af=band(-5, -115), bob=(5, 5, 5), lean=(3, 13), **LOW),
   g(an=band(-10, -120), af=band(-5, -115), bob=(5, 5, 5), lean=(3, 12), **LOW),
   g(an=band(-40, -125), af=band(-35, -120), bob=(2, 2, 2), lean=(1, 4), root=(1, 0)),
   g(an=band(-45, -115), af=band(-40, -110), bob=(1, 1, 1), lean=(0, 1), root=(1, 0)),
   g()],
  ['pain', 'pain', 'pain', 'pain', 'strain', 'strain', 'squint', None, None],
  None,
  dict(fps=10, rm='E: -1 jolted back, -1 as the wave bursts out of the back, +1 +1 recovering (net 0)',
       anchored={0: [('wSplash', 'head', 6, 12), ('wRing', 'head', 5, 14)],
                 1: [('wArc1', 'head', 3, 14, {'onFig': True}), ('wDrops', 'head', 7, 10, _A(_FADE))],
                 2: [('wArcB2', 'head', -1, 14, {'onFig': True}), ('wArc1', 'head', 3, 14, {'onFig': True, 'alpha': _FADE})],
                 3: [('wJetBL', 'head', -16, 14), ('wArcB3', 'head', -9, 14), ('wDropsL', 'head', -14, 8, _A(_FADE))],
                 4: [('wJetB', 'head', -18, 16, _A(_FADE)), ('wDrops', 'head', -16, 12)],
                 5: [('wDrops', 'feet', 2, -8, _A(_FADE)), ('wPuddle', 'feet', 0, -1)],
                 6: [('wPuddle', 'feet', -1, -1, _A(_FADE))]})),
})

# ---------- Cancer ninjutsu v1 (part 12, 2026-11-03): Water Cutter, Whirlpool, Tsunami ----------
def _wBlade(R, t, tail=6, seed=0):   # Water Cutter: a thin ')' blade of high-pressure water flying right: white cutting edge, ice, light body, deep back, deep-edge tips, a spray of drops trailing
    import random
    rnd = random.Random(seed); h = 2 * R + 1; w = tail + t + 3; rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        dy = (y - R) / R; s = 1 - dy * dy; xf = tail + round(t * s) + 1; th = max(1, round((t * 0.6 + 1) * s ** 0.5))
        for i in range(th + 1):
            x = xf - i
            if 0 <= x < w: rows[y][x] = 'n' if abs(dy) > 0.85 else 'W' if i == 0 else 'I' if i == 1 else 'a' if i < th else 'A'
        if abs(dy) < 0.5:
            for x in range(0, xf - th - 1):
                if rnd.random() < 0.35 * (x + 1) / (xf - th): rows[y][x] = rnd.choice('aAI')
    return [''.join(q) for q in rows]
def _wCut(n, seed=0):   # Water Cutter hit: a diagonal slash of water, top-right to bottom-left, white core, ice flanks, drops thrown off it
    import random
    rnd = random.Random(seed); rows = [['.'] * n for _ in range(n)]
    for i in range(n):
        x, y = n - 1 - i, i; e = abs(i - n / 2) / (n / 2)
        rows[y][x] = 'W' if e < 0.6 else 'I'
        for d, ch in ((1, 'I'), (-1, 'a')):
            if 0 <= x + d < n and e < 0.8: rows[y][x + d] = ch
    for _ in range(n // 2):
        x, y = rnd.randrange(n), rnd.randrange(n)
        if rows[y][x] == '.': rows[y][x] = rnd.choice('aAI')
    return [''.join(q) for q in rows]
def _vortex(rx, ry, phase, part='all', arms=3):   # Whirlpool: a churning whirlpool seen from the side as a flat ellipse: deep-edge eye, deep water, spiral arms of light water and ice turning with phase, white foam dashes on the rim
    w, h = 2 * rx + 1, 2 * ry + 1; rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            u, v = (x - rx) / rx, (y - ry) / ry; d = math.hypot(u, v)
            if d > 1: continue
            a = math.atan2(v, u); sp = (a + 2.6 * d * math.pi + phase * math.pi / 2) % (2 * math.pi / arms)
            ch = 'n' if d < 0.22 else 'A'
            if d >= 0.22 and sp < 0.55: ch = 'I' if d > 0.6 else 'a'
            if d > 0.86: ch = 'W' if (x + phase * 2) % 4 < 2 else 'I'
            rows[y][x] = ch
    if part == 'front':
        for y in range(h):
            if y <= ry: rows[y] = ['.'] * w
    return [''.join(q) for q in rows]
def _helix(rx, H, phase, front=True, strands=3, turns=1.6):   # Whirlpool: water spiralling up round the legs; front strands are drawn over the fighter, back strands behind it
    w = 2 * rx + 1; rows = [['.'] * w for _ in range(H)]
    for s in range(strands):
        for t in range(240):
            u = t / 239; th = phase * math.pi / 2 + s * 2 * math.pi / strands + u * 2 * math.pi * turns
            r_ = rx * (1 - 0.35 * u); x = round(rx + r_ * math.cos(th)); y = round(H - 1 - u * (H - 1))
            if (math.sin(th) > 0) != front or not (0 <= x < w): continue
            rows[y][x] = ('W' if t % 9 == 0 else 'I' if u > 0.6 else 'a') if front else 'A'
            if y + 1 < H and rows[y + 1][x] == '.': rows[y + 1][x] = ('a' if u > 0.6 else 'A') if front else 'n'   # 2 px thick strands
    return [''.join(q) for q in rows]
def _engulf(w, h, seed):   # Tsunami struck: the crashed wave's churning mass swallowing the fighter: a rounded body with a foaming, ragged top, swirling ice-white currents, deep water at the rim, white bubbles
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            u = (x - (w - 1) / 2) / (w / 2); v = (y - h * 0.55) / (h * 0.55)
            wob = 0.12 * math.sin(x * 0.7 + seed) + 0.08 * math.sin(x * 1.9)
            d = u * u * (1 + 0.6 * max(0, v)) + (v * v if v < 0 else v * v * 0.5) - wob * (v < 0)
            if d > 1: continue
            sw = math.sin(0.33 * x + 0.5 * math.sin(0.21 * y + seed) * 6) + math.sin(0.17 * y - 0.4 * x)
            ch = 'A' if d > 0.82 else 'I' if sw > 1.25 else 'a'
            if v < 0 and d > 0.72: ch = 'W' if rnd.random() < 0.7 else 'I'
            rows[y][x] = ch
    for _ in range(w * h // 30):
        x, y = rnd.randrange(w), rnd.randrange(h)
        if rows[y][x] in 'aI': rows[y][x] = 'W'
    return [''.join(q) for q in rows]
def _foam(w, h, seed):   # white foam and spray thrown up off a breaking wave
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for _ in range(w * h // 5):
        x, y = rnd.randrange(w), rnd.randrange(h)
        if rnd.random() < 1 - y / h * 0.5: rows[y][x] = rnd.choice('WWI')
    return [''.join(q) for q in rows]
NPAT.update({'wBladeS': _wBlade(4, 2, tail=2, seed=1), 'wBlade': _wBlade(7, 4, seed=2), 'wBladeL': _wBlade(9, 5, tail=8, seed=3), 'wCut': _wCut(13, 4),
             **{'wVortex%d' % p: _vortex(19, 6, p) for p in range(4)}, **{'wVortexF%d' % p: _vortex(19, 6, p, 'front') for p in range(4)},
             **{'wVortexS%d' % p: _vortex(10, 3, p) for p in range(2)}, **{'wVortexSF%d' % p: _vortex(10, 3, p, 'front') for p in range(2)},
             **{'wHelixF%d' % p: _helix(11, 20, p) for p in range(4)}, **{'wHelixB%d' % p: _helix(11, 20, p, front=False) for p in range(4)},
             **{'wCrestB%d' % h: _flipx(_crest(h, curl=min(1, h / 30))) for h in (20, 40, 52)}, 'wCrest56': _crest(56, thick=5), 'wCrestB56': _flipx(_crest(56, thick=5)), 'wCrest56T': [q if i < 17 else '.' * len(q) for i, q in enumerate(_crest(56, thick=5))], 'wCrest52T': [q if i < 16 else '.' * len(q) for i, q in enumerate(_crest(52, thick=5))], 'wCrestB56T': [q if i < 17 else '.' * len(q) for i, q in enumerate(_flipx(_crest(56, thick=5)))],
             'wEngulf': _engulf(32, 54, 5), 'wEngulfLow': _engulf(32, 54, 5)[30:], 'wFoam': _foam(25, 10, 6), 'wFoamL': _foam(37, 14, 7)})
_WAURA = ('#dff6ff', '#2f7fe0')   # water aura (runtime, follows the fighter's own outline)
CLIPS.update({
 'waterCutter': ('Water Cutter', 4,
  'Water Cutter (Cancer ninjutsu, Elemental 20, Ranged: the caster conjures a high-pressure water blade): from the guard the fighter makes the seal at the chin and water beads rise round it; it sweeps the near knife hand back behind it at shoulder height and the water gathers along the edge of the hand, pressed into a thin spinning blade; then it slashes the knife hand forward flat and level, stepping in, and the blade (a thin white-edged crescent of high-pressure water trailing spray) is flung off the edge of the hand and flies on toward the target; the hand follows through high, drops shaken off it, and the fighter settles back into the guard (spec extra.projectile: the testbed flies wBladeL from the near hand to the target, then draws wCut on it; the target plays hitReact).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(75, 95, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(80, 95, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 2), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(30, -60), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-115, -125, fistKind='palm'), af=band(35, -40), bob=(2, 2, 2), lean=(2, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-115, -125, fistKind='palm'), af=band(35, -40), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -110), af=band(-30, -100), bob=(1, 1, 2), lean=(1, 2), root=(-2, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'roar', 'strain', 'squint', None, None],
  [0, 1, 1, 2, 2, 1, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +2 stepping into the slash, -2 settling back',
       extra={'projectile': {'rule': 'Water Cutter: from frame 5 (frame 4 draws the blade leaving the hand) the testbed flies NPAT wBladeL from the near hand to the target at chest height (fast, 2-3 frames), then draws wCut on it; the target plays hitReact', 'from': 'hand', 'frame': 5, 'pattern': 'wBladeL', 'hit': 'wCut', 'targetState': 'hitReact'}},
       anchored={1: [('wDrops', 'head', 0, 14, _A(_FADE))],
                 2: [('wOrb2', 'head', -18, 8), ('wDrops', 'head', -15, 4, _A(_FADE)), ('wArcB2', 'head', -12, 8, _A(_FADE))],
                 3: [('wBladeS', 'head', -20, 8), ('wOrb2', 'head', -14, 9, _A(_FADE)), ('wArcB2', 'head', -11, 8)],
                 4: [('wBlade', 'hand', 1, 0), ('wJetB', 'hand', -8, 0, _A(_FADE))],
                 5: [('wDrops', 'hand', -2, 3), ('wArc1', 'hand', -2, 3, _A(_FADE))],
                 6: [('wDrops', 'hand', -3, 8, _A(_FADE))]})),
 'whirlpool': ('Whirlpool', 6,
  'Whirlpool (Cancer ninjutsu, Elemental 8, 2 m AoE centred on the target, Root 1 round STR save DC 12: the caster conjures a puddle of water that violently turns into a churning whirlpool beneath the opponent): from the guard the fighter makes the seal at the chin; then it reaches the near open hand out low toward the target, palm down, water dripping from it, and circles the palm over the ground, beads of water running round beneath it; it clenches the hand into a fist and wrenches it round (the targets play whirlpoolCaught: the puddle opens under their feet and churns into a whirlpool); it holds the twist a beat and settles back into the guard.', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-45, -60, fistKind='palm'), bob=(2, 2, 2), lean=(1, 3)),
     g(an=band(-50, -70, fistKind='palm'), bob=(2, 2, 2), lean=(1, 4)),
     g(an=band(-42, -65, fistKind='palm'), bob=(2, 2, 3), lean=(1, 4)),
     g(an=band(-48, -58, fistKind='palm'), bob=(2, 2, 3), lean=(1, 4)),
     g(an=band(-50, -65), bob=(3, 3, 3), lean=(1, 5), root=(1, 0), **LOW),
     g(an=band(-50, -65), bob=(3, 3, 3), lean=(1, 5), **LOW),
     g(an=band(-50, -115), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'roar', 'strain', None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +1 wrenching the fist round, -1 back',
       extra={'targetState': {'rule': 'Whirlpool: from the active frame (6, the wrench) the target and every fighter within the 2 m AoE round it play whirlpoolCaught: frames 0-3 once (the puddle opens and churns into a whirlpool), then frames 4-9 on loop while the Root lasts, then whirlpoolRelease once', 'state': 'whirlpoolCaught', 'loopFrom': 4, 'release': 'whirlpoolRelease', 'element': 'water'}},
       anchored={1: [('wDrops', 'head', 0, 14, _A(_FADE))],
                 2: [('wDrops', 'hand', 0, 4, _A(_FADE)), ('wOrb2', 'hand', 3, 6)],
                 3: [('wDrops', 'hand', 0, 5, _A(_FADE)), ('wOrb2', 'hand', -1, 7), ('wOrb2', 'hand', 5, 5, _A(_FADE))],
                 4: [('wOrb2', 'hand', -4, 6), ('wOrb2', 'hand', 2, 8, _A(_FADE)), ('wRing', 'hand', 0, 7, _A(_FADE))],
                 5: [('wOrb2', 'hand', 0, 9), ('wOrb2', 'hand', -4, 5, _A(_FADE)), ('wRing', 'hand', 0, 7)],
                 6: [('wSplashS', 'hand', 0, -2), ('wRing2', 'hand', 0, 2, _A(_FADE))],
                 7: [('wDrops', 'hand', 0, 4, _A(_FADE))]})),
 'whirlpoolCaught': ('Whirlpool Caught', 0,
  'Whirlpool Caught (target state of Whirlpool, Root 1 round): a puddle of water spreads under the fighter\'s feet and opens into a churning whirlpool (deep eye, spiral arms of light water, white foam on the rim, the near rim lapping over its feet); the fighter lurches, its feet dragged into the turn, arms thrown out for balance; water spirals up round its legs to the knee; then (looping while the Root lasts) it strains to pull free, sinking a little, arms flailing, the whirlpool turning and the water spiralling round the legs.', [
     g(an=band(-50, -130), af=band(-40, -125), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-80, -110), af=band(40, 70), bob=(2, 2, 2), lean=(-1, -3)),
     g(an=band(-100, -130), af=band(60, 95), bob=(3, 3, 3), lean=(1, 3), **LOW),
     g(an=band(-95, -120), af=band(55, 90), bob=(4, 4, 4), lean=(1, 4), **LOW),
     g(an=band(-100, -130), af=band(60, 95), bob=(4, 4, 4), lean=(1, 4), root=(1, 0), **LOW),
     g(an=band(-85, -105), af=band(45, 70), bob=(4, 4, 5), lean=(2, 6), **LOW),
     g(an=band(-100, -125), af=band(60, 90), bob=(4, 4, 4), lean=(1, 4), root=(-1, 0), **LOW),
     g(an=band(-110, -140), af=band(65, 100), bob=(4, 4, 4), lean=(0, 2), **LOW),
     g(an=band(-90, -110), af=band(50, 75), bob=(4, 4, 5), lean=(2, 6), root=(1, 0), **LOW),
     g(an=band(-100, -130), af=band(60, 95), bob=(4, 4, 4), lean=(1, 4), root=(-1, 0), **LOW)],
  ['squint', 'pain', 'pain', 'strain', 'strain', 'pain', 'strain', 'strain', 'pain', 'strain'],
  None,
  dict(fps=8, rm='E: rocking 1 px in the loop (net 0)', extra={'loop': True, 'loopFrom': 4},
       anchored={0: [('wPuddle', 'feet', 0, -1)],
                 1: [('wVortexS0', 'feet', 0, -2, {'behind': True}), ('wVortexSF0', 'feet', 0, -2), ('wDrops', 'feet', 0, -6, _A(_FADE))],
                 2: [('wVortex1', 'feet', 0, -3, {'behind': True}), ('wVortexF1', 'feet', 0, -3), ('wSplashS', 'feet', 8, -5)],
                 3: [('wVortex2', 'feet', 0, -3, {'behind': True}), ('wVortexF2', 'feet', 0, -3), ('wHelixB0', 'feet', 0, -12, {'behind': True}), ('wHelixF0', 'feet', 0, -12, _A(_FADE))],
                 **{k_: [('wVortex%d' % (k_ % 4), 'feet', 0, -3, {'behind': True}), ('wVortexF%d' % (k_ % 4), 'feet', 0, -3), ('wHelixB%d' % (k_ % 4), 'feet', 0, -12, {'behind': True}), ('wHelixF%d' % (k_ % 4), 'feet', 0, -12, {'alpha': {'a': 215, 'A': 215, 'I': 230}})] + ([('wSplashS', 'feet', -9 if k_ % 4 else 9, -6, _A(_FADE))] if k_ % 2 else []) for k_ in range(4, 10)}})),
 'whirlpoolRelease': ('Whirlpool Release', 0,
  'Whirlpool Release (target state, plays once when the Root of Whirlpool ends): the whirlpool slows and drains away into a puddle, the water round the legs falls back, and the fighter hauls its feet free and steps back up into the guard.', [
     g(an=band(-100, -130), af=band(60, 95), bob=(4, 4, 4), lean=(1, 4), **LOW),
     g(an=band(-70, -120), af=band(20, -40), bob=(2, 2, 3), lean=(1, 2), **LOW),
     g(an=band(-50, -125), af=band(-40, -120), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g(an=band(-50, -120), af=band(-40, -120), bob=(1, 1, 1), lean=(0, 0), root=(1, 0)),
     g()],
  ['strain', 'squint', 'squint', None, None],
  None,
  dict(fps=8, anchored={0: [('wVortexS1', 'feet', 0, -2, {'behind': True}), ('wVortexSF1', 'feet', 0, -2), ('wHelixF1', 'feet', 0, -12, _A(_FADE))],
                        1: [('wPuddle', 'feet', 0, -1), ('wDrops', 'feet', 0, -8, _A(_FADE))],
                        2: [('wPuddle', 'feet', 1, -1, _A(_FADE))]})),
 'tsunamiStruck': ('Tsunami Struck', 2,
  'Tsunami Struck v2 (target state of Tsunami, plays once when the wave front reaches the fighter): spray whips at it and it throws its forearms up over its head as the wave rears over it; the wave crashes down on it in a burst of foam and swallows it, and it is ripped off its feet and tumbled flat through the water (seen through it), swept back, bubbles streaming off it; the water dumps it down onto one knee as it drains away round it in a wake; it coughs, doubled over and dripping in a spreading flood, then hauls itself up into its guard.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(0, -2)),
     g(an=band(-140, -170), af=band(-130, -165), bob=(2, 2, 2), lean=(-1, -3)),
     g(an=band(-150, -175), af=band(-140, -170), bob=(3, 3, 3), lean=(-2, -6), root=(-3, 0), **LOW),
     g(an=band(-150, -175), af=band(-140, -170), bob=(1, 1, 1), lean=(0, 0), root=(-3, 0)),
     g(an=band(-120, -160), af=band(40, 90), bob=(1, 1, 1), lean=(0, 0), root=(-2, 0)),
     g(an=band(-40, -110), af=band(-30, -100), bob=(9, 10, 10), lean=(2, 8), root=(-2, 0), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-10, -120), af=band(-5, -115), bob=(9, 10, 10), lean=(3, 12), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-10, -120), af=band(-5, -115), bob=(9, 10, 10), lean=(3, 13), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-20, -120), af=band(-10, -115), bob=(4, 4, 4), lean=(2, 9), root=(2, 0), **LOW),
     g(an=band(-45, -120), af=band(-35, -115), bob=(2, 2, 2), lean=(1, 3), root=(4, 0)),
     g(root=(4, 0))],
  ['squint', 'pain', 'closed', 'closed', 'closed', 'pain', 'pain', 'strain', 'squint', 'squint', None],
  None,
  dict(fps=10, rm='E: -3 -3 -2 -2 swept back, +2 +4 +4 recovering (net 0)', invert={3: (1, 90), 4: (1, 90)},
       anchored={0: [('wFoam', 'feet', 12, -42, _A(_FADE)), ('wDrops', 'head', 8, 4), ('wSplashS', 'head', 8, 10)],   # v2: the wave itself is the zone wave the testbed rolls in (extra.zone of tsunami)
                 1: [('wFoamL', 'feet', 4, -56), ('wDropsL', 'head', 6, 0)],
                 2: [('wEngulf', 'feet', 2, -27, {'behind': True}), ('wEngulf', 'feet', 2, -27, {'onFig': True, 'alpha': {'a': 150, 'I': 160, 'A': 170, 'W': 220}}), ('wFoamL', 'feet', 4, -46), ('wSplashXL', 'feet', 6, -14)],
                 3: [('wEngulfH', 'feet', 0, -13, {'behind': True}), ('wEngulfH', 'feet', 0, -13, {'onFig': True, 'alpha': {'a': 140, 'I': 150, 'A': 160, 'W': 220}}), ('wFoam', 'feet', -4, -30), ('wBub2', 'feet', 8, -22), ('wBub1', 'feet', -6, -26)],
                 4: [('wEngulfH', 'feet', -2, -13, {'behind': True, 'alpha': {'a': 200, 'I': 200, 'A': 210, 'W': 230}}), ('wEngulfH', 'feet', -2, -13, {'onFig': True, 'alpha': {'a': 130, 'I': 140, 'A': 150, 'W': 210}}), ('wBub3', 'feet', 6, -24), ('wBub1', 'feet', -8, -20), ('wDropsL', 'feet', -6, -32)],
                 5: [('wEngulfLow', 'feet', -2, -12, {'behind': True}), ('wEngulfLow', 'feet', -2, -12, {'onFig': True, 'alpha': {'a': 140, 'I': 150, 'A': 160, 'W': 200}}), ('wSplashL', 'feet', 0, -9), ('wWakeL', 'feet', -14, -3)],
                 6: [('wPuddleL', 'feet', 0, -1), ('wWakeL', 'feet', -16, -3, _A(_FADE)), ('wDrops', 'head', 4, 8), ('wSplashS', 'head', 6, 10, _A(_FADE))],
                 7: [('wPuddleL', 'feet', 0, -1), ('wDrops', 'head', 4, 10, _A(_FADE)), ('wSplashS', 'head', 7, 12)],
                 8: [('wPuddleL', 'feet', -1, -1), ('wDrops', 'feet', 2, -10, _A(_FADE))],
                 9: [('wPuddle', 'feet', -3, -1, _A(_FADE))]})),
})

# ---------- Cancer genjutsu v1 (part 12, 2026-11-03): Regression, Pacification ----------
def _ripple(rx, cols='Ia', gap=0):   # a flat ripple ring seen from the side (an ellipse a third as tall as it is wide)
    ry = max(1, round(rx / 3)); w, h = 2 * rx + 1, 2 * ry + 1; rows = [['.'] * w for _ in range(h)]
    for t in range(160):
        a = t / 160 * 2 * math.pi; x, y = round(rx + rx * math.cos(a)), round(ry + ry * math.sin(a))
        if gap and (t // 8) % 2: continue
        rows[y][x] = cols[0] if math.sin(a) < 0 else cols[-1]
    return [''.join(q) for q in rows]
def _bubble(r):   # a soap / water bubble: thin ice ring, light lower rim, white glint top-left, hollow
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for y in range(w):
        for x in range(w):
            d = math.hypot(x - r, y - r)
            if r - 0.6 <= d <= r + 0.4: rows[y][x] = 'a' if y > r else 'I'
    if r > 1: rows[r - max(1, r // 2)][r - max(1, r // 2)] = 'W'
    return [''.join(q) for q in rows]
NPAT.update({'eyeW': ['.a.', 'aIa', '.a.'], 'eyeWF': ['..a..', '.aIa.', 'aIWIa', '.aIa.', '..a..'],
             'wRip3': _ripple(3), 'wRip5': _ripple(5), 'wRip7': _ripple(7, 'aA'), 'wRip9': _ripple(9, 'aA', gap=1), 'wRip12': _ripple(12, 'aA', gap=1),
             'wgw1': _arc(4, 2, 'Ia', gap=2), 'wgw2': _arc(6, 3, 'Ia', gap=2), 'wgw3': _arc(8, 4, 'aA', gap=2),
             'wBub1': _bubble(1), 'wBub2': _bubble(2), 'wBub3': _bubble(3),
             **{'wLull%d' % p: _sine(20, 2, 8, p * 2, cols='WIa') for p in range(4)}, **{'wLullS%d' % p: _sine(10, 1, 6, p * 2, cols='Ia') for p in range(4)}})
def _bigWave(h, seed=0):   # Tsunami v2 zone: the giant wave the testbed rolls across the AoE (front = right): a sloped deep back with a dark edge, a tall face shaded in bands (white foam edge, ice, light water, deep water), vertical streaks running down the face, a thick hollow curling lip full of foam, and spray blown off its crest
    import random
    rnd = random.Random(seed); w = round(h * 0.8) + 2; r = round(h * 0.2); W_ = w + r + 4
    rows = [['.'] * W_ for _ in range(h)]
    for y in range(h):
        s = 1 - y / (h - 1); x1 = round((w - 1) * (0.62 + 0.38 * s ** 1.4)); x0 = round((w - 1) * (0.62 * s ** 1.3))
        for x in range(x0, x1 + 1):
            e = x1 - x; b = x - x0
            ch = 'W' if e == 0 else 'I' if e < 3 else 'a' if e < 9 + round(6 * s) else 'A'
            if ch in 'aA' and (x * 7 + rnd.randrange(3)) % 11 == 0: ch = {'a': 'I', 'A': 'a'}[ch]   # streaks running down the face
            if b < 3: ch = 'n'
            elif b < 6 and ch == 'A' and (x + y) % 2: ch = 'n'
            rows[y][x] = ch
    cx, cy = w - 1, r + 2
    for y in range(0, cy + 1):   # the hollow under the lip: shadowed water between the face and the lip
        for x in range(cx - r // 2, cx + r):
            if 0 <= x < W_ and math.hypot(x - cx, y - cy) < r - 1 and rows[y][x] == '.': rows[y][x] = 'A' if math.hypot(x - cx, y - cy) > r * 0.45 else 'n'
    for t in range(400):   # the lip: from the crest over the top and forward, hooking down in front, tapering to a foamy tip
        u = t / 399; th = math.pi / 2 - u * (math.pi / 2 + math.pi / 3); th_ = max(2, round(r * 0.55 * (1 - 0.7 * u)))
        for dd in range(th_):
            rr = r - dd; x, y = round(cx - r * 0.25 * (1 - u) + rr * math.cos(th)), round(cy - rr * math.sin(th))
            if 0 <= x < W_ and 0 <= y < h:
                rows[y][x] = 'W' if dd == 0 or (dd < 3 and rnd.random() < 0.5) else 'I' if dd < 3 else 'a' if dd < th_ * 0.7 else 'A'
    for _ in range(h * 2):   # spray blown back off the crest and the lip
        a = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05); d = rnd.uniform(r * 0.9, r * 1.6)
        x, y = round(cx + d * math.cos(a)), round(cy + d * math.sin(a) * 0.6)
        if 0 <= x < W_ and 0 <= y < h and rows[y][x] == '.': rows[y][x] = rnd.choice('WWI')
    return [''.join(q) for q in rows]
def _flash(r, seed=0):   # Tsunami v2: a white burst of spray: ice heart, white rays of spray every 30 degrees, drops at their tips
    import random
    rnd = random.Random(seed); w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for y in range(w):
        for x in range(w):
            if math.hypot(x - r, y - r) <= r * 0.35: rows[y][x] = 'W' if math.hypot(x - r, y - r) <= r * 0.2 else 'I'
    for k in range(12):
        a = k * math.pi / 6 + rnd.uniform(-0.15, 0.15); L = r * rnd.uniform(0.7, 1.0)
        for t in range(int(L * 2)):
            d = t / 2; x, y = round(r + d * math.cos(a)), round(r + d * math.sin(a))
            if 0 <= x < w and 0 <= y < w and rows[y][x] == '.': rows[y][x] = 'W' if d < L * 0.6 else 'I' if d < L * 0.85 else 'a'
    return [''.join(q) for q in rows]
NPAT.update({**{'wSpoutF%d' % p: _helix(15, 40, p, turns=2.4) for p in range(4)}, **{'wSpoutB%d' % p: _helix(15, 40, p, front=False, turns=2.4) for p in range(4)},
             'wJetUp': [''.join(r) for r in zip(*_jet(18, 11, h=7))][::-1], 'wFlash': _flash(9, 3), 'wPuddleL': _sq(NPAT['wPuddle'], 2.4, 1.5),
             'wTsunamiBig': _bigWave(112, 4), 'wEngulfH': _engulf(58, 30, 9)})
_TODDLE_N, _TODDLE_F = band(-55, -70, fistKind='palm'), band(-45, -60, fistKind='palm')   # arms held out stiff and low in front, hands splayed, like a toddler
CLIPS.update({
 'regression': ('Regression', 6,
  'Regression (Cancer genjutsu, debuff: the caster forces the foe\'s mind to regress to that of a small child, before fine motor skills develop; Slow 2 rounds, INT save DC 12; range ~12 m): from the guard the fighter lifts the near hand palm up before its chest and its eyes kindle water blue; a single drop of water falls into the palm and spreads out in ripples, ring after ring, like time running backward; then it pushes the open palm out at the target and the ripples go out as dashed waves of water-blue thought; it settles back into the guard (the target plays regressed with the genjutsu mark in water colours).', [
     g(),
     g(an=band(-60, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-65, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-65, -150, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-65, -150, fistKind='palm'), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +1 pushing the palm out, -1 back',
       extra={'targetState': {'rule': 'Regression: from the active frame (5) the target plays regressed: frames 0-3 once (its guard melts away and it sinks into a toddler\'s stance), then frames 4-11 on loop until the Slow ends, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.water) is drawn over it throughout', 'state': 'regressed', 'loopFrom': 4, 'element': 'water', 'mark': 'genjutsuAfflicted'}},
       anchored={1: [('eyeW', 'eye', 0, 0), ('wOrb2', 'hand', 0, -12)],
                 2: [('eyeWF', 'eye', 0, 0), ('wOrb2', 'hand', 0, -5)],
                 3: [('eyeWF', 'eye', 0, 0), ('wSplashS', 'hand', 0, -4), ('wRip3', 'hand', 0, 0)],
                 4: [('eyeWF', 'eye', 0, 0), ('wRip5', 'hand', 0, 0), ('wRip3', 'hand', 0, 0, _A(_FADE)), ('wDrops', 'hand', 0, -6, _A(_FADE))],
                 5: [('eyeWF', 'eye', 0, 0), ('wRip7', 'hand', 2, 0, _A(_FADE)), ('wgw1', 'eye', 6, 0)],
                 6: [('eyeWF', 'eye', 0, 0), ('wgw2', 'eye', 11, 0), ('wgw1', 'eye', 6, 0)],
                 7: [('eyeW', 'eye', 0, 0), ('wgw3', 'eye', 16, 0), ('wgw2', 'eye', 11, 0)],
                 8: [('wgw3', 'eye', 20, 1, _A(_FADE))]})),
 'regressed': ('Regressed', 0,
  'Regressed (target state of Regression, Slow 2 rounds): the ripples wash over the fighter and it blinks, its guard melting away: its fists open, its arms drop and lift out stiffly in front of it, fingers splayed, and it sinks into a wide, knock-kneed toddler\'s stance, a soft ripple spreading round its feet; then (looping while the Slow lasts) it toddles clumsily on the spot, rocking side to side and tipping forward and back, its hands clumsily grabbing at nothing and opening again, almost falling and catching itself, while bubbles float up round its head.', [
     g(an=band(-50, -130), af=band(-45, -120), bob=(1, 1, 1), lean=(-1, -2), root=(-1, 0)),
     g(an=band(-45, -110, fistKind='palm'), af=band(-40, -105, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-50, -85, fistKind='palm'), af=band(-42, -75, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1), root=(1, 0), **LOW),
     g(an=_TODDLE_N, af=_TODDLE_F, bob=(3, 3, 3), lean=(1, 2), **LOW),
     g(an=_TODDLE_N, af=_TODDLE_F, bob=(3, 3, 3), lean=(2, 5), root=(1, 0), **LOW),
     g(an=band(-60, -75), af=_TODDLE_F, bob=(3, 3, 4), lean=(2, 6), **LOW),
     g(an=_TODDLE_N, af=_TODDLE_F, bob=(3, 3, 3), lean=(1, 3), root=(-1, 0), **LOW),
     g(an=_TODDLE_N, af=_TODDLE_F, bob=(2, 2, 3), lean=(-1, -2), root=(-1, 0), **LOW),
     g(an=_TODDLE_N, af=band(-50, -65), bob=(2, 2, 3), lean=(-2, -5), **LOW),
     g(an=band(-75, -95, fistKind='palm'), af=band(-65, -90, fistKind='palm'), bob=(3, 3, 3), lean=(-2, -6), root=(-1, 0), **LOW),
     g(an=_TODDLE_N, af=_TODDLE_F, bob=(3, 3, 3), lean=(0, 0), root=(1, 0), **LOW),
     g(an=_TODDLE_N, af=_TODDLE_F, bob=(3, 3, 3), lean=(1, 2), root=(1, 0), **LOW)],
  ['squint', 'closed', 'squint', None, None, 'squint', None, None, 'squint', 'strain', None, None],
  None,
  dict(fps=8, rm='E: -1 hit, +1 sinking in (net 0); loop +1 -1 -1 -1 +1 +1 rocking (net 0)', extra={'loop': True, 'loopFrom': 4},
       anchored={0: [('wgw2', 'head', 6, 8), ('wDrops', 'head', 4, 4, _A(_FADE))],
                 1: [('wgw1', 'head', 2, 8, _A(_FADE)), ('wRip5', 'feet', 0, -1)],
                 2: [('wRip9', 'feet', 0, -2, _A(_FADE)), ('wBub2', 'head', 14, 16)],
                 3: [('wRip12', 'feet', 0, -2, _A(_FADE)), ('wBub2', 'head', 14, 12), ('wBub1', 'head', -13, 17)],
                 4: [('wBub2', 'head', 14, 8), ('wBub1', 'head', -13, 14), ('wBub3', 'head', 12, 6, _A(_FADE))],
                 5: [('wBub1', 'head', -14, 11), ('wBub3', 'head', 12, 2, _A(_FADE)), ('wBub2', 'head', 14, 16)],
                 6: [('wBub1', 'head', -14, 8, _A(_FADE)), ('wBub2', 'head', 14, 12), ('wRip5', 'feet', 0, -1, _A(_FADE))],
                 7: [('wBub2', 'head', 14, 8), ('wBub1', 'head', -13, 17), ('wRip7', 'feet', 0, -1, _A(_FADE))],
                 8: [('wBub2', 'head', 14, 4, _A(_FADE)), ('wBub1', 'head', -13, 13), ('wBub3', 'head', -12, 16)],
                 9: [('wBub1', 'head', -13, 9), ('wBub3', 'head', -12, 12), ('wDrops', 'hand', 0, 2, _A(_FADE))],
                 10: [('wBub1', 'head', -13, 5, _A(_FADE)), ('wBub3', 'head', -12, 8), ('wBub2', 'head', 14, 18)],
                 11: [('wBub3', 'head', -12, 4, _A(_FADE)), ('wBub2', 'head', 14, 14)]})),
 'pacification': ('Pacification', 6,
  'Pacification (Cancer genjutsu, debuff: a soothing lull that makes the foe drop its weapon; Disarm 2 rounds, STR save DC 13; range ~12 m): from the guard the fighter closes its eyes and lowers both open palms in front of it, then presses them slowly down, calming, as if settling still water, a ripple spreading at its feet; its eyes open glowing water blue and it lifts the palms and eases them out toward the target, and a soft lullaby of water flows off them in gentle waving lines that drift on toward the target; it settles back into the guard (the target plays pacified with the genjutsu mark in water colours).', [
     g(),
     g(an=band(-55, -75, fistKind='palm'), af=band(-50, -70, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-45, -60, fistKind='palm'), af=band(-40, -55, fistKind='palm'), bob=(2, 2, 2), lean=(0, 1)),
     g(an=band(-40, -55, fistKind='palm'), af=band(-35, -50, fistKind='palm'), bob=(2, 2, 3), lean=(0, 1)),
     g(an=band(-70, -85, fistKind='palm'), af=band(-62, -80, fistKind='palm'), bob=(1, 1, 1), lean=(1, 2), root=(1, 0)),
     g(an=band(-78, -88, fistKind='palm'), af=band(-70, -85, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-78, -88, fistKind='palm'), af=band(-70, -85, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)),
     g(an=band(-75, -90, fistKind='palm'), af=band(-68, -88, fistKind='palm'), bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-55, -115), af=band(-45, -110), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g()],
  [None, 'closed', 'closed', 'closed', 'squint', None, None, None, None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +1 easing the palms out, -1 back',
       extra={'targetState': {'rule': 'Pacification: from the active frame (5) the target plays pacified: frames 0-3 once (the lull reaches it, its eyes droop, its hands open and its weapon slips from them), then frames 4-11 on loop until the Disarm ends, then its idle; the testbed drops the target\'s held weapon at its feet on frame 2 (Disarm) and returns it when the Disarm ends; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.water) is drawn over it throughout', 'state': 'pacified', 'loopFrom': 4, 'element': 'water', 'mark': 'genjutsuAfflicted', 'dropFrame': 2}},
       anchored={1: [('wRip5', 'feet', 4, -1, _A(_FADE))],
                 2: [('wRip9', 'feet', 4, -2, _A(_FADE)), ('wDrops', 'hand', 0, 4, _A(_FADE))],
                 3: [('wRip12', 'feet', 4, -2, _A(_FADE))],
                 4: [('eyeW', 'eye', 0, 0), ('wLullS0', 'hand', 0, -6)],
                 5: [('eyeWF', 'eye', 0, 0), ('wLull1', 'hand', -2, -7), ('wLullS1', 'hand', 0, 5, _A(_FADE))],
                 6: [('eyeWF', 'eye', 0, 0), ('wLull2', 'hand', -1, -8), ('wLullS2', 'hand', 1, 5), ('wBub1', 'hand', 2, -14)],
                 7: [('eyeW', 'eye', 0, 0), ('wLull3', 'hand', 0, -9, _A(_FADE)), ('wLullS3', 'hand', 2, 5, _A(_FADE)), ('wBub2', 'hand', 3, -17, _A(_FADE))],
                 8: [('wBub1', 'head', 10, -2, _A(_FADE))]})),
 'pacified': ('Pacified', 0,
  'Pacified (target state of Pacification, Disarm 2 rounds): the waving lines of the lullaby wash over the fighter; its eyelids droop, its guard sags, its fists open and its arms fall slack at its sides (the testbed drops its weapon at its feet), its head nodding forward; then (looping while the Disarm lasts) it sways gently on its feet, drowsy and calm, eyes half shut, head nodding and lifting, with soft lull lines drifting round its head, bubbles floating up and slow ripples spreading round its feet.', [
     g(an=band(-55, -125), af=band(-48, -118), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-40, -90, fistKind='palm'), af=band(-35, -85, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-15, -40, fistKind='palm'), af=band(-10, -35, fistKind='palm'), bob=(1, 1, 2), lean=(1, 2)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 4)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 4)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 5), root=(1, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 3), lean=(2, 6)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 4)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(1, 1, 2), lean=(0, 1)),
     g(an=AR_HANG_N, af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 3))],
  ['squint', 'squint', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'squint', 'squint', 'closed', 'closed'],
  None,
  dict(fps=6, rm='E: loop +1 swaying in, -1 back (net 0)', extra={'loop': True, 'loopFrom': 4},
       anchored={0: [('wLull1', 'head', 8, 10), ('wLullS0', 'head', 6, 16)],
                 1: [('wLull2', 'head', 2, 8, _A(_FADE)), ('wLullS1', 'head', 0, 16, _A(_FADE))],
                 2: [('wRip5', 'feet', 0, -1), ('wBub1', 'head', 11, 12)],
                 3: [('wRip9', 'feet', 0, -2, _A(_FADE)), ('wBub2', 'head', 12, 8), ('wLullS2', 'head', -12, 6, _A(_FADE))],
                 **{k_: [('wLullS%d' % (k_ % 4), 'head', -12, 6 - (k_ % 2), _A(_FADE)), ('wLullS%d' % ((k_ + 2) % 4), 'head', 12, 14 + (k_ % 2), _A(_FADE)),
                         ('wBub%d' % (1 + k_ % 2), 'head', 12 if k_ % 2 else -12, 12 - 3 * (k_ % 4)),
                         ('wRip%d' % (5, 7, 9, 12)[k_ % 4], 'feet', 0, -2, _A(_FADE))] for k_ in range(4, 12)}})),
})

# ---------- Tidal Slam v2 (part 13, 2026-11-03; Christopher 22:31: summon a wave, ride on top of it, slam the target with an elbow drop) ----------
def _rideWave(h, phase=0, w=60, p0=16, pk=46, F=12):   # the wave the fighter rides, front = right: a back slope rising to a broad rounded top the feet stand on (p0..pk), a lip curling forward over a hollow face, a churning foam skirt at its foot; h = rows above the floor of the top (the soles' row + 1)
    import random
    rnd = random.Random(70 + phase); H = h + 2; rows = [['.'] * w for _ in range(H)]
    def top(x):
        if x < p0: return h * (0.15 + 0.85 * (x / p0) ** 1.4)
        if x <= pk: return h + (1 if p0 + 4 < x < pk - 4 else 0)
        t = (x - pk) / F
        return h * (1 - 0.6 * t * t) if t <= 1 else -1
    for x in range(w):
        ht = top(x)
        if ht < 0: continue
        for yh in range(int(round(ht))):
            face = pk + 1 + F * 0.8 * (yh / h) ** 1.5
            if x > pk and x > face and yh < ht - 3: continue   # hollow under the curling lip
            e = ht - yh; y = H - 1 - yh
            if e < 1.2: ch = 'W' if x > p0 + 2 else 'I'
            elif e < 2.5: ch = 'I'
            elif x > pk - 2 and x > face - 2: ch = 'a'   # the light face inside the curl
            elif e < 4.5: ch = 'a'
            elif yh < 2 and x < pk: ch = 'n'
            else: ch = 'A'
            if ch == 'A' and (x - 2 * yh + 3 * phase) % 7 == 0: ch = 'a'   # streaks running up and back over the wave's body
            if ch == 'a' and e > 3 and (x + yh + 2 * phase) % 11 == 0: ch = 'I'   # glints
            rows[y][x] = ch
    for x in range(p0, pk + 2):   # foam boiling up round the rider's feet along the top
        if (x + phase) % 3: rows[H - 2 - h][x] = 'W' if (x + phase) % 3 == 1 else 'I'
    for x in range(pk + F - 6, min(w, pk + F + 2)):   # spray falling off the lip
        for _ in range(2):
            y = rnd.randint(H - h + 2, H - 2)
            if rows[y][x] == '.': rows[y][x] = rnd.choice('IaW')
    for x in range(pk - 2, w):   # the foam skirt where the curl meets the floor
        if rnd.random() < 0.75: rows[H - 1][x] = rnd.choice('WIW')
        if rnd.random() < 0.45 and rows[H - 2][x] == '.': rows[H - 2][x] = rnd.choice('WIa')
    for x in range(0, p0):   # spray streaming off the back
        if rnd.random() < 0.35:
            y = H - 1 - int(top(x)) - rnd.randint(1, 2)
            if 0 <= y < H: rows[y][x] = rnd.choice('Ia')
    return [''.join(q) for q in rows]
NPAT['wCrest40T'] = [q if i < 14 else '.' * len(q) for i, q in enumerate(NPAT['wCrest40'])]   # Tidal Slam v2.1: the crest's curling top only
NPAT['wCrest52TS'] = [q if i < 18 else '.' * len(q) for i, q in enumerate(NPAT['wCrest52'])]   # v2.2: the same for the tall crest that carries the elbow down
NPAT.update({**{'wRide%d_%d' % (h, p): _rideWave(h, p) for h in (4, 7, 9, 10, 11) for p in range(4)},
             'wRideBreak': _rideWave(8, 1, p0=22, pk=48, F=10), 'wRideCrash': _rideWave(5, 2, p0=26, pk=50, F=10)})
U.POSES += [leg('tsl-surf-lead', (33, 46), (40, 51), 42), kleg('tsl-surf-rear', (31, 46), (25, 51), (21, 56), 'toe30k'),   # Tidal Slam v2: a wide, knees-bent surfer's stance on the wave
            kleg('tsl-tuck-lead', (33, 44), (40, 47), (37, 53), 'toe30k'), kleg('tsl-tuck-rear', (31, 44), (24, 47), (19, 51), 'toe30k')]   # the leap off the wave: knees tucked, feet trailing
_LIFT = lambda dy: (0, 0, -dy, False)   # bodyRotation with no turn: the whole fighter lifted dy px (all layers stay registered)
_SURF = dict(ln='tsl-surf-rear', lf='tsl-surf-lead')
_TUCK = dict(ln='tsl-tuck-rear', lf='tsl-tuck-lead')
_EL_COCK, _EL_DIVE = band(-178, 80), band(-45, 170)   # elbow drop: arm raised, forearm folded behind the head; then the point of the elbow driven down and forward, forearm folded back up across the chest (the approved Mount Elbow Strike arm)
CLIPS['tidalSlam'] = ('Tidal Slam', 10,
  'Tidal Slam v2 (Cancer taijutsu gap closer, Physical 16, Melee (Reach +4m), Gap Closer: the fighter gathers a running start and gains enough momentum to slam into its opponent; Christopher 2026-11-03 22:31: the user summons a wave and rides on top of it before slamming into the target, the slam an elbow drop): from the guard the fighter presses both palms down to the water pooling round its feet, then sweeps them up and a wave swells up behind it; it crouches and springs, and the wave surges up under its feet and carries it forward: it rides on top of the wave in a wide surfer\'s stance, arms out for balance, foam boiling round its feet, the wave rolling on toward the target with a lip curling over its hollow face; at the top it rears back and raises the near arm, forearm folded behind the head, leaps off the crest and drops onto the target elbow first, the wave breaking over the impact in a great crown splash and a jet of water bursting forward; it lands crouched and rises back into the guard in a spreading puddle (the target plays tidalSlammed). The fighter is lifted whole by the bodyRotation dy (no turn) while it rides.', [
     g(),
     g(an=band(-25, -40, fistKind='palm'), af=band(-20, -35, fistKind='palm'), bob=(3, 3, 3), lean=(1, 3), **LOW),
     g(an=band(-120, -140, fistKind='palm'), af=band(-110, -135, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(40, 60), af=band(30, 50), bob=(6, 6, 6), lean=(2, 8), root=(1, 0), **BRACE),
     g(an=band(-75, -70, fistKind='palm'), af=band(70, 85, fistKind='palm'), bob=(3, 3, 3), lean=(1, 5), root=(4, 0), rot=_LIFT(4), **_TUCK),
     g(an=band(-70, -60, fistKind='palm'), af=band(65, 85, fistKind='palm'), bob=(5, 5, 5), lean=(1, 4), root=(6, 0), rot=_LIFT(9), **_SURF),
     g(an=band(-75, -65, fistKind='palm'), af=band(60, 80, fistKind='palm'), bob=(5, 5, 6), lean=(1, 5), root=(7, 0), rot=_LIFT(10), **_SURF),
     g(an=band(-70, -60, fistKind='palm'), af=band(65, 85, fistKind='palm'), bob=(5, 5, 5), lean=(1, 4), root=(7, 0), rot=_LIFT(11), **_SURF),
     g(an=_EL_COCK, af=band(-70, -80, fistKind='palm'), bob=(6, 6, 6), lean=(-1, -3), root=(6, 0), rot=_LIFT(10), **_SURF),
     g(an=_EL_COCK, af=band(-10, -120), bob=(3, 3, 3), lean=(3, 12), root=(5, 0), rot=_LIFT(10), **_TUCK),
     g(an=_EL_DIVE, af=band(-10, -120), bob=(2, 2, 2), lean=(4, 14), root=(4, 0), rot=_LIFT(7), **_TUCK),
     g(an=band(-30, 168), af=band(-10, -115), bob=(7, 7, 7), lean=(3, 13), root=(2, 0), **LOW),
     g(an=band(-40, -110), af=band(-30, -100), bob=(7, 7, 7), lean=(2, 8), root=(-2, 0), **LOW),
     g(an=band(-50, -120), af=band(-40, -115), bob=(3, 3, 3), lean=(1, 3)),
     g()],
  [None, 'squint', 'strain', 'strain', 'roar', 'strain', 'strain', 'strain', 'roar', 'roar', 'roar', 'roar', 'strain', 'squint', None],
  None,
  dict(fps=12, hitbox=[44, 12, 14, 16], damage='medium', rm='E: +1 into the crouch, +4 +6 +7 +7 riding the wave, +6 at the crest, +5 +4 +2 the leap and the flying elbow drop onto the target, -2 landing back off it; 40 px in all (travel)',
       blur={9: 7, 10: 6, 11: 4}, trail=WATER_TRAIL,
       extra={'travel': {'rule': 'Tidal Slam is a gap closer: the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40},
              'targetState': {'rule': 'Tidal Slam v2: on the hit (frame 10, the elbow lands on the shoulder) the target plays tidalSlammed once, then its idle', 'state': 'tidalSlammed', 'loopFrom': None, 'element': 'water'}},
       anchored={1: [('wPuddle', 'feet', 0, -1), ('wRip9', 'feet', 0, -2, _A(_FADE)), ('wDrops', 'feet', 0, -6, _A(_FADE))],
                 2: [('wPuddleL', 'feet', 0, -1), ('wCrest10', 'feet', -10, -5, {'behind': True, 'alpha': _CR}), ('wDrops', 'hand', 0, -4, _A(_FADE)), ('wSplashS', 'feet', 6, -4)],
                 3: [('wRide4_0', 'feet', -2, -2), ('wCrest20', 'feet', -11, -10, {'behind': True, 'alpha': _CR}), ('wDrops', 'feet', -14, -18, _A(_FADE))],
                 4: [('wCrest40', 'feet', -12, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wRide7_1', 'feet', -2, -4), ('wSplashS', 'feet', 0, -12), ('wDrops', 'feet', -16, -24, _A(_FADE))],
                 5: [('wCrest40', 'feet', -16, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wRide9_2', 'feet', -2, -5), ('wDropsL', 'feet', -22, -18, _A(_FADE))],
                 6: [('wCrest40', 'feet', -17, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wRide10_3', 'feet', -2, -5), ('wDrops', 'feet', -24, -20, _A(_FADE))],
                 7: [('wCrest52', 'feet', -16, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wRide11_0', 'feet', -2, -6), ('wFoam', 'feet', -12, -40, _A(_FADE)), ('wDropsL', 'feet', -22, -20, _A(_FADE))],
                 8: [('wCrest52', 'feet', -13, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wRide10_1', 'feet', -2, -5), ('wFoam', 'feet', -8, -38, _A(_FADE)), ('wSplashS', 'feet', 20, -12, _A(_FADE))],
                 9: [('wCrest52', 'feet', -10, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wRideBreak', 'feet', -2, -4), ('wDrops', 'feet', -18, -14, _A(_FADE))],
                 10: [('wCrest52', 'feet', -6, 0, {'behind': True, 'alpha': _CR, 'bottom': 63}), ('wCrest52TS', 'feet', -6, 0, {'alpha': {'n': 120, 'A': 140, 'a': 160, 'I': 190, 'W': 230}, 'bottom': 63}), ('wRideCrash', 'feet', -4, -3), ('wSplash', 'hand', 3, 2), ('wDrops', 'hand', -2, -3, _A(_FADE))],
                 11: [('wCrest20', 'feet', 2, 0, {'behind': True, 'alpha': _FADE, 'bottom': 62}), ('wSplashXL', 'hand', 0, 4), ('wJetL', 'hand', 12, 10), ('wDropsL', 'hand', 2, -6, _A(_FADE)), ('wPuddleL', 'feet', 8, -1)],
                 12: [('wSplashLD', 'feet', 12, -10, _A(_FADE)), ('wPuddleL', 'feet', 6, -1), ('wDrops', 'head', 8, 4, _A(_FADE))],
                 13: [('wPuddle', 'feet', 4, -1, _A(_FADE))]}))
CLIPS['tidalSlammed'] = ('Tidal Slammed', 0,
  'Tidal Slammed (target state of Tidal Slam v2, plays once on the hit): the caster\'s elbow crashes down on its head and shoulder and the wave breaks over it: it is crushed straight down, buckling to one knee, head bowed and forearms up over the head, water pouring over it and splashing up round it; it shakes the water off and rises back into the guard.', [
     g(an=band(-140, -170), af=band(-130, -165), bob=(3, 3, 4), lean=(-1, -3)),
     g(an=band(-130, -165), af=band(-120, -160), bob=(9, 10, 10), lean=(2, 8), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-110, -160), af=band(-100, -155), bob=(10, 10, 10), lean=(3, 11), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-40, -110), af=band(-30, -100), bob=(9, 10, 10), lean=(3, 12), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-40, -110), af=band(-30, -100), bob=(9, 10, 10), lean=(2, 9), ln='ss-kneel-rear', lf='ss-kneel-lead'),
     g(an=band(-45, -115), af=band(-35, -110), bob=(4, 4, 4), lean=(1, 4), **LOW),
     g(an=band(-50, -120), af=band(-40, -115), bob=(2, 2, 2), lean=(0, 2)),
     g()],
  ['pain', 'pain', 'closed', 'strain', 'squint', 'squint', None, None],
  None,
  dict(fps=10, rm='in place',
       anchored={0: [('wSplashL', 'head', 2, -2), ('wDrops', 'head', 4, -6)],
                 1: [('wSplashXL', 'feet', 0, -14), ('wFoamL', 'head', 0, 2, _A(_FADE)), ('wDropsL', 'head', 0, -4), ('wPuddleL', 'feet', 0, -1)],
                 2: [('wSplashLD', 'feet', 0, -10), ('wPuddleL', 'feet', 0, -1), ('wDropsL', 'head', 2, 0, _A(_FADE))],
                 3: [('wPuddleL', 'feet', 0, -1), ('wDrops', 'head', 2, 6), ('wSplashS', 'feet', -8, -4)],
                 4: [('wPuddleL', 'feet', 0, -1), ('wDrops', 'head', 0, 8, _A(_FADE))],
                 5: [('wPuddle', 'feet', 0, -1, _A(_FADE))]}))

def _bigWave3(h, phase=0, seed=4):   # Tsunami v3 zone (Christopher 2026-11-03 22:35: make the wave look better): a breaking wave, front = right: a rounded back rising to the crest with a deep edge, a thick lip pitching forward and down over a shadowed barrel, a concave face shading from deep water at the foot to ice and white under the lip, streaks and foam sliding down it with phase (0-3), whitewater boiling ahead of its foot, spray blown back off the crest
    import random
    from PIL import Image, ImageDraw
    rnd = random.Random(seed * 10 + phase); Wd = round(h * 0.95); W_ = Wd + 14; H = h
    def bez(p0, p1, p2, n=60): return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]
    T, P, F, B = (0.6 * Wd, 0.03 * H), (0.99 * Wd, 0.42 * H), (0.72 * Wd, 0.33 * H), (0.93 * Wd, H - 1)
    back = [(0.6 * Wd * s, (H - 1) - (H - 1 - 0.03 * H) * (1 - (1 - s) ** 2.4)) for s in (i / 60 for i in range(61))]
    poly = back + bez(T, (0.93 * Wd, -0.04 * H), P) + bez(P, (0.88 * Wd, 0.2 * H), F) + bez(F, (0.66 * Wd, 0.78 * H), B) + [(0, H - 1)]
    m = Image.new('L', (W_, H)); ImageDraw.Draw(m).polygon(poly, fill=1); M = m.load()
    rows = [['.'] * W_ for _ in range(H)]
    ins = lambda x, y: 0 <= x < W_ and 0 <= y < H and M[x, y]
    for y in range(H):
        for x in range(W_):
            if not M[x, y]: continue
            v = (H - 1 - y) / (H - 1)
            e = next(d for d in range(W_) if not ins(x + d, y)); b = next(d for d in range(W_) if not ins(x - d, y)); t = next(d for d in range(H) if not ins(x, y - d))
            d = min(e, t + 1); dz = (x + y) % 2
            if d <= 1: c = 'W' if v > 0.22 else 'I'
            elif d <= 3 + dz: c = 'I' if v > 0.3 else 'a'
            elif d <= 4 + round(10 * v) + dz and v > 0.5: c = 'I' if d <= 5 + dz else 'a'
            elif d <= 6 + round(16 * v) + 2 * dz: c = 'a' if v > 0.18 else 'A'
            else: c = 'A'
            if b <= 2: c = 'n'
            elif b <= 5 and c == 'A' and dz: c = 'n'
            if c in 'aA' and x % 7 == (y // 9 + 3 * (x // 7) + phase) % 7 and (y + 3 * phase) % 6 < 4: c = 'I' if c == 'a' else 'a'   # streaks sliding down
            rows[y][x] = c
    for x in range(round(F[0]), round(P[0])):   # the barrel: shadowed water seen inside the curl, under the lip, bounded by the curtain falling from the tip back to the face
        top_ = next((y for y in range(H) if M[x, y]), None)
        if top_ is None: continue
        y = top_
        while y < H and M[x, y]: y += 1
        ylim = P[1] + (P[0] - x) * 0.9   # the curtain line slants from the tip down and back to the face
        while y < min(H, ylim) and not M[x, y]:
            rows[y][x] = 'A' if (x + y) % 4 else 'a'; y += 1
    for k in range(0, 20):   # the curtain falling from the lip's tip into the barrel
        u = k / 19; px, py = bez(P, (0.88 * Wd, 0.2 * H), F, 19)[k]
        for d in range(1, 3 + round((1 - u) * 6)):
            y = round(py + d + (phase % 2)); x = round(px)
            if 0 <= y < H and 0 <= x < W_ and rows[y][x] == '.' and (d + k + phase) % 3: rows[y][x] = 'I' if d < 3 else 'a'
    for _ in range(h // 2):   # foam pouring off the lip down the face
        y = round(0.36 * H + rnd.random() ** 1.6 * 0.4 * H + (phase * 3) % 6)
        if y >= H: continue
        xs = [x for x in range(W_) if M[x, y]]
        if xs: x = max(xs) - rnd.randint(0, 3); rows[y][x] = 'W' if rows[y][x] != '.' else rows[y][x]
    base = round(B[0])
    for _ in range(h * 2):   # whitewater boiling ahead of the foot
        x = base - 12 + int(rnd.random() ** 0.9 * (W_ - base + 10)); hy = int(rnd.random() ** 2 * h * 0.18); y = H - 1 - hy
        if 0 <= x < W_ and 0 <= y < H: rows[y][x] = rnd.choice('WWIIa') if hy > 1 else rnd.choice('WIaa')
    for _ in range(h):   # spray blown back off the crest
        a = rnd.uniform(0, 1); x = round(T[0] - a * 0.35 * Wd - 2 * phase + rnd.randint(-2, 2)); y = round(T[1] + a * 0.22 * H - rnd.random() * 4 * (1 - a) + 2)
        if 0 <= x < W_ and 0 <= y < H and rows[y][x] == '.': rows[y][x] = rnd.choice('WWI')
    return [''.join(q) for q in rows]
def _bigWave4(h, phase=0, seed=4):   # Tsunami v4 zone (Christopher 2026-11-04: keep the large wave but make it look better): the v3 breaking wave reshaded: flowing current lines that follow the wave's curve and slide with phase (0-3) instead of tick streaks, a lace of foam along the crest, foam fingers clawing off the lip's tip, a smooth deep barrel with a thin see-through curtain, a darker foot, a softer back edge
    import random
    from PIL import Image, ImageDraw
    rnd = random.Random(seed * 10 + phase); Wd = round(h * 0.95); W_ = Wd + 18; H = h
    def bez(p0, p1, p2, n=60): return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]
    T, P, F, B = (0.6 * Wd, 0.03 * H), (1.0 * Wd, 0.44 * H), (0.72 * Wd, 0.33 * H), (0.93 * Wd, H - 1)
    LI = (0.88 * Wd, 0.2 * H)   # control point of the lip's underside
    back = [(0.6 * Wd * s, (H - 1) - (H - 1 - 0.03 * H) * (1 - (1 - s) ** 2.4)) for s in (i / 60 for i in range(61))]
    poly = back + bez(T, (0.94 * Wd, -0.04 * H), P) + bez(P, LI, F) + bez(F, (0.66 * Wd, 0.78 * H), B) + [(0, H - 1)]
    m = Image.new('L', (W_, H)); ImageDraw.Draw(m).polygon(poly, fill=1); M = m.load()
    rows = [['.'] * W_ for _ in range(H)]
    ins = lambda x, y: 0 <= x < W_ and 0 <= y < H and M[x, y]
    hsh = lambda x, y: (x * 73856093 ^ y * 19349663) % 97
    for y in range(H):
        for x in range(W_):
            if not M[x, y]: continue
            v = (H - 1 - y) / (H - 1)
            e = next(d for d in range(W_) if not ins(x + d, y)); b = next(d for d in range(W_) if not ins(x - d, y)); t = next(d for d in range(H) if not ins(x, y - d))
            d = min(e, t + 1); dz = (x + y) % 2
            if d <= 1: c = 'W' if v > 0.25 else 'I'
            elif d <= 3 + dz: c = 'I' if v > 0.3 else 'a'
            elif d <= 4 + round(10 * v) + dz and v > 0.5: c = 'I' if d <= 5 + dz else 'a'
            elif d <= 6 + round(16 * v) + 2 * dz: c = 'a' if v > 0.18 else 'A'
            elif e > 8 and v < 0.04 + 0.08 * hsh(x, y) / 97: c = 'n'   # the deep, dark foot of the wave, ragged
            else: c = 'A'
            if b <= 1: c = 'n'
            elif b <= 3 and c == 'A' and dz: c = 'n'
            if c in 'aA' and b > 3:   # current lines: bands parallel to the front edge (face and lip) and to the back, broken, sliding with phase
                if (d - 2 * phase) % 9 == 0 and hsh(x, y) > 22: c = 'I' if c == 'a' else 'a'
                elif x < T[0] and (b + 2 * phase) % 11 == 0 and hsh(x, y) > 30 and v > 0.2: c = 'a'
            if t <= 3 and v > 0.55 and c != 'n':   # a lace of foam along the crest, with holes that drift with phase
                c = 'I' if t == 3 or (t == 2 and (x // 2 + phase) % 3 == 0) else 'W'
            rows[y][x] = c
    for x in range(round(F[0]), round(P[0]) + 1):   # the barrel: deep water inside the curl, darkest against the face, bounded by the curtain from the tip back to the face
        top_ = next((y for y in range(H) if M[x, y]), None)
        if top_ is None: continue
        y = top_
        while y < H and M[x, y]: y += 1
        ylim = P[1] + (P[0] - x) * 0.9
        while y < min(H, ylim) and not M[x, y]:
            q = (x - F[0]) / max(1, P[0] - F[0]); rows[y][x] = 'n' if q < 0.35 or (q < 0.55 and (x + y) % 2) else 'A'; y += 1
    curt = bez(P, LI, F, 24)
    for k, (px, py) in enumerate(curt):   # the curtain: a thin see-through sheet falling from the lip's edge into the barrel
        for dd in range(1, 4 + round((1 - k / 24) * 5)):
            yy = round(py + dd + (phase % 2)); xx = round(px - dd * 0.4)
            if 0 <= yy < H and 0 <= xx < W_ and rows[yy][xx] in '.An' and (dd + k + phase) % 3: rows[yy][xx] = 'I' if dd < 3 else 'a'
    for f in range(4):   # foam fingers clawing forward and down off the lip's tip
        a0 = math.radians(-30 + 22 * f + 6 * (phase % 2)); L = 5 + (f * 3 + phase) % 4
        for s_ in range(L * 2):
            u = s_ / (L * 2); ang = a0 + u * 1.4
            xx, yy = round(P[0] - 1 + u * L * math.cos(a0)), round(P[1] - 2 + u * L * math.sin(ang) + 2 * f * u)
            if 0 <= xx < W_ and 0 <= yy < H: rows[yy][xx] = 'W' if u < 0.7 else 'I'
    for _ in range(14):   # spray thrown off the tip
        xx, yy = round(P[0] + rnd.uniform(0, 10) + phase), round(P[1] + rnd.uniform(-4, 10))
        if 0 <= xx < W_ and 0 <= yy < H and rows[yy][xx] == '.': rows[yy][xx] = rnd.choice('WIa')
    for _ in range(h // 2):   # foam pouring down the face from under the lip
        y = round(0.38 * H + rnd.random() ** 1.6 * 0.4 * H + (phase * 3) % 6)
        if y >= H: continue
        xs = [x for x in range(W_) if M[x, y]]
        if xs: x = max(xs) - rnd.randint(0, 3); rows[y][x] = 'W' if rows[y][x] != '.' else rows[y][x]
    base = round(B[0])
    for _ in range(h * 3):   # whitewater boiling ahead of the foot, in clumps
        cxw = base - 8 + rnd.random() ** 0.9 * (W_ - base + 6); hy0 = rnd.random() ** 2 * h * 0.16
        for _ in range(3):
            x = round(cxw + rnd.uniform(-1.5, 1.5)); y = H - 1 - round(hy0 + rnd.uniform(0, 1.5))
            if 0 <= x < W_ and 0 <= y < H: rows[y][x] = rnd.choice('WWWIa') if y < H - 2 else rnd.choice('WIIa')
    for _ in range(h):   # spray blown back off the crest
        a = rnd.uniform(0, 1); x = round(T[0] - a * 0.35 * Wd - 2 * phase + rnd.randint(-2, 2)); y = round(T[1] + a * 0.22 * H - rnd.random() * 4 * (1 - a) + 2)
        if 0 <= x < W_ and 0 <= y < H and rows[y][x] == '.': rows[y][x] = rnd.choice('WWI')
    return [''.join(q) for q in rows]
NPAT.update({'wTsunamiBig': _bigWave4(112, 0), **{'wTsunamiBig%d' % p: _bigWave4(112, p) for p in range(4)},   # v4 (2026-11-04); _bigWave3 kept for reference
             **{'wSpoutXF%d' % p: _helix(17, 52, p, turns=3.0) for p in range(4)}, **{'wSpoutXB%d' % p: _helix(17, 52, p, front=False, turns=3.0) for p in range(4)}})
# ---------- Tsunami v3 (part 13, 2026-11-03; Christopher 22:35: the fx is getting there, make the wave look better and add charging frames) ----------
# The renderer caps a clip at 16 frames, so the charge is its own clip, tsunamiCharge (16 frames, the shaking hold loops from 13),
# and tsunami is the release (8 frames, the thrust on frame 2). The zone wave is the new breaking wave wTsunamiBig0-3.
_OVER_N, _OVER_F = band(-160, -176, fistKind='palm'), band(-155, -174, fistKind='palm')   # both arms up, palms holding the wave overhead
_PDN_N, _PDN_F = band(-35, -40, fistKind='palm'), band(-30, -45, fistKind='palm')         # palms driven down at the floor
_TS_CR = lambda h, dx, dy: ('wCrest%d' % h, 'feet', dx, dy, {'behind': True, 'alpha': _CR})
CLIPS['tsunamiCharge'] = ('Tsunami Charge', 7,
  'Tsunami Charge v4 (charge-up of the Cancer ninjutsu ultimate Tsunami; Christopher 2026-11-03 22:35: more charging frames; 2026-11-04: extend the swirling water, remove the small wave): from the guard the fighter makes the seal and sinks low, eyes closing; drops of water lift off the floor and ripple rings spread round its feet; a spout of water spirals up round its whole body as its water aura flares wide; it drives both palms down and the floor bursts, jets of water shooting up round it into the spiral; it hauls its arms up and the spout widens and climbs with them into a towering vortex of water whirling round its whole body, spray streaming up off the top; then it holds its arms up inside the vortex, the whole body shaking with the strain (no wave behind it: the giant wave appears only on the release) (frames 13-15 loop while the charge lasts). The testbed then plays tsunami (the release).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 1), **BRACE),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 4), lean=(0, 0), **BRACE),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(4, 4, 5), lean=(0, 1), **BRACE),
     g(an=_PDN_N, af=_PDN_F, bob=(5, 6, 6), lean=(1, 7), **BRACE),
     g(an=_PDN_N, af=_PDN_F, bob=(5, 6, 6), lean=(1, 7), root=(1, 0), **BRACE),
     g(an=_PDN_N, af=_PDN_F, bob=(5, 6, 6), lean=(1, 6), root=(-1, 0), **BRACE),
     g(an=band(-110, -150, fistKind='palm'), af=band(-100, -145, fistKind='palm'), bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-145, -168, fistKind='palm'), af=band(-138, -165, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=_OVER_N, af=_OVER_F, bob=(0, -1, 0), lean=(0, -1)),
     g(an=_OVER_N, af=_OVER_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-162, -176, fistKind='palm'), af=band(-155, -172, fistKind='palm'), bob=(1, 0, 1), lean=(0, -2), root=(1, 0)),
     g(an=band(-158, -174, fistKind='palm'), af=band(-152, -170, fistKind='palm'), bob=(0, -1, 0), lean=(0, -1), root=(-1, 0))],
  [None, 'squint', 'closed', 'closed', 'closed', 'strain', 'roar', 'strain', 'strain', 'strain', 'strain', 'roar', 'strain', 'strain', 'roar', 'strain'],
  [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  dict(fps=10, auraColors=_WAURA, rm='E: +1 -1 shaken by the floor burst, +1 -1 shaking under the wave in the loop (net 0)',
       extra={'loop': True, 'loopFrom': 13, 'charge': {'rule': 'Tsunami v3 (ultimate, charge): when Tsunami is cast the testbed plays tsunamiCharge frames 0-12 once, then frames 13-15 on loop while the charge lasts (at least once), then tsunami (the release) from its frame 0; the wave behind the caster is part of these frames', 'then': 'tsunami'}},
       anchored={0: [('wDrops', 'feet', 0, -4, _A(_FADE))],
                 1: [('wDrops', 'feet', -4, -10, _A(_FADE)), ('wRip5', 'feet', 0, -1), ('wPuddle', 'feet', 0, -1)],
                 2: [('wDrops', 'feet', 5, -14, _A(_FADE)), ('wRip9', 'feet', 0, -2, _A(_FADE)), ('wPuddle', 'feet', 0, -1), ('wDrops', 'feet', -6, -20)],
                 3: [('wRip12', 'feet', 0, -2, _A(_FADE)), ('wPuddleL', 'feet', 0, -1), ('wDropsL', 'feet', 0, -24, _A(_FADE))],
                 4: [('wSpoutB0', 'feet', 0, -18, {'behind': True}), ('wSpoutF0', 'feet', 0, -18, _A(_FADE)), ('wDrops', 'head', -8, 0), ('wPuddleL', 'feet', 0, -1)],
                 5: [('wSpoutB1', 'feet', 0, -22, {'behind': True}), ('wSpoutF1', 'feet', 0, -22, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDrops', 'head', 8, -4), ('wPuddleL', 'feet', 0, -1)],
                 6: [('wSpoutB2', 'feet', 0, -22, {'behind': True}), ('wSpoutF2', 'feet', 0, -22, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', 0, -8, _A(_FADE)), ('wPuddleL', 'feet', 0, -1)],
                 7: [('wSpoutB3', 'feet', 0, -22, {'behind': True}), ('wSpoutF3', 'feet', 0, -22, _A(_FADE)), ('wJetUp', 'feet', -20, -14, {'behind': True}), ('wJetUp', 'feet', 14, -12), ('wSplashL', 'feet', 0, -9), ('wPuddleL', 'feet', 0, -1)],
                 8: [('wSpoutB0', 'feet', 0, -22, {'behind': True}), ('wSpoutF0', 'feet', 0, -22, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wJetUp', 'feet', -22, -18, {'behind': True}), ('wJetUp', 'feet', 16, -16, _A(_FADE)), ('wSplashS', 'feet', 6, -4), ('wPuddleL', 'feet', 0, -1)],
                 9: [('wSpoutB1', 'feet', 0, -22, {'behind': True}), ('wSpoutF1', 'feet', 0, -22, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wJetUp', 'feet', -22, -20, {'behind': True, 'alpha': _FADE}), ('wDropsL', 'feet', -8, -20), ('wPuddleL', 'feet', 0, -1)],
                 10: [('wSpoutB2', 'feet', 0, -22, {'behind': True}), ('wSpoutF2', 'feet', 0, -22, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'feet', 8, -26), ('wPuddleL', 'feet', 0, -1), ('wRip12', 'feet', 0, -2, _A(_FADE))],
                 11: [('wSpoutXB3', 'feet', 0, -26, {'behind': True}), ('wSpoutXF3', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', -6, -4, _A(_FADE)), ('wPuddleL', 'feet', 0, -1)],
                 12: [('wSpoutXB0', 'feet', 0, -26, {'behind': True}), ('wSpoutXF0', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', 6, -8), ('wPuddleL', 'feet', 0, -1), ('wRip12', 'feet', 0, -2, _A(_FADE))],
                 13: [('wSpoutXB1', 'feet', 0, -26, {'behind': True}), ('wSpoutXF1', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', -4, -8, _A(_FADE)), ('wPuddleL', 'feet', 0, -1), ('wSplashS', 'feet', -10, -4, _A(_FADE))],
                 14: [('wSpoutXB2', 'feet', 0, -26, {'behind': True}), ('wSpoutXF2', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', 8, -6), ('wPuddleL', 'feet', 0, -1), ('wSplashS', 'feet', 10, -4, _A(_FADE))],
                 15: [('wSpoutXB3', 'feet', 0, -26, {'behind': True}), ('wSpoutXF3', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', 0, -10, _A(_FADE)), ('wPuddleL', 'feet', 0, -1), ('wRip12', 'feet', 0, -2, _A(_FADE))]}))
CLIPS['tsunami'] = ('Tsunami', 2,
  'Tsunami v4 (Cancer ninjutsu ultimate, charge, Elemental 28, Wide AoE: the caster conjures a giant tidal wave that crashes violently into its opponents; Christopher 2026-11-03: more dramatic, it is an ultimate; 22:35: better wave, more charging frames): the release, played after tsunamiCharge: arms up inside the whirling vortex, the fighter hauls back once more, then thrusts both palms forward: the vortex bursts in a white explosion of spray and the giant wave surges out from it toward the targets, water flooding back round its feet; it settles into the guard. In the testbed the giant breaking wave itself (extra.zone) rolls across the whole AoE.', [
     g(an=_OVER_N, af=_OVER_F, bob=(0, -1, 0), lean=(0, -2)),
     g(an=band(-165, -178, fistKind='palm'), af=band(-160, -176, fistKind='palm'), bob=(1, 0, 1), lean=(-1, -4)),
     g(an=band(-92, -92, fistKind='palm'), af=band(-85, -88, fistKind='palm'), bob=(2, 2, 2), lean=(2, 7), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-92, -92, fistKind='palm'), af=band(-85, -88, fistKind='palm'), bob=(2, 2, 2), lean=(2, 7), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-88, -95, fistKind='palm'), af=band(-80, -95, fistKind='palm'), bob=(2, 2, 2), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-70, -110, fistKind='palm'), af=band(-60, -110), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-50, -120), af=band(-40, -110), bob=(1, 1, 2), lean=(0, 2), root=(-2, 0)),
     g()],
  ['strain', 'roar', 'roar', 'roar', 'strain', 'squint', None, None],
  [3, 3, 3, 3, 2, 2, 1, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +2 thrusting the palms forward, -2 settling back',
       extra={'targetState': {'rule': 'Tsunami v3 (ultimate, charge; after tsunamiCharge): from the active frame (frame 2, the thrust) the testbed rolls the giant wave across the AoE (extra.zone); each fighter in the zone plays tsunamiStruck once when the wave front reaches its hex, then its idle', 'state': 'tsunamiStruck', 'loopFrom': None, 'element': 'water'},
              'charge': {'rule': 'Tsunami v3: the cast plays tsunamiCharge first (its shaking hold loops from frame 13 while the charge lasts), then this clip', 'state': 'tsunamiCharge'},
              'zone': {'rule': 'Tsunami v4 (Christopher 2026-11-03: more dramatic; 22:35 and 2026-11-04 make the wave look better): from frame 2 the testbed draws the giant breaking wave (about twice a fighter\'s height, base on the floor line, lip toward the targets), cycling NPAT frames wTsunamiBig0-3 every frameMs so the streaks and foam slide down its face, starting just behind the caster and rolling away from it across the whole Wide AoE over crossMs, rising from 60% to full height in the first quarter of the run, white foam NPAT wFoamL streaming off its lip, NPAT wSplashXL bursting at each fighter it hits; when it reaches the far edge of the AoE it crashes (it drops over 3 frames into wSplashXL / wDropsL along the edge), then the hexes it crossed hold a sheet of flood water (#2f7fe0 at 45%, white glints) that drains away over floodMs; preview tool hex-sprites/tools/astro_tsunami.py', 'pattern': 'wTsunamiBig', 'frames': ['wTsunamiBig0', 'wTsunamiBig1', 'wTsunamiBig2', 'wTsunamiBig3'], 'frameMs': 100, 'foam': 'wFoamL', 'hit': 'wSplashXL', 'startFrame': 2, 'crossMs': 900, 'floodMs': 700, 'from': 'caster', 'shape': 'wide'}},
       anchored={0: [('wSpoutXB0', 'feet', 0, -26, {'behind': True}), ('wSpoutXF0', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', 12, -2, _A(_FADE)), ('wPuddleL', 'feet', 0, -1)],
                 1: [('wSpoutXB1', 'feet', 0, -26, {'behind': True}), ('wSpoutXF1', 'feet', 0, -26, {'alpha': {'a': 200, 'A': 200, 'I': 220}}), ('wDropsL', 'head', 8, -4), ('wPuddleL', 'feet', 0, -1)],
                 2: [('wFlash', 'hand', 2, 0), ('wSpoutXB2', 'feet', 0, -26, {'behind': True, 'alpha': _FADE}), ('wSplashXL', 'feet', 4, -14), ('wSplashLD', 'feet', 18, -10), ('wJetL', 'hand', 10, 0), ('wDropsL', 'head', 0, -8)],
                 3: [('wRing3', 'hand', 3, 0), ('wSplashXL', 'feet', 14, -14), ('wDropsL', 'feet', 16, -30), ('wDropsL', 'head', -6, -2, _A(_FADE)), ('wWakeL', 'feet', 12, -3)],
                 4: [('wSplashLD', 'feet', 22, -10, _A(_FADE)), ('wWakeL', 'feet', 12, -3), ('wPuddleL', 'feet', 4, -1), ('wDrops', 'head', 4, 4, _A(_FADE))],
                 5: [('wPuddleL', 'feet', 4, -1), ('wDropsL', 'feet', 14, -10, _A(_FADE)), ('wWake', 'feet', 14, -2, _A(_FADE))],
                 6: [('wPuddleL', 'feet', 2, -1, _A(_FADE))]}))

# ---------- Vice Grip v2 (part 13, 2026-11-04; Christopher 16:28: needs an fx rework) ----------
def _pincer(L, gt, b=3, seed=0):   # a crab's pincer of water closing forward (front = right) from the hand at the left middle: an upper jaw and a shorter lower jaw (the thumb), each a curved, tapering blade of water with a white glinting back, light body, deep inner edge and teeth along it; gt = half the gap between the tips (0 = snapped shut, tips crossing)
    H = 2 * (gt + b + 4) + 1; W_ = L + 3; c = H // 2; rows = [['.'] * W_ for _ in range(H)]
    def jaw(sign, Lj):
        for i in range(Lj * 3):
            t = i / (Lj * 3 - 1); x = t * Lj
            yc = c + sign * (1 + (gt - 1) * t + b * math.sin(math.pi * min(1, t * 1.1)))   # the jaw's centreline bows out, then hooks back in to its tip
            tk = 4.4 * (1 - t) + 1.2
            for k in range(int(round(tk))):
                y = round(yc - sign * k + sign * (tk - 1) / 2); X = round(x)
                if not (0 <= X < W_ and 0 <= y < H): continue
                outer = k == 0; inner = k == int(round(tk)) - 1 and k > 0
                rows[y][X] = 'W' if outer and t < 0.8 else 'I' if outer else 'A' if inner else 'a'
            if 0.25 < t < 0.85 and i % 6 == 0:   # teeth along the inner edge
                y = round(yc - sign * (tk - 1) / 2 - sign * 1)
                if 0 <= y < H and 0 <= round(x) < W_ and rows[y][round(x)] == '.': rows[y][round(x)] = 'I'
        tx, ty = round(Lj), round(c + sign * max(0, gt))
        if 0 <= tx < W_ and 0 <= ty < H: rows[ty][tx] = 'W'   # the glinting tip
    jaw(-1, L); jaw(1, round(L * 0.8))
    for y in range(c - 1, c + 2):   # the root, a knot of water round the hand
        for x in range(0, 3):
            if rows[y][x] == '.': rows[y][x] = 'a' if x else 'A'
    return [''.join(q) for q in rows]
def _clampBurst(r, seed=0):   # Vice Grip: water squeezed out sideways from the clamped pincers: short jets up and down, drops flung outward
    import random
    rnd = random.Random(seed); w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for k in range(10):
        a = math.radians(rnd.choice((-1, 1)) * rnd.uniform(40, 140)); L = rnd.uniform(r * 0.5, r)
        for d in range(int(L * 2)):
            q = d / 2; x, y = round(r + q * math.cos(a)), round(r + q * math.sin(a))
            if 0 <= x < w and 0 <= y < w and (d % 3 or q < L * 0.5): rows[y][x] = 'W' if q < L * 0.4 else 'I' if q < L * 0.75 else 'a'
    return [''.join(q) for q in rows]
NPAT.update({'wPinS': _pincer(9, 3, 2), 'wPin': _pincer(15, 7, 4), 'wPinL': _pincer(17, 8, 4), 'wPinHalf': _pincer(16, 3, 4), 'wPinShut': _pincer(17, -1, 2), 'wPinShutS': _pincer(14, -1, 2),
             'wClampBurst': _clampBurst(10, 3), 'wClampBurstS': _clampBurst(7, 5)})
_VG = CLIPS['viceGrip']
CLIPS['viceGrip'] = (_VG[0], _VG[1], _VG[2].replace('Vice Grip (Cancer taijutsu', 'Vice Grip v2 (Christopher 2026-11-04: fx rework; Cancer taijutsu').replace('each wrapped in a C of water; the pincers snap shut on the opponent with a splash', 'and water surges up the arms and forms round each hand into a big crab\'s pincer of water, two curved jaws with teeth gaping open; the pincers snap shut on the opponent, water squeezed out of the clamp in jets and a ring of spray'),
  _VG[3], _VG[4], _VG[5],
  {**_VG[6], 'anchored': {1: [('wWakeL', 'feet', -10, -3), ('wDrops', 'feet', -12, -6, _A(_FADE)), ('wOrb2', 'hand', 1, 0, _A(_FADE))],
                          2: [('wWakeL', 'feet', -12, -3), ('wSplashS', 'feet', -8, -4, _A(_FADE)), ('wPinS', 'hand', 3, 3), ('wDrops', 'hand', -4, -3, _A(_FADE))],
                          3: [('wPin', 'hand', 5, 5), ('wJetB', 'hand', -8, 2, _A(_FADE)), ('wJetB', 'hand', -8, 10, _A(_FADE)), ('wWake', 'feet', -10, -2)],
                          4: [('wPinL', 'hand', 6, 5), ('wDrops', 'hand', -2, 8, _A(_FADE))],
                          5: [('wPinShut', 'hand', 6, 2), ('wClampBurst', 'hand', 10, 2), ('wRing2', 'hand', 9, 2, _A(_FADE))],
                          6: [('wPinShut', 'hand', 6, 2), ('wClampBurstS', 'hand', 9, 2, _A(_FADE)), ('wDrops', 'hand', 2, 8)],
                          7: [('wPinShutS', 'hand', 5, 2, _A(_FADE)), ('wDrops', 'feet', 4, -6, _A(_FADE)), ('wPuddle', 'feet', 4, -1, _A(_FADE))]}})

# Vice Grip v3 (Christopher 2026-11-04 16:44: the water pincers grip round the target's body; the target plays a restrained, struggling animation)
_flipP = lambda pat: [r[::-1] for r in pat]   # pincer closing toward the left (its root on the right, toward the caster in front of an E-facing target)
NPAT.update({'wGripOpen': _flipP(_pincer(20, 6, 8)), 'wGrip': _flipP(_pincer(20, 1, 9)), 'wGripT': _flipP(_pincer(19, 0, 8))})
_GF = {'alpha': {'W': 215, 'I': 175, 'a': 150, 'A': 175}, 'onFig': True}   # the front of the clamp, see-through where it crosses the body
_grip = lambda nm, dy=15: [(nm, 'head', -2, dy, {'behind': True}), (nm, 'head', -2, dy, _GF)]
_garm = lambda p: [('wHoseThin%d' % (p % 4), 'head', 15, 13)]   # the water arm from the clamp's root out toward the caster's hand
_VG = CLIPS['viceGrip']; _VX = _VG[6]
# Vice Grip v4 (Christopher 2026-11-04 16:51: keep the pincer fx where it is but on the arm/hand, not below it: lower the arm onto it; the target reacts only on the impact frame): frames 3-7 the near arm is lowered so the hand sits in the pincer's root (frames 3-4) and level with the clamp round the target's body (frames 5-7)
_VGP = list(_VG[3])
_VGP[3] = g(an=band(-86, -94, fistKind='palm'), af=band(-60, -50, fistKind='palm'), bob=(4, 5, 5), lean=(2, 7), root=(3, 0), ln='sp-drive-rear', lf='sp-drive-lead')
_VGP[4] = g(an=band(-86, -94, fistKind='palm'), af=band(-60, -50, fistKind='palm'), bob=(4, 5, 5), lean=(2, 7), ln='sp-drive-rear', lf='sp-drive-lead')
_VGP[5] = g(an=band(-64, -70, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(3, 3, 4), lean=(1, 5), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead')
_VGP[6] = g(an=band(-64, -70, fistKind='palm'), af=band(-50, -40, fistKind='palm'), bob=(3, 3, 4), lean=(1, 5), ln='sp-drive-rear', lf='sp-drive-lead')
_VGP[7] = g(an=band(-62, -70, fistKind='palm'), af=band(-50, -42, fistKind='palm'), bob=(2, 3, 3), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead')
CLIPS['viceGrip'] = (_VG[0], _VG[1], _VG[2].replace('the pincers snap shut on the opponent', 'the pincer, rooted in the caster\'s hand, shoots forward and its jaws snap shut round the opponent\'s body on the impact frame (from then on drawn on the target, viceGripped), the caster\'s lowered hand still in its root; the pincers snap shut on the opponent'),
  _VGP, _VG[4], _VG[5],
  {**_VX, 'extra': {'grapple': {**_VX['extra']['grapple'], 'targetState': 'viceGripped', 'rule': _VX['extra']['grapple']['rule'] + '; Vice Grip v4: on the impact frame (frame 5) and not before, the target plays viceGripped (its frame 0 is the clamp shutting round its body; then it struggles, looping from frame 2) for as long as the hold lasts, instead of the clinch held idle, and the caster holds its last frames (5-7 looping) with its hand in the pincer\'s root'}},
   'anchored': {**_VX['anchored'],
                3: [('wPin', 'hand', 8, 0), ('wJetB', 'hand', -8, 2, _A(_FADE)), ('wJetB', 'hand', -8, 10, _A(_FADE)), ('wWake', 'feet', -10, -2)],
                4: [('wPinL', 'hand', 9, 0), ('wDrops', 'hand', -2, 8, _A(_FADE))],
                5: [('wHoseThin0', 'hand', 6, 0), ('wHoseRoot0', 'hand', 0, 0), ('wDrops', 'hand', 2, 6, _A(_FADE))],
                6: [('wHoseThin1', 'hand', 6, 0), ('wHoseRoot1', 'hand', 0, 0, _A(_FADE)), ('wDrops', 'hand', 2, 8)],
                7: [('wHoseThin2', 'hand', 6, 0), ('wDrops', 'feet', 4, -6, _A(_FADE)), ('wPuddle', 'feet', 4, -1, _A(_FADE))]}})
_PIN = lambda u, f, **k: g(an=band(u, f), af=band(-u // 2, f + 8), **k)   # arms clamped to the sides under the pincer, elbows working against it
CLIPS['viceGripped'] = ('Vice Gripped', 0,
  'Vice Gripped (target state of Vice Grip, held while the grapple lasts): frame 0 is the impact (Christopher 2026-11-04: targets react only on the impact frame): the caster\'s giant crab pincer of water has just snapped shut round the fighter\'s body, the upper jaw across the chest and arms, the lower round the hips, the tips meeting behind its back (the jaws see-through where they cross the body); the fighter jolts and its arms are pinned to its sides; then (looping from frame 2 while held) it struggles: wrenching back, twisting forward, elbows working out against the clamp, shoulders heaving, as the pincer squeezes and water squirts out of the joints; a rope of water runs from the clamp toward the caster.',
  [g(an=band(-30, -95), af=band(-20, -85), bob=(1, 1, 1), lean=(-1, -3)),
   _PIN(5, -50, bob=(1, 1, 1), lean=(-1, -2)),
   _PIN(18, -40, bob=(1, 1, 1), lean=(1, 2), root=(1, 0)),
   _PIN(2, -58, bob=(1, 1, 2), lean=(-2, -4)),
   _PIN(22, -35, bob=(1, 1, 1), lean=(0, 1)),
   _PIN(0, -50, bob=(2, 2, 2), lean=(-1, -2), root=(-1, 0)),
   _PIN(16, -42, bob=(1, 1, 1), lean=(1, 3)),
   _PIN(4, -56, bob=(1, 1, 2), lean=(-2, -4))],
  ['pain', 'pain', 'strain', 'pain', 'strain', 'strain', 'strain', 'pain'],
  None,
  dict(fps=8, rm='E: rocking 1 px in the struggle (net 0)', extra={'loop': True, 'loopFrom': 2},
       anchored={0: _grip('wGripT') + _garm(0) + [('wClampBurstS', 'head', -12, 15), ('wSplashS', 'head', 8, 12)],   # v4 impact-frame rule: frame 0 is the clamp shutting, no open jaws closing in beforehand
                 1: _grip('wGrip') + _garm(1) + [('wClampBurstS', 'head', 4, 26, _A(_FADE)), ('wDrops', 'head', 6, 4)],
                 **{k_: _grip('wGripT' if k_ % 2 else 'wGrip') + _garm(k_) + ([('wClampBurstS', 'head', -12 if k_ % 4 == 3 else 4, 15 if k_ % 4 == 3 else 26, _A(_FADE))] if k_ % 2 else [('wDrops', 'head', -8, 2, _A(_FADE))]) for k_ in range(2, 8)}}))

# ---------- Hydro Cannon Palm v2 (part 13, 2026-11-04; Christopher 16:31: not a water bullet but a long gushing flow of water, like a fire hose, coming from the caster's palm) ----------
def _hose(L, phase, h=11):   # one tileable 16 px stretch of the fire-hose stream (front = right), v2 (a straight, solid jet, not a wavy line): a flat centreline and an even thickness with only a small surface chop, lengthwise streaks of white and ice running along it (period 16, so tiles join; phase 0-3 slides them 4 px toward the target), a deep edge, flecks of spray peeling off top and bottom
    rows = [['.'] * L for _ in range(h)]; c = (h - 1) / 2; R = c - 1.2
    hs = lambda x, y: ((((x - 4 * phase) % 16) * 7919 + y * 104729) % 101)
    for x in range(L):
        u = (x - 4 * phase) % 16
        for y in range(h):
            side = 1 if y > c else -1
            hw = R + 0.45 * math.sin(2 * math.pi * (u + (5 if side > 0 else 0)) / 8)   # chop on the surface, top and bottom out of step
            d = abs(y - c)
            if d <= hw:
                q = d / hw; lane = (round(y - c) * 5 + u) % 16
                if q < 0.2: ch = 'I' if lane in (3, 11) else 'W'
                elif q < 0.55: ch = 'W' if lane < 4 else 'I'
                elif q < 0.85: ch = 'a' if lane % 6 else 'I'
                else: ch = 'A'
            elif d <= hw + 1.8 and hs(x, y) < 11: ch = 'I' if hs(x, y) < 5 else 'a'
            else: continue
            rows[y][x] = ch
    return [''.join(q) for q in rows]
def _hoseRoot(r, phase=0):   # the stream bursting out of the open palm: a bloom of spray round the hand, flaring back over the wrist, a ring of drops
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for k in range(16):
        a = math.radians(70 + 220 * k / 15 + 7 * phase); L = r * (0.55 + 0.45 * ((k * 5 + phase) % 3) / 2)
        for t in range(int(L * 2)):
            q = t / 2; x, y = round(r + q * math.cos(a)), round(r + q * math.sin(a) * 0.8)
            if 0 <= x < w and 0 <= y < w and (t % 3 or q < L * 0.5): rows[y][x] = 'W' if q < L * 0.35 else 'I' if q < L * 0.7 else 'a'
    for y in range(r - 2, r + 3):
        for x in range(r, w):
            if abs(y - r) <= 2 - (x - r) // 4 and rows[y][x] == '.': rows[y][x] = 'I'
    return [''.join(q) for q in rows]
def _hoseHit(phase, w=19, h=31):   # the stream breaking on the target: water hammering into it and deflecting up and down and back toward the caster in fans of drops under gravity, a white burst at the point of impact (the point is at the left edge, middle)
    import random
    rnd = random.Random(90 + phase); rows = [['.'] * w for _ in range(h)]; ox, oy = 2, h // 2
    for k in range(18):
        a = math.radians(rnd.choice((-1, 1)) * rnd.uniform(25, 160)); v = rnd.uniform(0.6, 1.0)
        for t in range(30):
            s = t / 29; x = ox + math.cos(a) * v * (w - 3) * s; y = oy + math.sin(a) * v * (h / 2 - 1) * s + 6 * s * s
            if t % 3 and s > 0.4: continue
            xi, yi = round(x), round(y)
            if 0 <= xi < w and 0 <= yi < h: rows[yi][xi] = 'W' if s < 0.35 else 'I' if s < 0.65 else 'a'
    for y in range(oy - 3, oy + 4):
        for x in range(0, 4 - abs(y - oy) // 2):
            rows[y][x] = 'W' if abs(y - oy) < 2 else 'I'
    return [''.join(q) for q in rows]
NPAT.update({**{'wHose%d' % p: _hose(16, p) for p in range(4)}, **{'wHoseThin%d' % p: _hose(16, p, h=7) for p in range(4)},
             **{'wHoseRoot%d' % p: _hoseRoot(6, p) for p in range(2)}, **{'wHoseHit%d' % p: _hoseHit(p) for p in range(4)}})
NPAT['wHoseTail'] = [''.join(ch if (x // 3 + y) % 2 == 0 else '.' for x, ch in enumerate(row)) for y, row in enumerate(_hose(16, 1, h=7))]   # the stream breaking up into a run of drops as it cuts off
_HOSE = lambda p, n=3, thin=False: [('wHose%s%d' % ('Thin' if thin else '', (p + k) % 4), 'hand', 9 + 16 * k, 0) for k in range(n)]   # the stream tiled forward from the palm to the cell's edge (the testbed carries it on to the target)
_HCP_N, _HCP_F = band(-90, -90, fistKind='palm'), band(30, -160)   # palm driven straight out at chest height, far arm drawn back
CLIPS['hydroCannonPalm'] = ('Hydro Cannon Palm', 4,
  'Hydro Cannon Palm v2 (Cancer taijutsu strike, Physical 14, Melee, 2 slots: the fighter slams its palm into the opponent, creating a hydrostatic pressure wave that travels through its body; Christopher 2026-11-04: not a water bullet but a long gushing flow of water, like a fire hose, coming from the palm): from the guard the fighter draws the rear hand back low beside the hip, palm open, and water swirls up the arm and gathers in the palm, swelling over three frames; then it drives the palm out and a thick stream of water blasts from it like a fire hose, a bloom of spray round the hand, the stream gushing straight into the target and breaking over it in fans of spray; the fighter braces against the force, sliding back a little as the stream keeps pouring for four frames, then it cuts off, the end of the stream breaking into a run of drops, and the fighter settles back into the guard (the target plays hydroWaved). Body from Shock Palm (approved) with a held thrust; water colours. In the testbed the stream itself is carried on from the palm to the target (extra.stream).', [
     g(),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -1), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 1), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=band(25, -60, fistKind='palm'), af=band(-75, -100), bob=(1, 1, 2), lean=(-1, -3), ln='sp-load-rear', lf='sp-load-lead'),
     g(an=_HCP_N, af=_HCP_F, bob=(2, 2, 2), lean=(2, 6), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_HCP_N, af=_HCP_F, bob=(2, 2, 2), lean=(1, 3), root=(-1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_HCP_N, af=_HCP_F, bob=(2, 2, 3), lean=(1, 3), root=(-1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_HCP_N, af=_HCP_F, bob=(2, 2, 2), lean=(1, 2), root=(-1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_HCP_N, af=_HCP_F, bob=(2, 2, 3), lean=(1, 3), root=(-1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-80, -95, fistKind='palm'), af=band(20, -150), bob=(1, 1, 2), lean=(1, 2), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -120), af=band(-30, 215), bob=(1, 1, 2), lean=(1, 3), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g()],
  [None, 'squint', 'squint', 'strain', 'roar', 'strain', 'strain', 'strain', 'strain', 'squint', None, None],
  None,
  dict(fps=10, hitbox=[46, 20, 18, 10], damage='heavy', rm='E: +2 stepping into the palm, -1 -1 -1 -1 driven back by the stream, +2 settling (net 0)',
       swirl={1: (0, 0.5), 2: (120, 0.8), 3: (240, 1.0)}, recolor=WATER_RECOLOR, keepFx=True,
       extra={'targetState': {'rule': 'Hydro Cannon Palm v2: when the stream reaches the target (frame 4) the target plays hydroWaved once, then its idle', 'state': 'hydroWaved'},
              'stream': {'rule': 'Hydro Cannon Palm v2 (Christopher 2026-11-04: a long gushing flow of water like a fire hose, from the palm): on frames 4-8 the testbed draws the stream from the caster\'s near hand (the arms layer\'s most forward pixel, the same anchor the clip uses) straight to the target\'s chest, tiling NPAT tile frames along it (16 px tiles; frame k uses tiles[(k + i) % 4] for the i-th tile so the ripples run toward the target), and NPAT hit[(k - 4) % 4] on the target at the point the stream meets it, its left edge on that point (mirrored for W); on frame 9 it draws tail tiles only over the last third, the stream cutting off; the clip itself bakes the stream from the palm to the edge of the cell', 'from': 'hand', 'frames': [4, 5, 6, 7, 8], 'tiles': ['wHose0', 'wHose1', 'wHose2', 'wHose3'], 'tile': 16, 'hit': ['wHoseHit0', 'wHoseHit1', 'wHoseHit2', 'wHoseHit3'], 'tailFrame': 9, 'tail': 'wHoseTail'}},
       anchored={1: [('wOrb2', 'hand', 0, 0)], 2: [('wOrb3', 'hand', 0, 0), ('wDrops', 'hand', 0, -4, _A(_FADE))], 3: [('wOrb4', 'hand', 0, 0), ('wSplashS', 'hand', 0, -5, _A(_FADE))],
                 4: _HOSE(0) + [('wHoseRoot0', 'hand', 1, 0), ('wRing', 'hand', 1, 0)],
                 5: _HOSE(1) + [('wHoseRoot1', 'hand', 1, 0), ('wDrops', 'hand', -2, 6, _A(_FADE))],
                 6: _HOSE(2) + [('wHoseRoot0', 'hand', 1, 0)],
                 7: _HOSE(3) + [('wHoseRoot1', 'hand', 1, 0), ('wDrops', 'hand', -3, 6, _A(_FADE))],
                 8: _HOSE(0, thin=True) + [('wHoseRoot0', 'hand', 1, 0, _A(_FADE))],
                 9: [('wHoseTail', 'hand', 25, 0), ('wDrops', 'hand', 4, 3)],
                 10: [('wDrops', 'hand', 0, 6, _A(_FADE)), ('wPuddle', 'feet', 6, -1, _A(_FADE))]}))

# Hydro Cannon Palm v3 (Christopher 2026-11-04 16:45: the water swirls round the hand for more frames): the palm loads for six frames, not three; everything from the thrust on moves 3 frames later
_HC = CLIPS['hydroCannonPalm']; _HCX = _HC[6]; _HCL = _HC[3][1:4]
_hcs = lambda k: k + 3 if k >= 4 else k
CLIPS['hydroCannonPalm'] = (_HC[0], 8, _HC[2].replace('swelling over three frames', 'swirling round and round the hand and swelling over six frames'),
  [_HC[3][0]] + [_HCL[0], _HCL[0], _HCL[1], _HCL[1], _HCL[2], _HCL[2]] + _HC[3][4:],
  [_HC[4][0], 'squint', 'squint', 'squint', 'strain', 'strain', 'strain'] + _HC[4][4:], _HC[5],
  {**_HCX, 'swirl': {1: (0, 0.4), 2: (60, 0.55), 3: (120, 0.7), 4: (180, 0.8), 5: (240, 0.9), 6: (300, 1.0)},
   'rm': _HCX['rm'].replace('+2 stepping', 'six frames loading, +2 stepping'),
   'extra': {**_HCX['extra'], 'targetState': {**_HCX['extra']['targetState'], 'rule': 'Hydro Cannon Palm v3: when the stream reaches the target (frame 8, the impact frame; Christopher 2026-11-04: targets react only on the impact frame) the target plays hydroWaved once, then its idle; before that it holds its guard'},
             'stream': {**_HCX['extra']['stream'], 'rule': _HCX['extra']['stream']['rule'].replace('frames 4-8', 'frames 7-11').replace('frame 9', 'frame 12').replace('(k - 4)', '(k - 7)'), 'frames': [7, 8, 9, 10, 11], 'tailFrame': 12, 'reachFrame': 8, 'reachRule': 'on frames before reachFrame the stream front is still travelling: draw the tiles only to halfway between the palm and the target, with NPAT front at the leading end and no hit fx; from reachFrame it reaches the target', 'front': 'wSplashS'}},
   'anchored': {1: [('wOrb2', 'hand', 0, 0)], 2: [('wOrb2', 'hand', 0, 0), ('wDrops', 'hand', 0, -4, _A(_FADE))], 3: [('wOrb3', 'hand', 0, 0)],
                4: [('wOrb3', 'hand', 0, 0), ('wDrops', 'hand', 2, -5, _A(_FADE))], 5: [('wOrb4', 'hand', 0, 0), ('wSplashS', 'hand', 0, -5, _A(_FADE))], 6: [('wOrb4', 'hand', 0, 0), ('wDrops', 'hand', -2, -6, _A(_FADE))],
                **{_hcs(k): v for k, v in _HCX['anchored'].items() if k >= 4}}})

# Hydro Cannon Palm v5 (Christopher 2026-11-04 17:15: v4 still broke the impact-frame rule; the stream got halfway in one frame and the target reacted the same frame it arrived): the stream front now travels for two frames (frame 7 a third of the way, frame 8 two thirds), drawn only by the testbed (no baked tiles reaching ahead of the front), and touches the target on frame 9, the impact frame; one more held pouring frame so the pour on the target still lasts four frames
_HC = CLIPS['hydroCannonPalm']; _HCX = _HC[6]
_HCF = list(_HC[3]); _HCF.insert(12, g(an=_HCP_N, af=_HCP_F, bob=(2, 2, 3), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'))
_HCE = list(_HC[4]); _HCE.insert(12, 'strain')
CLIPS['hydroCannonPalm'] = (_HC[0], 9, _HC[2].replace('Hydro Cannon Palm v2 (', 'Hydro Cannon Palm v5 (').replace('a thick stream of water blasts from it like a fire hose', 'a thick stream of water blasts from it like a fire hose, its front rushing across the gap for two frames before it reaches the target, which holds its guard until the water touches it'),
  _HCF, _HCE, _HC[5],
  {**_HCX, 'rm': _HCX['rm'].replace('-1 -1 -1 -1 driven back', '-1 -1 -1 -1 0 driven back'),
   'extra': {**_HCX['extra'],
             'targetState': {**_HCX['extra']['targetState'], 'rule': 'Hydro Cannon Palm v5: the target holds its plain guard on every frame before the stream touches it; on frame 9 (the impact frame, reachFrame, the clip\'s active frame) it plays hydroWaved once from its frame 0 (the moment the water hits), then its idle (Christopher 2026-11-04: targets react only on the impact frame)'},
             'stream': {**_HCX['extra']['stream'],
                        'rule': _HCX['extra']['stream']['rule'].replace('frames 7-11', 'frames 7-12').replace('frame 12', 'frame 13').replace('(k - 7)', '(k - 9)').replace('the clip itself bakes the stream from the palm to the edge of the cell', 'the clip itself bakes the stream from the palm to the edge of the cell from frame 9 only'),
                        'frames': [7, 8, 9, 10, 11, 12], 'tailFrame': 13, 'reachFrame': 9, 'travel': {'7': 0.33, '8': 0.66},
                        'reachRule': 'Hydro Cannon Palm v5: on frames before reachFrame the stream front is still travelling: draw the tiles from the palm only to travel[k] of the way to the target (frame 7 a third, frame 8 two thirds), with NPAT front at the leading end, and no hit fx and no target reaction; on reachFrame the front touches the target, the hit fx starts (hit[(k - reachFrame) % 4]) and the target starts hydroWaved'}},
   'anchored': {**{k: v for k, v in _HCX['anchored'].items() if k < 7},
                7: [('wHoseRoot0', 'hand', 1, 0), ('wRing', 'hand', 1, 0)],
                8: [('wHoseRoot1', 'hand', 1, 0), ('wDrops', 'hand', -2, 6, _A(_FADE))],
                9: _HOSE(2) + [('wHoseRoot0', 'hand', 1, 0)],
                10: _HOSE(3) + [('wHoseRoot1', 'hand', 1, 0), ('wDrops', 'hand', -3, 6, _A(_FADE))],
                11: _HOSE(0) + [('wHoseRoot0', 'hand', 1, 0)],
                12: _HOSE(1, thin=True) + [('wHoseRoot1', 'hand', 1, 0, _A(_FADE))],
                13: [('wHoseTail', 'hand', 25, 0), ('wDrops', 'hand', 4, 3)],
                14: [('wDrops', 'hand', 0, 6, _A(_FADE)), ('wPuddle', 'feet', 6, -1, _A(_FADE))]}})
# hydroWaved v2 (impact-frame rule): frame 0 is the instant the stream touches the chest: a first small jolt with the splash where the water meets it; the big jolt and the wave rolling through follow from frame 1
_HW = CLIPS['hydroWaved']; _HWX = _HW[6]
CLIPS['hydroWaved'] = (_HW[0], _HW[1], _HW[2].replace('Hydro Waved (target state of Hydro Cannon Palm): the palm lands on its chest and the water bursts there;', 'Hydro Waved v2 (target state of Hydro Cannon Palm; frame 0 is the impact, Christopher 2026-11-04: targets react only on the impact frame): the stream slams into its chest and the water bursts there, a first small jolt;'),
  [g(an=band(-40, -105), af=band(-35, -100), bob=(1, 1, 1), lean=(-1, -2))] + list(_HW[3]), ['pain'] + list(_HW[4]), _HW[5],
  {**_HWX, 'rm': 'E: 0 on the impact, -1 jolted back, -1 as the wave bursts out of the back, +1 +1 recovering (net 0)',
   'anchored': {0: [('wSplashS', 'head', 7, 12)], **{k + 1: v for k, v in _HWX['anchored'].items()}}})

# Vice Grip v5 (Christopher 2026-11-04 17:15: the water must encompass both of the caster's arms): water surges up over both arms (near and far, the far arm in its own far-arm sheet so its pixels are known) from the hands to the elbows and stays round both through the clamp and the hold; the far hand gets its own knot of water and its own water rope to the clamp
def water_arms(state, frames):
    """Vice Grip v5: a coat of water over the caster's arms, following the actual arm pixels: frames = {frame: reach}; every
    pixel of the near arm (arms.png) and of the visible far arm (far-arm.png where no other figure layer covers it) within
    reach px of that arm's hand gets a see-through water wash with moving glints, and the empty pixels next to it a deep-water rim"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    fx = Image.open(f).convert('RGBA'); px = fx.load()
    near = Image.open(d + 'arms.png').convert('RGBA').load(); far = Image.open(d + 'far-arm.png').convert('RGBA').load()
    cover = [Image.open(d + n).convert('RGBA').load() for n in FIG_LAYERS if n not in ('far-arm.png',) and os.path.exists(d + n)]
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    def put(X, Y, c):
        q = px[X, Y]
        if q[3] < c[3]: px[X, Y] = c
    for k, reach in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            sg = -1 if fd == 'W' else 1; npts = near_pts(near, k, r)
            for side, L in (('far', far), ('near', near)):
                pts = {(x, y) for y in range(64) for x in range(64) if L[k * 64 + x, r * 64 + y][3]}
                if side == 'far': pts = {(x, y) for (x, y) in pts if not any(C[k * 64 + x, r * 64 + y][3] for C in cover)}
                if not pts: continue
                tip = max(pts, key=lambda q: (sg * q[0], -q[1]))
                coat = {(x, y) for (x, y) in pts if math.hypot(x - tip[0], y - tip[1]) <= reach}
                for (x, y) in coat:
                    u = (sg * x + 2 * k + y) % 6
                    put(k * 64 + x, r * 64 + y, hexc(NPAL['W'], 235) if u == 0 else hexc(NPAL['I'], 225) if u == 3 else hexc(NPAL['A'], 225) if (x, y + 1) not in coat else hexc(NPAL['a'], 220))   # v5.1: near-solid water (a thin wash over skin read grey)
                for (x, y) in coat:
                    for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        X, Y = x + ex, y + ey
                        if 0 <= X < 64 and 0 <= Y < 64 and (X, Y) not in pts and not (side == 'far' and (X, Y) in npts):
                            put(k * 64 + X, r * 64 + Y, hexc(NPAL['A'], 235) if (X + Y + k) % 5 else hexc(NPAL['I'], 235))
    fx.save(f); print(state, 'water_arms', list(frames))
def near_pts(L, k, r):
    return {(x, y) for y in range(64) for x in range(64) if L[k * 64 + x, r * 64 + y][3]}
_VG = CLIPS['viceGrip']; _VX = _VG[6]
CLIPS['viceGrip'] = (_VG[0], _VG[1], _VG[2].replace('Vice Grip v2 (', 'Vice Grip v5 (').replace('water surges up the arms', 'water surges up over both arms, coating them from the hands to the elbows,'),
  _VG[3], _VG[4], _VG[5],
  {**_VX, 'farLayer': True, 'waterArms': {1: 4, 2: 9, 3: 15, 4: 16, 5: 16, 6: 16, 7: 14},
   'extra': {'grapple': {**_VX['extra']['grapple'], 'rule': _VX['extra']['grapple']['rule'] + '; Vice Grip v5: both of the caster\'s arms stay coated in water through the hold (frames 5-7), each hand with its own water rope to the clamp'}},
   'anchored': {**_VX['anchored'],
                2: _VX['anchored'][2] + [('wOrb2', 'farhand', 1, 0)],
                3: _VX['anchored'][3] + [('wOrb3', 'farhand', 1, 0)],
                4: _VX['anchored'][4] + [('wOrb3', 'farhand', 1, 0), ('wDrops', 'farhand', 0, 5, _A(_FADE))],
                5: _VX['anchored'][5] + [('wHoseThin1', 'farhand', 6, 0), ('wHoseRoot1', 'farhand', 0, 0, _A(_FADE))],
                6: _VX['anchored'][6] + [('wHoseThin2', 'farhand', 6, 0)],
                7: _VX['anchored'][7] + [('wHoseThin3', 'farhand', 6, 0)]}})

# Regression v2 + Pacification v2 (Christopher 2026-11-04 impact-frame rule): the genjutsu waves now fly from the caster's palm to the target (testbed projectile volley, frames 5 and 6, three frames each), so the first wave reaches the target on frame 7 (a third of the way on 5, two thirds on 6); frame 7 is the active (impact) frame and the target's state starts there, holding its guard until then
for _st, _pat, _hit, _nm in (('regression', 'wgw3', 'wRip5', 'Regression'), ('pacification', 'wLullS3', 'wRip5', 'Pacification')):
    _C = CLIPS[_st]; _X = _C[6]; _TS = _X['extra']['targetState']
    CLIPS[_st] = (_C[0], 7, _C[2], _C[3], _C[4], _C[5],
      {**_X, 'extra': {**_X['extra'],
        'targetState': {**_TS, 'rule': _TS['rule'].replace('from the active frame (5)', 'from frame 7, the active frame, when the first wave reaches it (v2, impact-frame rule; it holds its plain guard before that)')},
        'projectile': {'rule': '%s v2 (impact-frame rule): on frames 5 and 6 the testbed flies NPAT %s from the near palm to the target at chest height a third of the way per frame (frames 5, 6, 7 for the first), so the first arrives on frame 7 (the impact frame, when the target state starts) and the second on frame 8; each pops %s on the target' % (_nm, _pat, _hit),
                       'volley': [{'frame': 5, 'from': 'hand', 'pattern': _pat, 'hit': _hit, 'flyFrames': 3}, {'frame': 6, 'from': 'hand', 'pattern': _pat, 'hit': _hit, 'flyFrames': 3}]}}})

# ---------- Scorpio (Water) taijutsu v1 (part 14, 2026-11-04): Numbing Strike, Shadow Step, Kidney Shot ----------
# Scorpio colours: water and ice (W, I, a, A, n) with Scorpio's shadow (X near-black, x smoky edge) for the stealth work
def _iceSpark(r):   # an ice crystal flash: a white core, four long ice spikes and four short diagonal ones
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for d in range(r + 1):
        ch = 'W' if d < 2 else 'I' if d < r - 1 else 'a'
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): rows[r + dy * d][r + dx * d] = ch
        if d <= r // 2:
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)): rows[r + dy * d][r + dx * d] = 'I' if d < 2 else 'a'
    return [''.join(q) for q in rows]
def _frost(w, h, seed, n):   # a crust of frost crystals: scattered ice flecks with white glints and a few deep-blue specks
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for _ in range(n):
        x, y = rnd.randrange(w), rnd.randrange(h); rows[y][x] = rnd.choice('WIIaaA')
    return [''.join(q) for q in rows]
def _sPool(rx, ry=2):   # Shadow Step: a pool of shadow on the floor: near-black core, smoky edge, a thin deep-water rim
    w = 2 * rx + 1; h = 2 * ry + 1; rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            q = ((x - rx) / rx) ** 2 + ((y - ry) / max(1, ry)) ** 2
            if q <= 1: rows[y][x] = 'X' if q < 0.45 else 'x' if q < 0.8 else 'n'
    return [''.join(q) for q in rows]
def _sWisp(h, seed):   # shadow wisps curling up off the pool
    import random
    rnd = random.Random(seed); w = 9; rows = [['.'] * w for _ in range(h)]
    for k in range(3):
        x = 1 + 3 * k + rnd.choice((0, 1))
        for y in range(h - 1, -1, -1):
            if rnd.random() < 0.8: rows[y][max(0, min(w - 1, x + round(math.sin(y * 0.9 + k) * 1)))] = 'X' if y > h * 0.6 else 'x' if y > h * 0.3 else 'A'
    return [''.join(q) for q in rows]
NPAT.update({'iSpark2': _iceSpark(2), 'iSpark3': _iceSpark(3), 'iSpark5': _iceSpark(5), 'iFrost': _frost(9, 7, 1, 12), 'iFrostL': _frost(11, 13, 2, 22), 'iFrostS': _frost(5, 5, 3, 6),
             'sPool2': _sPool(4, 1), 'sPool4': _sPool(8, 2), 'sPool6': _sPool(12, 2), 'sPool7': _sPool(14, 3), 'sWisp': _sWisp(10, 1), 'sWisp2': _sWisp(14, 2), 'sWispS': _sWisp(6, 3)})
_NS_HIT = band(-95, -95, fistKind='point')   # two-finger nerve strike driven straight out at shoulder height
CLIPS.update({
 'numbingStrike': ('Numbing Strike', 4,
  'Numbing Strike (Scorpio taijutsu, Physical 14, Melee, Slow 2 rounds: a precise nerve strike that slows the opponent\'s reaction speed): from the guard the fighter narrows its eyes, sights the nerve and draws the lead hand back, two fingers out like a scorpion\'s sting, frost gathering on the fingertips; it darts in and stabs the two fingers into the opponent\'s shoulder joint: on the impact frame (4) an ice-crystal flash bursts at the point and frost crackles out; it snaps the hand back and returns to the guard (the target plays numbed).',
  [g(),
   g(af=band(-50, -140, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
   g(af=band(-40, -150, fistKind='point'), bob=(1, 1, 2), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
   g(af=band(-80, -100, fistKind='point'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=_NS_HIT, bob=(1, 1, 1), lean=(2, 5), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=_NS_HIT, bob=(1, 1, 1), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=band(-60, -130, fistKind='point'), bob=(1, 1, 1), lean=(1, 2), root=(-2, 0)),
   g(root=(-1, 0)),
   g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'squint', None, None, None],
  None,
  dict(fps=12, hitbox=[44, 16, 14, 8], damage='light', rm='E: +2 +1 darting in, -2 -1 back (net 0)',
       extra={'targetState': {'rule': 'Numbing Strike: on the impact frame (4, the active frame) and not before, the target plays numbed once (the struck arm goes dead and frost spreads from the point), then its idle; before that it holds its plain guard', 'state': 'numbed'}},
       anchored={1: [('iSpark2', 'farhand', 1, 0, _A(_FADE))], 2: [('iSpark2', 'farhand', 1, 0), ('iFrostS', 'farhand', -2, 0, _A(_FADE))],
                 3: [('iSpark2', 'farhand', 1, 0), ('wDrops', 'farhand', -6, 2, _A(_FADE))],
                 4: [('iSpark5', 'farhand', 3, 0), ('iFrost', 'farhand', 5, 0)],
                 5: [('iSpark3', 'farhand', 4, 0, _A(_FADE)), ('iFrostS', 'farhand', 6, 3)],
                 6: [('iFrostS', 'farhand', 0, 2, _A(_FADE))]})),
 'numbed': ('Numbed', 0,
  'Numbed (target state of Numbing Strike, Slow 2 rounds): frame 0 is the impact: the two fingers strike the lead shoulder, an ice flash, the shoulder jolts back; frost crackles out over the shoulder and down the arm, the arm goes dead and drops limp at its side, the fighter shudders with cold, then hauls the guard back up stiffly and slowly, frost still glinting on the arm.',
  [g(af=band(-30, -95), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
   g(af=band(-10, -60), bob=(1, 1, 1), lean=(-1, -2)),
   g(af=AR_HANG_F, bob=(1, 1, 2), lean=(0, -1)),
   g(af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 2)),
   g(af=AR_HANG_F, bob=(1, 1, 2), lean=(0, 1), root=(1, 0)),
   g(af=band(-25, -70), bob=(1, 1, 1), lean=(0, 1)),
   g(af=band(-45, -110), bob=(1, 1, 1), lean=(0, 0)),
   g()],
  ['pain', 'pain', 'strain', 'squint', 'squint', 'strain', None, None],
  None,
  dict(fps=8, rm='E: -1 struck, +1 recovering (net 0)',
       anchored={0: [('iSpark5', 'head', 4, 10), ('iFrostS', 'head', 3, 11)],
                 1: [('iFrost', 'head', 2, 12), ('iSpark2', 'head', 4, 9, _A(_FADE))],
                 2: [('iFrostL', 'head', 2, 17)], 3: [('iFrostL', 'head', 2, 18), ('iSpark2', 'head', 1, 24)],
                 4: [('iFrostL', 'head', 2, 18)], 5: [('iFrost', 'head', 3, 14)], 6: [('iFrostS', 'head', 3, 13, _A(_FADE))]})),
 'shadowStep': ('Shadow Step', 3,
  'Shadow Step (Scorpio taijutsu, teleport, buff, stance, priority, gap closer, +6 move, Stealth 1 round: the fighter vanishes and repositions in shadow): from the guard the fighter drops into a low crouch and a pool of shadow spreads under its feet, wisps curling up; it sinks into the pool and is gone, the pool sliding away along the floor; 40 px on the pool opens again and the fighter rises out of it, low, shadow streaming off it, into the guard, then fades into stealth (spec opacity; extra.travel: the game moves the fighter by 40 px).',
  [g(),
   g(an=band(-25, 205), af=band(-40, 215), bob=(3, 3, 3), lean=(1, 4), ln='ml-dip-rear', lf='ml-dip-lead'),
   g(an=band(-25, 205), af=band(-40, 215), bob=(6, 7, 7), lean=(1, 5), rot=_LIFT(-8), **BRACE),
   g(an=band(-25, 205), af=band(-40, 215), bob=(8, 9, 9), lean=(1, 5), rot=_LIFT(-22), **BRACE),
   g(an=band(-25, 205), af=band(-40, 215), bob=(8, 9, 9), lean=(1, 5), root=(40, 0), rot=_LIFT(-22), **BRACE),
   g(an=band(-25, 205), af=band(-40, 215), bob=(6, 7, 7), lean=(1, 5), rot=_LIFT(-12), **BRACE),
   g(an=band(-25, 208), af=band(-45, 220), bob=(3, 3, 3), lean=(1, 4), rot=_LIFT(-3), ln='ml-dip-rear', lf='ml-dip-lead'),
   g(an=band(-40, -110), af=band(-45, -120), bob=(1, 1, 2), lean=(0, 2)),
   g()],
  [None, 'squint', 'squint', 'closed', 'closed', 'squint', 'squint', None, None],
  None,
  dict(fps=10, rm='E: +40 while sunk in the shadow (frame 4, invisible); 40 px in all (travel); sinks 8, 22 px below the floor line (bodyRotation dy, the cell crops it) and rises 12, 3',
       opacity={'rule': 'Shadow Step: the fighter sinks into the shadow and is gone, and rises from it 40 px on into Stealth 1 round. Multiply the whole composited fighter (every layer, fx included; the shadow pool and wisps are drawn on the floor separately and stay visible) by self[k] for its own side and others[k] for any other viewer; after the clip the Stealth state holds the last value (self 0.4, others 0) until Stealth ends',
                'self': [1, 1, 0.75, 0.15, 0.15, 0.5, 0.8, 0.6, 0.4], 'others': [1, 1, 0.6, 0, 0, 0.4, 0.7, 0.3, 0]},
       extra={'travel': {'rule': 'Shadow Step is a teleport (Move +6): the fighter ends the clip 40 px further forward (sum of rootMotion); the game moves the fighter by that distance', 'E': 40},
              'floorFx': {'rule': 'Shadow Step: the shadow pool (sPool*) and wisps are drawn by the testbed on the floor at the fighter\'s feet and are NOT multiplied by opacity, so the pool shows while the fighter is invisible; frame 3 at the start spot, frame 4 sliding (the pool drawn at the start spot fading and at the new spot growing), frames 5-6 at the new spot; the clip also bakes them into fx for previews', 'frames': {'1': ['sPool2'], '2': ['sPool4', 'sWispS'], '3': ['sPool6', 'sWisp'], '4': ['sPool6', 'sWisp2'], '5': ['sPool6', 'sWisp'], '6': ['sPool4', 'sWispS'], '7': ['sPool2']}}},
       anchored={1: [('sPool2', 'feet', 0, -1)], 2: [('sPool4', 'feet', 0, -2), ('sWispS', 'feet', -2, -6)],
                 3: [('sPool6', 'feet', 0, -2), ('sWisp', 'feet', -1, -7), ('sWispS', 'feet', 6, -5)],
                 4: [('sPool7', 'feet', 0, -3), ('sWisp2', 'feet', 0, -9)],
                 5: [('sPool6', 'feet', 0, -2), ('sWisp2', 'feet', -2, -9), ('sWispS', 'feet', 6, -5)],
                 6: [('sPool4', 'feet', 0, -2), ('sWisp', 'feet', -4, -7, _A(_FADE))],
                 7: [('sPool2', 'feet', 0, -1, _A(_FADE)), ('sWispS', 'head', -6, 6, _A(_FADE))]})),
 'kidneyShot': ('Kidney Shot', 4,
  'Kidney Shot (Scorpio taijutsu, Physical 16, Melee: the fighter feints before delivering a vicious blow to the opponent\'s kidney): from the guard the fighter flicks a half jab at the face as a feint, eyes on the head; as the guard rises to meet it, it snaps the feint back, dips low and steps in to the side, and drives the rear fist round in a hooking blow into the opponent\'s flank under the ribs: on the impact frame (4) water bursts off the fist in a hard splash and a ring of spray; it rolls back out to the guard (the target plays kidneyStruck).',
  [g(),
   g(af=band(-72, -105), bob=(1, 1, 1), lean=(1, 2), root=(1, 0)),
   g(af=band(-55, -125), an=band(20, -40), bob=(3, 4, 4), lean=(2, 6), ln='sp-load-rear', lf='sp-load-lead'),
   g(af=band(-55, -125), an=band(-20, -70), bob=(4, 4, 4), lean=(2, 8), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=band(-55, -125), an=band(-40, -85), bob=(4, 4, 4), lean=(2, 9), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=band(-55, -125), an=band(-40, -85), bob=(4, 4, 4), lean=(2, 8), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=band(-55, -125), an=band(-30, -110), bob=(2, 2, 3), lean=(1, 4), root=(-2, 0)),
   g(root=(-2, 0)),
   g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'squint', None, None],
  None,
  dict(fps=12, hitbox=[42, 30, 14, 10], damage='heavy', rm='E: +1 feint, +2 +1 stepping into the hook, -2 -2 rolling out (net 0)',
       extra={'targetState': {'rule': 'Kidney Shot: on the impact frame (4, the active frame) and not before, the target plays kidneyStruck once, then its idle; during the feint (frames 1-3) it holds its plain guard', 'state': 'kidneyStruck'}},
       anchored={3: [('wDrops', 'hand', -6, -2, _A(_FADE))],
                 4: [('wSplash', 'hand', 4, -2), ('wRing', 'hand', 2, 0), ('wDrops', 'hand', 6, 4)],
                 5: [('wRing2', 'hand', 3, 0, _A(_FADE)), ('wDropsL', 'hand', 6, 2, _A(_FADE))],
                 6: [('wDrops', 'feet', 8, -6, _A(_FADE))]})),
 'kidneyStruck': ('Kidney Struck', 0,
  'Kidney Struck (target state of Kidney Shot): frame 0 is the impact: the hook lands in its flank and water bursts off it; it buckles sideways over the blow, the rear hand clutching the kidney, the lead arm dropping, knees dipping, face screwed up; it stays folded a beat, then straightens slowly, hand still on its side, and recovers the guard.',
  [g(an=band(20, -30), af=band(-35, -100), bob=(2, 2, 2), lean=(1, 3), root=(-2, 0)),
   g(an=band(30, -20), af=band(-20, -80), bob=(4, 4, 4), lean=(2, 7), root=(-1, 0), **LOW),
   g(an=band(30, -20), af=band(-10, -60), bob=(5, 5, 5), lean=(2, 8), **LOW),
   g(an=band(30, -20), af=band(-10, -60), bob=(5, 5, 5), lean=(2, 8), **LOW),
   g(an=band(25, -25), af=band(-30, -90), bob=(3, 3, 3), lean=(1, 4), root=(1, 0)),
   g(an=band(-20, -80), af=band(-45, -115), bob=(1, 1, 2), lean=(1, 2), root=(2, 0)),
   g()],
  ['pain', 'pain', 'strain', 'strain', 'squint', None, None],
  None,
  dict(fps=8, rm='E: -2 -1 driven back, +1 +2 recovering (net 0)',
       anchored={0: [('wSplashS', 'head', 2, 26), ('wDrops', 'head', -6, 22, _A(_FADE))], 1: [('wDrops', 'feet', -2, -10, _A(_FADE))]})),
})

# Numbing Strike v2 (Christopher 2026-11-04 20:49: multiple strikes with the arms alternating, exaggerated fx): four two-finger strikes, lead, rear, lead, rear (the last the finisher), each landing on its own frame (2, 3, 4, 5); the first is the impact frame; the target jolts on every hit
def _shards(r, seed, n=9):   # ice shards flung outward: short bright streaks with white heads
    import random
    rnd = random.Random(seed); w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for _ in range(n):
        a = rnd.uniform(0, 2 * math.pi); L = rnd.uniform(r * 0.45, r)
        for t in range(int(L * 2)):
            q = t / 2; x, y = round(r + q * math.cos(a)), round(r + q * math.sin(a))
            if 0 <= x < w and 0 <= y < w and q > r * 0.25: rows[y][x] = 'W' if q > L * 0.75 else 'I' if q > L * 0.45 else 'a'
    return [''.join(q) for q in rows]
def _iceRing(r):   # a ring of frost blasting out: ice edge, white glints every few pixels
    w = 2 * r + 1; rows = [['.'] * w for _ in range(w)]
    for i in range(int(2 * math.pi * r * 1.5)):
        a = i / (r * 1.5); x, y = round(r + r * math.cos(a)), round(r + r * math.sin(a) * 0.8)
        rows[y][x] = 'W' if i % 5 == 0 else 'I' if i % 2 else 'a'
    return [''.join(q) for q in rows]
NPAT.update({'iSpark7': _iceSpark(7), 'iSpark9': _iceSpark(9), 'iShards6': _shards(6, 4), 'iShards9': _shards(9, 5, 14), 'iShards12': _shards(12, 6, 18), 'iRing5': _iceRing(5), 'iRing8': _iceRing(8), 'iRing11': _iceRing(11)})
_NSL = band(-95, -95, fistKind='point'); _NSR = band(-92, -92, fistKind='point')   # lead / rear two-finger strike straight out
_NSLB, _NSRB = band(-50, -140, fistKind='point'), band(10, -60, fistKind='point')   # lead / rear pulled back, fingers ready
CLIPS['numbingStrike'] = ('Numbing Strikes', 2,   # renamed by Christopher 2026-11-04 20:52 (canon amendment); state id unchanged

  'Numbing Strike v2 (Scorpio taijutsu, Physical 14, Melee, Slow 2 rounds: precise nerve strikes that slow the opponent\'s reaction speed; Christopher 2026-11-04: multiple strikes, arms alternating, exaggerated fx): from the guard the fighter narrows its eyes and readies both hands, two fingers out like a scorpion\'s stings, frost smoking off the fingertips; then it unleashes a flurry of four nerve strikes, lead, rear, lead, rear, each stabbing a nerve point (lead shoulder, chest, upper arm, and the last, the finisher, driven into the shoulder joint with a step), each hit bursting in a big ice-crystal flash with ice shards flung out and a frost ring, the last the biggest; it snaps the hands back and returns to the guard (the target plays numbed, jolting at every hit).',
  [g(),
   g(af=_NSLB, an=_NSRB, bob=(1, 1, 2), lean=(-1, -2), ln='sp-load-rear', lf='sp-load-lead'),
   g(af=_NSL, an=_NSRB, bob=(1, 1, 1), lean=(1, 4), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=_NSLB, an=_NSR, bob=(1, 1, 1), lean=(1, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=_NSL, an=_NSRB, bob=(1, 1, 1), lean=(1, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=_NSLB, an=_NSR, bob=(2, 2, 2), lean=(2, 7), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=_NSLB, an=_NSR, bob=(2, 2, 2), lean=(2, 7), ln='sp-drive-rear', lf='sp-drive-lead'),
   g(af=band(-60, -130, fistKind='point'), an=band(-20, -100, fistKind='point'), bob=(1, 1, 1), lean=(1, 2), root=(-2, 0)),
   g(root=(-1, 0)),
   g()],
  [None, 'squint', 'strain', 'strain', 'strain', 'roar', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 1, 2, 2, 1, 0, 0],
  dict(fps=12, auraColors=('#dff6ff', '#2f7fe0'), farLayer=True, hitbox=[44, 16, 14, 14], damage='light', rm='E: +2 into the flurry, +1 stepping into the finisher, -2 -1 back (net 0)',
       extra={'targetState': {'rule': 'Numbing Strike v2: on the impact frame (2, the first strike, the active frame) and not before, the target plays numbed once: its frames 0-3 are the four hits (caster frames 2-5, both at 12 fps), then the arm goes dead, it shudders and slowly recovers its guard, then its idle; before frame 2 it holds its plain guard', 'state': 'numbed', 'hits': [2, 3, 4, 5]}},
       anchored={1: [('iSpark3', 'farhand', 1, 0), ('iSpark3', 'hand', 1, 0), ('iFrostS', 'farhand', -3, -2, _A(_FADE)), ('iFrostS', 'hand', -3, -2, _A(_FADE))],
                 2: [('iSpark7', 'farhand', 3, 0), ('iShards6', 'farhand', 4, 0), ('iSpark2', 'hand', 1, 0)],
                 3: [('iSpark7', 'hand', 3, 0), ('iShards6', 'hand', 4, 0), ('iRing5', 'hand', 3, 0), ('iFrostS', 'farhand', 0, 2, _A(_FADE))],
                 4: [('iSpark7', 'farhand', 3, 0), ('iShards9', 'farhand', 4, 0), ('iRing5', 'farhand', 3, 0), ('iFrostS', 'hand', 0, 2, _A(_FADE))],
                 5: [('iSpark9', 'hand', 4, 0), ('iShards12', 'hand', 5, 0), ('iRing8', 'hand', 4, 0)],
                 6: [('iRing11', 'hand', 5, 0, _A(_FADE)), ('iShards12', 'hand', 7, 2, _A(_FADE)), ('iFrost', 'hand', 2, 3)],
                 7: [('iFrostS', 'hand', 0, 3, _A(_FADE)), ('iFrostS', 'farhand', 0, 3, _A(_FADE))]}))
CLIPS['numbed'] = ('Numbed', 0,
  'Numbed v2 (target state of Numbing Strike v2, Slow 2 rounds; frame 0 is the impact): four hits, one per frame: the lead shoulder jolts back (0), the chest (1), the upper arm (2), and the finisher into the shoulder joint snaps it back hardest (3), an ice flash and shards at each point; frost crusts over the shoulder and down the arm, the arm goes dead and drops limp at its side, the fighter shudders with cold, then hauls the guard back up stiffly and slowly, frost still glinting on the arm.',
  [g(af=band(-35, -100), bob=(1, 1, 1), lean=(-1, -2), root=(-1, 0)),
   g(af=band(-30, -95), bob=(1, 1, 1), lean=(0, -1)),
   g(af=band(-20, -80), bob=(1, 1, 1), lean=(-1, -2)),
   g(af=band(-5, -50), bob=(1, 1, 2), lean=(-2, -5), root=(-1, 0)),
   g(af=AR_HANG_F, bob=(1, 1, 2), lean=(-1, -2)),
   g(af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 2)),
   g(af=AR_HANG_F, bob=(1, 1, 2), lean=(0, 1)),
   g(af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 2)),
   g(af=AR_HANG_F, bob=(1, 1, 2), lean=(0, 1), root=(1, 0)),
   g(af=band(-25, -70), bob=(1, 1, 1), lean=(0, 1)),
   g(af=band(-45, -110), bob=(1, 1, 1), lean=(0, 0), root=(1, 0)),
   g()],
  ['pain', 'pain', 'pain', 'pain', 'strain', 'squint', 'strain', 'squint', 'squint', 'strain', None, None],
  None,
  dict(fps=12, rm='E: -1 first hit, -1 the finisher, +1 +1 recovering (net 0)',
       anchored={0: [('iSpark7', 'head', 4, 10), ('iShards6', 'head', 2, 10)],
                 1: [('iSpark7', 'head', 5, 16), ('iShards6', 'head', 3, 16), ('iFrostS', 'head', 3, 11)],
                 2: [('iSpark7', 'head', 3, 13), ('iShards9', 'head', 1, 13), ('iFrost', 'head', 2, 12)],
                 3: [('iSpark9', 'head', 4, 10), ('iShards12', 'head', 0, 10), ('iRing8', 'head', 2, 11), ('iFrost', 'head', 2, 12)],
                 4: [('iFrostL', 'head', 2, 17), ('iRing11', 'head', 1, 12, _A(_FADE)), ('iShards9', 'head', -4, 12, _A(_FADE))],
                 5: [('iFrostL', 'head', 2, 18), ('iSpark2', 'head', 1, 24)], 6: [('iFrostL', 'head', 2, 18), ('iSpark3', 'head', 3, 14, _A(_FADE))],
                 7: [('iFrostL', 'head', 2, 18), ('iSpark2', 'head', 0, 28)], 8: [('iFrostL', 'head', 2, 18)], 9: [('iFrost', 'head', 3, 14)],
                 10: [('iFrostS', 'head', 3, 13, _A(_FADE))]}))

# Kidney Shot v2 (Christopher 2026-11-04 20:50: more exaggerated fx): water swirls round the rear fist as it loads, the feint flicks spray, and the hook lands in a huge water burst: an XL splash, ice-white shards, a double pressure ring; the target gets a big splash at the flank and water blasting out of its back
_KS = CLIPS['kidneyShot']
CLIPS['kidneyShot'] = (_KS[0], _KS[1], _KS[2].replace('Kidney Shot (', 'Kidney Shot v2 (exaggerated fx, Christopher 2026-11-04; ').replace('water bursts off the fist in a hard splash and a ring of spray', 'water explodes off the fist in a huge splash with white shards and a double pressure ring'),
  _KS[3], _KS[4], [0, 0, 1, 2, 2, 1, 0, 0, 0],
  {**_KS[6], 'auraColors': _WAURA, 'farLayer': True,
   'anchored': {1: [('wDrops', 'farhand', 3, 0, _A(_FADE)), ('wSplashS', 'farhand', 2, 0, _A(_FADE))],
                2: [('wSplashS', 'hand', 0, 2, _A(_FADE))],
                3: [('wOrb3', 'hand', 1, 0), ('wJetB', 'hand', -9, 0, _A(_FADE)), ('wDrops', 'hand', -6, 4, _A(_FADE))],
                4: [('wSplashXL', 'hand', 8, -4), ('iShards12', 'hand', 6, 0), ('wRing3', 'hand', 4, 0), ('wRing', 'hand', 2, 0)],
                5: [('wSplashL', 'hand', 9, -3, _A(_FADE)), ('iShards9', 'hand', 8, 2, _A(_FADE)), ('wDropsL', 'hand', 8, 4)],
                6: [('wDropsL', 'feet', 10, -10, _A(_FADE)), ('wPuddle', 'feet', 10, -1)],
                7: [('wPuddle', 'feet', 12, -1, _A(_FADE))]}})
_KT = CLIPS['kidneyStruck']
CLIPS['kidneyStruck'] = (_KT[0], _KT[1], _KT[2].replace('Kidney Struck (', 'Kidney Struck v2 (exaggerated fx; ').replace('water bursts off it', 'water explodes over its flank and blasts out of its back'),
  _KT[3], _KT[4], _KT[5],
  {**_KT[6], 'anchored': {0: [('wSplashL', 'head', 4, 24), ('iShards9', 'head', 2, 24), ('wJetBL', 'head', -18, 24)],
                          1: [('wJetBL', 'head', -20, 26, _A(_FADE)), ('wDropsL', 'head', -14, 22), ('wSplashS', 'head', 2, 26, _A(_FADE))],
                          2: [('wDropsL', 'feet', -6, -10, _A(_FADE)), ('wPuddle', 'feet', -2, -1)],
                          3: [('wPuddle', 'feet', -2, -1, _A(_FADE)), ('wDrops', 'head', 0, 26, _A(_FADE))]}})

# ---------- Scorpio (Water) ninjutsu v1 (part 15, 2026-11-04): Ice Shard, Frost Armor, Blizzard ----------
def _iDart(L=9):   # Ice Shard: an ice dart pointing LEFT (tip at x 0; drawn for darts behind a target facing W, mirrored otherwise): white tip, ice body, deep back, a faint frost tail
    rows = [['.'] * (L + 3) for _ in range(3)]
    for x in range(L):
        rows[1][x] = 'W' if x < 2 else 'I' if x < L * 0.55 else 'a' if x < L - 1 else 'A'
        if 2 <= x < L - 1: rows[0][x] = 'I' if x < L * 0.4 else 'a'; rows[2][x] = 'a' if x < L * 0.6 else 'A'
    rows[1][L] = 'a'; rows[1][L + 2] = 'I'
    return [''.join(q) for q in rows]
def _iDartForm(n):   # an ice dart freezing out of the air: n = 0 a glint and frost motes, 1 the dart half formed
    if n == 0: return ['..I..', '.....', 'I.W.I', '.....', '..I..']
    return ['.......', '..IIa..', 'WIIaaA.', '..aaA..', '.......']
def _snow(w, h, seed, n, slant=2):   # snow and sleet driven sideways (to the right): short slanted streaks, white heads, ice tails, a few deep flecks
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for _ in range(n):
        x, y = rnd.randrange(w), rnd.randrange(h); L = rnd.choice((1, 2, 2, 3))
        for t in range(L + 1):
            X, Y = x - t * slant, y - t
            if 0 <= X < w and 0 <= Y < h: rows[Y][X] = 'W' if t == 0 else 'I' if t == 1 else 'a'
    for _ in range(n // 4):
        x, y = rnd.randrange(w), rnd.randrange(h); rows[y][x] = rnd.choice('An')
    return [''.join(q) for q in rows]
def _snowSwirl(rx, ry, phase, n=14):   # Blizzard: flakes whirling round an ellipse over the head, a bright lead flake with a fading tail
    w, h = 2 * rx + 3, 2 * ry + 3; rows = [['.'] * w for _ in range(h)]
    for i in range(n):
        a = (i / n + phase / 4) * 2 * math.pi; x, y = round(rx + 1 + rx * math.cos(a)), round(ry + 1 + ry * math.sin(a))
        rows[y][x] = 'W' if i % 4 == 0 else 'I' if i % 2 else 'a'
    return [''.join(q) for q in rows]
def _breath(n):   # a puff of frozen breath
    return [['..I.', '.I.I', 'I.I.'], ['.I..I', 'I.II.', '.I.I.', 'I....']][n]
NPAT.update({'iDart': _sq(_iDart(9), 1.5, 1.7), 'iDartS': _iDart(6), 'iDartF0': _sq(_iDartForm(0), 1.6, 1.6), 'iDartF1': _sq(_iDartForm(1), 1.6, 1.6),
             'iSnowS': _snow(15, 11, 1, 14), 'iSnow': _snow(27, 21, 2, 34), 'iSnowL': _snow(45, 45, 3, 170, 3), 'iSnowL2': _snow(45, 45, 4, 170, 3), 'iSnowL3': _snow(45, 45, 5, 170, 3),
             **{'iSwirl%d' % p: _snowSwirl(10, 3, p) for p in range(4)}, **{'iSwirlL%d' % p: _snowSwirl(15, 4, p, 22) for p in range(4)},
             'iBreath': _breath(0), 'iBreathL': _breath(1)})
_ISHELL = ('#f4fbff', '#bfe8ff', '#7cc8ff', '#2f7fe0')   # Frost Armor shell: white rim glint, ice, light water, deep edge
_POINT = band(-95, -95, fistKind='point')
CLIPS.update({
 'iceShard': ('Ice Shard', 6,
  'Ice Shard (Scorpio ninjutsu, Elemental 10, Ranged, Priority: the caster conjures ice darts behind the opponent that strike without warning): from the guard the fighter makes the seal at the chin and its eyes narrow, frost breath curling off it; it points two fingers at the target like a scorpion\'s sting, and behind the target, out of its sight, the air freezes: glints, then three ice darts form in a fan, pointing at its back; the fighter flicks the fingers down and the darts shoot in; on the impact frame (6) they strike the target\'s back (the target plays iceShardStruck); the fighter lowers the hand and settles back into the guard (spec extra.targetFx: the testbed draws the forming and flying darts behind the target, nothing baked on the target before impact).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 2), lean=(0, 1)),
     g(an=_POINT, bob=(1, 1, 1), lean=(1, 2)),
     g(an=_POINT, bob=(1, 1, 1), lean=(1, 2)),
     g(an=band(-70, -75, fistKind='point'), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-70, -75, fistKind='point'), bob=(1, 1, 2), lean=(1, 3)),
     g(an=band(-50, -110), af=band(-40, -110), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, 'squint', 'closed', 'squint', 'squint', 'strain', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA,
       extra={'targetFx': {'rule': 'Ice Shard v1: drawn by the testbed round the target (dx is away from the caster, i.e. behind the target; dy from the floor up is negative; patterns are drawn for a caster facing E and a target facing W, mirror both when the caster faces W): the darts freeze out of the air behind the target (frames 3-4) and shoot in (frame 5); they strike on frame 6, when the target starts iceShardStruck', 'frames': {'3': [['iDartF0', 18, -40], ['iDartF0', 21, -30], ['iDartF0', 17, -21]], '4': [['iDartF1', 19, -40], ['iDartF1', 22, -30], ['iDartF1', 18, -21], ['iFrostS', 22, -32]], '5': [['iDart', 17, -39], ['iDart', 19, -30], ['iDart', 16, -22]]}},
              'targetState': {'rule': 'Ice Shard: on the impact frame (6) and not before, the target plays iceShardStruck once (struck in the back), then its idle', 'state': 'iceShardStruck', 'element': 'water'}},
       anchored={1: [('iBreath', 'head', 5, 2, _A(_FADE))], 2: [('iFrostS', 'head', 1, 16), ('iBreath', 'head', 6, 1, _A(_FADE))],
                 3: [('iSpark2', 'hand', 1, 0)], 4: [('iSpark3', 'hand', 1, 0), ('iFrostS', 'hand', -2, 1, _A(_FADE))],
                 5: [('iSpark2', 'hand', 1, 1)], 6: [('iFrostS', 'hand', -1, 2, _A(_FADE))]})),
 'iceShardStruck': ('Ice Shard Struck', 0,
  'Ice Shard Struck (target state of Ice Shard, plays once; frame 0 is the impact): three ice darts slam into the fighter\'s back without warning: it is jolted forward, arching, ice shattering off its back in shards and a frost ring; frost crusts over its shoulder blades, it staggers a step, glances over its shoulder and hauls itself back into its guard.', [
     g(an=band(-40, -110), af=band(-30, -100), bob=(1, 1, 1), lean=(2, 5), root=(1, 0)),
     g(an=band(-20, -90), af=band(-10, -85), bob=(1, 1, 2), lean=(-1, -4)),
     g(an=band(-30, -100), af=band(-20, -95), bob=(1, 1, 2), lean=(-1, -3)),
     g(an=band(-45, -115), af=band(-35, -110), bob=(1, 1, 1), lean=(0, -1), root=(-1, 0)),
     g()],
  ['pain', 'pain', 'strain', 'squint', None],
  None,
  dict(fps=10, rm='E: +1 jolted forward, -1 back (net 0)',
       anchored={0: [('iSpark9', 'head', -8, 16), ('iShards12', 'head', -10, 18), ('iSpark7', 'head', -9, 26), ('iRing11', 'head', -8, 20)],
                 1: [('iShards12', 'head', -12, 18, _A(_FADE)), ('iRing11', 'head', -10, 20, _A(_FADE)), ('iFrostL', 'head', -5, 18)],
                 2: [('iFrost', 'head', -5, 18), ('iSpark2', 'head', -7, 15)], 3: [('iFrostS', 'head', -5, 18, _A(_FADE))]})),
 'frostArmor': ('Frost Armor', 6,
  'Frost Armor (Scorpio ninjutsu, Self buff, FORT +20% 2 rounds: the caster freezes the air round its body into a thick layer of ice armour): from the guard the fighter makes the seal at the chin, eyes closing, its breath freezing; it drops into a low braced stance, fists low at the hips, and frost spreads out over the floor round its feet while snow motes rise; the ice grows up over it: a translucent ice-blue glaze over the whole fighter and a thick, faceted ice shell round its outline (white glinting rim, ice, deep-blue edge, crystal points), drawn by the testbed from its actual equipped look; on the active frame (6) it flexes and the shell cracks into place with an ice flash and shards; it rises back into the guard still armoured (the testbed keeps the shell while the buff lasts).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(3, 3, 3), lean=(0, 1), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=FLEX_N, af=FLEX_F, bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=band(-30, -100), af=band(-30, -95), bob=(1, 1, 1), lean=(0, 1)),
     g()],
  [None, 'squint', 'closed', 'strain', 'strain', 'strain', 'roar', 'strain', None, None],
  [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
  dict(fps=10, auraColors=_WAURA,
       extra={'iceShell': {'rule': 'Frost Armor v1 (runtime, like the aura: follows the outline of whatever the fighter wears): on frame k, grow the silhouette of every drawn layer except fx by widths[k] rings of 1 px; ring 0 in colors[1] (ice, with a colors[0] glint where (x * 5 + y) % 6 == 0), middle rings in colors[2], the outermost ring in colors[3] (deep edge); from spikeFrom rings on, crystal spikes: on outer-ring pixels where (x * 7 + y * 13) % 17 == 0 (not on the bottom 5 rows) push 2 px (3 when x + y is odd) straight out, away from the figure, colors[2] with a colors[0] tip; over the figure itself blend every pixel toward colors[1] by wash[k] / 255, with facet lines: colors[0] at 1.8x the alpha where (x + y) % 7 == 0, colors[2] at 1.3x where (x - y) % 11 is 0 or 1; after the clip the testbed keeps drawing the last frame\'s shell while the buff lasts (linger). Reference implementation: hex-sprites/tools/astro_scene.py ice_shell()', 'spikeFrom': 3, 'widths': [0, 0, 0, 1, 1, 2, 3, 3, 3, 3], 'wash': [0, 0, 0, 30, 50, 70, 85, 80, 80, 80], 'colors': list(_ISHELL), 'linger': True}},
       anchored={1: [('iBreath', 'head', 5, 2, _A(_FADE))], 2: [('iBreathL', 'head', 6, 2), ('iFrost', 'feet', 0, -2)],
                 3: [('iFrostL', 'feet', -8, -5), ('iFrostL', 'feet', 8, -5), ('iSpark3', 'head', -9, 30)],
                 4: [('iFrostL', 'feet', -8, -6), ('iFrostL', 'feet', 8, -6), ('iSpark3', 'head', 9, 22), ('iFrostS', 'head', -10, 12)],
                 5: [('iFrost', 'feet', 0, -3), ('iSpark5', 'head', -8, 18), ('iFrostS', 'head', 10, 8)],
                 6: [('iSpark9', 'head', 0, 20), ('iShards12', 'head', 0, 22), ('iRing11', 'head', 0, 24)],
                 7: [('iShards12', 'head', 0, 22, _A(_FADE)), ('iSpark3', 'head', 8, 10)], 8: [('iSpark2', 'head', -7, 26)]})),
 'blizzard': ('Blizzard', 7,
  'Blizzard (Scorpio ninjutsu, Elemental 10, Wide AoE, Slow 2 rounds INT save DC 12: a charged freezing storm that slows): from the guard the fighter makes the seal, breath freezing; it sinks and circles its open palms round each other before its chest, and snow begins to whirl between them, the whirl widening into a churning ring of snow and a bright cold heart, eyes squeezed as it charges; then it drives both palms forward with a roar and the storm is hurled out: a howling wall of snow and sleet rolls over the zone and buries the targets (they play blizzardStruck from the impact frame 7); it holds the push, then lowers its hands into the guard (spec extra.zone: the testbed rolls the storm over every tile of the AoE from frame 6 and keeps it on them a few frames).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-60, -120, fistKind='palm'), af=band(-55, -115, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-45, -125, fistKind='palm'), af=band(-75, -105, fistKind='palm'), bob=(2, 2, 2), lean=(-1, -2), **LOW),
     g(an=band(-75, -105, fistKind='palm'), af=band(-45, -125, fistKind='palm'), bob=(2, 2, 2), lean=(-1, -3), **LOW),
     g(an=band(-45, -125, fistKind='palm'), af=band(-75, -105, fistKind='palm'), bob=(3, 3, 3), lean=(-1, -4), **LOW),
     g(an=band(-90, -90, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), root=(2, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(2, 2, 2), lean=(2, 5), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-90, -90, fistKind='palm'), af=band(-88, -88, fistKind='palm'), bob=(2, 2, 2), lean=(2, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -110), af=band(-40, -110), bob=(1, 1, 1), lean=(1, 2), root=(-2, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'strain', 'roar', 'roar', 'strain', None, None],
  [0, 1, 1, 1, 2, 2, 3, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, farLayer=True, rm='E: +2 driving the palms forward, -2 back',
       extra={'zone': {'rule': 'Blizzard v1: from frame 6 the testbed rolls the snowstorm (NPAT iSnowL / iSnowL2 / iSnowL3, cycling one per frame, drawn over every fighter in the Wide AoE, centred 20 px above each AoE tile) in from the caster\'s side: frame 6 half way between caster and targets (iSnow), frames 7-10 over the AoE, fading on 10 (alpha 150)', 'from': 6, 'reach': 7, 'tiles': ['iSnowL', 'iSnowL2', 'iSnowL3'], 'front': 'iSnow', 'until': 10},
              'targetFx': {'rule': 'Blizzard v1 preview of extra.zone round one target (dx away from the caster, dy from the floor up)', 'frames': {'6': [['iSnow', -24, -30]], '7': [['iSnowL', 0, -24]], '8': [['iSnowL2', 0, -24]], '9': [['iSnowL3', 0, -24]], '10': [['iSnowL', 2, -24, 150]]}},
              'targetState': {'rule': 'Blizzard: on the impact frame (7, the storm reaches the AoE) and not before, every fighter in the AoE plays blizzardStruck: frames 0-3 once, then frames 4-7 on loop while the Slow lasts, then its idle', 'state': 'blizzardStruck', 'loopFrom': 4, 'element': 'water'}},
       anchored={1: [('iBreath', 'head', 5, 2, _A(_FADE))],
                 2: [('iSwirl0', 'hand', -2, 0), ('iFrostS', 'farhand', 0, 0)],
                 3: [('iSwirl1', 'hand', -3, 0), ('iSnowS', 'hand', -2, -2, _A(_FADE)), ('iSpark2', 'hand', -3, 0)],
                 4: [('iSwirlL2', 'hand', -3, 0), ('iSwirl3', 'hand', -3, -1), ('iSpark3', 'hand', -3, 0), ('iBreath', 'head', 6, 2, _A(_FADE))],
                 5: [('iSwirlL3', 'hand', -3, 0), ('iSwirlL1', 'hand', -3, -2), ('iSnowS', 'hand', -3, 0), ('iSpark5', 'hand', -3, 0)],
                 6: [('iSnow', 'hand', 12, 0), ('iSpark5', 'hand', 2, 0), ('iRing8', 'hand', 4, 0, _A(_FADE))],
                 7: [('iSnow', 'hand', 14, 0, _A(_FADE)), ('iSnowS', 'hand', 6, 0)],
                 8: [('iSnowS', 'hand', 8, 0, _A(_FADE))]})),
 'blizzardStruck': ('Blizzard Struck', 0,
  'Blizzard Struck (target state of Blizzard, Slow 2 rounds; frame 0 is the impact): the storm hits the fighter: it throws its forearms up over its face and is driven back a step, snow plastering it; frost crusts its shoulders and arms; then, looping while the Slow lasts, it hunches with its arms wrapped round itself, shivering, teeth chattering, frozen breath puffing, frost glinting on it.', [
     g(an=band(-140, -170), af=band(-130, -165), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-140, -170), af=band(-130, -165), bob=(1, 1, 2), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-30, -150), af=band(-20, -150), bob=(2, 2, 2), lean=(1, 2), **LOW),
     g(an=band(-25, -155), af=band(-15, -155), bob=(2, 2, 3), lean=(1, 3), **LOW),
     g(an=band(-25, -155), af=band(-15, -155), bob=(2, 2, 3), lean=(1, 3), **LOW),
     g(an=band(-28, -152), af=band(-18, -152), bob=(3, 3, 3), lean=(1, 3), root=(1, 0), **LOW),
     g(an=band(-25, -155), af=band(-15, -155), bob=(2, 2, 3), lean=(1, 3), **LOW),
     g(an=band(-28, -152), af=band(-18, -152), bob=(3, 3, 3), lean=(1, 3), root=(-1, 0), **LOW)],
  ['pain', 'squint', 'strain', 'strain', 'strain', 'squint', 'strain', 'squint'],
  None,
  dict(fps=8, rm='E: -1 -1 driven back, +1 -1 shiver in the loop (the testbed walks it back when the Slow ends)', extra={'loop': True, 'loopFrom': 4},
       anchored={0: [('iSnow', 'head', 0, 18), ('iSpark5', 'head', 6, 14)],
                 1: [('iSnow', 'head', -2, 20, _A(_FADE)), ('iFrost', 'head', 2, 14)],
                 2: [('iFrostL', 'head', 0, 18), ('iBreath', 'head', 6, 4, _A(_FADE))],
                 3: [('iFrostL', 'head', 0, 18), ('iSpark2', 'head', -5, 12)],
                 4: [('iFrostL', 'head', 0, 18), ('iBreath', 'head', 6, 3), ('iSnowS', 'head', 0, -2, _A(_FADE))],
                 5: [('iFrostL', 'head', 0, 18), ('iSpark2', 'head', 5, 22)],
                 6: [('iFrostL', 'head', 0, 18), ('iBreathL', 'head', 7, 3, _A(_FADE)), ('iSnowS', 'head', 2, 0, _A(_FADE))],
                 7: [('iFrostL', 'head', 0, 18), ('iSpark2', 'head', -4, 28)]})),
})


# ---------- Scorpio (Water) genjutsu v1 (part 15, 2026-11-04): Paranoia, Betrayal ----------
def _silh(state, k, eyes=True):   # Betrayal: the illusory betrayer, a faceless shadow figure cut from an approved pose (near-black body, smoky edge, cold ice-white eyes); a generic figure, not the caster, so it is a pattern
    from PIL import Image
    d = D + state + '/'; row = load(D + state + '.json')['directions'].index('E'); m = [[0] * 64 for _ in range(64)]
    for n in ('body.png', 'far-arm.png', 'male-gi.png', 'arms.png', 'fade-hair.png'):
        if not os.path.exists(d + n): continue
        px = Image.open(d + n).convert('RGBA').load()
        for y in range(64):
            for x in range(64):
                if px[k * 64 + x, row * 64 + y][3]: m[y][x] = 1
    ys = [y for y in range(64) if any(m[y])]; xs = [x for x in range(64) if any(m[y][x] for y in range(64))]
    rows = []
    for y in range(min(ys), 64):
        r = ''
        for x in range(min(xs), max(xs) + 1):
            if not m[y][x]: r += '.'; continue
            edge = any(not (0 <= x + ex < 64 and 0 <= y + ey < 64) or not m[y + ey][x + ex] for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            r += 'x' if edge else 'X'
        rows.append(r)
    if eyes:
        ep = os.path.join(d, 'brown-eyes.png')
        if os.path.exists(ep):
            px = Image.open(ep).convert('RGBA').load()
            for y in range(64):
                for x in range(64):
                    if px[k * 64 + x, row * 64 + y][3] and y >= min(ys): rows[y - min(ys)] = rows[y - min(ys)][:x - min(xs)] + 'I' + rows[y - min(ys)][x - min(xs) + 1:]
    return rows
def _sEyes(n):   # Paranoia: a pair of eyes opening in a blot of shadow (n 0 a slit, 1 open, 2 open and glowing)
    return [['..xxxxx..', '.xXXXXXx.', 'xXIXXXIXx', '.xXXXXXx.', '..xxxxx..'], ['..xxxxx..', '.xXIXIXx.', 'xXIWXIWXx', '.xXIXIXx.', '..xxxxx..'], ['.aaxxxaa.', 'axXIXIXxa', 'xXIWXIWXx', 'axXIXIXxa', '.aaxxxaa.']][n]
NPAT.update({'sgw1': _arc(4, 2, 'xA', gap=2), 'sgw2': _arc(6, 3, 'xA', gap=2), 'sgw3': _arc(8, 4, 'XA', gap=2),
             'sEye0': _sq(_sEyes(0), 1.7, 1.7), 'sEye1': _sq(_sEyes(1), 1.7, 1.7), 'sEye2': _sq(_sEyes(2), 1.7, 1.7), 'eyeS': ['.A.', 'AIA', '.A.'], 'eyeSF': ['..A..', '.AIA.', 'AIWIA', '.AIA.', '..A..'],
             'sKnife': _sq(['.W.', '.W.', 'WIW', '.I.', '.I.', 'xxx', '.x.'], 1.7, 1.5), 'sKnifeD': _sq(['.x.', 'xxx', '.I.', '.I.', 'WIW', '.W.', '.W.'], 1.7, 1.5),
             'sFigG': _silh('mausoleum', 0), 'sFigU': _silh('mausoleum', 6), 'sFigD': _silh('mausoleum', 7)})
_SHA = lambda a: {'alpha': {'X': a, 'x': round(a * 0.75), 'I': min(255, a + 40), 'W': min(255, a + 40)}}
CLIPS.update({
 'paranoia': ('Paranoia', 7,
  'Paranoia (Scorpio genjutsu, Mental debuff, Zone of Awareness, Confusion 2 rounds STR save DC 13: the caster invokes dread and paranoia in the opponent\'s mind): from the guard the fighter lifts two fingers to its temple, eyes narrowing, and its eyes kindle cold ice-blue; shadow wisps curl up off its shoulders; it sweeps the hand out, palm open, toward the target, and dark shadow-water thought waves roll off the palm (projectile volley, frames 5 and 6, impact frame 7); it holds the palm out, then settles into the guard.', [
     g(),
     g(an=band(-140, -165, fistKind='point'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-145, -170, fistKind='point'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-145, -170, fistKind='point'), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-110, -130, fistKind='palm'), bob=(1, 1, 1), lean=(1, 1)),
     g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'squint', 'squint', 'squint', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +1 sweeping the palm out, -1 back',
       extra={'projectile': {'rule': 'Paranoia v1 (impact-frame rule): on frames 5 and 6 the testbed flies NPAT sgw3 from the near palm to the target at chest height a third of the way per frame, so the first arrives on frame 7 (the impact frame, when the target state starts) and the second on frame 8; each pops sEye1 on the target', 'volley': [{'frame': 5, 'from': 'hand', 'pattern': 'sgw3', 'hit': 'sEye1', 'flyFrames': 3}, {'frame': 6, 'from': 'hand', 'pattern': 'sgw3', 'hit': 'sEye1', 'flyFrames': 3}]},
              'targetState': {'rule': 'Paranoia: from frame 7, the impact frame, when the first wave reaches it (it holds its plain guard before that), the target plays paranoid: frames 0-3 once, then frames 4-11 on loop while the Confusion lasts, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.water) is drawn over it throughout', 'state': 'paranoid', 'loopFrom': 4, 'element': 'water'}},
       anchored={1: [('eyeS', 'eye', 0, 0)], 2: [('eyeSF', 'eye', 0, 0), ('sWispS', 'head', -6, 14, _A(_FADE))],
                 3: [('eyeSF', 'eye', 0, 0), ('sWispS', 'head', -7, 12), ('sWispS', 'head', 5, 14, _A(_FADE))],
                 4: [('eyeSF', 'eye', 0, 0), ('sgw1', 'hand', 3, 0), ('sWispS', 'head', -7, 11, _A(_FADE))],
                 5: [('eyeSF', 'eye', 0, 0), ('sgw2', 'hand', 5, 0)], 6: [('eyeSF', 'eye', 0, 0), ('sgw2', 'hand', 5, 0, _A(_FADE))],
                 7: [('eyeS', 'eye', 0, 0)]})),
 'paranoid': ('Paranoid', 0,
  'Paranoid (target state of Paranoia, Confusion 2 rounds; frame 0 is the impact): the shadow waves wash over the fighter and it flinches; shadow eyes open in the dark round it, behind its back, over its shoulder, low by its feet; it jerks its guard up high, leans back, then hunches; then (looping while the Confusion lasts) it darts its guard and weight from side to side, front then back, never settling, as pairs of shadow eyes open and close round it in new places.', [
     g(an=band(-60, -150), af=band(-50, -140), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-120, -165), af=band(-110, -160), bob=(1, 1, 1), lean=(-1, -4)),
     g(an=band(-110, -160), af=band(-100, -155), bob=(1, 1, 2), lean=(1, 2)),
     g(an=band(-70, -150), af=band(-60, -145), bob=(2, 2, 3), lean=(1, 3), root=(1, 0), **LOW),
     g(an=band(-70, -150), af=band(-60, -145), bob=(2, 2, 3), lean=(1, 3), **LOW),
     g(an=band(-110, -160), af=band(-100, -155), bob=(1, 1, 2), lean=(-1, -4), root=(-1, 0)),
     g(an=band(-110, -160), af=band(-100, -155), bob=(1, 1, 2), lean=(-1, -4)),
     g(an=band(-60, -140), af=band(-50, -135), bob=(2, 2, 2), lean=(2, 4), root=(1, 0), **LOW),
     g(an=band(-60, -140), af=band(-50, -135), bob=(2, 2, 2), lean=(2, 4), **LOW),
     g(an=band(-120, -165), af=band(-110, -160), bob=(1, 1, 1), lean=(-1, -3), root=(-1, 0)),
     g(an=band(-120, -165), af=band(-110, -160), bob=(1, 1, 1), lean=(-1, -3)),
     g(an=band(-70, -150), af=band(-60, -145), bob=(2, 2, 3), lean=(1, 3), root=(1, 0), **LOW)],
  ['pain', 'pain', 'squint', 'pain', 'squint', 'pain', 'squint', 'pain', 'squint', 'pain', 'squint', 'pain'],
  None,
  dict(fps=8, rm='E: -1 flinch, +1 hunch; loop rocks -1 +1 -1 +1 (net 0)',
       anchored={0: [('sEye1', 'head', -16, 14), ('sgw2', 'head', 6, 16, _A(_FADE))],
                 1: [('sEye2', 'head', -16, 14), ('sEye0', 'head', 14, 2)],
                 2: [('sEye1', 'head', -16, 14, _A(_FADE)), ('sEye2', 'head', 14, 2), ('sEye0', 'feet', -14, -8)],
                 3: [('sEye1', 'feet', -14, -8), ('sEye1', 'head', 15, 4, _A(_FADE))],
                 4: [('sEye2', 'feet', -14, -8), ('sEye0', 'head', -15, 2)],
                 5: [('sEye1', 'head', -15, 2), ('sEye1', 'feet', -14, -8, _A(_FADE))],
                 6: [('sEye2', 'head', -15, 2), ('sEye0', 'head', 15, 18)],
                 7: [('sEye1', 'head', -15, 2, _A(_FADE)), ('sEye2', 'head', 15, 18)],
                 8: [('sEye0', 'head', -17, 20), ('sEye1', 'head', 15, 18, _A(_FADE))],
                 9: [('sEye2', 'head', -17, 20), ('sEye0', 'feet', 14, -10)],
                 10: [('sEye1', 'head', -17, 20, _A(_FADE)), ('sEye2', 'feet', 14, -10)],
                 11: [('sEye0', 'head', -16, 14), ('sEye1', 'feet', 14, -10, _A(_FADE))]},
       extra={'loop': True, 'loopFrom': 4})),
 'betrayal': ('Betrayal', 7,
  'Betrayal (Scorpio genjutsu, Mental debuff, Zone of Awareness, Confusion 1 round INT save DC 13: the caster projects an image of the opponent\'s death at the hands of a loved one, so it trembles with fear): from the guard the fighter lays its open palm over its heart, eyes closing, and its eyes open kindled cold ice-blue; shadow gathers in the palm; it turns the palm out toward the target and the shadow-water thought waves roll off it (projectile volley, frames 5 and 6, impact frame 7); it holds, then settles into the guard.', [
     g(),
     g(an=band(-20, -160, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(an=band(-20, -160, fistKind='palm'), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-20, -160, fistKind='palm'), bob=(1, 1, 2), lean=(0, -1)),
     g(an=band(-70, -110, fistKind='palm'), bob=(1, 1, 1), lean=(1, 1)),
     g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3), root=(1, 0)),
     *[g(an=band(-92, -92, fistKind='palm'), bob=(1, 1, 1), lean=(1, 3)) for _ in range(2)],
     g(an=band(-60, -120), bob=(1, 1, 2), lean=(0, 2), root=(-1, 0)),
     g()],
  [None, 'closed', 'closed', 'squint', 'strain', 'strain', 'squint', 'squint', None, None],
  [0, 1, 1, 1, 2, 2, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: +1 turning the palm out, -1 back',
       extra={'projectile': {'rule': 'Betrayal v1 (impact-frame rule): on frames 5 and 6 the testbed flies NPAT sgw3 from the near palm to the target at chest height a third of the way per frame, so the first arrives on frame 7 (the impact frame, when the target state starts) and the second on frame 8; each pops sgw1 on the target', 'volley': [{'frame': 5, 'from': 'hand', 'pattern': 'sgw3', 'hit': 'sgw1', 'flyFrames': 3}, {'frame': 6, 'from': 'hand', 'pattern': 'sgw3', 'hit': 'sgw1', 'flyFrames': 3}]},
              'targetState': {'rule': 'Betrayal: from frame 7, the impact frame (it holds its plain guard before that), the target plays betrayed: frames 0-5 once (the vision), then frames 6-11 on loop while the Confusion lasts, then its idle; the genjutsu mark (genjutsuAfflicted, recolour genjutsuMark.recolor.water) is drawn over it throughout', 'state': 'betrayed', 'loopFrom': 6, 'element': 'water'}},
       anchored={1: [('sWispS', 'hand', 0, -4, _A(_FADE))], 2: [('sWispS', 'hand', 0, -5), ('sPool2', 'hand', 0, 0)],
                 3: [('eyeSF', 'eye', 0, 0), ('sPool2', 'hand', 0, 0), ('sWispS', 'hand', 1, -5)],
                 4: [('eyeSF', 'eye', 0, 0), ('sgw1', 'hand', 3, 0)],
                 5: [('eyeSF', 'eye', 0, 0), ('sgw2', 'hand', 5, 0)], 6: [('eyeSF', 'eye', 0, 0), ('sgw2', 'hand', 5, 0, _A(_FADE))],
                 7: [('eyeS', 'eye', 0, 0)]})),
 'betrayed': ('Betrayed', 0,
  'Betrayed (target state of Betrayal, Confusion 1 round; frame 0 is the impact): the shadow waves wash over the fighter and it stiffens; behind it a faceless shadow figure, someone it loves, rises out of the dark with cold ice-white eyes, a knife raised high in both hands; the knife plunges down at its back with a cold flash and the fighter lurches, gasping, its guard falling; the figure melts back into shadow; then (looping while the Confusion lasts) the fighter stands frozen, arms half raised and shaking, trembling all over, and the figure flickers back into sight behind it now and then.', [
     g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-50, -120), af=band(-40, -115), bob=(1, 1, 1), lean=(0, -1)),
     g(an=band(-45, -110), af=band(-35, -105), bob=(1, 1, 1), lean=(-1, -2)),
     g(an=band(-30, -70), af=band(-20, -60), bob=(1, 1, 2), lean=(2, 5), root=(1, 0)),
     g(an=band(-25, -60), af=AR_HANG_F, bob=(2, 2, 2), lean=(1, 4)),
     g(an=band(-35, -100), af=band(-25, -90), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g(an=band(-40, -110), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1)),
     g(an=band(-43, -113), af=band(-33, -103), bob=(2, 2, 2), lean=(0, 2)),
     g(an=band(-40, -110), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1), root=(1, 0)),
     g(an=band(-43, -113), af=band(-33, -103), bob=(2, 2, 2), lean=(0, 2)),
     g(an=band(-40, -110), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g(an=band(-43, -113), af=band(-33, -103), bob=(2, 2, 2), lean=(0, 2))],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'squint', 'pain', 'squint', 'pain', 'squint'],
  None,
  dict(fps=10, rm='E: +1 lurching at the stab, -1 back; loop shakes +1 -1 (net 0)',
       anchored={0: [('sFigG', 'feet', -15, 0, {**_SHA(110), 'behind': True, 'bottom': 63}), ('sgw2', 'head', 6, 16, _A(_FADE))],
                 1: [('sFigG', 'feet', -15, 0, {**_SHA(210), 'behind': True, 'bottom': 63}), ('sWisp', 'feet', -15, -5, _A(_FADE))],
                 2: [('sFigU', 'feet', -15, 0, {**_SHA(235), 'behind': True, 'bottom': 63}), ('sKnife', 'head', -15, -9)],
                 3: [('sFigD', 'feet', -14, 0, {**_SHA(235), 'behind': True, 'bottom': 63}), ('sKnifeD', 'head', -9, 14), ('iSpark7', 'head', -6, 18), ('iShards9', 'head', -6, 18, _A(_FADE))],
                 4: [('sFigD', 'feet', -14, 0, {**_SHA(120), 'behind': True, 'bottom': 63}), ('sWisp2', 'feet', -14, -8), ('iFrostS', 'head', -5, 18)],
                 5: [('sWisp2', 'feet', -14, -8, _A(_FADE)), ('sPool6', 'feet', -14, -1)],
                 6: [('sPool4', 'feet', -14, -1, _A(_FADE))],
                 8: [('sFigG', 'feet', -15, 0, {**_SHA(70), 'behind': True, 'bottom': 63})],
                 9: [('sFigG', 'feet', -15, 0, {**_SHA(120), 'behind': True, 'bottom': 63})],
                 10: [('sFigG', 'feet', -15, 0, {**_SHA(60), 'behind': True, 'bottom': 63})]},
       extra={'loop': True, 'loopFrom': 6})),
})


# Blizzard v2 (Christopher 2026-11-04 21:03: it is an ultimate: more frames for dramatic effect, more exaggerated fx): 16 frames (the renderer's cap), a long charge inside a snow vortex, a white flash, then a cone of storm hurled from both palms; impact frame 11
def _snowCone(w, h, seed, n):   # a blast of snow and sleet fanning out to the right from a point at the left middle, densest along the axis
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]; c = (h - 1) / 2
    for _ in range(n):
        x = int(w * rnd.random() ** 0.7); half = 1 + c * x / w; y = round(c + rnd.uniform(-half, half) * rnd.random() ** 0.5)
        L = rnd.choice((1, 2, 3, 3, 4))
        for t in range(L + 1):
            X, Y = x - t * 2, y + round(t * (y - c) / max(1, x) * 2)
            if 0 <= X < w and 0 <= Y < h: rows[Y][X] = 'W' if t == 0 else 'I' if t < 2 else 'a'
    return [''.join(q) for q in rows]
def _haze(w, h, seed):   # a whiteout: sparse ice-white mist pixels, thicker low down
    import random
    rnd = random.Random(seed); rows = [['.'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if rnd.random() < 0.10 + 0.18 * y / h: rows[y][x] = 'I' if rnd.random() < 0.7 else 'W'
    return [''.join(q) for q in rows]
def _round(pat, seed, core=0.55):   # thin a square pattern out to a ragged round cloud: full inside core, fading to nothing at the ellipse edge
    import random
    rnd = random.Random(seed); h, w = len(pat), len(pat[0]); out = []
    for y, r in enumerate(pat):
        q = ''
        for x, ch in enumerate(r):
            d = math.hypot((x - (w - 1) / 2) / (w / 2), (y - (h - 1) / 2) / (h / 2))
            q += ch if ch != '.' and (d < core or (d < 1 and rnd.random() < (1 - d) / (1 - core))) else '.'
        out.append(q)
    return out
NPAT.update({**{'iHelixF%d' % p: _helix(17, 52, p, strands=4, turns=2.2) for p in range(4)}, **{'iHelixB%d' % p: _helix(17, 52, p, front=False, strands=4, turns=2.2) for p in range(4)},
             'iCone': _snowCone(31, 25, 1, 110), 'iCone2': _snowCone(31, 25, 2, 110), 'iConeL': _snowCone(41, 33, 3, 190),
             'iSnowXL': _round(_snow(61, 58, 6, 380, 3), 1), 'iSnowXL2': _round(_snow(61, 58, 7, 380, 3), 2), 'iSnowXL3': _round(_snow(61, 58, 8, 380, 3), 3), 'iHaze': _round(_haze(61, 58, 9), 4, 0.4), 'iFloorFrost': _frost(41, 5, 10, 60)})
_HZ = {'alpha': {'I': 110, 'W': 140}}
_BW = {'alpha': {'W': 200, 'I': 170, 'a': 150, 'A': 140}}
_BP = lambda a, f: band(a, f, fistKind='palm')
CLIPS['blizzard'] = ('Blizzard', 11,
  'Blizzard v2 (Scorpio ninjutsu ultimate, Elemental 10, Wide AoE, Slow 2 rounds INT save DC 12: a charged freezing storm that slows; Christopher 2026-11-04: an ultimate, more frames, exaggerated fx): from the guard the fighter makes the seal and its breath freezes; frost spreads over the floor round its feet; it sinks into a wide stance and circles its open palms round each other before its chest, and snow whirls up out of nowhere, a churning ring between the palms; the whirl grows into a howling vortex of snow spiralling round its whole body, the aura blazing ice-blue, the cold heart between its palms swelling; it drags its palms apart and the charge bursts in a white flash and a ring of ice; then it drives both palms forward with a roar and a huge cone of storm is hurled out of them; the wall of snow and sleet rolls over the zone, a whiteout swallowing the targets (they play blizzardStruck from the impact frame 11); it holds the push as the storm rages, then lowers its hands and settles into the guard (spec extra.zone: the testbed rolls the storm over every tile of the AoE).', [
     g(),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(1, 1, 1), lean=(0, 0)),
     g(an=U.SEAL_N, af=U.SEAL_F, bob=(2, 2, 2), lean=(0, 1), **LOW),
     g(an=_BP(-60, -120), af=_BP(-55, -115), bob=(2, 2, 2), lean=(0, 0), **LOW),
     g(an=_BP(-45, -125), af=_BP(-75, -105), bob=(3, 3, 3), lean=(-1, -2), **LOW),
     g(an=_BP(-75, -105), af=_BP(-45, -125), bob=(3, 3, 3), lean=(-1, -2), **LOW),
     g(an=_BP(-45, -125), af=_BP(-75, -105), bob=(3, 3, 3), lean=(-1, -3), **LOW),
     g(an=_BP(-75, -105), af=_BP(-45, -125), bob=(3, 3, 4), lean=(-1, -3), **LOW),
     g(an=_BP(-60, -120), af=_BP(-60, -115), bob=(4, 4, 4), lean=(-1, -4), **LOW),
     g(an=_BP(-100, -100), af=_BP(-20, -60), bob=(2, 2, 2), lean=(-1, -3)),
     g(an=_BP(-90, -90), af=_BP(-88, -88), bob=(2, 2, 2), lean=(2, 6), root=(3, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_BP(-90, -90), af=_BP(-88, -88), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_BP(-90, -90), af=_BP(-88, -88), bob=(2, 2, 3), lean=(2, 7), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=_BP(-90, -90), af=_BP(-88, -88), bob=(2, 2, 2), lean=(2, 6), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-50, -110), af=band(-40, -110), bob=(1, 1, 1), lean=(1, 2), root=(-3, 0)),
     g()],
  [None, 'squint', 'closed', 'squint', 'strain', 'strain', 'strain', 'strain', 'strain', 'roar', 'roar', 'roar', 'roar', 'strain', 'squint', None],
  [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1, 0],
  dict(fps=10, auraColors=_WAURA, farLayer=True, rm='E: +3 driving the palms forward, -3 back',
       extra={'zone': {'rule': 'Blizzard v2: from frame 10 the testbed rolls the snowstorm in from the caster\'s side: frame 10 the front gust half way between caster and targets (iConeL); from frame 11 (impact) to 15 over every fighter in the Wide AoE, centred 26 px above each AoE tile: iHaze (alpha I 110, W 140) under iSnowXL / iSnowXL2 / iSnowXL3 cycling one per frame, with iShards12 bursting on frame 11 and iSpark5 glints; frame 15 fades (alpha 150)', 'from': 10, 'reach': 11, 'tiles': ['iSnowXL', 'iSnowXL2', 'iSnowXL3'], 'haze': 'iHaze', 'front': 'iConeL', 'until': 15},
              'targetFx': {'rule': 'Blizzard v2 preview of extra.zone round one target (dx away from the caster, dy from the floor up)', 'frames': {'10': [['iConeL', -30, -30]], '11': [['iHaze', 0, -27, 130], ['iSnowXL', 0, -27], ['iShards12', 0, -30]], '12': [['iHaze', 0, -27, 130], ['iSnowXL2', 0, -27], ['iSpark5', 8, -40]], '13': [['iHaze', 0, -27, 130], ['iSnowXL3', 0, -27]], '14': [['iHaze', 0, -27, 120], ['iSnowXL', 0, -27], ['iSpark5', -8, -20]], '15': [['iHaze', 0, -27, 80], ['iSnowXL2', 0, -27, 150]]}},
              'targetState': {'rule': 'Blizzard v2: on the impact frame (11, the storm reaches the AoE) and not before, every fighter in the AoE plays blizzardStruck: frames 0-3 once, then frames 4-7 on loop while the Slow lasts, then its idle', 'state': 'blizzardStruck', 'loopFrom': 4, 'element': 'water'}},
       anchored={1: [('iBreath', 'head', 5, 2, _A(_FADE))],
                 2: [('iBreathL', 'head', 6, 2), ('iFrost', 'feet', 0, -2)],
                 3: [('iSwirl0', 'hand', -3, 0), ('iFloorFrost', 'feet', 0, -2, _A(_FADE)), ('iSnowS', 'hand', -2, -2, _A(_FADE))],
                 4: [('iSwirl1', 'hand', -3, 0), ('iFloorFrost', 'feet', 0, -2), ('iHelixB0', 'feet', 0, -26, {'behind': True, **_A(_FADE)}), ('iSpark2', 'hand', -3, 0)],
                 5: [('iSwirlL2', 'hand', -3, 0), ('iFloorFrost', 'feet', 0, -2), ('iHelixB1', 'feet', 0, -26, {'behind': True}), ('iHelixF1', 'feet', 0, -26, _A(_FADE)), ('iSpark3', 'hand', -3, 0)],
                 6: [('iSwirlL3', 'hand', -3, 0), ('iFloorFrost', 'feet', 0, -2), ('iHelixB2', 'feet', 0, -26, {'behind': True}), ('iHelixF2', 'feet', 0, -26, _BW), ('iSpark3', 'hand', -3, 0), ('iSnowS', 'head', -10, 8)],
                 7: [('iSwirlL0', 'hand', -3, 0), ('iSwirl1', 'hand', -3, -1), ('iFloorFrost', 'feet', 0, -2), ('iHelixB3', 'feet', 0, -26, {'behind': True}), ('iHelixF3', 'feet', 0, -26, _BW), ('iSpark5', 'hand', -3, 0), ('iSnowS', 'head', 10, 12)],
                 8: [('iSwirlL1', 'hand', -3, 0), ('iSwirlL3', 'hand', -3, -2), ('iFloorFrost', 'feet', 0, -2), ('iHelixB0', 'feet', 0, -26, {'behind': True}), ('iHelixF0', 'feet', 0, -26, _BW), ('iSpark7', 'hand', -3, 0), ('iSnow', 'head', 0, 14, _A(_FADE))],
                 9: [('iSpark9', 'head', 4, 22), ('iRing11', 'head', 4, 22), ('iShards12', 'head', 4, 22), ('iFloorFrost', 'feet', 0, -2), ('iHelixB1', 'feet', 0, -26, {'behind': True, **_A(_FADE)})],
                 10: [('iConeL', 'hand', 18, 0), ('iSpark7', 'hand', 2, 0), ('iRing8', 'hand', 4, 0), ('iFloorFrost', 'feet', 0, -2)],
                 11: [('iConeL', 'hand', 20, 0), ('iCone', 'hand', 13, 0), ('iSpark5', 'hand', 2, 0), ('iFloorFrost', 'feet', 0, -2)],
                 12: [('iConeL', 'hand', 20, 0, _BW), ('iCone2', 'hand', 13, 0), ('iFloorFrost', 'feet', 0, -2)],
                 13: [('iCone', 'hand', 14, 0, _A(_FADE)), ('iFloorFrost', 'feet', 0, -2, _A(_FADE))],
                 14: [('iSnowS', 'hand', 8, 0, _A(_FADE))]}))
_BS = CLIPS['blizzardStruck']
CLIPS['blizzardStruck'] = (_BS[0], _BS[1], _BS[2].replace('Blizzard Struck (', 'Blizzard Struck v2 (exaggerated fx; ').replace('snow plastering it;', 'snow plastering it, ice shards bursting round it;'), _BS[3], _BS[4], _BS[5],
  {**_BS[6], 'anchored': {0: [('iSnow', 'head', 0, 18), ('iSpark9', 'head', 6, 16), ('iShards12', 'head', 4, 18), ('iRing11', 'head', 4, 20)],
                          1: [('iSnow', 'head', -2, 20), ('iShards12', 'head', 0, 18, _A(_FADE)), ('iFrostL', 'head', 2, 14), ('iFrostL', 'head', -3, 24)],
                          2: [('iFrostL', 'head', 0, 18), ('iFrostL', 'head', -2, 30), ('iBreath', 'head', 6, 4, _A(_FADE)), ('iFloorFrost', 'feet', 0, -2)],
                          3: [('iFrostL', 'head', 0, 18), ('iFrostL', 'head', -2, 30), ('iSpark3', 'head', -5, 12), ('iFloorFrost', 'feet', 0, -2)],
                          4: [('iFrostL', 'head', 0, 18), ('iFrostL', 'head', -2, 30), ('iBreathL', 'head', 6, 3), ('iFloorFrost', 'feet', 0, -2)],
                          5: [('iFrostL', 'head', 0, 18), ('iFrostL', 'head', -2, 30), ('iSpark3', 'head', 5, 22), ('iFloorFrost', 'feet', 0, -2)],
                          6: [('iFrostL', 'head', 0, 18), ('iFrostL', 'head', -2, 30), ('iBreathL', 'head', 7, 3, _A(_FADE)), ('iFloorFrost', 'feet', 0, -2)],
                          7: [('iFrostL', 'head', 0, 18), ('iFrostL', 'head', -2, 30), ('iSpark3', 'head', -4, 28), ('iFloorFrost', 'feet', 0, -2)]}})

# Blizzard v3 (Christopher 2026-11-04 21:10: a caster-centred AoE of radius 3, and the fx must show it): the charge is kept; on frame 9 the charge bursts and the
# caster flings its arms out wide, and the storm erupts from it and races outward ring by ring (hex ring 1 on frame 10, 2 on 11, 3 on 12), then rages round
# the caster, who stands in the calm eye; the storm is drawn by the testbed (extra.zone), not baked, because it is far wider than a cell
_B2 = CLIPS['blizzard']; _BF = list(_B2[3])
_OUT = dict(an=band(-100, -130, fistKind='palm'), af=band(60, 95, fistKind='palm'))
_BF[10:14] = [g(**_OUT, bob=(3, 3, 3), lean=(0, -2), **LOW), g(**_OUT, bob=(3, 3, 3), lean=(0, -3), **LOW), g(**_OUT, bob=(3, 3, 4), lean=(0, -3), **LOW), g(**_OUT, bob=(2, 2, 3), lean=(0, -2), **LOW)]
_BF[14] = g(an=band(-50, -110), af=band(-40, -110), bob=(1, 1, 1), lean=(0, 1))
_BA = {k: v for k, v in _B2[6]['anchored'].items() if k < 9}
_BA.update({9: [('iSpark9', 'head', 4, 22), ('iRing11', 'feet', 0, -2), ('iShards12', 'head', 4, 22), ('iFloorFrost', 'feet', 0, -2)],
            10: [('iSpark7', 'hand', 0, 0), ('iSpark7', 'farhand', 0, 0), ('iRing11', 'feet', 0, -2, _A(_FADE)), ('iFloorFrost', 'feet', 0, -2), ('iHelixB2', 'feet', 0, -26, {'behind': True, **_A(_FADE)})],
            11: [('iSpark5', 'hand', 0, 0), ('iSpark5', 'farhand', 0, 0), ('iFloorFrost', 'feet', 0, -2), ('iSnowS', 'hand', 2, 0)],
            12: [('iSpark3', 'hand', 0, 0), ('iSpark3', 'farhand', 0, 0), ('iFloorFrost', 'feet', 0, -2)],
            13: [('iFloorFrost', 'feet', 0, -2, _A(_FADE))]})
_BX = dict(_B2[6]['extra']); _BX.pop('targetFx', None)
_BX['zone'] = {'rule': 'Blizzard v3 (Christopher 2026-11-04 21:10: caster-centred AoE, radius 3): selfCentered, no aim point. From frame 10 the testbed draws the storm erupting from the caster and racing outward hex ring by hex ring (front at ring 1 on frame 10, ring 2 on 11, ring 3 on 12, reaching (radius + 0.5) * hexStep * sqrt(3) on the floor, ry half of rx), a churning white front of driven snow at its edge; after that it rages round the caster and LINGERS (v3.1, Christopher 2026-11-04 22:05: the snow lingers for the duration of the ability): it stays on the AoE hexes it was cast on, looping, for zone.rounds rounds (the Slow\'s 2 rounds), and only fades out (over 0.5 s) when those rounds end: snow and sleet streaks circling the caster (counter-clockwise seen from above), 2-50 px above the floor, back half behind the fighters and front half over them, an ice-white haze over the whole disc, frost on the floor, and a calm eye (no snow within 20 px of the caster). v3.2 (Christopher 2026-11-04 22:09: diamond flash fx mixed in with the snow particles): about 150 diamond-dust glints whirl with the snow (same orbit as the flakes, 4-46 px up); each flashes 3 frames of every 6 at its own phase: a small diamond (white centre, 2 px arms, ice diagonals), then a white-hot star (arms 3-5 px: white, ice #dff6ff, light water #7cc8ff tip; white diagonals and light-water outer diagonal tips), then the small diamond again. Reference: hex-sprites/tools/astro_storm.py DIA. Each fighter in the AoE on the cast plays blizzardStruck from the frame the front passes its hex (ring 1 frame 10, ring 2 frame 11, ring 3 frame 12). Reference preview: hex-sprites/tools/astro_storm.py', 'selfCentered': True, 'radius': 3, 'rounds': 2, 'linger': True, 'anchor': 'cast hex', 'from': 10, 'ringFrames': {'1': 10, '2': 11, '3': 12}, 'eye': 20, 'colors': ['#ffffff', '#dff6ff', '#7cc8ff', '#2f7fe0']}
_BX['targetState'] = {**_BX['targetState'], 'rule': 'Blizzard v3: each fighter in the radius-3 AoE plays blizzardStruck from the frame the storm front reaches its hex (ring 1 frame 10 = the active frame, ring 2 frame 11, ring 3 frame 12) and not before: frames 0-3 once, then frames 4-7 on loop while the Slow lasts, then its idle'}
CLIPS['blizzard'] = ('Blizzard', 10, _B2[2].replace('Blizzard v2 (', 'Blizzard v3 (caster-centred AoE radius 3, Christopher 2026-11-04 21:10; ').replace('then it drives both palms forward with a roar and a huge cone of storm is hurled out of them; the wall of snow and sleet rolls over the zone, a whiteout swallowing the targets (they play blizzardStruck from the impact frame 11); it holds the push as the storm rages', 'then it flings its arms out wide with a roar and the storm erupts from it in every direction, racing outward ring by ring to three hexes, a whiteout swallowing everyone in it (each plays blizzardStruck as the front reaches it), while the caster stands in the calm eye; it holds the pose as the storm rages round it'),
  _BF, _B2[4], [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 1, 0], {**_B2[6], 'rm': 'E: 0 (it stands in the eye)', 'extra': _BX, 'anchored': _BA})

# Betrayal v2 (Christopher 2026-11-05 14:39: refine the shadow, add a knife to its silhouette, have it stab the target in the back several times, then the
# target turns round in shock before turning back to face the caster): the betrayer is cut from the approved Numbing Strikes poses (frame 1 loaded, frame 5
# thrust) with a shadow knife in its near hand; three stabs; the target turns through S to face where the shadow stood (rows swapped: extra.awayFrames), then back
def _silhK(state, k, L=8):   # the shadow figure with a knife held forward in the near hand: a dark blade (smoky edge) with an ice-white cutting edge and tip
    from PIL import Image
    d = D + state + '/'; row = load(D + state + '.json')['directions'].index('E'); m = [[0] * 64 for _ in range(64)]; eye = set()
    for n in ('body.png', 'far-arm.png', 'male-gi.png', 'arms.png', 'fade-hair.png'):
        if not os.path.exists(d + n): continue
        px = Image.open(d + n).convert('RGBA').load()
        for y in range(64):
            for x in range(64):
                if px[k * 64 + x, row * 64 + y][3]: m[y][x] = 1
    ap = Image.open(d + 'arms.png').convert('RGBA').load()
    arm = [(x, y) for y in range(64) for x in range(64) if ap[k * 64 + x, row * 64 + y][3]]
    hx, hy = max(arm, key=lambda q: (q[0], -q[1]))
    ep = d + 'brown-eyes.png'
    if os.path.exists(ep):
        px = Image.open(ep).convert('RGBA').load(); eye = {(x, y) for y in range(64) for x in range(64) if px[k * 64 + x, row * 64 + y][3]}
    knife = {}
    knife[(hx + 1, hy)] = 'x'; knife[(hx + 1, hy + 1)] = 'x'   # the grip in the fist, a guard
    knife[(hx + 1, hy - 1)] = 'x'
    for t in range(2, L + 2):
        if hx + t < 64:
            knife[(hx + t, hy)] = 'W' if t >= L else 'x'; knife[(hx + t, hy - 1)] = 'W' if t < L - 1 else 'I' if t < L else '.'   # smoky blade with an ice-white cutting edge and tip
            if t < L - 2: knife[(hx + t, hy + 1)] = 'X'   # the blade's dark back
    allx = [x for y in range(64) for x in range(64) if m[y][x]] + [x for (x, y), c in knife.items() if c != '.']
    ys = [y for y in range(64) if any(m[y])] + [y for (x, y) in knife]
    x0, x1, y0 = min(allx), max(allx), min(ys); rows = []
    for y in range(y0, 64):
        r = ''
        for x in range(x0, x1 + 1):
            if (x, y) in knife and knife[(x, y)] != '.': r += knife[(x, y)]; continue
            if not m[y][x]: r += '.'; continue
            if (x, y) in eye: r += 'I'; continue
            edge = any(not (0 <= x + ex < 64 and 0 <= y + ey < 64) or not m[y + ey][x + ex] for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            r += 'x' if edge else 'X'
        rows.append(r)
    return rows, (x0 + x1) / 2 - 32   # rows, the pattern centre's offset from the cell centre (so the feet stay put)
_PK1, _OK1 = _silhK('numbingStrike', 1, 7); _PK5, _OK5 = _silhK('numbingStrike', 5, 5)   # the blade buried in the back on the thrust (only the hilt shows)
NPAT.update({'sFigK1': _PK1, 'sFigK5': _PK5, 'sFigG2': _silh('numbingStrike', 0)})
def _fig(pat, a, dx=-21):   # the betrayer, feet on the floor behind the target (dx from the target's feet, toward its facing); the knife pose is centred on its own box, so shift back by its offset
    off = {'sFigK1': _OK1, 'sFigK5': _OK5 - 8}.get(pat, 0)   # the thrust pose stands further back, so the fist stops at the target's back
    return (pat, 'feet', round(dx + off), 0, {**_SHA(a), 'behind': True, 'bottom': 63})
_SHK = band(-140, -170)   # forearms flung up in shock
CLIPS['betrayed'] = ('Betrayed', 0,
  'Betrayed v2 (target state of Betrayal, Confusion 1 round; frame 0 is the impact; Christopher 2026-11-05: a knife in the shadow\'s silhouette, several stabs in the back, the target turns round in shock, then back to the caster): the shadow waves wash over the fighter and it stiffens; behind it a faceless shadow figure, someone it loves, rises out of the dark with cold ice-white eyes and a shadow knife in its hand; it drives the knife into the fighter\'s back three times, the fighter jolting forward with a cold flash and ice shards at each stab; the figure melts back into shadow; the fighter whirls round in shock to face where it stood, forearms up, trembling, finds only a pool of shadow; it turns back to face the caster, and then (looping while the Confusion lasts) stands frozen and trembling, arms half raised and shaking, the figure flickering faintly behind it.', [
     g(an=band(-55, -125), af=band(-45, -120), bob=(1, 1, 1), lean=(0, -1)),                                   # 0 impact: stiffens
     g(an=band(-50, -120), af=band(-40, -115), bob=(1, 1, 1), lean=(0, -1)),                                   # 1 the figure rises, knife drawn back
     g(an=band(-30, -70), af=band(-20, -60), bob=(1, 1, 2), lean=(2, 5), root=(1, 0)),                         # 2 stab 1
     g(an=band(-35, -85), af=band(-25, -80), bob=(1, 1, 1), lean=(1, 2)),                                      # 3 knife drawn back
     g(an=band(-25, -60), af=band(-15, -55), bob=(1, 1, 2), lean=(2, 6)),                                      # 4 stab 2
     g(an=band(-35, -85), af=band(-25, -80), bob=(1, 1, 1), lean=(1, 3)),                                      # 5 drawn back
     g(an=band(-20, -50), af=AR_HANG_F, bob=(2, 2, 2), lean=(3, 8)),                                           # 6 stab 3, the deepest
     g(an=band(-25, -60), af=AR_HANG_F, bob=(2, 2, 2), lean=(2, 5), root=(-1, 0)),                             # 7 gasping, the figure melts
     g(an=_SHK, af=_SHK, bob=(1, 1, 1), lean=(0, 0)),                                                          # 8 turning round (S)
     g(an=_SHK, af=band(-130, -165), bob=(1, 1, 1), lean=(-1, -3)),                                            # 9 facing where the shadow stood, in shock
     g(an=band(-130, -160), af=band(-125, -160), bob=(1, 1, 2), lean=(-1, -2)),                                # 10 trembling, looking
     g(an=_SHK, af=_SHK, bob=(1, 1, 1), lean=(0, 0)),                                                          # 11 turning back (S)
     g(an=band(-40, -110), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1)),                                    # 12 facing the caster again
     g(an=band(-43, -113), af=band(-33, -103), bob=(2, 2, 2), lean=(0, 2), root=(1, 0)),                       # 13-15 trembling loop
     g(an=band(-40, -110), af=band(-30, -100), bob=(1, 1, 2), lean=(0, 1), root=(-1, 0)),
     g(an=band(-43, -113), af=band(-33, -103), bob=(2, 2, 2), lean=(0, 2))],
  ['squint', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'pain', 'squint', 'pain', 'squint', 'pain'],
  None,
  dict(fps=10, rm='E: +1 jolted at the first stab, -1 gasping; loop shakes +1 -1 (net 0)', front={8: dict(R=stances.GA['R'], L=stances.GA['L']), 11: dict(R=stances.GA['R'], L=stances.GA['L'])},
       awayFrames=[9, 10],
       extra={'loop': True, 'loopFrom': 13, 'awayFrames': {'rule': 'Betrayal v2: on frames 9-10 the fighter faces away from its facing (it has turned round to look behind it, through the S frame 8, and turns back through S on 11): the E row holds the W-facing figure and the W row the E-facing one (only the figure layers are swapped; fx stays where it is drawn)', 'frames': [9, 10]}},
       anchored={0: [('sgw2', 'head', 6, 16, _A(_FADE)), ('sWisp', 'feet', -21, -5, _A(_FADE))],
                 1: [('sWispS', 'feet', -21, -3, _A(_FADE))],
                 2: [('iSpark7', 'head', -6, 18), ('iShards9', 'head', -7, 18)],
                 3: [('iFrostS', 'head', -5, 18)],
                 4: [('iSpark7', 'head', -6, 22), ('iShards9', 'head', -7, 22), ('iFrostS', 'head', -5, 18)],
                 5: [('iFrost', 'head', -5, 20)],
                 6: [('iSpark9', 'head', -6, 20), ('iShards12', 'head', -8, 20), ('iRing8', 'head', -6, 20), ('iFrost', 'head', -5, 20)],
                 7: [('sWisp2', 'feet', -21, -8), ('iFrost', 'head', -5, 20)],
                 8: [('sPool6', 'feet', 0, -1), ('sWispS', 'feet', 0, -4, _A(_FADE))],
                 9: [('sPool6', 'feet', -21, -1), ('sWispS', 'feet', -21, -4, _A(_FADE))],
                 10: [('sPool4', 'feet', -21, -1, _A(_FADE))]}))
# Betrayal v2.1 (Christopher 2026-11-05 14:56: no eyes on the shadow, and the silhouette is the target's own): the betrayer is no longer baked; the testbed draws it from the TARGET's own equipped sprite (the copies rule)
_BT = CLIPS['betrayed']
CLIPS['betrayed'] = (_BT[0], _BT[1], _BT[2].replace('Betrayed v2 (', 'Betrayed v2.1 (the shadow is the target\'s own silhouette, no eyes, Christopher 2026-11-05 14:56; ').replace('a faceless shadow figure, someone it loves, rises out of the dark with cold ice-white eyes and a shadow knife in its hand', 'its own shadow, a faceless, eyeless silhouette of itself wearing exactly what it wears, rises out of the dark with a shadow knife in its hand'),
  _BT[3], _BT[4], _BT[5],
  {**_BT[6], 'extra': {**_BT[6]['extra'], 'shadowDouble': {'rule': 'Betrayal v2.1 (Christopher 2026-11-05 14:56: no eyes, the silhouette is the target\'s own): drawn by the testbed, nothing baked. On each listed frame k, take the TARGET\'s own composited sprite (every equipped layer: body, clothing or armour, arms, far arm, shoulders, hair or helmet, weapons; no eyes, no fx) in the source state and frame [src, srcFrame], facing the target\'s own facing, and fill it as a flat shadow: #120d16 inside, #3a2f40 on its 1 px outer edge, no eyes or features; draw it dx px from the target\'s feet along its facing (negative = behind it), only where the target itself is not drawn, at alpha. knife > 0: a shadow knife in the near fist (the arms layer\'s most forward pixel): grip/guard #3a2f40 1 px ahead of the fist, then a blade knife px long running forward (#3a2f40 body, #12-0d16 back row under it, #ffffff cutting edge on the row above, #ffffff tip). Reference implementation: hex-sprites/tools/astro_scene.py shadow_double()'.replace('#12-0d16', '#120d16'),
      'frames': {'0': ['numbingStrike', 0, -21, 120, 0], '1': ['numbingStrike', 1, -21, 225, 7], '2': ['numbingStrike', 5, -29, 235, 5], '3': ['numbingStrike', 1, -21, 235, 7], '4': ['numbingStrike', 5, -29, 235, 5], '5': ['numbingStrike', 1, -21, 235, 7], '6': ['numbingStrike', 5, -29, 240, 5], '7': ['numbingStrike', 1, -21, 130, 7], '14': ['numbingStrike', 0, -21, 70, 0], '15': ['numbingStrike', 0, -21, 45, 0]}}}})

# ---------- Pisces (Water) taijutsu v1 (part 15, 2026-11-05): Evasive Sway, Slide Counter, Flow Strike ----------
# Pisces colours: water and ice (W, I, a, A, n); the sign's two fish circle the fighter as koi of water
def _koi(flip=False):   # a small fish of water swimming right: ice-white head, light body, deep fins and a forked tail
    p = ['...aa...', 'IWaaaA.n', '.IaaaAnn', '...AA..n']
    return [r[::-1] for r in p] if flip else p
def _ribbon(L, amp, phase, cols='WIa'):   # a ribbon of flowing water L px long: a sine streak, bright at the head (right), thinning to drops
    h = 2 * amp + 3; rows = [['.'] * L for _ in range(h)]
    for x in range(L):
        y = round(amp + 1 + amp * math.sin(x * 0.45 + phase)); u = x / max(1, L - 1)
        if u < 0.25 and x % 2: continue
        rows[y][x] = cols[0] if u > 0.8 else cols[1] if u > 0.45 else cols[2]
        if u > 0.3 and y + 1 < h: rows[y + 1][x] = 'A' if u < 0.7 else 'a'
    return [''.join(q) for q in rows]
NPAT.update({'pKoi': _sq(_koi(), 1.7, 1.7), 'pKoiB': _sq(_koi(True), 1.7, 1.7), **{'pRib%d' % p: _ribbon(16, 3, p * 1.6) for p in range(4)}, **{'pRibL%d' % p: _ribbon(28, 4, p * 1.6) for p in range(4)},
             'pRibB': _flipx(_ribbon(16, 3, 0)), 'pRibBL': _flipx(_ribbon(28, 4, 1.6)), 'pSlick': _sq(NPAT['wPuddle'], 3.0, 1.2), 'pWakeF': _flipx(NPAT['wWakeL'])})
def _orbit(k, n=8, rx=16, ry=4, dy=26):   # Evasive Sway: the two koi circling the fighter's waist half a turn apart, one turn every n frames; behind on the far side
    out = []
    for i, ph in enumerate((0, 0.5)):
        a = 2 * math.pi * (k / n + ph); x = round(rx * math.cos(a)); y = dy + round(ry * math.sin(a))
        nm = 'pKoi' if math.sin(a) > 0 else 'pKoiB'   # front half swims toward the facing, far half away
        out.append((nm, 'head', x, y, {} if math.sin(a) > 0 else {'behind': True}))
    return out
_SW = lambda d: dict(an=band(15 if d < 0 else -35, -30 if d < 0 else -70, fistKind='palm'), af=band(-35 if d < 0 else 10, -70 if d < 0 else -30, fistKind='palm'))
CLIPS.update({
 'evasiveSway': ('Evasive Sway', 3,
  'Evasive Sway (Pisces taijutsu stance buff, AGI +50% 2 rounds: the fighter focuses its mind to feel formless and fluid like water): from the guard the fighter lets its fists open and its guard melt down low and loose, eyes closing; water wells up round it and two koi of water slip out and circle its waist, half a turn apart (the two fish of Pisces); then it sways from side to side like weed in a current, boneless and easy, open hands trailing ribbons of water; it opens its eyes, still swaying, and settles back into the guard, the koi diving away (the testbed may keep the koi circling while the buff lasts: extra.linger).', [
     g(),
     g(an=band(-10, -40, fistKind='palm'), af=band(-20, -50, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)),
     g(**_SW(-1), bob=(2, 2, 3), lean=(-1, -6), root=(-2, 0), **LOW),
     g(an=band(5, -40, fistKind='palm'), af=band(-25, -60, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(**_SW(1), bob=(2, 2, 3), lean=(1, 7), root=(2, 0), **LOW),
     g(an=band(-25, -60, fistKind='palm'), af=band(0, -40, fistKind='palm'), bob=(1, 1, 1), lean=(0, 1)),
     g(**_SW(-1), bob=(2, 2, 3), lean=(-1, -6), root=(-2, 0), **LOW),
     g(an=band(5, -40, fistKind='palm'), af=band(-25, -60, fistKind='palm'), bob=(1, 1, 1), lean=(0, 0)),
     g(**_SW(1), bob=(2, 2, 3), lean=(1, 7), root=(2, 0), **LOW),
     g(an=band(-40, -110), af=band(-50, -120), bob=(2, 2, 2), lean=(0, 2)),
     g()],
  [None, 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'closed', 'squint', None, None],
  [0, 1, 1, 2, 1, 2, 1, 2, 1, 1, 0],
  dict(fps=8, auraColors=_WAURA, rm='sways 2 px back and forward on the beat (net 0)',
       extra={'linger': {'rule': 'Evasive Sway v1 (proposal): while the AGI buff lasts the testbed keeps the two koi (NPAT pKoi / pKoiB) circling the fighter\'s waist, half a turn apart, one turn every 8 frames on an ellipse rx 16 ry 4 about 26 px below the top of the head (front half over the fighter swimming toward its facing, far half behind it swimming away)', 'patterns': ['pKoi', 'pKoiB'], 'rx': 16, 'ry': 4, 'period': 8}},
       anchored={1: [('wDrops', 'feet', 0, -6, _A(_FADE)), ('wPuddle', 'feet', 0, -1, _A(_FADE))],
                 2: _orbit(2) + [('pRibB', 'hand', -9, 2), ('wPuddle', 'feet', 0, -1)],
                 3: _orbit(3) + [('pRib1', 'farhand', -6, 2, _A(_FADE)), ('wPuddle', 'feet', 0, -1)],
                 4: _orbit(4) + [('pRibBL', 'hand', -12, 2), ('wPuddle', 'feet', 0, -1)],
                 5: _orbit(5) + [('pRib2', 'hand', -6, 2, _A(_FADE)), ('wPuddle', 'feet', 0, -1)],
                 6: _orbit(6) + [('pRibB', 'farhand', -9, 2), ('wPuddle', 'feet', 0, -1)],
                 7: _orbit(7) + [('pRib3', 'hand', -6, 2, _A(_FADE)), ('wPuddle', 'feet', 0, -1)],
                 8: _orbit(8) + [('pRibBL', 'hand', -12, 2), ('wPuddle', 'feet', 0, -1)],
                 9: [('wSplashS', 'head', 12, 28, _A(_FADE)), ('wSplashS', 'head', -12, 28, _A(_FADE)), ('wPuddle', 'feet', 0, -1, _A(_FADE))]})),
 'slideCounter': ('Slide Counter', 5,
  'Slide Counter (Pisces taijutsu stance, counter, +6 m move: the fighter slips aside and repositions): from the guard the fighter drops low and water spreads into a slick under its feet; it slips back across the slick in one long frictionless slide, low and side-on, a wake curling off its lead foot; it plants, sinks into a low counter stance with both open hands out in front, water circling the palms, ready to turn the next attack, then rises into the guard (travel 22 px back; the testbed moves it to the chosen hex and keeps the counter stance hint).', [
     g(),
     g(an=band(-40, -110), af=band(-30, -105), bob=(3, 3, 3), lean=(0, 2), **LOW),
     g(an=band(-30, -100), af=band(-20, -95), bob=(4, 4, 4), lean=(-1, -2), root=(-7, 0), **LOW),
     g(an=band(-30, -100), af=band(-20, -95), bob=(4, 4, 4), lean=(-1, -3), root=(-8, 0), **LOW),
     g(an=band(-35, -105), af=band(-25, -100), bob=(4, 4, 4), lean=(-1, -2), root=(-5, 0), **LOW),
     g(an=band(-60, -100, fistKind='palm'), af=band(-80, -130, fistKind='palm'), bob=(4, 4, 4), lean=(1, 3), root=(-2, 0), **BRACE),
     g(an=band(-60, -100, fistKind='palm'), af=band(-80, -130, fistKind='palm'), bob=(4, 4, 4), lean=(1, 3), **BRACE),
     g(an=band(-55, -110), af=band(-45, -115), bob=(2, 2, 2), lean=(0, 1)),
     g()],
  [None, 'squint', 'squint', 'squint', 'squint', 'strain', 'squint', None, None],
  [0, 0, 1, 1, 1, 2, 1, 0, 0],
  dict(fps=10, auraColors=_WAURA, rm='E: -7 -8 -5 -2 sliding back (travel 22 px back)',
       anchored={1: [('wPuddle', 'feet', 0, -1), ('wDrops', 'feet', 4, -5, _A(_FADE))],
                 2: [('pSlick', 'feet', 4, -1), ('pWakeF', 'feet', 12, -3), ('wDrops', 'feet', 14, -8, _A(_FADE))],
                 3: [('pSlick', 'feet', 6, -1), ('pWakeF', 'feet', 13, -3), ('wSplashS', 'feet', 12, -5)],
                 4: [('pSlick', 'feet', 4, -1, _A(_FADE)), ('pWakeF', 'feet', 10, -3, _A(_FADE)), ('wDrops', 'feet', 10, -6)],
                 5: [('wPuddle', 'feet', 0, -1), ('wRing', 'hand', 0, 0), ('wRing', 'farhand', 0, 0, _A(_FADE)), ('wSplashS', 'feet', -5, -4)],
                 6: [('wPuddle', 'feet', 0, -1, _A(_FADE)), ('wRing2', 'hand', 0, 0, _A(_FADE)), ('wDrops', 'hand', 0, 2, _A(_FADE))]})),
 'flowStrike': ('Flow Strike', 5,
  'Flow Strike (Pisces taijutsu, True 14, Melee, bypasses poise and mitigation: the fighter throws a strike that evades the opponent\'s defences by being hard to track): from the guard the fighter ripples, its weight rolling one way then the other like water, the lead hand snaking in an S, a ribbon of water following its path; it dips under the line of the guard and the rear fist flows up through the gap like water through cupped hands, landing on the chin on the impact frame (5) in a splash and a ripple that passes straight through the target; the target\'s guard never moves (flowStruck); the fighter flows back out into the guard.', [
     g(),
     g(af=band(-40, -90), bob=(2, 2, 2), lean=(-1, -3), root=(1, 0), **LOW),
     g(af=band(-80, -120), bob=(2, 2, 3), lean=(1, 4), root=(1, 0), **LOW),
     g(af=band(-50, -95), an=band(10, -60), bob=(4, 4, 4), lean=(2, 7), root=(1, 0), ln='sp-load-rear', lf='sp-load-lead'),
     g(af=band(-50, -110), an=band(-60, -130), bob=(3, 3, 3), lean=(2, 6), root=(1, 0), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(af=band(-50, -110), an=band(-100, -120), bob=(1, 1, 2), lean=(2, 4), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(af=band(-50, -110), an=band(-100, -120), bob=(1, 1, 2), lean=(1, 3), ln='sp-drive-rear', lf='sp-drive-lead'),
     g(an=band(-40, -110), bob=(1, 1, 1), lean=(0, 1), root=(-2, 0)),
     g(root=(-2, 0)),
     g()],
  [None, 'squint', 'squint', 'strain', 'strain', 'roar', 'strain', None, None, None],
  [0, 1, 1, 1, 2, 2, 1, 0, 0, 0],
  dict(fps=12, auraColors=_WAURA, farLayer=True, hitbox=[42, 14, 14, 12], damage='heavy', rm='E: +1 +1 +1 +1 flowing in, -2 -2 back (net 0)',
       extra={'targetState': {'rule': 'Flow Strike: on the impact frame (5, the active frame) and not before, the target plays flowStruck once (its guard stays up: the strike went round it), then its idle', 'state': 'flowStruck'}},
       anchored={1: [('pRib0', 'farhand', -8, 1, _A(_FADE))],
                 2: [('pRibL1', 'farhand', -12, 2), ('wDrops', 'farhand', -6, 4, _A(_FADE))],
                 3: [('pRibL2', 'farhand', -12, 3, _A(_FADE)), ('pRibB', 'hand', -6, 2)],
                 4: [('pRibL3', 'hand', -12, 3), ('wOrb2', 'hand', 0, 0)],
                 5: [('wSplashL', 'hand', 6, -2), ('wRing3', 'hand', 4, 0), ('wRing2', 'hand', 2, 0), ('pRibL0', 'hand', -12, 4, _A(_FADE))],
                 6: [('wDropsL', 'hand', 6, 2, _A(_FADE)), ('wRing3', 'hand', 7, 0, _A(_FADE))]})),
 'flowStruck': ('Flow Struck', 0,
  'Flow Struck (target state of Flow Strike, plays once; frame 0 is the impact): the fist lands on the chin past its guard, which never moves: its head snaps back, a splash bursts off its chin and a ripple of water runs straight through its body and out of its back; it staggers a step with the guard still up, shakes its head and resets.', [
     g(bob=(1, 1, 1), lean=(-2, -6), root=(-1, 0)),
     g(bob=(1, 1, 2), lean=(-2, -5), root=(-1, 0)),
     g(bob=(1, 1, 1), lean=(-1, -3)),
     g(bob=(1, 1, 1), lean=(0, -1), root=(1, 0)),
     g(root=(1, 0))],
  ['pain', 'pain', 'squint', 'squint', None],
  None,
  dict(fps=12, rm='E: -1 -1 staggering, +1 +1 resetting (net 0)',
       anchored={0: [('wSplash', 'head', 5, 6), ('wRip7', 'head', 0, 18), ('iSpark5', 'head', 4, 6)],
                 1: [('wRip9', 'head', -3, 20, _A(_FADE)), ('wJetB', 'head', -14, 18), ('wDrops', 'head', 4, 4)],
                 2: [('wRip12', 'head', -6, 22, _A(_FADE)), ('wDrops', 'head', -10, 16, _A(_FADE))]})),
})


# Evasive Sway v2 (Christopher 2026-11-05 15:04: the animation needs a rework; the fx are fine): no more side-to-side rocking; a slow, boneless
# wave like water: the fighter sinks, its weight rolls back and forward in a smooth wave from the knees up through the shoulders, and its open
# hands trace continuous circles in front of it, half a turn apart (tai chi "cloud hands"), the water ribbons following the palms and the koi circling
def _cloud(k, n=8):
    import math as _m
    t = 2 * _m.pi * k / n
    near = band(round(-55 + 35 * _m.sin(t)), round(-95 + 30 * _m.cos(t)), fistKind='palm')
    far = band(round(-55 + 35 * _m.sin(t + _m.pi)), round(-95 + 30 * _m.cos(t + _m.pi)), fistKind='palm')
    lx = round(2 * _m.sin(t)); lean = (lx // 2, lx * 2)
    bob = 3 + round(_m.cos(t))
    return g(an=near, af=far, bob=(bob, bob, bob + 1), lean=lean, **LOW)
_EV = CLIPS['evasiveSway']
_EVF = [g(), g(an=band(-30, -80, fistKind='palm'), af=band(-25, -75, fistKind='palm'), bob=(1, 1, 2), lean=(0, 0)), g(an=band(-45, -95, fistKind='palm'), af=band(-40, -90, fistKind='palm'), bob=(2, 2, 3), lean=(0, 0), **LOW)] + [_cloud(k) for k in range(8)] + [g(an=band(-40, -110), af=band(-50, -120), bob=(2, 2, 2), lean=(0, 1)), g()]
_EVA = {1: [('wDrops', 'feet', 0, -6, _A(_FADE)), ('wPuddle', 'feet', 0, -1, _A(_FADE))], 2: [('wPuddle', 'feet', 0, -1), ('wRing', 'hand', 0, 0, _A(_FADE))]}
for k in range(8):
    f = k + 3
    _EVA[f] = _orbit(f) + [('wPuddle', 'feet', 0, -1), ('pRibB' if k % 2 else 'pRibBL', 'hand', -9, 2), ('pRibB' if k % 2 == 0 else 'pRibBL', 'farhand', -9, 2, _A(_FADE))] + ([('wRip5', 'feet', 0, -2, _A(_FADE))] if k % 4 == 0 else [])
_EVA[11] = [('wSplashS', 'head', 12, 28, _A(_FADE)), ('wSplashS', 'head', -12, 28, _A(_FADE)), ('wPuddle', 'feet', 0, -1, _A(_FADE))]
CLIPS['evasiveSway'] = (_EV[0], 3, _EV[2].replace('Evasive Sway (', 'Evasive Sway v2 (motion reworked, Christopher 2026-11-05; ').replace('then it sways from side to side like weed in a current, boneless and easy, open hands trailing ribbons of water;', 'then it sinks into a slow, boneless wave: its weight rolls back and forward from the knees up through the shoulders like a swell, and its open hands trace unbroken circles before it, half a turn apart, ribbons of water following the palms;'),
  _EVF, [None, 'closed', 'closed'] + ['closed'] * 8 + ['squint', None], [0, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 0],
  {**_EV[6], 'fps': 8, 'rm': 'E: 0 (it stays on its spot)', 'anchored': _EVA})

# Flow Strike v2 (Christopher 2026-11-05 15:05: the impact fx must be more dramatic): an XL water burst, ice-white shards, a double pressure ring and a white flash on the fist; the target gets a big splash on the chin, water blasting out of the back of its head and a triple ripple through the body
_FS = CLIPS['flowStrike']
CLIPS['flowStrike'] = (_FS[0], _FS[1], _FS[2].replace('Flow Strike (', 'Flow Strike v2 (dramatic impact fx; '), _FS[3], _FS[4], _FS[5],
  {**_FS[6], 'anchored': {**_FS[6]['anchored'],
      5: [('wSplashXL', 'hand', 8, -4), ('iSpark9', 'hand', 3, 0), ('iShards12', 'hand', 5, 0), ('wRing3', 'hand', 4, 0), ('iRing11', 'hand', 4, 0), ('pRibL0', 'hand', -12, 4, _A(_FADE))],
      6: [('wSplashL', 'hand', 9, -3, _A(_FADE)), ('iShards12', 'hand', 8, 2, _A(_FADE)), ('wDropsL', 'hand', 8, 4), ('iRing11', 'hand', 7, 0, _A(_FADE))],
      7: [('wDropsL', 'feet', 12, -10, _A(_FADE)), ('wPuddle', 'feet', 12, -1)]}})
_FT = CLIPS['flowStruck']
CLIPS['flowStruck'] = (_FT[0], _FT[1], _FT[2].replace('Flow Struck (', 'Flow Struck v2 (dramatic impact fx; '), _FT[3], _FT[4], _FT[5],
  {**_FT[6], 'anchored': {0: [('wSplashL', 'head', 5, 6), ('iSpark7', 'head', 4, 6), ('iShards9', 'head', 4, 6), ('wRip7', 'head', 0, 18), ('wJetBL', 'head', -18, 4)],
                          1: [('wRip9', 'head', -3, 20), ('wRip5', 'head', 0, 26, _A(_FADE)), ('wJetBL', 'head', -20, 5, _A(_FADE)), ('wDropsL', 'head', -10, 2)],
                          2: [('wRip12', 'head', -6, 22, _A(_FADE)), ('wDropsL', 'head', -14, 10, _A(_FADE)), ('wPuddle', 'feet', -4, -1)],
                          3: [('wPuddle', 'feet', -4, -1, _A(_FADE))]}})

def spec(state):
    U.CLIPS[state] = CLIPS[state]
    U.APPROVED[state] = APPROVED.get(state, STAT)
    U.spec(state)
    x = CLIPS[state][6]; s = load(D + state + '.json')
    for k, v in (x.get('extra') or {}).items(): s[k] = v
    if x.get('runtimeClones'):
        s['clones'] = {'rule': 'Christopher 2026-11-03 19:22: copies of the caster must wear whatever the caster wears, so they are not baked into fx: on each listed frame the testbed draws the caster\'s own composited current frame (every equipped layer, no fx) again dx px toward its facing (negative = behind), washed toward #e9eef4 by wash (default 0.35), outlined 1 px in rim when given, at alpha, only where the caster itself is not drawn; frames {k: [[dx, alpha, wash, rim]]}', 'frames': {str(k): [list(i) for i in v] for k, v in x['clones'].items()}}
    if CLIPS[state][5] and os.environ.get('AURA_BAKE') != '1':   # runtime aura (Christopher 2026-11-03 19:28: auras follow the hair outline); same record grstrikes.aura writes
        s['aura'] = {'rule': 'Runtime aura (Christopher 2026-11-03: all auras follow the outline of the hair): on frame k, when widths[k] > 0, the testbed grows the silhouette of every drawn layer except fx (body, clothing or armour, arms, shoulders, hair or helmet, eyes, weapons) by widths[k] rings of 1 px (4-neighbour / 3x3 max growth); ring 0 in colors[0], the others in colors[1]; the outermost ring only on pixels where (x + y + k) is even (flicker); drawn behind the fighter, only outside its silhouette', 'widths': list(CLIPS[state][5]), 'colors': list(x.get('auraColors') or ('#ffffff', '#e3e3e3'))}
    if x.get('farLayer'): s['arms']['farLayer'] = True   # the far arm in its own far-arm sheet (Flowing Sand Parry v2: its hand is tracked for the sand trail)
    if x.get('shapes'): s['expressions']['shapes'].update(copy.deepcopy(x['shapes']))
    if x.get('front') or {'roar', 'strain'} & set(CLIPS[state][4]):   # roar/strain faces (S shapes used by the turn, E for all)
        s['expressions']['shapes']['roar'] = {'E': copy.deepcopy(s['expressions']['shapes']['pain']['E']),
            'S': [[0, 1, '#000000'], [1, 1, '#000000'], [5, 1, '#000000'], [6, 1, '#000000'], [2, 3, '#000000'], [3, 3, '#000000'], [4, 3, '#000000'], [2, 4, '#000000'], [3, 4, '#70241d'], [4, 4, '#000000']]}   # eyes squeezed, mouth open in a yell (mid-face, clear of the chin)
        s['expressions']['shapes']['strain'] = {'E': copy.deepcopy(s['expressions']['shapes']['pain']['E']),
            'S': [[0, 1, '#000000'], [1, 1, '#000000'], [5, 1, '#000000'], [6, 1, '#000000'], [2, 4, '#000000'], [3, 4, '#000000'], [4, 4, '#000000']]}   # eyes squeezed, teeth clenched
    if x.get('front'):   # the fighter turns to face S for part of the clip (Blast Wave v2): every facing plays the S frames there
        s['facingOverride'] = {'rule': 'Christopher 2026-10-27: the fighter turns to face S (toward the viewer) for these frames whatever its facing; every row holds the S frame there (the rows are copied after the render), then it turns back', 'frames': sorted(x['front']), 'to': 'S'}
    save(s, D + state + '.json')
    if x.get('front'):
        import universal_sn as USN
        USN.SN[state] = x['front']; USN.sn(state)

def fx(state):
    x = CLIPS[state][6]
    if x.get('invert'): invert(state, x['invert'])
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
    if x.get('front') and CLIPS[state][5] and os.environ.get('AURA_BAKE') == '1': U.aura(state)   # (baked mode only; runtime auras need no redraw) the aura again, round the turned (S) figure
    if x.get('burst'):
        if x.get('burstEvery'):   # the spiked aura drawn on each facing's own row (the fighter keeps its facing)
            for i, r_ in enumerate(load(D + state + '.json')['directions']): burst(state, x['burst'], row=r_, spread=False, clean=i == 0)
        else: burst(state, x['burst'])
    if x.get('tint'): flush(state, x['tint'], x.get('veins', ()), *x.get('tintColors', ()))
    if x.get('hairTo'): hair_to(state, x['hairTo'])
    if x.get('meteor'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        meteor(state, x['meteor'])
    if x.get('swirl') or x.get('impact') or x.get('blast'):
        from PIL import Image
        f = D + state + '/fx.png'
        if not os.path.exists(f) or 'fx' not in load(D + state + '.json'): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f)   # no splash fx: start clean (not a stale render)
        if x.get('swirl'): swirl(state, x['swirl'])
        if x.get('impact'): impact(state, x['impact'])
        if x.get('blast'): blast(state, x['blast'])
    if x.get('awayFrames'): away(state, x['awayFrames'])
    if x.get('anchored'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_) or ('fx' not in load(D + state + '.json') and not CLIPS[state][5] and not x.get('keepFx')): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)   # clean start unless the aura was just drawn (keepFx: keep the arm swirl / impact drawn above; Sun Palm's approved render predates it)
        anchored(state, x['anchored'])
        if x.get('waterArms'): water_arms(state, x['waterArms'])
        if x.get('crystal'): crystalize(state, x['crystal'])
        if x.get('trails'): trails(state, x['trails'])
        if x.get('front'):   # turned frames: every row shows the E row's fx (drawn round the same S figure)
            fx_ = Image.open(f_).convert('RGBA'); dirs_ = load(D + state + '.json')['directions']; re_ = dirs_.index('E')
            for k in x['front']:
                cell = fx_.crop((k * 64, re_ * 64, k * 64 + 64, re_ * 64 + 64))
                for r_ in range(len(dirs_)):
                    if r_ != re_: fx_.paste(cell, (k * 64, r_ * 64))
            fx_.save(f_)
    if x.get('mask'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        mask(state, x['mask'], x.get('maskWaves'))
    if x.get('spinFire'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        spinFire(state, x['spinFire'])
    if x.get('kanaboRise'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        kanaboRise(state, x['kanaboRise'])
    if x.get('topFire'):
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_) or 'fx' not in load(D + state + '.json'): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        topFire(state, x['topFire'])
    if any(x.get(n) for n in ('rays', 'beam', 'cone', 'gather', 'nova', 'flare')):   # Leo sunlight fx, drawn over what is already there
        from PIL import Image
        f_ = D + state + '/fx.png'
        if not os.path.exists(f_) or ('fx' not in load(D + state + '.json') and not CLIPS[state][5] and not x.get('anchored')): Image.new('RGBA', Image.open(D + state + '/body.png').size).save(f_)
        for n in ('gather', 'nova', 'flare', 'rays', 'beam', 'cone'):
            if x.get(n): globals()[n](state, x[n])
    if x.get('clones') and not x.get('runtimeClones'): clones(state, x['clones'])   # v2 (Christopher 2026-11-03 19:22): runtimeClones = the testbed draws them from the caster's own sprite, nothing baked
    if x.get('legion'): legion(state, x['legion'])
    if x.get('ghosts'):
        from PIL import Image
        f = D + state + '/fx.png'; top = Image.open(f).convert('RGBA')   # blur + splash so far
        ghosts(state, x['ghosts'], x['ghostColors'])
        g_ = Image.open(f).convert('RGBA'); g_.alpha_composite(top); g_.save(f)   # streaks and flames stay over the afterimages
    if x.get('recolor'):   # fire-drawn helpers (swirl, impact) re-coloured for another element: {'#rrggbb': '#rrggbb'}
        from PIL import Image
        f_ = D + state + '/fx.png'; im = Image.open(f_).convert('RGBA'); px = im.load()
        m = {_hexc(a)[:3]: _hexc(b)[:3] for a, b in x['recolor'].items()}
        for yy in range(im.size[1]):
            for xx in range(im.size[0]):
                q = px[xx, yy]
                if q[3] and q[:3] in m: px[xx, yy] = m[q[:3]] + (q[3],)
        im.save(f_); print(state, 'recolor', len(m))
    if x.get('dissolve'): dissolve(state, x['dissolve'])   # last: the anchors above need the whole figure (re-render before re-running --fx)

def invert(state, frames):
    """Spinning Top: the rig has no upside-down pose, so these frames are drawn upright (hands up by the head, legs down in
    a V) and every figure layer's cell is turned over (rotated 180 degrees: two quarter turns) after the render, the head
    set on the floor. A 180 turn also mirrors the facing, so each row takes the opposite row's cell (it then faces its own
    way); frames = {k: back} with back=1 taking its own row's cell instead (seen from behind mid-spin), or {k: (1, -90)}
    for a quarter turn (the dive onto the head and the roll back out: the body laid flat, head toward the facing, on the
    floor; W turns the other way). Runs once per render
    (a marker holds the turned body.png's hash)."""
    from PIL import Image
    import hashlib
    d = D + state + '/'; mk = d + '.inverted'
    h_ = lambda: hashlib.md5(open(d + 'body.png', 'rb').read()).hexdigest()
    if os.path.exists(mk) and open(mk).read() == h_(): return
    dirs = load(D + state + '.json')['directions']; body = Image.open(d + 'body.png').convert('RGBA')
    shift = {}
    for k, back in frames.items():
        for r in range(len(dirs)):
            back_, deg = back if isinstance(back, tuple) else (back, 180)
            if deg != 180 and dirs[r] == 'W': deg = -deg
            src = r if back_ else (len(dirs) - 1 - r if set(dirs) == {'E', 'W'} else r)
            b = body.crop((k * 64, src * 64, k * 64 + 64, src * 64 + 64)).rotate(deg); bb = b.getbbox()
            dx = 0 if deg == 180 else 32 - (bb[0] + bb[2]) // 2
            shift[k, r] = (src, deg, dx, 63 - bb[3] + 1)   # the lowest body row (the head's top when turned over) rests on row 63
    for f in os.listdir(d):
        if not f.endswith('.png') or f == 'fx.png': continue
        im = Image.open(d + f).convert('RGBA'); src_im = im.copy()
        for (k, r), (src, deg, dx, dy) in shift.items():
            cell = src_im.crop((k * 64, src * 64, k * 64 + 64, src * 64 + 64)).rotate(deg)
            out = Image.new('RGBA', (64, 64)); out.paste(cell, (dx, dy))
            im.paste(out, (k * 64, r * 64))
        im.save(d + f)
    open(mk, 'w').write(h_()); print(state, 'invert', sorted(frames))

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
def flush(state, tint, veins, col=(0xff, 0x3a, 0x1a), vcol=(0x7a, 0x14, 0x0c), streak=None, moss=None):   # col/vcol: tint and vein colours (Oak Flesh: bark brown, dark grain); streak: bark grain streak colour (Oak Flesh v3)
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
                for (x, y) in skin: px[k * 64 + x, r * 64 + y] = tuple(col) + (al,)
                if streak:   # Oak Flesh v3 (Christopher 2026-10-28: read on the darkest skin tone): wavy vertical grain streaks over the bark, face clear
                    ty = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                    for (x, y) in skin:
                        if (x + y // 3) % 3 == 0: px[k * 64 + x, r * 64 + y] = tuple(streak) + (al,)   # v6: streaks run over the face too
                if moss:   # Oak Flesh v5 (Christopher 2026-10-28: all three colours combined): 2 px patches of moss on the bark, face clear
                    ty = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                    for (x, y) in skin:
                        if not (ty + 2 < y < ty + 11) and ((x // 2) * 5 + (y // 2) * 11) % 7 == 0: px[k * 64 + x, r * 64 + y] = tuple(moss) + (al,)
                if k not in veins or not skin: continue
                top_y = min(y for _, y in skin) if out == 'skin-fx.png' else -99
                for (x, y) in skin:
                    if top_y + 2 < y < top_y + 11:   # head: a short vein at the temple only, the face stays clean
                        if y in (top_y + 3, top_y + 4) and (x + y) % 3 == 0 and (x - 1, y) in skin and (x + 1, y) in skin: px[k * 64 + x, r * 64 + y] = tuple(vcol) + (255,)
                        continue
                    across = ((x - 1, y) in skin and (x + 1, y) in skin and (x - 2, y) not in skin | {(x, y)}) or ((x, y - 1) in skin and (x, y + 1) in skin)
                    # a vein runs down the middle of each limb's cross-section (arms, neck), broken every few pixels
                    mid = (x - 1, y) in skin and (x + 1, y) in skin if (x, y - 1) in skin and (x, y + 1) in skin else (x, y - 1) in skin and (x, y + 1) in skin
                    if mid and (x * 3 + y) % 5 != 0: px[k * 64 + x, r * 64 + y] = tuple(vcol) + (255,)
        img.save(d + out)
    print(state, 'flush', list(tint), 'veins', list(veins))

HAIR_LAYERS = ('afro-hair', 'afro-puff', 'bantu-knots', 'braided-side', 'fade-hair', 'flat-top', 'locs-loose', 'locs-tied', 'long-hair', 'modern-topknot', 'ronin-ponytail')
def hair_to(state, spec):   # Oak Flesh v6 (Christopher 2026-10-28: change the hair to the moss): every hair style's base ramp swapped on the given frames
    from PIL import Image
    d = D + state + '/'; m = {_hexc(a)[:3]: _hexc(b)[:3] for a, b in spec['map'].items()}
    for n in HAIR_LAYERS:
        f = d + n + '.png'
        if not os.path.exists(f): continue
        im = Image.open(f).convert('RGBA'); px = im.load()
        for k in spec['frames']:
            for yy in range(im.size[1]):
                for xx in range(k * 64, k * 64 + 64):
                    q = px[xx, yy]
                    if q[3] and q[:3] in m: px[xx, yy] = m[q[:3]] + (q[3],)
        im.save(f)
    print(state, 'hair', spec['frames'])

def away(state, frames):   # Betrayal v2: the fighter has turned round on these frames: swap the E and W rows of every figure layer (fx untouched)
    from PIL import Image
    d = D + state + '/'; dirs = load(D + state + '.json')['directions']; e, w = dirs.index('E'), dirs.index('W')
    for n in sorted(os.listdir(d)):
        if not n.endswith('.png') or n == 'fx.png': continue
        im = Image.open(d + n).convert('RGBA')
        if im.height < 64 * len(dirs): continue
        for k in frames:
            a = im.crop((k * 64, e * 64, k * 64 + 64, e * 64 + 64)); b = im.crop((k * 64, w * 64, k * 64 + 64, w * 64 + 64))
            im.paste(b, (k * 64, e * 64)); im.paste(a, (k * 64, w * 64))
        im.save(d + n)
    print(state, 'away (rows swapped)', frames)

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

def burst(state, frames, row='S', spread=True, clean=True):
    """Blast Wave v2 (facing S): embers gathering round the crouched fighter (stages 0-1), then the release: a spiked fire
    aura round the whole figure (inner yellow glow, flame spikes radiating out, longer at the release) and sonic-boom rings
    blasting out round it, white-hot, then yellow, orange, red as they widen and break up (stages 2-5). Drawn on the S row
    and copied to every row (all rows show the S frame there)"""
    import math, random
    from PIL import Image, ImageFilter
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']; rs = dirs.index(row)
    base = Image.open(d + 'body.png'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) and ('fx' in load(D + state + '.json') or not clean) else Image.new('RGBA', base.size)   # no splash fx: start clean
    if fx.size != base.size: n_ = Image.new('RGBA', base.size); n_.paste(fx, (0, 0)); fx = n_
    px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    lay = [Image.open(d + n).convert('RGBA') for n in FIG_LAYERS if os.path.exists(d + n)]   # v2 (2026-11-03): the widest outline of any look (see OUTFIT_LAYERS)
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
    for k in (frames if spread else ()):   # every row shows the S frame here
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(f); print(state, 'burst', frames)

def meteor(state, frames):
    """Meteor: a fireball forming above the raised hands ('form', radius), roiling (yellow core, orange body, red rim,
    flame licks off the top); then hurled ('fly', step): it streaks up and away toward the target's side of the sky with a
    tapering fire trail back to the hands, leaving embers ('trail')"""
    import math, random
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    fx = Image.open(f).convert('RGBA'); px = fx.load()
    hexc = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W_, Y, O, R_ = (255, 255, 255, 255), hexc(ELEMENT['Y']), hexc(ELEMENT['O']), hexc(ELEMENT['R'])
    def ball(k, r, cx, cy, rad, sg, rnd):
        for y in range(-rad - 3, rad + 1):
            for x in range(-rad - 1, rad + 2):
                dd = (x * x + y * y) ** 0.5
                X, Y_ = cx + sg * x, cy + y
                if not (0 <= X < 64 and 0 <= Y_ < 64): continue
                if dd <= rad:
                    c = W_ if dd < rad * 0.3 else Y if dd < rad * 0.6 else O if dd < rad - 0.8 else R_
                    if rad >= 4 and Y is c and rnd.random() < 0.2: c = O   # roiling
                    px[k * 64 + X, r * 64 + Y_] = c
                elif y < 0 and dd <= rad + 2 and rnd.random() < 0.35: px[k * 64 + X, r * 64 + Y_] = R_ if rnd.random() < 0.5 else O   # licks off the top
    for k, (kind, n) in frames.items():
        for fd in dirs:
            r = dirs.index(fd); sg = -1 if fd == 'W' else 1; rnd = random.Random(k * 13 + r)
            pts = _arm(state, 3, r); top = min(pts, key=lambda p: p[1]); hx = top[0]; hy = top[1]   # the raised palm (frame 3)
            if kind == 'form': ball(k, r, hx + sg, hy - min(n, 5) - 1, n, 1, rnd)   # big ones run off the top of the frame: too big for the sky
            elif kind == 'flash':   # the launch: the fireball at its biggest, lit white, light rays out from it
                ball(k, r, hx + sg * 3, hy - 6, 11, 1, rnd)
                for t in range(0, 360, 30):
                    th = math.radians(t)
                    for i in range(12, 20):
                        X, Y_ = round(hx + sg * 3 + i * math.cos(th)), round(hy - 6 + i * math.sin(th))
                        if 0 <= X < 64 and 0 <= Y_ < 64: px[k * 64 + X, r * 64 + Y_] = Y if i < 16 else O
            else:
                cx = hx + sg * (10 + 11 * n); cy = max(1, hy - 4 - 4 * n); rad = max(3, 9 - 2 * n)
                for t in range(0, 60):   # the trail back toward the hands, tapering
                    u = t / 60; tx = round(hx + sg * 4 + (cx - hx - sg * 4) * u); ty = round(hy + 4 + (cy - hy - 4) * u)
                    w = int(u * (5 if kind == 'fly' else 3))
                    for dy in range(-w, w + 1):
                        X, Y_ = tx, ty + dy
                        if 0 <= X < 64 and 0 <= Y_ < 64 and (kind != 'trail' or rnd.random() < 0.3) and rnd.random() < 0.4 + 0.5 * u:
                            px[k * 64 + X, r * 64 + Y_] = R_ if u < 0.4 else O if u < 0.75 else Y
                if kind == 'fly': ball(k, r, cx, cy, rad, sg, rnd)
                for i in range(8 + 6 * n):   # embers shed along the way, raining back down
                    X = hx + sg * rnd.randint(-6, 30); Y_ = rnd.randint(2, 20 + 10 * n)
                    if 0 <= X < 64: px[k * 64 + X, r * 64 + Y_] = (O, R_, Y)[i % 3]
    fx.save(f); print(state, 'meteor', list(frames))

def trails(state, t):   # Flowing Sand Parry v2: streams of sand following each open hand along its circle; t = {'near': frames, 'far': frames, 'len': n}
    """the hand of each arm (the arm pixel farthest from the chest) is found on every frame; on the listed frames a sand stream is
    drawn back along the hand's path through the last len frames (bent outward from the chest, so the stream follows the circle)"""
    from PIL import Image
    import random
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']; n = load(D + state + '.json')['frames']
    body = Image.open(d + 'body.png').convert('RGBA').load(); fx = Image.open(f).convert('RGBA'); px = fx.load()
    lay = {'near': Image.open(d + 'arms.png').convert('RGBA').load(), 'far': Image.open(d + 'far-arm.png').convert('RGBA').load()}
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    for r, fd in enumerate(dirs):
        if fd not in ('E', 'W'): continue
        for side in ('near', 'far'):
            tips = []
            for k in range(n):
                opq = [(x, y) for y in range(64) for x in range(64) if body[k * 64 + x, r * 64 + y][3]]
                top = min(y for _, y in opq); hx = sum(x for x, y in opq if y <= top + 9) / max(1, sum(1 for x, y in opq if y <= top + 9))
                chest = (hx, top + 17); L = lay[side]
                arm = [(x, y) for y in range(64) for x in range(64) if L[k * 64 + x, r * 64 + y][3]]
                tips.append((max(arm, key=lambda q: (q[0] - chest[0]) ** 2 + (q[1] - chest[1]) ** 2) if arm else None, chest))
            rnd = random.Random(r * 7 + (side == 'far'))
            for k in t[side]:
                pts = [tips[q] for q in range(max(0, k - t['len']), k + 1) if tips[q][0]]
                for i in range(len(pts) - 1):
                    (x0, y0), c0 = pts[i]; (x1, y1), _ = pts[i + 1]; age = len(pts) - 1 - i   # 1 = the newest stretch
                    a0 = math.atan2(y0 - c0[1], x0 - c0[0]); a1 = math.atan2(y1 - c0[1], x1 - c0[0])
                    if a1 - a0 > math.pi: a1 -= 2 * math.pi
                    if a0 - a1 > math.pi: a1 += 2 * math.pi
                    r0 = math.hypot(x0 - c0[0], y0 - c0[1]); r1 = math.hypot(x1 - c0[0], y1 - c0[1])
                    for u in range(13):
                        q = u / 12; a = a0 + (a1 - a0) * q; rr = r0 + (r1 - r0) * q
                        X = round(c0[0] + rr * math.cos(a)); Y = round(c0[1] + rr * math.sin(a))
                        if not (0 <= X < 64 and 0 <= Y < 64) or rnd.random() < 0.15 * age: continue
                        if any(L_[k * 64 + X, r * 64 + Y][3] for L_ in (body, lay['near'], lay['far'])) and side == 'far': continue   # the far arm's stream passes behind the body
                        cz = t.get('cols', 'ZSs'); ch = cz[0] if rnd.random() < 0.15 else cz[1] if age == 1 else cz[2]   # cols: (glint, newest, older); Libra wind 'Wfq'
                        px[k * 64 + X, r * 64 + Y] = hexc(NPAL[ch], 255 if age == 1 else 200 if age == 2 else 150)
                        if age < 3:   # the newer stretches two pixels thick, the second one outward from the chest
                            X2 = round(c0[0] + (rr + 1) * math.cos(a)); Y2 = round(c0[1] + (rr + 1) * math.sin(a))
                            if (X2, Y2) != (X, Y) and 0 <= X2 < 64 and 0 <= Y2 < 64 and not (side == 'far' and any(L_[k * 64 + X2, r * 64 + Y2][3] for L_ in (body, lay['near'], lay['far']))): px[k * 64 + X2, r * 64 + Y2] = hexc(NPAL[cz[2]], 210 if age == 1 else 160)
    fx.save(f); print(state, 'trails')

def crystalize(state, spec):   # Capricorn: crystal growing over the fighter. spec = {'shin': {frame: (pose, cover, alpha)}, 'arm': {frame: (cover, alpha)}}
    """shin: the near (kicking) leg's pixels within 2.5 px of its knee -> ankle line (AS_SEG, E coords, mirrored for W),
    covered from the ankle up by cover (0-1); arm: the near arm's skin (arms.png), covered from the hand (furthest from the shoulder) back.
    Crystal: teal body C, glint c facet lines, deep teal T on the edges and every fifth diagonal (the gem's shaded facets)"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    px = fx.load(); lays = [Image.open(d + n).convert('RGBA').load() for n in ('body.png', 'male-gi.png') if os.path.exists(d + n)]
    ap = Image.open(d + 'arms.png').convert('RGBA').load()
    C_, c_, T_ = _hexc(NPAL['C'])[:3], _hexc(NPAL['c'])[:3], _hexc(NPAL['T'])[:3]
    def paint(pts, al, k, r):
        for (x, y) in pts:
            edge = any((x + a, y + b) not in pts for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            col = T_ if edge or (x - y) % 5 == 0 else c_ if (x + y) % 4 == 0 else C_
            px[k * 64 + x, r * 64 + y] = col + (al,)
    for k, (pose, cov, al) in (spec.get('shin') or {}).items():
        (kx, ky), (ax_, ay_) = AS_SEG[pose]
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'
            pts = set()
            for y in range(64):
                for x in range(64):
                    if not any(L[k * 64 + x, r * 64 + y][3] for L in lays): continue
                    ex = 63 - x if flip else x
                    vx, vy = ax_ - kx, ay_ - ky; L2 = vx * vx + vy * vy
                    t = max(0, min(1.25, ((ex - kx) * vx + (y - ky) * vy) / L2))
                    if math.hypot(ex - (kx + t * vx), y - (ky + t * vy)) <= 2.5 and t >= 1 - cov: pts.add((x, y))
            paint(pts, al, k, r)
    for k, (cov, al) in (spec.get('arm') or {}).items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'
            arm = [(x, y) for y in range(64) for x in range(64) if ap[k * 64 + x, r * 64 + y][3]]
            if not arm: continue
            sh = min(arm, key=lambda q: abs(q[1] - 22) * 4 + abs(q[0] - 32))   # the shoulder: crystal grows from the hand (the skin furthest from it) back
            skin = [(x, y) for (x, y) in arm if ap[k * 64 + x, r * 64 + y][:3] in SKIN]
            skin.sort(key=lambda q: -math.hypot(q[0] - sh[0], q[1] - sh[1]))
            paint(set(skin[:round(len(skin) * cov)]), al, k, r)
    fx.save(f); print(state, 'crystalize', sorted(spec.get('shin') or {}), sorted(spec.get('arm') or {}))

def anchored(state, frames):
    """Splash fx placed on the fighter itself, so they ride every pose and root step: frames = {frame: [(pattern, anchor,
    dx, dy, opts)]}; anchor 'head' (centre of the head found in body.png), 'hand' (tip of the near arm, the arms layer's
    most forward pixel), 'farhand' (the same on the far arm), 'feet' (floor under the body); dx is toward the facing (mirrored for W, pattern flipped);
    the pattern is centred on the anchor; opts: 'behind' (only where the fighter is not drawn), {'alpha': {letter: a}}"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    lays = [Image.open(d + n).convert('RGBA').load() for n in FIG_LAYERS if os.path.exists(d + n)]   # 'behind'/'onFig' test the widest outline of any look (ANIMATION_RULES)
    px = fx.load(); bp = lays[0]; ap = Image.open(d + 'arms.png').convert('RGBA').load()
    fp = Image.open(d + 'far-arm.png').convert('RGBA').load() if os.path.exists(d + 'far-arm.png') else None
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    for k, items in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1
            opq = [(x, y) for y in range(64) for x in range(64) if bp[k * 64 + x, r * 64 + y][3]]
            top = min(y for _, y in opq); head = [x for x, y in opq if y <= top + 9]
            arm = [(x, y) for y in range(64) for x in range(64) if ap[k * 64 + x, r * 64 + y][3]]
            tip = (max if not flip else min)(arm, key=lambda q: (q[0], -q[1])) if arm else ((max(head), top + 8))
            farm = [(x, y) for y in range(64) for x in range(64) if fp and fp[k * 64 + x, r * 64 + y][3]]   # the far arm's most forward pixel (Wither Palm: the far palm's strikes)
            ftip = (max if not flip else min)(farm, key=lambda q: (q[0], -q[1])) if farm else tip
            anchors = {'head': ((min(head) + max(head)) / 2, top + 6), 'hand': tip, 'farhand': ftip, 'feet': ((min(x for x, _ in opq) + max(x for x, _ in opq)) / 2, 63), 'eye': _eye(state, k, r) or (max(head) - 2 if not flip else min(head) + 2, top + 5)}
            for item in items:
                name, an, dx, dy = item[:4]; opts = item[4] if len(item) > 4 else {}
                pat = NPAT[name]; h, w = len(pat), len(pat[0]); ax, ay = anchors[an]
                x0 = round(ax + sg * dx - (w - 1) / 2); y0 = round(ay + dy - (h - 1) / 2)
                if 'bottom' in opts: y0 = opts['bottom'] - h + 1   # Tidal Slam v2.2: the pattern's bottom row pinned to this row (a crest rising out of the wave under it)
                for yy, row in enumerate(pat):
                    for xx, ch in enumerate(row[::-1] if flip else row):
                        if ch == '.': continue
                        X, Y = x0 + xx, y0 + yy
                        if not (0 <= X < 64 and 0 <= Y < 64): continue
                        if opts.get('behind') and any(L[k * 64 + X, r * 64 + Y][3] for L in lays): continue
                        if opts.get('onFig') and not any(L[k * 64 + X, r * 64 + Y][3] for L in lays): continue   # Singularity: a veil drawn only over the fighter
                        px[k * 64 + X, r * 64 + Y] = hexc(NPAL[ch], opts.get('alpha', {}).get(ch, 255))
    fx.save(f); print(state, 'anchored', list(frames))

def mask(state, frames, waves=None):
    """Killing Intent v3 (Christopher 2026-10-27): an illusory demon mask appears over the caster's head, in profile matching
    its facing ('faint' outline only, 'full' translucent fill, 'flare' eye and fangs blazing, 'flicker' breaking up); placed
    from the head found in body.png each frame so it rides the lunge; the killing-intent waves roll out from the mask's mouth"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; dirs = load(D + state + '.json')['directions']
    body = Image.open(d + 'body.png').convert('RGBA'); fx = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', body.size)
    px = fx.load(); bp = body.load()
    hexc = lambda c, a=255: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
    def stamp(k, r, pat, x0, y0, flip, recol=None, alpha=None, skip=None):
        for yy, row in enumerate(pat):
            if skip and yy % 2 == skip - 1: continue
            for xx, ch in enumerate(row[::-1] if flip else row):
                if ch == '.': continue
                ch = (recol or {}).get(ch, ch)
                if ch == '.': continue
                X, Y = x0 + xx, y0 + yy
                if 0 <= X < 64 and 0 <= Y < 64: px[k * 64 + X, r * 64 + Y] = hexc(NPAL[ch], (alpha or {}).get(ch, 255))
    for k, stage in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            opq = [(x, y) for y in range(64) for x in range(64) if bp[k * 64 + x, r * 64 + y][3]]
            if not opq: continue
            top = min(y for _, y in opq); head = [x for x, y in opq if y <= top + 9]; L, R_ = min(head), max(head)
            flip = fd == 'W'; x0 = R_ + 3 - 17 if flip else L - 3; y0 = top - 4
            pat = NPAT['oniMask']
            if stage == 'faint': stamp(k, r, pat, x0, y0, flip, recol={'m': '.', 'M': '.', 'Y': '.', 'W': '.'}, alpha={'R': 150})
            elif stage == 'flicker': stamp(k, r, pat, x0, y0, flip, alpha={'m': 110, 'R': 170}, skip=1)
            else: stamp(k, r, pat, x0, y0, flip, alpha={'m': 175}, recol={'R': 'O', 'Y': 'W'} if stage == 'flare' else None)   # translucent fill: an illusion, the face shows faintly through
            for name, dx, dy in (waves or {}).get(k, ()):   # waves anchored at the mask's snout, bottom-left like nfx
                w = NPAT[name]; wx = (L - 3 + 18 + dx) if not flip else (R_ + 3 - 17 - dx - len(w[0]))
                stamp(k, r, w, wx, top + 9 + dy - len(w) + 1, flip)
    fx.save(f); print(state, 'mask', list(frames))

def clones(state, spec):
    """Gemini Mirage Clone / Phantom Legion: full-colour illusory copies of the fighter. spec = {frame: [(dx, alpha)]}: on each frame the
    whole figure (every drawn layer) is copied dx px toward the facing (negative = behind), washed toward pale silver (default 35%, optional 3rd item) and drawn
    at alpha on the fx layer, only where the real fighter is not, so the fighter stays on top; existing fx stays over the copies"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'
    names = [n for n in ('far-arm.png', 'body.png', 'male-gi.png', 'fade-hair.png', 'brown-eyes.png', 'arms.png') if os.path.exists(d + n)]
    lays = [Image.open(d + n).convert('RGBA') for n in names]
    comp = Image.new('RGBA', lays[0].size)
    for L in lays: comp.alpha_composite(L)
    cp = comp.load(); top = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', comp.size)
    base = Image.new('RGBA', comp.size); px = base.load(); dirs = load(D + state + '.json')['directions']; tint = (233, 238, 244)
    for k, items in spec.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            sg = -1 if fd == 'W' else 1
            for it in sorted(items, key=lambda t: -abs(t[0])):
                dx, al = it[:2]; wash = it[2] if len(it) > 2 else 0.35   # Mirage Clone v2: wash 0 = an indistinguishable full-colour copy
                rim = tuple(int(it[3][i:i + 2], 16) for i in (1, 3, 5)) if len(it) > 3 else None   # Phantom Legion v2: the copy's outline in the green rim
                for y in range(64):
                    for x in range(64):
                        q = cp[k * 64 + x, r * 64 + y]
                        X = x + sg * dx
                        if not q[3] or not (0 <= X < 64) or cp[k * 64 + X, r * 64 + y][3]: continue
                        c = tuple(round(q[i] * (1 - wash) + tint[i] * wash) for i in range(3))
                        if rim and any(not (0 <= x + ex < 64 and 0 <= y + ey < 64) or not cp[k * 64 + x + ex, r * 64 + y + ey][3] for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1))): c = rim
                        px[k * 64 + X, r * 64 + y] = c + (al,)
    base.alpha_composite(top); base.save(f); print(state, 'clones', list(spec))

def legion(state, spec):
    """Phantom Beset: washed copies of the caster (spec src state, frame srcFrame, every layer but fx) stand round the target,
    each facing it: spec frames = {k: [(dx, alpha)]}, dx toward the target's facing (a copy ahead takes the opposite facing's row,
    one behind the same facing's row), washed 35% toward pale silver, outlined in the green rim, drawn only where the target is not"""
    from PIL import Image
    d = D + state + '/'; f = d + 'fx.png'; s_ = D + spec['src'] + '/'; k0 = spec['srcFrame']
    sd = load(D + spec['src'] + '.json')['directions']
    names = [n for n in os.listdir(s_) if n.endswith('.png') and n != 'fx.png']
    def figure(fd):
        r = sd.index(fd); out = Image.new('RGBA', (64, 64))
        for n in ('far-arm.png', 'body.png', 'male-gi.png', 'fade-hair.png', 'brown-eyes.png', 'arms.png'):
            if n in names: out.alpha_composite(Image.open(s_ + n).convert('RGBA').crop((k0 * 64, r * 64, k0 * 64 + 64, r * 64 + 64)))
        return out.load()
    figs = {fd: figure(fd) for fd in ('E', 'W')}
    tl = [Image.open(d + n).convert('RGBA').load() for n in ('far-arm.png', 'body.png', 'male-gi.png', 'fade-hair.png', 'arms.png') if os.path.exists(d + n)]
    top = Image.open(f).convert('RGBA') if os.path.exists(f) else Image.new('RGBA', Image.open(d + 'body.png').size)
    base = Image.new('RGBA', top.size); px = base.load(); dirs = load(D + state + '.json')['directions']; tint = (233, 238, 244); rim = (0x39, 0xe7, 0x5f)
    for k, items in spec['frames'].items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            sg = -1 if fd == 'W' else 1
            for dx, al in sorted(items, key=lambda t: -abs(t[0])):
                cp = figs[('W' if fd == 'E' else 'E') if dx > 0 else fd]
                for y in range(64):
                    for x in range(64):
                        q = cp[x, y]
                        X = x + sg * dx
                        if not q[3] or not (0 <= X < 64) or any(L[k * 64 + X, r * 64 + y][3] for L in tl): continue
                        edge = any(not (0 <= x + ex < 64 and 0 <= y + ey < 64) or not cp[x + ex, y + ey][3] for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                        c = rim if edge else tuple(round(q[i] * 0.65 + tint[i] * 0.35) for i in range(3))
                        px[k * 64 + X, r * 64 + y] = c + (al,)
    base.alpha_composite(top); base.save(f); print(state, 'legion', list(spec['frames']))

def dissolve(state, frames):
    """Mirage Clone Dispel: the figure breaks up into scattered pixels: on each frame a fraction of the figure's pixels (every
    layer but fx) is cleared, the outer ones first, by a fixed per-pixel hash, so the break-up grows frame on frame; 1.0 clears
    the whole figure. Idempotent (clearing the same pixels again changes nothing)"""
    from PIL import Image
    d = D + state + '/'; dirs = load(D + state + '.json')['directions']
    for f in os.listdir(d):
        if not f.endswith('.png') or f == 'fx.png': continue
        im = Image.open(d + f).convert('RGBA'); px = im.load()
        for k, frac in frames.items():
            for r in range(len(dirs)):
                for y in range(64):
                    for x in range(64):
                        q = px[k * 64 + x, r * 64 + y]
                        if not q[3]: continue
                        h = ((x * 73856093) ^ (y * 19349663) ^ (k * 83492791)) % 1000 / 1000
                        edge = min(1, (abs(x - 32) / 14 + abs(y - 40) / 30) / 2)
                        if frac >= 1 or h * 0.7 + (1 - edge) * 0.3 < frac: px[k * 64 + x, r * 64 + y] = (0, 0, 0, 0)
        im.save(d + f)
    print(state, 'dissolve', frames)

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

def _eye(state, k, r):   # centre of the eye pixels (brown-eyes layer) in one cell
    from PIL import Image
    f = D + state + '/brown-eyes.png'
    if not os.path.exists(f): return None
    e = Image.open(f).convert('RGBA').load(); pts = [(x, y) for y in range(64) for x in range(64) if e[k * 64 + x, r * 64 + y][3]]
    return (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)) if pts else None

# ---- Leo ninjutsu / genjutsu (sunlight: white-hot core, gold, orange, red rim) ----
FIG_LAYERS = ('body.png', 'arms.png', 'far-arm.png', 'male-gi.png', 'fade-hair.png')
# Christopher 2026-11-03 19:28 (all auras follow the outline of the hair): baked silhouette-hugging fx (spiked eruptions, rays, glows)
# root outside the widest outline any equipped look can have, so they never paint over a hairstyle, helmet or armour; the plain aura is runtime
OUTFIT_LAYERS = ('long-hair', 'locs-tied', 'locs-loose', 'wrapped-headscarf', 'modern-topknot', 'braided-side', 'afro-puff', 'bantu-knots', 'ronin-ponytail',
                 'flat-top', 'afro-hair', 'headband-white', 'headband-red', 'headband-blue', 'scale-coat-helmet', 'lamellar-kabuto', 'molded-leather-cap', 'plate-bascinet',
                 'male-blue-armor', 'male-red-armor', 'blue-armor-shoulders', 'red-armor-shoulders', 'male-scale-coat', 'male-lamellar', 'male-studded-leather',
                 'male-plate-harness', 'scale-coat-shoulders', 'lamellar-shoulders', 'studded-leather-shoulders', 'plate-harness-shoulders')
FIG_LAYERS = FIG_LAYERS + tuple(n + '.png' for n in OUTFIT_LAYERS)
def _hexc(c, a=255): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def _open_fx(state, aura=False):   # the fx layer drawn so far this pass (fx() starts it clean when nothing else drew)
    from PIL import Image
    d = D + state + '/'; size = Image.open(d + 'body.png').size; fx = Image.open(d + 'fx.png').convert('RGBA')
    if fx.size != size: n_ = Image.new('RGBA', size); n_.paste(fx, (0, 0)); fx = n_
    return fx
def _fig(state, k, r):   # the figure's opaque pixels in one cell
    from PIL import Image
    d = D + state + '/'; lays = [Image.open(d + n).convert('RGBA').load() for n in FIG_LAYERS if os.path.exists(d + n)]
    return {(x, y) for y in range(64) for x in range(64) if any(L[k * 64 + x, r * 64 + y][3] for L in lays)}
def _tip(state, k, r, flip):   # the near hand: the arms layer's most forward pixel
    pts = _arm(state, k, r)
    return (min if flip else max)(pts, key=lambda q: (q[0], -q[1])) if pts else None

def rays(state, frames, aura=False):
    """Radiance: rays of sunlight bursting from the whole body, long and short in turn, turning slowly (frames = {k: (length, phase deg)});
    each ray starts a pixel off the silhouette edge, white at the root, then gold, orange, a red tip; drawn only outside the figure"""
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    W_, Y, O, R_ = (255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O']), _hexc(ELEMENT['R'])
    for k, (L0, ph) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); cx = sum(x for x, _ in fig) / len(fig); cy = sum(y for _, y in fig) / len(fig) - 4
            for i in range(16):
                th = math.radians(ph + 22.5 * i); L = L0 if i % 2 == 0 else max(2, L0 * 3 // 5)
                r0 = 0
                while r0 < 40 and (round(cx + r0 * math.cos(th)), round(cy - r0 * math.sin(th))) in fig: r0 += 1
                for j in range(L):
                    u = j / max(1, L - 1); c = W_ if u < 0.2 else Y if u < 0.55 else O if u < 0.85 else R_
                    for w in ((0, 0.6) if i % 2 == 0 and u < 0.6 else (0,)):   # the long rays are two pixels thick at the root
                        x = round(cx + (r0 + 2 + j) * math.cos(th) - w * math.sin(th)); y = round(cy - (r0 + 2 + j) * math.sin(th) * 1.1 - w * math.cos(th))
                        if 0 <= x < 64 and 0 <= y < 64 and (x, y) not in fig: px[k * 64 + x, r * 64 + y] = c
    fx.save(D + state + '/fx.png'); print(state, 'rays', list(frames))

def flare(state, frames, aura=False):
    """Radiance v3 (Christopher 2026-10-27, power-up reference): facing S, a towering aura of light erupting from the ground round
    the fighter (frames = {k: stage 0-3}): a glow hugging the body, white at the core, pale gold, gold, then tall jagged spikes
    fanning up and out with orange tips, longest straight up, and a ring of light flaring on the floor at the feet; drawn
    only outside the figure on the S row, then copied to every row (all rows show the S frame there)"""
    import random
    from PIL import ImageFilter, Image
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    W_, P_, Y, O = (255, 255, 255, 255), (255, 243, 176, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O'])
    every = isinstance(frames, dict) and frames.get('every')   # v4 (E-facing): drawn round each row's own figure, no turn
    if every: frames = {k: v for k, v in frames.items() if k != 'every'}
    for k, st, rs in [(k, st, r_) for k, st in frames.items() for r_ in (range(len(dirs)) if every else [dirs.index('S')])]:
        fig = _fig(state, k, rs); rnd = random.Random(k * 23)
        m = Image.new('L', (64, 64)); mp = m.load()
        for (x, y) in fig: mp[x, y] = 255
        cx = sum(x for x, _ in fig) / len(fig); top = min(y for _, y in fig); foot = max(y for _, y in fig)
        def P(x, y, c):
            x, y = round(x), round(y)
            if 0 <= x < 64 and 0 <= y < 64 and (x, y) not in fig: px[k * 64 + x, rs * 64 + y] = c
        g = [m]
        for i in range(4): g.append(g[-1].filter(ImageFilter.MaxFilter(3)))
        G = [q.load() for q in g]; wd = (1, 2, 3, 4)[st]
        if st >= 2:   # v3: the aura's body, a translucent mass of pale light filling round the fighter under the spikes
            vol = m.filter(ImageFilter.MaxFilter((0, 0, 9, 13)[st])).filter(ImageFilter.MaxFilter(5)).load()
            for y in range(64):
                for x in range(64):
                    if vol[x, y] and y < 62: P(x, y, (255, 246, 200, 150) if (x + y + k) % 3 else (255, 225, 77, 170))
        for y in range(64):   # the glow hugging the body: white, pale gold, gold, orange outward
            for x in range(64):
                for i in range(1, wd + 1):
                    if G[i][x, y] and not G[i - 1][x, y]: P(x, y, (W_, P_, Y, O)[min(3, i - 1 + (st < 2))]); break
        if st >= 1:   # the spikes: rays from the feet, each starting where it leaves the glow, fanning up and out, longest straight up
            L0 = (0, 8, 14, 17)[st]; ox, oy = cx, foot - 14; edge = G[min(wd, 4)] if st < 2 else vol
            for t in range(-100, 101, 4):
                a = math.radians(t + rnd.uniform(-1.5, 1.5)); ddx, ddy = math.sin(a), -math.cos(a) * 1.3
                d = 90   # from far outside, walk in toward the hips until the glow is hit: the spike roots there
                while d > 0:
                    xs, ys = ox + d * ddx, oy + d * ddy
                    if 0 <= round(xs) < 64 and 0 <= round(ys) < 64 and edge[round(xs), round(ys)]: break
                    d -= 0.5
                L = L0 * (0.55 + 0.45 * math.cos(a)) + rnd.randint(-3, 4) + (3 if abs(t) > 75 else 0)
                n = math.hypot(ddx, ddy); ux, uy = ddx / n, ddy / n
                for j in range(1, int(L)):
                    u = j / max(1, L - 1)
                    x, y = xs + j * ux, ys + j * uy
                    c = W_ if u < 0.25 else P_ if u < 0.5 else Y if u < 0.78 else O
                    P(x, y, c)
                    if u < 0.5: P(x - uy, y + ux, c)
            rx = (0, 16, 24, 26)[st]   # the ring of light flaring on the floor
            for tt in range(0, 360, 3):
                th = math.radians(tt); x, y = cx + rx * math.cos(th), 62 + 2 * math.sin(th)
                P(x, y, Y if math.sin(th) > 0 else O)
                if tt % 9 == 0: P(x, y - 1, P_)
        if every: continue
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(D + state + '/fx.png'); print(state, 'flare', list(frames))

def beam(state, frames, aura=False):
    """Solar Lance: a beam of solar fire from the near fingertips to the edge of the cell (frames = {k: (half-height, 'fire'|'fade')}):
    white-hot core, gold, orange, red rim; the rim flickers; 'fade' breaks it up into embers"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    ramp = [(255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O']), _hexc(ELEMENT['R'])]
    for k, (w, kind) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1; rnd = random.Random(k * 31 + r)
            tip = _tip(state, k, r, flip)
            if not tip: continue
            x0, y0 = tip[0] + sg * 2, tip[1]
            for i in range(64):
                x = x0 + sg * i
                if not 0 <= x < 64: break
                ww = min(w, 1 + i // 2)   # the beam flares out of the fingers over the first few pixels
                for dy in range(-ww, ww + 1):
                    lvl = min(3, round(abs(dy) * 3 / max(1, ww)))
                    if abs(dy) == ww and rnd.random() < 0.3: continue   # flickering rim
                    if kind == 'fade':
                        if rnd.random() < 0.55: continue
                        lvl = min(3, lvl + 1)
                    y = y0 + dy
                    if 0 <= y < 64: px[k * 64 + x, r * 64 + y] = ramp[lvl]
                if kind == 'fire' and i > 2 and rnd.random() < 0.35:   # sparks spitting off the beam's edges
                    y = y0 + rnd.choice((-1, 1)) * (ww + rnd.randint(2, 4))
                    if 0 <= y < 64: px[k * 64 + x, r * 64 + y] = ramp[rnd.randint(1, 2)]
    fx.save(D + state + '/fx.png'); print(state, 'beam', list(frames))

def cone(state, frames, aura=False):
    """Spotlight: a cone of pale gold light pouring from the open palm (v2: from the eyes) toward the target (frames = {k: (length, strength)}),
    widening as it goes, a bright core line near the palm, dithered and translucent so the scene shows through"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    src = frames.get('from', 'hand'); frames = {k: v for k, v in frames.items() if k != 'from'}   # v2: 'eye' pours it from the eyes
    for k, (L, st) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1; rnd = random.Random(k * 17 + r)
            tip = _eye(state, k, r) if src == 'eye' else _tip(state, k, r, flip)
            if not tip: continue
            x0, y0 = round(tip[0]) + sg * 2, round(tip[1])
            for i in range(L):
                x = x0 + sg * i
                if not 0 <= x < 64: break
                h = 1 + i * 0.5
                for dy in range(-round(h), round(h) + 1):
                    y = y0 + dy
                    if not 0 <= y < 64: continue
                    q = abs(dy) / max(1, h)
                    if q > 0.85: c = _hexc(ELEMENT['O'], round(200 * st))                          # the cone's edge
                    elif i < 8 and q < 0.3: c = _hexc('#ffffff', round(230 * st))                   # hot core line near the palm
                    elif (x + y) % 2 == 0 or q < 0.4: c = _hexc(ELEMENT['Y'], round((150 if q < 0.4 else 110) * st))
                    else: continue
                    if i > L - 4 and rnd.random() < 0.5: continue   # ragged leading edge
                    px[k * 64 + x, r * 64 + y] = c
    fx.save(D + state + '/fx.png'); print(state, 'cone', list(frames))

def gather(state, frames, aura=False):
    """Supernova wind-up: motes of light streaming in toward the fighter from all round, closing in and thickening by stage (0-3)"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']
    cols = [(255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O'])]
    for k, st in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); cx = sum(x for x, _ in fig) / len(fig); cy = sum(y for _, y in fig) / len(fig)
            rnd = random.Random(k * 11 + r)
            for i in range(16 + 6 * st):
                th = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(15, 27) - 3 * st
                x, y = cx + rr * math.cos(th), cy + rr * 1.15 * math.sin(th)
                for j in range(3):   # a short streak pointing in toward the fighter, bright head inward
                    X, Y_ = round(x - j * math.cos(th)), round(y - j * 1.15 * math.sin(th))
                    if 0 <= X < 64 and 0 <= Y_ < 64 and (X, Y_) not in fig: px[k * 64 + X, r * 64 + Y_] = cols[min(2, 2 - j + (j == 0 and st < 2))]
    fx.save(D + state + '/fx.png'); print(state, 'gather', list(frames))

def spinFire(state, frames):
    """Leash Kick: a ring of fire whirling round the legs through the pirouette (frames = {k: (start, end degrees swept, stage 0-3)}):
    a flat ellipse at knee-to-hip height swept further each frame, thicker each turn (stage 2 doubled), black and purple
    licks flickering in it every few degrees (Sagittarius); its far half hides behind the figure; stage 3 breaks up as the kick fires"""
    from PIL import Image
    f_ = D + state + '/fx.png'; fx = Image.open(f_).convert('RGBA'); px = fx.load(); dirs = load(D + state + '.json')['directions']
    Y, O, R_, P, K = (_hexc(ELEMENT[c]) for c in 'YORPK')
    for k, (a0, a1, st) in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); sg = -1 if fd == 'W' else 1
            cx = sum(x for x, _ in fig) / len(fig); cy = 46
            rx, ry = 13 + 2 * min(st, 2), 4 + (st >= 2)
            for ring in range(1 + (st >= 1) + (st >= 2)):
                for t in range(a0 * 2, a1 * 2):
                    th = math.radians(t / 2); x = round(cx + sg * (rx + ring) * math.cos(th)); y = round(cy + (ry + ring) * math.sin(th) - ring)
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    if st == 3 and (x + y + t) % 3: continue
                    if math.sin(th) < 0 and (x, y) in fig: continue
                    deg = t // 2; c = (Y, O, R_)[ring] if ring < 3 else R_
                    if deg % 40 < 6: c = P if ring == 0 else K   # Sagittarius: purple and black licks in the ring
                    px[k * 64 + x, r * 64 + y] = c
                    if deg % 30 == 0 and st >= 1 and y - 2 >= 0: px[k * 64 + x, r * 64 + y - 1] = O; px[k * 64 + x, r * 64 + y - 2] = R_ if deg % 60 else P   # tongues of flame licking up
    fx.save(f_); print(state, 'spinFire', list(frames))

def topFire(state, frames):
    """Spinning Top (turned over, spinning on the head): frames = {k: stage} (0 entry / exit embers, 1 a ring half swept,
    2 the full whirl). The feet are the highest figure pixels (one per side of the V when it is open); flames burst off
    each foot (alternating shapes so they flicker, a black/purple flame every other frame), a flat ring of fire whirls
    round the legs at foot height (yellow, orange, red rings with purple and black licks, its far half behind the legs,
    the swept part advancing each frame), and sparks scatter on the floor round the head"""
    from PIL import Image
    f_ = D + state + '/fx.png'; fx = Image.open(f_).convert('RGBA'); px = fx.load(); dirs = load(D + state + '.json')['directions']
    Y, O, R_, P, K = (_hexc(ELEMENT[c]) for c in 'YORPK')
    def stamp(k, r, name, cx, cy, flip):
        pat = NPAT[name]; h, w = len(pat), len(pat[0]); x0, y0 = round(cx - (w - 1) / 2), round(cy - (h - 1) / 2)
        for yy, row in enumerate(pat):
            for xx, ch in enumerate(row[::-1] if flip else row):
                X, Y_ = x0 + xx, y0 + yy
                if ch != '.' and 0 <= X < 64 and 0 <= Y_ < 64: px[k * 64 + X, r * 64 + Y_] = _hexc(NPAL[ch])
    for k, st in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            fig = _fig(state, k, r); flip = fd == 'W'; sg = -1 if flip else 1
            cx = (min(x for x, _ in fig) + max(x for x, _ in fig)) / 2; top = min(y for _, y in fig)
            l = [q for q in fig if q[0] < cx - 4]; rr = [q for q in fig if q[0] > cx + 4]
            wide = l and rr and min(y for _, y in l) < top + 4 and min(y for _, y in rr) < top + 4
            feet = [min(l, key=lambda q: q[1]), min(rr, key=lambda q: q[1])] if wide else [min(fig, key=lambda q: q[1])]
            if st == 0:
                for fx_, fy in feet: stamp(k, r, 'embers', fx_, fy - 2, flip)
                stamp(k, r, 'embers', cx - 7, 60, flip); continue
            cy = top + 5; rx, ry = (17 if wide else 12), 3
            sweep = 200 if st == 1 else 360; a0 = (k * 97) % 360
            for ring in range(3):
                for t in range(sweep * 2):
                    th = math.radians(a0 + t / 2); x = round(cx + sg * (rx + ring) * math.cos(th)); y = round(cy + (ry + ring) * math.sin(th) - ring)
                    if not (0 <= x < 64 and 0 <= y < 64): continue
                    if math.sin(th) < 0 and (x, y) in fig: continue
                    if st == 1 and t < sweep and (x + y + t) % 2: continue   # the tail of a part-swept ring breaks up
                    deg = int(a0 + t / 2); c = (Y, O, R_)[ring]
                    if deg % 45 < 6: c = P if ring == 0 else K
                    px[k * 64 + x, r * 64 + y] = c
                    if deg % 36 == 0 and y - 2 >= 0: px[k * 64 + x, r * 64 + y - 1] = O; px[k * 64 + x, r * 64 + y - 2] = R_ if deg % 72 else P   # tongues licking up off the ring
            for i, (fx_, fy) in enumerate(feet):
                stamp(k, r, ('flame3', 'flame2')[(k + i) % 2] if (k + i) % 3 else 'pflame2', fx_, fy - 3, flip)
            stamp(k, r, 'embers' if k % 2 else 'pembers', cx + 8, 60, flip); stamp(k, r, 'pembers' if k % 2 else 'embers', cx - 8, 60, flip)   # sparks on the floor round the head
    fx.save(f_); print(state, 'topFire', list(frames))

def kanaboRise(state, frames):
    """Ironwood Kanabo v2 (Christopher 2026-10-28: the club rises from the earth): frames = {k: rows} the club's height
    above the floor, head first, out of a crack in front of the fighter (only the part above row 62 shows), or
    {k: 'grip'} the whole club with its grip in the near fist (the arms layer's foremost pixel)"""
    from PIL import Image
    f_ = D + state + '/fx.png'; fx = Image.open(f_).convert('RGBA'); px = fx.load(); dirs = load(D + state + '.json')['directions']
    pat = NPAT['kanabo']; H, Wd = len(pat), len(pat[0]); GRIP = 26   # pattern row held in the fist
    for k, v in frames.items():
        for r, fd in enumerate(dirs):
            if fd not in ('E', 'W'): continue
            flip = fd == 'W'; sg = -1 if flip else 1
            fig = _fig(state, k, r); cx = (min(x for x, _ in fig) + max(x for x, _ in fig)) / 2
            if v == 'grip':
                tip = _tip(state, k, r, flip); x0 = tip[0] - Wd // 2 - sg; y0 = tip[1] - GRIP; floor = 63
            else:
                x0 = round(cx + sg * 13 - Wd / 2); y0 = 63 - v; floor = 62
            for yy, row in enumerate(pat):
                for xx, ch in enumerate(row[::-1] if flip else row):
                    X, Y_ = x0 + xx, y0 + yy
                    if ch != '.' and 0 <= X < 64 and 0 <= Y_ <= floor: px[k * 64 + X, r * 64 + Y_] = _hexc(NPAL[ch])
    fx.save(f_); print(state, 'kanaboRise', frames)

def nova(state, frames, aura=False):
    """Supernova release, facing S (every row shows the S frame here): 'core' a star kindling at the chest and the body glowing;
    'flash' a white flash swallowing the fighter and the whole cell; stages 0-4 the rings of light blasting out (white, gold,
    orange, red as they widen and break up), sun rays scattering and the glow draining off the body, embers raining down"""
    import random
    fx = _open_fx(state, aura); px = fx.load(); dirs = load(D + state + '.json')['directions']; rs = dirs.index('S')
    W_, Y, O, R_ = (255, 255, 255, 255), _hexc(ELEMENT['Y']), _hexc(ELEMENT['O']), _hexc(ELEMENT['R'])
    ramp = [W_, Y, O, R_]
    for k, st in frames.items():
        fig = _fig(state, k, rs); cx = sum(x for x, _ in fig) / len(fig); cy = sum(y for _, y in fig) / len(fig) - 10   # the heart
        rnd = random.Random(k * 5)
        def P(x, y, c, over=False):
            x, y = round(x), round(y)
            if 0 <= x < 64 and 0 <= y < 64 and (over or (x, y) not in fig): px[k * 64 + x, rs * 64 + y] = c
        glow = {'core': 90, 'core2': 140, 'flash': 215, 'flash2': 235, 0: 150, 1: 100, 2: 60, 3: 30, 4: 0}[st]
        for (x, y) in fig:   # the body glowing white-gold (blinding at the flash)
            if glow: P(x, y, (255, 250, 220, glow), over=True)
        if st in ('core', 'core2'):   # v2: core2 the star swollen and blazing, rays flickering off it
            n_ = 5 if st == 'core' else 8
            for i in range(-n_, n_ + 1):
                c = W_ if abs(i) < 2 + (st == 'core2') else Y if abs(i) < n_ - 1 else O
                P(cx + i, cy, c, True); P(cx, cy + i, c, True)
                if abs(i) < n_ // 2 + 1: P(cx + i, cy + i, Y, True); P(cx + i, cy - i, Y, True)
            if st == 'core2':
                for i in range(8):
                    th = math.radians(i * 45 + 22); 
                    for d in range(10, 14): P(cx + d * math.cos(th), cy + d * math.sin(th), Y if d < 12 else O)
        elif st in ('flash', 'flash2'):   # v2: flash2 the flash pulsing bigger on the held apex
            sc = 1.0 if st == 'flash' else 1.2
            for y in range(64):
                for x in range(64):
                    dd = math.hypot(x - cx, (y - cy) * 0.9) / sc
                    if dd < 14: c = (255, 255, 255, 255)
                    elif dd < 24: c = (255, 245, 190, 235)
                    elif dd < 34: c = _hexc(ELEMENT['Y'], 190)
                    elif dd < 42: c = _hexc(ELEMENT['O'], 140 if (x + y) % 2 == 0 else 0)
                    else: continue
                    if c[3]: P(x, y, c)
        else:
            for j in range(min(st, 2) + 1):   # the leading ring and up to two behind it
                age = st - j; rx = 20 + 10 * age; ry = rx * 0.8; c = ramp[min(3, age)]
                if rx > 52: continue
                for t in range(0, 360, 2):
                    if age >= 2 and (t // 12) % 3 == 0: continue
                    th = math.radians(t); P(cx + rx * math.cos(th), cy + 10 + ry * math.sin(th), c)
                    if age < 2: P(cx + (rx - 1) * math.cos(th), cy + 10 + (ry - 1) * math.sin(th), Y if age == 0 else O)
            if st <= 2:   # sun rays scattering out between the rings
                for i in range(12):
                    th = math.radians(i * 30 + 15 * st)
                    for d in range(8 + 6 * st, 16 + 8 * st):
                        if d % 3 != 2: P(cx + d * math.cos(th), cy + d * 0.9 * math.sin(th), Y if d < 14 + 6 * st else O)
            for i in range(6 + 4 * st):   # embers
                P(rnd.randint(2, 61), rnd.randint(2, 60), (O, R_, Y)[i % 3])
        cell = fx.crop((k * 64, rs * 64, k * 64 + 64, rs * 64 + 64))
        for r in range(len(dirs)):
            if r != rs: fx.paste(cell, (k * 64, r * 64))
    fx.save(D + state + '/fx.png'); print(state, 'nova', list(frames))

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--fx' in a: fx(a[a.index('--fx') + 1]); sys.exit()
    for st in (a or CLIPS): spec(st)
