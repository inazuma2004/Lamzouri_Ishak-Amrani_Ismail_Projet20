# 🏗️ Architecture Agentique — Mini-RAG & IA Autonome (Semaines 9-10)

> **Projet :** incidentsIT (IT Helpdesk Intelligent)  
> **Module :** Développement et déploiement d'applications intelligentes (2026-2027)  
> **Enseignant :** M. A. Larhlimi  
> **Conforme à :** arbre de décision du cours (ML → RAG, pas de génératif seul)

---

## 🎯 Objectif

Construire un **agent autonome de résolution d'incidents IT** qui :
1. **Qualifie** un ticket entrant avec le modèle ML supervisé existant (TF-IDF + LogisticRegression).
2. **Résout** le ticket en récupérant la procédure de dépannage adéquate depuis une base de runbooks via Mini-RAG.
3. **Cite ses sources** (toujours un runbook, jamais de génératif seul).
4. **Respecte le seuil d'incertitude** : si le modèle hésite (score < 0.60), l'agent ne résout pas automatiquement et renvoie vers un opérateur humain.

---

## 🧱 Composants

| Composant | Fichier | Rôle |
|-----------|---------|------|
| **Modèle ML** | `incidents_app/predict.py` | Qualification : catégorie + score de confiance |
| **Mini-RAG** | `incidents_app/rag.py` (wrapper `src/rag.py`) | Base vectorielle ChromaDB + embeddings sentence-transformers |
| **Runbooks** | `data/runbooks/*.md` | Base de connaissances (procédures de dépannage par catégorie) |
| **Indexation** | `scripts/indexer_runbooks.py` | Charge les runbooks dans ChromaDB |
| **IA Agentique** | `incidents_app/agent.py` (wrapper `src/agent.py`) | Agent autonome : ML → RAG → résolution |
| **API** | `app/main.py` | Endpoint `POST /resolve` |
| **UI** | `ui/app.py` + `ui/client.py` | Onglet "Résolution agentique" (Streamlit) |

---

## 🔄 Flux de résolution (agent autonome)

```
Ticket utilisateur (texte libre)
        │
        ▼
┌─────────────────────┐
│  1. QUALIFICATION ML │  incidents_app.predict.predire()
│    - Catégorie       │  (ex: Access, Hardware, Storage...)
│    - Score confiance │  (0.0 à 1.0)
│    - Seuil 0.60      │
└─────────────────────┘
        │
        ├─ score < 0.60 → A_VERIFIER
        │     │
        │     ▼
        │   Renvoi opérateur humain
        │   (aucune résolution auto)
        │
        ├─ score >= 0.60 → VALIDE
        │     │
        │     ▼
        ▼     ▼
┌─────────────────────┐
│  2. RÉSOLUTION RAG   │  incidents_app.rag.MiniRAG.rechercher()
│    - Filtre par      │  where={"categorie": <catégorie prédite>}
│      catégorie ML    │
│    - Similarité      │  cosine (embeddings sentence-transformers)
│    - Retourne runbook│  avec source citée (chemin, score)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  3. RÉPONSE FINALE   │  Retour : catégorie, score, statut,
│    - Procédure       │    runbook, résolution, sources, action_humaine
│    - Sources citées  │
└─────────────────────┘
```

---

## 📐 Seuil d'incertitude (règle Larhlimi)

| Score ML | Statut | Action de l'agent |
|----------|--------|-------------------|
| >= 0.60 | `VALIDE` | Résolution RAG automatique avec runbook cité |
| < 0.60 | `A_VERIFIER` | Pas de résolution, renvoi vers opérateur humain |

Le seuil de 0.60 est aligné sur le TP4 (courbe de seuil) et garantit que l'agent ne résout que les cas dont il est suffisamment confiant.

---

## 📚 Base de connaissances RAG (runbooks)

8 runbooks, un par catégorie ML, dans `data/runbooks/` :

| Catégorie | Fichier | Contenu |
|-----------|---------|---------|
| Access | `Access.md` | VPN, mot de passe, compte verrouillé, authentification |
| Administrative rights | `Administrative rights.md` | Élévation de privilèges, installation logiciels |
| HR Support | `HR Support.md` | Congés, onboarding, droits RH |
| Hardware | `Hardware.md` | Écran, clavier, imprimante, périphériques |
| Internal Project | `Internal Project.md` | Suivi projet, jalon, reporting |
| Miscellaneous | `Miscellaneous.md` | Demandes diverses non classées |
| Purchase | `Purchase.md` | Licence, poste de travail, achat matériel |
| Storage | `Storage.md` | Disque plein, quota, sauvegarde |

