(function(root){
"use strict";

// Live V3.4 playtest implementation for the 2026-08 DC / CC / DOT balance pass.
// The resolver and loadout economy consume this model by default for the tested
// Sign + Universal + Martial + Weapon scope. Grapples remain a separate lane.

const TIER_OFFSETS={C:13,B:10,A:8,S:7};
const TIER_LANDING={C:0.60,B:0.45,A:0.35,S:0.30};
const STATUS_TIERS={
  // S — hard action-economy control
  Prone:"S",Stun:"S",Fear:"S",Sleep:"S",
  // A — major control / denial
  Confusion:"A",Blind:"A",Root:"A",
  // B — tactical control
  Slow:"B",Snare:"B",Silence:"B",Disarm:"B",
  // C — attrition / light riders
  Bleed:"C",Burn:"C",Poison:"C",Psychosomatic:"C",Cripple:"C",
};

// Live-playtest defaults for automatic riders that currently have no authored
// save. Existing authored saves keep their save-stat identity. These defaults are
// deliberately isolated here because per-ability control/save stat identity is
// remain tunable from live-test evidence.
const DEFAULT_SAVE_STAT={
  Prone:"AGI",Stun:"FORT",Fear:"STR",Sleep:"INT",
  Confusion:"INT",Blind:"INT",Root:"AGI",
  Slow:"AGI",Snare:"AGI",Silence:"CHA",Disarm:"STR",
  Bleed:"AGI",Burn:"FORT",Poison:"FORT",Psychosomatic:"INT",Cripple:"FORT",
};

const MELEE_STAMINA_FLOOR={C:10,B:12,A:15,S:20};
const PURE_MELEE_EQUIV={A:20,S:30};
const FAMILY_SCALE={meleeStamina:1,rangedStamina:1.25,chakra:1.5};

const clamp=(v,lo,hi)=>Math.max(lo,Math.min(hi,v));
const trunc=n=>n<0?Math.ceil(n):Math.floor(n);

function statusTier(effectOrStatus){
  const status=typeof effectOrStatus==="string"?effectOrStatus:effectOrStatus?.status;
  return STATUS_TIERS[status]||null;
}
function saveStat(effect){return effect?.save?.stat||DEFAULT_SAVE_STAT[effect?.status]||null;}
function controlStat(ability,effect){
  if(ability?.controlStat)return ability.controlStat;if(effect?.controlStat)return effect.controlStat;
  const disc=ability?.disc||"",group=ability?.group||"",status=effect?.status||"";
  if(disc==="Genjutsu")return"CHA";
  if(disc==="Ninjutsu")return"INT";
  if(disc==="Dojutsu")return ability?.atk==="GenVisual"?"CHA":"INT";
  if(disc==="Trap"||disc==="Medical"||group==="Trap"||group==="Medical")return"INT";
  if(["Taijutsu","Martial","Weapon"].includes(disc)){
    if(["Bleed","Blind","Slow","Prone","Root","Snare","Cripple"].includes(status))return"AGI";
    return"STR";
  }
  return saveStat(effect);
}
function masteryBonus(abilityLevel){return Math.floor(Math.max(0,Number(abilityLevel)||0)/4);}
function statEdge(attackerStat,defenderStat){return clamp(trunc(((Number(attackerStat)||0)-(Number(defenderStat)||0))/5),-6,6);}
function candidateDC(tier,attackerStat,defenderStat,abilityLevel=0){
  if(!TIER_OFFSETS[tier])return null;
  return TIER_OFFSETS[tier]+statEdge(attackerStat,defenderStat)+masteryBonus(abilityLevel);
}
function resolveCandidateSave({tier,attackerStat,defenderStat,abilityLevel=0,roll}){
  const dc=candidateDC(tier,attackerStat,defenderStat,abilityLevel);
  if(dc==null)throw new Error(`Unknown DC tier ${tier}`);
  roll=Math.max(1,Math.min(20,Math.round(Number(roll)||1)));
  // Save die: natural 1 always fails, natural 20 always succeeds.
  const landed=roll===1?true:roll===20?false:roll<dc;
  return{tier,dc,roll,landed,resisted:!landed};
}
function exactLandingRate(tier,attackerStat,defenderStat,abilityLevel=0){
  let lands=0;for(let roll=1;roll<=20;roll++)if(resolveCandidateSave({tier,attackerStat,defenderStat,abilityLevel,roll}).landed)lands++;
  return lands/20;
}
function candidateStatusCheck(ability,effect,attackerStats,defenderStats,roll){
  const tier=statusTier(effect);if(!tier)return null;
  const sv=saveStat(effect),cs=controlStat(ability,effect);if(!sv||!cs)return null;
  const atk=attackerStats?.[cs]??0,def=defenderStats?.[sv]??0;
  return{...resolveCandidateSave({tier,attackerStat:atk,defenderStat:def,abilityLevel:ability?.abilityLevel||0,roll}),saveStat:sv,controlStat:cs,attackerStat:atk,defenderStat:def,automaticInLegacy:!effect.save};
}

function isPureControl(ability){return ability?.dmg==="None"&&["SingleEnemy","PointRadius"].includes(ability?.targeting);}
function isAoeControl(ability){return ability?.targeting==="PointRadius";}
function hasGuardBreak(ability){return Number(ability?.poiseMult||1)>1;}
function deliveryFamily(ability){
  if((ability?.chakra||0)>0)return"chakra";
  if((ability?.stam||0)>0&&(ability?.atk==="Projectile"||(ability?.maxR||1)>1))return"rangedStamina";
  return"meleeStamina";
}
function elementalCostMult(ability){return ability?.dmg==="Elemental"?1.75:1;}
function tierResourceFloor(ability,tier){
  const family=deliveryFamily(ability),scale=FAMILY_SCALE[family];
  let base;
  if(isPureControl(ability)&&PURE_MELEE_EQUIV[tier])base=PURE_MELEE_EQUIV[tier];
  else base=MELEE_STAMINA_FLOOR[tier];
  if(base==null)return null;
  let floor=Math.ceil(base*scale);
  if(tier==="S"&&hasGuardBreak(ability))floor=Math.ceil(floor*1.25);
  return{family,effectiveFloor:floor};
}
function candidateResource(ability,tier){
  const floor=tierResourceFloor(ability,tier);if(!floor)return null;
  const mult=elementalCostMult(ability);
  const channel=(ability?.chakra||0)>0?"chakra":(ability?.stam||0)>0?"stam":null;
  if(!channel)return{...floor,channel:null,currentAuthored:0,currentEffective:0,suggestedAuthored:0};
  const authored=Number(ability[channel]||0),effective=Math.round(authored*mult);
  // Floor is expressed as resolver-true spend. Elemental already pays x1.75,
  // so translate the floor back to authored Chakra instead of charging range twice.
  const suggested=Math.max(authored,Math.ceil(floor.effectiveFloor/mult));
  return{...floor,channel,currentAuthored:authored,currentEffective:effective,suggestedAuthored:suggested,suggestedEffective:Math.round(suggested*mult),resolverMult:mult};
}
function candidateSlots(ability,tier){
  if(!tier)return ability?.slots||1;
  if(ability?.name==="Sweeping Low")return 1;
  // Grapples never call this path: they are not Status effects in the catalog.
  if(tier==="C"||tier==="B")return 1;
  if(isPureControl(ability)||isAoeControl(ability))return tier==="S"?3:2;
  return 2;
}
function primaryTier(ability){
  let best=null;const order={C:1,B:2,A:3,S:4};
  for(const e of ability?.effects||[]){const t=statusTier(e);if(t&&(!best||order[t]>order[best]))best=t;}
  return best;
}
function auditAbility(ability){
  const tier=primaryTier(ability);if(!tier)return{ability,tier:null};
  return{ability,tier,slots:candidateSlots(ability,tier),resource:candidateResource(ability,tier),effects:(ability.effects||[]).filter(e=>statusTier(e)).map(e=>({status:e.status,tier:statusTier(e),saveStat:saveStat(e),automaticInLegacy:!e.save}))};
}

const API={
  TIER_OFFSETS,TIER_LANDING,STATUS_TIERS,DEFAULT_SAVE_STAT,MELEE_STAMINA_FLOOR,PURE_MELEE_EQUIV,FAMILY_SCALE,
  statusTier,saveStat,controlStat,masteryBonus,statEdge,candidateDC,resolveCandidateSave,exactLandingRate,candidateStatusCheck,
  isPureControl,isAoeControl,hasGuardBreak,deliveryFamily,elementalCostMult,tierResourceFloor,candidateResource,candidateSlots,primaryTier,auditAbility,
};
root.AFDC=API;

// Owner corrections (2026-08-13): Karate + Medical kit boundaries/ranges.
const AF=root.AF;
if(AF){
  AF.MARTIAL.Karate.moves=AF.MARTIAL.Karate.moves.filter(a=>a.name!=="Defensive Stance");
  const originalGeneralArts=AF.generalArts;
  const correctMedical=rows=>{for(const a of rows){if(a.group!=="Medical"&&a.disc!=="Medical")continue;if(a.name==="Palm Healing")a.maxR=1;if(a.name==="Cellular Activation"||a.name==="Chakra Transfer")a.maxR=3;}return rows;};
  AF.generalArts=()=>correctMedical(originalGeneralArts());
  const originalBuildLoadout=AF.buildLoadout;
  AF.buildLoadout=function(opt={}){const learned=new Set(opt.learnedMedical||[]);return correctMedical(originalBuildLoadout(opt)).filter(a=>(a.group!=="Medical"&&a.disc!=="Medical")||learned.has(a.name));};
  const wraithMoves=AF.ENEMIES.Wraith&&AF.ENEMIES.Wraith.moves;
  if(wraithMoves)AF.ENEMIES.Wraith.moves=function(){const rows=wraithMoves();const i=rows.findIndex(a=>a.name==="Spectral Touch");if(i>=0){const src=AF.zodiacAbilities("Pisces").find(a=>a.name==="Flow Strike");if(src)rows[i]={...src,name:"Spectral Touch",effects:(src.effects||[]).map(e=>({...e})),tags:[...(src.tags||[])]};}return rows;};
  if(root.document){const sel=root.document.getElementById("learnedMedical");if(sel){sel.innerHTML='<option value="">None</option><option value="Palm Healing|Cellular Activation|Chakra Transfer|Chakra Scalpel|Nerve Rupture">Medical Kit</option>';const f=sel.closest&&sel.closest(".field");const l=f&&f.querySelector("label");if(l)l.textContent="Learned Medical kit";const n=f&&f.querySelector("small.note");if(n)n.textContent="Live-test override until the find/learn system is implemented. Medical is learned as one support kit; non-support NPCs do not receive Medical abilities.";}}
}

if(typeof module!=="undefined"&&module.exports)module.exports=API;
})(typeof globalThis!=="undefined"?globalThis:this);
