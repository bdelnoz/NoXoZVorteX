# Changelog Complet - Analyseur de Conversations IA

## Vue d'ensemble
- **Projet** : Système d'analyse de conversations IA (ChatGPT, LeChat, Claude).
- **Auteur** : Bruno DELNOZ - bruno.delnoz@protonmail.com
- **Licence** : Open Source
- **Objectif** : Extraire compétences et sujets pour alimenter un CV technique.

---

## Historique des Versions

### Version 2.7.2 (2025-10-20)
- **Détection de doublons** : Hash multi-critères (titre, ID, timestamp, contenu).
- **Rapport détaillé** des doublons trouvés.
- **Corrections** : Import de `hashlib` et `Set`.

### Version 2.7.1 (2025-10-20)
- **Recherche récursive** : Support des répertoires (`./dossier/**/*.json`) et wildcards.
- **Corrections** : `glob.glob()` et patterns sans `**`.

### Version 2.7.0 (2025-10-19)
- **Refactorisation** : Architecture modulaire (7 modules : `config.py`, `utils.py`, `extractors.py`, etc.).
- **Nouveautés** :
  - Support multi-formats (ChatGPT, LeChat, Claude).
  - Auto-détection (`--aiall`).
  - Analyse locale (`--local`).
  - Mode simulation (`--simulate`).
  - Filtres avancés (`--only-split`, `--not-split`).
  - Rapports CSV/TXT détaillés.

### Version 2.6.0 (2025-01-15)
- Support initial de Claude AI.
- Amélioration de l'extraction des messages.

### Version 2.5.0 (2024-12-10)
- Support de LeChat (Mistral AI).
- Détection automatique du format.

### Version 2.4.0 (2024-11-05)
- Split automatique des conversations longues.
- `MAX_TOKENS` configurable.

### Version 2.3.0 (2024-10-20)
- Analyse parallèle avec `ThreadPoolExecutor`.
- Barre de progression (`tqdm`).

### Version 2.2.0 (2024-09-15)
- Catégorisation automatique par domaines.
- Extraction des compétences.

### Version 2.1.0 (2024-08-10)
- Intégration de l'API Mistral.
- Analyse sémantique IA.

### Version 2.0.0 (2024-07-01)
- Refonte de l'architecture.
- Support de l'environnement virtuel.

### Version 1.x (2023-2024)
- Versions initiales (support ChatGPT uniquement).

---

## Modules Secondaires

### config.py
- **Version** : 2.7.0
- **Contenu** : Constantes globales, gestion de l'API Mistral.

### utils.py
- **Version** : 2.7.0
- **Fonctions** : `ecrire_log()`, `generer_nom_sortie()`, `compter_tokens()`.

### extractors.py
- **Version** : 2.7.0
- **Fonctions** : Détection automatique des formats, extraction multi-format.

### api_analyzer.py
- **Version** : 2.7.0
- **Fonctions** : Appel API Mistral, découpage des conversations.

### reporters.py
- **Version** : 2.7.0
- **Fonctions** : Génération de rapports CSV/TXT.

### install.py
- **Version** : 2.7.0
- **Fonctions** : Vérification et installation des dépendances.

---

## Arguments CLI
```bash
--exec          # Lance l'analyse
--help          # Affiche l'aide
--install       # Installe les dépendances
--chatgpt       # Force le format ChatGPT
--lechat        # Force le format LeChat
--claude        # Force le format Claude
--aiall         # Auto-détection (recommandé)
--local         # Analyse locale (sans API)
--simulate      # Mode simulation
--recursive     # Recherche récursive
--merge-comp    # Fusionne les compétences
--workers -w N  # Workers parallèles
--delay -d N    # Délai entre requêtes API
```

---

## Exemples d'Utilisation
1. **Analyse simple (ChatGPT)** :
   ```bash
   ./analyse_conversations_merged.py --exec --chatgpt --fichier conversations.json
   ```
2. **Auto-détection multi-formats** :
   ```bash
   ./analyse_conversations_merged.py --exec --aiall --fichier "*.json"
   ```
3. **Recherche récursive** :
   ```bash
   ./analyse_conversations_merged.py --exec --recursive --fichier ./exports/
   ```

---

## Roadmap
- **v3.0.0** : Interface web, base de données SQLite, export PDF/Word.
- **v2.8.0** : Cache des résultats, mode diff, export JSON structuré.

---

## Bugs Connus
- Comptage de tokens approximatif.
- Rate limiting fixe (pas adaptatif).

---

## Configuration API Mistral
- **Endpoint** : `https://api.mistral.ai/v1/chat/completions`
- **Modèles** : `mistral-large-latest` (défaut).
- **Clé API** : `export MISTRAL_API_KEY="votre_clé"`

---

## Remerciements
- Mistral AI, OpenAI, Anthropic, communauté Python.
