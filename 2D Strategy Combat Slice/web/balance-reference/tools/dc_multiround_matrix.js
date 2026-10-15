"use strict";

/*
  Astro Fighters balance harness — elimination-only multi-round ecosystem pass.

  OWNER RULE (2026-08-13): battles do NOT end because a round limit is reached.
  A battle ends only when one faction has no living combatants. A simultaneous
  double KO is reported separately. If combat enters an exact repeated state for
  many consecutive rounds, the harness throws NON_TERMINATING_BATTLE; that is a
  test/engine failure, never a draw outcome.

  This file lives under balance-reference/tools and mutates cloned abilities only.
  Live catalog values remain intact.
*/
const fs=require("fs");
const path=require("path");
global.window=global;
require("../../af-core.js");
require("../../af-dc-model-v3.js");
require("../../af-ui-v3.js");
const {AF,AFDC:DC,AFUI}=global;

const OUT=path.resolve(__dirname,"..");
const MODES=["legacy","candidate"];
const BANDS=[
  {characterLevel:10,abilityLevel:0,label:"L10/A0"},
  {characterLevel:20,abilityLevel:5,label:"L20/A5"},
  {characterLevel:45,abilityLevel:10,label:"L45/A10"},
  {characterLevel:90,abilityLevel:10,label:"L90/A10"},
];
const PROFILE_SHARES={
  Balanced:{STR:.20,AGI:.20,FORT:.20,INT:.20,CHA:.20},
  PhysicalOffense:{STR:.30,AGI:.27,FORT:.18,INT:.10,CHA:.15},
  ControlOffense:{STR:.10,AGI:.18,FORT:.15,INT:.32,CHA:.25},
  PhysicalDefense:{STR:.20,AGI:.25,FORT:.30,INT:.10,CHA:.15},
  MentalDefense:{STR:.10,AGI:.15,FORT:.25,INT:.25,CHA:.25},
};
const PROFILE_NAMES=Object.keys(PROFILE_SHARES);
const SEEDS=Math.max(1,Number(process.env.AF_BALANCE_SEEDS)||2);
const DIFFICULTY_NOISE=0;
const NEUTRAL_SIGN="Libra";
const REPEATED_STATE_FAILURE=100;

const clone=x=>JSON.parse(JSON.stringify(x));
const avg=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:0;
const quantile=(a,q)=>{if(!a.length)return 0;const z=[...a].sort((x,y)=>x-y);return z[Math.floor((z.length-1)*q)];};

function exactLegalProfile(level,shares){
  const budget=AFUI.statBudget(level),names=AFUI.STAT_NAMES;
  let dp=new Map([[0,{score:0,vals:[]}]]);
  for(const name of names){
    const target=shares[name]*budget,next=new Map();
    const options=[];
    for(let v=AFUI.STAT_BASE_VALUE;v<=AFUI.STAT_MAX_VALUE;v++){
      const cost=AFUI.statValueCost(v);if(cost>budget)break;
      options.push({v,cost,pen:(cost-target)*(cost-target)});
    }
    for(const [spent,state] of dp)for(const o of options){
      const ns=spent+o.cost;if(ns>budget)continue;
      const score=state.score+o.pen,old=next.get(ns);
      if(!old||score<old.score)next.set(ns,{score,vals:[...state.vals,o.v]});
    }
    dp=next;
  }
  const best=dp.get(budget);if(!best)throw new Error(`No exact stat allocation for level ${level}`);
  const stats=Object.fromEntries(names.map((n,i)=>[n,best.vals[i]]));
  const state=AFUI.statBudgetState(level,stats);
  if(!state.valid||state.spent!==state.budget)throw new Error(`Illegal profile L${level}: ${JSON.stringify(state)}`);
  return stats;
}

const PROFILE_STATS={};
for(const band of BANDS){
  PROFILE_STATS[band.label]={};
  for(const [name,shares] of Object.entries(PROFILE_SHARES))PROFILE_STATS[band.label][name]=exactLegalProfile(band.characterLevel,shares);
}

function kitDefs(){
  const out=[{family:"Universal",name:"Universal Arts",key:"Universal",base:()=>AF.generalArts()}];
  for(const sign of AF.SIGNS)out.push({family:"Sign",name:`${sign} Sign`,key:`Sign:${sign}`,base:()=>[...AF.zodiacAbilities(sign),...AF.generalArts()]});
  for(const [key,style] of Object.entries(AF.MARTIAL))out.push({family:"Martial",name:key,key:`Martial:${key}`,base:()=>[style.stance,...style.moves,...AF.generalArts()]});
  for(const [key,kit] of Object.entries(AF.WEAPONS))out.push({family:"Weapon",name:key,key:`Weapon:${key}`,base:()=>[kit.stance,...kit.moves,...AF.generalArts()]});
  return out;
}
const KITS=kitDefs();
const TEMPLATE_CACHE=new Map();

