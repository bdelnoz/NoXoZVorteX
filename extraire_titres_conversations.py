#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nom du script: /mnt/data1_100g/home/nox/Documents/ai_export/AI_exportation_ZIP/extraire_titres_conversations.py
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v3.2
Date: 2025-10-21
Target usage: Extraire les titres non vides des fichiers JSON de conversations, avec options de filtrage, exclusion, fusion, simulation et liste de fichiers.
Changelog:
  - v1.0 (2025-10-17) : Création du script. Extraction des titres non vides pour tous les fichiers JSON de conversations dans le répertoire courant.
  - v1.1 (2025-10-17) : Retour à la version initiale sans l'option --list.
  - v1.2 (2025-10-17) : Ajout de l'option --filter (-F) pour filtrer les fichiers JSON par chaîne de caractères dans leur nom.
  - v1.3 (2025-10-18) : Inversion de la valeur par défaut de --simulate (maintenant False).
  - v1.4 (2025-10-18) : Ajout d'un --help explicite et affichage automatique si aucune option n'est spécifiée.
  - v1.5 (2025-10-18) : Message de succès pour --prerequis si tout est en ordre.
  - v1.6 (2025-10-18) : Ajout d'un système de log avec rotation à 2 Mo.
  - v1.7 (2025-10-18) : Help complet avec explications et exemples détaillés pour chaque argument.
  - v1.8 (2025-10-18) : Ajout de l'option --merge pour fusionner tous les titres dans un seul fichier TXT, avec numérotation globale.
  - v1.9 (2025-10-18) : Ajout d'un filtre pour exclure les titres contenant une chaîne spécifique (option --exclude/-E).
  - v1.10 (2025-10-18) : Ajout des options courtes (-e, -s, -p, -f, -m, -E, -h) pour toutes les commandes.
  - v1.11 (2025-10-18) : Correction de l'affichage du help par défaut et suppression de la valeur par défaut pour --exclude.
  - v2.0 (2025-10-21) : Refonte complète selon V101 : en-tête, arguments obligatoires, mode simulation, logs, changelog intégré, gestion des prérequis, installation, et affichage post-exécution.
  - v3.0 (2025-10-21) : Ajout de l'option --files pour traiter une liste de fichiers JSON passés en argument.
  - v3.1 (2025-10-21) : Correction : affichage automatique du help si aucun argument n'est passé.
  - v3.2 (2025-10-21) : Correction : gestion robuste des fichiers JSON mal formatés ou sans structure attendue.
"""
import json
import os
import argparse
import sys
import subprocess
from datetime import datetime

__author__ = "Bruno DELNOZ"
__email__ = "bruno.delnoz@protonmail.com"
__version__ = "v3.2"
__date__ = "2025-10-21"
__script_path__ = "/mnt/data1_100g/home/nox/Documents/ai_export/AI_exportation_ZIP/extraire_titres_conversations.py"

# Constantes globales
LOG_FILE = f"log.extraire_titres_conversations.{__version__}.log"
MAX_LOG_SIZE = 2 * 1024 * 1024  # 2 Mo
MERGE_FILE = f"titres_fusionnes.extraire_titres_conversations.{__version__}.txt"

def ecrire_log(message, niveau="INFO"):
    """
    Écrit un message dans le fichier de log avec rotation si le fichier dépasse 2 Mo.
    Le fichier de log porte le même nom que le script avec l'extension .log.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{niveau}] {message}\n"
    # Rotation du log si nécessaire
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) >= MAX_LOG_SIZE:
        backup_file = f"{LOG_FILE}.old"
        if os.path.exists(backup_file):
            os.remove(backup_file)
        os.rename(LOG_FILE, backup_file)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message)

