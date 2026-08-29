# Shared-foundation timber family candidate v1 — Source QA

**Package:** `AF-IC-SHARED-FOUNDATION`  
**Status:** source-qa / not source-approved / not runtime-activated  
**Date:** 2026-08-29

## Assets

### `timber-plaster-wall`
- source: `production/source/world/shared-foundation/timber-plaster-wall.png` — **1920×1600**
- runtime derivative: `docs/assets/world/shared-foundation/timber-plaster-wall.png` — **192×160**
- runtime SHA-256: `a0c451a9203ae1f31e9861cff707b98536f73a07b104c4cc64ab8dc8b4f0e253`
- source SHA-256: `777d58251e4f290392e14c48dbb5429c7d6cc8e8eea6a212e7c0f046c07331f1`

### `timber-post`
- source: `production/source/world/shared-foundation/timber-post.png` — **480×1280**
- runtime derivative: `docs/assets/world/shared-foundation/timber-post.png` — **48×128**
- runtime SHA-256: `d2aa9efaf003b8b29dea1925f2e8de270bac89a3bd7b3dbdd28f2bc45ab60704`
- source SHA-256: `ebe6df8862dd358f409985ffc464972b0ff599a4a29d7ea176d10b402a8dcf05`

### `horizontal-beam`
- source: `production/source/world/shared-foundation/horizontal-beam.png` — **1280×480**
- runtime derivative: `docs/assets/world/shared-foundation/horizontal-beam.png` — **128×48**
- runtime SHA-256: `4dfaf6a1be4efd75c9fdea1149fea6fbd30d05e7acc86ade8d21bbd656a54e05`
- source SHA-256: `52ed5530724fe63736444aa6ba368819845e6dc723cd26a09440998e86257ef9`

## Contract checks

- all three assets use the contracted 10:1 source/runtime relationship — PASS
- nearest-neighbor/pixel-preserving derivation — PASS
- NW/upper-left lighting logic shared across all three — PASS
- warm aged timber ramp shared across wall, post and beam — PASS
- restrained metal joinery rather than machinery ornament — PASS
- broad calm plaster planes with localized wear — PASS
- no neon, wet-reflective, steampunk, clockwork, or generic-fantasy treatment — PASS
- no character imagery; `NP-CHAR-001` is unaffected

## Visual-risk note

This report only establishes that the three files are coherent enough to enter **source QA**. It does not claim final homogeneity with `stone-clean` and `aged-stone-foundation`, nor does it grant source approval.

The five-asset family must be assembled and reviewed together before any asset advances to `source-approved` or `runtime-candidate`.

## Current family count

- benchmark assets authored: **5 / 5**
- benchmark assets in source QA: **5 / 5**
- source-approved: **0 / 5**
- runtime activated: **0 / 5**

Next gate: five-asset source assembly/homogeneity review.
