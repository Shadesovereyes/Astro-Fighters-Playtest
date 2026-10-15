"use strict";

const fs=require("fs");
const path=require("path");
global.window=global;
require("../af-core.js");
require("../af-dc-model-v3.js");
require("../af-core-v3-patch.js");
require("../af-ui-v3.js");

const {AF,AFDC,AFUI}=global;
if(!AF||!AFDC||!AFUI)throw new Error("AF / AFDC / AFUI failed to load");

const OUT=__dirname;
const MAX_ROUNDS=24;
const SEEDS=[5101,9209,16381];
const NOISE=0.12;
const LEVEL=20;
const STAT_NAMES=["STR","AGI","FORT","INT","CHA"];
const HARD=new Set(["Prone","Stun","Fear","Sleep"]);

function deepClone(v){return JSON.parse(JSON.stringify(v));}
function statusEffects(ab){return (ab.effects||[]).filter(e=>AFDC.statusTier(e));}
function isStatusAbility(ab){return statusEffects(ab).length>0;}
function isHardAbility(ab){return statusEffects(ab).some(e=>HARD.has(e.status));}

function familyDefs(){
  const rows=[];
  for(const sign of AF.SIGNS)rows.push({key:`Sign:${sign}`,label:sign,type:"Sign",value:sign});
  rows.push({key:"Universal",label:"Universal",type:"Universal",value:null});
  for(const style of Object.keys(AF.MARTIAL))rows.push({key:`Martial:${style}`,label:style,type:"Martial",value:style});
  for(const weapon of Object.keys(AF.WEAPONS))rows.push({key:`Weapon:${weapon}`,label:weapon,type:"Weapon",value:weapon});
  return rows;
}
const FAMILIES=familyDefs();

function baseLoadout(f){
  if(f.type==="Sign")return AF.buildLoadout({signs:[f.value],martials:[],weapon:null});
  if(f.type==="Martial")return AF.buildLoadout({signs:[],martials:[f.value],weapon:null});
  if(f.type==="Weapon")return AF.buildLoadout({signs:[],martials:[],weapon:f.value});
  return AF.buildLoadout({signs:[],martials:[],weapon:null});
}

function candidateLoadout(f){
  const abilities=deepClone(baseLoadout(f));
  for(const ab of abilities){
    const tier=AFDC.primaryTier(ab);if(!tier)continue;
    ab.slots=Math.max(Number(ab.slots)||1,AFDC.candidateSlots(ab,tier));
    const r=AFDC.candidateResource(ab,tier);
    if(r?.channel&&Number.isFinite(r.suggestedAuthored))ab[r.channel]=Math.max(Number(ab[r.channel])||0,r.suggestedAuthored);
  }
  return abilities;
}

function validBuildFromWeights(weights){
  const stats=Object.fromEntries(STAT_NAMES.map(s=>[s,AFUI.STAT_BASE_VALUE||6]));
  let remaining=AFUI.statBudget(LEVEL);
  const w=Object.fromEntries(STAT_NAMES.map(s=>[s,Math.max(0.1,Number(weights[s])||0.1)]));
  // Diminishing-return weighted allocator. Escalating marginal costs are respected.
  while(remaining>0){
    let pick=null,best=-Infinity;
    for(const s of STAT_NAMES){
      const cost=AFUI.marginalStatCost(stats[s]);if(cost>remaining)continue;
      const score=w[s]/(1+0.075*(stats[s]-(AFUI.STAT_BASE_VALUE||6)))/cost;
      if(score>best){best=score;pick=s;}
    }
    if(!pick)break;
    remaining-=AFUI.marginalStatCost(stats[pick]);stats[pick]++;
  }
  return stats;
}

function offenseWeights(f,abilities){
  const w={STR:1,AGI:2,FORT:1,INT:1,CHA:1.5};
  let stam=0,chakra=0,physical=0,mental=0;
  for(const ab of abilities){
    if((ab.stam||0)>0)stam++;if((ab.chakra||0)>0)chakra++;
    if(["Physical","True"].includes(ab.dmg))physical++;
    if(["Mental","Elemental"].includes(ab.dmg))mental++;
    for(const e of statusEffects(ab)){const s=AFDC.controlStat(ab,e);if(s)w[s]=(w[s]||0)+3;}
  }
  if(physical)w.STR+=3;if(mental||chakra)w.CHA+=2;
  if(f.type==="Sign"){w.INT+=3;w.CHA+=3;}
  if(f.type==="Martial"||f.type==="Weapon"){w.STR+=3;w.AGI+=3;}
  if(f.type==="Universal"){w.AGI+=2;w.INT+=2;}
  if(stam>chakra)w.FORT+=1.5;else if(chakra>stam)w.CHA+=1.5;
  return w;
}

