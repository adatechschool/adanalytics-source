# Enjeux RGPD du dataset

> Cette page t'aide à identifier les enjeux réglementaires de **ce dataset précis**. Le brief te demande de produire une synthèse des enjeux RGPD — utilise ce document comme point de départ, pas comme rendu fini.

## Ce que dit le RGPD en deux phrases

Le RGPD encadre le traitement des **données à caractère personnel** — toute information permettant d'identifier directement ou indirectement une personne physique. Tu dois pouvoir justifier que tu collectes, conserves et exploites ces données de manière minimale, sécurisée, finalisée et transparente.

## Les données personnelles présentes dans ton dataset

Liste à compléter et nuancer selon ton analyse :

| Donnée | Fichier | Type | Sensibilité |
|---|---|---|---|
| `first_name`, `last_name` | `users.csv` | Identification directe | Modérée |
| `email` | `users.csv` | Identification directe | Modérée |
| `age` | `users.csv` | Information personnelle | Faible isolée, modérée croisée |
| `ip_address` | `activity_logs.json` | Identifiant indirect | Modérée (jurisprudence CJUE 2016) |
| `user_agent` | `activity_logs.json` | Quasi-identifiant | Faible |
| Numéros de téléphone | `comments.csv` (dans le texte) | Identification directe | Modérée |
| Emails dans les commentaires | `comments.csv` (dans le texte) | Identification directe | Modérée |

⚠️ **Le simple fait que des données soient synthétiques ne change pas la démarche**. Pour le projet, tu raisonnes *comme si* ces données étaient réelles. C'est l'exercice attendu.

## Les principes du RGPD à mobiliser dans ton analyse

### 1. Minimisation
Tu ne charges et ne conserves que ce qui sert ta problématique. Si tu analyses la performance des tâches, tu n'as pas besoin des emails ni des adresses IP. **Justifie dans ton notebook ce que tu ne charges pas.**

### 2. Finalité
Le traitement doit avoir une finalité explicite. Dans le brief, ta finalité c'est l'analyse pédagogique d'un produit numérique. Ce n'est pas le marketing direct, ce n'est pas la surveillance individuelle. Cela limite ce que tu peux faire.

### 3. Anonymisation vs pseudonymisation
- **Pseudonymisation** : remplacer les identifiants directs par des codes (mais le mapping existe encore). Niveau de protection moyen.
- **Anonymisation** : impossible de remonter à la personne, même par croisement. Niveau de protection fort.

Le dataset utilise des prénoms/noms réels (synthétiques) et des `user_id` qui ne sont pas un vrai pseudonyme (lien direct dans la même table). Une vraie démarche d'analyse pseudonymiserait avant import dans le notebook.

### 4. Données dans les zones de texte libre
Les `comments.body` contiennent ponctuellement des emails et numéros de téléphone. C'est un classique en analyse de données : les utilisateurices copient-collent des infos perso dans des champs libres. **À traiter dans la phase de nettoyage** (regex de masquage par exemple).

## Pistes pour ta synthèse RGPD

Ce qu'on attend dans ton livrable :

1. **Inventaire** des données personnelles présentes
2. **Analyse de finalité** : pourquoi tu en as besoin, ou pas
3. **Mesures de protection** appliquées dans ton pipeline (pseudonymisation, masquage, agrégation)
4. **Données que tu choisis volontairement d'écarter** et pourquoi
5. **Limites** : ce que ton dataset ne permet pas (durée de conservation non documentée, base légale du recueil non documentée, etc.)

## Pour aller plus loin

- [RGPD — Texte de référence (CNIL)](https://www.cnil.fr/fr/reglement-europeen-protection-donnees)
- [Données personnelles : la définition de la CNIL](https://www.cnil.fr/fr/definition/donnee-personnelle)
- [Pseudonymisation et anonymisation — CNIL](https://www.cnil.fr/fr/lanonymisation-des-donnees-personnelles)

## Le piège classique

Ne traite pas le RGPD comme une **case à cocher en fin de notebook**. Une bonne analyste data intègre la réflexion RGPD **dès la phase d'exploration** : "ai-je besoin de cette colonne pour répondre à ma question ? si oui, à quel niveau d'agrégation ?". C'est cette posture qui est évaluée.
