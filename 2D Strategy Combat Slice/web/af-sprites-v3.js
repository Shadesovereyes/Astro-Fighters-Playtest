/* Sprite layer for the hex arena: the playtest character rig (web/characters/male.json, imported by
   tools/import-playtest-rig.mjs) drawn over the SVG map, and each resolved round replayed from the
   engine's event record (Battle.events: move, act, hit, evade, parry, knock).

   Presentation only. The engine resolves the round first and the page renders the final state; the
   replay then animates from the pre-round positions to that state. Nothing here feeds back into
   combat. If the rig cannot load (file://, the standalone or Artifact builds), handles() is false and
   the arena keeps its glyph tokens. */
(function(root){
"use strict";

const FRAME=64,PIVOT=[32,63];
// fighters drawn as glyphs: beasts, undead, summons and the caravan have no rig
const NON_HUMAN_GLYPHS=new Set(["🐻","🐯","🦀","🧟","👻","🦇"]);
const HAIRS=["fade-hair","long-hair","afro-hair"],EYES=["brown-eyes","purple-eyes"];
const WDEPTH_UNDER=["behind","trailBehind"],WDEPTH_OVER=["top","trail"];
// the hex testbed's weapon kits mapped onto the rig's authored weapons. The rig has no sickle or bow:
// Kyoketsu-Shoge's blade uses the one-handed tanto, and Kyudo shots play as ranged casts.
const WEAPON_KITS={Kenjutsu:"katana",KyoketsuShoge:"tanto"};

function hash(s){let h=2166136261;for(const ch of String(s||""))h=Math.imul(h^ch.codePointAt(0),16777619);return h>>>0;}
function isHumanoid(f){return !!f&&!f.isSummon&&!f.isCaravan&&!NON_HUMAN_GLYPHS.has(f.glyph);}

/* --- appearance palettes (character creator) ---
   Every option is a colour-only palette swap of the approved sheets: exact colours are remapped per layer and no
   pixel moves. Skin maps the locked 5-step Body1 ramp step for step (repository AGENTS.md). Tones 1 and 2 are the
   approved ramps; tones 3 and 4 are candidates awaiting the user's approval. Hair and eye colours come from one
   ramp rule (colorRamp): the picked colour is the hair's base and the iris's main tone, hair highlights are the
   ramp's lighter steps and the iris shadow its darker step. */
const SKIN_KEY=["#f6a35b","#c87845","#9e4a31","#70241d","#3f0505"];   // light, mid, shadow, dark, deep
const SKIN_TONES=[
  {id:"tone1",name:"Tone 1",ramp:SKIN_KEY,approved:true},
  {id:"tone2",name:"Tone 2",ramp:["#e0764b","#b24b36","#96392b","#7b2b21","#4a1510"],approved:true},
  {id:"tone3",name:"Tone 3",ramp:["#f7cfae","#e0a47f","#bf7a58","#8d4f36","#52261a"],approved:false},
  {id:"tone4",name:"Tone 4",ramp:["#9c6440","#7a4529","#5b2f1b","#402011","#230d06"],approved:false}
];
const HAIR_KEY={base:["#3f0505"],light1:["#70241d","#702219"],light2:["#9e4a31"]};
const EYE_KEY={base:["#a36b3e","#e39ced"],dark1:["#754c2b","#93549c"],lid:["#70241d"]};
const HAIR_PRESETS=[["Original",null],["Black","#1c1517"],["Chestnut","#5e3119"],["Auburn","#86301b"],["Ginger","#c0561f"],["Blonde","#d6a640"],
  ["Platinum","#e2d6b4"],["Silver","#9ba1aa"],["Blue","#3550b0"],["Pink","#cf6597"],["Green","#3b8a4c"],["Violet","#6d3fa6"]];
const EYE_PRESETS=[["Original",null],["Hazel","#977434"],["Green","#4b9a50"],["Blue","#4c7ed6"],["Grey","#8b95a3"],["Amber","#cf8a28"],
  ["Violet","#e39ced"],["Red","#c83a3a"]];
const HAIR_STYLES=[["fade-hair","Fade"],["long-hair","Long"],["afro-hair","Afro"]];
const OUTFITS=[["gi","Gi"],["blueArmor","Blue armour"],["redArmor","Red armour"]];
const hexToRgb=h=>{const n=parseInt(h.slice(1),16);return[n>>16&255,n>>8&255,n&255];};
const rgbToHex=([r,g,b])=>"#"+[r,g,b].map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,"0")).join("");
function rgbToHsl([r,g,b]){r/=255;g/=255;b/=255;const mx=Math.max(r,g,b),mn=Math.min(r,g,b),l=(mx+mn)/2;let h=0,s=0;
  if(mx!==mn){const d=mx-mn;s=l>.5?d/(2-mx-mn):d/(mx+mn);h=mx===r?(g-b)/d+(g<b?6:0):mx===g?(b-r)/d+2:(r-g)/d+4;h*=60;}return[h,s,l];}
function hslToRgb([h,s,l]){h=((h%360)+360)%360;const c=(1-Math.abs(2*l-1))*s,x=c*(1-Math.abs((h/60)%2-1)),m=l-c/2;
  const [r,g,b]=h<60?[c,x,0]:h<120?[x,c,0]:h<180?[0,c,x]:h<240?[0,x,c]:h<300?[x,0,c]:[c,0,x];return[(r+m)*255,(g+m)*255,(b+m)*255];}
// hue shifting, as pixel ramps do: highlights lean toward warm yellow, shadows toward cool violet
function shiftHue(h,to,by){const d=((to-h+540)%360)-180;return h+Math.sign(d)*Math.min(Math.abs(d),by);}
function lighter(hex){const [h,s,l]=rgbToHsl(hexToRgb(hex));return rgbToHex(hslToRgb([shiftHue(h,55,8),s*0.9,Math.min(0.93,l+(1-l)*0.22+0.04)]));}
function darker(hex){const [h,s,l]=rgbToHsl(hexToRgb(hex));return rgbToHex(hslToRgb([shiftHue(h,265,6),Math.min(1,s*1.05),l*0.66]));}
function colorRamp(hex){const l1=lighter(hex);return{light2:lighter(l1),light1:l1,base:hex.toLowerCase(),dark1:darker(hex)};}
const toneOf=id=>SKIN_TONES.find(t=>t.id===id)||SKIN_TONES[0];
// exact-colour maps (lower-case hex -> hex) for one look; null when the layer keeps its authored colours
function skinMap(look){const t=toneOf(look&&look.skin);if(t.ramp===SKIN_KEY)return null;const m={};SKIN_KEY.forEach((k,i)=>m[k]=t.ramp[i]);return m;}
function hairMap(look){if(!look||!look.hairColor)return null;const r=colorRamp(look.hairColor),m={};
  for(const [step,keys] of Object.entries(HAIR_KEY))for(const k of keys)m[k]=r[step];return m;}
function eyeMap(look){const m={},t=toneOf(look&&look.skin);let any=false;
  if(look&&look.eyeColor){const r=colorRamp(look.eyeColor);for(const k of EYE_KEY.base)m[k]=r.base;for(const k of EYE_KEY.dark1)m[k]=r.dark1;any=true;}
  if(t.ramp!==SKIN_KEY){for(const k of EYE_KEY.lid)m[k]=t.ramp[3];any=true;}
  return any?m:null;}
