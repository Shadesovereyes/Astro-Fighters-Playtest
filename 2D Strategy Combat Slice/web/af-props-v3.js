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
    if(opt.noise)v+=(hash(x>>1,y>>1,seed)-0.5)*opt.noise;
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
  Tree:{kind:"stand",shadow:[13,4],variants:[
    {name:"pine",w:40,h:50,ax:20,ay:46,draw(p){trunk(p,18,37,4,10,RAMP.bark,1,1);tier(p,20,21,38,16,RAMP.pine,3);tier(p,20,12,29,12,RAMP.pine,4);tier(p,20,4,19,8,RAMP.pine,5);tier(p,20,1,9,3,RAMP.pine,6);}},
    {name:"oak",w:42,h:50,ax:21,ay:46,draw(p){trunk(p,18,30,6,17,RAMP.bark,2,1);line(p,20,32,13,27,RAMP.bark[1],2);line(p,22,31,29,26,RAMP.bark[2],2);
      for(const[x,y,rx,ry,s]of[[12,25,8,7,1],[30,25,8,7,2],[21,28,10,6,3],[14,15,8,8,4],[28,15,8,8,5],[21,12,10,9,6],[21,21,11,8,7]])blob(p,x,y,rx,ry,RAMP.oak,{noise:0.6,seed:s,wobble:0.18,wobbleN:9});}},
    {name:"autumn",w:38,h:46,ax:19,ay:42,draw(p){trunk(p,17,28,5,15,RAMP.bark,3,1);line(p,19,30,12,24,RAMP.bark[1],1);
      for(const[x,y,rx,ry,s]of[[11,22,7,6,8],[27,22,7,6,9],[19,24,9,6,10],[13,13,7,7,11],[25,13,7,7,12],[19,10,9,8,13],[19,18,10,7,14]])blob(p,x,y,rx,ry,RAMP.autumn,{noise:0.6,seed:s,wobble:0.18,wobbleN:9});}},
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
  Water:{kind:"flat",frames:3,frameMs:520,outline:"#1b1612",variants:[
    {name:"pond",w:36,h:28,ax:18,ay:14,draw(p,f){
      for(let y=0;y<28;y++)for(let x=0;x<36;x++){const dx=(x+0.5-18)/15,dy=(y+0.5-14)/11,a=Math.atan2(dy,dx),k=Math.round((a+Math.PI)*10/(Math.PI*2));
        const d=Math.sqrt(dx*dx+dy*dy)/(1-0.16*hash(k,91,9));if(d>1)continue;
        let v=0.15+Math.pow(d,1.6)*0.55;if(d>0.88)v=0.78;p.set(x,y,pick(RAMP.water,v,x,y,0.5));}
      for(let i=0;i<6;i++){const x=6+Math.floor(hash(i,f,92)*22),y=6+Math.floor(hash(i,f+7,92)*14);if(p.get(x,y)&&p.get(x+2,y)){p.set(x,y,RAMP.water[4]);p.set(x+1,y,RAMP.water[4]);if(hash(i,f,93)<0.5)p.set(x+2,y,RAMP.water[3]);}}}},
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
    built[t]=spec.variants.map(v=>{const frames=[];for(let f=0;f<(spec.frames||1);f++){const p=new Pix(v.w,v.h);v.draw(p,f);p.outline(spec.outline||OUT);frames.push(toCanvas(p));}
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

const API={RAMP,SPEC,build,scene,draw,drawShadow,box,hash,get ready(){return!!build();}};
root.AFProps=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
})(typeof globalThis!=="undefined"?globalThis:this);
