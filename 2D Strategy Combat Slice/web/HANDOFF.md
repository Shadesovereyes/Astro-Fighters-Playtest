# Astro Fighters — Web Slice Handoff

_Last updated: 2026-08-17 after the striker/grappler balance pass, movement-phase and initiative
engine fixes, opponent-level UI, and the 1vX/scalable-roster scenario rewrite._

## Current state

- **Repository:** `Shadesovereyes/Astro-Fighters`
- **Working branches:** `claude/astrofighters-v3-4-web-qw2utw` and
  `claude/astrofighters-test-version-p1sw5a` — kept in sync by identical pushes; both currently
  at the same commit.
- **Unity/source branch:** `claude/astro-fighters-art-direction-dw2a5t`
- **Known unmerged sibling branch:** `claude/astro-fighter-dev-continue-1pffha` (diverged
  2026-08-13, last commit 2026-08-14, never merged) — 17 commits, most economy changes already
  independently re-adopted here, its scenario system superseded by 2026-08-17's roster rewrite,
  its dead-target retarget fix ported 2026-08-17. See the "2026-08-17" entries in
  `docs/DECISIONS.md` for the full reconciliation state and what's still genuinely unreviewed.
- **Canonical web entry:** `web/index.html`
- **Active tactical build:** `web/astro-fighters-2d-v3.4.html` (self-identifies as V3.5 —
  `AF.VERSION`/`AFUI.VERSION` — the filename was never renamed off V3.4; do not read the
  filename as the version).
- **Self-contained playtest build:** `web/astro-fighters-standalone.html`, rebuilt via
  `node build-standalone.js` from the split modules below.
- **Published Artifact build:** `web/astro-fighters-artifact.html`, rebuilt via
  `node build-standalone.js --artifact` — this is the fragment published to the live Artifact
  URL. Both standalone and artifact builds must be regenerated and republished together any time
  a runtime module changes; neither is committed-then-forgotten-stale on purpose.
- **Legacy published build:** `web/astro-fighters.html`.
- **Canonical ability source:** the native Google Sheet `AstroFighters_Abilities` —
  <https://docs.google.com/spreadsheets/d/193zbxqh5M08Du3NqUlCWhNN0qy5TePzxIdML3zuHFww/edit> —
  **not yet reconciled against the 2026-08-17 balance pass below; see "Workbook synchronization
  note."**
- **Ability mismatch audit:** `web/ABILITY_SPEC_AUDIT_2026-08-12.md`
- **Latest session log:** `web/SESSION_LOG_2026-08-17.md`
- **Balance-reference folder:** `web/balance-reference/`

## Canonical ability source and precedence

**The native Google Sheet is the forward canonical ability source.** The repo-root
`AstroFighters_Abilities.xlsx` is an **older snapshot and is NOT canonical** — do not use it
as truth, and do not copy values out of it into runtime. Where the handoff, older audits,
balance-reference files, runtime constants, or the repo XLSX disagree with the Sheet, **the
Sheet wins.**

Precedence inside the Sheet:

1. **Live Canonical Roster** — authoritative names and numeric ability values.
2. **Individual authored source tabs** (Sign Kits, Universal Arts, Martial & Weapon Styles, …)
   — descriptions, tags, stance-child relationships, authored ability identity.
3. **Positional Rules** — authoritative for Grappling/Grappled and Mounting/Mounted
   behaviour, Mount Access classification, positional save-DC modifiers, Mount/submission
   maintenance, passive Stamina recovery modifiers, Pull Guard Poise handling, Hip Escape,
   and positional weapon exceptions. It overrides legacy runtime assumptions about
   grapple/mount behaviour.
4. **Live Sync Notes / Legend & Notes** — additional authoring context.

Do not silently substitute old runtime values when the Sheet disagrees.

### Corrected names that must never regress

`Iron Fist` (Taurus Sign, **not** the Wrestling technique) · `Sumo Palm` (Wrestling, **not**
renamed) · `Wither Palm` (never `Wither Grasp`) · `Diamond Cutter` (never `Diamond Finger`) ·
`Wrestler's Prowess` (distinct from the single `Wrestling Stance`) · `Kyoketsu-Shoge` (never
`Kobudo`; no `Shuriken Throw`) · `Blade Throw` · **no Karate Defensive Stance**.

Do not create another versioned HTML page for ordinary fixes. Update the V3.4 modules, extend the existing smoke suites, and rebuild the existing standalone page.

V3.4/V3.5 has been the published artifact since the 2026-08-14 positional pass; this note is
historical. Do not create a NEW versioned HTML page for a future major pass either — extend
these same modules and rebuild.

## Active runtime files

Load order (see `astro-fighters-2d-v3.4.html`'s `<script>` tags and `build-standalone.js`'s
`MODULES` list — both must stay in sync with each other and with this list):

