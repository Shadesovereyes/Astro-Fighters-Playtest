(() => {
  const stateKey = 'af-art-review-draft-v1';
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => [...document.querySelectorAll(sel)];
  let rubric;

  function el(tag, attrs = {}, text = '') {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (key === 'class') node.className = value;
      else if (key === 'for') node.htmlFor = value;
      else node.setAttribute(key, value);
    }
    if (text) node.textContent = text;
    return node;
  }

  function renderRubric() {
    const failures = $('#automatic-failures');
    rubric.automaticFailures.forEach((label, i) => {
      const id = `auto-${i}`;
      const row = el('label', { class: 'check-row', for: id });
      row.append(el('input', { type: 'checkbox', id, 'data-auto-fail': i }));
      row.append(el('span', {}, label));
      failures.append(row);
    });

    const scores = $('#scores');
    rubric.categories.forEach((category, i) => {
      const row = el('div', { class: 'score-row' });
      const info = el('div', { class: 'score-info' });
      const title = el('strong', {}, `${i + 1}. ${category.name}`);
      const minText = category.min == null ? 'Public benchmark: 4+' : `Minimum: ${category.min}+${category.critical ? ' · critical' : ''}`;
      info.append(title, el('small', {}, minText));

      const input = el('input', {
        type: 'number', min: '0', max: '5', step: '1', value: '0',
        'data-score': category.id, 'aria-label': `${category.name} score`
      });
      row.append(info, input);
      scores.append(row);
    });
  }

  function classify(total) {
    return rubric.thresholds.find((t) => total >= t.min && total <= t.max) || rubric.thresholds[rubric.thresholds.length - 1];
  }

  function collect() {
    const scores = {};
    rubric.categories.forEach((category) => {
      const input = document.querySelector(`[data-score="${category.id}"]`);
      scores[category.id] = Math.max(0, Math.min(5, Number(input?.value || 0)));
    });
    return {
      schema: 'astro-fighters-art-review/v1',
      sceneId: $('#scene-id').value.trim(),
      packageId: $('#package-id').value.trim(),
      district: $('#district').value,
      reviewer: $('#reviewer').value.trim(),
      date: $('#review-date').value,
      automaticFailures: $$('[data-auto-fail]:checked').map((n) => rubric.automaticFailures[Number(n.dataset.autoFail)]),
      scores,
      notes: $('#notes').value.trim()
    };
  }

  function evaluate(review) {
    const total = Object.values(review.scores).reduce((sum, value) => sum + value, 0);
    const minimumFailures = rubric.categories
      .filter((category) => category.min != null && review.scores[category.id] < category.min)
      .map((category) => ({ id: category.id, name: category.name, score: review.scores[category.id], min: category.min, critical: category.critical }));
    const criticalFailures = minimumFailures.filter((x) => x.critical);
    const scoreClass = classify(total);
    const blocked = review.automaticFailures.length > 0 || criticalFailures.length > 0;
    const status = blocked ? { code: 'blocked', label: 'BLOCKED — CONTINUE DEVELOPMENT' } : scoreClass;
    const mayCompleteChecklist = !blocked && total >= 42;
    const publicReady = mayCompleteChecklist && review.scores.screenshot >= 4;
    return { total, minimumFailures, criticalFailures, scoreClass, status, mayCompleteChecklist, publicReady };
  }

  function update() {
    const review = collect();
    const result = evaluate(review);
    $('#total').textContent = `${result.total}/${rubric.maxScore}`;
    $('#status').textContent = result.status.label;
    $('#status').dataset.status = result.status.code;
    $('#completion').textContent = result.mayCompleteChecklist
      ? 'Checklist completion permitted for integrated items represented by this review.'
      : 'Do not strike checklist items; continue development.';

    const problems = $('#problems');
    problems.innerHTML = '';
    review.automaticFailures.forEach((x) => problems.append(el('li', {}, `Automatic failure: ${x}`)));
    result.criticalFailures.forEach((x) => problems.append(el('li', {}, `Critical minimum failed: ${x.name} ${x.score}/${x.min}.`)));
    result.minimumFailures.filter((x) => !x.critical).forEach((x) => problems.append(el('li', {}, `Minimum missed: ${x.name} ${x.score}/${x.min}.`)));
    if (!problems.children.length) problems.append(el('li', {}, 'No automatic or minimum-score blockers recorded.'));

    localStorage.setItem(stateKey, JSON.stringify(review));
    return { review, result };
  }

  function restore() {
    const raw = localStorage.getItem(stateKey);
    if (!raw) return;
    try {
      const saved = JSON.parse(raw);
      $('#scene-id').value = saved.sceneId || '';
      $('#package-id').value = saved.packageId || '';
      $('#district').value = saved.district || 'Imperial City — shared/global';
      $('#reviewer').value = saved.reviewer || '';
      $('#review-date').value = saved.date || new Date().toISOString().slice(0, 10);
      $('#notes').value = saved.notes || '';
      rubric.categories.forEach((category) => {
        const input = document.querySelector(`[data-score="${category.id}"]`);
        if (input) input.value = saved.scores?.[category.id] ?? 0;
      });
      const savedFailures = new Set(saved.automaticFailures || []);
      $$('[data-auto-fail]').forEach((n) => {
        n.checked = savedFailures.has(rubric.automaticFailures[Number(n.dataset.autoFail)]);
      });
    } catch (e) {
      console.warn('Could not restore review draft', e);
    }
  }

  function exportReview() {
    const { review, result } = update();
    const payload = {
      ...review,
      result: {
        total: result.total,
        maxScore: rubric.maxScore,
        classification: result.scoreClass.label,
        blocked: result.status.code === 'blocked',
        criticalFailures: result.criticalFailures,
        checklistCompletionPermitted: result.mayCompleteChecklist,
        publicReady: result.publicReady
      }
    };
    const blob = new Blob([JSON.stringify(payload, null, 2) + '\n'], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const safe = (review.sceneId || review.packageId || 'art-review').replace(/[^a-z0-9_-]+/gi, '-').replace(/^-|-$/g, '');
    a.href = url;
    a.download = `${safe || 'art-review'}.review.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function init() {
    rubric = await fetch('data/art-review-rubric.json', { cache: 'no-store' }).then((r) => {
      if (!r.ok) throw new Error(`Rubric load failed: ${r.status}`);
      return r.json();
    });
    renderRubric();
    $('#review-date').value = new Date().toISOString().slice(0, 10);
    restore();
    document.addEventListener('input', update);
    document.addEventListener('change', update);
    $('#export').addEventListener('click', exportReview);
    $('#reset').addEventListener('click', () => {
      localStorage.removeItem(stateKey);
      location.reload();
    });
    update();
  }

  init().catch((error) => {
    $('#load-error').hidden = false;
    $('#load-error').textContent = error.message;
    console.error(error);
  });
})();
