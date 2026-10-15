# Session log — 2026-08-14

## Scope

Implemented the approved **relationship-aware positional combat system** in the existing
V3.4 modules. No new versioned HTML/JS implementation was created; the existing standalone
artifact was rebuilt from the same seven modules.

## Authoritative source — precedence change

The canonical ability source for this work is the native Google Sheet
`AstroFighters_Abilities`
(`https://docs.google.com/spreadsheets/d/193zbxqh5M08Du3NqUlCWhNN0qy5TePzxIdML3zuHFww/edit`).

The repo-root `AstroFighters_Abilities.xlsx` is an **older snapshot and was not used** as
truth for this pass. Precedence inside the Sheet:

1. **Live Canonical Roster** — authoritative names and numeric ability values.
2. **Individual authored source tabs** (Sign Kits, Universal Arts, Martial & Weapon Styles, …)
   — descriptions, tags, stance-child relationships, authored ability identity.
3. **Positional Rules** — authoritative for Grappling/Grappled and Mounting/Mounted
   behaviour, Mount Access classification, positional save-DC modifiers, Mount/submission
   maintenance, passive Stamina recovery modifiers, Pull Guard Poise, Hip Escape, and
   positional weapon exceptions.
4. **Live Sync Notes / Legend & Notes** — additional authoring context.

## Files changed

| File | Change |
|---|---|
| `web/af-core.js` | Relationship state model, structured positional metadata, legality resolver, positional DC modifier, Relationship Maintenance phase, submissions, passive-recovery multipliers, standing-grapple Priority, catalog corrections, AI legality. |
| `web/af-core-v3-patch.js` | Slot-order-aware projected positional validation + reserved-slot enforcement in the plan sanitizer. |
| `web/af-ui-v3.js` | Projected relationship role/submission through the queue, positional dependency reasons, reserved-slot cap, relationship label, corrected Focus/grapple-tech effect summaries. |
| `web/af-map-v3.js` | `AFUI.queueContext` override now delegates relationship projection to the core model. |
| `web/af-page-v3.js` | Relationship panel + explicit release control, Mounting/FocusLock token badges, positional badge on ability cards, reserved-slot display, Kyoketsu-Shoge label. |
| `web/astro-fighters-2d-v3.4.html` | `#relationshipPanel` markup and its styles. |
| `web/af-v3.4.smoke.js` | Canonical value corrections + a new positional regression suite. |
| `web/astro-fighters-standalone.html` | Rebuilt via `node build-standalone.js`. |
| `web/HANDOFF.md` | Source-precedence correction and positional-system documentation. |

## 1. Relationship state architecture

`makeFighter` now carries a structural, directional relationship record:

```js
f.rel = { role, partner, rounds, voluntary }   // role ∈ AF.REL.*
f.submission = { holder, receiver, name, ability } | null
f.reservedSlots, f.releaseIntent, f.roundUses
```

- `AF.REL` = `Free | Grappling | Grappled | Mounting | Mounted`.
- `f.rel.role` is the **single source of truth**. The matching status entries
  (`Grappling`/`Grappled`/`Mounting`/`Mounted`) are display mirrors written by
  `syncRelStatuses`; nothing reads legality from them. Legacy `grappleTarget` /
  `grappledBy` are also maintained purely as mirrors.
- Standing Grapple and Mount are mutually exclusive. `enterMount()` clears both
  fighters' relationships first, then assigns Mounting/Mounted, so
  **Mounting never implies Grappling** and a fighter is never simultaneously
  Grappling + Mounting or Grappled + Mounted.
- Transitions: `enterStandingGrapple()`, `enterMount({voluntary})`, `endRelationship()`,
  `setSubmission()` / `clearSubmission()`.

## 2. Structured ability positional metadata

`POSITIONAL_RULES` encodes the Sheet's Positional Rules tab as a build-time data table,
joined onto catalog abilities by `(scope, name)` in `withPos()`. **69 audited abilities.**
Nothing at runtime parses display names.

```js
ab.pos = { access, req, transition, submission, positionalDc, audited, scope }
```

- `MountAccess` = `Neither | MountingOnly | MountedOnly | Both` (`AF.MOUNT_ACCESS`).
- `req` (relationship prerequisite) = `StandingGrapple | Grappling | Grappled | Mount |
  Mounting | Mounted`.
- `transition` = `StandingGrappleEntry | TransitionToMount | VoluntaryMounted |
  RelationshipReposition`.

`AF.positionalLegality(actor, ability, roleOverride?)` returns `{ok, code, reason}`.
Resolution order: Focus (never blocked by relationship, only by explicit Focus denial) →
once-per-round → generic movement/teleport block → Mount Access (when in Mount) →
relationship prerequisite (when not in Mount).

`MountAccess = Neither` means *"cannot be activated after the actor is already Mounting or
Mounted"*. Transition abilities (Pull Guard, Sweeping Shoulder, Flying Triangle, Suplex)
are correctly `Neither` and still create Mount, because they are used *before* Mount exists.

**Blank/unlisted abilities are UNAUDITED** (`access: null`) and stay legal — they receive no
new per-ability override. A visible consequence: unaudited Universal content such as
`Heavenly Kick` remains usable in Mount. That is the Sheet's explicit ruling, not an oversight.

## 3. Legacy auto-escape rule removed

The `if Grappled → replace every action with AttemptEscape()` rule is **gone**, along with
`attemptEscape()`, `canUseWhileGrappled()`, `releaseGrapple()`, the escape-check balance
constants, and the two mid-round "0 Stamina slips the hold" paths. A Grappled or Mounted
fighter now runs any action their positional metadata permits and fails cleanly with a
stated reason otherwise.

