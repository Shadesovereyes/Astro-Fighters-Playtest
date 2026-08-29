# stone-clean candidate v1 — Source QA

**Asset ID:** `stone-clean`  
**Package:** `AF-IC-SHARED-FOUNDATION`  
**Status:** source candidate / not source-approved / not runtime-activated  
**Date:** 2026-08-28

## Files

- Source master: `production/source/world/shared-foundation/stone-clean.png`
- Runtime derivative: `docs/assets/world/shared-foundation/stone-clean.png`

## Contract checks

- Source dimensions: **1920×1280** — PASS
- Runtime dimensions: **192×128** — PASS
- Scale relationship: **10:1** — PASS
- Derivation: nearest-neighbor source → runtime — PASS
- Downscaled source matches committed runtime pixel-for-pixel — PASS
- Runtime SHA-256: `85666759ef77a28443605c3af2dc0cfba7de3d5e6f67b16fbf6696ce84d5db17`
- Source SHA-256: `efe8c86cfdbc350ae411492a2cd473ae17c1f944ab6e1777a6349d3beaa71c8a`
- Runtime PNG: opaque RGBA, no smoothing — PASS
- Source PNG: indexed/palette PNG preserving runtime colors exactly — PASS

## Art-direction intent

This candidate was rebuilt after rejecting the first schematic/procedural five-asset trial. It uses the legacy Package 03 stone study only as material-reference evidence, not as a resized/cropped production asset.

Targeted corrections:

- irregular authored stone courses instead of obvious 32×32 cadence;
- dry matte pale/warm civic stone;
- broken NW/upper-left edge highlights;
- lower-right contact/shadow pixels;
- localized grime, chips, cracks, repair and restrained moss;
- cross-block wear so the hidden logical grid does not become the visual composition;
- no wet-reflective, cyberpunk, steampunk or generic-fantasy treatment.

## Gate status

This report does **not** grant source approval. `production/asset-manifest.json` and `docs/data/shared-foundation-runtime.json` remain unchanged for `stone-clean`; it stays `missing`/disabled in machine state until the current world reference/source-assembly gate is reviewed and passed.

The runtime PNG is committed only so the exact derivative is preserved beside the source candidate. Its existence does not make it runtime-ready.

## Next review

Review this candidate beside the salvaged reference set and the next aged-stone foundation study. If the material language is accepted, promote `stone-clean` through the normal manifest/registry state transition and use it as the effective pixel-density authority for the remaining shared-foundation family.
