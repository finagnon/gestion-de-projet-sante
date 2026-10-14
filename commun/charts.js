function el(name, attrs = {}, parent) {
  const e = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}
function showTip(html, evt) {
  tip.innerHTML = html; tip.style.opacity = 1;
  const x = Math.min(evt.clientX + 14, window.innerWidth - tip.offsetWidth - 8);
  const y = Math.max(evt.clientY - tip.offsetHeight - 12, 8);
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
}
function hideTip() { tip.style.opacity = 0; }
function cw(c) { return Math.max(Math.round(c.getBoundingClientRect().width) || 560, 280); }
function niceMax(v) { const p = Math.pow(10, Math.floor(Math.log10(v))); for (const m of [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]) if (m * p >= v) return m * p; return 10 * p; }

/* Courbe (1 série) avec réticule + infobulle */
function lineChart(container, pts, { fmtAxis, fmtTip, color = 'var(--series-1)' }) {
  container.innerHTML = '';
  const W = cw(container), H = 240, m = { t: 12, r: 14, b: 26, l: 58 };
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Courbe mensuelle' }, container);
  const max = niceMax(Math.max(...pts.map(p => p.v)) * 1.05);
  const x = i => m.l + i * (W - m.l - m.r) / (pts.length - 1), y = v => H - m.b - v / max * (H - m.t - m.b);
  const g = el('g', { class: 'axis' }, svg);
  for (let k = 0; k <= 4; k++) { const v = max * k / 4; el('line', { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), class: 'gridline' }, g); const t = el('text', { x: m.l - 8, y: y(v) + 4, 'text-anchor': 'end' }, g); t.textContent = fmtAxis(v); }
  pts.forEach((p, i) => { if (i % (W < 420 ? 3 : 2) === 0 || pts.length <= 6) { const t = el('text', { x: x(i), y: H - 8, 'text-anchor': 'middle' }, g); t.textContent = p.label; } });
  el('path', { d: pts.map((p, i) => (i ? 'L' : 'M') + x(i) + ',' + y(p.v)).join(''), fill: 'none', stroke: color, 'stroke-width': 2, 'stroke-linejoin': 'round' }, svg);
  const last = pts[pts.length - 1];
  el('circle', { cx: x(pts.length - 1), cy: y(last.v), r: 4, fill: color, stroke: 'var(--surface)', 'stroke-width': 2 }, svg);
  const lt = el('text', { x: x(pts.length - 1) - 6, y: y(last.v) - 10, 'text-anchor': 'end', class: 'lab-strong' }, svg); lt.textContent = fmtAxis(last.v);
  const cross = el('line', { y1: m.t, y2: H - m.b, stroke: 'rgba(255,255,255,.35)', 'stroke-width': 1, opacity: 0 }, svg);
  const dot = el('circle', { r: 5, fill: color, stroke: 'var(--surface)', 'stroke-width': 2, opacity: 0 }, svg);
  const hit = el('rect', { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: 'transparent' }, svg);
  hit.addEventListener('mousemove', e => {
    const r = svg.getBoundingClientRect(); const px = (e.clientX - r.left) * W / r.width;
    const i = Math.max(0, Math.min(pts.length - 1, Math.round((px - m.l) / ((W - m.l - m.r) / (pts.length - 1)))));
    cross.setAttribute('x1', x(i)); cross.setAttribute('x2', x(i)); cross.setAttribute('opacity', 1);
    dot.setAttribute('cx', x(i)); dot.setAttribute('cy', y(pts[i].v)); dot.setAttribute('opacity', 1);
    showTip(fmtTip(pts[i]), e);
  });
  hit.addEventListener('mouseleave', () => { cross.setAttribute('opacity', 0); dot.setAttribute('opacity', 0); hideTip(); });
}

