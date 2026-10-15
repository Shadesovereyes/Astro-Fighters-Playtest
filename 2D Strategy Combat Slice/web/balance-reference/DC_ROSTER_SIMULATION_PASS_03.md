# Astro Fighters — DC / Cost Roster Simulation Pass 03

_Date: 2026-08-12. Simulation findings only unless explicitly marked owner-locked._

This pass evaluates **all current sign-kit abilities, Universal/Generic arts, Martial styles, and Weapon kits together** against the same DC, action-slot, and resource-family rules. Dojutsu and Bloodline abilities are intentionally outside this pass because the owner requested sign kits + Universal + Martial/Weapon together first.

## Scope

Current runtime catalog evaluated from `web/af-core.js` on `claude/astrofighters-test-version-p1sw5a`:

- 94 sign-kit abilities
- 25 Universal/Generic/Medical/Trap/Summon abilities
- 39 Martial abilities
- 12 Weapon abilities
- **170 total**

Within that roster:

- 61 abilities directly apply a tiered hostile Status/DOT
- 53 direct hostile status effects currently use authored fixed saves
- 10 direct hostile status effects currently have **no save at all** (two abilities combine a saved effect with an automatic rider)
- 14 abilities use the separate grapple/grapple-tech/mount control system
- 5 abilities directly deny Stamina/Chakra resources and remain a separate pricing lane pending final drain-tier weights

## Owner-locked inputs used

- Equal-investment post-hit rider reliability: C 60%, B 45%, A ~35%, S ~30%.
- Standard melee-Stamina damaging-rider anchors: C 10, B 12, A 15, S 20, S+Guard Break 25.
- Pure A and Pure S control cost more resource than damaging riders of the same tier.
- Effect tier is not automatically final slot cost.
- Comparable melee Stamina < ranged Stamina < Chakra is intentional.
- Kyudo/ranged-Stamina pays a higher Stamina price for buying range.
- Guard Break and harmful-status premiums remain separately visible when stacked.

## 1. Current fixed DCs collapse immediately

The current save rule is `defender effective stat + d20 >= authored DC -> resisted`. Direct-save DCs are mostly 11–14.

Using the actual career-budget balanced-stat reference points from Pass 02:

- Level 1 balanced relevant stat ≈ 9
- Level 10 balanced relevant stat ≈ 18
- Level 20 ≈ 24
- Level 50 ≈ 36
- Level 100 ≈ 50

Across the **53 currently saved direct hostile effects**:

- at level 1, mean landing rate is only about **12.1%** before any attack-roll gate;
- at level 10, **all 53 fixed-save effects have 0% landing probability** against an equally built balanced defender;
- the same remains true at levels 20/50/100.

So the existing authored DC 11–14 values are not merely weak at high level—they are already below the approved reliability targets at level 1 and become mathematically obsolete by level 10.

## 2. The opposite problem: automatic hostile riders

Ten direct hostile riders currently bypass saves entirely:

- Aries — Mach Lunge: Burn
- Leo — Sun Palm: Burn
- Virgo — Sandstorm: Bleed rider
- Libra — Aero Palm: Bleed
- Scorpio — Numbing Strike: Slow
- Capricorn — Adamantine Shin: Bleed
- Universal — Solar Flare: Blind
- Universal — Viper Strike: Bleed
- Trap — Flash Bomb: Blind
- Trap — Spike Pit: Bleed rider

On a representative 75% single-target hit rate, an automatic rider procs on **75% of raw attempts**. Automatic AoE/trap riders effectively apply at **100% per target in the area** because `resolveAoe` does not make an attack roll.

Under the candidate tier DC model, equal-investment base-level raw-attempt rates become approximately:

- single-target damaging C: 75% hit × 60% rider = **45%**
- single-target damaging B: **33.75%**
- single-target damaging A: **26.25%**
- single-target damaging S: **22.5%**
- pure/AoE one-gate A: **35% per target**
- pure/AoE one-gate S: **30% per target**

