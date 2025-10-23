#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nom du script: analyse_conversations_merged.py
Auteur: Bruno DELNOZ - bruno.delnoz@protonmail.com
Version: v2.7.5 - FIX ERREUR IMPORT + LOGIQUE FINALE
Date: 2025-10-22

Script principal - Orchestre tous les modules
"""

import os
import sys
import argparse
import json
import csv
import glob
import time
import hashlib
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

# Imports des modules locaux
# NOTE IMPORT FIXE: verifier_prerequis remplacé par verifier_prerequis_complet
from config import (
    VERSION, INPUT_FILE, MAX_WORKERS, MODEL, MAX_TOKENS,
    ENV_DIR, obtenir_api_key
)
from utils import ecrire_log, generer_nom_sortie, compter_tokens
from extractors import extraire_messages, detecter_format_json
from api_analyzer import analyser_conversation, decouper_conversation
from reporters import generer_rapport_sujets, generer_rapport_competences
from install import (
    verifier_prerequis_complet, verifier_dependances, installer_dependances,
    supprimer_fichier
)
from help import afficher_aide, afficher_changelog
from categories import (
    categoriser_competence_automatique, normaliser_domaine,
    normaliser_competence
)


def generer_hash_conversation(conv: Dict, format_conv: str) -> str:
    """
    Génère un hash unique pour une conversation basé sur son contenu.
    Utilisé pour détecter les doublons.
    """
    # Créer une signature unique basée sur plusieurs critères
    signature_parts = []

    # 1. Titre ou nom
    titre = conv.get("title", conv.get("name", ""))
    if titre:
        signature_parts.append(f"title:{titre}")

    # 2. ID de conversation si disponible
    conv_id = conv.get("id", conv.get("uuid", conv.get("conversation_id", "")))
    if conv_id:
        signature_parts.append(f"id:{conv_id}")

    # 3. Timestamp de création si disponible
    created = conv.get("create_time", conv.get("created_at", conv.get("createdAt", "")))
    if created:
        signature_parts.append(f"created:{created}")

    # 4. Nombre de messages
    if format_conv == "chatgpt":
        mapping = conv.get("mapping", {})
        nb_messages = len([m for m in mapping.values() if m.get("message")])
    elif format_conv == "lechat":
        messages = conv.get("messages", conv.get("exchanges", []))
        nb_messages = len(messages)
    elif format_conv == "claude":
        messages = conv.get("chat_messages", [])
        nb_messages = len(messages)
    else:
        nb_messages = 0

    signature_parts.append(f"msgs:{nb_messages}")

    # 5. Hash des premiers et derniers messages (pour signature de contenu)
    try:
        from extractors import extraire_messages
        messages_text = extraire_messages(conv, format_conv)
        if messages_text:
            # Prendre les 3 premiers et 3 derniers messages
            sample_messages = messages_text[:3] + messages_text[-3:]
            content_sample = "".join(sample_messages)
            # Hash du contenu échantillon
            content_hash = hashlib.md5(content_sample.encode('utf-8')).hexdigest()[:8]
            signature_parts.append(f"content:{content_hash}")
    except:
        pass

    # Créer le hash final
    signature = "|".join(signature_parts)
    return hashlib.sha256(signature.encode('utf-8')).hexdigest()


def detecter_doublons(toutes_conversations: List[Dict]) -> Dict[str, Any]:
    """
    Détecte les conversations en doublon et retourne les statistiques.
    """
    hash_map = {}
    doublons = []
    conversations_uniques = []

    for idx, conv in enumerate(toutes_conversations):
        format_conv = conv.get('_format', 'unknown')
        conv_hash = generer_hash_conversation(conv, format_conv)

        if conv_hash in hash_map:
            # Doublon détecté
            original_idx = hash_map[conv_hash]
            original_conv = toutes_conversations[original_idx]

            doublons.append({
                'original': {
                    'index': original_idx,
                    'titre': original_conv.get('title', original_conv.get('name', 'Sans titre')),
                    'fichier': original_conv.get('_source_file', 'inconnu'),
                    'format': original_conv.get('_format', 'unknown')
                },
                'doublon': {
                    'index': idx,
                    'titre': conv.get('title', conv.get('name', 'Sans titre')),
                    'fichier': conv.get('_source_file', 'inconnu'),
                    'format': conv.get('_format', 'unknown')
                },
                'hash': conv_hash
            })
        else:
            # Conversation unique
            hash_map[conv_hash] = idx
            conversations_uniques.append(conv)

    return {
        'conversations_uniques': conversations_uniques,
        'doublons': doublons,
        'nb_total': len(toutes_conversations),
        'nb_uniques': len(conversations_uniques),
        'nb_doublons': len(doublons)
    }


def afficher_rapport_doublons(rapport_doublons: Dict[str, Any]) -> None:
    """
    Affiche un rapport détaillé des doublons détectés.
    """
    if rapport_doublons['nb_doublons'] == 0:
        print("✅ Aucun doublon détecté\n")
        return

    print(f"\n⚠️  DOUBLONS DÉTECTÉS")
    print("─" * 100)
    print(f"   • Conversations totales : {rapport_doublons['nb_total']}")
    print(f"   • Conversations uniques : {rapport_doublons['nb_uniques']}")
    print(f"   • Doublons trouvés : {rapport_doublons['nb_doublons']}")
    print()

    print("   Détail des doublons :")
    print()

    for i, doublon in enumerate(rapport_doublons['doublons'], 1):
        orig = doublon['original']
        dupl = doublon['doublon']

        print(f"   [{i}] Doublon détecté :")
        print(f"       ➤ ORIGINAL  : #{orig['index']:3d} - {orig['titre'][:60]}")
        print(f"         └─ Fichier : {orig['fichier']} [{orig['format'].upper()}]")
        print(f"       ➤ DOUBLON   : #{dupl['index']:3d} - {dupl['titre'][:60]}")
        print(f"         └─ Fichier : {dupl['fichier']} [{dupl['format'].upper()}]")
        print(f"       └─ Hash    : {doublon['hash'][:16]}...")
        print()

    print(f"{'─' * 100}\n")
    print(f"💡 Les doublons ont été automatiquement exclus de l'analyse.")
    print(f"   Seules les {rapport_doublons['nb_uniques']} conversations uniques seront traitées.\n")


def charger_fichiers(fichiers_a_traiter: List[str], format_source: str) -> tuple:
    """Charge et analyse les fichiers JSON."""
    toutes_conversations = []
    stats_chargement = {'chatgpt': 0, 'lechat': 0, 'claude': 0, 'unknown': 0, 'erreurs': 0}

    print("📂 Chargement des fichiers...")
    for fichier in fichiers_a_traiter:
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)

            if format_source == "auto":
                format_detecte = detecter_format_json(data, fichier)
            else:
                format_detecte = format_source

            stats_chargement[format_detecte] = stats_chargement.get(format_detecte, 0) + 1

            if format_detecte == "chatgpt":
                if isinstance(data, list):
                    for conv in data:
                        conv['_source_file'] = os.path.basename(fichier)
                        conv['_format'] = 'chatgpt'
                        toutes_conversations.append(conv)
                    print(f"   ✅ ChatGPT: {os.path.basename(fichier)} ({len(data)} conversations)")

            elif format_detecte == "lechat":
                if isinstance(data, list):
                    titre = os.path.splitext(os.path.basename(fichier))[0]
                    import re
                    titre = re.sub(r'^chat-', '', titre)
                    titre = re.sub(r'^AI_exportation_', '', titre)
                    titre = re.sub(r'_conversations$', '', titre)
                    conv = {
                        "title": titre or "Conversation LeChat",
                        "messages": data,
                        "_source_file": os.path.basename(fichier),
                        "_format": "lechat"
                    }
                    toutes_conversations.append(conv)
                    print(f"   ✅ LeChat: {os.path.basename(fichier)} ({len(data)} messages)")
                elif isinstance(data, dict):
                    titre = data.get("title", os.path.splitext(os.path.basename(fichier))[0])
                    data['title'] = titre
                    data['_source_file'] = os.path.basename(fichier)
                    data['_format'] = 'lechat'
                    toutes_conversations.append(data)
                    nb_msg = len(data.get('messages', data.get('exchanges', [])))
                    print(f"   ✅ LeChat: {os.path.basename(fichier)} ({nb_msg} messages)")

            elif format_detecte == "claude":
                if isinstance(data, list):
                    for conv in data:
                        conv['_source_file'] = os.path.basename(fichier)
                        conv['_format'] = 'claude'
                        if 'title' not in conv and 'name' not in conv:
                            conv['title'] = f"Claude - {conv.get('uuid', 'Sans titre')[:8]}"
                        toutes_conversations.append(conv)
                    print(f"   ✅ Claude: {os.path.basename(fichier)} ({len(data)} conversations)")
                elif isinstance(data, dict):
                    data['_source_file'] = os.path.basename(fichier)
                    data['_format'] = 'claude'
                    if 'title' not in data and 'name' not in data:
                        data['title'] = f"Claude - {data.get('uuid', 'Sans titre')[:8]}"
                    toutes_conversations.append(data)
                    print(f"   ✅ Claude: {os.path.basename(fichier)} (1 conversation)")

            else:
                print(f"   ⚠️ Format inconnu: {os.path.basename(fichier)}")
                stats_chargement['unknown'] = stats_chargement.get('unknown', 0) + 1

        except json.JSONDecodeError as e:
            print(f"   ❌ Erreur JSON: {os.path.basename(fichier)}")
            ecrire_log(f"Erreur JSON {fichier}: {e}", "ERROR")
            stats_chargement['erreurs'] += 1
        except Exception as e:
            print(f"   ❌ Erreur: {os.path.basename(fichier)}")
            ecrire_log(f"Erreur {fichier}: {e}", "ERROR")
            stats_chargement['erreurs'] += 1

    return toutes_conversations, stats_chargement


def preparer_conversations(
    toutes_conversations: List[Dict],
    format_source: str,
    args: argparse.Namespace
) -> tuple:
    """Prépare les conversations pour l'analyse."""
    print("📋 Extraction des messages:")
    conversations_a_analyser = []
    conversations_splittees_info = []

    for idx, conv in enumerate(toutes_conversations):
        titre = conv.get("title", conv.get("name", f"Conversation #{idx + 1}"))
        source_file = conv.get('_source_file', 'inconnu')
        format_conv = conv.get('_format', format_source)

        messages = extraire_messages(conv, format_conv)

        if not messages:
            print(f"   ⚠️ #{idx + 1}: {titre[:50]}... - Aucun message")
            continue

        token_count = compter_tokens("\n".join(messages))
        sera_splittee = token_count > MAX_TOKENS

        split_status = "SPLIT" if sera_splittee else "OK"
        split_icon = "✂️" if sera_splittee else "✅"

        print(f"   • #{idx + 1}: {titre[:60]}")
        print(f"     └─ {len(messages)} messages, {token_count:,} tokens, {format_conv.upper()} [{split_icon} {split_status}]")

        conversations_splittees_info.append({
            'index': idx + 1,
            'titre': titre,
            'sera_splittee': sera_splittee,
            'token_count': token_count,
            'nb_messages': len(messages)
        })

        if args.cnbr and (idx + 1) != args.cnbr:
            continue

        if args.only_split and not sera_splittee:
            continue

        if args.not_split and sera_splittee:
            continue

        parties = decouper_conversation(conv, messages)
        for partie in parties:
            partie['_source_file'] = source_file
            partie['_format'] = format_conv
        conversations_a_analyser.extend(parties)

    return conversations_a_analyser, conversations_splittees_info


