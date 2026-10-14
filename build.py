"""
Construit les trois cas d'étude de gestion de projet (données 100 % fictives) :
  1. Cadrage d'un projet (note de cadrage, RACI, jalons, budget)
  2. Planification d'un déploiement (chemin critique, Gantt, risques, budget)
  3. Pilotage d'un programme Agile (vélocité, valeur acquise, comité, RGPD)

Pour chaque projet : calculs en Python, résultats en CSV et page HTML autonome (index.html).
Usage : python build.py
"""
import html
import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
CSS = (ROOT / "commun" / "style.css").read_text(encoding="utf-8")
JS = (ROOT / "commun" / "charts.js").read_text(encoding="utf-8") + (ROOT / "commun" / "charts_extra.js").read_text(encoding="utf-8")
PORTFOLIO = "https://portfolio-fiacre-yehossou.vercel.app"
GITHUB = "https://github.com/finagnon/gestion-de-projet-sante"
PAGES = [("gestion-projet-1-cadrage.html", "1 · Cadrage"), ("gestion-projet-2-planification.html", "2 · Planification"),
         ("gestion-projet-3-pilotage.html", "3 · Pilotage de programme")]
e = html.escape
eur = lambda v: f"{v:,.0f} €".replace(",", " ")
fr = lambda v, d=2: f"{v:.{d}f}".replace(".", ",")
pct = lambda v, d=0: f"{v * 100:.{d}f} %".replace(".", ",")

EXTRA_CSS = """
  .tabs { display:flex; gap:8px; flex-wrap:wrap; margin-top:18px; }
  .tabs a { padding:7px 13px; border-radius:999px; border:1px solid var(--border); background:var(--surface); color:var(--text-2); font-size:.83rem; font-weight:600; }
  .tabs a.on { background:var(--accent); color:#06111f; border-color:var(--accent); }
  .tabs a:hover { text-decoration:none; border-color:var(--accent); }
  .level { display:inline-block; margin-left:8px; padding:2px 9px; border-radius:999px; font-size:.7rem; border:1px solid var(--border); color:var(--text-2); vertical-align:middle; }
  .doc { display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:16px; }
  .doc .card p, .doc .card li { color:var(--text-2); font-size:.88rem; }
  .doc .card ul { padding-left:18px; margin-top:6px; }
  .doc .card li { margin-bottom:4px; }
  .full { grid-column: 1 / -1; }
  .letter { display:inline-flex; align-items:center; justify-content:center; min-width:30px; height:26px; padding:0 6px; border-radius:7px; font-weight:700; font-size:.78rem; border:1px solid var(--border); color:var(--text-2); }
  .letter.A { background:var(--accent); color:#06111f; border-color:var(--accent); }
  .letter.R { border-color:var(--accent); color:var(--text); }
  td.c, th.c { text-align:center; }
  .riskgrid { display:grid; grid-template-columns: 34px repeat(5, 1fr); gap:4px; font-size:.75rem; }
  .riskgrid .cell { aspect-ratio: 1.6; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:700; color:#06111f; position:relative; }
  .riskgrid .ax { color:var(--muted); display:flex; align-items:center; justify-content:center; }
  .z1 { background:#1f3a2a; color:var(--text-2) !important; } .z2 { background:#7a5a1e; } .z3 { background:#b4532f; } .z4 { background:#a3302f; color:var(--text) !important; }
  .meteo { font-size:1.4rem; }
  .bar { height:8px; border-radius:4px; background:var(--surface-2); overflow:hidden; min-width:90px; }
  .bar > i { display:block; height:100%; background:var(--series-1); border-radius:4px; }
  .doc > *, .grid > *, main > * { min-width: 0; }
  .kpis-4 { grid-template-columns: repeat(4, 1fr); }
  @media (max-width: 860px) { .doc { grid-template-columns: 1fr; } .kpis-4 { grid-template-columns: repeat(2, 1fr); } }
"""


def page(idx, title, kicker, lead, notice, body, data, script):
    tabs = "".join(f'<a class="{"on" if i == idx else ""}" href="{PORTFOLIO}/{f}">{e(t)}</a>' for i, (f, t) in enumerate(PAGES))
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} | Fiacre Yehossou</title>
<meta name="description" content="{e(lead)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<header class="wrap">
  <div class="topbar">
    <a href="{PORTFOLIO}/#projets">← Portfolio de Fiacre Yehossou</a>
    <div class="links"><a class="btn" href="{GITHUB}" target="_blank" rel="noopener noreferrer">Code sur GitHub ↗</a></div>
  </div>
  <nav class="tabs" aria-label="Les trois cas de gestion de projet">{tabs}</nav>
  <span class="kicker">{e(kicker)}</span>
  <h1>{e(title)}</h1>
  <p class="lead">{e(lead)}</p>
  <p class="notice">{notice}</p>
