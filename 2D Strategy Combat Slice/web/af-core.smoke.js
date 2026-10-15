"use strict";

const assert = require("assert");
global.window = global;
require("./af-core.js");
require("./af-dc-model-v3.js");

const AF = global.AF;
const DC = global.AFDC;
assert(AF && typeof AF.buildChart === "function", "AF core did not load");
assert(DC && typeof DC.resolveCandidateSave === "function", "AF DC live model did not load");
assert.strictEqual(AF.BAL.useCandidateDcModel,true,"candidate DC must be the live V3.4 default");
assert.strictEqual(AF.BAL.useCandidateEconomy,true,"candidate economy must be the live V3.4 default");

AF.setSeed(42);
AF.resetIds();

/* -------------------------------------------------------------------------
   DC / CC / DOT SHADOW MODEL
   This is intentionally not wired into live applyStatus yet. It proves the
   candidate math against the real Sign + Universal + Martial + Weapon catalog.
   ------------------------------------------------------------------------- */
const roster=[];
for(const sign of AF.SIGNS)roster.push(...AF.zodiacAbilities(sign));
roster.push(...AF.generalArts());
for(const style of Object.values(AF.MARTIAL))roster.push(style.stance,...style.moves);
for(const kit of Object.values(AF.WEAPONS))roster.push(kit.stance,...kit.moves);
assert(roster.length>=160,"DC test roster unexpectedly lost a large content family");

const hostileStatusAbilities=roster.filter(ab=>["SingleEnemy","PointRadius"].includes(ab.targeting)&&(ab.effects||[]).some(e=>DC.statusTier(e)));
assert(hostileStatusAbilities.length>=55,"Expected the full cross-kit hostile Status/DOT roster to be under shadow audit");
const harmfulEffects=hostileStatusAbilities.flatMap(ab=>(ab.effects||[]).filter(e=>DC.statusTier(e)).map(e=>({ab,e})));
assert(harmfulEffects.length>=hostileStatusAbilities.length,"Every audited ability should contribute at least one harmful tiered effect");
for(const {ab,e} of harmfulEffects){
  assert(DC.statusTier(e),`${ab.name} / ${e.status} is missing a DC tier`);
  assert(DC.saveStat(e),`${ab.name} / ${e.status} has no authored or provisional save-stat identity`);
}
const automaticHostileRiders=harmfulEffects.filter(({e})=>!e.save);
for(const {ab,e} of automaticHostileRiders){
  const test=DC.candidateStatusCheck(ab,e,{STR:20,AGI:20,FORT:20,INT:20,CHA:20},{STR:20,AGI:20,FORT:20,INT:20,CHA:20},10);
  assert(test&&test.saveStat,`${ab.name} / ${e.status} automatic rider cannot be normalized by the candidate model`);
}

// Owner-approved equal-investment L0 post-hit baselines.
assert.strictEqual(DC.exactLandingRate("C",20,20,0),0.60);
assert.strictEqual(DC.exactLandingRate("B",20,20,0),0.45);
assert.strictEqual(DC.exactLandingRate("A",20,20,0),0.35);
assert.strictEqual(DC.exactLandingRate("S",20,20,0),0.30);
// Candidate ability mastery: +2 DC by L10.
assert.strictEqual(DC.exactLandingRate("C",20,20,10),0.70);
assert.strictEqual(DC.exactLandingRate("B",20,20,10),0.55);
assert.strictEqual(DC.exactLandingRate("A",20,20,10),0.45);
assert.strictEqual(DC.exactLandingRate("S",20,20,10),0.40);
// Career-stat scaling anchor: +/-27 relevant-stat edge -> +/-5 DC before cap.
assert.strictEqual(DC.exactLandingRate("S",47,20,10),0.65);
assert.strictEqual(DC.exactLandingRate("S",20,47,10),0.15);
assert.strictEqual(DC.resolveCandidateSave({tier:"S",attackerStat:100,defenderStat:1,abilityLevel:10,roll:20}).landed,false,"Natural 20 must always resist");
assert.strictEqual(DC.resolveCandidateSave({tier:"S",attackerStat:1,defenderStat:100,abilityLevel:0,roll:1}).landed,true,"Natural 1 must always fail the save");

