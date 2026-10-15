(function(root){
"use strict";
const AF=root.AF,AFUI=root.AFUI;
if(!AF||!AFUI)throw new Error("AF core and AFUI must load before the V3.5 progression overlay");
const LEGACY_PROXY={STR:9,AGI:9,FORT:9,INT:9,CHA:8};
let pendingPlayerStats=null;
const originalMakeFighter=AF.makeFighter;

AFUI.queueCanonicalPlayerStats=function queueCanonicalPlayerStats(stats){pendingPlayerStats=AFUI.normalizeStats(stats);return{...pendingPlayerStats};};
AFUI.clearCanonicalPlayerStats=function clearCanonicalPlayerStats(){pendingPlayerStats=null;};
AFUI.legacyStatProxy=function legacyStatProxy(){return{...LEGACY_PROXY};};
AF.makeFighter=function makeFighterV34(options){
  if(options?.isPlayer&&pendingPlayerStats){options={...options,stats:{...pendingPlayerStats}};pendingPlayerStats=null;}
  return originalMakeFighter(options);
};
AF.VERSION="2d-v3.5";
AFUI.VERSION="2d-v3.5";

if(typeof document==="undefined"||typeof window==="undefined")return;
const $=id=>document.getElementById(id);
function rawStats(){return Object.fromEntries(AFUI.STAT_NAMES.map(name=>[name,+$("s"+name)?.value]));}
function writeStats(stats){const row=AFUI.normalizeStats(stats);for(const name of AFUI.STAT_NAMES){const input=$("s"+name);if(input)input.value=row[name];}}
function renderBudget(){
  const row=AFUI.normalizeStats(rawStats()),level=AFUI.normLevel(+$('level').value),state=AFUI.statBudgetState(level,row);
  const total=$('statTotal'),note=$('statBudgetNote');
  if(total){total.textContent=`${state.spent} / ${state.budget}`;total.style.color=!state.valid?'var(--red)':state.remaining===0?'var(--green)':'var(--gold)';}
  if(note){note.textContent=!state.valid?`Over budget by ${state.overspent} point${state.overspent===1?'':'s'}. Lower one or more attributes.`:state.remaining===0?'Level budget fully allocated.':`${state.remaining} point${state.remaining===1?'':'s'} left to allocate at level ${state.level}.`;note.className=!state.valid?'error':state.remaining===0?'ok':'note';}
  for(const name of AFUI.STAT_NAMES){const value=row[name],cost=value>=AFUI.STAT_MAX_VALUE?null:AFUI.marginalStatCost(value),label=$("cost"+name);if(label)label.textContent=cost==null?'Maximum reached':`Next +1 costs ${cost} point${cost===1?'':'s'}`;}
  return state;
}
function installAllocator(){
  const stats=$('stats'),level=$('level'),range=$('levelRange'),start=$('start');if(!stats||!level||!range||!start)return;
  const section=stats.closest('.section'),intro=section?.querySelector('.note'),summaryLabel=section?.querySelector('.summaryline span');
  if(intro)intro.textContent='Every attribute starts at 6. Raising a stat costs 1 point below 20, 2 below 30, 3 below 40, 4 below 50, and 5 thereafter.';
  if(summaryLabel)summaryLabel.textContent='Points spent / level budget';
  stats.innerHTML=AFUI.STAT_NAMES.map((name,i)=>`<div class="field"><label>${name}</label><input id="s${name}" type="number" min="${AFUI.STAT_BASE_VALUE}" max="${AFUI.STAT_MAX_VALUE}" value="${[9,9,9,9,8][i]}"><small id="cost${name}" class="note" style="display:block;margin-top:4px;font-size:9px"></small></div>`).join('');
  if(!$('statBudgetNote'))section?.querySelector('.summaryline')?.insertAdjacentHTML('afterend','<div id="statBudgetNote" class="ok">Level budget fully allocated.</div><div class="actions"><button id="autoStats" class="secondary" type="button">Auto-spend evenly</button><button id="resetStats" class="secondary" type="button">Reset to base 6</button></div>');
  for(const name of AFUI.STAT_NAMES){const input=$("s"+name);input.addEventListener('input',renderBudget);input.addEventListener('change',()=>{writeStats(rawStats());renderBudget();});}
  $('autoStats').onclick=()=>{writeStats(AFUI.evenStatBuild(+level.value));renderBudget();};
  $('resetStats').onclick=()=>{writeStats(Object.fromEntries(AFUI.STAT_NAMES.map(name=>[name,AFUI.STAT_BASE_VALUE])));renderBudget();};
  const levelChanged=()=>{const n=AFUI.normLevel(+level.value);level.value=n;range.value=n;writeStats(AFUI.trimStatsToBudget(n,rawStats()));renderBudget();};
  level.addEventListener('input',levelChanged);range.addEventListener('input',levelChanged);
  level.value='1';range.value='1';level.dispatchEvent(new Event('input',{bubbles:true}));
  start.addEventListener('click',event=>{
    const canonical=AFUI.normalizeStats(rawStats()),state=AFUI.statBudgetState(+level.value,canonical);
    if(!state.valid){event.preventDefault();event.stopImmediatePropagation();const error=$('setupError');if(error)error.textContent=`Attribute allocation exceeds the level ${state.level} budget by ${state.overspent} point${state.overspent===1?'':'s'}.`;return;}
    AFUI.queueCanonicalPlayerStats(canonical);writeStats(AFUI.legacyStatProxy());
    setTimeout(()=>{writeStats(canonical);AFUI.clearCanonicalPlayerStats();renderBudget();},0);
  },true);
  AFUI.VERSION='2d-v3.5';const engine=$('engineState');if(engine)engine.textContent=`AF ${AF.VERSION} · UI ${AFUI.VERSION}`;
  renderBudget();
}
window.addEventListener('DOMContentLoaded',()=>setTimeout(installAllocator,0));
})(typeof globalThis!=="undefined"?globalThis:this);
