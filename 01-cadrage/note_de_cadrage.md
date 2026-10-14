# Note de cadrage — Tableau de bord des approvisionnements de la pharmacie

> Cas d'étude **fictif** (établissement, personnes, montants et dates inventés). Aucune donnée patient ni donnée personnelle.

| | |
|---|---|
| **Sponsor** | Directeur des achats |
| **Chef de projet** | Chef de projet data |
| **Durée** | 12 semaines |
| **Budget** | 29,6 k€ estimés + réserve de 10 % (3 k€), plafond 33 k€ |
| **Version** | 1.0 — validée en comité de pilotage (semaine 2) |

## 1. Contexte et problème
La pharmacie produit son reporting d'approvisionnement à la main à partir de plusieurs extractions Excel :
2 jours de travail par mois, des chiffres qui diffèrent selon les services et aucune alerte avant les ruptures.

## 2. Objectifs SMART
1. Publier un tableau de bord hebdomadaire couvrant **100 % des références critiques** d'ici la semaine 11.
2. Réduire le temps de production du reporting mensuel de **2 jours à 1 jour** dans les 3 mois suivant la mise en production.
3. Atteindre **80 % d'utilisateurs actifs** parmi les 15 utilisateurs cibles à M+2.

## 3. Périmètre
- **Inclus :** stocks, consommations, commandes et fournisseurs de la pharmacie ; 3 services pilotes.
- **Exclu :** données patients, prescriptions, facturation, autres établissements.

## 4. Livrables
Note de cadrage · spécifications fonctionnelles et dictionnaire des KPI · modèle de données · tableau de bord ·
guide utilisateur · PV de recette · rapport de clôture.

## 5. Contraintes et hypothèses
- Budget plafond 33 k€ réserve comprise ; chef de projet à 60 %, développeur BI à 50 %, référents métiers 2 jours par mois.
- **RGPD :** aucune donnée personnelle dans le tableau de bord (principe de minimisation) ; DPO consulté dès le cadrage.
- Hypothèse : accès en lecture aux bases achats accordé avant la semaine 3.

## 6. Jalons et décisions
Voir [`data/jalons.csv`](data/jalons.csv) : 7 jalons, dont 2 décisions Go / No-go (cadrage, mise en production).

## 7. Organisation et RACI
Voir [`data/raci.csv`](data/raci.csv). Règle vérifiée par `build.py` : **un seul « A » par activité** et au moins un « R ».

## 8. Gouvernance
- Comité de pilotage toutes les 3 semaines (sponsor, pharmacien gérant, chef de projet, DSI).
- Point d'équipe hebdomadaire de 30 minutes, tableau de suivi partagé.

## 9. Budget
Voir [`data/budget.csv`](data/budget.csv) et le calcul dans [`budget_calcule.csv`](budget_calcule.csv).

## 10. Risques identifiés au cadrage
Voir [`data/risques_initiaux.csv`](data/risques_initiaux.csv).

## 11. Critères de succès
Les 3 objectifs SMART sont mesurés à M+3 et présentés au sponsor dans le rapport de clôture.
