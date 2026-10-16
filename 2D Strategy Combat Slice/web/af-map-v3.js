(function(root){
"use strict";
const AF=root.AF,AFUI=root.AFUI;
if(!AF||!AFUI)throw new Error("AF core and AFUI must load before the V3.2 fixes");

function hasEffect(ab,kind,pred){return(ab.effects||[]).some(e=>e.k===kind&&(!pred||pred(e)));}
function activeKey(player,type){
  const stance=type==="martial"?player.activeMartial:player.activeWeapon;
  if(!stance)return null;
  return type==="martial"?(stance.styleKey||stance.sourceKey||null):(stance.weaponKey||stance.sourceKey||null);
}
AFUI.queueContext=function queueContextV32(player,queue){
  const martial=new Set(),weapon=new Set();
  const am=activeKey(player,"martial"),aw=activeKey(player,"weapon");
  if(am)martial.add(am);else if(aw)weapon.add(aw);
  let eye=!!player.eyeActive;
  for(const a of queue||[]){
    if(a.tags.includes("MartialStance")&&a.styleKey){martial.clear();weapon.clear();martial.add(a.styleKey);}
    if(a.tags.includes("WeaponStance")&&a.weaponKey){weapon.clear();martial.clear();weapon.add(a.weaponKey);}
    if(a.tags.includes("EyeOpen")||hasEffect(a,"ActivateEye"))eye=true;
  }
  // Relationship projection is owned by the core positional model, not re-derived here.
  const role=AFUI.projectedRelRole(player,queue||[]);
  return{martial,weapon,eye,role,
    grapple:AF.isStandingRole(role),mount:AF.isMountRole(role),
    submission:AFUI.projectedSubmission(player,queue||[])};
};
AFUI.queueRevealTarget=function queueRevealTarget(ab){
  if(ab?.isStyleStance)return{category:"Martial",source:ab.styleKey||"All"};
  if(ab?.isWeaponStance)return{category:"Weapon",source:ab.weaponKey||"All"};
  return null;
};
AFUI.canRenderFighter=function canRenderFighter(B,viewer,fighter){
  if(!AF.alive(fighter))return false;
  if(fighter===viewer||fighter.faction===viewer.faction)return true;
  return B.perceives(viewer,fighter);
};
AFUI.visibleFighters=function visibleFighters(B,viewer){return B.all.filter(f=>AFUI.canRenderFighter(B,viewer,f));};
if(!AF.__fogBattleTracked){
  const BaseBattle=AF.Battle;
  AF.Battle=class FogTrackedBattle extends BaseBattle{constructor(...args){super(...args);root.__AF_ACTIVE_BATTLE=this;}};
  AF.__fogBattleTracked=true;
}
AFUI.VERSION="2d-v3.5";

if(typeof document==="undefined"||typeof window==="undefined")return;

const STYLE_ID="af-map-readability-v32";
const HARD_GLYPHS=new Set(["🌲","⬡","▰"]);
const SOFT_GLYPHS=new Set(["♣","▪","☁"]);
const FELL_GLYPHS=new Set(["🪵"]);
const HAZARD_GLYPHS=new Set(["▲","✳"]);
const CSS=`
.map-legend{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:7px 11px;border-bottom:1px solid #252f50;background:#090e1c;color:var(--muted);font-size:10px}
.legend-item{display:inline-flex;align-items:center;gap:4px}.legend-swatch{width:14px;height:12px;border:2px solid;border-radius:3px;background:#10182d}
.legend-swatch.player{background:#123a4b;border-color:var(--cyan)}.legend-swatch.ally{background:#153a2d;border-color:var(--green)}.legend-swatch.enemy{background:#451c2a;border-color:var(--red)}
.legend-swatch.los{background:#30213d;border-color:#c17edc}.legend-swatch.hard{background:#41272a;border-color:var(--orange)}
.hex{transition:fill .12s,stroke .12s,stroke-width .12s}.hex.los-block{fill:#30213d;stroke:#9e68b7;stroke-width:1.7}.hex.move-block{fill:#41272a;stroke:var(--orange);stroke-width:1.9}
.hex.occupied-player{fill:#123a4b;stroke:var(--cyan);stroke-width:2.5}.hex.occupied-ally{fill:#153a2d;stroke:var(--green);stroke-width:2.3}.hex.occupied-enemy{fill:#451c2a;stroke:var(--red);stroke-width:2.3}
.hex.fell-block{fill:#33291a;stroke:#b98a4a;stroke-width:1.7}.legend-swatch.fell{background:#33291a;border-color:#b98a4a}
.hex.hazard-tile{fill:#3d1620;stroke:#e0475e;stroke-width:2.1}.legend-swatch.hazard{background:#3d1620;border-color:#e0475e}
.token.fog-hidden{display:none}.hex.reachable{fill:#153b46}.hex.selected{fill:#385879;stroke:#fff;stroke-width:2.8}.hex.hover{stroke:var(--cyan);stroke-width:2.5}
.terrain.map-blocking{filter:drop-shadow(0 0 3px #000)}.occupant-ring{pointer-events:none;fill:none;stroke-width:3;opacity:.9}.occupant-ring.player{stroke:var(--cyan)}.occupant-ring.ally{stroke:var(--green)}.occupant-ring.enemy{stroke:var(--red)}
`;
const LEGEND='<div class="map-legend" aria-label="Battle map legend"><span class="legend-item"><i class="legend-swatch player"></i>Player</span><span class="legend-item"><i class="legend-swatch ally"></i>Ally</span><span class="legend-item"><i class="legend-swatch enemy"></i>Enemy</span><span class="legend-item"><i class="legend-swatch los"></i>Blocks sight</span><span class="legend-item"><i class="legend-swatch hard"></i>Blocks move + sight</span><span class="legend-item"><i class="legend-swatch fell"></i>Felled — blocks move</span><span class="legend-item"><i class="legend-swatch hazard"></i>Hazard — damages on entry</span></div>';
function coord(el){return`${el.getAttribute("x")},${el.getAttribute("y")}`;}
function installStanceReveal(){
  document.addEventListener("click",event=>{
    const button=event.target.closest?.("button.ability[data-id]");if(!button)return;
    const tags=[...button.querySelectorAll(".cost")].map(x=>x.textContent.trim());
    const category=tags.includes("MartialStance")?"Martial":tags.includes("WeaponStance")?"Weapon":null;
    if(!category)return;
    const style=(button.closest(".style-panel")?.querySelector(".style-head b")?.textContent||button.querySelector(".source")?.textContent||"").trim();
    setTimeout(()=>{
      const tab=[...document.querySelectorAll("#categoryTabs button")].find(x=>x.dataset.cat===category);tab?.click();
      setTimeout(()=>{
        const search=document.getElementById("abilitySearch");if(search){search.value="";search.dispatchEvent(new Event("input",{bubbles:true}));}
        const locked=document.getElementById("showLocked");if(locked&&locked.checked){locked.checked=false;locked.dispatchEvent(new Event("change",{bubbles:true}));}
        const source=document.getElementById("sourceFilter");
        if(source&&[...source.options].some(o=>o.value===style||o.textContent===style)){source.value=style;source.dispatchEvent(new Event("change",{bubbles:true}));}
        const panel=[...document.querySelectorAll(".style-panel")].find(x=>x.querySelector(".style-head b")?.textContent.trim()===style);panel?.scrollIntoView({block:"nearest",behavior:"smooth"});
      },0);
    },0);
  },true);
}
function installMap(){
  if(!document.getElementById(STYLE_ID)){const style=document.createElement("style");style.id=STYLE_ID;style.textContent=CSS;document.head.appendChild(style);}
  const arena=document.getElementById("arena"),toolbar=document.querySelector(".arena-wrap .toolbar");
  if(!arena||!toolbar)return;
  if(!document.querySelector(".map-legend"))toolbar.insertAdjacentHTML("afterend",LEGEND);
  arena.setAttribute("role","img");arena.setAttribute("aria-label","Hex battle arena");
  let observer,queued=false;
  function decorate(){
    queued=false;observer.disconnect();
    const cells=new Map();
    for(const group of arena.querySelectorAll(":scope > g")){
      const polygon=group.querySelector("polygon.hex"),terrain=group.querySelector("text.terrain");
      if(!polygon||!terrain)continue;
      polygon.classList.remove("los-block","move-block","fell-block","hazard-tile","occupied-player","occupied-ally","occupied-enemy");
      group.querySelectorAll("circle.occupant-ring").forEach(x=>x.remove());
      const glyph=(terrain.textContent||"").trim();
      if(HARD_GLYPHS.has(glyph)){polygon.classList.add("los-block","move-block");terrain.classList.add("map-blocking");}
      else if(SOFT_GLYPHS.has(glyph)){polygon.classList.add("los-block");terrain.classList.add("map-blocking");}
      else if(FELL_GLYPHS.has(glyph)){polygon.classList.add("fell-block");terrain.classList.add("map-blocking");}
      else if(HAZARD_GLYPHS.has(glyph)){polygon.classList.add("hazard-tile");terrain.classList.add("map-blocking");}
      else terrain.classList.remove("map-blocking");
      cells.set(coord(terrain),{group,polygon,terrain});
    }
    const tokens=[...arena.querySelectorAll(":scope > text.token:not(.move-preview)")];
    const B=root.__AF_ACTIVE_BATTLE,viewer=B?.all.find(f=>f.isPlayer&&AF.alive(f))||null;
    const fighters=B?B.all.filter(AF.alive):[];let visibleHostiles=0,hiddenHostiles=0;
    tokens.forEach((token,index)=>{
      const fighter=fighters[index]||null;
      const visible=!fighter||!viewer||AFUI.canRenderFighter(B,viewer,fighter);
      token.classList.toggle("fog-hidden",!visible);
      if(fighter&&viewer&&fighter.faction!==viewer.faction){if(visible)visibleHostiles++;else hiddenHostiles++;}
      if(!visible)return;
      const cell=cells.get(coord(token));if(!cell)return;
      const kind=token.classList.contains("player")?"player":token.classList.contains("ally")?"ally":"enemy";
      cell.polygon.classList.add(`occupied-${kind}`);
      const ring=document.createElementNS("http://www.w3.org/2000/svg","circle");ring.setAttribute("class",`occupant-ring ${kind}`);ring.setAttribute("cx",token.getAttribute("x"));ring.setAttribute("cy",token.getAttribute("y"));ring.setAttribute("r",String(Math.round((AFUI.arenaHexStep?AFUI.arenaHexStep():34)*0.59)));cell.group.insertBefore(ring,cell.terrain);
    });
    arena.dataset.visibleHostiles=String(visibleHostiles);arena.dataset.hiddenHostiles=String(hiddenHostiles);
    observer.observe(arena,{childList:true,subtree:true});
  }
  observer=new MutationObserver(()=>{if(!queued){queued=true;requestAnimationFrame(decorate);}});
  observer.observe(arena,{childList:true,subtree:true});decorate();
}
window.addEventListener("DOMContentLoaded",()=>{installStanceReveal();installMap();});
})(typeof globalThis!=="undefined"?globalThis:this);
