# Dictionnaire de données

Ce document décrit le contenu de chaque fichier du dataset. Toutes les données sont **synthétiques** (générées par script) mais imitent fidèlement ce que produirait une vraie plateforme type Lovelace Factory.

> ⚠️ Les données présentent volontairement des **défauts** : doublons, valeurs manquantes, incohérences. C'est ton terrain d'exploration. Les défauts sont mentionnés dans chaque section.

---

## Vue d'ensemble

| Fichier | Format | Lignes (~) | Description |
|---|---|---|---|
| `data/raw/organizations.csv` | CSV | 18 | Promos et équipes utilisant la plateforme |
| `data/raw/users.csv` | CSV | 245 | Utilisateurices de la plateforme |
| `data/raw/projects.csv` | CSV | 95 | Projets créés sur la plateforme |
| `data/raw/tasks.csv` | CSV | 1850 | Tâches associées aux projets |
| `data/raw/task_assignments.csv` | CSV | ~2400 | Affectations tâche ↔ utilisateurice |
| `data/raw/comments.csv` | CSV | 3200 | Commentaires sur les tâches |
| `data/raw/activity_logs.json` | JSON | 12000 | Journal d'activité applicatif |
| `data/raw/performance_metrics.csv` | CSV | ~200 | Métriques journalières (6 mois) |
| `data/reference/promos.csv` | CSV | 18 | Table de référence propre (niveau de promo) |

Période couverte : **2024-09-01** à **2025-03-31** (7 mois).

---

## `organizations.csv`

Organisations ou promos rattachées à la plateforme.

| Colonne | Type | Description |
|---|---|---|
| `org_id` | string | Identifiant unique, format `org_XXX` |
| `name` | string | Nom lisible (ex. "Promo Curie") |
| `created_at` | datetime ISO | Date de création |
| `plan` | enum | `free`, `pro`, `enterprise` |
| `active` | bool | Organisation toujours active |

**Clé primaire :** `org_id`

---

## `users.csv`

Utilisateurices de la plateforme.

| Colonne | Type | Description |
|---|---|---|
| `user_id` | string | Identifiant unique, format `usr_XXXX` |
| `first_name` | string | Prénom |
| `last_name` | string | Nom de famille |
| `email` | string | Email (cf. défauts ci-dessous) |
| `age` | int | Âge déclaré (cf. défauts) |
| `org_id` | string | FK → `organizations.org_id` |
| `role` | enum | `member`, `lead`, `admin`, `observer` |
| `created_at` | datetime ISO | Date de création du compte |
| `last_login_at` | datetime ISO ou vide | Dernière connexion (vide = jamais connecté) |
| `is_active` | bool | Compte actif |

**Défauts connus :**
- ~5 vrais doublons (même personne enregistrée 2x avec un `user_id` différent mais email identique)
- ~3 % d'emails malformés (espace en tête, casse mixte)
- ~4 % d'âges aberrants (négatifs, > 100)
- ~7 % de `last_login_at` vides (jamais connectés)

---

## `projects.csv`

Projets créés sur la plateforme.

| Colonne | Type | Description |
|---|---|---|
| `project_id` | string | Identifiant unique, format `prj_XXXX` |
| `name` | string | Nom du projet |
| `org_id` | string | FK → `organizations.org_id` |
| `owner_id` | string | FK → `users.user_id` (porteuse du projet) |
| `status` | enum | `planning`, `active`, `completed`, `archived`, `on_hold` |
| `created_at` | datetime ISO | Date de création |
| `ended_at` | datetime ISO ou vide | Date de fin (uniquement si `status=completed`) |
| `budget_eur` | float ou vide | Budget en euros |

**Défauts connus :**
- ~5 % de projets dont le `owner_id` n'appartient pas à l'`org_id` du projet
- ~10 % de projets `completed` dont `ended_at < created_at`
- ~30 % de budgets manquants

---

## `tasks.csv`

Tâches associées aux projets.

| Colonne | Type | Description |
|---|---|---|
| `task_id` | string | Identifiant unique, format `tsk_XXXXX` |
| `project_id` | string | FK → `projects.project_id` |
| `title` | string | Intitulé de la tâche |
| `status` | enum | `todo`, `in_progress`, `in_review`, `done`, `blocked`, `cancelled` |
| `priority` | enum | `low`, `medium`, `high`, `critical` |
| `estimated_hours` | float ou vide | Estimation initiale en heures |
| `actual_hours` | float ou vide | Temps réellement passé (uniquement si `done`) |
| `created_at` | datetime ISO | Date de création |
| `completed_at` | datetime ISO ou vide | Date de complétion (uniquement si `done`) |

