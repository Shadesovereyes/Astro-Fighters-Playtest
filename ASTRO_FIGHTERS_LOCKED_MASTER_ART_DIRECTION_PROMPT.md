# Astro Fighters — LOCKED MASTER ART DIRECTION

**Status:** LOCKED  
**Role:** Visual canon and asset-art authority  
**Repository/runtime behavior:** `AGENTS.md`  
**Persistent negative corrections:** `production/NEGATIVE_PROMPT_REGISTER.md`  
**Current package contract:** `production/asset-manifest.json`  
**Acceptance:** `Astro Fighters — Art Preview Review Rubric.md` + `docs/data/art-review-rubric.json`

This file defines **what Astro Fighters must look like**. It intentionally does not duplicate repository workflow, branch state, score-processing logic, or completion tracking owned elsewhere.

---

# 1. Master visual directive

Create **production-quality pixel art** for Astro Fighters with the detail density, silhouette quality, material rendering, and authored pixel craftsmanship of the approved character reference sheets.

The world and characters must look as if they were produced by the same studio using one pixel vocabulary.

**The world rises to the character standard. The character standard is never lowered to excuse weaker scenery.**

Core identity:

- premium 90s-anime-inspired pixel craftsmanship;
- Edo-period Japanese daily-life foundation;
- martial culture;
- hip-hop/streetwear social texture;
- warm lived-in analog material language;
- Japandi restraint;
- inherited ancient civic infrastructure integrated into ordinary city life;
- dry matte surfaces and controlled local lighting;
- strong silhouettes and readable value grouping at gameplay scale.

Avoid generic fantasy, generic Japanese village styling, generic “Asian city” styling, RPG Maker language, smooth painted backgrounds, sterile sci-fi, cyberpunk, Victorian/steampunk spectacle, and low-detail scenery under premium sprites.

---

# 2. Generation vocabulary discipline

Certain generic words repeatedly cause off-canon drift and must not be used as generation anchors.

Do not use as generic prompt language:

- `neon`
- `wet street`, `wet asphalt`, `reflective pavement`
- `machine hall`, `engine room`
- `boiler`, `pistons`, `gears`, `clockwork`
- generic `machinery`
- generic `brass`
- generic `pipes`
- `steam` as the visual identity
- `furnace`
- generic `factory`
- `monumental city`
- generic `tower`, `spire`, `ziggurat`
- `pagoda`
- `temple gate`
- generic `Asian city`
- `cyberpunk`, `Blade Runner`
- magenta/cyan glow language

Functional requirements in a checklist do not override this rule. Translate the function into canon-specific language before prompting.

Character and population prompts must also apply the persistent negative constraints in `production/NEGATIVE_PROMPT_REGISTER.md`.

Preferred language:

- pale civic stone;
- slate;
- patinated copper;
- warm aged Edo timber;
- restrained clean-iron brackets;
- sealed/recessed service channels;
- integrated instrument alcoves or analog housings;
- dry matte paving;
- localized waterline darkening where physically appropriate;
- warm sodium amber and weak cathode green only for evening/night local lighting;
- horizontal inherited civic massing;
- named canonical apparatus rather than generic industrial spectacle.

---

# 3. Imperial City canon

Imperial City is a dense martial metropolis built through two visible eras.

## Inherited Great Shell layer

The older civic layer is cold, restrained, and integrated:

- pale civic stone;
- slate;
- patinated copper;
- sealed architectural technology;
- broad horizontal terraces and walls;
- recessed instrument alcoves behind glass where needed;
- very low generic vertical-object count;
- ancient infrastructure treated as architecture, not as exposed machinery.

The Great Shell should feel like a dam, cistern, substation, observatory, civic reservoir, or sealed infrastructure complex translated into this world's architecture—not a boiler room.

## Present inhabited layer

The current city is warmer and improvised:

- Edo timber construction;
- aged plaster;
- cloth, rope, paper, repaired surfaces;
- rust and patina as restrained accents;
- visible lashings, plates, repair seams, and adaptive construction;
- small human-scale commerce and domestic occupation;
- hip-hop social identity layered naturally into clothing, music, banners, crew markings, and street life.