const SKIN_LAYERS=new Set(["body","arms","far-arm"]);
const palMemo=new Map();
function paletteFor(layer,look){
  const kind=SKIN_LAYERS.has(layer)?"skin":HAIRS.includes(layer)?"hair":EYES.includes(layer)?"eye":null;
  if(!kind||!look)return null;
  const key=kind+"|"+(look.skin||"")+"|"+(kind==="hair"?look.hairColor||"":kind==="eye"?look.eyeColor||"":"");
  if(palMemo.has(key))return palMemo.get(key);
  const m=kind==="skin"?skinMap(look):kind==="hair"?hairMap(look):eyeMap(look);
  palMemo.set(key,m);return m;
}
const PALETTES={SKIN_KEY,SKIN_TONES,HAIR_KEY,EYE_KEY,HAIR_PRESETS,EYE_PRESETS,HAIR_STYLES,OUTFITS,colorRamp,paletteFor};
// outfit by side: allies in blue armour, opponents in red; the player wears what the character creator saved (AFLook),
// otherwise the gi. Opponents' skin, hair and eyes vary by name.
function appearanceFor(f,player){
  if(f===player){
    const saved=root.AFLook&&root.AFLook.get?root.AFLook.get():null;
    return Object.assign({outfit:"gi",hair:"long-hair",eyes:"brown-eyes",skin:"tone1",hairColor:null,eyeColor:null},saved||{});
  }
  const side=player&&f.faction===player.faction?"blueArmor":"redArmor";
  const h=hash(f.name);
  return{outfit:side,hair:HAIRS[h%HAIRS.length],eyes:"brown-eyes",skin:SKIN_TONES[(h>>>5)%SKIN_TONES.length].id,
    hairColor:HAIR_PRESETS[(h>>>8)%HAIR_PRESETS.length][1],eyeColor:EYE_PRESETS[(h>>>12)%EYE_PRESETS.length][1]};
}
function scopeKit(ab){const sc=ab&&ab.pos&&ab.pos.scope;if(!sc)return null;const [kind,key]=sc.split("|");return kind==="Weapon"?key:null;}
function stanceKit(f){const w=f&&f.activeWeapon;return w?(w.weaponKey||w.sourceKey||null):null;}
function weaponFor(f,ab){const k=scopeKit(ab)||stanceKit(f);return WEAPON_KITS[k]||null;}
// the looping pose a fighter holds between actions
function basePose(f){
  if((f.stam||0)<=0)return{state:"exhausted"};
  const w=weaponFor(f,null);
  if(w==="katana")return{state:"twoHandGuard",weapon:"katana"};
  if(w==="tanto")return{state:"oneHandGuard",weapon:"tanto"};
  return{state:"guard"};
}
function isStrike(ab){return !!ab&&!!ab.dmg&&ab.dmg!=="None";}
// what an act plays, from the ability table (af-anim-map-v3.js): a clip sequence, a ranged bolt, or nothing.
// Repeated katana light cuts alternate down and up so a string of slashes reads as a chain.
function attackClip(f,ab,counters){
  const map=root.AFAnimMap?root.AFAnimMap.forAbility(ab):null;
  if(!map)return null;
  if(!map.play.length)return isStrike(ab)&&ab.atk!=="Melee"?{kind:"cast",fit:map.fit,need:map.need}:null;
  const n=counters?(counters.get(f)||0):0;if(counters)counters.set(f,n+1);
  const seq=map.play.map(([state,clip])=>({state,clip:state==="katanaLight"&&n%2?(clip==="downCut"?"upCut":"downCut"):clip}));
  return{seq,weapon:map.weapon||weaponFor(f,null),fit:map.fit,need:map.need};
}
// How a landed hit reads on the defender (owner ruling 2026-10-14): while the defender still had poise when
// the blow landed, it is taken on the guard (block); the blow that empties poise plays the guard-break
// stagger; only hits on a fighter already at 0 poise play the recoil. A downing blow always recoils.
function hitReaction(e){
  if(e.killed||!e.guarded)return"hitReact";
  return e.broke?"guardBreak":"block";
}
// four-direction facing along the dominant screen axis (the rig's attack rule); W mirrors E in the sheets
function faceToward(a,b,fallback){
  const dx=b.x-a.x,dy=b.y-a.y;
  if(!dx&&!dy)return fallback||"S";
  return Math.abs(dx)>=Math.abs(dy)?(dx>0?"E":"W"):(dy>0?"S":"N");
}
// hitReact is authored for E and W only: a fighter facing N or S recoils in the E/W row toward the hitter
function reactFacing(state,facing,a,b,def){
  const rows=def&&def.states[state]?def.states[state].rows:["S","E","N","W"];
  if(rows.includes(facing))return facing;
  return b.x>=a.x?"W":"E";
}
// Clinch moves (approved paired clips, 2026-10-14/15): by the actor's standing-grapple role and ability name ->
// [actor clip, partner clip], played on the same frames. Rolling Throw is usable from either role; the thrower always
// plays the holder's side of the pair.
const CLINCH_CLIPS={
  Grappling:{"Uppercut":["clinchUppercut","clinchUppercutHit"],"Knee Strikes":["clinchKnee","clinchKneeHit"],"Elbow Strike":["clinchElbow","clinchElbowHit"],
    "Body Shot":["clinchBodyShot","clinchBodyShotHit"],"Hip Toss":["clinchHipToss","clinchHipTossHit"],"Rolling Throw":["clinchRollingThrow","clinchRollingThrowHit"]},
  Grappled:{"Uppercut":["clinchHeldUppercut","clinchHoldHit"],"Knee Strikes":["clinchHeldKnee","clinchHoldKneeHit"],"Elbow Strike":["clinchHeldElbow","clinchHoldElbowHit"],
    "Rolling Throw":["clinchRollingThrow","clinchRollingThrowHit"]}
};
const THROWS=new Set(["Hip Toss","Rolling Throw"]);
function clinchClips(role,ab){const t=CLINCH_CLIPS[role];return t&&ab?t[ab.name]||null:null;}
const PAIR_GAP=27;          // holder and held pivots, px apart along E/W (the approved pair previews)
// where a clinched pair stands: pulled together around the midpoint of their cells, side by side, the holder
// facing the held fighter along E/W
function pairSpots(h,d){
  const mx=(h.x+d.x)/2,my=Math.round((h.y+d.y)/2),sx=d.x>=h.x?1:-1;
  const hx=Math.round(mx-sx*PAIR_GAP/2);
  return{holder:{x:hx,y:my,facing:sx>0?"E":"W"},held:{x:hx+sx*PAIR_GAP,y:my,facing:sx>0?"W":"E"}};
}
// Groups a round's events into beats played in order. The movement phase is one beat (everyone walks
// at once); each act is a beat holding its own approach, the act, and the reactions it caused.
function planBeats(events){
  const beats=[];let moves=[],cur=null;
  for(const e of events||[]){
    if(e.type==="move"&&e.phase==="move"){moves.push(e);continue;}
    if(e.type==="drown"){let b=beats.find(x=>x.drown);if(!b){b={drown:[]};beats.push(b);}b.drown.push(e);continue;}
    if(e.type==="move"&&e.phase==="action"){if(cur&&!cur.act)cur.approach.push(e);else{cur={approach:[e],act:null,reactions:[]};beats.push(cur);}continue;}
    if(e.type==="act"){if(cur&&!cur.act&&cur.approach.length)cur.act=e;else{cur={approach:[],act:e,reactions:[]};beats.push(cur);}continue;}
    if(!cur){cur={approach:[],act:null,reactions:[]};beats.push(cur);}
    cur.reactions.push(e);
  }
  if(moves.length)beats.unshift({moves});
  return beats;
}

// a facing a state can draw: the dominant-axis facing when the state has that row, else E/W toward the other
function faceIn(rows,a,b,fallback){
  const f=faceToward(a,b,fallback);
  if(!rows||rows.includes(f))return f;
  return b.x>=a.x?"E":"W";
}

/* --- GIF encoder (GIF89a, LZW), for the recap export ---
   Frames are RGBA ImageData-like {width,height,data}. Each frame stores only the rectangle that changed since the
   previous one (disposal "leave in place"); an unchanged frame lengthens the previous frame's delay. A frame with more
   than 256 colours is reduced by dropping low bits per channel until it fits. */