## 4. Standing-grapple Priority

`standingGrapplePriority(owner, entry)` grants the Grappling controller one Priority step in
the initiative scheduler, **only** for actions involving the specific Grappled opponent.
Mount grants no equivalent generic bonus.

## 5. Movement / Teleport

`isRooted` now covers every non-Free role, so planned movement is blocked while Grappling,
Grappled, Mounting, or Mounted. `isGenericMovementAbility()` additionally blocks gap-closers,
teleports, and self-relocation abilities — but explicitly exempts authored relationship
techniques (anything with transition metadata or a `GrappleTech` effect), so Rolling Throw
and the other relationship repositions still work.

## 6. Focus

Focus is never blocked by a relationship; only the new `FocusLock` status (applied by Cross
Choke, Strangle, Flying Triangle, Cord Garrote) denies it.

`Catch Breath` / `Charge Chakra` were **stale in runtime** (flat +30 and +25 % Poise). They now
restore **20 % of the channel's max pool and grant no Poise**, per the Sheet.

## 7. Positional save-DC modifiers

`positionalDcModifier(actor, ability)` returns an **additive** modifier applied *after* the
normal live DC calculation, and only for abilities flagged `positionalDc`:

`Free +0 · Grappling +1 · Grappled +1 · Mounting +2 · Mounted −2`

Flagged today: **Nerve Disruptor**, **Numbing Strike**, **Calf Kick**. No other status
ability receives the scaffold.

The obsolete blanket `mountGenjutsuDcBonus` (+4 to any save DC against a Mounted target) was
**removed** — it was exactly the kind of blanket positional DC the Sheet forbids.

## 8. Passive Stamina recovery

`passiveRecovery()` computes the canonical regen first, multiplies by the relationship
factor, then rounds:

`Free 100 % · Grappling 50 % · Grappled 50 % · Mounting 25 % · Mounted 25 %`

A submission adds no further penalty; the fighter's current positional relationship is used.

## 9. Relationship Maintenance phase

`postRound()` was split into the canonical order, wired through `endOfRound()`:

1. resolve normal round actions
2. `postRoundEffects()` — status ticks, stealth, sleep, haunt, buff decay
3. `relationshipMaintenance()`
4. `passiveRecovery()`
5. next-round planning

`relationshipMaintenance()` snapshots every fighter's role at the **start** of the phase and
passes that snapshot to recovery, so a relationship that collapses during maintenance still
recovers at its old rate that tick and resumes Free recovery on the next eligible tick.
Recovery can never retroactively fund upkeep.

## 10–12. Mount maintenance, submissions, Submission Lock

- No active submission → the **Mounting** fighter pays **10 Stamina**. Unpaid/declined →
  Mount ends, both Free at melee range.
- Active submission → the **submission holder** (Mounting *or* Mounted) pays **10 Stamina**
  and reserves **1 of 5 action slots** for the upcoming round, leaving four freely
  programmable. Successful submission upkeep **replaces** ordinary Mount upkeep;
  10 + 10 is never charged in the same cycle.
- Failed/declined submission upkeep → end the submission **first**, then let the Mounting
  fighter resolve ordinary Mount upkeep.
- **Submission Lock:** while a submission is successfully maintained, neither participant
  may drop Mount as a shortcut to cancel it. The UI hides the release control from the
  non-holder and explains why.
- Reaching 0 Stamina mid-round never ends a relationship. Relationships end only through an
  explicit effect, maintenance failure/voluntary release, or an invalid/dead participant.
- **Maintenance never repeats initial submission damage or statuses.** Establishing the
  submission resolves its authored effects once; maintenance preserves the lock only.

Explicit release path: `fighter.releaseIntent`, surfaced as a button in the relationship panel.
With nothing set, an affordable relationship is **maintained by default** — never silently released.

## 15–16. Pull Guard and Hip Escape

- Forced Mounted entry breaks Poise (`poise = 0`, recover delay set).
- Successful **Pull Guard** is a voluntary bottom transition: the user becomes Mounted, the
  opponent becomes Mounting, standing roles end, and the user's **current** Poise is
  preserved exactly (37→37, 4→4, 0→0). Preserve, never restore.
- Jiu-Jitsu Stance itself carries **no** Poise exception — the exception lives in Pull
  Guard's transition metadata.
- `startRound` no longer force-zeroes a Mounted fighter's Poise every round; Mount now
  *suppresses Poise recovery*, and only the forced-mount entry breaks it. Without this the
  Pull Guard preservation would have been erased on the following round.
- **Hip Escape** (Judo, Mounted only): 2 slots, 20 Stamina, no damage, drains exactly
  15 Stamina from the fighter currently Mounting the actor, once per round, and does not
  directly end Mount or a submission. Its pressure surfaces naturally at the next
  maintenance check (regression-tested).

## 17–19. Ability identity and stance children

Corrected to the Sheet:

- Taurus `Sumo Palm` → **Iron Fist** (Mounting only). Wrestling keeps **Sumo Palm**
  (now True damage 5 / 8 Stamina, no poise damage) and is *not* renamed.
