# Changelog (FR)

## v2.7.5 / v3.2 / v1.7 / v2.11 — État documenté

Cette documentation a été réalignée sur l'état réel des scripts présents dans le dépôt.

### Couverture fonctionnelle confirmée
- `analyse_conversations_merged.py` : analyse multi-format (ChatGPT, LeChat, Claude), déduplication, split, rapports CSV/TXT, consolidation des compétences.
- `extract_and_collect_json.py` : extraction ZIP + collecte JSON avec mode simulation.
- `extraire_titres_conversations.py` : extraction de titres, filtrage et fusion.
- `testapi_lechat.sh` : test API Mistral/LeChat en shell.

### Versions constatées dans le code
- `analyse_conversations_merged.py`: **v2.7.5**
- `config.py` (constantes globales): **v2.7.0**
- `extraire_titres_conversations.py`: **v3.2**
- `extract_and_collect_json.py`: **v1.7**
- `testapi_lechat.sh`: **v2.11**

### Note de cohérence
- Certaines métadonnées de version diffèrent entre scripts (ex: `analyse_conversations_merged.py` vs `config.py`).
- La documentation décrit les fonctionnalités disponibles sans modifier le code.