function lzw(indices,minCode){
  const out=[];let cur=0,bits=0;const emit=(code,size)=>{cur|=code<<bits;bits+=size;while(bits>=8){out.push(cur&255);cur>>>=8;bits-=8;}};
  const clear=1<<minCode,eoi=clear+1;let size=minCode+1,next=eoi+1,dict=new Map();
  emit(clear,size);
  let prefix=indices[0];
  for(let i=1;i<indices.length;i++){
    const k=indices[i],key=prefix*4096+k;const hit=dict.get(key);
    if(hit!==undefined){prefix=hit;continue;}
    emit(prefix,size);
    if(next<4096){dict.set(key,next++);if(next>(1<<size)&&size<12)size++;}
    else{emit(clear,size);dict=new Map();size=minCode+1;next=eoi+1;}
    prefix=k;
  }
  emit(prefix,size);emit(eoi,size);if(bits>0)out.push(cur&255);
  return out;
}
function GifEncoder(width,height){
  const bytes=[];const w16=v=>{bytes.push(v&255,v>>8&255);};const str=s=>{for(const c of s)bytes.push(c.charCodeAt(0));};
  str("GIF89a");w16(width);w16(height);bytes.push(0x70,0,0);           // no global table, 8-bit colour resolution
  str("!");bytes.push(0xff,11);str("NETSCAPE2.0");bytes.push(3,1,0,0,0); // loop forever
  let prev=null,pending=null,frames=0;
  function quantize(px){
    for(let shift=0;shift<=6;shift++){                                  // at 6 (2 bits a channel) 64 colours always fit
      const mask=(0xff<<shift)&0xff,half=shift?1<<(shift-1):0,map=new Map(),pal=[];let ok=true;
      const idx=new Uint8Array(px.length/4),q=v=>v&&shift?(v&mask)|half:v&mask;
      for(let i=0,j=0;i<px.length;i+=4,j++){
        const r=q(px[i]),g=q(px[i+1]),b=q(px[i+2]),key=r<<16|g<<8|b;
        let k=map.get(key);if(k===undefined){if(pal.length>=768){ok=false;break;}k=pal.length/3;map.set(key,k);pal.push(r,g,b);}idx[j]=k;
      }
      if(ok)return{idx,pal};
    }
    throw new Error("GIF quantize failed");
  }
  function write(f){
    const {x,y,w,h,px,delay}=f,{idx,pal}=quantize(px);
    let bitsPer=1;while((1<<bitsPer)<pal.length/3)bitsPer++;
    const tableLen=1<<bitsPer;
    str("!");bytes.push(0xf9,4,1<<2,delay&255,delay>>8&255,0,0);         // disposal 1 (leave in place), no transparency
    str(",");w16(x);w16(y);w16(w);w16(h);bytes.push(0x80|(bitsPer-1));
    for(let i=0;i<tableLen*3;i++)bytes.push(i<pal.length?pal[i]:0);
    const minCode=Math.max(2,bitsPer),data=lzw(idx,minCode);bytes.push(minCode);
    for(let i=0;i<data.length;i+=255){const n=Math.min(255,data.length-i);bytes.push(n);for(let k=0;k<n;k++)bytes.push(data[i+k]);}
    bytes.push(0);frames++;
  }
  return{
    // delay in hundredths of a second
    add(image,delay){
      const d=image.data;let x0=0,y0=0,x1=width-1,y1=height-1;
      if(prev){
        x0=width;y0=height;x1=-1;y1=-1;
        for(let y=0;y<height;y++)for(let x=0;x<width;x++){const i=(y*width+x)*4;
          if(d[i]!==prev[i]||d[i+1]!==prev[i+1]||d[i+2]!==prev[i+2]){if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}}
        if(x1<0){if(pending)pending.delay+=delay;return;}
      }
      if(pending)write(pending);
      const w=x1-x0+1,h=y1-y0+1,px=new Uint8ClampedArray(w*h*4);
      for(let y=0;y<h;y++)px.set(d.subarray(((y0+y)*width+x0)*4,((y0+y)*width+x0+w)*4),y*w*4);
      pending={x:x0,y:y0,w,h,px,delay};prev=new Uint8ClampedArray(d);
    },
    finish(){if(pending){write(pending);pending=null;}bytes.push(0x3b);return new Uint8Array(bytes);},
    get frames(){return frames+(pending?1:0);}
  };
}

const API={FRAME,PIVOT,isHumanoid,appearanceFor,weaponFor,basePose,attackClip,hitReaction,faceToward,faceIn,reactFacing,planBeats,clinchClips,pairSpots,
  PALETTES,GifEncoder,ready:false,handles:()=>false,attach(){},beginRound(){},playRound(){return null;},cancel(){},sync(){}};
root.AFSprites=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
if(typeof document==="undefined"||typeof window==="undefined"||typeof fetch!=="function")return;

/* ---------------- browser runtime ---------------- */
const DEF_URL="characters/male.json";
// the feet sit below a hex centre by 0.4 of the hex step (14 px at the old step 34, 8 at the step 20 of 2026-10-15)
const feet=()=>Math.round(((hooks&&hooks.hexStep&&hooks.hexStep())||34)*0.4);
const hexStep=()=>(hooks&&hooks.hexStep&&hooks.hexStep())||34;
const STEP_MS=260;          // walk time per hex
const KNOCK_MS=200,PROJECTILE_MS=230,PARRY_MS=520,BLOCK_MS=420,FADE_MS=420;
const RECAP_GAP_MS=450;     // pause between rounds of the post-fight recap
const STORE="af.sprites.animate";
let def=null,images=new Map(),hooks=null,canvas=null,ctx=null,groundC=null,gctx=null,groundDrawn="",groundImgDrawn=null,sprites=new Map(),frozen=false,playToken=0;
let battle=null,viewer=null,recap=false,recorder=null;
const projectiles=[];

function animateOn(){try{return localStorage.getItem(STORE)!=="0";}catch{return true;}}
function setAnimate(v){try{localStorage.setItem(STORE,v?"1":"0");}catch{/* private mode */}}

// a single-file build (build-standalone.js --rig) inlines the rig: AF_RIG = {def, files: {path: data URI}}
const INLINE=root.AF_RIG||null;
const srcOf=p=>INLINE&&INLINE.files&&INLINE.files[p]||p;
function img(path){
  if(!path)return null;let im=images.get(path);
  if(!im){im=new Image();im.decoding="async";im.src=srcOf(path);images.set(path,im);}
  return im.complete&&im.naturalWidth?im:null;
}
function preload(){
  const paths=new Set([def.contactShadow]);
  for(const st of Object.values(def.states)){
    for(const p of Object.values(st.layers))paths.add(p);
    for(const it of (st.weapons&&st.weapons.items)||[])for(const p of Object.values(it.layers))paths.add(p);
  }
  return Promise.all([...paths].map(p=>new Promise(res=>{const im=new Image();im.onload=im.onerror=()=>res();im.src=srcOf(p);images.set(p,im);})));
}

const load=(INLINE&&INLINE.def?Promise.resolve(INLINE.def):fetch(DEF_URL).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();}))
  .then(d=>{def=d;return preload();})
  .then(()=>{API.ready=true;API.handles=f=>isHumanoid(f);hooks&&hooks.rerender&&hooks.rerender();})
  .catch(()=>{API.ready=false;});

/* --- canvas over the SVG arena --- */
function ensureCanvas(){
  const svg=document.getElementById("arena");if(!svg)return false;
  if(canvas&&canvas.isConnected)return true;
  canvas=document.createElement("canvas");canvas.className="sprite-layer";canvas.setAttribute("aria-hidden","true");
  svg.insertAdjacentElement("afterend",canvas);ctx=canvas.getContext("2d");
  // the painted arena ground sits under the SVG grid, which draws over it faintly (af-props-v3.js ground)
  groundC=document.createElement("canvas");groundC.className="ground-layer";groundC.setAttribute("aria-hidden","true");
  svg.insertAdjacentElement("beforebegin",groundC);gctx=groundC.getContext("2d");groundDrawn="";
  if(!document.getElementById("af-sprite-style")){
    const st=document.createElement("style");st.id="af-sprite-style";
    st.textContent=".sprite-layer{position:absolute;pointer-events:none;image-rendering:pixelated;z-index:2}"
      +".ground-layer{position:absolute;pointer-events:none;image-rendering:pixelated;z-index:0;display:none}.props-on .ground-layer{display:block}"
      +".props-on .arena{position:relative;z-index:1}"
      +".arena text.token.sprited{opacity:0}.sprite-toggle{display:inline-flex;gap:5px;align-items:center;font-size:11px;color:var(--muted);cursor:pointer}";
    document.head.appendChild(st);
  }
  const bar=document.querySelector(".arena-wrap .toolbar");
  if(bar&&!bar.querySelector(".sprite-toggle")){
    const lab=document.createElement("label");lab.className="sprite-toggle";
    lab.innerHTML=`<input type="checkbox" id="spriteAnimate"${animateOn()?" checked":""}> Animate rounds`;
    lab.querySelector("input").addEventListener("change",e=>{setAnimate(e.target.checked);if(!e.target.checked)skip();});
    bar.appendChild(lab);
  }
  return true;
}
// map the SVG's viewBox onto the canvas (preserveAspectRatio xMidYMid meet), at device resolution
function layout(){
  const svg=document.getElementById("arena");if(!svg||!canvas)return null;
  const vb=svg.viewBox.baseVal,box=svg.getBoundingClientRect(),wrap=canvas.offsetParent||svg.parentElement,wb=wrap.getBoundingClientRect();
  if(!box.width||!box.height||!vb||!vb.width)return null;
  const dpr=window.devicePixelRatio||1;
  canvas.style.left=(box.left-wb.left+wrap.scrollLeft)+"px";canvas.style.top=(box.top-wb.top+wrap.scrollTop)+"px";
  canvas.style.width=box.width+"px";canvas.style.height=box.height+"px";
  const W=Math.round(box.width*dpr),H=Math.round(box.height*dpr);
  if(canvas.width!==W)canvas.width=W;if(canvas.height!==H)canvas.height=H;
  const s=Math.min(box.width/vb.width,box.height/vb.height)*dpr;
  const ox=(W-vb.width*s)/2-vb.x*s,oy=(H-vb.height*s)/2-vb.y*s;
  if(groundC){groundC.style.cssText=canvas.style.cssText;if(groundC.width!==W)groundC.width=W;if(groundC.height!==H)groundC.height=H;}
  return{s,ox,oy,vbW:vb.width,vbH:vb.height};
}

