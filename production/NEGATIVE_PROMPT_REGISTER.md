# Astro Fighters — Negative Prompt Register

**Role:** Persistent correction register for visual generation and asset authoring  
**Authority:** Read with `AGENTS.md` and `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`  
**Rule:** An explicit user correction to generated art, asset style, proportions, materials, composition, or presentation must be recorded here before further related generation so the same failure is not repeated.

This file stores **negative constraints learned from review**. It does not replace positive canon in the Master Art Direction. Each entry should describe the rejected drift and the preferred correction in concrete visual terms.

---

## Character proportions

### NP-CHAR-001 — No chibi / super-deformed player proportions

**Correction source:** User rejected the chibi-looking player used in Slice 0 presentation imagery.

**Do not generate or approve:**

- chibi proportions;
- super-deformed / SD proportions;
- mascot-like miniature bodies;
- oversized heads relative to torso and legs;
- bobble-head silhouettes;
- compressed torso length;
- shortened legs used to make the character read cute or toy-like;
- childlike body proportions unless a specifically authored child character requires them;
- runtime mockups that enlarge the head to preserve readability at the expense of the canonical paper-doll silhouette.

**Required correction:**

- grounded anime/action-RPG body proportions;
- young-adult/adult proportions for adult fighters;
- smaller head relative to the full body than chibi/SD art;
- natural torso length;
- longer, anatomically believable legs;
- readable but non-caricatured hands/feet and limb mass;
- preserve the established paper-doll silhouette and anchor/foot-contact contract when reducing to runtime scale;
- maintain the same non-chibi proportion language across all eight facings.

**Applies to:**

- playable characters;
- NPCs;
- source masters;
- runtime sprites;
- concept/reference sheets;
- presentation images;
- Phaser capture mockups/reference imagery.

A presentation board may not use a chibi proxy merely because the environment is the nominal subject; character depictions shown alongside production art must still respect the canonical proportion language.

---

## Existing global negative vocabulary

The following established drift magnets remain prohibited as generic prompt anchors and are also documented in the Master Art Direction / `AGENTS.md`:

- neon;
- wet street / wet asphalt / mirrored reflective pavement;
- machine hall / engine room;
- boiler / pistons / gears / clockwork;
- generic machinery;
- generic brass;
- generic pipes;
- steam as a hero aesthetic;
- furnace;
- generic factory;
- monumental city;
- generic tower / spire / ziggurat;
- pagoda;
- temple gate;
- generic Asian city;
- cyberpunk / Blade Runner;
- magenta/cyan glow language.

---

## Maintenance rule

When the user gives a new visual correction:

1. identify the failure mode precisely;
2. add a new `NP-*` entry in the relevant section of this file;
3. add or update the corresponding positive/negative canon in the most relevant authority file when the correction changes a lasting art rule;
4. do not remove earlier corrections unless the user explicitly reverses or supersedes them;
5. do not mark the correction as satisfied merely because a later presentation image looks better—production assets still pass the normal source → runtime → Phaser → rubric pipeline.
