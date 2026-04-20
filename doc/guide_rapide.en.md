# Quick Guide (EN)

## 1) Extract JSON files from ZIP exports
```bash
python3 extract_and_collect_json.py --exec
```

## 2) Local analysis (no API)
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "./extraction_json/*.json"
```

## 3) Mistral API analysis
```bash
export MISTRAL_API_KEY="your_key"
python3 analyse_conversations_merged.py --exec --aiall --fichier "./extraction_json/*.json"
```

## 4) Merge skills by domain
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --merge-comp --fichier "./extraction_json/*.json"
```

## 5) Extract titles
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## Useful reminders
- Supported analysis formats: ChatGPT, LeChat, Claude.
- Recursive scan available with `--recursive`.
- Long conversation filters:
  - `--only-split` (>31k tokens)
  - `--not-split` (≤31k tokens)
