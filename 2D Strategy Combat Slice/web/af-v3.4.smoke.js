"use strict";
const assert=require("assert");
const fs=require("fs");
global.window=global;
require("./af-core.js");
require("./af-dc-model-v3.js");
require("./af-core-v3-patch.js");
require("./af-ui-v3.js");
require("./af-map-v3.js");
require("./af-progression-v3.js");
const {AF,AFUI}=global;

assert.equal(AF.BAL.statBaseValue,6);
assert.equal(AF.BAL.statPointsAtLevel1,14);
assert.equal(AF.BAL.statPointsPerLevel,5);
assert.deepStrictEqual(AF.BAL.statCostTierThresholds,[20,30,40,50]);
assert.deepStrictEqual(AF.BAL.statCostTierCosts,[1,2,3,4,5]);
assert.equal(AF.VERSION,"2d-v3.5");
assert.equal(AFUI.VERSION,"2d-v3.5");
assert.equal(AF.BAL.useCandidateDcModel,true);
assert.equal(AF.BAL.useCandidateEconomy,true);

assert.equal(AFUI.statBudget(1),14);
assert.equal(AFUI.statBudget(20),109);
assert.equal(AFUI.statBudget(100),509);
assert.deepStrictEqual([19,20,29,30,39,40,49,50].map(AFUI.marginalStatCost),[1,2,2,3,3,4,4,5]);
assert.deepStrictEqual([20,30,40,50,100].map(AFUI.statValueCost),[14,34,64,104,354]);

const level1={STR:9,AGI:9,FORT:9,INT:9,CHA:8};
assert.deepStrictEqual(AFUI.statBudgetState(1,level1),{level:1,normalized:level1,budget:14,spent:14,remaining:0,overspent:0,valid:true});
const sameAt20=AFUI.statBudgetState(20,level1);
assert.equal(sameAt20.budget,109);assert.equal(sameAt20.spent,14);assert.equal(sameAt20.remaining,95);

for(const level of [1,2,10,20,45,100]){
  const row=AFUI.evenStatBuild(level),state=AFUI.statBudgetState(level,row);
  assert(state.valid,`L${level}: even build overspent`);
  assert(state.remaining>=0,`L${level}: negative remaining`);
  const affordable=AFUI.STAT_NAMES.some(name=>row[name]<AFUI.STAT_MAX_VALUE&&AFUI.marginalStatCost(row[name])<=state.remaining);
  assert(!affordable,`L${level}: affordable point left unspent`);
}
const high=AFUI.evenStatBuild(100),trimmed=AFUI.trimStatsToBudget(1,high);
assert.equal(AFUI.statBudgetState(1,trimmed).spent,14);
assert.deepStrictEqual(AFUI.normalizeStats({STR:1,AGI:101,FORT:9.4,INT:"12",CHA:null}),{STR:6,AGI:100,FORT:9,INT:12,CHA:6});

const canonical={STR:20,AGI:18,FORT:16,INT:15,CHA:14};
AFUI.queueCanonicalPlayerStats(canonical);
const player=AF.makeFighter({name:"Player",sign:"Gemini",stats:AFUI.legacyStatProxy(),faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:[]});
assert.deepStrictEqual(player.stats,canonical);
const npcStats={STR:8,AGI:9,FORT:10,INT:11,CHA:12};
const npc=AF.makeFighter({name:"NPC",sign:"Leo",stats:npcStats,faction:1,cell:AF.hx(1,0),abilities:[]});
assert.deepStrictEqual(npc.stats,npcStats);

// --- Regression: trained martial styles must populate the player loadout ---
// Bug: core buildLoadout only honored a singular opt.martial, but the V3.4 page
// builds loadouts through AFUI.buildPlayerAbilities, which passes a martials[]
// array. The array was ignored, so selecting styles produced ZERO martial
// abilities and the Martial category, stance panels, and child gating were empty.
const martialChart=AF.buildChart(Date.UTC(1990,5,15,14,30)+5*3600000,40.71,-74.01);
const twoStyles=AFUI.buildPlayerAbilities(martialChart,20,{martials:["Boxing","MuayThai"],weapon:"Kenjutsu"});
const stanceKeys=twoStyles.abilities.filter(a=>a.isStyleStance).map(a=>a.styleKey).sort();
assert.deepStrictEqual(stanceKeys,["Boxing","MuayThai"],"Both trained martial stances must be present");
assert(twoStyles.abilities.filter(a=>a.isStyleStance).every(a=>a.tags.includes("MartialStance")&&AFUI.categoryOf(a)==="Martial"),"Martial stances must keep their tag and category");
assert(twoStyles.abilities.some(a=>a.isStyleTechnique&&(a.parentStyles||[]).includes("Boxing")),"Boxing must contribute techniques");
assert(twoStyles.abilities.some(a=>a.isStyleTechnique&&(a.parentStyles||[]).includes("MuayThai")),"Muay Thai must contribute techniques");
const clinch=twoStyles.abilities.filter(a=>a.name==="Clinch");
assert.equal(clinch.length,1,"Shared Clinch technique must be deduped to a single card");
assert(clinch[0].parentStyles.includes("Boxing")&&clinch[0].parentStyles.includes("MuayThai"),"Shared Clinch must list both parent styles");
assert(twoStyles.abilities.some(a=>a.isWeaponStance&&a.weaponKey==="Kenjutsu"),"Weapon stance must be present");
const oneStyle=AFUI.buildPlayerAbilities(martialChart,20,{martials:["Judo"]});
assert(oneStyle.abilities.some(a=>a.isStyleStance&&a.styleKey==="Judo"),"Single trained style must produce its stance");
const trainee=AF.makeFighter({name:"Trainee",sign:"Gemini",stats:{STR:12,AGI:12,FORT:12,INT:10,CHA:10},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:twoStyles.abilities});
const boxStance=trainee.abilities.find(a=>a.isStyleStance&&a.styleKey==="Boxing");
const boxJab=trainee.abilities.find(a=>a.name==="Jab-Cross");
assert(AFUI.dependencyReason(boxJab,trainee,[]),"Technique must be gated before its stance is queued");
assert(!AFUI.dependencyReason(boxJab,trainee,[boxStance]),"Technique must reveal after its stance is queued");


// --- Regression: canonical martial/weapon reconciliation batch 1 ---
const byName=(rows,name)=>rows.find(a=>a.name===name);
const boxing=AF.MARTIAL.Boxing.moves,muay=AF.MARTIAL.MuayThai.moves,jj=AF.MARTIAL.JiuJitsu.moves,wrestling=AF.MARTIAL.Wrestling.moves;
const bob=byName(boxing,"Bob and Weave");
assert.equal(bob.stam,15,"Bob and Weave authored stamina cost");
assert(!bob.effects.some(e=>e.k==="MC"||e.k==="Move"),"Bob and Weave must not grant movement");
assert.deepStrictEqual(bob.effects.find(e=>e.k==="Buff"),{k:"Buff",stat:"AGI",pct:20,dur:1},"Bob and Weave is AGI +20% for one round only");
const bodyShot=byName(boxing,"Body Shot");assert(bodyShot&&bodyShot.effects.some(e=>e.k==="Res"&&e.res==="Stamina"&&e.amt===-10),"Boxing Body Shot must drain 10 stamina");assert(!AF.generalArts().some(a=>a.name==="Solar Plexus Strike"||a.name==="Body Shot"),"General Taijutsu must not duplicate Boxing Body Shot");
assert.equal(byName(boxing,"Haymaker").poiseMult,1.5);assert.equal(byName(boxing,"Haymaker").stam,10,"Guard Break premium is authored directly, not by a hidden floor");
const teep=byName(muay,"Teep Kick"),roundhouse=byName(muay,"Roundhouse Kick"),elbow=byName(muay,"Elbow Strike"),calf=byName(muay,"Calf Kick");assert.equal(teep.effects.find(e=>e.k==="Status").save.stat,"AGI","Teep Kick Slow uses AGI save");
assert(teep.stam>roundhouse.stam&&calf.stam>roundhouse.stam,"Guard Break / Slow Muay Thai moves carry authored stamina premiums over the clean kick");
assert.equal(roundhouse.effects.find(e=>e.k==="Damage").power,12,"canonical Roundhouse Kick power");assert.equal(roundhouse.stam,10);
assert.equal(elbow.stam,10,"canonical Elbow Strike cost (Sheet)");
assert(byName(muay,"Jab-Cross")&&byName(muay,"Uppercut"),"Muay Thai stance children include Jab-Cross and Uppercut");
assert.equal(byName(boxing,"Uppercut").poiseMultWhenGrappling,1.5,"Uppercut is Guard Break only while the user is Grappling");
assert.equal(byName(boxing,"Uppercut").poiseMult,1,"Uppercut carries no unconditional Guard Break");
assert(byName(jj,"Arm bar"),"Jiu-Jitsu Arm bar must exist");
assert.equal(byName(jj,"Strangle").stam,11);assert.equal(byName(jj,"Arm bar").stam,11,"Jiu-Jitsu submission stamina costs were cut ~25% as part of the grappling-parity pass (2026-08-15)");
assert.equal(byName(jj,"Strangle").effects.find(e=>e.k==="GrappleTech").status,"Silence","Strangle applies Silence, not Sleep");
const batchSingleLeg=byName(wrestling,"Single Leg Shot");assert.equal(batchSingleLeg.reach,2);assert(!batchSingleLeg.tags.includes("Priority"));assert(!batchSingleLeg.effects.some(e=>e.k==="Buff"&&e.stat==="AGI"));
// Wrestling keeps Sumo Palm. It is NOT renamed to Iron Fist. Its True damage type was
// dropped (2026-08-15, owner call): it is now Physical, so it is mitigated by the target's
// STR and — as an unavoidable consequence of the type switch — now deals poise damage at
// the standard 1.0 ratio (previously 0.0). Kept intentionally low-power to offset that.
const sumo=byName(wrestling,"Sumo Palm");assert.equal(sumo.dmg,"Physical");assert.equal(sumo.poiseMult,1);assert.equal(sumo.stam,15,"Sumo Palm's stamina cost was raised as part of the grappling-parity pass (2026-08-15)");assert.equal(sumo.slots,2,"Sumo Palm now costs 2 action slots, capping its per-round throughput");assert.equal(sumo.effects.find(e=>e.k==="Damage").power,8,"Sumo Palm power raised 5->8 as part of the Candidate-3 balance baseline (2026-08-15)");
assert(!byName(wrestling,"Iron Fist"),"Iron Fist is the Taurus Sign ability, never the Wrestling technique");
// Exactly one ability named Wrestling Stance, and Wrestler's Prowess is a separate technique.
assert.equal(AF.MARTIAL.Wrestling.stance.name,"Wrestling Stance");
assert.equal(wrestling.filter(a=>a.name==="Wrestling Stance").length,0,"Wrestling Stance must not be duplicated as a technique");
const prowess=byName(wrestling,"Wrestler's Prowess");assert(prowess&&prowess.stam===15);
assert.deepStrictEqual(prowess.effects.find(e=>e.k==="Buff"),{k:"Buff",stat:"STR",pct:20,dur:1},"Wrestler's Prowess is STR +20% for 1 round");
const chokeSlam=byName(wrestling,"Choke Slam");assert(chokeSlam&&chokeSlam.slots===2&&chokeSlam.stam===40,"Choke Slam's stamina cost was cut 50->40 (2026-08-17 grappling-parity pass) to bring it in line with Cross Choke's cost-for-power");assert.equal(chokeSlam.poiseMult,2);
assert.equal(chokeSlam.effects.find(e=>e.k==="Damage").power,32,"Choke Slam's power raised as the heavy-hitting counterpart to the lighter Hip Toss (2026-08-15)");
const karate=AF.MARTIAL.Karate.moves;
const blitz=byName(karate,"Karate Blitz");assert.equal(blitz.reach,2);assert(blitz.tags.includes("Priority"));assert(!blitz.effects.some(e=>e.k==="Status"&&e.status==="Stagger"),"Karate Blitz must not carry Stagger");
const sideKick=byName(karate,"Side Kick");assert.equal(sideKick.effects.find(e=>e.k==="Damage").power,10,"Side Kick power raised 8->10 as part of the Karate damage pass (2026-08-17)");assert.equal(sideKick.stam,10);assert(!sideKick.reach,"Side Kick is a clean melee basic attack, not a reach move");
assert.deepStrictEqual(sideKick.effects.find(e=>e.k==="Push"),{k:"Push",tiles:1},"Side Kick pushes the target back 1 tile on a landed hit, unconditional on any save (2026-08-17)");
const groundAndPound=byName(wrestling,"Ground and Pound");assert.equal(groundAndPound.effects.find(e=>e.k==="Res"&&e.res==="Stamina")?.amt,-12,"Ground and Pound saps 12 Stamina on hit (2026-08-17, owner call)");
// Horse Stance is a Karate child (Sheet); Karate Defensive Stance stays REMOVED.
assert.equal(byName(karate,"Horse Stance").stam,15,"Horse Stance owner-approved stamina cost");
assert(!byName(karate,"Defensive Stance"),"Karate Defensive Stance must never be restored");
assert(byName(boxing,"Defensive Stance"),"Boxing Defensive Stance remains");
assert(byName(karate,"Whirlwind Kick"),"Karate stance children include Whirlwind Kick");
assert.equal(byName(karate,"Sweeping Low").effects.find(e=>e.k==="Damage").power,7,"Sweeping Low power raised 5->7 as part of the Karate damage pass (2026-08-17) — kept modest since its job is the Prone opener, not raw damage");
assert.equal(byName(karate,"Sweeping Low").stam,20,"canonical Sweeping Low stamina floor — deliberately untouched by the damage pass");
assert.equal(byName(muay,"Knee Strikes").stam,30,"Guard Break clinch attack must cost more than Dirty Boxing at 25");
const judo=AF.MARTIAL.Judo.moves;
// Hip Toss was redesigned (2026-08-15) into a Choke Slam-shaped clean strike: lighter power,
// but a better Stamina-per-power ratio than Choke Slam (1.0 vs 1.56), and no longer inflicts
// Prone or breaks the hold on use.
assert.equal(byName(judo,"Hip Toss").stam,22,"Hip Toss Stamina cost raised to 22 as part of the Candidate-3 balance baseline (2026-08-15)");
assert.equal(byName(judo,"Hip Toss").slots,1);
assert.equal(byName(judo,"Hip Toss").effects.find(e=>e.k==="Damage").power,15,"Hip Toss power sits below Choke Slam's 32");
assert(!byName(judo,"Hip Toss").effects.some(e=>e.k==="GrappleTech"),"Hip Toss no longer routes through the GrappleTech contest");
// Hip Toss per the abilities sheet ("Prone 1rd; breaks the hold") and the user's landing ruling (2026-10-15): a landed
// Hip Toss puts the target Prone in the cell behind the user and ends the hold.
{const tk=byName(judo,"Hip Toss").effects.find(e=>e.k==="Takedown");assert(tk&&tk.status==="Prone"&&tk.dur===1&&tk.behind===1,"Hip Toss carries the Prone takedown behind the user");}
assert.equal(byName(judo,"Hip Toss").poiseMult,1.5,"Hip Toss carries a standard Guard Break, lighter than Choke Slam's 2x");
const suplex=byName(wrestling,"Suplex");assert(suplex&&suplex.slots===3&&suplex.stam===40,"Suplex's stamina cost was cut 50->40 (2026-08-17 grappling-parity pass)");assert.equal(suplex.poiseMult,1.5,"Suplex is a standard Guard Break — the 2x ceiling is Choke Slam's alone (2026-08-25 correction)");assert(!suplex.poiseCap,"Suplex must not carry its own poiseCap override now that it isn't at the 2x ceiling");
const ken=AF.WEAPONS.Kenjutsu.moves,kyu=AF.WEAPONS.Kyudo.moves,kob=AF.WEAPONS.KyoketsuShoge.moves;
assert(!AF.WEAPONS.Kobudo,"Kobudo is renamed Kyoketsu-Shoge");
const slash=byName(ken,"Kenjutsu Slash");assert.equal(slash.stam,20);assert.equal(slash.effects.find(e=>e.k==="Damage").power,12);assert(slash.effects.some(e=>e.k==="Status"&&e.status==="Bleed"&&e.save.stat==="AGI"&&e.save.dc===12));
const parry=byName(ken,"Parry");assert.equal(parry.stam,35);assert(parry.effects.some(e=>e.k==="WardNext"),"Parry must arm one targeted-hostile negate");
const thrust=byName(ken,"Precision Thrust");assert.equal(thrust.dmg,"True");assert.equal(thrust.poiseMult,1.5);assert.equal(thrust.stam,25);assert.equal(byName(ken,"Hilt Bash").stam,25,"Guard Break + Stun must visibly carry both balance premiums");
const rain=byName(kyu,"Arrow Rain");assert(rain&&rain.targeting==="PointRadius"&&rain.radius===2&&rain.slots===2&&rain.stam===25,"Kyudo Arrow Rain must be a 2-tile ground AoE");
// Kyoketsu-Shoge canonical kit: Blade Throw / Kusari Chain Snare / Chain Yank / Sickle Strike / Cord Garrote.
assert(!byName(kob,"Shuriken Throw"),"Shuriken Throw is not part of the canonical Kyoketsu-Shoge kit");
const bladeThrow=byName(kob,"Blade Throw");assert(bladeThrow.effects.some(e=>e.k==="Status"&&e.status==="Bleed"),"Blade Throw carries its authored Bleed");assert.equal(bladeThrow.stam,15);
const sickle=byName(kob,"Sickle Strike");assert(sickle&&sickle.stam===15&&sickle.effects.find(e=>e.k==="Damage").power===8);
const garrote=byName(kob,"Cord Garrote");assert(garrote&&garrote.slots===2&&garrote.stam===25);
assert(garrote.effects.some(e=>e.k==="GrappleTech"&&e.submission&&e.focusLock>0),"Cord Garrote is a Maintained Submission that denies Focus");

