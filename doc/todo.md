# TODO / Évolutions souhaitées

## Alignement options & ergonomie
- [ ] Ajouter des options de sortie dédiées pour séparer logs/résultats (ex: `--target_dir_results`, `--target_dir_log`).
- [ ] Harmoniser les conventions d'arguments entre scripts (noms, alias, cohérence FR/EN).
- [ ] Renommer éventuellement `--dir` en `--source_dir` dans `extraire_titres_conversations.py` pour expliciter la source.

## Formats et couverture
- [ ] Étendre la détection/extraction à d'autres formats d'export (ex: Grok) si des exports cibles sont disponibles.
- [ ] Clarifier dans chaque help les formats réellement supportés et les limites connues.

## Reporting
- [ ] Ajouter un récapitulatif final “nombre de conversations par IA + total global” dans tous les modes (réel/simulate).
- [ ] Uniformiser les chemins de sortie (`./log`, `./results`) quand aucun dossier cible n'est fourni.

## Script API shell
- [ ] Faire prioriser la variable d'environnement pour la clé API et fallback sur fichier `.lechat`.
- [ ] Réduire le double appel `curl` (réponse + code HTTP) en un seul appel instrumenté.

## Qualité
- [ ] Ajouter une suite de tests minimale pour les parsers de formats.
- [ ] Ajouter une validation de syntaxe automatique (CI) pour scripts Python et shell.