</header>
<main class="wrap">
{body}
</main>
<div class="tip" id="tip" role="status" aria-live="polite"></div>
<script>
const DATA = {json.dumps(data, ensure_ascii=False)};
const NS = 'http://www.w3.org/2000/svg';
const tip = document.getElementById('tip');
const fmtNum = (v, d = 0) => new Intl.NumberFormat('fr-FR', {{ maximumFractionDigits: d, minimumFractionDigits: d }}).format(v);
const fmtEur = v => fmtNum(v) + ' €';
const fmtK = v => fmtNum(v / 1000) + ' k€';
{JS}
function render() {{
{script}
}}
render();
let rz, lastW = window.innerWidth;
window.addEventListener('resize', () => {{ clearTimeout(rz); rz = setTimeout(() => {{ if (window.innerWidth !== lastW) {{ lastW = window.innerWidth; render(); }} }}, 150); }});
</script>
</body>
</html>"""


NOTICE = ("🔒 <b>Cas d'étude fictif</b> construit pour illustrer une méthode de gestion de projet, inspiré de projets "
          "data en milieu hospitalier. Établissement, personnes, montants et dates sont inventés. "
          "Aucune donnée patient ni donnée personnelle (RGPD).")


def tiles(items):
    return f'<section class="kpis kpis-{len(items)}" style="margin-top:22px">' + "".join(
        f'<div class="tile"><div class="lbl">{e(a)}</div><div class="val">{e(b)}</div><div class="sub">{e(c)}</div></div>'
        for a, b, c in items) + "</section>"


def table(df, num=(), center=(), raw=()):
    head = "".join(f'<th class="{"num" if c in num else "c" if c in center else ""}">{e(c)}</th>' for c in df.columns)
    rows = "".join("<tr>" + "".join(
        f'<td class="{"num" if c in num else "c" if c in center else ""}" style="white-space:normal">{v if c in raw else e(str(v))}</td>'
        for c, v in r.items()) + "</tr>" for r in df.to_dict("records"))
    return f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


# --------------------------------------------------------------------------- 1. CADRAGE
def build_cadrage():
    d = ROOT / "01-cadrage"
    raci = pd.read_csv(d / "data" / "raci.csv")
    jalons = pd.read_csv(d / "data" / "jalons.csv")
    budget = pd.read_csv(d / "data" / "budget.csv")
    risques = pd.read_csv(d / "data" / "risques_initiaux.csv")
    budget["montant_eur"] = budget["jours"] * budget["tjm_eur"] + budget["forfait_eur"]
    total = float(budget["montant_eur"].sum())
    reserve = round(total * 0.10, -2)
    budget.to_csv(d / "budget_calcule.csv", index=False)

    # contrôle de cohérence du RACI : exactement un A par activité, au moins un R
    roles = raci.columns[1:]
    controle = []
    for r in raci.itertuples(index=False):
        vals = [str(v) for v in r[1:]]
        nb_a = sum("A" in v for v in vals); nb_r = sum("R" in v for v in vals)
        controle.append({"activite": r[0], "nb_A": nb_a, "nb_R": nb_r, "conforme": nb_a == 1 and nb_r >= 1})
    controle = pd.DataFrame(controle)
    controle.to_csv(d / "controle_raci.csv", index=False)
    assert controle["conforme"].all(), "RACI incohérent"

    raci_html = raci.copy()
    for c in roles:
        raci_html[c] = raci_html[c].map(lambda v: " ".join(f'<span class="letter {x}">{x}</span>' for x in str(v).split("/")))
    raci_html = raci_html.rename(columns={"activite": "Activité"})

    body = tiles([
        ("Durée", "12 semaines", "de la note de cadrage au bilan"),
        ("Budget estimé", f"{total / 1000:.1f} k€".replace(".", ","), f"+ réserve 10 % ({eur(reserve)})"),
        ("Jalons", str(len(jalons)), "dont 2 décisions Go / No-go"),
        ("Parties prenantes", str(len(roles)), "rôles dans la matrice RACI"),
    ]) + f"""
