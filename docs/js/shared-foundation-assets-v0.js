(() => {
  'use strict';

  const OUTER_FRAME_ID = 'game';
  const REGISTRY_URL = 'data/shared-foundation-runtime.json';
  const PROD_PREFIX = 'af-prod-';
  const frame = document.getElementById(OUTER_FRAME_ID);
  if (!frame) return;

  const activationStatuses = new Set(['runtime-candidate', 'integrated', 'approved']);

  function keyFor(id) {
    return `${PROD_PREFIX}${id}`;
  }

  async function fetchRegistry(win) {
    const response = await win.fetch(REGISTRY_URL, { cache: 'no-store' });
    if (!response.ok) throw new Error(`shared-foundation registry HTTP ${response.status}`);
    return response.json();
  }

  function eligibleAssets(registry) {
    return (registry.assets || []).filter((asset) =>
      asset.enabled === true && activationStatuses.has(asset.status)
    );
  }

  function loadEligible(scene, assets) {
    return new Promise((resolve) => {
      if (!assets.length) return resolve({ loaded: [], failed: [] });

      const loaded = [];
      const failed = [];
      const pending = new Set();

      for (const asset of assets) {
        const key = keyFor(asset.id);
        if (scene.textures.exists(key)) {
          loaded.push(asset.id);
          continue;
        }
        pending.add(key);
        scene.load.image(key, asset.runtimePath);
      }

      if (!pending.size) return resolve({ loaded, failed });

      const onFileComplete = (key) => {
        if (!pending.has(key)) return;
        pending.delete(key);
        loaded.push(key.slice(PROD_PREFIX.length));
      };
      const onFileError = (file) => {
        const key = file?.key;
        if (!pending.has(key)) return;
        pending.delete(key);
        failed.push(key.slice(PROD_PREFIX.length));
      };

      scene.load.on('filecomplete', onFileComplete);
      scene.load.on('loaderror', onFileError);
      scene.load.once('complete', () => {
        scene.load.off('filecomplete', onFileComplete);
        scene.load.off('loaderror', onFileError);
        resolve({ loaded, failed });
      });
      scene.load.start();
    });
  }

  function swapScaffoldTextures(scene, registry, loadedIds) {
    const loaded = new Set(loadedIds);
    const swaps = [];

    for (const asset of registry.assets || []) {
      if (!loaded.has(asset.id) || !asset.replacesScaffoldTexture) continue;
      const productionKey = keyFor(asset.id);
      for (const obj of scene.afRefactorObjects || []) {
        const currentKey = obj?.texture?.key;
        if (currentKey !== asset.replacesScaffoldTexture) continue;
        obj.setTexture?.(productionKey);
        obj.setData?.('afProductionAssetId', asset.id);
        obj.setData?.('afProductionAssetStatus', asset.status);
        swaps.push({ assetId: asset.id, replaced: currentKey });
      }
    }

    return swaps;
  }

  function updateScaffoldLabel(scene, activatedCount) {
    const labels = (scene.afLayerObjects?.['atmosphere-fx'] || []).filter((obj) => obj?.text?.includes('TECHNICAL WORLD-REFACTOR'));
    for (const label of labels) {
      if (activatedCount > 0) {
        label.setText(`MIXED TECHNICAL SCAFFOLD + ${activatedCount} RUNTIME CANDIDATE${activatedCount === 1 ? '' : 'S'} · NOT ART REVIEW`);
      }
    }
  }

  function installAudit(win, registry, result, swaps) {
    const prior = win.AF_SHARED_FOUNDATION_V0 || {};
    const activated = swaps.map((entry) => entry.assetId);
    win.AF_SHARED_FOUNDATION_V0 = {
      ...prior,
      installed: true,
      version: '0.1.0',
      registryUrl: REGISTRY_URL,
      reviewState: registry.reviewState,
      eligible: eligibleAssets(registry).map((asset) => asset.id),
      loaded: result.loaded,
      failed: result.failed,
      activated,
      productionArtComplete: false,
      audit() {
        return {
          installed: true,
          registryUrl: REGISTRY_URL,
          reviewState: registry.reviewState,
          eligible: [...this.eligible],
          loaded: [...this.loaded],
          failed: [...this.failed],
          activated: [...this.activated],
          productionArtComplete: false,
          note: 'Only explicitly enabled runtime-candidate-or-higher assets may replace technical scaffold textures. Mixed scenes remain invalid for art review.'
        };
      }
    };
    win.AF_TEST ||= {};
    win.AF_TEST.sharedFoundation = () => win.AF_SHARED_FOUNDATION_V0.audit();
  }

  async function activate(win) {
    if (!win.AF_GAME || !win.AF_TEST?.MAPS || !win.AF_WORLD_REFACTOR_V0?.installed) return false;

    let scene;
    try { scene = win.AF_GAME.scene.getScene('World'); } catch (_) { return false; }
    if (!scene) return false;

    const registry = await fetchRegistry(win);
    const eligible = eligibleAssets(registry);
    const result = await loadEligible(scene, eligible);
    const swaps = swapScaffoldTextures(scene, registry, result.loaded);
    updateScaffoldLabel(scene, swaps.length);
    installAudit(win, registry, result, swaps);

    console.info('Astro Fighters shared-foundation runtime registry', win.AF_SHARED_FOUNDATION_V0.audit());
    return true;
  }

  function boot() {
    const win = frame.contentWindow;
    if (!win) return;
    let attempts = 0;
    const timer = setInterval(async () => {
      attempts += 1;
      try {
        if (await activate(win)) clearInterval(timer);
      } catch (error) {
        console.warn('Shared-foundation runtime activation deferred', error);
      }
      if (attempts > 200) clearInterval(timer);
    }, 75);
  }

  frame.addEventListener('load', boot);
  if (frame.contentDocument?.readyState === 'complete') boot();
})();