**Défauts connus :**
- ~4 % de titres tronqués (`"Implé..."`) ou vides
- ~15 % de `estimated_hours` manquantes
- ~5 % de `estimated_hours` aberrantes (0, négatives, 9999)

---

## `task_assignments.csv`

Table de jointure N-N entre tâches et utilisateurices.

| Colonne | Type | Description |
|---|---|---|
| `assignment_id` | string | Identifiant unique |
| `task_id` | string | FK → `tasks.task_id` |
| `user_id` | string | FK → `users.user_id` |
| `assigned_at` | datetime ISO | Date d'affectation |

**Défauts connus :**
- ~5 % des tâches n'ont aucune assignation (orphelines)

---

## `comments.csv`

Commentaires sur les tâches.

| Colonne | Type | Description |
|---|---|---|
| `comment_id` | string | Identifiant unique |
| `task_id` | string | FK → `tasks.task_id` |
| `user_id` | string | FK → `users.user_id` (cf. défauts) |
| `body` | string | Contenu textuel du commentaire |
| `created_at` | datetime ISO | Date du commentaire |

**Défauts connus :**
- ~3 % de `user_id` qui ne correspondent à aucun utilisateur (FK cassée)
- Quelques commentaires vides ou type spam (`"asdf"`, `"test test"`)
- ~5 % contiennent des emails dans le texte, ~3 % des numéros de téléphone (👉 **point RGPD important**)

---

## `activity_logs.json`

Journal d'activité applicatif, format JSON list.

```json
{
  "log_id": "log_000123",
  "timestamp": "2025-01-12T14:23:45",
  "user_id": "usr_0042",
  "action": "create_project",
  "ip_address": "82.144.12.7",
  "user_agent": "Mozilla/5.0 ...",
  "duration_ms": 234,
  "status_code": 200,
  "project_id": "prj_0017"      // présent seulement pour les actions liées aux projets
}
```

**Actions possibles :** `login`, `logout`, `create_project`, `update_project`, `delete_project`, `create_task`, `update_task`, `complete_task`, `comment_task`, `assign_task`, `view_dashboard`, `export_data`, `invite_user`, `change_status`, `upload_file`, `search`.

**Défauts connus :**
- ~2 % de timestamps au format français (`12/01/2025 14:23:45`) au lieu de l'ISO
- ~1 % sans `user_id`
- Le champ `project_id` n'est présent que pour les actions liées aux projets — ce n'est pas un défaut, c'est la structure logique du JSON

**Note RGPD :** les `ip_address` sont des données personnelles au sens du RGPD.

---

## `performance_metrics.csv`

Métriques applicatives agrégées par jour (proxy d'observabilité backend).

| Colonne | Type | Description |
|---|---|---|
| `date` | date | Jour (YYYY-MM-DD) |
| `total_requests` | int | Nombre total de requêtes HTTP |
| `error_rate` | float | Taux d'erreur (0.0 à 1.0) |
| `p50_latency_ms` | int | Médiane de la latence |
| `p95_latency_ms` | int | 95e percentile de la latence |
| `p99_latency_ms` | int | 99e percentile de la latence |
| `active_users` | int | Utilisateurices actives ce jour |
| `incident` | bool | Indicateur d'incident (taux d'erreur élevé) |

**Défauts connus :**
- ~2 % de jours manquants (trous dans la série temporelle)

---

## `data/reference/promos.csv`

Table de référence **propre** (sans défauts). Permet de croiser les organisations avec leur niveau de promo.

| Colonne | Type | Description |
|---|---|---|
| `org_id` | string | FK → `organizations.org_id` |
| `promo_code` | string | Code court (`P001`, `P002`, …) |
| `level` | enum | `junior`, `intermediate`, `senior` |

---

## Schéma relationnel

```
organizations  ──┐
                 ├─< users
                 └─< projects ─< tasks ─< task_assignments ─> users
                                     │
                                     └─< comments ─> users

activity_logs ───> users (et project_id parfois)
performance_metrics : pas de FK, série temporelle indépendante
```

## Conseil méthodologique

Ne tente pas de tout charger et tout nettoyer d'un coup. Pars de **ta problématique** : quelles tables sont nécessaires ? Quelles colonnes ? Quels défauts doivent être corrigés *pour cette analyse-là* ?

Un commentaire vide n'est un problème que si tu analyses la qualité des commentaires. Sinon, ignore-le.
