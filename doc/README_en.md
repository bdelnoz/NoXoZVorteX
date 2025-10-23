# IA Conversation Analyzer - README

## Description
Python script to extract and analyze technical subjects and skills discussed in conversations with AIs (ChatGPT, Claude, LeChat).
**Goal**: Capitalize on knowledge gained from 900+ conversations to build a detailed technical CV.

---

## Installation

### Prerequisites
- Python 3.8+
- Execution rights on scripts

### Commands
```bash
# Install dependencies (automatic venv)
./analyse_conversations_merged.py --install
```

---

## Options (exact copy of `--help`)

| Option               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `--help`             | Display this help                                                           |
| `--exec`             | Run analysis                                                                |
| `--install`          | Install dependencies                                                        |
| `--lechat`           | Export format for LeChat (Mistral)                                          |
| `--chatgpt`          | Export format for ChatGPT                                                   |
| `--claude`           | Export format for Claude                                                    |
| `--aiall`, `--auto`  | Auto-detect ALL formats                                                     |
| `--local`            | Local analysis WITHOUT API calls (free)                                     |
| `--avec-contexte`    | Add descriptions/examples to subjects                                       |
| `--merge-comp`       | Display ALL skills by domain                                                |
| `--simulate`         | API simulation mode (test without credits)                                  |
| `--only-split`       | Analyze ONLY conversations > 31000 tokens                                   |
| `--not-split`        | Analyze ONLY conversations ≤ 31000 tokens                                   |
| `--cnbr N`           | Analyze only conversation N                                                 |
| `--fichier`, `-F`    | JSON file(s) (supports `*.json` for multiple)                              |
| `--recursive`        | Recursive search in subfolders                                              |
| `--model`, `-m`      | Pixtral model (default: `pixtral-large-latest`)                             |
| `--workers`, `-w N`  | Parallel workers (default: 5)                                              |
| `--delay`, `-d N`    | Delay between API requests (default: 0.5s)                                 |
| `--remove`           | Delete created element (CSV/log)                                            |
| `--dir`, `-d STR`    | JSON directory (default: current)                                          |
| `--files`            | List of JSON files to process                                               |
| `--filter STR`       | Filter to select files                                                      |
| `--changelog`        | Display full changelog                                                      |
| `--exclude`, `-E`    | String to exclude from titles                                               |

---

## Execution Examples

### 1. Installation
```bash
./analyse_conversations_merged.py --install
```

### 2. Local Analysis (all formats)
```bash
./analyse_conversations_merged.py --local --aiall
```

### 3. Analysis with API (LeChat)
```bash
export MISTRAL_API_KEY='your_key'
./analyse_conversations_merged.py --lechat
```

### 4. Merge Skills by Domain
```bash
./analyse_conversations_merged.py --merge-comp
```

### 5. Recursive Search
```bash
./analyse_conversations_merged.py --recursive
```

---

## Outputs
- `resultat_analyse_*.csv`: Structured results (subjects, skills, tokens).
- `log.analyse_*.log`: Detailed analysis logs.
- `.backup.*`: Automatic backups.

---

### Output Example (extract from `resultat_analyse_sujets_multi_local_20251021_040516.csv`)
```csv
subject,skills,tokens,date
Cybersecurity,Linux Firewall,IPtables,2025-10-20
Scripting,Advanced Python,Bash,2025-10-21
Artificial Intelligence,Tokenization,Language Models,2025-10-20
```

---

## Initial Goal
This script was designed to extract and structure **927+ conversations** with AIs, in order to generate a **comprehensive technical CV** (30-40 pages) highlighting skills acquired through interaction with ChatGPT, Claude, LeChat, etc.
