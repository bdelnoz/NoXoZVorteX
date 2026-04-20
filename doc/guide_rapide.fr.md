# Guide Rapide (FR)

## 1) Extraire les JSON depuis des ZIP
```bash
python3 extract_and_collect_json.py --exec
```

## 2) Analyse locale (sans API)
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "./extraction_json/*.json"
```

## 3) Analyse API Mistral
```bash
export MISTRAL_API_KEY="votre_cle"
python3 analyse_conversations_merged.py --exec --aiall --fichier "./extraction_json/*.json"
```

## 4) Fusion des compétences
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --merge-comp --fichier "./extraction_json/*.json"
```

## 5) Extraction des titres
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## Rappels utiles
- Formats gérés par l'analyse: ChatGPT, LeChat, Claude.
- Recherche récursive possible: ajouter `--recursive`.
- Filtrage des conversations longues:
  - `--only-split` (>31k tokens)
  - `--not-split` (≤31k tokens)
