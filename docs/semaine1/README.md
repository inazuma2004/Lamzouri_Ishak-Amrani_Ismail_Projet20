# Dossier de lancement (semaine 1) — Agent Autonome d'Incidents IT

**Date de cadrage :** 09 Novembre 2026  
**Module :** Développement et déploiement d’applications intelligentes  
**Enseignant :** M. A. Larhlimi  
**Dépôt GitHub officiel :** [https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20)  
**Branche principale :** `main`

---

## 👥 Notre répartition (Équipe de 2 étudiants)

| Livrable | Rédacteur | Relecteur | Fichier dans le dépôt |
| --- | --- | --- | --- |
| **1. Descriptif du projet** | Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004)) | Ismail Amrani ([@Amaranix](https://github.com/Amaranix)) | `docs/semaine1/1-descriptif.md` |
| **2. Dataset** | Ismail Amrani ([@Amaranix](https://github.com/Amaranix)) | Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004)) | `docs/semaine1/2-dataset.md` + `data/sample/` |
| **3. Maquette globale** | Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004)) | Ismail Amrani ([@Amaranix](https://github.com/Amaranix)) | `docs/semaine1/3-maquette.md` + `docs/semaine1/img/` |
| **4. Pipeline des tâches** | Ismail Amrani ([@Amaranix](https://github.com/Amaranix)) | Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004)) | `docs/semaine1/4-pipeline.md` |

---

## 📁 Organisation des Fichiers

```text
docs/semaine1/
├── README.md                          <- Synthèse et répartition (ce fichier)
├── 1-descriptif.md                    <- Livrable 1 : Descriptif détaillé du projet
├── 2-dataset.md                       <- Livrable 2 : Description, analyse et qualité du dataset
├── 3-maquette.md                      <- Livrable 3 : Architecture système et maquettes d'écrans
├── 4-pipeline.md                      <- Livrable 4 : Découpage WBS, jalons et Gantt
└── img/                               <- Wireframes PNG des 3 écrans (générés par script)
    ├── ecran1_qualification.png
    ├── ecran2_incertitude.png
    └── ecran3_batch.png

Dossier_de_lancement_semaine1.md       <- à la racine du dépôt : version consolidée des 4 livrables
data/sample/
├── tickets_sample.csv                 <- Échantillon représentatif réel (120 lignes, 8 classes)
└── README.md                          <- Documentation de l'échantillon
```

---

## 🎯 Statut d'avancement de l'équipe

- **Semaine 1 (Cadrage & Dataset) :** les 4 livrables remis le 09/11/2026 (étiquette `semaine1-remis`) ; décision de l'enseignant à reporter dans le dossier de lancement.
- **Dépôt Git & Hygiène :** `.gitignore` (ni `.env`, ni modèle, ni CSV complet) ; configuration pytest, Ruff et mypy dans `pyproject.toml` ; 4 tests (`pytest -q`).
- **Échantillon de données :** Présent dans `data/sample/tickets_sample.csv` (33 Ko, 120 tickets équilibrés).
- **Maquette :** 3 wireframes PNG dans `docs/semaine1/img/` (qualification, incertitude, batch CSV).
- **Prototype :** application complète sur le poste de développement (modèle, API FastAPI, interface web React, RAG extractif) ; son code entre dans le dépôt push après push, à partir de S2-1 ([`Jalons_Push_GitHub_Projet20.md`](../../Jalons_Push_GitHub_Projet20.md)).
- **Défense du RAG :** [`docs/cadrage/rapport_conception_initiale.md`, section 6](../cadrage/rapport_conception_initiale.md#6-défense-du-rag-extractif-semaines-9-10) : critères (b) et (c), coûts mesurés, limites.

---

## ✅ Checklist de remise (Coordinateur)

- [x] `docs/semaine1/README.md` avec la répartition rédacteurs et relecteurs.
- [x] Les quatre livrables rédigés, revus et fusionnés sur la branche principale.
- [x] Échantillon de données présent dans `data/sample/tickets_sample.csv`.
- [x] Schéma d'architecture Mermaid et parcours utilisateur visibles sur GitHub.
- [x] Wireframes PNG des 3 écrans dans `docs/semaine1/img/`.
- [x] Pipeline chronologique défini (`4-pipeline.md`, diagramme de Gantt).
- [x] Dossier complet consolidé : [`Dossier_de_lancement_semaine1.md`](../../Dossier_de_lancement_semaine1.md), à la racine.

