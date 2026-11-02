# Fiche de Cadrage Complète - Binôme : Lamzouri-Amrani - Projet 20

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
1. Classification automatique (8 catégories).
2. Seuil d'incertitude (60%) pour supervision humaine.
3. API REST pour intégration.
4. Interface Streamlit de pilotage.

**Périmètre** :
| Inclus | Exclu |
|---|---|
| Modèle ML supervisé (TF-IDF + LogReg) | Déploiement multi-cloud |
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
**Type** : ☑ Application web (Streamlit)
- **Écran 1** : Dashboard statistique (Vue d'ensemble).
- **Écran 2** : Interface de test (Input texte -> Classification -> Probabilités).
- **Écran 3** : Journal des prédictions douteuses (Supervision humaine).

**Architecture** :
`Utilisateur` ↔ `Streamlit` ↔ `API FastAPI` ↔ `Scikit-Learn Model`

---

## 6. Technologies et outils
### 6.1 Développement
| Catégorie | Outil | Justification |
|---|---|---|
| Langage | Python 3.13 | Standard académique |
| Framework | FastAPI | Performances API |
| Modèle | Scikit-Learn | Efficacité NLP classique |
| Tests | Pytest | Couverture unitaire/int |

### 6.2 Déploiement
| Catégorie | Outil | Justification |
|---|---|---|
| CI/CD | GitHub Actions | Automatisation |
| Monitoring | Journalisation locale | Traçabilité |

---

## 7. Répartition des tâches et calendrier
| Étape | Responsable | Début | Fin |
|---|---|---|---|
| Cadrage et Dataset | Ishak (A) | S1 | S2 |
| Préparation du dataset | Ismail (B) | S1 | S2 |
| Développement du cœur de l'agent | Ishak (A) | S2 | S3 |
| Intégration API & Tests | Ismail (B) | S3 | S4 |
| Interface utilisateur (UI) | Ishak (A) | S4 | S5 |
| Conteneurisation & Déploiement | Ismail (B) | S5 | S6 |
| Documentation & Présentation | Ishak (A) / Ismail (B) | S1 | S6 |

---

## 8. Questionnaire de cadrage

**Q1. Quel problème concret votre agent résout-il, et comment ce problème est-il traité aujourd'hui sans agent IA ?**
Le support informatique est saturé par des tickets récurrents. Sans agent, le routage est manuel, lent et coûteux.

**Q2. Qui est l'utilisateur final de votre agent, et comment interagit-il avec lui au quotidien ?**
Le technicien IT Helpdesk, via une interface web pour superviser les tickets routés.

**Q3. Quelle valeur ajoutée apporte l'agent par rapport à une solution classique ?**
Une automatisation intelligente qui s'adapte, contrairement aux règles fixes fragiles.

**Q4. Quelles sont les entrées de l'agent et quelles sorties produit-il ?**
Entrée : Texte brut (ticket). Sortie : Catégorie + Confiance. Ex: "VPN HS" -> "Access", 95%.

**Q5. Quelles décisions l'agent prend-il de façon autonome ?**
Le classement automatique par catégorie.

**Q6. Quel type de mémoire votre agent utilise-t-il ?**
Mémoire à court terme pour la requête actuelle et base de connaissance technique pour le RAG (future évolution).

**Q7. Décrivez la qualité de vos données : valeurs manquantes, bruit, déséquilibre, biais potentiels.**
Dataset nettoyé, classes équilibrées pour l'entraînement.

**Q8. Quelles sont les limites de votre dataset ?**
Jargon spécifique non présent dans le dataset pouvant causer des erreurs.

**Q9. Justifiez le choix de votre framework d'agents et de votre modèle LLM.**
Scikit-learn pour le ML classique (coût/performance). 

**Q10. Comment votre architecture gère-t-elle les erreurs ?**
Seuil d'abstention (60%) : si < 60%, routage manuel.

**Q11. Décrivez l'environnement de déploiement cible.**
Web conteneurisée via Docker (S6).

**Q12. Quels sont les coûts d'exploitation attendus ?**
Coût nul (ML classique local). Évolutivité gérée par API stateless.

**Q13. Quelles métriques utiliserez-vous pour évaluer votre agent ?**
F1-Macro score (> 0.85). Critère : Amélioration du temps de routage.

**Q14. Quels tests prévoyez-vous ?**
Tests unitaires (pytest) sur API, tests d'intégration, jeu de données de référence (gold set).

**Q15. Identifiez les principaux risques de votre projet.**
Sécurité (validation Pydantic), éthique (biais de données).
