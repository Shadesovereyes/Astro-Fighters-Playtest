(function(root){
"use strict";
const AF=root.AF;
if(!AF)throw new Error("AF core must load before the V3 patch");
if(AF.__v3Patched)return;

const originalBuildLoadout=AF.buildLoadout;
const originalResolveRound=AF.resolveRound;
const uniq=a=>[...new Set(a.filter(Boolean))];

function martialParents(name,keys){
  return uniq(keys.filter(k=>AF.MARTIAL[k]&&AF.MARTIAL[k].moves.some(m=>m.name===name)));
}
function weaponParents(name,key){
  return key&&AF.WEAPONS[key]&&AF.WEAPONS[key].moves.some(m=>m.name===name)?[key]:[];
}
function styleForStance(name,keys){return keys.find(k=>AF.MARTIAL[k]&&AF.MARTIAL[k].stance.name===name)||null;}
function weaponForStance(name,key){return key&&AF.WEAPONS[key]&&AF.WEAPONS[key].stance.name===name?key:null;}
function bloodlineKey(name){return AF.BLOOD_KEYS.find(k=>AF.BLOODLINES[k].name===name)||null;}

AF.buildLoadout=function buildLoadoutV3(opt={}){
  const rows=originalBuildLoadout(opt);
  const martialKeys=opt.unlockAll?Object.keys(AF.MARTIAL):uniq([...(opt.martials||[]),...(opt.martial?[opt.martial]:[])]);
  const weaponKey=opt.weapon||null;
  const deduped=[];
  const martialMoves=new Map();

  for(const ab of rows){
    if(ab.kitSign){
      Object.assign(ab,{sourceKind:"Zodiac",sourceKey:ab.kitSign});
    }else if(ab.tags.includes("MartialStance")){
      const key=styleForStance(ab.name,martialKeys);
      Object.assign(ab,{sourceKind:"Martial",sourceKey:key,styleKey:key,parentStyles:key?[key]:[],isStyleStance:true});
    }else if(ab.disc==="Martial"){
      const parents=martialParents(ab.name,martialKeys);
      Object.assign(ab,{sourceKind:"Martial",sourceKey:parents[0]||null,styleKey:parents[0]||null,parentStyles:parents,isStyleTechnique:true});
      const dkey=ab.disc+"|"+ab.name;
      if(martialMoves.has(dkey)){
        const kept=martialMoves.get(dkey);
        kept.parentStyles=uniq([...(kept.parentStyles||[]),...parents]);
        if(kept.parentStyles.length>1)kept.sourceKey="Shared martial";
        continue;
      }
      martialMoves.set(dkey,ab);
    }else if(ab.tags.includes("WeaponStance")){
      const key=weaponForStance(ab.name,weaponKey);
      Object.assign(ab,{sourceKind:"Weapon",sourceKey:key,weaponKey:key,parentWeapons:key?[key]:[],isWeaponStance:true});
    }else if(ab.disc==="Weapon"){
      const parents=weaponParents(ab.name,weaponKey);
      Object.assign(ab,{sourceKind:"Weapon",sourceKey:parents[0]||null,weaponKey:parents[0]||null,parentWeapons:parents,isWeaponTechnique:true});
    }else if(ab.eyePlanet){
      Object.assign(ab,{sourceKind:"Dojutsu",sourceKey:ab.eyePlanet});
    }else{
      const blood=bloodlineKey(ab.name);
      if(blood)Object.assign(ab,{sourceKind:"Bloodline",sourceKey:blood,bloodlineKey:blood});
      else Object.assign(ab,{sourceKind:"Universal",sourceKey:ab.group||"General"});
    }
    deduped.push(ab);
  }
  return deduped;
};

function activeKey(owner,type){
  const stance=type==="martial"?owner.activeMartial:owner.activeWeapon;
  if(!stance)return null;
  return type==="martial"?(stance.styleKey||stance.sourceKey||null):(stance.weaponKey||stance.sourceKey||null);
}
function projectedCell(B,plan){
  const owner=plan.owner,goal=plan.moveTo;
  if(!goal||AF.isRooted(owner))return owner.cell;
  let mc=AF.moveBudget(owner);
  const {cells}=B.grid.reachable(owner.cell,mc,c=>B.occupied(c,owner));
  return cells.get(AF.hkey(goal))||owner.cell;
}
function projectedPositions(B,plans){
  const out=new Map(B.all.map(f=>[f,f.cell]));
  for(const p of plans||[])out.set(p.owner,projectedCell(B,p));
  return out;
}
function projectedNearestEnemy(B,owner,positions){
  const from=positions.get(owner)||owner.cell;let best=null,bd=Infinity;
  for(const e of B.all){
    if(!AF.alive(e)||e.faction===owner.faction)continue;
    const d=AF.hdist(from,positions.get(e)||e.cell);
    if(d<bd){bd=d;best=e;}
  }
  return best;
}
function playerTargetingReason(B,owner,ab,positions,chosenTarget,chosenPoint){
  if(!owner.isPlayer)return null;
  const from=positions.get(owner)||owner.cell;
  // A throw destination is aimed relative to the grapple partner's cell and the ability's
  // authored throw range — a different check than AoE/terrain/summon placement, which is
  // relative to the caster. An unaimed throw (no chosenPoint) is always fine: the engine
  // falls back to its default straight-line-away direction.
  const throwEffect=(ab.effects||[]).find(e=>e.k==="GrappleTech"&&e.throw>0);
  if(throwEffect){
    if(!chosenPoint)return null;
    const partner=AF.relPartner(owner);
    if(!partner)return null; // no live relationship yet; execution will reject the ability itself
    if(AF.hdist(partner.cell,chosenPoint)>throwEffect.throw)return`${ab.name} can't throw that far`;
    return null;
  }
  // Ground-targeted placement (AoE / terrain / summon): validate the cell, not a creature.
  if(chosenPoint){
    const dist=AF.hdist(from,chosenPoint);
    if(ab.needsLoS&&!B.grid.los(from,chosenPoint))return`${ab.name} has no line of sight to that spot`;
    if(AF.evalRange(ab,dist).outcome==="Impossible")return`${ab.name} can't reach that spot`;
    return null;
  }
  if(ab.targeting==="SingleAlly"){
  if(!chosenTarget)return null;
  if(!AF.alive(chosenTarget)||chosenTarget.faction!==owner.faction)return`${ab.name} has no valid ally target`;
  const to=positions.get(chosenTarget)||chosenTarget.cell,dist=AF.hdist(from,to);
  if(dist>(ab.maxR??1))return`${ab.name} is out of range for ${chosenTarget.name}`;
  return null;
}
if(ab.targeting!=="SingleEnemy")return null;
  const partner=AF.relPartner(owner);
  const linked=partner&&AF.alive(partner)?partner:null;
  const target=linked||chosenTarget||projectedNearestEnemy(B,owner,positions);
  if(!target)return null;
  if(!AF.alive(target)||target.faction===owner.faction)return`${ab.name} has no valid target`;
  if(!B.perceives(owner,target))return`${owner.name} has lost sight of ${target.name}`;
  const to=positions.get(target)||target.cell,dist=AF.hdist(from,to);
  if(ab.needsLoS&&!B.grid.los(from,to))return`${ab.name} has no line of sight to ${target.name}`;
  if(dist>AF.DR.awareness(AF.eff(owner)))return`${ab.name} has no clear line to ${target.name}`;
  // Reach abilities are melee attacks with a gap-closing lunge: valid as long as the target is
  // within the reach radius of where the user will stand (the lunge closes the rest at resolution).
  if(ab.reach>0){if(dist>ab.reach)return`${target.name} slipped out of ${ab.name}'s reach`;return null;}
  if(AF.evalRange(ab,dist).outcome==="Impossible")return`${ab.name} is out of range for ${target.name}`;
  return null;
}
// Slot-order-aware role projection is shared with the AI planner (AF.advanceProjectedRole).
const advanceProjectedRole=AF.advanceProjectedRole;
function sanitizePlan(B,plan,positions){
  const martial=new Set(),weapon=new Set();
  const am=activeKey(plan.owner,"martial"),aw=activeKey(plan.owner,"weapon");
  if(am)martial.add(am);if(aw)weapon.add(aw);
  const actions=[];
  // Projected relationship role: a transition earlier in the plan can legitimately
  // unlock a later Mount-only technique. Execution still revalidates the REAL state,
  // so a failed transition makes the follow-up fail cleanly instead of running.
  let role=AF.relRole(plan.owner);
  let slots=0;const slotCap=AF.availableSlots(plan.owner);
  for(let entry of plan.actions||[]){
    const ab=entry&&entry.ability?entry.ability:entry;
    let chosenTarget=entry&&entry.ability?entry.target:null;const chosenPoint=entry&&entry.ability?entry.point:null;
    // A queued strike whose chosen enemy has already fallen (died earlier this round, or to a
    // start-of-round DOT) retargets to the weakest reachable foe instead of being dropped.
    if(ab.targeting==="SingleEnemy"&&chosenTarget&&!AF.alive(chosenTarget)){
      const swap=AF.retargetDefeated(B,plan.owner,ab);
      if(swap){B.line(`${chosenTarget.name} is down — ${plan.owner.name} redirects ${ab.name} to ${swap.name}.`,"sys");entry={ability:ab,target:swap,point:chosenPoint};chosenTarget=swap;}
    }
    let reason=null;
    if(ab.isStyleTechnique&&ab.parentStyles?.length&&!ab.parentStyles.some(k=>martial.has(k)))reason=`${ab.name} requires its martial stance`;
    if(ab.isWeaponTechnique&&ab.parentWeapons?.length&&!ab.parentWeapons.some(k=>weapon.has(k)))reason=`${ab.name} requires its weapon stance`;
    if(!reason){const legal=AF.positionalLegality(plan.owner,ab,role);if(!legal.ok)reason=`${ab.name} is illegal from ${role} — ${legal.reason}`;}
    if(!reason&&slots+(ab.slots||1)>slotCap)reason=`${ab.name} exceeds the ${slotCap} usable action slots`;
    if(!reason)reason=playerTargetingReason(B,plan.owner,ab,positions,chosenTarget,chosenPoint);
    if(reason){B.line(`${plan.owner.name}'s ${reason}; the action is removed from the plan.`,"sys");continue;}
    actions.push(entry);slots+=ab.slots||1;
    role=advanceProjectedRole(role,ab);
    if(ab.tags.includes("MartialStance")&&ab.styleKey){martial.clear();weapon.clear();martial.add(ab.styleKey);}
    if(ab.tags.includes("WeaponStance")&&ab.weaponKey){weapon.clear();martial.clear();weapon.add(ab.weaponKey);}
  }
  return{...plan,actions};
}
AF.resolveRound=function resolveRoundV3(B,plans){
  const positions=projectedPositions(B,plans);
  return originalResolveRound(B,plans.map(p=>sanitizePlan(B,p,positions)));
};
AF.VERSION="2d-v3.3";
AF.__v3Patched=true;
})(typeof globalThis!=="undefined"?globalThis:this);
