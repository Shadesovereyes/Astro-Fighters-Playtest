# Astro Fighters — Current Development Status

**Updated:** 2026-08-27  
**Working branch:** `development/art-review-workflow-v1`  
**Draft PR:** #11

## Current production state

No world or character checklist item is currently recorded as rubric-approved/struck through. Existing runtime art must therefore be treated as unapproved until an integrated Phaser review passes the mandatory gate.

The active package remains **pre-art / contracted**. No checklist item was marked complete during the workflow/QA engineering work on this branch.

## Repository boundary

This repository remains the **public runtime/playtest host and art-production control surface** described by the root README. Source-authority art belongs to the separate/private development repository; this public repository records the contract, acceptance rules, logical source registration, runtime destinations, review tooling, and handoff state.

Do not substitute a generated/procedural placeholder in this public repository merely to satisfy a source path. The locked source workflow still applies in the development repository.

## Active dependency package

`AF-IC-SHARED-FOUNDATION`

The package contract in [`production/asset-manifest.json`](./production/asset-manifest.json) is now complete enough to begin source production. It locks:

- canonical `N, NE, E, SE, S, SW, W, NW` facing order;
- 480×640 per-direction character source canvas;
- shared character body center `[240,600]` and foot-contact line `y=600`;
- 48×64 runtime benchmark frame and pivot `[24,60]`;
- 10× world source-to-runtime scale for this package;
- source/runtime dimensions for every shared-foundation world dependency;
- world layer role, palette/material families, anchor, collision role, occlusion role, and stable runtime path;
- explicit `{direction}` source patterns for base-underlayer and dressed benchmark masters;
- explicit `{layer}/{direction}` modular character source registration;
- fully dressed unarmed Academy street-fighter benchmark outfit and palette families;
- the mandatory source gate that blocks runtime derivation until reference, modular assembly, and isolation/anchor QA pass.

The package remains `contracted`; its actual source images are still missing/unapproved.

## Runtime / workflow engineering completed in this branch

- Extracted the v4 launcher hotfix from inline HTML into `docs/js/playtest-v4-patch.js` without intentionally changing behavior.
- Reduced `docs/play-v4.html` to a stable launcher that loads the versioned patch file.
- Added `docs/art-review.html`, a GitHub Pages review surface that enforces automatic-failure and critical-minimum rules.
- Added `docs/data/art-review-rubric.json` as the machine-readable scoring authority used by the review surface.
- Synced the browser rubric with the revised Master Prompt automatic failures for anatomical equipment routing, clothing occlusion, contaminated modular isolates, and uncleaned automatic reductions.
- Added `production/asset-manifest.json` as the single-current-state registration/production contract.
- Added `tools/validate-production.mjs` to reject drift in canonical direction rules, source/runtime dimensions, package registration, score gates, and approval evidence.
- Added `tools/validate-source-png.mjs` for PNG-level QA of contracted world and character assets. It checks expected dimensions, RGBA format, hard alpha, non-empty pixels, transparency where required, and reports registration/contact/color diagnostics.
- Added `.github/workflows/validate-production.yml` so GitHub Actions syntax-checks the QA/browser scripts and runs the production contract validator on pushes and pull requests.

## Source QA commands

World source example:

```bash
node tools/validate-source-png.mjs world stone-clean source path/to/stone-clean.png
```

World runtime candidate example:

```bash
node tools/validate-source-png.mjs world timber-post runtime path/to/timber-post.png
```

Character source example:

```bash
node tools/validate-source-png.mjs character S source path/to/base-underlayer/S.png base
```

Character dressed benchmark example:

```bash
node tools/validate-source-png.mjs character NE source path/to/dressed-benchmark/NE.png dressed
```

The PNG tool is diagnostic/contract enforcement only. Passing it does not make an asset production-approved; source comparison, target pixel cleanup, Phaser integration, and the mandatory integrated rubric still remain downstream gates.

## Next production gate

Create and approve narrow source references in the development repository before runtime derivation:

1. shared Imperial stone / threshold / drainage material slice;
2. shared timber-post / beam / plaster-wall / stone-foundation architectural slice;
3. eight separate canonical base-underlayer masters on the shared 480×640 lattice;
4. eight separate fully dressed benchmark masters on that same lattice;
5. modular source component set registered to the benchmark;
6. PNG isolation / dimension / hard-alpha QA plus visual source-assembly QA;
7. source approval;
8. 48×64 / target-resolution derivation and manual pixel cleanup;
9. Phaser integration using the stable public runtime paths;
10. integrated rubric review using `/docs/art-review.html`;
11. only at 42+ with no automatic failures and all critical minimums passing, strike the corresponding checklist items.

If any upstream gate fails, repair it before continuing downstream. Git history is the iteration archive; keep only current authorities and current handoff state.