<section class="doc">
  <div class="card">
    <h2>Contexte et problème</h2>
    <p>La pharmacie d'un centre hospitalier (fictif) produit son reporting d'approvisionnement à la main, à partir de
    plusieurs extractions Excel : 2 jours par mois, des chiffres qui diffèrent selon les services et aucune alerte
    sur les ruptures avant qu'elles ne surviennent.</p>
  </div>
  <div class="card">
    <h2>Objectifs SMART</h2>
    <ul>
      <li>Publier un tableau de bord hebdomadaire couvrant <b>100 % des références critiques</b> d'ici la semaine 11.</li>
      <li>Réduire le temps de production du reporting mensuel de <b>2 jours à 1 jour</b> dans les 3 mois suivant la mise en production.</li>
      <li>Atteindre <b>80 % d'utilisateurs actifs</b> parmi les 15 utilisateurs cibles à M+2.</li>
    </ul>
  </div>
  <div class="card">
    <h2>Périmètre</h2>
    <p><b>Inclus :</b> stocks, consommations, commandes et fournisseurs de la pharmacie ; 3 services pilotes.</p>
    <p style="margin-top:6px"><b>Exclu :</b> données patients, prescriptions, facturation, autres établissements.</p>
  </div>
  <div class="card">
    <h2>Contraintes et hypothèses</h2>
    <ul>
      <li>Budget plafond : 33 k€ réserve comprise ; équipe : chef de projet à 60 %, développeur BI à 50 %.</li>
      <li>RGPD : <b>aucune donnée personnelle</b> dans le tableau de bord (minimisation), DPO consulté au cadrage.</li>
      <li>Hypothèse : accès en lecture aux bases achats accordé avant la semaine 3.</li>
    </ul>
  </div>
  <div class="card full">
    <h2>Jalons et décisions</h2>
    <p class="desc">Chaque jalon a un livrable et une décision attendue.</p>
    <div id="chart-jalons"></div>
  </div>
  <div class="card full">
    <h2>Matrice RACI</h2>
    <p class="desc">R = réalise · <b>A = approuve (un seul par activité)</b> · C = consulté · I = informé. Cohérence vérifiée par le script.</p>
    {table(raci_html, center=list(roles), raw=list(roles))}
  </div>
  <div class="card">
    <h2>Budget estimatif</h2>
    <p class="desc">Jours × taux journalier (fictif) + forfaits.</p>
    <div id="chart-budget"></div>
  </div>
  <div class="card">
    <h2>Critères de succès et gouvernance</h2>
    <ul>
      <li>Comité de pilotage toutes les 3 semaines (sponsor, pharmacien, chef de projet, DSI).</li>
      <li>Point d'équipe hebdomadaire de 30 min et tableau de suivi partagé.</li>
      <li>Succès mesuré à M+3 sur les 3 objectifs SMART, présenté au sponsor.</li>
    </ul>
  </div>
  <div class="card full">
    <h2>Risques identifiés au cadrage</h2>
    {table(risques.rename(columns={"risque": "Risque", "probabilite": "Probabilité", "impact": "Impact", "reponse": "Réponse prévue"}))}
  </div>
</section>
<section class="method"><div><h3>Compétences démontrées</h3><ul><li>Cadrage, objectifs SMART, périmètre in/out.</li><li>RACI, gouvernance, jalons et décisions Go / No-go.</li><li>Budget estimatif et réserve pour aléas.</li></ul></div>
<div><h3>Livrables du dépôt</h3><ul><li><code>note_de_cadrage.md</code>, données RACI, jalons, budget, risques (CSV).</li><li><code>build.py</code> : calcul du budget et contrôle de cohérence du RACI.</li></ul></div></section>"""
    data = {"jalons": jalons.to_dict("records"), "budget": budget[["poste", "montant_eur"]].to_dict("records")}
    script = """
  timeline(document.getElementById('chart-jalons'), DATA.jalons);
  hbarChart(document.getElementById('chart-budget'), DATA.budget.map(b => ({ label: b.poste, v: b.montant_eur, b })),
    [{ key: 'v', color: 'var(--series-1)' }], { fmtVal: v => fmtEur(v), fmtTip: r => `<b>${r.label}</b><br>${fmtEur(r.v)}`, labelW: 230 });
