#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de génération de rapports
Gère la création des fichiers TXT de sujets et compétences
"""

import os
from datetime import datetime
from typing import Dict, List, Set
from categories import ORDRE_PRIORITAIRE, categoriser_competence_automatique


def generer_rapport_sujets(
    sujets_par_domaine: Dict[str, Set[str]],
    resultats: List[Dict],
    stats_chargement: Dict,
    format_source: str,
    multi_fichiers: bool,
    fichiers_a_traiter: List[str],
    mode_local: bool,
    model: str
) -> str:
    """Génère le fichier TXT avec tous les sujets par domaines."""
    
    if multi_fichiers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_filename = f"resultat_sujets_par_domaines_multi_{timestamp}.txt"
    else:
        nom_base = os.path.splitext(os.path.basename(fichiers_a_traiter[0]))[0]
        mode_suffix = "local" if mode_local else "api"
        txt_filename = f"resultat_sujets_par_domaines_{nom_base}_{mode_suffix}.txt"
    
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("╔" + "═" * 98 + "╗\n")
        f.write("║" + " " * 98 + "║\n")
        f.write("║" + "     ANALYSE DES CONVERSATIONS AI - SUJETS PAR DOMAINES".center(98) + "║\n")
        f.write("║" + " " * 98 + "║\n")
        f.write("╚" + "═" * 98 + "╝\n\n")
        
        f.write(f"Analyse effectuée le : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write(f"Nombre de conversations analysées : {len(resultats)}\n")
        f.write(f"Nombre de domaines identifiés : {len(sujets_par_domaine)}\n")
        total_sujets = sum(len(sujets) for sujets in sujets_par_domaine.values())
        f.write(f"Nombre total de sujets uniques : {total_sujets}\n\n")
        
        if format_source == "auto":
            f.write("Formats détectés : ")
            formats_detectes = []
            for fmt in ['chatgpt', 'lechat', 'claude']:
                count = stats_chargement.get(fmt, 0)
                if count > 0:
                    formats_detectes.append(f"{fmt.upper()} ({count})")
            f.write(", ".join(formats_detectes) + "\n\n")
        
        f.write("─" * 100 + "\n\n")
        
        # Domaines à afficher : prioritaires d'abord, puis alphabétique
        domaines_a_afficher = []
        for domaine_prio in ORDRE_PRIORITAIRE:
            if domaine_prio in sujets_par_domaine:
                domaines_a_afficher.append(domaine_prio)
        
        for domaine in sorted(sujets_par_domaine.keys()):
            if domaine not in domaines_a_afficher:
                domaines_a_afficher.append(domaine)
        
        # Affichage de chaque domaine avec tous les sujets
        for index, domaine in enumerate(domaines_a_afficher, 1):
            sujets = sorted(sujets_par_domaine[domaine], key=str.lower)
            
            # Mise en avant spéciale pour l'IA
            is_ia = 'intelligence artificielle' in domaine.lower() or 'ia' in domaine.lower() or 'ml' in domaine.lower()
            
            if is_ia:
                f.write("★" * 100 + "\n")
                f.write(f"★★★  {index}. {domaine.upper()}  ★★★\n")
                f.write("★" * 100 + "\n")
            else:
                f.write(f"{index}. {domaine}\n")
                f.write("─" * 100 + "\n")
            
            f.write(f"   Nombre de sujets uniques : {len(sujets)}\n\n")
            
            # Liste des sujets avec numérotation
            for i, sujet in enumerate(sujets, 1):
                f.write(f"   {i:3d}. {sujet}\n")
            
            f.write("\n")
            if is_ia:
                f.write("★" * 100 + "\n\n")
            else:
                f.write("\n")
        
        # Statistiques finales détaillées
        f.write("═" * 100 + "\n\n")
        f.write("STATISTIQUES DÉTAILLÉES\n\n")
        
        domaines_stats = [(d, len(sujets_par_domaine[d])) for d in domaines_a_afficher]
        domaines_stats_sorted = sorted(domaines_stats, key=lambda x: x[1], reverse=True)
        
        f.write("Répartition des sujets par domaine :\n\n")
        for domaine, count in domaines_stats_sorted:
            pourcentage = (count / total_sujets * 100) if total_sujets > 0 else 0
            barre = "█" * int(pourcentage / 2)
            f.write(f"   {domaine:50s} : {count:4d} ({pourcentage:5.1f}%) {barre}\n")
        
        f.write("\n" + "═" * 100 + "\n\n")
        
        # Domaine le plus représenté
        if domaines_stats_sorted:
            domaine_max = domaines_stats_sorted[0]
            f.write(f"🏆 Domaine le plus représenté : {domaine_max[0]}\n")
            f.write(f"   Nombre de sujets : {domaine_max[1]} ({domaine_max[1]/total_sujets*100:.1f}%)\n\n")
        
        # Distribution des domaines
        domaines_10plus = sum(1 for d, n in domaines_stats if n >= 10)
        domaines_5_9 = sum(1 for d, n in domaines_stats if 5 <= n < 10)
        domaines_moins5 = sum(1 for d, n in domaines_stats if n < 5)
        
        f.write(f"📊 Distribution des sujets :\n")
        f.write(f"   • Domaines avec 10+ sujets : {domaines_10plus}\n")
        f.write(f"   • Domaines avec 5-9 sujets : {domaines_5_9}\n")
        f.write(f"   • Domaines avec <5 sujets : {domaines_moins5}\n\n")
        
        # Informations sur les fichiers sources
        fichiers_sources = set(r.get('_source_file', 'inconnu') for r in resultats)
        if len(fichiers_sources) > 1:
            f.write(f"📁 Fichiers sources analysés : {len(fichiers_sources)}\n\n")
            for fs in sorted(fichiers_sources):
                nb_conv = sum(1 for r in resultats if r.get('_source_file') == fs)
                f.write(f"   • {fs} : {nb_conv} conversation(s)\n")
        
        f.write("\n" + "─" * 100 + "\n")
        f.write(f"\nFichier généré automatiquement par analyse_conversations_merged.py v2.7.0\n")
        f.write(f"Mode d'analyse : {'Local (sans API)' if mode_local else f'API Mistral - {model}'}\n")
    
    return txt_filename


def generer_rapport_competences(
    competences_globales: Dict[str, Set[str]],
    stats_domaines: Dict[str, int],
    fichiers_a_traiter: List[str],
    resultats: List[Dict],
    multi_fichiers: bool,
    mode_local: bool,
    model: str
) -> str:
    """Génère le fichier TXT avec toutes les compétences consolidées."""
    
    if multi_fichiers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_filename = f"resultat_analyse_sujets_multi_competences_par_domaines_{timestamp}.txt"
    else:
        nom_base = os.path.splitext(os.path.basename(fichiers_a_traiter[0]))[0]
        mode_suffix = "local" if mode_local else "api"
        txt_filename = f"resultat_analyse_sujets_{nom_base}_competences_par_domaines_{mode_suffix}.txt"
    
    domaines_tries = []
    for domaine_prioritaire in ORDRE_PRIORITAIRE:
        if domaine_prioritaire in competences_globales:
            domaines_tries.append(domaine_prioritaire)
    
    for domaine in sorted(competences_globales.keys()):
        if domaine not in domaines_tries:
            domaines_tries.append(domaine)
    
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("╔" * 80 + "\n")
        f.write("  COMPÉTENCES PROFESSIONNELLES DÉTECTÉES - CONSOLIDATION PAR DOMAINES\n")
        f.write("  Profil: Expert informatique - 30 ans d'expérience\n")
        f.write("╚" * 80 + "\n\n")
        
        f.write(f"📊 Analyse effectuée le: {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
        f.write(f"📁 Source(s): {len(fichiers_a_traiter)} fichier(s), {len(resultats)} conversation(s)\n")
        f.write(f"🤖 Mode: {'Analyse locale' if mode_local else f'API Mistral ({model})'}\n")
        f.write(f"🎯 Domaines identifiés: {len(competences_globales)}\n")
        total_competences = sum(len(comps) for comps in competences_globales.values())
        f.write(f"✨ Compétences uniques: {total_competences}\n\n")
        
        f.write("─" * 80 + "\n\n")
        
        for idx, domaine in enumerate(domaines_tries, 1):
            competences = sorted(competences_globales[domaine], key=str.lower)
            nb_mentions = stats_domaines[domaine]
            
            is_ia = 'intelligence artificielle' in domaine.lower() or 'ia' in domaine.lower() or 'ml' in domaine.lower()
            
            if is_ia:
                f.write("★" * 80 + "\n")
                f.write(f"★★★  {idx}. {domaine.upper()}  ★★★\n")
                f.write("★" * 80 + "\n")
            else:
                f.write(f"{idx}. {domaine}\n")
                f.write("─" * 80 + "\n")
            
            f.write(f"   Compétences uniques: {len(competences)} | Mentions: {nb_mentions}\n\n")
            
            competences_str = ", ".join(competences)
            f.write(f"   {competences_str}\n\n")
            
            if is_ia:
                f.write("★" * 80 + "\n\n")
            else:
                f.write("\n")
    
    return txt_filename