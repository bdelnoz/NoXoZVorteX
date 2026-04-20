# README (Français) — NoXoZVorteX

## Objectif du projet
NoXoZVorteX sert à industrialiser un flux simple:
1. récupérer des exports IA (souvent ZIP),
2. extraire/collecter les JSON,
3. analyser les conversations,
4. produire des rapports CSV/TXT orientés sujets et compétences.

## Périmètre fonctionnel actuel

### 1) Extraction/collecte des JSON
Script: `extract_and_collect_json.py` (v1.7)

- Recherche des fichiers `.zip`.
- Extraction dans `./extraction_zip/<nom_archive>/`.
- Collecte de tous les `.json` vers `./extraction_json/`.
- Gestion des collisions de noms.
- Commandes principales:
  - `--help|-h`
  - `--exec|-exe`
  - `--simulate|-s`
  - `--prerequis|-pr`
  - `--install|-i`
  - `--changelog|-ch`

### 2) Analyse multi-format des conversations
Script: `analyse_conversations_merged.py` (v2.7.5)

- Formats gérés: **ChatGPT**, **LeChat/Mistral**, **Claude**.
- Analyse locale (`--local`) ou via API Mistral.
- Auto-détection des formats (`--aiall` / `--auto`).
- Analyse multi-fichiers et recherche récursive (`--recursive`).
- Déduplication par hash multi-critères.
- Découpage automatique des conversations dépassant `MAX_TOKENS` (31 000).
- Traitement parallèle (`--workers`) + délai API (`--delay`).
- Rapports:
  - CSV résultats bruts
  - TXT sujets par domaines
  - TXT compétences consolidées (option `--merge-comp`)

Options CLI disponibles:
- `--help`, `--exec`, `--install`, `--prerequis`, `--changelog`
- `--chatgpt`, `--lechat`, `--claude`, `--aiall|--auto`
- `--local`, `--simulate`, `--avec-contexte`
- `--only-split`, `--not-split`, `--cnbr`
- `--fichier|-F`, `--recursive`
- `--model|-m`, `--workers|-w`, `--delay|-d`
- `--remove`, `--delete`, `--undelete`

### 3) Extraction de titres
Script: `extraire_titres_conversations.py` (v3.2)

- Extraction de titres non vides dans des exports JSON.
- Filtre par nom de fichier (`--filter`) et exclusion par chaîne (`--exclude`).
- Mode fusion (`--merge`) pour un seul TXT global.
- Traitement par dossier (`--dir`) ou liste explicite (`--files`).

### 4) Test API Mistral/LeChat
Script: `testapi_lechat.sh` (v2.11)

- Test endpoint Mistral (`/chat/completions` par défaut).
- Mode simulation (`--simulate true|false`).
- Personnalisation message (`--payload-content`).
- Option `--create-chat` (nom de chat) côté script.

## Prérequis

- Python 3.8+
- Dépendances analyse: `requests`, `tqdm`, `tiktoken`
- En mode API:

```bash
export MISTRAL_API_KEY="votre_cle"
```

## Exemples

### Pipeline recommandé
```bash
python3 extract_and_collect_json.py --exec
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "./extraction_json/*.json"
```

### Analyse API + fusion des compétences
```bash
python3 analyse_conversations_merged.py --exec --aiall --merge-comp --fichier "./extraction_json/*.json"
```

### Extraction des titres fusionnée
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## Fichiers générés (résumé)
- Analyse: `resultat_analyse_sujets_*.csv`, `resultat_sujets_par_domaines_*.txt`
- Compétences: `resultat_analyse_*_competences_par_domaines.txt`
- Logs: `log.*.log`
