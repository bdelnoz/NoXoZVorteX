# Complete Changelog - IA Conversation Analyzer

## Overview
- **Project**: IA conversation analysis system (ChatGPT, LeChat, Claude).
- **Author**: Bruno DELNOZ - bruno.delnoz@protonmail.com
- **License**: Open Source
- **Goal**: Extract skills and subjects to build a technical CV.

---

## Version History

### Version 2.7.2 (2025-10-20)
- **Duplicate Detection**: Multi-criteria hash (title, ID, timestamp, content).
- **Detailed Report** of found duplicates.
- **Fixes**: Import of `hashlib` and `Set`.

### Version 2.7.1 (2025-10-20)
- **Recursive Search**: Support for directories (`./folder/**/*.json`) and wildcards.
- **Fixes**: `glob.glob()` and patterns without `**`.

### Version 2.7.0 (2025-10-19)
- **Refactoring**: Modular architecture (7 modules: `config.py`, `utils.py`, `extractors.py`, etc.).
- **New Features**:
  - Multi-format support (ChatGPT, LeChat, Claude).
  - Auto-detection (`--aiall`).
  - Local analysis (`--local`).
  - Simulation mode (`--simulate`).
  - Advanced filters (`--only-split`, `--not-split`).
  - Detailed CSV/TXT reports.

### Version 2.6.0 (2025-01-15)
- Initial Claude AI support.
- Improved message extraction.

### Version 2.5.0 (2024-12-10)
- LeChat (Mistral AI) support.
- Automatic format detection.

### Version 2.4.0 (2024-11-05)
- Automatic splitting of long conversations.
- Configurable `MAX_TOKENS`.

### Version 2.3.0 (2024-10-20)
- Parallel analysis with `ThreadPoolExecutor`.
- Progress bar (`tqdm`).

### Version 2.2.0 (2024-09-15)
- Automatic categorization by domain.
- Skill extraction.

### Version 2.1.0 (2024-08-10)
- Mistral API integration.
- AI semantic analysis.

### Version 2.0.0 (2024-07-01)
- Architecture overhaul.
- Virtual environment support.

### Version 1.x (2023-2024)
- Initial versions (ChatGPT only).

---

## Secondary Modules

### config.py
- **Version**: 2.7.0
- **Content**: Global constants, Mistral API management.

### utils.py
- **Version**: 2.7.0
- **Functions**: `ecrire_log()`, `generer_nom_sortie()`, `compter_tokens()`.

### extractors.py
- **Version**: 2.7.0
- **Functions**: Automatic format detection, multi-format extraction.

### api_analyzer.py
- **Version**: 2.7.0
- **Functions**: Mistral API calls, conversation splitting.

### reporters.py
- **Version**: 2.7.0
- **Functions**: CSV/TXT report generation.

### install.py
- **Version**: 2.7.0
- **Functions**: Dependency check and installation.

---

## CLI Arguments
```bash
--exec          # Run analysis
--help          # Display help
--install       # Install dependencies
--chatgpt       # Force ChatGPT format
--lechat        # Force LeChat format
--claude        # Force Claude format
--aiall         # Auto-detection (recommended)
--local         # Local analysis (no API)
--simulate      # Simulation mode
--recursive     # Recursive search
--merge-comp    # Merge skills
--workers -w N  # Parallel workers
--delay -d N    # Delay between API requests
```

---

## Usage Examples
1. **Simple Analysis (ChatGPT)**:
   ```bash
   ./analyse_conversations_merged.py --exec --chatgpt --fichier conversations.json
   ```
2. **Multi-format Auto-detection**:
   ```bash
   ./analyse_conversations_merged.py --exec --aiall --fichier "*.json"
   ```
3. **Recursive Search**:
   ```bash
   ./analyse_conversations_merged.py --exec --recursive --fichier ./exports/
   ```

---

## Roadmap
- **v3.0.0**: Web interface, SQLite database, PDF/Word export.
- **v2.8.0**: Result caching, diff mode, structured JSON export.

---

## Known Bugs
- Approximate token counting.
- Fixed rate limiting (not adaptive).

---

## Mistral API Configuration
- **Endpoint**: `https://api.mistral.ai/v1/chat/completions`
- **Models**: `mistral-large-latest` (default).
- **API Key**: `export MISTRAL_API_KEY="your_key"`

---

## Acknowledgements
- Mistral AI, OpenAI, Anthropic, Python community.
