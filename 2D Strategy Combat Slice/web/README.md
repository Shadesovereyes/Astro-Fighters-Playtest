# Astro Fighters — Web Combat Testbed

Open [`index.html`](index.html) to launch the current browser testbed. It redirects to the active tactical build (`astro-fighters-2d-v3.4.html`) while the runtime modules remain split for debugging and regression isolation. The engine self-identifies as **V3.5** (`AF.VERSION` / `AFUI.VERSION`) even though the entry-point filename was never renamed off V3.4 — go by the version string, not the filename.

## Single-file builds

For remote play/testing or publishing, `astro-fighters-2d-v3.4.html` and its seven runtime modules can be bundled into one self-contained file:

```bash
cd web
node build-standalone.js            # -> astro-fighters-standalone.html
node build-standalone.js --artifact # -> astro-fighters-artifact.html (also, an Artifact-ready fragment)
```

Run both after changing any runtime module — `astro-fighters-standalone.html` is committed to the repo and must stay current; `astro-fighters-artifact.html` is the fragment published to the live Artifact and is gitignored, so it only needs to exist locally when publishing.

## Active runtime

Load order (must match `astro-fighters-2d-v3.4.html`'s `<script>` tags and `build-standalone.js`'s `MODULES` list):

1. `af-core.js` — DOM-free chart, hex-grid, combat, content, and AI engine.
2. `af-dc-model-v3.js` — shared candidate tier/DC/cost model (default-off in ordinary play; see `HANDOFF.md`).
3. `af-core-v3-patch.js` — V3 stance metadata, player targeting validation, and LoS enforcement patch.
4. `af-ui-v3.js` — progression, ability grouping, dependency, queue, and stat-budget view model.
5. `af-page-v3.js` — setup, HUD, arena, queue, and combat-log controller.
6. `af-map-v3.js` — map readability, occupied-cell treatments, stance-panel reveal, and fog of war.
7. `af-progression-v3.js` — canonical level-based attribute allocator and legacy-controller bridge. Runs after `af-page-v3.js`'s own setup, so it has the final say on setup-form defaults.

The split modules are intentionally retained for the current acceptance cycle. They should be merged only after manual browser acceptance, so cleanup does not introduce unrelated combat regressions.

## Tests

Run from `web/`:

```bash
node af-core.smoke.js
node af-v3.4.smoke.js
```

The current regression coverage includes chart/loadout construction, deterministic combat, movement-only rounds, stance-child gating, LoS blockers, fog of war, canonical level/stat budgets, relationship-aware positional combat, AGI-priority movement/initiative resolution, and the roster-based scenario system.

## Legacy compatibility

`astro-fighters.html` is the older 1-D standalone build. It remains only because the published artifact may still reference it. Remove or archive it after the published entry point is migrated and V3.4/V3.5 passes manual acceptance.

## Documentation

- `HANDOFF.md` — current continuation instructions and known gaps.
- `ASTRO_FIGHTERS_2D_V3_AUDIT.md` — acceptance checklist and deferred systems (dated 2026-08-05; a point-in-time audit, not kept live).
- `SESSION_LOG_2026-08-17.md` — latest session log; earlier `SESSION_LOG_*.md` files are historical development records.
- `../docs/DECISIONS.md` — the canonical, dated ledger of owner rulings and locked balance values.
