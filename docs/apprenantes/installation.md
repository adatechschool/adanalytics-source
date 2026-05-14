# Installation

Ce guide t'accompagne pas à pas pour lancer le projet Adanalytics sur ta machine. Si tu rencontres un blocage, consulte [le troubleshooting de l'espace formateurice](https://github.com/adatechschool/adanalytics) ou demande sur le Slack `#bloc2-data`.

## Prérequis

| Outil | Version minimale | Vérification |
|---|---|---|
| Python | 3.10 | `python --version` ou `python3 --version` |
| pip | 22 | `pip --version` |
| Git | 2.x | `git --version` |

Sur **macOS** : Python est généralement déjà installé. Si non : `brew install python@3.11`.
Sur **Windows** : télécharger depuis [python.org](https://www.python.org/downloads/), cocher *"Add Python to PATH"* à l'installation.
Sur **Linux** : `sudo apt install python3 python3-venv python3-pip git`.

## Étape 1 — Récupérer le repo

```bash
git clone https://github.com/adatechschool/adanalytics.git
cd adanalytics
```

## Étape 2 — Créer un environnement virtuel

L'environnement virtuel isole les dépendances du projet de ton système. C'est une bonne pratique systématique.

**macOS / Linux :**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell) :**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Tu sais que l'environnement est actif quand `(.venv)` apparaît au début de ton prompt.

## Étape 3 — Installer les dépendances

```bash
pip install -r requirements.txt
```

Cela installe pandas, plotly, jupyter et leurs dépendances. L'installation peut prendre 2 à 5 minutes.

## Étape 4 — Vérifier que tout fonctionne

```bash
jupyter notebook
```

Une fenêtre de navigateur s'ouvre. Ouvre `notebooks/00-demarrage.ipynb` et exécute toutes les cellules (`Cell` → `Run All`). Si la dernière cellule affiche le résumé du dataset sans erreur, tu es prête.

## Workflow Git recommandé

Tu vas modifier des notebooks, créer des fichiers de travail. **Ne pousse rien sur le repo `adatechschool/adanalytics`** : c'est en lecture seule pour toi. Travaille dans **ton propre fork** ou un repo séparé pour ton analyse.

```bash
# Créer ton propre repo de travail à côté
# (à faire une seule fois)
mkdir ../mon-analyse-adanalytics
cd ../mon-analyse-adanalytics
git init
# y copier tes notebooks au fur et à mesure
```

Ou alternative : fork le repo officiel et travaille sur ta version.

## Mettre à jour le repo

Si une version corrigée du dataset ou un correctif est publié pendant le projet, tu pourras récupérer les changements via :

```bash
git pull origin main
```

Pense à committer ton travail (sur ton repo perso) avant de pull.

## Problèmes fréquents

**`python: command not found`** → essaye `python3` à la place. Sur Windows, vérifie que Python est bien dans le PATH.

**`pip install` échoue avec une erreur SSL** → tu es probablement derrière un proxy. Demande de l'aide sur Slack en partageant le message d'erreur complet.

**Jupyter ne s'ouvre pas dans le navigateur** → recopie l'URL `http://localhost:8888/?token=...` affichée dans le terminal et colle-la dans ton navigateur.

**Les imports `pandas` ou `plotly` échouent dans le notebook** → vérifie que ton environnement virtuel est bien activé **avant** de lancer Jupyter. Si Jupyter tourne avec le mauvais Python, tu peux installer le kernel : `python -m ipykernel install --user --name=adanalytics`.

**ModuleNotFoundError sur ipykernel** → `pip install ipykernel` puis relance Jupyter.
