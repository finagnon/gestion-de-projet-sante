/* Courbes multi-séries (même unité) avec réticule + infobulle ; valeurs null = non tracées */
function multiLine(container, labels, series, { fmtAxis, fmtTip, minY = 0 }) {
  container.innerHTML = '';
  const W = cw(container), H = 250, m = { t: 14, r: 64, b: 26, l: 58 };
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Courbes' }, container);
  const all = series.flatMap(s => s.values.filter(v => v !== null));
  const max = niceMax(Math.max(...all) * 1.05);
  const x = i => m.l + i * (W - m.l - m.r) / (labels.length - 1), y = v => H - m.b - (v - minY) / (max - minY) * (H - m.t - m.b);
  const g = el('g', { class: 'axis' }, svg);
  for (let k = 0; k <= 4; k++) { const v = minY + (max - minY) * k / 4; el('line', { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), class: 'gridline' }, g); const t = el('text', { x: m.l - 8, y: y(v) + 4, 'text-anchor': 'end' }, g); t.textContent = fmtAxis(v); }
  const step = W < 420 ? 3 : (labels.length > 8 ? 2 : 1);
  labels.forEach((l, i) => { if (i % step === 0) { const t = el('text', { x: x(i), y: H - 8, 'text-anchor': 'middle' }, g); t.textContent = l; } });
  series.forEach(s => {
    let d = '', started = false;
    s.values.forEach((v, i) => { if (v === null) { started = false; return; } d += (started ? 'L' : 'M') + x(i) + ',' + y(v); started = true; });
    el('path', { d, fill: 'none', stroke: s.color, 'stroke-width': 2, 'stroke-dasharray': s.dash || '', 'stroke-linejoin': 'round' }, svg);
    const li = s.values.map((v, i) => v === null ? -1 : i).filter(i => i >= 0).pop();
    if (li !== undefined) {
      el('circle', { cx: x(li), cy: y(s.values[li]), r: 4, fill: s.color, stroke: 'var(--surface)', 'stroke-width': 2 }, svg);
      const t = el('text', { x: x(li) + 7, y: y(s.values[li]) + 4, class: 'lab-strong' }, svg); t.textContent = s.short || s.name;
    }
  });
  const cross = el('line', { y1: m.t, y2: H - m.b, stroke: 'rgba(255,255,255,.35)', 'stroke-width': 1, opacity: 0 }, svg);
  const hit = el('rect', { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: 'transparent' }, svg);
  hit.addEventListener('mousemove', e => {
    const r = svg.getBoundingClientRect(); const px = (e.clientX - r.left) * W / r.width;
    const i = Math.max(0, Math.min(labels.length - 1, Math.round((px - m.l) / ((W - m.l - m.r) / (labels.length - 1)))));
    cross.setAttribute('x1', x(i)); cross.setAttribute('x2', x(i)); cross.setAttribute('opacity', 1);
    showTip(fmtTip(i), e);
  });
  hit.addEventListener('mouseleave', () => { cross.setAttribute('opacity', 0); hideTip(); });
}