const liveKit=AF.buildLoadout({signs:["Aries"],martials:["Karate"],weapon:"Kenjutsu"});
assert(!liveKit.some(a=>a.name==="Palm Healing"||a.name==="Cellular Activation"),"normal loadouts must not automatically learn healing");
assert.strictEqual(liveKit.find(a=>a.name==="Sweeping Low").stam,20,"live S-rider stamina floor must apply");
assert.strictEqual(liveKit.find(a=>a.name==="Hilt Bash").slots,2,"live S-rider slot pressure must apply");
const learnedKit=AF.buildLoadout({signs:["Aries"],learnedMedical:["Palm Healing"]}),livePalm=learnedKit.find(a=>a.name==="Palm Healing");
assert(livePalm&&livePalm.maxR===1&&livePalm.healOutputMult===0.70,"learned Palm must be adjacent range at 70% output");

const byName=name=>roster.find(ab=>ab.name===name);
const effect=(name,status)=>byName(name).effects.find(e=>e.status===status);
const viper=byName("Viper Strike");
const viperBleed=effect("Viper Strike","Bleed");
assert.strictEqual(viperBleed.save,undefined,"Viper Strike is expected to remain a legacy automatic rider until live DC integration");
const viperShadow=DC.candidateStatusCheck(viper,viperBleed,{AGI:20},{AGI:20},12);
assert.strictEqual(viperShadow.tier,"C");
assert.strictEqual(viperShadow.saveStat,"AGI");
assert.strictEqual(viperShadow.automaticInLegacy,true);
assert.strictEqual(viperShadow.landed,true,"Equal-stat C rider should land on d20 12 under candidate DC 13");
assert.strictEqual(DC.statusTier(effect("Hidden Mist","Stealth")),null,"Beneficial/self states must not be forced through harmful DC tiers");
assert.strictEqual(DC.primaryTier(byName("Clinch")),null,"Grapples stay on their separate contest lane");

// Slot pressure anchors.
assert.strictEqual(DC.candidateSlots(byName("Elbow Strike"),"C"),1);
assert.strictEqual(DC.candidateSlots(byName("Calf Kick"),"B"),1);
assert.strictEqual(DC.candidateSlots(byName("Heavenly Kick"),"S"),2);
assert.strictEqual(DC.candidateSlots(byName("Killing Intent"),"S"),3);
assert.strictEqual(DC.candidateSlots(byName("Sweeping Low"),"S"),1,"Sweeping Low keeps the approved one-slot Karate exception");
assert.strictEqual(DC.candidateSlots(byName("Hilt Bash"),"S"),2);

// Resolver-true resource-floor anchors. Elemental x1.75 is counted once.
assert.strictEqual(DC.candidateResource(byName("Viper Strike"),"C").suggestedAuthored,10);
assert.strictEqual(DC.candidateResource(byName("Calf Kick"),"B").suggestedAuthored,12);
assert.strictEqual(DC.candidateResource(byName("Sweeping Low"),"S").suggestedAuthored,20);
assert.strictEqual(DC.candidateResource(byName("Hilt Bash"),"S").suggestedAuthored,25);
assert.strictEqual(DC.candidateResource(byName("Shatter Punch"),"S").suggestedAuthored,25);
assert.strictEqual(DC.candidateResource(byName("Killing Intent"),"S").suggestedAuthored,45,"Pure S Genjutsu pays the provisional higher Chakra floor");
const mausoleum=DC.candidateResource(byName("Mausoleum"),"S");
assert.strictEqual(mausoleum.currentEffective,39,"Mausoleum resolver-true Chakra spend should include Elemental x1.75");
assert.strictEqual(mausoleum.suggestedAuthored,22,"Do not double-charge an Elemental S rider already above the effective floor");


