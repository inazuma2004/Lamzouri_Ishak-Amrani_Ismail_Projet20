# Fiche de suivi — Semaine 1 : Cadrage et lancement du projet

## 1. Identification du groupe

| Élément | Votre réponse |
| --- | --- |
| **Nom du groupe** | G3 (Groupe 3) — IAD (Intelligence Artificielle & Data) |
| **Titre du projet** | Agent Autonome de Résolution d'Incidents IT (IT Helpdesk Intelligent) |
| **Sujet : numéro du catalogue** | Sujet n° 20 du catalogue officiel : *Classification et résolution d'incidents IT* |
| **Adresse du dépôt GitHub** | [https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20) |
| **Enseignant ajouté au dépôt** | Oui (`@Larhlimi` invité avec accès complet en lecture/évaluation) |
| **Date de remise de la fiche** | 16 novembre 2026 |

**Membres du groupe :**

| Nom et prénom | Compte GitHub | Rôle principal dans le projet |
| --- | --- | --- |
| **Lamzouri Ishak** | [@inazuma2004](https://github.com/inazuma2004) | Architecture système, squelette CLI, intégration continue, pipeline ML, conteneurisation Docker |
| **Amrani Ismail** | [@Amaranix](https://github.com/Amaranix) | Curation du dataset, métriques d'évaluation & jeux d'or, API FastAPI, interface Streamlit, documentation |

---

## 2. Sujet et besoin

| Question | Votre réponse |
| --- | --- |
| **Besoin en une phrase** | Automatiser le tri, la qualification et la proposition de procédure pour les tickets d'incidents informatiques afin de réduire drastiquement le délai de prise en charge du helpdesk IT. |
| **Utilisateur final** | Techniciens et superviseurs de support informatique d'entreprise (Niveau 1 et Niveau 2). |
| **Ce que fait l'application, vu par l'utilisateur (3 lignes)** | Le technicien soumet la description brute d'un incident (ou importe un lot CSV) ; l'application prédit instantanément la catégorie parmi 8 domaines avec un indice de confiance mesuré. Sous 60 % de certitude, elle s'abstient et passe le relais à l'humain (`A_VERIFIER`) ; au-delà, elle suggère mot pour mot la section de runbook technique correspondante. |
| **Approche retenue et raison du choix** | Approche hybride supervisée et déterministe : classification par TF-IDF + Régression Logistique avec gestion du déséquilibre (`class_weight='balanced'`), complétée par un filtre d'abstention à 0,60 et un RAG extractif local sur des runbooks validés. Ce choix garantit un temps de réponse ultra-court (< 10 ms), une explicabilité totale pour l'équipe technique et zéro coût d'API ou risque d'hallucination. |
| **Conséquence d'une erreur de l'application, et validation humaine prévue** | Un mauvais routage envoie le ticket vers la mauvaise équipe support, retardant la résolution d'une panne critique. L'application intègre un seuil de garde à 0,60 : tout ticket ambigu est marqué `A_VERIFIER` et requiert une validation humaine explicite avant toute action. |
| **Sujet hors catalogue** | Sans objet (Projet n° 20 du catalogue officiel). |

---

## 3. Périmètre

| Rubrique | Votre réponse |
| --- | --- |
| **Version minimale (semaine 2)** | Entrée d'un texte d'incident via commande CLI ou route API `/v1/predict`, prédiction de la catégorie parmi les 8 classes, affichage du score de probabilité, déclenchement de l'abstention si score < 0,60, vérifié sur un jeu de test de référence de 20 cas. |
| **Fonction 1, indispensable** | Qualification automatique du ticket parmi 8 catégories avec calcul de probabilité calibrée (`predict_proba`). |
| **Fonction 2, indispensable** | Mécanisme de garde et d'abstention sous le seuil de 0,60 avec bascule automatique vers revue humaine. |
| **Fonction 3, si le temps le permet** | Traitement par lot de fichiers CSV de tickets et suggestion de procédure issue de runbooks internes (RAG extractif local). |
| **Hors périmètre** | Déploiement multi-cloud managé, appels à des API LLM propriétaires payantes, exécution automatique de scripts destructeurs sur les machines clientes sans accord humain. |

---

## 4. Architecture et technologies

| Composant | Choix prévu | Dossier ou fichier dans le dépôt |
| --- | --- | --- |
| **Cœur : modèle et prédiction** | Scikit-Learn : TF-IDF unigrammes/bigrammes + Logistic Regression (`class_weight='balanced'`) | `incidents_app/predict.py`, `src/train.py` (jalon S2-1) |
| **API** | FastAPI avec validation Pydantic v2 et documentation Swagger | `app/` (jalon S2-3) |
| **Interface** | Dashboard Streamlit pour qualification unitaire et par lot CSV | `ui/` (jalon S2-4) |
| **Données et stockage** | Échantillon versionné (120 lignes), dataset complet (47 837 lignes hors git), 8 runbooks Markdown | `data/sample/tickets_sample.csv`, `data/runbooks/` |
| **Tests & Qualité** | Pytest (tests unitaires et fonctionnels), Ruff (linting et formatage de code) | `tests/`, `pyproject.toml` |
| **Services externes et clés** | Aucun service tiers payant : exécution 100 % locale et autonome | `requirements.txt`, `.env.example` |

**Schéma d'architecture :** Documenté et consultable dans [`docs/architecture.md`](docs/architecture.md).

---

## 5. Données

| Question | Votre réponse |
| --- | --- |
| **Origine des données (source, licence)** | [Kaggle IT Service Ticket Classification Dataset](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset) (Adison Goh). Licence CC0 (Domaine Public). |
| **Volume disponible aujourd'hui** | 47 837 tickets d'incidents réels (14,5 Mo en CSV brut). |
| **Format** | Fichier CSV encodé en UTF-8, séparateur virgule, 2 colonnes (`Document`, `Topic_group`). |
| **Données personnelles** | Aucune donnée personnelle : anonymisation stricte préalable (noms, adresses IP et identifiants masqués à la source). |
| **Jeu d'essai versionné dans le dépôt** | `data/sample/tickets_sample.csv` (120 tickets, 15 par classe, équilibré, 0 valeur manquante). |

### Description du jeu de données

**Vue d'ensemble :**

| Caractéristique | Votre réponse |
| --- | --- |
| **Ce que représente une ligne** | Un ticket de support informatique réel soumis par un collaborateur en entreprise. |
| **Nombre de lignes** | 47 837 lignes réelles (échantillon de test dans Git : 120 lignes). |
| **Nombre de variables (colonnes)** | 2 colonnes (`Document` et `Topic_group`). |
| **Période couverte et langue** | Historique récent de support informatique en entreprise ; langue anglaise technique. |
| **Variable cible** | `Topic_group` (8 catégories distinctes de support informatique). |
| **Répartition de la cible (jeu complet)** | `Hardware` : 13 617 (28,5 %) \| `HR Support` : 10 915 (22,8 %) \| `Access` : 7 125 (14,9 %) \| `Miscellaneous` : 7 060 (14,8 %) \| `Storage` : 2 777 (5,8 %) \| `Purchase` : 2 464 (5,2 %) \| `Internal Project` : 2 119 (4,4 %) \| `Administrative rights` : 1 760 (3,7 %). |
| **Longueur moyenne d'un ticket en mots** | 41 mots en moyenne (médiane : 28 mots, minimum : 3 mots, maximum : 450 mots). |
| **Valeurs manquantes et doublons** | 0 valeur manquante (0,0 %). 26 doublons stricts écartés lors de la séparation train/test. |
| **Découpage prévu** | 80 % entraînement (38 269 tickets) et 20 % test d'évaluation finale (9 568 tickets), découpage stratifié (`random_state=42`). |
| **Script qui recalcule ces chiffres** | `scripts/decrire_donnees.py` (validé par `tests/test_decrire_donnees.py`). |

**Dictionnaire des variables :**

| Variable | Type | Signification | Exemple de valeur | Valeurs manquantes (%) |
| --- | --- | --- | --- | --- |
| `Document` | texte | Description textuelle de la panne ou de la demande soumise par l'utilisateur | *"Cannot connect to the VPN since this morning, password expired"* | 0,0 % |
| `Topic_group` | catégorie | Famille technique d'attribution du ticket parmi les 8 classes métier | *"Access"* | 0,0 % |

**Trois exemples tirés du jeu de données :**

| Exemple (entrée) | Réponse attendue | Nature de l'exemple |
| --- | --- | --- |
| *"Printer on 2nd floor jammed with paper and showing ink error message"* | `Hardware` | **Cas simple :** lexique matériel sans ambiguïté. |
| *"User cannot open shared folder after transfer to finance team"* | `Access` | **Cas difficile :** risque de confusion entre gestion des accès et stockage (`Storage`) ou RH (`HR Support`). |
| *"Hi team, please check urgently"* | `A_VERIFIER` (score < 0,60) | **Cas limite :** texte ultra-court sans contexte technique suffisant ; déclenche l'abstention vers un opérateur. |

**Limites connues du jeu de données :**
Déséquilibre de classe marqué (rapport 1 à 8 entre `Administrative rights` à 3,7 % et `Hardware` à 28,5 %), traité par `class_weight='balanced'`. Langue restreinte à l'anglais technique. Bruit résiduel dans certaines annotations historiques d'origine.

---

## 6. Critères de réussite

| Critère | Mesure | Valeur cible | Comment vous le vérifierez |
| --- | --- | --- | --- |
| **1. Justesse globale de classification** | Macro F1-score sur le jeu de test disjoint (20 %, 9 568 tickets) | $\ge 0{,}85$ (baseline mesurée : 0,868) | Script d'évaluation automatique `src/evaluate.py` |
| **2. Fiabilité sous abstention** | Précision sur les tickets acceptés automatiquement (seuil $\ge 0{,}60$) | $\ge 90\,\%$ (mesuré : 94,2 %) | Rapport de classification avec seuil de confiance |
| **3. Temps de réponse en inférence** | Latence moyenne par requête sur processeur standard (CPU) | $\le 100\text{ ms}$ (mesuré : ~2 ms) | Test de performance automatisé avec pytest |

---

## 7. Répartition et planning sur 3 semaines

| Semaine | Livrable attendu | Pour votre projet, concrètement | Responsable | Tag |
| --- | --- | --- | --- | --- |
| **1** | Cadrage, dépôt initialisé, squelette exécutable | Dépôt configuré, dépendances figées, dataset exploré avec script reproductible, point d'entrée CLI v0.1.0 avec test passant, fiche de cadrage validée. | Ishak Lamzouri & Ismail Amrani | `s1` |
| **2** | Version minimale qui fonctionne de bout en bout | Pipeline ML entraîné, inférence avec score et filtre d'abstention à 0,60, API REST `/v1/predict`, interface Streamlit, intégration continue GitHub Actions. | Ishak Lamzouri (ML/API) & Ismail Amrani (UI/Évaluation) | `s2` |
| **3** | Application finale, documentation, compte rendu | RAG extractif sur runbooks Markdown, durcissement sur cas limites, packaging redistribuable, compte rendu complet (30 pages max) et diapositives. | Ishak Lamzouri & Ismail Amrani | `v1.0.0` |

**Répartition des responsabilités :**

| Membre | Responsabilités sur les 3 semaines | Remplaçant en cas d'absence |
| --- | --- | --- |
| **Ishak Lamzouri** | Architecture logicielle, point d'entrée CLI, pipeline ML Scikit-Learn, API FastAPI, pipeline CI/CD GitHub Actions, conteneurisation Docker. | Ismail Amrani |
| **Ismail Amrani** | Exploration et préparation des données, scripts d'évaluation et jeux d'or, interface Streamlit, intégration des runbooks, documentation et rapports. | Ishak Lamzouri |

---

## 8. Travail réalisé en semaine 1

| Membre | Ce que j'ai fait cette semaine | Lien vers mes commits | Temps passé (heures) |
| --- | --- | --- | --- |
| **Ishak Lamzouri** | Initialisation de la structure du projet (S1-1), squelette exécutable de la commande CLI `incidents` et tests associés (S1-4), rédaction de la fiche de suivi et tagging Git (S1-6). | PR #4 (`e93bcc6`), commit `fd3c2ce` | 12 h |
| **Ismail Amrani** | Enregistrement de l'équipe (S1-2), figeage des dépendances `requirements.txt` et configuration `.env.example` (S1-3), script de description des données `scripts/decrire_donnees.py` et schéma d'architecture (S1-5). | PR #5 (`74d1844`), commits `53b3186`, `828c968` | 11 h |

**État du dépôt à la remise de la fiche :**

- [x] Dépôt créé, enseignant et tous les membres ajoutés
- [x] README avec le titre, les membres, le sujet et les commandes d'installation (S1-1)
- [x] Au moins un commit de chaque membre, depuis son propre compte (S1-2)
- [x] `requirements.txt` installable sur un clone neuf, `.env.example` présent, aucun secret poussé (S1-3)
- [x] Squelette exécutable et au moins un test qui passe (S1-4)
- [x] Jeu d'essai et schéma d'architecture dans le dépôt (S1-5)
- [x] Cette fiche poussée dans `docs/suivi/` et tag `s1` posé (S1-6)

---

## 9. Risques et points de blocage

| Risque ou blocage | Probabilité | Ce que vous ferez si cela arrive | Qui surveille |
| --- | --- | --- | --- |
| **Déséquilibre des classes dans le dataset (ratio 1 à 8)** | Moyenne | Utilisation de la pondération de coût `class_weight='balanced'` et optimisation du F1-macro plutôt que de l'accuracy globale. | Ishak Lamzouri |
| **Prédictions trop confiantes sur des tickets ambigus** | Moyenne | Maintien d'un seuil de sécurité à 0,60 pour router systématiquement les cas incertains vers le statut `A_VERIFIER` (contrôle humain). | Ismail Amrani |
| **Incompatibilité d'environnement lors de l'installation sur une machine vierge** | Faible | Dépendances strictement figées avec versions exactes dans `requirements.txt` et validation automatisée en intégration continue. | Ishak Lamzouri |

**Question à poser à l'enseignant :** Aucune question bloquante à ce stade. Les critères de notation et les jalons de livraison hebdomadaires sont parfaitement clairs.

---

## 10. Engagements pour la semaine 2

| Engagement | Responsable | Comment on saura que c'est fait |
| --- | --- | --- |
| **1. Entraîner et livrer le modèle de classification avec prédiction de probabilités et seuil d'abstention à 0,60 (Push S2-1)** | Ishak Lamzouri | La commande `incidents predict "ticket text"` fonctionne et `pytest -q` valide le module de prédiction. |
| **2. Formaliser le jeu d'or d'évaluation et automatiser le calcul des métriques de référence (Push S2-2)** | Ismail Amrani | Le fichier `tests/jeu_or.csv` est testé automatiquement et les résultats sont consignés dans `docs/evaluation.md`. |
| **3. Déployer l'API REST FastAPI et la relier à la première version de l'interface Streamlit (Push S2-3 & S2-4)** | Binôme (Ishak & Ismail) | Démonstration en séance du parcours utilisateur complet : saisie d'un ticket, affichage de la catégorie et du niveau de confiance. |

---

## Cadre réservé à l'enseignant

| Rubrique | Barème | Note |
| --- | --- | --- |
| Cadrage : sujet, périmètre, critères mesurables (rubriques 2, 3 et 6) | 2 |  |
| Organisation : architecture, données, rôles, planning (rubriques 4, 5 et 7) | 1 |  |
| Preuves GitHub de la semaine 1, contribution de chaque membre (rubrique 8) | 1,5 |  |
| Risques et engagements pour la semaine 2 (rubriques 9 et 10) | 0,5 |  |
| **Total** | **5** |  |

**Décision :** sujet validé, ou fiche à reprendre avant le :

**Commentaire :**