Present-day industrialization follows **Meiji Japanese logic**, not Victorian Europe. Rail language may include Japanese timber-and-iron station forms, interurban electric rail, catenary, simple platform sheds, cargo carts, and practical infrastructure without steampunk ornament.

## Locked city orientation

- Palace / Crown authority is north.
- Port / harbor opens south.
- East, west, and north gates connect outward.
- Major district families include Crown, Merchant/Market, Grand Canal, Observatory, Port, Old Shellworks, residential/canal areas, Academy, civic spaces, and rougher fringe/outer zones.
- The Grand Canal is a hydraulic/civic spine.

---

# 4. Architectural language

Use Edo timber architecture as the inhabited baseline:

- irimoya / kirizuma roof logic where applicable;
- single-storey and modest multi-storey eaves;
- machiya/storefront logic;
- shoji/paper-panel systems;
- engawa/veranda conditions;
- noren and wooden signboards;
- vertical Japanese signage language;
- practical timber framing and stone foundations.

Avoid Chinese architectural drift. Do not default to paifang, Chinese palace roofs, hanzi-dominant signage, generic “temple gate” silhouettes, or pagoda composition.

Where a torii-like or ceremonial element is appropriate, it must be specific to the scene and canon rather than used as a generic Japanese shorthand.

Architecture should preserve **Japandi restraint**:

- one hero relationship per composition;
- broad calm wall/ground planes;
- negative space;
- restrained prop density;
- open sky or quiet planes where appropriate;
- ornament concentrated where it has social or functional meaning.

---

# 5. Projection, scale, grid, and depth

Use the locked **flat-faced 3/4 cabinet projection**.

Depth comes from:

- overlap;
- top/front-face separation;
- Y/depth sorting;
- contact/cast shadows;
- architecture height;
- foreground occluders;
- authored cutaways;
- scale relationships.

Do not use dramatic photographic vanishing-point convergence or isometric diamond projection.

The game may use a hidden **32×32 logical grid**, but the ordinary world must read as continuous natural space.

Do not expose the grid through:

- paving seams;
- floorboards;
- wall segmentation;
- checkerboarding;
- prop spacing;
- decals;
- repeated 32-pixel cadence;
- persistent overlay lines.

Temporary combat telegraphs may reveal spatial quantization only when mechanically necessary.

---

# 6. Modular world construction

Production gameplay art must support the layered Phaser world described in `AGENTS.md`.

Typical layer roles:

- ground;
- decals / wear;
- architecture;
- architecture dressing;
- props-back;
- interactives;
- actors;
- props-front / occluders;
- local shadows;
- restrained atmosphere/FX.

World art must be authored as reusable game assets, not as a smooth flattened painting.

A reference image may define target quality, composition, material, or silhouette, but it may not be cropped into final modules and called production-ready without independent clean authoring and QA.

---

# 7. Material language

Materials must be visually distinguishable through pixel-cluster behavior, edges, highlight/shadow response, wear pattern, texture frequency, and palette—not merely different colors.

Primary families:

- pale/warm civic stone;
- aged stone foundations;
- pristine and weathered timber;
- warm plaster;
- slate and roof tile;
- paper;
- rope;
- cloth;
- clean iron;
- rusted metal;
- patinated copper;
- soot/grime;
- water;
- damp masonry only in localized physically plausible conditions;
- moss and foliage.

Harbor surfaces may show waterline darkening, salt wear, algae, or localized dampness, but ordinary paving remains matte and non-mirrored. Do not use glossy rain-slick streets as an attractiveness shortcut.

---

# 8. Lighting

Default exterior key direction: **upper-left / northwest**.

General behavior:

- upper-left highlight;
- local-color midtone;
- lower-right shadow;
- darkest values in cavities and contact edges;
- restrained local shadows rather than broad cinematic grading.

Daylight / neutral warm daytime is the default production benchmark.