// Parry behavior: a fast defender arms the ward; the next hostile single-target
// ability is canceled, then the ward is consumed so a later attack can land.
// (Uppercut, not Jab-Cross: Jab-Cross is a System 3 Combo ability now and deliberately does
// NOT get fully negated by a single Parry charge — see the dedicated test further down. This
// generic-negation test needs an ordinary single-strike ability instead.)
AF.setRNG(()=>0);
const parryDef=AF.makeFighter({name:"Parrier",sign:"Libra",stats:{STR:10,AGI:40,FORT:20,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[parry]});
const parryAtkAb={...byName(boxing,"Uppercut"),id:"parry-test-uppercut",effects:byName(boxing,"Uppercut").effects.map(e=>({...e})),tags:[]};
const parryAtk=AF.makeFighter({name:"Attacker",sign:"Aries",stats:{STR:20,AGI:20,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[parryAtkAb]});
const parryBattle=new AF.Battle([parryDef,parryAtk],AF.makeArena(5));const hpBeforeParry=parryDef.hp;
AF.resolveRound(parryBattle,[{owner:parryDef,actions:[parry],moveTo:null},{owner:parryAtk,actions:[parryAtkAb],moveTo:null}]);
assert.equal(parryDef.hp,hpBeforeParry,"Parry must negate the next hostile targeted ability");assert.equal(parryDef.wardNext,0,"Parry ward must be consumed once");assert(parryBattle.log.some(x=>x.text.includes("parries")),"Parry cancellation must be visible in combat log");
parryBattle.round++;AF.resolveRound(parryBattle,[{owner:parryDef,actions:[],moveTo:null},{owner:parryAtk,actions:[parryAtkAb],moveTo:null}]);
assert(parryDef.hp<hpBeforeParry,"After the ward is consumed, a later targeted attack can damage the defender");
AF.setSeed(0xC0FFEE);

// --- Regression: queued Focus restores fund later actions in the planner ---
// The affordability gate must credit a queued Catch Breath / Charge Chakra restore,
// in queue order, so the player can plan a Focus -> expensive-move combo (which the
// engine already resolves successfully because restores apply mid-round).
const focusChart=AF.buildChart(Date.UTC(1990,5,15,14,30)+5*3600000,40.71,-74.01);
const focusKit=AFUI.buildPlayerAbilities(focusChart,20,{martials:["Boxing"]});
const planner=AF.makeFighter({name:"Planner",sign:"Gemini",stats:{STR:12,AGI:12,FORT:12,INT:10,CHA:10},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:focusKit.abilities});
const catchBreath=planner.abilities.find(a=>a.name==="Catch Breath");
// A stamina move that is NOT dependency-gated, so only resources can block it.
const move=planner.abilities.find(a=>a.stam>0&&!a.tags.includes("Focus")&&a.targeting!=="Self"&&!AFUI.dependencyReason(a,planner,[]));
assert(catchBreath&&move,"Setup: Catch Breath and an ungated stamina move must be in the loadout");
// Canonical Focus: 20% of the channel's max pool, and NO poise.
const cbEffect=catchBreath.effects.find(e=>e.k==="Res"&&e.res==="Stamina")||{};
assert.equal(cbEffect.pct,AF.BAL.focusRestorePercent,"Catch Breath restores 20% of max Stamina");
assert(!catchBreath.effects.some(e=>e.k==="Res"&&e.res==="Poise"),"Focus actions grant no Poise");
const chargeChakra=planner.abilities.find(a=>a.name==="Charge Chakra");
assert.equal((chargeChakra.effects.find(e=>e.k==="Res"&&e.res==="Chakra")||{}).pct,AF.BAL.focusRestorePercent,"Charge Chakra restores 20% of max Chakra");
assert(!chargeChakra.effects.some(e=>e.k==="Res"&&e.res==="Poise"),"Focus actions grant no Poise");
const cbRestore=(cbEffect.amt||0)+Math.round(planner.maxStam*(cbEffect.pct||0));
assert(cbRestore>0,"Catch Breath must restore stamina");
const moveCost=Math.round(move.stam*AF.costMult(move));
planner.stam=0;
assert(AFUI.lockReason(move,planner,[]),`${move.name} must be blocked with no stamina and nothing queued`);
assert(!AFUI.lockReason(move,planner,[catchBreath]),"Queuing Catch Breath first must unlock the move");
// Running deduction is order-aware: after one Catch Breath funds one move, a second
// copy is gated unless the single restore covered both.
const fundsTwo=cbRestore>=2*moveCost;
assert.equal(!!AFUI.lockReason(move,planner,[catchBreath,move]),!fundsTwo,"Second move gating must reflect remaining restored stamina");
// A restore does not appear from thin air: with an empty queue the gate is unchanged.
planner.stam=moveCost;
assert(!AFUI.lockReason(move,planner,[]),"Move must be allowed when current stamina already covers it");

// --- Regression: Slice 1 progression (ability/character XP + level scaling) ---
const progChart=AF.buildChart(Date.UTC(1990,5,15,14,30)+5*3600000,40.71,-74.01);
// Ability-level XP curve: triangular thresholds, capped.
assert.equal(AFUI.abilityLevelFromXp(0),0);
assert.equal(AFUI.abilityLevelFromXp(AFUI.abilityXpToReach(1)),1);
assert.equal(AFUI.abilityLevelFromXp(AFUI.abilityXpToReach(1)-1),0);
assert.equal(AFUI.abilityLevelFromXp(AFUI.abilityXpToReach(AF.BAL.abilityLevelCap)),AF.BAL.abilityLevelCap);
assert.equal(AFUI.abilityLevelFromXp(1e9),AF.BAL.abilityLevelCap,"ability level must cap");

// A zero-XP progress profile must not change any ability (backward compatible).
const noProg=AFUI.buildPlayerAbilities(progChart,20,{martials:["Boxing"]});
const zeroProg=AFUI.buildPlayerAbilities(progChart,20,{martials:["Boxing"],progress:AFUI.newProgress()});
assert(!noProg.abilities.some(a=>a.name==="Palm Healing"||a.name==="Cellular Activation"),"healing must be learned, not automatic");
const supportNoProg=AFUI.buildPlayerAbilities(progChart,20,{martials:["Boxing"],learnedMedical:["Palm Healing"]});
const snap=a=>a.map(x=>({k:AF.abilityKey(x),stam:x.stam,chakra:x.chakra,pow:(x.effects.find(e=>e.k==="Damage"||e.k==="Heal")||{}).power}));
assert.deepStrictEqual(snap(zeroProg.abilities),snap(noProg.abilities),"zero-XP progress must be a no-op");

// Offensive scaling: a maxed move gains flat power AND costs more stamina.
function buildLeveled(name,A){
  const base=noProg.abilities.find(a=>a.name===name);
  const prog=AFUI.newProgress();prog.abilityXp[AF.abilityKey(base)]=AFUI.abilityXpToReach(A);
  return AFUI.buildPlayerAbilities(progChart,20,{martials:["Boxing"],progress:prog}).abilities.find(a=>a.name===name);
}
const spx0=noProg.abilities.find(a=>a.name==="Body Shot");
const spxMax=buildLeveled("Body Shot",AF.BAL.abilityLevelCap);
assert(spxMax.effects.find(e=>e.k==="Damage").power>spx0.effects.find(e=>e.k==="Damage").power,"leveled move must hit harder");
assert(spxMax.stam>spx0.stam,"leveled move must cost more stamina");

// Heal rule: never chakra-positive below max, exactly 1:1 at max, baseline swapped.
function palmAt(A){
  const base=supportNoProg.abilities.find(a=>a.name==="Palm Healing");
  const prog=AFUI.newProgress();prog.abilityXp[AF.abilityKey(base)]=AFUI.abilityXpToReach(A);
  const p=AFUI.buildPlayerAbilities(progChart,20,{martials:["Boxing"],learnedMedical:["Palm Healing"],progress:prog}).abilities.find(a=>a.name==="Palm Healing");
  const raw=p.effects.find(e=>e.k==="Heal").power;return{raw,heal:Math.round(raw*(p.healOutputMult??1)),spent:Math.round(p.chakra*AF.costMult(p))};
}
const healCap=AF.BAL.abilityLevelCap;
const palm0=palmAt(0);assert(palm0.spent===25&&palm0.raw===15&&palm0.heal===11,"Palm keeps authored power 15 but resolves at 70% output");
for(let A=0;A<healCap;A++){const {heal,spent}=palmAt(A);assert(heal<spent,`heal must cost more chakra than it restores below max (lvl ${A}: ${heal} vs ${spent})`);}
const palmMax=palmAt(healCap);assert.equal(palmMax.raw,palmMax.spent,"raw mastery curve still reaches 1:1");assert.equal(palmMax.heal,Math.round(palmMax.spent*0.70),"Palm final output stays at 70% after mastery");

// Path A: heal magnitude is decoupled from CHA — same ability heals the same
// regardless of the healer's chakra stat.
function healOutput(cha){
  AF.setSeed(1);AF.resetIds();
  const heal=AFUI.buildPlayerAbilities(progChart,20,{learnedMedical:["Palm Healing"]}).abilities.find(a=>a.name==="Palm Healing");
  const healer=AF.makeFighter({name:"Healer",sign:"Gemini",stats:{STR:6,AGI:6,FORT:6,INT:6,CHA:cha},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:[heal]});
  const ally=AF.makeFighter({name:"Ally",sign:"Leo",stats:{STR:10,AGI:10,FORT:10,INT:6,CHA:6},faction:0,cell:AF.hx(1,0),abilities:[]});
  ally.hp=10;const before=ally.hp;
  AF.resolveRound(new AF.Battle([healer,ally],AF.makeArena(5)),[{owner:healer,actions:[heal],moveTo:null},{owner:ally,actions:[],moveTo:null}]);
  return ally.hp-before;
}
assert.equal(healOutput(6),healOutput(40),"heal output must not scale with CHA");
const palmRange=AFUI.buildPlayerAbilities(progChart,20,{learnedMedical:["Palm Healing"]}).abilities.find(a=>a.name==="Palm Healing");
assert.equal(palmRange.maxR,1,"Palm Healing must be adjacent/melee range");

// minCHA gate: a stat-gated ability is locked until CHA meets the threshold.
const gated=AFUI.buildPlayerAbilities(progChart,20,{learnedMedical:["Palm Healing"]}).abilities.find(a=>a.name==="Palm Healing");gated.minCHA=20;
const lowCHA=AF.makeFighter({name:"Low",sign:"Gemini",stats:{STR:10,AGI:10,FORT:10,INT:10,CHA:12},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:[]});
const hiCHA=AF.makeFighter({name:"Hi",sign:"Gemini",stats:{STR:10,AGI:10,FORT:10,INT:10,CHA:25},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:[]});
assert.equal(AFUI.dependencyReason(gated,lowCHA,[]),"requires CHA 20","below-threshold CHA must gate the ability");
assert(!AFUI.dependencyReason(gated,hiCHA,[]),"meeting the CHA threshold must unlock the ability");

// XP accrual → commit → rebuild is scaled; god-mode commits nothing.
AF.setSeed(3);AF.resetIds();
const career=AFUI.newProgress();
const careerKit=AFUI.buildPlayerAbilities(progChart,20,{martials:["Boxing"],progress:career});
const hero=AF.makeFighter({name:"You",sign:progChart.placements.Sun.sign,stats:{STR:20,AGI:14,FORT:16,INT:10,CHA:12},faction:0,cell:AF.hx(-2,0),isPlayer:true,abilities:careerKit.abilities});
const villain=AF.makeFighter({name:"Foe",sign:"Leo",stats:{STR:10,AGI:8,FORT:20,INT:6,CHA:6},faction:1,cell:AF.hx(2,0),abilities:AF.enemyLoadout("StreetThug")});
const careerBattle=new AF.Battle([hero,villain],AF.makeArena(5));
let cr=0;while(!careerBattle.decided()&&cr<30){const plans=careerBattle.all.filter(AF.alive).map(f=>AF.planFor(careerBattle,f,0.1));AF.resolveRound(careerBattle,plans);careerBattle.round++;cr++;}
assert(careerBattle.xp.get(hero)&&careerBattle.xp.get(hero).size>0,"player must accrue ability XP from combat");
const usedKey=[...careerBattle.xp.get(hero).keys()][0];
const commit=AFUI.commitProgress(careerBattle,career);
assert(commit.committed&&career.charXp>0,"commit must add character XP");
assert(career.abilityXp[usedKey]>0,"a used ability must gain XP");
careerBattle.god=true;
const gp=AFUI.newProgress(),gpBefore=JSON.stringify(gp),godCommit=AFUI.commitProgress(careerBattle,gp);
assert(!godCommit.committed&&JSON.stringify(gp)===gpBefore,"god-mode battles must not award progression");

// --- Regression: Targeting Slice A (explicit, perception-gated target/point) ---
const tChart=AF.buildChart(Date.UTC(1990,5,15,14,30)+5*3600000,40.71,-74.01);
const tKit=AFUI.buildPlayerAbilities(tChart,20,{forceAllKits:true});
const ranged=tKit.abilities.find(a=>a.targeting==="SingleEnemy"&&a.maxR>=4&&a.effects.some(e=>e.k==="Damage")&&a.dmg!=="None"&&!a.tags.includes("Charge")&&!a.tags.includes("Ultimate")&&!a.tags.includes("EyeJutsu")&&!a.tags.includes("RequiresGrapple"));
const aoeAb=tKit.abilities.find(a=>a.targeting==="PointRadius"&&a.effects.some(e=>e.k==="Damage"));
assert(ranged&&aoeAb,"Setup: need a ranged single-enemy and a PointRadius damage ability");
const mkPlayer=cell=>{const p=AF.makeFighter({name:"You",sign:"Gemini",stats:{STR:16,AGI:14,FORT:14,INT:16,CHA:20},faction:0,cell,isPlayer:true,abilities:tKit.abilities});p.stam=999;p.chakra=999;p.supplies=9;return p;};
const mkFoe=(name,fac,cell)=>AF.makeFighter({name,sign:"Leo",stats:{STR:10,AGI:6,FORT:20,INT:6,CHA:6},faction:fac,cell,abilities:[]});
// Explicit target engages the chosen (far) enemy, never the nearest (log-based so it is
// robust to the single-target hit roll; the *selection* is what Slice A changes).
AF.setSeed(7);AF.resetIds();
let tYou=mkPlayer(AF.hx(-2,0)),tNear=mkFoe("Farraday",1,AF.hx(-1,0)),tFar=mkFoe("Zeta",2,AF.hx(2,0));
let tB=new AF.Battle([tYou,tNear,tFar],AF.makeArena(5));
const nearHpBefore=tNear.hp;
AF.resolveRound(tB,[{owner:tYou,actions:[{ability:ranged,target:tFar}],moveTo:null}]);
let tLog=tB.log.map(x=>x.text).join(" ");
assert.equal(tNear.hp,nearHpBefore,"explicit far-target must not touch the nearest enemy");
assert(tLog.includes("Zeta")&&!tLog.includes("Farraday"),"explicit target must engage the chosen enemy, not the nearest");
// No target -> engages the nearest perceivable enemy.
AF.setSeed(7);AF.resetIds();
tYou=mkPlayer(AF.hx(-2,0));tNear=mkFoe("Farraday",1,AF.hx(-1,0));tFar=mkFoe("Zeta",2,AF.hx(2,0));
tB=new AF.Battle([tYou,tNear,tFar],AF.makeArena(5));
AF.resolveRound(tB,[{owner:tYou,actions:[ranged],moveTo:null}]);
assert(tB.log.map(x=>x.text).join(" ").includes("Farraday"),"auto-target must engage the nearest perceivable enemy");
// Perception gating: a stealthed enemy is not a selectable target, but a cell-placed AoE
// still hits and reveals it (AoE resolves without a to-hit roll — deterministic).
AF.setSeed(7);AF.resetIds();
tYou=mkPlayer(AF.hx(-2,0));
const tHid=mkFoe("Ghost",1,AF.hx(1,0));tHid.statuses.push({kind:"Stealth",rounds:99,stacks:1,tick:0,mag:0});
tB=new AF.Battle([tYou,tHid],AF.makeArena(5));
assert(!tB.perceives(tYou,tHid),"a stealthed enemy is not perceived");
assert(tB.nearestPerceivedEnemy(tYou)===null,"a stealthed enemy is absent from the perceivable-target list");
const hidHpBefore=tHid.hp;
AF.resolveRound(tB,[{owner:tYou,actions:[{ability:aoeAb,point:{q:1,r:0}}],moveTo:null}]);
assert(tHid.hp<hidHpBefore&&!AF.hasStatus(tHid,"Stealth"),"cell-placed AoE must hit and reveal a hidden enemy");

// --- Regression: anti-trap terrain generation (all walkable cells stay connected) ---
for(let seed=1;seed<=12;seed++){
  AF.setSeed(seed);
  const grid=AF.makeArena(5);
  const spawns=[AF.hx(-4,2),AF.hx(4,-2),AF.hx(0,4)];
  AF.generateTerrain(grid,spawns);
  const walkable=grid.cells().filter(c=>!grid.blocksMove(c));
  const start=walkable[0],reached=new Set([AF.hkey(start)]),q=[start];
  while(q.length){const cur=q.shift();for(const nb of AF.neighbors(cur)){if(!grid.inBounds(nb)||grid.blocksMove(nb))continue;const k=AF.hkey(nb);if(!reached.has(k)){reached.add(k);q.push(nb);}}}
  assert.equal(reached.size,walkable.length,`seed ${seed}: walkable cells not one connected region (${reached.size}/${walkable.length})`);
  for(const s of spawns)assert(!grid.blocksMove(s)&&reached.has(AF.hkey(s)),`seed ${seed}: a spawn is walled in`);
}

// --- Regression: destructible terrain (damaging AoE fells trees / clears bushes) ---
const dg=AF.makeArena(5);
dg.set(AF.hx(1,0),"Tree");dg.set(AF.hx(2,0),"Bush");dg.set(AF.hx(1,1),"Rock");
assert(dg.blocksMove(AF.hx(1,0))&&dg.blocksSight(AF.hx(1,0)),"a tree blocks move and sight");
const blast=dg.blastTerrain(AF.hx(1,0),1);
assert.equal(dg.terrainAt(AF.hx(1,0)),"FelledTree","tree is felled by the blast");
assert(dg.blocksMove(AF.hx(1,0))&&!dg.blocksSight(AF.hx(1,0)),"a felled tree blocks move but no longer blocks sight");
assert.equal(dg.terrainAt(AF.hx(2,0)),"Open","bush is cleared by the blast");
assert.equal(dg.terrainAt(AF.hx(1,1)),"Rock","rock is not destructible");
assert(blast.trees===1&&blast.bushes===1,"blast reports 1 tree felled and 1 bush cleared");

// --- Regression: Earth Wall placement radius grows with ability level ---
const ewChart=AF.buildChart(Date.UTC(1990,5,15,14,30)+5*3600000,40.71,-74.01);
const ewQuick=AFUI.buildPlayerAbilities(ewChart,20,{forceAllKits:true}).abilities.find(a=>a.name==="Earth Wall");
assert(ewQuick&&ewQuick.effects.some(e=>e.k==="Terrain"&&e.kind==="Wall"),"Setup: Earth Wall places Wall terrain");
function earthWallAt(A){const prog=AFUI.newProgress();prog.abilityXp[AF.abilityKey(ewQuick)]=AFUI.abilityXpToReach(A);
  return AFUI.buildPlayerAbilities(ewChart,20,{forceAllKits:true,progress:prog}).abilities.find(a=>a.name==="Earth Wall");}
assert.equal(earthWallAt(0).radius,0,"Earth Wall at ability level 0 is a single tile (radius 0)");
assert(earthWallAt(AF.BAL.abilityLevelCap).radius===ewQuick.radius&&ewQuick.radius>=2,"Earth Wall at max ability level restores its full authored radius");
assert(earthWallAt(Math.round(AF.BAL.abilityLevelCap/2)).radius>0&&earthWallAt(Math.round(AF.BAL.abilityLevelCap/2)).radius<ewQuick.radius,"Earth Wall radius grows partway at mid level");

// --- Regression: caravan escort (path advance, speed, heavy ranged fire) ---
function escortPath(a,b){const n=AF.hdist(a,b),out=[{...a}];for(let i=1;i<=n;i++){const t=i/n;out.push(AF.cubeRound(a.q+(b.q-a.q)*t,a.r+(b.r-a.r)*t));}return out;}
const carPath=escortPath(AF.hx(-5,0),AF.hx(5,0));
assert.equal(carPath.length,11,"escort path spans the arena");
function mkCaravan(hp,speed,attack){const c=AF.makeFighter({name:"Caravan",sign:"Taurus",stats:{STR:8,AGI:2,FORT:20,INT:6,CHA:6},faction:0,cell:{...carPath[0]},glyph:"C"});c.isCaravan=true;c.maxHp=hp;c.hp=hp;c.path=carPath;c.pathIndex=0;c.speed=speed;c.caravanAttack=attack;return c;}
function roundsToGoal(speed){AF.setSeed(1);AF.resetIds();const car=mkCaravan(1000,speed,null),B=new AF.Battle([car],AF.makeArena(5));let n=0;while(n<40){if(AF.stepCaravan(B,car).reachedGoal){n++;break;}n++;}return n;}
assert.equal(roundsToGoal(1),10,"standard caravan (speed 1) reaches B in 10 rounds");
assert.equal(roundsToGoal(2),5,"light caravan (speed 2) reaches B in 5 rounds");
// heavy caravan fires on an in-range attacker
AF.setSeed(2);AF.resetIds();
const heavy=mkCaravan(1500,1,{power:18,radius:2});
const raider=AF.makeFighter({name:"Raider",sign:"Leo",stats:{STR:10,AGI:6,FORT:20,INT:6,CHA:6},faction:1,cell:AF.hx(-4,0),abilities:[]});
const escB=new AF.Battle([heavy,raider],AF.makeArena(5));
const raiderHp=raider.hp;AF.stepCaravan(escB,heavy);
assert(raider.hp<raiderHp,"heavy caravan fires a bolt at an in-range attacker");
assert(escB.log.some(x=>/Caravan Bolt/.test(x.text)),"heavy caravan fire is logged");
// a standard caravan does not fire
AF.setSeed(2);AF.resetIds();
const std=mkCaravan(1000,1,null),near=AF.makeFighter({name:"R2",sign:"Leo",stats:{STR:10,AGI:6,FORT:20,INT:6,CHA:6},faction:1,cell:AF.hx(-4,0),abilities:[]});
const stdB=new AF.Battle([std,near],AF.makeArena(5));const nHp=near.hp;AF.stepCaravan(stdB,std);
assert.equal(near.hp,nHp,"a standard (unarmed) caravan deals no damage");

// --- Regression: caravan ambush (player attacks an enemy-owned caravan) ---
// The same caravan machinery serves the enemy side: a faction-1 armed caravan fires on a
// faction-0 attacker (the player's side), the mirror of the escort case.
AF.setSeed(2);AF.resetIds();
const foeCar=mkCaravan(1500,1,{power:18,radius:2});foeCar.faction=1;
const raiderP=AF.makeFighter({name:"Ambusher",sign:"Leo",stats:{STR:10,AGI:6,FORT:20,INT:6,CHA:6},faction:0,cell:AF.hx(-4,0),abilities:[]});
const ambB=new AF.Battle([foeCar,raiderP],AF.makeArena(5));
const rpHp=raiderP.hp;AF.stepCaravan(ambB,foeCar);
assert(raiderP.hp<rpHp,"an enemy (faction 1) caravan fires on the player-side attacker");

// --- Regression: a downed player still lets the fight auto-resolve to a winner ---
// (mirrors the page controller's autoResolveDowned loop: hand every live fighter to the AI
//  and play out the round until B.decided(), even though the human can no longer act.)
AF.setSeed(3);AF.resetIds();
const dPlayer=AF.makeFighter({name:"Downed",sign:"Gemini",stats:{STR:10,AGI:10,FORT:10,INT:10,CHA:10},faction:0,cell:AF.hx(-1,0),isPlayer:true,abilities:[]});
const dAlly=AF.makeFighter({name:"Guardian",sign:"Leo",stats:{STR:26,AGI:16,FORT:22,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:AF.enemyLoadout("StreetThug")});
dAlly.stam=999;dAlly.chakra=999;dAlly.maxHp=9999;dAlly.hp=9999;
const dFoe=AF.makeFighter({name:"Marauder",sign:"Leo",stats:{STR:8,AGI:6,FORT:6,INT:6,CHA:6},faction:1,cell:AF.hx(1,0),abilities:AF.enemyLoadout("StreetThug")});
const dB=new AF.Battle([dPlayer,dAlly,dFoe],AF.makeArena(5));
dPlayer.hp=0; // the player is downed
assert(!AF.alive(dPlayer),"player is downed");
assert(!dB.decided(),"with the player down but an ally alive, the battle is NOT yet decided");
let dGuard=0;
while(!dB.decided()&&dGuard++<200){
  const plans=dB.all.filter(f=>AF.alive(f)&&!f.isCaravan).map(f=>AF.planFor(dB,f,0));
  AF.resolveRound(dB,plans);dB.round++;
}
assert(dB.decided(),"the AI-driven loop drives the downed-player battle to a decision");
assert(AF.alive(dAlly)&&!AF.alive(dFoe),"the surviving ally wins the auto-resolved battle for the player's faction");

// --- Regression: reach abilities are gap-closers (lunge to melee), not bonus movement ---
const reachKit=AFUI.buildPlayerAbilities(martialChart,20,{martials:["Wrestling"]});
const sls=reachKit.abilities.find(a=>a.name==="Single Leg Shot");
const wrestleStance=reachKit.abilities.find(a=>a.isStyleStance&&(a.styleKey==="Wrestling"||a.name==="Wrestling Stance"));
assert(sls&&sls.reach>0,"Single Leg Shot carries a reach radius");
const clinchAb=reachKit.abilities.find(a=>a.name==="Clinch");
assert(clinchAb&&!clinchAb.reach,"Clinch stays plain melee (no reach) so Single Leg Shot's reach is worth taking");
assert(!sls.tags.includes("Priority"),"Single Leg Shot no longer has Priority");
assert(!sls.effects.some(e=>e.k==="Buff"&&e.stat==="AGI"),"Single Leg Shot no longer grants an AGI buff");
assert.equal(sls.atk,"Melee","reach abilities land as melee — full accuracy once the lunge connects");
assert(!sls.effects.some(e=>e.k==="MC"||e.k==="Move"),"slotting a reach ability grants no extra movement tiles");
function reachShot(gap,move,flee){
  AF.setSeed(11);AF.resetIds();
  const A=AF.makeFighter({name:"Wrestler",sign:"Aries",stats:{STR:16,AGI:6,FORT:14,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:reachKit.abilities});
  A.activeMartial=wrestleStance; // stance active so the technique is legal
  const D=AF.makeFighter({name:"Runner",sign:"Leo",stats:{STR:10,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(gap,0),abilities:[]});
  const B=new AF.Battle([A,D],AF.makeArena(8));
  AF.resolveRound(B,[{owner:A,actions:[{ability:sls,target:D}],moveTo:move||null},{owner:D,actions:[],moveTo:flee||null}]);
  return{finalGap:AF.hdist(A.cell,D.cell),grappled:AF.hasStatus(D,"Grappled"),lunged:B.log.some(x=>/lunges in/.test(x.text))};
}
const caught=reachShot(sls.reach); // target sitting at the edge of the reach radius
assert.equal(caught.finalGap,1,"reach puts the user adjacent to a target inside the reach radius");
assert(caught.grappled,"the takedown lands (previously the action was stripped as out of range)");
// running target: the wrestler spends movement to close, then the lunge covers the last few tiles
const chased=reachShot(3,AF.hx(2,0),AF.hx(4,0)); // wrestler moves 2 (mc spent), runner flees to 4 -> gap 2 -> lunge
assert(chased.lunged,"the reach lunge fires to catch a runner that movement alone couldn't reach");
assert(chased.grappled&&chased.finalGap===1,"the lunge drags the wrestler into melee on the runner");
const escaped=reachShot(7); // well beyond reach + the wrestler's movement
assert(!escaped.grappled,"a target well beyond reach escapes the takedown");
assert(escaped.finalGap>1,"the wrestler can't catch a target that stayed out of reach");

// --- Regression: Slow / Snare reduce movement (not just initiative), Root stops it ---
(function(){
  const mk=ss=>{const f=AF.makeFighter({name:"M",sign:"Aries",stats:{STR:10,AGI:20,FORT:10,INT:10,CHA:10},faction:0,cell:AF.hx(0,0),abilities:[]});for(const s of ss)f.statuses.push({kind:s,rounds:2,stacks:1,tick:0,mag:0});return f;};
  const base=AF.moveBudget(mk([]));
  assert(base>1,"a healthy fighter has a real movement budget");
  assert.equal(AF.moveBudget(mk(["Slow"])),Math.floor(base*AF.BAL.slowMoveMult),"Slow cuts the movement budget");
  assert(AF.moveBudget(mk(["Slow"]))<base,"a Slowed fighter moves fewer tiles than a healthy one");
  assert.equal(AF.moveBudget(mk(["Root"])),0,"Root stops movement entirely");
  assert(AF.moveBudget(mk(["Slow","Snare"]))<AF.moveBudget(mk(["Slow"])),"Slow and Snare compound");
})();
// --- Regression: the combat log marks the start of each round + notes reduced movement ---
(function(){
  AF.setSeed(5);AF.resetIds();
  const a=AF.makeFighter({name:"A",sign:"Aries",stats:{STR:10,AGI:20,FORT:10,INT:10,CHA:10},faction:0,cell:AF.hx(0,0),abilities:[]});
  a.statuses.push({kind:"Slow",rounds:2,stacks:1,tick:0,mag:0});
  const foe=AF.makeFighter({name:"B",sign:"Leo",stats:{STR:10,AGI:10,FORT:10,INT:10,CHA:10},faction:1,cell:AF.hx(2,0),abilities:[]});
  const B=new AF.Battle([a,foe],AF.makeArena(5));
  AF.resolveRound(B,[{owner:a,actions:[],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(B.log.some(x=>x.cls==="round-sep"&&/Round 1/.test(x.text)),"each resolved round opens with a round separator in the log");
  assert(B.log.some(x=>/is Slowed — movement/.test(x.text)),"a slowed fighter's reduced movement is logged");
})();



/* =====================================================================
   POSITIONAL COMBAT REGRESSION SUITE
   Canonical source: AstroFighters_Abilities Google Sheet → "Positional Rules"
   (relationship legality, DC scaling, maintenance, submissions, Pull Guard,
   Hip Escape, Focus, movement, queue projection, AI legality).
   ===================================================================== */
(function positionalRegression(){
const REL=AF.REL;
const STATS={STR:12,AGI:12,FORT:14,INT:10,CHA:10};
function fighter(name,faction,q,r,abilities,isPlayer){
  return AF.makeFighter({name,sign:"Aries",stats:{...STATS},faction,cell:AF.hx(q,r),abilities:abilities||[],isPlayer:!!isPlayer});
}
function kit(styleKeys,weaponKey){
  return AF.buildLoadout({sign:"Aries",martials:styleKeys||[],weapon:weaponKey||null});
}
const find=(rows,name)=>rows.find(a=>a.name===name);
function mountPair(){
  const a=fighter("Top",0,0,0,[]),b=fighter("Bottom",1,1,0,[]);
  const B=new AF.Battle([a,b],AF.makeArena(5));
  AF.enterMount(B,a,b,{voluntary:false});
  return{a,b,B};
}
/* ---------- 1. state transitions ---------- */
(function stateModel(){
  const a=fighter("Top",0,0,0),b=fighter("Bottom",1,1,0);
  const B=new AF.Battle([a,b],AF.makeArena(5));
  AF.enterStandingGrapple(B,a,b,5);
  assert.equal(AF.relRole(a),REL.GRAPPLING);
  assert.equal(AF.relRole(b),REL.GRAPPLED);
  assert.equal(AF.relPartner(a),b);assert.equal(AF.relPartner(b),a);
  AF.enterMount(B,a,b,{voluntary:false});
  assert.equal(AF.relRole(a),REL.MOUNTING,"grapple->mount promotes the top fighter");
  assert.equal(AF.relRole(b),REL.MOUNTED);
  assert(!AF.hasStatus(a,"Grappling"),"Mount clears Grappling");
  assert(!AF.hasStatus(b,"Grappled"),"Mount clears Grappled");
  assert(!AF.isGrappling(a),"Mounting is NOT automatically Grappling");
  assert.equal(B.all.filter(AF.isMounting).length,1,"exactly one Mounting participant");
  assert.equal(B.all.filter(AF.isMounted).length,1,"exactly one Mounted participant");
  AF.endRelationship(B,a,"test");
  assert.equal(AF.relRole(a),REL.FREE);assert.equal(AF.relRole(b),REL.FREE);
})();

/* ---------- 2. ability legality matrix ---------- */
(function legality(){
  const all=kit(["Boxing","MuayThai","Judo","JiuJitsu","Karate","Wrestling"],"KyoketsuShoge");
  const ken=kit([],"Kenjutsu"),kyu=kit([],"Kyudo");
  const a=fighter("A",0,0,0,all),b=fighter("B",1,1,0,all);
  const legalIn=(ab,role)=>AF.positionalLegality(a,ab,role).ok;
  const ab=n=>{const f=find(all,n);assert(f,"missing ability "+n);return f;};

  // Boxing: entire style Mount-illegal
  for(const n of ["Jab-Cross","Uppercut","Haymaker","Bob and Weave","Defensive Stance","Dirty Boxing","Body Shot"]){
    const row=all.filter(x=>x.name===n&&x.disc==="Martial")[0];
    assert(!legalIn(row,REL.MOUNTING)&&!legalIn(row,REL.MOUNTED),`Boxing ${n} must be blocked in Mount`);
  }
  assert(!legalIn(AF.MARTIAL.Boxing.stance,REL.MOUNTING),"Boxing Stance blocked in Mount");
  assert(!legalIn(AF.MARTIAL.Karate.stance,REL.MOUNTING),"Karate Stance blocked in Mount");
  for(const m of AF.MARTIAL.Karate.moves)assert(!legalIn(m,REL.MOUNTING)&&!legalIn(m,REL.MOUNTED),`Karate ${m.name} blocked in Mount`);

  // Muay Thai
  assert(legalIn(AF.MARTIAL.MuayThai.stance,REL.MOUNTING)&&legalIn(AF.MARTIAL.MuayThai.stance,REL.MOUNTED),"Muay Thai stance Both");
  const mt=n=>find(AF.MARTIAL.MuayThai.moves,n);
  for(const n of ["Elbow Strike","Knee Strikes"])
    assert(legalIn(mt(n),REL.MOUNTING)&&legalIn(mt(n),REL.MOUNTED),`Muay Thai ${n} legal top and bottom`);
  for(const n of ["Roundhouse Kick","Teep Kick","Calf Kick","Uppercut","Jab-Cross"])
    assert(!legalIn(mt(n),REL.MOUNTING)&&!legalIn(mt(n),REL.MOUNTED),`Muay Thai ${n} Mount-illegal`);

  // Judo
  const jd=n=>find(AF.MARTIAL.Judo.moves,n);
  assert(legalIn(jd("Cross Choke"),REL.MOUNTING)&&!legalIn(jd("Cross Choke"),REL.MOUNTED),"Cross Choke top only");
  assert(legalIn(jd("Hip Escape"),REL.MOUNTED)&&!legalIn(jd("Hip Escape"),REL.MOUNTING),"Hip Escape bottom only");
  for(const n of ["Hip Toss","Rolling Throw","Sweeping Shoulder"])
    assert(!legalIn(jd(n),REL.MOUNTING)&&!legalIn(jd(n),REL.MOUNTED),`Judo ${n} unusable once Mount exists`);
  assert(legalIn(jd("Sweeping Shoulder"),REL.GRAPPLING),"Sweeping Shoulder legal from standing grapple");
  assert(!legalIn(jd("Sweeping Shoulder"),REL.FREE),"Sweeping Shoulder needs a standing grapple");

  // Jiu-Jitsu
  const jj=n=>find(AF.MARTIAL.JiuJitsu.moves,n);
  assert(legalIn(jj("Arm bar"),REL.MOUNTING)&&legalIn(jj("Arm bar"),REL.MOUNTED),"Arm bar top and bottom");
  assert(!legalIn(jj("Arm bar"),REL.FREE)&&!legalIn(jj("Arm bar"),REL.GRAPPLING),"Arm bar requires Mount");
  // Strangle became bottom-legal alongside Arm bar (2026-08-15): Jiu-Jitsu can now initiate
  // a submission from either the top or the bottom of a Mount.
  assert(legalIn(jj("Strangle"),REL.MOUNTING)&&legalIn(jj("Strangle"),REL.MOUNTED),"Strangle top and bottom");
  assert(!legalIn(jj("Strangle"),REL.FREE)&&!legalIn(jj("Strangle"),REL.GRAPPLING),"Strangle requires Mount");
  assert(legalIn(jj("Pull Guard"),REL.GRAPPLING)&&legalIn(jj("Pull Guard"),REL.GRAPPLED),"Pull Guard is a standing transition");
  assert(!legalIn(jj("Pull Guard"),REL.MOUNTING)&&!legalIn(jj("Pull Guard"),REL.MOUNTED),"Pull Guard not usable after Mount exists");
  assert(legalIn(jj("Flying Triangle"),REL.GRAPPLING)&&!legalIn(jj("Flying Triangle"),REL.MOUNTING),"Flying Triangle is transition-only before Mount");

  // Wrestling
  const wr=n=>find(AF.MARTIAL.Wrestling.moves,n);
  assert(legalIn(AF.MARTIAL.Wrestling.stance,REL.MOUNTING)&&legalIn(AF.MARTIAL.Wrestling.stance,REL.MOUNTED),"Wrestling Stance Both");
  assert(legalIn(wr("Sumo Palm"),REL.MOUNTING)&&!legalIn(wr("Sumo Palm"),REL.MOUNTED),"Sumo Palm top only");
  assert(legalIn(wr("Wrestler's Prowess"),REL.MOUNTING)&&legalIn(wr("Wrestler's Prowess"),REL.MOUNTED),"Wrestler's Prowess top and bottom");
  for(const n of ["Single Leg Shot","Suplex","Choke Slam"])
    assert(!legalIn(wr(n),REL.MOUNTING)&&!legalIn(wr(n),REL.MOUNTED),`Wrestling ${n} unusable after Mount exists`);

  // Weapons
  for(const m of [AF.WEAPONS.Kenjutsu.stance,...AF.WEAPONS.Kenjutsu.moves,AF.WEAPONS.Kyudo.stance,...AF.WEAPONS.Kyudo.moves])
    assert(!legalIn(m,REL.MOUNTING)&&!legalIn(m,REL.MOUNTED),`${m.name} (Kenjutsu/Kyudo) blocked in Mount`);
  const ks=n=>find(AF.WEAPONS.KyoketsuShoge.moves,n);
  assert(legalIn(AF.WEAPONS.KyoketsuShoge.stance,REL.MOUNTING)&&legalIn(AF.WEAPONS.KyoketsuShoge.stance,REL.MOUNTED),"Kyoketsu-Shoge stance Both");
  assert(legalIn(ks("Sickle Strike"),REL.GRAPPLING)&&legalIn(ks("Sickle Strike"),REL.GRAPPLED)&&legalIn(ks("Sickle Strike"),REL.MOUNTING)&&legalIn(ks("Sickle Strike"),REL.MOUNTED),"Sickle Strike Both");
  assert(legalIn(ks("Cord Garrote"),REL.MOUNTING)&&legalIn(ks("Cord Garrote"),REL.MOUNTED),"Cord Garrote from either Mount position");
  assert(legalIn(ks("Blade Throw"),REL.GRAPPLING),"Blade Throw legal while Grappling");
  assert(!legalIn(ks("Blade Throw"),REL.GRAPPLED),"Blade Throw illegal while Grappled");
  assert(!legalIn(ks("Blade Throw"),REL.MOUNTING)&&!legalIn(ks("Blade Throw"),REL.MOUNTED),"Blade Throw has no Mount access");

  // Sign matrix spot checks (needs every sign kit)
  const everySign=AF.buildLoadout({unlockAll:true});
  const sign=n=>{const f=find(everySign,n);assert(f,"missing sign ability "+n);return f;};
  assert(legalIn(sign("Iron Fist"),REL.MOUNTING)&&!legalIn(sign("Iron Fist"),REL.MOUNTED),"Taurus Iron Fist top only");
  assert(legalIn(sign("Silica Strike"),REL.MOUNTING)&&legalIn(sign("Silica Strike"),REL.MOUNTED),"Silica Strike Both");
  assert(legalIn(sign("Wither Palm"),REL.MOUNTING)&&!legalIn(sign("Wither Palm"),REL.MOUNTED),"Wither Palm top only");
  assert(legalIn(sign("Diamond Cutter"),REL.MOUNTING)&&legalIn(sign("Diamond Cutter"),REL.MOUNTED),"Diamond Cutter Both");
  assert(!legalIn(sign("Aero Palm"),REL.MOUNTING),"Aero Palm Mount-illegal");
  assert(!legalIn(sign("Flow Strike"),REL.MOUNTED),"Flow Strike Mount-illegal");
  assert(legalIn(sign("Shatter Punch"),REL.MOUNTING)&&!legalIn(sign("Shatter Punch"),REL.MOUNTED),"Shatter Punch top only");
  assert(legalIn(sign("Hydro Cannon Palm"),REL.MOUNTING)&&!legalIn(sign("Hydro Cannon Palm"),REL.MOUNTED),"Hydro Cannon Palm top only");
  assert(legalIn(sign("Kidney Shot"),REL.MOUNTING)&&!legalIn(sign("Kidney Shot"),REL.MOUNTED),"Kidney Shot top only");
  assert(legalIn(sign("Echo Fist"),REL.MOUNTED)&&legalIn(sign("Shock Palm"),REL.MOUNTED),"Echo Fist / Shock Palm Both");

  // unaudited abilities are NOT automatically illegal
  const unaudited=everySign.find(x=>x.kitSign&&x.disc==="Ninjutsu"&&!AF.posMeta(x).audited);
  assert(unaudited&&AF.positionalLegality(a,unaudited,REL.MOUNTING).ok,"unaudited abilities stay legal in Mount");
})();

/* ---------- 3. positional save-DC modifiers ---------- */
(function dcModifiers(){
  const all=AF.buildLoadout({unlockAll:true,martials:["MuayThai"]});
  const a=fighter("A",0,0,0,all);
  const nerve=find(all,"Nerve Disruptor"),numb=find(all,"Numbing Strike"),calf=find(AF.MARTIAL.MuayThai.moves,"Calf Kick");
  const echo=find(all,"Echo Fist"),shatter=find(all,"Shatter Punch");
  assert(nerve&&numb&&calf&&echo&&shatter,"DC test setup");
  const at=(ab,role)=>{a.rel={role,partner:null,rounds:0,voluntary:false};return AF.positionalDcModifier(a,ab);};
  for(const ab of [nerve,numb,calf]){
    assert.equal(at(ab,REL.FREE),0,`${ab.name} Free +0`);
    assert.equal(at(ab,REL.GRAPPLING),1,`${ab.name} Grappling +1`);
    assert.equal(at(ab,REL.GRAPPLED),1,`${ab.name} Grappled +1`);
    assert.equal(at(ab,REL.MOUNTING),2,`${ab.name} Mounting +2`);
    assert.equal(at(ab,REL.MOUNTED),-2,`${ab.name} Mounted -2`);
  }
  // Not every status ability receives the scaffold.
  for(const ab of [echo,shatter])for(const role of [REL.FREE,REL.GRAPPLING,REL.MOUNTING,REL.MOUNTED])
    assert.equal(at(ab,role),0,`${ab.name} is not flagged for positional DC scaling`);
  assert(!AF.posMeta(shatter).positionalDc,"Shatter Punch carries no positional DC flag");
  a.rel={role:REL.FREE,partner:null,rounds:0,voluntary:false};
})();

/* ---------- 4. passive stamina recovery ---------- */
(function passive(){
  const base=AF.DR.stamRegen(STATS);
  assert.equal(base,12,"test fighter's canonical passive stamina regen is 12");
  const expect={[REL.FREE]:12,[REL.GRAPPLING]:6,[REL.GRAPPLED]:6,[REL.MOUNTING]:3,[REL.MOUNTED]:3};
  for(const role of Object.keys(expect)){
    const f=fighter("R",0,0,0,[]);f.stam=0;
    const B=new AF.Battle([f],AF.makeArena(5));
    AF.passiveRecovery(B,f,role);
    assert.equal(f.stam,expect[role],`${role} passive stamina recovery`);
  }
})();

/* ---------- 5. mount maintenance ---------- */
function mountPair(){
  const a=fighter("Top",0,0,0,[]),b=fighter("Bottom",1,1,0,[]);
  const B=new AF.Battle([a,b],AF.makeArena(5));
  AF.enterMount(B,a,b,{voluntary:false});
  return{a,b,B};
}
(function maintenance(){
  {const{a,b,B}=mountPair();a.stam=40;AF.relationshipMaintenance(B);
   assert.equal(a.stam,30,"Mount upkeep costs 10 Stamina");
   assert.equal(AF.relRole(a),REL.MOUNTING,"paid upkeep keeps the mount");}
  {const{a,b,B}=mountPair();a.stam=4;AF.relationshipMaintenance(B);
   assert.equal(AF.relRole(a),REL.FREE);assert.equal(AF.relRole(b),REL.FREE,"failed upkeep returns both to Free");
   assert.equal(AF.hdist(a.cell,b.cell),1,"both remain at melee range");}
  // hitting 0 stamina mid-round does NOT instantly escape
  {const{a,b,B}=mountPair();a.stam=0;
   assert.equal(AF.relRole(a),REL.MOUNTING,"0 Stamina mid-round does not break Mount");
   assert.equal(AF.relRole(b),REL.MOUNTED);}
  // recovery cannot retroactively fund maintenance
  {const{a,b,B}=mountPair();a.stam=4;AF.endOfRound(B);
   assert.equal(AF.relRole(a),REL.FREE,"passive recovery cannot retroactively pay upkeep");
   assert.equal(a.stam,7,"the collapsing cycle still recovers at the Mounting 25% snapshot rate (4 + round(12*0.25))");
   const c=fighter("Solo",0,3,0,[]);c.stam=0;const B3=new AF.Battle([c],AF.makeArena(5));
   AF.endOfRound(B3);assert.equal(c.stam,12,"Free recovery resumes at the full rate on the next eligible tick");}
  // explicit voluntary release
  {const{a,b,B}=mountPair();a.stam=99;a.releaseIntent=true;AF.relationshipMaintenance(B);
   assert.equal(AF.relRole(a),REL.FREE,"explicit release path ends the mount");
   assert.equal(a.stam,99,"release costs nothing");}
})();

/* ---------- 6. maintained submissions (kept by USE, not upkeep) ---------- */
(function submissions(){
  const judoKit=kit(["Judo"]),jjKit=kit(["JiuJitsu"]);
  const crossChoke=find(judoKit,"Cross Choke"),armbar=find(jjKit,"Arm bar");
  // Establishing then continuing: a live submission that was applied THIS round survives.
  {const{a,b,B}=mountPair();B.round=4;
   const sub=AF.setSubmission(a,b,crossChoke,"Cross Choke",B.round);
   a.stam=99;const before=a.stam;
   AF.relationshipMaintenance(B);
   assert(AF.activeSubmission(a),"a submission worked this round survives maintenance");
   assert.equal(a.stam,before-AF.BAL.mountUpkeepStamina,"there is no separate passive submission upkeep");
   assert.equal(a.reservedSlots,undefined,"submissions no longer reserve an action slot");
   assert.equal(AF.availableSlots(a),5,"the full slate stays programmable");}
  // Not re-queued: the hold is simply released, and Mount then resolves its own upkeep.
  {const{a,b,B}=mountPair();B.round=4;
   AF.setSubmission(a,b,crossChoke,"Cross Choke",3); // last worked a round ago
   a.stam=99;
   AF.relationshipMaintenance(B);
   assert(!AF.activeSubmission(a),"a submission not worked this round is released");
   assert.equal(a.stam,99-AF.BAL.mountUpkeepStamina,"Mount upkeep still resolves after the release");
   assert.equal(AF.relRole(a),REL.MOUNTING,"releasing the submission does not end Mount");}
  // The holder may be Mounting or Mounted.
  {const{a,b,B}=mountPair();B.round=2;
   AF.setSubmission(b,a,armbar,"Arm bar",B.round);b.stam=99;a.stam=99;
   AF.relationshipMaintenance(B);
   assert(AF.activeSubmission(b),"a bottom-position holder keeps the submission by working it");
   assert.equal(a.stam,99-AF.BAL.mountUpkeepStamina,"the Mounting fighter still pays Mount upkeep");}
  // Submission Lock: a live submission cannot be erased by dropping Mount.
  {const{a,b,B}=mountPair();B.round=2;
   AF.setSubmission(b,a,armbar,"Arm bar",B.round);b.stam=99;a.stam=99;a.releaseIntent=true;
   AF.relationshipMaintenance(B);
   assert(AF.activeSubmission(b),"a live submission cannot be erased by dropping Mount");
   assert.equal(AF.relRole(a),REL.MOUNTING,"Mount is locked while the submission is live");}
  // ...but once the submission lapses, the same release intent does end Mount.
  {const{a,b,B}=mountPair();B.round=4;
   AF.setSubmission(b,a,armbar,"Arm bar",3);b.stam=99;a.stam=99;a.releaseIntent=true;
   AF.relationshipMaintenance(B);
   assert(!AF.activeSubmission(b),"the lapsed submission is released");
   assert.equal(AF.relRole(a),REL.FREE,"Mount can then be given up");}

  /* Escalation: each consecutive maintained round raises BOTH cost and damage. */
  assert.equal(AF.BAL.submissionCostEscalation,0.5);
  assert.equal(AF.BAL.submissionDamageEscalation,0.5);
  {const{a,b}=mountPair();
   const sub=AF.setSubmission(a,b,crossChoke,"Cross Choke",1);
   assert.equal(AF.submissionCostMult(null),1,"a fresh hold is charged at face value");
   assert.equal(AF.submissionDamageMult(null),1);
   assert.equal(AF.submissionCostMult(sub),1.5,"the first continuation already escalates");
   assert.equal(AF.submissionDamageMult(sub),1.5);
   sub.consecutive=1;assert.equal(AF.submissionCostMult(sub),2);assert.equal(AF.submissionDamageMult(sub),2);
   sub.consecutive=3;assert.equal(AF.submissionCostMult(sub),3);assert.equal(AF.submissionDamageMult(sub),3);
   // continuation is identity-matched: same holder, same partner, same technique
   sub.consecutive=2;
   assert.equal(AF.continuedSubmission(a,crossChoke),sub,"the same technique continues the hold");
   assert.equal(AF.continuedSubmission(a,armbar),null,"a different technique starts a new hold");
   assert.equal(AF.continuedSubmission(b,crossChoke),null,"only the holder continues it");}

  /* End to end through the real resolver: establish, then crank it twice. */
  {AF.setSeed(31);
   const top=fighter("Top",0,0,0,judoKit,{isPlayer:true}),bot=fighter("Bot",1,1,0,[]);
   bot.stats.STR=2;bot.stats.AGI=2;bot.stats.INT=2;
   top.activeMartial=judoKit.find(x=>x.name==="Judo Stance");
   const B=new AF.Battle([top,bot],AF.makeArena(5));
   AF.enterMount(B,top,bot,{voluntary:false});
   const choke=find(top.abilities,"Cross Choke");
   const quoted=[],hits=[];
   for(let r=0;r<3;r++){
     const hpBefore=bot.hp;
     // What the player is quoted for this action, before it resolves.
     quoted.push(AFUI.projectedCosts([choke],top).stam);
     top.stam=top.maxStam;
     AF.resolveRound(B,[{owner:top,actions:[choke],moveTo:null},{owner:bot,actions:[],moveTo:null}]);
     B.round++;
     hits.push(hpBefore-bot.hp);
   }
   const sub=AF.activeSubmission(top);
   assert(sub,"the submission survives while it is worked every round");
   assert.equal(sub.consecutive,2,"three worked rounds = two escalation steps");
   assert(quoted[1]>quoted[0]&&quoted[2]>quoted[1],`consecutive rounds are quoted higher: ${quoted.join(" < ")}`);
   assert(hits[1]>hits[0]&&hits[2]>hits[1],`consecutive rounds hit harder: ${hits.join(" < ")}`);
   // The ENGINE charges that escalated cost, not the face value: one short and it fizzles.
   {const due=AFUI.projectedCosts([choke],top).stam;
    assert(due>choke.stam,"a continued submission is dearer than its face cost");
    top.stam=due-1;const logLen=B.log.length;B.round++;
    AF.resolveRound(B,[{owner:top,actions:[choke],moveTo:null},{owner:bot,actions:[],moveTo:null}]);
    assert(B.log.slice(logLen).some(x=>/fizzles \(not enough resources\)/.test(x.text)),
      `the engine charges the escalated ${due}, so ${due-1} is not enough`);}
   // stop working it and the hold drops at the next maintenance
   AF.setSubmission(top,bot,choke,"Cross Choke",B.round);
   B.round++;top.stam=top.maxStam;
   AF.resolveRound(B,[{owner:top,actions:[],moveTo:null},{owner:bot,actions:[],moveTo:null}]);
   assert(!AF.activeSubmission(top),"skipping the submission for one round releases it");}
})();

/* ---------- 6b. Wrestling: Ground and Pound + Reversal (owner-authored 2026-08-15) ---------- */
(function wrestlingGroundGame(){
  const wr=kit(["Wrestling"]);
  const gp=find(wr,"Ground and Pound"),rv=find(wr,"Reversal");
  assert(gp&&rv,"Wrestling gains Ground and Pound and Reversal");

  // Ground and Pound: 12 power / 10 Stamina / 2 slots / Mounting only. Gained a Stamina-sap
  // rider (2026-08-17) so it pressures a pinned foe's escape/upkeep costs, not damage alone.
  assert.equal(gp.slots,2);assert.equal(gp.stam,10);assert.equal(gp.chakra,0);
  assert.equal(gp.effects.find(e=>e.k==="Damage").power,12);
  assert.equal(gp.effects.length,2,"Ground and Pound now carries damage plus a Stamina-drain rider");
  assert.equal(gp.effects.find(e=>e.k==="Res"&&e.res==="Stamina")?.amt,-12,"Ground and Pound saps 12 Stamina on hit");
  assert.equal(gp.poiseMult,1,"Ground and Pound is not a Guard Break");
  assert(!gp.poiseMultWhenGrappling,"no conditional Guard Break either");

  // Reversal: 0 power / 3 slots / DC 10 STR+AGI contest / Mounted only.
  assert.equal(rv.slots,3);assert.equal(rv.stam,30);assert.equal(rv.dmg,"None");
  const rvTech=rv.effects.find(e=>e.k==="GrappleTech");
  assert(rvTech,"Reversal resolves as a relationship technique");
  assert.equal(rvTech.power,0,"Reversal deals no damage");
  assert.equal(rvTech.dc,10,"DC 10 contest");
  assert.equal(rvTech.best,false,"the contest is STR+AGI, not the best-of pairing");
  assert(rvTech.mount&&rvTech.reversal&&!rvTech.voluntaryBottom,"Reversal puts the USER on top");

  // Positional gating.
  const w=fighter("W",0,0,0,wr);
  const only=(ab,role)=>[REL.FREE,REL.GRAPPLING,REL.GRAPPLED,REL.MOUNTING,REL.MOUNTED]
    .filter(r=>AF.positionalLegality(w,ab,r).ok).join(",");
  assert.equal(only(gp),REL.MOUNTING,"Ground and Pound is Mounting only");
  assert.equal(only(rv),REL.MOUNTED,"Reversal is Mounted only");

  // A reversal flips the position, breaks the new bottom fighter's Poise, and kills a
  // submission that was layered over the old relationship.
  {AF.setSeed(11);
   const jjRows=kit(["JiuJitsu"]);
   const me=fighter("Me",0,0,0,wr,true),opp=fighter("Opp",1,1,0,jjRows);
   // Make the DC 10 STR+AGI contest deterministic: 28 + 10 is out of the defender's reach.
   me.stats.STR=14;me.stats.AGI=14;opp.stats.STR=4;opp.stats.AGI=4;
   me.activeMartial=wr.find(x=>x.name==="Wrestling Stance");
   const B=new AF.Battle([me,opp],AF.makeArena(5));
   AF.enterMount(B,opp,me,{voluntary:false});
   AF.setSubmission(opp,me,find(jjRows,"Strangle"),"Strangle",B.round);
   assert.equal(AF.relRole(me),REL.MOUNTED);
   assert(AF.activeSubmission(me),"the opponent holds a submission from the top");
   const hpBefore=opp.hp;
   me.stam=999;
   AF.resolveRound(B,[{owner:me,actions:[find(me.abilities,"Reversal")],moveTo:null},{owner:opp,actions:[],moveTo:null}]);
   assert.equal(AF.relRole(me),REL.MOUNTING,"the reversal puts the user on top");
   assert.equal(AF.relRole(opp),REL.MOUNTED,"and the opponent underneath");
   assert(!AF.activeSubmission(me),"the submission over the old position is broken");
   assert.equal(opp.poise,0,"forced entry breaks the new bottom fighter's Poise");
   assert.equal(opp.hp,hpBefore,"Reversal itself deals no damage");
   assert(B.log.some(x=>/reverses the position/.test(x.text)),"the reversal is announced in the log");
   // Ground and Pound is now legal from the position the reversal won.
   assert(AF.positionalLegality(me,find(me.abilities,"Ground and Pound")).ok,
     "Ground and Pound opens up from the reversed-into top position");}

  // A Wrestler NPC uses each from the position that allows it.
  {AF.setSeed(11);
   const rows=AF.enemyLoadout("Wrestler"),def=AF.ENEMIES.Wrestler;
   const npc=AF.makeFighter({name:"Wrestler",sign:"Aries",stats:{...def.stats},faction:0,cell:AF.hx(0,0),abilities:rows,persona:def.persona});
   const foe=fighter("Foe",1,1,0,[]);
   npc.activeMartial=rows.find(x=>x.name==="Wrestling Stance");
   const B=new AF.Battle([npc,foe],AF.makeArena(5));
   AF.enterMount(B,foe,npc,{voluntary:false});
   const pinned=AF.planFor(B,npc,0.05).actions.map(a=>a.name);
   assert(pinned.includes("Reversal"),`a pinned Wrestler reaches for Reversal, got ${pinned.join(" · ")}`);
   AF.endRelationship(B,npc,"reset");AF.enterMount(B,npc,foe,{voluntary:false});
   const onTop=AF.planFor(B,npc,0.05).actions.map(a=>a.name);
   assert(onTop.includes("Ground and Pound"),`a mounting Wrestler uses Ground and Pound, got ${onTop.join(" · ")}`);
   assert(!onTop.includes("Reversal"),"a fighter already on top has nothing to reverse");}
})();

/* ---------- 6c. submissions lower the Reversal DC proportionally to their age ---------- */
(function escapeResistance(){
  const wr=kit(["Wrestling"]),judo=kit(["Judo"]);
  const rv=find(wr,"Reversal"),hip=find(judo,"Hip Escape");
  assert(AF.posMeta(rv).escape,"Reversal is the contested positional escape");
  assert(!AF.posMeta(hip).escape,"Hip Escape is flat resource damage — it carries no check to resist");
  assert.equal(AF.BAL.submissionEscapeDcPerRound,2);

  // Resistance counts turns the hold has been WORKED, and only resists the fighter caught in it.
  {const{a,b,B}=mountPair();
   assert.equal(AF.submissionEscapeTurns(b),0,"no submission means no resistance");
   const sub=AF.setSubmission(a,b,null,"Strangle",B.round);
   assert.equal(AF.submissionEscapeTurns(b),1,"the round it is locked in already counts as one turn");
   assert.equal(AF.submissionEscapeResistance(b),2);
   sub.consecutive=2;
   assert.equal(AF.submissionEscapeTurns(b),3);
   assert.equal(AF.submissionEscapeResistance(b),6,"resistance is proportional to turns held");
   assert.equal(AF.submissionEscapeTurns(a),0,"the HOLDER is not resisted — they are not escaping");}

  /* Measured success at even stats. The contest denies on def + d20 >= atk + dc, so the
     resistance is subtracted from Reversal's DC 10 and the escape gets strictly harder. */
  function reversalRate(turns,runs){
    let ok=0;
    for(let i=0;i<runs;i++){
      AF.setSeed(i*7+1);
      const rows=kit(["Wrestling"]);
      const me=fighter("Me",0,0,0,rows),opp=fighter("Opp",1,1,0,[]);
      me.activeMartial=rows.find(x=>x.name==="Wrestling Stance");
      const B=new AF.Battle([me,opp],AF.makeArena(5));
      AF.enterMount(B,opp,me,{voluntary:false});
      if(turns>0){const sub=AF.setSubmission(opp,me,null,"Strangle",B.round);sub.consecutive=turns-1;}
      me.stam=999;
      AF.resolveRound(B,[{owner:me,actions:[find(rows,"Reversal")],moveTo:null},{owner:opp,actions:[],moveTo:null}]);
      if(AF.relRole(me)===REL.MOUNTING)ok++;
    }
    return 100*ok/runs;
  }
  const none=reversalRate(0,240),t1=reversalRate(1,240),t3=reversalRate(3,240);
  assert(none>t1&&t1>t3,`Reversal gets strictly harder as the hold ages: ${none}% > ${t1}% > ${t3}%`);
  assert(none>35&&none<60,`an unresisted DC 10 Reversal lands around half the time, got ${none}%`);
  assert(t3<none/2,`three turns of submission at least halves the Reversal, got ${t3}% vs ${none}%`);

  // A denied Reversal still costs: the attempt is spent, the flip simply does not happen.
  {AF.setSeed(3);
   const rows=kit(["Wrestling"]);
   const me=fighter("Me",0,0,0,rows),opp=fighter("Opp",1,1,0,[]);
   me.activeMartial=rows.find(x=>x.name==="Wrestling Stance");
   const B=new AF.Battle([me,opp],AF.makeArena(5));
   AF.enterMount(B,opp,me,{voluntary:false});
   const sub=AF.setSubmission(opp,me,null,"Strangle",B.round);sub.consecutive=19; // effectively hopeless
   me.stam=999;const before=me.stam;
   AF.resolveRound(B,[{owner:me,actions:[find(rows,"Reversal")],moveTo:null},{owner:opp,actions:[],moveTo:null}]);
   assert.equal(AF.relRole(me),REL.MOUNTED,"a deeply worked hold denies the reversal");
   assert(before-me.stam>=rv.stam,"a denied Reversal still pays its Stamina");
   assert(B.log.some(x=>/escape DC 10 →/.test(x.text)),"the denial names the reduced DC");}

  /* Hip Escape is untouched: no check, so it always lands its drain no matter how long the
     hold has been on. Its pressure on the mounter's upkeep is the counterplay, not a roll. */
  {AF.setSeed(3);
   const rows=kit(["Judo"]);
   const me=fighter("Me",0,0,0,rows),opp=fighter("Opp",1,1,0,[]);
   me.activeMartial=rows.find(x=>x.name==="Judo Stance");
   const B=new AF.Battle([me,opp],AF.makeArena(5));
   AF.enterMount(B,opp,me,{voluntary:false});
   const sub=AF.setSubmission(opp,me,null,"Strangle",B.round);sub.consecutive=19;
   me.stam=999;opp.stam=99;const oppBefore=opp.stam;
   AF.resolveRound(B,[{owner:me,actions:[find(rows,"Hip Escape")],moveTo:null},{owner:opp,actions:[],moveTo:null}]);
   assert.equal(oppBefore-opp.stam,15+AF.BAL.mountUpkeepStamina-3,
     "Hip Escape drains its full 15 even under a long-held submission");}

  // The resistance is submission-specific: a plain Mount with no hold resists nothing.
  {const{a,b}=mountPair();
   assert.equal(AF.submissionEscapeResistance(b),0,"a bare Mount does not resist escapes");}
})();

/* ---------- 7. zero stamina is never an escape ---------- */
(function zeroStam(){
  const{a,b,B}=mountPair();AF.setSubmission(a,b,null,"Strangle");
  b.stam=0;a.stam=0;
  assert.equal(AF.relRole(b),REL.MOUNTED,"0 Stamina never breaks Mount");
  assert(AF.activeSubmission(b),"0 Stamina never breaks a maintained submission");
  const g1=fighter("G",0,0,0,[]),g2=fighter("H",1,1,0,[]);
  const B2=new AF.Battle([g1,g2],AF.makeArena(5));
  AF.enterStandingGrapple(B2,g1,g2,5);g2.stam=0;
  assert.equal(AF.relRole(g2),REL.GRAPPLED,"0 Stamina never breaks a standing grapple");
})();

/* ---------- 8. Pull Guard poise ---------- */
(function pullGuard(){
  {const a=fighter("Top",0,0,0,[]),b=fighter("Bot",1,1,0,[]);
   const B=new AF.Battle([a,b],AF.makeArena(5));b.poise=37;
   AF.enterMount(B,a,b,{voluntary:false});
   assert.equal(b.poise,0,"forced Mount entry breaks Poise");}
  {const a=fighter("Top",0,0,0,[]),b=fighter("Bot",1,1,0,[]);
   const B=new AF.Battle([a,b],AF.makeArena(5));b.poise=37;
   AF.enterMount(B,a,b,{voluntary:true});
   assert.equal(b.poise,37,"Pull Guard preserves current Poise");}
  {const a=fighter("Top",0,0,0,[]),b=fighter("Bot",1,1,0,[]);
   const B=new AF.Battle([a,b],AF.makeArena(5));b.poise=4;
   AF.enterMount(B,a,b,{voluntary:true});
   assert.equal(b.poise,4,"Pull Guard preserves a low Poise value exactly");}
  {const a=fighter("Top",0,0,0,[]),b=fighter("Bot",1,1,0,[]);
   const B=new AF.Battle([a,b],AF.makeArena(5));b.poise=0;
   AF.enterMount(B,a,b,{voluntary:true});
   assert.equal(b.poise,0,"Pull Guard at 0 Poise stays 0 — preserve, never restore");}
  // Jiu-Jitsu Stance alone grants no Poise protection
  const jjStance=AF.MARTIAL.JiuJitsu.stance;
  assert(!jjStance.preservesPoise&&!AF.posMeta(jjStance).transition,"Jiu-Jitsu Stance carries no transition/Poise exception");
  const pg=find(AF.MARTIAL.JiuJitsu.moves,"Pull Guard");
  assert.equal(AF.posMeta(pg).transition,AF.TRANSITION.VOLUNTARY_BOTTOM,"the exception belongs to Pull Guard's transition metadata");
})();
/* Hip Escape in a real round: 15 stamina off the Mounter, no HP damage, once/round. */
(function hipEscapeRound(){
  AF.setSeed(3);
  const judo=AF.buildLoadout({sign:"Aries",martials:["Judo"]});
  const hip=find(judo,"Hip Escape");
  const top=fighter("Top",0,0,0,[]),bot=fighter("Bot",1,1,0,judo,true);
  bot.activeMartial=judo.find(x=>x.name==="Judo Stance");
  const B=new AF.Battle([top,bot],AF.makeArena(5));
  AF.enterMount(B,top,bot,{voluntary:false});
  top.stam=40;bot.stam=60;const hp0=top.hp;
  AF.resolveRound(B,[{owner:bot,actions:[hip,hip],moveTo:null},{owner:top,actions:[],moveTo:null}]);
  assert.equal(top.hp,hp0,"Hip Escape deals no HP damage");
  // 40 - 15 (one Hip Escape only; second is once-per-round blocked) - 10 mount upkeep + 3 recovery
  assert.equal(top.stam,40-15-10+3,`Hip Escape drains exactly 15; got ${top.stam}`);
  assert(B.log.some(x=>/once per round/.test(x.text)),"the second Hip Escape is refused as once-per-round");
  assert.equal(AF.relRole(top),REL.MOUNTING,"Hip Escape does not directly end Mount");
})();

/* Hip Escape stamina pressure can cause a later upkeep failure. */
(function hipEscapePressure(){
  AF.setSeed(4);
  const judo=AF.buildLoadout({sign:"Aries",martials:["Judo"]});
  const hip=find(judo,"Hip Escape");
  const top=fighter("Top",0,0,0,[]),bot=fighter("Bot",1,1,0,judo,true);
  bot.activeMartial=judo.find(x=>x.name==="Judo Stance");
  const B=new AF.Battle([top,bot],AF.makeArena(5));
  AF.enterMount(B,top,bot,{voluntary:false});
  top.stam=20;bot.stam=60;
  AF.resolveRound(B,[{owner:bot,actions:[hip],moveTo:null},{owner:top,actions:[],moveTo:null}]);
  assert.equal(AF.relRole(top),REL.FREE,"stamina pressure from Hip Escape causes the later upkeep to fail");
  assert.equal(AF.relRole(bot),REL.FREE);
})();

/* Focus is legal in every relationship and restores 20% with no poise. */
(function focus(){
  for(const role of [REL.GRAPPLING,REL.GRAPPLED,REL.MOUNTING,REL.MOUNTED]){
    const kitRows=AF.buildLoadout({sign:"Aries"});
    const cb=find(kitRows,"Catch Breath"),cc=find(kitRows,"Charge Chakra");
    const a=fighter("A",0,0,0,kitRows,true),b=fighter("B",1,1,0,[]);
    const B=new AF.Battle([a,b],AF.makeArena(5));
    if(AF.isStandingRole(role))AF.enterStandingGrapple(B,role===REL.GRAPPLING?a:b,role===REL.GRAPPLING?b:a,5);
    else AF.enterMount(B,role===REL.MOUNTING?a:b,role===REL.MOUNTING?b:a,{voluntary:false});
    assert.equal(AF.relRole(a),role);
    assert(AF.positionalLegality(a,cb).ok,`Catch Breath legal while ${role}`);
    assert(AF.positionalLegality(a,cc).ok,`Charge Chakra legal while ${role}`);
    assert(!cb.effects.some(e=>e.k==="Res"&&e.res==="Poise")&&!cc.effects.some(e=>e.k==="Res"&&e.res==="Poise"),"Focus carries no Poise effect");
    a.stam=0;a.chakra=0;a.poise=0;
    AF.resolveRound(B,[{owner:a,actions:[cb,cc],moveTo:null},{owner:b,actions:[],moveTo:null}]);
    // Focus restore (20% of max) + this role's upkeep + this role's passive recovery.
    const focusGain=Math.round(a.maxStam*AF.BAL.focusRestorePercent);
    const upkeep=role===REL.GRAPPLING?AF.BAL.grappleHoldUpkeepStamina:role===REL.MOUNTING?AF.BAL.mountUpkeepStamina:0;
    const regen=Math.round(AF.DR.stamRegen(a.stats)*AF.passiveStaminaFactor(role));
    assert.equal(a.stam,focusGain-upkeep+regen,`Catch Breath restored 20% of max stamina while ${role}`);
    assert.equal(a.chakra,Math.round(AF.effMaxChakra(a)*AF.BAL.focusRestorePercent)+AF.DR.chakRegen(a.stats),`Charge Chakra restored 20% while ${role}`);
    if(role===REL.MOUNTED)assert.equal(a.poise,0,"Focus grants no poise (Mounted keeps its broken guard)");
  }
  // explicit Focus denial still applies
  const kitRows=AF.buildLoadout({sign:"Aries"});
  const cb=find(kitRows,"Catch Breath");
  const a=fighter("A",0,0,0,kitRows);
  a.statuses.push({kind:"FocusLock",rounds:1,stacks:1,tick:0,mag:0});
  assert(!AF.positionalLegality(a,cb).ok,"an explicit Focus lock still denies Focus");
})();

/* Movement / teleport blocked; authored relationship repositions still work. */
(function movement(){
  const rows=AF.buildLoadout({unlockAll:true,martials:["Judo"]});
  const a=fighter("A",0,0,0,rows),b=fighter("B",1,1,0,[]);
  const B=new AF.Battle([a,b],AF.makeArena(5));
  const machLunge=find(rows,"Mach Lunge"); // GapCloser
  const rolling=find(AF.MARTIAL.Judo.moves,"Rolling Throw");
  for(const role of [REL.GRAPPLING,REL.GRAPPLED,REL.MOUNTING,REL.MOUNTED]){
    assert(!AF.positionalLegality(a,machLunge,role).ok,`generic gap-closer blocked while ${role}`);
  }
  assert(AF.positionalLegality(a,rolling,REL.GRAPPLING).ok,"Rolling Throw is a relationship reposition, not ordinary movement");
  assert(AF.positionalLegality(a,rolling,REL.GRAPPLED).ok,"Rolling Throw usable from either standing role");
  // engine-level: an engaged fighter cannot execute a planned move
  AF.enterStandingGrapple(B,a,b,5);
  const before={...a.cell};
  AF.resolveRound(B,[{owner:a,actions:[],moveTo:AF.hx(3,0)},{owner:b,actions:[],moveTo:null}]);
  assert.deepStrictEqual({q:a.cell.q,r:a.cell.r},{q:before.q,r:before.r},"planned movement is blocked while engaged");
})();

/* Full chain through real abilities: Clinch -> Sweeping Shoulder -> Cross Choke. */
(function chain(){
  AF.setSeed(9);
  const judo=AF.buildLoadout({sign:"Aries",martials:["Judo"]});
  const clinch=find(judo,"Clinch"),sweep=find(judo,"Sweeping Shoulder"),choke=find(judo,"Cross Choke");
  const stance=judo.find(x=>x.name==="Judo Stance");
  const a=fighter("A",0,0,0,judo,true),b=fighter("B",1,1,0,[]);
  b.stats.STR=2;b.stats.AGI=2;b.stats.INT=2;
  const B=new AF.Battle([a,b],AF.makeArena(5));
  a.activeMartial=stance;
  AF.resolveRound(B,[{owner:a,actions:[clinch,sweep,choke],moveTo:null},{owner:b,actions:[],moveTo:null}]);
  assert.equal(AF.relRole(a),REL.MOUNTING,"the chain reaches Mounting");
  assert.equal(AF.relRole(b),REL.MOUNTED);
  assert(!AF.hasStatus(a,"Grappling")&&!AF.hasStatus(b,"Grappled"),"standing roles cleared by the mount transition");
  const sub=AF.activeSubmission(a);
  assert(sub&&sub.holder===a&&sub.name==="Cross Choke","Cross Choke establishes a Maintained Submission held by the Mounting fighter");
  assert(!a.reservedSlots,"submissions no longer reserve an action slot");
  assert.equal(AF.activeSubmission(a).appliedRound,B.round,"the establishing round is recorded so maintenance can see it was worked");
})();

/* Execution revalidation: a failed transition must not let a follow-up run illegally. */
(function revalidate(){
  AF.setSeed(2);
  const judo=AF.buildLoadout({sign:"Aries",martials:["Judo"]});
  const clinch=find(judo,"Clinch"),sweep=find(judo,"Sweeping Shoulder"),choke=find(judo,"Cross Choke");
  const stance=judo.find(x=>x.name==="Judo Stance");
  const a=fighter("A",0,0,0,judo,true),b=fighter("B",1,1,0,[]);
  b.stats.STR=60;b.stats.AGI=60;b.stats.INT=60; // denies the transition
  const B=new AF.Battle([a,b],AF.makeArena(5));
  a.activeMartial=stance;
  AF.resolveRound(B,[{owner:a,actions:[clinch,sweep,choke],moveTo:null},{owner:b,actions:[],moveTo:null}]);
  assert.notEqual(AF.relRole(a),REL.MOUNTING,"the transition failed");
  assert(!AF.activeSubmission(a),"the Mount-only follow-up did not execute");
  assert(B.log.some(x=>/can't use Cross Choke/.test(x.text)),"the illegal follow-up fails cleanly with a reason");
})();

/* Queue projection: stance children reveal, and a queued transition unlocks a later Mount-only move. */
(function queueProjection(){
  const judo=AF.buildLoadout({sign:"Aries",martials:["Judo"]});
  const stance=judo.find(x=>x.name==="Judo Stance"),clinch=find(judo,"Clinch");
  const sweep=find(judo,"Sweeping Shoulder"),choke=find(judo,"Cross Choke"),hip=find(judo,"Hip Escape");
  const p=fighter("P",0,0,0,judo,true);
  assert(AFUI.dependencyReason(clinch,p,[]),"Judo children stay hidden with no stance");
  assert(!AFUI.dependencyReason(clinch,p,[stance]),"queueing the stance reveals Clinch");
  assert(AFUI.dependencyReason(choke,p,[stance]),"Cross Choke stays hidden while Free");
  assert(AFUI.dependencyReason(sweep,p,[stance]),"Sweeping Shoulder needs a standing grapple");
  assert(!AFUI.dependencyReason(sweep,p,[stance,clinch]),"a queued Clinch projects the standing grapple");
  assert(!AFUI.dependencyReason(choke,p,[stance,clinch,sweep]),"a queued transition projects Mounting and reveals Cross Choke");
  assert(AFUI.dependencyReason(hip,p,[stance,clinch,sweep]),"Hip Escape stays hidden from the projected top position");
  assert.equal(AFUI.projectedRelRole(p,[stance,clinch,sweep]),REL.MOUNTING);
  // reasons are player-legible
  assert.equal(AFUI.dependencyReason(choke,p,[stance]),"Requires Mounting");
  assert.equal(AFUI.dependencyReason(hip,p,[stance]),"Requires Mounted");
  assert.equal(AFUI.dependencyReason(sweep,p,[stance]),"Requires standing Grapple");
})();

/* AI obeys the same positional rules and never plans an illegal action. */
(function ai(){
  AF.setSeed(21);
  const rows=AF.buildLoadout({unlockAll:true,martials:["Boxing","MuayThai","Judo","JiuJitsu","Karate","Wrestling"],weapon:"Kenjutsu"});
  for(const role of [REL.MOUNTING,REL.MOUNTED,REL.GRAPPLING,REL.GRAPPLED]){
    const npc=fighter("NPC",0,0,0,rows),foe=fighter("Foe",1,1,0,rows);
    npc.activeMartial=rows.find(x=>x.name==="Muay Thai Stance");
    const B=new AF.Battle([npc,foe],AF.makeArena(5));
    if(AF.isStandingRole(role))AF.enterStandingGrapple(B,role===REL.GRAPPLING?npc:foe,role===REL.GRAPPLING?foe:npc,5);
    else AF.enterMount(B,role===REL.MOUNTING?npc:foe,role===REL.MOUNTING?foe:npc,{voluntary:false});
    const plan=AF.planFor(B,npc,0.1);
    for(const ab of plan.actions){
      const legal=AF.positionalLegality(npc,ab);
      assert(legal.ok,`AI planned ${ab.name} illegally from ${role}: ${legal.reason}`);
    }
    assert(!plan.moveTo||!AF.isRooted(npc),"AI does not plan movement while engaged");
  }
  // A style NPC holding a submission re-queues the hold rather than letting it lapse.
  const jjRows=AF.enemyLoadout("Jiujiteiro");
  const npc=AF.makeFighter({name:"JJ",sign:"Aries",stats:{...AF.ENEMIES.Jiujiteiro.stats},faction:0,cell:AF.hx(0,0),abilities:jjRows,persona:AF.ENEMIES.Jiujiteiro.persona});
  const foe=fighter("Foe",1,1,0,[]);
  npc.activeMartial=jjRows.find(x=>x.name==="Jiu-Jitsu Stance");
  const B=new AF.Battle([npc,foe],AF.makeArena(5));B.round=3;
  AF.enterMount(B,npc,foe,{voluntary:false});
  AF.setSubmission(npc,foe,jjRows.find(a=>a.name==="Arm bar"),"Arm bar",2);
  const plan=AF.planFor(B,npc,0.05);
  assert(plan.actions.some(x=>x.name==="Arm bar"),
    `an AI holding a submission must re-queue it, got ${plan.actions.map(x=>x.name).join(" · ")}`);
  assert(plan.actions.reduce((n,a)=>n+a.slots,0)<=AF.BAL.actionSlotsPerRound,"AI stays within the slot budget");
  // Working the hold repeatedly inside ONE round must not ratchet the escalation more than once.
  {const sub=AF.activeSubmission(npc),before=sub.consecutive;
   const ab=jjRows.find(a=>a.name==="Arm bar");
   npc.stam=999;
   AF.resolveRound(B,[{owner:npc,actions:[ab,ab,ab],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
   const after=AF.activeSubmission(npc);
   assert(after,"the hold survives a round it was worked in");
   assert.equal(after.consecutive,before+1,"escalation is per consecutive round, not per use");}
})();

/* Standing-grapple priority is directional and does not apply in Mount. */
(function priority(){
  const rows=AF.buildLoadout({sign:"Aries"});
  const jab={...rows.find(a=>a.targeting==="SingleEnemy")};
  const a=fighter("A",0,0,0,rows),b=fighter("B",1,1,0,rows),c=fighter("C",1,2,0,rows);
  const B=new AF.Battle([a,b,c],AF.makeArena(5));
  AF.enterStandingGrapple(B,a,b,5);
  assert(AF.standingGrapplePriority(a,{ability:jab,target:b})>0,"the Grappling controller gets +1 positional Priority against the Grappled opponent");
  assert.equal(AF.standingGrapplePriority(a,{ability:jab,target:c}),0,"it is not a global initiative buff");
  assert.equal(AF.standingGrapplePriority(b,{ability:jab,target:a}),0,"the Grappled fighter gets no bonus");
  AF.enterMount(B,a,b,{voluntary:false});
  assert.equal(AF.standingGrapplePriority(a,{ability:jab,target:b}),0,"Mount grants no generic Priority bonus");
})();

/* ---------- per-style martial NPCs ---------- */
(function styleNpcs(){
  const styleNpcs={Boxer:"Boxing",MuayThaiFighter:"MuayThai",Judoka:"Judo",
    Jiujiteiro:"JiuJitsu",Karateka:"Karate",Wrestler:"Wrestling"};
  assert(!AF.ENEMIES.MartialArtist,"the single combined Martial Artist NPC is replaced by per-style NPCs");
  for(const [key,style] of Object.entries(styleNpcs)){
    const def=AF.ENEMIES[key];
    assert(def,`missing style NPC ${key}`);
    assert.equal(def.martial,style,`${key} is bound to the ${style} style`);
    const rows=AF.enemyLoadout(key);
    const stance=rows.find(a=>a.tags.includes("MartialStance"));
    assert(stance,`${key} must carry its own martial stance`);
    assert.equal(stance.name,AF.MARTIAL[style].stance.name,`${key} carries the ${style} stance`);
    assert.equal(stance.styleKey,style,"the NPC stance is annotated with its style key");
    // every technique of that style is present and annotated as its child
    for(const m of AF.MARTIAL[style].moves){
      const got=rows.find(a=>a.name===m.name);
      assert(got,`${key} is missing ${m.name}`);
      assert(got.isStyleTechnique&&got.parentStyles.includes(style),`${key}'s ${m.name} must be gated behind the ${style} stance`);
    }
    // no other style's techniques leak in
    for(const other of Object.keys(AF.MARTIAL)){
      if(other===style)continue;
      const uniq=AF.MARTIAL[other].moves.filter(m=>!AF.MARTIAL[style].moves.some(x=>x.name===m.name)
        &&m.name!==AF.MARTIAL[style].stance.name);
      for(const m of uniq)assert(!rows.some(a=>a.name===m.name&&a.disc==="Martial"),`${key} must not carry ${other} ${m.name}`);
    }
    // the AI opens with its own stance, and never plans an illegal or stance-less action
    AF.setSeed(17);
    const npc=AF.makeFighter({name:def.name,sign:"Aries",stats:{...def.stats},faction:0,cell:AF.hx(0,0),abilities:rows,persona:def.persona});
    const foe=AF.makeFighter({name:"Foe",sign:"Leo",stats:{STR:11,AGI:11,FORT:11,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
    const B=new AF.Battle([npc,foe],AF.makeArena(5));
    const plan=AF.planFor(B,npc,0.1);
    assert.equal(plan.actions[0]&&plan.actions[0].name,AF.MARTIAL[style].stance.name,`${key} opens with its own stance`);
    for(const ab of plan.actions)assert(AF.positionalLegality(npc,ab).ok||plan.actions.indexOf(ab)>0,`${key} planned an illegal opener`);
  }
  /* OWNER RULING: striking and grappling styles are deliberate counter-play. Balance is only
     compared WITHIN an archetype; a striker losing to a grappler is intended, not a defect. */
  const archetypes={Boxer:"striking",MuayThaiFighter:"striking",Karateka:"striking",
    Judoka:"grappling",Jiujiteiro:"grappling",Wrestler:"grappling"};
  for(const [key,arch] of Object.entries(archetypes))
    assert.equal(AF.ENEMIES[key].archetype,arch,`${key} must be tagged as a ${arch} archetype`);
  const striking=AF.ENEMY_KEYS.filter(k=>AF.ENEMIES[k].archetype==="striking");
  const grappling=AF.ENEMY_KEYS.filter(k=>AF.ENEMIES[k].archetype==="grappling");
  assert.equal(striking.length,3,"three striking style NPCs");
  assert.equal(grappling.length,3,"three grappling style NPCs");
  // The archetype split is real: only the grappling styles carry relationship techniques.
  for(const k of grappling)
    assert(AF.enemyLoadout(k).some(a=>a.effects.some(e=>e.k==="GrappleTech")),
      `${k} is a grappling archetype and must carry relationship techniques`);
  for(const k of striking)
    assert(!AF.enemyLoadout(k).some(a=>a.effects.some(e=>e.k==="GrappleTech")),
      `${k} is a striking archetype and must not carry relationship techniques`);

  // Style-NPC stat totals must match EXACTLY (owner ruling, 2026-08-17): style-vs-style balance
  // testing is only a fair comparison of the KITS if every NPC brings the same total stat
  // budget to it — kits differ in how they spend a stat spread, not in how much of one they
  // get. (Round-robin testing had found MuayThaiFighter at 44 against every other style's
  // 47-49, a plain stat-budget outlier that skewed Boxer vs Muay Thai to 75/25 independent of
  // either kit's own numbers — an earlier, looser version of this test only caught totals
  // drifting >2.5 from the average; this is the tightened follow-up.)
  {const totals=Object.fromEntries(AF.ENEMY_KEYS.filter(k=>[...striking,...grappling].includes(k))
    .map(k=>[k,Object.values(AF.ENEMIES[k].stats).reduce((a,b)=>a+b,0)]));
   const vals=Object.values(totals);
   for(const [k,t] of Object.entries(totals))
     assert.equal(t,vals[0],`${k}'s total stat budget (${t}) must exactly match every other style NPC's — totals: ${JSON.stringify(totals)}`);}

  // A grappling NPC actually pursues standing grapple -> mount -> submission, checked stage
  // by stage rather than counting rounds. Judo Chop's 2026-08-15 combo-starter redesign (2
  // slots, marks the user for a bonus-DC Clinch) now precedes the entry: Stance 1 + Judo Chop
  // 2 + Clinch 1 = 4, leaving Sweeping Shoulder and Cross Choke for later rounds. Judo Chop
  // has no hard oncePerRound cap (a player may deliberately queue a second copy), but the
  // planner devalues a repeat SelfMark heavily, so it should not pick Judo Chop twice here on
  // its own. Each stage is set up directly (the same pattern the AI-legality test below uses)
  // so the check does not depend on any round's contests actually rolling successfully.
  AF.setSeed(5);
  const jd=AF.ENEMIES.Judoka;
  const judoka=AF.makeFighter({name:"Judoka",sign:"Aries",stats:{...jd.stats},faction:0,cell:AF.hx(0,0),abilities:AF.enemyLoadout("Judoka"),persona:jd.persona});
  const target=AF.makeFighter({name:"Foe",sign:"Leo",stats:{STR:11,AGI:11,FORT:11,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  const jb=new AF.Battle([judoka,target],AF.makeArena(5));
  const opening=AF.planFor(jb,judoka,0.1).actions.map(a=>a.name);
  assert(opening.includes("Clinch"),
    `Judoka must open with the standing-grapple entry, got ${opening.join(" · ")}`);
  AF.enterStandingGrapple(jb,judoka,target,5);
  const standing=AF.planFor(jb,judoka,0.1).actions.map(a=>a.name);
  assert(standing.includes("Sweeping Shoulder"),
    `Judoka must plan the mount transition once standing-grappling, got ${standing.join(" · ")}`);
  AF.enterMount(jb,judoka,target,{voluntary:false});
  const mounted=AF.planFor(jb,judoka,0.1).actions.map(a=>a.name);
  assert(mounted.includes("Cross Choke"),
    `Judoka must follow up with the submission once Mount is established, got ${mounted.join(" · ")}`);
  // the projected chain is bounded so a failed entry does not waste the whole round
  assert(AF.BAL.aiMaxProjectedChain>=1&&AF.BAL.aiMaxProjectedChain<=3,"projected AI chain depth stays bounded");
  // a fighter whose position offers no legal offence takes the explicit release path
  const box=AF.makeFighter({name:"Boxer",sign:"Aries",stats:{...AF.ENEMIES.Boxer.stats},faction:0,cell:AF.hx(0,0),abilities:AF.enemyLoadout("Boxer"),persona:"aggressive"});
  const bot=AF.makeFighter({name:"Bot",sign:"Leo",stats:{STR:11,AGI:11,FORT:11,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  const bb=new AF.Battle([box,bot],AF.makeArena(5));
  AF.enterMount(bb,box,bot,{voluntary:false});
  assert(!box.abilities.some(a=>AF.positionalLegality(box,a).ok&&a.effects.some(e=>e.k==="Damage")),
    "Boxing is entirely Mount-illegal, so a mounting Boxer has no legal offence");
  AF.planFor(bb,box,0.1);
  assert.equal(box.releaseIntent,true,"an NPC holding a position it cannot use releases it instead of stalling");
  // a controlled fighter has no release path
  bot.releaseIntent=false;AF.planFor(bb,bot,0.1);
  assert.equal(bot.releaseIntent,false,"a Mounted fighter cannot release its way out");
})();

/* ---------- Rolling Throw: player-aimed destination (2026-08-15) ---------- */
(function rollingThrowAim(){
  const judo=kit(["Judo"]);
  const rolling=find(judo,"Rolling Throw"),stance=find(judo,"Judo Stance");
  function setup(seed){
    AF.setSeed(seed);
    const a=fighter("A",0,0,0,judo,true);a.activeMartial=stance;
    const b=fighter("B",1,1,0,[]);
    // Rolling Throw's grapple-tech contest is a real roll; a weak B guarantees it lands so
    // the test isolates throw DESTINATION behavior, not contest variance.
    b.stats.STR=2;b.stats.AGI=2;
    const B=new AF.Battle([a,b],AF.makeArena(5));
    AF.enterStandingGrapple(B,a,b,5);
    a.stam=99;a.chakra=99;a.supplies=99;
    return{B,a,b};
  }
  // Unaimed: the abilities sheet's "3 tiles away from user", landing on the thrower's far side (user ruling
  // 2026-10-15: the thrown fighter goes over the thrower's head, as the approved Rolling Throw animation shows).
  {const{B,a,b}=setup(1);const before={...b.cell};
   AF.resolveRound(B,[{owner:a,actions:[rolling],moveTo:null},{owner:b,actions:[],moveTo:null}]);
   const far=AF.hx(a.cell.q+3*(a.cell.q-before.q),a.cell.r+3*(a.cell.r-before.r));
   assert.equal(b.cell.q,far.q);assert.equal(b.cell.r,far.r);
   assert.equal(AF.hdist(a.cell,b.cell),3,"an unaimed Rolling Throw lands the target 3 tiles from the thrower");
   assert.notEqual(JSON.stringify(b.cell),JSON.stringify(before),"an unaimed Rolling Throw still moves the target by default");}
  // Aimed within the authored throw range: lands exactly at the chosen point.
  {const{B,a,b}=setup(1);const aim=AF.hx(2,-1);
   assert(AF.hdist(b.cell,aim)<=rolling.effects.find(e=>e.k==="GrappleTech").throw,"test aim must be in range");
   AF.resolveRound(B,[{owner:a,actions:[{ability:rolling,target:null,point:aim}],moveTo:null},{owner:b,actions:[],moveTo:null}]);
   assert.equal(b.cell.q,aim.q);assert.equal(b.cell.r,aim.r,"a player-aimed Rolling Throw lands the target exactly where chosen");}
  // Aimed beyond the authored throw range: the player-targeting sanitizer rejects the whole
  // action rather than silently substituting the default, matching how out-of-range AoE
  // placement already behaves.
  {const{B,a,b}=setup(1);const before={...b.cell};const tooFar=AF.hx(5,-5);
   AF.resolveRound(B,[{owner:a,actions:[{ability:rolling,target:null,point:tooFar}],moveTo:null},{owner:b,actions:[],moveTo:null}]);
   assert.equal(b.cell.q,before.q);assert.equal(b.cell.r,before.r,"an out-of-range aim is stripped by the sanitizer, not silently redirected");
   assert(B.log.some(x=>/can't throw that far/.test(x.text)),"the rejection names the reason");}
  // Hip Toss: a landed toss puts the target Prone in the cell behind the thrower and ends the hold
  {const toss=find(judo,"Hip Toss");let landed=false;
   for(let seed=1;seed<40&&!landed;seed++){const{B,a,b}=setup(seed);const before={...b.cell};
     AF.resolveRound(B,[{owner:a,actions:[toss],moveTo:null},{owner:b,actions:[],moveTo:null}]);
     if(!B.events.some(e=>e.type==="hit"&&e.who===b))continue;landed=true;
     assert.equal(b.cell.q,a.cell.q+(a.cell.q-before.q));assert.equal(b.cell.r,a.cell.r+(a.cell.r-before.r),"Hip Toss lands the target behind the thrower");
     assert(B.log.some(x=>/thrown down behind A — Prone/.test(x.text)),"Hip Toss puts the target Prone (1 round, so it has ticked off by the round's end)");
     assert.equal(AF.relRole(a),AF.REL.FREE,"Hip Toss ends the hold");}
   assert(landed,"some seed lands the Hip Toss");}
  console.log("  Rolling Throw aiming OK");
})();

/* ---------- AI never targets what it cannot perceive (2026-08-15) ---------- */
(function aiPerception(){
  // resolveSingleEnemy's fallback (used by every AI-planned action, since planFor pushes bare
  // ability objects with no explicit target) must pick the nearest PERCEIVED enemy, not the
  // nearest enemy by raw distance — Stealth, awareness range and line of sight all apply.
  const boxing=kit(["Boxing"]);
  const jab=find(boxing,"Jab-Cross"),stance=find(boxing,"Boxing Stance");
  {const attacker=fighter("AI",0,0,0,boxing);attacker.activeMartial=stance;attacker.stam=99;
   const hidden=fighter("Hidden",1,1,0,[]);
   hidden.statuses.push({kind:"Stealth",rounds:99,stacks:1,tick:0,mag:0});
   const B=new AF.Battle([attacker,hidden],AF.makeArena(5));
   const hpBefore=hidden.hp;
   AF.resolveRound(B,[{owner:attacker,actions:[jab],moveTo:null},{owner:hidden,actions:[],moveTo:null}]);
   assert.equal(hidden.hp,hpBefore,"a Stealthed fighter takes no damage from an AI's blind attack");
   assert(B.log.some(x=>/has no target/.test(x.text)),"the AI's action reports finding no target, not a wasted hit on a hidden foe");}
  // Same guarantee end to end: with a nearer Stealthed foe and a farther visible one, a full
  // round must land damage on the visible foe, never the hidden one closer at hand.
  {AF.setSeed(3);
   const attacker=fighter("AI",0,0,0,boxing);attacker.activeMartial=stance;attacker.stam=99;
   const near=fighter("Near",1,1,0,[]);near.statuses.push({kind:"Stealth",rounds:99,stacks:1,tick:0,mag:0});
   const far=fighter("Far",1,3,0,[]);
   const B=new AF.Battle([attacker,near,far],AF.makeArena(5));
   const nearHpBefore=near.hp;
   AF.resolveRound(B,[{owner:attacker,actions:[jab],moveTo:null},{owner:near,actions:[],moveTo:null},{owner:far,actions:[],moveTo:null}]);
   assert.equal(near.hp,nearHpBefore,"the nearer Stealthed foe takes no damage even with a farther visible foe also in play");
   console.log("  AI perception OK");}
})();

/* ---------- AI planner stops wasting resources on unreachable/unperceived targets
   (2026-08-17) ---------- */
(function plannerAvoidsWastedAttacks(){
  // planFor's score() used to evaluate every melee ability as if the actor were already at
  // point-blank range, regardless of real distance, and fell back to the nearest RAW enemy
  // (ignoring perception) for attack scoring whenever nothing was currently perceived. Both let
  // the AI queue a melee attack it could not possibly land — which then paid its Stamina cost
  // in full before fizzling with "too far" / "has no clear line" at resolution.
  const boxing=kit(["Boxing"]);
  const stance=find(boxing,"Boxing Stance");
  const meleeNames=new Set(boxing.filter(a=>a.atk==="Melee"&&a.effects.some(e=>e.k==="Damage")).map(a=>a.name));
  {// Far out of range: no plausible movement budget closes this gap in one round.
   const grid=AF.makeArena(20);
   const actor=AF.makeFighter({name:"AI",sign:"Aries",stats:{STR:12,AGI:12,FORT:12,INT:10,CHA:10},faction:0,cell:AF.hx(-8,0),abilities:boxing,isPlayer:false});
   actor.activeMartial=stance;
   const foe=AF.makeFighter({name:"Foe",sign:"Leo",stats:{STR:12,AGI:12,FORT:12,INT:10,CHA:10},faction:1,cell:AF.hx(15,0),abilities:[],isPlayer:false});
   const B=new AF.Battle([actor,foe],grid);
   AF.setSeed(7);
   const plan=AF.planFor(B,actor,0.12);
   assert(!plan.actions.some(a=>meleeNames.has(a.name)),"a fighter 23 tiles from its foe must not plan a melee attack it cannot possibly reach this round");
   assert(plan.moveTo,"the far-apart fighter should still plan to move toward the foe");}
  {// Adjacent but Stealthed: in range, but not perceived — must not plan an attack on it either.
   const actor=fighter("AI",0,0,0,boxing);actor.activeMartial=stance;
   const foe=fighter("Foe",1,1,0,[]);foe.statuses.push({kind:"Stealth",rounds:99,stacks:1,tick:0,mag:0});
   const B=new AF.Battle([actor,foe],AF.makeArena(5));
   AF.setSeed(7);
   const plan=AF.planFor(B,actor,0.12);
   assert(!plan.actions.some(a=>meleeNames.has(a.name)),"a fighter adjacent to an unperceived (Stealthed) foe must not plan a melee attack on it");}
  console.log("  AI planner avoids unreachable/unperceived attacks OK");
})();

/* ---------- Multi-round approach: Movement Credit unlocks a same-round follow-up
   (2026-08-18) ---------- */
(function plannerUsesMcForFollowUp(){
  // approachDist used to be a single value computed once at the top of planFor from the
  // actor's base movement budget alone. A queued Movement Credit self-buff (Shadow Step,
  // Mach Dash, ...) scored as a flat, distance-blind bonus and never actually shrank the
  // reachability figure later slots were scored against — so the AI could queue a
  // gap-closing buff and then still refuse to queue the very attack it just enabled, because
  // every subsequent slot still saw the stale, un-updated distance. Shadow Step (MC+10) at a
  // distance the base budget alone can't close, but MC+10 easily can, must now also queue a
  // real follow-up melee attack in the same plan.
  const shadowStep=AF.KITS.Scorpio.tai.find(a=>a.name==="Shadow Step");
  const numbing=AF.KITS.Scorpio.tai.find(a=>a.name==="Numbing Strike");
  const stats={STR:13,AGI:17,FORT:8,INT:5,CHA:15};
  const actor=AF.makeFighter({name:"AI",sign:"Scorpio",stats,faction:0,cell:AF.hx(0,0),abilities:[shadowStep,numbing],isPlayer:false});
  const foe=AF.makeFighter({name:"Foe",sign:"Leo",stats:{STR:12,AGI:12,FORT:12,INT:10,CHA:10},faction:1,cell:AF.hx(5,0),isPlayer:false});
  const B=new AF.Battle([actor,foe],AF.makeArena(15));
  assert(B.perceives(actor,foe),"the foe must be within perceived range for this to test MC reachability, not the perception gate");
  assert(AF.DR.mc(stats)<AF.hdist(actor.cell,foe.cell)-1,"base movement budget alone must not be enough to reach melee range");
  AF.setSeed(7);
  const plan=AF.planFor(B,actor,0.12);
  assert(plan.actions.some(a=>a.name==="Shadow Step"),"the gap-closing Movement Credit ability should be queued");
  assert(plan.actions.some(a=>a.name==="Numbing Strike"),"the melee follow-up it enables should also be queued in the same plan");
  console.log("  AI planner values Movement Credit for a same-round follow-up attack OK");
})();

/* ---------- Resource refund when an action never gets a real chance to land (2026-08-17)
   ---------- */
(function refundOnStructuralFailure(){
  // resolveAction paid an ability's Stamina/Chakra cost BEFORE resolveSingleEnemy determined
  // whether the target was even reachable/perceived — so a queued action against a hopeless
  // target (no target, Stealthed, out of reach, no line of sight) silently wasted the cost. A
  // miss (evaded) or a parry (wardNext) is a real, legitimately-paid-for attempt and must NOT
  // be refunded; only a structural "this could never have landed" failure should be.
  const boxing=kit(["Boxing"]);
  const jab=find(boxing,"Jab-Cross"),stance=find(boxing,"Boxing Stance");
  function stamAfter(queueAction){
    const attacker=fighter("AI",0,0,0,boxing);attacker.activeMartial=stance;attacker.stam=50;
    const hidden=fighter("Hidden",1,1,0,[]);hidden.statuses.push({kind:"Stealth",rounds:99,stacks:1,tick:0,mag:0});
    const B=new AF.Battle([attacker,hidden],AF.makeArena(5));
    AF.resolveRound(B,[{owner:attacker,actions:queueAction?[jab]:[],moveTo:null},{owner:hidden,actions:[],moveTo:null}]);
    return attacker.stam;
  }
  assert.equal(stamAfter(true),stamAfter(false),"a Jab-Cross that fizzles against an unperceived (Stealthed) foe must cost nothing net — refunded, not just logged");
  console.log("  resource refund on structural action failure OK");
})();

/* ---------- AI doesn't burn its action budget "restoring" already-full resources
   (2026-08-18) ---------- */
(function noWastedSelfCareWhenFull(){
  // Catch Breath / Charge Chakra ("Focus") / Recompose previously scored a flat 1.5 whenever
  // the matching pool was at or above 30% — including a fresh fighter sitting at 100%. Combined
  // with the out-of-range/unperceived attack gate (which scores those near zero), a fighter
  // that couldn't yet reach its foe had nothing else competing above the picker's threshold, so
  // it spent its whole action budget each round "restoring" Stamina/Chakra/Poise it never lost.
  const st=AF.makeFighter({name:"StreetThug",sign:"Aries",stats:AF.ENEMIES.StreetThug.stats,faction:1,cell:AF.hx(-8,0),abilities:AF.enemyLoadout("StreetThug")});
  const foe=AF.makeFighter({name:"Foe",sign:"Leo",stats:{STR:12,AGI:12,FORT:12,INT:10,CHA:10},faction:0,cell:AF.hx(15,0),abilities:[],isPlayer:true});
  assert.equal(st.stam,st.maxStam,"test setup: fighter must start at full Stamina");
  assert.equal(st.chakra,st.maxChakra,"test setup: fighter must start at full Chakra");
  assert.equal(st.poise,st.maxPoise,"test setup: fighter must start at full Poise");
  const B=new AF.Battle([st,foe],AF.makeArena(20));
  AF.setSeed(7);
  const plan=AF.planFor(B,st,0.12);
  assert.equal(plan.actions.length,0,"a fully-rested fighter that can't yet reach its foe should plan no actions at all, not fill its budget with no-op self-care");
  console.log("  AI skips self-care abilities when already at full resources OK");
})();

/* ---------- Awareness range is CHA only, and the AI never tracks an enemy it hasn't actually
   perceived (2026-08-18, owner ruling) ---------- */
(function chaOnlyAwarenessAndFogOfWar(){
  // Vision range must scale with CHA alone. INT still drives the separate Stealth-detection
  // contest (DR.perception) but must not leak into how far a fighter can simply see.
  const base={STR:10,AGI:10,FORT:10,INT:10,CHA:10};
  assert.equal(AF.DR.awareness(base),AF.DR.awareness({...base,INT:40}),"raising INT alone must not extend vision range");
  assert(AF.DR.awareness({...base,CHA:20})>AF.DR.awareness(base),"raising CHA must extend vision range");

  // A fighter that once saw an enemy, who has since moved out of view, must chase that stale
  // remembered position — never the enemy's true current position. This is what actually keeps
  // the AI honest: real fog of war, not just a suppressed attack roll.
  // Stale memory and the enemy's true live position are placed in OPPOSITE directions from the
  // tracker, so "closing in on the memory" and "closing in on the true position" can't be
  // conflated by geometry — only a genuine live-position leak would move the tracker toward b.
  const a=fighter("Tracker",0,0,0,[]);
  const b=fighter("Ghost",1,20,0,[]);
  const stale=AF.hx(-10,0);
  const trueDistBefore=AF.hdist(a.cell,b.cell);
  const B=new AF.Battle([a,b],AF.makeArena(25));
  a.enemyMemory.set(b,{...stale}); // overwrite the spawn-seeded memory with an older sighting
  AF.setSeed(7);
  const plan=AF.planFor(B,a,0.12);
  assert(plan.moveTo,"the tracker must still have somewhere to move");
  assert(AF.hdist(plan.moveTo,stale)<AF.hdist(a.cell,stale),"the tracker must close in on the STALE remembered position");
  assert(AF.hdist(plan.moveTo,b.cell)>=trueDistBefore,"the tracker must make no progress toward the enemy's true, unperceived live position — it moved the opposite way, toward stale memory instead");

  // Spawning further apart than anyone's awareness range (a real case now that maps scale up)
  // must not leave the AI with nothing to do at all — Battle seeds every fighter's memory with
  // each enemy's spawn cell precisely so this can't happen.
  const c=fighter("Far",0,-10,0,[]);
  const d=fighter("Away",1,10,0,[]);
  const B2=new AF.Battle([c,d],AF.makeArena(25));
  assert(AF.hdist(c.cell,d.cell)>AF.DR.awareness(AF.eff(c)),"test setup: must actually start outside awareness range");
  AF.setSeed(7);
  const plan2=AF.planFor(B2,c,0.12);
  assert(plan2.moveTo,"a fighter spawned outside awareness range must still have a spawn-seeded memory to move toward, not freeze in place");
  console.log("  CHA-only awareness + fog-of-war memory (not omniscient tracking) OK");
})();

/* ---------- Kicks are illegal while grappling (2026-08-15) ---------- */
(function kicksBlockedWhileGrappling(){
  const rows=kit(["MuayThai","Karate"]);
  const legalIn=(name,role)=>{
    const ab=find(rows,name);
    const dummy=fighter("D",0,0,0,[]);
    return AF.positionalLegality(dummy,ab,role).ok;
  };
  for(const n of ["Roundhouse Kick","Teep Kick","Calf Kick","Sweeping Low","Side Kick","Whirlwind Kick"]){
    assert(legalIn(n,REL.FREE),`${n} must be usable while Free`);
    assert(!legalIn(n,REL.GRAPPLING),`${n} must be illegal while Grappling`);
    assert(!legalIn(n,REL.GRAPPLED),`${n} must be illegal while Grappled`);
  }
  // Close-range strikes are unaffected: a clinch does not stop a punch, elbow or knee.
  for(const n of["Elbow Strike","Hammer Fist","Jab-Cross","Uppercut"])
    assert(legalIn(n,REL.GRAPPLING),`${n} (not a kick) must stay legal while Grappling`);
  console.log("  kicks blocked while grappling OK");
})();

/* ---------- Ground hazards: Spike Pit / Caltrops linger on the map (2026-08-16) ---------- */
(function groundHazards(){
  const spikePit=AF.generalArts().find(a=>a.name==="Spike Pit");
  assert(spikePit.effects.length===1&&spikePit.effects[0].k==="Terrain"&&spikePit.effects[0].trigger,
    "Spike Pit is a lingering hazard (Terrain+trigger), not an instant burst");
  const cell=AF.hx(0,0);
  // Casting directly on the caster's own cell: the hazard is registered, an onlooker
  // elsewhere is untouched, and — critically — the owner standing right on top of their
  // own trap is immune, both at the instant it's laid and on the next round's hazard tick.
  {const caster=fighter("Trapper",0,0,0,[spikePit],true);caster.stam=99;caster.chakra=99;caster.supplies=99;
   const bystander=fighter("Bystander",1,4,0,[]);
   const B=new AF.Battle([caster,bystander],AF.makeArena(5));
   const casterHpBefore=caster.hp;
   AF.resolveRound(B,[{owner:caster,actions:[{ability:spikePit,target:null,point:cell}],moveTo:null},{owner:bystander,actions:[],moveTo:null}]);
   assert.equal(B.grid.terrainAt(cell),"Spikes","the cast leaves Spikes terrain on the target cell");
   const hz=B.grid.hazardAt(cell);
   assert(hz&&hz.effects.some(e=>e.k==="Damage"),"the cell carries a hazard trigger with the trap's damage effect");
   assert.equal(bystander.hp,bystander.maxHp,"nobody standing elsewhere is hurt by placing the trap");
   assert.equal(caster.hp,casterHpBefore,"laying the trap on your own cell doesn't hurt you");
   AF.resolveRound(B,[{owner:caster,actions:[],moveTo:null},{owner:bystander,actions:[],moveTo:null}]);
   assert.equal(caster.hp,casterHpBefore,"the round-tick hazard pass never hurts the trap's own owner either");}
  // Stepping onto the hazard cell later triggers it, and it survives (re-triggers) until its
  // authored 3-round duration expires.
  {const caster=fighter("Trapper",0,-2,0,[spikePit],true);caster.stam=99;caster.chakra=99;caster.supplies=99;
   const victim=fighter("Victim",1,2,0,[]);
   const B=new AF.Battle([caster,victim],AF.makeArena(5));
   AF.resolveRound(B,[{owner:caster,actions:[{ability:spikePit,target:null,point:cell}],moveTo:null},{owner:victim,actions:[],moveTo:null}]);
   assert(B.grid.hazardAt(cell),"the hazard is live the round it's placed");
   const hpBefore=victim.hp;
   AF.resolveRound(B,[{owner:caster,actions:[],moveTo:null},{owner:victim,actions:[],moveTo:cell}]);
   assert(victim.hp<hpBefore,"walking onto the Spikes hazard deals damage");
   assert(B.log.some(x=>/sets off Trapper's Spike Pit/.test(x.text)),"the log names who triggered whose trap");
   assert(B.grid.hazardAt(cell),"the hazard is still live for round 2 of its 3-round duration");
   const hpAfterFirstHit=victim.hp;
   // Round 3: still standing in it, so it re-triggers again before finally lapsing.
   AF.resolveRound(B,[{owner:caster,actions:[],moveTo:null},{owner:victim,actions:[],moveTo:null}]);
   assert(victim.hp<hpAfterFirstHit,"a lingering hazard hurts you again each round you stay on it");
   assert.equal(B.grid.terrainAt(cell),"Open","the hazard tile reverts to Open once its 3-round duration lapses");
   assert(!B.grid.hazardAt(cell),"the hazard trigger is cleared along with the terrain");}
  console.log("  ground hazards OK");
})();

/* ---------- Recompose: a third Focus action, poise instead of stam/chakra (2026-08-16) ---------- */
(function recomposeFocus(){
  const recompose=AF.generalArts().find(a=>a.name==="Recompose");
  assert(recompose&&recompose.tags.includes("Focus"),"Recompose is registered as a Focus action");
  assert.equal(recompose.stam,0,"Recompose has no flat stamina cost");
  assert.equal(recompose.stamPct,AF.BAL.recomposeCostPercent,"Recompose costs a % of max stamina instead");
  assert.equal(recompose.chakraPct,AF.BAL.recomposeCostPercent,"Recompose costs a % of max chakra instead");
  // Costs the right % of max pools and restores poise, unlike Catch Breath / Charge Chakra.
  // Starting pools are deliberately mid-range: high enough to afford the cost, low enough
  // that neither the cost nor the restore clips against a 0/max clamp, and clear of poise's
  // "hits 0 -> snaps back to full next round" rule, which a bare 0 would trigger and mask
  // Recompose's own contribution entirely. The round's ordinary passive regen (stamina/chakra
  // at end of round, poise at start of round) still happens regardless, so it's folded into
  // the expected values via the same DR formulas the engine itself uses.
  {const a=fighter("A",0,0,0,[recompose],true);
   a.stam=50;a.chakra=50;a.poise=50;
   const b=fighter("B",1,4,0,[]);
   const B=new AF.Battle([a,b],AF.makeArena(5));
   const costStam=Math.round(a.maxStam*AF.BAL.recomposeCostPercent),costChakra=Math.round(a.maxChakra*AF.BAL.recomposeCostPercent);
   const poiseRegen=AF.DR.poiseRegen(a.stats);
   const stamRegen=Math.round(AF.DR.stamRegen(a.stats)*AF.passiveStaminaFactor(AF.REL.FREE));
   const chakraRegen=AF.DR.chakRegen(a.stats);
   AF.resolveRound(B,[{owner:a,actions:[recompose],moveTo:null},{owner:b,actions:[],moveTo:null}]);
   assert.equal(a.stam,Math.min(a.maxStam,50-costStam+stamRegen),"costs 10% of max stamina (net of the round's passive regen)");
   assert.equal(a.chakra,Math.min(AF.effMaxChakra(a),50-costChakra+chakraRegen),"costs 10% of max chakra (net of the round's passive regen)");
   assert.equal(a.poise,Math.min(a.maxPoise,50+poiseRegen+Math.round(a.maxPoise*AF.BAL.focusRestorePercent)),"restores 20% of max poise on top of the round's passive regen");}
  // No effect while Mounted (pinned) — the resource is still spent, but poise doesn't move.
  {const{a:top,b:bottom,B}=mountPair();
   bottom.abilities=[recompose];bottom.poise=0;bottom.stam=bottom.maxStam;bottom.chakra=bottom.maxChakra;
   AF.resolveRound(B,[{owner:top,actions:[],moveTo:null},{owner:bottom,actions:[recompose],moveTo:null}]);
   assert.equal(bottom.poise,0,"Recompose grants no poise while Mounted");}
  console.log("  Recompose Focus action OK");
})();

/* ---------- A broken guard climbs back gradually, not a free full reset (2026-08-17) ---------- */
(function poiseBreakNoFullReset(){
  const a=fighter("A",0,0,0,[],true);
  const b=fighter("B",1,4,0,[]);
  const B=new AF.Battle([a,b],AF.makeArena(5));
  // Simulate the state applyDamage leaves a fighter in the instant their guard cracks.
  a.poise=0;a.poiseRecoverDelay=1;
  const regen=AF.DR.poiseRegen(a.stats);
  assert(regen<a.maxPoise,"sanity: normal passive poise regen is a fraction of max, not a full refill");
  AF.resolveRound(B,[{owner:a,actions:[],moveTo:null},{owner:b,actions:[],moveTo:null}]);
  assert.equal(a.poise,0,"the round right after breaking is still a recovery-delay round: no regen yet");
  AF.resolveRound(B,[{owner:a,actions:[],moveTo:null},{owner:b,actions:[],moveTo:null}]);
  assert.equal(a.poise,Math.min(a.maxPoise,regen),"once the delay lapses, a broken guard regens at the ordinary passive rate — it does not snap back to max");
  console.log("  poise break has no full reset OK");
})();

/* ---------- Side Kick: unconditional push on a landed hit, no separate save (2026-08-17) ---------- */
(function sideKickPush(){
  const karate=kit(["Karate"]);
  const sideKick=find(karate,"Side Kick"),stance=find(karate,"Karate Stance");
  assert.deepStrictEqual(sideKick.effects.find(e=>e.k==="Push"),{k:"Push",tiles:1},"Side Kick carries a plain 1-tile Push, no save wrapper");
  AF.setSeed(1);
  // A lopsided matchup so the base attack roll — the only roll gating this — reliably lands.
  const a=AF.makeFighter({name:"A",sign:"Aries",stats:{STR:20,AGI:20,FORT:14,INT:10,CHA:20},faction:0,cell:AF.hx(-1,0),abilities:karate,isPlayer:true});
  a.activeMartial=stance;a.stam=99;
  const b=AF.makeFighter({name:"B",sign:"Aries",stats:{STR:1,AGI:1,FORT:14,INT:1,CHA:1},faction:1,cell:AF.hx(0,0)});
  const B=new AF.Battle([a,b],AF.makeArena(5));
  assert.equal(AF.hdist(a.cell,b.cell),1,"test setup sanity: target starts adjacent to the attacker");
  AF.resolveRound(B,[{owner:a,actions:[sideKick],moveTo:null},{owner:b,actions:[],moveTo:null}]);
  assert.equal(AF.hdist(a.cell,b.cell),2,"a landed Side Kick pushes the target 1 tile further away, straight back from the attacker");
  console.log("  Side Kick unconditional push OK");
})();

/* ---------- Movement-phase collision resolution is AGI-priority, not plan-array order (2026-08-17) ---------- */
(function movementPriority(){
  const a=fighter("Fast",0,-2,0,[],true);a.stats.AGI=40;
  const b=fighter("Slow",1,2,0,[]);b.stats.AGI=12;
  const B=new AF.Battle([a,b],AF.makeArena(5));
  const target=AF.hx(0,0);
  // Both fighters plan to move to the exact same cell. Slow is listed FIRST in the plans array
  // — if resolution still went by array order rather than AGI, it would win the contested cell.
  AF.resolveRound(B,[{owner:b,actions:[],moveTo:target},{owner:a,actions:[],moveTo:target}]);
  assert.equal(a.cell.q,target.q);assert.equal(a.cell.r,target.r,"the higher-AGI fighter claims the contested cell even when listed second in the plans array");
  assert.notEqual(JSON.stringify(b.cell),JSON.stringify(target),"the lower-AGI fighter does not also end up on the contested cell");
  assert.equal(AF.hdist(b.cell,target),1,"the lower-AGI fighter instead lands on a cell adjacent to its original target, not stranded unmoved");
  console.log("  movement-phase AGI-priority collision resolution OK");
})();

/* ---------- Opponent/ally level scaling (2026-08-17) ---------- */
(function enemyLevelScaling(){
  const base=AF.ENEMIES.Boxer.stats;
  assert.deepStrictEqual(AF.scaleEnemyStats(base,20),{...base},"level 20 (the canonical baseline every style NPC was balance-tested at) must reproduce the input stats unchanged");
  const low=AF.scaleEnemyStats(base,1),high=AF.scaleEnemyStats(base,100);
  for(const k of Object.keys(base)){
    assert(low[k]<base[k],`level 1 must scale ${k} down from the level-20 baseline`);
    assert(high[k]>base[k],`level 100 must scale ${k} up from the level-20 baseline`);
    assert(low[k]>=AF.BAL.enemyLevelStatFloor,`scaled stats never drop below the floor (${k}=${low[k]})`);
  }
  // Shape is preserved: whichever stat led at baseline still leads after scaling.
  const topStat=Object.entries(base).sort((a,b)=>b[1]-a[1])[0][0];
  assert.equal(Object.entries(high).sort((a,b)=>b[1]-a[1])[0][0],topStat,"scaling doesn't reorder a style's relative stat emphasis");
  console.log("  opponent/ally level scaling OK");
})();

/* ---------- Initiative tie-break: AGI, not plans-array order (2026-08-17) ---------- */
(function initiativeTieBreak(){
  // Force d(BAL.initDie) to always roll 1, so baseInit is exactly AGI+1 for both fighters —
  // no randomness left to fight the deliberately engineered tie.
  AF.setRNG(()=>0);
  const lo=fighter("TieLow",0,-2,0,[]);lo.stats.AGI=20;
  const hi=fighter("TieHigh",1,2,0,[]);hi.stats.AGI=40;
  // selOffset = initWeight(ability) - initBaseActionCost(20). A plain 1-slot ability weighs the
  // 20 baseline (selOffset 0); a plain 3-slot ability weighs 20+2*10=40 (selOffset 20) — exactly
  // enough to cancel TieHigh's +20 AGI edge, so both fighters land on the identical init key.
  const abLow={name:"TieLowMove",id:"tieLowMove",tags:[],slots:1,targeting:"Self",effects:[],stam:0,chakra:0,stamPct:0,chakraPct:0,supply:0,dmg:0};
  const abHigh={name:"TieHighMove",id:"tieHighMove",tags:[],slots:3,targeting:"Self",effects:[],stam:0,chakra:0,stamPct:0,chakraPct:0,supply:0,dmg:0};
  assert.equal(AF.initWeight(abLow)-20,0,"test setup: TieLowMove must have selOffset 0");
  assert.equal(AF.initWeight(abHigh)-20,20,"test setup: TieHighMove must have selOffset 20, matching the 20-point AGI gap");
  const B=new AF.Battle([lo,hi],AF.makeArena(5));
  // TieLow is listed FIRST in plans — under the old array-order tiebreak it would wrongly act
  // first despite the identical key. TieHigh is listed second on purpose.
  AF.resolveRound(B,[{owner:lo,actions:[abLow],moveTo:null},{owner:hi,actions:[abHigh],moveTo:null}]);
  const iLow=B.log.findIndex(x=>/flows into TieLowMove/.test(x.text));
  const iHigh=B.log.findIndex(x=>/flows into TieHighMove/.test(x.text));
  assert(iHigh>=0&&iLow>=0,"both actions must have resolved");
  assert(iHigh<iLow,"on a genuine initiative tie, the higher-AGI fighter acts first even when listed second in the plans array");
  AF.setSeed(13);
  console.log("  initiative tie-break favors AGI over plans-array order OK");
})();

/* ---------- Retarget off a defeated foe, ported from the orphaned dev-continue branch
   (2026-08-17) ---------- */
(function retargetDefeatedTarget(){
  AF.setRNG(()=>0);
  const rtAb={...byName(boxing,"Jab-Cross"),id:"retarget-jab",effects:byName(boxing,"Jab-Cross").effects.map(e=>({...e})),tags:[]};
  const rtOwner=AF.makeFighter({name:"Striker",sign:"Aries",stats:{STR:20,AGI:14,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:[rtAb]});
  const rtDead=AF.makeFighter({name:"Doomed",sign:"Leo",stats:{STR:8,AGI:8,FORT:8,INT:8,CHA:8},faction:1,cell:AF.hx(-1,0),abilities:[]});
  const rtWeak=AF.makeFighter({name:"Weakling",sign:"Leo",stats:{STR:8,AGI:8,FORT:8,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  const rtStrong=AF.makeFighter({name:"Bruiser",sign:"Leo",stats:{STR:8,AGI:8,FORT:8,INT:8,CHA:8},faction:1,cell:AF.hx(0,1),abilities:[]});
  rtWeak.hp=Math.round(rtWeak.maxHp*0.2); // the lowest-HP live foe
  const rtB=new AF.Battle([rtOwner,rtDead,rtWeak,rtStrong],AF.makeArena(5));
  rtDead.hp=0; // the queued target is defeated before the action resolves
  const rtWeakBefore=rtWeak.hp,rtStrongBefore=rtStrong.hp;
  AF.resolveRound(rtB,[{owner:rtOwner,actions:[{ability:rtAb,target:rtDead}],moveTo:null}]);
  assert(rtWeak.hp<rtWeakBefore,"a defeated-target action must redirect to the weakest reachable foe");
  assert.equal(rtStrong.hp,rtStrongBefore,"redirect must pick the lowest-HP foe, not a healthier one in range");
  assert(rtB.log.some(x=>x.text.includes("redirects")),"the retarget must be visible in the combat log");
  // Mid-round: a target the player kills with an earlier queued action makes a later action
  // pointed at that same enemy redirect at resolution time (the engine path, distinct from the
  // player-plan sanitizer path exercised above).
  AF.setRNG(()=>0.5);
  const mrOwner=AF.makeFighter({name:"Duelist",sign:"Aries",stats:{STR:20,AGI:14,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),isPlayer:true,abilities:[rtAb]});
  const mrDead=AF.makeFighter({name:"Fragile",sign:"Leo",stats:{STR:8,AGI:8,FORT:6,INT:8,CHA:8},faction:1,cell:AF.hx(-1,0),abilities:[]});
  const mrWeak=AF.makeFighter({name:"Runt",sign:"Leo",stats:{STR:8,AGI:8,FORT:8,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  mrDead.hp=1;mrWeak.hp=Math.round(mrWeak.maxHp*0.3);
  const mrB=new AF.Battle([mrOwner,mrDead,mrWeak],AF.makeArena(5));
  const mrWeakBefore=mrWeak.hp;
  AF.resolveRound(mrB,[{owner:mrOwner,actions:[{ability:rtAb,target:mrDead},{ability:rtAb,target:mrDead}],moveTo:null}]);
  assert(!AF.alive(mrDead),"the first queued action should have felled the chosen target");
  assert(mrWeak.hp<mrWeakBefore,"a later action pointed at the mid-round-killed target must redirect to the weakest foe");
  AF.setSeed(13);
  console.log("  retarget off a defeated foe (mid-round + start-of-round) OK");
})();

global.__AF_POSITIONAL_SUITE_RAN=true;
})();
assert(global.__AF_POSITIONAL_SUITE_RAN,"the positional regression suite must actually execute");

const html=fs.readFileSync("./astro-fighters-2d-v3.4.html","utf8");
const overlay=fs.readFileSync("./af-progression-v3.js","utf8");
for(const marker of ["statBudgetNote","autoStats","resetStats","Points spent / level budget","14 points at level 1","+5 per level","Copy log",'id="copyLog"','value="ambush"','id="mapSize"'])assert(html.includes(marker),`HTML missing ${marker}`);
assert(html.includes('<script src="af-progression-v3.js"></script>'));
const page=fs.readFileSync("./af-page-v3.js","utf8");
for(const marker of ['scenario==="ambush"','isCaravanScenario','const def=car.faction','Ambush Success','Ambush Failed'])assert(page.includes(marker),`page controller missing ${marker}`);
// map-size scaling (2026-08-18): a bigger roster gets a genuinely bigger arena, not just more
// cells crammed into the same fixed pixel canvas.
for(const marker of ['function computeArenaGeometry','function mapRadiusFor','MAP_SIZES={small:5,medium:7,large:10}','const spawnScale=mapRadius/MAP_SIZES.small'])assert(page.includes(marker),`page controller missing map-size marker ${marker}`);
// status/eye indicators over character tokens
for(const marker of ['STATUS_GLYPH','function fighterIndicators','f.eyeActive)badges.push','canRenderFighter(S.B,viewer,f)'])assert(page.includes(marker),`page controller missing indicator marker ${marker}`);
for(const marker of ['.statind','statind-g','statind.eye','.cost.reach','.reach-outline'])assert(html.includes(marker),`HTML missing style ${marker}`);
// positional combat UI
for(const marker of ['id="relationshipPanel"','.relationship','.rel-role','.rel-sub','rel-release'])assert(html.includes(marker),`HTML missing positional marker ${marker}`);
for(const marker of ['function renderRelationship','function positionalBadge','AFUI.relationshipLabel','or the hold is released','Mounting:"🧗"'])assert(page.includes(marker),`page controller missing positional marker ${marker}`);
// The submission release control is gone: a hold is kept by queueing it, released by not.
assert(!/Release .*submission/i.test(page),"submissions must have no release control");
assert(page.includes('AF.submissionCostMult'),"ability cards must quote the escalated submission cost");
const core=fs.readFileSync("./af-core.js","utf8"),patch=fs.readFileSync("./af-core-v3-patch.js","utf8");
assert(core.includes("function retargetDefeated"),"core missing defeated-target retarget helper");
assert(patch.includes("AF.retargetDefeated"),"player plan sanitizer must retarget a defeated foe instead of dropping the action");
for(const marker of ['function gapClose','ab.reach>0&&dist>1'])assert(core.includes(marker),`core missing reach marker ${marker}`);
for(const marker of ['function reachPerimeter','reach-outline','reachR>0'])assert(page.includes(marker),`page missing reach indicator marker ${marker}`);
for(const marker of ['function moveBudget','round-sep'])assert(core.includes(marker),`core missing marker ${marker}`);
for(const marker of ['.round-sep','.cost.guard'])assert(html.includes(marker),`HTML missing style ${marker}`);
assert(page.includes('a.poiseMult>1'),"ability card missing the guard-break indicator");
// Every NPC key the page hard-codes as a default must exist in the roster.
for(const m of page.matchAll(/"(?:enemy1|enemy2|ally)"\)\.value="([A-Za-z]+)"/g))
  assert(AF.ENEMIES[m[1]],`page controller defaults to a non-existent NPC: ${m[1]}`);
const ui=fs.readFileSync("./af-ui-v3.js","utf8"),mapmod=fs.readFileSync("./af-map-v3.js","utf8");
for(const marker of ['function projectedRelRole','function projectedSubmission','function relationshipLabel','AF.positionalLegality'])assert(ui.includes(marker),`AFUI missing positional marker ${marker}`);
assert(mapmod.includes('AFUI.projectedRelRole'),"map queueContext override must delegate role projection to the core model");
assert(patch.includes('AF.positionalLegality'),"plan sanitizer missing projected positional validation");
assert(core.includes('function relationshipMaintenance'),"core missing the Relationship Maintenance phase");
assert(!core.includes('attemptEscape'),"the legacy Grappled = auto-escape rule must be gone");
assert(!core.includes('submissionUpkeepStamina')&&!core.includes('submissionSlotReserve'),
  "the passive submission upkeep and slot reservation must be gone");
assert(!core.includes('reservedSlots'),"submissions no longer reserve an action slot");
assert(!core.includes('mountGenjutsuDcBonus'),"the obsolete blanket mounted-target DC bonus must be gone");
assert(!/Karate[\s\S]{0,400}Defensive Stance/.test(core.slice(core.indexOf("Karate:{stance:"),core.indexOf("Karate:{stance:")+400)),"Karate Defensive Stance must stay removed");
assert(patch.includes('ab.reach>0'),"patch missing reach-aware targeting gate");
for(const marker of ["legacyStatProxy","queueCanonicalPlayerStats","Auto-spend evenly","trimStatsToBudget","Attribute allocation exceeds","addEventListener('click'"])assert(overlay.includes(marker),`overlay missing ${marker}`);

/* ---------- System 3: ability clashes (2026-08-25) ---------- */
(function jabCrossBurnsThroughParry(){
  // Jab-Cross is a Combo ability now — the jab's own resolveStrike call burns the Parry
  // charge, but the cross gets an independent roll afterward since wardNext is already spent.
  AF.setRNG(()=>0);
  const ken=AF.WEAPONS.Kenjutsu.moves,boxing=AF.MARTIAL.Boxing.moves;
  const parry=ken.find(a=>a.name==="Parry"),jabCross=boxing.find(a=>a.name==="Jab-Cross");
  assert(jabCross.tags.includes("Combo"),"Jab-Cross must carry the Combo tag");
  assert.equal(jabCross.effects.length,2,"Jab-Cross must carry two Damage effects (jab, cross)");
  const def=AF.makeFighter({name:"Parrier2",sign:"Libra",stats:{STR:10,AGI:40,FORT:20,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[parry]});
  const atk=AF.makeFighter({name:"ComboAtk",sign:"Aries",stats:{STR:20,AGI:20,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[jabCross]});
  const jcB=new AF.Battle([def,atk],AF.makeArena(5));const jcHpBefore=def.hp;
  AF.resolveRound(jcB,[{owner:def,actions:[parry],moveTo:null},{owner:atk,actions:[jabCross],moveTo:null}]);
  assert.equal(def.wardNext,0,"the jab must still burn the Parry charge even though the cross gets through");
  assert(def.hp<jcHpBefore,"the cross must land even though the jab into the same Parry was blocked");
  assert(jcB.log.some(x=>x.text.includes("parries")),"the jab's parry must still be logged");
  console.log("  Jab-Cross burns through Parry OK");
})();
(function jabLandsCrossFollowsAutomatically(){
  AF.setRNG(()=>0);
  const jabCross=byName(boxing,"Jab-Cross");
  const def=AF.makeFighter({name:"D3",sign:"Libra",stats:{STR:10,AGI:10,FORT:20,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[]});
  const atk=AF.makeFighter({name:"A3",sign:"Aries",stats:{STR:20,AGI:20,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[jabCross]});
  const jlB=new AF.Battle([def,atk],AF.makeArena(5));const jlHpBefore=def.hp;
  AF.resolveRound(jlB,[{owner:def,actions:[],moveTo:null},{owner:atk,actions:[jabCross],moveTo:null}]);
  assert(jlB.log.some(x=>x.text.includes("cross follows through automatically")),"a landed jab must trigger the automatic, unrollable cross");
  assert(def.hp<jlHpBefore-5,"a fully-landed combo must deal more than either strike alone");
  console.log("  Jab lands -> cross follows through automatically OK");
})();
(function kickMissSetsUpOpponentsShotNotTheMisser(){
  // The beneficiary must be whoever DODGED the kick, never the fighter who threw it — and only
  // when the dodger's own very next queued action is the specific named payoff.
  AF.setRNG(()=>0.99); // guarantees the kick is evaded (roll 99 vs. a hit chance well under 100)
  const karate=AF.MARTIAL.Karate.moves,wrestling=AF.MARTIAL.Wrestling.moves;
  const sideKick=karate.find(a=>a.name==="Side Kick"),singleLeg=wrestling.find(a=>a.name==="Single Leg Shot");
  const striker=AF.makeFighter({name:"Striker2",sign:"Aries",stats:{STR:12,AGI:12,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[sideKick]});
  const wrestler=AF.makeFighter({name:"Wrestler2",sign:"Taurus",stats:{STR:12,AGI:12,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[singleLeg]});
  const kmB=new AF.Battle([striker,wrestler],AF.makeArena(5));
  AF.resolveRound(kmB,[{owner:striker,actions:[sideKick],moveTo:null},{owner:wrestler,actions:[singleLeg],moveTo:null}]);
  assert(kmB.log.some(x=>x.text.includes("reads the miss — the takedown is wide open")),"the dodger must be credited with reading the miss");
  assert(kmB.log.some(x=>x.text.includes(`DC ${AF.BAL.grappleLandDC}+${AF.BAL.kickWhiffShotBonus}`)),"the bonus must actually apply to the wrestler's own following grapple attempt");
  console.log("  kick miss sets up the opponent's queued Single Leg Shot (not the misser) OK");
})();
(function negativeCasesDoNotCrossPollinate(){
  // A kick missing into anything other than the opponent's queued Single Leg Shot grants
  // nothing — including when the very next thing queued is Clinch, the OTHER pairing's payoff.
  AF.setRNG(()=>0.99);
  const karate=AF.MARTIAL.Karate.moves,boxing2=AF.MARTIAL.Boxing.moves;
  const sideKick=karate.find(a=>a.name==="Side Kick"),clinch=boxing2.find(a=>a.name==="Clinch");
  const striker=AF.makeFighter({name:"Striker3",sign:"Aries",stats:{STR:12,AGI:12,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[sideKick]});
  const other=AF.makeFighter({name:"Other3",sign:"Taurus",stats:{STR:12,AGI:12,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[clinch]});
  const ncB=new AF.Battle([striker,other],AF.makeArena(5));
  AF.resolveRound(ncB,[{owner:striker,actions:[sideKick],moveTo:null},{owner:other,actions:[clinch],moveTo:null}]);
  assert(!AF.getStatus(other,"GrappleSetup"),"a kick miss must not set up Clinch — only Single Leg Shot qualifies");
  console.log("  kick miss into the wrong payoff grants nothing OK");
})();
(function upperCutStuffsSingleLegShot(){
  // The flagship Tier 2 signature: bonus damage, a guard-break-caliber poise floor even with no
  // live grapple state, and a costly negate — the shot's stamina is paid, never refunded.
  AF.setRNG(()=>0);
  const uppercut=byName(boxing,"Uppercut"),wrestling2=AF.MARTIAL.Wrestling.moves,singleLeg=wrestling2.find(a=>a.name==="Single Leg Shot");
  const striker=AF.makeFighter({name:"Striker4",sign:"Aries",stats:{STR:16,AGI:30,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[uppercut]});
  const wrestler=AF.makeFighter({name:"Wrestler4",sign:"Taurus",stats:{STR:16,AGI:6,FORT:14,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[singleLeg]});
  const usB=new AF.Battle([striker,wrestler],AF.makeArena(5));const stamBefore=wrestler.stam;
  AF.resolveRound(usB,[{owner:striker,actions:[uppercut],moveTo:null},{owner:wrestler,actions:[singleLeg],moveTo:null}]);
  assert(usB.log.some(x=>x.text.includes("critical uppercut")),"the flagship signature must fire and log a critical hit, not a generic guard-break line");
  assert.equal(AF.relRole(wrestler),AF.REL.FREE,"the negated Single Leg Shot must never establish a grapple");
  // The shot's 15 stamina is deducted then never refunded — only round-end passive regen (same
  // formula the engine already uses) brings it back partway, unlike a free pendingSkips cancel.
  const expectedStam=stamBefore-15+AF.DR.stamRegen(wrestler.stats);
  assert.equal(wrestler.stam,expectedStam,"a Tier 2 negate must still cost the full stamina — only regen, not a refund, changes the number");
  console.log("  Uppercut stuffs Single Leg Shot (bonus dmg + poise floor + costly negate) OK");
})();
(function shotLandsFirstGrantsUppercutGuardBreak(){
  // The mirror direction: a landed shot doesn't weaken the follow-up uppercut, it exposes the
  // wrestler's own guard — floored at the same 2.0 ceiling Choke Slam already sits at.
  const uppercut=byName(boxing,"Uppercut"),wrestling3=AF.MARTIAL.Wrestling.moves,singleLeg=wrestling3.find(a=>a.name==="Single Leg Shot");
  function run(withSetup){
    AF.setRNG(()=>0);
    const wrestler=AF.makeFighter({name:"W5",sign:"Taurus",stats:{STR:30,AGI:20,FORT:14,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[singleLeg]});
    const striker=AF.makeFighter({name:"S5",sign:"Aries",stats:{STR:8,AGI:6,FORT:6,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[uppercut]});
    wrestler.poise=6; // low enough that only the floored 2.0x multiplier breaks it, not a bare 1x Uppercut
    const B=new AF.Battle([wrestler,striker],AF.makeArena(5));
    const actions=withSetup?[{owner:wrestler,actions:[singleLeg],moveTo:null},{owner:striker,actions:[uppercut],moveTo:null}]
                            :[{owner:striker,actions:[uppercut],moveTo:null}];
    AF.resolveRound(B,actions);
    return{broke:wrestler.pendingSkips>0,log:B.log};
  }
  const without=run(false);
  assert(!without.broke,"control: a bare Uppercut against a low-but-not-trivial poise pool must not break it on its own");
  const withSetup=run(true);
  assert(withSetup.broke,"a landed Single Leg Shot must grant the wrestler's own next Uppercut a guard-break-caliber poise floor");
  assert(withSetup.log.some(x=>x.text.includes("guard is wide open")),"the setup must be logged when the shot lands");
  console.log("  Single Leg Shot landing sets up the wrestler's own Uppercut for a guard break OK");
})();
(function parryPunishesKarateBlitzWithInitiative(){
  // Parry already negates Karate Blitz for free via wardNext; this signature is the extra
  // reward for reading something that fast at all.
  AF.setRNG(()=>0);
  const ken=AF.WEAPONS.Kenjutsu.moves,karate2=AF.MARTIAL.Karate.moves;
  const parry2=ken.find(a=>a.name==="Parry"),blitz=karate2.find(a=>a.name==="Karate Blitz");
  const def=AF.makeFighter({name:"Def6",sign:"Libra",stats:{STR:10,AGI:40,FORT:20,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[parry2]});
  const atk=AF.makeFighter({name:"Atk6",sign:"Aries",stats:{STR:20,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(2,0),abilities:[blitz]});
  const pkB=new AF.Battle([def,atk],AF.makeArena(5));
  AF.resolveRound(pkB,[{owner:def,actions:[parry2],moveTo:null},{owner:atk,actions:[blitz],moveTo:null}]);
  assert(pkB.log.some(x=>x.text.includes("parries")&&x.text.includes("Karate Blitz")),"Karate Blitz must still be negated for free by the parry");
  assert(pkB.log.some(x=>x.text.includes("punishes the read")),"the signature reward must fire on top of the free negation");
  console.log("  Parry punishes Karate Blitz (negate + initiative reward) OK");
})();
(function poiseBreakCollisionClearsStaleNegate(){
  // When a floored hit is big enough to also break poise outright, the free pendingSkips
  // stagger fires first in the picking loop (before resolveAction ever runs) — pendingClashNegate
  // must not survive to wrongly fire on some later, unrelated action.
  AF.setRNG(()=>0);
  const uppercut=byName(boxing,"Uppercut"),wrestling4=AF.MARTIAL.Wrestling.moves,singleLeg=wrestling4.find(a=>a.name==="Single Leg Shot");
  const striker=AF.makeFighter({name:"Striker7",sign:"Aries",stats:{STR:30,AGI:30,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[uppercut]});
  const wrestler=AF.makeFighter({name:"Wrestler7",sign:"Taurus",stats:{STR:16,AGI:6,FORT:14,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[singleLeg]});
  wrestler.poise=10; // low enough that the flagship's floored (2.0x) poise hit zeroes it outright
  const cB=new AF.Battle([striker,wrestler],AF.makeArena(5));const stamBefore=wrestler.stam;
  AF.resolveRound(cB,[{owner:striker,actions:[uppercut],moveTo:null},{owner:wrestler,actions:[singleLeg],moveTo:null}]);
  assert(cB.log.some(x=>x.text.includes("guard shatters")),"a low enough poise pool must still break outright under the floored hit");
  assert(cB.log.some(x=>x.text.includes("is staggered")),"the free stagger-cancel must be what actually skips the Single Leg Shot");
  assert(!cB.log.some(x=>x.text.includes("is read and stopped cold")),"the costly negate message must not ALSO fire — the free stagger wins the race in the picking loop");
  assert.equal(wrestler.pendingClashNegate,false,"pendingClashNegate must not survive to leak onto a later action");
  assert.equal(wrestler.stam,stamBefore,"the free stagger path must cost nothing — no stamina deducted at all, unlike the costly-negate case above");
  console.log("  poise-break/negate collision: free stagger wins, stale negate cleared OK");
})();
(function forcedMountEntryStaggersOnlyWhenItDealtDamage(){
  // A forced (non-voluntary) Mount transition always zeroes poise outright (enterMount), but
  // that alone never used to grant the free stagger-cancel the way an ordinary poise break
  // does. Owner correction (2026-08-25): it should, when the technique that forced the Mount
  // also dealt damage — Suplex, not the 0-power Reversal.
  AF.setRNG(()=>0);
  const wrestling=AF.MARTIAL.Wrestling.moves;
  const clinchTech=wrestling.find(a=>a.name==="Clinch")||AF.MARTIAL.Boxing.moves.find(a=>a.name==="Clinch");
  const suplex=wrestling.find(a=>a.name==="Suplex");
  const reversal=wrestling.find(a=>a.name==="Reversal");
  assert.equal(reversal.effects.find(e=>e.k==="GrappleTech").power,0,"Reversal must deal no damage — it's a pure position flip, the case this fix must NOT stagger");
  const wrestler=AF.makeFighter({name:"MountW",sign:"Taurus",stats:{STR:30,AGI:20,FORT:14,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[clinchTech,suplex]});
  const foe=AF.makeFighter({name:"MountF",sign:"Aries",stats:{STR:8,AGI:6,FORT:6,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  const mB=new AF.Battle([wrestler,foe],AF.makeArena(5));
  AF.resolveRound(mB,[{owner:wrestler,actions:[clinchTech],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  mB.round++;
  AF.resolveRound(mB,[{owner:wrestler,actions:[suplex],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert.equal(foe.poise,0,"landing Suplex must still unconditionally zero poise via the forced Mount entry");
  assert.equal(AF.relRole(foe),AF.REL.MOUNTED,"Suplex must still force Mount");
  assert(foe.pendingSkips>0,"a forced Mount entry off a technique that also dealt damage must now grant the free stagger-cancel too");
  console.log("  Suplex's forced Mount entry now staggers (Reversal's 0-power case confirmed exempt) OK");
})();
(function pullGuardNeverStaggersTheJJUser(){
  // Pull Guard also enters Mount, but voluntarily and from the bottom — it must stay on the
  // separate `voluntary:true` branch of enterMount, which never touches pendingSkips at all,
  // regardless of the new stagger:e.power>0 flag (Pull Guard deals no damage anyway, but the
  // real guarantee here is structural: the voluntary branch doesn't check `stagger` at all).
  AF.setRNG(()=>0);
  const jj=AF.MARTIAL.JiuJitsu.moves;
  const clinchTech=jj.find(a=>a.name==="Clinch");
  const pullGuard=jj.find(a=>a.name==="Pull Guard");
  assert.equal(pullGuard.effects.find(e=>e.k==="GrappleTech").power,0,"Pull Guard must deal no damage — it's a pure voluntary bottom transition");
  const jjUser=AF.makeFighter({name:"PG",sign:"Pisces",stats:{STR:10,AGI:14,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[clinchTech,pullGuard]});
  const opp=AF.makeFighter({name:"PGOpp",sign:"Aries",stats:{STR:12,AGI:8,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  const pgB=new AF.Battle([jjUser,opp],AF.makeArena(5));
  AF.resolveRound(pgB,[{owner:jjUser,actions:[clinchTech],moveTo:null},{owner:opp,actions:[],moveTo:null}]);
  pgB.round++;
  const poiseBefore=jjUser.poise;
  AF.resolveRound(pgB,[{owner:jjUser,actions:[pullGuard],moveTo:null},{owner:opp,actions:[],moveTo:null}]);
  assert.equal(AF.relRole(jjUser),AF.REL.MOUNTED,"Pull Guard must still voluntarily send the JJ user to Mounted");
  assert.equal(jjUser.poise,poiseBefore,"a voluntary Pull Guard must preserve the JJ user's poise exactly, not zero it");
  assert.equal(jjUser.pendingSkips,0,"the JJ user must never be staggered by their own voluntary Pull Guard");
  console.log("  Pull Guard never staggers the JJ user OK");
})();
(function teepKickAntiPriorityAndConditionalGuardBreak(){
  // Teep Kick's Guard Break is conditional now: it's earned by reading a Priority-tagged
  // damaging rush, not authored as a flat property of the move — and it needs the scoped
  // anti-priority bonus just to have a fair shot at acting first against one at all.
  const muay=AF.MARTIAL.MuayThai.moves,teep=muay.find(a=>a.name==="Teep Kick"),jab=muay.find(a=>a.name==="Jab-Cross");
  const machLunge=AF.KITS.Aries.tai.find(a=>a.name==="Mach Lunge");
  assert(machLunge.tags.includes("Priority")&&AF.isDamagingRush(machLunge),"Mach Lunge must be a Priority-tagged damaging rush for this test to mean anything");

  // Same AGI on both sides: without the anti-priority bonus, Mach Lunge's Priority weight (8)
  // beats Teep Kick's Normal weight (20) by ~12 in the picking key, so Teep Kick would almost
  // never act first here. With the bonus, it's a fair race — and setRNG(0) always maxes the
  // shared d10 initiative roll for both, so a fair race resolves as a tie broken by array order.
  AF.setRNG(()=>0);
  const teepUser=AF.makeFighter({name:"TeepUser",sign:"Libra",stats:{STR:10,AGI:14,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[teep]});
  const rusher=AF.makeFighter({name:"Rusher",sign:"Aries",stats:{STR:14,AGI:14,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[machLunge]});
  const rB=new AF.Battle([teepUser,rusher],AF.makeArena(5));
  AF.resolveRound(rB,[{owner:teepUser,actions:[teep],moveTo:null},{owner:rusher,actions:[machLunge],moveTo:null}]);
  const teepLine=rB.log.findIndex(x=>x.text.includes("Teep Kick"));
  const lungeLine=rB.log.findIndex(x=>x.text.includes("Mach Lunge"));
  assert(teepLine>=0&&lungeLine>=0&&teepLine<lungeLine,"the anti-priority bonus must let Teep Kick act before a same-AGI Priority rush, not after");
  assert(rB.log.some(x=>x.text.includes("reads the rush and catches it clean")),"landing on a target with a queued Priority rush must earn the conditional Guard Break");

  // Control: an ordinary, non-rush ability queued next earns no bonus and no Guard Break floor —
  // same fair race (nothing to counter), but poise damage stays at Teep Kick's own baseline (1x).
  AF.setRNG(()=>0);
  const teepUser2=AF.makeFighter({name:"TeepUser2",sign:"Libra",stats:{STR:10,AGI:14,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[teep]});
  const ordinary=AF.makeFighter({name:"Ordinary",sign:"Aries",stats:{STR:14,AGI:14,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[jab]});
  const cB=new AF.Battle([teepUser2,ordinary],AF.makeArena(5));
  AF.resolveRound(cB,[{owner:teepUser2,actions:[teep],moveTo:null},{owner:ordinary,actions:[jab],moveTo:null}]);
  assert(!cB.log.some(x=>x.text.includes("reads the rush and catches it clean")),"a Teep Kick with nothing to counter must not get the conditional Guard Break");
  const poiseLostControl=ordinary.maxPoise-ordinary.poise;

  // Same comparison against Tidal Slam: a damaging rush, but NOT Priority-tagged — already a
  // fair fight (no bonus needed), and per the owner's own framing the Guard Break is earned
  // specifically by countering a PRIORITY ability, so Tidal Slam must not grant it either.
  AF.setRNG(()=>0);
  const teepUser3=AF.makeFighter({name:"TeepUser3",sign:"Libra",stats:{STR:10,AGI:14,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[teep]});
  const tidal=AF.KITS.Cancer.tai.find(a=>a.name==="Tidal Slam");
  assert(AF.isDamagingRush(tidal)&&!tidal.tags.includes("Priority"),"Tidal Slam must be a damaging rush that is NOT Priority-tagged, the case this must stay exempt from");
  const slammer=AF.makeFighter({name:"Slammer",sign:"Cancer",stats:{STR:14,AGI:14,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[tidal]});
  const tB=new AF.Battle([teepUser3,slammer],AF.makeArena(5));
  AF.resolveRound(tB,[{owner:teepUser3,actions:[teep],moveTo:null},{owner:slammer,actions:[tidal],moveTo:null}]);
  assert(!tB.log.some(x=>x.text.includes("reads the rush and catches it clean")),"Tidal Slam is a damaging rush but not a Priority one — it must not grant the conditional Guard Break either");
  console.log("  Teep Kick: scoped anti-priority + conditional Guard Break (Priority rushes only, Tidal Slam confirmed exempt) OK");
})();
(function deniedMomentumClashRuleRemoved(){
  // The old "Counter-tagged hit lands on a queued damaging rush" Tier 1 clash rule was dead code:
  // matchClashRules only runs from inside applyDamage's Damage-effect path, and every ability
  // that carries the Counter tag (Parry, Flowing Sand Parry, Static Shell, Flow Parry, Slide
  // Counter) is a self-buff/ward with zero Damage effects, so the branch could never fire. This
  // guards that invariant rather than reviving the branch: if a future Counter ability ever
  // gains a Damage effect, this test breaks as a signal to design the clash rule back in on
  // purpose, not have it silently reactivate as an unintended side effect.
  const counterAbilities=[];
  for(const kit of Object.values(AF.MARTIAL))for(const m of kit.moves)if(m.tags.includes("Counter"))counterAbilities.push(m);
  for(const kit of Object.values(AF.WEAPONS))for(const m of kit.moves)if(m.tags.includes("Counter"))counterAbilities.push(m);
  assert(counterAbilities.length>0,"expected at least one Counter-tagged ability to exist to make this guard meaningful");
  for(const ab of counterAbilities)assert(!ab.effects.some(e=>e.k==="Damage"),`${ab.name} is Counter-tagged and now deals Damage — the removed clash rule may need to come back intentionally`);
  console.log("  Denied-momentum clash rule stays removed (no Counter ability deals damage) OK");
})();
(function ordinaryDamageDoesNotInterruptWindUp(){
  // 2026-08-25, owner call: ordinary chip damage must NOT cancel a Stance/Charge commitment —
  // only a poise-break stagger or hard CC does, and those already cancel any queued action
  // (Stance/Charge or not) through their own pre-existing, clash-independent mechanisms.
  const kenSlash=AF.WEAPONS.Kenjutsu.moves.find(a=>a.name==="Kenjutsu Slash");
  const haymaker=AF.MARTIAL.Boxing.moves.find(a=>a.name==="Haymaker");
  const calledShot=AF.WEAPONS.Kyudo.moves.find(a=>a.name==="Called Shot");
  // Ordinary hit: archer takes a plain Kenjutsu Slash first (higher AGI guarantees the attacker
  // resolves first) but their poise holds — the draw must still go off clean.
  AF.setRNG(()=>0);
  const attacker=AF.makeFighter({name:"Slasher",sign:"Aries",stats:{STR:12,AGI:16,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[kenSlash]});
  const archer=AF.makeFighter({name:"OrdinaryArcher",sign:"Sagittarius",stats:{STR:10,AGI:10,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const B=new AF.Battle([attacker,archer],AF.makeArena(5));
  AF.resolveRound(B,[{owner:attacker,actions:[kenSlash],moveTo:null},{owner:archer,actions:[calledShot],moveTo:null}]);
  assert(archer.hp<archer.maxHp,"the ordinary hit must actually land for this test to mean anything");
  assert(archer.poise>0,"the ordinary hit must not break poise, or this isn't testing the 'ordinary damage' case");
  assert(AF.isRooted(archer),"an ordinary, non-breaking hit must not cancel the archer's draw");
  assert(archer.chargingAction===calledShot,"the draw must still be held after merely being chip-damaged");
  // Stagger DOES cancel it: force a poise break (guard-break Haymaker vs near-zero poise) and
  // confirm the draw never fires — this was already true before the wind-up rule's removal, via
  // the generic staggerCancelsNextAction mechanism, not anything clash-specific.
  AF.setRNG(()=>0);
  const brawler=AF.makeFighter({name:"Brawler",sign:"Aries",stats:{STR:14,AGI:16,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[haymaker]});
  const archer2=AF.makeFighter({name:"StaggeredArcher",sign:"Sagittarius",stats:{STR:10,AGI:10,FORT:12,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  archer2.poise=1;
  const B2=new AF.Battle([brawler,archer2],AF.makeArena(5));
  AF.resolveRound(B2,[{owner:brawler,actions:[haymaker],moveTo:null},{owner:archer2,actions:[calledShot],moveTo:null}]);
  assert(B2.log.some(x=>x.text.includes("staggered — action canceled")),"the poise break must stagger-cancel the archer's queued draw");
  assert(!AF.isRooted(archer2),"a staggered draw must never actually root the archer");
  assert(!archer2.chargingAction,"a staggered draw must never actually begin charging");
  console.log("  Ordinary damage no longer interrupts a Stance/Charge wind-up; stagger and hard CC still do, for free OK");
})();
(function kyudoDoubleNockCombo(){
  // Kyudo's Jab-Cross analog: same two-strike Combo shape, just at range.
  AF.setRNG(()=>0);
  const kyudo=AF.WEAPONS.Kyudo.moves,dn=kyudo.find(a=>a.name==="Double Nock");
  assert(dn.tags.includes("Combo")&&dn.effects.length===2,"Double Nock must be a two-effect Combo ability");
  const archer=AF.makeFighter({name:"DNArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[dn]});
  const foe=AF.makeFighter({name:"DNFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(3,0),abilities:[]});
  const B=new AF.Battle([archer,foe],AF.makeArena(6));
  AF.resolveRound(B,[{owner:archer,actions:[dn],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(B.log.some(x=>x.text.includes("cross follows through automatically")),"a landed first arrow must auto-fire the second, same as Jab-Cross");
  const hits=B.log.filter(x=>x.text.includes("Double Nock →")).length;
  assert.equal(hits,2,"both nocked arrows must land as two separate strikes");
  console.log("  Double Nock resolves as a two-strike Combo, same shape as Jab-Cross OK");
})();
(function kyudoAchillesShotSlow(){
  AF.setRNG(()=>0);
  const kyudo=AF.WEAPONS.Kyudo.moves,ach=kyudo.find(a=>a.name==="Achilles Shot");
  const archer=AF.makeFighter({name:"AchArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[ach]});
  const foe=AF.makeFighter({name:"AchFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(3,0),abilities:[]});
  const B=new AF.Battle([archer,foe],AF.makeArena(6));
  AF.resolveRound(B,[{owner:archer,actions:[ach],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(AF.hasStatus(foe,"Slow"),"Achilles Shot must impose Slow on a landed hit");
  console.log("  Achilles Shot imposes Slow on landing OK");
})();
(function kyudoCalledShotDrawAndFire(){
  // Called Shot is a single ability spanning two rounds, same UX as the Ultimate "Charge" tag
  // (Meteor/Tsunami/etc.): round 1 draws and roots the archer, round 2 auto-fires with no
  // action needing to be re-queued — see resolveAction's Charge branch and resolveRound's
  // chargeBeam eruption path.
  AF.setRNG(()=>0);
  const kyudo=AF.WEAPONS.Kyudo.moves,calledShot=kyudo.find(a=>a.name==="Called Shot"),kyudoShot=kyudo.find(a=>a.name==="Kyudo Shot");
  const archer=AF.makeFighter({name:"DrawArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const foe=AF.makeFighter({name:"DrawFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(3,0),abilities:[]});
  const B=new AF.Battle([archer,foe],AF.makeArena(6));
  AF.resolveRound(B,[{owner:archer,actions:[{ability:calledShot,target:foe}],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(AF.isRooted(archer),"the archer must be rooted while their shot is drawn");
  assert(archer.chargingAction===calledShot,"the draw must still be pending after round 1");
  assert.equal(foe.hp,foe.maxHp,"drawing must not deal any damage on the round it's cast");
  AF.resolveRound(B,[{owner:archer,actions:[],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(B.log.some(x=>x.text.includes("drawn shot finds its mark")),"the held draw must announce the crit when it fires");
  assert(foe.hp<foe.maxHp,"the drawn shot must actually land");
  assert(!archer.chargingAction,"the charge must be cleared once it erupts");
  const drawnPoiseLost=foe.maxPoise-foe.poise;
  // Compare against a cold ordinary Projectile (Kyudo Shot) to confirm the drawn shot's poise
  // floor breaks strictly more guard than an un-drawn hit.
  AF.setRNG(()=>0);
  const coldArcher=AF.makeFighter({name:"ColdArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[kyudoShot]});
  const coldFoe=AF.makeFighter({name:"ColdFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(3,0),abilities:[]});
  const coldB=new AF.Battle([coldArcher,coldFoe],AF.makeArena(6));
  AF.resolveRound(coldB,[{owner:coldArcher,actions:[kyudoShot],moveTo:null},{owner:coldFoe,actions:[],moveTo:null}]);
  const coldPoiseLost=coldFoe.maxPoise-coldFoe.poise;
  assert(drawnPoiseLost>coldPoiseLost,"a drawn Called Shot's poise floor must break more guard than an ordinary shot");
  console.log("  Called Shot draws and roots on round 1, auto-fires with a guaranteed crit/poise floor on round 2 OK");
})();
(function kyudoCalledShotBeamAndPiercing(){
  // The beam: anyone standing between the archer and the aimed target also takes the arrow,
  // scaled down only if they share the archer's own faction (ordinary AoE friendly-fire rule).
  // Called Shot now spans two rounds (draw + auto-fire), so each scenario below queues the draw
  // in round 1 and lets it erupt in round 2 (empty actions, same as an Ultimate Charge).
  AF.setRNG(()=>0);
  const kyudo=AF.WEAPONS.Kyudo.moves,calledShot=kyudo.find(a=>a.name==="Called Shot"),kyudoShot=kyudo.find(a=>a.name==="Kyudo Shot");
  const archer=AF.makeFighter({name:"BeamArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const bystander=AF.makeFighter({name:"Bystander",sign:"Aries",stats:{STR:10,AGI:10,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(2,0),abilities:[]});
  const foe=AF.makeFighter({name:"BeamFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const bB=new AF.Battle([archer,bystander,foe],AF.makeArena(6));
  AF.resolveRound(bB,[{owner:archer,actions:[{ability:calledShot,target:foe}],moveTo:null},{owner:bystander,actions:[],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  AF.resolveRound(bB,[{owner:archer,actions:[],moveTo:null},{owner:bystander,actions:[],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(bystander.hp<bystander.maxHp,"a fighter standing between the archer and the aimed target must also be hit");
  assert(foe.hp<foe.maxHp,"the aimed target must still take the primary hit");
  assert(bB.log.some(x=>x.text.includes("caught in the arrow's path")),"the beam hit must be logged");
  // Piercing: Called Shot ignores destructible cover (Tree) but is still stopped by hard cover
  // (Wall) — the opposite of an ordinary Projectile like Kyudo Shot, which Tree still blocks.
  AF.setRNG(()=>0);
  const treeArcher=AF.makeFighter({name:"TreeArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const treeFoe=AF.makeFighter({name:"TreeFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const treeB=new AF.Battle([treeArcher,treeFoe],AF.makeArena(6));
  treeB.grid.set(AF.hx(2,0),"Tree");
  AF.resolveRound(treeB,[{owner:treeArcher,actions:[{ability:calledShot,target:treeFoe}],moveTo:null},{owner:treeFoe,actions:[],moveTo:null}]);
  AF.resolveRound(treeB,[{owner:treeArcher,actions:[],moveTo:null},{owner:treeFoe,actions:[],moveTo:null}]);
  assert(treeFoe.hp<treeFoe.maxHp,"Called Shot must pierce a Tree standing in its path");
  AF.setRNG(()=>0);
  const blockedArcher=AF.makeFighter({name:"BlockedArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[kyudoShot]});
  const blockedFoe=AF.makeFighter({name:"BlockedFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const blockedB=new AF.Battle([blockedArcher,blockedFoe],AF.makeArena(6));
  blockedB.grid.set(AF.hx(2,0),"Tree");
  AF.resolveRound(blockedB,[{owner:blockedArcher,actions:[kyudoShot],moveTo:null},{owner:blockedFoe,actions:[],moveTo:null}]);
  assert.equal(blockedFoe.hp,blockedFoe.maxHp,"an ordinary Kyudo Shot must still be blocked by a Tree, unlike the Piercing Called Shot");
  AF.setRNG(()=>0);
  const wallArcher=AF.makeFighter({name:"WallArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const wallFoe=AF.makeFighter({name:"WallFoe",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const wallB=new AF.Battle([wallArcher,wallFoe],AF.makeArena(6));
  wallB.grid.set(AF.hx(2,0),"Wall",0,999);
  AF.resolveRound(wallB,[{owner:wallArcher,actions:[{ability:calledShot,target:wallFoe}],moveTo:null},{owner:wallFoe,actions:[],moveTo:null}]);
  AF.resolveRound(wallB,[{owner:wallArcher,actions:[],moveTo:null},{owner:wallFoe,actions:[],moveTo:null}]);
  assert.equal(wallFoe.hp,wallFoe.maxHp,"a Wall (hard cover) must still block Called Shot even though it pierces Tree/Bush");
  console.log("  Called Shot travels as a beam and pierces destructible cover but not Wall/Rock OK");
})();
(function kyudoCalledShotFiresAtLastKnownPosition(){
  // 2026-08-25, owner call: losing the locked target between the draw and the eruption (dead,
  // out of LoS, or just walked out of perception range) must NOT cancel the shot or silently
  // retarget a different living enemy. The archer looses at the last place they actually saw
  // their mark — c.chargeTargetCell, refreshed every round the target is still tracked.
  const kyudo=AF.WEAPONS.Kyudo.moves,calledShot=kyudo.find(a=>a.name==="Called Shot");
  // Case 1: target walks out of LoS behind a Wall, and the cell they were last seen at is now
  // empty — the shot must still fire at that cell (not fizzle, not retarget) and simply find no
  // one there.
  AF.setRNG(()=>0);
  const archer=AF.makeFighter({name:"LKArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const foe=AF.makeFighter({name:"LKFoe",sign:"Aries",stats:{STR:12,AGI:14,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const B=new AF.Battle([archer,foe],AF.makeArena(8));
  AF.resolveRound(B,[{owner:archer,actions:[{ability:calledShot,target:foe}],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert.deepEqual(archer.chargeTargetCell,{q:4,r:0},"the draw must lock the target's cell at cast time");
  foe.cell=AF.hx(4,2); // foe leaves its last-known cell, so it's empty when the shot fires
  AF.resolveRound(B,[{owner:archer,actions:[],moveTo:null},{owner:foe,actions:[],moveTo:null}]);
  assert(B.log.some(x=>x.text.includes("last known position")),"losing the target must still fire the shot at its last-known cell, not silently drop it");
  assert.equal(foe.hp,foe.maxHp,"an empty last-known cell must deal no damage to the foe who actually moved away");
  console.log("  Called Shot fires at the target's last-known cell instead of fizzling when it walks out of perception OK");
  // Case 2: a fighter dies between the draw and the eruption — the shot must still resolve at
  // their last-known (death) cell, and must NEVER auto-retarget a different living enemy just
  // because one happens to still be perceived.
  AF.setRNG(()=>0);
  const archer2=AF.makeFighter({name:"DeathArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const foe2=AF.makeFighter({name:"DeathFoe",sign:"Aries",stats:{STR:12,AGI:14,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const otherEnemy=AF.makeFighter({name:"OtherEnemy",sign:"Aries",stats:{STR:12,AGI:10,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(0,4),abilities:[]});
  const B2=new AF.Battle([archer2,foe2,otherEnemy],AF.makeArena(10));
  AF.resolveRound(B2,[{owner:archer2,actions:[{ability:calledShot,target:foe2}],moveTo:null},{owner:foe2,actions:[],moveTo:null},{owner:otherEnemy,actions:[],moveTo:null}]);
  foe2.hp=0;
  AF.resolveRound(B2,[{owner:archer2,actions:[],moveTo:null},{owner:foe2,actions:[],moveTo:null},{owner:otherEnemy,actions:[],moveTo:null}]);
  assert.equal(otherEnemy.hp,otherEnemy.maxHp,"a dead target must never cause Called Shot to auto-retarget a different living enemy");
  console.log("  Called Shot never auto-retargets a different living enemy when the locked target dies first OK");
  // Case 3: someone else happens to be standing at the target's last-known cell when the shot
  // fires — the arrow flies to that point in space and hits whoever's actually there.
  AF.setRNG(()=>0);
  const archer3=AF.makeFighter({name:"BystanderArcher",sign:"Sagittarius",stats:{STR:10,AGI:12,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[calledShot]});
  const foe3=AF.makeFighter({name:"WanderFoe",sign:"Aries",stats:{STR:12,AGI:14,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(4,0),abilities:[]});
  const wanderIn=AF.makeFighter({name:"WanderIn",sign:"Aries",stats:{STR:10,AGI:10,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(8,0),abilities:[]});
  const B3=new AF.Battle([archer3,foe3,wanderIn],AF.makeArena(12));
  AF.resolveRound(B3,[{owner:archer3,actions:[{ability:calledShot,target:foe3}],moveTo:null},{owner:foe3,actions:[],moveTo:null},{owner:wanderIn,actions:[],moveTo:null}]);
  foe3.cell=AF.hx(9,0);wanderIn.cell=AF.hx(4,0);
  AF.resolveRound(B3,[{owner:archer3,actions:[],moveTo:null},{owner:foe3,actions:[],moveTo:null},{owner:wanderIn,actions:[],moveTo:null}]);
  assert.equal(foe3.hp,foe3.maxHp,"the original target who actually left the cell must take no damage");
  assert(wanderIn.hp<wanderIn.maxHp,"whoever is standing at the last-known cell when the shot fires must take the hit");
  console.log("  Called Shot hits whoever is standing at the target's last-known cell when it fires OK");
})();
(function aiResourcePacingDiscouragesSpend(){
  // 2026-08-26, owner call: the AI's only prior anti-spam mechanism was repetitionExtra's
  // stamina/chakra surcharge, which score() never weighed — a fighter with stamina to spare
  // just kept re-picking its single best move every slot, paying the surcharge without ever
  // treating it as a reason to spend differently. resourcePaceMult discounts a candidate by how
  // much of its pool the pick costs AND how depleted that pool already is, so under real
  // pressure the AI should diversify instead of feeding one move an ever-growing surcharge.
  AF.setRNG(()=>0.42); // fixed mid-range roll so evasion/hit outcomes are deterministic across runs
  const thugAbilities=AF.enemyLoadout("StreetThug");
  const thug=AF.makeFighter({name:"PacingThug",sign:"Aries",stats:{STR:14,AGI:10,FORT:8,INT:6,CHA:6},faction:1,cell:AF.hx(0,0),abilities:thugAbilities,persona:"brute"});
  const player=AF.makeFighter({name:"PacingPlayer",sign:"Leo",stats:{STR:10,AGI:10,FORT:20,INT:10,CHA:10},faction:0,cell:AF.hx(1,0),abilities:[]});
  const B=new AF.Battle([thug,player],AF.makeArena(6));
  const seen=new Set();
  for(let round=1;round<=3;round++){
    const p=AF.planFor(B,thug,1);
    for(const a of p.actions)seen.add(a.name);
    AF.resolveRound(B,[{owner:thug,actions:p.actions,moveTo:p.moveTo},{owner:player,actions:[],moveTo:null}]);
  }
  assert(seen.size>=3,`a resource-pressured fighter must diversify across several rounds instead of spamming one move — saw only [${[...seen].join(", ")}]`);
  console.log("  AI resource pacing diversifies move choice under stamina pressure instead of feeding one move's repetition surcharge OK");
})();
(function aiAvoidsRepeatedlyResistedMove(){
  // Opponent-read: an ability this SPECIFIC foe has already beaten several times this fight
  // (recordResisted, hooked into evasion/parry/grapple-denial) should get discounted enough to
  // fall out of the AI's picks, without ever being permanently banned (see aiResistanceDiscountFloor).
  AF.setRNG(()=>0);
  const kenjutsu=AF.WEAPONS.Kenjutsu.moves;
  const slash=kenjutsu.find(a=>a.name==="Kenjutsu Slash"),thrust=kenjutsu.find(a=>a.name==="Precision Thrust"),bash=kenjutsu.find(a=>a.name==="Hilt Bash");
  const attacker=AF.makeFighter({name:"ReadAttacker",sign:"Aries",stats:{STR:12,AGI:10,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[slash,thrust,bash],persona:"aggressive"});
  const foe=AF.makeFighter({name:"ReadFoe",sign:"Aries",stats:{STR:10,AGI:10,FORT:10,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[]});
  const m=new Map();m.set("Kenjutsu Slash",3);attacker.resisted.set(foe,m);
  const B=new AF.Battle([attacker,foe],AF.makeArena(6));
  const plan=AF.planFor(B,attacker,1).actions.map(a=>a.name);
  assert(!plan.includes("Kenjutsu Slash"),`an ability this foe has resisted 3 times already should fall out of the plan, got [${plan.join(", ")}]`);
  console.log("  AI discounts and drops an ability this specific foe has already repeatedly resisted OK");
})();
(function aiReadsGrappleHeavyFoePattern(){
  // Opponent-pattern-read: a foe who has been grappling heavily this fight (foeGrappleFraction)
  // should make the AI stop trading its own Grapple attempts with them and lean into Priority
  // strikes instead, which already punish a queued grapple entry via the "mid-entry" clash rule.
  AF.setRNG(()=>0);
  const clinch=AF.MARTIAL.Boxing.moves.find(a=>a.name==="Clinch");
  const jabCross=AF.MARTIAL.Boxing.moves.find(a=>a.name==="Jab-Cross");
  const muayThai=Object.values(AF.MARTIAL).find(k=>k.moves.some(m=>m.name==="Teep Kick"));
  const teep=muayThai.moves.find(a=>a.name==="Teep Kick");
  const actor=AF.makeFighter({name:"PatternReader",sign:"Aries",stats:{STR:10,AGI:10,FORT:10,INT:8,CHA:8},faction:0,cell:AF.hx(0,0),abilities:[clinch,jabCross,teep],persona:"aggressive"});
  const wrestler=AF.makeFighter({name:"GrappleHeavyFoe",sign:"Aries",stats:{STR:12,AGI:8,FORT:12,INT:8,CHA:8},faction:1,cell:AF.hx(1,0),abilities:[clinch]});
  wrestler.repeat[clinch.id]=5; // simulates a fight's worth of repeated grapple attempts
  const B=new AF.Battle([actor,wrestler],AF.makeArena(6));
  const plan=AF.planFor(B,actor,1).actions.map(a=>a.name);
  assert(!plan.includes("Clinch"),`the AI should stop trading grapples with a foe who's been grappling heavily, got [${plan.join(", ")}]`);
  assert(plan.includes("Teep Kick"),`the AI should lean into a Priority strike against a grapple-heavy foe, got [${plan.join(", ")}]`);
  console.log("  AI reads a grapple-heavy foe's pattern and favors Priority strikes over trading its own grapple attempts OK");
})();

console.log(JSON.stringify({ok:true,positionalCombat:{relationshipStates:AF.REL_ROLES,mountAccess:Object.values(AF.MOUNT_ACCESS),auditedAbilities:Object.values(AF.POSITIONAL_RULES).reduce((n,g)=>n+Object.keys(g).length,0),mountUpkeep:AF.BAL.mountUpkeepStamina,submissionUpkeep:AF.BAL.submissionUpkeepStamina,submissionSlotReserve:AF.BAL.submissionSlotReserve,focusRestorePercent:AF.BAL.focusRestorePercent},canonicalStatBase:AFUI.STAT_BASE_VALUE,level1Budget:AFUI.statBudget(1),level20Budget:AFUI.statBudget(20),level100Budget:AFUI.statBudget(100),level1Build:AFUI.evenStatBuild(1),level20Build:AFUI.evenStatBuild(20),maxOneStatCost:AFUI.statValueCost(100),canonicalPlayerStatsReachCombat:true,npcStatsUnaffected:true,loweringLevelTrimsOverspend:true,escalatingCostChecks:true,progressionSlice1:true,palmBaseline:"25c/15hp",maxHealRatio:"1:1",abilityLevelCap:AF.BAL.abilityLevelCap},null,2));
