/* Astro Fighters World Package 05 — facade staging bridge.
Reference-first architecture integration. Not checklist completion. */
(() => {
  "use strict";
  const API = window.AF_WORLD_PACKAGE05 = window.AF_WORLD_PACKAGE05 || {};
  const MANIFEST_URL = "assets/metadata/world/package05-facade.json";
  const TEX = "af-world-package05-atlas";
  API.version = "package05-v1";
  API.status = "reference-gate-passed-facade-staging-candidate";

  function note(t){
    console.warn("[AF world p05]",t);
    let e=document.getElementById("af-world-package05-note");
    if(!e){e=document.createElement("div");e.id="af-world-package05-note";
      e.style.cssText="position:fixed;z-index:99997;right:8px;bottom:8px;max-width:520px;padding:8px 10px;background:#141410;color:#D5BAA0;border:1px solid #756A55;font:11px/1.35 ui-monospace,monospace;pointer-events:none";
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
  async function manifest(){const r=await fetch(MANIFEST_URL,{cache:"no-store"});if(!r.ok)throw new Error("manifest "+r.status);return r.json();}
  async function load(scene,m){
    if(scene.textures.exists(TEX))return;
    await new Promise((res,rej)=>{
      const fail=f=>rej(new Error("Package 05 atlas load failed: "+(f?.src||"unknown")));
      scene.load.once("loaderror",fail);scene.load.once("complete",()=>{scene.load.off("loaderror",fail);res();});
      scene.load.image(TEX,m.runtime.atlas_image);if(!scene.load.isLoading())scene.load.start();
    });
    const t=scene.textures.get(TEX);
    for(const arr of Object.values(m.runtime.families))for(const it of arr){
      const [x,y,w,h]=it.frame;if(!t.has(it.id))t.add(it.id,0,x,y,w,h);
    }
    t.setFilter(Phaser.Textures.FilterMode.NEAREST);
  }
  function create(scene,m){
    const target=player(scene);
    const baseX=Math.round((target?.x ?? scene.cameras.main.worldView.centerX)+170);
    const baseY=Math.round((target?.y ?? scene.cameras.main.worldView.centerY)+20);
    const root=scene.add.container(baseX,baseY);root.name="af-world-package05-facade";root.setDepth(baseY-25);
    const fam=m.runtime.families,state={scene,root,target,index:0,visible:true};
    const pick=(f,i)=>{const a=fam[f]||[];return a.length?a[((i%a.length)+a.length)%a.length]:null;};
    function add(f,i,x,y,z=0){const it=pick(f,i);if(!it)return null;const s=scene.add.image(x,y,TEX,it.id).setOrigin(.5,1);s.texture.setFilter(Phaser.Textures.FilterMode.NEAREST);s.setDepth(z);root.add(s);return s;}
    function rebuild(){
      root.removeAll(true);const i=state.index;
      add("wall",i,0,-34,0);add("door-window",i,0,-22,1);add("roof-eave",i,0,-116,2);
      add("awning-sign",i,0,-38,3);add("street-prop",i,-72,5,4);add("street-prop",i+1,72,6,4);
    }
    state.cycle=()=>{state.index=(state.index+1)%5;rebuild();note(`Package 05 facade variant ${state.index+1}. F2 toggle · F3 cycle.`);};
    state.setVisible=v=>{state.visible=!!v;root.setVisible(state.visible);};state.destroy=()=>root.destroy(true);rebuild();
    const keys=scene.input?.keyboard?.addKeys({toggle:"F2",cycle:"F3"});
    const update=()=>{if(!keys||!root.active)return;if(Phaser.Input.Keyboard.JustDown(keys.toggle))state.setVisible(!state.visible);if(Phaser.Input.Keyboard.JustDown(keys.cycle))state.cycle();
      if(state.target&&Number.isFinite(state.target.y)&&Number.isFinite(state.target.depth))root.setDepth(baseY<state.target.y?state.target.depth-20:state.target.depth+20);};
    scene.events.on("update",update);scene.events.once("shutdown",()=>scene.events.off("update",update));API.active=state;return state;
  }
  API.install=async()=>{try{const f=findScene();if(!f){note("Package 05: Phaser scene not detected.");return null;}const m=await manifest();await load(f.scene,m);const s=create(f.scene,m);note("Package 05 attached in Phaser. F2 toggles facade; F3 cycles variants. Staging candidate only.");return s;}
    catch(e){note("Package 05 failed: "+(e?.message||e));return null;}};
  (function boot(n=0){if(findScene())return API.install();if(n<80)setTimeout(()=>boot(n+1),250);else note("Package 05: Phaser runtime not detected after 20s.");})();
})();