function defenseWeightsAgainst(enemyAbilities){
  const w={STR:2.0,AGI:2.0,FORT:2.5,INT:1.5,CHA:1.5};
  for(const ab of enemyAbilities)for(const e of statusEffects(ab)){const s=AFDC.saveStat(e);if(s)w[s]=(w[s]||0)+3;}
  // General survivability: STR mitigates physical; AGI/CHA improve evasion; FORT adds HP/poise.
  w.STR+=1.5;w.AGI+=1.5;w.CHA+=0.75;w.FORT+=2;
  return w;
}

function buildFor(role,f,ownAbilities,enemyAbilities){
  if(role==="balanced")return AFUI.evenStatBuild(LEVEL);
  if(role==="offense")return validBuildFromWeights(offenseWeights(f,ownAbilities));
  if(role==="defense")return validBuildFromWeights(defenseWeightsAgainst(enemyAbilities));
  throw new Error(`unknown role ${role}`);
}

function makeCombatant(name,f,abilities,stats,faction,cell){
  return AF.makeFighter({name,sign:f.type==="Sign"?f.value:"Aries",stats,faction,cell,abilities,isPlayer:false});
}

function statusNameFromLog(text){
  for(const s of Object.keys(AFDC.STATUS_TIERS))if(text.includes(`gripped by ${s}`)||text.includes(`takes on ${s}`))return s;
  return null;
}
function resistedNameFromLog(text){
  for(const s of Object.keys(AFDC.STATUS_TIERS))if(text.includes(`resists ${s}`))return s;
  return null;
}

function runBattle({fa,fb,mode,roleA,roleB,seed}){
  AF.resetIds();AF.setSeed(seed);AF.BAL.useCandidateDcModel=(mode==="candidate");
  const rawA=baseLoadout(fa),rawB=baseLoadout(fb);
  const absA=mode==="candidate"?candidateLoadout(fa):deepClone(rawA);
  const absB=mode==="candidate"?candidateLoadout(fb):deepClone(rawB);
  const statsA=buildFor(roleA,fa,absA,absB),statsB=buildFor(roleB,fb,absB,absA);
  const a=makeCombatant(`A ${fa.label}`,fa,absA,statsA,0,AF.hx(-3,0));
  const b=makeCombatant(`B ${fb.label}`,fb,absB,statsB,1,AF.hx(3,0));
  const B=new AF.Battle([a,b],AF.makeArena(5));
  let rounds=0,actions=0,slots=0,statusActions=0,hardActions=0,lands=0,hardLands=0,resists=0;
  const selected={};
  while(!B.decided()&&rounds<MAX_ROUNDS){
    const startLog=B.log.length;
    const plans=[];
    for(const fighter of [...B.all]){
      if(!AF.alive(fighter))continue;
      const p=AF.planFor(B,fighter,NOISE);p.owner=fighter;plans.push(p);
      if(fighter===a||fighter===b){
        for(const ab of p.actions||[]){
          actions++;slots+=Number(ab.slots)||1;selected[ab.name]=(selected[ab.name]||0)+1;
          if(isStatusAbility(ab))statusActions++;
          if(isHardAbility(ab))hardActions++;
        }
      }
    }
    AF.resolveRound(B,plans);
    for(const entry of B.log.slice(startLog)){
      const text=String(entry.text||"");
      const landed=statusNameFromLog(text);if(landed){lands++;if(HARD.has(landed))hardLands++;}
      if(resistedNameFromLog(text))resists++;
    }
    rounds++;B.round+=1;
  }
  const alive0=B.all.some(x=>AF.alive(x)&&x.faction===0),alive1=B.all.some(x=>AF.alive(x)&&x.faction===1);
  const winner=alive0&&!alive1?"A":alive1&&!alive0?"B":"tie";
  const resPct=x=>({stam:x.maxStam?x.stam/x.maxStam:0,chakra:AF.effMaxChakra(x)?x.chakra/AF.effMaxChakra(x):0});
  const ra=resPct(a),rb=resPct(b);
  return{
    familyA:fa.key,familyB:fb.key,mode,roleA,roleB,seed,winner,rounds,decided:B.decided(),
    actions,slots,statusActions,hardActions,statusLands:lands,hardLands,statusResists:resists,
    endStamPct:(ra.stam+rb.stam)/2,endChakraPct:(ra.chakra+rb.chakra)/2,
    hpA:a.hp,hpB:b.hp,statsA,statsB,selected,
  };
}