- Virgo `Wither Grasp` → **Wither Palm** (Mounting only). `Wither Grasp` is not restored.
- Capricorn `Diamond Finger` → **Diamond Cutter** (Both).
- Weapon style `Kobudo` → **Kyoketsu-Shoge**; kit is Blade Throw / Kusari Chain Snare /
  Chain Yank / Sickle Strike / Cord Garrote. `Shuriken Throw` is **not** canon and was
  removed (the PVE Bandit's "Thrown Knife" now reskins the Kyudo shot).
- Wrestling: `Horse Stance` moved to **Karate**; Wrestling gains **Wrestler's Prowess**
  (Self, 15 Stamina, STR +20 % 1 rd) as a distinct ability. Exactly one ability is named
  `Wrestling Stance`.
- **Karate Defensive Stance stays removed.** Boxing Defensive Stance remains.
- Added missing stance children: Boxing `Uppercut`; Muay Thai `Jab-Cross` + `Uppercut`;
  Judo `Cross Choke` + `Hip Escape`; Wrestling `Choke Slam`.
- `Uppercut` implements "Guard Break only while in clinch" via `poiseMultWhenGrappling`,
  applied only when the user's role is Grappling.

Stance-child reveal uses the existing projected-queue dependency system, with positional
filtering applied **in addition** to stance filtering.

### Numeric reconciliation

Automated comparison against the Sheet after this pass:

- **Martial & Weapon Styles: 59/59 rows match** (power, slots, base Stamina) — no drift.
- **Live Canonical Roster Sign Kits: 94/94 rows match**, none missing, none extra.

## 20. UI / player feedback

- `#relationshipPanel` shows the role (Grappling / Grappled / Mounting / Mounted), the
  partner, any Maintained Submission and who holds it, the upkeep cost, the passive-recovery
  rate, the standing-grapple Priority note, the movement restriction, any reserved slot, and
  an explicit release control (hidden from the non-holder under Submission Lock).
- Ability cards carry a positional badge ("Mounting only", "Mount: both", "Not in Mount",
  "Maintained Submission", "Positional DC", …).
- Lock reasons are player-legible: `Requires Mounting`, `Requires Mounted`,
  `Cannot be used in Mount`, `Requires standing Grapple`, `Requires Grappling`,
  `No movement while in Mount`, `N action slot reserved for submission upkeep`.
- Slot readout shows `used / usable` and names the reservation.
- Token badges added for `Mounting` (🧗) and `FocusLock` (🚫).

## 21. AI

- `planFor().score()` now calls `AF.positionalLegality()` — NPCs obey exactly the same rules
  as the player validator.
- The AI honours `availableSlots()` so it never plans over a reserved submission slot.
- Hip Escape is valued against what the Mounter still needs for upkeep.
- The AI no longer plans style techniques whose parent stance is neither active nor already
  in the plan (`stanceReadyFor`), because the shared plan sanitizer would strip them anyway.
  Measured: **0 stripped AI actions** across 150 AI-vs-AI battles (previously non-zero).

## Test results

```
$ cd web && node af-core.smoke.js     → ok
$ cd web && node af-v3.4.smoke.js     → ok
$ cd web && node build-standalone.js  → wrote astro-fighters-standalone.html (247.7 KB, 7 modules inlined)
```

`af-v3.4.smoke.js` gained a **positional combat regression suite** covering:

- **State:** Grapple→Mount clears Grappling/Grappled; exactly one Mounting and one Mounted;
  Mounting is not automatically Grappling; symmetric partner references.
- **Legality:** all Boxing blocked in Mount; all Karate blocked in Mount; Muay Thai
  Elbow/Knee legal both, all kicks + Jab-Cross + Uppercut blocked; Judo Cross Choke top only,
  Hip Escape bottom only, throws unusable after Mount; Jiu-Jitsu Arm bar top and bottom,
  Strangle top only, Pull Guard/Flying Triangle standing-only; Wrestling Sumo Palm top only,
  Wrestler's Prowess both, Single Leg/Suplex/Choke Slam blocked after Mount;
  Kenjutsu + Kyudo fully blocked; Kyoketsu-Shoge exceptions (stance Both, Sickle Strike Both,
  Cord Garrote both Mount positions, Blade Throw Grappling-only and never Grappled or in Mount);
  Sign spot checks (Iron Fist, Wither Palm, Diamond Cutter, Silica Strike, Aero Palm,
  Flow Strike, Shatter Punch, Hydro Cannon Palm, Kidney Shot, Echo Fist, Shock Palm);
  unaudited abilities stay legal.
- **DC:** modifiers only on flagged abilities; Free +0 / Grappling +1 / Grappled +1 /
  Mounting +2 / Mounted −2; applied after the normal live DC calculation.
- **Passive Stamina:** regen-12 fighter → Free 12, Grappling 6, Grappled 6, Mounting 3,
  Mounted 3.
- **Mount maintenance:** sufficient 10 maintains; insufficient fails; 0 mid-round does not
  escape; recovery cannot retroactively fund upkeep; failed upkeep returns both to Free at
  melee; explicit release path.
- **Submission:** holder can be Mounting or Mounted; 10 Stamina + one next-round slot
  charged/reserved (4 free); no double-charge; failed upkeep ends submission first, then
  Mount upkeep resolves; Submission Lock; no repeated initial damage/status.
- **Pull Guard:** forced Mount breaks Poise; voluntary preserves 37 and 4 exactly; 0 stays 0;
  Jiu-Jitsu Stance alone grants nothing.
- **Hip Escape:** 2 slots / 20 Stamina / exactly 15 drained / no damage / once per round /
  does not end Mount; and a case where its drain causes the *later* upkeep to fail.
- **Focus:** legal in all four roles with exact restore arithmetic; grants no Poise;
  `FocusLock` still denies it.
- **Movement:** gap-closers blocked in all four roles; Rolling Throw still legal; a planned
  move is not executed while engaged.
- **Queue:** stance children reveal; a queued transition projects the new role and reveals
  Mount-only follow-ups; execution revalidation prevents a failed transition from enabling
  an illegal follow-up.
- **AI:** no illegal plans from any of the four roles; reserved slot honoured.
- **Priority:** directional against the Grappled opponent only; none for the Grappled
  fighter; none in Mount.

### Beyond the suite

- **150 AI-vs-AI battles** across four style pairings: 0 crashes, 0 stripped AI actions,
  avg 6.2 rounds, max 10.
- **80 AI battles starting from a live Mount** (half with a pre-set submission):
  0 illegal AI actions, 0 slot overruns, 370 mount-rounds and 175 submission-rounds
  observed, 62/80 relationships ended naturally through maintenance or KO.
- **Headless Chromium check of the rebuilt standalone:** page loads with **no console or
  page errors**; the weapon selector reads "Kyoketsu-Shoge"; forcing the player into Mounted
  renders the relationship panel with the release control and filters the ability window to
  Mount-legal content only. Role-correct stance-child reveal verified in-browser:
  Mounted → Hip Escape only, Mounting → Cross Choke only,
  Grappling → Hip Toss / Rolling Throw / Sweeping Shoulder.

## Unresolved / known gaps

1. **Numbing Strike's base save DC is still not finalised.** The positional modifier hook is
   wired and tested; no base DC was invented. Its live rider currently resolves through the
   candidate tier model like other unflagged riders.
2. **NPCs never seek out a martial/weapon stance.** This is pre-existing (verified against
   the unmodified branch) and means NPCs cannot organically enter Grapple/Mount through a
   martial style. Positional AI legality is correct and tested, but adding stance-seeking is
   a strategy heuristic that was deliberately left out of this pass.
3. **Karate Side Kick's authored "AGI save DC12, push target back 1 tile"** is not
   implemented — there is no target-knockback effect in the engine. Power/cost were synced to
   the Sheet; the rider was left as-is rather than invented.
4. **Range approximations for Kyoketsu-Shoge.** The Sheet expresses Blade Throw as
   "1/3 Zone of Awareness" and Chain Yank/Kusari Chain Snare as "1/2 Zone of Awareness";
   runtime uses fixed tile radii (3 and 6). Needs an owner ruling if fractional
   awareness-derived ranges are intended to be literal.
5. **Standing-grapple hold upkeep (5 Stamina) is unaudited legacy behaviour.** The Sheet only
   defines Mount and submission upkeep. It was preserved and moved into the Relationship
   Maintenance phase; it is no longer evaluated mid-round.
6. **Manual browser interaction acceptance is still required** before promoting V3.4 to the
   published artifact. The headless checks above are not a substitute for the manual
   checklist.
7. **Repo-root `AstroFighters_Abilities.xlsx` remains stale** and was intentionally not
   updated; the Google Sheet is the forward canonical source.


---

# Follow-up — per-style martial NPCs (continued session, 2026-08-15)

## Request

Split the single combined `Martial Artist` NPC into one NPC per martial art style, each with
access to its own stance, then ship a playtest-ready artifact.

## NPC roster change

`ENEMIES.MartialArtist` (a Muay Thai fighter with reskinned flavour names and no real stance
gating) is **replaced by six style NPCs**, each carrying its own stance plus that style's full
canonical kit under **canonical names**, so the positional matrix is directly observable in
play:

| Key | Name | Glyph | Style | Persona | Stats (STR/AGI/FORT/INT/CHA) |
|---|---|---|---|---|---|
| `Boxer` | Boxer | B | Boxing | aggressive | 12/12/10/6/7 |
| `MuayThaiFighter` | Muay Thai Fighter | MT | MuayThai | aggressive | 11/12/9/6/6 |
| `Judoka` | Judoka | J | Judo | brute | 13/11/11/7/6 |
| `Jiujiteiro` | Jiu-Jitsu Fighter | JJ | JiuJitsu | skirmisher | 11/13/10/9/6 |
| `Karateka` | Karateka | K | Karate | assassin | 11/14/9/7/6 |
| `Wrestler` | Wrestler | W | Wrestling | brute | 14/10/12/6/6 |

New `ENEMIES` entries take a `martial:` style key instead of a hand-written `moves()` list.
`martialKitFor(styleKey)` builds the kit and stamps the **same** `isStyleStance` /
`isStyleTechnique` / `styleKey` / `parentStyles` annotations a player's trained style receives,
so NPC stance-child gating, positional legality and plan sanitation are identical to the
player's. The NPCs appear automatically in the enemy/ally pickers (they are driven by
`AF.ENEMY_KEYS`).