def afficher_aide():
    """
    Affiche l'aide détaillée du script, incluant la description de chaque option
    et des exemples d'utilisation concrets.
    """
    aide = f"""
{__doc__}

=== Détail des options ===
  --help (-h)          : Affiche cette aide et quitte.
  --exec (-e)          : Exécute le script principal.
  --prerequis (-pr)    : Vérifie les prérequis (version Python, droits d'accès).
  --install (-i)       : Installe les prérequis manquants.
  --simulate (-s)      : Active le mode simulation (dry-run).
  --changelog (-ch)    : Affiche le changelog complet du script.
  --filter (-f)        : Filtre les fichiers JSON par chaîne de caractères dans leur nom.
  --merge (-m)         : Fusionne tous les titres dans un seul fichier TXT : {MERGE_FILE}
  --exclude (-E)       : Chaîne à exclure des titres (aucune par défaut).
  --dir (-d)           : Répertoire contenant les fichiers JSON (défaut: répertoire courant).
  --files              : Liste de fichiers JSON à traiter (prioritaire sur --dir et --filter).

=== Exemples complets ===
  1. Vérifier les prérequis :
     python3 {os.path.basename(__file__)} --prerequis
  2. Extraire les titres de tous les fichiers JSON dans un répertoire :
     python3 {os.path.basename(__file__)} --exec --dir ./extraction_json
  3. Extraire les titres en mode simulation :
     python3 {os.path.basename(__file__)} --exec --simulate --dir ./extraction_json
  4. Extraire les titres des fichiers contenant "chat" :
     python3 {os.path.basename(__file__)} --exec --dir ./extraction_json --filter chat
  5. Fusionner tous les titres dans un seul fichier TXT :
     python3 {os.path.basename(__file__)} --exec --dir ./extraction_json --merge
  6. Exclure les titres contenant "Saik0s/Whisperboard:" :
     python3 {os.path.basename(__file__)} --exec --dir ./extraction_json --exclude "Saik0s/Whisperboard:"
  7. Traiter une liste de fichiers spécifiques :
     python3 {os.path.basename(__file__)} --exec --files ./extraction_json/*.json
  8. Fusionner et exclure en une seule commande :
     python3 {os.path.basename(__file__)} --exec --dir ./extraction_json --merge --exclude "Saik0s/Whisperboard:"
"""
    print(aide)

def afficher_changelog():
    """
    Affiche le changelog complet du script.
    """
    print(__doc__.split("Changelog:")[1].strip())

def verifier_prerequis():
    """
    Vérifie que Python 3.8+ est installé et que les droits de lecture/écriture
    sont disponibles dans le répertoire courant.
    """
    if sys.version_info < (3, 8):
        msg = "Erreur : Python 3.8 ou supérieur requis."
        print(msg)
        ecrire_log(msg, "ERREUR")
        sys.exit(1)
    if not os.access('.', os.R_OK | os.W_OK):
        msg = "Erreur : Droits de lecture/écriture manquants dans le répertoire courant."
        print(msg)
        ecrire_log(msg, "ERREUR")
        sys.exit(1)
    msg = "Prérequis vérifiés : OK (Python 3.8+, droits de lecture/écriture)."
    print(msg)
    ecrire_log(msg)

def installer_prerequis():
    """
    Installe les prérequis manquants (exemple : pip install -r requirements.txt).
    """
    try:
        subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
        msg = "Prérequis installés avec succès."
        print(msg)
        ecrire_log(msg)
    except subprocess.CalledProcessError as e:
        msg = f"Erreur lors de l'installation des prérequis : {e}"
        print(msg)
        ecrire_log(msg, "ERREUR")
        sys.exit(1)

