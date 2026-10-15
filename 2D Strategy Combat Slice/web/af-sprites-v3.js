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
// outfit by side: the player in the gi, allies in blue armour, opponents in red; hair and eyes vary by name
function appearanceFor(f,player){
  const side=f===player?"gi":player&&f.faction===player.faction?"blueArmor":"redArmor";
  const h=hash(f.name);
  return{outfit:side,hair:f===player?"long-hair":HAIRS[h%HAIRS.length],eyes:EYES[(h>>>3)%EYES.length]};
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
    if(e.type==="move"&&e.phase==="action"){if(cur&&!cur.act)cur.approach.push(e);else{cur={approach:[e],act:null,reactions:[]};beats.push(cur);}continue;}
    if(e.type==="act"){if(cur&&!cur.act&&cur.approach.length)cur.act=e;else{cur={approach:[],act:e,reactions:[]};beats.push(cur);}continue;}
    if(!cur){cur={approach:[],act:null,reactions:[]};beats.push(cur);}
    cur.reactions.push(e);
  }
  if(moves.length)beats.unshift({moves});
  return beats;
}

const API={FRAME,PIVOT,isHumanoid,appearanceFor,weaponFor,basePose,attackClip,hitReaction,faceToward,reactFacing,planBeats,clinchClips,pairSpots,
  ready:false,handles:()=>false,attach(){},beginRound(){},playRound(){return null;},cancel(){},sync(){}};
root.AFSprites=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
if(typeof document==="undefined"||typeof window==="undefined"||typeof fetch!=="function")return;

/* ---------------- browser runtime ---------------- */
const DEF_URL="characters/male.json";
const FEET=14;              // the feet sit this far below a hex centre
const STEP_MS=260;          // walk time per hex
const KNOCK_MS=200,PROJECTILE_MS=230,PARRY_MS=520,BLOCK_MS=420,FADE_MS=420;
const RECAP_GAP_MS=450;     // pause between rounds of the post-fight recap
const STORE="af.sprites.animate";
let def=null,images=new Map(),hooks=null,canvas=null,ctx=null,sprites=new Map(),frozen=false,playToken=0;
let battle=null,viewer=null,recap=false;
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
  if(!document.getElementById("af-sprite-style")){
    const st=document.createElement("style");st.id="af-sprite-style";
    st.textContent=".sprite-layer{position:absolute;pointer-events:none;image-rendering:pixelated;z-index:2}"
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
  return{s,ox,oy};
}