function scaledAbility(base,abilityLevel,mode){
  const original=clone(base),ab=clone(base);
  if(abilityLevel>0)AFUI.scaleAbility(ab,abilityLevel);
  ab.abilityLevel=abilityLevel;
  if(mode!=="candidate")return ab;
  const tier=DC.primaryTier(original);if(!tier)return ab;
  ab.slots=Math.max(ab.slots||1,DC.candidateSlots(original,tier)||1);
  const dual=(original.stam||0)>0&&(original.chakra||0)>0;
  if(!dual){
    const res=DC.candidateResource(original,tier);
    if(res&&res.channel){
      const growth=1+(AF.BAL.abilityCostGrowth||0)*abilityLevel;
      ab[res.channel]=Math.max(ab[res.channel]||0,Math.round(res.suggestedAuthored*growth));
    }
  }
  return ab;
}
function buildKitAbilities(def,abilityLevel,mode){
  const key=`${def.key}|${abilityLevel}|${mode}`;
  if(TEMPLATE_CACHE.has(key))return clone(TEMPLATE_CACHE.get(key));
  const seen=new Set(),out=[];
  for(const a of def.base()){
    const k=`${a.group}|${a.name}`;if(seen.has(k))continue;seen.add(k);
    out.push(scaledAbility(a,abilityLevel,mode));
  }
  TEMPLATE_CACHE.set(key,out);
  return clone(out);
}
function stanceOf(def,abilities){
  if(def.family==="Martial")return abilities.find(a=>a.tags?.includes("MartialStance"));
  if(def.family==="Weapon")return abilities.find(a=>a.tags?.includes("WeaponStance"));
  return null;
}
function actionCost(ab,priorUses){
  let stam=Math.round((ab.stam||0)*AF.costMult(ab)),chakra=Math.round((ab.chakra||0)*AF.costMult(ab));
  if(priorUses>=AF.BAL.repetitionFreeUses){
    const over=priorUses-AF.BAL.repetitionFreeUses+1;
    stam+=Math.round((ab.stam||0)*AF.BAL.repetitionStrainPerExtra*over);
    chakra+=Math.round((ab.chakra||0)*AF.BAL.repetitionStrainPerExtra*over);
  }
  return{stam,chakra,supply:ab.supply||0,slots:ab.slots||1};
}
function selfRestore(ab,f){
  let stam=0,chakra=0;
  if(ab.targeting==="Self")for(const e of ab.effects||[]){
    if(e.k!=="Res")continue;
    if(e.res==="Stamina")stam+=Math.max(0,(e.amt||0)+(e.pct?Math.round(f.maxStam*e.pct):0));
    if(e.res==="Chakra")chakra+=Math.max(0,(e.amt||0)+(e.pct?Math.round(AF.effMaxChakra(f)*e.pct):0));
  }
  return{stam,chakra};
}
function legalizePlan(plan,f,def,stance){
  const active=def.family==="Martial"?f.activeMartial:def.family==="Weapon"?f.activeWeapon:true;
  const rows=(!active&&stance)?[stance,...plan.actions.filter(a=>a!==stance)]:[...plan.actions];
  const actions=[],uses=new Map();let slots=0,stam=f.stam,chakra=f.chakra,supply=f.supplies;
  for(const ab of rows){
    const n=uses.get(ab.id)||0,c=actionCost(ab,n);
    if(slots+c.slots>5||stam<c.stam||chakra<c.chakra||supply<c.supply)continue;
    actions.push(ab);uses.set(ab.id,n+1);slots+=c.slots;stam-=c.stam;chakra-=c.chakra;supply-=c.supply;
    const r=selfRestore(ab,f);stam=Math.min(f.maxStam,stam+r.stam);chakra=Math.min(AF.effMaxChakra(f),chakra+r.chakra);
  }
  return{...plan,actions};
}
function makeCombatant(def,stats,abilityLevel,mode,faction,cell){
  const abilities=buildKitAbilities(def,abilityLevel,mode),stance=stanceOf(def,abilities);
  const fighter=AF.makeFighter({name:`${def.name} ${faction?"B":"A"}`,sign:NEUTRAL_SIGN,stats:{...stats},faction,cell,abilities,persona:"balanced"});
  return{fighter,stance};
}
function stateSignature(a,b){
  const one=f=>JSON.stringify({
    hp:f.hp,stam:f.stam,chakra:f.chakra,poise:f.poise,cell:[f.cell.q,f.cell.r],pendingSkips:f.pendingSkips||0,
    activeMartial:f.activeMartial?.name||null,activeWeapon:f.activeWeapon?.name||null,wardNext:f.wardNext||0,
    statuses:(f.statuses||[]).map(s=>[s.kind,s.rounds,s.stacks,s.tick,s.breakDC,s.freeDenials]).sort(),
    grappleTarget:f.grappleTarget?.name||null,grappledBy:f.grappledBy?.name||null,
  });
  return`${one(a)}|${one(b)}`;
}

