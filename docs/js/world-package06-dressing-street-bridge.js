/* Astro Fighters World Package 06 — architectural dressing + street slice staging.
Reference-first integration. No checklist completion claim. */
(() => {
  "use strict";
  const API=window.AF_WORLD_PACKAGE06=window.AF_WORLD_PACKAGE06||{};
  const MANIFEST_URL="assets/metadata/world/package06-dressing-street.json";
  const TEX="af-world-package06-atlas";
  API.version="package06-v3";
  API.status="clean-isolation-v3-staging-candidate";

  function note(t){
    console.warn("[AF world p06]",t);
    let e=document.getElementById("af-world-package06-note");
    if(!e){e=document.createElement("div");e.id="af-world-package06-note";
      e.style.cssText="position:fixed;z-index:99996;right:8px;top:8px;max-width:560px;padding:8px 10px;background:#141410;color:#D5BAA0;border:1px solid #756A55;font:11px/1.35 ui-monospace,monospace;pointer-events:none";
      document.body.appendChild(e);}
    e.textContent=t;
  }
  function findScene(){
    const P=window.Phaser;if(!P||!Array.isArray(P.GAMES)||!P.GAMES.length)return null;
    const game=P.GAMES.find(Boolean),scene=game?.scene?.getScenes(true)?.find(s=>s?.sys?.isActive());
    return scene?{P,game,scene}:null;
  }
  function player(scene){
    const p=window.AF_PAPERDOLL_PACKAGE01?.active?.target;
    if(p&&Number.isFinite(p.x)&&Number.isFinite(p.y))return p;
    const c=[scene.player,scene.registry?.get?.("player"),scene.data?.get?.("player")];
    for(const o of scene.children?.list||[]){
      if(!o)continue;const n=String(o.name||"").toLowerCase();
      if(["player","fighter","hero"].includes(n))c.push(o);
      if(typeof o.getData==="function"&&(o.getData("isPlayer")||o.getData("playerControlled")))c.push(o);
    }
    return c.find(o=>o&&Number.isFinite(o.x)&&Number.isFinite(o.y))||null;
  }
  async function getManifest(){const r=await fetch(MANIFEST_URL,{cache:"no-store"});if(!r.ok)throw new Error("manifest "+r.status);return r.json();}
  async function load(scene,m){
    if(!scene.textures.exists(TEX)){
      await new Promise((res,rej)=>{
        const fail=f=>rej(new Error("Package 06 atlas load failed: "+(f?.src||"unknown")));
        scene.load.once("loaderror",fail);scene.load.once("complete",()=>{scene.load.off("loaderror",fail);res();});
        const uri=window[m.runtime.atlas_data_uri_global]; if(!uri) throw new Error("Package 06 atlas data URI missing"); scene.load.image(TEX,uri);if(!scene.load.isLoading())scene.load.start();
      });
    }
    const t=scene.textures.get(TEX);
    for(const arr of Object.values(m.runtime.families))for(const it of arr){
      const [x,y,w,h]=it.frame;if(!t.has(it.id))t.add(it.id,0,x,y,w,h);
    }
    t.setFilter(Phaser.Textures.FilterMode.NEAREST);
  }
  function create(scene,m){
    const target=player(scene),cam=scene.cameras.main;
    const anchorX=Math.round((target?.x??cam.worldView.centerX)+170);
    const anchorY=Math.round((target?.y??cam.worldView.centerY)+28);
    const root=scene.add.container(anchorX,anchorY);root.name="af-world-package06-dressing";
    const fam=m.runtime.families,state={scene,root,target,index:0,visible:true};
    const pick=(f,i)=>{const a=fam[f]||[];return a.length?a[((i%a.length)+a.length)%a.length]:null;};
    function add(f,i,x,y,z){
      const it=pick(f,i);if(!it)return;
      const s=scene.add.image(x,y,TEX,it.id).setOrigin(.5,1);
      s.texture.setFilter(Phaser.Textures.FilterMode.NEAREST);s.setDepth(z);root.add(s);
    }
    const layouts=[
      [
        ["lantern",0,-86,-118,5],["lantern",3,76,-108,5],
        ["sign",0,95,-54,4],["sign",2,-18,-42,4],
        ["prop",1,-88,4,3],["prop",2,82,6,3],
        ["decor",0,-118,2,2],["decor",3,118,4,2]
      ],
      [
        ["lantern",2,-74,-104,5],["lantern",3,68,-102,5],
        ["sign",1,98,-58,4],["sign",3,-24,-44,4],
        ["prop",2,-90,5,3],["prop",3,84,5,3],
        ["decor",2,-114,4,2],["decor",3,118,5,2]
      ],
      [
        ["lantern",1,-80,-112,5],["lantern",2,73,-104,5],
        ["sign",2,98,-56,4],["sign",0,-20,-42,4],
        ["prop",1,-88,5,3],["prop",0,85,5,3],
        ["decor",1,-118,3,2],["decor",0,120,5,2]
      ]
    ];
    function rebuild(){
      root.removeAll(true);
      for(const [f,i,x,y,z] of layouts[state.index])add(f,i,x,y,z);
    }
    state.cycle=()=>{state.index=(state.index+1)%layouts.length;rebuild();note(`Package 06 dressing layout ${state.index+1}/${layouts.length}. F9 toggle · F10 cycle.`);};
    state.setVisible=v=>{state.visible=!!v;root.setVisible(state.visible);};state.destroy=()=>root.destroy(true);rebuild();
    const keys=scene.input?.keyboard?.addKeys({toggle:"F9",cycle:"F10"});
    const update=()=>{
      if(!keys||!root.active)return;
      if(Phaser.Input.Keyboard.JustDown(keys.toggle))state.setVisible(!state.visible);
      if(Phaser.Input.Keyboard.JustDown(keys.cycle))state.cycle();
      if(state.target&&Number.isFinite(state.target.y)&&Number.isFinite(state.target.depth)){
        root.setDepth(anchorY<state.target.y?state.target.depth-30:state.target.depth+30);
      }else root.setDepth(anchorY);
    };
    scene.events.on("update",update);scene.events.once("shutdown",()=>scene.events.off("update",update));
    API.active=state;return state;
  }
  API.install=async()=>{try{
    const f=findScene();if(!f){note("Package 06: Phaser scene not detected.");return null;}
    const m=await getManifest();await load(f.scene,m);const s=create(f.scene,m);
    note("Package 06 v3 attached. F9 toggles clean-isolated architectural dressing; F10 cycles authored dressing layouts. No grid is rendered.");
    return s;
  }catch(e){note("Package 06 failed: "+(e?.message||e));return null;}};
  (function boot(n=0){if(findScene())return API.install();if(n<80)setTimeout(()=>boot(n+1),250);else note("Package 06: Phaser runtime not detected after 20s.");})();
})();