// Real resolver integration: legacy authored DC remains the default; candidate path is opt-in.
function runSingleStatusAbility(ab,useCandidate,stats={STR:20,AGI:20,FORT:20,INT:20,CHA:20},rng=()=>0){
  const attacker=AF.makeFighter({name:"DC Attacker",sign:"Aries",stats:{...stats},faction:0,cell:AF.hx(0,0),abilities:[ab]});
  const defender=AF.makeFighter({name:"DC Defender",sign:"Taurus",stats:{...stats},faction:1,cell:AF.hx(1,0),abilities:[]});
  const B=new AF.Battle([attacker,defender],AF.makeArena(3));
  AF.BAL.useCandidateDcModel=useCandidate;AF.setRNG(rng);
  AF.resolveRound(B,[{owner:attacker,actions:[{ability:ab,target:defender}],moveTo:null},{owner:defender,actions:[],moveTo:null}]);
  return{B,attacker,defender};
}
const killingIntentBase=byName("Killing Intent");
const killingIntent={...killingIntentBase,effects:killingIntentBase.effects.map(e=>e.status==="Stun"?{...e,dur:2}:{...e})}; // test-only clone survives postRound for inspection
const legacyStun=runSingleStatusAbility(killingIntent,false);
assert.strictEqual(AF.hasStatus(legacyStun.defender,"Stun"),false,"Legacy fixed DC should still resist at STR 20 on natural 1");
const candidateStun=runSingleStatusAbility(killingIntent,true);
assert.strictEqual(AF.hasStatus(candidateStun.defender,"Stun"),true,"Candidate natural 1 must land S-tier Stun at equal stats");
assert(candidateStun.B.log.some(x=>String(x.calc||"").includes("Candidate save vs Stun")),"Candidate resolver path should identify itself in combat calculation logs");
assert.strictEqual(candidateStun.defender.statuses.find(s=>s.kind==="Stun").breakDC,7,"Candidate S-tier equal-stat L0 Stun should seed breakDC from candidate DC 7");

// Legacy automatic rider normalization. Sequence: initiative=1, attack roll=0%, save=nat20.
const viperSeq=()=>{const q=[0,0,0.999999];return()=>q.length?q.shift():0;};
const legacyBleed=runSingleStatusAbility(viper,false,undefined,viperSeq());
assert.strictEqual(AF.hasStatus(legacyBleed.defender,"Bleed"),true,"Legacy Viper Strike Bleed should remain automatic while candidate mode is off");
const candidateBleed=runSingleStatusAbility(viper,true,undefined,viperSeq());
assert.strictEqual(AF.hasStatus(candidateBleed.defender,"Bleed"),false,"Candidate natural 20 should resist Viper Strike's formerly automatic C-tier Bleed");
AF.BAL.useCandidateDcModel=true;AF.setSeed(42);


// Provisional test-only control-stat identity anchors.
assert.strictEqual(DC.controlStat(byName("Killing Intent"),effect("Killing Intent","Stun")),"CHA","Genjutsu control uses CHA in the test schema");
assert.strictEqual(DC.controlStat(byName("Mausoleum"),effect("Mausoleum","Stun")),"INT","Ninjutsu control uses INT in the test schema");
assert.strictEqual(DC.controlStat(byName("Sweeping Low"),effect("Sweeping Low","Prone")),"AGI","finesse physical control uses AGI");
assert.strictEqual(DC.controlStat(byName("Hilt Bash"),effect("Hilt Bash","Stun")),"STR","force physical control uses STR");
assert.strictEqual(DC.controlStat(byName("Flash Bomb"),effect("Flash Bomb","Blind")),"INT","Trap control uses INT");

// AI planner regression: a damaging rider must receive both damage and status value.
const cleanPlannerAb={...byName("Viper Strike"),id:"planner-clean",name:"Planner Clean",effects:byName("Viper Strike").effects.filter(e=>e.k!=="Status").map(e=>({...e})),tags:[]};
const riderPlannerAb={...byName("Viper Strike"),id:"planner-rider",name:"Planner Rider",effects:byName("Viper Strike").effects.map(e=>({...e,save:e.save?{...e.save}:undefined})),tags:[]};
const plannerActor=AF.makeFighter({name:"Planner Actor",sign:"Aries",stats:{STR:20,AGI:20,FORT:20,INT:20,CHA:20},faction:0,cell:AF.hx(0,0),abilities:[cleanPlannerAb,riderPlannerAb]});
const plannerFoe=AF.makeFighter({name:"Planner Foe",sign:"Taurus",stats:{STR:20,AGI:20,FORT:20,INT:20,CHA:20},faction:1,cell:AF.hx(1,0),abilities:[]});
const plannerBattle=new AF.Battle([plannerActor,plannerFoe],AF.makeArena(3));
AF.BAL.useCandidateDcModel=true;AF.setSeed(77);
const riderPlan=AF.planFor(plannerBattle,plannerActor,0);
assert(riderPlan.actions.length&&riderPlan.actions[0].name==="Planner Rider","AI must value a damaging status rider above otherwise identical clean damage");
AF.BAL.useCandidateDcModel=true;AF.setSeed(42);

