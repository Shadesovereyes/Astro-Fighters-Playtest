# Astro Fighters V3.4 — Ability Spec Audit

> **Balance invariants added after this audit:** Guard Break abilities require an authored Stamina premium over comparable clean abilities in the same discipline. DOT/harmful-status abilities require a premium in every resource channel they consume (Stamina, Chakra, Supplies/other expendables as applicable); if they consume both Stamina and Chakra, both must be higher. These rules govern reconciliation/balance decisions even where older numbers below do not yet satisfy them.

**Date:** 2026-08-12  
**Branch audited:** `claude/astrofighters-test-version-p1sw5a`  
**Canonical spec:** `AstroFighters_Abilities.xlsx`  
**Runtime audited:** `web/af-core.js` as loaded by V3.4, plus V3 annotations from `af-core-v3-patch.js` / `af-ui-v3.js`.

## Executive summary

The spreadsheet and runtime are **not currently synchronized**. This is not a small handful of typos: the sign kits in particular have broad numeric/content drift, several canonical abilities are absent or still use older names/content, and the catalog still contains several stale ability implementations that predate the current canonical spec.

| Area | Canonical rows | Runtime rows | Name coverage | Main result |
|---|---:|---:|---|---|
| Sign kits | 100 | 94 | 85 exact names | 15 canonical names absent; 9 stale/extra names; 82/85 exact-name rows differ in at least one basic field |
| Universal/support | 28 | 26 | 25 exact names | 3 canonical names absent, 1 stale rename; 15/25 exact-name rows differ in basic fields |
| Martial + weapon | 50 authored rows (5 are repeated Shared Clinch rows) | 47 runtime entries | 41 exact non-shared rows | 4 canonical techniques absent; 30 exact rows differ in basic fields |
| Dojutsu | 20 | 20 | 20/20 | Names/effects/costs largely aligned; non-damaging Mental CC is represented as `dmg: None` in runtime |
| Bloodline releases | 16 | 16 | 16/16 | Strongest-aligned catalog; names, costs and authored status effects match |

`Basic field` means damage type, listed power, slots, stamina, or chakra. The appendix compares canonical authored values to the raw runtime ability objects; runtime cost multipliers/floors may further change the actual paid cost.

## Release-blocking / high-impact mismatches

| Item | Audit finding |
|---|---|
| **Reach verification correction** | Re-checking the actual branch history and current source confirms the shared reach system **is live**: `gapClose` exists, reach attacks lunge without spending movement, the V3 patch validates `ab.reach`, Single Leg Shot has reach 2 with no Priority/AGI buff, and the arena has the reach perimeter. The earlier audit statement that `gapClose` was absent was incorrect. Some individual sign abilities still carry stale `MC`-based GapCloser content and remain reconciliation items. |
| **Lightning Cutter** | Spec: Elemental, power 50, 3 slots, 60 chakra, melee reach +6m, Ultimate + Priority + Gap Closer + Morality Morph. Runtime: `dmg: Mental`, power 24, 1 slot, 25 chakra, ranged Projectile maxR 10, Priority + GapCloser, `MC +6`, not Ultimate. |
| **Sand Burial** | Spec: single-target Elemental 15, 40 chakra, Guard Break, Root 2 rounds (STR DC13). Runtime: PointRadius AoE, Elemental 22, 22 chakra, no Root and no guard-break multiplier. |
| **Mausoleum** | Spec: non-damaging Terrain wall for 2 rounds + Root 1 round (STR DC14), 40 chakra. Runtime: Elemental single-target damage 6 + Stun 2 rounds (FORT DC14), 22 chakra; no terrain effect. |
| **Key CC substitutions** | `Kneel` is Root in spec but Stun in runtime; `Titan's Gaze` is Root in spec but Slow in runtime; `Betrayal` is Fear in spec but Confusion in runtime; `Shock Palm` should stun the next hostile action but runtime only deals damage. |
| **Missing canonical sign abilities** | `Pouncing Strike` (Leo), `Ghost Bomb` (Sagittarius), `Shell Crusher` (Cancer), `Stone Skin`, `Stone Rampart`, Taurus `Wither Grasp` + `Withering Squeeze`, and others listed below are not present under their canonical identities. |
| **Universal/support gaps** | `Shadow Constriction` and `Substitution` are missing. `Shadow Cloak` is still named `Gloom Shroud`. `Chakra Bullet` is spec True 5 / 10 chakra but runtime Elemental 14 / 12 chakra. |
| **Palm Healing documented divergence** | Spreadsheet says 15 chakra / Heal 25. Runtime is 25 chakra / Heal 15. This mismatch is **intentional in the current handoff/DF-19 heal rebalance**, so either the spreadsheet must be updated or that design decision must be reverted; both cannot remain authoritative. |
| **Martial/weapon missing techniques** | `Boxing Solar Plexus Strike`, `Jiu-Jitsu Arm bar`, `Wrestling Suplex`, and `Kyudo Arrow Rain` are canonical but absent from the runtime style tables. |
| **Parry semantics** | Spec: 50 stamina and negates the next hostile ability targeting the caster. Runtime: 6 stamina and only AGI +20% for 1 round. The `Counter` tag alone does not implement the authored immunity. |
| **Weapon/martial behavior drift** | Kenjutsu Slash lacks its authored Bleed; Precision Thrust is authored Guard Break but runtime has no poise multiplier; Wrestling Sumo Palm is authored Physical guard break but runtime is True damage with no guard break. |
| **Guard-break rule conflict** | Spreadsheet legend and multiple ability rows say Guard Break deals 2x poise damage. Runtime hard-caps guard-break at 1.5x (`poiseMult=1.5`), and the handoff explicitly says the UI displays 1.5x. This is a systemic spec-vs-design conflict, not a one-row bug. |

