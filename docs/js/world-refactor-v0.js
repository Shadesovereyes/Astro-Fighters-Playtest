(() => {
  'use strict';

  const OUTER_FRAME_ID = 'game';
  const TILE = 32;
  const VIEW_W = 640;
  const VIEW_H = 360;
  const MOVE_SPEED_PPS = 104;
  const PLAYER_RADIUS_X = 0.28;
  const PLAYER_RADIUS_Y = 0.20;
  const LAYER_ORDER = [
    'ground',
    'decals',
    'architecture',
    'architecture-dressing',
    'props-back',
    'collision',
    'interactives',
    'actors',
    'props-front-occluders',
    'local-shadows',
    'atmosphere-fx'
  ];

  const frame = document.getElementById(OUTER_FRAME_ID);
  if (!frame) return;

  function facingFor(dx, dy, fallback = 'S') {
    if (!dx && !dy) return fallback;
    const x = Math.abs(dx) < 0.15 ? 0 : Math.sign(dx);
    const y = Math.abs(dy) < 0.15 ? 0 : Math.sign(dy);
    if (x === 0 && y < 0) return 'N';
    if (x > 0 && y < 0) return 'NE';
    if (x > 0 && y === 0) return 'E';
    if (x > 0 && y > 0) return 'SE';
    if (x === 0 && y > 0) return 'S';
    if (x < 0 && y > 0) return 'SW';
    if (x < 0 && y === 0) return 'W';
    if (x < 0 && y < 0) return 'NW';
    return fallback;
  }

  function overlapsRect(x, y, rx, ry, rect) {
    return (
      x + rx > rect.x &&
      x - rx < rect.x + rect.w &&
      y + ry > rect.y &&
      y - ry < rect.y + rect.h
    );
  }

  function blockedAt(scene, map, x, y) {
    const maxX = (VIEW_W - 16) / TILE;
    const maxY = (VIEW_H - 31) / TILE;
    if (x < 0 || y < 0 || x > maxX || y > maxY) return true;

    const authored = scene.afCollisionRects || map.blocked || [];
    if (authored.some((r) => overlapsRect(x, y, PLAYER_RADIUS_X, PLAYER_RADIUS_Y, r))) return true;

    return (scene.enemies || []).some((enemy) => {
      if (enemy.hp <= 0) return false;
      return Math.hypot(enemy.x - x, enemy.y - y) < 0.56;
    });
  }

  function destroyRefactorObjects(scene) {
    for (const obj of scene.afRefactorObjects || []) {
      try { obj?.destroy?.(); } catch (_) { /* best-effort teardown */ }
    }
    scene.afRefactorObjects = [];
    scene.afLayerObjects = Object.fromEntries(LAYER_ORDER.map((name) => [name, []]));
    scene.afCollisionRects = [];
  }

  function register(scene, layer, obj) {
    if (!obj) return obj;
    scene.afRefactorObjects ||= [];
    scene.afLayerObjects ||= Object.fromEntries(LAYER_ORDER.map((name) => [name, []]));
    obj.setData?.('afWorldLayer', layer);
    scene.afRefactorObjects.push(obj);
    scene.afLayerObjects[layer].push(obj);
    return obj;
  }

  function makeTexture(scene, key, width, height, painter) {
    if (scene.textures.exists(key)) return;
    const g = scene.make.graphics({ x: 0, y: 0, add: false });
    painter(g, width, height);
    g.generateTexture(key, width, height);
    g.destroy();
  }

  function ensureScaffoldTextures(scene) {
    makeTexture(scene, 'af-scaffold-ground', 256, 256, (g) => {
      g.fillStyle(0x777267, 1); g.fillRect(0, 0, 256, 256);
      const stones = [
        [4, 7, 58, 39, 0x817b70], [68, 4, 78, 45, 0x6f6b62], [153, 9, 97, 33, 0x858074],
        [8, 55, 93, 52, 0x706c63], [108, 52, 57, 47, 0x827c70], [172, 49, 77, 60, 0x6b6860],
        [3, 115, 68, 61, 0x827d72], [78, 110, 102, 49, 0x716d64], [187, 118, 63, 51, 0x7f796e],
        [7, 184, 112, 65, 0x706c63], [126, 169, 58, 77, 0x817b70], [191, 176, 59, 70, 0x6c6961]
      ];
      for (const [x, y, w, h, c] of stones) {
        g.fillStyle(c, 1); g.fillRect(x, y, w, h);
        g.lineStyle(2, 0x5a574f, 0.9); g.strokeRect(x, y, w, h);
      }
      g.lineStyle(2, 0x56534c, 0.7);
      g.beginPath(); g.moveTo(29, 26); g.lineTo(41, 36); g.lineTo(37, 49); g.lineTo(52, 57); g.strokePath();
      g.beginPath(); g.moveTo(141, 137); g.lineTo(132, 149); g.lineTo(145, 160); g.lineTo(138, 178); g.strokePath();
      g.beginPath(); g.moveTo(214, 197); g.lineTo(200, 210); g.lineTo(207, 225); g.strokePath();
    });

    makeTexture(scene, 'af-scaffold-wall', 160, 128, (g) => {
      g.fillStyle(0xb6aa8e, 1); g.fillRect(0, 0, 160, 128);
      g.fillStyle(0x3f3528, 1); g.fillRect(0, 0, 10, 128); g.fillRect(150, 0, 10, 128); g.fillRect(0, 0, 160, 10);
      g.fillStyle(0x5d4c37, 1); g.fillRect(72, 0, 12, 128);
      g.fillStyle(0x9e9278, 1); g.fillRect(16, 18, 48, 4); g.fillRect(92, 80, 43, 4);
      g.fillStyle(0x887c67, 1); g.fillRect(22, 94, 31, 3); g.fillRect(101, 30, 34, 3);
    });

    makeTexture(scene, 'af-scaffold-foundation', 128, 32, (g) => {
      g.fillStyle(0x615f59, 1); g.fillRect(0, 0, 128, 32);
      g.fillStyle(0x75716a, 1); g.fillRect(3, 3, 42, 12); g.fillRect(49, 4, 35, 11); g.fillRect(88, 2, 37, 13);
      g.fillStyle(0x6d6962, 1); g.fillRect(5, 18, 31, 11); g.fillRect(40, 17, 51, 12); g.fillRect(95, 18, 29, 10);
      g.lineStyle(1, 0x4f4d49, 1); g.strokeRect(0, 0, 128, 32);
    });

    makeTexture(scene, 'af-scaffold-threshold', 96, 24, (g) => {
      g.fillStyle(0x6a665e, 1); g.fillRect(0, 7, 96, 17);
      g.fillStyle(0x3f3427, 1); g.fillRect(0, 0, 96, 7);
      g.fillStyle(0x908675, 1); g.fillRect(8, 11, 31, 5); g.fillRect(46, 13, 39, 5);
    });

    makeTexture(scene, 'af-scaffold-post', 32, 96, (g) => {
      g.fillStyle(0x2f2921, 1); g.fillRect(7, 0, 18, 96);
      g.fillStyle(0x594936, 1); g.fillRect(10, 3, 8, 89);
      g.fillStyle(0x756047, 1); g.fillRect(11, 8, 4, 74);
      g.fillStyle(0x40382d, 1); g.fillRect(3, 18, 26, 7); g.fillRect(2, 73, 28, 7);
      g.fillStyle(0x77716a, 1); g.fillRect(5, 75, 22, 3);
    });

    makeTexture(scene, 'af-scaffold-shadow', 40, 16, (g) => {
      g.fillStyle(0x11120f, 0.28); g.fillEllipse(20, 8, 34, 10);
    });
  }

  function addTechnicalScaffold(scene, win, mapName) {
    destroyRefactorObjects(scene);
    ensureScaffoldTextures(scene);

    const map = win.AF_TEST.MAPS[mapName] || win.AF_TEST.MAPS['Imperial Docks'];
    const hiddenLegacy = (scene.layers || []).filter((obj) => [-20, -10, -8].includes(obj?.depth));
    hiddenLegacy.forEach((obj) => obj.setVisible?.(false));

    const ground = scene.add.tileSprite(0, 0, VIEW_W, VIEW_H, 'af-scaffold-ground').setOrigin(0).setDepth(-40);
    register(scene, 'ground', ground);

    for (const rect of map.blocked || []) {
      const x = rect.x * TILE;
      const y = rect.y * TILE;
      const w = rect.w * TILE;
      const h = rect.h * TILE;
      const wall = scene.add.tileSprite(x, y, w, h, 'af-scaffold-wall').setOrigin(0).setDepth(10 + rect.y);
      const foundationH = Math.min(24, h);
      const foundation = scene.add.tileSprite(x, y + h - foundationH, w, foundationH, 'af-scaffold-foundation').setOrigin(0).setDepth(20 + rect.y);
      register(scene, 'architecture', wall);
      register(scene, 'architecture', foundation);
    }

    for (const exit of map.exits || []) {
      const threshold = scene.add.image(exit.x * TILE + 16, Math.max(12, exit.y * TILE + 18), 'af-scaffold-threshold')
        .setOrigin(0.5, 0.5)
        .setDepth(55 + exit.y);
      register(scene, 'architecture-dressing', threshold);
    }

    const proofPost = { x: 10.0, y: 5.8, w: 0.42, h: 0.44 };
    if (mapName === 'Imperial Docks') {
      const shadow = scene.add.image(proofPost.x * TILE + 16, proofPost.y * TILE + 30, 'af-scaffold-shadow')
        .setDepth(195)
        .setOrigin(0.5);
      const post = scene.add.image(proofPost.x * TILE + 16, proofPost.y * TILE + 31, 'af-scaffold-post')
        .setOrigin(0.5, 1)
        .setDepth(90 + proofPost.y * 20 + 10);
      register(scene, 'local-shadows', shadow);
      register(scene, 'props-front-occluders', post);
    }

    scene.afCollisionRects = [...(map.blocked || []).map((r) => ({ ...r }))];
    if (mapName === 'Imperial Docks') scene.afCollisionRects.push(proofPost);

    for (const rect of scene.afCollisionRects) {
      const collision = scene.add.rectangle(
        rect.x * TILE,
        rect.y * TILE,
        rect.w * TILE,
        rect.h * TILE,
        0xff0000,
        0
      ).setOrigin(0).setVisible(false);
      collision.setData('collisionOnly', true);
      register(scene, 'collision', collision);
    }

    const label = scene.add.text(VIEW_W - 6, VIEW_H - 5, 'TECHNICAL WORLD-REFACTOR SCAFFOLD · NOT ART REVIEW', {
      fontFamily: 'monospace', fontSize: '7px', color: '#b7ab94', backgroundColor: '#111418cc', padding: { x: 4, y: 2 }
    }).setOrigin(1, 1).setDepth(900);
    register(scene, 'atmosphere-fx', label);
  }

  function install(win) {
    if (win.AF_WORLD_REFACTOR_V0?.installed) return;
    const game = win.AF_GAME;
    const test = win.AF_TEST;
    if (!game || !test?.MAPS) return false;

    let scene;
    try { scene = game.scene.getScene('World'); } catch (_) { return false; }
    if (!scene) return false;

    const original = {
      create: scene.create,
      clearWorld: scene.clearWorld,
      loadMap: scene.loadMap,
      update: scene.update
    };

    scene.clearWorld = function afClearWorld() {
      destroyRefactorObjects(this);
      return original.clearWorld.call(this);
    };

    scene.loadMap = function afLoadMap(name, keepPosition = false) {
      const result = original.loadMap.call(this, name, keepPosition);
      addTechnicalScaffold(this, win, name);
      return result;
    };

    scene.create = function afCreate() {
      const result = original.create.call(this);
      this.afContinuousMovement = true;
      return result;
    };

    scene.update = function afContinuousUpdate(time, delta) {
      if (this.pausedByUi) return original.update.call(this, time, delta);

      const s = test.getState();
      const map = test.MAPS[s.map] || test.MAPS['Imperial Docks'];
      const mv = this.readMove();
      let dx = Number(mv.dx || 0);
      let dy = Number(mv.dy || 0);
      const moving = !!(dx || dy);

      if (moving) {
        const len = Math.hypot(dx, dy) || 1;
        dx /= len;
        dy /= len;
        const distanceGrid = (MOVE_SPEED_PPS * Math.min(delta, 50) / 1000) / TILE;
        const stepX = dx * distanceGrid;
        const stepY = dy * distanceGrid;

        let nextX = s.x;
        let nextY = s.y;
        if (!blockedAt(this, map, nextX + stepX, nextY)) nextX += stepX;
        if (!blockedAt(this, map, nextX, nextY + stepY)) nextY += stepY;

        s.x = nextX;
        s.y = nextY;
        s.facing = facingFor(dx, dy, s.facing);
        s.tutorialFlags ||= {};
        s.tutorialFlags.moved = true;
        test.setState(s);
      }

      this.isMoving = moving;
      this.lastStep = time; // suppress legacy fixed-step movement while retaining the rest of the proven update loop
      return original.update.call(this, time, delta);
    };

    const audit = () => {
      const current = game.scene.getScene('World');
      const hiddenGridObjects = (current?.layers || []).filter((obj) => obj?.depth === -8 && obj?.visible !== false);
      const layerCounts = Object.fromEntries(LAYER_ORDER.map((name) => [name, current?.afLayerObjects?.[name]?.length || 0]));
      return {
        installed: true,
        productionArt: false,
        scaffoldOnly: true,
        continuousMovement: true,
        movementPixelsPerSecond: MOVE_SPEED_PPS,
        normalizedDiagonals: true,
        hiddenGrid: hiddenGridObjects.length === 0,
        collisionIndependentFromAppearance: (current?.afCollisionRects?.length || 0) > 0,
        separateRuntimeTextures: ['af-scaffold-ground', 'af-scaffold-wall', 'af-scaffold-foundation', 'af-scaffold-threshold', 'af-scaffold-post'].filter((key) => current?.textures?.exists(key)),
        layerOrder: [...LAYER_ORDER],
        layerCounts,
        occlusionProofObject: (current?.afLayerObjects?.['props-front-occluders']?.length || 0) > 0,
        legacyBakedBackgroundVisible: (current?.layers || []).some((obj) => obj?.depth === -20 && obj?.visible !== false),
        note: 'Technical scaffold only. Replace scaffold textures with approved Slice 0 runtime assets before art review.'
      };
    };

    win.AF_WORLD_REFACTOR_V0 = { installed: true, version: '0.1.0', audit };
    test.worldRefactor = audit;

    if (game.scene.isActive('World')) {
      const state = test.getState();
      scene.loadMap(state.map, true);
    }

    console.info('Astro Fighters Phaser World Refactor v0 installed', audit());
    return true;
  }

  function boot() {
    const win = frame.contentWindow;
    if (!win) return;
    let attempts = 0;
    const timer = setInterval(() => {
      attempts += 1;
      if (install(win) || attempts > 200) clearInterval(timer);
    }, 50);
  }

  frame.addEventListener('load', boot);
  if (frame.contentDocument?.readyState === 'complete') boot();
})();