const SCENARIOS=[
  {key:"balanced",pairs:[["balanced","balanced"]]},
  {key:"offense",pairs:[["offense","offense"]]},
  {key:"defense",pairs:[["defense","defense"]]},
  {key:"offense_vs_defense",pairs:[["offense","defense"],["defense","offense"]]},
];

const battles=[];
let caseIndex=0;
for(let i=0;i<FAMILIES.length;i++)for(let j=i;j<FAMILIES.length;j++){
  const fa=FAMILIES[i],fb=FAMILIES[j];
  for(const sc of SCENARIOS)for(const [roleA,roleB] of sc.pairs)for(let si=0;si<SEEDS.length;si++){
    const shared=SEEDS[si]+caseIndex*97;
    for(const mode of ["legacy","candidate"])battles.push(runBattle({fa,fb,mode,roleA,roleB,seed:shared}));
  }
  caseIndex++;
}
AF.BAL.useCandidateDcModel=false;

function mean(xs){return xs.length?xs.reduce((a,b)=>a+b,0)/xs.length:0;}
function pct(x){return (100*x).toFixed(1)+"%";}
function modeScenarioSummary(mode,scenario){
  const rows=battles.filter(b=>b.mode===mode&&(scenario==="all"||scenarioFor(b)===scenario));
  return{
    mode,scenario,battles:rows.length,decidedPct:mean(rows.map(r=>r.decided?1:0)),avgRounds:mean(rows.map(r=>r.rounds)),
    actionsPerFighterRound:rows.reduce((s,r)=>s+r.actions,0)/Math.max(1,rows.reduce((s,r)=>s+2*r.rounds,0)),
    slotsPerFighterRound:rows.reduce((s,r)=>s+r.slots,0)/Math.max(1,rows.reduce((s,r)=>s+2*r.rounds,0)),
    statusActionShare:rows.reduce((s,r)=>s+r.statusActions,0)/Math.max(1,rows.reduce((s,r)=>s+r.actions,0)),
    hardActionShare:rows.reduce((s,r)=>s+r.hardActions,0)/Math.max(1,rows.reduce((s,r)=>s+r.actions,0)),
    statusLandsPerBattle:mean(rows.map(r=>r.statusLands)),hardLandsPerBattle:mean(rows.map(r=>r.hardLands)),
    resistsPerBattle:mean(rows.map(r=>r.statusResists)),endStamPct:mean(rows.map(r=>r.endStamPct)),endChakraPct:mean(rows.map(r=>r.endChakraPct)),
  };
}
function scenarioFor(b){
  if(b.roleA==="balanced"&&b.roleB==="balanced")return"balanced";
  if(b.roleA==="offense"&&b.roleB==="offense")return"offense";
  if(b.roleA==="defense"&&b.roleB==="defense")return"defense";
  return"offense_vs_defense";
}

const summaries=[];
for(const mode of ["legacy","candidate"])for(const sc of ["all",...SCENARIOS.map(x=>x.key)])summaries.push(modeScenarioSummary(mode,sc));

function familyRows(mode){
  return FAMILIES.map(f=>{
    const rows=battles.filter(b=>b.mode===mode&&(b.familyA===f.key||b.familyB===f.key));
    let score=0,games=0,wins=0,losses=0,ties=0;
    for(const b of rows){const side=b.familyA===f.key?"A":"B";games++;
      if(b.winner==="tie"){score+=.5;ties++;}else if(b.winner===side){score++;wins++;}else losses++;
    }
    return{mode,family:f.key,label:f.label,type:f.type,games,wins,losses,ties,scorePct:score/games,avgRounds:mean(rows.map(r=>r.rounds)),statusLandsPerGame:mean(rows.map(r=>r.statusLands)),hardLandsPerGame:mean(rows.map(r=>r.hardLands))};
  });
}
const familyMetrics=[...familyRows("legacy"),...familyRows("candidate")];