def analyser_toutes_conversations(
    conversations_a_analyser: List[Dict],
    api_key: str,
    args: argparse.Namespace
) -> List[Dict]:
    """Analyse toutes les conversations en parallèle."""
    try:
        from tqdm import tqdm
        use_tqdm = True
    except ImportError:
        use_tqdm = False
        print("⚠️ tqdm non disponible, utilisation de print simple")

    resultats = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                analyser_conversation,
                conv,
                api_key,
                args.model,
                args.simulate,
                args.local,
                args.avec_contexte,
                args.delay
            ): conv
            for conv in conversations_a_analyser
        }

        if use_tqdm:
            for future in tqdm(
                as_completed(futures),
                total=len(conversations_a_analyser),
                desc="🔄 Analyse",
                unit="conv"
            ):
                try:
                    resultats.append(future.result())
                except Exception as e:
                    ecrire_log(f"Erreur traitement: {e}", "ERROR")
        else:
            total = len(conversations_a_analyser)
            for i, future in enumerate(as_completed(futures), 1):
                try:
                    resultats.append(future.result())
                    print(f"🔄 Analyse: {i}/{total} conversations", end='\r')
                except Exception as e:
                    ecrire_log(f"Erreur traitement: {e}", "ERROR")
            print()

    return sorted(resultats, key=lambda x: (x.get("conversation_id", ""), x.get("partie", "1/1")))


