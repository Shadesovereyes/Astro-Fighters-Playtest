"use strict";
// Sprite layer for the hex testbed: the engine's round event record, the replay planner, the
// clip choice per ability, and the imported rig runtime it draws from.
const assert=require("assert");
const fs=require("fs");
const path=require("path");
global.window=global;
require("./af-core.js");
require("./af-dc-model-v3.js");
require("./af-core-v3-patch.js");
require("./af-ui-v3.js");
require("./af-anim-map-v3.js");
const SPR=require("./af-sprites-v3.js");
const {AF}=global;

// --- the imported rig: every sheet the runtime names exists, at the frame size its state declares
const def=JSON.parse(fs.readFileSync(path.join(__dirname,"characters/male.json"),"utf8"));
assert.equal(def.schema,"astro-fighters-character-runtime/v1");
assert.deepStrictEqual(def.frameSize,[64,64]);
assert.deepStrictEqual(def.pivot,SPR.PIVOT);
assert.ok(def.source&&def.source.commit,"rig records the playtest commit it was imported from");
function png(file){const b=fs.readFileSync(path.join(__dirname,file));assert.equal(b.subarray(1,4).toString("ascii"),"PNG",file);return{w:b.readUInt32BE(16),h:b.readUInt32BE(20)};}
let sheets=0;
for(const [name,st] of Object.entries(def.states)){
  for(const [layer,file] of Object.entries(st.layers)){const {w,h}=png(file);sheets++;
    assert.equal(w,st.frames*64,`${name}/${layer} width`);assert.equal(h,st.rows.length*64,`${name}/${layer} height`);}
  for(const it of (st.weapons&&st.weapons.items)||[])for(const file of Object.values(it.layers)){const {w,h}=png(file);sheets++;
    assert.equal(w,st.frames*128,`${name} weapon width`);assert.equal(h,st.rows.length*128,`${name} weapon height`);}
}
png(def.contactShadow);
// every clip the replay can ask for is authored
const clips=[["lightAttack","jab"],["lightAttack","cross"],["heavyAttack","lowKick"],["heavyAttack","snapKick"],["heavyAttack","spinRoundhouse"],
  ["katanaLight","downCut"],["katanaLight","upCut"],["katanaHeavy","sideCutR"],["katanaHeavy","sideCutL"],
  ["oneHandLight","stab1"],["oneHandLight","stab2"],["oneHandLight","stab3"],["oneHandHeavy","swipeR"],["oneHandHeavy","swipeL"],
  ["weave","weave"],["block","block"],["hitReact","hitReact"],["guardBreak","guardBreak"]];
for(const [st,c] of clips)assert.ok(def.states[st]&&def.states[st].clips[c],`missing clip ${st}/${c}`);
for(const st of ["guard","twoHandGuard","oneHandGuard","exhausted","walk"])assert.ok(def.states[st],`missing state ${st}`);
for(const o of ["gi","blueArmor","redArmor"])assert.ok(def.outfits[o],`missing outfit ${o}`);

