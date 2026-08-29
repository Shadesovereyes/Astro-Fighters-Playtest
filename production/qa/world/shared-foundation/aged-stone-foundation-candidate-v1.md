# aged-stone-foundation candidate v1 — Source QA

**Asset ID:** `aged-stone-foundation`  
**Package:** `AF-IC-SHARED-FOUNDATION`  
**Status:** source-qa / not source-approved / not runtime-activated  
**Date:** 2026-08-29

## Files

- Source master: `production/source/world/shared-foundation/aged-stone-foundation.png`
- Runtime derivative: `docs/assets/world/shared-foundation/aged-stone-foundation.png`

## Contract checks

- Source dimensions: **1920×640** — PASS
- Runtime dimensions: **192×64** — PASS
- Scale relationship: **10:1** — PASS
- Derivation: nearest-neighbor source → runtime — PASS
- Runtime SHA-256: `e566f22a98fbc4a5f9b09086a7528f59300fb8dfde8e7de7744b417f74d83bbb`
- Source SHA-256: `55b87d019a1f46c8843fc16f7d379ab589a2f36a74f085f24ca291d0af9d4ee5`

## Art-direction intent

This candidate inherits the same effective pixel grammar as `stone-clean` while reading older and heavier:

- larger masonry blocks and deeper joint shadows than the street surface;
- dry matte pale/warm stone with darker aged contact edges;
- NW/upper-left broken highlights;
- localized grime, chips, cracks, and restrained moss concentrated near lower/contact regions;
- no wet-reflective treatment;
- no dungeon/fantasy masonry language;
- no visible 32×32 gameplay-grid cadence;
- no steampunk/cyberpunk machinery cues.

## Gate status

This asset is now tracked as `source-qa` in both the production manifest and guarded runtime registry. The registry remains `enabled: false`; therefore the file cannot replace the Phaser scaffold yet.

This QA state records real authored progress without claiming source approval, runtime-candidate status, integration, or production approval.

## Next review

Review `stone-clean` and `aged-stone-foundation` together as the first two-material family. If their pixel density, lighting, value hierarchy, and Imperial City material identity pass, continue the same grammar into `timber-plaster-wall`, `timber-post`, and `horizontal-beam` before runtime activation.
