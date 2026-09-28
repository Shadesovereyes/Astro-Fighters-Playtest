/* Astro Fighters — approved character sheet registry.
   Register the approved 512×64 base sheets (eight 64×64 directional frames) and their
   transparent 512×64 overlays here once they are committed under docs/assets/characters/.
   Paths are relative to /docs. While `approved.male` is null the runtime falls back to the
   legacy 48×64 runtime candidate sheets and labels them as such. Never register a redrawn,
   regenerated, resized, or resampled copy of an approved base sheet. */
(() => {
  'use strict';
  window.AF_CHARACTERS = {
    approved: {
      male: null,   // 'assets/characters/base/male-base.png'
      female: null  // 'assets/characters/base/female-base.png'
    },
    // layer -> [{id, path}] ; draw order follows the list order, after the base sheet.
    overlays: {}
  };
})();