"""
    script = TIMELINE_JS + script
    html_out = page(0, "Cadrage d'un projet de tableau de bord des approvisionnements",
                    "Gestion de projet • Niveau 1 : cadrage",
                    "Note de cadrage complète d'un projet data en pharmacie hospitalière : contexte, objectifs SMART, périmètre, "
                    "jalons, matrice RACI, budget et risques.", NOTICE, body, data, script)
    (d / "index.html").write_text(html_out, encoding="utf-8")
    return total


TIMELINE_JS = """
function timeline(container, items) {
  container.innerHTML = '';
  const W = cw(container), narrow = W < 640, H = narrow ? 20 + items.length * 46 : 130;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Frise des jalons' }, container);
  if (!narrow) {
    const m = { l: 40, r: 40 }, x = s => m.l + (s - 1) / 11 * (W - m.l - m.r), y0 = 70;
    el('line', { x1: m.l, x2: W - m.r, y1: y0, y2: y0, stroke: 'rgba(255,255,255,.25)', 'stroke-width': 2 }, svg);
    for (let s = 1; s <= 12; s++) { const t = el('text', { x: x(s), y: y0 + 24, 'text-anchor': 'middle', class: 'lab' }, svg); t.textContent = 'S' + s; }
    items.forEach((j, i) => {
      const cx = x(j.semaine);
      el('path', { d: `M${cx},${y0 - 8} L${cx + 8},${y0} L${cx},${y0 + 8} L${cx - 8},${y0} Z`, fill: 'var(--series-1)', stroke: 'var(--surface)', 'stroke-width': 2 }, svg);
      const up = i % 2 === 0, t = el('text', { x: cx, y: up ? y0 - 18 : y0 + 46, 'text-anchor': 'middle', class: 'lab-strong' }, svg); t.textContent = j.jalon;
      const hit = el('rect', { x: cx - 30, y: 0, width: 60, height: H, fill: 'transparent' }, svg);
      hit.addEventListener('mousemove', ev => showTip(`<b>S${j.semaine} — ${j.jalon}</b><br>Livrable : ${j.livrable}<br>Décision : ${j.decision}`, ev));
      hit.addEventListener('mouseleave', hideTip);
    });
  } else {
    items.forEach((j, i) => {
      const yy = 24 + i * 46;
      el('path', { d: `M20,${yy - 7} L27,${yy} L20,${yy + 7} L13,${yy} Z`, fill: 'var(--series-1)' }, svg);
      const t = el('text', { x: 40, y: yy + 4, class: 'lab-strong' }, svg); t.textContent = `S${j.semaine} — ${j.jalon}`;
      const t2 = el('text', { x: 40, y: yy + 20, class: 'lab' }, svg); t2.textContent = j.livrable.length > 46 ? j.livrable.slice(0, 45) + '…' : j.livrable;
    });
  }
}
"""


# --------------------------------------------------------------------------- 2. PLANIFICATION
def cpm(t: pd.DataFrame) -> pd.DataFrame:
    t = t.copy()
    t["pred"] = t["predecesseurs"].fillna("").map(lambda s: [p for p in s.split(";") if p])
    es, ef = {}, {}
    pending = list(t["id"])
    dur = dict(zip(t["id"], t["duree_j"]))
    pred = dict(zip(t["id"], t["pred"]))
    while pending:  # passe avant (tri topologique implicite)
        for i in list(pending):
            if all(p in ef for p in pred[i]):
                es[i] = max([ef[p] for p in pred[i]], default=0); ef[i] = es[i] + dur[i]; pending.remove(i)
    fin = max(ef.values())
    succ = {i: [j for j in t["id"] if i in pred[j]] for i in t["id"]}
    lf, ls = {}, {}
    pending = list(t["id"])  # passe arrière
    while pending:
        for i in list(pending):
            if all(s in ls for s in succ[i]):
                lf[i] = min([ls[s] for s in succ[i]], default=fin); ls[i] = lf[i] - dur[i]; pending.remove(i)
    t["debut_au_plus_tot"] = t["id"].map(es); t["fin_au_plus_tot"] = t["id"].map(ef)
    t["debut_au_plus_tard"] = t["id"].map(ls); t["fin_au_plus_tard"] = t["id"].map(lf)
    t["marge_totale_j"] = t["debut_au_plus_tard"] - t["debut_au_plus_tot"]
    t["critique"] = t["marge_totale_j"] == 0
    jours = pd.bdate_range("2026-01-05", periods=fin + 1)
    t["date_debut"] = t["debut_au_plus_tot"].map(lambda k: jours[k].date().isoformat())
    t["date_fin"] = t["fin_au_plus_tot"].map(lambda k: jours[k - 1].date().isoformat())
    return t.drop(columns=["pred"]), fin, jours


def build_planification():
    d = ROOT / "02-planification"
    taches, duree, jours = cpm(pd.read_csv(d / "data" / "taches.csv"))
    risques = pd.read_csv(d / "data" / "risques.csv")
    risques["score"] = risques["probabilite"] * risques["impact"]
    risques["niveau"] = pd.cut(risques["score"], [0, 4, 9, 15, 25], labels=["Faible", "Modéré", "Élevé", "Critique"])
    taches.to_csv(d / "planning_calcule.csv", index=False)
    risques.sort_values("score", ascending=False).to_csv(d / "registre_risques_calcule.csv", index=False)

    budget_phase = taches.groupby("phase", sort=False)["cout_eur"].sum().reset_index()
    total = float(budget_phase["cout_eur"].sum()); reserve = round(total * 0.10, -2)
    chemin = " → ".join(taches.loc[taches["critique"], "id"])
    crit = taches[taches["critique"]]
    n_crit_r = int((risques["score"] >= 12).sum())
    fin_date = jours[duree - 1].strftime("%d/%m/%Y")

    body = tiles([
        ("Durée totale (chemin critique)", f"{duree} jours ouvrés", f"du 05/01/2026 au {fin_date}"),
        ("Tâches critiques", f"{len(crit)} / {len(taches)}", "marge totale nulle"),
        ("Budget de référence", f"{total / 1000:.1f} k€".replace(".", ","), f"+ réserve 10 % ({eur(reserve)})"),
        ("Risques élevés ou critiques", str(n_crit_r), f"sur {len(risques)} risques suivis"),
    ]) + f"""
<section class="card tablecard">
  <div class="tablehead"><div><h2>Diagramme de Gantt et chemin critique</h2>
  <p class="desc" style="margin:0">Dates au plus tôt calculées par la méthode du chemin critique (CPM). Survolez une barre pour voir les marges.</p></div>
  <div class="legend"><span><i style="background:var(--series-2)"></i>Tâche critique</span><span><i style="background:var(--series-1)"></i>Tâche avec marge</span><span>◆ Jalon de décision</span></div></div>
  <div id="gantt" style="overflow-x:auto"></div>
  <p class="desc" style="margin-top:10px">Chemin critique : {e(chemin)}</p>
