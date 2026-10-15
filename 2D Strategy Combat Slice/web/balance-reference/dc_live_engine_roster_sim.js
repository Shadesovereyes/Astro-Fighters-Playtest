"use strict";
const fs=require("fs");
global.window=global;
require("../af-core.js");
require("../af-dc-model-v3.js");
const {AF,AFDC:DC}=global;
AF.BAL.useCandidateDcModel=true;
AF.setSeed(0xDCC0DE);

const roster=[];
for(const sign of AF.SIGNS)roster.push(...AF.zodiacAbilities(sign));
roster.push(...AF.generalArts());
for(const [style,row] of Object.entries(AF.MARTIAL))roster.push(row.stance,...row.moves);
for(const [kit,row] of Object.entries(AF.WEAPONS))roster.push(row.stance,...row.moves);

const entries=[];
for(const ab of roster){
  if(!["SingleEnemy","PointRadius"].includes(ab.targeting))continue;
  for(const e of ab.effects||[]){const tier=DC.statusTier(e);if(!tier)continue;entries.push({ab,e,tier,control:DC.controlStat(ab,e),save:DC.saveStat(e),legacyAutomatic:!e.save});}
}
if(roster.length<160||entries.length<60)throw new Error(`unexpected roster coverage ${roster.length}/${entries.length}`);
for(const x of entries)if(!x.control||!x.save)throw new Error(`missing control/save identity: ${x.ab.name}/${x.e.status}`);

