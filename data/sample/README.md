# Échantillon de Données (Sample Dataset) — Incidents IT

Ce dossier contient un échantillon représentatif et léger du jeu de données principal utilisé pour l'entraînement et la validation de l'agent intelligent de résolution d'incidents IT.

## 📁 Contenu

| Fichier | Format | Lignes | Taille | Description |
|---|---|---|---|---|
| `tickets_sample.csv` | CSV (UTF-8) | 120 lignes | 32,7 Ko | Échantillon équilibré de 15 tickets par catégorie pour les 8 classes du projet. |

## 🏷️ Structure des colonnes

- **`Document`** : description de l'incident, en anglais, écrite par un employé, déjà nettoyée par l'auteur du dataset (minuscules, sans ponctuation ni chiffres).
- **`Topic_group`** : Catégorie cible assignée par le support IT parmi les 8 classes :
  1. `Hardware`
  2. `HR Support`
  3. `Access`
  4. `Miscellaneous`
  5. `Storage`
  6. `Purchase`
  7. `Internal Project`
  8. `Administrative rights`

## ⚖️ Licence et Origine

- **Origine :** Sous-ensemble extrait de `all_tickets_processed_improved_v3.csv` (Kaggle IT Service Ticket Classification Dataset par Adison Goh).
- **Licence :** CC0 : Domaine Public (usage libre, académique et commercial).
- **Données personnelles :** aucune repérée : aucun chiffre, adresse e-mail ni adresse IP dans les 47 837 tickets du jeu complet (recherche par expression régulière, 19/11/2026). Les noms propres ne se détectent pas automatiquement.

