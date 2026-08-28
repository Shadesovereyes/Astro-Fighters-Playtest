/* Astro Fighters World Package 03 v5 — Imperial stone material module bridge.
   Reference-first staging integration. Runtime PNG bytes are loaded from text data chunks.
   This is not checklist completion. */
(() => {
  "use strict";
  const API = window.AF_WORLD_PACKAGE03 = window.AF_WORLD_PACKAGE03 || {};
  API.version = "package03-v5";
  API.status = "reference-gate-passed-single-module-integration-candidate";
  const MATERIALS = ["clean", "cracked", "patched", "damp"];

  function notice(message) {
    console.warn("[AF world p03]", message);
    let el = document.getElementById("af-world-package03-warning");
    if (!el) {
      el = document.createElement("div");
      el.id = "af-world-package03-warning";
      el.style.cssText = "position:fixed;z-index:99998;left:8px;bottom:8px;max-width:520px;padding:8px 10px;background:#141410;color:#D5BAA0;border:1px solid #756A55;font:11px/1.35 ui-monospace,monospace;pointer-events:none";
      document.body.appendChild(el);
    }
    el.textContent = message;
  }

  function findScene() {
    const P = window.Phaser;
    if (!P || !Array.isArray(P.GAMES) || !P.GAMES.length) return null;
    const game = P.GAMES.find(Boolean);
    const scene = game?.scene?.getScenes(true)?.find(s => s?.sys?.isActive());
    return scene ? { P, game, scene } : null;
  }

  function locatePlayer(scene) {
    const pd = window.AF_PAPERDOLL_PACKAGE01?.active;
    if (pd?.target && Number.isFinite(pd.target.x) && Number.isFinite(pd.target.y)) return pd.target;
    const candidates = [scene.player, scene.registry?.get?.("player"), scene.data?.get?.("player")];
    for (const o of scene.children?.list || []) {
      if (!o) continue;
      const n = String(o.name || "").toLowerCase();
      if (["player", "fighter", "hero"].includes(n)) candidates.push(o);
      if (typeof o.getData === "function" && (o.getData("isPlayer") || o.getData("playerControlled"))) candidates.push(o);
    }
    return candidates.find(o => o && Number.isFinite(o.x) && Number.isFinite(o.y)) || null;
  }

  function loadTextures(scene) {
    const data = window.AF_WORLD_P03_DATA || {};
    for (const mat of MATERIALS) if (!data[mat]) throw new Error(`embedded material data missing: ${mat}`);
    return new Promise((resolve, reject) => {
      let missing = 0;
      for (const mat of MATERIALS) {
        const key = `af-world-p03-${mat}`;
        if (!scene.textures.exists(key)) { scene.load.image(key, data[mat]); missing++; }
      }
      if (!missing) return resolve();
      const fail = file => reject(new Error("stone module load failed: " + (file?.key || file?.src || "unknown")));
      scene.load.once("loaderror", fail);
      scene.load.once("complete", () => { scene.load.off("loaderror", fail); resolve(); });
      if (!scene.load.isLoading()) scene.load.start();
    });
  }

  function createModule(scene) {
    const target = locatePlayer(scene);
    const module = scene.add.image(0, 0, `af-world-p03-${MATERIALS[0]}`);
    module.name = "af-world-package03-material-module";
    module.setOrigin(0.5, 0.5);
    module.texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
    const p = target || { x: scene.cameras?.main?.worldView?.centerX || 0, y: scene.cameras?.main?.worldView?.centerY || 0 };
    module.setPosition(Math.round(p.x), Math.round(p.y + 24));
    module.setDepth(Number.isFinite(target?.depth) ? target.depth - 100 : -20);

    const state = { scene, target, module, materials: MATERIALS.slice(), index: 0, visible: true };
    state.setMaterial = mat => {
      const i = MATERIALS.indexOf(mat);
      if (i < 0) return false;
      state.index = i;
      module.setTexture(`af-world-p03-${mat}`);
      module.texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
      return true;
    };
    state.cycle = () => {
      state.index = (state.index + 1) % MATERIALS.length;
      state.setMaterial(MATERIALS[state.index]);
      notice(`Package 03 material: ${MATERIALS[state.index]}. F6 cycles; F7 toggles. Single authored module only—no edge-to-edge tiling.`);
    };
    state.setVisible = v => { state.visible = !!v; module.setVisible(state.visible); };
    state.destroy = () => module.destroy();

    const keys = scene.input?.keyboard?.addKeys({ cycle: "F6", toggle: "F7" }) || null;
    const update = () => {
      if (!module.active || !keys) return;
      if (Phaser.Input.Keyboard.JustDown(keys.cycle)) state.cycle();
      if (Phaser.Input.Keyboard.JustDown(keys.toggle)) state.setVisible(!state.visible);
    };
    scene.events.on("update", update);
    scene.events.once("shutdown", () => scene.events.off("update", update));
    API.active = state;
    return state;
  }

  API.install = async function install() {
    try {
      const found = findScene();
      if (!found) { notice("World Package 03: active Phaser scene not detected."); return null; }
      await loadTextures(found.scene);
      const state = createModule(found.scene);
      notice("World Package 03 v5 attached in Phaser. F6 cycles clean/cracked/patched/damp; F7 toggles. Embedded runtime modules; no repeated ground tiling in this gate.");
      return state;
    } catch (e) {
      notice("World Package 03 integration failed: " + (e?.message || e));
      return null;
    }
  };

  function boot(attempt = 0) {
    if (findScene()) return API.install();
    if (attempt < 80) return setTimeout(() => boot(attempt + 1), 250);
    notice("World Package 03: Phaser runtime was not detected after 20 seconds.");
  }
  boot();
})();
