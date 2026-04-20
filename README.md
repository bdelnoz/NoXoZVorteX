# NoXoZVorteX

Outil open-source Python pour **extraire, centraliser et analyser** des historiques de conversations IA exportées (ChatGPT, LeChat/Mistral, Claude).

> ⚠️ Ce dépôt est en **alpha** et contient des écarts de versions entre modules (ex: script principal v2.7.5, config/reporting v2.7.0).

## Ce que le dépôt contient réellement

### 1) Analyse de conversations multi-formats
Script principal : `analyse_conversations_merged.py`

Fonctionnalités disponibles dans l'état actuel :
- Détection de format : ChatGPT / LeChat / Claude (`--aiall`, `--auto`).
- Extraction des messages selon le format.
- Détection de doublons par hash multi-critères.
- Découpage des conversations longues (> `MAX_TOKENS`, défaut 31 000).
- Analyse **locale** (sans API) ou via API Mistral.
- Exécution parallèle (`ThreadPoolExecutor`, option `--workers`).
- Génération de rapports CSV + TXT (sujets, et compétences consolidées via `--merge-comp`).
- Recherche récursive de JSON (`--recursive`).

### 2) Extraction de titres de conversations
Script : `extraire_titres_conversations.py`
- Extrait les titres non vides depuis des fichiers JSON.
- Supporte : simulation, filtre de fichiers, exclusion de texte, fusion des titres, liste de fichiers explicite.

### 3) Extraction ZIP + collecte des JSON
Script : `extract_and_collect_json.py`
- Décompresse les `.zip` trouvés.
- Collecte ensuite les `.json` dans un dossier de consolidation.
- Gère collisions de noms, logs et mode simulation.

### 4) Test API LeChat/Mistral
Script shell : `testapi_lechat.sh`
- Envoi de requêtes vers `https://api.mistral.ai/v1/chat/completions`.
- Mode simulation, endpoint custom, payload custom.

---

## Prérequis

- Python 3.8+
- Dépendances Python utilisées par le projet : `requests`, `tqdm`, `tiktoken`
- Optionnel : variable d'environnement `MISTRAL_API_KEY` pour le mode API

Installation guidée (script principal) :
```bash
python3 analyse_conversations_merged.py --install
```

---

## Utilisation rapide

### A. Analyse locale multi-formats (sans API)
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --fichier "*.json"
```

### B. Analyse API Mistral
```bash
export MISTRAL_API_KEY="<votre_cle>"
python3 analyse_conversations_merged.py --exec --aiall --fichier "*.json"
```

### C. Fusion des compétences détectées
```bash
python3 analyse_conversations_merged.py --exec --local --aiall --merge-comp --fichier "*.json"
```

### D. Extraction de titres
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

### E. ZIP -> JSON consolidés
```bash
python3 extract_and_collect_json.py --exec
```

---

## Fichiers de sortie (par défaut)

Le dépôt écrit actuellement les sorties dans le répertoire courant / répertoire du script selon les scripts :
- `resultat_analyse_*.csv`
- `resultat_sujets_par_domaines_*.txt`
- `resultat_analyse_*_competences_par_domaines_*.txt`
- `log.*.log`

---

## Limites connues (état actuel du code)

- `analyse_conversations_merged.py --help` peut échouer sans dépendances installées (import `requests` au chargement).
- Le script principal gère ChatGPT/LeChat/Claude ; **Grok n'est pas implémenté**.
- `extraire_titres_conversations.py` utilise encore `--dir` (pas `--source_dir`).
- `testapi_lechat.sh` lit la clé dans `.lechat` (pas via `MISTRAL_API_KEY` en priorité).
- Pas de `--target_dir_results` / `--target_dir_log` dans le script principal actuellement.

---

## Licence

Voir `LICENSE`.
