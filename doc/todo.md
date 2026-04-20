# TODO (aligné au code actuel)

## Priorité haute
- [ ] Ajouter `--target_dir_results` et `--target_dir_log` dans `analyse_conversations_merged.py`.
- [ ] Mettre à jour `testapi_lechat.sh` pour utiliser `MISTRAL_API_KEY` en priorité, puis fallback `.lechat`.
- [ ] Renommer `--dir` en `--source_dir` (avec compatibilité rétroactive) dans `extraire_titres_conversations.py`.
- [ ] Ajouter détection/prise en charge Grok (en plus de ChatGPT/LeChat/Claude) dans l'extraction et l'analyse.
- [ ] Ajouter un récapitulatif final du nombre de conversations par IA + total global en fin d'exécution.

## Priorité moyenne
- [ ] Harmoniser les versions internes (v2.7.5 vs v2.7.0).
- [ ] Éviter l'échec du `--help` sans dépendances installées (imports différés).
- [ ] Unifier la documentation FR/EN par source unique.

## Priorité basse
- [ ] Ajouter un dossier `examples/` avec jeux JSON minimaux.
- [ ] Ajouter tests automatisés CLI (smoke tests).
