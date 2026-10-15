(function(root){
"use strict";
const AF=root.AF;
if(!AF)throw new Error("AF core must load before AFUI");
Object.assign(AF.BAL,{
  statBaseValue:AF.BAL.statBaseValue??6,
  statPointsAtLevel1:AF.BAL.statPointsAtLevel1??14,
  statPointsPerLevel:AF.BAL.statPointsPerLevel??5,
  statCostTierThresholds:AF.BAL.statCostTierThresholds||[20,30,40,50],
  statCostTierCosts:AF.BAL.statCostTierCosts||[1,2,3,4,5],
  // --- Progression (Slice 1): ability/character XP + level-based scaling ---
  abilityLevelCap:AF.BAL.abilityLevelCap??10,
  abilityXpBase:AF.BAL.abilityXpBase??50,        // xp to reach level L = base·L·(L+1)/2
  abilityCostGrowth:AF.BAL.abilityCostGrowth??0.05, // +5%/level to stam & chakra cost
  abilityMagPerCost:AF.BAL.abilityMagPerCost??0.06, // offensive: flat +power = round(this·(baseStam+baseChakra)·level)
  healEffMax:AF.BAL.healEffMax??1.0,             // heal:chakra-spent ceiling at max level (1:1)
  healEffCurveExp:AF.BAL.healEffCurveExp??1.5,   // concavity of the approach to 1:1
  xpControlRaw:AF.BAL.xpControlRaw??8,           // raw XP for landing a control/grapple effect
  xpPerOutput:AF.BAL.xpPerOutput??1.0,           // ability-xp per point of raw effect output
  abilityXpPerBattleCap:AF.BAL.abilityXpPerBattleCap??300, // max ability-xp one move earns per battle
  charXpBase:AF.BAL.charXpBase??200,             // char-xp to reach level L = base·(L-1)·L/2
  charXpPerOutput:AF.BAL.charXpPerOutput??0.5,   // char-xp per point of raw output (win or loss)
  charXpPerRound:AF.BAL.charXpPerRound??4,       // participation char-xp per round fought (loss still earns)
  charXpWinBonusPct:AF.BAL.charXpWinBonusPct??0.25 // victory adds this fraction on top of usage+participation
});

const LEVEL_MILESTONES=[
  {level:1,label:"Unawakened",detail:"Universal arts and trained styles"},
  {level:10,label:"Ascendant",detail:"Rising-sign kit"},
  {level:15,label:"Moon",detail:"Moon kit and Nakshatra summon"},
  {level:20,label:"Sun",detail:"Sun kit and Ultimate techniques"},
  {level:25,label:"Venus",detail:"Venus-sign kit"},
  {level:30,label:"Mercury",detail:"Mercury-sign kit"},
  {level:35,label:"Mars",detail:"Mars-sign kit"},
  {level:45,label:"Jupiter",detail:"Jupiter-sign kit"},
  {level:60,label:"Saturn",detail:"Saturn-sign kit"},
  {level:75,label:"Uranus",detail:"Uranus-sign kit"},
  {level:90,label:"Outer Planets",detail:"Neptune- and Pluto-sign kits"},
  {level:100,label:"North Node",detail:"Karmic Ultimate milestone (not authored yet)"}
];
const PLANET_UNLOCKS=[
  {level:15,planet:"Moon"},
  {level:20,planet:"Sun"},
  {level:25,planet:"Venus"},
  {level:30,planet:"Mercury"},
  {level:35,planet:"Mars"},
  {level:45,planet:"Jupiter"},
  {level:60,planet:"Saturn"},
  {level:75,planet:"Uranus"},
  {level:90,planet:"Neptune"},
  {level:90,planet:"Pluto"}
];
const CATEGORIES=["Ready","Zodiac","Universal","Martial","Weapon","Support","Advanced"];

const STAT_NAMES=["STR","AGI","FORT","INT","CHA"];
const STAT_BASE_VALUE=AF.BAL.statBaseValue??6;
const STAT_MAX_VALUE=100;
const STAT_POINTS_AT_LEVEL1=AF.BAL.statPointsAtLevel1??14;
const STAT_POINTS_PER_LEVEL=AF.BAL.statPointsPerLevel??5;
const STAT_COST_THRESHOLDS=[...(AF.BAL.statCostTierThresholds||[20,30,40,50])];
const STAT_COSTS=[...(AF.BAL.statCostTierCosts||[1,2,3,4,5])];

function statBudget(level){
  level=normLevel(level);
  return STAT_POINTS_AT_LEVEL1+STAT_POINTS_PER_LEVEL*(level-1);
}
function normalizeStats(stats={}){
  return Object.fromEntries(STAT_NAMES.map(name=>{
    const raw=Math.round(Number(stats[name]));
    const value=Number.isFinite(raw)?raw:STAT_BASE_VALUE;
    return[name,Math.max(STAT_BASE_VALUE,Math.min(STAT_MAX_VALUE,value))];
  }));
}
function marginalStatCost(currentValue){
  const value=Math.max(STAT_BASE_VALUE,Math.min(STAT_MAX_VALUE,Math.round(Number(currentValue)||STAT_BASE_VALUE)));
  for(let i=0;i<STAT_COST_THRESHOLDS.length&&i<STAT_COSTS.length;i++)if(value<STAT_COST_THRESHOLDS[i])return STAT_COSTS[i];
  return STAT_COSTS[STAT_COSTS.length-1]||1;
}
function statValueCost(value){
  value=Math.max(STAT_BASE_VALUE,Math.min(STAT_MAX_VALUE,Math.round(Number(value)||STAT_BASE_VALUE)));
  let total=0;
  for(let current=STAT_BASE_VALUE;current<value;current++)total+=marginalStatCost(current);
  return total;
}
function statAllocationCost(stats){
  const row=normalizeStats(stats);
  return STAT_NAMES.reduce((sum,name)=>sum+statValueCost(row[name]),0);
}
function statBudgetState(level,stats){
  const normalized=normalizeStats(stats),budget=statBudget(level),spent=statAllocationCost(normalized);
  return{level:normLevel(level),normalized,budget,spent,remaining:budget-spent,overspent:Math.max(0,spent-budget),valid:spent<=budget};
}
function trimStatsToBudget(level,stats){
  const out=normalizeStats(stats),budget=statBudget(level);
  while(statAllocationCost(out)>budget){
    let pick=null;
    for(const name of STAT_NAMES){
      if(out[name]<=STAT_BASE_VALUE)continue;
      if(!pick||out[name]>out[pick])pick=name;
    }
    if(!pick)break;
    out[pick]--;
  }
  return out;
}
function evenStatBuild(level){
  const out=Object.fromEntries(STAT_NAMES.map(name=>[name,STAT_BASE_VALUE]));
  let remaining=statBudget(level),cursor=0;
  while(remaining>0){
    let pick=-1,best=Infinity;
    for(let step=0;step<STAT_NAMES.length;step++){
      const i=(cursor+step)%STAT_NAMES.length,name=STAT_NAMES[i],value=out[name],cost=marginalStatCost(value);
      if(value>=STAT_MAX_VALUE||cost>remaining)continue;
      if(value<best){best=value;pick=i;}
    }
    if(pick<0)break;
    const name=STAT_NAMES[pick],cost=marginalStatCost(out[name]);
    out[name]++;remaining-=cost;cursor=(pick+1)%STAT_NAMES.length;
  }
  return out;
}

function normLevel(level){const n=Math.round(Number(level)||1);return Math.max(1,Math.min(100,n));}
function phaseFor(level){
  if(level<10)return"Unawakened";
  if(level<15)return"Ascendant";
  if(level<20)return"Lunar Awakening";
  if(level<45)return"Inner Planet Awakening";
  if(level<90)return"Outer Planet Awakening";
  if(level<100)return"Fully Awakened Chart";
  return"Nodal Threshold";
}
function levelProfile(chart,level,forceAllKits=false){
  level=normLevel(level);
  const entries=[],eyes=[];
  if(forceAllKits){
    for(const sign of AF.SIGNS)entries.push({source:"Debug",sign,level:1});
    eyes.push(...AF.PLANETS);
  }else{
    if(level>=10)entries.push({source:"Ascendant",sign:chart.asc.sign,level:10});
    for(const u of PLANET_UNLOCKS)if(level>=u.level){
      entries.push({source:u.planet,sign:chart.placements[u.planet].sign,level:u.level});
      eyes.push(u.planet);
    }
  }
  const signs=[...new Set(entries.map(x=>x.sign))];
  const next=LEVEL_MILESTONES.find(m=>m.level>level)||null;
  return{
    level,phase:phaseFor(level),entries,signs,eyes:[...new Set(eyes)],
    summon:forceAllKits||level>=15,
    ultimates:forceAllKits||level>=20,
    northNode:level>=100,
    forceAllKits:!!forceAllKits,
    nextUnlock:next
  };
}
function buildPlayerAbilities(chart,level,opt={}){
  const profile=levelProfile(chart,level,!!opt.forceAllKits);
  const selectedEye=profile.eyes.includes(opt.eye)?opt.eye:null;
  let abilities=AF.buildLoadout({
    signs:profile.signs,
    martials:opt.martials||[],
    weapon:opt.weapon||null,
    eye:selectedEye,
    bloodline:opt.bloodline||null,
    learnedMedical:opt.learnedMedical||[]
  });
  if(!profile.ultimates)abilities=abilities.filter(a=>!a.tags.includes("Ultimate"));
  if(!profile.summon)abilities=abilities.filter(a=>a.disc!=="Summon"&&!a.effects.some(e=>e.k==="SpawnSummon"));
  if(opt.progress)applyProgression(abilities,opt.progress);
  return{profile,abilities,selectedEye};
}
function categoryOf(ab){
  if(ab.tags.includes("Focus"))return"Focus";
  if(ab.kitSign||ab.sourceKind==="Zodiac")return"Zodiac";
  if(ab.disc==="Martial"||ab.sourceKind==="Martial")return"Martial";
  if(ab.disc==="Weapon"||ab.sourceKind==="Weapon")return"Weapon";
  if(["Medical","Trap","Summon"].includes(ab.group)||["Medical","Trap","Summon"].includes(ab.disc))return"Support";
  if(["Dojutsu","Bloodline"].includes(ab.group)||["Dojutsu","Bloodline"].includes(ab.sourceKind)||ab.disc==="Dojutsu")return"Advanced";
  return"Universal";
}
function activeStyleKey(player,type){
  const v=type==="martial"?player.activeMartial:player.activeWeapon;
  if(!v)return null;
  return type==="martial"?(v.styleKey||v.sourceKey||null):(v.weaponKey||v.sourceKey||null);
}
function hasEffect(ab,kind,pred){return ab.effects.some(e=>e.k===kind&&(!pred||pred(e)));}
/* Slot-order-aware projection of the fighter's relationship role through the queue.
   A transition queued earlier can make a later Mount-only technique *potentially* legal;
   the engine still revalidates at execution, so a failed transition cannot let the
   follow-up run illegally. */
function projectedRelRole(player,queue){
  let role=AF.relRole(player);
  for(const a of queue||[]){
    const gt=(a.effects||[]).find(e=>e.k==="GrappleTech");
    if(hasEffect(a,"Grapple")){if(role===AF.REL.FREE)role=AF.REL.GRAPPLING;continue;}
    if(hasEffect(a,"Takedown")){role=AF.REL.FREE;continue;}
    if(!gt)continue;
    if(gt.mount)role=gt.voluntaryBottom?AF.REL.MOUNTED:AF.REL.MOUNTING;
    else if(gt.throw>0||gt.breakHold)role=AF.REL.FREE;
  }
  return role;
}
function projectedSubmission(player,queue){
  let sub=!!AF.activeSubmission(player),role=AF.relRole(player);
  for(const a of queue||[]){
    const gt=(a.effects||[]).find(e=>e.k==="GrappleTech");
    if(hasEffect(a,"Grapple")){if(role===AF.REL.FREE)role=AF.REL.GRAPPLING;continue;}
    if(hasEffect(a,"Takedown")){role=AF.REL.FREE;sub=false;continue;}
    if(!gt)continue;
    if(gt.mount)role=gt.voluntaryBottom?AF.REL.MOUNTED:AF.REL.MOUNTING;
    else if(gt.throw>0||gt.breakHold){role=AF.REL.FREE;sub=false;}
    if(gt.submission&&AF.isMountRole(role))sub=true;
  }
  return sub;
}
function queueContext(player,queue){
  const martial=new Set(),weapon=new Set();
  const am=activeStyleKey(player,"martial"),aw=activeStyleKey(player,"weapon");
  if(am)martial.add(am);if(aw)weapon.add(aw);
  let eye=!!player.eyeActive;
  const role=projectedRelRole(player,queue);
  for(const a of queue){
    if(a.tags.includes("MartialStance")&&a.styleKey)martial.add(a.styleKey);
    if(a.tags.includes("WeaponStance")&&a.weaponKey)weapon.add(a.weaponKey);
    if(a.tags.includes("EyeOpen")||hasEffect(a,"ActivateEye"))eye=true;
  }
  return{martial,weapon,eye,role,
    grapple:AF.isStandingRole(role),mount:AF.isMountRole(role),
    submission:projectedSubmission(player,queue)};
}
function dependencyReason(ab,player,queue){
  const c=queueContext(player,queue);
  if(ab.minCHA&&(player.stats?.CHA||0)<ab.minCHA)return`requires CHA ${ab.minCHA}`;
  if(ab.isStyleTechnique&&ab.parentStyles?.length&&!ab.parentStyles.some(k=>c.martial.has(k)))return`queue or activate ${ab.parentStyles.join(" / ")} Stance`;
  if(ab.isWeaponTechnique&&ab.parentWeapons?.length&&!ab.parentWeapons.some(k=>c.weapon.has(k)))return`queue or activate ${ab.parentWeapons.join(" / ")} Stance`;
  if(ab.tags.includes("EyeJutsu")&&!c.eye)return"open the equipped eye first";
  // Positional filtering is applied IN ADDITION to stance filtering.
  const legal=AF.positionalLegality(player,ab,c.role);
  if(!legal.ok)return legal.reason;
  return null;
}
// Human-readable current relationship, for the ability window header.
function relationshipLabel(player){
  const role=AF.relRole(player),p=AF.relPartner(player);
  if(role===AF.REL.FREE||!p)return{role:AF.REL.FREE,text:"Free",partner:null,submission:null};
  const sub=AF.activeSubmission(player);
  return{role,text:`${role} — ${p.name}`,partner:p,
    submission:sub?{name:sub.name,holder:sub.holder.name,holding:sub.holder===player,
      consecutive:sub.consecutive,
      costMult:AF.submissionCostMult(sub),damageMult:AF.submissionDamageMult(sub),
      // How much harder the hold has made escaping, for the fighter caught in it.
      escapeTurns:AF.submissionEscapeTurns(player),
      escapeResistance:AF.submissionEscapeResistance(player)}:null};
}
function actionCost(a,priorUses,player){
  // Continuing a held submission costs more each consecutive round, so the queue must show it.
  const sub=player?AF.submissionCostMult(AF.continuedSubmission(player,a)):1;
  // stamPct/chakraPct (Recompose) cost a % of the caster's own max pool — meaningless without
  // a player to size that pool against, so they're a no-op in player-less previews.
  const pctStam=player&&a.stamPct?Math.round(a.stamPct*player.maxStam):0;
  const pctChakra=player&&a.chakraPct?Math.round(a.chakraPct*AF.effMaxChakra(player)):0;
  let stam=Math.round((a.stam+pctStam)*AF.costMult(a)*sub),chakra=Math.round((a.chakra+pctChakra)*AF.costMult(a)*sub);
  if(priorUses>=AF.BAL.repetitionFreeUses){
    const over=priorUses-AF.BAL.repetitionFreeUses+1;
    stam+=Math.round(a.stam*AF.BAL.repetitionStrainPerExtra*over);
    chakra+=Math.round(a.chakra*AF.BAL.repetitionStrainPerExtra*over);
  }
  return{stam,chakra,supplies:a.supply||0,slots:a.slots};
}
function projectedCosts(queue,player){
  let slots=0,stam=0,chakra=0,supplies=0;const uses=new Map();
  for(const a of queue){const n=uses.get(a.id)||0;uses.set(a.id,n+1);const c=actionCost(a,n,player);slots+=c.slots;stam+=c.stam;chakra+=c.chakra;supplies+=c.supplies;}
  return{slots,stam,chakra,supplies};
}
// Self-targeted Stamina/Chakra a queued action restores when it resolves. Focus
// actions (Catch Breath +stamina, Charge Chakra +chakra) apply their restore
// mid-round, so later queued actions can spend it. The planner mirrors that so it
// does not forbid a plan the engine would actually complete.
function selfRestore(ab,player){
  let stam=0,chakra=0;
  if(ab.targeting==="Self")for(const e of ab.effects||[]){
    if(e.k!=="Res")continue;
    if(e.res==="Stamina"){const g=(e.amt||0)+(e.pct?Math.round(player.maxStam*e.pct):0);if(g>0)stam+=g;}
    else if(e.res==="Chakra"){const g=(e.amt||0)+(e.pct?Math.round(AF.effMaxChakra(player)*e.pct):0);if(g>0)chakra+=g;}
  }
  return{stam,chakra};
}
// Running stamina/chakra/supplies/slots after resolving `queue` in order, crediting
// each action's self restore (capped at the player's maxima), matching engine flow.
function queueResourceState(player,queue){
  let stam=player.stam,chakra=player.chakra,supplies=player.supplies,slots=0;const uses=new Map();
  for(const a of queue){
    const n=uses.get(a.id)||0;uses.set(a.id,n+1);const c=actionCost(a,n,player);
    stam-=c.stam;chakra-=c.chakra;supplies-=c.supplies;slots+=c.slots;
    const r=selfRestore(a,player);
    stam=Math.min(player.maxStam,stam+r.stam);chakra=Math.min(AF.effMaxChakra(player),chakra+r.chakra);
  }
  return{stam,chakra,supplies,slots,uses};
}
function lockReason(ab,player,queue){
  const dep=dependencyReason(ab,player,queue);if(dep)return dep;
  if(ab.tags.includes("MartialStance")&&activeStyleKey(player,"martial")===ab.styleKey)return"stance already active";
  if(ab.tags.includes("WeaponStance")&&activeStyleKey(player,"weapon")===ab.weaponKey)return"stance already active";
  if(queue.some(q=>q.id===ab.id)&&ab.tags.includes("Stance"))return"stance already queued";
  if(AF.hasStatus(player,"Silence")&&ab.chakra>0)return"silenced";
  if(AF.hasStatus(player,"Disarm")&&ab.disc==="Weapon")return"disarmed";
  if(ab.tags.includes("Trap")&&(player.trapUses[ab.id]||0)>=AF.BAL.trapUsesPerBattle)return"trap pouch empty";
  const rs=queueResourceState(player,queue);
  const cap=AF.availableSlots(player);
  if(rs.slots+ab.slots>cap)return "not enough action slots";
  const cost=actionCost(ab,rs.uses.get(ab.id)||0,player);
  if(cost.stam>rs.stam)return`needs ${cost.stam-rs.stam} more stamina`;
  if(cost.chakra>rs.chakra)return`needs ${cost.chakra-rs.chakra} more chakra`;
  if(cost.supplies>rs.supplies)return"not enough supplies";
  return null;
}
function dependencyVisible(ab,player,queue,showLockedChildren=false){
  if(showLockedChildren)return true;
  return !dependencyReason(ab,player,queue);
}
function sourceLabel(ab){
  if(ab.tags.includes("Focus"))return"Focus";
  if(ab.kitSign)return`${ab.kitSign} kit`;
  if(ab.parentStyles?.length>1)return"Shared martial";if(ab.styleKey||ab.parentStyles?.length)return(ab.styleKey||ab.parentStyles.join(" / "));
  if(ab.weaponKey||ab.parentWeapons?.length)return(ab.weaponKey||ab.parentWeapons.join(" / "));
  if(ab.eyePlanet)return`${ab.eyePlanet} eye`;
  if(ab.bloodlineKey)return ab.bloodlineKey;
  return ab.group||ab.disc||"Universal";
}
function effectSummary(e,ab){
  if(e.k==="Damage")return`Power ${e.power}`;
  if(e.k==="Heal")return`Heal ${Math.max(0,Math.round(e.power*(ab?.healOutputMult??1)))}`;
  if(e.k==="Status"){
  const scope=ab&&ab.group!=="Dojutsu"&&ab.group!=="Bloodline"&&ab.disc!=="Dojutsu",tier=scope&&AF.BAL.useCandidateDcModel&&root.AFDC&&root.AFDC.statusTier(e);
  return`${e.status} ${e.dur||1}rd${tier?` (${tier}-tier ${root.AFDC.saveStat(e)} save)`:e.save?` (${e.save.stat} DC${e.save.dc})`:""}`;
}
  if(e.k==="Res")return`${e.res} ${e.amt>=0?"+":""}${e.amt}${e.pct?` +${Math.round(e.pct*100)}%`:""}`;
  if(e.k==="Buff")return`${e.stat} ${e.pct>=0?"+":""}${e.pct}% ${e.dur}rd`;
  if(e.k==="Terrain")return e.trigger?`${e.kind} hazard ${e.dur}rd — ${e.trigger.map(t=>effectSummary(t,ab)).join(", ")} on entry`:`${e.kind} terrain ${e.dur}rd`;
  if(e.k==="Grapple")return`Standing Grapple ${e.dur}rd`;
  if(e.k==="Takedown")return`${e.status} ${e.dur}rd; thrown ${e.behind} tile behind the user; ends the hold`;
  if(e.k==="GrappleTech"){
    const parts=[];
    if(e.mount)parts.push(e.voluntaryBottom?"Voluntary transition to Mounted":"Transition to Mounting");
    if(e.submission)parts.push("Maintained Submission");
    if(e.throw>0)parts.push("Relationship reposition");
    else if(e.breakHold)parts.push("Ends the hold");
    if(e.focusLock>0)parts.push(`Denies Focus ${e.focusLock}rd`);
    return parts.length?parts.join(" · "):"Grapple technique";
  }
  if(e.k==="SpawnSummon")return"Call companion";
  if(e.k==="Haunt")return"Persistent phantom";
  if(e.k==="ActivateEye")return`Open ${e.planet} eye`;
  if(e.k==="MC")return`Movement +${e.amt}`;
  if(e.k==="Move")return`Move ${e.tiles}`;
  if(e.k==="Push")return`Pushes target back ${e.tiles} tile${e.tiles>1?"s":""}`;
  if(e.k==="WardNext")return"Negate next targeted hostile ability";
  return e.k;
}
function abilitySummary(ab){
  if(ab.name==="Catch Breath")return`Recover ${Math.round(AF.BAL.focusRestorePercent*100)}% of max stamina. Grants no poise.`;
  if(ab.name==="Charge Chakra")return`Recover ${Math.round(AF.BAL.focusRestorePercent*100)}% of max chakra. Grants no poise.`;
  if(ab.name==="Recompose")return`Recover ${Math.round(AF.BAL.focusRestorePercent*100)}% of max poise. Costs ${Math.round(AF.BAL.recomposeCostPercent*100)}% of max stamina and ${Math.round(AF.BAL.recomposeCostPercent*100)}% of max chakra. No effect while Mounted.`;
  const fx=ab.effects.map(e=>effectSummary(e,ab)).filter(Boolean).join(" · ");
  const target=ab.targeting==="Self"?"Self":ab.targeting==="PointRadius"?`Area r${ab.radius||1}`:ab.targeting||"Target";
  return`${target}${ab.dmg&&ab.dmg!=="None"?` · ${ab.dmg}`:""}${fx?` · ${fx}`:""}`;
}
function matches(ab,query){
  if(!query)return true;
  const q=query.toLowerCase();
  return[ab.name,ab.disc,ab.group,ab.kitSign,sourceLabel(ab),...(ab.tags||[]),abilitySummary(ab)].filter(Boolean).join(" ").toLowerCase().includes(q);
}
function visibleAbilities(abilities,player,queue,opt={}){
  const category=opt.category||"Ready",source=opt.source||"All",query=(opt.query||"").trim();
  return abilities.filter(ab=>{
    if(ab.tags.includes("Focus"))return false;
    if(!dependencyVisible(ab,player,queue,!!opt.showLockedChildren))return false;
    const cat=categoryOf(ab);
    if(category==="Ready"){if(lockReason(ab,player,queue))return false;}
    else if(cat!==category)return false;
    if(source!=="All"&&sourceLabel(ab)!==source&&ab.disc!==source&&ab.kitSign!==source)return false;
    return matches(ab,query);
  });
}
function focusAbilities(abilities){return abilities.filter(a=>a.tags.includes("Focus")).sort((a,b)=>a.name.localeCompare(b.name));}
function sourcesFor(abilities,player,queue,category){
  const rows=abilities.filter(a=>!a.tags.includes("Focus")&&dependencyVisible(a,player,queue,false)&&(category==="Ready"?!lockReason(a,player,queue):categoryOf(a)===category));
  return["All",...new Set(rows.map(sourceLabel).sort())];
}
function categoryCounts(abilities,player,queue){
  const out={};
  for(const c of CATEGORIES)out[c]=visibleAbilities(abilities,player,queue,{category:c}).length;
  return out;
}
function validateQueue(player,queue){
  const invalid=[];
  for(let i=0;i<queue.length;i++){const reason=dependencyReason(queue[i],player,queue.slice(0,i));if(reason)invalid.push({index:i,ability:queue[i],reason});}
  return invalid;
}
function sanitizeQueue(player,queue){
  const kept=[],dropped=[];
  for(const ab of queue){const reason=dependencyReason(ab,player,kept);if(reason)dropped.push({ability:ab,reason});else kept.push(ab);}
  return{kept,dropped};
}
function groupRows(rows,category){
  const m=new Map();
  for(const a of rows){
    let key;
    if(category==="Zodiac")key=`${a.kitSign||"Unknown"} · ${a.disc}`;
    else if(category==="Ready")key=categoryOf(a);
    else key=sourceLabel(a);
    if(!m.has(key))m.set(key,[]);m.get(key).push(a);
  }
  for(const list of m.values())list.sort((a,b)=>a.name.localeCompare(b.name));
  return[...m.entries()];
}

/* =========================================================================
   PROGRESSION (Slice 1) — character XP + per-ability XP, and the level-based
   magnitude/cost scaling. A profile is { charXp, level, abilityXp:{key:xp} }.
   The engine (af-core) only records raw effect output into Battle.xp; this layer
   owns the curves, the scaling applied at build, and the end-of-battle commit.
   Nothing here runs unless a profile is passed to buildPlayerAbilities / commit.
   ========================================================================= */
function newProgress(){return{charXp:0,level:1,abilityXp:{}};}
function abilityXpToReach(L){return AF.BAL.abilityXpBase*L*(L+1)/2;}
function abilityLevelFromXp(xp){const cap=AF.BAL.abilityLevelCap;let L=0;while(L<cap&&(xp||0)>=abilityXpToReach(L+1))L++;return L;}
function charXpToReach(L){return AF.BAL.charXpBase*(L-1)*L/2;}
function charLevelFromXp(xp){let L=1;while(L<100&&(xp||0)>=charXpToReach(L+1))L++;return L;}
// Focus/stance abilities are enablers, not scalable output — never level them.
function isProgressable(ab){return !(ab.tags?.includes("Focus")||ab.tags?.includes("Stance"));}
function healEffectsOf(ab){return(ab.effects||[]).filter(e=>e.k==="Heal");}
// Efficiency (HP restored ÷ chakra spent) rises from the ability's authored ratio
// toward the 1:1 ceiling, reaching it exactly at max ability level.
function healEfficiencyAt(eff0,A){const cap=AF.BAL.abilityLevelCap,mx=AF.BAL.healEffMax;if(A>=cap)return mx;return mx-(mx-eff0)*Math.pow(1-A/cap,AF.BAL.healEffCurveExp);}
// Scale a freshly-built ability clone in place for ability level A (>0).
function scaleAbility(ab,A){
  if(A<=0||!isProgressable(ab))return ab;
  const cm=1+AF.BAL.abilityCostGrowth*A,costBaseStam=ab.stam||0,costBaseChakra=ab.chakra||0;
  const baseStam=ab._authoredStam??costBaseStam,baseChakra=ab._authoredChakra??costBaseChakra;
  const heals=healEffectsOf(ab);
  ab.stam=Math.round(costBaseStam*cm);ab.chakra=Math.round(costBaseChakra*cm);
  if(heals.length){
    const effChakra0=Math.round(baseChakra*AF.costMult(ab)),effChakraNow=Math.round(ab.chakra*AF.costMult(ab));
    for(const e of heals){
      const eff0=effChakra0>0?Math.min(AF.BAL.healEffMax,e.power/effChakra0):AF.BAL.healEffMax;
      e.power=Math.floor(effChakraNow*healEfficiencyAt(eff0,A));
    }
  }else{
    // Offensive mastery stays normalized by original authored cost; balance floors raise spend, not bonus damage.
    const add=Math.round(AF.BAL.abilityMagPerCost*(baseStam+baseChakra)*A);
    if(add>0)for(const e of ab.effects||[])if(e.k==="Damage")e.power+=add;
  }
  return ab;
}
// Terrain-placing abilities (e.g. Earth Wall) grow their placement radius with use:
// a single tile at ability level 0, up to the authored radius at max level.
function scaleTerrainRadius(ab,A){
  if(!(ab.radius>0)||!(ab.effects||[]).some(e=>e.k==="Terrain"))return;
  ab.radius=Math.round(ab.radius*Math.min(1,A/AF.BAL.abilityLevelCap));
}
function applyProgression(abilities,progress){
  if(!progress||!progress.abilityXp)return abilities;
  for(const ab of abilities){const A=abilityLevelFromXp(progress.abilityXp[AF.abilityKey(ab)]||0);ab.abilityLevel=A;scaleTerrainRadius(ab,A);if(A>0)scaleAbility(ab,A);}
  return abilities;
}
// Fold a finished battle's XP ledger into the player's profile. God-mode and
// force-unlock battles award nothing (mirrors the canon save rule).
function commitProgress(battle,progress,opt={}){
  if(!battle||!progress)return{committed:false,reason:"missing"};
  if(battle.god||opt.god)return{committed:false,reason:"god-mode"};
  const player=battle.all.find(f=>f.isPlayer);
  if(!player)return{committed:false,reason:"no-player"};
  progress.abilityXp=progress.abilityXp||{};
  const ledger=battle.xp&&battle.xp.get(player),abilityGains={};let totalRaw=0;
  if(ledger)for(const[key,raw]of ledger){
    totalRaw+=raw;
    const gain=Math.min(AF.BAL.abilityXpPerBattleCap,Math.round(raw*AF.BAL.xpPerOutput));
    const before=abilityLevelFromXp(progress.abilityXp[key]||0);
    progress.abilityXp[key]=(progress.abilityXp[key]||0)+gain;
    abilityGains[key]={xp:gain,levelBefore:before,levelAfter:abilityLevelFromXp(progress.abilityXp[key])};
  }
  const factionAlive=battle.all.some(f=>f.faction===player.faction&&AF.alive(f));
  const enemyAlive=battle.all.some(f=>f.faction!==player.faction&&AF.alive(f));
  const won=opt.won!=null?!!opt.won:(factionAlive&&!enemyAlive);
  const rounds=Math.max(1,(battle.round||1)-1);
  const charFromOutput=Math.round(totalRaw*AF.BAL.charXpPerOutput);
  const charFromParticipation=rounds*AF.BAL.charXpPerRound;
  const base=charFromOutput+charFromParticipation;
  const charFromWin=won?Math.round(base*AF.BAL.charXpWinBonusPct):0;
  const charGain=base+charFromWin;
  const levelBefore=charLevelFromXp(progress.charXp||0);
  progress.charXp=(progress.charXp||0)+charGain;progress.level=charLevelFromXp(progress.charXp);
  return{committed:true,won,abilityGains,charGain,charFromOutput,charFromParticipation,charFromWin,rounds,totalRaw,charXp:progress.charXp,levelBefore,levelAfter:progress.level};
}

root.AFUI={
  VERSION:"2d-v3.5",LEVEL_MILESTONES,PLANET_UNLOCKS,CATEGORIES,normLevel,levelProfile,buildPlayerAbilities,
  STAT_NAMES,STAT_BASE_VALUE,STAT_MAX_VALUE,STAT_POINTS_AT_LEVEL1,STAT_POINTS_PER_LEVEL,STAT_COST_THRESHOLDS,STAT_COSTS,
  statBudget,normalizeStats,marginalStatCost,statValueCost,statAllocationCost,statBudgetState,trimStatsToBudget,evenStatBuild,
  categoryOf,sourceLabel,abilitySummary,projectedCosts,dependencyReason,dependencyVisible,lockReason,
  projectedRelRole,projectedSubmission,relationshipLabel,queueContext,
  visibleAbilities,focusAbilities,sourcesFor,categoryCounts,validateQueue,sanitizeQueue,groupRows,queueContext,matches,
  newProgress,abilityXpToReach,abilityLevelFromXp,charXpToReach,charLevelFromXp,scaleAbility,applyProgression,commitProgress,healEfficiencyAt
};
})(typeof globalThis!=="undefined"?globalThis:this);