</section>
<section class="grid">
  <div class="card">
    <h2>Matrice des risques</h2>
    <p class="desc">Nombre de risques par probabilité (lignes) et impact (colonnes). Survolez une case pour voir les risques.</p>
    <div id="matrix"></div>
  </div>
  <div class="card">
    <h2>Budget de référence par phase</h2>
    <p class="desc">Coût des tâches de chaque phase, hors réserve.</p>
    <div id="chart-budget"></div>
  </div>
</section>
<section class="card tablecard">
  <h2>Registre des risques</h2>
  <p class="desc">Score = probabilité × impact (1 à 25). Stratégies : éviter, réduire, transférer, accepter.</p>
  {table(risques.sort_values("score", ascending=False)[["id", "risque", "categorie", "probabilite", "impact", "score", "niveau", "strategie", "reponse", "proprietaire"]]
         .rename(columns={"id": "ID", "risque": "Risque", "categorie": "Catégorie", "probabilite": "P", "impact": "I", "score": "Score",
                          "niveau": "Niveau", "strategie": "Stratégie", "reponse": "Réponse", "proprietaire": "Propriétaire"}), num=["P", "I", "Score"])}
</section>
<section class="method"><div><h3>Méthode</h3><ul><li>Découpage du projet en 20 tâches (WBS) avec durées, dépendances, responsables et coûts.</li>
<li>Calcul en Python des dates au plus tôt / au plus tard et des marges (chemin critique).</li><li>Registre des risques avec score, stratégie de réponse et propriétaire.</li></ul></div>
<div><h3>Lecture</h3><ul><li>Toute journée de retard sur une tâche critique décale la fin du projet ; les autres tâches ont de la marge.</li>
<li>Le risque R01 (interface avec les achats) porte sur T05, qui n'a que 3 jours de marge : au-delà, la tâche devient critique et décale la fin du projet. C'est la priorité de suivi du comité.</li></ul></div></section>"""
    data = {"taches": taches[["id", "tache", "phase", "duree_j", "debut_au_plus_tot", "fin_au_plus_tot", "marge_totale_j", "critique",
                              "responsable", "date_debut", "date_fin"]].to_dict("records"), "duree": duree,
            "risques": risques[["id", "risque", "probabilite", "impact", "score"]].to_dict("records"),
            "budget": budget_phase.to_dict("records")}
    script = GANTT_JS + """
  gantt(document.getElementById('gantt'), DATA.taches, DATA.duree);
  matrix(document.getElementById('matrix'), DATA.risques);
  hbarChart(document.getElementById('chart-budget'), DATA.budget.map(b => ({ label: b.phase, v: b.cout_eur })),
    [{ key: 'v', color: 'var(--series-1)' }], { fmtVal: v => fmtK(v), fmtTip: r => `<b>${r.label}</b><br>${fmtEur(r.v)}`, labelW: 130 });
