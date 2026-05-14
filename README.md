# Adanalytics

> Dataset et environnement de démarrage pour le projet **Adanalytics** — spécialité Data, Bloc 2 — Ada Tech School.

Ce dépôt contient les **données générées par Lovelace Factory** que tu vas analyser pendant les semaines 5 à 15. Tu y trouveras des données issues de plusieurs sources (PostgreSQL exporté en CSV, logs JSON, métriques applicatives), volontairement **imparfaites** : c'est à toi de les explorer, les nettoyer, les croiser et les faire parler.

---

## 🎯 Objectif du projet

Formuler une problématique métier à partir des données disponibles, construire un pipeline d'analyse documenté et produire un tableau de bord interactif. Le brief complet est sur Moodle.

## 📦 Ce qu'il y a dans ce repo

```
adanalytics/
├── data/
│   ├── raw/              ← les données brutes à analyser (sales)
│   └── reference/        ← tables de référence propres
├── notebooks/
│   ├── 00-demarrage.ipynb       ← charger et inspecter les données
│   └── 01-exemple-exploration.ipynb  ← exemple guidé si tu es bloquée
├── docs/
│   ├── apprenantes/      ← installation, dictionnaire de données, RGPD
│   └── formateurices/    ← réservé aux formateurices
├── scripts/
│   └── generate_data.py  ← script qui a produit le dataset
└── requirements.txt
```

## 🚀 Démarrage rapide

**Prérequis :** Python 3.10 ou plus, Git, Jupyter.

```bash
# 1. Cloner le repo
git clone https://github.com/adatechschool/adanalytics.git
cd adanalytics

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate            # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer Jupyter
jupyter notebook
```

Ouvre ensuite `notebooks/00-demarrage.ipynb` pour vérifier que tout fonctionne.

## 📚 Que lire en premier

1. [`docs/apprenantes/installation.md`](docs/apprenantes/installation.md) — installation détaillée
2. [`docs/apprenantes/dictionnaire-donnees.md`](docs/apprenantes/dictionnaire-donnees.md) — description de chaque table et champ
3. [`docs/apprenantes/rgpd.md`](docs/apprenantes/rgpd.md) — enjeux réglementaires du dataset
4. `notebooks/00-demarrage.ipynb` — chargement des données

## ⚠️ Le dataset est volontairement imparfait

Tu vas y trouver des doublons, des valeurs manquantes, des incohérences, des outliers et des formats hétérogènes. **C'est normal**, c'est ton terrain d'entraînement au nettoyage. Les vrais datasets en entreprise ressemblent à ça.

Tu n'es pas censée tout corriger d'un coup. Le travail de nettoyage doit être **piloté par ta problématique** : tu ne nettoies que ce qui sert ta question.

## 🔁 Régénérer le dataset

Si tu veux explorer une variante du dataset (par exemple pour t'entraîner sur d'autres données), tu peux régénérer un dataset avec un autre seed :

```bash
python scripts/generate_data.py --seed 123 --output data
```

**Attention :** la correction et les attendus se basent sur le dataset par défaut (`--seed 42`). Ne change pas le seed sans raison.

## 🧑‍🏫 Formateurices

La doc d'animation (lancement du projet, grille d'évaluation, pistes d'analyses, FAQ) est réservée aux formateurices et distribuée séparément — elle ne fait pas partie de ce repo.

## 📄 Licence

Code et données pédagogiques sous licence MIT. Voir [`LICENSE`](LICENSE).
