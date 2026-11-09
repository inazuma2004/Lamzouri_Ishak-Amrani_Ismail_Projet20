# Livrable 3 : Maquette globale

**Rédacteur :** Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004))  
**Relecteur :** Ismail Amrani ([@Amaranix](https://github.com/Amaranix))  
**Fichiers :** `docs/semaine1/3-maquette.md` + `docs/semaine1/img/` (3 wireframes PNG)

> Les wireframes PNG sont régénérables avec `python scripts/generer_wireframes.py`. Les blocs ASCII ci-dessous en sont la version texte, lisible directement dans le Markdown.

---

## 3.1 Schéma d'architecture globale

```mermaid
flowchart TD
    subgraph Client ["Interface & Clients"]
        U["Utilisateur / Technicien L1"]
        UI["Interface Web (Streamlit)"]
        CLI["CLI Python (incidents)"]
        U -->|Texte d'incident ou fichier CSV| UI
        U -->|Ligne de commande| CLI
    end

    subgraph Backend ["Service API (FastAPI)"]
        API["FastAPI App (/predict & /resolve)"]
        VAL["Validation Pydantic (TicketIn, PredictionOut)"]
        API --- VAL
    end

    subgraph Intelligence ["Moteurs d'IA"]
        ML["Modèle ML (Scikit-Learn TF-IDF + LogisticRegression)"]
        AGENT["Agent de Résolution Autonome"]
        RAG["Mini-RAG (ChromaDB + sentence-transformers)"]
        RUNBOOKS[("Runbooks Markdown (data/runbooks/*.md)")]
        
        AGENT -->|1. Classifier| ML
        AGENT -->|2. Rechercher procédure si score >= 0.60| RAG
        RAG --- RUNBOOKS
    end

    UI -->|Requête HTTP REST| API
    CLI -->|Appel direct| AGENT
    API -->|Délégation| AGENT
    API -->|Réponse JSON (Catégorie, Confiance, Procédure, Statut)| UI
```

---

## 3.2 Légende du schéma

| Composant | Rôle et technologies | Fonctionnalité servie |
| --- | --- | --- |
| **Interface Web (Streamlit)** | Saisie unitaire de ticket et import en lot de fichiers CSV avec visualisations graphiques. | F3 |
| **CLI Python (`incidents`)** | Interface console pour automatisation batch ou invocation directe par script. | F1, F3 |
| **API FastAPI** | Endpoints `/health`, `/predict`, `/resolve` avec validation automatique des schémas Pydantic. | F3 |
| **Modèle ML** | Pipeline de classification supervisée Scikit-learn (TF-IDF + Régression Logistique). | F1 |
| **Agent Autonome** | Orchestrateur logique appliquant le seuil d'incertitude (60%) et routant vers le RAG ou l'humain. | F1, F2 |
| **Mini-RAG & Runbooks** | Base vectorielle ChromaDB indexant les procédures de dépannage techniques Markdown. | F4 |

---

## 3.3 Maquette des écrans (Interface Streamlit)

### Écran 1 : Qualification unitaire d'un incident

![Écran 1 — Qualification unitaire](img/ecran1_qualification.png)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 🚀 IT Helpdesk Intelligent — Qualification d'incidents               │
├────────────────────────────────────────────────────────────────────────┤
│ Description de l'incident :                                            │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ VPN client fails to authenticate with error code 403               │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [ Prédire la catégorie ]                                              │
│                                                                        │
│ Résultat :                                                             │
│ • Catégorie : [ Access ]                                              │
│ • Score de confiance : [ 92.4% ]  ████████████████░░░░                │
│ • Statut : ✅ VALIDE (Confiance suffisante)                           │
│                                                                        │
│ Procédure suggérée (Runbook Access.md) :                              │
│ > 1. Vérifier la date d'expiration du mot de passe Active Directory.  │
│ > 2. Réinitialiser le jeton MFA sur le portail d'authentification.     │
└────────────────────────────────────────────────────────────────────────┘
```

### Écran 2 : Alerte d'incertitude (Gestion de l'abstention)

![Écran 2 — Alerte d'incertitude](img/ecran2_incertitude.png)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ Résultat pour : "something is weird with the office computer"          │
│                                                                        │
│ • Catégorie suggérée : Miscellaneous                                   │
│ • Score de confiance : 41.2%   ██████░░░░░░░░░░░░░░                   │
│ • Statut : ⚠️ A_VERIFIER                                              │
│                                                                        │
│ ⚠️ ATTENTION : Le niveau de confiance est inférieur au seuil de 60%.  │
│ Ce ticket a été réorienté automatiquement vers un technicien humain.   │
└────────────────────────────────────────────────────────────────────────┘
```

### Écran 3 : Traitement par lot (Fichier CSV)

![Écran 3 — Traitement par lot CSV](img/ecran3_batch.png)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 📁 Traitement par lot d'incidents IT                                  │
│ Déposez votre fichier CSV contenant une colonne 'Document' :          │
│ [ 📄 Glisser-déposer tickets_nouveaux.csv ici ]                       │
│                                                                        │
│ Distribution des prédictions (Graphique en barres)                    │
│ [ Hardware: 35% | Access: 25% | HR Support: 20% | Autres: 20% ]       │
│                                                                        │
│ Tableau des résultats (Aperçu des 10 premiers tickets)                │
│ ┌────────────────────────────────────────┬─────────────┬─────────┬───┐│
│ │ Description                            │ Catégorie   │ Score   │St ││
│ ├────────────────────────────────────────┼─────────────┼─────────┼───┤│
│ │ Laptop screen flickering black         │ Hardware    │ 95.1%   │OK ││
│ │ Request new mouse and keyboard         │ Purchase    │ 89.4%   │OK ││
│ └────────────────────────────────────────┴─────────────┴─────────┴───┘│
│ [ ⬇️ Télécharger le CSV annoté avec prédictions et statuts ]           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3.4 Parcours utilisateur

1. **Scénario nominal unitaire :**
   - Le technicien L1 ouvre l'application Streamlit.
   - Il colle la description reçue d'un utilisateur dans la zone de texte.
   - Il clique sur *« Prédire la catégorie »*.
   - L'écran affiche instantanément la catégorie (`Access`), le score (92%), le badge vert `VALIDE`, et le résumé de la procédure technique issue du runbook avec sa source.
2. **Scénario d'incertitude :**
   - Le texte saisi est ambigu ou trop court.
   - Le score calculé est de 41% (< 60%).
   - L'écran affiche une bannière orange d'alerte `A_VERIFIER` invitant à un diagnostic manuel sans forcer une décision erronée.
3. **Scénario de traitement par lot :**
   - L'administrateur charge un export CSV de tickets hebdomadaires.
   - L'application traite l'intégralité du fichier en quelques secondes.
   - L'utilisateur visualise la répartition des pannes par catégorie et télécharge le fichier annoté avec les colonnes `prediction`, `score`, et `statut`.

---

## Critères d'acceptation (vérifiés par le relecteur)

- [x] Chaque composant du livrable 1 apparaît dans le schéma d'architecture.
- [x] Le flux complet d'une requête est traçable de bout en bout.
- [x] Chaque fonctionnalité du MVP est illustrée sur au moins une maquette d'écran.
- [x] Le diagramme Mermaid est valide et s'affiche nativement sur GitHub.
- [x] Les cas d'erreur et d'incertitude sont explicitement traités visuellement.