## AI changes required to make those NPCs actually work

A style NPC whose whole kit sits behind a stance exposed four real gaps. All four are
legality/liveness plumbing, not strategy:

1. **`stanceOpener()`** - when a fighter's kit is gated behind a stance and none of it is
   currently usable, it opens with the stance that unlocks the most legal techniques. The
   stance itself must pass `positionalLegality`, so a Mount-illegal stance is never queued
   from Mount. This closes the previously-reported gap where NPCs could never reach
   Grapple/Mount organically.
2. **Slot-order-aware planning** - the planner now projects the relationship role through its
   own plan (`AF.advanceProjectedRole`, shared with the plan sanitizer) instead of scoring
   every slot against the current role. Before this, grapplers filled all five slots with
   `Clinch`.
3. **`plannerSelfRestore()`** - the AI now credits Focus restores in its affordability
   projection, exactly as the player's queue planner already did. Without it a submission
   holder would plan `Catch Breath / Focus` and never queue the attack it could afford after
   the restore.
4. **`decideRelease()`** - NPCs can now use the explicit release path. A fighter holding a
   position that offers it no legal offence stops paying upkeep for it. Controlled fighters
   (Grappled/Mounted non-holders) have no release path, and Submission Lock is still enforced
   during maintenance, so this can never bypass an opponent's maintained submission.