function battleMetrics(defA,defB,profileA,profileB,band,mode,seed){
  AF.resetIds();AF.setSeed(seed);AF.BAL.useCandidateDcModel=mode==="candidate";
  const a=makeCombatant(defA,PROFILE_STATS[band.label][profileA],band.abilityLevel,mode,0,AF.hx(-2,0));
  const b=makeCombatant(defB,PROFILE_STATS[band.label][profileB],band.abilityLevel,mode,1,AF.hx(2,0));
  const B=new AF.Battle([a.fighter,b.fighter],AF.makeArena(5));
  let round=0,lastState=null,repeated=0;
  while(!B.decided()){
    round++;B.round=round;
    let pa=AF.planFor(B,a.fighter,DIFFICULTY_NOISE),pb=AF.planFor(B,b.fighter,DIFFICULTY_NOISE);
    pa=legalizePlan(pa,a.fighter,defA,a.stance);pb=legalizePlan(pb,b.fighter,defB,b.stance);
    AF.resolveRound(B,[pa,pb]);
    if(!B.decided()){
      const state=stateSignature(a.fighter,b.fighter);
      if(state===lastState)repeated++;else{lastState=state;repeated=0;}
      if(repeated>=REPEATED_STATE_FAILURE){
        throw new Error(`NON_TERMINATING_BATTLE ${defA.key}(${profileA}) vs ${defB.key}(${profileB}) ${band.label} ${mode} seed=${seed}; exact state repeated ${REPEATED_STATE_FAILURE} rounds at round ${round}`);
      }
    }
  }
  const aliveA=AF.alive(a.fighter),aliveB=AF.alive(b.fighter);
  const winner=aliveA&&!aliveB?"A":aliveB&&!aliveA?"B":!aliveA&&!aliveB?"doubleKO":null;
  if(!winner)throw new Error(`INVALID_ELIMINATION_STATE ${defA.key} vs ${defB.key} round ${round}`);
  const logs=B.log||[];
  return{
    winner,rounds:round,
    landed:logs.filter(x=>String(x.text||"").includes(" is gripped by ")).length,
    resisted:logs.filter(x=>String(x.text||"").includes(" resists ")).length,
    denied:logs.filter(x=>/action is lost|staggered — action canceled|fast asleep/.test(String(x.text||""))).length,
    fizzles:logs.filter(x=>String(x.text||"").includes("fizzles (not enough resources)")).length,
  };
}
function aggregate(meta,battles){
  const n=battles.length,rounds=battles.map(x=>x.rounds);
  const winsA=battles.filter(x=>x.winner==="A").length,winsB=battles.filter(x=>x.winner==="B").length,doubleKOs=battles.filter(x=>x.winner==="doubleKO").length;
  return{...meta,n,winsA,winsB,doubleKOs,winRateA:winsA/n,winRateB:winsB/n,doubleKORate:doubleKOs/n,
    avgRounds:avg(rounds),medianRounds:quantile(rounds,.5),p90Rounds:quantile(rounds,.9),p95Rounds:quantile(rounds,.95),maxRounds:Math.max(...rounds),
    avgLanded:avg(battles.map(x=>x.landed)),avgResisted:avg(battles.map(x=>x.resisted)),avgDenied:avg(battles.map(x=>x.denied)),avgFizzles:avg(battles.map(x=>x.fizzles))};
}

const rows=[];let battleCount=0;
for(const mode of MODES)for(const band of BANDS)for(const profile of PROFILE_NAMES){
  for(let i=0;i<KITS.length;i++)for(let j=i+1;j<KITS.length;j++){
    const battles=[];
    for(let s=0;s<SEEDS;s++){
      const flip=s%2===1;
      if(!flip)battles.push(battleMetrics(KITS[i],KITS[j],profile,profile,band,mode,100000+band.characterLevel*1000+i*101+j*17+s));
      else{
        const r=battleMetrics(KITS[j],KITS[i],profile,profile,band,mode,100000+band.characterLevel*1000+i*101+j*17+s);
        battles.push({...r,winner:r.winner==="A"?"B":r.winner==="B"?"A":"doubleKO"});
      }
      battleCount++;
    }
    rows.push(aggregate({mode,band:band.label,profile,kitA:KITS[i].key,kitB:KITS[j].key},battles));
  }
}
AF.BAL.useCandidateDcModel=false;
const result={
  rule:"Elimination only. No round cap. Simultaneous double KO is separate. Repeated exact state is a failing non-termination bug, never a draw.",
  seeds:SEEDS,kits:KITS.length,battles:battleCount,profiles:PROFILE_STATS,rows,
};
fs.writeFileSync(path.join(OUT,"DC_MULTIROUND_ELIMINATION_RESULTS.json"),JSON.stringify(result,null,2));
console.log(JSON.stringify({ok:true,kits:KITS.length,battles:battleCount,rule:result.rule},null,2));