/* --- sprite state --- */
// in the recap the SVG tokens show the end of the fight, so glyph fighters (beasts, summons, the caravan) move on the canvas too
const drawn=f=>!!f&&(API.handles(f)||(recap&&!!f.glyph));
function spriteFor(f){
  let sp=sprites.get(f);
  if(!sp){const p=hooks.cellPx(f.cell);sp={f,x:p.x,y:p.y+FEET,facing:f.faction===(viewer&&viewer.faction)?"E":"W",anim:null,alpha:1,look:appearanceFor(f,viewer),visible:true,dead:false,glyph:API.handles(f)?null:f.glyph,pose:null};sprites.set(f,sp);}
  return sp;
}
function play(sp,state,clip,opts){
  const st=def.states[state];if(!st)return 0;
  const c=clip&&st.clips&&st.clips[clip]?st.clips[clip]:{frames:[...Array(st.frames).keys()],fps:st.fps};
  sp.anim={state,frames:c.frames,fps:c.fps||st.fps,loop:!!(opts&&opts.loop)||!!c.loop,hold:!!(opts&&opts.hold),t0:performance.now(),weapon:opts&&opts.weapon||null,motion:!(opts&&opts.loop),path:opts&&opts.path||null};
  return sp.anim.loop?0:c.frames.length*1000/sp.anim.fps;
}
function holdBase(sp){
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
function blit(path,col,row,size,dx,dy){const im=img(path);if(im)ctx.drawImage(im,col*size,row*size,size,size,dx,dy,size,size);}
function drawGlyph(sp){
  const cls=sp.f===viewer?"#2fe0ff":viewer&&sp.f.faction===viewer.faction?"#5fe08a":"#ff5d6c";
  ctx.globalAlpha=sp.alpha;ctx.font="25px system-ui,'Segoe UI Emoji','Apple Color Emoji',sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.shadowColor=cls;ctx.shadowBlur=8;ctx.fillText(sp.glyph,sp.x,sp.y-FEET);ctx.shadowBlur=0;ctx.globalAlpha=1;
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
  const [ax,ay]=pathOffset(st,sp,fr);
  const x=Math.round(ax-PIVOT[0]),y=Math.round(ay-PIVOT[1]);
  const isPair=!!part,want=k=>!part||part===k;
  const outfit=def.outfits[sp.look.outfit]||def.outfits.gi;
  const pick={body:"body",arms:"arms",clothing:outfit.clothing,armAccessories:outfit.armAccessories,hair:sp.look.hair,eyes:sp.look.eyes};
  const items=[];
  if(fr.weapon&&st.weapons)for(const it of st.weapons.items){if(it.item===fr.weapon&&!items.some(x=>x.slot===it.slot))items.push(it);}
  const weapon=depth=>{for(const it of items)if(it.layers[depth])blit(it.layers[depth],fr.col,row,128,x-32,y-32);};
  ctx.globalAlpha=sp.alpha;
  if(want("far")&&st.layers["far-arm"])blit(st.layers["far-arm"],fr.col,row,FRAME,x,y);
  if(want("body")){
    blit(def.contactShadow,def.referenceFrameOrder.indexOf(sp.facing),0,FRAME,Math.round(ax-PIVOT[0]),Math.round(ay-PIVOT[1]));
    WDEPTH_UNDER.forEach(weapon);
    for(const {slot} of def.slots){
      if(slot==="arms"){weapon("front");if(isPair)continue;}
      const layer=pick[slot];if(layer&&st.layers[layer])blit(st.layers[layer],fr.col,row,FRAME,x,y);
    }
    WDEPTH_OVER.forEach(weapon);
  }
  if(want("arms")&&isPair&&st.layers.arms)blit(st.layers.arms,fr.col,row,FRAME,x,y);
  const fx=st.layers["impact-fx"]||st.layers.fx;
  if(want("fx")&&fx)blit(fx,fr.col,row,FRAME,x,y);
  ctx.globalAlpha=1;
}
// a clinched pair, back to front (approved layering): holder far arm, held far arm, holder body, held body, held
// near arm, holder near arm, then the impact FX
function drawPair(h,d,now){
  drawSprite(h,now,"far");drawSprite(d,now,"far");drawSprite(h,now,"body");drawSprite(d,now,"body");
  drawSprite(d,now,"arms");drawSprite(h,now,"arms");drawSprite(d,now,"fx");drawSprite(h,now,"fx");
}
function frame(now){
  requestAnimationFrame(frame);
  if(!API.ready||!canvas||!canvas.isConnected||!canvas.offsetParent)return;
  const L=layout();if(!L)return;
  ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.setTransform(L.s,0,0,L.s,L.ox,L.oy);ctx.imageSmoothingEnabled=false;
  const list=[...sprites.values()].filter(sp=>sp.visible&&sp.alpha>0).sort((a,b)=>a.y-b.y);
  const done=new Set();
  for(const sp of list){
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
const px=c=>{const p=hooks.cellPx(c);return{x:p.x,y:p.y+FEET};};
function hexes(a,b){return root.AF?Math.max(1,root.AF.hdist(a,b)):1;}
async function fadeOut(sp,token){
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
    if(Math.hypot(h.x-d.x,h.y-d.y)>70)return;          // not adjacent: a ranged hold stays apart
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
const OPP={E:"W",W:"E",N:"S",S:"N"};
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
    h.facing=OPP[h.facing]||h.facing;holdBase(h);glide(h,hHome,GLIDE_MS,token);
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
    for(const m of beat.approach)await walk(m,token);
    await act(beat,counters,token);
  }
}
function settle(){
  frozen=false;recap=false;
  for(const [f,sp] of sprites)if(sp.glyph)sprites.delete(f);
  for(const sp of sprites.values()){sp.pose=null;sp.pair=null;}
  if(hooks&&hooks.onRecap)hooks.onRecap(null);
  for(const [f,sp] of sprites){
    if(!root.AF||!root.AF.alive(f)){sprites.delete(f);continue;}
    const p=px(f.cell);sp.x=p.x;sp.y=p.y;sp.alpha=1;holdBase(sp);
  }
  API.sync(battle,viewer);
}
function skip(){playToken++;projectiles.length=0;settle();}

API.attach=function(h){hooks=h;};
API.cancel=function(){if(frozen)skip();};
API.beginRound=function(){if(API.ready&&animateOn()&&ensureCanvas())frozen=true;};
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
    if(!alive&&!(frozen&&sprites.has(f)))continue;
    const sp=spriteFor(f);seen.add(f);
    sp.visible=!player||!root.AFUI||!alive||root.AFUI.canRenderFighter(B,player,f);
    if(!frozen){const p=px(f.cell);sp.x=p.x;sp.y=p.y;sp.pair=null;if(!sp.anim||sp.anim.loop)holdBase(sp);}
  }
  for(const f of [...sprites.keys()])if(!seen.has(f))sprites.delete(f);
  if(!frozen)applyStaticPairs(f=>root.AF.alive(f)?f.rel:null,f=>f.cell);
};
// the post-fight recap: every round of B.history replayed in order at normal speed, each from where
// the fighters stood as it began. Resolves true when it played to the end, false when skipped.
API.playRecap=function(B,player){
  const rounds=(B&&B.history||[]).filter(h=>h.events.length);
  if(!API.ready||!rounds.length||!hooks||!ensureCanvas())return Promise.resolve(false);
  battle=B;viewer=player||viewer;
  const token=++playToken;projectiles.length=0;frozen=true;recap=true;sprites.clear();
  const place=h=>{
    const keep=new Set();
    for(const s of h.start){
      if(!s.alive||!drawn(s.f))continue;keep.add(s.f);
      const sp=spriteFor(s.f),p=px(s.cell);
      sp.x=p.x;sp.y=p.y;sp.alpha=1;sp.dead=false;sp.pose={stam:s.stam,activeWeapon:s.activeWeapon};
      sp.visible=true;                   // the fight is over: the recap shows everyone
      holdBase(sp);
    }
    for(const f of [...sprites.keys()])if(!keep.has(f))sprites.delete(f);
    const snap=new Map(h.start.map(s=>[s.f,s]));
    applyStaticPairs(f=>snap.get(f)&&snap.get(f).alive?snap.get(f).rel:null,f=>snap.get(f)&&snap.get(f).cell);
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
API.skip=function(){if(frozen)skip();};
API.animateOn=animateOn;
API.whenReady=()=>load;
API.debug=()=>({ready:API.ready,sprites:[...sprites.values()].map(sp=>({name:sp.f.name,x:Math.round(sp.x),y:Math.round(sp.y),facing:sp.facing,state:sp.anim&&sp.anim.state,visible:sp.visible,alpha:sp.alpha})),frozen,playing:playToken});
})(typeof globalThis!=="undefined"?globalThis:this);
