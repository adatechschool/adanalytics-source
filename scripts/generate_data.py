"""
Générateur de données Lovelace Factory pour le projet Adanalytics.

Ce script produit un dataset réaliste mais SYNTHÉTIQUE simulant l'activité
d'une plateforme de gestion de projets type "Lovelace Factory".

Les données sont volontairement IMPARFAITES (doublons, valeurs manquantes,
incohérences de format, outliers) pour donner du grain à moudre aux
apprenantes lors de la phase de nettoyage.

Reproductible : on fixe le seed pour que chaque exécution produise
exactement le même dataset (utile pour la correction).

Usage :
    python scripts/generate_data.py
    python scripts/generate_data.py --seed 42 --output data/raw

Sortie :
    data/raw/users.csv
    data/raw/organizations.csv
    data/raw/projects.csv
    data/raw/tasks.csv
    data/raw/task_assignments.csv
    data/raw/comments.csv
    data/raw/activity_logs.json
    data/raw/performance_metrics.csv
    data/reference/promos.csv
"""

import argparse
import csv
import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

# ----- Paramètres globaux du dataset -----
NB_ORGS = 18
NB_USERS = 240
NB_PROJECTS = 95
NB_TASKS = 1850
NB_COMMENTS = 3200
NB_LOGS = 12000
NB_METRICS_DAYS = 180  # 6 mois de métriques journalières

START_DATE = datetime(2024, 9, 1)
END_DATE = datetime(2025, 3, 31)

# Pools réalistes
FIRST_NAMES = [
    "Camille", "Sarah", "Lina", "Inès", "Yasmine", "Léa", "Manon", "Chloé",
    "Anissa", "Fatou", "Awa", "Mariam", "Aïcha", "Sophie", "Emma", "Jade",
    "Louise", "Alice", "Maya", "Nora", "Salma", "Khadija", "Amina", "Zoé",
    "Romane", "Juliette", "Clara", "Eva", "Lou", "Mia", "Iris", "Margot",
    "Théo", "Lucas", "Hugo", "Léo", "Adam", "Raphaël", "Arthur", "Louis",
    "Yanis", "Mehdi", "Karim", "Idriss", "Sami", "Noah", "Gabriel",
]
LAST_NAMES = [
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Petit", "Richard",
    "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefèvre", "Michel",
    "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier", "Morel",
    "Girard", "André", "Lefebvre", "Mercier", "Dupont", "Lambert", "Bonnet",
    "François", "Martinez", "Legrand", "Garnier", "Faure", "Rousseau",
    "Blanc", "Guerin", "Muller", "Henry", "Roussel", "Nicolas", "Perrin",
    "Morin", "Mathieu", "Clément", "Gauthier", "Dumont", "Lopez",
    "Diallo", "Traoré", "Cissé", "Ben Ali", "Cherif", "Bensaid", "Hadj",
]
DOMAINS = [
    "gmail.com", "outlook.com", "yahoo.fr", "hotmail.fr", "protonmail.com",
    "lovelace-factory.com", "lovelace-factory.fr",
]
ORG_NAMES = [
    "Promo Curie", "Promo Hopper", "Promo Lovelace", "Promo Goldwasser",
    "Promo Joliot", "Promo Noether", "Promo Yalow", "Promo Bell",
    "Cohorte 2024-1", "Cohorte 2024-2", "Cohorte Alpha", "Cohorte Beta",
    "Equipe Pédagogique", "Squad Carrière", "Admin Ada", "Test interne",
    "Promo Tester", "Promo Ada",
]
PROJECT_PREFIXES = [
    "API", "Dashboard", "Refonte", "Migration", "POC", "MVP", "V2",
    "Outil", "Plateforme", "Module", "Pipeline", "Système",
]
PROJECT_TOPICS = [
    "compta", "RH", "gestion projet", "CRM", "facturation", "support client",
    "monitoring", "analytics", "réservation", "logistique", "e-commerce",
    "newsletter", "onboarding", "auth", "billing", "reporting",
]
TASK_VERBS = [
    "Implémenter", "Corriger", "Tester", "Déployer", "Documenter", "Refactor",
    "Designer", "Estimer", "Spécifier", "Valider", "Reviewer", "Optimiser",
]
TASK_OBJECTS = [
    "endpoint /users", "formulaire login", "page profil", "système d'auth",
    "export CSV", "filtre de recherche", "modal de confirmation",
    "pipeline CI", "dockerfile backend", "schéma BDD", "migration",
    "API utilisateurs", "composant Header", "footer", "tests unitaires",
    "documentation", "wireframes", "maquettes Figma", "intégration Stripe",
    "envoi d'emails", "gestion des erreurs", "logs structurés",
]
TASK_STATUSES = ["todo", "in_progress", "in_review", "done", "blocked", "cancelled"]
TASK_STATUS_WEIGHTS = [0.20, 0.18, 0.10, 0.42, 0.05, 0.05]
TASK_PRIORITIES = ["low", "medium", "high", "critical"]
TASK_PRIORITY_WEIGHTS = [0.25, 0.45, 0.22, 0.08]
ROLES = ["member", "lead", "admin", "observer"]
ROLE_WEIGHTS = [0.65, 0.20, 0.08, 0.07]
LOG_ACTIONS = [
    "login", "logout", "create_project", "update_project", "delete_project",
    "create_task", "update_task", "complete_task", "comment_task",
    "assign_task", "view_dashboard", "export_data", "invite_user",
    "change_status", "upload_file", "search",
]
COMMENT_SAMPLES = [
    "C'est OK pour moi",
    "À revoir avec l'équipe design",
    "Done ✓",
    "Je m'en occupe demain",
    "Bloqué sur la connexion BDD, besoin d'aide",
    "Merci !",
    "Voir issue #42",
    "Pourquoi pas avec une approche différente ?",
    "Ça marche en local mais pas en prod, à creuser",
    "Validé par le client",
    "Pas urgent, on verra en S7",
    "+1",
    "Je propose qu'on en discute mardi",
    "Spec à jour dans Notion",
    "Test passé, prêt à merger",
    "Reviewer SVP avant jeudi",
    "Cf. capture d'écran",
    "Trop compliqué, à simplifier",
    "Question : doit-on gérer le cas X ?",
    "OK rebase et merge",
    "",  # commentaire vide (donnée sale)
    "test test test",  # commentaire de spam (donnée sale)
    "asdf",  # commentaire bidon
]


