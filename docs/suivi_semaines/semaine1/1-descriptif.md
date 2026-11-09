# Livrable 1 : Descriptif du projet mis à jour

**Rédacteur :** Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004))  
**Relecteur :** Ismail Amrani ([@Amaranix](https://github.com/Amaranix))  
**Fichier :** `docs/semaine1/1-descriptif.md`

---

## 1.1 Contexte et problème

Dans les centres de support informatique (IT Service Desk), des centaines de tickets d'incidents arrivent chaque jour en texte libre non structuré. Aujourd'hui, des techniciens de niveau 1 doivent lire manuellement chaque ticket pour identifier la catégorie (matériel, accès, droits, réseau, stockage) et l'affecter à la bonne équipe, ce qui entraîne des délais de plusieurs heures et de fréquentes erreurs d'aiguillage.

## 1.2 Objectif en une phrase

Qualifier automatiquement les incidents informatiques en temps réel avec un score de confiance et assister leur résolution via des procédures techniques indexées, tout en déléguant à l'humain en cas de doute.

## 1.3 Utilisateurs cibles et scénario d'usage principal

- **Utilisateurs cibles :** Techniciens de support IT niveau 1 (gain de temps au routage) et collaborateurs de l'entreprise déclarant un incident.
- **Scénario d'usage principal :**
  1. L'utilisateur saisit son problème en texte libre (ex. : *"Impossible de me connecter au VPN depuis ce matin, mot de passe expiré"*).
  2. L'agent analyse le texte en moins de 50 ms et identifie la catégorie (`Access`) avec un score de confiance de 92%.
  3. Le score dépassant le seuil de 60%, l'agent marque le ticket comme `VALIDE` et recherche automatiquement la procédure de dépannage associée dans la base de runbooks.
  4. L'utilisateur reçoit la qualification immédiate et les étapes de déblocage avec la source du runbook citée ; si le score avait été inférieur à 60%, le ticket aurait été étiqueté `A_VERIFIER` et transmis à un technicien humain.

## 1.4 Fonctionnalités du MVP (Équipe de 2 étudiants)

| N° | Fonctionnalité | Ce que l'utilisateur voit ou obtient | Priorité |
| --- | --- | --- | --- |
| **F1** | Classification automatique supervisée en 8 catégories | La catégorie d'incident prédite avec son score de confiance calculé en millisecondes. | Indispensable |
| **F2** | Gestion de l'incertitude et abstention automatique | Un badge visuel clair (`VALIDE` en vert si confiance >= 60%, `A_VERIFIER` en orange sinon). | Indispensable |
| **F3** | Double interface d'utilisation (API REST & UI Streamlit) | Une API `/predict` documentée et une interface web avec saisie unitaire et traitement par lot CSV. | Indispensable |
| **F4** | Moteur Mini-RAG de recommandation de procédures | L'affichage des étapes techniques de résolution extraites du runbook officiel avec citation de la source. | Souhaitable |

## 1.5 Services et composants techniques

| Service ou composant | Rôle dans le projet | Technologie choisie | Pourquoi ce choix |
| --- | --- | --- | --- |
| **Modèle ML** | Classification supervisée de texte | Scikit-learn (`TfidfVectorizer` + `LogisticRegression`) | Moins de 10 ms par prédiction, frugalité en mémoire (<15 Mo), tourne sur PC portable sans GPU. |
| **Recherche ou mémoire** | Base de connaissances et runbooks | ChromaDB locale + `sentence-transformers` | Recherche sémantique locale gratuite sans dépendance cloud payante ni quota externe. |
| **Outils appelés par l'agent** | CLI d'administration et scripts | Python (`incidents_app/cli.py`) | Permet d'intégrer l'outil dans des scripts système ou des cron jobs administrateur. |
| **API** | Exposition des prédictions et résolutions | FastAPI + Uvicorn + Pydantic v2 | Documentation Swagger automatique, validation stricte des types et asynchronisme natif. |
| **Interface** | Tableau de bord utilisateur et lot CSV | Streamlit | Prototypage rapide, affichage interactif de graphiques et téléchargement direct des résultats. |
| **Conteneur et intégration continue** | Reproductibilité et validation continue | Docker, Docker Compose, GitHub Actions | Exécution identique sur toute machine hôte et tests automatiques à chaque commit. |

## 1.6 Hors périmètre

- Utilisation d'API propriétaires payantes (OpenAI GPT-4, Claude).
- Intégration directe aux API cloud de ServiceNow, Jira Service Desk ou Zendesk.
- Envoi automatique de notifications SMS ou e-mails push.
- Entraînement en continu en production (*online learning*).

## 1.7 Écart avec la fiche du catalogue

Nous avons étendu la classification supervisée initiale en y intégrant un module **Mini-RAG local** branché sur des runbooks IT au format Markdown. Cela permet à l'agent non seulement d'aiguiller le ticket, mais aussi de suggérer la procédure de dépannage immédiatement exploitable avec citation stricte des sources, conformément aux principes d'explicabilité du cours.

---

## Critères d'acceptation (vérifiés par le relecteur)

- [x] Le problème et l'utilisateur sont compréhensibles sans le catalogue.
- [x] Le nombre de fonctionnalités correspond à la taille de l'équipe (3 à 4 fonctionnalités pour un binôme).
- [x] Chaque fonctionnalité est démontrable avec un résultat concret.
- [x] Chaque composant technique dispose d'une justification explicite.
- [x] Le hors périmètre est clairement délimité.