/* --- sprite state --- */
// in the recap the SVG tokens show the end of the fight, so glyph fighters (beasts, summons, the caravan) move on the canvas too
const drawn=f=>!!f&&(API.handles(f)||(recap&&!!f.glyph));
function spriteFor(f){
  let sp=sprites.get(f);
  if(!sp){const p=hooks.cellPx(f.cell);sp={f,x:p.x,y:p.y+feet(),facing:f.faction===(viewer&&viewer.faction)?"E":"W",anim:null,alpha:1,look:appearanceFor(f,viewer),visible:true,dead:false,glyph:API.handles(f)?null:f.glyph,pose:null};sprites.set(f,sp);}
  return sp;
}
function play(sp,state,clip,opts){
  const st=def.states[state];if(!st)return 0;
  sp.sink=0;
  const c=clip&&st.clips&&st.clips[clip]?st.clips[clip]:{frames:[...Array(st.frames).keys()],fps:st.fps};
  sp.anim={state,frames:c.frames,fps:c.fps||st.fps,loop:!!(opts&&opts.loop)||!!c.loop,hold:!!(opts&&opts.hold),t0:performance.now(),weapon:opts&&opts.weapon||null,motion:!(opts&&opts.loop),path:opts&&opts.path||null};
  return sp.anim.loop?0:c.frames.length*1000/sp.anim.fps;
}
function holdBase(sp){
  if(sp.dead&&canDown(sp)){goDown(sp);return;}
  if(!sp.glyph&&sp.f&&sp.f.drowning&&root.AF&&root.AF.alive(sp.f)&&root.AF.onWater&&root.AF.onWater(sp.f)){startDrown(sp);return;}
  if(sp.pair){play(sp,sp.pair.role==="holder"?"clinchHold":"clinchHeld",null,{loop:true});return;}
  const b=basePose(sp.pose||sp.f);play(sp,b.state,null,{loop:true,weapon:b.weapon});
}
// clinch pairing on the canvas (presentation only: the engine's relationship decides who is paired)
// h holds d; hp and dp are where each stands unpaired (their cells). Returns the paired spots.
function setPair(h,d,hp,dp){
  h.pair={other:d,role:"holder"};d.pair={other:h,role:"held"};
  h.home={x:hp.x,y:hp.y};d.home={x:dp.x,y:dp.y};
  const P=pairSpots(hp,dp);
  h.facing=P.holder.facing;d.facing=P.held.facing;
  return P;
}
// the engine's standing grapples drawn as clinched pairs (adjacent humanoids only: a ranged hold such as Shadow
// Possession or a chain snare stays apart); relOf/cellOf read the live fighter or a recap snapshot
function applyStaticPairs(relOf,cellOf){
  for(const sp of sprites.values()){sp.pair=null;sp.home=null;}
  for(const [f,sp] of sprites){
    const r=relOf(f);if(!r||r.role!=="Grappling"||sp.glyph||!sp.visible)continue;
    const o=sprites.get(r.partner);if(!o||o.glyph||!o.visible||o.pair)continue;
    const a=cellOf(f),b=cellOf(r.partner);if(!a||!b||!root.AF||root.AF.hdist(a,b)>1)continue;
    const P=setPair(sp,o,px(a),px(b));
    sp.x=P.holder.x;sp.y=P.holder.y;o.x=P.held.x;o.y=P.held.y;
    if(!sp.anim||sp.anim.loop)holdBase(sp);if(!o.anim||o.anim.loop)holdBase(o);
  }
}
function unpair(sp){const o=sp.pair&&sp.pair.other;sp.pair=null;if(o&&o.pair&&o.pair.other===sp)o.pair=null;}
const paired=(a,b)=>!!a.pair&&a.pair.other===b;
function frameOf(sp,now){
  const a=sp.anim;if(!a)return null;
  let i=Math.floor((now-a.t0)*a.fps/1000);
  if(a.loop)i%=a.frames.length;else if(i>=a.frames.length){if(a.hold)i=a.frames.length-1;else{holdBase(sp);return frameOf(sp,now);}}
  return{state:a.state,col:a.frames[i],i,weapon:a.weapon,motion:a.motion,path:a.path};
}
// cumulative root motion (pixels in frame space) up to the current frame of a one-shot clip
function rootOffset(st,facing,fr){
  const rm=st.rootMotion;if(!rm||!fr.motion)return[0,0];
  const list=Array.isArray(rm)?rm:rm[facing];if(!list)return[0,0];
  let x=0,y=0;for(let k=0;k<=fr.col&&k<list.length;k++){x+=list[k][0];y+=list[k][1];}
  return[x,y];
}

