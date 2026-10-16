/* Character creator (user, 2026-10-15): the player picks a skin tone, hair style, hair colour, eye colour and outfit
   for the rig drawn in the arena. Every choice is a palette swap or a layer pick over the approved male sheets
   (af-sprites-v3.js PALETTES); nothing is redrawn. The look is kept in this browser (localStorage) and read by
   AFSprites.appearanceFor when the player's sprite is created.

   Skin tones 1 and 2 are approved ramps; 3 and 4 are candidates until the user approves them. */
(function(root){
"use strict";
const STORE="af.look.v1";
const DEFAULT={outfit:"gi",hair:"long-hair",eyes:"brown-eyes",skin:"tone1",hairColor:null,eyeColor:null};
const HEX=/^#[0-9a-f]{6}$/i;
function clean(v){
  const P=root.AFSprites&&root.AFSprites.PALETTES,o={...DEFAULT};if(!v||typeof v!=="object")return o;
  if(P&&P.OUTFITS.some(x=>x[0]===v.outfit))o.outfit=v.outfit;
  if(P&&P.HAIR_STYLES.some(x=>x[0]===v.hair))o.hair=v.hair;
  if(P&&P.SKIN_TONES.some(x=>x.id===v.skin))o.skin=v.skin;
  if(HEX.test(v.hairColor||""))o.hairColor=v.hairColor.toLowerCase();
  if(HEX.test(v.eyeColor||""))o.eyeColor=v.eyeColor.toLowerCase();
  return o;
}
let look=(()=>{try{return clean(JSON.parse(localStorage.getItem(STORE)));}catch{return clean(null);}})();
function save(){try{localStorage.setItem(STORE,JSON.stringify(look));}catch{/* private mode: the look lasts this page load */}}
root.AFLook={get:()=>({...look}),set(v){look=clean({...look,...v});save();return{...look};},reset(){look=clean(null);save();return{...look};},DEFAULT};
if(typeof module!=="undefined"&&module.exports)module.exports=root.AFLook;
if(typeof document==="undefined")return;

const CSS=`.creator{display:grid;gap:10px}.creator-preview{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap}
.creator-preview canvas{background:radial-gradient(circle,#1a2442,#0a1020 75%);border:1px solid var(--line);border-radius:10px;image-rendering:pixelated;max-width:100%}
.creator-row{display:grid;grid-template-columns:96px 1fr;gap:8px;align-items:center}.creator-row>label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.swatches{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.swatch{width:26px;height:26px;border-radius:7px;border:2px solid #2c3659;padding:0;cursor:pointer;position:relative}
.swatch.on{border-color:var(--gold);box-shadow:0 0 0 2px #ffd16655}.swatch.orig{background:repeating-linear-gradient(45deg,#2a3150 0 4px,#11172b 4px 8px)}
.tone{display:inline-flex;flex-direction:column;align-items:center;gap:3px;background:transparent;border:2px solid #2c3659;border-radius:9px;padding:4px 6px;cursor:pointer;color:var(--text);font-size:10px}
.tone.on{border-color:var(--gold)}.tone .ramp{display:flex;border-radius:4px;overflow:hidden}.tone .ramp i{width:9px;height:18px;display:block}
.tone small{color:var(--muted);font-size:9px}
.pick{display:inline-flex;align-items:center;gap:5px;font-size:10px;color:var(--muted)}.pick input[type=color]{width:34px;height:26px;border:1px solid var(--line);border-radius:6px;background:#090e1d;padding:1px}
.seg{display:flex;gap:4px;flex-wrap:wrap}.seg button{border:1px solid #344066;background:#0d1427;color:#bdc7e9;border-radius:7px;padding:5px 9px;font-size:11px}.seg button.on{background:#33446e;color:#fff;border-color:#6075ad}`;

const $=id=>document.getElementById(id);
let preview=null,pctx=null,walking=false,raf=0;
function seg(id,items,cur){return`<div class="seg" id="${id}">${items.map(([v,n])=>`<button type="button" data-v="${v}" class="${v===cur?"on":""}">${n}</button>`).join("")}</div>`;}
function swatches(id,presets,cur,pickId){
  return`<div class="swatches" id="${id}">${presets.map(([n,c])=>`<button type="button" class="swatch${c?"":" orig"}${(c||null)===(cur||null)?" on":""}" title="${n}" aria-label="${n}" data-c="${c||""}" style="${c?`background:${c}`:""}"></button>`).join("")}
    <label class="pick">Any colour <input type="color" id="${pickId}" value="${cur||"#7a4a2a"}"></label></div>`;
}
function render(){
  const P=root.AFSprites.PALETTES,box=$("creatorBody");if(!box)return;
  box.innerHTML=`<div class="creator">
    <div class="creator-preview"><canvas id="creatorCanvas" width="512" height="128" aria-label="Your fighter facing south, east, north and west"></canvas>
      <div class="seg" id="creatorMotion"><button type="button" data-v="guard" class="${walking?"":"on"}">Stand</button><button type="button" data-v="walk" class="${walking?"on":""}">Walk</button></div></div>
    <div class="creator-row"><label>Skin tone</label><div class="swatches" id="creatorSkin">${P.SKIN_TONES.map(t=>`<button type="button" class="tone${t.id===look.skin?" on":""}" data-v="${t.id}"><span class="ramp">${t.ramp.map(c=>`<i style="background:${c}"></i>`).join("")}</span>${t.name}${t.approved?"":"<small>candidate</small>"}</button>`).join("")}</div></div>
    <div class="creator-row"><label>Hair style</label>${seg("creatorHair",P.HAIR_STYLES,look.hair)}</div>
    <div class="creator-row"><label>Hair colour</label>${swatches("creatorHairColor",P.HAIR_PRESETS,look.hairColor,"creatorHairPick")}</div>
    <div class="creator-row"><label>Eye colour</label>${swatches("creatorEyeColor",P.EYE_PRESETS,look.eyeColor,"creatorEyePick")}</div>
    <div class="creator-row"><label>Outfit</label>${seg("creatorOutfit",P.OUTFITS,look.outfit)}</div>
    <div class="note">Hair and eye colours use one ramp rule: the colour you pick is the hair's base and the iris colour; highlights and the iris shadow are derived from it. Striped swatch = the authored colours.</div>
  </div>`;
  preview=$("creatorCanvas");pctx=preview.getContext("2d");
  const set=v=>{root.AFLook.set(v);render();};
  box.querySelectorAll("#creatorSkin .tone").forEach(b=>b.onclick=()=>set({skin:b.dataset.v}));
  box.querySelectorAll("#creatorHair button").forEach(b=>b.onclick=()=>set({hair:b.dataset.v}));
  box.querySelectorAll("#creatorOutfit button").forEach(b=>b.onclick=()=>set({outfit:b.dataset.v}));
  box.querySelectorAll("#creatorMotion button").forEach(b=>b.onclick=()=>{walking=b.dataset.v==="walk";render();});
  box.querySelectorAll("#creatorHairColor .swatch").forEach(b=>b.onclick=()=>set({hairColor:b.dataset.c||null}));
  box.querySelectorAll("#creatorEyeColor .swatch").forEach(b=>b.onclick=()=>set({eyeColor:b.dataset.c||null}));
  // live while dragging the picker, saved when it closes
  const live=(id,key)=>{const el=$(id);el.oninput=()=>{look={...look,[key]:el.value.toLowerCase()};};el.onchange=()=>set({[key]:el.value});};
  live("creatorHairPick","hairColor");live("creatorEyePick","eyeColor");
}
function loop(now){
  raf=requestAnimationFrame(loop);
  if(!pctx||!preview.isConnected||!preview.offsetParent)return;
  root.AFSprites.drawLook(pctx,look,{state:walking?"walk":"guard",now,scale:2});
}
function install(){
  const S=root.AFSprites;if(!S||!S.PALETTES||!S.drawLook)return;
  const stats=$("stats"),anchor=stats&&stats.closest(".section");if(!anchor)return;
  if(!$("af-creator-style")){const st=document.createElement("style");st.id="af-creator-style";st.textContent=CSS;document.head.appendChild(st);}
  anchor.insertAdjacentHTML("beforebegin",`<div class="section" id="creatorSection"><h3>Appearance</h3><div id="creatorBody"><div class="note">Loading the character rig…</div></div></div>`);
  S.whenReady().then(()=>{
    if(!S.ready){$("creatorBody").innerHTML='<div class="note">The character rig did not load, so the arena draws glyph tokens and the look cannot be previewed.</div>';return;}
    render();if(!raf)raf=requestAnimationFrame(loop);
  });
}
window.addEventListener("DOMContentLoaded",install);
})(typeof globalThis!=="undefined"?globalThis:this);