"""
    html_out = page(1, "Planification du déploiement d'un logiciel de gestion des stocks",
                    "Gestion de projet • Niveau 2 : planification",
                    "Déploiement d'un logiciel de gestion des stocks dans 3 services de soins : découpage en tâches, chemin critique, "
                    "diagramme de Gantt, registre des risques et budget de référence.", NOTICE, body, data, script)
    (d / "index.html").write_text(html_out, encoding="utf-8")
    return duree, total


GANTT_JS = """
function gantt(container, tasks, total) {
  container.innerHTML = '';
  const W = Math.max(cw(container), 720), rowH = 26, m = { t: 26, l: 300, r: 20 }, H = m.t + tasks.length * rowH + 10;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, style: `width:${W}px;max-width:none`, role: 'img', 'aria-label': 'Diagramme de Gantt' }, container);
  const x = d => m.l + d / total * (W - m.l - m.r);
  for (let wk = 0; wk < total; wk += 5) {
    el('line', { x1: x(wk), x2: x(wk), y1: m.t - 6, y2: H - 6, class: 'gridline' }, svg);
    const t = el('text', { x: x(wk) + 3, y: 14, class: 'lab' }, svg); t.textContent = 'Sem. ' + (wk / 5 + 1);
  }
  let phase = '';
  tasks.forEach((tk, i) => {
    const y = m.t + i * rowH;
    const lab = el('text', { x: 8, y: y + 17, class: tk.critique ? 'lab-strong' : 'lab' }, svg);
    const name = `${tk.id} ${tk.tache}`; lab.textContent = name.length > 46 ? name.slice(0, 45) + '…' : name;
    const color = tk.critique ? 'var(--series-2)' : 'var(--series-1)';
    if (tk.duree_j <= 1) {
      const cx = x(tk.debut_au_plus_tot) + 4;
      el('path', { d: `M${cx},${y + 5} L${cx + 8},${y + 13} L${cx},${y + 21} L${cx - 8},${y + 13} Z`, fill: color }, svg);
    } else {
      el('rect', { x: x(tk.debut_au_plus_tot), y: y + 6, width: Math.max(x(tk.fin_au_plus_tot) - x(tk.debut_au_plus_tot) - 2, 3), height: 14, rx: 4, fill: color }, svg);
      if (tk.marge_totale_j > 0) el('rect', { x: x(tk.fin_au_plus_tot), y: y + 11, width: x(tk.fin_au_plus_tot + tk.marge_totale_j) - x(tk.fin_au_plus_tot), height: 4, rx: 2, fill: 'rgba(255,255,255,.18)' }, svg);
    }
    const hit = el('rect', { x: 0, y, width: W, height: rowH, fill: 'transparent' }, svg);
    hit.addEventListener('mousemove', e => showTip(`<b>${tk.id} — ${tk.tache}</b><br>${tk.phase} · ${tk.responsable}<br>Du ${tk.date_debut.split('-').reverse().join('/')} au ${tk.date_fin.split('-').reverse().join('/')} (${tk.duree_j} j)<br>Marge totale : ${tk.marge_totale_j} j${tk.critique ? ' — <b>critique</b>' : ''}`, e));
    hit.addEventListener('mouseleave', hideTip);
  });
}
function matrix(container, risks) {
  const z = s => s <= 4 ? 'z1' : s <= 9 ? 'z2' : s <= 15 ? 'z3' : 'z4';
  let h = '<div class="riskgrid">';
  for (let p = 5; p >= 1; p--) {
    h += `<div class="ax">P${p}</div>`;
    for (let i = 1; i <= 5; i++) {
      const rs = risks.filter(r => r.probabilite === p && r.impact === i);
      h += `<div class="cell ${z(p * i)}" data-p="${p}" data-i="${i}">${rs.length ? rs.map(r => r.id).join(' ') : ''}</div>`;
    }
  }
  h += '<div></div>' + [1, 2, 3, 4, 5].map(i => `<div class="ax">I${i}</div>`).join('') + '</div>';
  h += '<p class="desc" style="margin-top:8px">Zones : faible (≤ 4) · modéré (5-9) · élevé (10-15) · critique (≥ 16).</p>';
  container.innerHTML = h;
  container.querySelectorAll('.cell').forEach(c => {
    const rs = risks.filter(r => r.probabilite === +c.dataset.p && r.impact === +c.dataset.i);
    if (!rs.length) return;
    c.addEventListener('mousemove', e => showTip(rs.map(r => `<b>${r.id}</b> ${r.risque} (score ${r.score})`).join('<br>'), e));
    c.addEventListener('mouseleave', hideTip);
  });
}
"""


# --------------------------------------------------------------------------- 3. PILOTAGE DE PROGRAMME
def build_pilotage():
    d = ROOT / "03-pilotage-programme"
    sp = pd.read_csv(d / "data" / "sprints.csv")
    ev = pd.read_csv(d / "data" / "valeur_acquise.csv")
    ch = pd.read_csv(d / "data" / "chantiers.csv")
    rk = pd.read_csv(d / "data" / "risques.csv")
    dec = pd.read_csv(d / "data" / "decisions.csv")
    rg = pd.read_csv(d / "data" / "conformite_rgpd.csv")

    # --- Agile : vélocité et prévision de fin
    done = sp[sp["statut"] == "Terminé"].copy()
    done["cumul_realise"] = done["points_realises"].cumsum()
    velo3 = float(done["points_realises"].tail(3).mean())
    scope = int(sp["perimetre_total_points"].iloc[-1])
    restant = scope - int(done["cumul_realise"].iloc[-1])
    sprints_necessaires = math.ceil(restant / velo3)
    sprints_prevus = int((sp["statut"] == "Prévu").sum())
    fiabilite = float(done["points_realises"].sum() / done["points_engages"].sum())

    # --- Valeur acquise (EVM) à la date d'état
    bac = float(ev["pv_cumule_eur"].iloc[-1])
    last = ev.dropna(subset=["ev_cumule_eur"]).iloc[-1]
    pv, evv, ac = float(last["pv_cumule_eur"]), float(last["ev_cumule_eur"]), float(last["ac_cumule_eur"])
    spi, cpi = evv / pv, evv / ac
    eac = bac / cpi; vac = bac - eac; tcpi = (bac - evv) / (bac - ac)
    evm = pd.DataFrame([{"date_etat": last["mois"], "BAC": bac, "PV": pv, "EV": evv, "AC": ac, "SV": evv - pv, "CV": evv - ac,
                         "SPI": round(spi, 3), "CPI": round(cpi, 3), "EAC": round(eac), "ETC": round(eac - ac), "VAC": round(vac), "TCPI": round(tcpi, 3)}])
    evm.to_csv(d / "indicateurs_valeur_acquise.csv", index=False)
    pd.DataFrame([{"velocite_moyenne_3_derniers": round(velo3, 1), "perimetre_points": scope, "points_restants": restant,
                   "sprints_necessaires": sprints_necessaires, "sprints_prevus": sprints_prevus,
                   "fiabilite_engagements": round(fiabilite, 3)}]).to_csv(d / "prevision_agile.csv", index=False)

    rk["score"] = rk["probabilite"] * rk["impact"]
    meteo_icon = {"Ensoleillé": "☀️", "Nuageux": "⛅", "Orageux": "⛈️"}
    ch_html = ch.assign(meteo=ch["meteo"].map(lambda m: f'<span class="meteo" title="{m}">{meteo_icon[m]}</span> {m}'),
                        avancement=ch["avancement"].map(lambda a: f'<div class="bar"><i style="width:{a * 100:.0f}%"></i></div>{pct(a)}'))
    statut_icon = {"Fait": ("var(--good)", "✓"), "En cours": ("var(--serious)", "◆"), "À faire": ("var(--critical)", "⚠")}
    rg_html = rg.assign(statut=rg["statut"].map(lambda s: f'<span class="status"><span class="dot" style="background:{statut_icon[s][0]}"></span>{statut_icon[s][1]} {s}</span>'))
    retard = sprints_necessaires - sprints_prevus

    body = tiles([
        ("Indice de délai (SPI)", f"{spi:.2f}".replace(".", ","), f"valeur acquise / planifiée au {last['mois']}"),
        ("Indice de coût (CPI)", f"{cpi:.2f}".replace(".", ","), "valeur acquise / coût réel"),
        ("Coût final estimé (EAC)", f"{eac / 1000:.0f} k€", f"budget {bac / 1000:.0f} k€ · écart {vac / 1000:+.0f} k€"),
        ("Vélocité moyenne", f"{velo3:.1f} pts".replace(".", ","), "3 derniers sprints"),
        ("Fin prévisionnelle", f"+{retard} sprints" if retard > 0 else "À l'heure", f"{restant} points restants · {sprints_prevus} sprints prévus"),
        ("Conformité RGPD", f"{int((rg['statut'] == 'Fait').sum())} / {len(rg)}", "exigences satisfaites"),
    ]) + f"""
