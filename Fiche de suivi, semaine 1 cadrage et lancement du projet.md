# Fiche de suivi, semaine 1 : cadrage et lancement du projet

> Copies identiques : `docs/suivi/fiche-semaine-1.md` (emplacement de la liste des push), `Fiche_de_suivi_semaine1.md` et
> `Fiche de suivi, semaine 1 cadrage et lancement du projet.md` (racine du dépôt). Corrigée le 19/11/2026 : chiffres
> recalculés par `scripts/decrire_donnees.py`, exemples tirés du fichier réel, auteurs des commits relus dans l'historique,
> interface Streamlit remplacée par une interface web React.

## 1. Identification du groupe

| Élément | Votre réponse |
| --- | --- |
| Nom du groupe | G3, IAD (IA et Data), binôme Lamzouri-Amrani |
| Titre du projet | incidentsIT : agent de résolution d'incidents IT |
| Sujet : numéro du catalogue | n° 20, « Agent autonome de résolution d'incidents IT » |
| Adresse du dépôt GitHub | https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20 |
| Enseignant ajouté au dépôt (oui ou non) | Oui : compte `@Larhlimi`, collaborateur du dépôt |
| Date de remise de la fiche | 16/11/2026 ; version corrigée le 19/11/2026 |

Membres du groupe :