/* --- drawing --- */
// a sheet recoloured for one look (character creator): exact colours swapped on a copy, cached per sheet and palette
const tints=new Map();
function tinted(path,map){
  if(!map.__key)Object.defineProperty(map,"__key",{value:JSON.stringify(map)});const key=path+"|"+map.__key;let c=tints.get(key);if(c)return c;
  const im=img(path);if(!im)return null;
  c=document.createElement("canvas");c.width=im.naturalWidth;c.height=im.naturalHeight;
  const x=c.getContext("2d");x.drawImage(im,0,0);
  const id=x.getImageData(0,0,c.width,c.height),d=id.data,rgb={};
  for(const [k,v] of Object.entries(map))rgb[parseInt(k.slice(1),16)]=parseInt(v.slice(1),16);
  for(let i=0;i<d.length;i+=4){if(!d[i+3])continue;const n=d[i]<<16|d[i+1]<<8|d[i+2],t=rgb[n];if(t!==undefined){d[i]=t>>16&255;d[i+1]=t>>8&255;d[i+2]=t&255;}}
  x.putImageData(id,0,0);tints.set(key,c);return c;
}
function blit(path,col,row,size,dx,dy,map){const im=map?tinted(path,map):img(path);if(im)ctx.drawImage(im,col*size,row*size,size,size,dx,dy,size,size);}
function drawGlyph(sp){
  const cls=sp.f===viewer?"#2fe0ff":viewer&&sp.f.faction===viewer.faction?"#5fe08a":"#ff5d6c";
  ctx.globalAlpha=sp.alpha;ctx.font=Math.round(hexStep()*0.75)+"px system-ui,'Segoe UI Emoji','Apple Color Emoji',sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.shadowColor=cls;ctx.shadowBlur=8;ctx.fillText(sp.glyph,sp.x,sp.y-feet());ctx.shadowBlur=0;ctx.globalAlpha=1;
}
// a path clip (a throw) carries the fighter from path.from to path.to in step with the clip's authored root motion,
// so the art's flight timing lands it on the engine's cell
function pathOffset(st,sp,fr){
  const p=fr.path,[rx,ry]=rootOffset(st,sp.facing,fr);
  if(!p)return[sp.x+rx,sp.y+ry];
  const k=p.total?Math.max(0,Math.min(1,rx/p.total)):0;
  return[p.from.x+(p.to.x-p.from.x)*k,p.from.y+(p.to.y-p.from.y)*k];
}
// parts: "far" (the far arm), "body" (everything but the near arm when paired), "arms" (the near arm, paired only),
// "fx"; unpaired fighters draw "far", "body" (with the arms in slot order) and "fx" together
function drawSprite(sp,now,part){
  if(sp.glyph){if(recap&&(!part||part==="body"))drawGlyph(sp);return;}
  const fr=frameOf(sp,now);if(!fr)return;
  const st=def.states[fr.state];let row=st.rows.indexOf(sp.facing);if(row<0)row=0;
  const [ax,ay0]=pathOffset(st,sp,fr),sink=sp.sink||0,ay=ay0+sink;
  const x=Math.round(ax-PIVOT[0]),y=Math.round(ay-PIVOT[1]);
  if(sink){ctx.save();ctx.beginPath();ctx.rect(Math.round(ax)-80,Math.round(ay0)-140,160,140-2);ctx.clip();}
  const isPair=!!part,want=k=>!part||part===k;
  const outfit=def.outfits[sp.look.outfit]||def.outfits.gi;
  const pick={body:"body",arms:"arms",clothing:outfit.clothing,armAccessories:outfit.armAccessories,hair:sp.look.hair,eyes:sp.look.eyes};
  const items=[];
  if(fr.weapon&&st.weapons)for(const it of st.weapons.items){if(it.item===fr.weapon&&!items.some(x=>x.slot===it.slot))items.push(it);}
  const weapon=depth=>{for(const it of items)if(it.layers[depth])blit(it.layers[depth],fr.col,row,128,x-32,y-32);};
  ctx.globalAlpha=sp.alpha;
  const pal=layer=>paletteFor(layer,sp.look);
  if(want("far")&&st.layers["far-arm"])blit(st.layers["far-arm"],fr.col,row,FRAME,x,y,pal("far-arm"));
  if(want("body")){
    if(!sink)blit(def.contactShadow,def.referenceFrameOrder.indexOf(sp.facing),0,FRAME,Math.round(ax-PIVOT[0]),Math.round(ay-PIVOT[1]));
    WDEPTH_UNDER.forEach(weapon);
    for(const {slot} of def.slots){
      if(slot==="arms"){weapon("front");if(isPair)continue;}
      const layer=pick[slot];if(layer&&st.layers[layer])blit(st.layers[layer],fr.col,row,FRAME,x,y,pal(layer));
    }
    WDEPTH_OVER.forEach(weapon);
  }
  if(want("arms")&&isPair&&st.layers.arms)blit(st.layers.arms,fr.col,row,FRAME,x,y,pal("arms"));
  const fx=st.layers["impact-fx"]||st.layers.fx;
  if(want("fx")&&fx&&!sink)blit(fx,fr.col,row,FRAME,x,y);
  ctx.globalAlpha=1;
  if(sink){ctx.restore();foamRing(Math.round(ax),Math.round(ay0)-2,now);}
}
// a pixel ring of foam where a drowning fighter meets the water
function foamRing(cx,cy,now){
  const r=11+((Math.floor(now/220))%2),ry=3;ctx.fillStyle="#a8d8ec";
  for(let a=0;a<64;a++){const t=a/64*Math.PI*2,px=Math.round(cx+Math.cos(t)*r),py=Math.round(cy+Math.sin(t)*ry);if((a+Math.floor(now/160))%5===0)continue;ctx.fillRect(px,py,1,1);}
  ctx.fillStyle="#ffffff";for(const k of[0,1,2]){const t=(now/700+k*2.1)%(Math.PI*2);ctx.fillRect(Math.round(cx+Math.cos(t)*(r-3)),Math.round(cy+Math.sin(t)*ry)-1,1,1);}
}
// a clinched pair, back to front (approved layering): holder far arm, held far arm, holder body, held body, held
// near arm, holder near arm, then the impact FX
function drawPair(h,d,now){
  drawSprite(h,now,"far");drawSprite(d,now,"far");drawSprite(h,now,"body");drawSprite(d,now,"body");
  drawSprite(d,now,"arms");drawSprite(h,now,"arms");drawSprite(d,now,"fx");drawSprite(h,now,"fx");
}
// every fighter and projectile, back to front, onto ctx (its transform already maps viewBox units)
// environment props (af-props-v3.js): ground pieces under everything, standing props depth sorted with the fighters
// and drawn see-through while a fighter stands behind one
let terrain=null;
function propScene(){const P=root.AFProps;return terrain&&P&&P.ready?P.scene(terrain,feet()):null;}
function drawScene(now){
  const list=[...sprites.values()].filter(sp=>sp.visible&&sp.alpha>0).sort((a,b)=>a.y-b.y);
  const done=new Set(),P=root.AFProps,env=propScene();
  if(env){for(const it of env.flat)P.draw(ctx,it,now);for(const it of env.stand)P.drawShadow(ctx,it);}
  const order=env?[...env.stand.map(it=>({prop:it,y:it.y-0.5})),...list.map(sp=>({sp,y:sp.y}))].sort((a,b)=>a.y-b.y):list.map(sp=>({sp}));
  for(const e of order){
    if(e.prop){const b=P.box(e.prop),behind=list.some(sp=>!sp.glyph&&sp.y<e.prop.y&&sp.x+7>b.x0&&sp.x-7<b.x1&&sp.y>b.y0+6&&sp.y-44<b.y1);
      P.draw(ctx,e.prop,now,behind?0.45:1);continue;}
    const sp=e.sp;
    if(done.has(sp))continue;
    const o=sp.pair&&sp.pair.other;
    if(o&&o.pair&&o.pair.other===sp&&o.visible&&o.alpha>0&&!sp.glyph&&!o.glyph){
      const h=sp.pair.role==="holder"?sp:o,d=h===sp?o:sp;drawPair(h,d,now);done.add(o);
    }else drawSprite(sp,now);
    done.add(sp);
  }
  for(const p of projectiles){
    const t=Math.min(1,(now-p.t0)/PROJECTILE_MS),px=p.a.x+(p.b.x-p.a.x)*t,py=p.a.y+(p.b.y-p.a.y)*t-30;
    ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(px,py,3.5,0,Math.PI*2);ctx.fill();
  }
}
function frame(now){
  requestAnimationFrame(frame);
  if(recorder)recorder.tick(now);
  if(!API.ready||!canvas||!canvas.isConnected||!canvas.offsetParent)return;
  const L=layout();if(!L)return;
  ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.setTransform(L.s,0,0,L.s,L.ox,L.oy);ctx.imageSmoothingEnabled=false;
  drawGround(L);
  drawScene(now);
}
// the ground canvas only repaints when the arena, its size or the ground image changes
function arenaGround(vbW,vbH){const P=root.AFProps;if(!terrain||!P||!P.ground||!propScene())return null;return P.ground(terrain,hexStep(),Math.round(vbW),Math.round(vbH));}
function paintBackdrop(c,vbW,vbH){const g=c.createRadialGradient(vbW/2,vbH/2,0,vbW/2,vbH/2,Math.max(vbW,vbH)*0.72);g.addColorStop(0,"#121a32");g.addColorStop(1,"#070b17");c.fillStyle=g;c.fillRect(0,0,vbW,vbH);}
function drawGround(L){
  if(!gctx)return;const img=arenaGround(L.vbW,L.vbH),key=img?[groundC.width,groundC.height,L.s,L.ox,L.oy].join("|"):"";
  if(key===groundDrawn&&img===groundImgDrawn)return;groundDrawn=key;groundImgDrawn=img;
  gctx.setTransform(1,0,0,1,0,0);gctx.clearRect(0,0,groundC.width,groundC.height);if(!img)return;
  gctx.setTransform(L.s,0,0,L.s,L.ox,L.oy);gctx.imageSmoothingEnabled=false;paintBackdrop(gctx,L.vbW,L.vbH);gctx.drawImage(img,0,0);
}
// the grid hides while a round or the recap plays (user, 2026-10-15) and comes back for planning
function gridOff(on){const w=canvas&&canvas.parentElement;if(w)w.classList.toggle("grid-off",!!on);}
// draws onto another context (the recorder, the character-creator preview) with the same routines
function withCtx(other,fn){const keep=ctx;ctx=other;try{fn();}finally{ctx=keep;}}
requestAnimationFrame(frame);