Two bounded valuation adjustments were also needed:

- **`GrappleTech` valuation** distinguishes taking top mount from a voluntary bottom
  transition - structurally opposite outcomes that previously scored alike. A voluntary
  bottom transition is only valued positively for a fighter that can actually work a
  submission from underneath.
- **`BAL.aiMaxProjectedChain = 2`** bounds how many actions the AI stakes on a transition it
  has not yet realised. A projected entry can be shrugged off or fall short of range, and
  execution revalidates; past the cap a pick must be legal under the fighter's **real** role
  too, so the rest of the round stays useful when the entry misses.

**Planner/sanitizer agreement is a hard invariant here.** An intermediate version of the cap
made the two disagree and the sanitizer stripped 885 AI actions across 300 battles; the final
rule (every pick legal under the projected role, and additionally under the real role past the
cap) restores **0 stripped actions**.

## Bug found and fixed: the Focus-loop stalemate

The first matrix run left battles unresolved at the 60-round test ceiling. Diagnosis: a Boxer
Mounting a Jiu-Jitsu fighter who held an Arm bar from the bottom. Boxing is entirely
Mount-illegal, so the Boxer had **zero** legal offensive actions; Submission Lock (correctly)
prevented it from dropping the mount; and the Jiu-Jitsu fighter could not afford its own Arm
bar because the planner ignored Focus restores. Both sides Focus-looped forever.

Fixes 3 and 4 above resolve it. After them, **0 of 300 battles are unresolved.**

## Test results

```
$ cd web && node af-core.smoke.js     -> ok
$ cd web && node af-v3.4.smoke.js     -> ok
$ cd web && node build-standalone.js  -> wrote astro-fighters-standalone.html (254.3 KB, 7 modules inlined)
```

New regression coverage in `af-v3.4.smoke.js`:

- `MartialArtist` is gone; each of the six style NPCs exists and is bound to its style.
- Each NPC carries its own stance, annotated with its `styleKey`.
- Each NPC carries every technique of its style, annotated as a child of that stance.
- No other style's techniques leak into an NPC's kit.
- Each NPC's AI plan **opens with its own stance**.
- The Judoka plans a full `Clinch -> Sweeping Shoulder -> Cross Choke` line.
- The projected AI chain depth stays bounded.
- A Mounting Boxer (no legal offence) sets `releaseIntent`; a Mounted fighter does not.

### Style-vs-style matrix - 300 battles (every ordered pairing x 10 seeds)

| Metric | Result |
|---|---:|
| Crashes | **0** |
| AI actions stripped by the sanitizer | **0** |
| Battles unresolved at 80 rounds | **0** |
| Battles reaching a standing Grapple | 190 |
| Battles reaching Mount | 158 |
| Battles establishing a Maintained Submission | 134 |
| Battles using the voluntary release path | 36 |
| Average rounds | 13.6 |
| Longest battle | 67 rounds |

### Browser verification of the rebuilt standalone

No console or page errors. All six NPCs appear in the enemy/ally pickers. A live
player-vs-Judoka battle exercised the whole loop:

```
Judoka locks Starfighter in a standing grapple - Judoka is Grappling, Starfighter is Grappled.
Judoka takes mount on Starfighter, guard shattered - Judoka is Mounting, Starfighter is Mounted.
  Judoka locks in Cross Choke as a Maintained Submission from Mounting.
Judoka maintains Cross Choke from Mounting - 10 Stamina and 1 action slot reserved next round (4 free).
  Starfighter recovers 3 stamina (Mounted 25% of 10).
  Judoka recovers 3 stamina (Mounting 25% of 11).
```

## Reconciliation with the previously published artifact

Before overwriting the live "Astro Fighters - 2-D Testbed V3.4" artifact it was fetched and
diffed against this branch. It turned out to carry **two balance values that have never
existed in this repository on any branch** - work from a session that was never committed
here. Everything else it had was pre-positional legacy this pass deliberately removed.

| Value | Published artifact | This branch (before) | Resolution |
|---|---:|---:|---|
| `poiseRegenMaxPercent` | 0.10 | 0.25 | **Adopted 0.10.** The Sheet's "Focus actions & poise regen" row rules passive poise regeneration at 10% of max per round (was 25%). This branch was stale; a genuine miss from the first pass. |
| `staminaBase` | 50 | 20 | **Adopted 50** on the owner's call. Not ruled anywhere in the Sheet, so it was raised as an explicit decision rather than resolved silently. |

Both are now in runtime, so publishing the rebuilt page discards nothing.

## Archetype ruling — how these NPCs must be balance-tested

**Owner ruling (2026-08-15): counter-play between grappling and striking styles is
intended.** Balance comparisons are only meaningful **within** an archetype. A striker
losing to a grappler, or the reverse, is the designed matchup dynamic and is never a
balance defect.

| Archetype | Styles |
|---|---|
| Striking | Boxer, Muay Thai Fighter, Karateka |
| Grappling | Judoka, Jiu-Jitsu Fighter, Wrestler |

This is recorded in code as `ENEMIES[key].archetype` and asserted in the smoke suite,
including the structural check that only grappling styles carry relationship techniques.
The earlier cross-archetype matrix in this log measured the wrong thing; the numbers below
replace it.

## Balance findings — within-archetype only (NOT changed in runtime)

Every ordered pairing inside each archetype x 20 seeds. No authored value was altered to
improve these; the Sheet and the approved prompt are law.

