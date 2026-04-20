# IA Conversation Analyzer — Documentation (EN)

## Current repository scope

The repository currently ships 4 usable scripts:

1. `analyse_conversations_merged.py`  
   Multi-source conversation analysis (ChatGPT, LeChat, Claude), local or via Mistral API.

2. `extraire_titres_conversations.py`  
   Extracts non-empty conversation titles from JSON files.

3. `extract_and_collect_json.py`  
   Extracts ZIP files and consolidates JSON files.

4. `testapi_lechat.sh`  
   Manual API test script for Mistral/LeChat endpoints.

---

## `analyse_conversations_merged.py`

### Available CLI options
- `--exec`
- `--install`
- `--help`
- `--chatgpt` / `--lechat` / `--claude` / `--aiall` (`--auto`)
- `--local`
- `--simulate`
- `--avec-contexte`
- `--merge-comp`
- `--only-split` / `--not-split`
- `--cnbr N`
- `--fichier -F <patterns...>`
- `--recursive`
- `--model -m <model>`
- `--workers -w <n>`
- `--delay -d <sec>`
- `--remove` / `--delete` / `--undelete`
- `--prerequis`
- `--changelog`

### Capabilities
- Automatic format detection.
- Duplicate conversation detection using hash signatures.
- Conversation split when token count exceeds `MAX_TOKENS=31000`.
- Local analysis (no API) or Mistral API analysis.
- CSV + TXT reports (subjects, and merged skills with `--merge-comp`).

### Example
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "*.json"
```

---

## `extraire_titres_conversations.py`

### Options
- `--exec`
- `--help`
- `--prerequis`
- `--install`
- `--simulate`
- `--changelog`
- `--filter`
- `--merge`
- `--exclude`
- `--dir`
- `--files`

---

## `extract_and_collect_json.py`

### What it does
- Scans current directory and subdirectories for ZIP files.
- Extracts archives into `./extraction_zip/`.
- Collects extracted JSON files into `./extraction_json/`.

---

## `testapi_lechat.sh`

### Core behavior
- Sends `POST` requests to `/chat/completions` (or custom endpoint).
- Supports `--create-chat`, `--payload-content`, and simulation mode.

### Current limitation
- API key is loaded from a local `.lechat` file in script directory.

---

## Known gaps (current state)

- No Grok format support in analyzer/extractor.
- No `--source_dir` switch yet (only `--dir`) in title extractor.
- No global output directory switches such as `--target_dir_results` / `--target_dir_log`.
