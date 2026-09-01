# Astro Fighters — Modular Source Layer Integrity Rules

**Status:** LOCKED production rule  
**Scope:** all character paper-doll layers, clothing, hair, equipment, accessories, modular props, and any production source asset intended to exist independently beneath another layer.  
**Purpose:** prevent clipped visibility slices, occlusion-boundary cutoffs, contaminated isolates, false-positive source approvals, and accidental promotion of reference illustrations into modular game assets.

---

# 0. Reference Material vs Production Modular Assets

Polished illustration, cel-shaded art, painted turnarounds, concept boards, anatomy studies, garment studies, and equipment studies may be used as **REFERENCE ONLY** or **REFERENCE PASS** material.

Those images may define:

- character identity;
- anatomy/proportions;
- garment construction;
- hidden-underlayer intent;
- near/far routing;
- equipment mounting;
- silhouette and facing;
- material and color relationships.

They do **not** become production modular assets merely because they are cropped, segmented, placed on transparency, or arranged like sprite-sheet components.

Once a layer is identified as `SOURCE CANDIDATE`, `PIXEL SOURCE`, `SOURCE PASS`, `RUNTIME`, `IN-GAME`, or a Phaser-loaded asset, it must satisfy this integrity standard **and** `ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md`.

> **REFERENCE ART MAY EXPLAIN THE OBJECT. PRODUCTION SOURCE ART MUST ACTUALLY AUTHOR THE OBJECT.**

---

# 1. Governing Rule — Visibility Is Not Geometry

A production source layer must represent the **complete reusable component**, not merely the pixels visible in the fully dressed reference image.

**Occlusion boundaries are not clipping boundaries.**

If a sash, sleeve, weapon, hand, outer garment, hair mass, accessory, or other upper layer covers part of a lower component, the lower component must continue naturally underneath the occluder wherever its real construction would continue.

Examples:

- pants continue underneath a sash, belt, front cloth panel, hanging cord, weapon, and coat overlap;
- an inner top continues underneath outerwear and crossed front panels;
- a haori panel continues underneath a near sleeve, sash, hand, or weapon where the garment physically continues;
- a sleeve continues underneath a hand/cuff overlap up to its real cuff/opening edge;
- a scabbard or strap continues underneath the hand, sash, torso, or coat according to the approved mount geometry;
- hair back-mass continues underneath the head/neck/front-hair layers where appropriate.

A source layer that ends exactly where another layer begins is invalid unless that edge is a **real authored physical edge** such as a hem, cuff opening, collar opening, seam boundary, cut end, object tip, or intentionally separate component boundary.

---

# 2. Visibility-Slice Prohibition

The following are **automatic production source-stage failures**:

- extracting only the currently visible pixels of a garment or body part from a dressed composite;
- treating a segmentation mask of visible pixels as the finished modular source layer;
- pants that are chopped off at the sash or front cloth panel;
- sleeves chopped at a hand/arm overlap rather than continuing to the actual cuff opening;
- haori front/near/far pieces that exist as disconnected fragments because hidden portions were never authored;
- weapon, scabbard, cord, strap, or charm layers that stop at an overlap instead of continuing behind it;
- hard straight or jagged alpha cuts that correspond to another layer's silhouette rather than the component's own physical edge;
- sparse fragments that reconstruct the dressed composite but do not form a coherent standalone component;
- using generated presentation-board panels, checkerboard previews, labels, or pseudo-PNG tiles as if they were actual isolated production source files;
- cutting a polished illustrative reference into transparent pieces and promoting those pieces directly to game-source status.

**Pixel-exact reconstruction of the dressed composite does not override any of these failures.**

A polished reference image may still be valid as `REFERENCE ONLY`; the failure occurs when its visible fragments are misidentified as production modular source.

---

# 3. Reconstruction Is Necessary but Not Sufficient

A modular production source set must pass three independent requirements:

1. **Composite fidelity** — the assembled stack matches the approved dressed reference for the facing.
2. **Component integrity** — every layer is a coherent, continuous, independently usable source component with correct hidden continuation.
3. **Pixel-source integrity** — every production layer satisfies `ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md` rather than remaining painterly/reference rendering.

A set may reconstruct the reference with `0` changed pixels and still **FAIL** if the individual layers are clipped visibility slices or if those layers are not true pixel art.