### Striking mirror — 120 battles

| Style | Record | Win rate |
|---|---:|---:|
| Boxer | 73-7 | **91%** |
| Muay Thai Fighter | 40-40 | 50% |
| Karateka | 7-73 | **9%** |

Average 5.5 rounds, longest 9. Zero crashes, zero stripped AI actions, zero unresolved.
No grapples occurred, as expected for a striking mirror.

**Karate is badly underpowered among strikers.** Its kit is the lowest power-per-Stamina in
the archetype: Sweeping Low 5 power / 20 Stamina, Karate Blitz 8/12, Side Kick 8/10, Hammer
Fist 10/10, Whirlwind Kick 10/15. Boxing gets Jab-Cross 10/8, Uppercut 12/12 and Haymaker
10/10 with Guard Break over the same Stamina band. These are authored Sheet values, so this
is reported rather than tuned.

### Grappling mirror — 120 battles

| Style | Record | Win rate |
|---|---:|---:|
| Judoka | 57-23 | **71%** |
| Wrestler | 52-28 | 65% |
| Jiu-Jitsu Fighter | 11-69 | **14%** |

Average 18.8 rounds, longest 46. Zero crashes, zero stripped AI actions, zero unresolved.
**112 of 120 battles reached Mount and 111 established a Maintained Submission** — the
positional system is heavily exercised in this pool, which makes it the right pool for
positional playtesting.

**Jiu-Jitsu is badly underpowered among grapplers**, and the structural reason is clear: it
is the only style in the game with **zero standing offence**. Its entire kit is Clinch, Pull
Guard, Strangle, Flying Triangle and Arm bar — every damaging option requires an established
relationship, so a failed Clinch is a wasted round. Judo still has Hip Toss / Rolling Throw /
Sweeping Shoulder, and Wrestling has Sumo Palm as a standing True-damage attack.

### Pacing note

Grappling mirrors run roughly 3x longer than striking mirrors (18.8 vs 5.5 rounds). That
follows directly from the approved Mount economy — 10 Stamina Mount upkeep plus 10 for a
submission against a 25% passive recovery — and is expected, not a fault. It is worth knowing
when scheduling playtest sessions.

### Open questions for owner ruling

1. Is Karate's striking-mirror floor (9%) intended, or should its power-per-Stamina rise?
2. Is Jiu-Jitsu's total lack of standing offence intended? It is thematically coherent but
   costs it the grappling mirror (14%).
3. **Numbing Strike's base save DC remains unresolved**, exactly as the prompt stated. The
   positional modifier hook is wired and tested; no base DC was invented.

## Playtest artifact

`node build-standalone.js --artifact` now also emits `web/astro-fighters-artifact.html`: the
same page as an Artifact-ready fragment (the `<head>` contents minus host-supplied meta tags,
followed by the `<body>` contents), because the Artifact host supplies its own
`<!doctype>/<html>/<head>/<body>` skeleton. The transform asserts that no wrapper tag
survives. The fragment is a derived build output and is gitignored.

The page is fully self-contained - no external scripts, styles, fonts or images - and was
verified rendering inside a replica of the host skeleton before publishing. It updates the
existing "Astro Fighters - 2-D Testbed V3.4" entry rather than creating a new link.


---

# Follow-up — submissions kept by use, not upkeep (2026-08-15)

## Owner ruling

The release button for submissions is unnecessary. A Maintained Submission is now held by
**re-queueing the submission ability every round**; a round that passes without it releases the
hold. And like abilities used in succession, **each consecutive round raises both the resource
cost and the damage** of the submission.

This supersedes prompt section 11's passive-upkeep model (10 Stamina + 1 reserved action slot)
and section 13's "maintenance never repeats the initial damage" — damage now recurs because the
holder is actively re-using the ability and paying an escalating price for it, which was the
concern that rule guarded against.

## What changed

| Old (prompt section 11) | New |
|---|---|
| 10 Stamina passive upkeep at maintenance | **No passive upkeep** |
| 1 of 5 action slots reserved next round | **No reservation** — the full slate stays programmable |
| Explicit release control for the submission | **None** — not queueing it *is* the release |
| Submission upkeep replaced Mount upkeep | **Mount upkeep always resolves on its own terms** |
| Maintenance never repeats initial damage | Damage recurs by re-use, escalating each round |

### Escalation

`BAL.submissionCostEscalation = 0.5` and `BAL.submissionDamageEscalation = 0.5`.

Establishing the hold is charged at face value. Every consecutive round after that steps up:

| Round of the hold | Cost / damage | Cross Choke Stamina |
|---|---|---:|
| 1 (establish) | x1.0 | 15 |
| 2 | x1.5 | 23 |
| 3 | x2.0 | 30 |
| 4 | x2.5 | 38 |

Escalation is **per consecutive round, not per use** — working the hold twice in one round does
not ratchet it twice; repeat uses inside a round pay ordinary repetition strain instead.

A continuation is identity-matched: same holder, same partner, same authored technique. Switching
to a different submission starts a fresh hold at face value.

### Submission Lock survives

While a submission is live, the Mounting fighter still cannot voluntarily drop Mount to erase it.
Mount keeps its own explicit release control, which is hidden while a submission holds. Once the
submission lapses, the same release intent ends Mount normally.

## Interpretation I had to make — flagged for a ruling

Prompt section 11 said successful submission upkeep *replaces* ordinary Mount upkeep, so 10+10 was
never charged in one cycle. That rule existed to stop **two passive charges** stacking. The
submission now has no passive charge at all, so I read the replacement clause as dying with the
upkeep it referred to: **Mount upkeep (section 10, still law) now always resolves**, and the
submission is paid purely through its escalating action cost.

