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
| **F4** | Moteur Mini-RAG de recommandation de procédures | L'affichage des étapes techniques de résolution extraites du runbook officiel avec citation de la source. | Indispensable (livré S9-10) |

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

La justification complète de ce choix (arbre de décision, critères `(a)` à `(d)`, coûts mesurés, limites) est consignée dans [`docs/decisions/justification_rag.md`](../decisions/justification_rag.md).

---

## 1.8 Métrique de succès métier et seuil d'acceptation

Le succès du projet ne se limite pas à l'accuracy du modèle : il se mesure à la capacité de l'agent à **qualifier correctement** un ticket et à **fournir une procédure vérifiable** sans faire perdre de temps au technicien.

| Indicateur | Définition | Seuil d'acceptation |
| --- | --- | --- |
| **Taux de couverture automatique** | Part des tickets dont le score de confiance est ≥ 0,60 et qui sont donc traités sans validation humaine préalable. | **≥ 70 %** |
| **Précision sur les tickets couverts** | Part des tickets couverts dont la catégorie prédite est correcte (comparaison au label réel). | **≥ 90 %** |
| **Taux global de qualification correcte** | Part des tickets correctement routés, tous statuts confondus. | **≥ 80 %** |
| **F1-macro (modèle)** | Moyenne harmonique précision/rappel par classe, sur le jeu de test disjoint (20 %). | **≥ 0,85** (mesuré : **0,857**) |
| **Traçabilité RAG** | Part des réponses `VALIDE` qui citent au moins une source de runbook. | **100 %** (vérifié par `tests/test_agent.py`) |
| **Pertinence du runbook** | Part des tickets du jeu d'or pour lesquels le runbook retourné est le bon. | **≥ 90 %** sur 20 tickets |
| **Latence API** | Temps de réponse p95 de `/predict` et `/resolve`. | **< 100 ms** (mesuré : **2,22 ms** et **23 ms**) |
| **Abstention** | Part des tickets avec score < 0,60 effectivement renvoyés en `A_VERIFIER`. | **100 %** (vérifié par les tests) |

**Règle de décision :** le projet est accepté si **tous** les seuils sont atteints. Un échec sur le F1-macro (< 0,85) ou sur la traçabilité RAG (une réponse `VALIDE` sans source) est bloquant : il déclenche une revue du modèle ou de l'index avant livraison.

---

## 1.9 Défense du RAG extractif (critères b et c de la grille)

Le RAG n'est utilisé que pour la **résolution** (F4), jamais pour la classification (F1). La classification reste un problème de ML supervisé, car des données étiquetées existent (critère `a`). La résolution, elle, doit produire une procédure issue de documents internes : c'est le cas d'usage du RAG.

### (b) Vérifiabilité

Chaque réponse `VALIDE` renvoie **le texte exact du runbook** et **le chemin de la source** (`data/runbooks/Access.md`), avec le score de similarité. Le runbook est versionné dans Git : on peut savoir quelle version a produit quelle réponse. Le technicien peut ouvrir la source et vérifier chaque étape avant de l'appliquer. Un modèle génératif seul ne garantit jamais qu'une commande ou un numéro d'étape existe réellement dans le document.

### (c) Coût par requête

Le RAG est **extractif** : ChromaDB + `sentence-transformers` (`all-MiniLM-L6-v2`) récupèrent le runbook, puis le texte est renvoyé **verbatim**. Il n'y a **aucune génération par LLM**, donc **aucun coût par token** et **aucun appel API payant**.

| Mesure (09/11/2026, CPU, sans GPU) | Valeur |
| --- | --- |
| Latence RAG moyenne / p95 | **23,00 ms** / **25,36 ms** |
| Latence ML moyenne | **2,22 ms** |
| Runbooks indexés | **8** |
| Index ChromaDB | **21,90 Mo** |
| Cache du modèle d'embedding | **87,34 Mo** |
| Coût marginal par requête | **0 €** |

À 1 000 tickets/jour, le RAG consomme environ **23 secondes de CPU cumulées** ; à 10 000 tickets/jour, environ **4 minutes**. Aucun serveur dédié ni plateforme payante n'est nécessaire, ce qui respecte la contrainte « doit tourner sur un portable ».

### Pourquoi pas un modèle génératif seul ?

Un LLM génératif serait facturé **au token** à chaque ticket, introduirait une latence réseau, ne garantirait pas la source et pourrait inventer une commande. Le cours (`cas2-reglement.md`) accepte ce coût pour « quelques dizaines de questions par jour » ; notre volume est de **centaines de tickets par jour**, donc le même raisonnement conduit à un RAG **sans génération**. Le détail de la comparaison et les limites assumées figurent dans [`docs/decisions/justification_rag.md`](../decisions/justification_rag.md).

---

## Critères d'acceptation (vérifiés par le relecteur)

- [x] Le problème et l'utilisateur sont compréhensibles sans le catalogue.
- [x] Le nombre de fonctionnalités correspond à la taille de l'équipe (3 à 4 fonctionnalités pour un binôme).
- [x] Chaque fonctionnalité est démontrable avec un résultat concret.
- [x] Chaque composant technique dispose d'une justification explicite.
- [x] Le hors périmètre est clairement délimité.

