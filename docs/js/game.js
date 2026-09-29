/* Astro Fighters — Phaser world runtime.
   Open-world, real-time action RPG playtest. Requires, in order:
   Phaser, canonical-roster.js, astro-natal.js, world/scaffold-textures.js, world/maps.js. */
(() => {
  'use strict';

  const BUILD = 'phaser-world-refactor-v0';
  const SAVE_KEY = 'astroFighters.phaserSlice.v1';
  const TILE = 32;                 // hidden logic grid; never drawn
  const VIEW_W = 640, VIEW_H = 360;
  const SLOT_MS = 1800;            // one legacy "round"; used to convert round-based durations to real time
  const RECOVERY_MS_PER_SLOT = 520;// real-time action recovery per legacy action slot
  const PLAYER_SPEED = 112;        // px/s
  const DASH_SPEED = 330, DASH_MS = 190, DODGE_IFRAME_MS = 300, DODGE_COST = 10;
  const ENEMY_SPEED = 72, AGGRO_RANGE = 170, DEAGGRO_RANGE = 280;
  const ENEMY_REACH = 24, ENEMY_WINDUP_MS = 460, ENEMY_RECOVER_MS = 760;
  const SCALE = window.AF_SCALE;   // player-relative scale authority (world/scale-guide.js)
  const INTERACT_RANGE = SCALE.player.interactionRange;
  // Actor foot collision box, authored independently of the 64×64 sprite frame.
  const FOOT_HW = SCALE.player.collision.w/2, FOOT_H = SCALE.player.collision.h;
  const DIRS = [
    {name:'N',dx:0,dy:-1},{name:'NE',dx:1,dy:-1},{name:'E',dx:1,dy:0},{name:'SE',dx:1,dy:1},
    {name:'S',dx:0,dy:1},{name:'SW',dx:-1,dy:1},{name:'W',dx:-1,dy:0},{name:'NW',dx:-1,dy:-1}
  ];
  const ANGLE_DIRS = ['E','SE','S','SW','W','NW','N','NE'];
  const TRAP_CHOICES = ['Explosive Tag','Flash Bomb','Spike Pit','Smoke Screen','Caltrops'];
  const POST_ACADEMY_HOTBAR = ['Iron Mountain Strike','Chakra Bullet','Charge Chakra','Catch Breath','Recompose','Guardian Barrier'];
  const BASIC_JAB = {id:'foundation-basic-jab',name:'Basic Jab',description:'Foundation straight punch.',dmgType:'Physical',power:6,slots:1,stam:4,chakra:0,range:1.45,source:'Foundation',section:'Foundation'};
  const DEPTH = {ground:-3000, decals:-2900, dressingFlat:-2350, trap:-2300, shadow:-2400, collision:15000, fx:20000, label:21000, float:22000};

  const {MAPS, LOOKS} = window.AF_WORLD;
  const AUTHORED_MODULES = window.AF_WORLD.authoredModules || {};

  const $ = id => document.getElementById(id);
  const overlays = ['title-overlay','birth-overlay','chart-overlay','appearance-overlay','dialog-overlay','trap-overlay','field-menu'];
  const clamp = (v,a,b)=>Math.max(a,Math.min(b,v));
  const deepClone = obj => JSON.parse(JSON.stringify(obj));
  const now = ()=>performance.now();
  const dist = (a,b)=>Math.hypot(a.x-b.x,a.y-b.y);

  function hideAllOverlays(){ for(const id of overlays) $(id).classList.add('hidden'); }
  function showOverlay(id){ hideAllOverlays(); $(id).classList.remove('hidden'); }
  function toast(msg, ms=1800){ const t=$('toast'); t.textContent=msg; t.classList.remove('hidden'); clearTimeout(toast._timer); toast._timer=setTimeout(()=>t.classList.add('hidden'),ms); }
  function pct(v,max){ return max<=0?0:clamp((v/max)*100,0,100); }
  function safeText(s){ return String(s??'').replace(/[<>&]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;'}[c])); }
  function isOpen(id){ return !$(id).classList.contains('hidden'); }

  function dirFromVector(vx,vy){ return ANGLE_DIRS[(Math.round(Math.atan2(vy,vx)/(Math.PI/4))+8)%8]; }
  function dirVector(name){ const d=DIRS.find(v=>v.name===name)||DIRS[4]; const l=Math.hypot(d.dx,d.dy); return {x:d.dx/l,y:d.dy/l}; }

  function abilityRecords(){ return (typeof CANONICAL_ABILITY_RECORDS !== 'undefined' && Array.isArray(CANONICAL_ABILITY_RECORDS)) ? CANONICAL_ABILITY_RECORDS : []; }
  function abilityByName(name){
    const aliases = {
      'Iron Mountain Strike':['Iron Mountain Strike','Iron Mountain'],
      'Shadow Cloak':['Shadow Cloak','Gloom Shroud'],
      'Basic Jab':['Basic Jab']
    };
    if(name==='Basic Jab') return BASIC_JAB;
    const opts=aliases[name]||[name];
    return abilityRecords().find(a=>opts.some(n=>String(a.name||'').trim()===n)) || null;
  }
  function runtimeCost(a,key,state){
    if(!a) return 0;
    const maxKey=key==='stam'?'maxStamina':'maxChakra';
    const pctKey=key==='stam'?'costStamPct':'costChakraPct';
    if(Number.isFinite(a[pctKey])) return Math.ceil(state.stats[maxKey]*a[pctKey]);
    const v=a[key];
    return Number.isFinite(v)?v:0;
  }
  function recoveryMs(a){ return Math.max(1,Number(a?.slots)||1)*RECOVERY_MS_PER_SLOT; }
  function cleanAbilityName(a){ return String(a?.name||'Unknown').trim(); }

  const DEFAULT_STATE = {
    build:BUILD, created:false, academyComplete:false, academyRewardGranted:false,
    level:1, xp:0, xpDebt:0, gold:0, map:'Imperial Docks', x:MAPS['Imperial Docks'].spawn.x, y:MAPS['Imperial Docks'].spawn.y, posUnits:'px', facing:'N',
    name:'Fighter', appearance:{sex:'male',skin:'tone2',hair:'afro',eyes:'brown',outfit:'gi'}, wardrobe:['gi'],
    birth:null, chart:null,
    stats:{maxHp:100,hp:100,maxStamina:100,stamina:100,maxChakra:100,chakra:100,maxPoise:100,poise:100},
    attributes:{STR:10,AGI:10,FORT:10,INT:10,CHA:10},
    learned:['Basic Jab'], hotbar:['Basic Jab'], trapStock:{}, armedTrap:null, inventory:[], equipment:{Gi:{name:'Gi',durability:100,maxDurability:100}},
    questState:{academy_intro:{state:'active'}}, targetId:null, nextActionAt:0, guard:false, dodgeUntil:0,
    kills:{}, corpses:[], tutorialFlags:{moved:false,targeted:false,jabbed:false,guarded:false,dodged:false,menu:false}
  };

  let state = deepClone(DEFAULT_STATE);
  let pendingChart = null;
  let worldScene = null;
  let currentDialogClose = null;
  let memorySave = null;
  function storageGet(){
    try{return localStorage.getItem(SAVE_KEY);}catch(e){return memorySave;}
  }
  function storageSet(value){
    memorySave=value;
    try{localStorage.setItem(SAVE_KEY,value);return true;}catch(e){return false;}
  }

  function normalizeState(s){
    const out = Object.assign(deepClone(DEFAULT_STATE), s||{});
    out.stats = Object.assign({}, DEFAULT_STATE.stats, s?.stats||{});
    out.attributes = Object.assign({}, DEFAULT_STATE.attributes, s?.attributes||{});
    // Legacy 48×64 paper-doll saves carry no `sex`; they migrate to the default approved look.
    out.appearance = sanitizeLook(s?.appearance);
    out.wardrobe = [...new Set([CHARS.starterOutfit,...(Array.isArray(s?.wardrobe)?s.wardrobe:[])])].filter(id=>OUTFITS[id]);
    if(!out.wardrobe.includes(out.appearance.outfit)) out.appearance.outfit=CHARS.starterOutfit;
    out.equipment = Object.assign({}, s?.equipment||{}); delete out.equipment.trainingJacket;
    for(const id of out.wardrobe){ const n=OUTFITS[id].name; out.equipment[n] ||= {name:n,durability:100,maxDurability:100}; }
    if(!MAPS[out.map]) out.map='Imperial Docks';
    // Migrate tile-step saves (integer grid cells) to world-pixel positions.
    if(out.posUnits!=='px' || !Number.isFinite(out.x) || !Number.isFinite(out.y)){
      const sp=MAPS[out.map].spawn; out.x=sp.x; out.y=sp.y; out.posUnits='px';
    }
    for(const c of (s?.corpses||[])) if(c && c.posUnits!=='px'){ c.x=(c.x||0)*TILE+16; c.y=(c.y||0)*TILE+28; c.posUnits='px'; }
    out.trapStock = Object.assign({}, s?.trapStock||{});
    out.questState = Object.assign({}, DEFAULT_STATE.questState, s?.questState||{});
    out.tutorialFlags = Object.assign({}, DEFAULT_STATE.tutorialFlags, s?.tutorialFlags||{});
    out.learned = Array.isArray(s?.learned)?s.learned:['Basic Jab'];
    out.hotbar = Array.isArray(s?.hotbar)?s.hotbar:['Basic Jab'];
    out.corpses = Array.isArray(s?.corpses)?s.corpses:[];
    out.nextActionAt = 0; out.dodgeUntil = 0; out.guard = false;
    return out;
  }
  function saveGame(silent=false){
    state.build=BUILD;
    storageSet(JSON.stringify(state));
    if(!silent) toast('Game saved.');
    updateContinueButton();
  }
  function loadGame(){
    try{ const raw=storageGet(); if(!raw) return false; state=normalizeState(JSON.parse(raw)); return !!state.created; }
    catch(e){ console.warn('Save load failed',e); return false; }
  }
  function updateContinueButton(){ $('continue-btn').disabled=!storageGet(); }

  function makeTestChart(){
    const utc=AF_ASTRO.zonedLocalToUtc('1994-07-21','18:42','America/New_York');
    return AF_ASTRO.buildChart(utc,40.7128,-74.006,{placeName:'New York, NY, USA',timeZone:'America/New_York'});
  }
  function quickState(opts={}){
    state=normalizeState(DEFAULT_STATE);
    state.created=true; state.name='Akio'; state.birth={date:'1994-07-21',time:'18:42',place:'New York, NY, USA',lat:40.7128,lon:-74.006,tz:'America/New_York'}; state.chart=makeTestChart();
    if(opts.academy){ grantAcademyKit(['Explosive Tag','Flash Bomb','Spike Pit'], true); }
    if(opts.map){ state.map=opts.map; const sp=MAPS[opts.map]?.spawn||MAPS['Imperial Docks'].spawn; state.x=sp.x; state.y=sp.y; }
    return state;
  }

  function chartRows(chart){
    if(!chart) return [];
    const rows=[['Ascendant',chart.Ascendant],['Sun',chart.planets?.Sun],['Moon',chart.planets?.Moon]];
    for(const p of ['Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']) rows.push([p,chart.planets?.[p]]);
    rows.push(['North Node',chart.NorthNode]);
    return rows.filter(r=>r[1]);
  }

  function progressionLevelForPlacement(key){
    const map={Ascendant:10,Moon:15,Sun:20,Venus:25,Mercury:30,Mars:35,Jupiter:45,Saturn:60,Uranus:75,Neptune:90,Pluto:90,'North Node':100};
    return map[key]||1;
  }
  function accessForAbility(a){
    if(!a) return {ok:false,reason:'Missing ability record'};
    const name=cleanAbilityName(a);
    if(name==='Basic Jab') return {ok:true,reason:'Foundation technique'};
    const source=String(a.source||'').trim();
    const section=String(a.section||'');
    if(source==='General' || source==='Neutral' || ['Yang','Yin'].includes(source) || section==='Universal Arts'){
      if(source==='Trap' || String(a.discipline||'')==='Trap') return state.academyComplete?{ok:true}:{ok:false,reason:'Complete the Astro Fighter Academy tutorial'};
      if(['Medical','Summon','Genjutsu'].includes(source)) return {ok:false,reason:'Requires specialist training'};
      return state.academyComplete?{ok:true}:{ok:false,reason:'Complete the Astro Fighter Academy tutorial'};
    }
    if(source==='Trap' || String(a.discipline||'')==='Trap') return state.academyComplete?{ok:true}:{ok:false,reason:'Complete the Astro Fighter Academy tutorial'};
    if(section.includes('Martial') || /weapon kit|trained/i.test(String(a.access||''))) return {ok:false,reason:'Requires trained/equipped martial or weapon kit'};
    if(section.includes('Sign')) return {ok:false,reason:'Natal sign technique has not awakened at this level'};
    return {ok:false,reason:String(a.access||'Locked by progression')};
  }

  function gainXp(amount){
    let n=amount;
    if(state.xpDebt>0){ const pay=Math.min(state.xpDebt,n); state.xpDebt-=pay; n-=pay; }
    state.xp+=n;
    while(state.xp>=state.level*100){
      state.xp-=state.level*100; state.level++;
      state.stats.maxHp+=10; state.stats.maxStamina+=5; state.stats.maxChakra+=5;
      state.stats.hp=state.stats.maxHp; state.stats.stamina=state.stats.maxStamina; state.stats.chakra=state.stats.maxChakra;
      toast(`Level ${state.level} · HP/Stamina/Chakra increased`,2600);
    }
  }

  /* ---------------- Paper-doll characters (approved 512×64 sheets) ---------------- */

  // Layers come from the committed /Paperdolls sheets via world/characters.js. Each sheet is
  // eight 64×64 directional frames; one frame per direction, no invented animation frames.
  const CHARS = window.AF_CHARACTERS;
  const frameFor = facing => Math.max(0, CHARS.frameOrder.indexOf(facing));
  const COMPASS = ['N','NE','E','SE','S','SW','W','NW'];
  let FOOT_Y = 63; // lowest opaque row of the south body frame, measured at runtime
  // Outfit catalogue. Defense is the share of incoming damage absorbed (placeholder balance).
  const OUTFITS = {
    gi:{name:'Gi',price:0,defense:0,description:'Standard Academy training gi. Starter outfit.'},
    'red-armor':{name:'Red Armor',price:80,defense:.15,description:'Lacquered red plate over a fighter wrap, with shoulder guards. Absorbs 15% of incoming damage.'},
    'blue-armor':{name:'Blue Armor',price:80,defense:.15,description:'Blue plate over a fighter wrap, with shoulder guards. Absorbs 15% of incoming damage.'}
  };
  const DEFAULT_LOOK = {sex:'male',skin:'tone2',hair:'afro',eyes:'brown',outfit:CHARS.starterOutfit};
  function sanitizeLook(a){
    const sex=CHARS.sexes[a?.sex]?a.sex:'male', d=CHARS.sexes[sex];
    const pick=(k,v)=>d[k][v]?v:Object.keys(d[k])[0];
    return {sex,skin:pick('skin',a?.skin),hair:pick('hair',a?.hair),eyes:pick('eyes',a?.eyes),outfit:d.outfits[a?.outfit]?a.outfit:CHARS.starterOutfit};
  }
  const outfitFits=(sex,id)=>!!CHARS.sexes[sex]?.outfits?.[id];
  const layerKey=(sex,slot,id)=>`pd-${sex}-${slot}-${id}`;
  const assetPath=path=>(window.AF_ASSET_DATA&&window.AF_ASSET_DATA[path])||path;
  /* Ordered layers for a look, following CHARS.drawOrder: body → clothing → arms → shoulders → hair → eyes. */
  function lookLayers(look){
    const L=sanitizeLook(look), d=CHARS.sexes[L.sex], o=d.outfits[L.outfit];
    const bySlot={body:[L.skin,d.skin[L.skin].body],clothing:[L.outfit,o.clothing],arms:[L.skin,d.skin[L.skin].arms],shoulders:[L.outfit,o.shoulders],hair:[L.hair,d.hair[L.hair].layer],eyes:[L.eyes,d.eyes[L.eyes].layer]};
    return CHARS.drawOrder.filter(slot=>bySlot[slot][1]).map(slot=>({slot,key:layerKey(L.sex,slot,bySlot[slot][0]),path:bySlot[slot][1].path}));
  }
  function allLayerRefs(){
    const refs=[];
    for(const [sex,d] of Object.entries(CHARS.sexes)){
      for(const [id,sk] of Object.entries(d.skin)) refs.push([layerKey(sex,'body',id),sk.body.path],[layerKey(sex,'arms',id),sk.arms.path]);
      for(const k of ['hair','eyes']) for(const [id,o] of Object.entries(d[k])) refs.push([layerKey(sex,k,id),o.layer.path]);
      for(const [id,o] of Object.entries(d.outfits)){ refs.push([layerKey(sex,'clothing',id),o.clothing.path]); if(o.shoulders) refs.push([layerKey(sex,'shoulders',id),o.shoulders.path]); }
    }
    return refs;
  }

  /* ---- character creator preview (mechanical layer composite, integer 4× nearest-neighbour) ---- */
  function readCreatorAppearance(){ return sanitizeLook({sex:$('sex-opt')?.value,skin:$('skin-opt')?.value,hair:$('hair-opt')?.value,eyes:$('eyes-opt')?.value,outfit:CHARS.starterOutfit}); }
  function fillCreatorOptions(){
    const d=CHARS.sexes[$('sex-opt').value]||CHARS.sexes.male;
    for(const [id,k] of [['skin-opt','skin'],['hair-opt','hair'],['eyes-opt','eyes']]){
      const sel=$(id), prev=sel.value;
      sel.innerHTML=Object.entries(d[k]).map(([v,o])=>`<option value="${v}">${safeText(o.label)}</option>`).join('');
      if(d[k][prev]) sel.value=prev;
    }
  }
  const domImages=new Map();
  function loadDomImage(path){
    if(!domImages.has(path)) domImages.set(path,new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=()=>rej(new Error(`Paper-doll layer failed: ${path}`));i.src=assetPath(path);}));
    return domImages.get(path);
  }
  let creatorFacing='S', creatorToken=0;
  async function drawPaperDollPreview(){
    const canvas=$('paperdoll-preview'); if(!canvas||$('appearance-overlay').classList.contains('hidden')) return;
    const token=++creatorToken, imgs=[];
    for(const l of lookLayers(readCreatorAppearance())){ try{imgs.push(await loadDomImage(l.path));}catch(e){console.warn(e);} }
    if(token!==creatorToken) return;
    const g=canvas.getContext('2d'); g.imageSmoothingEnabled=false;
    const grad=g.createLinearGradient(0,0,0,canvas.height);grad.addColorStop(0,'#263a42');grad.addColorStop(.78,'#1a2023');grad.addColorStop(.785,'#5e5643');grad.addColorStop(1,'#342d25');g.fillStyle=grad;g.fillRect(0,0,canvas.width,canvas.height);
    const f=frameFor(creatorFacing);
    for(const im of imgs) g.drawImage(im,f*64,0,64,64,0,0,canvas.width,canvas.height);
    $('preview-facing').textContent=creatorFacing;
  }
  function startCreatorPreview(){ if(!$('skin-opt').options.length) fillCreatorOptions(); drawPaperDollPreview(); }
  function bindCreatorPreview(){
    $('sex-opt')?.addEventListener('input',()=>{fillCreatorOptions();drawPaperDollPreview();});
    for(const id of ['skin-opt','hair-opt','eyes-opt']) $(id)?.addEventListener('input',()=>drawPaperDollPreview());
    $('preview-left')?.addEventListener('click',()=>{creatorFacing=COMPASS[(COMPASS.indexOf(creatorFacing)+7)%8];drawPaperDollPreview();});
    $('preview-right')?.addEventListener('click',()=>{creatorFacing=COMPASS[(COMPASS.indexOf(creatorFacing)+1)%8];drawPaperDollPreview();});
  }

  /* A layered actor. Container position is the foot-contact point; the sprite frame is 64×64. */
  class PaperDoll {
    constructor(scene, look, x, y){ this.scene=scene; this.container=scene.add.container(x,y); this.sprites=[]; this.sig=''; this.frame=frameFor('S'); this.apply(look); this.place(x,y); }
    apply(look){
      const layers=lookLayers(look), sig=layers.map(l=>l.key).join('|');
      if(sig===this.sig) return; this.sig=sig; this.look=sanitizeLook(look);
      for(const e of this.sprites) e.sprite.destroy();
      this.sprites=layers.filter(l=>this.scene.textures.exists(l.key)).map(l=>{
        const sp=this.scene.add.sprite(0,0,l.key,this.frame).setOrigin(SCALE.player.pivotX/64,(FOOT_Y+1)/64);
        this.container.add(sp); return {def:{slot:l.slot},sprite:sp,variant:l.key};
      });
    }
    pose(facing){ this.frame=frameFor(facing); for(const e of this.sprites) e.sprite.setFrame(this.frame); }
    place(x,y){ this.container.setPosition(Math.round(x),Math.round(y)); this.container.setDepth(y); }
    destroy(){ this.container.destroy(); }
  }
  const makePlayerDoll=(scene,x,y)=>new PaperDoll(scene,state.appearance,x,y);

  /* ---- wardrobe: owned outfits persist through death; carried inventory does not ---- */
  function ownsOutfit(id){ return (state.wardrobe||[]).includes(id); }
  function equipOutfit(id){
    if(!ownsOutfit(id)){ toast('You do not own that outfit.'); return false; }
    if(!outfitFits(state.appearance.sex,id)){ toast(`${OUTFITS[id]?.name||id} is not fitted for this frame yet.`); return false; }
    state.appearance.outfit=id; worldScene?.player?.doll.apply(state.appearance); saveGame(true); toast(`Equipped ${OUTFITS[id].name}.`,1200); return true;
  }
  function buyOutfit(id){
    const o=OUTFITS[id]; if(!o) return false;
    if(ownsOutfit(id)){ toast('Already owned.'); return false; }
    if(!outfitFits(state.appearance.sex,id)){ toast(`${o.name} is not fitted for this frame yet.`); return false; }
    if(state.gold<o.price){ toast(`Not enough mon. ${o.name} costs ${o.price}.`); return false; }
    state.gold-=o.price; state.wardrobe.push(id); state.equipment[o.name]={name:o.name,durability:100,maxDurability:100};
    saveGame(true); toast(`Bought ${o.name} · −${o.price} mon`,1600); return true;
  }
  function sellOutfit(id){
    const o=OUTFITS[id]; if(!o||!ownsOutfit(id)||id===CHARS.starterOutfit) return false;
    if(state.appearance.outfit===id){ state.appearance.outfit=CHARS.starterOutfit; worldScene?.player?.doll.apply(state.appearance); }
    const price=Math.floor(o.price/2); state.gold+=price; state.wardrobe=state.wardrobe.filter(x=>x!==id); delete state.equipment[o.name];
    saveGame(true); toast(`Sold ${o.name} · +${price} mon`,1600); return true;
  }
  function openShop(merchant){
    const render=()=>{
      const rows=(merchant.stock||[]).map(id=>{
        const o=OUTFITS[id], owned=ownsOutfit(id), fits=outfitFits(state.appearance.sex,id), worn=state.appearance.outfit===id;
        const btns=!fits?'<span class="shop-note">Not yet fitted for the female frame</span>'
          :owned?`${worn?'<span class="shop-note">Equipped</span>':`<button data-shop="equip" data-id="${id}">Equip</button>`}<button data-shop="sell" data-id="${id}">Sell ${Math.floor(o.price/2)}</button>`
          :`<button data-shop="buy" data-id="${id}" class="primary"${state.gold<o.price?' disabled':''}>Buy ${o.price}</button>`;
        return `<div class="shop-row"><div><b>${safeText(o.name)}</b><small>${safeText(o.description)}</small></div><div class="shop-actions">${btns}</div></div>`;
      }).join('');
      showDialog(merchant.name,`<div class="shop-purse">Your purse: <b>${state.gold} mon</b></div>${rows}`,[{label:'Leave shop'}]);
      document.querySelectorAll('#dialog-text [data-shop]').forEach(b=>b.addEventListener('click',()=>{
        const id=b.dataset.id; if(b.dataset.shop==='buy') buyOutfit(id); else if(b.dataset.shop==='sell') sellOutfit(id); else equipOutfit(id);
        updateHud(true); render();
      }));
    };
    render();
  }

  /* ---------------- Dialogue, tutorial, Academy kit ---------------- */

  function showDialog(speaker,text,buttons=[{label:'Continue'}]){
    $('dialog-speaker').textContent=speaker;
    $('dialog-text').innerHTML=text;
    const wrap=$('dialog-actions'); wrap.innerHTML='';
    $('dialog-overlay').classList.remove('hidden');
    worldScene?.setPaused(true);
    buttons.forEach((b)=>{
      const btn=document.createElement('button'); btn.textContent=b.label||'Continue'; if(b.primary!==false) btn.classList.add('primary');
      btn.addEventListener('click',()=>{ if(b.onClick) b.onClick(); else closeDialog(); }); wrap.appendChild(btn);
    });
  }
  function closeDialog(){ $('dialog-overlay').classList.add('hidden'); worldScene?.setPaused(false); if(currentDialogClose){const fn=currentDialogClose;currentDialogClose=null;fn();} }
  function showLines(speaker,lines){
    let i=0;
    const next=()=>{ if(i>=lines.length){closeDialog();return;} const last=i===lines.length-1; showDialog(speaker,lines[i++],[{label:last?'Close':'Continue',onClick:next}]); };
    next();
  }

  function startSenseiTutorial(){
    const lines=[
      ['Sensei Daichi','Every Astro Fighter survives by reading four resources: <b>HP</b> keeps you standing, <b>Stamina</b> fuels physical technique, <b>Chakra</b> fuels ninjutsu, and <b>Poise</b> is your resistance to being staggered.'],
      ['Sensei Daichi','Move freely with <b>WASD</b> or the arrows. <b>Tab</b> cycles a target. Hold <b>Shift</b> to guard. <b>Space</b> dashes in the direction you are moving and grants a brief invulnerability window.'],
      ['Sensei Daichi','Every technique commits you. A 1-slot technique leaves you in recovery for about half a second; 2 slots for a full second. Read your opponent\'s wind-up, guard or dash through it, then punish the recovery.'],
      ['Sensei Daichi','Focus actions keep you functional. <b>Charge Chakra</b> restores Chakra, <b>Catch Breath</b> restores Stamina, and <b>Recompose</b> spends 10% max Stamina plus 10% max Chakra to restore 20% max Poise.'],
      ['Sensei Daichi','Your birth chart determines which sign arts can awaken later. At level 1, you have only the foundation strike until this Academy certifies your General and Trap curriculum. Test your jab on the sparring student if you wish.']
    ];
    let i=0;
    const next=()=>{
      if(i>=lines.length){ closeDialog(); openTrapSelection(); return; }
      const [sp,tx]=lines[i++]; showDialog(sp,tx,[{label:i===lines.length?'Choose Academy Supplies':'Continue',onClick:()=>{ $('dialog-overlay').classList.add('hidden'); next(); }}]);
    };
    next();
  }

  function openTrapSelection(){
    const box=$('trap-choices'); box.innerHTML='';
    for(const name of TRAP_CHOICES){
      const a=abilityByName(name); const row=document.createElement('label'); row.className='trap-choice';
      row.innerHTML=`<input type="checkbox" value="${safeText(name)}"><div><b>${safeText(name)}</b><div>${safeText(a?.description||a?.statusText||'Supply-consuming trap')}</div></div>`;
      box.appendChild(row);
    }
    const update=()=>{ const checked=[...box.querySelectorAll('input:checked')]; $('trap-count').textContent=`${checked.length} / 3 selected`; $('trap-confirm').disabled=checked.length!==3; [...box.querySelectorAll('input:not(:checked)')].forEach(i=>i.disabled=checked.length>=3); };
    box.querySelectorAll('input').forEach(i=>i.addEventListener('change',update)); update();
    $('trap-confirm').onclick=()=>{ const selected=[...box.querySelectorAll('input:checked')].map(i=>i.value); grantAcademyKit(selected,false); $('trap-overlay').classList.add('hidden'); worldScene?.setPaused(false); showDialog('Sensei Daichi','Foundation certification complete. I have issued <b>100 mon</b>, a <b>Trap Pouch</b>, and ten supplies for each of your three selections. General and Trap arts are now unlocked — <b>Q</b> arms a trap type, <b>F</b> sets it at your feet. The Fringe Ward is open when you are ready to test yourself.',[{label:'Return to the floor',onClick:()=>{closeDialog(); worldScene?.refreshFromState();}}]); };
    hideAllOverlays(); $('trap-overlay').classList.remove('hidden'); worldScene?.setPaused(true);
  }

  function grantAcademyKit(selected, silent=false){
    if(state.academyRewardGranted) return false;
    const unique=[...new Set((selected||[]).filter(n=>TRAP_CHOICES.includes(n)))].slice(0,3);
    if(unique.length!==3) return false;
    state.academyComplete=true; state.academyRewardGranted=true; state.gold+=100;
    if(!state.inventory.some(i=>i.name==='Trap Pouch')) state.inventory.push({name:'Trap Pouch',qty:1,type:'key'});
    for(const n of unique) state.trapStock[n]=10;
    state.armedTrap=unique[0];
    state.learned=[...new Set(['Basic Jab',...state.learned,...abilityRecords().filter(a=>{
      const src=String(a.source||'').trim(),disc=String(a.discipline||'').trim();
      return (String(a.section||'')==='Universal Arts' && !['Medical','Summon','Genjutsu'].includes(src)) || src==='General' || src==='Neutral' || ['Yang','Yin','Trap'].includes(src) || disc==='Trap';
    }).map(cleanAbilityName)])];
    state.hotbar=POST_ACADEMY_HOTBAR.slice();
    state.questState.academy_intro={state:'completed'};
    saveGame(true);
    if(!silent) toast('Academy certified · +100 mon · General + Trap unlocked',2600);
    return true;
  }

  /* ---------------- Field menu and HUD ---------------- */

  function showFieldMenu(tab='status'){
    if(!state.created) return;
    state.tutorialFlags.menu=true; worldScene?.setPaused(true); hideAllOverlays(); $('field-menu').classList.remove('hidden'); renderFieldTab(tab);
  }
  function closeFieldMenu(){ $('field-menu').classList.add('hidden'); worldScene?.setPaused(false); }
  function renderFieldTab(tab){
    document.querySelectorAll('#field-menu [data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab));
    const c=$('field-content');
    if(tab==='status'){
      c.innerHTML=`<span class="eyebrow">REGISTERED FIGHTER</span><h1>${safeText(state.name)} · Lv ${state.level}</h1><div class="stat-grid">
      <div class="stat-card"><small>HP</small><b>${Math.round(state.stats.hp)}/${state.stats.maxHp}</b></div><div class="stat-card"><small>STAMINA</small><b>${Math.round(state.stats.stamina)}/${state.stats.maxStamina}</b></div><div class="stat-card"><small>CHAKRA</small><b>${Math.round(state.stats.chakra)}/${state.stats.maxChakra}</b></div><div class="stat-card"><small>POISE</small><b>${Math.round(state.stats.poise)}/${state.stats.maxPoise}</b></div><div class="stat-card"><small>MON</small><b>${state.gold}</b></div><div class="stat-card"><small>XP</small><b>${state.xp}/${state.level*100}</b></div><div class="stat-card"><small>XP DEBT</small><b>${state.xpDebt}</b></div><div class="stat-card"><small>KILLS</small><b>${Object.values(state.kills).reduce((a,b)=>a+b,0)}</b></div></div><p>${state.academyComplete?'Academy certified. General and Trap curriculum active.':'Academy certification pending. Only Basic Jab is battle-ready.'}</p>`;
    } else if(tab==='abilities'){
      const records=[BASIC_JAB,...abilityRecords()];
      c.innerHTML=`<span class="eyebrow">ABILITY LIBRARY</span><h1>${records.length} records</h1><p>Loaded from the canonical runtime roster. Locked records remain visible with their gate reason.</p>` + records.map(a=>{const ac=accessForAbility(a),st=runtimeCost(a,'stam',state),ch=runtimeCost(a,'chakra',state);return `<div class="ability-row ${ac.ok?'':'locked'}"><b>${safeText(cleanAbilityName(a))}</b><span class="cost">${st?`STA ${st} `:''}${ch?`CHK ${ch} `:''}${a.slots?`${a.slots} slot`:''}</span><span class="reason">${safeText(ac.ok?(a.statusText||a.description||'Ready'):ac.reason)}</span></div>`;}).join('');
    } else if(tab==='inventory'){
      const items=[...state.inventory.map(i=>`${i.name} ×${i.qty||1}`),...Object.entries(state.trapStock).filter(([,q])=>q>0).map(([n,q])=>`${n} supplies ×${q}`)];
      c.innerHTML=`<span class="eyebrow">CARRIED INVENTORY</span><h1>Inventory</h1>${items.length?items.map(x=>`<div class="inv-row">${safeText(x)}</div>`).join(''):'<p>No carried items.</p>'}<h2>Wardrobe</h2>${state.wardrobe.map(id=>{const o=OUTFITS[id],worn=state.appearance.outfit===id,fits=outfitFits(state.appearance.sex,id),eq=state.equipment[o.name];return `<div class="inv-row wardrobe-row"><span><b>${safeText(o.name)}</b>${eq?` · durability ${eq.durability}/${eq.maxDurability}`:''}${o.defense?` · absorbs ${Math.round(o.defense*100)}%`:''}</span>${worn?'<span class="shop-note">Equipped</span>':fits?`<button data-equip="${id}">Equip</button>`:'<span class="shop-note">Not fitted for this frame</span>'}</div>`;}).join('')}<p class="note">Owned outfits stay with you when you fall; carried items and trap stock stay on your corpse.</p>`;
      c.querySelectorAll('[data-equip]').forEach(btn=>btn.addEventListener('click',()=>{equipOutfit(btn.dataset.equip);renderFieldTab('inventory');}));
    } else if(tab==='chart'){
      c.innerHTML=`<span class="eyebrow">NATAL RECORD</span><h1>${safeText(state.birth?.place||'Unknown birthplace')}</h1><table class="chart-table"><thead><tr><th>Placement</th><th>Sign</th><th>Degree</th><th>Awakens</th></tr></thead><tbody>${chartRows(state.chart).map(([k,v])=>`<tr><td>${safeText(k)}</td><td>${safeText(v.sign)} · ${safeText(v.element)}</td><td>${Number(v.degree||0).toFixed(1)}°</td><td>Lv ${progressionLevelForPlacement(k)}</td></tr>`).join('')}</tbody></table>`;
    } else {
      c.innerHTML=`<span class="eyebrow">CONTROLS</span><h1>Field Controls</h1><div class="control-grid"><kbd>WASD / Arrows</kbd><span>Continuous 8-way movement; diagonals are normalized.</span><kbd>E</kbd><span>Interact / talk / use a door or road. Also advances dialogue.</span><kbd>Tab</kbd><span>Cycle target (nearest first).</span><kbd>Shift (hold)</kbd><span>Guard: slower movement, reduced damage, costs Stamina when struck.</span><kbd>Space</kbd><span>Dash in your movement direction with brief invulnerability.</span><kbd>1–6 / J</kbd><span>Use hotbar ability (J = slot 1). Techniques have wind-up and recovery.</span><kbd>Q / F</kbd><span>Cycle armed trap / set trap at your feet (after Academy).</span><kbd>Esc</kbd><span>Pause and open this field menu.</span><kbd>F2</kbd><span>Toggle authored collision debug view.</span></div>`;
    }
  }

  let lastHud=0;
  function updateHud(force=false){
    if(!state.created) return;
    const t=now(); if(!force && t-lastHud<90) return; lastHud=t;
    $('hud-name').textContent=`${state.name} · Lv ${state.level}`;
    const specs=[['hp','hp','maxHp'],['stam','stamina','maxStamina'],['chakra','chakra','maxChakra'],['poise','poise','maxPoise']];
    for(const [id,k,m] of specs){ $(`${id}-fill`).style.width=`${pct(state.stats[k],state.stats[m])}%`; $(`${id}-text`).textContent=`${id.toUpperCase()} ${Math.round(state.stats[k])}/${state.stats[m]}`; }
    const map=MAPS[state.map]; $('zone-title').textContent=map?.display||state.map;
    $('objective').textContent=state.academyComplete && state.map==='Civic Ward'?'Academy complete. East road → Fringe Ward combat test.':state.academyComplete && state.map==='Academy'?'Certified. Return to the Civic Ward and take the east road.':(map?.objective||'');
    $('money').textContent=`MON ${state.gold}`;
    const left=Math.max(0,state.nextActionAt-t); $('cooldown').textContent=left>0?`RECOVERY ${(left/1000).toFixed(1)}s`:'ACTION READY';
    $('hotbar').innerHTML=state.hotbar.slice(0,6).map((n,i)=>{const a=abilityByName(n)||BASIC_JAB;const st=runtimeCost(a,'stam',state),ch=runtimeCost(a,'chakra',state);return `<div class="slot ${left>0?'cooling':''}"><kbd>${i+1}</kbd><b>${safeText(n)}</b><small>${a.slots||1}S${st?` · STA ${st}`:''}${ch?` · CHK ${ch}`:''}</small></div>`;}).join('');
    const traps=Object.entries(state.trapStock).filter(([,q])=>q>0);
    $('trap-hud').innerHTML=traps.length?`TRAP <b>${safeText(state.armedTrap||traps[0][0])}</b> ×${state.trapStock[state.armedTrap||traps[0][0]]||0} · Q cycle · F set`:'';
    const auth=worldScene?.authoredIds?.size||0, scaf=worldScene?.scaffoldCount||0;
    const art=map?.artState==='scaffold'
      ? (auth&&!scaf?`Separate Phaser world modules · ${auth} authored runtime candidates · unreviewed, not production-approved`
        :`Separate Phaser world modules · ${auth?`${auth} authored + `:''}procedural scaffold textures · not production art`)
      : 'Legacy baked district backdrop · temporary development scaffold · not production art';
    const who='Player: approved 512×64 paper-doll layers';
    $('art-state').textContent=`${art} · ${who}${worldScene?.stature?` · S=${worldScene.stature}px`:''}`;
  }

  /* ---------------- Scenes ---------------- */

  class TitleScene extends Phaser.Scene {
    constructor(){ super('Title'); }
    create(){
      this.cameras.main.setBackgroundColor('#101315');
      const g=this.add.graphics(); g.fillStyle(0x101315,1); g.fillRect(0,0,640,360);
      for(let i=0;i<80;i++){const x=(i*83)%640,y=(i*47)%260,a=.15+((i%5)*.06);g.fillStyle(0xd5c38e,a);g.fillRect(x,y,1+(i%2),1+(i%2));}
      g.lineStyle(1,0x6a5540,.38); for(let r=34;r<150;r+=26) g.strokeCircle(320,170,r);
      g.lineStyle(1,0x8b704b,.38); for(let i=0;i<12;i++){const a=i*Math.PI/6;g.lineBetween(320,170,320+Math.cos(a)*150,170+Math.sin(a)*150);}
      this.add.text(320,170,'AF',{fontFamily:'Georgia',fontSize:'72px',color:'#7f4a39',stroke:'#1a1716',strokeThickness:6}).setOrigin(.5);
    }
  }

  const SCAFFOLD_IDS = Object.keys(window.AF_SCAFFOLD?.SPECS||{});

  class WorldScene extends Phaser.Scene {
    constructor(){ super('World'); this.pausedByUi=false; this.builtColliders=[]; this.interactables=[]; this.guideMeasures=[]; this.mapObjects=[]; this.enemies=[]; this.npcs=[]; this.colliders=[]; this.occluders=[]; this.traps=[]; this.projectiles=[]; this.pending=[]; this.layerIndex={}; this.selected=null; this.authoredCount=0; }
    preload(){
      for(const m of Object.values(MAPS)) if(m.backdrop) this.load.image(`env-${m.key}`,assetPath(m.backdrop));
      for(const [id,path] of Object.entries(AUTHORED_MODULES)) this.load.image(`mod-${id}`,path);
      const [fw,fh]=SCALE.player.frame;
      for(const [key,path] of allLayerRefs()) this.load.spritesheet(key,assetPath(path),{frameWidth:fw,frameHeight:fh});
    }
    create(){
      worldScene=this;
      const look=sanitizeLook(state.appearance), m=this.measureFrame(layerKey(look.sex,'body',look.skin),frameFor('S'));
      this.stature=m.stature; this.footY=m.footY; this.statureSource=m; FOOT_Y=m.footY;
      this.keys=this.input.keyboard.addKeys({up:'W',down:'S',left:'A',right:'D',up2:'UP',down2:'DOWN',left2:'LEFT',right2:'RIGHT',guard:'SHIFT'});
      this.input.keyboard.addCapture('SPACE,TAB,UP,DOWN,LEFT,RIGHT');
      const kb=this.input.keyboard;
      kb.on('keydown-ESC',()=>{ if(isOpen('dialog-overlay')||isOpen('trap-overlay')) return; if($('field-menu').classList.contains('hidden')) showFieldMenu('status'); else closeFieldMenu(); });
      kb.on('keydown-E',()=>this.interact());
      kb.on('keydown-TAB',()=>this.cycleTarget());
      kb.on('keydown-SPACE',()=>this.dodge());
      kb.on('keydown-Q',()=>this.cycleTrap());
      kb.on('keydown-F',()=>this.placeTrap());
      kb.on('keydown-J',()=>this.useHotbar(0));
      kb.on('keydown-F2',()=>{ if(this.collisionDebug){ this.collisionDebug.setVisible(!this.collisionDebug.visible); } });
      ['ONE','TWO','THREE','FOUR','FIVE','SIX'].forEach((k,i)=>kb.on(`keydown-${k}`,()=>this.useHotbar(i)));
      this.events.once('shutdown',()=>{ this.clearWorld(); if(worldScene===this) worldScene=null; });
      this.buildMap(state.map,null); $('hud').classList.remove('hidden'); hideAllOverlays(); updateHud(true);
      window.__AF_WORLD_READY=true;
    }
    /* Opaque bounds of one texture frame: stature = visible height, footY = lowest opaque row. */
    measureFrame(key,idx){
      const fr=this.textures.getFrame(key,idx), img=fr.source.image;
      const c=document.createElement('canvas'); c.width=fr.cutWidth; c.height=fr.cutHeight;
      const g=c.getContext('2d',{willReadFrequently:true}); g.drawImage(img,fr.cutX,fr.cutY,fr.cutWidth,fr.cutHeight,0,0,fr.cutWidth,fr.cutHeight);
      const d=g.getImageData(0,0,c.width,c.height).data; let minX=c.width,minY=c.height,maxX=-1,maxY=-1;
      for(let y=0;y<c.height;y++) for(let x=0;x<c.width;x++) if(d[(y*c.width+x)*4+3]){ if(x<minX)minX=x; if(x>maxX)maxX=x; if(y<minY)minY=y; if(y>maxY)maxY=y; }
      return {key,frame:idx,frameSize:[c.width,c.height],bbox:[minX,minY,maxX,maxY],stature:maxY-minY+1,footY:maxY};
    }
    setPaused(v){ this.pausedByUi=!!v; if(!v) this.inputLockUntil=now()+220; }
    refreshFromState(){ this.buildMap(state.map,null); updateHud(true); }

    track(obj,layer){ this.mapObjects.push(obj); if(layer){ (this.layerIndex[layer] ||= []).push(obj); obj.setData?.('layer',layer); } return obj; }
    clearWorld(){
      for(const o of this.mapObjects) o?.destroy?.();
      for(const a of [...this.enemies,...this.npcs]) { a.doll?.destroy(); a.label?.destroy(); a.bar?.destroy(); }
      this.player?.doll.destroy();
      this.mapObjects=[];this.enemies=[];this.npcs=[];this.interactables=[];this.guideMeasures=[];this.colliders=[];this.occluders=[];this.traps=[];this.projectiles=[];this.pending=[];this.layerIndex={};this.selected=null;this.player=null;this.dash=null;this.motes=null;
    }

    /* Opaque bounds of a whole texture (cached per key). */
    contentBounds(key){
      this.boundsCache ||= {};
      if(this.boundsCache[key]) return this.boundsCache[key];
      const src=this.textures.get(key).getSourceImage(), c=document.createElement('canvas'); c.width=src.width; c.height=src.height;
      const g=c.getContext('2d',{willReadFrequently:true}); g.drawImage(src,0,0);
      const d=g.getImageData(0,0,c.width,c.height).data; let minX=c.width,minY=c.height,maxX=-1,maxY=-1;
      for(let y=0;y<c.height;y++) for(let x=0;x<c.width;x++) if(d[(y*c.width+x)*4+3]){ if(x<minX)minX=x; if(x>maxX)maxX=x; if(y<minY)minY=y; if(y>maxY)maxY=y; }
      return this.boundsCache[key]=maxX<0?{minX:0,minY:0,maxX:c.width-1,maxY:c.height-1}:{minX,minY,maxX,maxY};
    }
    moduleTexture(id){
      if(this.textures.exists(`mod-${id}`)){ this.authoredCount++; (this.authoredIds ||= new Set()).add(id); return `mod-${id}`; }
      this.scaffoldCount=(this.scaffoldCount||0)+1;
      const key=`scaf-${id}`;
      if(!this.textures.exists(key)) this.textures.addCanvas(key, window.AF_SCAFFOLD.build(id));
      return key;
    }

    buildMap(name, arrival){
      const map=MAPS[name]||MAPS['Imperial Docks'];
      this.clearWorld(); this.authoredCount=0; this.scaffoldCount=0; this.authoredIds=new Set(); this.placed=[];
      state.map=MAPS[name]?name:'Imperial Docks';
      if(arrival){ state.x=arrival.x; state.y=arrival.y; if(arrival.facing) state.facing=arrival.facing; }
      this.map=map;
      const cam=this.cameras.main; cam.setBounds(0,0,map.width,map.height); cam.stopFollow(); cam.setScroll(0,0);

      if(map.backdrop){
        this.track(this.add.image(0,0,`env-${map.key}`).setOrigin(0).setDepth(DEPTH.ground),'ground');
      }
      if(map.builder==='slice0') this.buildSlice0(map);
      if(map.builder==='scale') this.buildScaleGuide(map);

      // Collision: authored data only. Debug view is hidden unless toggled (F2).
      this.colliders=[...(map.colliders||[]).map(c=>({...c})),...(this.builtColliders||[])]; this.builtColliders=[];
      this.interactables=(map.interactables||[]).map(o=>({...o}));
      const dbg=this.add.graphics().setDepth(DEPTH.collision).setVisible(false);
      dbg.fillStyle(0xff3355,.28); dbg.lineStyle(1,0xff3355,.9);
      for(const c of this.colliders){ dbg.fillRect(c.x,c.y,c.w,c.h); dbg.strokeRect(c.x+.5,c.y+.5,c.w-1,c.h-1); }
      dbg.fillStyle(0x55ddff,.22); for(const e of map.exits||[]) dbg.fillRect(e.x,e.y,e.w,e.h);
      this.collisionDebug=this.track(dbg,'collision');

      for(const n of map.npcs||[]) this.spawnNpc(n);
      for(const e of map.enemies||[]) this.spawnEnemy(e);
      for(const c of state.corpses||[]) if(c.map===state.map && !c.recovered) this.spawnCorpseMarker(c);

      if(!this.isFree(state.x,state.y,null)){ state.x=map.spawn.x; state.y=map.spawn.y; }
      this.player={x:state.x,y:state.y,doll:makePlayerDoll(this,state.x,state.y),moving:false,staggerUntil:0};
      if(map.width>VIEW_W||map.height>VIEW_H){ cam.startFollow(this.player.doll.container,true,0.16,0.16); cam.setDeadzone(96,48); }
      else cam.setDeadzone();

      this.targetRing=this.track(this.add.graphics().setDepth(DEPTH.trap+1).setVisible(false));
      this.fxLayer=this.track(this.add.graphics().setDepth(DEPTH.fx),'atmosphere-fx');
      this.selected=null; this.updatePrompt(); updateHud(true); saveGame(true);
    }

    buildGround(map){
      const spec=map.ground||{modules:[['stone-clean',3],['stone-cracked',1]],seed:3};
      const r=(seed=>()=>{seed=(seed*16807)%2147483647;return (seed-1)/2147483646;})(spec.seed||7);
      const weights=spec.modules, total=weights.reduce((s,[,w])=>s+w,0);
      const pickModule=()=>{let v=r()*total;for(const [id,w] of weights){if((v-=w)<0)return id;}return weights[0][0];};
      let depth=DEPTH.ground;
      for(let y=0;y<map.height;y+=128){
        const off=Math.floor(r()*192);
        for(let x=-off;x<map.width;x+=192) this.track(this.add.image(x,y,this.moduleTexture(pickModule())).setOrigin(0).setDepth(depth+=0.001),'ground');
      }
      return r;
    }
    /* Player-scale reference: every guide object is sized from AF_SCALE ratios × measured stature. */
    buildScaleGuide(map){
      const S=this.stature; this.buildGround(map);
      const bridges=map.guideItems.filter(g=>g.item.startsWith('bridge')).map(g=>{const k=g.item==='bridge-single'?'bridgeSingle':'bridgePair';const w=SCALE.px(k,S);return [g.x-w/2,g.x+w/2];}).sort((a,b)=>a[0]-b[0]);
      const cn=map.canal, water=this.add.graphics().setDepth(DEPTH.ground+5);
      water.fillStyle(0x1b262b,1).fillRect(cn.x,cn.y,cn.w,cn.h).fillStyle(0x26363d,1).fillRect(cn.x,cn.y+cn.h-10,cn.w,10).fillStyle(0x777064,1).fillRect(cn.x,cn.y-4,cn.w,4).fillRect(cn.x,cn.y+cn.h,cn.w,4);
      this.track(water,'ground');
      let cx=cn.x; for(const [a,b] of bridges){ this.builtColliders.push({x:cx,y:cn.y,w:a-cx,h:cn.h}); cx=b; } this.builtColliders.push({x:cx,y:cn.y,w:cn.x+cn.w-cx,h:cn.h});
      for(const gi of map.guideItems){
        const it=SCALE.items[gi.item](S), key=`guide-${gi.item}-${S}`;
        if(!this.textures.exists(key)) this.textures.addCanvas(key,it.canvas);
        const img=this.add.image(Math.round(gi.x-it.anchor[0]),Math.round(gi.y-it.anchor[1]),key).setOrigin(0).setDepth(gi.y+(it.sortOffset||0));
        this.track(img,gi.item==='ruler'?'atmosphere-fx':it.occluder?'architecture':'props-back');
        for(const c of it.colliders) this.builtColliders.push({x:Math.round(gi.x+c.x),y:Math.round(gi.y+c.y),w:Math.round(c.w),h:Math.round(c.h)});
        if(it.occluder) this.occluders.push({img,sortY:gi.y,x:img.x,y:img.y,w:img.width,h:img.height,alpha:1});
        const lines=Object.entries(it.measures).map(([k,v])=>`${SCALE.guide[k].label}: ${v}px = ${(v/S).toFixed(2)}S`);
        if(gi.item==='ruler') lines.push(`Player stature S = ${S}px`);
        if(lines.length) this.track(this.add.text(gi.x,gi.y+4+(gi.labelDy||0),lines.join('\n'),{fontFamily:'monospace',fontSize:'7px',color:'#e8dcc0',backgroundColor:'#0d0d0ecc',padding:{x:2,y:1}}).setOrigin(.5,0).setDepth(DEPTH.label),'interactives');
        this.guideMeasures.push({item:gi.item,measures:it.measures});
      }
    }
    buildSlice0(map){
      const r=this.buildGround(map);
      let overlay=0;
      for(const p of map.placements){
        const key=this.moduleTexture(p.tex), img=this.add.image(p.x,p.y,key).setOrigin(0);
        // Authored modules are placed by their opaque content, not their canvas corner:
        // `bottom` puts the lowest opaque row on that world line; `cx` centres the content horizontally.
        const cb=this.contentBounds(key);
        if(p.cx!=null) img.x=Math.round(p.cx-(cb.minX+cb.maxX+1)/2);
        if(p.bottom!=null) img.y=p.bottom-(cb.maxY+1);
        if(p.layer==='ground') img.setDepth(DEPTH.ground+10+(overlay++)*0.001);
        else if(p.layer==='decals') img.setDepth(DEPTH.decals);
        else if(p.sortY===-1) img.setDepth(DEPTH.dressingFlat);
        else img.setDepth(p.sortY);
        this.track(img,p.layer);
        if(p.occluder) this.occluders.push({img,sortY:p.sortY,x:img.x+cb.minX,y:img.y+cb.minY,w:cb.maxX-cb.minX+1,h:cb.maxY-cb.minY+1,alpha:1});
        this.placed.push({tex:p.tex,key,x:img.x,y:img.y,bounds:{x:img.x+cb.minX,y:img.y+cb.minY,w:cb.maxX-cb.minX+1,h:cb.maxY-cb.minY+1}});
      }
      const sh=this.add.graphics().setDepth(DEPTH.shadow);
      for(const s of map.shadows||[]){ sh.fillStyle(0x0d0c0b,s.a); sh.fillRect(s.x,s.y,s.w,s.h); sh.fillStyle(0x0d0c0b,s.a*.5); sh.fillRect(s.x+2,s.y+s.h,s.w-4,2); }
      this.track(sh,'local-shadows');
      // Atmosphere: sparse drifting dust motes.
      this.motes=Array.from({length:26},()=>({x:r()*map.width,y:r()*map.height,vx:4+r()*6,vy:-2+r()*4,a:.18+r()*.25}));
    }

    spawnNpc(n){
      const doll=new PaperDoll(this,LOOKS[n.look]||LOOKS.keeper,n.x,n.y); doll.pose(n.facing||'S','idle',0);
      const label=this.add.text(n.x,n.y-66,n.name,{fontFamily:'monospace',fontSize:'8px',color:'#f1dfbb',backgroundColor:'#151515aa',padding:{x:2,y:1}}).setOrigin(.5,1).setDepth(DEPTH.label);
      this.npcs.push({...n,doll,label,facing:n.facing||'S'});
    }
    spawnEnemy(e){
      const copy=deepClone(e); copy.home={x:e.x,y:e.y}; copy.facing='S'; copy.phase='idle'; copy.phaseUntil=0; copy.aggro=false; copy.stunUntil=0; copy.slowUntil=0; copy.moving=false;
      copy.doll=new PaperDoll(this,LOOKS[e.look]||LOOKS.thug,e.x,e.y);
      copy.label=this.add.text(e.x,e.y-66,copy.name,{fontFamily:'monospace',fontSize:'8px',color:'#f0d7c1',backgroundColor:'#151515aa',padding:{x:2,y:1}}).setOrigin(.5,1).setDepth(DEPTH.label);
      copy.bar=this.add.graphics().setDepth(DEPTH.label);
      this.enemies.push(copy);
    }
    spawnCorpseMarker(c){
      const g=this.add.graphics().setDepth(DEPTH.trap); g.fillStyle(0x1a1512,.7); g.fillEllipse(c.x,c.y-2,26,9); g.lineStyle(1,0xd8ad62,.8); g.strokeEllipse(c.x,c.y-2,26,9);
      this.track(g,'interactives');
    }

    /* ---- collision ---- */
    footBox(x,y){ return {x:x-FOOT_HW,y:y-FOOT_H,w:FOOT_HW*2,h:FOOT_H}; }
    isFree(x,y,self){
      const m=this.map, b=this.footBox(x,y);
      if(b.x<0||b.y<0||b.x+b.w>m.width||b.y+b.h>m.height) return false;
      for(const c of this.colliders) if(b.x<c.x+c.w&&b.x+b.w>c.x&&b.y<c.y+c.h&&b.y+b.h>c.y) return false;
      const bodies=[...this.npcs,...this.enemies.filter(e=>e.hp>0)];
      if(this.player && self!==this.player) bodies.push(this.player);
      for(const o of bodies){ if(o===self) continue; if(Math.abs(o.x-x)<FOOT_HW*2-1 && Math.abs(o.y-y)<FOOT_H) return false; }
      return true;
    }
    /* Axis-separated movement with sub-stepping so fast dashes cannot tunnel through thin colliders. */
    moveBody(body,dx,dy){
      const steps=Math.max(1,Math.ceil(Math.max(Math.abs(dx),Math.abs(dy))/3));
      const sx=dx/steps, sy=dy/steps; let moved=false;
      for(let i=0;i<steps;i++){
        if(sx&&this.isFree(body.x+sx,body.y,body)){body.x+=sx;moved=true;}
        if(sy&&this.isFree(body.x,body.y+sy,body)){body.y+=sy;moved=true;}
      }
      return moved;
    }

    /* ---- player ---- */
    readMove(){
      const k=this.keys; const up=k.up.isDown||k.up2.isDown,down=k.down.isDown||k.down2.isDown,left=k.left.isDown||k.left2.isDown,right=k.right.isDown||k.right2.isDown;
      return {x:(right?1:0)-(left?1:0),y:(down?1:0)-(up?1:0)};
    }
    stepPlayer(dt,input,t){
      const p=this.player; if(!p) return;
      let vx=input.x, vy=input.y; const len=Math.hypot(vx,vy); if(len>0){vx/=len;vy/=len;}
      let speed=PLAYER_SPEED;
      if(state.guard) speed*=0.5;
      if(t<p.staggerUntil) speed=0;
      if(t<(this.attackCommitUntil||0)) speed*=0.3;
      if(this.dash){ vx=this.dash.vx; vy=this.dash.vy; speed=DASH_SPEED; if(t>=this.dash.until) this.dash=null; }
      const moved=(vx||vy)&&speed>0 ? this.moveBody(p,vx*speed*dt,vy*speed*dt) : false;
      p.moving=!!moved && len>0;
      if(len>0 && !this.dash && t>=p.staggerUntil){
        if(state.guard && this.selected?.hp>0) state.facing=dirFromVector(this.selected.x-p.x,this.selected.y-p.y);
        else state.facing=dirFromVector(vx,vy);
      }
      if(p.moving) state.tutorialFlags.moved=true;
      state.x=p.x; state.y=p.y;
    }
    updatePlayerVisual(t=now()){
      const p=this.player; if(!p) return;
      const anim=(state.guard||t<(this.attackCommitUntil||0))?'ready':p.moving?'walk':'idle';
      p.doll.apply(state.appearance); p.doll.pose(state.facing,anim,t); p.doll.place(p.x,p.y);
      p.doll.container.setAlpha(t<state.dodgeUntil?0.6:1);
    }

    nearestExit(){
      const p=this.player; if(!p) return null;
      return (this.map.exits||[]).find(e=>p.x>=e.x-10&&p.x<=e.x+e.w+10&&p.y>=e.y-10&&p.y<=e.y+e.h+10)||null;
    }
    /* Shared interaction framework: NPCs and world interactables (doors, signs, stations) resolve through one query. */
    nearestNpc(){ const p=this.player; return [...this.npcs,...this.interactables].filter(n=>dist(n,p)<=INTERACT_RANGE).sort((a,b)=>dist(a,p)-dist(b,p))[0]||null; }
    nearestCorpse(){ const p=this.player; return (state.corpses||[]).find(c=>c.map===state.map&&!c.recovered&&dist(c,p)<=28)||null; }
    updatePrompt(){
      if(!this.player) return;
      let prompt='';
      const npc=this.nearestNpc(), exit=this.nearestExit(), corpse=this.nearestCorpse();
      if(exit) prompt=exit.requiresAcademy&&!state.academyComplete?'Road closed · Academy certification required':exit.auto?`→ ${exit.label}`:`E · ${exit.label}`;
      if(npc) prompt=npc.doll?`E · Speak with ${npc.name}`:`E · Examine ${npc.name}`;
      if(corpse) prompt='E · Recover your fallen inventory';
      if($('prompt').textContent!==prompt) $('prompt').textContent=prompt;
    }
    interact(){
      if(this.pausedByUi||now()<(this.inputLockUntil||0)||!this.player) return;
      const corpse=this.nearestCorpse(); if(corpse){this.recoverCorpse(corpse);return;}
      const n=this.nearestNpc();
      if(n){
        if(n.doll) n.facing=dirFromVector(this.player.x-n.x,this.player.y-n.y);
        if(n.role==='armorer'){ openShop(n); return; }
        if(n.role==='sensei'){ if(state.academyComplete) showDialog('Sensei Daichi','Your foundation certification is complete. The Fringe Ward is past the east road of the Civic Ward. Train there, then return when you are ready for deeper systems.',[{label:'Understood'}]); else startSenseiTutorial(); }
        else showLines(n.name,n.lines||['…']);
        return;
      }
      const exit=this.nearestExit(); if(exit) this.useExit(exit);
    }
    useExit(exit){
      if(exit.requiresAcademy&&!state.academyComplete){toast('Academy certification required.');return false;}
      const target=MAPS[exit.target]; if(!target) return false;
      const arrival=target.arrivals?.[exit.arrive]||target.spawn;
      this.buildMap(exit.target,arrival); return true;
    }

    /* ---- targeting & combat ---- */
    liveEnemies(){ return this.enemies.filter(e=>e.hp>0); }
    cycleTarget(){
      if(this.pausedByUi) return;
      const p=this.player, live=this.liveEnemies().sort((a,b)=>dist(a,p)-dist(b,p));
      if(!live.length){this.selected=null;state.targetId=null;return;}
      let idx=this.selected?live.findIndex(e=>e.id===this.selected.id):-1; idx=(idx+1)%live.length;
      this.selected=live[idx]; state.targetId=this.selected.id; state.tutorialFlags.targeted=true; toast(`Target: ${this.selected.name}`,900);
    }
    useHotbar(index){
      if(this.pausedByUi||!this.player||now()<(this.inputLockUntil||0)) return;
      const t=now(); if(t<this.player.staggerUntil){toast('Staggered!',700);return;}
      const name=state.hotbar[index]; if(!name) return; const a=abilityByName(name)||(name==='Basic Jab'?BASIC_JAB:null); if(!a){toast(`Ability data missing: ${name}`);return;}
      const access=accessForAbility(a); if(!access.ok){toast(access.reason);return;} if(t<state.nextActionAt){toast('Still recovering.',700);return;}
      const st=runtimeCost(a,'stam',state),ch=runtimeCost(a,'chakra',state); if(state.stats.stamina<st){toast('Not enough Stamina.');return;} if(state.stats.chakra<ch){toast('Not enough Chakra.');return;}
      state.stats.stamina-=st;state.stats.chakra-=ch;state.nextActionAt=t+recoveryMs(a); if(st) this.lastStaminaUse=t;
      const n=cleanAbilityName(a);
      if(n==='Charge Chakra'){state.stats.chakra=clamp(state.stats.chakra+30,0,state.stats.maxChakra);state.stats.poise=clamp(state.stats.poise+state.stats.maxPoise*.25,0,state.stats.maxPoise);toast('Charge Chakra · +30 Chakra · +25 Poise');this.auraFx(0x6DC4F2);}
      else if(n==='Catch Breath'){state.stats.stamina=clamp(state.stats.stamina+30,0,state.stats.maxStamina);state.stats.poise=clamp(state.stats.poise+state.stats.maxPoise*.25,0,state.stats.maxPoise);toast('Catch Breath · +30 Stamina · +25 Poise');this.auraFx(0x86A07C);}
      else if(n==='Recompose'){state.stats.poise=clamp(state.stats.poise+state.stats.maxPoise*.20,0,state.stats.maxPoise);toast('Recompose · +20% max Poise');this.auraFx(0xCCA457);}
      else if(n==='Guardian Barrier'){state.stats.poise=clamp(state.stats.poise+20,0,state.stats.maxPoise);this.fortifiedUntil=t+2*SLOT_MS;toast('Guardian Barrier · Fortified');this.auraFx(0x5EC39C);}
      else this.attackWith(a,t);
      if(n==='Basic Jab') state.tutorialFlags.jabbed=true; updateHud(true);
    }
    pickTarget(reach){
      const p=this.player, fv=dirVector(state.facing);
      if(this.selected?.hp>0 && dist(this.selected,p)<=reach) return this.selected;
      const cands=this.liveEnemies().filter(e=>{const d=dist(e,p);if(d>reach)return false;const dot=((e.x-p.x)*fv.x+(e.y-p.y)*fv.y)/(d||1);return dot>0.2||d<14;});
      return cands.sort((a,b)=>dist(a,p)-dist(b,p))[0]||null;
    }
    attackWith(a,t){
      const p=this.player, rangeTiles=Number(a.range)||1.45, reach=rangeTiles*TILE*0.75+12;
      if(rangeTiles>2){ // projectile technique
        const tgt=this.pickTarget(rangeTiles*TILE);
        const v=tgt?{x:tgt.x-p.x,y:(tgt.y-20)-(p.y-24)}:dirVector(state.facing); const l=Math.hypot(v.x,v.y)||1;
        if(tgt) state.facing=dirFromVector(v.x,v.y);
        this.attackCommitUntil=t+180;
        this.pending.push({at:t+140,fn:()=>this.spawnProjectile(a,p.x,p.y-24,v.x/l,v.y/l,rangeTiles*TILE)});
        return;
      }
      const tgt=this.pickTarget(reach+16);
      if(tgt) state.facing=dirFromVector(tgt.x-p.x,tgt.y-p.y);
      this.attackCommitUntil=t+240;
      this.pending.push({at:t+120,fn:()=>{
        this.slashFx(p.x,p.y,state.facing);
        const hit=this.pickTarget(reach);
        if(!hit){ return; }
        this.damageEnemy(hit,Number(a.power)||0,a);
      }});
    }
    spawnProjectile(a,x,y,vx,vy,maxDist){
      const g=this.add.graphics().setDepth(DEPTH.fx-1); g.fillStyle(0x6DC4F2,1); g.fillCircle(0,0,3); g.fillStyle(0xAEEBFF,1); g.fillCircle(-1,-1,1);
      g.setPosition(x,y); this.track(g,'atmosphere-fx');
      this.projectiles.push({a,g,x,y,vx,vy,left:maxDist,speed:280});
    }
    stepProjectiles(dt){
      for(const pr of this.projectiles){
        const step=pr.speed*dt; pr.x+=pr.vx*step; pr.y+=pr.vy*step; pr.left-=step; pr.g.setPosition(Math.round(pr.x),Math.round(pr.y)).setDepth(pr.y+24);
        const hit=this.liveEnemies().find(e=>Math.abs(e.x-pr.x)<11&&pr.y>e.y-44&&pr.y<e.y+2);
        const wall=this.colliders.some(c=>pr.x>c.x&&pr.x<c.x+c.w&&pr.y+24>c.y&&pr.y+24<c.y+c.h);
        if(hit){ this.damageEnemy(hit,Number(pr.a.power)||0,pr.a); pr.dead=true; }
        else if(wall||pr.left<=0){ pr.dead=true; }
        if(pr.dead){ this.burstFx(pr.x,pr.y,0x6DC4F2,10); pr.g.destroy(); }
      }
      this.projectiles=this.projectiles.filter(p=>!p.dead);
    }
    damageEnemy(e,raw,a={}){
      if(e.hp<=0) return;
      const t=now();
      if(raw<=0){ this.floatText(e.x,e.y-48,cleanAbilityName(a),'#d8c9a6'); return; }
      const dmg=Math.max(1,Math.round(raw)); e.hp-=dmg;
      const poiseDmg=dmg*0.8*((a.tags||[]).includes('guardBreak')?1.6:1);
      e.poise=Math.max(0,e.poise-poiseDmg);
      if(e.poise<=0){ e.stunUntil=Math.max(e.stunUntil,t+900); e.poise=e.maxPoise; e.phase='idle'; this.floatText(e.x,e.y-58,'STAGGER','#e7c47e'); }
      if(e.hostile) e.aggro=true;
      const kb=dirVector(dirFromVector(e.x-this.player.x,e.y-this.player.y)); this.moveBody(e,kb.x*6,kb.y*6);
      this.floatText(e.x,e.y-44,`-${dmg}`); this.flash(e.doll);
      if(e.hp<=0){
        e.hp=0; e.doll.container.setAlpha(.45); e.label.setText(`${e.name} · DOWN`); e.bar.clear();
        if(this.selected===e){this.selected=null;state.targetId=null;}
        if(e.respawnMs){ e.respawnAt=t+e.respawnMs; toast(`${e.name} yields.`,1200); }
        else { state.kills[e.name]=(state.kills[e.name]||0)+1; state.gold+=e.mon||0; gainXp(e.xp||0); toast(`${e.name} defeated · +${e.xp||0} XP${e.mon?` · +${e.mon} mon`:''}`); }
        saveGame(true);
      }
    }
    damagePlayer(raw,from){
      const t=now(), p=this.player; if(!p) return;
      if(t<state.dodgeUntil){ this.floatText(p.x,p.y-60,'EVADE','#9bc3cd'); return; }
      let dmg=raw;
      if(state.guard && state.stats.stamina>0){ dmg=Math.ceil(dmg*.45); state.stats.stamina=Math.max(0,state.stats.stamina-raw*.8); this.lastStaminaUse=t; }
      if(t<(this.fortifiedUntil||0)) dmg=Math.ceil(dmg*.75);
      const armor=OUTFITS[state.appearance.outfit]?.defense||0; if(armor) dmg=Math.max(1,Math.round(dmg*(1-armor)));
      state.stats.hp-=dmg; state.stats.poise-=Math.ceil(dmg*.9);
      this.floatText(p.x,p.y-60,`-${dmg}`,'#e38f7f'); this.flash(p.doll); this.cameras.main.shake(90,0.004);
      if(state.stats.poise<=0){ p.staggerUntil=t+650; state.stats.poise=Math.round(state.stats.maxPoise*.5); this.floatText(p.x,p.y-72,'STAGGERED','#e7c47e'); }
      if(from){ const kb=dirVector(dirFromVector(p.x-from.x,p.y-from.y)); this.moveBody(p,kb.x*5,kb.y*5); }
      if(state.stats.hp<=0){ state.stats.hp=0; this.handleDeath(); }
      updateHud(true);
    }
    dodge(){
      if(this.pausedByUi||!this.player||this.dash||now()<(this.inputLockUntil||0)) return;
      const t=now(); if(t<this.player.staggerUntil||t<(this.dodgeReadyAt||0)) return;
      if(state.stats.stamina<DODGE_COST){toast('Not enough Stamina to dash.',800);return;}
      const mv=this.readMove(); const v=(mv.x||mv.y)?(()=>{const l=Math.hypot(mv.x,mv.y);return {x:mv.x/l,y:mv.y/l};})():dirVector(state.facing);
      state.stats.stamina-=DODGE_COST; this.lastStaminaUse=t; state.dodgeUntil=t+DODGE_IFRAME_MS; this.dodgeReadyAt=t+DASH_MS+160;
      this.dash={vx:v.x,vy:v.y,until:t+DASH_MS}; state.tutorialFlags.dodged=true; updateHud(true);
    }

    /* ---- traps ---- */
    cycleTrap(){
      if(this.pausedByUi) return;
      const owned=TRAP_CHOICES.filter(n=>(state.trapStock[n]||0)>0);
      if(!owned.length){toast(state.academyComplete?'Trap Pouch empty.':'No trap supplies. Complete the Academy tutorial.');return;}
      const i=owned.indexOf(state.armedTrap); state.armedTrap=owned[(i+1)%owned.length]; toast(`Armed: ${state.armedTrap}`,900); updateHud(true);
    }
    placeTrap(){
      if(this.pausedByUi||!this.player||now()<(this.inputLockUntil||0)) return;
      const t=now(); const owned=TRAP_CHOICES.filter(n=>(state.trapStock[n]||0)>0);
      if(!owned.length){toast(state.academyComplete?'Trap Pouch empty.':'No trap supplies. Complete the Academy tutorial.');return;}
      if(!owned.includes(state.armedTrap)) state.armedTrap=owned[0];
      const name=state.armedTrap, a=abilityByName(name)||{name,slots:1,stam:10,power:0};
      if(!accessForAbility(a).ok){toast(accessForAbility(a).reason);return;}
      if(t<state.nextActionAt){toast('Still recovering.',700);return;}
      const st=runtimeCost(a,'stam',state); if(state.stats.stamina<st){toast('Not enough Stamina.');return;}
      state.stats.stamina-=st; this.lastStaminaUse=t; state.nextActionAt=t+recoveryMs(a); state.trapStock[name]-=1;
      const fv=dirVector(state.facing), x=this.player.x+fv.x*14, y=this.player.y+fv.y*10;
      const spec={
        'Explosive Tag':{trigger:18,radius:50,armMs:350,lifeMs:30000,once:true},
        'Flash Bomb':{trigger:22,radius:64,armMs:250,lifeMs:30000,once:true},
        'Spike Pit':{trigger:18,radius:18,armMs:200,lifeMs:3*SLOT_MS,tickMs:700},
        'Caltrops':{trigger:22,radius:22,armMs:150,lifeMs:3*SLOT_MS,tickMs:700},
        'Smoke Screen':{trigger:0,radius:54,armMs:0,lifeMs:2*SLOT_MS,smoke:true}
      }[name]||{trigger:18,radius:30,armMs:300,lifeMs:10000,once:true};
      const g=this.add.graphics().setDepth(spec.smoke?DEPTH.fx-2:DEPTH.trap);
      this.track(g,'interactives');
      this.traps.push({name,a,x,y,g,...spec,armedAt:t+spec.armMs,expiresAt:t+spec.lifeMs,lastTick:{}});
      toast(`${name} set · ${state.trapStock[name]} left`,1000); saveGame(true); updateHud(true);
    }
    drawTrap(tr,t){
      const g=tr.g; g.clear(); const armed=t>=tr.armedAt;
      if(tr.smoke){ const k=clamp((tr.expiresAt-t)/600,0,1); for(let i=0;i<9;i++){const a=i/9*Math.PI*2+t/1600;g.fillStyle(0x9a978d,.22*k);g.fillCircle(tr.x+Math.cos(a)*tr.radius*.55,tr.y-14+Math.sin(a)*tr.radius*.3,tr.radius*.5);} return; }
      if(tr.name==='Spike Pit'){ g.fillStyle(0x1b1612,.8); g.fillEllipse(tr.x,tr.y,tr.radius*2,tr.radius); g.fillStyle(0x8f877a,1); for(let i=-2;i<=2;i++) g.fillRect(tr.x+i*5,tr.y-3+(i&1),1,3); return; }
      if(tr.name==='Caltrops'){ g.fillStyle(0x474c4e,1); for(let i=0;i<12;i++){const a=i*2.4,d=(i%4)*5;g.fillRect(Math.round(tr.x+Math.cos(a)*d*1.3),Math.round(tr.y+Math.sin(a)*d*.6),2,1);} return; }
      g.fillStyle(0x2b2017,1); g.fillRect(tr.x-5,tr.y-3,10,6); g.fillStyle(tr.name==='Flash Bomb'?0xd7cdb3:0xb93b38,1); g.fillRect(tr.x-4,tr.y-2,8,4);
      if(armed && Math.floor(t/300)%2) { g.fillStyle(0xf0cf8f,1); g.fillRect(tr.x-1,tr.y-1,2,2); }
    }
    stepTraps(t){
      for(const tr of this.traps){
        if(t>=tr.expiresAt){ tr.dead=true; continue; }
        this.drawTrap(tr,t);
        if(t<tr.armedAt||tr.smoke) continue;
        const inside=this.liveEnemies().filter(e=>e.hostile&&Math.hypot(e.x-tr.x,(e.y-tr.y)*1.6)<=tr.trigger);
        if(!inside.length) continue;
        if(tr.once){
          const hitR=tr.radius, victims=this.liveEnemies().filter(e=>e.hostile&&Math.hypot(e.x-tr.x,(e.y-tr.y)*1.4)<=hitR);
          if(tr.name==='Flash Bomb'){ for(const e of victims){ e.stunUntil=t+SLOT_MS; e.phase='idle'; this.floatText(e.x,e.y-58,'BLINDED','#f0e7c8'); } this.burstFx(tr.x,tr.y-10,0xf5efd8,hitR); }
          else { for(const e of victims){ this.damageEnemy(e,Number(tr.a.power)||16,tr.a); e.poise=Math.max(0,e.poise-20); } this.burstFx(tr.x,tr.y-8,0xE23622,hitR); this.cameras.main.shake(140,0.006); }
          tr.dead=true;
        } else {
          for(const e of inside){
            if(t-(tr.lastTick[e.id]||0)<tr.tickMs) continue; tr.lastTick[e.id]=t;
            this.damageEnemy(e,Number(tr.a.power)||4,tr.a);
            if(tr.name==='Caltrops'){ e.slowUntil=t+SLOT_MS; }
          }
        }
      }
      for(const tr of this.traps) if(tr.dead) tr.g.destroy();
      this.traps=this.traps.filter(tr=>!tr.dead);
    }
    inSmoke(x,y){ return this.traps.some(tr=>tr.smoke&&Math.hypot(x-tr.x,(y-tr.y)*1.4)<=tr.radius); }

    /* ---- enemies & NPCs ---- */
    stepEnemies(dt,t){
      const p=this.player;
      for(const e of this.enemies){
        if(e.hp<=0){
          if(e.respawnAt&&t>=e.respawnAt){ e.hp=e.maxHp; e.poise=e.maxPoise; e.respawnAt=0; e.doll.container.setAlpha(1); e.label.setText(e.name); }
          continue;
        }
        e.moving=false;
        if(t<e.stunUntil){ this.syncActor(e,t,'idle'); continue; }
        if(e.hostile && p){
          const d=dist(e,p), hidden=this.inSmoke(p.x,p.y)||this.inSmoke(e.x,e.y);
          if(!e.aggro && d<AGGRO_RANGE && !hidden) e.aggro=true;
          if(e.aggro && (d>DEAGGRO_RANGE || (hidden && e.phase!=='windup'))) { e.aggro=false; if(e.phase!=='windup') e.phase='idle'; }
          if(e.phase==='windup'){
            if(t>=e.phaseUntil){
              if(dist(e,p)<=ENEMY_REACH+8) this.damagePlayer(e.power||6,e);
              this.slashFx(e.x,e.y,e.facing,0xd78d7e);
              e.phase='recover'; e.phaseUntil=t+ENEMY_RECOVER_MS;
            }
          } else if(e.phase==='recover'){
            if(t>=e.phaseUntil) e.phase=e.aggro?'chase':'idle';
          } else if(e.aggro){
            e.phase='chase';
            if(d<=ENEMY_REACH){ e.phase='windup'; e.phaseUntil=t+ENEMY_WINDUP_MS; e.facing=dirFromVector(p.x-e.x,p.y-e.y); }
            else this.steer(e,p.x,p.y,dt,t);
          } else {
            e.phase='idle';
            if(dist(e,e.home)>6) this.steer(e,e.home.x,e.home.y,dt,t,0.6);
          }
        }
        this.syncActor(e,t,e.phase==='windup'?'ready':e.moving?'walk':'idle');
      }
      for(const n of this.npcs){
        if(p && dist(n,p)<60) n.facing=dirFromVector(p.x-n.x,p.y-n.y);
        this.syncActor(n,t,'idle');
      }
    }
    steer(e,tx,ty,dt,t,mult=1){
      const dx=tx-e.x, dy=ty-e.y, l=Math.hypot(dx,dy)||1, sp=ENEMY_SPEED*mult*(t<e.slowUntil?0.45:1)*dt;
      let moved=this.moveBody(e,dx/l*sp,dy/l*sp);
      if(!moved){ // simple wall-follow: try the two perpendiculars
        moved=this.moveBody(e,-dy/l*sp,dx/l*sp)||this.moveBody(e,dy/l*sp,-dx/l*sp);
      }
      e.moving=moved; if(moved) e.facing=dirFromVector(dx,dy);
    }
    syncActor(a,t,anim){
      a.doll.pose(a.facing,anim,t+((a.id||'').length*97)); a.doll.place(a.x,a.y);
      a.label?.setPosition(Math.round(a.x),Math.round(a.y-64));
      if(a.bar){
        a.bar.clear();
        if(a.hp>0 && (a.aggro||a.hp<a.maxHp)){
          const w=24,x=Math.round(a.x-w/2),y=Math.round(a.y-62);
          a.bar.fillStyle(0x0d0d0e,.85).fillRect(x-1,y-1,w+2,4).fillStyle(0x834641,1).fillRect(x,y,Math.round(w*a.hp/a.maxHp),2);
          if(a.phase==='windup'){ a.bar.fillStyle(0xE23622,1).fillRect(Math.round(a.x)-1,y-8,2,5); }
        }
      }
    }

    /* ---- death & recovery ---- */
    handleDeath(){
      const drops={inventory:deepClone(state.inventory),trapStock:deepClone(state.trapStock),map:state.map,x:Math.round(state.x),y:Math.round(state.y),posUnits:'px',recovered:false,createdAt:Date.now()};
      state.corpses.push(drops);state.inventory=[];state.trapStock={};state.xpDebt+=25;
      for(const e of Object.values(state.equipment||{})) e.durability=Math.max(0,Math.floor(e.durability*.9));
      state.stats.hp=state.stats.maxHp;state.stats.stamina=state.stats.maxStamina;state.stats.chakra=state.stats.maxChakra;state.stats.poise=state.stats.maxPoise;
      const sp=MAPS['Imperial Docks'].spawn; state.map='Imperial Docks';state.x=sp.x;state.y=sp.y;saveGame(true);
      showDialog('DEFEATED','You awaken at the Imperial Docks with <b>25 XP debt</b>. Equipped durability fell by 10%. Your carried inventory and trap stock remain on a recoverable corpse in the district where you fell.',[{label:'Return to the Docks',onClick:()=>{closeDialog();this.buildMap('Imperial Docks',sp);}}]);
    }
    recoverCorpse(c){
      state.inventory.push(...(c.inventory||[])); for(const [n,q] of Object.entries(c.trapStock||{})) state.trapStock[n]=(state.trapStock[n]||0)+q;c.recovered=true;saveGame(true);toast('Corpse recovered · inventory restored',2400);
      this.buildMap(state.map,{x:this.player.x,y:this.player.y,facing:state.facing});
    }

    /* ---- FX ---- */
    floatText(x,y,text,color='#f5d17f'){const t=this.add.text(Math.round(x),Math.round(y),text,{fontFamily:'monospace',fontSize:'11px',fontStyle:'bold',color,stroke:'#111',strokeThickness:3}).setOrigin(.5).setDepth(DEPTH.float);this.tweens.add({targets:t,y:y-22,alpha:0,duration:650,onComplete:()=>t.destroy()});}
    flash(doll){ doll.container.setAlpha(.35); this.time.delayedCall(70,()=>doll.container?.active&&doll.container.setAlpha(1)); }
    slashFx(x,y,facing,color=0xf0e7c8){
      const v=dirVector(facing), cx=x+v.x*16, cy=y-26+v.y*10, g=this.add.graphics().setDepth(y+1);
      g.lineStyle(2,color,.9); g.beginPath(); const base=Math.atan2(v.y,v.x); g.arc(cx,cy,11,base-1.0,base+1.0); g.strokePath();
      this.tweens.add({targets:g,alpha:0,duration:160,onComplete:()=>g.destroy()});
    }
    burstFx(x,y,color,r){ const g=this.add.graphics().setDepth(DEPTH.fx); g.fillStyle(color,.55); g.fillCircle(x,y,r*.4); g.lineStyle(2,color,.9); g.strokeCircle(x,y,r*.6); g.setPosition(0,0); this.tweens.add({targets:g,alpha:0,duration:320,onComplete:()=>g.destroy()}); }
    auraFx(color){ const p=this.player; if(!p) return; const g=this.add.graphics().setDepth(p.y+1); g.lineStyle(1,color,.9); g.strokeEllipse(p.x,p.y-2,26,9); g.strokeEllipse(p.x,p.y-30,30,50); this.tweens.add({targets:g,alpha:0,duration:420,onComplete:()=>g.destroy()}); }

    stepOccluders(){
      const p=this.player; if(!p) return;
      const px=p.x-10, py=p.y-58, pw=20, ph=58;
      for(const o of this.occluders){
        const overlap=px<o.x+o.w&&px+pw>o.x&&py<o.y+o.h&&py+ph>o.y;
        const target=(overlap&&p.y<o.sortY)?0.42:1;
        o.alpha+= (target-o.alpha)*0.25; o.img.setAlpha(o.alpha);
      }
    }
    stepAtmosphere(dt){
      if(!this.motes) { this.fxLayer?.clear(); return; }
      const g=this.fxLayer; g.clear();
      for(const m of this.motes){ m.x=(m.x+m.vx*dt+this.map.width)%this.map.width; m.y=(m.y+m.vy*dt+this.map.height)%this.map.height; g.fillStyle(0xe8dcc0,m.a); g.fillRect(Math.round(m.x),Math.round(m.y),1,1); }
    }
    stepRegen(dt,t){
      const s=state.stats;
      if(!state.guard && t-(this.lastStaminaUse||0)>900) s.stamina=clamp(s.stamina+10*dt,0,s.maxStamina);
      const threatened=this.enemies.some(e=>e.aggro&&e.hp>0);
      if(!threatened) s.poise=clamp(s.poise+4*dt,0,s.maxPoise);
    }
    drawTargetRing(){
      const g=this.targetRing; if(!g) return; g.clear();
      if(this.selected?.hp>0){ g.setVisible(true); g.lineStyle(1,0xe1b15d,1); g.strokeEllipse(Math.round(this.selected.x),Math.round(this.selected.y-1),26,9); }
      else { g.setVisible(false); if(this.selected) this.selected=null; }
    }

    update(time,delta){
      if(!this.player) return;
      const t=now();
      if(this.pausedByUi){ this.updatePlayerVisual(t); return; }
      const dt=Math.min(delta,50)/1000;
      state.guard=!!this.keys.guard.isDown && t>=this.player.staggerUntil; if(state.guard) state.tutorialFlags.guarded=true;
      this.stepPlayer(dt,this.readMove(),t);
      for(const job of this.pending) if(t>=job.at){ job.done=true; job.fn(); }
      this.pending=this.pending.filter(j=>!j.done);
      if(!this.player) return; // map changed during a pending job
      this.stepProjectiles(dt); this.stepTraps(t); this.stepEnemies(dt,t); this.stepRegen(dt,t);
      if(!this.player) return; // death reset
      this.updatePlayerVisual(t); this.stepOccluders(); this.stepAtmosphere(dt); this.drawTargetRing();
      const exit=this.nearestExit(); if(exit?.auto && !(exit.requiresAcademy&&!state.academyComplete)){ this.useExit(exit); return; }
      this.updatePrompt(); updateHud();
      if(t-(this.lastAutosave||0)>5000){ this.lastAutosave=t; saveGame(true); }
    }
  }

  let game = null;
  function ensureGame(){
    if(game) return game;
    const config={
      type:Phaser.AUTO,parent:'game-root',width:VIEW_W,height:VIEW_H,backgroundColor:'#101315',pixelArt:true,antialias:false,roundPixels:true,
      scale:{mode:Phaser.Scale.FIT,autoCenter:Phaser.Scale.CENTER_BOTH,width:VIEW_W,height:VIEW_H},
      render:{pixelArt:true,antialias:false,roundPixels:true,powerPreference:'high-performance'},
      audio:{noAudio:true},scene:[TitleScene,WorldScene],banner:false
    };
    try{
      game=new Phaser.Game(config); window.AF_GAME=game; return game;
    }catch(e){
      console.error('Renderer startup failed',e);
      toast('This preview blocked the game renderer. Character creator remains usable.',4500);
      game=null; window.AF_GAME=null; return null;
    }
  }
  window.AF_GAME=null;

  function enterWorld(){
    state.created=true;
    const g=ensureGame();
    if(!g){ showOverlay('appearance-overlay'); return; }
    hideAllOverlays(); $('hud').classList.remove('hidden');
    const start=()=>{
      if(g.scene.isActive('Title')) g.scene.stop('Title');
      if(g.scene.isActive('World')) worldScene?.refreshFromState(); else g.scene.start('World');
    };
    if(g.isBooted) start(); else g.events.once('ready',start);
    saveGame(true);
  }
  function returnToTitle(){
    saveGame(true); $('field-menu').classList.add('hidden'); $('hud').classList.add('hidden');
    if(game){ if(game.scene.isActive('World'))game.scene.stop('World'); if(!game.scene.isActive('Title'))game.scene.start('Title'); }
    window.__AF_WORLD_READY=false;
    showOverlay('title-overlay');updateContinueButton();
  }

  $('new-btn').onclick=(e)=>{e?.preventDefault?.();showOverlay('birth-overlay');};
  $('birth-back').onclick=(e)=>{e?.preventDefault?.();showOverlay('title-overlay');};
  $('chart-back').onclick=(e)=>{e?.preventDefault?.();showOverlay('birth-overlay');};
  $('appearance-back').onclick=(e)=>{e?.preventDefault?.();showOverlay('chart-overlay');};
  $('appearance-btn').onclick=(e)=>{e?.preventDefault?.();showOverlay('appearance-overlay');startCreatorPreview();drawPaperDollPreview();};
  $('continue-btn').onclick=()=>{ if(loadGame())enterWorld(); };
  $('quick-btn').onclick=()=>{quickState();enterWorld();};
  $('scale-btn').onclick=()=>{ if(!loadGame()) quickState(); const sp=MAPS['Scale Reference'].spawn; state.map='Scale Reference'; state.x=sp.x; state.y=sp.y; enterWorld(); };
  $('slice0-btn').onclick=()=>{ if(!loadGame()) quickState(); const sp=MAPS['Slice 0'].spawn; state.map='Slice 0'; state.x=sp.x; state.y=sp.y; enterWorld(); };
  $('chart-btn').onclick=(event)=>{event?.preventDefault?.();
    try{
      const birth={date:$('birth-date').value,time:$('birth-time').value,place:$('birth-place').value.trim(),lat:Number($('birth-lat').value),lon:Number($('birth-lon').value),tz:$('birth-tz').value.trim()||'UTC'};
      if(!birth.date||!birth.time||!Number.isFinite(birth.lat)||!Number.isFinite(birth.lon)) throw new Error('Date, exact local time, latitude, and longitude are required.');
      const utc=AF_ASTRO.zonedLocalToUtc(birth.date,birth.time,birth.tz); pendingChart=AF_ASTRO.buildChart(utc,birth.lat,birth.lon,{placeName:birth.place,timeZone:birth.tz}); state.birth=birth;
      $('chart-summary').textContent=`${birth.place} · ${birth.date} ${birth.time} ${birth.tz} · UTC ${pendingChart.birthUtc}`;
      $('chart-grid').innerHTML=chartRows(pendingChart).map(([k,v])=>`<div class="placement"><b>${safeText(k)}</b><span>${safeText(v.sign)} · ${safeText(v.element)} · ${Number(v.degree).toFixed(1)}°${v.retrograde?' ℞':''}</span></div>`).join('');
      showOverlay('chart-overlay');
    } catch(e){toast(e.message||String(e),3000);}
  };
  $('enter-world-btn').onclick=()=>{
    const birth=state.birth;
    state=normalizeState(DEFAULT_STATE); state.created=true;state.name=$('fighter-name').value.trim()||'Fighter';state.birth=birth||{date:$('birth-date').value,time:$('birth-time').value,place:$('birth-place').value,lat:Number($('birth-lat').value),lon:Number($('birth-lon').value),tz:$('birth-tz').value};state.chart=pendingChart||makeTestChart();state.appearance=readCreatorAppearance();
    enterWorld();
  };
  $('close-menu').onclick=closeFieldMenu; $('save-btn').onclick=()=>saveGame(false); $('return-title-btn').onclick=returnToTitle;
  document.querySelectorAll('#field-menu [data-tab]').forEach(b=>b.addEventListener('click',()=>renderFieldTab(b.dataset.tab)));

  // Keyboard advance for dialogue: Enter / E / Space presses the first dialogue button.
  document.addEventListener('keydown',e=>{
    if(!isOpen('dialog-overlay')) return;
    if(['Enter','e','E',' '].includes(e.key)){ e.preventDefault(); $('dialog-actions').querySelector('button')?.click(); }
  });

  window.addEventListener('blur',()=>{if(state.created)saveGame(true);}); window.addEventListener('beforeunload',()=>{if(state.created)saveGame(true);});

  /* ---------------- Self tests (?selftest) ---------------- */

  async function runSelfTests(){
    const results=[]; const test=(name,fn)=>{try{const v=fn();if(v===false)throw new Error('assertion returned false');results.push({name,ok:true});}catch(e){results.push({name,ok:false,error:String(e.message||e)});}};
    const S=worldScene;
    test('Phaser version 4.2.1',()=>Phaser.VERSION==='4.2.1');
    test('Renderer initialized',()=>!!game?.renderer);
    test('Pixel-art renderer settings retained',()=>game.config.pixelArt===true&&game.config.antialias===false&&game.config.roundPixels===true);
    test('Canonical roster is 180 records',()=>abilityRecords().length===180);
    test('Recompose exists',()=>!!abilityByName('Recompose'));
    test('Player contract is the 512×64 sheet of eight 64×64 frames',()=>JSON.stringify(SCALE.player.sheetCanvas)==='[512,64]'&&JSON.stringify(SCALE.player.frame)==='[64,64]'&&SCALE.player.framesPerSheet===8&&SCALE.player.frameOrder.length===8);
    test('Every registered paper-doll layer loads as a 512×64 sheet of eight 64×64 frames',()=>allLayerRefs().every(([k])=>game.textures.exists(k)&&game.textures.get(k).getSourceImage().width===512&&game.textures.get(k).getSourceImage().height===64&&game.textures.get(k).frameTotal-1===8));
    test('Frame order is the confirmed approved order (S first)',()=>JSON.stringify(CHARS.frameOrder)===JSON.stringify(SCALE.player.frameOrder)&&CHARS.frameOrder[0]==='S');
    test('Male and female options: 2 skin tones, hair, 2 eye colours',()=>Object.keys(CHARS.sexes.male.skin).length===2&&Object.keys(CHARS.sexes.female.skin).length===2&&Object.keys(CHARS.sexes.male.hair).length===3&&Object.keys(CHARS.sexes.female.hair).length===2&&Object.keys(CHARS.sexes.male.eyes).length===2);
    test('Draw order is body, clothing, arms, shoulders, hair, eyes',()=>lookLayers({sex:'male',outfit:'red-armor'}).map(l=>l.slot).join()==='body,clothing,arms,shoulders,hair,eyes');
    test('Gi is the starter outfit for both frames',()=>{const n=normalizeState(DEFAULT_STATE);return n.appearance.outfit==='gi'&&n.wardrobe.join()==='gi'&&outfitFits('female','gi')&&outfitFits('male','gi');});
    test('Player stature is measured from the base frame',()=>S.stature>=40&&S.stature<=64&&S.footY>=S.stature-1);
    test('Player collision is an authored foot box, not the sprite frame',()=>FOOT_HW*2===SCALE.player.collision.w&&FOOT_H===SCALE.player.collision.h&&FOOT_HW*2<SCALE.player.frame[0]);
    test('Eight-direction facing from movement vector',()=>['E','SE','S','SW','W','NW','N','NE'].every((d,i)=>dirFromVector(Math.cos(i*Math.PI/4),Math.sin(i*Math.PI/4))===d));
    const old=deepClone(state);
    quickState(); S.buildMap('Imperial Docks',MAPS['Imperial Docks'].spawn);
    test('Fresh fighter starts with Basic Jab only',()=>state.hotbar.length===1&&state.hotbar[0]==='Basic Jab'&&!state.academyComplete);
    test('General locked pre-Academy',()=>!accessForAbility(abilityByName('Chakra Bullet')).ok);
    test('Continuous movement: position advances by speed×dt, not whole tiles',()=>{const p=S.player,x0=p.x;S.stepPlayer(0.1,{x:1,y:0},now());const dx=p.x-x0;return Math.abs(dx-PLAYER_SPEED*0.1)<0.5 && dx%TILE!==0;});
    test('Diagonal movement is normalized',()=>{const p=S.player;p.x=300;p.y=222;const x0=p.x,y0=p.y;S.stepPlayer(0.1,{x:1,y:-1},now());const d=Math.hypot(p.x-x0,p.y-y0);return Math.abs(d-PLAYER_SPEED*0.1)<0.6;});
    test('Authored collision blocks movement independently of art',()=>{const p=S.player;p.x=200;p.y=200;for(let i=0;i<30;i++)S.stepPlayer(0.05,{x:-1,y:0},now());return p.x-FOOT_HW>=168-0.01;});
    test('No grid overlay; collision debug view hidden by default',()=>!S.layerIndex.grid&&S.collisionDebug.visible===false);
    S.buildMap('Scale Reference',MAPS['Scale Reference'].spawn);
    test('Scale reference objects are sized from ratios of measured stature',()=>S.guideMeasures.length>=12&&S.guideMeasures.every(g=>Object.entries(g.measures).every(([k,v])=>SCALE.within(k,v,S.stature))));
    test('Scale reference door admits the player collision box',()=>{const d=S.guideMeasures.find(g=>g.item==='wall-door').measures;return d.doorOpeningW>FOOT_HW*2+8;});
    test('Single-file bridge admits the player; canal blocks elsewhere',()=>{const p=S.player;p.x=650;p.y=420;for(let i=0;i<40;i++)S.stepPlayer(0.05,{x:0,y:-1},now());const crossed=p.y<272;p.x=600;p.y=420;for(let i=0;i<40;i++)S.stepPlayer(0.05,{x:0,y:-1},now());return crossed&&p.y>400;});
    S.buildMap('Slice 0',MAPS['Slice 0'].spawn);
    test('Slice 0 scaffold proportions fall within player-relative tolerances',()=>Object.entries(MAPS['Slice 0'].proportions).every(([k,v])=>SCALE.within(k,v,S.stature)));
    test('Slice 0 door is an interactable through the shared framework',()=>{S.player.x=480;S.player.y=258;return S.nearestNpc()?.id==='courtyard-door';});
    test('Slice 0 loads ≥10 separate environment textures',()=>new Set(S.mapObjects.filter(o=>o.type==='Image').map(o=>o.texture.key)).size>=10);
    test('Slice 0 routes objects into manifest world layers',()=>['ground','decals','architecture','architecture-dressing','props-back','collision','props-front-occluders','local-shadows','atmosphere-fx'].every(l=>(S.layerIndex[l]||[]).length>0));
    test('Slice 0 has no full-frame backdrop',()=>!S.mapObjects.some(o=>o.type==='Image'&&o.width>=VIEW_W&&o.height>=VIEW_H));
    test('Player sorts behind gate beam when north of it and in front when south',()=>{const beam=S.occluders.find(o=>o.img.texture.key.endsWith('horizontal-beam'));S.player.x=480;S.player.y=300;S.updatePlayerVisual();const behind=S.player.doll.container.depth<beam.img.depth;S.player.y=420;S.updatePlayerVisual();return behind&&S.player.doll.container.depth>beam.img.depth;});
    test('Foreground occluder fades when the player is behind it',()=>{const lp=S.occluders.find(o=>o.img.texture.key.endsWith('lantern-post'));S.player.x=360;S.player.y=470;S.updatePlayerVisual();for(let i=0;i<20;i++)S.stepOccluders();return lp.img.alpha<0.6;});
    test('Academy reward grants exactly once',()=>{const a=grantAcademyKit(['Explosive Tag','Flash Bomb','Spike Pit'],true),g=state.gold,b=grantAcademyKit(['Explosive Tag','Flash Bomb','Spike Pit'],true);return a===true&&b===false&&g===100&&state.gold===100;});
    test('Academy grants 10 of each chosen trap',()=>state.trapStock['Explosive Tag']===10&&state.trapStock['Flash Bomb']===10&&state.trapStock['Spike Pit']===10);
    test('Smoke Bomb is not a x10 Academy choice',()=>!TRAP_CHOICES.includes('Smoke Bomb'));
    test('Post-Academy hotbar matches approved default',()=>JSON.stringify(state.hotbar)===JSON.stringify(POST_ACADEMY_HOTBAR));
    test('General unlocked post-Academy',()=>accessForAbility(abilityByName('Chakra Bullet')).ok);
    test('Recompose costs 10% max Stamina and Chakra',()=>runtimeCost(abilityByName('Recompose'),'stam',state)===10&&runtimeCost(abilityByName('Recompose'),'chakra',state)===10);
    test('Real-time recovery scales with slots',()=>recoveryMs({slots:1})===RECOVERY_MS_PER_SLOT&&recoveryMs({slots:2})===2*RECOVERY_MS_PER_SLOT);
    test('Academy is reachable from the safe Civic Ward',()=>MAPS['Civic Ward'].enemies.length===0&&MAPS['Civic Ward'].exits.some(e=>e.target==='Academy'));
    test('Fringe Ward contains hostile thugs',()=>MAPS['Fringe Ward'].enemies.filter(e=>e.hostile).length>=2);
    S.buildMap('Fringe Ward',MAPS['Fringe Ward'].spawn);
    test('Placed trap consumes one supply',()=>{state.nextActionAt=0;state.armedTrap='Spike Pit';S.inputLockUntil=0;S.placeTrap();return state.trapStock['Spike Pit']===9&&S.traps.length===1;});
    test('Armor purchase: mon decreases, wardrobe grows, paper doll changes, persists through save/load',()=>{state.appearance.sex='male';state.gold=100;const ok=buyOutfit('red-armor')&&equipOutfit('red-armor');const layers=S.player.doll.sprites.map(e=>e.variant).join();saveGame(true);loadGame();return ok&&state.gold===20&&state.wardrobe.includes('red-armor')&&state.appearance.outfit==='red-armor'&&layers.includes('pd-male-shoulders-red-armor');});
    test('Armor cannot be bought without enough mon',()=>{state.gold=10;return !buyOutfit('blue-armor')&&state.gold===10;});
    test('Armor is not offered to the female frame (no female armor layers)',()=>!outfitFits('female','red-armor')&&!outfitFits('female','blue-armor'));
    test('Selling returns half price and reverts to the Gi',()=>{state.gold=0;const ok=sellOutfit('red-armor');return ok&&state.gold===40&&state.appearance.outfit==='gi'&&!state.wardrobe.includes('red-armor');});
    test('Map transitions preserve mon, inventory, and trap stock',()=>{const before=JSON.stringify([state.gold,state.inventory,state.trapStock]);S.useExit(MAPS['Fringe Ward'].exits[0]);const mid=state.map;S.buildMap('Fringe Ward',MAPS['Fringe Ward'].spawn);return mid==='Civic Ward'&&JSON.stringify([state.gold,state.inventory,state.trapStock])===before;});
    test('Melee hit damages an adjacent enemy in real time',()=>{const e=S.enemies[0];S.player.x=e.x-18;S.player.y=e.y;state.facing='E';const hp=e.hp;S.damageEnemy(e,6,BASIC_JAB);return e.hp===hp-6;});
    state=old; S.buildMap(state.map,null);
    const ok=results.every(r=>r.ok); document.body.dataset.selftest=ok?'pass':'fail'; window.__AF_SELFTEST={ok,results,build:BUILD,phaser:Phaser.VERSION,renderer:game?.renderer?.type,abilityCount:abilityRecords().length};
    console.table(results); if(!ok)console.error('Astro Fighters selftest failed',results.filter(r=>!r.ok)); else console.log('Astro Fighters selftest PASS',results.length);
    return window.__AF_SELFTEST;
  }

  window.AF_TEST={
    BUILD,SLOT_MS,RECOVERY_MS_PER_SLOT,PLAYER_SPEED,TRAP_CHOICES,POST_ACADEMY_HOTBAR,MAPS,
    getState:()=>deepClone(state),setState:s=>{state=normalizeState(s);},quickState,grantAcademyKit,abilityByName,accessForAbility,runtimeCost,runSelfTests,
    enterMap:(name)=>{const sp=MAPS[name].spawn;if(worldScene)worldScene.buildMap(name,sp);else{state.map=name;state.x=sp.x;state.y=sp.y;}},
    teleport:(x,y)=>{state.x=x;state.y=y;if(worldScene?.player){worldScene.player.x=x;worldScene.player.y=y;worldScene.updatePlayerVisual();worldScene.updatePrompt();}},
    useHotbar:(i)=>worldScene?.useHotbar(i),
    scene:()=>worldScene,
    worldLayers:()=>Object.fromEntries(Object.entries(worldScene?.layerIndex||{}).map(([k,v])=>[k,v.length])),
    paperDoll:()=>({look:deepClone(state.appearance),wardrobe:[...state.wardrobe],previewFacing:creatorFacing,layers:(worldScene?.player?.doll.sprites||[]).map(e=>({slot:e.def.slot,texture:e.sprite.texture.key,frame:[e.sprite.frame.width,e.sprite.frame.height]}))}),
    buyOutfit,sellOutfit,equipOutfit,
    renderer:()=>({phaser:Phaser.VERSION,type:game?.renderer?.type,webgl:game?.renderer?.type===Phaser.WEBGL,canvas:game?.renderer?.type===Phaser.CANVAS})
  };

  bindCreatorPreview();
  updateContinueButton();
  { const s=$('js-status'); if(s){s.textContent='JavaScript active · full Astro Fighters app initialized';s.style.color='#7fd4a7';} window.AF_FULL_APP_READY=true; }
  const qp=new URLSearchParams(location.search);
  const bootFromQuery=()=>{
    if(qp.has('selftest')){quickState();enterWorld(); const wait=()=>{if(window.__AF_WORLD_READY)setTimeout(runSelfTests,120);else setTimeout(wait,25);};wait();}
    else if(qp.has('fringe')){quickState({academy:true,map:'Fringe Ward'});enterWorld();}
    else if(qp.has('academy')){quickState({map:'Academy'});enterWorld();}
    else if(qp.has('slice0')){quickState({map:'Slice 0'});enterWorld();}
    else if(qp.has('scale')){quickState({map:'Scale Reference'});enterWorld();}
    else if(qp.has('quickstart')){quickState();enterWorld();}
  };
  setTimeout(bootFromQuery,50);
})();
