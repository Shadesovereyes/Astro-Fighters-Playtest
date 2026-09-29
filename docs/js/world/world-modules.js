/* Astro Fighters — authored world module registry.
   Source authority: the committed /World Assets folder. Runtime copies live under docs/assets/world/.
   derivation 'copy'       — runtime file is byte-identical to the source.
   derivation 'alpha-snap' — source was exported with near-opaque alpha (248–254); the runtime copy
                              snaps alpha ≥128 → 255 and <128 → 0 with RGB untouched
                              (tools/sync-runtime-assets.mjs). Fix at source to return to 'copy'.
   Any id listed here replaces the procedural scaffold texture of the same id in Phaser.
   QA state lives in production/asset-manifest.json; being listed here is not approval. */
(() => {
  'use strict';
  const W = 'World Assets/Exterior/';
  const sf = (id, src, derivation = 'copy') => [id, {path: `assets/world/shared-foundation/${id}.png`, source: W + src, derivation}];
  const dr = (id, src, derivation = 'copy') => [id, {path: `assets/world/slice0-dressing/${id}.png`, source: W + src, derivation}];
  window.AF_WORLD_MODULES = Object.fromEntries([
    sf('stone-clean', 'Ground/Stone Floor/stone-clean/Stone Floor.png'),
    sf('stone-cracked', 'Ground/Stone Floor/stone-cracked/stone-cracked.png'),
    sf('stone-patched', 'Ground/Stone Floor/stone-patched/Stone Patched.png'),
    sf('stone-timber-transition', 'Ground/Stone Floor/stone-timber-transition/Stone-timber-transition.png'),
    sf('building-threshold', 'Ground/Door threshold/Door Threshorld .png'),
    sf('drainage-channel', 'Ground/Drainage/drainage-channel-east-west/drainage-channel-east-west.png'),
    sf('drainage-grate', 'Decals/drainage-grate/drainage-grate.png'),
    sf('cracks', 'Decals/cracks/cracks.png'),
    sf('stains', 'Decals/stains/stains.png'),
    sf('cart-wear', 'Decals/cart-wear/cart-wear.png'),
    sf('timber-post', 'architecture/timber-post/timber-post.png'),
    sf('horizontal-beam', 'architecture/horizontal-beam/horizontal-beam.png'),
    sf('timber-plaster-wall', 'architecture/timber-plaster-wall/timber-plaster-wall.png', 'alpha-snap'),
    sf('aged-stone-foundation', 'architecture/aged-stone-foundation/aged-stone-foundation.png'),
    dr('doorway', 'architecture/doorway/Doorway.png'),
    dr('noren', 'architecture/noren/noren.png', 'alpha-snap'),
    dr('lantern-post', 'architecture/lantern-post/lantern-post.png', 'alpha-snap'),
    dr('crate-stack', 'architecture/crate-stack/crate-stack.png', 'alpha-snap')
  ]);
})();