/* Barres verticales (1 série) */
function barChart(container, pts, { fmtAxis, fmtTip, color = 'var(--series-1)' }) {
  container.innerHTML = '';
  const W = cw(container), H = 240, m = { t: 12, r: 10, b: 26, l: 48 };
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Barres mensuelles' }, container);
  const max = niceMax(Math.max(...pts.map(p => p.v), 0.0001) * 1.1);
  const bw = (W - m.l - m.r) / pts.length, y = v => H - m.b - v / max * (H - m.t - m.b);
  const g = el('g', { class: 'axis' }, svg);
  for (let k = 0; k <= 4; k++) { const v = max * k / 4; el('line', { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), class: 'gridline' }, g); const t = el('text', { x: m.l - 8, y: y(v) + 4, 'text-anchor': 'end' }, g); t.textContent = fmtAxis(v); }
  const top = pts.reduce((a, b) => (b.v > a.v ? b : a));
  pts.forEach((p, i) => {
    const x0 = m.l + i * bw + 3, w = bw - 6, h = Math.max(H - m.b - y(p.v), 0), r = Math.min(4, w / 2, h);
    const yTop = H - m.b - h;
    const d = h > 0 ? `M${x0},${H - m.b} V${yTop + r} Q${x0},${yTop} ${x0 + r},${yTop} H${x0 + w - r} Q${x0 + w},${yTop} ${x0 + w},${yTop + r} V${H - m.b} Z` : '';
    if (d) el('path', { d, fill: color }, svg);
    if (W >= 420 || i % 2 === 0) { const t = el('text', { x: x0 + w / 2, y: H - 8, 'text-anchor': 'middle', class: 'lab' }, svg); t.textContent = p.label; }
    if (p === top) { const lt = el('text', { x: x0 + w / 2, y: yTop - 6, 'text-anchor': 'middle', class: 'lab-strong' }, svg); lt.textContent = fmtAxis(p.v); }
    const hit = el('rect', { x: m.l + i * bw, y: m.t, width: bw, height: H - m.t - m.b, fill: 'transparent' }, svg);
    hit.addEventListener('mousemove', e => showTip(fmtTip(p), e)); hit.addEventListener('mouseleave', hideTip);
  });
}

/* Barres horizontales groupées (1 ou 2 séries) */
function hbarChart(container, rows, series, { fmtVal, fmtTip, labelW = 170 }) {
  container.innerHTML = '';
  const rowH = series.length > 1 ? 34 : 30, W = cw(container), m = { t: 6, r: 56, b: 6, l: Math.min(labelW, Math.round(W * 0.38)) };
  const H = m.t + m.b + rows.length * rowH;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Barres horizontales' }, container);
  const max = Math.max(...rows.flatMap(r => series.map(s => r[s.key]))) * 1.02;
  const x = v => m.l + v / max * (W - m.l - m.r);
  const bh = series.length > 1 ? 11 : 16;
  rows.forEach((r, i) => {
    const y0 = m.t + i * rowH;
    const t = el('text', { x: m.l - 10, y: y0 + rowH / 2 + 4, 'text-anchor': 'end', class: 'lab' }, svg); const maxC = Math.floor((m.l - 16) / 5.9); t.textContent = r.label.length > maxC ? r.label.slice(0, maxC - 1) + '…' : r.label;
    series.forEach((s, j) => {
      const yy = y0 + (rowH - bh * series.length - 2 * (series.length - 1)) / 2 + j * (bh + 2);
      const w = Math.max(x(r[s.key]) - m.l, 0), rr = Math.min(4, bh / 2, w);
      el('path', { d: `M${m.l},${yy} H${m.l + w - rr} Q${m.l + w},${yy} ${m.l + w},${yy + rr} V${yy + bh - rr} Q${m.l + w},${yy + bh} ${m.l + w - rr},${yy + bh} H${m.l} Z`, fill: s.color }, svg);
      const lt = el('text', { x: m.l + w + 6, y: yy + bh / 2 + 4, class: j === series.length - 1 ? 'lab-strong' : 'lab' }, svg); lt.textContent = fmtVal(r[s.key]);
    });
    const hit = el('rect', { x: 0, y: y0, width: W, height: rowH, fill: 'transparent' }, svg);
    hit.addEventListener('mousemove', e => showTip(fmtTip(r), e)); hit.addEventListener('mouseleave', hideTip);
  });
}

