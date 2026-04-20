# Analyseur de Conversations IA — Documentation (FR)

## Périmètre réel du dépôt

Le projet fournit actuellement 4 scripts utilisables :

1. `analyse_conversations_merged.py`  
   Analyse des conversations exportées (ChatGPT, LeChat, Claude), en local ou via API Mistral.

2. `extraire_titres_conversations.py`  
   Extraction des titres de conversations JSON.

3. `extract_and_collect_json.py`  
   Décompression des archives ZIP et centralisation des JSON.

4. `testapi_lechat.sh`  
   Test manuel des endpoints API Mistral/LeChat.

---

## `analyse_conversations_merged.py`

### Options CLI disponibles
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

### Capacités
- Détection automatique du format JSON.
- Déduplication des conversations (hash).
- Découpage automatique des conversations trop longues (`MAX_TOKENS=31000`).
- Analyse locale (sans API) ou API Mistral.
- Sorties CSV + TXT sujets + TXT compétences (option `--merge-comp`).

### Exemple
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

### Exemple
```bash
python3 extraire_titres_conversations.py --exec --dir ./extraction_json --merge
```

---

## `extract_and_collect_json.py`

### Rôle
- Scan du répertoire courant + sous-répertoires pour trouver les ZIP.
- Extraction dans `./extraction_zip/`.
- Copie des JSON extraits dans `./extraction_json/`.

### Modes
- `--exec` (réel)
- `--simulate` (dry-run)
- `--prerequis`, `--install`, `--help`, `--changelog`

---

## `testapi_lechat.sh`

### Fonctions principales
- Appel `POST` de `/chat/completions` (ou endpoint custom).
- Support `--create-chat`, `--payload-content`, `--simulate`.

### Limitation actuelle
- La clé API est lue depuis le fichier `.lechat` du répertoire du script.

---

## Limites et points à prévoir

- Pas de support Grok dans l'extraction/analyse principale.
- Pas de `--source_dir` (seulement `--dir`) dans `extraire_titres_conversations.py`.
- Pas d'option de redirection globale des répertoires de sortie (`--target_dir_results`, `--target_dir_log`).
