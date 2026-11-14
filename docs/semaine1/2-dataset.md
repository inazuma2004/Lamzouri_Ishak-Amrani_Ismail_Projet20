# Livrable 2 : Dataset

**Rédacteur :** Ismail Amrani ([@Amaranix](https://github.com/Amaranix))  
**Relecteur :** Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004))  
**Fichiers :** `docs/semaine1/2-dataset.md` + `data/sample/tickets_sample.csv`

---

## 2.1 Description

| Rubrique | Réponse |
| --- | --- |
| **Nom et source (lien)** | `all_tickets_processed_improved_v3.csv` — [Kaggle IT Service Ticket Classification Dataset](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset) |
| **Producteur ou propriétaire** | Adison Goh (données réelles anonymisées issues d'un centre de support informatique d'entreprise) |
| **Volume** | 47 837 lignes, 2 colonnes, environ 14.5 Mo |
| **Format et structure** | Fichier CSV (encodage UTF-8, séparateur virgule). Colonnes : `Document` (texte brut de l'incident), `Topic_group` (catégorie) |
| **Langue et période couverte** | Anglais technique d'entreprise, historique d'incidents IT récents |
| **Licence et droits d'usage** | CC0 : Domaine Public (autorisation totale d'utilisation académique et commerciale sans restriction) |
| **Données personnelles ou sensibles** | Aucune : les données ont fait l'objet d'une anonymisation stricte préalable (noms d'utilisateurs, adresses IP et identifiants masqués) |
| **Emplacement des données complètes** | `data/all_tickets_processed_improved_v3.csv`, hors Git, versionné par DVC (pointeur `.dvc` de 126 octets, empreinte md5 `a05aa13d…`) ; source d'origine : Kaggle |

## 2.2 Qualité constatée sur l'échantillon

L'échantillon `data/sample/tickets_sample.csv` compte 120 lignes, 15 par classe (équilibré par construction). Sur le jeu complet :
- **Valeurs manquantes :** 0 valeur nulle ou vide sur l'ensemble du dataset (`Document` et `Topic_group` sont systématiquement renseignés).
- **Distribution des 8 classes (jeu complet, 47 837 tickets) :**
  1. `Hardware` : 13 617 tickets (28.5 %)
  2. `HR Support` : 10 915 tickets (22.8 %)
  3. `Access` : 7 125 tickets (14.9 %)
  4. `Miscellaneous` : 7 060 tickets (14.8 %)
  5. `Storage` : 2 777 tickets (5.8 %)
  6. `Purchase` : 2 464 tickets (5.1 %)
  7. `Internal Project` : 2 119 tickets (4.4 %)
  8. `Administrative rights` : 1 760 tickets (3.7 %)
- **Prise en charge du déséquilibre :** le rapport est de 1 à 8 entre la plus petite classe et la plus grande ; il est compensé dans le pipeline scikit-learn par `class_weight='balanced'`.
- **Bruit constaté :** certaines étiquettes sont discutables (des tickets Outlook étiquetés `Administrative rights`, des alertes serveur étiquetées `Hardware`) et certains textes sont presque vides après nettoyage. Ces cas expliquent l'essentiel des erreurs du modèle.

## 2.3 Justification par fonctionnalité

| Fonctionnalité | Données utilisées | En quoi elles suffisent |
| --- | --- | --- |
| **F1 (Classification)** | Les colonnes `Document` et `Topic_group` sur 47 837 exemples | Le volume et la diversité du vocabulaire donnent un F1 macro de 0,868 sur un jeu de test disjoint (20 %, jamais vu à l'entraînement). |
| **F2 (Incertitude)** | Les probabilités de sortie (`predict_proba`) calculées sur les classes | Au seuil de 0,60, le modèle traite seul 78,4 % des tickets de test, avec 94,2 % de justesse sur ceux-là ; les autres partent chez un technicien. |
| **F3 (Lot CSV)** | La structure tabulaire standard du fichier CSV | Permet de simuler directement l'injection de fichiers de tickets en production dans l'interface Streamlit. |

## 2.4 Alternative de repli

En cas d'indisponibilité de la source Kaggle principale, nous disposons :
1. De l'archive locale complète conservée dans `data/archive.zip` (100% autonome sans connexion internet).
2. Du dataset public alternatif *"IT Support Tickets"* de Suraj Kumar sur Kaggle.
*Perte en cas de repli :* Réajustement mineur du dictionnaire des catégories (passant de 8 à 5 classes).

## 2.5 Jeu de test

- **Jeu d'or des tickets :** 20 tickets rédigés par l'équipe avec la catégorie attendue (`tests/jeu_or.csv`, lu par `tests/test_jeu_or.py`) : 11 justes, 6 abstentions, 3 erreurs franches déclarées comme erreurs connues.
- **Jeu d'or des procédures :** 17 requêtes avec la section de runbook attendue (`tests/jeu_or_rag.csv`), dont 4 reformulées sans les mots du runbook et 3 hors sujet qui doivent être refusées.
- **Jeu de test d'évaluation globale :** 20% du dataset principal (9 568 tickets) réservés pour le test final hors entraînement (`test_size=0.20`, `stratify=y`, `random_state=42`).

---

## Critères d'acceptation (vérifiés par le relecteur)

- [x] L'échantillon est présent dans `data/sample/tickets_sample.csv` (120 lignes) et s'ouvre sans erreur.
- [x] La licence CC0 autorise l'usage sans restriction dans le cadre du cours.
- [x] Aucune donnée personnelle (PII) n'est présente dans le dépôt.
- [x] Toutes les fonctionnalités du MVP sont justifiées par les données.
- [x] L'alternative de repli est documentée et testée localement.
- [x] Les deux jeux d'or sont formalisés et exécutés automatiquement par pytest.

