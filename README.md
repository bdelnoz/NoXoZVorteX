# NoXoZVorteX

Outil Python pour **extraire, collecter et analyser** des exports de conversations IA (ChatGPT, LeChat/Mistral, Claude), puis produire des rapports exploitables pour la capitalisation de compétences.

## Scripts principaux

- `extract_and_collect_json.py` (v1.7)
  - Parcourt le dossier courant, extrait les `.zip` dans `./extraction_zip/`, puis collecte les `.json` dans `./extraction_json/`.
  - Modes: `--exec`, `--simulate`, `--prerequis`, `--install`, `--help`, `--changelog`.
- `analyse_conversations_merged.py` (v2.7.5)
  - Analyse locale ou via API Mistral des conversations, avec auto-détection de format et rapports CSV/TXT.
  - Support: ChatGPT, LeChat, Claude.
  - Fonctions clés: déduplication, split automatique des longues conversations, analyse parallèle, consolidation des compétences.
- `extraire_titres_conversations.py` (v3.2)
  - Extrait les titres non vides depuis des JSON, avec filtres et mode fusion.
- `testapi_lechat.sh` (v2.11)
  - Script shell de test API Mistral/LeChat avec simulation et options de payload.

## Prérequis

- Python 3.8+
- Dépendances Python pour l'analyse: `requests`, `tqdm`, `tiktoken`
- (Optionnel) clé API Mistral:

```bash
export MISTRAL_API_KEY="votre_cle"
```

## Démarrage rapide

### 1) Extraire/collecter les JSON depuis des ZIP

```bash
python3 extract_and_collect_json.py --exec
```

### 2) Analyser les conversations (mode local)

```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "./extraction_json/*.json"
```

### 3) Analyser via API Mistral

```bash
python3 analyse_conversations_merged.py --exec --aiall --fichier "./extraction_json/*.json"
```

### 4) Extraire uniquement les titres

```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## Sorties générées

### `analyse_conversations_merged.py`
- `resultat_analyse_sujets_*.csv`
- `resultat_sujets_par_domaines_*.txt`
- `resultat_analyse_*_competences_par_domaines.txt` (avec `--merge-comp`)
- `log.analyse_chatgpt.v2.7.0.log`

### `extract_and_collect_json.py`
- `extraction_zip/`
- `extraction_json/`
- `log.extract_and_collect_json.py.v1.7.log`

### `extraire_titres_conversations.py`
- `titres_*.extraire_titres_conversations.v3.2.txt`
- `titres_fusionnes.extraire_titres_conversations.v3.2.txt`
- `log.extraire_titres_conversations.v3.2.log`

## Documentation détaillée

- FR: `doc/README_fr.md`
- EN: `doc/README_en.md`
- Guides rapides: `doc/guide_rapide.fr.md`, `doc/guide_rapide.en.md`
- Changelogs: `doc/changelog.fr.md`, `doc/changelog.en.md`
- État des évolutions: `doc/todo.md`
