/* Character-creator UI: birthplace search (folded in from the former play-v4 launcher patch). */
(() => {
  const $ = (id) => document.getElementById(id);

  function installBirthplaceSearch() {
    const old = $('birth-place');
    if (!old) return;

    const input = old.cloneNode(true);
    old.replaceWith(input);
    $('birth-place-results')?.remove();
    document.querySelector('.birth-place-search-status')?.remove();

    input.placeholder = 'Search city, town, or postal code';

    const wrap = document.createElement('div');
    wrap.style.cssText = 'display:grid;grid-template-columns:1fr auto;gap:6px';
    input.parentElement.insertBefore(wrap, input);
    wrap.appendChild(input);

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = 'Search';
    btn.style.cssText = 'padding:7px 12px';
    wrap.appendChild(btn);

    const results = document.createElement('div');
    results.style.cssText = 'display:none;margin-top:6px;border:1px solid #5b5144;background:#121416;max-height:210px;overflow:auto;position:relative;z-index:130';
    wrap.insertAdjacentElement('afterend', results);

    const status = document.createElement('div');
    status.style.cssText = 'margin-top:5px;font:10px/1.35 ui-monospace,monospace;color:#9e9585;text-transform:none;letter-spacing:0';
    status.textContent = 'Search a birthplace to fill coordinates and timezone.';
    results.insertAdjacentElement('afterend', status);

    let seq = 0;
    let timer = 0;
    const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
    const label = (r) => r.label || [r.name, r.admin1, r.country].filter(Boolean).join(', ');
    const close = () => { results.style.display = 'none'; };

    async function run() {
      clearTimeout(timer);
      const q = input.value.trim();
      const my = ++seq;
      if (q.length < 2) {
        close();
        status.textContent = 'Enter at least 2 characters.';
        return;
      }

      status.textContent = 'Searching locations…';
      status.style.color = '#9bc3cd';

      try {
        if (typeof AF_ASTRO === 'undefined' || typeof AF_ASTRO.searchPlaces !== 'function') {
          throw new Error('Natal geocoder unavailable');
        }
        const rows = await AF_ASTRO.searchPlaces(q);
        if (my !== seq) return;

        results.innerHTML = '';
        if (!rows.length) {
          close();
          status.style.color = '#d5ad68';
          status.textContent = 'No matching location found. Manual coordinates and timezone still work.';
          return;
        }

        for (const r of rows) {
          const b = document.createElement('button');
          b.type = 'button';
          b.style.cssText = 'display:block;width:100%;border:0;border-bottom:1px solid #38342e;background:#16191b;color:#eadfc8;padding:9px 10px;text-align:left';
          b.innerHTML = '<b style="display:block;color:#efd39d">' + esc(label(r)) + '</b>' +
            '<small style="display:block;color:#9e9585">' +
            esc([r.admin1, r.country, r.timezone].filter(Boolean).join(' · ')) + ' · ' +
            Number(r.latitude).toFixed(4) + ', ' + Number(r.longitude).toFixed(4) + '</small>';
          b.onclick = () => {
            input.value = label(r);
            $('birth-lat').value = Number(r.latitude).toFixed(4);
            $('birth-lon').value = Number(r.longitude).toFixed(4);
            $('birth-tz').value = r.timezone || 'UTC';
            status.style.color = '#8fb28f';
            status.textContent = 'Selected ' + label(r) + ' · ' + $('birth-lat').value + ', ' + $('birth-lon').value + ' · ' + $('birth-tz').value;
            close();
          };
          results.appendChild(b);
        }

        results.style.display = 'block';
        status.style.color = '#8fb28f';
        status.textContent = 'Choose a result.';
      } catch (e) {
        close();
        status.style.color = '#d78d7e';
        status.textContent = 'Location search failed. Manual coordinates and timezone still work.';
        console.warn(e);
      }
    }

    btn.onclick = run;
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        run();
      }
    });
    input.addEventListener('input', () => {
      clearTimeout(timer);
      close();
      if (input.value.trim().length >= 3) timer = setTimeout(run, 450);
    });
  }

  installBirthplaceSearch();
})();
