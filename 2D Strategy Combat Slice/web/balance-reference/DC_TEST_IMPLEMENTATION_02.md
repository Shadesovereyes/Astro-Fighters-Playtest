# Astro Fighters — DC Test Implementation 02

_Date: 2026-08-12._

## Scope

The candidate tier-DC model is now wired into the real `af-core.js` status resolver behind `BAL.useCandidateDcModel`, which defaults to `false`. No live playtest behavior changes unless a test explicitly enables the flag.

## Candidate path behavior

- Only hostile tiered Status/DOT effects enter the candidate path.
- Self-applied states remain automatic.
- Grapples remain on the existing grapple contest lane.
- Legacy automatic hostile riders gain their provisional tier/save identity while candidate mode is enabled.
- The originating ability is passed into status resolution so `abilityLevel` and future per-ability `controlStat` metadata can affect DC.
- Ability progression now annotates built abilities with `abilityLevel`; this is inert while candidate mode is off.
- Natural 1 always fails the save; natural 20 always succeeds.
- Mounted target DC bonus is preserved during the test path.
- Stun/Fear/Sleep seed their later `breakDC` from the candidate DC that actually landed.

## Deterministic resolver regressions

`af-core.smoke.js` proves both modes through `AF.resolveRound`:

1. **Killing Intent / Stun:** at equal STR 20 with a natural 1, legacy authored DC 13 is resisted; candidate S-tier DC 7 lands.
2. **Viper Strike / Bleed:** with an attack hit followed by natural 20, legacy mode still applies the previously automatic Bleed; candidate mode resists it.
3. Candidate mode returns to `false` before the ordinary deterministic combat smoke continues.

## Not yet enabled for balance acceptance

This is infrastructure for controlled engine tests. It does not yet lock per-ability attacker control-stat identities, AoE premium, drain tiers, harmful Trap Supply premium, or final roster resource/slot changes.
