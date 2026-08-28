# Astro Fighters — Phaser World Refactor v0

**Status:** Required before Imperial City Slice 0 can be called integrated  
**Target:** Open-world, real-time action-combat RPG  
**Engine:** Phaser runtime under `/docs`

## Why this refactor exists

The current browser prototype genuinely runs Phaser, but its `WorldScene` still carries vertical-slice shortcuts that are not acceptable as the production world architecture:

- each district is loaded as one full-frame environment image;
- the player/paper-doll is layered over that baked image;
- a visible 32×32 route/grid overlay is drawn with Phaser Graphics;
- exploration movement advances through integer grid positions on a fixed step timer;
- collision is represented primarily as grid rectangles rather than authored world collision bodies;
- this makes environment work tend toward flattened illustration/collage composition instead of a layered game world.

These shortcuts were useful for proving systems. They are not the target presentation or movement model for the open-world action RPG.

---

# Locked correction

Imperial City production must remain in Phaser, but world construction changes from **baked map image + grid-step actor** to **modular Phaser scene + continuous real-time actor**.

A presentation board, concept painting, source-art collage, or Python/PIL composite may be used to judge art direction, but it may never be treated as an integrated gameplay review.

**The integrated art gate is valid only when the scene is rendered by Phaser from separate runtime assets.**

---

# 1. Runtime world layers

The production scene must create separate Phaser objects/containers corresponding to the locked world layer order:

1. `ground`
2. `decals`
3. `architecture`
4. `architecture-dressing`
5. `props-back`
6. `collision`
7. `interactives`
8. `actors`
9. `props-front-occluders`
10. `local-shadows`
11. `atmosphere-fx`

No single full-screen illustration may substitute for these layers.

A flattened environment image may exist only as a concept/reference image or a temporary non-reviewable development backdrop.

---

# 2. Pixel rendering contract

Retain the existing Phaser pixel-rendering configuration:

- `pixelArt: true`
- `antialias: false`
- `roundPixels: true`
- integer camera/display scaling wherever possible
- no smoothing or photographic interpolation
- consistent runtime pixel density across player, NPCs, architecture, props, and ground

Production reviews must reject mixed-resolution collage appearance even when all files are technically PNGs.

---

# 3. Hidden-grid rule

The 32×32 logical movement/combat grid may remain available for systems that need spatial quantization, authored placement, AI reasoning, or combat telegraphs.

It must not be drawn as a persistent world overlay.

Remove the current route/grid graphics from presentation gameplay.

Allowed visible grid information is limited to intentional temporary mechanical telegraphs where the game design explicitly requires it.

---

# 4. Real-time exploration movement

The production player controller must not move by one integer tile every fixed `STEP_MS` interval.

Replace exploration stepping with continuous real-time movement:

- input vector from WASD/arrows/controller;
- normalize diagonals so eight-way movement does not gain speed;
- velocity expressed in pixels/second;
- delta-time movement/update;
- eight-direction facing selected from the movement vector;
- idle/walk/ready animation driven from real movement state;
- authored collision resolution against world bodies;
- movement remains smooth while sprite rendering remains pixel-snapped where appropriate.

The hidden 32×32 grid may still be sampled internally for AI, navigation sectors, encounter logic, abilities, or interaction indexing, but it must not control the visible cadence of ordinary exploration.

---

# 5. Collision

World collision must become independent from the appearance of the ground image.

Use authored collision data for:

- wall foundations;
- building footprints;
- posts/solid props where appropriate;
- railings;
- quay edges;
- water boundaries;
- stairs/threshold constraints where needed;
- bridges;
- doors/gates;
- combat blockers.

Collision geometry may align to the hidden grid where useful but should follow believable architecture rather than exposing a chessboard rhythm.

---

# 6. Depth and occlusion

Characters must be able to move in front of and behind appropriate scene elements.

Use Phaser depth ordering / containers / authored sort metadata for:

- walls and roof/cutaway components;
- posts and beams;
- market awnings;
- trees/shrubs;
- railings;
- signs/lanterns;
- foreground fences;
- other tall props.

Foreground occluders must be separate assets. Do not bake them into the ground or background image.

Interior cutaway behavior must operate on authored room/architecture groups, not per-cell fog or visibility reveals.

---

# 7. Slice 0 engine test

Before Harbor production, build **Foundation Courtyard Slice 0** inside Phaser from separate files.

Minimum Phaser objects/textures:

- Imperial stone ground module(s);
- crack/stain/cart-wear decals;
- aged stone foundation;
- timber/plaster wall;
- timber post;
- horizontal beam;
- building threshold;
- drainage channel/grate;
- blank sign and/or lantern/noren dressing;
- one foreground occluder;
- fully dressed eight-direction player paper doll.

The scene must allow the player to walk around the courtyard and visibly pass behind at least one foreground/architectural element.

---

# 8. Valid integrated preview

A valid Slice 0 preview must be captured from the actual Phaser game canvas while the scene is running.

It must not be:

- a Photoshop/PIL composite;
- a presentation board;
- an image-generation montage;
- a flattened concept scene presented as runtime;
- a screenshot of assets arranged on a contact sheet.

Every visual element claimed as a gameplay asset must be loaded and positioned by Phaser.

The preview should demonstrate:

- gameplay camera framing;
- actual player runtime scale;
- actual nearest-neighbor/pixel rendering;
- live depth ordering;
- hidden grid;
- collision/traversal space;
- coherent pixel density;
- character/world homogeneity.

Only this preview may be scored as an integrated gameplay candidate.

---

# 9. Treatment of the prior Slice 0 collage/source-candidate work

The generated production boards remain useful as **composition and material references only**.

Any assets extracted or cropped from those boards are **not production masters** and must not be promoted merely because they were separated into PNG files or resized to a contracted canvas.

They may be used for:

- composition reference;
- silhouette reference;
- material/color reference;
- asset-list discovery;
- temporary non-reviewable engine scaffolding.

They may not be marked `source-approved`, `runtime-candidate`, `integrated`, or `approved` without independent production-quality authoring/cleanup and the normal gates.

---

# 10. Completion gate for this refactor

The Phaser world refactor is sufficiently proven for continued city production when:

- [ ] the visible debug grid is absent from normal gameplay;
- [ ] exploration movement is continuous real-time rather than tile-step cadence;
- [ ] Slice 0 loads multiple separate environment textures rather than one baked background;
- [ ] collision exists separately from artwork;
- [ ] one foreground/architectural occlusion case works live;
- [ ] the paper-doll player remains eight-directional;
- [ ] pixel-art renderer settings remain enabled;
- [ ] an actual Phaser-canvas screenshot is used for the integrated art review;
- [ ] no collage/full-frame background is being treated as a production world asset.

This refactor changes the world/runtime presentation layer. It does not discard valid combat, character, inventory, astrology, dialogue, progression, or tutorial systems already proven by the browser vertical slice.