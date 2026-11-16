# Jalons & Push GitHub — Projet 20 : Incidents IT

**Binôme :** Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004)) & Ismail Amrani ([@Amaranix](https://github.com/Amaranix))  
**Groupe :** G3 — IAD  
**Sujet n° 20 :** *Agent autonome de résolution d'incidents IT*  
**Dépôt :** [https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20)

---

## 1. Calendrier des 18 Jalons et Tags

Le projet est rythmé par 18 jalons obligatoires (6 par semaine), chacun développé sur une branche dédiée puis intégré dans `main` via une Pull Request relue et validée par le binôme.

| Semaine | Objectif principal | Jalons | Tag Git associé | Statut |
| --- | --- | --- | --- | --- |
| **Semaine 1** | Cadrer le projet, initialiser le dépôt et poser le squelette exécutable | S1-1 à S1-6 | `s1` | **En cours de finalisation** |
| **Semaine 2** | Version minimale fonctionnelle de bout en bout (ML, API, UI) | S2-1 à S2-6 | `s2` | Planifié |
| **Semaine 3** | Durcissement, RAG runbooks, cas limites, packaging et livraison finale | S3-1 à S3-6 | `v1.0.0` | Planifié |

---

## 2. Détail des Jalons par Semaine

### Semaine 1 : Cadrage et démarrage (Tag `s1`)

| Jalon | Branche | Contenu ciblé pour le Projet 20 | Auteur principal | Preuve vérifiée sur GitHub |
| --- | --- | --- | --- | --- |
| **S1-1** | `s1-1-initialisation` | Structure du projet (`src/`, `tests/`, `docs/`, `data/`), `.gitignore` assaini et `README.md` initial complet. | Ishak Lamzouri | README lisible, arborescence propre (PR #4 fusionnée). |
| **S1-2** | `s1-2-equipe` | Fichier `docs/equipe.md` avec nom, compte GitHub et rôle de chaque membre. | Ismail Amrani | Commit de chaque compte dans l'historique (PR #5 fusionnée). |
| **S1-3** | `s1-3-environnement` | Fichier `requirements.txt` figé, `.env.example` sans secret, documentation des commandes d'installation. | Ismail Amrani | Installation reproductible sur clone neuf. |
| **S1-4** | `s1-4-squelette` | Commande CLI `incidents --version` (v0.1.0) dans `incidents_app/cli.py` et premier test unitaire. | Ishak Lamzouri | `pytest -q` passe avec succès sur le point d'entrée. |
| **S1-5** | `s1-5-donnees-architecture` | Échantillon représentatif `data/sample/tickets_sample.csv`, script `scripts/decrire_donnees.py` et schéma `docs/architecture.md`. | Ismail Amrani | Script exécutable recalculant les chiffres exacts (47 837 tickets, 8 classes). |
| **S1-6** | `s1-6-fiche-suivi` | Fiche de suivi `docs/suivi/fiche-semaine-1.md` et racine `Fiche_de_suivi_semaine1.md` complétées ; tag `s1`. | Binôme (Ishak & Ismail) | Tag `s1` visible sur GitHub, fiches entièrement renseignées. |

---

### Semaine 2 : Version minimale de bout en bout (Tag `s2`)

| Jalon | Branche | Contenu ciblé pour le Projet 20 | Auteur principal | Preuve attendue |
| --- | --- | --- | --- | --- |
| **S2-1** | `s2-1-coeur-ml` | Pipeline Scikit-Learn (TF-IDF + LogisticRegression), fonction `predict` et sous-commande CLI `incidents predict`. | Ishak Lamzouri | Tests de prédiction unitaires verts ; exemple dans le README. |
| **S2-2** | `s2-2-jeu-evaluation` | Jeu de test étiqueté (jeu d'or de 20 tickets), script de calcul du macro F1-score et documentation dans `docs/evaluation.md`. | Ismail Amrani | Mesure chiffrée (F1 $\ge 0{,}85$) vérifiable par script. |
| **S2-3** | `s2-3-api` | Routes FastAPI `/v1/health` et `/v1/predict`, gestion des codes d'erreur, validation Pydantic et tests d'API. | Ishak Lamzouri | Documentation OpenAPI interactive `/docs` ; tests API verts. |
| **S2-4** | `s2-4-interface` | Dashboard Streamlit relié à l'API pour la qualification unitaire d'un ticket avec jauge de confiance. | Ismail Amrani | Capture d'écran dans `docs/` et démonstration fonctionnelle en direct. |
| **S2-5** | `s2-5-qualite` | Pipeline CI GitHub Actions exécutant automatiquement Pytest et Ruff sur chaque PR. | Ishak Lamzouri | Coche verte CI sur le dernier commit de `main`. |
| **S2-6** | `s2-6-fiche-suivi` | Fiche de suivi `docs/suivi/fiche-semaine-2.md`, README mis à jour (lancement en 3 commandes), tag `s2`. | Binôme (Ishak & Ismail) | Tag `s2` poussé sur GitHub. |

---

### Semaine 3 : Finition, vérification et livraison finale (Tag `v1.0.0`)

| Jalon | Branche | Contenu ciblé pour le Projet 20 | Auteur principal | Preuve attendue |
| --- | --- | --- | --- | --- |
| **S3-1** | `s3-1-cas-limites` | Robustesse : traitement du texte vide (code 2), abstention sous 0,60, suggestion de runbook via RAG extractif. | Ishak Lamzouri | Tests pytest sur cas limites et abstention verts. |
| **S3-2** | `s3-2-evaluation-finale` | Mesures complètes sur les 9 568 tickets de test, rapport de dérive, analyse d'erreurs typiques dans `docs/evaluation.md`. | Ismail Amrani | Chiffres définitifs reproductibles. |
| **S3-3** | `s3-3-reproductibilite` | Vérification de l'installation sur clone vierge, configuration Docker et Docker Compose. | Ishak Lamzouri | Lancement complet en une seule commande conteneurisée. |
| **S3-4** | `s3-4-documentation` | `README.md` exhaustif, `CHANGELOG.md` retraçant les versions, guide d'installation hors ligne. | Ismail Amrani | Documentation complète pour utilisateur externe. |
| **S3-5** | `s3-5-documents-finaux` | Fiche de suivi semaine 3, rapport écrit final (30 pages max) et diapositives de soutenance dans `docs/`. | Binôme (Ishak & Ismail) | 3 fichiers présents et validés. |
| **S3-6** | `s3-6-release-v1` | Tag `v1.0.0` et publication de la Release GitHub avec paquet installable et notes de version. | Binôme (Ishak & Ismail) | Release officielle publiée sur GitHub. |

---

## 3. Règles d'Or et Conventions Git

1. **Format des messages de commit :** Toujours commencer par l'identifiant du jalon suivi d'un verbe à l'infinitif :
   `S1-4 : ajouter le point d'entrée incidents et son premier test`
2. **Hygiène stricte :** Aucun secret, fichier `.env`, base volumineuse ou fichier modèle binaire `.joblib` ne doit être poussé.
3. **Collaboration réelle :** Chaque membre porte ses branches depuis son propre compte GitHub et les Pull Requests sont obligatoirement relues avant fusion dans `main`.