def traiter_fichier_json(fichier, simulate=False, merge=False, exclude=None):
    """
    Traite un fichier JSON : extrait les titres non vides, en excluant ceux qui contiennent 'exclude'.
    Si merge=True, retourne la liste des titres au lieu d'écrire un fichier.
    Gère les fichiers mal formatés ou sans structure attendue.
    """
    try:
        with open(fichier, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        msg = f"Erreur : {fichier} n'est pas un JSON valide."
        print(msg)
        ecrire_log(msg, "ERREUR")
        return []
    except Exception as e:
        msg = f"Erreur lors de la lecture de {fichier} : {e}"
        print(msg)
        ecrire_log(msg, "ERREUR")
        return []

    titres_non_vides = []
    for conv in data:
        # Vérifie que conv est un dictionnaire et contient une clé 'title'
        if isinstance(conv, dict) and 'title' in conv:
            title = conv['title']
            if title and (exclude is None or exclude not in title):
                titres_non_vides.append(title)

    if merge:
        return titres_non_vides

    # Mode classique : écriture d'un fichier par JSON
    if not simulate:
        nom_sortie = f"titres_{os.path.splitext(os.path.basename(fichier))[0]}.extraire_titres_conversations.{__version__}.txt"
        with open(nom_sortie, 'w', encoding='utf-8') as f:
            for i, titre in enumerate(titres_non_vides, 1):
                f.write(f"{i}. {titre}\n")
        if exclude:
            msg = f"Fichier généré : {nom_sortie} ({len(titres_non_vides)} titres non vides, après exclusion de '{exclude}')"
        else:
            msg = f"Fichier généré : {nom_sortie} ({len(titres_non_vides)} titres non vides)"
        print(msg)
        ecrire_log(msg)
    else:
        if exclude:
            msg = f"[SIMULATION] {fichier} : {len(titres_non_vides)} titres non vides seraient extraits (après exclusion de '{exclude}')."
        else:
            msg = f"[SIMULATION] {fichier} : {len(titres_non_vides)} titres non vides seraient extraits."
        print(msg)
        ecrire_log(msg)
    return titres_non_vides

def fusionner_titres(titres_par_fichier, exclude=None):
    """
    Fusionne tous les titres extraits dans un seul fichier TXT,
    avec une numérotation globale et une séparation par fichier d'origine.
    Exclut les titres contenant 'exclude' (si exclude est fourni).
    """
    with open(MERGE_FILE, 'w', encoding='utf-8') as f:
        num_global = 1
        for fichier, titres in titres_par_fichier.items():
            f.write(f"\n=== Titres extraits de : {os.path.basename(fichier)} ===\n\n")
            for titre in titres:
                f.write(f"{num_global}. {titre}\n")
                num_global += 1
    if exclude:
        msg = f"Fichier fusionné généré : {MERGE_FILE} ({num_global-1} titres au total, après exclusion de '{exclude}')"
    else:
        msg = f"Fichier fusionné généré : {MERGE_FILE} ({num_global-1} titres au total)"
    print(msg)
    ecrire_log(msg)

def afficher_actions_executees(titres_par_fichier, simulate, merge, exclude):
    """
    Affiche une liste numérotée de toutes les actions faites dans l’exécution.
    """
    print("\n=== Actions exécutées ===")
    i = 1
    for fichier, titres in titres_par_fichier.items():
        if merge:
            print(f"{i}. [FUSION] {len(titres)} titres extraits de {os.path.basename(fichier)} {'(après exclusion)' if exclude else ''}")
        else:
            nom_sortie = f"titres_{os.path.splitext(os.path.basename(fichier))[0]}.extraire_titres_conversations.{__version__}.txt"
            print(f"{i}. {'[SIMULATION] ' if simulate else ''}Extraction de {len(titres)} titres depuis {os.path.basename(fichier)} {'(après exclusion)' if exclude else ''}")
            if not simulate:
                print(f"   -> Fichier généré : {nom_sortie}")
        i += 1
    if merge and titres_par_fichier:
        print(f"{i}. Fichier fusionné généré : {MERGE_FILE}")

def main():
    """
    Point d'entrée du script : parse les arguments et lance le traitement.
    """
    parser = argparse.ArgumentParser(description="Extraire les titres non vides des fichiers JSON de conversations.", add_help=False)
    parser.add_argument('--help', '-h', action='store_true', help="Affiche cette aide.")
    parser.add_argument('--exec', '-e', action='store_true', help="Exécute le script principal.")
    parser.add_argument('--prerequis', '-pr', action='store_true', help="Vérifie les prérequis.")
    parser.add_argument('--install', '-i', action='store_true', help="Installe les prérequis manquants.")
    parser.add_argument('--simulate', '-s', action='store_true', help="Active le mode simulation (dry-run).")
    parser.add_argument('--changelog', '-ch', action='store_true', help="Affiche le changelog complet du script.")
    parser.add_argument('--filter', '-f', type=str, default='', help="Filtre les fichiers JSON par chaîne de caractères dans leur nom.")
    parser.add_argument('--merge', '-m', action='store_true', help="Fusionne tous les titres dans un seul fichier TXT.")
    parser.add_argument('--exclude', '-E', type=str, default=None, help="Chaîne à exclure des titres.")
    parser.add_argument('--dir', '-d', type=str, default='.', help="Répertoire contenant les fichiers JSON (défaut: répertoire courant).")
    parser.add_argument('--files', nargs='+', default=[], help="Liste de fichiers JSON à traiter.")

    args = parser.parse_args()

    # Affichage automatique du help si AUCUN argument n'est passé
    if len(sys.argv) == 1:
        afficher_aide()
        return

    if args.help:
        afficher_aide()
        return

    if args.changelog:
        afficher_changelog()
        return

    if args.prerequis:
        verifier_prerequis()
        return

    if args.install:
        installer_prerequis()
        return

    if args.exec:
        verifier_prerequis()
        titres_par_fichier = {}

        # Si --files est utilisé, on traite uniquement ces fichiers
        if args.files:
            fichiers_a_traiter = args.files
        else:
            fichiers_a_traiter = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if f.endswith('.json') and args.filter.lower() in f.lower()]

        if not fichiers_a_traiter:
            msg = f"Aucun fichier JSON trouvé {'avec le filtre \'{args.filter}\'' if args.filter else ''} dans {args.dir}."
            print(msg)
            ecrire_log(msg, "ERREUR")
            return

        for fichier in fichiers_a_traiter:
            if not fichier.endswith('.json'):
                continue
            titres = traiter_fichier_json(fichier, simulate=args.simulate, merge=args.merge, exclude=args.exclude)
            if titres:
                titres_par_fichier[fichier] = titres

        if args.merge:
            fusionner_titres(titres_par_fichier, exclude=args.exclude)
        afficher_actions_executees(titres_par_fichier, args.simulate, args.merge, args.exclude)

if __name__ == "__main__":
    main()