## Structural name/content mismatches

### Sign kits — canonical names absent from runtime

- `Cancer / Taijutsu / Shell Crusher`
- `Capricorn / Ninjutsu / Stalactite Eruption`
- `Capricorn / Taijutsu / Diamond Punch`
- `Leo / Taijutsu / Pouncing Strike`
- `Sagittarius / Ninjutsu / Ghost Bomb`
- `Sagittarius / Taijutsu / Bladed Kick`
- `Sagittarius / Taijutsu / Flow State`
- `Sagittarius / Taijutsu / Spin Fire Kick`
- `Taurus / Ninjutsu / Ironwill Kanabo`
- `Taurus / Ninjutsu / Stone Rampart`
- `Taurus / Ninjutsu / Stone Skin`
- `Taurus / Taijutsu / Boulder Palm`
- `Taurus / Taijutsu / Wither Grasp`
- `Taurus / Taijutsu / Withering Squeeze`
- `Virgo / Taijutsu / Sapping Palm`

### Sign kits — runtime names not present in canonical sheet

- `Capricorn / Ninjutsu / Stalactite Rain`
- `Capricorn / Taijutsu / Diamond Finger`
- `Sagittarius / Taijutsu / Flow Dodge`
- `Sagittarius / Taijutsu / Leash Kick`
- `Sagittarius / Taijutsu / Spinning Top`
- `Taurus / Ninjutsu / Ironwood Kanabo`
- `Taurus / Ninjutsu / Root Sanctuary`
- `Taurus / Taijutsu / Sumo Palm`
- `Virgo / Taijutsu / Wither Grasp`

Likely stale/rename pairs include `Diamond Punch → Diamond Finger`, `Stalactite Eruption → Stalactite Rain`, `Spin Fire Kick → Spinning Top`, `Flow State → Flow Dodge`, `Bladed Kick → Leash Kick`, `Ironwill Kanabo → Ironwood Kanabo`, Taurus `Boulder Palm → Sumo Palm`, and Virgo `Sapping Palm → Wither Grasp`. These are not treated as safe automatic renames because several also changed effects.

### Universal/support

- Canonical missing: `Shadow Cloak`, `Shadow Constriction`, `Substitution`.
- Runtime-only/stale name: `Gloom Shroud` (probable old name for `Shadow Cloak`).

### Martial / weapon

- Canonical missing: `Boxing / Solar Plexus Strike`
- Canonical missing: `JiuJitsu / Arm bar`
- Canonical missing: `Kyudo / Arrow Rain`
- Canonical missing: `Wrestling / Suplex`
- Runtime contains a Karate `Defensive Stance` entry even though the sheet only references it in Karate Stance's unlock text and does not provide a separate Karate row.

## Targeting / semantics mismatches found by field audit

- **Virgo — Sand Burial:** spec explicitly says single target; runtime uses `PointRadius`.
- **Capricorn — Mausoleum:** spec is Terrain placement; runtime uses `SingleEnemy` and no Terrain effect.
- **Cancer — Whirlpool:** runtime is ground `PointRadius`; the sheet calls it a single-target AoE centered on the target. This needs a design choice: locked target-centered AoE vs freely placed ground AoE.
- The eye and bloodline targeting structures are otherwise consistent with their canonical rows.