Recommendation from testing: unless an ability is explicitly designed as a guaranteed rider, these ten effects should be converted to the shared tier DC system instead of remaining automatic.

## 3. Candidate DC curve remains healthy roster-wide

Current best candidate from Pass 02:

```text
StatEdge = clamp(trunc((AttackerControlStat - DefenderSaveStat) / 5), -6, +6)
MasteryBonus = floor(AbilityLevel / 4)
DC = TierOffset + StatEdge + MasteryBonus

TierOffset: C=13, B=10, A=8, S=7
Natural 1 on save = status lands
Natural 20 on save = resisted
Otherwise d20 >= DC resists
```

At equal investment it preserves the owner targets regardless of absolute character level. At extreme specialist advantage plus max mastery it caps S-tier around 70% on the save check rather than becoming automatic. A damaging S rider with a representative 75% attack hit rate therefore caps around 52.5% raw-attempt proc even in that extreme matchup.

This remains the recommended DC candidate for live engine implementation/testing.

## 4. Grapples stay on a separate control lane

Do **not** convert Clinch, Single Leg Shot, Kusari Chain Snare, mount advancement, or grapple techniques to the ordinary tier DC formula yet.

The grapple engine already uses relative attacker/defender stat contests, setup actions, escape attempts, hold upkeep, rooting, and mounted-state costs. Those are real balance gates. Generic C/B/A/S save math would double-charge setup and erase the useful distinction established in the earlier balance framework.

Grapple/control techniques still need resource/slot valuation, but their landing formula should remain separately calibrated.

## 5. Resource-family hierarchy is already strongly visible in clean attacks

Resolver-true cost was used, not just the authored number. Elemental abilities currently multiply their authored spend by `BAL.elementalCostMult = 1.75`.

Clean damaging actions without tiered harmful riders show these current medians:

| Delivery family | Clean abilities sampled | Median resolver-true spend | Observed range |
|---|---:|---:|---:|
| Melee Stamina | 22 | **10** | 8–30 |
| Ranged Stamina | 3 | **20** | 20–25 |
| Chakra | 21 | **35** | 21–70 |

This strongly supports the owner's intended hierarchy: **melee Stamina < ranged Stamina < Chakra** is already present at the resolver level.

Important consequence: future resource formulas must price **resolver-true final spend**. Applying a new blanket Chakra multiplier on top of Elemental Ninjutsu's existing ×1.75 would charge its range twice. Non-elemental ranged Chakra control (especially Genjutsu) does not receive that elemental multiplier and therefore needs its higher authored Chakra floor directly.

## 6. Base resource-floor audit for direct tiered statuses

Using the owner-approved melee Stamina anchors and the provisional ranged-family/effective-Chakra floors from Pass 01/02, **35 direct-status abilities are below their minimum base floor** before adding damage magnitude, AoE, Priority, range, or other advantages:

- Sign kits: 25
- Universal arts: 7
- Martial: 3
- Weapon: 0

This is a **minimum-floor audit**, not a request to reduce abilities above the floor. Being above the floor may be correct because of damage, AoE, range, duration, Guard Break, or other value.

### Highest-priority S-tier under-floor cases

- Aries Shatter Punch — current 12 Stamina; S + Guard Break floor **25**, candidate 2 slots.
- Gemini Sonic Sweep — current 12; S rider floor **20**, candidate 2 slots.
- Cancer Hydro Cannon Palm — current 10; S rider floor **20**, candidate 2 slots.
- Universal Heavenly Kick — current 10; S rider floor **20**, candidate 2 slots.
- Karate Sweeping Low — current 8; owner S-rider floor **20**, but **remains 1 slot** to preserve the approved Karate five-action string.
- Pure S Genjutsu Killing Intent / Kneel / Siren's Lure / Escapism — current 18 Chakra each; provisional pure-S Chakra floor **45**, candidate 3 slots.

### Important already-priced S examples