/* --- replay --- */
const wait=ms=>new Promise(r=>setTimeout(r,ms));
function tween(sp,to,ms,token){
  const from={x:sp.x,y:sp.y},t0=performance.now();
  return new Promise(res=>{
    const step=()=>{if(token!==playToken)return res();const t=Math.min(1,(performance.now()-t0)/ms);
      sp.x=from.x+(to.x-from.x)*t;sp.y=from.y+(to.y-from.y)*t;if(t<1)requestAnimationFrame(step);else res();};
    step();
  });
}
const px=c=>{const p=hooks.cellPx(c);return{x:p.x,y:p.y+feet()};};
function hexes(a,b){return root.AF?Math.max(1,root.AF.hdist(a,b)):1;}
// drowning (user, 2026-10-15): a fighter out of chakra on water sinks to the waist and flails, arms up over the head.
// Built from the approved guard-break frames (arms flung up), whole-pixel sunk and cut off at the waterline, with a ring
// of foam round the body; no new body pixels.
const DROWN_SINK=22,DROWN_FRAMES=[0,1,2,1],DROWN_FPS=5,DROWN_MS=1600;
function startDrown(sp){
  if(sp.anim&&sp.anim.drown){sp.sink=DROWN_SINK;return;}
  play(sp,"guardBreak",null,{loop:true});
  sp.anim.frames=DROWN_FRAMES;sp.anim.fps=DROWN_FPS;sp.anim.motion=false;sp.anim.drown=true;sp.sink=DROWN_SINK;
  if(def.states.guardBreak.rows.includes("S"))sp.facing="S";   // face the viewer: both arms show above the water
}
async function drown(e,token){
  if(!drawn(e.who))return;const sp=spriteFor(e.who);if(sp.glyph)return;
  startDrown(sp);await wait(DROWN_MS);if(token!==playToken)return;
  if(e.killed){sp.sink=0;sp.anim=null;goDown(sp);}
}
// defeated humanoids stay on the field lying in the downed state (user 2026-10-15: "a downed stance for when players
// are defeated instead of them disappearing ... similar to the prone stance but with the eyes closed"); glyph fighters
// (beasts, summons) still fade out
const canDown=sp=>!!(sp&&!sp.glyph&&def&&def.states.downed);
function goDown(sp){
  sp.dead=true;sp.alpha=1;sp.pair=null;
  if(sp.anim&&sp.anim.state==="downed")return;
  const rows=def.states.downed.rows;
  if(!rows.includes(sp.facing)){const foe=foeOf(sp);sp.facing=foe?(foe.x>=sp.x?"E":"W"):(sp.facing==="W"?"W":"E");}
  play(sp,"downed",null,{loop:true});
}
async function fadeOut(sp,token){
  if(canDown(sp)){goDown(sp);return;}
  sp.dead=true;const t0=performance.now();
  while(token===playToken&&sp.alpha>0){await wait(16);sp.alpha=Math.max(0,1-(performance.now()-t0)/FADE_MS);}
}
async function walk(e,token){
  if(!drawn(e.who))return;const sp=spriteFor(e.who),to=px(e.to);
  sp.facing=faceToward(sp,to,sp.facing);play(sp,"walk",null,{loop:true});
  await tween(sp,to,STEP_MS*hexes(e.from,e.to),token);holdBase(sp);
}
function glide(sp,to,ms,token){return tween(sp,to,ms,token);}
const GLIDE_MS=160;
async function react(e,token){
  if(e.type==="grapple"){
    if(!API.handles(e.who)||!API.handles(e.target))return;
    const h=spriteFor(e.who),d=spriteFor(e.target);
    if(Math.hypot(h.x-d.x,h.y-d.y)>hexStep()*2.2)return;          // not adjacent: a ranged hold stays apart
    const P=setPair(h,d,{x:h.x,y:h.y},{x:d.x,y:d.y});holdBase(h);holdBase(d);
    await Promise.all([glide(h,P.holder,GLIDE_MS,token),glide(d,P.held,GLIDE_MS,token)]);return;
  }
  if(e.type==="release"){
    const a=drawn(e.who)?spriteFor(e.who):null,b=drawn(e.partner)?spriteFor(e.partner):null;
    if(!a||!b||!paired(a,b))return;
    unpair(a);holdBase(a);holdBase(b);
    await Promise.all([a.home&&glide(a,a.home,GLIDE_MS,token),b.home&&glide(b,b.home,GLIDE_MS,token)]);return;
  }
  if(!drawn(e.who)){return;}
  const sp=spriteFor(e.who),by=e.by&&drawn(e.by)?spriteFor(e.by):(e.by?px(e.by.cell):sp);
  if(e.type==="knock"){await tween(sp,px(e.to),KNOCK_MS,token);return;}
  if(sp.glyph){if(e.type==="hit"&&e.killed)await fadeOut(sp,token);else await wait(BLOCK_MS);return;}
  sp.facing=faceToward(sp,by,sp.facing);
  if(e.type==="evade"){await wait(play(sp,"weave","weave"));return;}
  if(e.type==="parry"){play(sp,"block","block",{loop:true});await wait(PARRY_MS);holdBase(sp);return;}
  if(e.type==="hit"){
    const state=hitReaction(e);
    if(state==="block"){play(sp,"block","block",{loop:true});await wait(BLOCK_MS);holdBase(sp);return;}
    sp.facing=reactFacing(state,sp.facing,sp,by,def);
    const ms=play(sp,state,state,{hold:!!e.killed});
    if(e.killed){await wait(ms*0.7);await fadeOut(sp,token);return;}
    await wait(ms);
  }
}
async function act(beat,counters,token){
  const e=beat.act;if(!e)return;
  const ab=e.ab,who=e.who,clip=attackClip(who,ab,counters);
  const target=e.target||beat.reactions.find(r=>r.by===who)?.who||null;
  const aim=target?(drawn(target)?spriteFor(target):px(target.cell)):(e.point?px(e.point):null);
  if(!API.handles(who)){                 // a glyph attacker: its targets still react
    await Promise.all(beat.reactions.map(r=>react(r,token)));return;
  }
  const sp=spriteFor(who);
  if(target)sp.lastTarget=target;
  if(target&&sp.pair&&sp.pair.other.f===target){
    const cc=clinchClips(sp.pair.role==="holder"?"Grappling":"Grappled",ab);
    if(cc){await clinchAct(beat,sp,sp.pair.other,cc,ab,token);return;}
  }
  if(aim)sp.facing=faceToward(sp,aim,sp.facing);
  if(!clip){await Promise.all(beat.reactions.map(r=>react(r,token)));return;}   // stances, buffs, heals
  if(clip.kind==="cast"){
    if(aim){projectiles.push({a:{x:sp.x,y:sp.y},b:{x:aim.x,y:aim.y},t0:performance.now(),color:ab.dmg==="Chakra"||ab.dmg==="Magical"?"#7fd7ff":"#f5d17f"});
      await wait(PROJECTILE_MS);projectiles.shift();}
    await Promise.all(beat.reactions.map(r=>react(r,token)));return;
  }
  // every clip but the last plays through; the reactions start on the last clip's strike frame
  for(let i=0;i<clip.seq.length-1;i++){await wait(play(sp,clip.seq[i].state,clip.seq[i].clip,{weapon:clip.weapon}));if(token!==playToken)return;}
  const last=clip.seq[clip.seq.length-1];
  const ms=play(sp,last.state,last.clip,{weapon:clip.weapon});
  await wait(ms*0.55);
  await Promise.all([wait(ms*0.45),...beat.reactions.map(r=>react(r,token))]);
}
// Auto-facing (user, 2026-10-15): a fighter at rest turns to whoever it is fighting. Its focus is the page's chosen
// target for that fighter (the player's main target), else its clinch partner, else the nearest drawn opponent. Paired,
// prone, dead and mid-clip fighters keep their facing.
function foeOf(sp){
  for(const t of [hooks&&hooks.focusOf?hooks.focusOf(sp.f):null,sp.lastTarget]){
    const o=t&&sprites.get(t);if(o&&!o.dead&&o.alpha>0&&o.visible&&o!==sp)return o;
  }
  let best=null,bd=Infinity;
  for(const x of sprites.values()){
    if(x===sp||x.dead||x.alpha<=0||!x.visible||!x.f||x.f.faction===sp.f.faction)continue;
    const d=Math.hypot(x.x-sp.x,x.y-sp.y);if(d<bd){bd=d;best=x;}
  }
  return best;
}
function faceFoes(){
  if(!def)return;
  for(const sp of sprites.values()){
    if(sp.glyph||sp.dead||sp.pair||!sp.f)continue;
    const a=sp.anim;if(a&&(!a.loop||a.state==="prone"||a.drown))continue;
    const o=foeOf(sp);if(!o)continue;
    const st=def.states[a?a.state:"guard"];sp.facing=faceIn(st&&st.rows,sp,o,sp.facing);
  }
}
function rootTotal(state,facing){const rm=def.states[state].rootMotion,l=rm&&(Array.isArray(rm)?rm:rm[facing])||[];return l.reduce((a,v)=>a+v[0],0);}
// a clinch move: the actor's clip and the partner's paired reaction on the same frames. A landed throw carries the
// thrown fighter to the engine's landing cell along the clip's flight, then it lies prone for the clip's holdSeconds
// (1.5 s, user 2026-10-15) and kips up, turning to face the thrower; the thrower ends turned toward it.
async function clinchAct(beat,sp,o,cc,ab,token){
  const hit=beat.reactions.find(r=>r.type==="hit"&&r.who===o.f&&r.by===sp.f);
  const knock=beat.reactions.find(r=>r.type==="knock"&&r.who===o.f);
  const own=r=>r===hit||r===knock||r.type==="release"&&(r.who===sp.f||r.who===o.f)||(r.type==="evade"||r.type==="parry")&&r.who===o.f;
  const rest=beat.reactions.filter(r=>!own(r));
  if(THROWS.has(ab.name)){
    if(!hit){await wait(BLOCK_MS);await Promise.all(rest.map(r=>react(r,token)));return;}   // missed or denied: the hold stays
    // the thrower plays the holder's side of the pair
    let h=sp,d=o;
    if(sp.pair.role!=="holder"){const hh=sp.home||{x:sp.x,y:sp.y},dh=o.home||{x:o.x,y:o.y},P=setPair(sp,o,hh,dh);sp.x=P.holder.x;sp.y=P.holder.y;o.x=P.held.x;o.y=P.held.y;}
    const hHome=h.home||{x:h.x,y:h.y},dest=knock?px(knock.to):(d.home||{x:d.x,y:d.y});
    const hTot=rootTotal(cc[0],h.facing),dTot=rootTotal(cc[1],d.facing);
    const hFrom={x:h.x,y:h.y},dFrom={x:d.x,y:d.y};
    const msH=play(h,cc[0],cc[0],{hold:true,path:{from:hFrom,to:hHome,total:hTot}});
    const msD=play(d,cc[1],cc[1],{hold:true,path:{from:dFrom,to:dest,total:dTot}});
    await wait(Math.max(msH,msD));if(token!==playToken)return;
    unpair(h);
    if(hTot){h.x=hHome.x;h.y=hHome.y;}
    h.facing=faceIn(def.states.guard.rows,hHome,dest,h.facing);holdBase(h);glide(h,hHome,GLIDE_MS,token);
    d.x=dest.x;d.y=dest.y;
    const restDone=Promise.all(rest.map(r=>react(r,token)));
    if(hit.killed){play(d,"prone",null,{loop:true});await fadeOut(d,token);await restDone;return;}
    const pr=def.states.prone,hold=(pr.clips&&pr.clips.prone&&pr.clips.prone.holdSeconds||1.5)*1000;
    play(d,"prone",null,{loop:true});await wait(hold);if(token!==playToken)return;
    await wait(play(d,"getUp","getUp",{hold:true}));if(token!==playToken)return;
    d.facing=faceToward(d,h,d.facing);holdBase(d);
    await restDone;return;
  }
  const ms=play(sp,cc[0],cc[0]);
  if(hit&&!hit.killed)play(o,cc[1],cc[1]);
  await wait(ms*0.55);
  const after=[];
  if(hit&&hit.killed){unpair(sp);holdBase(sp);after.push(react(hit,token));}
  await Promise.all([wait(ms*0.45),...after,...rest.map(r=>react(r,token))]);
  for(const r of beat.reactions)if(r.type==="release"&&(r.who===sp.f||r.who===o.f))await react(r,token);
}
async function replay(events,token){
  const counters=new Map();
  for(const beat of planBeats(events)){
    if(token!==playToken)return;
    if(beat.moves){await Promise.all(beat.moves.map(m=>walk(m,token)));continue;}
    if(beat.drown){await Promise.all(beat.drown.map(e=>drown(e,token)));continue;}
    for(const m of beat.approach)await walk(m,token);
    await act(beat,counters,token);
    if(token===playToken)faceFoes();
  }
}
function settle(){
  frozen=false;recap=false;gridOff(false);
  for(const [f,sp] of sprites)if(sp.glyph)sprites.delete(f);
  for(const sp of sprites.values()){sp.pose=null;sp.pair=null;}
  if(hooks&&hooks.onRecap)hooks.onRecap(null);
  for(const [f,sp] of sprites){
    if(!root.AF||!root.AF.alive(f)){if(canDown(sp)){const p=px(f.cell);sp.x=p.x;sp.y=p.y;goDown(sp);}else sprites.delete(f);continue;}
    const p=px(f.cell);sp.x=p.x;sp.y=p.y;sp.alpha=1;holdBase(sp);
  }
  API.sync(battle,viewer);
  faceFoes();
}
function skip(){playToken++;projectiles.length=0;settle();}