## Recommended reconciliation order

1. **Fix structural/semantic blockers first:** missing abilities, stale names, wrong damage type/targeting/status, stale per-ability gap-closer definitions, Parry, and the four missing martial/weapon techniques.
2. **Choose the authoritative systemic rules:** 2x vs 1.5x guard break; spreadsheet Palm Healing vs DF-19 heal rebalance; target-locked vs free-ground AoEs.
3. **Then synchronize numeric values** (power/slots/stamina/chakra) in batches by catalog, with smoke coverage per batch.
4. Only after the roster matches the canonical spec should Priority 2 (new synergy/content) begin; otherwise new combos would be built on stale abilities.

## Appendix A — exact-name sign-kit basic-field diffs

- **Aries / Taijutsu / Mach Lunge** — power: 8 → 14
- **Aries / Taijutsu / Shatter Punch** — stam: 15 → 20, power: 10 → 20
- **Aries / Taijutsu / Inner Gate: Adrenaline** — stam: 30 → 10
- **Aries / Ninjutsu / Blast Wave** — chakra: 25 → 18, power: 20 → 8
- **Aries / Ninjutsu / Explosive Runes** — chakra: 30 → 18, power: 25 → 12
- **Aries / Ninjutsu / Meteor** — chakra: 60 → 40, power: 100 → 35
- **Aries / Genjutsu / Blind Rage** — dmg: Mental → None
- **Aries / Genjutsu / Killing Intent** — dmg: Mental → None
- **Leo / Taijutsu / King's Posture** — stam: 15 → 8
- **Leo / Taijutsu / Sun Palm** — stam: 10 → 8, power: 10 → 14
- **Leo / Taijutsu / Battle Roar** — stam: 10 → 12, power: 10 → 12
- **Leo / Ninjutsu / Solar Lance** — chakra: 30 → 20, power: 25 → 18
- **Leo / Ninjutsu / Radiance** — chakra: 40 → 22
- **Leo / Ninjutsu / Supernova** — slots: 3 → 2, chakra: 60 → 30, power: 50 → 30
- **Leo / Genjutsu / Spotlight** — dmg: Mental → None
- **Leo / Genjutsu / Kneel** — dmg: Mental → None
- **Taurus / Taijutsu / Mountain Stance** — stam: 15 → 8
- **Taurus / Taijutsu / Bull Rush** — stam: 15 → 12, power: 8 → 14
- **Taurus / Ninjutsu / Oak Flesh** — slots: 2 → 1, chakra: 25 → 18
- **Taurus / Genjutsu / Material Fixation** — dmg: Mental → None, chakra: 30 → 18
- **Taurus / Genjutsu / Planetary Pressure** — dmg: Mental → None, chakra: 30 → 18
- **Virgo / Taijutsu / Silica Strike** — power: 10 → 12
- **Virgo / Taijutsu / Flowing Sand Parry** — stam: 15 → 8
- **Virgo / Ninjutsu / Sand Burial** — chakra: 40 → 22, power: 15 → 22
- **Virgo / Ninjutsu / Sandstorm** — chakra: 60 → 30, power: 40 → 30
- **Virgo / Genjutsu / Phantom Plague** — dmg: Mental → None, chakra: 30 → 45
- **Virgo / Genjutsu / Coffin Syndrome** — dmg: Mental → None, chakra: 30 → 18
- **Capricorn / Taijutsu / Adamantine Shin** — stam: 15 → 20, power: 10 → 16
- **Capricorn / Taijutsu / Prismatic Skin** — stam: 15 → 8
- **Capricorn / Ninjutsu / Geode Blast** — chakra: 30 → 20, power: 25 → 20
- **Capricorn / Ninjutsu / Mausoleum** — dmg: None → Elemental, chakra: 40 → 22, power: 0 → 6
- **Capricorn / Genjutsu / Atlas's Regret** — dmg: Mental → None, chakra: 30 → 18
- **Capricorn / Genjutsu / Titan's Gaze** — dmg: Mental → None, chakra: 30 → 18
- **Aquarius / Taijutsu / Nerve Disruptor** — stam: 10 → 8
- **Aquarius / Taijutsu / Static Shell** — stam: 15 → 8
- **Aquarius / Taijutsu / Shock Palm** — stam: 10 → 12, power: 10 → 16
- **Aquarius / Ninjutsu / Voltaic Orb** — chakra: 25 → 20, power: 20 → 14
- **Aquarius / Ninjutsu / Lightning Cutter** — dmg: Elemental → Mental, slots: 3 → 1, chakra: 60 → 25, power: 50 → 24
- **Aquarius / Ninjutsu / EMP Field** — chakra: 40 → 22
- **Aquarius / Genjutsu / System Crash** — dmg: Mental → None, chakra: 30 → 18
- **Aquarius / Genjutsu / Lag Switch** — dmg: Mental → None, chakra: 30 → 18
- **Libra / Taijutsu / Aero Palm** — power: 8 → 12
- **Libra / Taijutsu / Flow Parry** — stam: 15 → 8
- **Libra / Taijutsu / Feather Step** — stam: 30 → 6
- **Libra / Ninjutsu / Gale Slicer** — chakra: 30 → 20, power: 20 → 18
- **Libra / Ninjutsu / Pressure Blast** — chakra: 30 → 20, power: 25 → 14
- **Libra / Ninjutsu / Singularity Sphere** — slots: 3 → 2, chakra: 60 → 35, power: 40 → 32
- **Libra / Genjutsu / Indecision** — dmg: Mental → None, chakra: 30 → 18
- **Libra / Genjutsu / Vertigo** — dmg: Mental → None, chakra: 30 → 18
- **Gemini / Taijutsu / Mach Dash** — stam: 30 → 6
- **Gemini / Taijutsu / Echo Fist** — power: 15 → 16
- **Gemini / Taijutsu / Sonic Sweep** — stam: 10 → 8, power: 10 → 12
- **Gemini / Ninjutsu / Howling Blast** — chakra: 25 → 18, power: 8 → 12
- **Gemini / Ninjutsu / Mirage Clone** — chakra: 40 → 22
- **Gemini / Ninjutsu / Resonance Chamber** — slots: 5 → 2, chakra: 60 → 35, power: 60 → 30
- **Gemini / Genjutsu / Tinnitus** — dmg: Mental → None, chakra: 30 → 18
- **Gemini / Genjutsu / Phantom Legion** — dmg: Mental → None, slots: 3 → 1, chakra: 30 → 22
- **Cancer / Taijutsu / Tidal Slam** — power: 8 → 16
- **Cancer / Taijutsu / Vice Grip** — dmg: None → Physical, slots: 3 → 1, stam: 30 → 20, power: 0 → 8
- **Cancer / Taijutsu / Hydro Cannon Palm** — stam: 10 → 12, power: 10 → 16
- **Cancer / Ninjutsu / Water Cutter** — chakra: 25 → 18, power: 25 → 18
- **Cancer / Ninjutsu / Whirlpool** — slots: 3 → 1, chakra: 30 → 22, power: 15 → 20
- **Cancer / Ninjutsu / Tsunami** — chakra: 60 → 35, power: 60 → 32
- **Cancer / Genjutsu / Regression** — dmg: Mental → None, chakra: 18 → 16
- **Cancer / Genjutsu / Pacification** — dmg: Mental → None, chakra: 18 → 16
- **Scorpio / Taijutsu / Numbing Strike** — stam: 10 → 8, power: 10 → 12
- **Scorpio / Taijutsu / Shadow Step** — stam: 25 → 6
- **Scorpio / Taijutsu / Kidney Shot** — stam: 10 → 8, power: 15 → 16
- **Scorpio / Ninjutsu / Ice Shard** — chakra: 30 → 20, power: 20 → 18
- **Scorpio / Ninjutsu / Frost Armor** — chakra: 40 → 22
- **Scorpio / Ninjutsu / Blizzard** — slots: 3 → 2, chakra: 60 → 30, power: 40 → 28
- **Scorpio / Genjutsu / Paranoia** — dmg: Mental → None, chakra: 30 → 18
- **Scorpio / Genjutsu / Betrayal** — dmg: Mental → None, chakra: 30 → 18
- **Pisces / Taijutsu / Evasive Sway** — stam: 8 → 6
- **Pisces / Taijutsu / Slide Counter** — stam: 8 → 6
- **Pisces / Taijutsu / Flow Strike** — stam: 10 → 8, power: 5 → 8
- **Pisces / Ninjutsu / Bubble Prison** — slots: 3 → 2, chakra: 30 → 22, power: 10 → 12
- **Pisces / Ninjutsu / Hidden Mist** — chakra: 25 → 18
- **Pisces / Ninjutsu / Water Dragon** — slots: 50 → 2, chakra: 60 → 30, power: 26 → 30
- **Pisces / Genjutsu / Siren's Lure** — dmg: Mental → None, chakra: 30 → 18
- **Pisces / Genjutsu / Escapism** — dmg: Mental → None, slots: 3 → 2, chakra: 30 → 22

