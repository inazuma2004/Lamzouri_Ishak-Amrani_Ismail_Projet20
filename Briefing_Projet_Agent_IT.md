# 🚀 Briefing Projet : Agent Autonome de Résolution d'Incidents IT
**Module :** Développement et déploiement d’applications intelligentes (Année universitaire 2026-2027)  
**Enseignant :** A. Larhlimi  
**Équipe :** Travail en binôme  
**Livrable immédiat :** Fin de la Semaine 5 (Étude de conception - 15% de la note) et TP cumulatifs  

---

### 📊 1. Le Dataset retenu : IT Service Ticket Classification
* **Source & Format :** Fichier tabulaire (CSV) disponible sur Kaggle, contenant environ 48 000 lignes de tickets réels.
* **Structure des données :** 
  * `Features` (X) : Descriptions textuelles des pannes saisies par les utilisateurs (*ex: "Impossible de me connecter au VPN", "Écran noir sur mon poste"*).
  * `Target` (y) : Catégories d'incidents informatiques (*Hardware, Access, Network, Storage...*).
* **Pourquoi ce choix ?** Il respecte scrupuleusement la contrainte stricte du syllabus : **"Aucune plateforme payante, rien qui ne tourne pas sur un ordinateur portable"**. Il permet un apprentissage rapide en moins d'une minute sous forme de Pipeline Scikit-Learn.

---

### 🎯 2. Le Cadrage Officiel (Grille de Décision du Cours)
Pour nos fiches de cadrage (Semaine 1, TP1) et notre soutenance, voici notre positionnement scientifique basé sur l'arbre de décision officiel :

* **Pourquoi pas de simples "Règles Métier" ?** La logique de description d'une panne par un être humain n'est ni connue à l'avance, ni stable. Les expressions linguistiques et le jargon varient trop d'un utilisateur à l'autre.
* **Pourquoi notre problème principal relève du "Machine Learning Classique" ?** Nous traitons une tâche de **classification supervisée de texte** (NLP). Nous descendons dans l'arbre décisionnel car :
  * **Critère (a) (Données étiquetées) :** Nous disposons d'un historique massif de tickets informatiques déjà annotés par des techniciens.
  * **Critère (c) (Coût par requête) :** L'approche `TfidfVectorizer` + `LogisticRegression` ou `LinearSVC` garantit une prédiction en quelques millisecondes avec une empreinte mémoire minime et un coût d'infrastructure nul (pas besoin de processeur graphique GPU en production).
  * **Critère (d) (Conséquence d'une erreur) :** L'erreur de routage automatique d'un ticket n'a pas de conséquence grave. Elle est facilement gérée dans l'interface en fixant un `SEUIL_INCERTITUDE` (ex: 60%) pour renvoyer le ticket douteux à une validation humaine.

---

### 🗺️ 3. Cycle de Vie et Roadmap de l'Application (De la Semaine 1 à 11)
Notre application va grandir de manière incrémentale sur un **dépôt GitHub unique**, sans jamais jeter le code des étapes précédentes :

1. **Semaine 2 (Modèle) :** Écriture du script `train.py` (découpage stratifié pour préserver l'équilibre des classes et éviter les fuites de données) et génération du fichier `models/metrics.json`.
2. **Semaine 3 (API FastAPI) :** Exposition du modèle via un endpoint `POST /predict`. L'API reçoit la description en JSON, valide le format à l'aide d'un schéma Pydantic (protection contre les entrées volumineuses ou malformées) et renvoie la catégorie prédite avec sa confiance.
3. **Semaine 5 (Interface Streamlit) :** Conception d'une interface utilisateur web interactive. Elle intègre des widgets d'entrée, des graphiques Plotly et un avertissement orange *"À vérifier par un agent"* dès que le modèle hésite.
4. **Semaine 9 (Mini-RAG) :** Stockage et indexation des procédures techniques de dépannage (runbooks) dans une base de données vectorielle locale (`sentence-transformers` + `Chroma` ou `Ollama`).
5. **Semaine 10 (IA Agentique) :** Assemblage final en un système multi-agents autonome. Le modèle ML classique qualifie le domaine du ticket (ex: *Réseau*), puis l'**Agent Autonome** prend le relais, interroge le **RAG** pour extraire la bonne procédure et affiche directement la solution de résolution à l'utilisateur.

---

### ⚠️ 4. Règles de Survie Logicielles et MLOps pour le Binôme
La notation de M. Larhlimi repose sur la rigueur de l'ingénierie logicielle et non sur la performance brute du modèle :

* **Gestion des artefacts :** Interdiction absolue de pousser le dossier `.venv/`, les données brutes ou le fichier `.joblib` sur Git. Ils doivent être exclus via le fichier `.gitignore`. Seule la mesure de performance (`models/metrics.json`) est versionnée pour prouver la qualité du modèle à l'intégration continue (CI).
* **Workflow Git rigoureux :** Aucun commit direct sur la branche `main`. Chaque tâche doit faire l'objet d'une branche dédiée (*ex: feat/cadrage-cas3*), validée par une Pull Request (PR) relue par l'autre membre et acceptée uniquement si la CI GitHub Actions est verte.
* **Critère de succès :** Du code modulaire, documenté, exécutable en trois commandes sur une machine vierge, et un fichier `docs/` détaillant sincèrement l'analyse de nos erreurs de prédiction.

---
*Ce document sert de référence partagée pour notre étude de conception et la structure de notre dépôt informatique.*
