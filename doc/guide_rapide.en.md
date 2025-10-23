# Quick Guide - IA Conversation Analyzer

## Installation
```bash
./analyse_conversations_merged.py --install
```

## Basic Usage
1. **Local Analysis** (no API):
   ```bash
   ./analyse_conversations_merged.py --exec --local --aiall --fichier conversations.json
   ```
2. **Analysis with API** (e.g., LeChat):
   ```bash
   export MISTRAL_API_KEY='your_key'
   ./analyse_conversations_merged.py --exec --lechat --fichier conversations.json
   ```
3. **Merge Skills**:
   ```bash
   ./analyse_conversations_merged.py --exec --merge-comp --fichier "*.json"
   ```

---

## Advanced Usage Examples

### 1. Recursive Search
```bash
./analyse_conversations_merged.py --exec --recursive --fichier ./conversations_folder/
```

### 2. Multi-file with Consolidation
```bash
./analyse_conversations_merged.py --exec --aiall --merge-comp --fichier "*.json"
```

### 3. Analysis with Specific Model
```bash
./analyse_conversations_merged.py --exec --model mistral-large-latest --fichier conversations.json
```

### 4. Optimized Performance
```bash
./analyse_conversations_merged.py --exec --workers 10 --delay 0.2 --fichier "*.json"
```

---

## Mistral API Configuration
- **Endpoint**: `https://api.mistral.ai/v1/chat/completions`
- **Available Models**:
  - `mistral-tiny` (fast, lightweight)
  - `mistral-small` (balanced)
  - `mistral-large-latest` (most powerful, default)
- **API Key**:
  ```bash
  export MISTRAL_API_KEY="your_key"
  ```

---

## Why This Project?
To **extract and structure** skills acquired through conversations with AIs, and generate a **comprehensive technical CV** in a few commands.

---

### Useful Options
| Option          | Description                          |
|-----------------|--------------------------------------|
| `--recursive`   | Recursive folder search.             |
| `--merge-comp`  | Merge skills by domain.              |
| `--simulate`    | Simulation mode (no API cost).       |
| `--workers -w`  | Number of parallel workers.          |
| `--delay -d`    | Delay between API requests (seconds).|
