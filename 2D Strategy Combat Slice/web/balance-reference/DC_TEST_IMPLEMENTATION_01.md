# Astro Fighters — DC Test Implementation 01

_Date: 2026-08-12. Test-only implementation; live combat behavior is unchanged._

## Purpose

This slice moves the roster-wide DC / CC / DOT balance work from offline math into executable code without silently changing the V3.4 playtest. The candidate formula, tier map, slot rules, and resource-floor rules now live in a shadow module and are exercised by the existing core smoke suite.

## Files

- `web/af-dc-model-v3.js` — shadow/test balance model. It is **not loaded by the live HTML/runtime yet**.
- `web/af-core.smoke.js` — existing smoke suite extended to enumerate the actual Sign + Universal + Martial + Weapon catalog and exercise the shadow model.

No additional versioned HTML page or standalone test suite was created.

## Implemented shadow API

`AFDC` exposes:

- intrinsic harmful status tier lookup;
- authored/provisional save-stat identity lookup;
- candidate control-stat identity hook (`ability.controlStat` / `effect.controlStat`, with save-stat fallback);
- `/5 stat edge, ±6 cap` DC math;
- `floor(AbilityLevel / 4)` mastery contribution;
- natural-1 fail / natural-20 resist protection;
- exact discrete landing-rate calculation;
- candidate status checks for both authored-save and currently automatic riders;
- damaging/pure/AoE slot recommendations;
- melee-Stamina / ranged-Stamina / Chakra delivery-family classification;
- resolver-true resource floors that count the existing Elemental `×1.75` exactly once;
- per-ability audit output.

## Tier map in executable test code

- **S:** Prone, Stun, Fear, Sleep
- **A:** Confusion, Blind, Root
- **B:** Slow, Snare, Silence, Disarm
- **C:** Bleed, Burn, Poison, Psychosomatic, Cripple

Beneficial/self states such as Stealth, Fortified, Shield and Regen are not forced through the harmful DC model. Grapple/GrappleTech/Mounted remain outside this module's ordinary Status path.

## Provisional save identities for legacy automatic riders

Existing authored saves retain their authored defender stat. The shadow model needs a temporary save identity for harmful riders that currently have no save so they can be simulated before catalog authoring is changed.

Current provisional defaults:

- Prone AGI
- Stun FORT
- Fear STR
- Sleep INT
- Confusion INT
- Blind INT
- Root AGI
- Slow AGI
- Snare AGI
- Silence CHA
- Disarm STR
- Bleed AGI
- Burn FORT
- Poison FORT
- Psychosomatic INT
- Cripple FORT

These defaults are **not owner-locked per-ability authoring**. The final control/save identity pass still needs to choose stats based on technique fantasy and discipline.

## Smoke coverage

The existing `af-core.smoke.js` now dynamically constructs the requested balance roster from:

- all 12 Sign kits;
- Universal/Generic/Medical/Trap/Summon arts;
- every Martial style stance + technique;
- every Weapon stance + technique.

The test is coverage-driven instead of permanently asserting exact roster counts. It verifies that:

1. the cross-kit roster did not unexpectedly lose a major content family;
2. every ordinary harmful Status/DOT effect is recognized by the tier map;
3. every recognized harmful effect has either an authored or provisional save-stat identity;
4. every current automatic harmful rider can be evaluated by the candidate model;
5. equal-investment L0 rates are exactly C/B/A/S = 60/45/35/30%;
6. equal-investment L10 rates are exactly 70/55/45/40%;
7. the representative ±27 relevant-stat edge gives S L10 = 65% / 15%;
8. natural 20 always resists and natural 1 always fails the save;
9. representative slot anchors remain correct: C/B one slot, normal S two, pure S three, Sweeping Low one, Hilt Bash two;
10. representative resource floors remain correct, including no double-charge for Elemental Ninjutsu.

## Executed local regression

A locally available self-contained V3.4 snapshot was used to execute the shadow module in Node. That snapshot predates a few current catalog edits, so its enumeration is 167 abilities / 62 hostile status abilities / 13 automatic riders rather than the current branch audit counts.

The **behavioral regression passed** on that snapshot:

```json
{
  "ok": true,
  "roster": 167,
  "hostile": 62,
  "harmful": 64,
  "automatic": 13
}
```

Passing checks included tier/save coverage, candidate probabilities, specialization scaling, natural-roll guards, slot anchors, resolver-true Elemental handling, and representative C/B/A/S resource floors.

The committed smoke dynamically evaluates the current branch catalog, so the older local snapshot's count differences are not used as balance evidence.

## What has NOT changed yet

- `web/af-core.js` still resolves ordinary Status saves with the legacy authored fixed DC path.
- Current automatic riders are still automatic in live combat.
- Catalog slot counts and resource costs have not been mass-rewritten.
- The live V3.4 HTML and standalone do not load `af-dc-model-v3.js`.
- Grapple landing/escape logic is unchanged.
- The AI planner still under-values damaging status riders because its current score path treats Damage and Status utility as mutually exclusive.

Therefore this slice cannot change normal player-facing combat outcomes.

## Next test implementation slice

1. Add a default-off runtime balance switch for candidate status saves.
2. Pass the originating ability into the status resolver so ability mastery and authored control-stat identity are available at save time.
3. Annotate built abilities with their current ability level when progression is applied.
4. Under the switch, normalize ordinary harmful Status effects—including legacy automatic riders—through `AFDC.candidateStatusCheck`; keep Grapple/GrappleTech separate.
5. Preserve authored/legacy behavior with the switch off and add deterministic old-vs-candidate resolver tests.
6. Decide how Mounted's existing +4 Genjutsu DC modifier should translate into the relative candidate system before enabling candidate saves for real battle simulations.
7. Fix AI damage+rider scoring before using planner selection rates in balance conclusions.
8. Then run actual low/mid/high career battles with the candidate switch enabled.

Do not apply roster-wide final costs or write the workbook from this test slice alone.