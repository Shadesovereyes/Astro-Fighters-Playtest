/* Environment props for the hex arena (user, 2026-10-15: "build out the environment more make trees rocks and other
   environmental objects"). CANDIDATE art for the legacy hex testbed, awaiting the user's approval; not production world
   art and not in production/asset-manifest.json.

   Every prop is authored here as a deterministic pixel spec (shapes, ramps, a fixed light from the upper left, a 4x4
   ordered dither and integer hashes) and rasterised once into small canvases at 1 px = 1 viewBox unit, the same density
   as the character rig. No generated imagery and no resampling: the arena canvas scales them by an integer factor with
   nearest-neighbour, like the fighters.

   Terrain kinds come from the engine (af-core.js Grid): Tree, Rock, Bush, Rubble, Water, Wall, FelledTree, Smoke,
   Spikes, Caltrops; Open cells get ground dressing (grass, pebbles, flowers, mushrooms) that has no gameplay effect.
   "stand" props are depth sorted with the fighters; "flat" props lie on the ground under everything. */
(function(root){
"use strict";
const OUT="#000000";
const RAMP={
  pine:["#0c2219","#173d27","#245c33","#3c7c3c","#6aa64a"],
  oak:["#16280f","#284519","#3f6a22","#61922f","#9dc248"],
  autumn:["#3a1608","#6b2c0e","#a24c16","#d27a22","#f2b546"],
  bark:["#24140c","#432616","#653d22","#8a5a34"],
  stone:["#1f2029","#383a47","#575a69","#80839a","#b2b5c2"],
  sand:["#2c2620","#4b4136","#6f6352","#9a8c74","#c7b998"],
  earth:["#281b15","#463024","#6a4832","#8f6646","#bb8d62"],
  moss:["#2c4a1c","#4a7228","#76a23a"],
  water:["#0a1c36","#12315a","#1d4e86","#3577b4","#8cc7ec"],
  wood:["#5a3a1e","#8a5e32","#b88b52","#dcb67c"],
  metal:["#22262e","#4a525e","#7d8796","#c4ccd6","#f1f5f9"],
  smoke:["#33363f","#535763","#7b808c","#a6abb5","#d3d6dc"],
  grass:["#1a3417","#2a5222","#41752e","#6a9e3c"],
};
const BAYER=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];
const bay=(x,y)=>BAYER[(y&3)*4+(x&3)]/16-0.47;
const LIGHT=(()=>{const v=[-0.55,-0.72,0.55],n=Math.hypot(...v);return v.map(a=>a/n);})();
function hash(a,b,s){let h=(Math.imul(a|0,0x27d4eb2d)+Math.imul(b|0,0x165667b1)+Math.imul((s|0)+1,0x9e3779b1))|0;
  for(let k=0;k<2;k++){h^=h>>>16;h=Math.imul(h,0x85ebca6b);h^=h>>>13;h=Math.imul(h,0xc2b2ae35);h^=h>>>16;h=(h+Math.imul(k+a|0,0x61c88647))|0;}
  return(h>>>0)/4294967296;}
const clamp=(v,a,b)=>v<a?a:v>b?b:v;
const pick=(ramp,v,x,y,d=0.55)=>ramp[clamp(Math.round(v*(ramp.length-1)+bay(x,y)*d),0,ramp.length-1)];
const lam=(nx,ny,nz)=>Math.max(0,nx*LIGHT[0]+ny*LIGHT[1]+nz*LIGHT[2]);

/* --- a pixel buffer and the authoring primitives --- */
function Pix(w,h){this.w=w;this.h=h;this.c=new Array(w*h).fill(null);}
Pix.prototype.set=function(x,y,col){x=Math.floor(x);y=Math.floor(y);if(x<0||y<0||x>=this.w||y>=this.h||!col)return;this.c[y*this.w+x]=col;};
Pix.prototype.get=function(x,y){return x<0||y<0||x>=this.w||y>=this.h?null:this.c[y*this.w+x];};
// a 1 px outline round every opaque pixel (4-neighbour), like the character sheets
Pix.prototype.outline=function(col=OUT){
  const add=[];for(let y=0;y<this.h;y++)for(let x=0;x<this.w;x++){if(this.get(x,y))continue;
    if(this.get(x-1,y)||this.get(x+1,y)||this.get(x,y-1)||this.get(x,y+1))add.push([x,y]);}
  for(const[x,y]of add)this.set(x,y,col);return this;
};
// a lit ellipsoid; opt: facets (flat-shaded stone), noise (leafy clumps), bias, clipBottom, seed
function blob(p,cx,cy,rx,ry,ramp,opt={}){
  const seed=opt.seed||0,rot=hash(seed,7,3)*Math.PI*2;
  for(let y=Math.floor(cy-ry-1);y<=cy+ry+1;y++)for(let x=Math.floor(cx-rx-1);x<=cx+rx+1;x++){
    if(opt.clipBottom!=null&&y>opt.clipBottom)continue;
    const dx=(x+0.5-cx)/rx,dy=(y+0.5-cy)/ry;let d2=dx*dx+dy*dy;
    if(opt.wobble){const a=Math.atan2(dy,dx),k=Math.round((a+Math.PI)*opt.wobbleN/(Math.PI*2));d2/=Math.pow(1-opt.wobble*hash(k,seed,11),2);}
    if(d2>1)continue;
    let nx=dx,ny=dy,nz=Math.sqrt(Math.max(0,1-d2));
    if(opt.facets){const st=Math.PI*2/opt.facets,a=Math.round((Math.atan2(dy,dx)-rot)/st)*st+rot,r=Math.sqrt(d2)<0.42?0.2:0.78;
      nx=Math.cos(a)*r;ny=Math.sin(a)*r;nz=Math.sqrt(1-r*r);}
    let v=lam(nx,ny,nz)*1.12-0.08+(opt.bias||0);
    if(opt.noise){const k=opt.cell||2;v+=(hash(Math.floor(x/k),Math.floor(y/k),seed)-0.5)*opt.noise;}
    p.set(x,y,pick(ramp,v,x,y,opt.dither==null?0.55:opt.dither));
  }
}
// one tier of a conifer: a cone with a ragged hem
function tier(p,cx,top,bot,hw,ramp,seed){
  for(let y=top;y<=bot+1;y++){const t=(y-top)/Math.max(1,bot-top),half=0.6+hw*Math.min(1,t);
    for(let x=Math.floor(cx-half-1);x<=cx+half+1;x++){
      const dx=(x+0.5-cx)/half;if(Math.abs(dx)>1)continue;
      if(y>bot&&hash(x,seed,5)<0.55)continue;                      // drooping hem
      if(y>=bot-1&&Math.abs(dx)>0.82&&hash(x,y,seed)<0.5)continue;
      const nx=dx*0.85,ny=-0.2+0.35*t,nz=Math.sqrt(Math.max(0,1-nx*nx-ny*ny));
      let v=lam(nx,ny,nz)*1.1-0.12+(1-t)*0.12+(hash(x>>1,y,seed)-0.5)*0.45;
      p.set(x,y,pick(ramp,v,x,y));
    }}
}
// a vertical bark column, lit from the left, with streaks
function trunk(p,x0,y0,w,h,ramp,seed,flare=0){
  for(let y=y0;y<y0+h;y++){const f=y>=y0+h-2?flare:0;
    for(let x=x0-f;x<x0+w+f;x++){const t=(x-(x0-f)+0.5)/(w+2*f);let v=0.95-t*0.9+(hash(x,y>>1,seed)<0.18?-0.35:0);p.set(x,y,pick(ramp,v,x,y,0.3));}}
}
// a thick line (branches, planks)
function line(p,x0,y0,x1,y1,col,w=1){
  const n=Math.max(Math.abs(x1-x0),Math.abs(y1-y0))*2||1;
  for(let i=0;i<=n;i++){const x=x0+(x1-x0)*i/n,y=y0+(y1-y0)*i/n;for(let k=0;k<w;k++)p.set(x+(Math.abs(y1-y0)>Math.abs(x1-x0)?k:0),y+(Math.abs(y1-y0)>Math.abs(x1-x0)?0:k),col);}
}
function toCanvas(p){
  const c=document.createElement("canvas");c.width=p.w;c.height=p.h;const g=c.getContext("2d"),id=g.createImageData(p.w,p.h);
  for(let i=0;i<p.c.length;i++){const col=p.c[i];if(!col)continue;const n=parseInt(col.slice(1),16);id.data[i*4]=n>>16;id.data[i*4+1]=(n>>8)&255;id.data[i*4+2]=n&255;id.data[i*4+3]=255;}
  g.putImageData(id,0,0);return c;
}
// a pixel-edged ground shadow under a standing prop
function shadow(rx,ry){
  const p=new Pix(rx*2+1,ry*2+1);
  for(let y=0;y<p.h;y++)for(let x=0;x<p.w;x++){const dx=(x-rx)/(rx+0.5),dy=(y-ry)/(ry+0.5);if(dx*dx+dy*dy<=1)p.set(x,y,"#000000");}
  const c=toCanvas(p);c.ax=rx;c.ay=ry;return c;
}

/* --- the props: each variant is {w,h,ax,ay,draw(p)}; ax/ay is the foot point, set on the cell's ground point --- */
const SPEC={
  // trees stand about 2 to 2.4 fighters tall (user, 2026-10-15): the fighter figure is ~46 px, so 96-112 px
  Tree:{kind:"stand",shadow:[22,6],variants:[
    {name:"pine",w:64,h:112,ax:32,ay:108,draw(p){trunk(p,29,88,6,21,RAMP.bark,1,1);
      tier(p,32,58,92,29,RAMP.pine,3);tier(p,32,40,74,23,RAMP.pine,4);tier(p,32,23,56,17,RAMP.pine,5);tier(p,32,9,37,11,RAMP.pine,6);tier(p,32,1,18,5,RAMP.pine,7);}},
    {name:"oak",w:76,h:104,ax:38,ay:101,draw(p){trunk(p,33,58,10,44,RAMP.bark,2,2);
      line(p,37,64,22,50,RAMP.bark[1],3);line(p,41,62,55,48,RAMP.bark[2],3);line(p,38,60,36,44,RAMP.bark[2],2);
      for(const[x,y,rx,ry,s,b]of[[38,38,22,16,7,-0.25],[20,56,15,12,1,-0.1],[56,56,15,12,2,-0.1],[38,62,19,9,3,-0.15],[23,36,15,14,4,0],[53,36,15,14,5,0],[38,28,19,16,6,0.08]])blob(p,x,y,rx,ry,RAMP.oak,{noise:0.5,cell:2,seed:s,bias:b,wobble:0.16,wobbleN:12});}},
    {name:"autumn",w:70,h:96,ax:35,ay:93,draw(p){trunk(p,31,54,8,40,RAMP.bark,3,2);line(p,34,60,21,46,RAMP.bark[1],2);line(p,38,58,49,47,RAMP.bark[2],2);
      for(const[x,y,rx,ry,s,b]of[[35,36,19,14,14,-0.25],[19,51,13,11,8,-0.1],[51,51,13,11,9,-0.1],[35,56,17,9,10,-0.15],[22,33,13,13,11,0],[48,33,13,13,12,0],[35,25,17,14,13,0.08]])blob(p,x,y,rx,ry,RAMP.autumn,{noise:0.5,cell:2,seed:s,bias:b,wobble:0.16,wobbleN:12});}},
  ]},
  Rock:{kind:"stand",shadow:[13,4],variants:[
    {name:"boulder",w:34,h:26,ax:17,ay:22,draw(p){blob(p,17,14,13,10,RAMP.stone,{facets:7,seed:21,clipBottom:22});
      for(let y=3;y<12;y++)for(let x=8;x<26;x++){const c=p.get(x,y);if(c&&(c===RAMP.stone[3]||c===RAMP.stone[4])&&hash(x>>1,y>>1,22)<0.42)p.set(x,y,RAMP.moss[hash(x,y,23)<0.5?1:2]);}
      line(p,19,9,22,15,RAMP.stone[0]);line(p,22,15,21,19,RAMP.stone[0]);}},
    {name:"standing stone",w:32,h:34,ax:15,ay:30,draw(p){blob(p,14,17,7,14,RAMP.stone,{facets:5,seed:24,clipBottom:30});blob(p,24,25,6,5,RAMP.stone,{facets:6,seed:25,clipBottom:30});
      line(p,13,9,15,14,RAMP.stone[1]);}},
    {name:"cluster",w:34,h:26,ax:17,ay:22,draw(p){blob(p,22,13,9,9,RAMP.sand,{facets:6,seed:26,clipBottom:22});blob(p,10,16,8,7,RAMP.sand,{facets:6,seed:27,clipBottom:22});blob(p,17,19,7,4,RAMP.sand,{facets:5,seed:28,clipBottom:22});}},
  ]},
  Bush:{kind:"stand",shadow:[12,3],variants:[
    {name:"shrub",w:32,h:22,ax:16,ay:19,draw(p){for(const[x,y,rx,ry,s]of[[9,13,7,6,31],[23,13,7,6,32],[16,9,8,7,33],[16,15,9,5,34]])blob(p,x,y,rx,ry,RAMP.oak,{noise:0.7,seed:s,clipBottom:19,wobble:0.2,wobbleN:7});}},
    {name:"berry bush",w:32,h:22,ax:16,ay:19,draw(p){for(const[x,y,rx,ry,s]of[[10,13,7,6,35],[22,12,8,7,36],[15,15,9,5,37]])blob(p,x,y,rx,ry,RAMP.pine,{noise:0.7,seed:s,clipBottom:19,wobble:0.2,wobbleN:7});
      for(let i=0;i<9;i++){const x=5+Math.floor(hash(i,1,38)*22),y=6+Math.floor(hash(i,2,38)*10);if(p.get(x,y)&&p.get(x+1,y)){p.set(x,y,"#c8324a");p.set(x+1,y,"#7a1527");if(hash(i,3,38)<0.6)p.set(x,y-1,"#f07a8a");}}}},
    {name:"flowering bush",w:32,h:22,ax:16,ay:19,draw(p){for(const[x,y,rx,ry,s]of[[9,14,7,5,39],[22,13,8,6,40],[15,10,7,6,41]])blob(p,x,y,rx,ry,RAMP.grass,{noise:0.7,seed:s,clipBottom:19,wobble:0.2,wobbleN:7});
      for(let i=0;i<11;i++){const x=4+Math.floor(hash(i,1,42)*24),y=5+Math.floor(hash(i,2,42)*11);if(p.get(x,y)){p.set(x,y,"#f2d16b");p.set(x+1,y,"#f6f0d8");p.set(x,y+1,"#d99a2b");}}}},
  ]},
  Rubble:{kind:"stand",shadow:[12,3],variants:[
    {name:"stones",w:30,h:18,ax:15,ay:15,draw(p){[[17,9,5,4.2,0],[10,11,4.5,3.6,1],[14,13,4,3,0],[22,13,3.6,2.8,1],[6,14,2.6,2,0],[25,15,2.2,1.6,0],[19,15,2.4,1.8,1]].forEach(([x,y,rx,ry,k],i)=>blob(p,x,y,rx,ry,k?RAMP.sand:RAMP.stone,{facets:5,seed:52+i,clipBottom:15}));}},
    {name:"broken planks",w:30,h:18,ax:15,ay:15,draw(p){line(p,4,8,22,12,RAMP.wood[1],3);line(p,4,8,22,12,RAMP.wood[2],2);line(p,4,8,22,12,RAMP.wood[3],1);line(p,12,4,25,7,RAMP.wood[0],3);line(p,12,4,25,7,RAMP.wood[2],1);
      for(let i=0;i<5;i++){const x=6+hash(i,1,53)*18,y=10+hash(i,2,53)*4,r=1.6+hash(i,3,53)*2.4;blob(p,x,y,r+0.5,r*0.75,RAMP.sand,{facets:5,seed:54+i,clipBottom:15});}}},
  ]},
  Wall:{kind:"stand",shadow:[15,4],variants:[
    {name:"earth wall",w:34,h:32,ax:17,ay:28,draw(p){
      for(let y=9;y<=28;y++)for(let x=3;x<=30;x++){const row=Math.floor((y-9)/5),jx=(row%2?0:4);
        const mortar=(y-9)%5===4||((x+jx)%8===0);let v=0.62-(x-3)/27*0.35+(hash(x>>1,y>>1,61)-0.5)*0.3+(mortar?-0.45:0);p.set(x,y,pick(RAMP.earth,v,x,y,0.4));}
      blob(p,16.5,8,14,4.5,RAMP.earth,{noise:0.4,seed:62,bias:0.25});
      for(const[a,b,c,d]of[[9,13,11,19],[11,19,10,23],[24,18,26,24]])line(p,a,b,c,d,RAMP.earth[0]);}},
  ]},
  FelledTree:{kind:"stand",shadow:[15,3],variants:[
    {name:"log",w:38,h:18,ax:19,ay:15,draw(p){
      for(let y=6;y<=14;y++)for(let x=4;x<=31;x++){const t=(y-6)/8;let v=0.95-t*0.85+(hash(x>>1,y,71)<0.2?-0.3:0);p.set(x,y,pick(RAMP.bark,v,x,y,0.3));}
      for(let x=2;x<=4;x++)for(let y=6;y<=14;y++)if(hash(x,y,72)<0.6)p.set(x,y,RAMP.bark[1]);
      blob(p,32.5,10,3,4.8,RAMP.wood,{seed:73,bias:0.3,dither:0});
      p.set(32,10,RAMP.wood[1]);p.set(33,9,RAMP.wood[1]);p.set(32,8,RAMP.wood[2]);
      line(p,14,6,11,2,RAMP.bark[2],1);blob(p,10,3,3,2,RAMP.oak,{noise:0.5,seed:74});}},
    {name:"stump and log",w:38,h:22,ax:19,ay:19,draw(p){
      trunk(p,4,9,7,10,RAMP.bark,75,1);blob(p,7.5,9,4,1.8,RAMP.wood,{seed:76,bias:0.35,dither:0});p.set(7,9,RAMP.wood[1]);
      for(let y=11;y<=18;y++)for(let x=14;x<=34;x++){const t=(y-11)/7;let v=0.95-t*0.85+(hash(x>>1,y,77)<0.2?-0.3:0);p.set(x,y,pick(RAMP.bark,v,x,y,0.3));}
      blob(p,14,14.5,2.5,4,RAMP.wood,{seed:78,bias:0.25,dither:0});}},
  ]},
  Smoke:{kind:"stand",alpha:0.82,frames:4,frameMs:260,variants:[
    {name:"smoke",w:36,h:38,ax:18,ay:34,draw(p,f){
      for(let i=0;i<6;i++){const ph=(i/6+f/4)%1,x=18+(hash(i,1,81)-0.5)*16+Math.sin(ph*6.28+i)*2,y=31-ph*22,r=4+ph*6+hash(i,2,81)*2;
        blob(p,x,y,r,r*0.85,RAMP.smoke,{noise:0.35,seed:82+i,bias:0.12});}}},
  ]},
  // water fills its whole tile and runs on into the next one: the lake itself is painted into the arena ground; this is
  // only the moving glints on top of it
  Water:{kind:"flat",frames:3,frameMs:520,outline:false,variants:[
    {name:"glints",w:34,h:30,ax:17,ay:15,draw(p,f){
      for(let i=0;i<7;i++){const x=4+Math.floor(hash(i,f,92)*25),y=4+Math.floor(hash(i,f+7,92)*21),l=2+Math.floor(hash(i,f,94)*2);
        for(let k=0;k<l;k++)p.set(x+k,y,k===0||k===l-1?RAMP.water[3]:RAMP.water[4]);}}},
  ]},
  Spikes:{kind:"flat",variants:[
    {name:"spike pit",w:30,h:22,ax:15,ay:13,draw(p){
      blob(p,15,15,12,6,["#0b0706","#171009","#2a1c12","#3f2c1c"],{bias:-0.5,seed:101});
      for(let i=0;i<7;i++){const x=6+Math.round(hash(i,1,102)*17),base=13+Math.round(hash(i,2,102)*5),h=5+Math.round(hash(i,3,102)*3);
        for(let y=0;y<h;y++){p.set(x,base-y,RAMP.metal[y>h-3?4:3]);if(y<h-2){p.set(x-1,base-y,RAMP.metal[2]);p.set(x+1,base-y,RAMP.metal[1]);}}}}},
  ]},
  Caltrops:{kind:"flat",variants:[
    {name:"caltrops",w:30,h:20,ax:15,ay:10,draw(p){
      for(let i=0;i<8;i++){const x=4+Math.round(hash(i,1,111)*21),y=4+Math.round(hash(i,2,111)*12);
        p.set(x,y,RAMP.metal[4]);p.set(x-1,y,RAMP.metal[2]);p.set(x+1,y,RAMP.metal[2]);p.set(x,y-1,RAMP.metal[3]);p.set(x,y+1,RAMP.metal[1]);
        if(hash(i,3,111)<0.5){p.set(x-1,y-1,RAMP.metal[3]);p.set(x+1,y+1,RAMP.metal[1]);}else{p.set(x+1,y-1,RAMP.metal[3]);p.set(x-1,y+1,RAMP.metal[1]);}}}},
  ]},
};
// ground dressing on open cells: tiny, flat, no gameplay effect
const DECOR=[
  {name:"grass",w:9,h:7,outline:RAMP.grass[0],draw(p,s){for(let i=0;i<5;i++){const x=1+i*1.6,h=3+Math.round(hash(i,s,121)*3),lean=hash(i,s,122)<0.5?-1:1;for(let y=0;y<h;y++)p.set(x+(y>h-2?lean:0),6-y,RAMP.grass[y>=h-2?3:2]);}}},
  {name:"grass",w:9,h:7,outline:RAMP.grass[0],draw(p,s){for(let i=0;i<4;i++){const x=1.5+i*2,h=2+Math.round(hash(i,s,123)*4);for(let y=0;y<h;y++)p.set(x,6-y,RAMP.grass[y>=h-1?3:1+(i&1)]);}}},
  {name:"pebbles",w:9,h:6,outline:"#0d0e14",draw(p,s){for(let i=0;i<3;i++){const x=1.5+i*2.6+hash(i,s,124),y=2+hash(i,s,125)*2.5;blob(p,x,y,1.4+hash(i,s,126),1.1,RAMP.stone,{facets:4,seed:s+i,dither:0.3});}}},
  {name:"flowers",w:9,h:7,outline:RAMP.grass[0],draw(p,s){const cols=[["#e86a8a","#f6c0cc"],["#f2d16b","#fff3c4"],["#8fa8ff","#dbe3ff"]][Math.floor(hash(1,s,127)*3)];
    for(let i=0;i<3;i++){const x=1.5+i*2.8,h=2+Math.round(hash(i,s,128)*2);for(let y=0;y<h;y++)p.set(x,6-y,RAMP.grass[2]);p.set(x,6-h,cols[0]);p.set(x+1,6-h,cols[0]);p.set(x,5-h,cols[1]);}}},
  {name:"mushrooms",w:8,h:7,outline:"#1a0d0a",draw(p,s){for(const[x,h]of[[2,3],[5,2]]){for(let y=0;y<h;y++)p.set(x,6-y,"#e9dcc4");p.set(x-1,6-h,"#b8322a");p.set(x,6-h,"#d9473b");p.set(x+1,6-h,"#8a2119");p.set(x,5-h,"#f07a6a");}}},
];

/* --- build every variant and frame once --- */
let built=null;
function build(){
  if(built||typeof document==="undefined")return built;
  built={};
  for(const[t,spec]of Object.entries(SPEC)){
    built[t]=spec.variants.map(v=>{const frames=[];for(let f=0;f<(spec.frames||1);f++){const p=new Pix(v.w,v.h);v.draw(p,f);if(spec.outline!==false)p.outline(spec.outline||OUT);frames.push(toCanvas(p));}
      return{name:v.name,ax:v.ax,ay:v.ay,w:v.w,h:v.h,frames,kind:spec.kind,alpha:spec.alpha||1,frameMs:spec.frameMs||0,shadow:spec.shadow?shadow(...spec.shadow):null};});
  }
  built.decor=[];for(let s=0;s<3;s++)DECOR.forEach(d=>{const p=new Pix(d.w,d.h);d.draw(p,s+1);p.outline(d.outline);const c=toCanvas(p);built.decor.push({name:d.name,ax:d.w>>1,ay:d.h-1,w:d.w,h:d.h,frames:[c],kind:"flat",alpha:1,frameMs:0});});
  return built;
}

/* --- placing them: cells [{x,y,t}] (hex centre in viewBox units and the terrain kind) --- */
let lastKey="",lastScene=null;
// feet: how far below the hex centre a fighter's feet stand (the sprite layer's feet())
function scene(cells,feet){
  const B=build();if(!B||!cells)return null;
  const key=feet+"|"+cells.map(c=>c.x+","+c.y+c.t).join(";");if(key===lastKey)return lastScene;
  const flat=[],stand=[];
  for(const c of cells){
    const qx=Math.round(c.x*7),qy=Math.round(c.y*5),vars=B[c.t];
    if(vars&&vars.length){const v=vars[Math.floor(hash(qx,qy,1)*vars.length)],flip=v.kind==="stand"&&c.t!=="Smoke"&&hash(qx,qy,2)<0.5;
      const it={v,flip,x:Math.round(c.x),y:Math.round(c.y+(v.kind==="stand"?feet-1:0)),phase:Math.floor(hash(qx,qy,3)*4)};
      (v.kind==="stand"?stand:flat).push(it);continue;}
    if(c.t==="Open"&&hash(qx,qy,4)<0.6){const n=1+(hash(qx,qy,5)<0.35?1:0);
      for(let i=0;i<n;i++){const d=B.decor[Math.floor(hash(qx+i,qy,6)*B.decor.length)],a=hash(qx,qy+i,7)*Math.PI*2,r=4+hash(qx+i,qy+i,8)*8;
        flat.push({v:d,flip:hash(qx,qy,9+i)<0.5,x:Math.round(c.x+Math.cos(a)*r),y:Math.round(c.y+Math.sin(a)*r*0.8+3),phase:0});}}
  }
  stand.sort((a,b)=>a.y-b.y);
  lastKey=key;lastScene={flat,stand};return lastScene;
}
function draw(ctx,it,now,alpha=1){
  const v=it.v,img=v.frames.length>1?v.frames[(Math.floor(now/v.frameMs)+it.phase)%v.frames.length]:v.frames[0];
  ctx.globalAlpha=alpha*v.alpha;
  if(it.flip){ctx.save();ctx.translate(it.x,0);ctx.scale(-1,1);ctx.drawImage(img,-v.ax,it.y-v.ay);ctx.restore();}
  else ctx.drawImage(img,it.x-v.ax,it.y-v.ay);
  ctx.globalAlpha=1;
}
function drawShadow(ctx,it){const s=it.v.shadow;if(!s)return;ctx.globalAlpha=0.32;ctx.drawImage(s,it.x-s.ax,it.y-s.ay);ctx.globalAlpha=1;}
// the box a standing prop covers, for the see-through test against fighters behind it
const box=it=>({x0:it.x-it.v.ax+3,x1:it.x-it.v.ax+it.v.w-3,y0:it.y-it.v.ay+2,y1:it.y-2});

/* --- the seamless arena ground (user, 2026-10-15): one painted surface over the whole hex island, so the grid can sit
   under it as a faint planning aid and vanish while rounds play. A raised plateau: grass with darker and lighter
   patches and worn dirt, an outline round the island and an earth cliff face under its southern edge. --- */
const GROUND={grass:["#1c2e17","#24391d","#2c4523","#36522a","#435f31"],dirt:["#2e2219","#3b2c20","#4a3828","#5a4532"],
  cliff:["#47321f","#3a2919","#2c1f13","#21170e"],lip:"#52703a",bank:["#3d3324","#4d4130","#5e5039"],
  water:["#0b1d38","#12305a","#1a467e","#2a68a6","#4f93c8"],foam:"#a8d8ec"};
function vnoise(x,y,sc,seed){const gx=x/sc,gy=y/sc,x0=Math.floor(gx),y0=Math.floor(gy),fx=gx-x0,fy=gy-y0,sx=fx*fx*(3-2*fx),sy=fy*fy*(3-2*fy);
  const a=hash(x0,y0,seed),b=hash(x0+1,y0,seed),c=hash(x0,y0+1,seed),d=hash(x0+1,y0+1,seed);return a+(b-a)*sx+(c-a)*sy+(a-b-c+d)*sx*sy;}
let groundKey="",groundImg=null;
// cells [{x,y}] hex centres, s the hex step, W x H the viewBox size; returns a W x H canvas (transparent off the island)
function ground(cells,s,W,H){
  if(typeof document==="undefined"||!cells||!cells.length)return null;
  const o=cells[0],key=[W,H,s,cells.length,o.x,o.y,cells.filter(c=>c.t==="Water").map(c=>c.x+","+c.y).join(";")].join("|");if(key===groundKey)return groundImg;
  const SQ=Math.sqrt(3),cellKey=(x,y)=>{const dx=x-o.x,dy=y-o.y,q=(SQ/3*dx-dy/3)/s,r=(2/3*dy)/s,yy=-q-r;
    let rq=Math.round(q),rr=Math.round(r),ry=Math.round(yy);const eq=Math.abs(rq-q),er=Math.abs(rr-r),ey=Math.abs(ry-yy);
    if(eq>er&&eq>ey)rq=-ry-rr;else if(er>ey)rr=-rq-ry;return rq+","+rr;};
  const set=new Set(cells.map(c=>cellKey(c.x,c.y))),wet=new Set(cells.filter(c=>c.t==="Water").map(c=>cellKey(c.x,c.y))),inside=new Uint8Array(W*H);
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const k=cellKey(x+0.5,y+0.5);inside[y*W+x]=wet.has(k)?2:set.has(k)?1:0;}
  // distance (in px, 4-neighbour) from the shore inside the water, and from the water on dry ground
  const dist=new Int16Array(W*H).fill(99),q=[];
  for(let i=0;i<W*H;i++){if(inside[i]!==2)continue;const x=i%W,y=(i/W)|0;
    if([[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>{const xx=x+dx,yy=y+dy;return xx>=0&&yy>=0&&xx<W&&yy<H&&inside[yy*W+xx]===1;})){dist[i]=1;q.push(i);}}
  for(let h=0;h<q.length;h++){const i=q[h],x=i%W,y=(i/W)|0;if(dist[i]>=14)continue;
    for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){const xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=W||yy>=H)continue;const j=yy*W+xx;if(inside[j]===2&&dist[j]>dist[i]+1){dist[j]=dist[i]+1;q.push(j);}}}
  const nearWater=(x,y)=>{for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){if(Math.abs(dx)+Math.abs(dy)>2)continue;const xx=x+dx,yy=y+dy;if(xx>=0&&yy>=0&&xx<W&&yy<H&&inside[yy*W+xx]===2)return true;}return false;};
  const at=(x,y)=>x>=0&&y>=0&&x<W&&y<H&&inside[y*W+x]>0;
  const c=document.createElement("canvas");c.width=W;c.height=H;const g=c.getContext("2d"),id=g.createImageData(W,H),D=id.data;
  const put=(i,col)=>{const n=parseInt(col.slice(1),16);D[i*4]=n>>16;D[i*4+1]=(n>>8)&255;D[i*4+2]=n&255;D[i*4+3]=255;};
  const CLIFF=9;
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=y*W+x;
    if(inside[i]===2){
      const d=dist[i],n=vnoise(x,y,11,8)*0.6+vnoise(x,y,4,9)*0.4;let col;
      if(d<=1)col=GROUND.foam;
      else{const depth=clamp((d-1)/11,0,1);col=GROUND.water[clamp(Math.round(4-depth*3.4-(n-0.5)*1.1+bay(x,y)*0.8),0,4)];}
      if(!at(x,y-1))col=GROUND.foam;
      put(i,col);continue;}
    if(inside[i]){
      if(nearWater(x,y)){put(i,GROUND.bank[clamp(Math.round(1+bay(x,y)*1.4+(hash(x,y,10)-0.5)),0,2)]);continue;}
      const n=vnoise(x,y,26,1)*0.5+vnoise(x,y,9,2)*0.32+vnoise(x,y,3,3)*0.18,dn=vnoise(x+311,y+97,34,4)+(vnoise(x,y,6,5)-0.5)*0.18;
      let col;
      if(dn>0.7)col=GROUND.dirt[clamp(Math.round((n-0.2)*4+bay(x,y)*0.8),0,3)];
      else if(dn>0.66&&bay(x,y)>0)col=GROUND.dirt[1];
      else{col=GROUND.grass[clamp(Math.round((n-0.18)*5.2+bay(x,y)*0.7),0,4)];
        const h=hash(x,y,6);if(h<0.012)col=GROUND.grass[4];else if(h<0.02)col=GROUND.grass[0];
        if(h>0.995&&at(x,y+1))col=GROUND.lip;}
      if(!at(x,y-1))col=GROUND.lip;                                       // a light lip along the top edge
      put(i,col);continue;}
    // under the island: the cliff face, then an outline
    let k=0;for(let d=1;d<=CLIFF+1;d++)if(at(x,y-d)){k=d;break;}
    if(k&&k<=CLIFF){const above=at(x,y-k)?0:1;void above;
      put(i,(hash(x>>1,y,7)<0.12&&k>1)?GROUND.cliff[3]:GROUND.cliff[clamp(Math.floor((k-1)/2.5+bay(x,y)*0.5),0,3)]);continue;}
    if(k===CLIFF+1||at(x-1,y)||at(x+1,y)||at(x,y+1)||at(x,y-1)){put(i,OUT);continue;}
    // the cliff's own side outline
    let side=false;for(let d=1;d<=CLIFF&&!side;d++)if(at(x-1,y-d)||at(x+1,y-d))side=true;
    if(side)put(i,OUT);
  }
  g.putImageData(id,0,0);groundKey=key;groundImg=c;return c;
}

const API={RAMP,SPEC,GROUND,build,scene,draw,drawShadow,box,hash,ground,get ready(){return!!build();}};
root.AFProps=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
})(typeof globalThis!=="undefined"?globalThis:this);