For evening/night:

- low-saturation warm sodium amber;
- weak cathode green only where functionally justified;
- local pools of light on timber/stone;
- dry matte paving;
- no mirrored reflections;
- no magenta/cyan or cyberpunk glow language.

---

# 9. Population and clothing identity

The city population should predominantly use brown-skin hues, with broad variation rather than one repeated tone.

## Character proportion standard

Adult and young-adult fighters must use **grounded anime/action-RPG proportions**, not chibi or super-deformed proportions.

Reject:

- chibi / super-deformed / SD bodies;
- mascot-like miniature proportions;
- oversized heads relative to the torso and legs;
- bobble-head silhouettes;
- compressed torsos;
- shortened legs used to create a cute or toy-like read;
- childlike proportions on adult characters;
- presentation or mockup characters that distort the canonical paper-doll silhouette merely for readability.

Require:

- a smaller head relative to the full body than chibi/SD art;
- natural torso length;
- longer, anatomically believable legs;
- grounded young-adult/adult fighter silhouettes;
- consistent proportion language across all eight directions;
- preservation of the canonical paper-doll silhouette through runtime reduction.

This rule applies to production characters, NPCs, source masters, runtime sprites, concept/reference sheets, presentation images, and gameplay-reference mockups. A board or environment study does not get an exemption to use a chibi proxy.

A specifically authored child character may use age-appropriate proportions, but only when that character is intentionally a child.

Character clothing fuses:

- open haori/happi logic;
- hoodies/tracksuit/streetwear attitude where compatible;
- obi/sashes over practical trousers;
- kimono sleeve volume where appropriate;
- mixed sneaker-hybrid martial footwear with some geta/waraji influence;
- sagemono/pouches/cords;
- jewelry and role accessories;
- embroidered or painted mon/crew identifiers.

Do not default to European period dress, generic medieval fantasy, Harajuku caricature, or cyberpunk techwear.

Crew/faction colorways should remain differentiated and restrained. Avoid allowing one accent family—especially purple—to dominate the population or scene.

---

# 10. Character source authority

Current canonical character contract is defined in `production/asset-manifest.json`.

Locked baseline:

- directions: `N, NE, E, SE, S, SW, W, NW`;
- `S` = front/toward camera;
- `N` = back/away from camera;
- source canvas: `480×640` per direction;
- source body center: `[240,600]`;
- source foot-contact line: `y=600`;
- runtime frame: `48×64`;
- runtime pivot: `[24,60]`;
- idle: 4 frames/direction;
- walk: 6 frames/direction;
- ready: 2 frames/direction.

The interchangeable base is never nude:

- male base = body/skin + hair/face + base shorts;
- female base = body/skin + hair/face + base shorts + sports bra.

Other clothing/equipment remains modular unless a locked design explicitly says otherwise.

---

# 11. Eight-direction anatomy and routing

Every visible character module must obey the full direction:

- `N` back;
- `NE` back-right 3/4;
- `E` right profile;
- `SE` front-right 3/4;
- `S` front;
- `SW` front-left 3/4;
- `W` left profile;
- `NW` back-left 3/4.

Direction affects the complete silhouette: head, neck, shoulders, torso, hips, arms, hands, legs, feet, hair, clothing, sash, accessories, shadow, weapon/scabbard, and overlap order.

A front-facing body with only facial pixels or accessory placement changed is invalid.

Equipment follows the character's **anatomical side**, not screen-left/screen-right. Direction-specific front/back/near/far routing must preserve believable body relationships.

Mirroring may be used diagnostically or as an early candidate only where symmetry is truly valid; do not treat mirrored directional art as independently authored final work when garment/anatomy routing differs.

---

# 12. Character fashion families

Appropriate playable-fighter families include:

## Inner tops

- wrapped martial top;
- sleeveless fighter wrap;
- cropped fitted underlayer;
- hooded underlayer;
- banded chest-wrap top.

## Outerwear

- patterned haori;
- short utility jacket;
- split-tail street haori;
- sleeveless battle coat;
- scarf-collar fighter jacket.

