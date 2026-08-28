/* Astro Fighters — Package 07 Kairo composite idle benchmark.
   Pixel-accurate runtime benchmark only; not a substitute for the modular paper-doll stack. */
(() => {
  "use strict";
  const API = window.AF_KAIRO_IDLE_BENCHMARK = window.AF_KAIRO_IDLE_BENCHMARK || {};
  const MANIFEST_URL = "assets/metadata/characters/package07-kairo-idle-benchmark.json";
  const TEX = "af-kairo-idle-benchmark";
  API.version = "package07-benchmark-v3";
  API.status = "runtime-composite-benchmark-candidate";

  function note(t) {
    console.warn("[AF Kairo benchmark]", t);
    let e = document.getElementById("af-kairo-benchmark-note");
    if (!e) {
      e = document.createElement("div");
      e.id = "af-kairo-benchmark-note";
      e.style.cssText = "position:fixed;z-index:99995;left:8px;bottom:8px;max-width:520px;padding:7px 9px;background:#141410;color:#D5BAA0;border:1px solid #756A55;font:10px/1.35 ui-monospace,monospace;pointer-events:none";
      document.body.appendChild(e);
    }
    e.textContent = t;
  }

  function findScene() {
    const P = window.Phaser;
    if (!P || !Array.isArray(P.GAMES) || !P.GAMES.length) return null;
    const game = P.GAMES.find(Boolean);
    const scene = game?.scene?.getScenes(true)?.find(s => s?.sys?.isActive());
    return scene ? { P, game, scene } : null;
  }

  function player(scene) {
    const candidates = [scene.player, scene.registry?.get?.("player"), scene.data?.get?.("player")];
    for (const o of scene.children?.list || []) {
      if (!o) continue;
      const n = String(o.name || "").toLowerCase();
      if (["player","fighter","hero"].includes(n)) candidates.push(o);
      if (typeof o.getData === "function" && (o.getData("isPlayer") || o.getData("playerControlled"))) candidates.push(o);
    }
    return candidates.find(o => o && Number.isFinite(o.x) && Number.isFinite(o.y)) || null;
  }

  async function getManifest() {
    const r = await fetch(MANIFEST_URL, { cache: "no-store" });
    if (!r.ok) throw new Error("manifest " + r.status);
    return r.json();
  }

  function frameName(layer, dir) { return `${layer}-${dir}`; }

  function register(scene, m) {
    const t = scene.textures.get(TEX);
    if (!t || t.key === "__MISSING") throw new Error("benchmark texture missing");
    const fw = m.atlas.frame_width, fh = m.atlas.frame_height;
    for (const [dir, idx] of Object.entries(m.direction_frame_index)) {
      for (const [layer, info] of Object.entries(m.layers)) {
        const name = frameName(layer, dir);
        if (!t.has(name)) t.add(name, 0, idx * fw, info.row * fh, fw, fh);
      }
    }
    t.setFilter(Phaser.Textures.FilterMode.NEAREST);
  }

  async function load(scene, m) {
    if (!scene.textures.exists(TEX)) {
      await new Promise((resolve, reject) => {
        const fail = f => reject(new Error("benchmark atlas failed: " + (f?.src || "unknown")));
        scene.load.once("loaderror", fail);
        scene.load.once("complete", () => {
          scene.load.off("loaderror", fail);
          resolve();
        });
        scene.load.image(TEX, m.atlas.image);
        if (!scene.load.isLoading()) scene.load.start();
      });
    }
    register(scene, m);
  }

  function create(scene, m) {
    const target = player(scene);
    const root = scene.add.container(0, 0);
    root.name = "af-kairo-idle-benchmark";
    root.setDepth(999991);

    const shadow = scene.add.image(0, 0, TEX, frameName("shadow", "s"));
    const character = scene.add.image(0, 0, TEX, frameName("character", "s"));
    const ox = m.anchor[0] / m.runtime_frame_size[0];
    const oy = m.anchor[1] / m.runtime_frame_size[1];
    shadow.setOrigin(ox, oy);
    character.setOrigin(ox, oy);
    shadow.texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
    character.texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
    root.add([shadow, character]);

    const state = {
      scene, target, root, shadow, character,
      direction: "s",
      visible: true,
      replace: !!window.AF_KAIRO_BENCHMARK_REPLACE
    };

    function setDirection(dir) {
      if (!(dir in m.direction_frame_index)) return;
      state.direction = dir;
      shadow.setFrame(frameName("shadow", dir));
      character.setFrame(frameName("character", dir));
    }
    state.setDirection = setDirection;
    state.setVisible = v => { state.visible = !!v; root.setVisible(state.visible); };
    state.destroy = () => {
      if (state.target && state.replace && typeof state.target.setVisible === "function") state.target.setVisible(true);
      root.destroy(true);
    };

    if (target && state.replace && typeof target.setVisible === "function") target.setVisible(false);

    const keys = scene.input?.keyboard?.addKeys({
      N:"NUMPAD_EIGHT", NE:"NUMPAD_NINE", E:"NUMPAD_SIX", SE:"NUMPAD_THREE",
      S:"NUMPAD_TWO", SW:"NUMPAD_ONE", W:"NUMPAD_FOUR", NW:"NUMPAD_SEVEN",
      toggle:"F11"
    });

    const update = () => {
      if (!root.active) return;
      if (target && target.active !== false) {
        let x = target.x, y = target.y;
        if (typeof target.getBottomCenter === "function") {
          const b = target.getBottomCenter();
          if (b && Number.isFinite(b.x) && Number.isFinite(b.y)) { x = b.x; y = b.y; }
        }
        root.setPosition(Math.round(x), Math.round(y));
        if (Number.isFinite(target.depth)) root.setDepth(target.depth + 0.02);
      } else {
        const cam = scene.cameras?.main;
        if (cam) root.setPosition(Math.round(cam.worldView.centerX), Math.round(cam.worldView.centerY));
      }

      if (keys) {
        for (const [dir, key] of [["n","N"],["ne","NE"],["e","E"],["se","SE"],["s","S"],["sw","SW"],["w","W"],["nw","NW"]]) {
          if (Phaser.Input.Keyboard.JustDown(keys[key])) setDirection(dir);
        }
        if (Phaser.Input.Keyboard.JustDown(keys.toggle)) state.setVisible(!state.visible);
      }
    };
    scene.events.on("update", update);
    scene.events.once("shutdown", () => scene.events.off("update", update));

    API.active = state;
    return state;
  }

  API.install = async () => {
    try {
      const f = findScene();
      if (!f) { note("Package 07 benchmark: active Phaser scene not detected."); return null; }
      const m = await getManifest();
      await load(f.scene, m);
      const state = create(f.scene, m);
      note("Kairo 8-direction idle benchmark attached. F11 toggles; numpad changes facing. Composite benchmark only.");
      return state;
    } catch (e) {
      note("Package 07 benchmark failed: " + (e?.message || e));
      return null;
    }
  };

  (function boot(n=0){
    if (findScene()) return API.install();
    if (n < 80) setTimeout(() => boot(n+1), 250);
    else note("Package 07 benchmark: Phaser runtime not detected after 20s.");
  })();
})();