## Appendix B — universal/support basic-field diffs

- **Chakra Bullet** — dmg: True → Elemental, chakra: 10 → 12, power: 5 → 14
- **Solar Plexus Strike** — stam: 8 → 20
- **Iron Mountain** — stam: 10 → 20
- **Guardian Barrier** — slots: 3 → 1, chakra: 30 → 18
- **Solar Flare** — chakra: 25 → 15, power: 0 → 6
- **Chakra Drain** — chakra: 10 → 12, power: 5 → 8
- **Shadow Possession** — chakra: 30 → 20
- **Palm Healing** — chakra: 15 → 25, power: 0 → 15
- **Chakra Scalpel** — stam: 10 → 8, power: 5 → 8
- **Nerve Rupture** — slots: 3 → 1, stam: 15 → 8
- **Explosive Tag** — chakra: 5 → 15, power: 20 → 16
- **Flash Bomb** — chakra: 5 → 12
- **Spike Pit** — chakra: 5 → 12
- **Smoke Screen** — chakra: 5 → 12
- **Phantom Haunt** — dmg: Mental → None, chakra: 30 → 45, power: 15 → 0

## Appendix C — martial/weapon basic-field diffs

- **Boxing / Jab-Cross** — stam: 8 → 5
- **Boxing / Haymaker** — stam: 10 → 20, power: 10 → 18
- **Boxing / Bob and Weave** — stam: 15 → 6
- **Boxing / Defensive Stance** — stam: 15 → 6
- **Boxing / Dirty Boxing** — stam: 25 → 22
- **MuayThai / Roundhouse Kick** — stam: 8 → 6, power: 10 → 12
- **MuayThai / Teep Kick** — stam: 10 → 20
- **MuayThai / Elbow Strike** — stam: 8 → 9, power: 10 → 12
- **MuayThai / Knee Strikes** — stam: 25 → 26, power: 20 → 24
- **Judo / Hip Toss** — stam: 10 → 14, power: 8 → 0
- **Judo / Rolling Throw** — stam: 10 → 14, power: 8 → 0
- **Judo / Sweeping Shoulder** — stam: 10 → 12, power: 6 → 0
- **JiuJitsu / Strangle** — stam: 10 → 14, power: 15 → 0
- **JiuJitsu / Flying Triangle** — stam: 25 → 18, power: 15 → 0
- **Karate / Sweeping Low** — stam: 8 → 6
- **Karate / Karate Blitz** — stam: 10 → 8
- **Karate / Side Kick** — power: 8 → 12
- **Karate / Hammer Fist** — stam: 10 → 20, power: 10 → 12
- **Karate / Whirlwind Kick** — stam: 15 → 12, power: 10 → 12
- **Wrestling / Single Leg Shot** — stam: 15 → 14
- **Wrestling / Sumo Palm** — dmg: Physical → True, power: 10 → 12
- **Wrestling / Horse Stance** — stam: 20 → 8
- **Kenjutsu / Kenjutsu Slash** — stam: 15 → 8, power: 10 → 16
- **Kenjutsu / Parry** — stam: 50 → 6
- **Kenjutsu / Hilt Bash** — stam: 10 → 20, power: 5 → 8
- **Kenjutsu / Precision Thrust** — stam: 15 → 8, power: 10 → 12
- **Kyudo / Kyudo Shot** — slots: 2 → 1, stam: 20 → 10, power: 15 → 26
- **Kobudo / Shuriken Throw** — stam: 10 → 6, power: 15 → 10
- **Kobudo / Kusari Chain Snare** — stam: 20 → 14
- **Kobudo / Chain Yank** — stam: 25 → 18, power: 20 → 14

## Notes on interpretation

- The spreadsheet legend says listed costs are authored base values while runtime floors/multipliers can modify actual paid cost. This audit still lists raw object mismatches because the handoff explicitly asks to reconcile the canonical ability spec with what V3.4 implements.
- Non-damaging Genjutsu rows often say `Dmg Type = Mental` in the sheet while runtime stores `dmg: None` and applies a mental CC effect. Those are recorded as a representation difference rather than automatically treated as broken behavior.
- Bloodline release comparison found no substantive name/cost/status mismatch. Dojutsu is also close to spec, making those two catalogs good regression anchors while the other catalogs are reconciled.