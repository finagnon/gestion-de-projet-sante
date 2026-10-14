# Gestion de projet data en santé — 3 cas d'étude, du cadrage au pilotage de programme

Trois cas d'étude progressifs qui montrent une démarche complète de chef de projet data,
appliquée au milieu hospitalier. Chaque cas a sa page en ligne, ses données et ses calculs.

| Niveau | Cas | Ce qu'il démontre | Page en ligne |
|---|---|---|---|
| 1 · Simple | [Cadrage d'un projet de tableau de bord](01-cadrage/) | Note de cadrage, objectifs SMART, périmètre, jalons, **RACI** (contrôle automatique), budget, risques | [Voir](https://portfolio-fiacre-yehossou.vercel.app/gestion-projet-1-cadrage.html) |
| 2 · Intermédiaire | [Planification d'un déploiement logiciel](02-planification/) | Découpage en 20 tâches, **chemin critique (CPM)** calculé en Python, **Gantt**, registre et matrice des risques, budget par phase | [Voir](https://portfolio-fiacre-yehossou.vercel.app/gestion-projet-2-planification.html) |
| 3 · Complet | [Pilotage d'un programme data en Agile](03-pilotage-programme/) | Scrum (vélocité, burn-up, fiabilité des engagements), **valeur acquise** (SPI, CPI, EAC, TCPI), météo des chantiers, risques, journal des décisions, **conformité RGPD** des données de santé | [Voir](https://portfolio-fiacre-yehossou.vercel.app/gestion-projet-3-pilotage.html) |

> 🔒 **Cas fictifs, conformes au RGPD.** Établissement, personnes, montants et dates sont inventés.
> Les dépôts ne contiennent **aucune donnée patient ni donnée personnelle**.

## Résultats clés

**1. Cadrage** : budget estimé de 29,6 k€ (+ 10 % de réserve), 7 jalons dont 2 Go / No-go, RACI vérifié
(un seul responsable « A » par activité).

**2. Planification** : 65 jours ouvrés sur le chemin critique (16 tâches critiques sur 20), budget de 48,5 k€,
3 risques élevés ou critiques. Le risque n°1 porte sur une tâche qui n'a que 3 jours de marge.

**3. Pilotage** : à mi-parcours, SPI 0,85 et CPI 0,90 ; coût final estimé à 266 k€ pour un budget de 240 k€ ;
6 sprints nécessaires au lieu de 4 à la vélocité actuelle. La page propose un arbitrage chiffré au comité
(délai, budget ou périmètre).

## Structure

```
├── build.py                       # calculs (budget, RACI, CPM, valeur acquise, vélocité) + génération des pages
├── commun/                        # styles et graphiques partagés (HTML/CSS/JS sans dépendance)
├── 01-cadrage/                    # note_de_cadrage.md, data/*.csv, index.html
├── 02-planification/              # data/taches.csv, data/risques.csv, planning_calcule.csv, index.html
└── 03-pilotage-programme/         # data/*.csv, indicateurs_valeur_acquise.csv, prevision_agile.csv, index.html
```

## Lancer

```bash
pip install -r requirements.txt
python build.py
```

## Méthodes et formules

- **Chemin critique (CPM)** : passe avant (dates au plus tôt), passe arrière (dates au plus tard), marge totale = début au plus tard − début au plus tôt ; une tâche est critique si sa marge est nulle.
- **Valeur acquise** : SPI = EV / PV ; CPI = EV / AC ; EAC = BAC / CPI ; VAC = BAC − EAC ; TCPI = (BAC − EV) / (BAC − AC).
- **Prévision Agile** : sprints restants = points restants / vélocité moyenne des 3 derniers sprints.
- **Risques** : score = probabilité × impact (1 à 25), stratégie (éviter, réduire, transférer, accepter) et propriétaire.

---
Projet réalisé par **Fiacre Yehossou** — Data Analyst | Data Steward | Business Analyst ·
[Portfolio](https://portfolio-fiacre-yehossou.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/fiacre-yehossou)