AF.resetIds(); // keep the original deterministic combat smoke independent of audit construction.

const chart = AF.buildChart(Date.UTC(1990, 5, 15, 14, 30), 40.71, -74.01);
assert.strictEqual(chart.placements.Sun.sign, "Gemini");

const loadout = AF.chartToLoadout(chart);
assert(loadout.unlockedSigns.length >= 5, "Chart unlocks unexpectedly sparse");
assert(loadout.summonSpecies?.name, "Chart summon is missing");

const grid = AF.makeArena(5);
assert.strictEqual(grid.cells().length, 91, "Radius-5 arena must contain 91 cells");

grid.set(AF.hx(0, 0), "Wall", 3, 30);
assert.strictEqual(grid.blocksMove(AF.hx(0, 0)), true);
assert.strictEqual(grid.blocksSight(AF.hx(0, 0)), true);
assert.strictEqual(grid.los(AF.hx(-2, 0), AF.hx(2, 0)), false, "Wall must block LoS");

grid.set(AF.hx(0, 0), "Open");
assert.strictEqual(grid.los(AF.hx(-2, 0), AF.hx(2, 0)), true, "Open line must restore LoS");

const player = AF.makeFighter({
  name: "You",
  sign: loadout.sun,
  stats: { STR: 9, AGI: 10, FORT: 9, INT: 8, CHA: 8 },
  faction: 0,
  cell: AF.hx(-4, 2),
  abilities: AF.buildLoadout({
    signs: loadout.unlockedSigns,
    martial: "MuayThai",
    weapon: "Kenjutsu",
    eye: "Sun",
    bloodline: "Blaze",
  }),
  isPlayer: true,
  summonSpecies: loadout.summonSpecies,
});

const enemyTemplate = AF.ENEMIES.Sorcerer;
const enemy = AF.makeFighter({
  name: enemyTemplate.name,
  sign: "Leo",
  stats: enemyTemplate.stats,
  faction: 1,
  cell: AF.hx(4, -2),
  abilities: AF.enemyLoadout("Sorcerer"),
  glyph: enemyTemplate.glyph,
  focus: enemyTemplate.focus,
  persona: enemyTemplate.persona,
});

AF.generateTerrain(grid, [player.cell, enemy.cell]);
const battle = new AF.Battle([player, enemy], grid);

const reachable = grid.reachable(
  player.cell,
  AF.DR.mc(AF.eff(player)),
  (cell) => battle.occupied(cell, player),
);
assert(reachable.cells.size > 1, "Player must have reachable movement cells");

let rounds = 0;
while (!battle.decided() && rounds < 40) {
  const playerPlan = AF.planFor(battle, player, 0.1);
  playerPlan.owner = player;
  const otherPlans = battle.all
    .filter((fighter) => fighter !== player && AF.alive(fighter))
    .map((fighter) => AF.planFor(battle, fighter, 0.1));

  AF.resolveRound(battle, [playerPlan, ...otherPlans]);
  rounds += 1;
  battle.round += 1;
}

assert(battle.decided(), "Battle did not resolve within 40 rounds");
assert(battle.log.length > 0, "Combat log stayed empty");

console.log(JSON.stringify({
  ok: true,
  dcShadowModel: {
    roster: roster.length,
    hostileStatusAbilities: hostileStatusAbilities.length,
    harmfulEffects: harmfulEffects.length,
    automaticHostileRiders: automaticHostileRiders.length,
    equalL0: { C: .60, B: .45, A: .35, S: .30 },
  },
  sun: loadout.sun,
  moon: loadout.moon,
  rising: loadout.rising,
  unlockedKits: loadout.unlockedSigns.length,
  summon: loadout.summonSpecies,
  arenaCells: grid.cells().length,
  rounds,
  winner: AF.alive(player) ? player.name : enemy.name,
  logEntries: battle.log.length,
}, null, 2));