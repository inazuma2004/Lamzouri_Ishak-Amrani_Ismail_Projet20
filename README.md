# 🤖 Agent Autonome de Résolution d'Incidents IT (IT Helpdesk Intelligent)

> **Module :** Développement et déploiement d’applications intelligentes (2026-2027)  
> **Enseignant :** M. A. Larhlimi  
> **Équipe de développement (Binôme) :**
> - **Ishak Lamzouri** ([@inazuma2004](https://github.com/inazuma2004))
> - **Ismail Amrani** ([@Amaranix](https://github.com/Amaranix))  
> **Dépôt officiel GitHub :** [https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20)  
> **Jalon actuel :** Semaine 1 — Cadrage & Dossier de lancement (Étiquette : `semaine1-remis`)

---

## 📌 Présentation du Projet

Ce projet a pour objectif de concevoir, déployer et exploiter en production un **système intelligent et agentique dédié à la gestion autonome d'incidents informatiques (IT Helpdesk)**. 

Conformément à la grille de cadrage méthodologique du cours, notre architecture logicielle combine deux mondes complémentaires :
1. **Une brique de Machine Learning classique (NLP supervisé)** pour classifier et router instantanément les descriptions d'incidents utilisateurs vers la bonne catégorie avec un calcul de score d'incertitude.
2. **Une brique IA Agentique et Mini-RAG** où l'agent autonome prend en charge la catégorie qualifiée, extrait la procédure de dépannage adéquate (runbook) depuis une base vectorielle, et fournit la solution directement à l'utilisateur.

---

## 📁 Livrables Officiels — Semaine 1 (Cadrage & Lancement)

L'ensemble des livrables de cadrage et de lancement exigés par l'enseignant pour la Semaine 1 sont accessibles directement ci-dessous :

| Livrable | Description | Emplacement dans le dépôt |
| :--- | :--- | :--- |
| **Dossier de lancement** | Dossier complet consolidé (Livrables 1, 2, 3 et 4) | [`docs/semaine1/Dossier_de_lancement_semaine1.md`](docs/semaine1/Dossier_de_lancement_semaine1.md) |
| **Fiche de cadrage** | Fiche officielle du binôme pour le Projet 20 | [`Lamzouri-Amrani_Projet20.md`](Lamzouri-Amrani_Projet20.md) |
| **Échantillon de données** | Échantillon représentatif réel (120 lignes, 8 classes équilibrées) | [`data/sample/tickets_sample.csv`](data/sample/tickets_sample.csv) |
| **Rapport de conception** | Étude de cadrage initial et analyse des besoins | [`docs/cadrage/rapport_conception_initiale.md`](docs/cadrage/rapport_conception_initiale.md) |
| **Vidéos de cadrage** | Enregistrements de soutenance des deux membres | [`docs/media/`](docs/media/) |
| **Modèle de rapport** | Archive modèle LaTeX fournie pour les rapports | [`modele-rapport-latex.zip`](modele-rapport-latex.zip) |

---

## 🎬 Vidéos de Soutenance & Cadrage Initial

Dans le cadre du premier livrable (Cadrage et Choix d'Approche), les deux vidéos de présentation du binôme sont disponibles dans [`docs/media/`](docs/media/) :
* 📹 **Vidéo d'Ismail Amrani :** [`docs/media/presentation_cadrage_Amrani_Ismail.mp4`](docs/media/presentation_cadrage_Amrani_Ismail.mp4)
* 📹 **Vidéo d'Ishak Lamzouri :** [`docs/media/presentation_cadrage_Lamzouri_Ishak.mp4`](docs/media/presentation_cadrage_Lamzouri_Ishak.mp4)
* 📜 **Scripts minutés et argumentations scientifiques :** [`docs/media/README.md`](docs/media/README.md)

---

## 📊 Le Dataset Retenu

* **Nom :** [IT Service Ticket Classification Dataset sur Kaggle](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset)
* **Volumétrie :** 47 837 tickets réels d'assistance informatique (anonymisés, licence CC0 Domaine Public)
* **Format :** CSV (`Document`, `Topic_group`)
* **Classes cibles (8) :** `Hardware`, `Access`, `Storage`, `HR Support`, `Purchase`, `Internal Project`, `Administrative rights`, `Miscellaneous`.
* **Échantillon versionné :** [`data/sample/tickets_sample.csv`](data/sample/tickets_sample.csv) (120 tickets, 15 par classe, 25 Ko).
* **Documentation du dataset :** [`data/README.md`](data/README.md)

---

## 🎯 Justification Scientifique de l'Approche (Grille du Cours)

En suivant l'arbre décisionnel officiel de **M. Larhlimi** :
- **Pourquoi pas de simples Règles Métier ?** La diversité linguistique et le jargon des utilisateurs rendent la formulation des pannes non figée et non déterministe.
- **Pourquoi le Machine Learning Supervisé pour la classification ?**
  - **Critère (a) - Données étiquetées :** Nous disposons de 47 800+ tickets déjà annotés par des techniciens.
  - **Critère (b) - Vérifiabilité :** Évaluation sur un jeu de test disjoint via $F_1$-score macro et audit des n-grammes TF-IDF.
  - **Critère (c) - Coût et Latence :** L'inférence sur CPU prend moins de 5 millisecondes avec une empreinte mémoire minime, évitant tout GPU payant en production.
  - **Critère (d) - Conséquence d'une erreur :** Risque faible, sécurisé dans l'interface par un seuil d'incertitude (60%) réorientant les cas ambigus vers un opérateur humain (`A_VERIFIER`).

---

## 📂 Organisation du Dépôt — Semaine 1

```text
projet_incidentsIT/
├── data/
│   ├── README.md               # Guide et spécification du dataset Kaggle
│   └── sample/
│       ├── README.md           # Description de l'échantillon
│       └── tickets_sample.csv  # Échantillon réel (120 lignes, 8 classes)
├── docs/
│   ├── cadrage/
│   │   └── rapport_conception_initiale.md  # Rapport initial d'étude
│   ├── media/
│   │   ├── presentation_cadrage_Amrani_Ismail.mp4
│   │   ├── presentation_cadrage_Lamzouri_Ishak.mp4
│   │   └── README.md           # Scripts minutés des vidéos
│   └── semaine1/
│       ├── README.md           # Tableau de répartition Rédacteur / Relecteur
│       ├── 1-descriptif.md     # Livrable 1 : Descriptif mis à jour
│       ├── 2-dataset.md        # Livrable 2 : Description du dataset
│       ├── 3-maquette.md       # Livrable 3 : Schéma Mermaid et wireframes
│       ├── 4-pipeline.md       # Livrable 4 : 12 tâches et Gantt
│       ├── Dossier_de_lancement_semaine1.md  # Version consolidée intégrale
│       └── img/                # Maquettes des 3 écrans (PNG)
│           ├── ecran1_qualification.png
│           ├── ecran2_incertitude.png
│           └── ecran3_batch.png
├── Lamzouri-Amrani_Projet20.md # Fiche de cadrage officielle du binôme
├── modele-rapport-latex.zip    # Modèle de rapport LaTeX
├── .gitignore                  # Exclusion stricte des artefacts lourds
└── README.md                   # Ce fichier de présentation
```

---

## 👥 Auteurs (Binôme)
- **Ishak Lamzouri** ([@inazuma2004](https://github.com/inazuma2004)) — `lamzouriishak@gmail.com`
- **Ismail Amrani** ([@Amaranix](https://github.com/Amaranix)) — `amranix33@gmail.com`
