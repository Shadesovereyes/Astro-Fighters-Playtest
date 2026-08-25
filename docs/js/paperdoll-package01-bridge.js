/* Astro Fighters paper-doll Package 01 Phaser integration bridge.
   Engineering candidate only: do not treat as art approval. */
(() => {
  "use strict";
  const PACKAGE_URL = "assets/metadata/characters/kairo-package01.json";
  const TEXTURE_KEY = "af-pd01-atlas";
  const API = window.AF_PAPERDOLL_PACKAGE01 = window.AF_PAPERDOLL_PACKAGE01 || {};
  API.version = "package01";
  API.status = "reference-derived-engineering-candidate";
  API.instances = [];

  function notice(message) {
    console.warn("[AF paperdoll]", message);
    let el = document.getElementById("af-paperdoll-warning");
    if (!el) {
      el = document.createElement("div");
      el.id = "af-paperdoll-warning";
      el.style.cssText = "position:fixed;z-index:99999;right:8px;bottom:8px;max-width:390px;padding:8px 10px;background:#141410;color:#F5D5BB;border:1px solid #756A55;font:11px/1.35 ui-monospace,monospace;pointer-events:none";
      document.body.appendChild(el);
    }
    el.textContent = message;
  }

  function getGameAndScene() {
    const P = window.Phaser;
    if (!P || !Array.isArray(P.GAMES) || !P.GAMES.length) return null;
    const game = P.GAMES.find(Boolean);
    if (!game || !game.scene) return null;
    const scenes = game.scene.getScenes(true);
    const scene = scenes.find(s => s && s.sys && s.sys.isActive());
    return scene ? { P, game, scene } : null;
  }

  function locatePlayer(scene) {
    const candidates = [];
    if (scene.player) candidates.push(scene.player);
    if (scene.registry && scene.registry.get("player")) candidates.push(scene.registry.get("player"));
    if (scene.data && scene.data.get("player")) candidates.push(scene.data.get("player"));
    if (scene.children && Array.isArray(scene.children.list)) {
      for (const o of scene.children.list) {
        if (!o) continue;
        const n = String(o.name || "").toLowerCase();
        if (n === "player" || n === "fighter" || n === "hero") candidates.push(o);
        if (typeof o.getData === "function" && (o.getData("isPlayer") || o.getData("playerControlled"))) candidates.push(o);
      }
    }
    return candidates.find(o => o && Number.isFinite(o.x) && Number.isFinite(o.y)) || null;
  }

  async function fetchManifest() {
    const response = await fetch(PACKAGE_URL, { cache: "no-store" });
    if (!response.ok) throw new Error("manifest " + response.status);
    return response.json();
  }

  function frameName(layer, dir) { return layer + "-" + dir; }

  function registerFrames(scene, manifest) {
    const texture = scene.textures.get(TEXTURE_KEY);
    if (!texture || texture.key === "__MISSING") throw new Error("packed texture missing");
    const fw = manifest.atlas.frame_width || manifest.runtime_frame_size[0];
    const fh = manifest.atlas.frame_height || manifest.runtime_frame_size[1];
    for (const [layer, info] of Object.entries(manifest.layers)) {
      for (const [dir, index] of Object.entries(manifest.direction_frame_index)) {
        const name = frameName(layer, dir);
        if (!texture.has(name)) texture.add(name, 0, index * fw, info.row * fh, fw, fh);
      }
    }
    texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
  }

  function loadAtlas(scene, manifest) {
    return new Promise((resolve, reject) => {
      if (scene.textures.exists(TEXTURE_KEY)) {
        registerFrames(scene, manifest);
        return resolve();
      }
      const onError = file => reject(new Error("asset load failed: " + (file && file.src || "unknown")));
      scene.load.once("loaderror", onError);
      scene.load.once("complete", () => {
        scene.load.off("loaderror", onError);
        try { registerFrames(scene, manifest); resolve(); } catch (e) { reject(e); }
      });
      const atlasSource = window.AF_PAPERDOLL_PACKAGE01_ATLAS_DATA_URI || manifest.atlas.image;
      scene.load.image(TEXTURE_KEY, atlasSource);
      if (!scene.load.isLoading()) scene.load.start();
    });
  }

  function createPaperDoll(scene, manifest) {
    const target = locatePlayer(scene);
    const container = scene.add.container(0, 0);
    container.name = "af-paperdoll-package01";
    container.setDepth(999990);

    const sprites = {};
    for (const layer of Object.keys(manifest.layers)) {
      const s = scene.add.image(0, 0, TEXTURE_KEY, frameName(layer, "s"));
      s.name = "af-pd01-" + layer;
      s.setOrigin(
        manifest.anchor[0] / manifest.runtime_frame_size[0],
        manifest.anchor[1] / manifest.runtime_frame_size[1]
      );
      sprites[layer] = s;
    }

    const state = {
      scene, manifest, target, container, sprites,
      direction: "s",
      visible: true,
      replace: !!window.AF_PAPERDOLL_PACKAGE01_REPLACE
    };

    function applyOrder() {
      const order = manifest.layer_order_by_direction[state.direction] || manifest.layer_order_default;
      container.removeAll(false);
      for (const layer of order) if (sprites[layer]) container.add(sprites[layer]);
    }

    function setDirection(dir) {
      if (!(dir in manifest.direction_frame_index)) return;
      state.direction = dir;
      for (const [layer, sprite] of Object.entries(sprites)) sprite.setFrame(frameName(layer, dir));
      applyOrder();
    }

    state.setDirection = setDirection;
    state.setLayerVisible = (layer, visible) => { if (sprites[layer]) sprites[layer].setVisible(!!visible); };
    state.setVisible = visible => { state.visible = !!visible; container.setVisible(state.visible); };
    state.destroy = () => {
      if (state.target && state.replace && typeof state.target.setVisible === "function") state.target.setVisible(true);
      container.destroy(true);
    };

    setDirection("s");
    if (target && state.replace && typeof target.setVisible === "function") target.setVisible(false);

    const keys = scene.input && scene.input.keyboard ? scene.input.keyboard.addKeys({
      N: "NUMPAD_EIGHT", NE: "NUMPAD_NINE", E: "NUMPAD_SIX", SE: "NUMPAD_THREE",
      S: "NUMPAD_TWO", SW: "NUMPAD_ONE", W: "NUMPAD_FOUR", NW: "NUMPAD_SEVEN",
      toggle: "F8"
    }) : null;

    const update = () => {
      if (!container.active) return;
      if (target && target.active !== false) {
        let x = target.x, y = target.y;
        if (typeof target.getBottomCenter === "function") {
          const b = target.getBottomCenter();
          if (b && Number.isFinite(b.x) && Number.isFinite(b.y)) { x = b.x; y = b.y; }
        }
        container.setPosition(Math.round(x), Math.round(y));
        if (Number.isFinite(target.depth)) container.setDepth(target.depth + 0.01);
      } else if (scene.cameras && scene.cameras.main) {
        const cam = scene.cameras.main;
        container.setPosition(Math.round(cam.worldView.centerX), Math.round(cam.worldView.centerY));
      }

      if (keys) {
        for (const [dir, keyName] of [["n","N"],["ne","NE"],["e","E"],["se","SE"],["s","S"],["sw","SW"],["w","W"],["nw","NW"]]) {
          if (Phaser.Input.Keyboard.JustDown(keys[keyName])) setDirection(dir);
        }
        if (Phaser.Input.Keyboard.JustDown(keys.toggle)) state.setVisible(!state.visible);
      }
    };

    scene.events.on("update", update);
    scene.events.once("shutdown", () => scene.events.off("update", update));
    API.instances.push(state);
    API.active = state;
    return state;
  }

  API.install = async function install() {
    try {
      const found = getGameAndScene();
      if (!found) {
        notice("Paper-doll Package 01: Phaser.GAMES active scene not detected. Integration did not attach.");
        return null;
      }
      const manifest = await fetchManifest();
      await loadAtlas(found.scene, manifest);
      const state = createPaperDoll(found.scene, manifest);
      notice(state.target
        ? "Paper-doll Package 01 attached to the active Phaser player. F8 toggles; numpad directions select facing."
        : "Paper-doll Package 01 loaded into the active Phaser scene, but the player object was not auto-detected; candidate is at camera center.");
      return state;
    } catch (err) {
      notice("Paper-doll Package 01 integration failed: " + (err && err.message || err));
      return null;
    }
  };

  function boot(attempt = 0) {
    if (getGameAndScene()) return API.install();
    if (attempt < 80) return setTimeout(() => boot(attempt + 1), 250);
    notice("Paper-doll Package 01: Phaser runtime was not detected after 20 seconds.");
  }

  boot();
})();
