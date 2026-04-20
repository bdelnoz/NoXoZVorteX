# Changelog (EN)

## v2.7.5 / v3.2 / v1.7 / v2.11 — Documented state

Documentation has been realigned with the actual scripts currently present in the repository.

### Confirmed feature coverage
- `analyse_conversations_merged.py`: multi-format analysis (ChatGPT, LeChat, Claude), deduplication, split handling, CSV/TXT reports, skill consolidation.
- `extract_and_collect_json.py`: ZIP extraction + JSON collection with simulation mode.
- `extraire_titres_conversations.py`: title extraction, filtering, and merge output.
- `testapi_lechat.sh`: shell-based Mistral/LeChat API testing.

### Versions observed in code
- `analyse_conversations_merged.py`: **v2.7.5**
- `config.py` (global constants): **v2.7.0**
- `extraire_titres_conversations.py`: **v3.2**
- `extract_and_collect_json.py`: **v1.7**
- `testapi_lechat.sh`: **v2.11**

### Consistency note
- Some version metadata differs across scripts (e.g., `analyse_conversations_merged.py` vs `config.py`).
- This update documents current behavior without changing code.
