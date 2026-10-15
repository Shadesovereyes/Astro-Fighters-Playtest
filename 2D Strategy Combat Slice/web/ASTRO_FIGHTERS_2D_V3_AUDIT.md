# Astro Fighters 2-D V3.1 — Functional and UX Audit

Date: 2026-08-05
Branch target: `claude/astrofighters-test-version-p1sw5a`

## Audit basis

The V3.1 testbed was checked against:

- `web/HANDOFF.md`
- `docs/IMPLEMENTATION_SPEC.md`
- `web/astro-fighters.html` (the earlier playable 1-D reference)
- *Astro Fighters: Core Systems and Combat Philosophy*
- `AstroFighters_Abilities.xlsx`

The ability spreadsheet is authoritative for the following UX rules:

- **Charge Chakra** and **Catch Breath** are universal, repeatable Focus actions.
- Martial and weapon stances are parents that reveal their associated techniques.
- Dependency actions should not appear as ordinary ready choices before their prerequisite exists.

## Release blockers found in V2

| Area | Finding | V3 disposition |
|---|---|---|
| Universal actions | Charge Chakra and Catch Breath were buried in the flat list and could appear absent. | Fixed: pinned Focus rail, always visible and searchable. |
| Ability organization | Flat discipline filtering exposed too many unrelated choices. | Fixed: categories, authored-source filters, search, contextual counts, grouped source panels. |
| Stance dependencies | Martial and weapon techniques appeared before their stance was queued or active. | Fixed: hidden by default; queued/active parent stance reveals children. |
| Queue dependencies | Children could be ordered before their parent. | Fixed: projected queue validation rejects invalid ordering; removing a parent cascades dependents. |
| Eye dependencies | Eye jutsu could be presented before opening the eye. | Fixed: eye-open action acts as parent in the same dependency model. |
| Grapple dependencies | Follow-ups could contribute to option overload before a grapple existed. | Fixed: hidden until the combat state or earlier queued action supplies the prerequisite. |
| Movement-only turns | UI required an action even when the player only wanted to reposition. | Fixed: movement-only round resolution is valid. |
| Level selection | Progression milestones were absent. | Fixed: levels 1–100 with canonical chart-unlock milestones and profile summaries. |
| Scenario selection | Only one duel flow was exposed. | Fixed: 1v1, 2v2, and 3-way FFA test scenarios. |
| Debug coverage | Test controls were incomplete. | Fixed: all-sign override, god mode, roster heal, terrain regeneration, seed, and key balance controls. |
| Map readability | Tokens and terrain glyphs did not sufficiently alter their underlying cells. | Fixed: faction-colored occupied cells/rings, distinct soft/hard LoS blocker treatments, center rings, and a map legend. |

## Level milestone implementation

The testbed uses the progression milestones in the current design document:

- 1–9: Universal/general training only
- 10: Ascendant sign kit
- 15: Moon sign kit and summon access
- 20: Sun sign kit and ultimate access
- 25: Venus sign kit
- 30: Mercury sign kit
- 35: Mars sign kit
- 45: Jupiter sign kit
- 60: Saturn sign kit
- 75: Uranus sign kit
- 90: Neptune and Pluto sign kits
- 100: North Node milestone is displayed, but its Karmic Ultimate is not yet authored in the JavaScript catalog

This supersedes the older vertical-slice shortcut that spawned every test character fully awakened. A debug override remains available for full-catalog testing.

## Automated validation performed

The following tests passed:

- JavaScript syntax validation for the core patch, UI view-model, page controller, and map overlay
- Birth chart generation and level-derived loadout creation
- Exactly two universal Focus actions present at all tested levels
- Level milestone unlock matrix
- Martial stance parent-child visibility
- Weapon stance parent-child visibility
- Eye-open parent-child ordering
- Queue ordering validation and dependent-action cascading
- Engine-side rejection of martial and weapon techniques without their stance
- Movement-only round resolution
- Hex reachability and planned movement application
- Multi-combatant battle setup and resolution
- Deterministic full battle to a clean result
- Standalone packaging with zero external script dependencies
- Static DOM audit for duplicate element IDs
- Static map-rendering audit for player/ally/enemy occupied classes, soft/hard blocker classes, redraw observation, legend markup, and V3.1 script wiring

Latest repository-target deterministic smoke result:

```json
{
  "ok": true,
  "chart": {"sun": "Gemini", "moon": "Pisces", "asc": "Libra"},
  "focus": 2,
  "levelMilestones": true,
  "stanceGating": true,
  "movementOnly": true,
  "multiCombat": true,
  "mapReadability": true,
  "rounds": 17,
  "logEntries": 316
}
```

## Manual acceptance checklist

Before treating V3.1 as the new primary slice, manually verify:

1. At level 1, Catch Breath and Charge Chakra are pinned and no chart kit is shown.
2. At level 10, only the Ascendant kit is added.
3. At level 15, the Moon kit and Summon Companion are added.
4. At level 20, the Sun kit and eligible ultimates appear.
5. A trained martial style initially shows only its stance.
6. Queueing that stance reveals only its own child techniques.
7. Queueing a different stance later switches the projected stance and corresponding children.
8. Removing a stance removes any children that depend on it.
9. Eye jutsu appears only after its eye is active or the eye-opening action is queued earlier.
10. Selecting a reachable hex produces the movement preview and can resolve without another action.
11. Player, ally, and hostile occupied cells are immediately distinguishable from empty cells.
12. Sight-only blockers are visually distinct from movement-and-sight blockers, and the legend matches.
13. All three scenarios start and resolve without console errors.
14. Search, category, source, and dependency filters reduce the list predictably.
15. Focus actions remain visible regardless of active ability filters.

## Known gaps that remain explicit

These are not hidden behind a “ready” claim:

- Historical timezone and daylight-saving conversion remains approximate.
- The city list is still a reduced test gazetteer rather than the complete project database.
- Ground-target selection for AoE and explicit ally-target selection are still simplified by the core resolver.
- North Node / Karmic Ultimate content is not authored.
- Decan and Dwad are displayed, but their authored augment/passive effects are not yet applied.
- Morality morphs, transit modifiers, and eye stage-passives remain deferred.
- Automated Chromium interaction could not be run in the current runtime; validation is engine/view-model headless plus static page auditing. Manual browser acceptance remains required.

## Recommendation

Use V3.1 as the only current testing candidate. Keep the 1-D page and V2 files as references until the manual acceptance checklist passes. Do not repoint the primary published artifact until those browser checks are complete.
