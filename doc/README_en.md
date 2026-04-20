# README (English) — NoXoZVorteX

## Project goal
NoXoZVorteX provides a practical pipeline to:
1. ingest AI exports (often ZIP files),
2. extract and collect JSON files,
3. analyze conversations,
4. generate CSV/TXT reports for topics and skills.

## Current feature scope

### 1) JSON extraction/collection
Script: `extract_and_collect_json.py` (v1.7)

- Scans for `.zip` files.
- Extracts archives into `./extraction_zip/<archive_name>/`.
- Collects all discovered `.json` files into `./extraction_json/`.
- Handles filename collisions.
- Main flags:
  - `--help|-h`
  - `--exec|-exe`
  - `--simulate|-s`
  - `--prerequis|-pr`
  - `--install|-i`
  - `--changelog|-ch`

### 2) Multi-format conversation analysis
Script: `analyse_conversations_merged.py` (v2.7.5)

- Supported formats: **ChatGPT**, **LeChat/Mistral**, **Claude**.
- Local analysis (`--local`) or Mistral API mode.
- Auto format detection (`--aiall` / `--auto`).
- Multi-file and recursive discovery (`--recursive`).
- Duplicate detection with multi-criteria hash.
- Automatic split for oversized conversations (`MAX_TOKENS = 31,000`).
- Parallel execution (`--workers`) and API throttling (`--delay`).
- Reports:
  - CSV raw results
  - TXT topics grouped by domains
  - TXT consolidated skills (`--merge-comp`)

Available CLI options:
- `--help`, `--exec`, `--install`, `--prerequis`, `--changelog`
- `--chatgpt`, `--lechat`, `--claude`, `--aiall|--auto`
- `--local`, `--simulate`, `--avec-contexte`
- `--only-split`, `--not-split`, `--cnbr`
- `--fichier|-F`, `--recursive`
- `--model|-m`, `--workers|-w`, `--delay|-d`
- `--remove`, `--delete`, `--undelete`

### 3) Title extraction utility
Script: `extraire_titres_conversations.py` (v3.2)

- Extracts non-empty titles from JSON conversation exports.
- Filename filter (`--filter`) and title exclusion (`--exclude`).
- Merge mode (`--merge`) for a single TXT output.
- Input from directory (`--dir`) or explicit file list (`--files`).

### 4) Mistral/LeChat API test script
Script: `testapi_lechat.sh` (v2.11)

- Tests Mistral endpoint (`/chat/completions` by default).
- Simulation mode (`--simulate true|false`).
- Custom user message (`--payload-content`).
- `--create-chat` option handled by script logic.

## Requirements

- Python 3.8+
- Analysis dependencies: `requests`, `tqdm`, `tiktoken`
- API mode requires:

```bash
export MISTRAL_API_KEY="your_key"
```

## Example flows

### Recommended pipeline
```bash
python3 extract_and_collect_json.py --exec
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "./extraction_json/*.json"
```

### API analysis + consolidated skills
```bash
python3 analyse_conversations_merged.py --exec --aiall --merge-comp --fichier "./extraction_json/*.json"
```

### Merged title extraction
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## Output summary
- Analysis outputs: `resultat_analyse_sujets_*.csv`, `resultat_sujets_par_domaines_*.txt`
- Skills outputs: `resultat_analyse_*_competences_par_domaines.txt`
- Logs: `log.*.log`