<section class="grid">
  <div class="card">
    <h2>Courbe en S : valeur acquise</h2>
    <p class="desc">Cumul en euros : valeur planifiée (PV), acquise (EV) et coût réel (AC).</p>
    <div class="legend"><span><i style="background:var(--series-1)"></i>Planifiée (PV)</span><span><i style="background:var(--series-2)"></i>Acquise (EV)</span><span><i style="background:#199e70"></i>Coût réel (AC)</span></div>
    <div id="chart-evm"></div>
  </div>
  <div class="card">
    <h2>Burn-up de la release 1</h2>
    <p class="desc">Points réalisés cumulés face au périmètre, avec prévision à la vélocité moyenne.</p>
    <div class="legend"><span><i style="background:var(--series-1)"></i>Périmètre</span><span><i style="background:var(--series-2)"></i>Réalisé</span><span><i style="background:var(--series-2);opacity:.5"></i>Prévision</span></div>
    <div id="chart-burnup"></div>
  </div>
  <div class="card">
    <h2>Vélocité par sprint</h2>
    <p class="desc">Points réalisés. Fiabilité des engagements : {pct(fiabilite)} des points engagés livrés.</p>
    <div id="chart-velo"></div>
  </div>
  <div class="card">
    <h2>Lecture pour le comité de pilotage</h2>
    <ul style="padding-left:18px;color:var(--text-2);font-size:.88rem">
      <li>Le programme a <b>{pct(1 - spi)} de retard</b> sur la valeur planifiée (SPI {fr(spi)}) et dépense <b>{pct(1 / cpi - 1)} de plus</b> que la valeur produite (CPI {fr(cpi)}).</li>
      <li>À ce rythme, le coût final atteindrait <b>{eac / 1000:.0f} k€</b> pour un budget de {bac / 1000:.0f} k€. Pour tenir le budget, l'équipe devrait être {pct(tcpi - 1)} plus efficiente (TCPI {fr(tcpi)}) : peu réaliste.</li>
      <li>Côté Agile, {restant} points restent à livrer à {fr(velo3, 1)} points par sprint : <b>{sprints_necessaires} sprints</b> au lieu de {sprints_prevus}.</li>
      <li><b>Recommandation :</b> proposer au prochain comité le report du module d'alertes automatiques en release 2 (−14 points), qui ramène le dépassement à environ un sprint, en plus du renfort déjà décidé.</li>
    </ul>
  </div>
