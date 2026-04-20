# Guide Rapide (FR)

## 1) Installer les dépendances
```bash
python3 analyse_conversations_merged.py --install
```

## 2) Analyser des exports JSON (sans API)
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "*.json"
```

## 3) Analyser avec API Mistral
```bash
export MISTRAL_API_KEY="<votre_cle>"
python3 analyse_conversations_merged.py --exec --aiall --fichier "*.json"
```

## 4) Consolider les compétences
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --merge-comp --fichier "*.json"
```

## 5) Traitement récursif
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --recursive --fichier "./exports/*.json"
```

## 6) Extraction des titres
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

## 7) ZIP -> JSON centralisés
```bash
python3 extract_and_collect_json.py --exec
```

## Sorties générées
- CSV : `resultat_analyse_*.csv`
- TXT sujets : `resultat_sujets_par_domaines_*.txt`
- TXT compétences : `resultat_analyse_*_competences_par_domaines_*.txt`
- Logs : `log.*.log`