function pairKey(b){return [b.familyA,b.familyB].sort().join(" vs ")+` | ${scenarioFor(b)}`;}
const pairMap=new Map();
for(const b of battles){const k=pairKey(b);if(!pairMap.has(k))pairMap.set(k,{legacy:[],candidate:[]});pairMap.get(k)[b.mode].push(b);}
const shifts=[];
for(const [key,m] of pairMap){
  if(!m.legacy.length||!m.candidate.length)continue;
  const canonical=key.split(" vs ")[0];
  const score=(rows)=>mean(rows.map(b=>{const side=b.familyA===canonical?"A":"B";return b.winner==="tie"?.5:b.winner===side?1:0;}));
  const ls=score(m.legacy),cs=score(m.candidate);
  shifts.push({pair:key,legacyScore:ls,candidateScore:cs,scoreDelta:cs-ls,legacyRounds:mean(m.legacy.map(x=>x.rounds)),candidateRounds:mean(m.candidate.map(x=>x.rounds)),roundDelta:mean(m.candidate.map(x=>x.rounds))-mean(m.legacy.map(x=>x.rounds))});
}
shifts.sort((a,b)=>Math.abs(b.scoreDelta)-Math.abs(a.scoreDelta));

const audit=[];
for(const f of FAMILIES){
  const raw=baseLoadout(f),cand=candidateLoadout(f);let slotChanged=0,resChanged=0;
  for(let i=0;i<raw.length;i++){
    const a=raw[i],c=cand[i];if((c.slots||1)>(a.slots||1))slotChanged++;
    if((c.stam||0)>(a.stam||0)||(c.chakra||0)>(a.chakra||0))resChanged++;
  }
  audit.push({family:f.key,abilities:raw.length,slotChanged,resChanged});
}

const summary={
  date:"2026-08-13",level:LEVEL,maxRounds:MAX_ROUNDS,seeds:SEEDS,noise:NOISE,
  families:FAMILIES.map(f=>f.key),familyCount:FAMILIES.length,
  pairCount:FAMILIES.length*(FAMILIES.length+1)/2,battles:battles.length,
  modes:["legacy","candidate"],scenarios:SCENARIOS.map(x=>x.key),
  candidateRules:{dcFlag:true,slotsAndResources:"AFDC candidate floors on cloned test loadouts only",liveDefaultsChanged:false},
  summaries,audit,topPairShifts:shifts.slice(0,20),
};

