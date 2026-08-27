# Kairo — Package 07 v41–v43 Registration QA

## Why this pass exists

The previous source work established clean garment isolation and direction-aware layer routing, but the actual garment scale and placement still relied too heavily on broad manual percentages. That made it difficult to tell whether a new iteration was genuinely closer to the approved Kairo turnaround.

v41–v43 change the review method so candidate and benchmark are measured on the same `480×640` body lattice and displayed at the same body scale.

## v41 — benchmark-envelope registration

v41 measures garment-specific target envelopes directly from the approved dressed Kairo turnaround and fits the contamination-free source isolates into those envelopes.

Measured families:

- wrapped inner top
- short street-haori
- baggy trousers
- wrapped footwear
- sash cloth reference

This pass is useful as a measurement scaffold, not production approval.

## v42 — open-haori correction

v41 exposed a source problem that was obscuring the torso: the standalone front/three-quarter haori reference contains dark presentation/mannequin fill inside the garment opening.

v42 removes the large central low-chroma presentation-fill components from the open-front directions while retaining the actual fabric, trim, sleeve and outline pixels.

Result: the inner top/body is visible through the haori opening instead of being covered by an opaque dark panel.

## v43 — silhouette tuning

v43 keeps the corrected open haori and adjusts family-specific silhouette scale after comparing candidate and benchmark at identical body scale.

Current corrections include:

- wider outer-haori envelope so sleeves reach the intended shoulder/arm silhouette;
- reduced trouser volume;
- reduced footwear scale;
- reduced waist/sash bulk;
- narrower late body routing so only head and actual hand/wrist tips repaint over clothing.

## What v43 proves

The source pipeline can now make measurable corrections against the dressed benchmark without returning to opaque whole-garment overlays.

The comparison surface deliberately crops candidate and benchmark using the **same base-body window**. Weapon length no longer changes the review zoom, so clothing proportions can be judged directly.

## Remaining source defects

v43 is **not production-approved**.

Visible work still required:

- N/NE/E/W haori sleeve-to-hand seams need manual pixel cleanup;
- front/three-quarter haori width still needs per-facing rather than family-wide tuning;
- trousers and footwear need final per-facing rise/contact adjustments;
- the sash source remains a reference because pouch/gourd/charm must remain separate modules;
- rear-view waist routing still needs refinement;
- equipment must be manually registered after the clothing silhouette is locked;
- four NW equipment source directions still need independent authoring;
- hairless scalp source remains below final art quality.

## Runtime gate

No `48×64` runtime derivation is approved by this pass.

The sequence remains:

`CLEAN SOURCE → BODY-SCALE BENCHMARK REVIEW → PER-FACING PIXEL POLISH → FULL SOURCE APPROVAL → 48×64 DERIVATION → PHASER`
