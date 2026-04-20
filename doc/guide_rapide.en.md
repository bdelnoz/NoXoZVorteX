# Quick Guide (EN)

## 1) Install dependencies
```bash
python3 analyse_conversations_merged.py --install
```

## 2) Analyze JSON exports (local mode)
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "*.json"
```

## 3) Analyze with Mistral API
```bash
export MISTRAL_API_KEY="<your_key>"
python3 analyse_conversations_merged.py --exec --aiall --fichier "*.json"
```

## 4) Merge skills by domain
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --merge-comp --fichier "*.json"
```

## 5) Recursive processing
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --recursive --fichier "./exports/*.json"
```

## 6) Extract titles
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## 7) ZIP -> consolidated JSON
```bash
python3 extract_and_collect_json.py --exec
```

## Generated outputs
- CSV: `resultat_analyse_*.csv`
- Subjects TXT: `resultat_sujets_par_domaines_*.txt`
- Skills TXT: `resultat_analyse_*_competences_par_domaines_*.txt`
- Logs: `log.*.log`