The alternative reading — a live submission suspends Mount upkeep — is a one-line change if you
prefer it. It matters: see the Wrestler swing below.

## Files changed

`af-core.js` (constants, submission record, escalation, maintenance, AI), `af-core-v3-patch.js`
(slot message), `af-ui-v3.js` (escalated quoting, relationship label), `af-page-v3.js` (panel,
ability-card price, no submission release), `af-v3.4.smoke.js` (rewritten submission suite).

## Test results

```
$ cd web && node af-core.smoke.js     -> ok
$ cd web && node af-v3.4.smoke.js     -> ok
$ cd web && node build-standalone.js --artifact -> ok
```

Rewritten submission regression coverage:

- A hold worked this round survives maintenance, with no passive charge and no reserved slot.
- A hold not worked this round is released, and Mount upkeep still resolves afterwards.
- The holder may be Mounting or Mounted; the Mounting fighter always pays Mount upkeep.
- Submission Lock blocks a voluntary Mount release while the hold is live, and stops blocking
  once it lapses.
- Escalation multipliers: fresh x1.0, first continuation x1.5, then x2.0, x2.5.
- Continuation is identity-matched by holder, partner and technique.
- End to end through the real resolver: three worked rounds give two escalation steps, the player
  quote rises each round, the **engine** charges that escalated cost (one Stamina short and the
  action fizzles), damage rises each round, and skipping a round releases the hold.
- Working the hold three times in one round ratchets it exactly once.
- A style NPC holding a submission re-queues it rather than letting it lapse.

### AI fix found on the way

The planner never valued grapple-tech damage at all — a 25-power Cross Choke scored lower than a
jab, because its power lives on the `GrappleTech` effect rather than a `Damage` effect. Now scored
explicitly, with the submission escalation applied.

### Browser verification

No console or page errors. With a live Cross Choke the panel reads *"queue Cross Choke again this
round or the hold is released · round N of the hold · next application x2.0 cost, x2.0 damage"*,
there is **no** submission release button, slots read `0 / 5`, and the ability card quotes the
escalated Stamina (15 / 23 / 30 / 38).

## Balance impact — grappling mirror, 120 battles

| Style | Before (passive upkeep) | After (use-based + escalation) |
|---|---:|---:|
| Wrestler | 65% | **90%** |
| Judoka | 71% | 40% |
| Jiu-Jitsu Fighter | 14% | 20% |
| Avg rounds | 18.8 | 17.8 |
| Battles with a submission | 164/300 | 106/120 |

**Submission chains average 1.6 rounds and top out at 3** — the escalating cost is doing its job
as a self-limiter.

Wrestling gained sharply because it is the only grappling style with **no submission at all**
(Sumo Palm, Suplex, Choke Slam), so it is untouched by the new submission cost while Judo and
Jiu-Jitsu now pay an escalating price for their holds *and* Mount upkeep. If that swing is not
wanted, the Mount-upkeep interpretation above is the lever.

The striking mirror is unchanged (Boxer 91%, Muay Thai 50%, Karateka 9%) — no submissions occur
there, as expected.


---

# Follow-up — Wrestling ground game: Ground and Pound + Reversal (2026-08-15)

Two owner-authored Wrestling techniques. **Neither is in the Sheet's Positional Rules or
Martial & Weapon tabs yet** — they are marked as such in `POSITIONAL_RULES` so a future Sheet
sync does not silently drop them.

## Ground and Pound

| | |
|---|---|
| Power | 12 Physical |
| Stamina | 10 |
| Action slots | 2 |
| Secondary effects | **none** — no rider, no Guard Break, conditional or otherwise |
| Position | **Mounting only** (illegal Free, Grappling, Grappled and Mounted) |

## Reversal

| | |
|---|---|
| Power | 0 — deals no damage |
| Stamina | **30** (my pick; "mid-high" was left open — see below) |
| Action slots | 3 |
| Check | **DC 10 STR + AGI contest** |
| Position | **Mounted only** |
| Effect | Swaps the user from Mounted to Mounting; the opponent goes underneath |