Machine reconstruction tests therefore may report only **COMPOSITE PASS**. They may not mark the direction or package **SOURCE PASS** until manual component-integrity review and pixel-source review also pass.

Generated text, green checkmarks, status badges, filenames, dimensions, palette labels, or QA claims embedded inside an image are presentation pixels only and are never accepted as validation evidence.

---

# 4. Mandatory Occluder-Toggle Test

Before a character direction or modular production source package can pass, review the assembled source by hiding upper layers one at a time.

For every meaningful overlap:

1. assemble the approved normal stack;
2. disable the occluding layer;
3. inspect the newly revealed lower component;
4. confirm that the lower component continues with plausible anatomy/material construction;
5. confirm there is no hole, amputated shape, copied occluder edge, abrupt vertical/horizontal cutoff, or disconnected fragment;
6. confirm the revealed pixels still satisfy the pixel-art source standard rather than being soft/painted filler;
7. restore the occluder and repeat for the next overlap.

At minimum, character source QA must toggle-test:

- sash / belt over pants and inner top;
- weapon / scabbard over sash, pants, torso, and outerwear;
- near/far haori panels against torso, sash, pants, sleeves, and hands;
- sleeves against hands/cuffs;
- hair front against hair back/head;
- accessories against the garment or body that supports them.

If removing an upper layer exposes obviously unfinished pixels, non-pixel filler, or a copied occlusion boundary, the lower layer is not production-ready.

---

# 5. Hidden-Underlayer Completion Rule

Hidden-source pixels may legitimately exist even though they are absent from the final dressed composite.

They must satisfy all of the following:

- they occupy a plausible continuation of the component;
- they remain on the shared source lattice and anatomical anchors;
- they are hidden by the intended higher layer in the approved normal stack;
- they do not create visible silhouette contamination when the normal stack is assembled;
- they use the correct palette/material treatment;
- they are authored from the component's construction, not filled procedurally merely to satisfy a pixel count;
- their edges are component edges, not copies of an occluder's alpha boundary;
- when the asset is production source, the hidden pixels are deliberately authored pixel art, not smooth illustrative fill borrowed from a reference image.

Automatic flood fills, broad color segmentation, alpha expansion, distance transforms, or similar image-analysis operations may help diagnose where hidden continuation is needed, but **may not be the authority for final hidden-source geometry or final production pixels**.

A polished reference illustration may be used to infer how the hidden area should be constructed. The final production layer must still be independently authored as pixel art.

---

# 6. Character Near/Far Layer Standard

For direction-aware clothing such as Kairo's haori, near/far decomposition must create **continuous garment pieces**, not separate islands of visible pixels.

For each facing:

- `haori_back` contains the coherent behind-body/back-mass portion;
- `haori_far_sleeve` contains the full far sleeve up to real attachment/opening boundaries;
- `haori_front_far` contains a coherent far/front panel where applicable;
- `haori_near_sleeve` contains the full near sleeve up to real attachment/opening boundaries;
- `haori_front_near` contains a coherent near/front panel where applicable.

A layer may be intentionally empty for a facing, but a non-empty layer may not be a collection of arbitrary visibility scraps.

The same continuity standard applies to body near/far hands, sash front/back/ties, equipment front/back, hair front/back, and comparable modular systems.

Reference studies may show a complete garment in polished illustration form; production decomposition uses that construction information but must create coherent pixel-authored pieces on the shared lattice.

---

# 7. Mandatory Individual-Layer Review

Every production source layer must be reviewed **alone** before source approval.

Required review surfaces:

- transparent/checkerboard individual layer at useful scale;
- full alpha extent visible with safety padding;
- shared-lattice inset or anchor overlay when placement matters;
- grouped review of related pieces such as all haori parts or all equipment parts;
- normal assembled composite;
- 100%/zoomed pixel inspection sufficient to distinguish deliberate clusters from soft illustrative rendering.

The individual-layer view must make clipping and non-pixel rendering easy to see. Do not hide a weak isolate by showing only the final composite.

---

# 8. Contact-Sheet Rule

QA/contact sheets are diagnostic documents, not art sources.

Every production-source contact sheet must:

