NoXoZVorteX is an open-source toolkit to consolidate AI conversation history into actionable knowledge.

## What it does today
- Extracts `.zip` exports and gathers `.json` files (`extract_and_collect_json.py`).
- Analyzes conversations across **ChatGPT, LeChat/Mistral, and Claude** (`analyse_conversations_merged.py`).
- Produces CSV/TXT reports for topics and skill domains.
- Extracts conversation titles with filtering/merge options (`extraire_titres_conversations.py`).
- Provides a shell script to test Mistral API calls (`testapi_lechat.sh`).

## Why this project
After hundreds of AI conversations spread over multiple exports, this project helps centralize, deduplicate, and transform that content into structured skill insights.

## Tech stack
- Python 3.8+
- Optional Mistral API integration (`MISTRAL_API_KEY`)
- Modular scripts (extract/collect, analyze, report, title extraction)

## Current maturity
- Functional CLI tooling with modular architecture.
- Works as a practical automation toolkit; still evolving.

---

NoXoZVorteX est une boîte à outils open-source pour transformer des historiques de conversations IA en connaissances exploitables.

## Ce que le projet fait aujourd'hui
- Extrait les exports `.zip` et regroupe les `.json` (`extract_and_collect_json.py`).
- Analyse des conversations **ChatGPT, LeChat/Mistral et Claude** (`analyse_conversations_merged.py`).
- Génère des rapports CSV/TXT (sujets et domaines de compétences).
- Extrait les titres avec filtres/fusion (`extraire_titres_conversations.py`).
- Fournit un script shell de test API Mistral (`testapi_lechat.sh`).

## Pourquoi ce projet
Après des centaines de conversations IA réparties dans plusieurs exports, l'objectif est de centraliser, dédupliquer et convertir ces échanges en insights de compétences.

## Stack technique
- Python 3.8+
- Intégration API Mistral optionnelle (`MISTRAL_API_KEY`)
- Scripts modulaires (extract/collect, analyse, reporting, extraction de titres)

## Maturité actuelle
- Outillage CLI fonctionnel et modulaire.
- Utilisable en production personnelle, avec évolutions en cours.
