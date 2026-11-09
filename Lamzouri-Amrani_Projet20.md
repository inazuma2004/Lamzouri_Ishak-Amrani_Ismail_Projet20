# Fiche de Cadrage Complète - Binôme : Lamzouri-Amrani - Projet 20

> **Version :** 1.1 — 09/11/2026  
> **Mise à jour :** le RAG n'est plus une « évolution future » : il est implémenté (RAG extractif local) et défendu dans [`docs/decisions/justification_rag.md`](docs/decisions/justification_rag.md).

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
3. Résolution assistée par RAG extractif : runbook cité, texte verbatim, sans LLM génératif.
4. API REST (`/predict`, `/resolve`) et interface Streamlit de pilotage.

**Périmètre** :
| Inclus | Exclu |
|---|---|
| Modèle ML supervisé (TF-IDF + LogReg) | Déploiement multi-cloud |
| RAG extractif local (ChromaDB + runbooks) | LLM génératif payant / API externe |
| API FastAPI et Dashboard Streamlit | Correction physique des pannes |
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
**Type** : ☑ Application web (Streamlit) + API REST + CLI
- **Écran 1** : Dashboard statistique (Vue d'ensemble).
- **Écran 2** : Interface de test (Input texte -> Classification -> Probabilités).
- **Écran 3** : Journal des prédictions douteuses (Supervision humaine, statut `A_VERIFIER`).
- **Écran 4** : Résolution agentique (runbook proposé + source citée + statut).

**Architecture** :
`Utilisateur` ↔ `Streamlit / CLI` ↔ `API FastAPI` ↔ `Agent` → `ML (Scikit-Learn)` + `RAG extractif (ChromaDB + runbooks)`  
*Le RAG ne génère pas de texte : il retourne le runbook verbatim avec sa source. Aucun LLM génératif.*

---

## 6. Technologies et outils
### 6.1 Développement
| Catégorie | Outil | Justification |
|---|---|---|
| Langage | Python 3.13 | Standard académique, écosystème IA mature |
| Framework API | FastAPI + Pydantic v2 | Validation stricte, documentation Swagger, performance |
| Framework d'agents | Aucun (orchestration Python maison : `IncidentAgent`) | Pas de dépendance lourde ; le flux ML → RAG → humain est explicite et testable |
| Modèle LLM | **Aucun** — RAG extractif | Le RAG renvoie le runbook verbatim : 0 €/token, zéro hallucination, source citée |
| Modèle ML | Scikit-Learn (TF-IDF + LogisticRegression) | F1-macro 0,857, 2,22 ms par prédiction, CPU portable |
| Base vectorielle (RAG) | ChromaDB local | Persistance sur disque, filtre par catégorie, aucun service cloud |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | Modèle léger (~87 Mo), rapide sur CPU, gratuit |
| Interface | Streamlit | Prototypage rapide, saisie unitaire et traitement par lot |
| Tests | Pytest (+ `ruff`, `mypy`) | Couverture unitaire/intégration, lint et typage |
| Gestion de version | Git + GitHub | Branches `feat/...`, PR, CI GitHub Actions |

### 6.2 Déploiement
| Catégorie | Outil | Justification |
|---|---|---|
| Conteneurisation | Docker + Docker Compose | API et UI reproductibles sur toute machine |
| Hébergement | Local (portable) / Docker | Respecte la contrainte « pas de plateforme payante » |
| CI/CD | GitHub Actions | `pytest`, `ruff`, `mypy` à chaque push/PR |
| Monitoring | Journalisation locale + `/health` | Traçabilité des requêtes et diagnostic |
| Gestion des secrets | Variables d'environnement (`.env`, non versionné) | Aucune clé LLM ; les secrets ne sont pas dans Git |
| Exposition | API REST (8000) + UI Streamlit (8501) | Accès technicien via navigateur ou client HTTP |

---

## 7. Répartition des tâches et calendrier

*Calendrier du projet d'équipe (4 semaines), conforme au dossier de lancement. Le détail WBS (T1–T12), les dépendances et le Gantt figurent dans [`docs/semaine1/4-pipeline.md`](docs/semaine1/4-pipeline.md). Le journal des TPs suit la progression du cours (Atelier 0 → TP1 → TP2 → TP3 → TP4).*

| Étape | Responsable | Début | Fin |
|---|---|---|---|
| Cadrage, dataset, dépôt Git | Ishak (A) + Ismail (B) | S1 | S1 |
| Modèle ML + seuil d'incertitude | Ismail (B) | S1 | S1 |
| API FastAPI + interface Streamlit | Ismail (B) + Ishak (A) | S2 | S2 |
| RAG, agent, packaging, Docker | Ismail (B) + Ishak (A) | S3 | S3 |
| Tests, CI, gel du code | Ismail (B) + Ishak (A) | S4 | S4 |
| Documentation & soutenance | Ishak (A) + Ismail (B) | S1 | S4 |

---

## 8. Questionnaire de cadrage

**Q1. Quel problème concret votre agent résout-il, et comment ce problème est-il traité aujourd'hui sans agent IA ?**
Le support informatique est saturé par des tickets récurrents. Sans agent, le routage est manuel, lent et coûteux.

**Q2. Qui est l'utilisateur final de votre agent, et comment interagit-il avec lui au quotidien ?**
Le technicien IT Helpdesk, via une interface web pour superviser les tickets routés.

**Q3. Quelle valeur ajoutée apporte l'agent par rapport à une solution classique ?**
Une automatisation intelligente qui s'adapte, contrairement aux règles fixes fragiles.

**Q4. Quelles sont les entrées de l'agent et quelles sorties produit-il ?**
Entrée : texte brut du ticket. Sorties : catégorie, score de confiance, statut (`VALIDE` / `A_VERIFIER`), runbook proposé, texte de la procédure et source citée. Exemple : « VPN HS, mot de passe expiré » → `Access`, 99,9 %, `VALIDE`, runbook `data/runbooks/Access.md`.

**Q5. Quelles décisions l'agent prend-il de façon autonome ?**
Il qualifie la catégorie, applique le seuil de 0,60 et décide de résoudre automatiquement ou de renvoyer à un humain. S'il résout, il recherche le runbook correspondant via le RAG. Il n'exécute aucune commande et ne modifie aucun système : la décision finale d'application reste humaine.

**Q6. Quel type de mémoire votre agent utilise-t-il ?**
Mémoire à court terme : la requête et la prédiction courantes. Mémoire à long terme : l'index vectoriel ChromaDB des 8 runbooks (persisté sur disque, reconstruit par `scripts/indexer_runbooks.py`) et le modèle ML sérialisé. Le RAG n'est pas une évolution future : il est implémenté dans `incidents_app/rag.py` et appelé par l'agent via `/resolve`.

**Q7. Décrivez la qualité de vos données : valeurs manquantes, bruit, déséquilibre, biais potentiels.**
Dataset nettoyé, classes équilibrées pour l'entraînement.

**Q8. Quelles sont les limites de votre dataset ?**
Jargon spécifique non présent dans le dataset pouvant causer des erreurs.

**Q9. Justifiez le choix de votre framework d'agents et de votre modèle LLM.**
Aucun framework d'agents ni LLM génératif. L'orchestration est un module Python maison (`IncidentAgent`) : ML Scikit-Learn pour la qualification, puis ChromaDB + `sentence-transformers` (`all-MiniLM-L6-v2`) pour le retrieval. Alternatives écartées : LLM génératif seul (coût par token, hallucination, non-vérifiable), RAG + LLM (coût et reformulation), règles métier (trop fragiles sur du texte libre). La justification complète est dans `docs/decisions/justification_rag.md`.

**Q10. Comment votre architecture gère-t-elle les erreurs ?**
Seuil d'abstention (60%) : si < 60%, routage manuel.

**Q11. Décrivez l'environnement de déploiement cible.**
Web conteneurisée via Docker (S6).

**Q12. Quels sont les coûts d'exploitation attendus ?**
Coût marginal **0 € par requête** : ML local 2,22 ms, RAG extractif 23 ms, index 21,9 Mo, modèle d'embedding 87,3 Mo, aucun appel API payant, aucun token. À 1 000 tickets/jour, environ 23 secondes de CPU cumulées. L'API est stateless : la montée en charge se fait par réplicas, sans coût par token. Le seul coût est le matériel (portable existant).

**Q13. Quelles métriques utiliserez-vous pour évaluer votre agent ?**
F1-macro ≥ 0,85 (mesuré : 0,857) ; taux de couverture automatique ≥ 70 % ; précision sur les tickets couverts ≥ 90 % ; 100 % des réponses `VALIDE` avec source citée ; pertinence du runbook ≥ 90 % sur le jeu d'or de 20 tickets ; latence p95 < 100 ms (mesuré : 2,22 ms ML et 23 ms RAG).

**Q14. Quels tests prévoyez-vous ?**
Tests unitaires (pytest) sur API, tests d'intégration, jeu de données de référence (gold set).

**Q15. Identifiez les principaux risques de votre projet.**
1. **Hallucination :** nulle par construction, le RAG est extractif et cite la source.
2. **Retrieval non pertinent :** filtre par catégorie ML, seuil de 0,60, source affichée ; évolution prévue par découpage en passages.
3. **Runbook obsolète :** runbooks versionnés dans Git, ré-indexation par script.
4. **Biais du dataset :** classes déséquilibrées compensées par `class_weight='balanced'`.
5. **Sécurité :** validation Pydantic, aucune donnée personnelle dans l'index, aucune exécution automatique des commandes.
6. **Dépendance externe :** aucune API payante ; le système fonctionne hors ligne.