def random_date(start: datetime, end: datetime) -> datetime:
    """Tire une date aléatoire entre start et end."""
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def slugify(text: str) -> str:
    """Slug simple pour les emails."""
    text = text.lower()
    replacements = {"à": "a", "â": "a", "ä": "a", "é": "e", "è": "e", "ê": "e",
                    "ë": "e", "î": "i", "ï": "i", "ô": "o", "ö": "o", "ù": "u",
                    "û": "u", "ü": "u", "ç": "c", " ": ".", "'": ""}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return "".join(c for c in text if c.isalnum() or c == ".")


# ============================================================
# Génération des entités
# ============================================================

def gen_organizations() -> list[dict]:
    """Génère les organisations (promos / équipes)."""
    orgs = []
    names = random.sample(ORG_NAMES, NB_ORGS)
    for i, name in enumerate(names, start=1):
        created = random_date(START_DATE, START_DATE + timedelta(days=60))
        orgs.append({
            "org_id": f"org_{i:03d}",
            "name": name,
            "created_at": created.isoformat(),
            "plan": random.choices(
                ["free", "pro", "enterprise"], weights=[0.5, 0.35, 0.15]
            )[0],
            "active": random.choices([True, False], weights=[0.85, 0.15])[0],
        })
    return orgs


def gen_users(orgs: list[dict]) -> list[dict]:
    """Génère les utilisateurices, rattachées à une organisation."""
    users = []
    used_emails = set()
    for i in range(1, NB_USERS + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        # Une partie des emails est mal formattée (donnée sale)
        domain = random.choice(DOMAINS)
        base_email = f"{slugify(first)}.{slugify(last)}@{domain}"
        # ~5% de doublons d'email avec suffixe numérique pour casser la cohérence
        if base_email in used_emails or random.random() < 0.03:
            base_email = f"{slugify(first)}.{slugify(last)}{random.randint(1, 99)}@{domain}"
        # ~3% d'emails malformés (espace en trop, majuscules)
        if random.random() < 0.03:
            base_email = " " + base_email.upper()
        used_emails.add(base_email)

        org = random.choice(orgs)
        created = random_date(START_DATE, END_DATE - timedelta(days=30))

        # ~7% n'ont pas de date de dernière connexion (jamais connectés)
        if random.random() < 0.07:
            last_login = None
        else:
            last_login = random_date(created, END_DATE).isoformat()

        # ~4% ont un âge incohérent (donnée sale)
        if random.random() < 0.04:
            age = random.choice([-3, 0, 15, 150, 999])
        else:
            age = random.randint(20, 55)

        users.append({
            "user_id": f"usr_{i:04d}",
            "first_name": first,
            "last_name": last,
            "email": base_email,
            "age": age,
            "org_id": org["org_id"],
            "role": random.choices(ROLES, weights=ROLE_WEIGHTS)[0],
            "created_at": created.isoformat(),
            "last_login_at": last_login,
            "is_active": random.choices([True, False], weights=[0.82, 0.18])[0],
        })

    # On ajoute ~5 vrais doublons exacts (même personne enregistrée 2x)
    duplicates = random.sample(users, 5)
    for dup in duplicates:
        copy = dict(dup)
        copy["user_id"] = f"usr_{len(users) + 1:04d}"
        users.append(copy)

    return users


def gen_projects(orgs: list[dict], users: list[dict]) -> list[dict]:
    """Génère les projets, rattachés à une org et à un·e owner."""
    projects = []
    for i in range(1, NB_PROJECTS + 1):
        org = random.choice(orgs)
        # On veut un owner qui appartient à l'org (cohérence)... la plupart du temps
        org_users = [u for u in users if u["org_id"] == org["org_id"]]
        if org_users and random.random() > 0.05:
            owner = random.choice(org_users)
        else:
            owner = random.choice(users)  # incohérence volontaire dans 5% des cas

        created = random_date(START_DATE, END_DATE - timedelta(days=10))
        name = f"{random.choice(PROJECT_PREFIXES)} {random.choice(PROJECT_TOPICS)}"

        # ~10% de projets terminés ont une date de fin avant date de début (donnée sale)
        status = random.choices(
            ["planning", "active", "completed", "archived", "on_hold"],
            weights=[0.10, 0.50, 0.25, 0.10, 0.05],
        )[0]

        if status == "completed":
            if random.random() < 0.10:
                # incohérence : fin avant début
                end = created - timedelta(days=random.randint(1, 30))
            else:
                end = random_date(created, END_DATE)
            end_str = end.isoformat()
        else:
            end_str = None

        projects.append({
            "project_id": f"prj_{i:04d}",
            "name": name,
            "org_id": org["org_id"],
            "owner_id": owner["user_id"],
            "status": status,
            "created_at": created.isoformat(),
            "ended_at": end_str,
            "budget_eur": round(random.uniform(500, 50000), 2) if random.random() > 0.30 else None,
        })
    return projects


def gen_tasks(projects: list[dict]) -> list[dict]:
    """Génère les tâches, rattachées à un projet."""
    tasks = []
    for i in range(1, NB_TASKS + 1):
        project = random.choice(projects)
        created_base = datetime.fromisoformat(project["created_at"])
        # Tâche créée entre date de projet et END_DATE
        created = random_date(created_base, END_DATE)

        status = random.choices(TASK_STATUSES, weights=TASK_STATUS_WEIGHTS)[0]
        priority = random.choices(TASK_PRIORITIES, weights=TASK_PRIORITY_WEIGHTS)[0]
        title = f"{random.choice(TASK_VERBS)} {random.choice(TASK_OBJECTS)}"

        # ~8% de titres tronqués / vides (donnée sale)
        if random.random() < 0.04:
            title = title[:5] + "..."
        elif random.random() < 0.04:
            title = ""

        if status == "done":
            completed = random_date(created, min(END_DATE, created + timedelta(days=45)))
            completed_str = completed.isoformat()
            actual_hours = round(random.uniform(0.5, 30), 1)
        else:
            completed_str = None
            actual_hours = None

        # Estimated hours : ~15% manquant, ~5% absurde
        if random.random() < 0.15:
            est_hours = None
        elif random.random() < 0.05:
            est_hours = random.choice([0, -2, 9999])
        else:
            est_hours = round(random.choice([0.5, 1, 2, 4, 8, 16, 24]) +
                              random.uniform(-0.5, 2), 1)

        tasks.append({
            "task_id": f"tsk_{i:05d}",
            "project_id": project["project_id"],
            "title": title,
            "status": status,
            "priority": priority,
            "estimated_hours": est_hours,
            "actual_hours": actual_hours,
            "created_at": created.isoformat(),
            "completed_at": completed_str,
        })
    return tasks


def gen_task_assignments(tasks: list[dict], users: list[dict]) -> list[dict]:
    """Affectations N-N entre tâches et utilisateurices."""
    assignments = []
    aid = 1
    for task in tasks:
        # ~5% des tâches n'ont pas d'assignation
        if random.random() < 0.05:
            continue
        # 1 à 3 personnes par tâche
        nb = random.choices([1, 2, 3], weights=[0.70, 0.22, 0.08])[0]
        assignees = random.sample(users, nb)
        for u in assignees:
            assignments.append({
                "assignment_id": f"asg_{aid:06d}",
                "task_id": task["task_id"],
                "user_id": u["user_id"],
                "assigned_at": task["created_at"],
            })
            aid += 1
    return assignments


def gen_comments(tasks: list[dict], users: list[dict]) -> list[dict]:
    """Commentaires sur les tâches."""
    comments = []
    for i in range(1, NB_COMMENTS + 1):
        task = random.choice(tasks)
        user = random.choice(users)
        created = random_date(
            datetime.fromisoformat(task["created_at"]),
            END_DATE,
        )
        # ~8% de commentaires avec utilisateurice qui n'existe pas (FK cassée)
        if random.random() < 0.03:
            user_id = f"usr_{random.randint(9000, 9999):04d}"
        else:
            user_id = user["user_id"]

        body = random.choice(COMMENT_SAMPLES)
        # ~5% contiennent un email (à signaler côté RGPD)
        if random.random() < 0.05:
            body = body + f" cf {slugify(random.choice(FIRST_NAMES))}.{slugify(random.choice(LAST_NAMES))}@gmail.com"
        # ~3% contiennent un numéro de téléphone (donnée perso)
        if random.random() < 0.03:
            body = body + f" tel : 06{random.randint(10000000, 99999999)}"

        comments.append({
            "comment_id": f"cmt_{i:06d}",
            "task_id": task["task_id"],
            "user_id": user_id,
            "body": body,
            "created_at": created.isoformat(),
        })
    return comments


def gen_activity_logs(users: list[dict], projects: list[dict]) -> list[dict]:
    """Logs d'activité au format JSON structuré."""
    logs = []
    for i in range(1, NB_LOGS + 1):
        user = random.choice(users)
        action = random.choice(LOG_ACTIONS)
        ts = random_date(START_DATE, END_DATE)

        log = {
            "log_id": f"log_{i:06d}",
            "timestamp": ts.isoformat(),
            "user_id": user["user_id"],
            "action": action,
            "ip_address": f"{random.randint(10, 220)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
            "user_agent": random.choice([
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120",
                "Mozilla/5.0 (Windows NT 10.0) Firefox/119",
                "Mozilla/5.0 (X11; Linux x86_64) Chrome/121",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Safari/605",
            ]),
            "duration_ms": random.choices(
                [random.randint(20, 200), random.randint(200, 1000), random.randint(1000, 8000)],
                weights=[0.70, 0.25, 0.05],
            )[0],
            "status_code": random.choices(
                [200, 201, 304, 400, 401, 404, 500],
                weights=[0.65, 0.10, 0.10, 0.05, 0.05, 0.03, 0.02],
            )[0],
        }

        # Ajout de contexte selon l'action
        if action in ("create_project", "update_project", "delete_project"):
            log["project_id"] = random.choice(projects)["project_id"]

        # ~2% des logs ont un timestamp mal formatté (donnée sale)
        if random.random() < 0.02:
            log["timestamp"] = ts.strftime("%d/%m/%Y %H:%M:%S")  # format FR au lieu d'ISO

        # ~1% n'ont pas de user_id
        if random.random() < 0.01:
            log["user_id"] = None

        logs.append(log)

    return logs


def gen_performance_metrics() -> list[dict]:
    """Métriques applicatives journalières (proxy d'observabilité)."""
    metrics = []
    current = START_DATE
    day = 1
    while current <= END_DATE:
        # Pattern hebdo : moins d'activité le week-end
        weekday = current.weekday()
        weekend_factor = 0.35 if weekday >= 5 else 1.0

        base_requests = int(random.gauss(8500, 1200) * weekend_factor)
        # ~3% de jours avec un incident (pic d'erreurs)
        is_incident = random.random() < 0.03
        if is_incident:
            error_rate = round(random.uniform(0.08, 0.25), 4)
            p95_latency = random.randint(1500, 4500)
        else:
            error_rate = round(random.uniform(0.001, 0.02), 4)
            p95_latency = random.randint(150, 600)

        metrics.append({
            "date": current.strftime("%Y-%m-%d"),
            "total_requests": max(0, base_requests),
            "error_rate": error_rate,
            "p50_latency_ms": random.randint(40, 180),
            "p95_latency_ms": p95_latency,
            "p99_latency_ms": p95_latency + random.randint(100, 800),
            "active_users": int(random.gauss(120, 30) * weekend_factor),
            "incident": is_incident,
        })
        current += timedelta(days=1)
        day += 1

    # ~2% de jours manquants (volontairement supprimés)
    nb_remove = int(len(metrics) * 0.02)
    to_remove = random.sample(range(len(metrics)), nb_remove)
    return [m for i, m in enumerate(metrics) if i not in to_remove]


def gen_promos_reference() -> list[dict]:
    """Table de référence propre : correspondance org_id -> infos promo."""
    return [
        {"org_id": f"org_{i:03d}", "promo_code": f"P{i:03d}",
         "level": random.choice(["junior", "intermediate", "senior"])}
        for i in range(1, NB_ORGS + 1)
    ]


# ============================================================
# Écriture des fichiers
# ============================================================

def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(seed: int, output_dir: Path) -> None:
    random.seed(seed)
    print(f"🌱 Génération avec seed={seed}")
    print(f"📁 Sortie : {output_dir.resolve()}")

    raw = output_dir / "raw"
    ref = output_dir / "reference"

    print("→ organisations…")
    orgs = gen_organizations()
    write_csv(raw / "organizations.csv", orgs,
              ["org_id", "name", "created_at", "plan", "active"])

    print("→ utilisateurices…")
    users = gen_users(orgs)
    write_csv(raw / "users.csv", users,
              ["user_id", "first_name", "last_name", "email", "age",
               "org_id", "role", "created_at", "last_login_at", "is_active"])

    print("→ projets…")
    projects = gen_projects(orgs, users)
    write_csv(raw / "projects.csv", projects,
              ["project_id", "name", "org_id", "owner_id", "status",
               "created_at", "ended_at", "budget_eur"])

    print("→ tâches…")
    tasks = gen_tasks(projects)
    write_csv(raw / "tasks.csv", tasks,
              ["task_id", "project_id", "title", "status", "priority",
               "estimated_hours", "actual_hours", "created_at", "completed_at"])

    print("→ assignations…")
    assignments = gen_task_assignments(tasks, users)
    write_csv(raw / "task_assignments.csv", assignments,
              ["assignment_id", "task_id", "user_id", "assigned_at"])

    print("→ commentaires…")
    comments = gen_comments(tasks, users)
    write_csv(raw / "comments.csv", comments,
              ["comment_id", "task_id", "user_id", "body", "created_at"])

    print("→ logs d'activité…")
    logs = gen_activity_logs(users, projects)
    write_json(raw / "activity_logs.json", logs)

    print("→ métriques de performance…")
    metrics = gen_performance_metrics()
    write_csv(raw / "performance_metrics.csv", metrics,
              ["date", "total_requests", "error_rate", "p50_latency_ms",
               "p95_latency_ms", "p99_latency_ms", "active_users", "incident"])

    print("→ table de référence promos…")
    promos = gen_promos_reference()
    write_csv(ref / "promos.csv", promos, ["org_id", "promo_code", "level"])

    print()
    print("✅ Génération terminée.")
    print(f"   {len(orgs):>6} organisations")
    print(f"   {len(users):>6} utilisateurices (dont doublons)")
    print(f"   {len(projects):>6} projets")
    print(f"   {len(tasks):>6} tâches")
    print(f"   {len(assignments):>6} assignations")
    print(f"   {len(comments):>6} commentaires")
    print(f"   {len(logs):>6} logs d'activité")
    print(f"   {len(metrics):>6} jours de métriques")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    parser.add_argument("--seed", type=int, default=42,
                        help="Seed pour la reproductibilité (défaut : 42)")
    parser.add_argument("--output", type=Path, default=Path("data"),
                        help="Dossier de sortie (défaut : data)")
    args = parser.parse_args()
    main(args.seed, args.output)