API.attach=function(h){hooks=h;};
API.cancel=function(){if(frozen)skip();};
API.beginRound=function(){if(API.ready&&animateOn()&&ensureCanvas()){frozen=true;gridOff(true);}};
API.playRound=function(B){
  if(!frozen||!API.ready){frozen=false;return Promise.resolve();}
  const token=++playToken;
  return replay(B.events||[],token).catch(e=>console.error(e)).then(()=>{if(token===playToken)settle();});
};
// called after every arena render: keeps one sprite per visible humanoid, at its cell unless a replay holds it
API.sync=function(B,player){
  battle=B;viewer=player;
  if(recap)return;                       // the recap places everyone itself
  if(!API.ready||!B||!hooks||!ensureCanvas())return;
  const seen=new Set();
  for(const f of B.all){
    if(!API.handles(f))continue;
    const alive=root.AF.alive(f);
    if(!alive&&!(frozen&&sprites.has(f))&&!def.states.downed)continue;
    const sp=spriteFor(f);seen.add(f);
    sp.visible=!player||!root.AFUI||!alive||root.AFUI.canRenderFighter(B,player,f);
    if(!alive&&!frozen){const p=px(f.cell);sp.x=p.x;sp.y=p.y;sp.pair=null;goDown(sp);continue;}
    if(!frozen){const p=px(f.cell);sp.x=p.x;sp.y=p.y;sp.pair=null;if(!sp.anim||sp.anim.loop)holdBase(sp);}
  }
  for(const f of [...sprites.keys()])if(!seen.has(f))sprites.delete(f);
  if(!frozen){applyStaticPairs(f=>root.AF.alive(f)?f.rel:null,f=>f.cell);faceFoes();}
};
// the post-fight recap: every round of B.history replayed in order at normal speed, each from where
// the fighters stood as it began. Resolves true when it played to the end, false when skipped.
API.playRecap=function(B,player){
  const rounds=(B&&B.history||[]).filter(h=>h.events.length);
  if(!API.ready||!rounds.length||!hooks||!ensureCanvas())return Promise.resolve(false);
  battle=B;viewer=player||viewer;
  const token=++playToken;projectiles.length=0;frozen=true;recap=true;sprites.clear();gridOff(true);
  const place=h=>{
    const keep=new Set();
    for(const s of h.start){
      if(!drawn(s.f)||(!s.alive&&!(API.handles(s.f)&&def.states.downed)))continue;keep.add(s.f);
      const sp=spriteFor(s.f),p=px(s.cell);
      sp.x=p.x;sp.y=p.y;sp.alpha=1;sp.dead=false;sp.pose={stam:s.stam,activeWeapon:s.activeWeapon};
      sp.visible=true;                   // the fight is over: the recap shows everyone
      if(!s.alive){sp.pair=null;goDown(sp);continue;}
      holdBase(sp);
    }
    for(const f of [...sprites.keys()])if(!keep.has(f))sprites.delete(f);
    const snap=new Map(h.start.map(s=>[s.f,s]));
    applyStaticPairs(f=>snap.get(f)&&snap.get(f).alive?snap.get(f).rel:null,f=>snap.get(f)&&snap.get(f).cell);
    faceFoes();
  };
  return (async()=>{
    for(let i=0;i<rounds.length;i++){
      if(token!==playToken)return false;
      place(rounds[i]);if(hooks.onRecap)hooks.onRecap({round:rounds[i].round,index:i+1,total:rounds.length});
      await wait(RECAP_GAP_MS);if(token!==playToken)return false;
      await replay(rounds[i].events,token);
    }
    if(token!==playToken)return false;
    await wait(RECAP_GAP_MS);return token===playToken;
  })().catch(e=>{console.error(e);return false;}).then(done=>{if(token===playToken)settle();return done;});
};
/* --- recap export (user, 2026-10-15): the recap recorded as a video and a GIF ---
   The board is redrawn on the recording canvas from the grid (hooks.board(): hex centres, terrain kind and glyph),
   then the sprites through the same drawing routines. Video: MediaRecorder at 2x (WebM, or MP4 where WebM is not
   offered). GIF: 10 fps at 1x, encoded frame by frame while the recap plays. */
