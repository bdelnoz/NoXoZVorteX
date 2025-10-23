# Guide Rapide - Analyseur de Conversations IA

## Installation
```bash
./analyse_conversations_merged.py --install
```

## Utilisation de Base
1. **Analyse locale** (sans API) :
   ```bash
   ./analyse_conversations_merged.py --exec --local --aiall --fichier conversations.json
   ```
2. **Analyse avec API** (ex: LeChat) :
   ```bash
   export MISTRAL_API_KEY='votre_clé'
   ./analyse_conversations_merged.py --exec --lechat --fichier conversations.json
   ```
3. **Fusion des compétences** :
   ```bash
   ./analyse_conversations_merged.py --exec --merge-comp --fichier "*.json"
   ```

---

## Exemples d'Utilisation Avancés

### 1. Recherche récursive
```bash
./analyse_conversations_merged.py --exec --recursive --fichier ./dossier_conversations/
```

### 2. Multi-fichiers avec consolidation
```bash
./analyse_conversations_merged.py --exec --aiall --merge-comp --fichier "*.json"
```

### 3. Analyse avec modèle spécifique
```bash
./analyse_conversations_merged.py --exec --model mistral-large-latest --fichier conversations.json
```

### 4. Performance optimisée
```bash
./analyse_conversations_merged.py --exec --workers 10 --delay 0.2 --fichier "*.json"
```

---

## Configuration API Mistral
- **Endpoint** : `https://api.mistral.ai/v1/chat/completions`
- **Modèles disponibles** :
  - `mistral-tiny` (rapide, léger)
  - `mistral-small` (équilibré)
  - `mistral-large-latest` (le plus puissant, par défaut)
- **Clé API** :
  ```bash
  export MISTRAL_API_KEY="votre_clé"
  ```

---

## Pourquoi ce projet ?
Pour **extraire et structurer** les compétences acquises via des conversations avec des IA, et générer un **CV technique complet** en quelques commandes.

---

### Options Utiles
| Option          | Description                          |
|-----------------|--------------------------------------|
| `--recursive`   | Recherche récursive dans les dossiers.|
| `--merge-comp`  | Fusionne les compétences par domaine. |
| `--simulate`    | Mode simulation (sans coût API).     |
| `--workers -w`  | Nombre de workers parallèles.        |
| `--delay -d`    | Délai entre requêtes API (secondes). |