## Pants

- loose fighter trousers;
- cuffed worker trousers;
- hakama-influenced combat pants;
- wrapped-shin trousers;
- reinforced street-martial slacks.

## Footwear

- wrapped boots;
- tabi-boot hybrid;
- sandal-boot hybrid;
- sneaker-hybrid martial shoes.

## Waist/accessories

- rope/cloth sash;
- obi-derived waist treatment;
- charm-cord belt;
- pouches;
- wrist wraps;
- neck cord;
- bead ties;
- shoulder cloth ties;
- talisman strips;
- scabbard cords where relevant.

Priority Afro-descended hairstyles include short Afro, high puff, short freeform locs, braided twists, and puff undercut.

---

# 13. Occlusion and interiors

Environment height classes:

- **Low:** may cover feet/lower legs; normally remains visible.
- **Mid:** may cover meaningful body area but should not permanently erase the controlled silhouette.
- **Tall:** buildings, roofs, large trees, gantries, elevated infrastructure; must support authored cutaway/fade/visibility behavior.

Never fade the player as the primary solution.

Interior visibility is room/region-based:

- roof disappears by authored architectural region;
- back/north wall may remain full height;
- side walls taper or cut away where appropriate;
- front/south wall becomes a low cutaway;
- no per-cell visibility reveal.

The player should perceive **the room becoming visible**, not tiles being uncovered.

---

# 14. District identity

Districts share one city-wide art language but require their own authored spatial/material/social identity.

- **Harbor / Docks:** quay, piers, cargo, nets, boats, shipwright frontage, rope systems, waterline wear, restrained loading infrastructure.
- **Market / Shops:** machiya/storefront logic, signs, awnings, stalls, merchandise, narrow passages, commercial clutter.
- **Residential / Canal:** dense homes, laundry, plants, household storage, small bridges, canal edges, neighborhood life.
- **Academy:** gates, dojo construction, training yards, practice equipment, banners/insignia, students/instructors, furnished cutaway rooms.
- **Workshops:** benches, hand tools, material racks, repair stock, sealed service housings, practical vents, labor clutter.
- **Civic / Administrative:** formal offices, controlled public space, official signage, guards, records, restrained high-status materials.
- **Palace / Crown:** larger scale, refined stone, ceremonial order, banners, controlled symmetry, guard infrastructure.
- **Observatory / inherited infrastructure:** sealed civic apparatus, restrained instrumentation, stone/copper/slate language.
- **Fringe / outer ward:** patched paving, repaired timber, improvised commerce, salvaged materials, clan/crew influence, worn but still premium craftsmanship.

Do not differentiate districts only by swapping props on the same generic building shell.

---

# 15. Composition restraint

For key gameplay/reference images:

- use one clear hero relationship;
- preserve large quiet wall/ground/sky planes;
- avoid decorative clutter for its own sake;
- keep enough negative space to read character silhouettes;
- use props to imply occupation and daily life rather than fill every cell;
- avoid giant astrolabes, giant decorative apparatus, or generic skyline spectacle as automatic focal points.

When a single composition is intended as an Imperial City key illustration, open sky/plain wall/bare ground may occupy roughly 40% of the frame when useful to maintain restraint.

---

# 16. Production-art acceptance

The production pipeline itself is governed by `AGENTS.md`; the visual rule is simple:

> **reference target → purpose-built modular source art → clean source assembly → target-resolution cleanup → actual Phaser integration → rubric review**

Never use:

> **pretty generated image → crop/shrink → call it finished game art**

A mechanically reduced image is not pixel-final simply because it loads.

A checklist item is not complete merely because a source PNG exists or a mockup looks good. Integrated Phaser gameplay must pass the locked rubric.

---

# 17. Final acceptance question

Before approving any scene or asset family, ask:

> **Does this look like premium Astro Fighters character art inhabiting a premium Astro Fighters world, or like premium character art placed inside a cheaper/generic environment?**

If the second interpretation is reasonably possible, development continues.