- auto-fit each layer's **entire nontransparent alpha bounding box**;
- add visible padding around that bounding box;
- never crop, zoom through, or cut off any nontransparent source pixel;
- preserve aspect ratio;
- show enough checkerboard/background contrast to inspect alpha edges;
- place labels outside the asset image area;
- include a full-lattice inset when registration matters;
- avoid decorative presentation that makes source defects harder to inspect;
- display the actual production pixel layer, not an illustrative stand-in.

A contact sheet that clips a component or substitutes a polished reference image for the actual production layer is itself a QA failure and must be regenerated before review continues.

---

# 9. Source-Pass Gate

A direction/package may be marked **SOURCE PASS** only when all of the following are true:

- correct direction identity and shared registration;
- clean individual source files;
- no neighboring-source, label, border, matte, checkerboard, or presentation contamination;
- no clipped visibility slices;
- continuous hidden underlayers beneath all meaningful occluders;
- real physical edges distinguishable from occlusion edges;
- near/far pieces form coherent component shapes;
- hands/cuffs and body/garment boundaries remain independently swappable;
- anatomical equipment mount and front/back routing are correct;
- occluder-toggle test passes;
- individual-layer manual review passes;
- `PIXEL SOURCE PASS` under `ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md` passes;
- normal assembled composite matches the approved reference;
- no visible silhouette contamination in the normal stack.

**Machine reconstruction PASS + manual component-integrity FAIL = SOURCE FAIL.**  
**Component integrity PASS + pixel-source FAIL = SOURCE FAIL.**  
**Reference PASS alone never equals SOURCE PASS.**

Do not start the next direction, runtime reduction, animation derivation, or Phaser promotion while this gate is failing.

---

# 10. Review Vocabulary

Use these status terms precisely:

- **REFERENCE ONLY** — exploratory/reference material; may be polished illustration; cannot be treated as a game asset.
- **REFERENCE PASS** — visual/design target approved; may still be illustrative and non-production.
- **COMPOSITE PASS** — assembled production pixels match the approved dressed target; does not imply source layers are clean.
- **COMPONENT INTEGRITY PASS** — standalone layer geometry and hidden continuations pass manual review.
- **PIXEL SOURCE PASS** — production source rendering satisfies the locked pixel-art standard.
- **SOURCE PASS** — composite fidelity + component integrity + pixel-source integrity + registration/contamination checks all pass.
- **RUNTIME PASS** — target-resolution asset has completed manual pixel cleanup and runtime validation.

Never shorten **COMPOSITE PASS**, **REFERENCE PASS**, or **COMPONENT INTEGRITY PASS** to simply **PASS** when the remaining source gates have not been reviewed.

---

# 11. Kairo Package 07 Immediate Application

For the current Kairo source workflow:

- polished/cel-shaded Kairo sheets may remain approved as **REFERENCE ONLY / REFERENCE PASS** material where they correctly establish identity, garment construction, facing, and equipment placement;
- those references are not production sprites and must not be promoted by cropping/shrinking/quantizing them;
- `S` and every subsequent production direction must be judged under this rule and the Pixel-Art Source Standard;
- `SE` is **not approved** while its near/far haori, hands/cuffs, pants/waist, or equipment pieces remain clipped visibility slices or non-pixel source rendering;
- `E` remains blocked until SE earns **SOURCE PASS**, not merely reference approval, component integrity, or pixel-exact composite reconstruction;
- after SE passes, continue one direction at a time: `E → NE → N → NW → W → SW`;
- do not return to simultaneous eight-direction generation as a substitute for finishing the active production direction.

---

## Locked summary

> **REFERENCE ART MAY BE ILLUSTRATIVE. GAME ASSETS MAY NOT.**  
> **AUTHOR THE OBJECT, NOT THE VISIBLE FRAGMENT.**  
> **AN OCCLUDER MAY HIDE SOURCE PIXELS; IT MAY NOT DEFINE WHERE THE HIDDEN OBJECT ENDS.**  
> **EXACT COMPOSITE RECONSTRUCTION IS NOT SOURCE APPROVAL.**  
> **SOURCE PASS REQUIRES BOTH COMPLETE COMPONENT GEOMETRY AND TRUE PIXEL-ART PRODUCTION PIXELS.**