def sauvegarder_resultats_csv(
    OUTPUT_FILE: str,
    resultats: List[Dict],
    multi_fichiers: bool,
    format_source: str
) -> None:
    """Sauvegarde les résultats dans un fichier CSV."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        fieldnames = [
            "conversation_id", "titre_original", "titre", "sujets",
            "nombre_sujets", "nombre_domaines", "token_count", "statut", "partie"
        ]
        if multi_fichiers or format_source == "auto":
            fieldnames.extend(["fichier_source", "format"])

        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        if multi_fichiers or format_source == "auto":
            for r in resultats:
                if 'fichier_source' not in r:
                    r['fichier_source'] = r.get('_source_file', 'inconnu')
                if 'format' not in r:
                    r['format'] = r.get('_format', 'unknown')

        writer.writerows(resultats)


def collecter_sujets_par_domaine(resultats: List[Dict]) -> Dict[str, set]:
    """Collecte et organise les sujets par domaine."""
    sujets_par_domaine = {}

    for resultat in resultats:
        sujets = resultat.get("sujets", "")
        if sujets and not sujets.startswith("[ERREUR") and sujets != "[VIDE]":
            for sujet_complet in sujets.split(";"):
                sujet_complet = sujet_complet.strip()
                if not sujet_complet:
                    continue

                if sujet_complet.startswith("[") and "]" in sujet_complet:
                    domaine = sujet_complet[1:sujet_complet.index("]")]
                    sujet = sujet_complet[sujet_complet.index("]")+1:].strip()
                else:
                    domaine = categoriser_competence_automatique(sujet_complet)
                    sujet = sujet_complet

                if domaine not in sujets_par_domaine:
                    sujets_par_domaine[domaine] = set()
                sujets_par_domaine[domaine].add(sujet)

    return sujets_par_domaine


def consolider_competences(resultats: List[Dict]) -> tuple:
    """Consolide toutes les compétences par domaine."""
    competences_globales = {}
    stats_domaines = {}

    for resultat in resultats:
        if "competences_par_domaine" in resultat:
            for domaine, competences in resultat["competences_par_domaine"].items():
                domaine_norm = normaliser_domaine(domaine)
                if domaine_norm not in competences_globales:
                    competences_globales[domaine_norm] = set()
                    stats_domaines[domaine_norm] = 0

                for comp in competences:
                    comp_norm = normaliser_competence(comp)
                    if comp_norm and len(comp_norm) > 2:
                        competences_globales[domaine_norm].add(comp_norm)
                stats_domaines[domaine_norm] += 1
        else:
            sujets = resultat.get("sujets", "")
            if sujets and not sujets.startswith("[ERREUR") and sujets != "[VIDE]":
                for sujet in sujets.split(";"):
                    sujet = sujet.strip()
                    if not sujet:
                        continue

                    if sujet.startswith("[") and "]" in sujet:
                        domaine = sujet[1:sujet.index("]")]
                        competence = sujet[sujet.index("]")+1:].strip()
                    else:
                        domaine = categoriser_competence_automatique(sujet)
                        competence = sujet

                    domaine_norm = normaliser_domaine(domaine)
                    comp_norm = normaliser_competence(competence)

                    if len(comp_norm) > 2:
                        if domaine_norm not in competences_globales:
                            competences_globales[domaine_norm] = set()
                            stats_domaines[domaine_norm] = 0
                        competences_globales[domaine_norm].add(comp_norm)
                        stats_domaines[domaine_norm] += 1

    return competences_globales, stats_domaines


def afficher_rapport_final(
    temps_debut: float,
    resultats: List[Dict],
    conversations_splittees_info: List[Dict],
    fichiers_generes: List[Dict],
    OUTPUT_FILE: str,
    total_sujets: int,
    len_sujets_par_domaine: int
) -> None:
    """Affiche le rapport détaillé final."""
    temps_fin = time.time()
    temps_execution = temps_fin - temps_debut

    print("\n" + "╔" * 100)
    print("╔" + "═" * 98 + "╔")
    print("╔" + " " * 30 + "📊 RAPPORT DÉTAILLÉ DES OPÉRATIONS" + " " * 34 + "╔")
    print("╔" + "═" * 98 + "╔")
    print("╚" * 100 + "\n")

    print("⏱️  TEMPS D'EXÉCUTION")
    print("─" * 100)
    minutes = int(temps_execution // 60)
    secondes = int(temps_execution % 60)
    print(f"   • Durée totale : {minutes}m {secondes}s ({temps_execution:.2f} secondes)")
    if len(resultats) > 0:
        conv_par_sec = len(resultats) / temps_execution
        print(f"   • Performance : {conv_par_sec:.2f} conversations/seconde")
    print()

    print("✂️  DÉTAIL DES CONVERSATIONS SPLIT/NON-SPLIT")
    print("─" * 100)
    nb_splittees = sum(1 for info in conversations_splittees_info if info['sera_splittee'])
    nb_non_splittees = len(conversations_splittees_info) - nb_splittees

    print(f"\n   Conversations NON découpées ({nb_non_splittees}) :\n")
    for info in conversations_splittees_info:
        if not info['sera_splittee']:
            print(f"      ✅ #{info['index']:3d} - {info['titre'][:70]}")
            print(f"           └─ {info['nb_messages']} messages, {info['token_count']:,} tokens")

    if nb_splittees > 0:
        print(f"\n   Conversations DÉCOUPÉES ({nb_splittees}) :\n")
        for info in conversations_splittees_info:
            if info['sera_splittee']:
                print(f"      ✂️  #{info['index']:3d} - {info['titre'][:70]}")
                print(f"           └─ {info['nb_messages']} messages, {info['token_count']:,} tokens → SPLIT EN 2 PARTIES")
    print()

    print("📁 FICHIERS GÉNÉRÉS - RÉCAPITULATIF COMPLET")
    print("─" * 100)
    print(f"\n   Nombre total de fichiers générés : {len(fichiers_generes)}\n")

    for i, fichier in enumerate(fichiers_generes, 1):
        print(f"   {i}. [{fichier['type']}] {fichier['nom']}")
        print(f"      ├─ Description : {fichier['description']}")
        print(f"      ├─ Taille : {fichier['taille']:,} octets ({fichier['taille']/1024:.2f} KB)")
        print(f"      └─ Chemin : {fichier['chemin']}")
        print()

    taille_totale = sum(f['taille'] for f in fichiers_generes)
    print(f"   💾 Espace disque total utilisé : {taille_totale:,} octets ({taille_totale/1024:.2f} KB / {taille_totale/1024/1024:.2f} MB)")
    print()

    print("📊 STATISTIQUES FINALES")
    print("─" * 100)
    analysees = sum(1 for r in resultats if "Analysée" in r["statut"] or r["statut"] == "Simulée")
    vides = sum(1 for r in resultats if r["statut"] == "Vide")
    erreurs = sum(1 for r in resultats if "Erreur" in r["statut"])
    total_tokens = sum(r.get("token_count", 0) for r in resultats)
    parties_splittees = sum(1 for r in resultats if "/" in r.get("partie", "1/1") and r.get("partie") != "1/1")

    print(f"   • Conversations analysées : {len(resultats)}")
    print(f"   • Analysées avec succès : {analysees}")
    print(f"   • Vides : {vides}")
    print(f"   • Erreurs : {erreurs}")
    print(f"   • Conversations splittées : {nb_splittees}")
    print(f"   • Parties générées (split) : {parties_splittees}")
    print(f"   • Total tokens traités : {total_tokens:,}")
    print(f"   • Domaines identifiés : {len_sujets_par_domaine}")
    print(f"   • Sujets uniques : {total_sujets}")
    print()

    print("╔" * 100)
    print("╔" + "═" * 98 + "╔")
    print("╔" + " " * 25 + "✅ ANALYSE TERMINÉE AVEC SUCCÈS - v2.7.5" + " " * 32 + "╔")
    print("╔" + "═" * 98 + "╔")
    print("╚" * 100 + "\n")

    print("💡 PROCHAINES ÉTAPES :")
    print("   1. Consultez le fichier CSV pour les données brutes")
    print("   2. Consultez le fichier TXT sujets pour une vue organisée par domaines")
    print("   3. Utilisez ces informations pour enrichir votre CV ou profil LinkedIn")
    print()


def main() -> None:
    """Fonction principale."""
    temps_debut = time.time()

    if len(sys.argv) == 1:
        afficher_aide()
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    parser.add_argument('--exec', action='store_true')
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--chatgpt', action='store_true', default=False)
    parser.add_argument('--lechat', action='store_true', default=False)
    parser.add_argument('--claude', action='store_true', default=False)
    parser.add_argument('--aiall', '--auto', action='store_true', default=False)
    parser.add_argument('--local', action='store_true', default=False)
    parser.add_argument('--avec-contexte', action='store_true', default=False)
    parser.add_argument('--merge-comp', action='store_true', default=False)
    parser.add_argument('--simulate', action='store_true', default=False)
    parser.add_argument('--only-split', action='store_true', default=False)
    parser.add_argument('--not-split', action='store_true', default=False)
    parser.add_argument('--cnbr', type=int)
    parser.add_argument('--fichier', '-F', type=str, nargs='*', default=[INPUT_FILE])
    parser.add_argument('--model', '-m', type=str, default=MODEL)
    parser.add_argument('--workers', '-w', type=int, default=MAX_WORKERS)
    parser.add_argument('--delay', '-d', type=float, default=0.5)
    parser.add_argument('--remove', action='store_true')
    parser.add_argument('--delete', action='store_true')
    parser.add_argument('--undelete', action='store_true')
    parser.add_argument('--prerequis', action='store_true')
    parser.add_argument('--changelog', action='store_true')
    parser.add_argument('--recursive', action='store_true', default=False)

    args = parser.parse_args()

    # Gestion des commandes simples
    if args.help:
        afficher_aide()
        return

    if args.changelog:
        afficher_changelog()
        return

    if args.prerequis:
        verifier_prerequis_complet()
        return

    if args.install:
        installer_dependances()
        return

    if args.remove or args.delete:
        fichiers = glob.glob("resultat_analyse_*.csv") + glob.glob("log.analyse_chatgpt*.log")
        for f in fichiers:
            supprimer_fichier(f, backup=args.delete)
        return

    if args.undelete:
        import shutil
        backups = glob.glob("*.backup.*")
        if backups:
            recent = max(backups, key=os.path.getctime)
            target = recent.split('.backup.')[0]
            shutil.copy2(recent, target)
            print(f"🔄 Restauré depuis {recent} vers {target}")
        else:
            print("⚠️ Aucun backup trouvé")
        return

    if not args.exec:
        print("❌ Utilisez --exec pour lancer l'analyse.")
        return

    # Vérification des dépendances
    api_key = None
    if not args.local:
        manquantes = verifier_dependances()
        if manquantes:
            print("❌ Dépendances manquantes. Veuillez exécuter le script depuis l'environnement virtuel.")
            print(f"\n1. Activez le venv: source {ENV_DIR}/bin/activate")
            print("2. Ré-exécutez la commande.")
            sys.exit(1)

        if not args.simulate:
            api_key = obtenir_api_key()

    # Déterminer le format
    if args.aiall:
        format_source = "auto"
    elif args.claude:
        format_source = "claude"
    elif args.chatgpt:
        format_source = "chatgpt"
    elif args.lechat:
        format_source = "lechat"
    else:
        format_source = "auto"

    # Recherche des fichiers - SECTION CORRIGÉE
    fichier_patterns = args.fichier if isinstance(args.fichier, list) else [args.fichier]
    fichiers_a_traiter = []

    for pattern in fichier_patterns:
        # Si --recursive est activé et que le pattern ne contient pas déjà **
        if args.recursive and '**' not in pattern:
            # Si le pattern est un répertoire, ajouter **/*.json
            if os.path.isdir(pattern):
                pattern = os.path.join(pattern, '**', '*.json')
            # Si c'est un fichier avec wildcard, ajouter ** au chemin
            elif '*' in pattern:
                base_dir = os.path.dirname(pattern) or '.'
                filename = os.path.basename(pattern)
                pattern = os.path.join(base_dir, '**', filename)
            # Sinon, chercher le pattern dans tous les sous-dossiers
            else:
                base_dir = os.path.dirname(pattern) or '.'
                filename = os.path.basename(pattern)
                if filename:
                    pattern = os.path.join(base_dir, '**', filename)
                else:
                    pattern = os.path.join(pattern, '**', '*.json')

        # Effectuer la recherche
        if '**' in pattern or args.recursive:
            fichiers_trouves = glob.glob(pattern, recursive=True)
        else:
            fichiers_trouves = glob.glob(pattern)

        if fichiers_trouves:
            fichiers_a_traiter.extend(fichiers_trouves)
            ecrire_log(f"Fichiers trouvés pour {pattern}: {len(fichiers_trouves)}", "INFO")

    if not fichiers_a_traiter:
        print(f"❌ Aucun fichier trouvé")
        return

    fichiers_a_traiter = sorted(list(set(fichiers_a_traiter)))

    if len(fichiers_a_traiter) > 1:
        print(f"📁 Fichiers trouvés: {len(fichiers_a_traiter)}")
        for f in fichiers_a_traiter:
            print(f"   • {f}")
        print()

    multi_fichiers = len(fichiers_a_traiter) > 1
    OUTPUT_FILE = generer_nom_sortie(
        fichiers_a_traiter[0],
        multi_fichiers,
        args.local,
        args.only_split,
        args.not_split
    )

    # Affichage header
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  Analyse de conversations AI v2.7.5 - FIX ERREUR IMPORT       ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    if multi_fichiers:
        print(f"📁 Fichiers: {len(fichiers_a_traiter)} fichiers JSON")
    else:
        print(f"📁 Fichier: {fichiers_a_traiter[0]}")
    print(f"🤖 Modèle: {args.model if not args.local else 'Analyse locale (sans API)'}")
    print(f"⚡ Workers: {args.workers}")

    if format_source == "auto":
        print("🔍 Format: AUTO-DÉTECTION (ChatGPT/LeChat/Claude)")
    else:
        print(f"📄 Format: {format_source.upper()}")

    if args.local:
        print("🔧 Mode: ANALYSE LOCALE (gratuit, sans API)")
    elif args.simulate:
        print("🧪 Mode: SIMULATION")

    if args.recursive:
        print("🔍 Mode: RECHERCHE RÉCURSIVE activée")
    print()

    try:
        # Chargement des fichiers
        toutes_conversations, stats_chargement = charger_fichiers(fichiers_a_traiter, format_source)

        if not toutes_conversations:
            print("\n❌ Aucune conversation trouvée.")
            return

        print(f"\n{'─' * 70}")
        print(f"📊 Total chargé: {len(toutes_conversations)} conversations")
        if format_source == "auto":
            print(f"\n📋 Formats détectés:")
            for fmt in ['chatgpt', 'lechat', 'claude']:
                count = stats_chargement.get(fmt, 0)
                if count > 0:
                    icone = "🤖" if fmt == "chatgpt" else "🦙" if fmt == "lechat" else "🧠"
                    print(f"   {icone} {fmt.upper()}: {count} fichier(s)")
        print(f"{'─' * 70}\n")

        # Détection des doublons
        print("🔍 Détection des doublons...")
        rapport_doublons = detecter_doublons(toutes_conversations)
        afficher_rapport_doublons(rapport_doublons)

        # Utiliser uniquement les conversations uniques
        toutes_conversations = rapport_doublons['conversations_uniques']

        if not toutes_conversations:
            print("\n❌ Aucune conversation unique trouvée après déduplication.")
            return

        # Préparation des conversations
        conversations_a_analyser, conversations_splittees_info = preparer_conversations(
            toutes_conversations, format_source, args
        )

        if not conversations_a_analyser:
            print("\n❌ Aucune conversation à analyser après filtrage.")
            return

        print(f"\n{'╔' * 70}")
        print(f"✅ {len(conversations_a_analyser)} conversations analysables")
        print(f"{'╚' * 70}\n")

        # Analyse des conversations
        resultats = analyser_toutes_conversations(conversations_a_analyser, api_key, args)

        # Sauvegarde CSV
        sauvegarder_resultats_csv(OUTPUT_FILE, resultats, multi_fichiers, format_source)

        # Collecte des sujets
        sujets_par_domaine = collecter_sujets_par_domaine(resultats)

        # Génération rapport sujets
        txt_sujets_filename = generer_rapport_sujets(
            sujets_par_domaine,
            resultats,
            stats_chargement,
            format_source,
            multi_fichiers,
            fichiers_a_traiter,
            args.local,
            args.model
        )

        total_sujets = sum(len(sujets) for sujets in sujets_par_domaine.values())
        txt_sujets_size = os.path.getsize(txt_sujets_filename) if os.path.exists(txt_sujets_filename) else 0
        print(f"✅ Fichier TXT sujets créé: {txt_sujets_filename}")
        print(f"   └─ {len(sujets_par_domaine)} domaines, {total_sujets} sujets uniques")
        print(f"   └─ Taille: {txt_sujets_size:,} octets ({txt_sujets_size/1024:.2f} KB)\n")

        # Liste des fichiers générés
        from config import LOG_FILE
        fichiers_generes = []

        if os.path.exists(OUTPUT_FILE):
            fichiers_generes.append({
                'nom': OUTPUT_FILE,
                'type': 'CSV',
                'description': 'Résultats bruts de l\'analyse',
                'taille': os.path.getsize(OUTPUT_FILE),
                'chemin': os.path.abspath(OUTPUT_FILE)
            })

        if os.path.exists(txt_sujets_filename):
            fichiers_generes.append({
                'nom': txt_sujets_filename,
                'type': 'TXT',
                'description': f'Tous les sujets triés ({len(sujets_par_domaine)} domaines, {total_sujets} sujets)',
                'taille': os.path.getsize(txt_sujets_filename),
                'chemin': os.path.abspath(txt_sujets_filename)
            })

        if os.path.exists(LOG_FILE):
            fichiers_generes.append({
                'nom': LOG_FILE,
                'type': 'LOG',
                'description': 'Journal des opérations',
                'taille': os.path.getsize(LOG_FILE),
                'chemin': os.path.abspath(LOG_FILE)
            })

        # Consolidation des compétences si demandé
        if args.merge_comp:
            print("\n" + "╔" * 70)
            print("📊 CONSOLIDATION DES COMPÉTENCES PAR DOMAINES")
            print("╚" * 70 + "\n")

            competences_globales, stats_domaines = consolider_competences(resultats)

            if not competences_globales:
                print("⚠️ Aucune compétence trouvée à consolider.\n")
            else:
                txt_comp_filename = generer_rapport_competences(
                    competences_globales,
                    stats_domaines,
                    fichiers_a_traiter,
                    resultats,
                    multi_fichiers,
                    args.local,
                    args.model
                )

                total_comp = sum(len(comps) for comps in competences_globales.values())
                txt_comp_size = os.path.getsize(txt_comp_filename) if os.path.exists(txt_comp_filename) else 0
                print(f"✅ Fichier consolidé créé: {txt_comp_filename}")
                print(f"   └─ {len(competences_globales)} domaines, {total_comp} compétences uniques")
                print(f"   └─ Taille: {txt_comp_size:,} octets ({txt_comp_size/1024:.2f} KB)\n")

                fichiers_generes.append({
                    'nom': txt_comp_filename,
                    'type': 'TXT',
                    'description': f'Compétences consolidées ({len(competences_globales)} domaines)',
                    'taille': txt_comp_size,
                    'chemin': os.path.abspath(txt_comp_filename)
                })

        # Affichage rapport final
        afficher_rapport_final(
            temps_debut,
            resultats,
            conversations_splittees_info,
            fichiers_generes,
            OUTPUT_FILE,
            total_sujets,
            len(sujets_par_domaine)
        )

    except Exception as e:
        print(f"❌ Erreur fatale: {str(e)}")
        ecrire_log(f"Erreur fatale: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Correction V2.7.5 : La relance automatique robuste

    # 1. Obtenir le chemin absolu du venv
    venv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ENV_DIR)

    # 2. Vérifier si on est déjà dans l'environnement virtuel (le chemin de l'exécutable)
    # On utilise sys.prefix ou sys.base_prefix pour déterminer si on est dans un venv
    is_in_venv = hasattr(sys, 'real_prefix') or (sys.prefix != sys.base_prefix) or (venv_path in sys.executable)

    # 3. Conditions de relance :
    should_relaunch = (
        os.path.exists(venv_path) and         # Le venv doit exister
        not is_in_venv and                    # On ne doit pas être déjà dedans
        '--install' not in sys.argv and       # Ne pas relancer pendant l'installation
        '--help' not in sys.argv and          # Ne pas relancer pour l'aide
        len(sys.argv) > 1                     # Un argument doit être présent (--prerequis, --exec, etc.)
    )

    if should_relaunch:
        python_path = os.path.join(venv_path, "bin", "python3")

        if os.path.exists(python_path):
            ecrire_log(f"Relance automatique du script dans le venv: {python_path}", "DEBUG")
            try:
                # Utiliser os.execv pour remplacer le processus actuel par le nouveau
                os.execv(python_path, [python_path] + sys.argv)
            except Exception as e:
                print(f"⚠️ Avertissement: Échec de la relance automatique dans le venv ({python_path}).")
                print(f"   Erreur système: {e}")
                print("   Exécution dans l'environnement actuel (peut échouer si dépendances manquantes)...")
                ecrire_log(f"Échec relance: {e}", "ERROR")

    # Exécuter la fonction principale
    main()