| Nom et prénom | Compte GitHub | Rôle principal dans le projet |
| --- | --- | --- |
| Lamzouri Ishak | [@inazuma2004](https://github.com/inazuma2004) | dépôt et intégration continue, commande `incidents`, modèle de classification, API FastAPI, cas limites, Docker |
| Amrani Ismail | [@Amaranix](https://github.com/Amaranix) | jeu d'évaluation et mesures, interface web React, évaluation finale, documentation finale |

## 2. Sujet et besoin

| Question | Votre réponse |
| --- | --- |
| Besoin en une phrase | Le helpdesk lit et route chaque ticket à la main ; l'application classe le ticket, fixe sa priorité et cite la procédure à suivre, et signale les tickets qu'elle ne sait pas traiter. |
| Utilisateur final | Technicien de support de niveau 1, qui reçoit les tickets rédigés par les employés. |
| Ce que fait l'application, vu par l'utilisateur (3 lignes au plus) | Le technicien colle un ticket (en anglais) ou dépose un CSV. Il obtient la catégorie parmi 8, la confiance, la priorité P1 à P4 et la section de runbook citée mot pour mot. Sous 0,60 de confiance, le ticket est marqué `A_VERIFIER` et lui revient. |
| Approche retenue et raison du choix | Apprentissage supervisé (TF-IDF + régression logistique) pour la catégorie : 47 837 tickets déjà étiquetés, 1,5 ms par ticket sur CPU, mots décisifs affichables. Règles écrites pour la priorité (elle doit s'expliquer). Recherche dans les runbooks (RAG extractif) pour la procédure : le texte est recopié, pas généré. |
| Conséquence d'une erreur de l'application, et validation humaine prévue | Un ticket mal classé part vers la mauvaise équipe et attend. Garde-fous : abstention sous 0,60 (le technicien choisit la catégorie et sa correction est enregistrée), aucune procédure citée sous le seuil de pertinence 0,27, aucune action exécutée sur un poste. |
| Sujet hors catalogue | Sans objet. |

## 3. Périmètre

| Rubrique | Votre réponse |
| --- | --- |
| Version minimale : le parcours montré en semaine 2 | Le technicien colle un ticket dans l'interface web React ; elle appelle `POST /v1/predict` ; l'écran affiche la catégorie, la confiance sur une jauge marquée au seuil 0,60, et `A_VERIFIER` sous ce seuil. Même parcours en ligne de commande : `incidents predict "<ticket>"`. |
| Fonction 1, indispensable | Classer un ticket parmi les 8 catégories, avec la probabilité du modèle comme confiance. |
| Fonction 2, indispensable | S'abstenir sous 0,60 : statut `A_VERIFIER`, correction du technicien enregistrée pour le réentraînement. |
| Fonction 3, si le temps le permet | Qualifier un lot CSV, et citer la section de runbook qui s'applique (8 runbooks, 27 sections). |
| Hors périmètre | Exécuter une réparation sur un poste ; appeler un modèle de langage payant ; se connecter à un outil de ticketing (ServiceNow, Jira) ; traiter des tickets dans une autre langue que l'anglais (ils partent chez un humain). |

## 4. Architecture et technologies

| Composant | Choix prévu | Dossier ou fichier dans le dépôt |
| --- | --- | --- |
| Cœur : modèle | scikit-learn : TF-IDF (mots et paires de mots) + régression logistique, `class_weight="balanced"` | `src/train.py`, `incidents_app/predict.py` (push S2-1) |
| API | FastAPI + Pydantic v2 : `/health` public, `/v1/predict` protégé par clé, erreurs au format `{"erreur": {"code", "message"}}` | `app/` (push S2-3) |
| Interface | React 19 + Vite + TypeScript + Tailwind CSS ; construite en fichiers statiques que l'API sert sur `/` (un seul service, un seul port) | `web/` (push S2-4) |
| Données et stockage | Échantillon de 120 tickets versionné ; fichier complet hors Git (DVC) ; runbooks Markdown | `data/sample/tickets_sample.csv`, `data/runbooks/` (push S2-1 à S3-1) |
| Tests | pytest ; Ruff ; contrôle de types TypeScript au build de l'interface | `tests/`, `pyproject.toml` |
| Services externes et clés nécessaires | Aucun service payant ni appel réseau. Une clé : `API_KEYS` (accès à l'API), dans `.env`, jamais dans Git ; modèle à remplir : `.env.example` | `.env.example` |

Schéma d'architecture (Mermaid) : [`docs/architecture.md`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/blob/main/docs/architecture.md).

## 5. Données

| Question | Votre réponse |
| --- | --- |
| Origine des données (source, licence) | [IT Service Ticket Classification Dataset](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset), Kaggle (Adison Goh), licence CC0 1.0 |
| Volume disponible aujourd'hui | 47 837 tickets, fichier `all_tickets_processed_improved_v3.csv` de 14,6 Mo |
| Format | CSV UTF-8, séparateur virgule, 2 colonnes |
| Données personnelles | Non repérées : aucun chiffre, adresse e-mail ni adresse IP dans les 47 837 textes (recherche par expression régulière, 19/11/2026). Les noms propres ne se détectent pas automatiquement. |
| Jeu d'essai versionné dans le dépôt | `data/sample/tickets_sample.csv` : 120 tickets, 15 par catégorie |

### Description du jeu de données

Vue d'ensemble :

| Caractéristique | Votre réponse |
| --- | --- |
| Ce que représente une ligne | Un ticket de support IT : le texte écrit par l'employé, et la catégorie donnée par le support. |
| Nombre de lignes | 47 837 |
| Nombre de variables (colonnes) | 2 |
| Période couverte et langue | Période non indiquée par la source ; anglais. Texte déjà nettoyé : minuscules, sans ponctuation ni chiffres. |
| Variable cible | `Topic_group`, 8 catégories |
| Répartition de la cible | Hardware 13 617 (28,5 %), HR Support 10 915 (22,8 %), Access 7 125 (14,9 %), Miscellaneous 7 060 (14,8 %), Storage 2 777 (5,8 %), Purchase 2 464 (5,2 %), Internal Project 2 119 (4,4 %), Administrative rights 1 760 (3,7 %) |
| Longueur d'un ticket, en mots | moyenne 43,6 ; médiane 26 ; minimum 2 ; maximum 981 |
| Valeurs manquantes et doublons | 0 valeur manquante, 0 ligne en double : aucun traitement nécessaire |
| Découpage prévu | Test : 20 % stratifié, graine 42 (9 568 tickets), utilisé une seule fois pour le modèle retenu. Entraînement : 38 269 tickets, dont 20 % mis de côté comme validation pour choisir les réglages. |
| Script qui recalcule ces chiffres | `python scripts/decrire_donnees.py data/all_tickets_processed_improved_v3.csv` (sans argument : l'échantillon versionné) ; testé par `tests/test_decrire_donnees.py` |

Dictionnaire des variables :

| Variable | Type | Signification | Exemple de valeur | Valeurs manquantes (%) |
| --- | --- | --- | --- | --- |
| `Document` | texte | Description du problème par l'employé, nettoyée | `access to tuesday july joiner hello please confluence folder please create accounts credentials thank` | 0 |
| `Topic_group` | catégorie (8 valeurs) | Équipe ou famille de demande attribuée par le support | `Access` | 0 |

Trois exemples tirés du jeu de données (numéro de ligne du CSV, en-tête exclu, compté à partir de 0) ; la prédiction est celle du prototype local, sous le seuil 0,60 :

| Exemple (entrée) | Réponse attendue | Nature de l'exemple |
| --- | --- | --- |
| ligne 12 880 : `access to tuesday july joiner hello please confluence folder please create accounts credentials thank` | `Access` | Cas simple : prédit `Access`, confiance 0,99, traité seul. |
| ligne 20 737 : `access to thursday february pm hello want give permissions find repositories folder please help thank developer` | `Access` | Cas difficile : prédit `Storage` à 0,73, donc au-dessus du seuil ; « repositories folder » tire vers le stockage. C'est le type d'erreur que le seuil ne rattrape pas. |
| ligne 5 979 : `printer driver printer driver hello needed printer driver installed had rights logging against thank fixing best` | `Hardware` | Cas limite : confiance 0,58, juste sous 0,60 ; le ticket part chez un technicien (`A_VERIFIER`). |

Limites connues du jeu de données : classes déséquilibrées (Hardware 7,7 fois plus fréquent qu'Administrative rights) ; anglais seulement ; texte déjà nettoyé, alors qu'un ticket réel contient majuscules, chiffres et ponctuation ; étiquettes parfois discutables (tickets Outlook classés `Administrative rights`) ; 14 tickets de 2 mots seulement.

## 6. Critères de réussite

Mesures du prototype local ; elles deviennent reproductibles dans le dépôt avec le script d'évaluation du push S2-2.

| Critère | Mesure | Valeur cible | Comment vous le vérifierez |
| --- | --- | --- | --- |
| Justesse de la classification | F1 macro sur les 9 568 tickets de test | ≥ 0,85 (prototype : 0,868) | `python src/evaluate.py`, qui écrit `models/metrics.json` |
| Fiabilité quand l'application décide seule | Précision sur les tickets au-dessus de 0,60, avec au moins 70 % des tickets traités seuls | ≥ 90 % (prototype : 94,2 % sur 78,4 % des tickets) | même script ; seuil lu dans `incidents_app/predict.py` |
| Rapidité | Latence p95 de `/v1/predict` | < 100 ms (prototype : 1,5 ms) | même script, mesure sur un échantillon de tickets de test |

## 7. Répartition et planning sur 3 semaines

| Semaine | Livrable attendu | Pour notre projet, concrètement | Responsable | Tag |
| --- | --- | --- | --- | --- |
| 1 | Cadrage, dépôt initialisé, squelette exécutable | README, `.gitignore`, `requirements.txt` figé, `.env.example`, commande `incidents --version` et son test, script de description des données, schéma d'architecture, cette fiche | Ishak Lamzouri (S1-1, S1-3 à S1-5) ; Ismail Amrani (S1-2, sa ligne) ; binôme (S1-6) | `s1` |
| 2 | Version minimale de bout en bout | modèle et `incidents predict` (S2-1, Ishak) ; jeu d'or de 20 tickets et `docs/evaluation.md` (S2-2, Ismail) ; API `/health` et `/v1/predict` (S2-3, Ishak) ; interface web React reliée à l'API (S2-4, Ismail) ; CI pytest, Ruff, build de l'interface (S2-5, Ishak) ; fiche 2 (S2-6, binôme) | voir colonne précédente | `s2` |
| 3 | Application finale, documentation, compte rendu | texte vide ou trop long, API indisponible, abstention, chacun testé (S3-1, Ishak) ; évaluation finale (S3-2, Ismail) ; clone neuf et Docker (S3-3, Ishak) ; README final et `CHANGELOG.md` (S3-4, Ismail) ; fiche 3, compte rendu, support (S3-5, binôme) ; release (S3-6, binôme) | voir colonne précédente | `v1.0.0` |

Répartition des responsabilités :

| Membre | Responsabilités sur les 3 semaines | Remplaçant en cas d'absence |
| --- | --- | --- |
| Ishak Lamzouri | dépôt et CI, commande `incidents`, modèle de classification, API FastAPI, cas limites, Docker | Ismail Amrani |
| Ismail Amrani | jeu d'évaluation et mesures, interface web React, évaluation finale, documentation finale | Ishak Lamzouri |

## 8. Travail réalisé en semaine 1

Chaque membre remplit sa ligne lui-même. Commits relus dans l'historique de `main` le 19/11/2026.

| Membre | Ce que j'ai fait cette semaine | Lien vers mes commits | Temps passé (heures) |
| --- | --- | --- | --- |
| Ishak Lamzouri | S1-1 structure et README ; S1-2 ma ligne de `docs/equipe.md` ; S1-3 `requirements.txt` figé et `.env.example` ; S1-4 commande `incidents` et ses 2 tests ; S1-5 `scripts/decrire_donnees.py` et `docs/architecture.md` ; S1-6 cette fiche et les jalons ; fusion des PR #4, #6, #7 | [`e93bcc6`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/e93bcc6), [`74d1844`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/74d1844), [`53b3186`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/53b3186), [`fd3c2ce`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/fd3c2ce), [`828c968`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/828c968), [`194995b`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/194995b) | 12 |
| Ismail Amrani | Relecture et fusion de la PR #5 (commit de fusion [`1ababd0`](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20/commit/1ababd0), depuis @Amaranix). À compléter par Ismail depuis son compte, avec le commit de sa ligne de `docs/equipe.md`. | à compléter par Ismail | à compléter par Ismail |

État du dépôt à la remise de la fiche :

- [x] Dépôt créé, enseignant et tous les membres ajoutés
- [x] README avec le titre, les membres, le sujet et les commandes d'installation (S1-1)
- [ ] Au moins un commit de chaque membre, depuis son propre compte (S1-2) : Ismail n'a qu'un commit de fusion ; sa ligne de `docs/equipe.md` reste à pousser depuis @Amaranix
- [ ] `requirements.txt` installable sur un clone neuf, `.env.example` présent, aucun secret poussé (S1-3) : installation sur clone neuf à refaire et à consigner ici
- [x] Squelette exécutable et au moins un test qui passe (S1-4) : `pytest -q` donne 4 tests réussis
- [x] Jeu d'essai et schéma d'architecture dans le dépôt (S1-5)
- [ ] Cette fiche poussée dans `docs/suivi/` et tag `s1` posé (S1-6) : le tag `s1` désigne `16f0369`, avant cette correction ; à déplacer sur le commit de fusion de la correction

## 9. Risques et points de blocage

| Risque ou blocage | Probabilité | Ce que nous ferons si cela arrive | Qui surveille |
| --- | --- | --- | --- |
| Ismail sans push à son nom en semaine 1 (règle : un push par membre et par semaine) | forte | Ismail pousse sa ligne de `docs/equipe.md` depuis @Amaranix avant la remise ; il est auteur de S2-2 et S2-4 en semaine 2 | Ismail Amrani |
| Erreur sûre d'elle (au-dessus de 0,60 mais fausse), comme l'exemple de la ligne 20 737 | moyenne | Mesurer la précision des tickets traités seuls (cible ≥ 90 %) ; relever le seuil si elle passe sous la cible | Ismail Amrani |
| Installation impossible sur le poste de l'enseignant (PyTorch volumineux, Node.js absent) | moyenne | Versions figées dans `requirements.txt` et `web/package-lock.json` ; interface construite par la CI et par l'image Docker, sans Node.js chez l'utilisateur | Ishak Lamzouri |

Question à poser à l'enseignant : le tag `v1.0.0` existe déjà dans le dépôt (version du TP 4). Faut-il le supprimer pour réserver `v1.0.0` à la release finale (push S3-6), ou numéroter la release finale autrement ?

## 10. Engagements pour la semaine 2

| Engagement | Responsable | Comment on saura que c'est fait |
| --- | --- | --- |
| `incidents predict "<ticket>"` renvoie catégorie, confiance et statut (S2-1) | Ishak Lamzouri | tests du module de prédiction verts dans la CI ; exemple d'appel dans le README |
| 20 tickets avec la réponse attendue et un script qui calcule les trois critères de la rubrique 6 (S2-2) | Ismail Amrani | `tests/jeu_or.csv` et `src/evaluate.py` dans le dépôt ; première mesure écrite dans `docs/evaluation.md` |
| Interface web React reliée à `/v1/predict` : saisie d'un ticket, jauge, statut (S2-4) | Ismail Amrani | capture d'écran dans `docs/` ; démonstration en séance |

## Cadre réservé à l'enseignant

| Rubrique | Barème | Note |
| --- | --- | --- |
| Cadrage : sujet, périmètre, critères mesurables (rubriques 2, 3 et 6) | 2 |  |
| Organisation : architecture, données, rôles, planning (rubriques 4, 5 et 7) | 1 |  |
| Preuves GitHub de la semaine 1, contribution de chaque membre (rubrique 8) | 1,5 |  |
| Risques et engagements pour la semaine 2 (rubriques 9 et 10) | 0,5 |  |
| **Total** | **5** |  |

Décision : sujet validé, ou fiche à reprendre avant le :

Commentaire :