const REC_SCALE=2,GIF_MS=100;
const TERRAIN_STYLE={open:["#10182d","#293457"],hard:["#41272a","#ffac66"],soft:["#30213d","#9e68b7"],fell:["#33291a","#b98a4a"],hazard:["#3d1620","#e0475e"]};
function videoType(){
  if(typeof MediaRecorder==="undefined"||!MediaRecorder.isTypeSupported)return null;
  for(const t of["video/webm;codecs=vp9","video/webm;codecs=vp8","video/webm","video/mp4;codecs=avc1","video/mp4"])if(MediaRecorder.isTypeSupported(t))return t;
  return null;
}
function drawBoard(c,b){
  const s=b.hexStep-1,g=c.createRadialGradient(b.vbW/2,b.vbH/2,0,b.vbW/2,b.vbH/2,Math.max(b.vbW,b.vbH)*0.72);
  g.addColorStop(0,"#121a32");g.addColorStop(1,"#070b17");c.fillStyle=g;c.fillRect(0,0,b.vbW,b.vbH);
  c.lineWidth=0.8;c.textAlign="center";c.textBaseline="middle";c.font=Math.round(b.hexStep*0.48)+"px system-ui,'Segoe UI Emoji','Apple Color Emoji',sans-serif";
  for(const cell of b.cells){
    const [fill,stroke]=TERRAIN_STYLE[cell.kind]||TERRAIN_STYLE.open;
    c.beginPath();for(let i=0;i<6;i++){const a=(60*i-30)*Math.PI/180,x=cell.x+s*Math.cos(a),y=cell.y+s*Math.sin(a);i?c.lineTo(x,y):c.moveTo(x,y);}c.closePath();
    c.fillStyle=fill;c.fill();c.strokeStyle=stroke;c.stroke();
    if(cell.glyph&&!propScene()){c.fillStyle="#fff";c.fillText(cell.glyph,cell.x,cell.y);}
  }
}
// the page hands over every cell [{x,y,t}] whenever it redraws the arena; the SVG glyphs hide while props draw
API.setTerrain=function(cells){terrain=cells||null;const on=!!(API.ready&&propScene()),w=canvas&&canvas.parentElement;if(w)w.classList.toggle("props-on",on);};
API.canRecord=()=>API.ready;API.videoType=videoType;
// plays the recap while recording it; resolves {video:{blob,ext}|null, gif:Blob|null, complete}
API.recordRecap=function(B,player,opt={}){
  if(!API.ready||!hooks||!hooks.board)return Promise.resolve(null);
  const b=hooks.board();if(!b)return Promise.resolve(null);
  const W=b.vbW*REC_SCALE,H=b.vbH*REC_SCALE;
  const boardC=document.createElement("canvas");boardC.width=b.vbW;boardC.height=b.vbH;
  {const bc=boardC.getContext("2d"),img=arenaGround(b.vbW,b.vbH);if(img){paintBackdrop(bc,b.vbW,b.vbH);bc.drawImage(img,0,0);}else drawBoard(bc,b);}
  const rec=document.createElement("canvas");rec.width=W;rec.height=H;const rc=rec.getContext("2d");
  const small=document.createElement("canvas");small.width=b.vbW;small.height=b.vbH;const sc=small.getContext("2d",{willReadFrequently:true});
  let label="";
  const paint=now=>{
    rc.setTransform(1,0,0,1,0,0);rc.imageSmoothingEnabled=false;rc.drawImage(boardC,0,0,W,H);
    rc.setTransform(REC_SCALE,0,0,REC_SCALE,0,0);withCtx(rc,()=>drawScene(now));
    rc.setTransform(1,0,0,1,0,0);
    if(label){rc.font="bold 22px system-ui,sans-serif";rc.textAlign="left";rc.textBaseline="top";rc.fillStyle="#000a";rc.fillRect(12,12,rc.measureText(label).width+20,34);rc.fillStyle="#ffd166";rc.fillText(label,22,18);}
  };
  const type=opt.video===false?null:videoType();
  let mr=null;const chunks=[];
  if(type&&rec.captureStream){try{mr=new MediaRecorder(rec.captureStream(30),{mimeType:type,videoBitsPerSecond:6e6});mr.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};}catch(e){mr=null;}}
  const gif=opt.gif===false?null:GifEncoder(b.vbW,b.vbH);let lastGif=-Infinity;
  const prevOnRecap=hooks.onRecap;
  hooks.onRecap=p=>{label=p?`Round ${p.round}`:"";if(prevOnRecap)prevOnRecap(p?{...p,recording:true}:null);};
  paint(performance.now());
  recorder={tick(now){
    paint(now);
    if(gif&&now-lastGif>=GIF_MS){lastGif=now;sc.imageSmoothingEnabled=false;sc.drawImage(rec,0,0,b.vbW,b.vbH);gif.add(sc.getImageData(0,0,b.vbW,b.vbH),GIF_MS/10);}
  }};
  if(mr)mr.start(250);
  return API.playRecap(B,player).then(complete=>{
    recorder=null;hooks.onRecap=prevOnRecap;
    const stopped=mr?new Promise(res=>{mr.onstop=res;mr.stop();}):Promise.resolve();
    return stopped.then(()=>({complete,
      video:mr&&chunks.length?{blob:new Blob(chunks,{type:type.split(";")[0]}),ext:type.includes("mp4")?"mp4":"webm"}:null,
      gif:gif&&gif.frames?new Blob([gif.finish()],{type:"image/gif"}):null}));
  }).catch(e=>{recorder=null;hooks.onRecap=prevOnRecap;console.error(e);return null;});
};
/* --- character-creator preview: a look drawn standing (or walking) in each of the four facings --- */
API.drawLook=function(c2d,look,opt={}){
  if(!API.ready)return false;
  const state=opt.state||"guard",now=opt.now||performance.now(),scale=opt.scale||2,facings=opt.facings||["S","E","N","W"];
  c2d.setTransform(1,0,0,1,0,0);c2d.clearRect(0,0,c2d.canvas.width,c2d.canvas.height);c2d.imageSmoothingEnabled=false;
  facings.forEach((facing,i)=>{
    const sp={f:null,x:32,y:63,facing,alpha:1,look,visible:true,glyph:null,pose:{stam:1}};
    sp.anim={state,frames:[...Array(def.states[state].frames).keys()],fps:def.states[state].fps,loop:true,t0:0,motion:false};
    c2d.setTransform(scale,0,0,scale,i*64*scale,0);withCtx(c2d,()=>drawSprite(sp,now));
  });
  c2d.setTransform(1,0,0,1,0,0);return true;
};
API.skip=function(){if(frozen)skip();};
API.animateOn=animateOn;
API.whenReady=()=>load;
API.debug=()=>({ready:API.ready,sprites:[...sprites.values()].map(sp=>({name:sp.f.name,x:Math.round(sp.x),y:Math.round(sp.y),facing:sp.facing,state:sp.anim&&sp.anim.state,visible:sp.visible,alpha:sp.alpha})),frozen,playing:playToken});
})(typeof globalThis!=="undefined"?globalThis:this);
