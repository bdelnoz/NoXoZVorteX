# Changelog (EN)

## 2026-04-20 — Full documentation refresh

Docs were aligned with the **actual** repository behavior (no code changes):
- Active scripts inventory:
  - `analyse_conversations_merged.py`
  - `extraire_titres_conversations.py`
  - `extract_and_collect_json.py`
  - `testapi_lechat.sh`
- CLI options updated to match current argument parsers.
- Implemented features vs missing features clearly separated.
- Known limitations documented:
  - no Grok support,
  - no `--source_dir` in title extractor,
  - no `--target_dir_results` / `--target_dir_log`,
  - `.lechat` file is used for API key in `testapi_lechat.sh`.

---

## Previous history

Older 2.x entries were partly inconsistent with current code state.  
They were replaced with a documentation-first changelog focused on present behavior.