**Stamina choice.** You specified "mid-high" without a number. Wrestling's existing costs run
8 (Sumo Palm), 15 (Single Leg Shot, Wrestler's Prowess), 50 (Suplex, Choke Slam). I used **30**:
above Hip Escape's 20 — the other bottom-position tool, which only drains the mounter — and
clearly below the 50-Stamina slams. Say the word if you want it elsewhere.

### Implementation note

Reversal needed no new effect semantics. A bottom fighter taking the top **is** the ordinary
mount transition with the roles swapped, so it resolves as a `GrappleTech` with `mount:true`
used from the Mounted position — `enterMount(user, opponent)`. That means it inherits the
approved rules for free:

- Forced entry **breaks the new bottom fighter's Poise** (section 15).
- `enterMount` clears both relationships first, so **any submission layered over the old
  position is broken** by the reversal.
- Submission Lock is not bypassed: that rule blocks *voluntarily dropping* Mount, whereas a
  reversal is an explicit contested relationship-changing effect, which section 14 lists as a
  legitimate way a relationship changes.

A `reversal` marker on the effect exists only so the log announces the flip once rather than
printing the generic "takes mount" line as well.

## Test results

```
$ cd web && node af-core.smoke.js     -> ok
$ cd web && node af-v3.4.smoke.js     -> ok
$ cd web && node build-standalone.js --artifact -> ok
```

New regression coverage:

- Ground and Pound: 12 power / 10 Stamina / 2 slots, **exactly one effect** (damage), no Guard
  Break, and legal in **Mounting only** across all five roles.
- Reversal: 0 power / 30 Stamina / 3 slots, DC 10, contest is STR+AGI (not the best-of pairing),
  puts the **user** on top, and is legal in **Mounted only** across all five roles.
- End to end: pinned under an opponent holding a Strangle, a reversal flips the roles, breaks
  the submission, breaks the new bottom fighter's Poise, deals no damage, announces itself, and
  opens up Ground and Pound from the position it just won.
- A Wrestler NPC reaches for Reversal when pinned and Ground and Pound when on top, and never
  queues Reversal while already on top.

### Grappling mirror — 120 battles

| Metric | Before | After |
|---|---:|---:|
| Wrestler | 90% | 90% |
| Judoka | 40% | 43% |
| Jiu-Jitsu Fighter | 20% | 18% |
| Avg rounds | 17.8 | 16.7 |
| Battles featuring Ground and Pound | — | **58 / 120** |
| Battles featuring a Reversal | — | **30 / 120** |

Zero crashes, zero stripped AI actions, zero unresolved. Both techniques see heavy use without
moving the mirror's standings — they add texture to the ground game rather than power.

### Browser verification

No console or page errors. As Mounting the card reads *"Ground and Pound · SingleEnemy ·
Physical · Power 12 · 2◆ 10 · Mounting only"*; as Mounted it reads *"Reversal · SingleEnemy ·
Transition to Mounting · 3◆ 30 · Mounted only"*. Each is hidden from the other position.


---

# Follow-up — submissions resist Reversal proportionally to their age (2026-08-15)

## Owner ruling

A submission should **lower the chance a Reversal works, proportionally to the number of turns
it has been active**. Escape early or lose the window.

Hip Escape is explicitly **out of scope**: it has no DC check, it is flat resource damage, and
it is untouched. (I briefly gated it too and backed that out — corrected below.)

## Rule

`BAL.submissionEscapeDcPerRound = 2`.

The relationship contest denies on `defence + d20 >= attack + dc`, so a **lower** DC is harder
for the escaper. Resistance is therefore **subtracted** from Reversal's authored DC 10:

| Turns the hold has been worked | Effective DC | Success at even stats |
|---:|---:|---:|
| none (bare Mount) | 10 | 48% |
| 1 | 8 | 37% |
| 2 | 6 | 27% |
| 3 | 4 | 16% |
| 4 | 2 | 5% |
| 5 | 0 | 0% |

Turns count from the round the hold is locked in, so a freshly established submission already
resists at −2.

**It is never absolutely impossible** — the contest is stat-based, so raw strength still breaks
out of a deeply worked hold. At 5 turns held: even stats 0%, but 18/18 STR+AGI succeeds 56% and
24/24 succeeds 100%. Escape resistance shifts the odds; it does not wall the position off.

Only the fighter **caught** in the hold is resisted. A holder working a submission from the
bottom is not escaping anything, so their own Reversal is unaffected.

A denied Reversal **still pays its 30 Stamina** — a failed escape attempt is spent.

## Generalisation

The rule is carried on positional metadata as `pos.escape`, not hardcoded to Reversal, so any
future contested escape inherits it by adding one flag. Uncontested abilities are never gated by
it — that is the distinction that keeps Hip Escape clean.

## Correction made during this pass

I first applied resistance to Hip Escape as well, inventing a contest for it (base DC 14, same
−2 ramp). That was wrong: Hip Escape as authored in section 16 has no check at all. The gate,
its constant `submissionEscapeBaseDc`, and its tests were removed. Hip Escape now provably
drains its full 15 Stamina even under a submission held 20 turns — its counterplay is the
pressure it puts on the mounter's upkeep, not a roll.

## Test results

```
$ cd web && node af-core.smoke.js     -> ok
$ cd web && node af-v3.4.smoke.js     -> ok
$ cd web && node build-standalone.js --artifact -> ok
```

New coverage:

- Reversal is flagged `pos.escape`; **Hip Escape is asserted NOT to be**.
- Resistance counts turns worked (1 on the establishing round), is proportional (`−2` per turn),
  and applies only to the fighter caught in the hold, never the holder.
- Measured over 240 runs per point: Reversal is strictly harder as the hold ages, an unresisted
  DC 10 lands roughly half the time, and three turns at least halves it.
- A denied Reversal still pays its Stamina, and the log names the reduced DC (`escape DC 10 →`).
- **Hip Escape drains its full 15 under a hold worked 20 turns** — no gate, no roll.
- A bare Mount with no submission resists nothing.

### AI

Escapes lose planner value as the hold tightens (`× max(0.2, 1 − 0.18 × turns)`), so a pinned
NPC stops burning its whole slate on a hopeless 3-slot Reversal. It still attempts one — that
remains its best out — it just no longer over-commits.

### Browser verification

No console or page errors. The relationship panel gains *"Locked in 3 turns — contested escapes
are at −6 DC and get harder every turn it holds"*, and the Reversal card's badge reads
*"Contested escape"* with no hold, then *"Escape DC −2 (held 1rd)"* → *"Escape DC −6 (held 3rd)"*.

### Grappling mirror — 120 battles

Wrestler 90%, Judoka 45%, Jiu-Jitsu 15%; average 16.1 rounds, longest 41. Zero crashes, zero
stripped AI actions, zero unresolved. 107 battles featured a submission, with **27 successful
reversals against 59 denied** — the resistance is visibly biting without removing the escape.
Submission chains still average 1.5 and cap at 3.