function csvEscape(v){const s=typeof v==="object"?JSON.stringify(v):String(v??"");return /[",\n]/.test(s)?`"${s.replaceAll('"','""')}"`:s;}
function writeCsv(file,rows,cols){fs.writeFileSync(path.join(OUT,file),[cols.join(","),...rows.map(r=>cols.map(c=>csvEscape(r[c])).join(","))].join("\n")+"\n");}

writeCsv("dc_multiround_pass_05_family.csv",familyMetrics,["mode","family","label","type","games","wins","losses","ties","scorePct","avgRounds","statusLandsPerGame","hardLandsPerGame"]);
writeCsv("dc_multiround_pass_05_matchup_shifts.csv",shifts,["pair","legacyScore","candidateScore","scoreDelta","legacyRounds","candidateRounds","roundDelta"]);
writeCsv("dc_multiround_pass_05_battles.csv",battles.map(({selected,statsA,statsB,...x})=>x),["familyA","familyB","mode","roleA","roleB","seed","winner","rounds","decided","actions","slots","statusActions","hardActions","statusLands","hardLands","statusResists","endStamPct","endChakraPct","hpA","hpB"]);
fs.writeFileSync(path.join(OUT,"dc_multiround_pass_05_summary.json"),JSON.stringify(summary,null,2)+"\n");

const allL=summaries.find(x=>x.mode==="legacy"&&x.scenario==="all"),allC=summaries.find(x=>x.mode==="candidate"&&x.scenario==="all");
const candFamilies=familyMetrics.filter(x=>x.mode==="candidate").sort((a,b)=>b.scorePct-a.scorePct);
const legacyFamilies=familyMetrics.filter(x=>x.mode==="legacy").sort((a,b)=>b.scorePct-a.scorePct);
function fmtSummary(s){return `| ${s.mode} | ${s.battles} | ${s.avgRounds.toFixed(2)} | ${pct(s.decidedPct)} | ${s.actionsPerFighterRound.toFixed(2)} | ${s.slotsPerFighterRound.toFixed(2)} | ${pct(s.statusActionShare)} | ${s.statusLandsPerBattle.toFixed(2)} | ${s.hardLandsPerBattle.toFixed(2)} | ${pct(s.endStamPct)} | ${pct(s.endChakraPct)} |`;}
function topTable(rows){return rows.slice(0,6).map(r=>`| ${r.family} | ${pct(r.scorePct)} | ${r.avgRounds.toFixed(2)} | ${r.hardLandsPerGame.toFixed(2)} |`).join("\n");}
function bottomTable(rows){return [...rows].sort((a,b)=>a.scorePct-b.scorePct).slice(0,6).map(r=>`| ${r.family} | ${pct(r.scorePct)} | ${r.avgRounds.toFixed(2)} | ${r.hardLandsPerGame.toFixed(2)} |`).join("\n");}
const md=`# Astro Fighters — Multi-round DC / Slot / Resource Pass 05\n\n_Date: 2026-08-13._\n\nThis is the first paired **multi-round kit-vs-kit** pass using the real AI planner and real combat resolver. Candidate mode enables the candidate tier-DC resolver and applies candidate slot/resource floors to **cloned test loadouts only**. Live authored ability costs/slots and the default DC flag remain unchanged.\n\n## Coverage\n\n- Families: **${FAMILIES.length}** (12 Sign, Universal-only, 6 Martial, 3 Weapon).\n- Universal arts are present in every normal kit loadout, matching actual player access.\n- Unordered family pairs including mirrors: **${summary.pairCount}**.\n- Scenarios: balanced/balanced, offense/offense, defense/defense, plus both orientations of offense-vs-defense.\n- Seeds per scenario/orientation: **${SEEDS.length}**.\n- Legacy + candidate battles resolved: **${battles.length}**.\n- Level: **${LEVEL}**; open radius-5 arena; maximum **${MAX_ROUNDS}** rounds; planner noise ${NOISE}.\n\n## Overall comparison\n\n| Mode | Battles | Avg rounds | Decided | Actions / fighter-round | Slots / fighter-round | Status-action share | Status lands / battle | Hard-CC lands / battle | End Stamina | End Chakra |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n${fmtSummary(allL)}\n${fmtSummary(allC)}\n\nCandidate-minus-legacy deltas: **${(allC.avgRounds-allL.avgRounds).toFixed(2)} rounds**, **${(allC.actionsPerFighterRound-allL.actionsPerFighterRound).toFixed(2)} actions/fighter-round**, **${(allC.hardLandsPerBattle-allL.hardLandsPerBattle).toFixed(2)} hard-control lands/battle**.\n\n## Candidate family results — highest aggregate scores\n\n| Family | Score | Avg rounds | Hard lands/game |\n|---|---:|---:|---:|\n${topTable(candFamilies)}\n\n## Candidate family results — lowest aggregate scores\n\n| Family | Score | Avg rounds | Hard lands/game |\n|---|---:|---:|---:|\n${bottomTable(candFamilies)}\n\n## Legacy family results — highest aggregate scores\n\n| Family | Score | Avg rounds | Hard lands/game |\n|---|---:|---:|---:|\n${topTable(legacyFamilies)}\n\n## Largest paired candidate-vs-legacy matchup swings\n\n| Pair / scenario | Legacy score | Candidate score | Delta | Round delta |\n|---|---:|---:|---:|---:|\n${shifts.slice(0,12).map(r=>`| ${r.pair} | ${pct(r.legacyScore)} | ${pct(r.candidateScore)} | ${(r.scoreDelta*100).toFixed(1)} pp | ${r.roundDelta.toFixed(2)} |`).join("\n")}\n\n## Interpretation rules\n\nThis pass is a **screening pass**, not final approval. Three seeds per cell are enough to expose large systemic pacing/resource/selection problems, but not enough to declare small pairwise win-rate differences meaningful. The next pass should concentrate additional seeds on outlier families and the largest paired swings rather than brute-force every cell equally.\n\nThe candidate delivery multipliers (ranged-Stamina x1.25, Chakra x1.50), pure-control resource floors, slot formula, and provisional control-stat identities remain test hypotheses unless separately owner-approved.\n`;
fs.writeFileSync(path.join(OUT,"DC_MULTIRound_PASS_05.md"),md);

console.log(JSON.stringify({ok:true,families:FAMILIES.length,pairs:summary.pairCount,battles:battles.length,legacy:{avgRounds:allL.avgRounds,decided:allL.decidedPct,actions:allL.actionsPerFighterRound,hard:allL.hardLandsPerBattle,endStam:allL.endStamPct,endChakra:allL.endChakraPct},candidate:{avgRounds:allC.avgRounds,decided:allC.decidedPct,actions:allC.actionsPerFighterRound,hard:allC.hardLandsPerBattle,endStam:allC.endStamPct,endChakra:allC.endChakraPct},topCandidate:candFamilies.slice(0,5).map(x=>[x.family,x.scorePct]),bottomCandidate:[...candFamilies].sort((a,b)=>a.scorePct-b.scorePct).slice(0,5).map(x=>[x.family,x.scorePct]),topShift:shifts[0]},null,2));