- Kenjutsu Hilt Bash — current **25 Stamina**, exactly matches the S + Guard Break resource floor; candidate action cost increases from 1 to **2 slots**.
- Capricorn Mausoleum and Pisces Bubble Prison — authored 22 Chakra Elemental; resolver-true spend ≈ **38**, already above the provisional 30 effective-Chakra S-rider floor. They mainly need the 2-slot hard-control action tax, not another blanket Chakra increase.

## 7. A-tier action-economy pressure

The simultaneous slot pass recommends **26 current direct-status abilities increase action-slot cost**:

- Sign kits: 20
- Universal: 5
- Martial: 0
- Weapon: 1

Typical outcomes:

- ordinary damaging A rider -> 2 slots
- ordinary damaging S rider -> 2 slots
- pure A -> 2 slots
- pure S -> 3 slots
- S + Guard Break -> 2 slots
- C/B riders stay 1 slot normally
- Sweeping Low remains the explicit 1-slot S exception because it sacrifices damage and pays the full S Stamina premium
- setup-gated grapple techniques remain authored 1–2 slots pending their separate chain test

This means the slot model is doing what was intended: strong pure control becomes frequency-limited, while weak/common riders remain combo-friendly.

## 8. Elemental AoE is not attack-gated

A key roster-wide correction: `resolveAoe` applies effects directly to targets in the radius; it does not make the ordinary single-target accuracy roll.

Therefore a damaging AoE + A/S status is a **single-gate control package**, not a normal damaging rider. It should be priced closer to pure control for reliability, then receive additional AoE/extra-target value through resource/slots.

Examples include Sandstorm, Singularity Sphere, Whirlpool, EMP Field, Blizzard, Spike Pit and Caltrops.

Several Elemental AoEs already have high resolver-true Chakra spend because of ×1.75 and 2-slot costs. These should not be blindly raised from the same raw-Chakra table as pure Genjutsu; evaluate their existing effective spend first.

## 9. Trap resource channels need a second premium

Harmful Trap abilities consume both Chakra and Supply. The standing owner rule says harmful-status/Guard-Break premiums must remain visible in **every resource channel consumed**.

Flash Bomb, Spike Pit and Caltrops currently still consume only 1 Supply—the same as clean/support traps. Their Chakra cost is also below the new status floors.

The next trap-specific test should decide whether harmful traps consume 2 Supplies, use a stronger per-battle charge restriction, or another explicit expendable premium. Do not solve this by Chakra alone if the ability already consumes Supply.

## 10. Resource-denial riders are a separate pending tier

Five abilities directly deny Stamina/Chakra rather than applying a named status. They were included in the simultaneous roster scan but not forced into the C/B/A/S status table yet:

- Spinning Top
- Wither Grasp
- Vice Grip
- Chakra Drain
- Boxing Body Shot

Their magnitude/duration/value needs its own mapping (for example -10 vs -15 vs -20 resource) before exact slot/resource floors are locked. They should still obey the same principle that a harmful rider costs more than a clean same-family comparator.

## 11. Recommended implementation order from this simultaneous pass

1. Implement the candidate tier DC function in the headless engine behind a balance switch/test path.
2. Convert the ten automatic hostile riders to tier saves for simulation, not final canon until their individual fantasy exceptions are reviewed.
3. Apply candidate slot counts to A/S ordinary status packages in the simulation harness; keep Sweeping Low at 1 and grapples in their own lane.
4. Apply base resource floors using **resolver-true spend**, so Elemental ×1.75 is counted once.
5. Add trap Supply-premium tests.
6. Add resource-drain magnitude tiers.
7. Run Monte Carlo full attack -> save -> status plus 3–6 round sustain for the entire 170-ability roster at equal, specialist-attacker, and specialist-defender career builds.
8. Only after the aggregate outliers are acceptable, write final costs back into runtime/workbook and rebuild standalone.

## Current conclusion

The shared model is viable across all three requested content families, but the current roster is not ready for a straight cost-only rebalance. The fixed-save/automatic-rider split must be normalized first. Once that is done, the owner-approved resource ladder and the separate action-slot pressure model produce coherent cross-kit behavior without flattening Martial combo flow or double-charging ranged Chakra abilities.