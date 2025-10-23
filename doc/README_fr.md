# Analyseur de Conversations IA - README

## Description
Script Python pour extraire et analyser les sujets et compétences techniques abordés dans des conversations avec des IA (ChatGPT, Claude, LeChat).
**Objectif** : Capitaliser les connaissances acquises via 900+ conversations pour alimenter un CV technique détaillé.

---

## Installation

### Prérequis
- Python 3.8+
- Droits d'exécution sur les scripts

### Commandes
```bash
# Installation des dépendances (venv automatique)
./analyse_conversations_merged.py --install
```

---

## Options (copie exacte du `--help`)

| Option               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `--help`             | Affiche cette aide                                                          |
| `--exec`             | Lance l'analyse                                                            |
| `--install`          | Installe les dépendances                                                   |
| `--lechat`           | Format d'export LeChat (Mistral)                                           |
| `--chatgpt`          | Format d'export ChatGPT                                                    |
| `--claude`           | Format d'export Claude                                                     |
| `--aiall`, `--auto`  | Auto-détection de TOUS les formats                                         |
| `--local`            | Analyse locale SANS appel API (gratuit)                                    |
| `--avec-contexte`    | Ajoute descriptions/exemples aux sujets                                    |
| `--merge-comp`       | Affiche TOUTES les compétences par domaines                                |
| `--simulate`         | Mode simulation API (test sans crédits)                                    |
| `--only-split`       | Analyse UNIQUEMENT conversations > 31000 tokens                           |
| `--not-split`        | Analyse UNIQUEMENT conversations ≤ 31000 tokens                           |
| `--cnbr N`           | Analyse uniquement la conversation N                                       |
| `--fichier`, `-F`    | Fichier(s) JSON (supporte `*.json` pour plusieurs)                        |
| `--recursive`        | Recherche récursive dans sous-dossiers                                     |
| `--model`, `-m`      | Modèle Pixtral (défaut: `pixtral-large-latest`)                            |
| `--workers`, `-w N`  | Workers parallèles (défaut: 5)                                             |
| `--delay`, `-d N`    | Délai entre requêtes API (défaut: 0.5s)                                    |
| `--remove`           | Supprime élément créé (CSV/log)                                            |
| `--dir`, `-d STR`    | Répertoire des JSON (défaut: courant)                                      |
| `--files`            | Liste de fichiers JSON à traiter                                           |
| `--filter STR`       | Filtre pour sélectionner les fichiers                                      |
| `--changelog`        | Afficher changelog complet                                                 |
| `--exclude`, `-E`    | Chaîne à exclure des titres                                                |

---

## Exemples d'Exécution

### 1. Installation
```bash
./analyse_conversations_merged.py --install
```

### 2. Analyse locale (tous formats)
```bash
./analyse_conversations_merged.py --local --aiall
```

### 3. Analyse avec API (LeChat)
```bash
export MISTRAL_API_KEY='votre_clé'
./analyse_conversations_merged.py --lechat
```

### 4. Fusion des compétences par domaines
```bash
./analyse_conversations_merged.py --merge-comp
```

### 5. Recherche récursive
```bash
./analyse_conversations_merged.py --recursive
```

---

## Sorties
- `resultat_analyse_*.csv` : Résultats structurés (sujets, compétences, tokens).
- `log.analyse_*.log` : Logs détaillés de l'analyse.
- `.backup.*` : Backups automatiques.

---

### Exemple de Sortie (extrait de `resultat_analyse_sujets_multi_local_20251021_040516.csv`)
```csv
sujet,compétences,tokens,date
Cybersécurité,Firewall Linux,IPtables,2025-10-20
Scripting,Python avancé,Bash,2025-10-21
Intelligence Artificielle,Tokenisation,Modèles de langage,2025-10-20
```

---

## Objectif Initial
Ce script a été conçu pour extraire et structurer les **927+ conversations** avec des IA, afin de générer un **CV technique complet** (30-40 pages) mettant en avant les compétences acquises via l'interaction avec ChatGPT, Claude, LeChat, etc.