</section>
<section class="card tablecard"><h2>Météo des chantiers</h2>{table(ch_html.rename(columns={"chantier": "Chantier", "responsable": "Responsable", "meteo": "Météo", "avancement": "Avancement", "commentaire": "Commentaire"}), raw=["Météo", "Avancement"])}</section>
<section class="card tablecard"><h2>Top risques du programme</h2>{table(rk.sort_values("score", ascending=False).rename(columns={"risque": "Risque", "probabilite": "P", "impact": "I", "score": "Score", "tendance": "Tendance", "reponse": "Réponse", "proprietaire": "Propriétaire"})[["Risque", "P", "I", "Score", "Tendance", "Réponse", "Propriétaire"]], num=["P", "I", "Score"])}</section>
<section class="card tablecard"><h2>Journal des décisions</h2>{table(dec.rename(columns={"date": "Date", "instance": "Instance", "decision": "Décision", "impact": "Impact"}))}</section>
<section class="card tablecard"><h2>Conformité RGPD (données de santé)</h2>
<p class="desc">Un entrepôt de données de santé exige une analyse d'impact, un hébergeur certifié HDS, la pseudonymisation et des accès tracés.</p>
{table(rg_html.rename(columns={"exigence": "Exigence", "reference": "Référence", "statut": "Statut", "preuve": "Preuve / action"}), raw=["Statut"])}</section>
<section class="method"><div><h3>Méthode</h3><ul><li>Scrum : sprints de 4 semaines, vélocité, burn-up et fiabilité des engagements.</li>
<li>Valeur acquise (EVM) : PV, EV, AC, SPI, CPI, EAC, VAC, TCPI calculés en Python.</li><li>Gouvernance : météo des chantiers, registre des risques, journal des décisions.</li></ul></div>
<div><h3>Pourquoi les deux approches</h3><ul><li>La vélocité dit <i>quand</i> le périmètre sera livré ; la valeur acquise dit <i>combien</i> il coûtera.</li>
<li>Les croiser permet de proposer au sponsor un arbitrage chiffré : délai, budget ou périmètre.</li></ul></div></section>"""

    labels_m = [m[5:] + "/" + m[2:4] for m in ev["mois"]]
    fv = lambda s: [None if pd.isna(v) else float(v) for v in s]
    cum = list(done["cumul_realise"].astype(float))
    forecast = [None] * (len(cum) - 1) + [cum[-1]] + [min(cum[-1] + velo3 * k, scope) for k in range(1, sprints_prevus + 1)]
    data = {"mois": labels_m, "pv": fv(ev["pv_cumule_eur"]), "ev": fv(ev["ev_cumule_eur"]), "ac": fv(ev["ac_cumule_eur"]),
            "sprints": list(sp["sprint"]), "scope": [float(v) for v in sp["perimetre_total_points"]],
            "realise": cum + [None] * sprints_prevus, "prevision": forecast,
            "velo": [{"label": s, "v": float(v)} for s, v in zip(done["sprint"], done["points_realises"])],
            "engages": [float(v) for v in done["points_engages"]]}
    script = """
  multiLine(document.getElementById('chart-evm'), DATA.mois, [
    { name: 'PV', values: DATA.pv, color: 'var(--series-1)' }, { name: 'EV', values: DATA.ev, color: 'var(--series-2)' }, { name: 'AC', values: DATA.ac, color: '#199e70' }],
    { fmtAxis: fmtK, fmtTip: i => `<b>${DATA.mois[i]}</b><br>PV : ${fmtEur(DATA.pv[i])}` + (DATA.ev[i] !== null ? `<br>EV : ${fmtEur(DATA.ev[i])}<br>AC : ${fmtEur(DATA.ac[i])}` : '<br><i>prévisionnel</i>') });
  multiLine(document.getElementById('chart-burnup'), DATA.sprints, [
    { name: 'Périmètre', values: DATA.scope, color: 'var(--series-1)' }, { name: 'Réalisé', values: DATA.realise, color: 'var(--series-2)' },
    { name: 'Prévision', values: DATA.prevision, color: 'var(--series-2)', dash: '5 4', short: 'Prév.' }],
    { fmtAxis: v => fmtNum(v) + ' pts', fmtTip: i => `<b>${DATA.sprints[i]}</b><br>Périmètre : ${DATA.scope[i]} pts` + (DATA.realise[i] !== null ? `<br>Réalisé cumulé : ${DATA.realise[i]} pts` : '') + (DATA.prevision[i] !== null && DATA.realise[i] === null ? `<br>Prévision : ${fmtNum(DATA.prevision[i])} pts` : '') });
  barChart(document.getElementById('chart-velo'), DATA.velo.map((v, i) => ({ ...v, e: DATA.engages[i] })),
    { fmtAxis: v => fmtNum(v), fmtTip: p => `<b>${p.label}</b><br>Réalisés : ${p.v} pts<br>Engagés : ${p.e} pts` });
"""
    html_out = page(2, "Pilotage d'un programme data en Agile avec la valeur acquise",
                    "Gestion de projet • Niveau 3 : pilotage de programme",
                    "Programme fictif d'entrepôt de données et d'indicateurs qualité des soins : sprints Scrum, vélocité, valeur acquise, "
                    "météo des chantiers, risques, décisions du comité et conformité RGPD des données de santé.", NOTICE, body, data, script)
    (d / "index.html").write_text(html_out, encoding="utf-8")
    return evm.iloc[0].to_dict(), velo3, sprints_necessaires, sprints_prevus


if __name__ == "__main__":
    t1 = build_cadrage()
    d2, t2 = build_planification()
    evm, v, n, p = build_pilotage()
    print(f"1. Cadrage : budget estimé {t1:,.0f} €")
    print(f"2. Planification : {d2} jours ouvrés sur le chemin critique, budget {t2:,.0f} €")
    print(f"3. Pilotage : SPI {evm['SPI']}, CPI {evm['CPI']}, EAC {evm['EAC']:,.0f} €, vélocité {v:.1f}, {n} sprints nécessaires pour {p} prévus")
