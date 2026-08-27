# Kairo — Package 07 v37/v40 QA

## v37 — precise hand / sleeve routing

The v36 clean-chest integration still used a late body mask that was too broad around the arms. That caused the body to reappear over too much of the haori sleeve in several facings.

v37 narrows the late-visible body regions to:

- head / hair;
- wrist / hand zones only.

Upper forearms remain below the haori unless the approved dressed benchmark for that facing specifically requires otherwise.

This is a structural correction to the paper-doll draw order. It directly addresses the earlier problem where some clothing views looked like a broad overlay and other views had the body incorrectly painted back over the garment.

v37 remains a source candidate. Sleeve/cuff/hand seams still require per-facing source polish.

## v39 — hairless body candidate

v39 creates an eight-direction hairless-body source candidate on the same 480×640 body lattice used by v35.

The existing hair is removed and a direction-specific scalp silhouette is reconstructed behind the preserved face / ears / neck / body.

This is not production approval. The scalp is currently an engineering-quality source candidate and still requires manual source-art shaping and shading before it can become the locked hairless body master.

## v40 — hair re-layer validation

v40 registers the approved eight-direction hair source back over the v39 hairless candidate.

The purpose is to validate that:

- hair can exist as an independent paper-doll layer;
- the shared head/crown anchor is workable across all eight facings;
- removing hair from the body does not require changing the character lattice;
- a future hair swap can use the same directional routing.

The re-layer test is successful enough to keep developing the separation path, but it does not make v39 production-ready.

## Locked runtime gate

No 48×64 derivation is allowed yet.

Remaining blockers:

1. final source review of v35 clean chest;
2. manual source-art polish of the v39 hairless scalp;
3. per-facing sleeve/cuff/hand polish on v37;
4. manual equipment registration;
5. four missing NW equipment directions;
6. complete eight-direction source-stack approval.
