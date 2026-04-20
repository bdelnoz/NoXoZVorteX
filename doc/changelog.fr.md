# Changelog (FR)

## 2026-04-20 — Mise à jour documentaire complète

Documentation alignée avec l'état **réel** du dépôt (sans modification du code) :
- Inventaire des scripts actifs :
  - `analyse_conversations_merged.py`
  - `extraire_titres_conversations.py`
  - `extract_and_collect_json.py`
  - `testapi_lechat.sh`
- Révision des options CLI documentées selon les parseurs actuels.
- Clarification des fonctionnalités déjà implémentées vs non implémentées.
- Ajout des limites connues :
  - pas de support Grok,
  - pas de `--source_dir` dans l'extracteur de titres,
  - pas de `--target_dir_results` / `--target_dir_log`,
  - clé API `.lechat` utilisée par `testapi_lechat.sh`.

---

## Historique antérieur

Les anciennes entrées versionnelles (2.x) étaient partielles et parfois non synchronisées avec le code courant.  
Elles ont été remplacées par une version documentaire centrée sur l'état présent du dépôt.
