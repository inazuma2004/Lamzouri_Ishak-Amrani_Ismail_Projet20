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
| **Emplacement des données complètes** | Racine locale du projet : `data/all_tickets_processed_improved_v3.csv` |

## 2.2 Qualité constatée sur l'échantillon

L'inspection de l'échantillon extrait dans `data/sample/tickets_sample.csv` (120 lignes, 15 exemples par classe) montre :
- **Valeurs manquantes :** 0 valeur nulle ou vide sur l'ensemble du dataset (`Document` et `Topic_group` sont systématiquement renseignés).
- **Distribution des 8 classes :**
  1. `Hardware` : 13 617 tickets (28.5 %)
  2. `HR Support` : 10 915 tickets (22.8 %)
  3. `Access` : 7 125 tickets (14.9 %)
  4. `Miscellaneous` : 7 060 tickets (14.8 %)
  5. `Storage` : 2 777 tickets (5.8 %)
  6. `Purchase` : 2 464 tickets (5.1 %)
  7. `Internal Project` : 2 119 tickets (4.4 %)
  8. `Administrative rights` : 1 760 tickets (3.7 %)
- **Prise en charge du déséquilibre :** Le déséquilibre naturel est compensé dans le pipeline Scikit-Learn via le paramètre `class_weight='balanced'`.

## 2.3 Justification par fonctionnalité

| Fonctionnalité | Données utilisées | En quoi elles suffisent |
| --- | --- | --- |
| **F1 (Classification)** | Les colonnes `Document` et `Topic_group` sur 47 837 exemples | Le volume élevé et la diversité du vocabulaire permettent d'obtenir un score F1-macro > 0.85 en validation croisée. |
| **F2 (Incertitude)** | Les probabilités de sortie (`predict_proba`) calculées sur les classes | Les tickets ambigus aux frontières de décision ont des scores faibles (<0.60), ce qui valide le seuil d'abstention. |
| **F3 (Lot CSV)** | La structure tabulaire standard du fichier CSV | Permet de simuler directement l'injection de fichiers de tickets en production dans l'interface Streamlit. |

## 2.4 Alternative de repli

En cas d'indisponibilité de la source Kaggle principale, nous disposons :
1. De l'archive locale complète conservée dans `data/archive.zip` (100% autonome sans connexion internet).
2. Du dataset public alternatif *"IT Support Tickets"* de Suraj Kumar sur Kaggle.
*Perte en cas de repli :* Réajustement mineur du dictionnaire des catégories (passant de 8 à 5 classes).

## 2.5 Jeu de test

- **Jeu d'or unitaire :** 20 cas représentatifs rédigés et validés par l'équipe dans `tests/test_jeu_or.py`, couvrant des formulations directes, des variantes orthographiques, du jargon technique et des tickets volontairement ambigus.
- **Jeu de test d'évaluation globale :** 20% du dataset principal (soit environ 9 567 tickets) réservés pour le test final hors entraînement (`test_size=0.20`, `stratify=y`, `random_state=42`).

---

## Critères d'acceptation (vérifiés par le relecteur)

- [x] L'échantillon est présent dans `data/sample/tickets_sample.csv` (120 lignes) et s'ouvre sans erreur.
- [x] La licence CC0 autorise l'usage sans restriction dans le cadre du cours.
- [x] Aucune donnée personnelle (PII) n'est présente dans le dépôt.
- [x] Toutes les fonctionnalités du MVP sont justifiées par les données.
- [x] L'alternative de repli est documentée et testée localement.
- [x] Le jeu d'or de test est formalisé et exécuté automatiquement par pytest.