1. `web/af-core.js` — DOM-free chart, grid, combat, content, status resolution, and AI core.
2. `web/af-dc-model-v3.js` — shared candidate tier/DC/cost model (see "Candidate DC test
   implementation status" below; default-off in ordinary play).
3. `web/af-core-v3-patch.js` — V3 stance annotations, action-plan validation, and player LoS/range enforcement.
4. `web/af-ui-v3.js` — level profiles, attribute budgets, ability grouping, dependency rules, queue projections, and progression scaling.
5. `web/af-page-v3.js` — page controller and SVG arena renderer.
6. `web/af-map-v3.js` — occupied-cell styling, terrain blocker styling, stance reveal, and perception-based hostile visibility.
7. `web/af-progression-v3.js` — DOM allocator and compatibility bridge for the legacy fixed-sum controller. Runs on `setTimeout(installAllocator, 0)` **after** `af-page-v3.js`'s own `DOMContentLoaded` handler finishes, so it always gets the final say on setup-form defaults — see "Player's true default level is 1, not 20" below.

Current smoke suites:

```bash
cd web
node af-core.smoke.js
node af-v3.4.smoke.js
```

Standalone + Artifact rebuild (run both after any runtime module change):

```bash
cd web
node build-standalone.js
node build-standalone.js --artifact
```

## Implemented systems that must not regress

- Real natal-chart calculation with manual birth UTC offset.
- Canonical chart progression from L1 through L100 milestones.
- Attribute allocation: base 6, 14 points at L1, +5 points per later character level, escalating marginal costs after 20/30/40/50.
- Career progression with character XP and per-ability XP, ability level cap 10, and persisted career identity/stats.
- Ability leveling increases offensive power and Stamina/Chakra cost; Focus/stance abilities do not level.
- Healing remains Chakra-negative by design. **Palm Healing is learned Medical content (not automatic), 25 base Chakra, authored Heal power 15, 1 slot, adjacent/melee range, and resolves at 70% of its normal post-mastery heal curve**. Cauterize and inherent kit heals retain their authored identities unless separately ruled.
- Universal Focus actions (`Catch Breath`, `Charge Chakra`) remain permanently visible, restore **20% of the channel's max pool**, grant **no Poise**, and can fund later queued actions in the same round.
- Multiple trained Martial styles with parent-stance child gating.
- Weapon, eye, and other dependency-based child gating.
- **Relationship-aware positional combat** (see the dedicated section below).
- Five-action queue with ordering validation and repetition strain after the second repeated use of the same ability.
- Player-driven main target, per-action target overrides, AoE cell targeting, ally targeting, summon placement, and last-known hidden-enemy ghosts.
- Hex movement, movement-only rounds, terrain, LoS, awareness, fog of war, destructible foliage, and navigable terrain generation.
- Occupied fighter hexes and LoS-blocking terrain receive distinct map readability treatment.
- Reach techniques are melee gap-closers, not ranged attacks; reach does not add movement budget.
- Slow/Snare/Root movement effects share `AF.moveBudget` so engine, UI preview, and planned movement agree.
- Every non-Free relationship role blocks voluntary movement, generic Movement abilities, Teleport, and generic gap-closers; authored relationship techniques (e.g. Rolling Throw) are explicit exceptions.
- Duel (1v1), 1vX gang battle (player vs 1–9 same-faction opponents), Team battle and
  Free-for-all (dynamic roster, up to **10 combatants total including the player** — a
  scalability testbed, not a final gameplay cap), Escort, and Caravan Ambush scenarios
  (2026-08-17 rewrite of the old fixed 1v1/2v2/3-way shapes; see `docs/DECISIONS.md`).
- Opponent/ally level selection in setup, defaulting to and tracking the player's own level
  until a specific field is edited by hand (`AF.scaleEnemyStats`, 2026-08-17).
- Movement resolves as its own AGI-priority sub-phase before actions each round; initiative
  ties within the action-scheduling loop also go to the higher current AGI (2026-08-17 engine
  fixes — see `docs/DECISIONS.md`).
- A queued single-target attack whose chosen enemy is defeated before it resolves (mid-round or
  stale at round start) retargets to the weakest reachable foe instead of fizzling or being
  silently dropped (2026-08-17).
- Auto-resolve continues a team/objective battle when the human player is downed.
- Combat-log copy control and round separators.
- Status/eye indicators are perception-gated so hidden opponents do not leak information.

## Cleanup rule

The old V1/V2/V3/V3.1 tactical pages, obsolete V2/V3.0–V3.3 smoke suites, and temporary multi-style patches were removed. **Git history is the archive. Do not reintroduce versioned HTML/JS copies for routine fixes.**

`web/balance-reference/` is intentionally the one exception for balance-analysis documents and machine-readable test outputs; it keeps reference material out of the runtime-file namespace.

## Canonical Martial / Weapon rulings already approved

### Global authoring rules

- Guard Break is **1.5x poise damage**, except explicitly separate authored mechanics such as Suplex's 2x poise treatment.
- A Guard Break ability must cost more resource than a comparable clean ability in the same family/role.
- DOT and harmful-status/control abilities must cost more in **every resource channel they consume** than comparable clean abilities.
- Extra action slots supplement resource premiums; slots do not replace them.
- If an ability combines Guard Break and a harmful rider, both premiums must remain visible.
- Repetition strain must be enabled in balance testing.
- Stance-flow action cost is a real balance cost; cross-style buff borrowing is never treated as free.

### Boxing

- `Jab-Cross`: Physical 10 / 8 Stamina.
- `Haymaker`: Physical 10 / 10 Stamina / Guard Break.
- `Bob and Weave`: AGI +20% for 1 round, 15 Stamina, no movement rider.
- `Defensive Stance`: 15 Stamina, poise overcap/restoration role. **Boxing only** — Karate Defensive Stance is removed and must not be restored.
- `Clinch`: 15 Stamina.
- `Dirty Boxing`: Physical 20 / 25 Stamina / requires grapple.
- `Body Shot`: Physical 8 / 10 Stamina / target Stamina -10.
- The General Taijutsu Solar Plexus Strike duplicate was removed entirely.
- Approved Boxing mixed-string control: `2x Jab-Cross + 2x Body Shot + 1x Haymaker`.
- **Open item (2026-08-17):** Boxer is the highest-net-win-rate style NPC in either archetype
  bracket (76.3% in the striking mirror) — that's now the dominant explanation for Karateka's
  remaining floor after the Karate damage pass below, not Karate being broken. Not yet
  investigated or ruled on; see `docs/DECISIONS.md`.

### Karate

Numbers below are current runtime (verified against `af-core.js`), post the 2026-08-17 damage
pass — see `docs/DECISIONS.md` for the full round-robin evidence and rationale. **Stamina costs
were deliberately left untouched by that pass**, per owner direction; only power changed.

- `Sweeping Low`: Physical **7** / 20 Stamina / Prone (save AGI DC 12) / 1 slot. Intentionally
  modest damage — its job is the Prone control opener, not raw damage. 20 Stamina was already
  the runtime value (a prior "candidate balance floor" note about this is now resolved/stale).
- `Karate Blitz`: Physical **13** / 12 Stamina / Priority + reach(2) / GapCloser / **no Stagger**.
- `Side Kick`: Physical **10** / 10 Stamina / plain melee, no reach / **unconditionally pushes
  the target back 1 tile whenever the base attack lands** (`E.push(1)`, added 2026-08-17 — no
  separate save, a deliberate deviation from the Sheet's originally authored "AGI DC12" gated
  version; see the Sheet-sync note below).
- `Hammer Fist`: Physical **16** / 10 Stamina / Guard Break (1.5x poise).
- `Whirlwind Kick`: Physical **15** / 15 Stamina / 1-tile PointRadius AoE, 1 slot.
- `Horse Stance`: self, 15 Stamina, STR +20% for 1 round (see the temporary-STR section below).
- Approved Karate flow: `Karate Blitz -> Side Kick -> Side Kick -> Sweeping Low -> Hammer Fist`
  (this is the design intent the 2026-08-17 damage pass was tuned to reinforce: blitz in, apply
  Side Kick's push utility, land the Prone opener, follow up with the now-real Hammer Fist
  damage dealer).
- Sweeping Low is intentionally eligible to remain **1 slot** despite S-tier Prone because it has an attack gate, sacrifices damage versus Side Kick, and preserves the approved five-action string; its premium is primarily resource cost.
- Round-robin (120 seeds/matchup): Karateka net win rate in the striking mirror ~2.5% → 23.8%.
  Still the bracket floor — see the Boxing "open item" note above for why.

### Wrestling

Numbers below are current runtime, post the 2026-08-17 grappling-mirror pass — see
`docs/DECISIONS.md` for evidence. Reached ~50% net win rate (parity) in the grappling mirror
after these changes; the underlying Mount-lock-in gap (see the Ground and Pound note) is not
fully closed, just compensated.

- `Suplex`: 40 Stamina (was 50) / power 30 / DC 13 / 3 slots / Mounting only / 2x poise.
- `Choke Slam`: 40 Stamina (was 50) / power 32 / 2 slots / Guard Break / 2x poise.
- `Ground and Pound`: power 12 / 10 Stamina / 2 slots / Mounting only / now also
  **`Stamina −12`** rider on the target (added 2026-08-17), pressuring their Mount-escape/upkeep
  costs. Root cause of its prior underperformance is structural, not numeric: unlike Judo/
  Jiu-Jitsu's Maintained Submission (which makes escaping progressively more expensive each
  round it's renewed), Ground and Pound has no lock-in mechanic, so Wrestling's Mount uptime is
  fragile even though the move itself is resource-efficient. The Stamina rider is partial
  compensation, not a fix for the underlying gap.
- `Sumo Palm`: Physical, power 8, 15 Stamina, 2 slots (unchanged this pass; see the
  2026-08-15 note above about its True→Physical conversion).

### Karate / Wrestling temporary-STR technique

- `Horse Stance` is a **Karate** child: 15 Stamina, STR +20% for 1 round.
- The Wrestling equivalent is `Wrestler's Prowess`: 15 Stamina, STR +20% for 1 round, and is a
  separate ability from the single `Wrestling Stance`.
- Cross-style borrowing pays stance entry, buff action, return stance, and repeats that tax when the buff must be refreshed.

### Weapon anchors

- Kenjutsu Slash: 20 Stamina + Bleed rider.
- Parry: 50 Stamina and negates the next targeted hostile ability.
- Hilt Bash: 25 Stamina, Guard Break + Stun; current resource cost already matches the approved S+GB Stamina floor, but the roster pass recommends 2 slots.
- Precision Thrust: 20 Stamina, True damage + Guard Break.
- Kyudo Shot: 20 Stamina / 2 slots / range 10.
- Arrow Rain: 20 Stamina / 2 slots / AoE.
- Kyoketsu-Shoge `Blade Throw`: 15 Stamina / Bleed rider / **Grappling only**, never while Grappled and never in Mount. (Supersedes the obsolete `Shuriken Throw`, which is no longer canon.)
- Kusari Chain Snare: ranged-Stamina grapple lane.


## Relationship-aware positional combat (2026-08-14)

Canonical source: the Sheet's **Positional Rules** tab. Full implementation notes and test
results are in `web/SESSION_LOG_2026-08-14.md`.

### State model

Relationships are **structural and directional**, held on the fighter, not inferred from
status strings or display names:

```js
f.rel = { role, partner, rounds, voluntary }   // AF.REL: Free | Grappling | Grappled | Mounting | Mounted
f.submission = { holder, receiver, name, ability } | null
f.reservedSlots, f.releaseIntent
```

- Standing Grapple (`Grappling`/`Grappled`) and Mount (`Mounting`/`Mounted`) are **mutually
  exclusive**. A successful transition into Mount clears the standing roles.
- **Mounting never implies Grappling.** No fighter is simultaneously Grappling + Mounting or
  Grappled + Mounted.
- The `Grappling`/`Grappled`/`Mounting`/`Mounted` statuses and the legacy `grappleTarget` /
  `grappledBy` fields are **display mirrors only**, written by `syncRelStatuses`.

### Ability metadata

`AF.POSITIONAL_RULES` encodes the Positional Rules tab (69 audited abilities) and is joined
onto catalog abilities at build time as `ab.pos`:

```js
{ access, req, transition, submission, positionalDc, audited, scope }
```

`AF.positionalLegality(actor, ability, roleOverride?) → {ok, code, reason}` is the **single**
legality authority, shared by the engine, the plan sanitizer, the UI, and the AI.

- `MountAccess = Neither` means the ability **cannot be activated once the actor is already
  Mounting or Mounted**. It does *not* mean the ability can never create Mount — Pull Guard,
  Sweeping Shoulder, Flying Triangle and Suplex are all `Neither` transitions.
- **Blank/unlisted abilities are UNAUDITED and stay legal.** They receive no per-ability
  override. Do not invent legality for unaudited content.

### Removed

The old `Grappled → AttemptEscape()` substitution is **gone**, with `attemptEscape()`,
`canUseWhileGrappled()`, `releaseGrapple()`, the escape-DC constants, and the mid-round
"0 Stamina slips the hold" paths. The blanket `mountGenjutsuDcBonus` (+4 vs a Mounted target)
is also gone. **Do not restore any of them.**

### Canonical numbers

| Rule | Value |
|---|---|
| Standing-grapple Priority | +1 step, **only** vs the specific Grappled opponent; none in Mount |
| Positional save-DC (flagged abilities only, additive, after the live DC) | Free +0 · Grappling +1 · Grappled +1 · Mounting +2 · Mounted −2 |
| Passive Stamina recovery | Free 100% · Grappling 50% · Grappled 50% · Mounting 25% · Mounted 25% |
| Mount upkeep | 10 Stamina (Mounting fighter) |
| Maintained Submission upkeep | 10 Stamina + 1 reserved action slot (holder, Mounting **or** Mounted) |
| Focus restore | 20% of max, no Poise |

Abilities flagged for positional DC scaling: **Nerve Disruptor**, **Numbing Strike**,
**Calf Kick**. Do not extend the scaffold to other status abilities without an owner ruling.

### Round order

```
1. resolve normal round actions
2. postRoundEffects()          — status ticks / stealth / sleep / haunt / buff decay
3. relationshipMaintenance()   — snapshots roles at phase start
4. passiveRecovery(snapshot)
5. next-round planning
```

Maintenance runs **before** recovery: a fighter can never rely on the regen that is about to
happen to pay this cycle's upkeep. The role snapshot is taken at the start of maintenance, so
a relationship that collapses during the phase still recovers at its old rate that tick.

### Maintenance rules

- The **Mounting** fighter always pays **10 Stamina** Mount upkeep. Unpaid/declined → Mount
  ends, both Free at melee range.
- **A Maintained Submission has no upkeep and no reserved slot** (owner ruling, 2026-08-15,
  superseding the prompt's passive-upkeep model). The holder — Mounting *or* Mounted — keeps it
  by **re-queueing the submission ability every round**; a round without it releases the hold.
  Not queueing it *is* the release, so submissions have no release control.
- **Each consecutive round escalates the submission's cost AND damage** by
  `BAL.submissionCostEscalation` / `submissionDamageEscalation` (0.5 each): establish ×1.0,
  then ×1.5, ×2.0, ×2.5 … Escalation is per consecutive **round**, not per use — working the
  hold twice in one round ratchets it once. A different technique starts a fresh hold.
- **Submission Lock:** while a hold is live the Mounting fighter cannot voluntarily drop Mount
  to erase it. Mount's own release control is hidden until the hold lapses.
- **A submission resists contested escapes proportionally to its age.** Every turn the hold has
  been worked subtracts `BAL.submissionEscapeDcPerRound` (2) from the DC of an escape flagged
  `pos.escape` — currently Reversal only. The contest denies on `defence + d20 >= attack + dc`,
  so a lower DC is harder for the escaper: DC 10 → 8 → 6 → 4 (48% → 37% → 27% → 16% at even
  stats). Only the fighter **caught** in the hold is resisted, never the holder, and a denied
  attempt still pays its cost. It is never absolutely impossible — the contest is stat-based, so
  a far stronger fighter still breaks a long-held hold.
- **Hip Escape is never gated by this.** It has no DC check — it is flat resource damage, and its
  counterplay is the pressure it puts on the mounter's upkeep. Do not add a roll to it.
- Damage recurs because the holder actively re-uses the ability at an escalating price. This
  supersedes the old "maintenance never repeats initial damage" rule — its purpose (no free
  repeated hits) is now served by the escalating cost.
- **Open interpretation:** the prompt's "submission upkeep replaces Mount upkeep" clause existed
  to stop two *passive* charges stacking. With no passive submission charge left, Mount upkeep
  now always resolves. The alternative (a live submission suspends Mount upkeep) is a one-line
  change and is the lever for the Wrestler's win-rate swing.
- **Zero Stamina is never an escape.** Relationships end only via an explicit effect,
  maintenance failure/voluntary release, or an invalid/dead participant.
- With no explicit release intent, an affordable relationship is **maintained by default**.

### Pull Guard / Hip Escape

- Forced Mounted entry breaks Poise. Successful **Pull Guard** is a voluntary bottom
  transition that **preserves the user's current Poise** (37→37, 4→4, 0→0). Preserve, never
  restore. Jiu-Jitsu Stance alone grants no Poise protection — the exception lives in Pull
  Guard's transition metadata.
- Mount suppresses Poise *recovery*; only the forced entry breaks Poise. (`startRound` no
  longer re-zeroes a Mounted fighter each round — that would erase Pull Guard's preservation.)
- **Hip Escape** (Judo, Mounted only): 2 slots, 20 Stamina, no damage, drains exactly
  15 Stamina from the fighter Mounting the actor, once per round, and does **not** directly
  end Mount or a submission. Its pressure surfaces at the next maintenance check.

### Owner-authored content not yet in the Sheet

These exist in runtime but have **no row in the Sheet** yet. Do not drop them on a future sync.

| Style | Ability | Authored |
|---|---|---|
| Wrestling | **Ground and Pound** — 12 power / 10 Stamina / 2 slots / no secondary effects / **Mounting only** | 2026-08-15 |
| Wrestling | **Reversal** — 0 power / 30 Stamina / 3 slots / DC 10 STR+AGI contest / **Mounted only**; swaps the user from Mounted to Mounting | 2026-08-15 |

Reversal reuses the ordinary mount transition (a `GrappleTech` with `mount:true` used from the
bottom **is** `enterMount(user, opponent)`), so it inherits forced-entry Poise break and clears
any submission over the old position. Its 30 Stamina was chosen, not specified — "mid-high"
against Wrestling's 8 / 15 / 50 ladder.

### Per-style martial NPCs

The combined `Martial Artist` NPC is **removed**. There is now one NPC per martial style —
`Boxer`, `MuayThaiFighter`, `Judoka`, `Jiujiteiro`, `Karateka`, `Wrestler` — each declared with
a `martial:` style key rather than a hand-written `moves()` list. `martialKitFor(styleKey)`
gives each its own stance plus that style's full canonical kit under canonical names, stamped
with the **same** `isStyleStance` / `isStyleTechnique` / `styleKey` / `parentStyles`
annotations a player's trained style receives. Stance-child gating, positional legality and
plan sanitation are therefore identical for NPC and player. They appear automatically in the
enemy/ally pickers via `AF.ENEMY_KEYS`.

**Stat-budget equalization (2026-08-17, owner ruling):** all six style NPCs now total **exactly
48** raw stat points each, enforced by an exact-equality regression test (tightened from an
earlier 2.5-point tolerance band). Each style keeps its own relative shape (Wrestler still leans
STR/FORT, Karateka still leans AGI). Style-vs-style balance testing is only a fair read on the
KITS when every NPC brings the same total budget to it — a prior outlier (MuayThaiFighter at 44
against everyone else's 47–49) had been silently skewing the Boxer/Muay Thai matchup
independent of either kit's own numbers. See `docs/DECISIONS.md` for the root-cause trace.
`AF.scaleEnemyStats(stats, level)` (level-20 anchor, see "Opponent/ally level selection" above)
scales this canonical 48-point block; it does not change the equalization itself.

### AI planning rules that must not regress

- `stanceOpener()` — a fighter whose kit is gated behind a stance opens with the stance that
  unlocks the most legal techniques. The stance must itself be positionally legal.
- The planner projects the relationship role through its own plan via
  `AF.advanceProjectedRole`, **shared with the plan sanitizer**. Planner and sanitizer must
  always agree: every pick is legal under the projected role, and past
  `BAL.aiMaxProjectedChain` (2) it must also be legal under the fighter's real role. If they
  drift apart the sanitizer silently guts AI plans — watch the "removed from the plan" log
  count, which must stay at 0 in AI-vs-AI runs.
- `plannerSelfRestore()` — the AI credits Focus restores when projecting affordability, the
  same way `AFUI.selfRestore` does for the player.
- `decideRelease()` — NPCs use the explicit release path when their position offers no legal
  offence. Controlled fighters have none, and Submission Lock still applies at maintenance.
- **(2026-08-17) Guard Break poise damage is scored as real tempo denial**, not just folded
  silently into an ability's raw damage score. Reuses the existing `poiseDamage()` formula and
  the planner's already-computed base-damage estimate; scores higher when the estimated poise
  damage would break the target's current Poise outright.
- **(2026-08-17) Self-Buff effects are scored by real magnitude and duration**, replacing a flat
  useless `+4` that didn't distinguish a strong buff from a token one. A dedup guard stops the
  AI from re-buffing a stat that already has an active buff.
- **(2026-08-17) The Push effect (Karate Side Kick's new rider) has a flat planner score.** No
  attempt was made to value positional consequences (e.g. pushing a foe off a hazard, or out of
  an ally's reach) — that would need real board-state lookahead the greedy per-slot planner
  doesn't have.
- **Known planner limitation, not yet addressed:** the planner scores each slot's best pick
  independently — it has no combo/sequencing awareness across a multi-action plan. The Karate
  damage pass (below) worked around this by shaping per-move power so the *existing* greedy
  scoring naturally prefers the intended combo, rather than teaching the planner to plan ahead.

Together the pre-2026-08-17 items fixed a **Focus-loop stalemate**: a Mount-illegal style
(Boxing) Mounting a fighter who held a bottom submission had zero legal actions, could not drop
the mount because of Submission Lock, and neither side could afford to act.

### Known gaps

1. **Numbing Strike's base save DC is not finalised.** The positional hook is wired; no base
   DC was invented.
2. ~~**Karate Side Kick's authored "AGI DC12, push back 1 tile"** rider is unimplemented.~~
   **Resolved 2026-08-17**, but not as originally authored: the owner ruled it should push
   **unconditionally whenever the base attack lands, with no separate save**, after the DC-gated
   version's concern (a Karateka locking an opponent with repeat pushes) was checked against
   movement-budget math and ruled out. The Sheet still describes the DC-gated version — **the
   Sheet needs updating to match**, or an owner ruling to keep the Sheet's DC and change runtime
   back; do not silently resync to the DC version without that ruling.
3. **Kyoketsu-Shoge fractional ranges** ("1/3" and "1/2 Zone of Awareness") are approximated
   as fixed tile radii (3 and 6); needs an owner ruling.
4. **Standing-grapple hold upkeep (5 Stamina) is unaudited legacy behaviour** preserved from
   the old runtime and moved into the maintenance phase.
5. **Melee approach churn** — pure-melee fighters often spend rounds out of range of each
   other. Pre-existing, but was substantially reduced (not eliminated) by the 2026-08-17
   movement-phase AGI-priority fix below — that fix addressed an unfairness bug in *who* wins a
   contested cell, not the underlying "both fighters need a full round to close" pacing issue.

### Economy values reconciled 2026-08-15

The previously published artifact carried two values that had never existed in this repo:
`poiseRegenMaxPercent 0.10` (**Sheet-mandated** — "Focus actions & poise regen" rules passive
poise regeneration at 10% of max per round, was 25%; this branch was stale) and
`staminaBase 50` (not ruled in the Sheet; **adopted on the owner's call** rather than
silently discarded). Both are now in runtime. Always diff a published artifact against the
branch before overwriting it — those two values existed nowhere else.

### Archetype ruling — how to balance-test the style NPCs

**Striking and grappling styles are deliberate counter-play (owner ruling, 2026-08-15).**
Compare balance **only within an archetype**. A striker losing to a grappler, or the reverse,
is the intended matchup dynamic and is never a balance defect. Do not read cross-archetype
win rates as a balance signal.

| Archetype | Styles |
|---|---|
| Striking | Boxer, Muay Thai Fighter, Karateka |
| Grappling | Judoka, Jiu-Jitsu Fighter, Wrestler |

Recorded as `AF.ENEMIES[key].archetype` and asserted in the smoke suite, including that only
grappling styles carry relationship techniques.

### Within-archetype balance — baseline (superseded numbers, kept for trend context) and current state

Every ordered pairing inside each archetype x 20 seeds; the ORIGINAL pass below changed no
authored value, and is kept here only so the 2026-08-17 before/after deltas in `docs/DECISIONS.md`
are legible. **Do not treat the numbers in this subsection as current** — see the "ruled and
fixed" / "still open" split right after it.

- **Striking mirror** (120 battles, avg 5.5 rounds): Boxer 91%, Muay Thai 50%, Karateka 9%.
  Karate has the lowest power-per-Stamina in the archetype.
- **Grappling mirror** (120 battles, avg 18.8 rounds): Judoka 71%, Wrestler 65%,
  Jiu-Jitsu 14%. 112/120 reached Mount and 111 established a submission — this is the pool to
  use for positional playtesting.
- **Jiu-Jitsu is the only style with zero standing offence** — every damaging option needs an
  established relationship, so a failed Clinch wastes the round. That is the structural cause
  of its floor.
- Grappling mirrors run ~3x longer than striking mirrors. That follows from the approved
  Mount economy and is expected.

**Ruled and fixed (2026-08-17):** Karate's floor was ruled **not** intended and given a
targeted damage pass (net win rate ~2.5% → 23.8% — see the Karate section above and
`docs/DECISIONS.md`). Wrestling's grappling-mirror standing was also raised via Suplex/Choke
Slam cost cuts and the Ground and Pound Stamina rider (→ ~50% net, parity). All six style NPCs'
stat totals were additionally equalized to 48, which had been a confound in the Boxer/Muay Thai
matchup specifically (see "Per-style martial NPCs" above).

**Still open:**
- **Boxer is now the clear striking-mirror outlier** (76.3% net win rate) — this is the
  dominant remaining explanation for Karateka's residual floor, not a Karate defect. Not yet
  investigated.
- **Whether Jiu-Jitsu's ~14% floor is intended** was not addressed this pass — no Jiu-Jitsu
  ability numbers were touched. Its "zero standing offence" structural cause above still
  applies. Needs its own owner ruling and pass, same shape as Karate's.
- Re-run the full within-archetype matrix (not just the pairings that moved) after any further
  changes, since a stat-budget or AI-scoring fix can shift matchups that weren't directly
  touched — as the Boxer/Muay Thai case demonstrated.

## DC / CC / DOT balance framework — current owner-locked rules

Detailed reference lives under `web/balance-reference/`.

### Intrinsic tier is not final slot cost

A harmful effect receives an **intrinsic CC/DOT tier** based on what happens after it lands. Final action-slot and resource cost are then determined by the complete package: attack-roll gate, save reliability, duration/magnitude, setup requirements, damage sacrificed or gained, Guard Break, range, AoE, Reach, Priority, repetition strain, and other advantages.

Do not use a rule such as `S tier = 3 slots` in isolation.

### Working intrinsic tiers

- **S:** Prone, Stun, Fear, Sleep; Mounted is S-value but belongs to the setup-gated grapple lane.
- **A:** Grappled-value states, Confusion, Blind, strong Root variants.
- **B:** Slow, Snare, Silence, Disarm; matchup-dependent tactical denial.
- **C:** light Bleed/Burn/Poison/Psychosomatic, Cripple, and other attrition riders; DOT tier rises with total damage/duration.

### Equal-investment rider reliability targets

These percentages are the chance the status lands **after the attack already hit** for ordinary damaging riders:

| Tier | Equal-investment rider landing target |
|---|---:|
| C | **60%** |
| B | **45%** |
| A | **~35%** |
| S | **~30%** |

C/B effects are intentionally reliable enough to feel like natural consequences of a hit. Example: if a sword connects, a light Bleed should occur more often than not.

Pure control and AoE/single-gate control do not receive the normal single-target hit gate, so they require larger slot/resource premiums.

### Owner-locked melee-Stamina rider ladder

For a normal damaging melee-Stamina rider, base floors are:

| Package | Stamina floor |
|---|---:|
| C rider | **10** |
| B rider | **12** |
| A rider | **15** |
| S rider | **20** |
| S + Guard Break | **25** |

Pure A and Pure S control must cost **more resource** than damaging riders of the same intrinsic tier. Exact pure-control floors remain provisional until live-engine sustain tests are complete.

### Resource-family hierarchy is intentional

Comparable raw resource costs must preserve:

**melee Stamina < ranged Stamina < Chakra**

This is a deliberate design choice. Chakra offensive/control abilities buy inherent range and therefore pay a higher numerical resource cost. Kyudo and other genuinely ranged Stamina techniques intentionally cost more Stamina than ordinary melee techniques because they buy the same positional/range advantage without spending Chakra.

Use **resolver-true spend**, not only the catalog number. Elemental Ninjutsu already pays `BAL.elementalCostMult = 1.75`; do not add a second blanket range multiplier that double-charges Elemental abilities.

## Live V3.4 DC formula — owner-approved for live playtesting

The current best roster-wide candidate is:

```text
StatEdge = clamp(trunc((AttackerControlStat - DefenderSaveStat) / 5), -6, +6)
MasteryBonus = floor(AbilityLevel / 4)
DC = TierOffset + StatEdge + MasteryBonus

TierOffset: C=13, B=10, A=8, S=7
Natural 1 on save -> status lands
Natural 20 on save -> status resisted
Otherwise d20 >= DC resists
```

This model keeps equal-investment L0 reliability at 60/45/35/30 regardless of absolute level, rewards specialization through mid/high career levels, and caps extreme mastered S-tier reliability around 70% on the save check rather than becoming automatic.

At a representative 75% single-target hit chance, equal-investment base raw-attempt proc rates are approximately C 45%, B 33.75%, A 26.25%, S 22.5%.

## Roster-wide simultaneous simulation — 2026-08-12

Scope tested from the current runtime catalog:

- **94 Sign-kit abilities**
- **25 Universal/Generic/Medical/Trap/Summon abilities**
- **39 Martial abilities**
- **12 Weapon abilities**
- **170 total abilities**

Within those 170:

- 61 abilities directly apply ordinary tiered hostile Status/DOT effects.
- 53 direct hostile effects currently use authored fixed saves.
- 10 direct hostile riders currently have no save at all.
- 14 abilities use the separate grapple/grapple-tech/mount control lane.
- 5 abilities directly deny Stamina/Chakra and need their own drain-value tiers.

### Fixed authored DCs are mathematically obsolete

The current engine save is effectively `defender effective stat + d20 >= authored DC -> resist`, while most catalog DCs are 11–14.

Against balanced career stats:

- at character level 1, the 53 fixed-save effects average only about **12.1% landing** before any attack gate;
- by level 10, **all 53 become 0%** against an equally built balanced defender;
- they remain 0% at higher balanced stat bands.

The static authored DC values therefore cannot survive career-stat growth.

### Automatic hostile riders are the opposite extreme

Current automatic riders identified in the requested roster include Mach Lunge Burn, Sun Palm Burn, Sandstorm Bleed, Aero Palm Bleed, Numbing Strike Slow, Adamantine Shin Bleed, Solar Flare Blind, Viper Strike Bleed, Flash Bomb Blind, and Spike Pit Bleed.

Unless an automatic rider is explicitly intended as a fantasy exception, it should enter the shared tier-save system. A normal 75% attack-gated automatic rider currently applies on 75% of raw attempts; an AoE automatic rider applies to every affected target because the current AoE resolver does not make the normal accuracy roll.

### AoE is a single-gate control package

`resolveAoe` applies effects directly to occupants in the radius. A damaging AoE + harmful status is therefore not equivalent to a single-target attack-gated rider. Price A/S AoE control closer to pure control reliability, then add extra-target value through resource/slot cost.

### Grapples remain a separate lane

Do not convert Clinch, Single Leg Shot, Kusari Chain Snare, mount advancement, or grapple follow-ups to the generic C/B/A/S DC formula yet. Grapples already pay through attacker-vs-defender contests, setup actions, rooting, escape checks, hold upkeep, mounted-state requirements, and follow-up dependency.

### Clean resource-family medians from the current runtime

Using resolver-true cost:

| Family | Median clean damaging spend |
|---|---:|
| melee Stamina | **10** |
| ranged Stamina | **20** |
| Chakra | **35** |

This supports the intended hierarchy and is the baseline for future same-family comparisons.

### Roster cost/slot outliers

The floor audit found **35 direct-status abilities below the candidate minimum resource floor** and **26 direct-status abilities that should increase action-slot cost** under the current model.

Important S-tier examples:

- Shatter Punch: 12 Stamina -> candidate S+GB floor 25, 1 -> 2 slots.
- Sonic Sweep: 12 -> candidate 20, 1 -> 2 slots.
- Hydro Cannon Palm: 10 -> candidate 20, 1 -> 2 slots.
- Heavenly Kick: 10 -> candidate 20, 1 -> 2 slots.
- Sweeping Low: 8 -> candidate 20, remains 1 slot.
- Pure S Genjutsu Killing Intent / Kneel / Siren's Lure / Escapism: current 18 Chakra -> provisional pure-S Chakra floor 45, 1 -> 3 slots.
- Hilt Bash: already 25 Stamina, recommend 2 slots.
- Mausoleum / Bubble Prison already have substantial resolver-true Elemental spend; mainly need the hard-control slot tax rather than another blanket Chakra increase.

### 50,000-attempt Monte Carlo results

The 61 ordinary Status/DOT abilities were each tested under equal L0, equal L10, level-20 specialist attacker L10, and level-20 specialist defender L10 conditions.

Aggregate candidate results:

| Tier / delivery | Equal L0 | Equal L10 | L20 specialist attacker L10 | L20 specialist defender L10 |
|---|---:|---:|---:|---:|
| C attack-gated | 45.1% | 52.5% | 71.2% | 33.8% |
| B attack-gated | 33.8% | 41.2% | 60.0% | 22.6% |
| B single-gate | 45.1% | 55.1% | 79.9% | 29.9% |
| A attack-gated | 26.2% | 34.0% | 52.3% | 15.2% |
| A single-gate | 34.9% | 45.0% | 70.0% | 20.0% |
| S attack-gated | 22.4% | 29.8% | 48.8% | 11.2% |
| S single-gate | 29.9% | 39.9% | 65.0% | 15.0% |

The candidate curve is internally coherent across the requested roster: specialization matters strongly, save investment counters it, and hard control does not become automatic.

### Simultaneous slot/resource sustain result

With representative resource stat 10 and the candidate floor/slot rules:

- C riders: generally 3–4 repeated uses depending on family/cost.
- B riders: generally 4–5, with expensive packages lower.
- **All 18 A-tier direct-status abilities cap at exactly 2 same-ability uses per round.**
- S pure/single-gate hard control: generally 1 use.
- Ordinary S attacks: generally 2 uses.
- Sweeping Low is the deliberate base-level exception at 3 repeated uses because it remains 1 slot; at ability L10, cost growth reduces it to 2 repeated uses. Its intended Karate string only uses it once.

Slots enforce the hard frequency ceiling; resource cost determines whether the fighter can actually afford the ceiling. That is the intended simultaneous balance behavior.

## Balance-reference files

`web/balance-reference/` is the canonical working reference for this balance phase:

- `README.md` — index and locked/provisional distinction.
- `DC_CC_BALANCE_FRAMEWORK.md` — intrinsic tiers, reliability targets, and effect-tier-vs-slot distinction.
- `DC_COST_MODEL_V0_2.md` — unified slot/resource model and resource-family hierarchy.
- `DC_SIMULATION_PASS_01.md` — early sustain/action-pressure/DC experiments; historical candidate values.
- `DC_SIMULATION_PASS_02.md` — career-stat scaling and recommended `/5, ±6` candidate.
- `DC_ROSTER_SIMULATION_PASS_03.md` — full 170-ability roster audit.
- `DC_ROSTER_SIMULATION_PASS_03B.md` — 50k-attempt Monte Carlo and sustain follow-up.
- `full_roster_dc_cost_pass.csv` — per-ability 170-row audit output.
- `full_roster_monte_carlo.csv` — 61-row direct-status Monte Carlo output.
- `roster_balance_summary.json` — compact machine-readable summary of scope, locked rules, candidate DC, and aggregate findings.

The matching development copies under `docs/` remain valid; `web/balance-reference/` exists so a model working directly in `web/` has the full balance context without relying on chat history.

## Important unresolved balance gates

Before writing the candidate model roster-wide into runtime/workbook:

1. **Assign attacker control-stat identity per ordinary DC ability.** Do not force every technique to use one global offensive stat; choose based on technique identity and discipline.
2. **Review the 10 automatic hostile riders.** Decide whether any are intentional guaranteed exceptions; convert the rest to tier saves.
3. **Lock AoE / extra-target premium.** AoE is single-gate in the current resolver and needs additional multi-target pricing.
4. **Lock resource-drain tiers.** Current drain riders include Body Shot, Spinning Top, Wither Palm, Vice Grip, and Chakra Drain.
5. **Lock harmful Trap Supply premium.** Flash Bomb, Spike Pit, and Caltrops currently pay the same 1 Supply as cleaner traps; harmful effects must pay a premium in every consumed resource channel.
6. **Fix AI planner rider scoring.** Current `planFor().score()` values status effects only in the `else` path when an ability has no Damage effect, so damaging status riders are under-valued by AI. Do not use planner pick-rate as balance evidence until damage + rider expected value are scored together.
7. **Test actual engine battles after candidate implementation.** Probability/economy simulations are not the final acceptance gate.
8. **Only after live tests pass:** write final costs/slots/DC metadata back into runtime and canonical workbook, rebuild standalone, run both smoke suites + browser acceptance, then update `docs/DECISIONS.md` with final locked values.

## Workbook synchronization note

The repo-root `AstroFighters_Abilities.xlsx` is **stale** and is no longer the canonical
source — see "Canonical ability source and precedence" above. It was intentionally not
updated in the 2026-08-14 positional pass. Do not claim any workbook is synchronized to a
newly approved pass unless it has actually been updated. Keep runtime, smoke assertions,
standalone, audit, handoff, and `docs/DECISIONS.md` aligned with the Google Sheet when a
slice is finalized.

**2026-08-17 balance pass — Sheet reconciliation status:** the Karate power redistribution,
Wrestling Suplex/Choke Slam/Ground and Pound changes, and style-NPC stat equalization to 48 are
runtime-only as of this writing; they have not been checked against or written back to the
Sheet. Side Kick's push rider is a **known, deliberate divergence** from the Sheet's authored
"AGI DC12, push back 1 tile" — see Known Gap #2 above — and needs an explicit owner call on
which version (DC-gated or unconditional) the Sheet should reflect before anyone reconciles it.

## Known non-balance gaps

- Manual browser interaction acceptance is still required before publishing V3.4.
- ~~NPC level/stat-budget selection is not exposed in setup.~~ **Resolved 2026-08-17** — see
  "Opponent/ally level selection" above.
- Historical timezone/DST handling and the city database remain incomplete.
- North Node ultimate, morality morphs, transit effects, eye-stage passives, and several chart-layer effects remain deferred.
- **Unmerged sibling branch** `claude/astro-fighter-dev-continue-1pffha` still has a Trained
  Medical Arts kit toggle, career-mode trained-kit additions after birth lock, an NPC
  Focus-log/stance-re-entry fix, and two small Caltrops/traps number differences (Slow duration,
  Stamina-vs-Chakra trap cost) not yet reviewed for porting. See its 2026-08-17 `docs/DECISIONS.md`
  entry for the full reconciliation state.

## Next work — recommended order

1. Implement the candidate tier-DC helper behind a test/balance path and author per-ability control stats for the ordinary Status/DOT roster.
2. Normalize automatic hostile riders except approved guaranteed exceptions.
3. Fix AI damage+rider scoring.
4. Define AoE extra-target premium, drain tiers, and harmful Trap Supply premium.
5. Apply candidate slots/resource floors in a test implementation using resolver-true cost; keep grapples separate and preserve the Sweeping Low 1-slot exception.
6. Run actual engine battles across Sign, Universal, Martial, and Weapon kits at balanced/specialist career profiles and ability L0/L5/L10.
7. Review outliers with the owner before finalizing runtime values.
8. Once approved, synchronize runtime + canonical workbook + smoke assertions + standalone + `docs/DECISIONS.md` + this handoff.

### Standing green-change process

- Develop on the designated working branch (`claude/astrofighters-v3-4-web-qw2utw` / `claude/astrofighters-test-version-p1sw5a`).
- For runtime changes: run `node web/af-core.smoke.js` and `node web/af-v3.4.smoke.js`.
- Rebuild `web/astro-fighters-standalone.html` with `node web/build-standalone.js` when runtime modules change.
- Re-run smoke suites after standalone rebuild.
- Run browser acceptance for UI-affecting changes.
- Do not create new versioned runtime HTML/JS files for ordinary fixes.
- Record major owner rulings and final balance changes in `docs/DECISIONS.md`.


## Candidate DC test implementation status

- `web/af-dc-model-v3.js` contains the shared candidate tier/DC/cost model.
- `af-core.js` now has `BAL.useCandidateDcModel`, **default `false`**.
- When enabled, hostile tiered Status/DOT effects use the candidate save formula; self states remain automatic and grapples remain separate.
- `applyEffects` now passes the originating ability into status resolution.
- Progression annotates abilities with `abilityLevel` so mastery can participate in candidate DC.
- `af-core.smoke.js` deterministically verifies legacy-vs-candidate Killing Intent and automatic-rider normalization with Viper Strike.
- Do not turn the flag on by default or treat the candidate as final canon until per-ability control-stat identities and controlled engine matchup results are owner-reviewed.

**Next:** author/test control-stat identity rules, enable candidate mode only inside controlled matchup harnesses, then run cross-roster battle simulations before final costs/slots are applied.


## Live-engine DC roster pass 04

- Candidate mode is now exercised through the real resolver across the full requested Sign + Universal + Martial + Weapon roster.
- Provisional attacker control-stat defaults under test: Genjutsu→CHA; Ninjutsu/Trap/Medical→INT; finesse physical riders→AGI; force physical riders→STR. **These mappings are not owner-locked.**
- The AI planner bug where damaging abilities skipped rider utility has been fixed: damage and harmful rider value are now additive. Candidate-mode planner scoring also weights rider value by tier and expected landing reliability.
- The live-engine harness writes `web/balance-reference/DC_LIVE_ENGINE_ROSTER_PASS_04.md` plus CSV/JSON results and asserts aggregate observed conditional landing rates stay within 2.5 percentage points of the exact candidate probabilities.
- Candidate mode remains default-off in ordinary play.

**Next:** inspect pass-04 outliers by discipline/control-stat pairing, then run actual multi-round AI-vs-AI kit matchups with candidate mode enabled and candidate slot/resource floors applied only in the test harness.


## 2026-08-13 live balance promotion — continuation state

- `BAL.useCandidateDcModel = true` and `BAL.useCandidateEconomy = true` in normal V3.4 playtesting. The active HTML and standalone both load `af-dc-model-v3.js`.
- Candidate save/economy promotion covers the tested **Sign + Universal + Martial + Weapon** scope. Grapples remain separate. Dojutsu/Bloodline control and dual-resource harmful-package pricing remain future balance work.
- Built player/NPC loadouts receive live package-aware single-resource floors/slots. Mastery magnitude still uses original authored cost, so a balance-price increase cannot grant bonus damage.
- Generic Palm Healing and Cellular Activation are no longer automatic. `generalArts()` retains their catalog records so support NPCs and future learning systems can reference them. The HTML **Learned Medical art** selector is temporary and must eventually be replaced by real ability acquisition + save persistence.
- Palm Healing: authored Heal power **15**, 25 base Chakra, 1 slot, max range 1, final output multiplier 0.70. Neutral-affinity base output is 11 HP. Player targeting and the engine both reject distant chosen allies; auto-targeting considers only allies in range. Support AI values injured in-range allies.
- The old 25–30+ round TTK alarm was largely an artifact of balance harnesses granting mastered Palm Healing to every fighter. Correct access returned the flagged ordinary candidate contexts to roughly the 6–8 round region. **Do not inject universal Palm into future roster tests.**
- Palm 70% team evidence: 2v2 support replacement value 59.2% wins vs 43.2% no Palm; 3v3 74.4% vs 66.1% no Palm. 70% retained nearly all 75% team contribution while reducing defensive-healer solo sustain. The newly live adjacent range still needs manual browser/team positioning validation.
- Balance methodology: no round-cap draws. Resolve to elimination/objective; simultaneous double KO is separate; repeated non-progressing states are failures.

### Next-model priorities

1. Manually browser-test `web/astro-fighters-standalone.html`: learned Palm selection, adjacent ally targeting after movement, distant-target rejection, support NPC behavior, candidate save calculation logs, and displayed tier/resource/slot values.
2. Rerun the full 22-kit **elimination-only** 1v1 matrix from the now-live loadout path, plus representative 2v2/3v3 teams. Do not give ordinary fighters unlearned Medical healing.
3. Recheck the Libra Control-Offense outlier under the real healing-access model.
4. Implement actual find/learn/persist ability acquisition and then remove the temporary learned-Medical HTML override.
5. Test and owner-rule dual-resource harmful-status premiums and the excluded Dojutsu/Bloodline control scope before broadening automated repricing.
6. Do **not** treat repo-root `AstroFighters_Abilities.xlsx` as canonical — the Google Sheet is the forward source. Regenerate the XLSX from the Sheet only if a binary snapshot is separately required.
7. Resolve the positional known-gaps list above (Numbing Strike base DC, NPC stance seeking, Side Kick knockback, Kyoketsu-Shoge fractional ranges, standing-hold upkeep ruling).

Do not restore a combat or simulation round cap.
