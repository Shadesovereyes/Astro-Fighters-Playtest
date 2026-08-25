/* Astro Fighters World Package 02 — Worn Imperial stone street (clean)
   Phaser integration candidate. No checklist completion implied. */
(() => {
  "use strict";
  const MANIFEST_URL = "assets/metadata/world/imperial-stone-clean-package02.json";
  const TEXTURE_KEY = "af-world-p02-stone-clean";
  const API = window.AF_WORLD_PACKAGE02 = window.AF_WORLD_PACKAGE02 || {};
  API.version = "package02";
  API.status = "reference-derived-integration-candidate";

  function notice(message) {
    console.warn("[AF world p02]", message);
    let el = document.getElementById("af-world-package02-warning");
    if (!el) {
      el = document.createElement("div");
      el.id = "af-world-package02-warning";
      el.style.cssText = "position:fixed;z-index:99998;left:8px;bottom:8px;max-width:430px;padding:8px 10px;background:#141410;color:#F5D5BB;border:1px solid #756A55;font:11px/1.35 ui-monospace,monospace;pointer-events:none";
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
      const name = String(o.name || "").toLowerCase();
      if (["player","fighter","hero"].includes(name)) candidates.push(o);
      if (typeof o.getData === "function" && (o.getData("isPlayer") || o.getData("playerControlled"))) candidates.push(o);
    }
    return candidates.find(o => o && Number.isFinite(o.x) && Number.isFinite(o.y)) || null;
  }

  async function fetchManifest() {
    const r = await fetch(MANIFEST_URL, { cache: "no-store" });
    if (!r.ok) throw new Error("manifest " + r.status);
    return r.json();
  }

  function registerFrames(scene, manifest) {
    const texture = scene.textures.get(TEXTURE_KEY);
    if (!texture || texture.key === "__MISSING") throw new Error("stone atlas texture missing");
    for (const [name, rect] of Object.entries(manifest.runtime.variants)) {
      if (!texture.has(name)) texture.add(name, 0, rect[0], rect[1], rect[2], rect[3]);
    }
    texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
  }

  function loadTexture(scene, manifest) {
    return new Promise((resolve, reject) => {
      if (scene.textures.exists(TEXTURE_KEY)) {
        registerFrames(scene, manifest);
        return resolve();
      }
      const data = window.AF_WORLD_PACKAGE02_STONE_ATLAS_DATA_URI;
      if (!data) return reject(new Error("embedded stone atlas data was not loaded"));
      const fail = file => reject(new Error("stone atlas load failed: " + (file?.src || "unknown")));
      scene.load.once("loaderror", fail);
      scene.load.once("complete", () => {
        scene.load.off("loaderror", fail);
        try { registerFrames(scene, manifest); resolve(); } catch (e) { reject(e); }
      });
      scene.load.image(TEXTURE_KEY, data);
      if (!scene.load.isLoading()) scene.load.start();
    });
  }

  function hashVariant(cx, cy) {
    let h = Math.imul(cx | 0, 73856093) ^ Math.imul(cy | 0, 19349663);
    h ^= h >>> 13;
    return ["a","b","c","d"][Math.abs(h) & 3];
  }

  function createGround(scene, manifest) {
    const stepX = manifest.integration.macro_step[0];
    const stepY = manifest.integration.macro_step[1];
    const radiusX = 3;
    const radiusY = 3;
    const target = locatePlayer(scene);
    const container = scene.add.container(0, 0);
    container.name = "af-world-package02-stone-ground";
    const cells = [];
    for (let iy = -radiusY; iy <= radiusY; iy++) {
      for (let ix = -radiusX; ix <= radiusX; ix++) {
        const image = scene.add.image(0, 0, TEXTURE_KEY, "a").setOrigin(0, 0);
        image.name = `af-world-p02-stone-${ix}-${iy}`;
        cells.push({ ix, iy, image });
        container.add(image);
      }
    }

    const state = { scene, manifest, target, container, cells, enabled: true, cellX: NaN, cellY: NaN };

    function centerPoint() {
      if (state.target && state.target.active !== false) return { x: state.target.x, y: state.target.y };
      const cam = scene.cameras?.main;
      return cam ? { x: cam.worldView.centerX, y: cam.worldView.centerY } : { x: 0, y: 0 };
    }

    function refresh(force = false) {
      const p = centerPoint();
      const cx = Math.floor(p.x / stepX);
      const cy = Math.floor(p.y / stepY);
      if (!force && cx === state.cellX && cy === state.cellY) return;
      state.cellX = cx; state.cellY = cy;
      for (const c of cells) {
        const gx = cx + c.ix;
        const gy = cy + c.iy;
        c.image.setPosition(gx * stepX, gy * stepY);
        c.image.setFrame(hashVariant(gx, gy));
      }
    }

    state.setVisible = visible => { state.enabled = !!visible; container.setVisible(state.enabled); };
    state.destroy = () => container.destroy(true);
    refresh(true);

    const keys = scene.input?.keyboard?.addKeys({ toggle: "F7" }) || null;
    const update = () => {
      if (!container.active) return;
      refresh(false);
      const depthBase = Number.isFinite(state.target?.depth) ? state.target.depth - 100 : -10;
      container.setDepth(depthBase);
      if (keys && Phaser.Input.Keyboard.JustDown(keys.toggle)) state.setVisible(!state.enabled);
    };
    scene.events.on("update", update);
    scene.events.once("shutdown", () => scene.events.off("update", update));
    API.active = state;
    return state;
  }

  API.install = async function install() {
    try {
      const found = findScene();
      if (!found) {
        notice("World Package 02: active Phaser scene not detected. Stone integration did not attach.");
        return null;
      }
      const manifest = await fetchManifest();
      await loadTexture(found.scene, manifest);
      const state = createGround(found.scene, manifest);
      notice("World Package 02 stone reference derivative attached in Phaser. F7 toggles the ground pass. Hidden 32×32 grid lines are never rendered.");
      return state;
    } catch (e) {
      notice("World Package 02 integration failed: " + (e?.message || e));
      return null;
    }
  };

  function boot(attempt = 0) {
    if (findScene()) return API.install();
    if (attempt < 80) return setTimeout(() => boot(attempt + 1), 250);
    notice("World Package 02: Phaser runtime was not detected after 20 seconds.");
  }
  boot();
})();
