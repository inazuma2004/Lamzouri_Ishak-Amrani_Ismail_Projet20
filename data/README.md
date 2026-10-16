# 📊 Dataset : IT Service Ticket Classification

Ce document détaille le jeu de données officiel retenu pour l'entraînement et l'évaluation de notre pipeline de résolution d'incidents IT.

---

## 🔗 Lien Officiel Kaggle

* **Lien du Dataset :** [IT Service Ticket Classification Dataset sur Kaggle](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset)
* **Auteur / Source :** Adison Goh (Kaggle)
* **Fichier principal utilisé :** `all_tickets_processed_improved_v3.csv` (taille : ~14.5 Mo)

---

## 📐 Description & Caractéristiques

* **Nombre d'instances :** 47 837 tickets réels d'assistance informatique
* **Format :** CSV (Comma-Separated Values), encodage UTF-8
* **Champs du dataset :**
  1. `Document` *(Feature X)* : Description textuelle non structurée de la panne, de la réclamation ou du besoin saisie par l'employé / utilisateur (*ex: "unable to connect to internal vpn", "monitor screen flickering and turning black"*).
  2. `Topic_group` *(Target y)* : Catégorie d'incident assignée par les techniciens de support IT.

### Distribution des Catégories (`Topic_group`) :
1. **Hardware** (~13 617 tickets) : Problèmes matériels (écran, disque, chargeur, clavier...).
2. **HR Support** (~10 915 tickets) : Demandes liées aux ressources humaines et processus internes.
3. **Access** (~7 125 tickets) : Comptes verrouillés, mots de passe, accès VPN, habilitations.
4. **Miscellaneous** (~7 060 tickets) : Requêtes diverses non standard.
5. **Storage** (~2 777 tickets) : Espace disque saturé, accès aux partages réseaux.
6. **Purchase** (~2 464 tickets) : Demandes d'achat de matériel ou de licences logicielles.
7. **Internal Project** (~2 119 tickets) : Incidents sur les outils et serveurs de projets internes.
8. **Administrative rights** (~1 760 tickets) : Élévation de privilèges, permissions administrateur.

---

## ⚖️ Conformité avec les Règles du Cours

Le choix de ce dataset répond point par point aux contraintes imposées par **M. A. Larhlimi** :
- **100% Gratuit et Open Data :** Accessible librement sur Kaggle, aucune dépendance à des APIs payantes.
- **Entraînement local & léger :** Fichier tabulaire de 14.5 Mo. L'entraînement d'un pipeline scikit-learn complet (`TfidfVectorizer` + `LogisticRegression` ou `LinearSVC`) s'effectue en **moins d'une minute sur un ordinateur portable standard**.
- **Anonymisation et Éthique :** Données débarrassées de toute information nominative sensible (PII), respectant les exigences éthiques et légales (RGPD / Loi 09-08 Maroc).
- **Évolution naturelle vers le Mini-RAG & Agent (S9 - S10) :** La catégorie prédite permet d'aiguiller l'Agent Autonome directement vers les runbooks techniques correspondants (ex: runbook VPN pour la classe *Access*).

---

## 🚀 Téléchargement & Intégration dans le Projet

Pour respecter les règles strictes du versionnement MLOps, les fichiers CSV volumineux sont **ignorés par Git** via le fichier `.gitignore`.

Pour télécharger le dataset localement :
```bash
# Option A : Via l'API Kaggle CLI
kaggle datasets download -d adisongoh/it-service-ticket-classification-dataset -p data/ --unzip

# Option B : Téléchargement manuel
# Télécharger "all_tickets_processed_improved_v3.csv" depuis la page Kaggle et le déposer dans data/
```
