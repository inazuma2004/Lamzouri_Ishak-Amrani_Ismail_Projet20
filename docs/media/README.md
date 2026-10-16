# 🎬 Vidéo de Présentation et de Cadrage du Projet

> **Projet :** Agent Autonome de Résolution d'Incidents IT  
> **Auteur de la présentation vidéo :** Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004))  
> **Binôme :** Ismail Amrani ([@Amaranix](https://github.com/Amaranix))  
> **Module :** Développement et déploiement d’applications intelligentes (Année 2026-2027)  
> **Enseignant :** M. A. Larhlimi  

---

## 📹 Fichier Vidéo

Le fichier vidéo complet de la soutenance/présentation de cadrage est disponible dans ce dossier :
- **Fichier local :** [`presentation_cadrage_Lamzouri_Ishak.mp4`](presentation_cadrage_Lamzouri_Ishak.mp4) (Taille : ~19.1 Mo)
- **Format :** MP4 H.264
- **Durée :** ~1 min 45 s

---

## 📝 Script et Argumentation Développée

Le discours prononcé dans la vidéo suit rigoureusement l'arbre de décision scientifique du cours :

### [00:00 - 00:15] Introduction et Sujet
> *"Bonjour à tous. Dans le cadre de notre projet d'application intelligente, notre objectif est de développer un agent autonome de résolution d'incidents IT. Pour concevoir ce système, nous avons sélectionné le jeu de données IT Service Ticket Classification disponible sur Kaggle. Aujourd'hui, je vais vous présenter notre démarche de cadrage et justifier scientifiquement notre choix d'approche technologique."*

### [00:15 - 00:45] Le Cadrage : Pourquoi éliminer les Règles Métier et le RAG pur ?
> *"En suivant scrupuleusement la grille de décision du cours, nous nous sommes posé les questions clés dans l'ordre :*  
> *1. La logique de diagnostic est-elle connue et stable ? Non. Les pannes informatiques et leurs descriptions textuelles rédigées par les utilisateurs varient constamment. L'approche par Règles Métier est donc exclue.*  
> *2. Peut-on utiliser le RAG seul dès le départ ? Non plus. Le RAG est idéal pour extraire des procédures depuis des documents internes. Cependant, avant de pouvoir chercher une solution documentée, l'agent doit impérativement comprendre et trier le problème entrant (s'agit-il d'un bug réseau, matériel, ou d'un problème d'accès ?)."*

### [00:45 - 01:20] Cœur de l'argumentation : L'approche Machine Learning Classique
> *"C'est pourquoi, à ce stade du cycle de vie, notre problème principal est un problème de Machine Learning Classique, et plus précisément de classification supervisée de texte.*  
> *Notre dataset répond parfaitement aux quatre critères de cadrage de la grille :*  
> *• **Critère (a) - Données étiquetées :** Nous disposons de milliers de tickets historiques déjà classés par catégories informatiques.*  
> *• **Critère (c) - Coût et Latence :** En utilisant une approche robuste comme TfidfVectorizer combinée à une LogisticRegression, notre modèle s'entraîne sur un simple ordinateur portable et prédit en quelques millisecondes pour un coût d'infrastructure nul.*  
> *• **Critère (d) - Conséquence d'une erreur :** L'impact d'un mauvais routage est faible et sera compensé dans l'interface en fixant un seuil d'incertitude pour alerter un agent humain."*

### [01:20 - 01:45] Conclusion et Évolution vers l'IA Agentique (Semaines 9-10)
> *"En conclusion, notre architecture logicielle va matérialiser ce choix : les premières semaines construiront cette brique de ML classique pour router les incidents. En semaine 9 et 10, nous ferons évoluer cette application vers un système hybride performant. Le modèle ML qualifiera le ticket, puis notre composant RAG interrogera les runbooks pour fournir la solution technique de manière totalement autonome. Notre dataset Kaggle est le socle idéal pour valider notre pipeline de bout en bout. Merci pour votre attention !"*
