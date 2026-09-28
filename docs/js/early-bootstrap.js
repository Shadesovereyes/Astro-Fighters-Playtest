/* Deterministic menu navigation available before the full app script loads. */

(()=>{
    const by=id=>document.getElementById(id);
    const overlays=['title-overlay','birth-overlay','chart-overlay','appearance-overlay','dialog-overlay','trap-overlay','field-menu'];
    const show=id=>{for(const x of overlays){const e=by(x);if(e)e.classList.add('hidden');}const t=by(id);if(t)t.classList.remove('hidden');};
    const bind=(id,target,after)=>{const e=by(id);if(!e)return;e.addEventListener('click',()=>{show(target);if(after)after();});};
    bind('new-btn','birth-overlay');
    bind('birth-back','title-overlay');
    bind('chart-back','birth-overlay');
    bind('appearance-back','chart-overlay');
    // If the full app has not loaded yet, these still provide deterministic navigation.
    bind('chart-btn','chart-overlay');
    bind('appearance-btn','appearance-overlay');
    window.AF_EARLY_BOOT=true;
    const s=by('js-status'); if(s){s.textContent='JavaScript active · early menu bootstrap ready';s.style.color='#9fd39f';}
  })();
  