Chaque runbook contient : symptômes couverts, procédure de dépannage numérotée, escalade, temps estimé, et la mention "Source : Runbook X — IT Helpdesk".

---

## 🔌 Endpoint API

**`POST /resolve`** — Résolution d'incident par l'agent autonome.

**Requête :**
```json
{ "text": "Cannot access the VPN, password expired" }
```

**Réponse (statut VALIDE) :**
```json
{
  "categorie": "Access",
  "score": 0.9997,
  "statut": "VALIDE",
  "runbook": "Runbook — Access (Accès & Authentification)",
  "resolution": "# Runbook — Access...\n\n## Procédure de dépannage\n1. Vérifier le verrouillage du compte...",
  "sources": [
    { "chemin": "data/runbooks/Access.md", "score": 0.322, "titre": "..." }
  ],
  "action_humaine": false,
  "message_humain": null
}
```

**Réponse (statut A_VERIFIER) :**
```json
{
  "categorie": "INDETERMINE",
  "score": 0.32,
  "statut": "A_VERIFIER",
  "runbook": null,
  "resolution": "Le modèle n'est pas suffisamment confiant... Une vérification humaine est requise.",
  "sources": [],
  "action_humaine": true,
  "message_humain": "Ticket à vérifier par un opérateur humain..."
}
```

---

## 🧠 Pourquoi cette approche (arbre de décision Larhlimi)

L'arbre de décision du cours impose :
1. **Règles métier** si logique connue et stable → non applicable (descriptions utilisateur variées)
2. **Machine Learning** si données étiquetées → OUI (47 837 tickets annotés) → classification de catégorie
3. **RAG** si réponse à tirer de documents → OUI (runbooks IT) → résolution avec source citée
4. **Génératif seul** seulement en dernier recours → **EXCLU** (peu vérifiable, coûteux)

L'agent combine ML (étape 2) + RAG (étape 3), sans jamais utiliser de génératif seul.

---

## 💰 Coût et vérifiabilité du RAG (défense)

Le RAG est **extractif** : il récupère le runbook et renvoie son texte **verbatim** avec la source. Il n'y a **aucune génération par LLM**, donc aucun coût par token et aucune hallucination possible par construction.

| Mesure (09/11/2026, CPU, sans GPU) | Valeur |
| --- | --- |
| Latence RAG moyenne / p95 | **23,00 ms** / **25,36 ms** |
| Latence ML moyenne | **2,22 ms** |
| Runbooks indexés | **8** |
| Index ChromaDB | **21,90 Mo** |
| Cache du modèle d'embedding | **87,34 Mo** |
| Coût marginal par requête | **0 €** |

- **(b) Vérifiabilité :** chaque réponse cite `data/runbooks/<Catégorie>.md` et le score de similarité ; le runbook est versionné dans Git.
- **(c) Coût :** 1 000 tickets/jour = environ **23 s de CPU** cumulées ; 10 000 tickets/jour = environ **4 min**. Aucun serveur dédié, aucune API payante.
- **Pourquoi pas un LLM ?** Coût par token, latence réseau, non-déterminisme et risque d'inventer une commande. Le cours (`cas2-reglement.md`) accepte ce coût pour quelques dizaines de questions/jour ; notre volume est de centaines de tickets/jour.

> 📘 Défense complète : [`docs/decisions/justification_rag.md`](decisions/justification_rag.md).

---

## 🧪 Tests

| Fichier | Couverture |
|---------|------------|
| `tests/test_rag.py` | Indexation, recherche par catégorie, source citée, pertinence Hardware |
| `tests/test_agent.py` | Résolution ticket clair, seuil d'abstention, source citée si VALIDE, qualifier() |

Exécution : `pytest tests/` → 42 passed, 4 xfailed, 0 failed.

---

## 🐳 Déploiement (Semaine 6)

```bash
# Construire l'image (inclut sentence-transformers, chromadb via requirements.txt)
docker build -t incidents-app:latest .

# Indexer les runbooks puis lancer
docker-compose up --build

# L'API est disponible sur http://localhost:8000
# L'UI sur http://localhost:8501
# Endpoint : POST http://localhost:8000/resolve
```

---

## 📊 Métriques du modèle ML (qualification)

- **F1-macro :** 0.857
- **Accuracy :** 0.857
- **Classes :** Access, Administrative rights, HR Support, Hardware, Internal Project, Miscellaneous, Purchase, Storage
- **Seuil d'abstention :** 0.60

---

*Document rédigé le 2026-11-04. Conforme aux exigences du module (M. A. Larhlimi, 2026-2027).*
