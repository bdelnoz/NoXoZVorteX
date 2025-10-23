#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'aide
Affiche l'aide et le changelog
"""

import os
from config import VERSION, LOG_FILE, MAX_TOKENS, MAX_WORKERS, MODEL


def afficher_aide() -> None:
    """Affiche l'aide du script."""
    aide = f"""
╔═══════════════════════════════════════════════════════════════╗
║  Analyse de conversations AI {VERSION} - ÉDITION FUSIONNÉE      ║
╚═══════════════════════════════════════════════════════════════╝

Version: {VERSION} (Rapport ultra-détaillé + Tracking complet)
Auteur: Bruno DELNOZ

## NOUVEAUTÉS v2.7.0
  ★ Génération automatique fichier TXT avec TOUS les sujets triés
  ★ Rapport ULTRA-COMPLET des opérations en fin de script
  ★ Affichage détaillé de TOUS les fichiers avec chemins absolus
  ★ Indicateur de split VISUEL pour chaque conversation (✂️/✅)
  ★ Liste complète conversations split vs non-split
  ★ Temps d'exécution + performance (conv/sec)
  ★ Espace disque total utilisé
  ★ Section "Prochaines étapes"

## Configuration API (optionnelle)
export MISTRAL_API_KEY='votre_clé_api'

## Options
  --help              Affiche cette aide
  --exec              Lance l'analyse
  --install           Installe les dépendances
  --chatgpt           Format d'export ChatGPT
  --lechat            Format d'export LeChat (Mistral)
  --claude            Format d'export Claude
  --aiall, --auto     Auto-détection de TOUS les formats
  --local             Analyse locale SANS appel API (gratuit)
  --avec-contexte     Ajoute descriptions/exemples aux sujets
  --merge-comp        Affiche TOUTES les compétences par domaines
  --simulate          Mode simulation API (test sans crédits)
  --only-split        Analyse UNIQUEMENT conversations > {MAX_TOKENS} tokens
  --not-split         Analyse UNIQUEMENT conversations ≤ {MAX_TOKENS} tokens
  --cnbr N            Analyse uniquement la conversation N
  --fichier, -F FILE  Fichier(s) JSON (supporte *.json pour plusieurs)
  --recursive         Recherche récursive dans sous-dossiers
  --model, -m MODEL   Modèle Mistral (défaut: {MODEL})
  --workers, -w N     Workers parallèles (défaut: {MAX_WORKERS})
  --delay, -d N       Délai entre requêtes API (défaut: 0.5s)
  --remove            Supprime élément créé (CSV/log)
  --delete            Suppression propre + backup horodaté
  --undelete          Retour arrière depuis backup
  --prerequis         Vérifier prérequis
  --changelog         Afficher changelog complet

## Exemples
1. Installer:
   python3 analyse_conversations_merged.py --install

2. Auto-détection (tous formats):
   python3 analyse_conversations_merged.py --exec --local --aiall --fichier *.json

3. Analyse ChatGPT locale:
   python3 analyse_conversations_merged.py --exec --local --chatgpt --fichier export.json

4. Analyse LeChat avec API:
   export MISTRAL_API_KEY='votre_clé'
   python3 analyse_conversations_merged.py --exec --lechat --fichier chat-*.json

5. Consolidation complète:
   python3 analyse_conversations_merged.py --exec --local --merge-comp --aiall --fichier *.json

6. Recherche récursive:
   python3 analyse_conversations_merged.py --exec --recursive --aiall --fichier **/*.json

## Focus IA
Le script détecte et met en avant:
  • Outils IA: ChatGPT, Claude, DALL-E, Midjourney, etc.
  • Techniques: Prompt Engineering, Fine-tuning, RAG
  • Frameworks: LangChain, Hugging Face, TensorFlow, PyTorch
  • Concepts: NLP, Computer Vision, MLOps
  • Compétences stratégiques affichées en PREMIER

## Sortie
Fichier CSV: resultat_analyse_*.csv
Fichier TXT sujets: resultat_sujets_par_domaines_*.txt
Fichier TXT compétences: resultat_analyse_*_competences_par_domaines.txt (avec --merge-comp)
  - Section IA dédiée en priorité
  - Format optimisé LinkedIn/CV
  - Log: {LOG_FILE} (rotation auto)
  - Backup: .backup.timestamp pour --delete
"""
    print(aide)


def afficher_changelog() -> None:
    """Affiche le changelog complet."""
    print("""
CHANGELOG COMPLET:

v2.7.0 (2025-10-19):
  - Génération automatique fichier TXT avec TOUS les sujets triés par domaines
  - Rapport ULTRA-COMPLET des opérations effectuées en fin de script
  - Affichage détaillé de TOUS les fichiers générés avec chemins absolus
  - Indicateur de split VISUEL pour CHAQUE conversation (✂️ SPLIT / ✅ OK)
  - Statistiques détaillées conversations split vs non-split avec liste complète
  - Tableau récapitulatif des fichiers avec type, taille, description, chemin
  - Temps d'exécution total + métriques de performance (conv/sec)
  - Espace disque total utilisé par tous les fichiers générés
  - Section "Prochaines étapes" pour guider l'utilisateur
  - Conservation INTÉGRALE du code v2.6.0 + ajouts massifs

v2.6.0 (2025-10-19):
  - Génération automatique fichier TXT avec TOUS les sujets triés par domaines
  - Rapport complet des opérations effectuées en fin de script
  - Affichage détaillé de TOUS les fichiers générés avec tailles et chemins
  - Indicateur de split pour chaque conversation (OUI/NON)
  - Statistiques détaillées conversations split vs non-split
  - Tableau récapitulatif des fichiers avec métriques
  - Temps d'exécution total et performance (conv/sec)
  - Conservation TOTALE du code v2.5.0

v2.5.0 (2025-10-19):
  - Fusion COMPLÈTE v2.3.3 + v2.4.0 sans doublons
  - Auto-détection intelligente: ChatGPT/LeChat/Claude
  - Support multi-formats simultané
  - Extraction optimisée par format (contentChunks inclus)
  - Consolidation avancée avec stats ultra-détaillées
  - Recherche récursive + multi-fichiers
  - Focus IA renforcé (score x3)
  - 35+ domaines de compétences
  - Logging complet avec rotation
  - Options backup/restore/delete/undelete
  - Mode simulation + prerequis
  - Gestion complète erreurs et retry
  - Normalisation intelligente domaines/compétences
  - Affichage ultra verbeux avec tableaux

v2.4.0 (2025-10-19):
  - AUTO-DÉTECTION MULTI-FORMATS
  - Fix: "--chatgpt et --lechat mutuellement exclusifs"
  - Fix: "Aucun message extrait" pour fichiers LeChat
  - --aiall: traite TOUS les formats dans un seul run

v2.3.3 (2025-10-19):
  - --recursive: recherche récursive .json
  - Traitement multi-fichiers étendu
  - Logs: fichiers trouvés récursivement

v2.3.2 (2025-10-19):
  - Correction SyntaxError
  - Ajout --remove, --delete, --undelete, --prerequis, --simulate, --changelog
  - Backup automatique horodaté
  
v2.3.1 (2025-10-19):
  - Support COMPLET LeChat: content + contentChunks
  - Compatible exports Mistral/LeChat natifs

v2.3.0 (2025-10-18):
  - PRIORITÉ MAXIMALE sur compétences IA/ML
  - Détection exhaustive IA
  - Catégorisation automatique avec bonus IA (x3)
    """)