function cloneAbility(ab,level){return{...ab,abilityLevel:level,effects:(ab.effects||[]).map(e=>({...e,save:e.save?{...e.save}:undefined})),tags:[...(ab.tags||[])]};}
function idealDistance(ab){if(ab.atk==="Melee"||ab.atk==="GenTouch"||ab.atk==="GenVisual")return 1;if(ab.atk==="Projectile")return ab.maxR>=5?5:Math.max(1,Math.min(3,ab.maxR||1));if(ab.atk==="Magic")return Math.max(1,Math.min(3,ab.maxR||1));return 1;}
function all20(){return{STR:20,AGI:20,FORT:20,INT:20,CHA:20};}
function runTrial(entry,scenario){
  const aStats=all20(),dStats=all20();
  if(scenario.atkEdge)aStats[entry.control]+=scenario.atkEdge;
  if(scenario.defEdge)dStats[entry.save]+=scenario.defEdge;
  const ab=cloneAbility(entry.ab,scenario.level),dist=idealDistance(ab),grid=AF.makeArena(10);
  const attacker=AF.makeFighter({name:"A",sign:"Aries",stats:aStats,faction:0,cell:AF.hx(0,0),abilities:[ab]});
  const defender=AF.makeFighter({name:"D",sign:"Taurus",stats:dStats,faction:1,cell:AF.hx(dist,0),abilities:[]});
  const B=new AF.Battle([attacker,defender],grid);
  const action={ability:ab,target:defender};if(ab.targeting==="PointRadius")action.point={...defender.cell};
  AF.resolveRound(B,[{owner:attacker,actions:[action],moveTo:null},{owner:defender,actions:[],moveTo:null}]);
  const needle=`Candidate save vs ${entry.e.status}`;
  const log=B.log.find(x=>String(x.calc||"").includes(needle));
  if(!log)return{delivered:false,landed:false};
  return{delivered:true,landed:String(log.calc).includes("→ failed")};
}
const scenarios=[
  {name:"equal_L0",level:0,atkEdge:0,defEdge:0},
  {name:"equal_L10",level:10,atkEdge:0,defEdge:0},
  {name:"specialist_attacker_L10",level:10,atkEdge:27,defEdge:0},
  {name:"specialist_defender_L10",level:10,atkEdge:0,defEdge:27},
];
const N=800,rows=[];
for(const entry of entries){for(const scenario of scenarios){let delivered=0,landed=0;for(let i=0;i<N;i++){const r=runTrial(entry,scenario);if(r.delivered){delivered++;if(r.landed)landed++;}}
  const atk=20+(scenario.atkEdge||0),def=20+(scenario.defEdge||0),expected=DC.exactLandingRate(entry.tier,atk,def,scenario.level);
  rows.push({ability:entry.ab.name,discipline:entry.ab.disc,group:entry.ab.group,status:entry.e.status,tier:entry.tier,controlStat:entry.control,saveStat:entry.save,legacyAutomatic:entry.legacyAutomatic,targeting:entry.ab.targeting,attackType:entry.ab.atk,scenario:scenario.name,attempts:N,delivered,landed,deliveryRate:delivered/N,conditionalLanding:delivered?landed/delivered:0,rawLanding:landed/N,expectedConditional:expected});
}}
function avg(arr,key,weightKey=null){if(!arr.length)return 0;if(!weightKey)return arr.reduce((s,x)=>s+x[key],0)/arr.length;const w=arr.reduce((s,x)=>s+x[weightKey],0);return w?arr.reduce((s,x)=>s+x[key]*x[weightKey],0)/w:0;}
const aggregates=[];
for(const scenario of scenarios)for(const tier of ["C","B","A","S"]){const subset=rows.filter(r=>r.scenario===scenario.name&&r.tier===tier);if(!subset.length)continue;const delivered=subset.reduce((s,r)=>s+r.delivered,0),landed=subset.reduce((s,r)=>s+r.landed,0);const expected=avg(subset,"expectedConditional");const observed=delivered?landed/delivered:0;aggregates.push({scenario:scenario.name,tier,effects:subset.length,delivered,landed,observedConditional:observed,expectedConditional:expected,deviationPctPoints:(observed-expected)*100});if(Math.abs(observed-expected)>0.025)throw new Error(`${scenario.name}/${tier} aggregate ${observed} deviates from ${expected}`);}
const controlCounts={};for(const e of entries){const k=`${e.ab.disc}:${e.control}`;controlCounts[k]=(controlCounts[k]||0)+1;}
const automatic=entries.filter(e=>e.legacyAutomatic).length;
const slotRaises=roster.map(ab=>DC.auditAbility(ab)).filter(x=>x.tier&&x.slots>(x.ability.slots||1)).length;
const resourceRaises=roster.map(ab=>DC.auditAbility(ab)).filter(x=>x.tier&&x.resource&&x.resource.channel&&x.resource.suggestedAuthored>x.resource.currentAuthored).length;
const summary={generated:"2026-08-12",rosterAbilities:roster.length,harmfulStatusEffects:entries.length,legacyAutomaticEffects:automatic,trialsPerEffectScenario:N,totalResolvedRounds:entries.length*scenarios.length*N,controlStatCounts:controlCounts,slotRaiseCandidates:slotRaises,resourceRaiseCandidates:resourceRaises,aggregates};
fs.writeFileSync(__dirname+"/DC_LIVE_ENGINE_ROSTER_RESULTS.json",JSON.stringify({summary,rows},null,2));
const cols=Object.keys(rows[0]);const esc=v=>{const s=String(v??"");return /[",\n]/.test(s)?`"${s.replace(/"/g,'""')}"`:s;};fs.writeFileSync(__dirname+"/DC_LIVE_ENGINE_ROSTER_RESULTS.csv",cols.join(",")+"\n"+rows.map(r=>cols.map(c=>esc(r[c])).join(",")).join("\n")+"\n");
let md=`# Astro Fighters — Live Engine DC Roster Pass 04\n\n_Date: 2026-08-12._\n\nThis pass exercises the candidate DC model through the real \`AF.resolveRound\` / \`applyStatus\` path with candidate mode enabled only inside the harness. It covers Sign, Universal, Martial, and Weapon abilities together.\n\n## Scope\n\n- Roster abilities: **${summary.rosterAbilities}**\n- Tiered hostile Status/DOT effects: **${summary.harmfulStatusEffects}**\n- Legacy automatic hostile effects normalized by candidate mode: **${summary.legacyAutomaticEffects}**\n- Trials per effect/scenario: **${N}**\n- Total real-engine resolved rounds: **${summary.totalResolvedRounds.toLocaleString()}**\n\n## Provisional attacker control-stat schema\n\nThis is a test hypothesis, **not owner-locked**. Explicit ability/effect metadata overrides all defaults.\n\n- Genjutsu → CHA\n- Ninjutsu → INT\n- Trap / Medical hostile control → INT\n- Physical finesse riders (Bleed, Blind, Slow, Prone, Root, Snare, Cripple) → AGI\n- Other physical force/control riders → STR\n- Dojutsu (outside this requested roster) → CHA for GenVisual, INT otherwise\n\n## Aggregate conditional landing results\n\n| Scenario | Tier | Effects | Observed | Exact target | Deviation |\n|---|---|---:|---:|---:|---:|\n`;
for(const a of aggregates)md+=`| ${a.scenario} | ${a.tier} | ${a.effects} | ${(a.observedConditional*100).toFixed(1)}% | ${(a.expectedConditional*100).toFixed(1)}% | ${a.deviationPctPoints>=0?"+":""}${a.deviationPctPoints.toFixed(2)} pp |\n`;
md+=`\n## Cost/slot shadow audit\n\n- Status abilities that would gain slots under the current candidate formula: **${slotRaises}**.\n- Status abilities below the current candidate authored-resource recommendation: **${resourceRaises}**.\n\n## Interpretation\n\nThe real resolver reproduces the candidate tier probabilities after delivery while preserving the engine's actual attack/range gate before single-target damaging riders. Automatic legacy riders now participate in the same save path during candidate-mode tests. This pass validates plumbing and probability behavior; it does **not** approve the provisional control-stat assignments or final resource/slot changes.\n`;
fs.writeFileSync(__dirname+"/DC_LIVE_ENGINE_ROSTER_PASS_04.md",md);
console.log(JSON.stringify(summary,null,2));
