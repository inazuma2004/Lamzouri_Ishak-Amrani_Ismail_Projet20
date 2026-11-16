# incidentsIT : agent de résolution d'incidents IT (projet 20)

> **Module :** Développement et déploiement d'applications intelligentes, 2026-2027
> **Enseignant :** A. Larhlimi
> **Groupe :** G3, IAD (IA et Data)
> **Sujet :** n° 20 du catalogue, « Agent autonome de résolution d'incidents IT » ; fiche de cadrage : [`Lamzouri-Amrani_Projet20.md`](Lamzouri-Amrani_Projet20.md)

| Membre | Compte GitHub | Rôle principal |
| --- | --- | --- |
| Ishak Lamzouri | [@inazuma2004](https://github.com/inazuma2004) | dépôt et intégration continue, seuil d'abstention, interface Streamlit, équipe d'agents, Docker |
| Ismail Amrani | [@Amaranix](https://github.com/Amaranix) | données, modèle de classification, API FastAPI, recherche dans les runbooks, paquet et commande `incidents`, suite de tests |

## Ce que fait l'application

Un technicien du helpdesk colle la description d'un ticket, rédigée en anglais comme les tickets
d'entraînement. L'application :

1. classe le ticket dans l'une des 8 catégories du dataset, avec un score de confiance ;
2. sous un score de 0,60, ne décide pas : le ticket est marqué `A_VERIFIER` et confié à un
   technicien ;
3. fixe une priorité de P1 à P4 par des règles métier écrites (un utilisateur bloqué donne P2) ;
4. cite, mot pour mot, la section de runbook qui s'applique (`Access.md > Compte verrouillé`),
   ou n'en cite aucune si aucune section ne dépasse le seuil de pertinence ;
5. fait contrôler la réponse par un agent vérificateur (source citée, équipe d'escalade, aucune
   consigne recopiée depuis le ticket) avant de l'afficher.

Exemple : « Cannot connect to the VPN since this morning, my password expired » donne
`Access`, confiance 88 %, priorité `P2`, statut `VALIDE`, section
« Access.md > Connexion VPN impossible ».

Le jeu de données ne contient que des tickets en anglais : un ticket rédigé dans une autre langue
part chez un technicien. L'application ne répare rien elle-même ; elle propose une procédure.

## Installation

Python 3.13 (les versions de `requirements.txt` sont celles qui ont entraîné le modèle).
Compter environ 2 Go et une dizaine de minutes : PyTorch est installé en version CPU, sans CUDA.

```powershell
git clone https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20.git
cd Lamzouri_Ishak-Amrani_Ismail_Projet20
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1                    # Linux, macOS : source .venv/bin/activate
pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
copy .env.example .env                          # Linux, macOS : cp .env.example .env
```

`.env` reste sur le poste (il est dans `.gitignore`). Remplacer les deux clés d'exemple par des
valeurs d'au moins 16 caractères :
`python -c "import secrets; print(secrets.token_urlsafe(24))"`.

## Avancement du dépôt

Le dépôt suit la liste des 18 push du cours (six par semaine, une branche et une pull request
relue par l'autre membre pour chacun). L'application existe en prototype local ; son code entre
dans le dépôt push après push.

| Semaine | Push | Contenu pour ce projet | Tag |
| --- | --- | --- | --- |
| 1 | S1-1 à S1-6 | structure du dépôt, équipe, environnement figé, commande `incidents` minimale et son test, données et architecture, fiche de suivi 1 | `s1` |
| 2 | S2-1 à S2-6 | modèle TF-IDF + régression logistique et fonction de prédiction, jeu d'or de 20 tickets et script d'évaluation, API FastAPI, interface Streamlit, CI (pytest, Ruff), fiche 2 | `s2` |
| 3 | S3-1 à S3-6 | cas limites (texte vide, score faible, service indisponible), évaluation finale, installation sur clone neuf et Docker, documentation finale, fiche 3, compte rendu et support, release | `v1.0.0` |

Les mesures citées dans la fiche de cadrage (F1 macro 0,868, couverture 78,4 %, précision des
tickets traités seuls 94,2 %) viennent du prototype local, sur 9 568 tickets de test. Elles
deviennent reproductibles dans ce dépôt avec les scripts d'évaluation du push S2-2.

## Données

[IT Service Ticket Classification Dataset](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset)
(Kaggle, licence CC0) : 47 837 tickets, 2 colonnes (`Document` : texte du ticket, déjà nettoyé, en
minuscules et presque sans ponctuation ; `Topic_group` : catégorie), aucune valeur manquante,
aucun doublon.

| Catégorie | Tickets | Part |
| --- | --- | --- |
| Hardware | 13 617 | 28,5 % |
| HR Support | 10 915 | 22,8 % |
| Access | 7 125 | 14,9 % |
| Miscellaneous | 7 060 | 14,8 % |
| Storage | 2 777 | 5,8 % |
| Purchase | 2 464 | 5,2 % |
| Internal Project | 2 119 | 4,4 % |
| Administrative rights | 1 760 | 3,7 % |

Le fichier complet (14 Mo) reste hors Git. Le dépôt versionne un échantillon :
[`data/sample/tickets_sample.csv`](data/sample/tickets_sample.csv), 120 tickets, 15 par
catégorie. Détails : [`data/README.md`](data/README.md).

## Pourquoi cette approche (grille du cours)

- **Pas de règles seules pour la catégorie :** un même problème s'écrit de dizaines de façons
  (« vpn down », « cannot connect remote access ») ; une liste de mots-clés ne couvre pas ces
  formulations.
- **Apprentissage supervisé pour la catégorie :**
  - (a) données étiquetées : 47 837 tickets déjà classés par des techniciens ;
  - (b) vérifiabilité : F1 macro sur un jeu de test disjoint, et mots qui ont pesé dans chaque
    décision ;
  - (c) coût et latence : sur CPU, sans GPU ni API payante, environ 2 ms par ticket (p95 mesuré
    sur le prototype) ;
  - (d) conséquence d'une erreur : un ticket mal routé perd du temps ; sous 0,60 de confiance, un
    humain tranche.
- **Règles pour la priorité, recherche documentaire (RAG extractif) pour la procédure :** la
  priorité doit s'expliquer, et la procédure doit venir d'un document interne, citée.

## Organisation du dépôt

```text
.
├── data/
│   ├── README.md                     # le dataset Kaggle : origine, colonnes, classes
│   └── sample/tickets_sample.csv     # 120 tickets, 15 par catégorie
├── docs/
│   ├── cadrage/rapport_conception_initiale.md
│   ├── media/                        # vidéos de cadrage des deux membres et leurs scripts
│   └── semaine1/                     # dossier de lancement (4 livrables) et maquettes
├── src/                              # scripts d'entraînement et d'évaluation (à partir de S2-1)
├── tests/                            # tests pytest
├── Lamzouri-Amrani_Projet20.md       # fiche de cadrage
├── modele-rapport-latex.zip          # modèle LaTeX fourni par l'enseignant pour le compte rendu
└── README.md
```

## Documents

| Document | Contenu |
| --- | --- |
| [`Lamzouri-Amrani_Projet20.md`](Lamzouri-Amrani_Projet20.md) | fiche de cadrage : besoin, périmètre, approche, critères de réussite |
| [`docs/semaine1/Dossier_de_lancement_semaine1.md`](docs/semaine1/Dossier_de_lancement_semaine1.md) | dossier de lancement : descriptif, dataset, maquettes, plan des tâches |
| [`docs/cadrage/rapport_conception_initiale.md`](docs/cadrage/rapport_conception_initiale.md) | choix de l'approche et défense du RAG extractif |
| [`docs/media/`](docs/media/) | vidéos de cadrage d'Ishak Lamzouri et d'Ismail Amrani |