// --- clip choice comes from the ability table
const melee=(name,o={})=>({name,group:"Martial",dmg:"Physical",atk:"Melee",maxR:1,slots:1,tags:[],effects:[{k:"Damage"}],pos:{scope:"Martial|Boxing"},...o});
const c=new Map(),f={name:"A",faction:0,stam:10};
const seq=x=>x.seq.map(s=>s.state+"/"+s.clip).join(",");
assert.equal(seq(SPR.attackClip(f,melee("Jab-Cross"),c)),"lightAttack/jab,lightAttack/cross");
assert.equal(seq(SPR.attackClip(f,melee("Roundhouse Kick"),c)),"heavyAttack/spinRoundhouse");
assert.equal(seq(SPR.attackClip(f,melee("Calf Kick"),c)),"heavyAttack/lowKick");
assert.equal(SPR.attackClip(f,melee("Haymaker"),c).fit,"standIn");
const k=new Map(),slash=melee("Kenjutsu Slash",{group:"Weapon",pos:{scope:"Weapon|Kenjutsu"}});
assert.equal(seq(SPR.attackClip(f,slash,k)),"katanaLight/downCut");
assert.equal(seq(SPR.attackClip(f,slash,k)),"katanaLight/upCut","repeated light cuts alternate");
assert.equal(SPR.attackClip(f,slash,new Map()).weapon,"katana");
assert.equal(SPR.attackClip(f,melee("Sickle Strike",{group:"Weapon",pos:{scope:"Weapon|KyoketsuShoge"}}),new Map()).weapon,"tanto");
assert.equal(SPR.attackClip(f,{name:"Fireball",group:"Ninjutsu",dmg:"Elemental",atk:"Projectile",maxR:5,slots:1,tags:[],effects:[{k:"Damage"}]},c).kind,"cast");
assert.equal(seq(SPR.attackClip(f,melee("Hip Toss",{group:"Martial",pos:{scope:"Martial|Judo"}}),c)),"clinchHipToss/clinchHipToss","Hip Toss plays the approved paired throw");
assert.equal(SPR.attackClip(f,melee("Sweeping Shoulder",{group:"Martial",pos:{scope:"Martial|Judo"}}),c),null,"ground grappling has no authored motion yet");
// clinch moves: the paired clips by standing-grapple role
assert.deepEqual(SPR.clinchClips("Grappling",{name:"Knee Strikes"}),["clinchKnee","clinchKneeHit"]);
assert.deepEqual(SPR.clinchClips("Grappled",{name:"Elbow Strike"}),["clinchHeldElbow","clinchHoldElbowHit"]);
assert.deepEqual(SPR.clinchClips("Grappled",{name:"Rolling Throw"}),["clinchRollingThrow","clinchRollingThrowHit"],"the thrower plays the holder's side from either role");
assert.equal(SPR.clinchClips("Grappled",{name:"Hip Toss"}),null);
{const P=SPR.pairSpots({x:100,y:200},{x:159,y:200});assert.equal(P.held.x-P.holder.x,27);assert.equal(P.holder.facing,"E");assert.equal(P.held.facing,"W");
 const Q=SPR.pairSpots({x:159,y:251},{x:100,y:200});assert.equal(Q.holder.x-Q.held.x,27);assert.equal(Q.holder.facing,"W");assert.equal(Q.holder.y,Q.held.y,"a pair stands side by side");}
assert.equal(seq(SPR.attackClip(f,{name:"Bob and Weave",group:"Martial",dmg:"None",atk:"Melee",tags:[],effects:[{k:"Buff"}]},c)),"weave/weave");
// every ability in the testbed resolves to clips the rig actually has
const MAP=require("./af-anim-map-v3.js");
const pool=[];for(const w of Object.keys(AF.WEAPONS))pool.push(...AF.buildLoadout({unlockAll:true,martials:Object.keys(AF.MARTIAL),weapon:w,learnedMedical:["Palm Healing","Cellular Activation"]}));
for(const key of AF.ENEMY_KEYS)pool.push(...AF.enemyLoadout(key));
for(const ab of pool){const m=MAP.forAbility(ab);assert.ok(["exact","standIn","missing"].includes(m.fit),ab.name);
  if(m.fit!=="exact")assert.ok(m.need,`${ab.name} must name the frames it waits on`);
  for(const [st,cl] of m.play){assert.ok(def.states[st],`${ab.name}: no state ${st}`);if(cl)assert.ok(def.states[st].clips[cl],`${ab.name}: no clip ${st}/${cl}`);}}
// a landed hit: block while the defender had poise, guard break on the emptying blow, recoil only at 0 poise
assert.equal(SPR.hitReaction({guarded:true,broke:false,killed:false}),"block");
assert.equal(SPR.hitReaction({guarded:true,broke:true,killed:false}),"guardBreak");
assert.equal(SPR.hitReaction({guarded:false,broke:false,killed:false}),"hitReact");
assert.equal(SPR.hitReaction({guarded:false,broke:true,killed:false}),"hitReact","a fighter already at 0 poise recoils even though the engine re-flags the break");
assert.equal(SPR.hitReaction({guarded:true,broke:false,killed:true}),"hitReact");
// stance and stamina pick the held pose
assert.equal(SPR.basePose({stam:10}).state,"guard");
assert.equal(SPR.basePose({stam:0}).state,"exhausted");
assert.deepStrictEqual(SPR.basePose({stam:10,activeWeapon:{weaponKey:"Kenjutsu"}}),{state:"twoHandGuard",weapon:"katana"});
// four-direction facing on the dominant screen axis; hitReact (E/W only) keeps to its rows
assert.equal(SPR.faceToward({x:0,y:0},{x:10,y:3}),"E");
assert.equal(SPR.faceToward({x:0,y:0},{x:-3,y:-10}),"N");
assert.equal(SPR.reactFacing("hitReact","N",{x:0,y:0},{x:5,y:-9},def),"W");
assert.equal(SPR.reactFacing("guardBreak","N",{x:0,y:0},{x:5,y:-9},def),"N");
// who gets a rig
assert.ok(SPR.isHumanoid({glyph:"🥊"}));
assert.ok(!SPR.isHumanoid({glyph:"🐻"}));
assert.ok(!SPR.isHumanoid({glyph:"♊",isSummon:true}));
assert.ok(SPR.isHumanoid({glyph:"♊",summonSpecies:{name:"Deer"}}),"a natal summon species does not make the summoner a summon");
const p0={name:"P",faction:0},a1={name:"Ally",faction:0},e1={name:"Foe",faction:1};
assert.equal(SPR.appearanceFor(p0,p0).outfit,"gi");
assert.equal(SPR.appearanceFor(a1,p0).outfit,"blueArmor");
assert.equal(SPR.appearanceFor(e1,p0).outfit,"redArmor");

