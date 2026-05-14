# Données

Ce dossier contient les données du projet Adanalytics.

## Structure

- **`raw/`** : données brutes telles qu'elles seraient exportées d'une plateforme Lovelace Factory en production. **Volontairement imparfaites** — c'est ton terrain de nettoyage.
- **`reference/`** : tables de référence propres, à utiliser comme socle stable pour tes croisements.

## Description détaillée

Voir le **[dictionnaire de données complet](../docs/apprenantes/dictionnaire-donnees.md)** pour la description champ par champ de chaque fichier, les défauts connus et le schéma relationnel.

## Régénération

Les fichiers de ce dossier sont produits par `../scripts/generate_data.py`. Reproductibles avec `--seed 42`.
