# Fiche de Cadrage Complète - Binôme : Lamzouri-Amrani - Projet 20

> **Version :** 1.2 — 14/11/2026  
> **Mise à jour :** le RAG est implémenté (RAG extractif local, découpé par section) et défendu dans [`docs/cadrage/rapport_conception_initiale.md`, section 6](docs/cadrage/rapport_conception_initiale.md#6-défense-du-rag-extractif-semaines-9-10) ; l'agent est devenu une équipe de cinq agents vérifiée par une boucle bornée. Les valeurs mesurées ci-dessous sont celles de l'application 1.1.0.  
> **Version 1.3 — 19/11/2026 :** l'interface Streamlit est remplacée par une interface web React servie par l'API ; les routes protégées sont sous `/v1` ; comptes `user` (technicien) et `admin` (responsable du helpdesk) avec mot de passe ; calendrier ramené à 3 semaines (consigne du 16/11/2026). Ces changements de périmètre sont soumis à la validation de l'enseignant (grille : « la fiche de cadrage fait référence »).

---

## 1. Identification du binôme
| | Membre A | Membre B |
|---|---|---|
| Nom | Lamzouri | Amrani |
| Prénom | Ishak | Ismail |
| Adresse courriel | lamzouriishak@gmail.com | amranix33@gmail.com |
| Groupe / Section | G3 — IAD (IA & Data) | G3 — IAD (IA & Data) |

---

## 2. Projet choisi
- **Numéro du projet** : 20
- **Intitulé du projet** : Agent Autonome de Résolution d'Incidents IT (IT Helpdesk Intelligent)
- **Type** : ☑ Informatique (1 à 20)  ☐ Industriel (21 à 40)
- **Catégorie** : Génie logiciel / Support informatique / NLP

---

## 3. Descriptif proposé
**Problème** : Le support informatique est submergé par des tickets récurrents (accès, matériel, mots de passe). Le routage manuel entraîne des délais critiques et des coûts opérationnels élevés.
**Utilisateurs** : Techniciens du helpdesk IT.
**Fonctionnalités** :
1. Classification automatique (8 catégories) par ML supervisé.
2. Seuil d'incertitude (60%) et abstention automatique vers un humain.
3. Résolution assistée par RAG extractif : section de runbook citée, texte verbatim, priorité P1 à P4 par règles métier, sans LLM génératif obligatoire.
4. API REST (`/v1/predict`, `/v1/resolve`) et interface web React de pilotage, servie par l'API.

**Périmètre** :
| Inclus | Exclu |
|---|---|
| Modèle ML supervisé (TF-IDF + LogReg) | Déploiement multi-cloud |
| RAG extractif local (ChromaDB + runbooks) | LLM génératif payant / API externe |
| API FastAPI et interface web React | Correction physique des pannes |
| CI/CD, Tests de bout en bout | Système de ticketing tiers |

---

## 4. Dataset
- **Nom/Lien** : `all_tickets_processed_improved_v3.csv` (Kaggle)
- **Source** : Kaggle - IT Service Ticket Classification
- **Taille** : 47 837 lignes, 2 colonnes
- **Format** : CSV
- **Champs** : `Document` (texte), `Topic_group` (label)

---

## 5. Proposition de maquette
**Type** : ☑ Application web (React, servie par l'API FastAPI) + API REST + CLI
- **Écran 1** : Nouveau ticket : catégorie, jauge de confiance, priorité, procédure citée, mots qui ont pesé, journal des agents.
- **Écran 2** : Traitement par lot CSV : répartition, confiance, justesse si l'étiquette est fournie, indicateurs de dérive.
- **Écran 3** : Supervision humaine : file des tickets `A_VERIFIER`, corrections envoyées au réentraînement, santé de l'API.
- **Écran 4** : Modèle et mesures : seuils du cadrage, matrice de confusion, comparaison des expériences.
- **Écran 5** : Base de connaissances : recherche dans les runbooks, refus hors sujet.

**Architecture** :
`Utilisateur` ↔ `Interface web React / CLI` ↔ `API FastAPI` ↔ `Équipe d'agents` → `ML (Scikit-Learn)` + `règles de priorité` + `RAG extractif (ChromaDB + runbooks)` + `vérification`  
*Le RAG ne génère pas de texte : il retourne la section du runbook verbatim avec sa source. Aucun LLM génératif obligatoire ; un modèle local (Ollama) peut résumer la procédure, au-dessus des étapes affichées mot pour mot.*

---

## 6. Technologies et outils
### 6.1 Développement
| Catégorie | Outil | Justification |
|---|---|---|
| Langage | Python 3.13 | Standard académique, écosystème IA mature |
| Framework API | FastAPI + Pydantic v2 | Validation stricte, documentation Swagger, performance |
| Framework d'agents | Aucun : équipe maison de cinq agents (`incidents_app/equipe.py`), bus de messages, boucle bornée | Pas de dépendance lourde ; chaque échange est journalisé et testable |
| Modèle LLM | **Aucun obligatoire** — RAG extractif ; Ollama `llama3.2:1b` local en option | Le RAG renvoie la section verbatim : 0 €/token, source citée ; le modèle local ne reçoit jamais le ticket |
| Modèle ML | Scikit-Learn (TF-IDF + LogisticRegression) | F1-macro 0,868, 1,5 ms par prédiction (p95), CPU portable |
| Base vectorielle (RAG) | ChromaDB local | Persistance sur disque, filtre par catégorie, aucun service cloud |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | Modèle léger (~87 Mo), rapide sur CPU, gratuit |
| Interface | React 19 + Vite + TypeScript + Tailwind CSS | Écrans sur mesure (jauge avec seuil, relais des agents, lot CSV) ; construite en fichiers statiques servis par l'API |
| Tests | Pytest (+ `ruff`, `mypy`) | Couverture unitaire/intégration, lint et typage |
| Gestion de version | Git + GitHub | Branches `feat/...`, PR, CI GitHub Actions |

### 6.2 Déploiement
| Catégorie | Outil | Justification |
|---|---|---|
| Conteneurisation | Docker + Docker Compose | Une image (l'API et l'interface qu'elle sert) reproductible sur toute machine |
| Hébergement | Local (portable) / Docker | Respecte la contrainte « pas de plateforme payante » |
| CI/CD | GitHub Actions | `pytest`, `ruff`, `mypy` à chaque push/PR |
| Monitoring | Journal JSON sans texte de ticket, `/health`, `/stats`, surveillance de la dérive (`/drift`) | Traçabilité des requêtes, latence et erreurs, alerte quand le vocabulaire change |
| Gestion des secrets | Variables d'environnement (`.env`, non versionné) | Aucune clé LLM ; les secrets ne sont pas dans Git |
| Exposition | Port 8000 : interface web sur `/`, API sous `/v1`, documentation sur `/docs` | Un seul port ; les routes `/v1` exigent une clé d'API |

---

## 7. Répartition des tâches et calendrier

*Calendrier du projet : 3 semaines (consigne du 16/11/2026), une étape par push de la liste du cours ; branches et auteurs dans [`Jalons_Push_GitHub_Projet20.md`](Jalons_Push_GitHub_Projet20.md). Le plan initial T1–T12 (4 semaines, remis le 09/11/2026) reste dans [`docs/semaine1/4-pipeline.md`](docs/semaine1/4-pipeline.md).*

| Étape | Responsable | Début | Fin |
|---|---|---|---|
| Dépôt, environnement, squelette, données et architecture (S1-1 à S1-5) | Ishak (A) + Ismail (B) | S1 | S1 |
| Modèle ML et prédiction (S2-1), API FastAPI (S2-3), intégration continue (S2-5) | Ishak (A) | S2 | S2 |
| Jeu d'évaluation (S2-2), interface web React (S2-4) | Ismail (B) | S2 | S2 |
| Cas limites (S3-1), exécution reproductible et Docker (S3-3) | Ishak (A) | S3 | S3 |
| Évaluation finale (S3-2), documentation finale (S3-4) | Ismail (B) | S3 | S3 |
| Fiches de suivi, compte rendu, soutenance, version v1.0.0 (S1-6, S2-6, S3-5, S3-6) | Ishak (A) + Ismail (B) | S1 | S3 |

---

## 8. Questionnaire de cadrage

**Q1. Quel problème concret votre agent résout-il, et comment ce problème est-il traité aujourd'hui sans agent IA ?**
Le support informatique est saturé par des tickets récurrents. Sans agent, le routage est manuel, lent et coûteux.

**Q2. Qui est l'utilisateur final de votre agent, et comment interagit-il avec lui au quotidien ?**
Le technicien IT Helpdesk, via une interface web pour superviser les tickets routés.

**Q3. Quelle valeur ajoutée apporte l'agent par rapport à une solution classique ?**
Le modèle apprend les formulations sur 47 837 tickets déjà classés (F1 macro 0,868 sur 9 568 tickets de test), là où une liste de mots-clés ne reconnaît que les mots prévus. Il signale quand il ne sait pas (abstention sous 0,60) et cite la procédure qu'il propose.

**Q4. Quelles sont les entrées de l'agent et quelles sorties produit-il ?**
Entrée : texte brut du ticket. Sorties : catégorie, score de confiance, priorité, statut (`VALIDE` / `A_VERIFIER`), procédure et source citée. Exemple : « Cannot connect to the VPN since this morning, my password expired » → `Access`, 88 %, `P2`, `VALIDE`, section « Access.md > Connexion VPN impossible ».

**Q5. Quelles décisions l'agent prend-il de façon autonome ?**
Il qualifie la catégorie, fixe la priorité, applique le seuil de 0,60 et décide de résoudre automatiquement ou de renvoyer à un humain. S'il résout, il recherche la section de runbook via le RAG, puis le Vérificateur contrôle la réponse (source, escalade, injection) avant de la livrer. Il n'exécute aucune commande et ne modifie aucun système : la décision finale d'application reste humaine.

**Q6. Quel type de mémoire votre agent utilise-t-il ?**
Mémoire à court terme : la requête et la prédiction courantes. Mémoire à long terme : l'index vectoriel ChromaDB des 27 sections des 8 runbooks (persisté sur disque, reconstruit automatiquement quand un runbook change), `MEMOIRE.md` (règles apprises, lues par le Vérificateur) et le modèle ML sérialisé. Le RAG n'est pas une évolution future : il est implémenté dans `incidents_app/rag.py` et appelé par l'agent via `/v1/resolve`.

**Q7. Décrivez la qualité de vos données : valeurs manquantes, bruit, déséquilibre, biais potentiels.**
Aucune valeur manquante. Classes déséquilibrées (Hardware 28,5 %, Administrative rights 3,7 %), compensées par `class_weight='balanced'`. Bruit : étiquettes parfois discutables (tickets Outlook étiquetés Administrative rights) et textes presque vides après nettoyage.

**Q8. Quelles sont les limites de votre dataset ?**
Tickets en anglais seulement : un ticket rédigé dans une autre langue est renvoyé à un humain. Vocabulaire absent du dataset (le mot « onboarding » n'y apparaît jamais), ce qui produit des erreurs sûres d'elles, déclarées dans le jeu d'or.

**Q9. Justifiez le choix de votre framework d'agents et de votre modèle LLM.**
Aucun framework d'agents ni LLM génératif obligatoire. L'orchestration est une équipe maison de cinq agents (`incidents_app/equipe.py`) : ML Scikit-Learn pour la qualification, règles métier pour la priorité, ChromaDB + `sentence-transformers` (`all-MiniLM-L6-v2`) pour le retrieval, vérification déterministe. Alternatives écartées : LLM génératif seul (coût par token, hallucination, non-vérifiable), RAG + LLM (coût et reformulation), règles métier (trop fragiles sur du texte libre). La justification complète est dans `docs/cadrage/rapport_conception_initiale.md` (section 6).

**Q10. Comment votre architecture gère-t-elle les erreurs ?**
Seuil d'abstention (60 %) : si < 60 %, routage manuel. Sans passage au-dessus du seuil de recherche, aucune source n'est citée. Une panne du modèle répond 500 sans exposer de détail ; la boucle des agents est bornée.

**Q11. Décrivez l'environnement de déploiement cible.**
Web conteneurisée via Docker Compose : une seule image, non root ; l'API sert aussi l'interface web ; seul le port 8000 est publié, et les routes `/v1` exigent une clé d'API.

**Q12. Quels sont les coûts d'exploitation attendus ?**
Coût marginal **0 € par requête** : ML local 1,5 ms (p95), recherche RAG 13 ms, mission complète des agents 66 ms (p95), index 0,6 Mo, modèle d'embedding 87 Mo, aucun appel API payant, aucun token. À 1 000 tickets/jour, environ 66 secondes de CPU cumulées. L'API est stateless : la montée en charge se fait par réplicas, sans coût par token. Le seul coût est le matériel (portable existant).

**Q13. Quelles métriques utiliserez-vous pour évaluer votre agent ?**
F1-macro ≥ 0,85 (mesuré : 0,868) ; taux de couverture automatique ≥ 70 % (mesuré : 78,4 %) ; précision sur les tickets couverts ≥ 90 % (mesuré : 94,2 %) ; 100 % des réponses `VALIDE` avec source citée (mesuré : 100 %) ; pertinence du runbook ≥ 90 % sur le jeu d'or de 20 tickets (mesuré : 92,3 %) ; latence p95 < 100 ms (mesuré : 1,5 ms `/v1/predict`, 66 ms `/v1/resolve`).

**Q14. Quels tests prévoyez-vous ?**
Tests unitaires et d'intégration (pytest) sur l'API, les agents et le RAG ; interface web : contrôle de types TypeScript et construction en CI, service de l'interface par l'API testé avec pytest ; deux jeux d'or (20 tickets, 17 requêtes) ; tests de structure Docker ; seuils relus dans `models/metrics.json` par la CI.

**Q15. Identifiez les principaux risques de votre projet.**
1. **Hallucination :** nulle par construction, le RAG est extractif et cite la source.
2. **Retrieval non pertinent :** runbooks découpés en sections, filtre par catégorie ML, seuil de 0,60 du modèle puis seuil de 0,27 de la recherche, source affichée.
3. **Runbook obsolète :** runbooks versionnés dans Git, index reconstruit automatiquement quand un runbook change.
4. **Biais du dataset :** classes déséquilibrées compensées par `class_weight='balanced'`.
5. **Sécurité :** validation Pydantic, aucune donnée personnelle dans l'index, aucune exécution automatique des commandes.
6. **Dépendance externe :** aucune API payante ; le système fonctionne hors ligne.