// --- engine event record over a real fight
AF.setSeed(7);
const mk=(k,fac,cell)=>{const E=AF.ENEMIES[k];return AF.makeFighter({name:E.name+fac,sign:"Leo",stats:E.stats,faction:fac,cell,abilities:AF.enemyLoadout(k),glyph:E.glyph,persona:E.persona,focus:E.focus});};
const a=mk("Boxer",0,AF.hx(-3,0)),b=mk("StreetThug",1,AF.hx(3,0));
const B=new AF.Battle([a,b],AF.makeArena(5));
const seen=new Set();
for(let r=0;r<12&&!B.decided();r++){
  const before=new Map(B.all.map(x=>[x,x.cell]));
  AF.resolveRound(B,[AF.planFor(B,a,0),AF.planFor(B,b,0)]);
  for(const e of B.events){
    seen.add(e.type);assert.equal(e.round,B.round,"events belong to the round just resolved");
    if(e.type==="move"){assert.notStrictEqual(AF.hkey(e.from),AF.hkey(e.to),"no zero-length moves");}
    if(e.type==="hit"){assert.ok(e.by&&e.ab&&typeof e.hp==="number"&&typeof e.guarded==="boolean");}
  }
  // a fighter's moves chain from its pre-round cell to where it ended
  for(const f of B.all){const mv=B.events.filter(e=>(e.type==="move"||e.type==="knock")&&e.who===f);
    if(mv.length){assert.equal(AF.hkey(mv[0].from),AF.hkey(before.get(f)));assert.equal(AF.hkey(mv[mv.length-1].to),AF.hkey(f.cell));}}
  // the replay plan keeps every event exactly once
  const beats=SPR.planBeats(B.events);
  const n=beats.reduce((s,bt)=>s+(bt.moves?bt.moves.length:bt.approach.length+(bt.act?1:0)+bt.reactions.length),0);
  assert.equal(n,B.events.length);
  B.round++;
}
// the fight's history keeps every round in order, each with where everyone stood as it began
assert.equal(B.history.length,B.round-1);
B.history.forEach((h,i)=>{assert.equal(h.round,i+1);assert.equal(h.start.length,B.all.length);
  const next=B.history[i+1];if(next)for(const s of next.start){const mv=h.events.filter(e=>(e.type==="move"||e.type==="knock")&&e.who===s.f);
    if(mv.length)assert.equal(AF.hkey(mv[mv.length-1].to),AF.hkey(s.cell),"a round starts where the last one left each fighter");}});
assert.strictEqual(B.history[B.history.length-1].events,B.events,"the last round's record is the live one");
for(const t of ["move","act","hit"])assert.ok(seen.has(t),`fight produced no ${t} event`);
// an action's own approach is placed before the act it serves
const bt=SPR.planBeats([{type:"move",phase:"action",who:a},{type:"act",who:a},{type:"hit",who:b,by:a}]);
assert.equal(bt.length,1);assert.equal(bt[0].approach.length,1);assert.ok(bt[0].act);assert.equal(bt[0].reactions.length,1);

console.log(JSON.stringify({ok:true,rigStates:Object.keys(def.states).length,sheets,eventTypes:[...seen].sort(),importedFrom:def.source.commit}));
