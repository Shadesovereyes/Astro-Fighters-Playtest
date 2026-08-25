/* Astro Fighters World Package 04 — thresholds, foundations, and timber post/beam staging.
   Reference-first Phaser integration candidate. Not checklist completion. */
(() => {
  "use strict";
  const API = window.AF_WORLD_PACKAGE04 = window.AF_WORLD_PACKAGE04 || {};
  API.version = "package04";
  API.status = "reference-gate-passed-phaser-staging-candidate";
  const ATLAS_URL = "assets/runtime/world/package04/package04-runtime-atlas-512x128.png";
  const TEX = "af-world-p04-atlas";
  const FRAMES = {
    threshold: [0,0,90,75],
    foundation_low: [96,0,65,71],
    foundation_mid: [168,0,75,94],
    foundation_high: [248,0,98,96],
    post_beam: [352,0,62,99]
  };
  const FOUNDATION_KEYS = ["foundation_low", "foundation_mid", "foundation_high"];

  function notice(message) {
    console.warn("[AF world p04]", message);
    let el = document.getElementById("af-world-package04-warning");
    if (!el) {
      el = document.createElement("div");
      el.id = "af-world-package04-warning";
      el.style.cssText = "position:fixed;z-index:99997;right:8px;bottom:8px;max-width:520px;padding:8px 10px;background:#141410;color:#D5BAA0;border:1px solid #756A55;font:11px/1.35 ui-monospace,monospace;pointer-events:none";
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
      if (["player","fighter","hero"].includes(n)) candidates.push(o);
      if (typeof o.getData === "function" && (o.getData("isPlayer") || o.getData("playerControlled"))) candidates.push(o);
    }
    return candidates.find(o => o && Number.isFinite(o.x) && Number.isFinite(o.y)) || null;
  }

  function registerFrames(scene) {
    const texture = scene.textures.get(TEX);
    if (!texture || texture.key === "__MISSING") throw new Error("Package 04 atlas texture missing");
    for (const [name, [x,y,w,h]] of Object.entries(FRAMES)) {
      if (!texture.has(name)) texture.add(name, 0, x, y, w, h);
    }
    texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
  }

  function loadAtlas(scene) {
    return new Promise((resolve, reject) => {
      if (scene.textures.exists(TEX)) { registerFrames(scene); return resolve(); }
      const fail = file => reject(new Error("Package 04 asset load failed: " + (file?.key || file?.src || "unknown")));
      scene.load.once("loaderror", fail);
      scene.load.once("complete", () => { scene.load.off("loaderror", fail); try { registerFrames(scene); resolve(); } catch (e) { reject(e); } });
      scene.load.image(TEX, ATLAS_URL);
      if (!scene.load.isLoading()) scene.load.start();
    });
  }

  function createAssembly(scene) {
    const target = locatePlayer(scene);
    const ground = window.AF_WORLD_PACKAGE03?.active?.module;
    const anchorX = Math.round(ground?.x ?? target?.x ?? scene.cameras?.main?.worldView?.centerX ?? 0);
    const anchorY = Math.round((ground?.y ?? target?.y ?? scene.cameras?.main?.worldView?.centerY ?? 0) - 44);
    const targetDepth = Number.isFinite(target?.depth) ? target.depth : anchorY;

    const foundation = scene.add.image(anchorX, anchorY, TEX, "foundation_mid").setOrigin(0.5, 1);
    const threshold = scene.add.image(anchorX, anchorY + 28, TEX, "threshold").setOrigin(0.5, 1);
    const post = scene.add.image(anchorX + 58, anchorY - 2, TEX, "post_beam").setOrigin(0.5, 1);
    foundation.setDepth(targetDepth - 2);
    threshold.setDepth(targetDepth - 1);
    post.setDepth(targetDepth + 1);

    const state = { scene, target, foundation, threshold, post, visible: true, foundationIndex: 1, anchorX, anchorY };
    state.setVisible = v => {
      state.visible = !!v;
      foundation.setVisible(state.visible); threshold.setVisible(state.visible); post.setVisible(state.visible);
    };
    state.cycleFoundation = () => {
      state.foundationIndex = (state.foundationIndex + 1) % FOUNDATION_KEYS.length;
      const k = FOUNDATION_KEYS[state.foundationIndex];
      foundation.setFrame(k);
      notice(`Package 04 foundation: ${k.replace('foundation_','')}. F5 cycles; F4 toggles. F6/F7 remain Package 03 ground controls.`);
    };
    state.destroy = () => { foundation.destroy(); threshold.destroy(); post.destroy(); };

    const keys = scene.input?.keyboard?.addKeys({ toggle: "F4", cycle: "F5" }) || null;
    const update = () => {
      if (!foundation.active) return;
      if (keys) {
        if (Phaser.Input.Keyboard.JustDown(keys.toggle)) state.setVisible(!state.visible);
        if (Phaser.Input.Keyboard.JustDown(keys.cycle)) state.cycleFoundation();
      }
      if (target && target.active !== false) {
        const d = Number.isFinite(target.depth) ? target.depth : target.y;
        foundation.setDepth(d - 2);
        threshold.setDepth(d - 1);
        // Screen y grows downward: north/behind the post means the post should occlude the fighter.
        post.setDepth(target.y < post.y ? d + 1 : d - 1);
      }
    };
    scene.events.on("update", update);
    scene.events.once("shutdown", () => scene.events.off("update", update));
    API.active = state;
    return state;
  }

  API.install = async function install() {
    try {
      const found = findScene();
      if (!found) { notice("World Package 04: active Phaser scene not detected."); return null; }
      await loadAtlas(found.scene);
      const state = createAssembly(found.scene);
      notice("World Package 04 attached in Phaser. F4 toggles structure; F5 cycles foundation height. Post/beam performs a north/south occlusion staging test.");
      return state;
    } catch (e) {
      notice("World Package 04 integration failed: " + (e?.message || e));
      return null;
    }
  };

  function boot(attempt = 0) {
    if (findScene()) return API.install();
    if (attempt < 80) return setTimeout(() => boot(attempt + 1), 250);
    notice("World Package 04: Phaser runtime was not detected after 20 seconds.");
  }
  boot();
})();
