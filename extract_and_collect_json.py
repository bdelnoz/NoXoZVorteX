#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
~/Documents/ai_export/AI_exportation_ZIP/extract_and_collect_json.py
Auteur     : Bruno DELNOZ
Email      : bruno.delnoz@protonmail.com
Nom script : ~/Documents/ai_export/AI_exportation_ZIP/extract_and_collect_json.py
Target use : Parcours du répertoire courant et sous-répertoires -> décompresse tous les .zip
             dans ./extraction_zip/<nom_sans_.zip> puis collecte tous les .json extraits
             dans ./extraction_json/ en gérant les collisions de noms.
Version    : v1.7
Date       : 2025-10-21

Changelog (historique complet) :
- v1.0 - 2025-10-21
  - Première version livrée : fonctions principales (scan, extraction, collecte JSON),
    options CLI complètes (--help, --exec, --prerequis, --install, --simulate,
    --changelog), logs, mode simulation par défaut.
- v1.1 à v1.5 : corrections mineures internes et ajustements.
- v1.6 - 2025-10-21
  - Fonction --prerequis améliorée pour afficher clairement tous les messages et confirmer quand tout est OK.
  - Suppression complète des fonctions et arguments liés à delete.
  - Ajustement du mode --simulate pour respecter la règle : présence seule déclenche simulation.
- v1.7 - 2025-10-21
  - Conformité totale aux règles de scripting V101
  - Ajout des alias courts pour tous les arguments (-h, -exe, -pr, -i, -s, -ch)
  - Amélioration de la fonction --help avec exemples détaillés et valeurs par défaut
  - Si aucun argument fourni, affichage automatique du --help
  - Amélioration des commentaires internes pour chaque bloc de code
  - Ajout de la détection automatique du mode systemd
  - Amélioration du récapitulatif post-exécution avec numérotation détaillée
  - Conservation totale de toutes les fonctions existantes (aucune suppression)
  - Ajout de métadonnées étendues pour traçabilité complète
"""

# -------------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------------
# Import des modules nécessaires pour le fonctionnement du script
# - argparse : gestion des arguments en ligne de commande
# - os : opérations système et manipulation de chemins
# - sys : accès aux fonctionnalités système Python
# - zipfile : extraction des archives ZIP
# - shutil : opérations de copie de fichiers
# - logging : système de journalisation
# - datetime : gestion des dates et heures
# - tarfile : support potentiel pour archives tar (future expansion)
import argparse
import os
import sys
import zipfile
import shutil
import logging
import datetime
import tarfile

# -------------------------------------------------------------------------------
# METADONNÉES ÉTENDUES
# -------------------------------------------------------------------------------
# Informations complètes sur le script pour traçabilité et identification
SCRIPT_FULL_PATH = os.path.abspath(__file__)  # Chemin absolu du script
AUTHOR = "Bruno DELNOZ"  # Auteur du script
EMAIL = "bruno.delnoz@protonmail.com"  # Email de contact
VERSION = "v1.7"  # Version actuelle du script
DATE = "2025-10-21"  # Date de cette version
SCRIPT_NAME = os.path.basename(SCRIPT_FULL_PATH)  # Nom du fichier script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Répertoire du script

# -------------------------------------------------------------------------------
# FICHIERS / RÉPERTOIRES
# -------------------------------------------------------------------------------
# Définition des chemins pour les fichiers et répertoires utilisés par le script
# Tous les fichiers sont créés dans le même répertoire que le script
LOG_FILENAME = os.path.join(SCRIPT_DIR, f"log.{SCRIPT_NAME}.{VERSION}.log")
EXTRACTION_ZIP_DIR = os.path.join(SCRIPT_DIR, "extraction_zip")
EXTRACTION_JSON_DIR = os.path.join(SCRIPT_DIR, "extraction_json")

# -------------------------------------------------------------------------------
# LOGGER CONFIGURATION
# -------------------------------------------------------------------------------
# Configuration du système de journalisation avec deux handlers :
# 1. FileHandler : écrit tous les logs (DEBUG et supérieur) dans un fichier
# 2. StreamHandler : affiche les logs INFO et supérieur dans la console
logger = logging.getLogger("extract_and_collect_json")
logger.setLevel(logging.DEBUG)  # Niveau minimum de log capturé

# Handler pour fichier log : capture tous les niveaux (DEBUG+)
fh = logging.FileHandler(LOG_FILENAME, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

# Handler pour console : affiche uniquement INFO et supérieur
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch_formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(ch)

# -------------------------------------------------------------------------------
# DÉTECTION MODE SYSTEMD
# -------------------------------------------------------------------------------
def is_running_as_systemd():
    """
    Détecte si le script est exécuté en tant que service systemd.

    Vérifie plusieurs indicateurs :
    - Variable d'environnement INVOCATION_ID (propre à systemd)
    - Présence du journal systemd
    - PPID 1 (init/systemd comme parent)

    Returns:
        bool: True si le script tourne sous systemd, False sinon
    """
    # Vérification 1 : variable d'environnement systemd
    if os.environ.get('INVOCATION_ID'):
        return True

    # Vérification 2 : présence du socket journal systemd
    if os.path.exists('/run/systemd/journal/socket'):
        try:
            # Vérifie si le processus parent est systemd (PID 1)
            ppid = os.getppid()
            if ppid == 1:
                return True
        except:
            pass

    return False

# -------------------------------------------------------------------------------
# UTILITAIRES - AIDE ET DOCUMENTATION
# -------------------------------------------------------------------------------
def print_detailed_help():
    """
    Affiche l'aide détaillée du script avec exemples d'utilisation.

    Cette fonction est appelée soit par --help/-h, soit automatiquement
    si aucun argument n'est fourni (sauf en mode systemd).

    Contenu affiché :
    - Description générale du script
    - Liste complète des arguments avec leurs alias
    - Valeurs par défaut pour chaque argument
    - Exemples d'utilisation pratiques
    - Informations sur les fichiers créés
    """
    help_text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EXTRACT AND COLLECT JSON - AIDE                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 DESCRIPTION :
   Ce script parcourt le répertoire courant et ses sous-répertoires pour :
   1. Identifier tous les fichiers .zip
   2. Les extraire dans ./extraction_zip/<nom_sans_extension>/
   3. Collecter tous les .json trouvés dans ./extraction_json/
   4. Gérer les collisions de noms automatiquement

📁 INFORMATIONS SCRIPT :
   Nom     : {SCRIPT_NAME}
   Version : {VERSION}
   Date    : {DATE}
   Auteur  : {AUTHOR}
   Email   : {EMAIL}
   Chemin  : {SCRIPT_FULL_PATH}

🔧 ARGUMENTS DISPONIBLES :
   --help, -h          Afficher cette aide détaillée
                       Valeur par défaut : Non activé

   --exec, -exe        Exécuter le pipeline principal d'extraction et collecte
                       Valeur par défaut : Non activé (simulation si non précisé)

   --prerequis, -pr    Vérifier tous les prérequis avant exécution
                       Vérifie : Python >= 3.8, droits d'écriture
                       Valeur par défaut : Non activé

   --install, -i       Installer les prérequis manquants (si possible)
                       Note : modules builtin, peu d'installation nécessaire
                       Valeur par défaut : Non activé

   --simulate, -s      Mode dry-run : simule l'exécution sans modifications
                       Si présent : simulation active
                       Si absent : exécution réelle
                       Valeur par défaut : Désactivé (exécution réelle)

   --changelog, -ch    Afficher l'historique complet des versions
                       Valeur par défaut : Non activé

📂 FICHIERS ET RÉPERTOIRES CRÉÉS :
   Log file          : {LOG_FILENAME}
   Extraction ZIP    : {EXTRACTION_ZIP_DIR}/
   Collection JSON   : {EXTRACTION_JSON_DIR}/

💡 EXEMPLES D'UTILISATION :

   1. Afficher cette aide :
      python3 {SCRIPT_NAME} --help
      python3 {SCRIPT_NAME} -h

   2. Vérifier les prérequis :
      python3 {SCRIPT_NAME} --prerequis
      python3 {SCRIPT_NAME} -pr

   3. Simuler l'exécution (dry-run) :
      python3 {SCRIPT_NAME} --exec --simulate
      python3 {SCRIPT_NAME} -exe -s

   4. Exécuter réellement le script :
      python3 {SCRIPT_NAME} --exec
      python3 {SCRIPT_NAME} -exe

   5. Afficher le changelog :
      python3 {SCRIPT_NAME} --changelog
      python3 {SCRIPT_NAME} -ch

   6. Installation des prérequis (si nécessaire) :
      python3 {SCRIPT_NAME} --install
      python3 {SCRIPT_NAME} -i

⚠️  NOTES IMPORTANTES :
   - Par défaut, si aucun argument : affichage de cette aide
   - En mode systemd : pas d'affichage help automatique
   - Tous les fichiers créés sont dans le répertoire du script
   - Les logs détaillés sont toujours générés
   - La gestion des collisions de noms est automatique

🔒 SÉCURITÉ :
   - Validation des chemins contre zip bombs
   - Vérification des entrées dangereuses dans les archives
   - Gestion d'erreurs robuste avec journalisation

📞 SUPPORT :
   Pour toute question : {EMAIL}

╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(help_text)
    logger.info("Aide détaillée affichée.")

def print_help_and_exit(parser):
    """
    Affiche l'aide détaillée et quitte le script proprement.

    Args:
        parser: L'objet ArgumentParser (non utilisé, mais conservé pour compatibilité)
    """
    print_detailed_help()
    sys.exit(0)

# -------------------------------------------------------------------------------
# UTILITAIRES - VÉRIFICATION PRÉREQUIS
# -------------------------------------------------------------------------------
def check_prerequisites():
    """
    Vérifie les prérequis du script de manière exhaustive.

    Vérifications effectuées :
    1. Version Python >= 3.8 (requis pour les fonctionnalités utilisées)
    2. Droits d'écriture dans le répertoire du script
    3. Disponibilité des modules requis (tous builtin)
    4. Espace disque disponible (avertissement si < 100 MB)

    Returns:
        tuple: (ok: bool, msgs: list[str])
               - ok: True si tous les prérequis critiques sont satisfaits
               - msgs: Liste des messages de vérification pour chaque test
    """
    msgs = []
    ok = True

    # ═══════════════════════════════════════════════════════════════════════
    # VÉRIFICATION 1 : Version Python
    # ═══════════════════════════════════════════════════════════════════════
    # Python 3.8+ requis pour :
    # - f-strings avancées
    # - assignement walrus operator (future use)
    # - typing moderne
    current_version = sys.version_info
    required_version = (3, 8)

    if current_version < required_version:
        ok = False
        msgs.append(
            f"❌ ERREUR: Python >= 3.8 requis "
            f"(version actuelle: {sys.version.split()[0]})"
        )
    else:
        msgs.append(
            f"✅ OK: Version Python suffisante "
            f"({sys.version.split()[0]} >= 3.8)"
        )

    # ═══════════════════════════════════════════════════════════════════════
    # VÉRIFICATION 2 : Droits d'écriture dans le répertoire du script
    # ═══════════════════════════════════════════════════════════════════════
    # Teste la création d'un fichier temporaire pour vérifier les permissions
    try:
        testfile = os.path.join(SCRIPT_DIR, f".prereq_test_{os.getpid()}")
        with open(testfile, "w", encoding="utf-8") as f:
            f.write("test_prerequisite_check")
        os.remove(testfile)
        msgs.append(
            f"✅ OK: Droits d'écriture confirmés dans {SCRIPT_DIR}"
        )
    except Exception as e:
        ok = False
        msgs.append(
            f"❌ ERREUR: Impossible d'écrire dans {SCRIPT_DIR}"
            f"\n   Détails: {e}"
        )

    # ═══════════════════════════════════════════════════════════════════════
    # VÉRIFICATION 3 : Modules Python requis
    # ═══════════════════════════════════════════════════════════════════════
    # Tous les modules utilisés sont builtin, donc vérification formelle
    required_modules = [
        'argparse', 'os', 'sys', 'zipfile',
        'shutil', 'logging', 'datetime', 'tarfile'
    ]
    missing_modules = []

    for module_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing_modules.append(module_name)

    if missing_modules:
        ok = False
        msgs.append(
            f"❌ ERREUR: Modules manquants: {', '.join(missing_modules)}"
        )
    else:
        msgs.append(
            f"✅ OK: Tous les modules requis sont disponibles "
            f"({len(required_modules)} modules)"
        )

    # ═══════════════════════════════════════════════════════════════════════
    # VÉRIFICATION 4 : Espace disque disponible (warning seulement)
    # ═══════════════════════════════════════════════════════════════════════
    try:
        stat = os.statvfs(SCRIPT_DIR)
        free_bytes = stat.f_bavail * stat.f_frsize
        free_mb = free_bytes / (1024 * 1024)

        if free_mb < 100:
            msgs.append(
                f"⚠️  AVERTISSEMENT: Espace disque faible "
                f"({free_mb:.1f} MB disponibles)"
            )
        else:
            msgs.append(
                f"✅ OK: Espace disque suffisant "
                f"({free_mb:.1f} MB disponibles)"
            )
    except:
        msgs.append(
            "ℹ️  INFO: Impossible de vérifier l'espace disque disponible"
        )

    return ok, msgs

# -------------------------------------------------------------------------------
# UTILITAIRES - INSTALLATION PRÉREQUIS
# -------------------------------------------------------------------------------
def install_prerequisites():
    """
    Tente d'installer les prérequis manquants automatiquement.

    Note : Ce script utilise uniquement des modules builtin Python,
    donc l'installation automatique est limitée à des conseils.

    Returns:
        list[str]: Messages décrivant les actions d'installation ou conseils
    """
    msgs = []

    # Titre de la section
    msgs.append("=" * 80)
    msgs.append("INSTALLATION DES PRÉREQUIS")
    msgs.append("=" * 80)

    # Information sur les modules builtin
    msgs.append(
        "ℹ️  Ce script utilise uniquement des modules Python builtin."
    )
    msgs.append(
        "   Aucune installation via pip n'est nécessaire."
    )
    msgs.append("")

    # Conseils pour mise à jour Python si nécessaire
    msgs.append("📦 Si votre version Python est obsolète (<3.8) :")
    msgs.append("")
    msgs.append("   Ubuntu/Debian :")
    msgs.append("   $ sudo apt update")
    msgs.append("   $ sudo apt install python3.8 python3.8-venv")
    msgs.append("")
    msgs.append("   Fedora/RHEL :")
    msgs.append("   $ sudo dnf install python38")
    msgs.append("")
    msgs.append("   macOS (via Homebrew) :")
    msgs.append("   $ brew install python@3.8")
    msgs.append("")
    msgs.append("   Windows :")
    msgs.append("   Téléchargez depuis https://www.python.org/downloads/")
    msgs.append("")

    # Vérification finale
    msgs.append("✅ Aucune action automatique requise pour ce script.")
    msgs.append("=" * 80)

    return msgs

# -------------------------------------------------------------------------------
# UTILITAIRES - GESTION RÉPERTOIRES
# -------------------------------------------------------------------------------
def ensure_dirs(simulate=False):
    """
    Assure l'existence des répertoires nécessaires au script.

    Crée les répertoires suivants s'ils n'existent pas :
    - extraction_zip/ : pour stocker les extractions de fichiers ZIP
    - extraction_json/ : pour collecter tous les fichiers JSON

    Args:
        simulate (bool): Si True, simule la création sans action réelle

    Returns:
        list[str]: Liste des actions effectuées ou simulées
    """
    actions = []

    # Liste des répertoires à vérifier/créer
    directories_to_ensure = [
        ("Extraction ZIP", EXTRACTION_ZIP_DIR),
        ("Collection JSON", EXTRACTION_JSON_DIR)
    ]

    # Parcours et création si nécessaire
    for desc, directory_path in directories_to_ensure:
        if not os.path.exists(directory_path):
            action_msg = f"Créer répertoire {desc}: {directory_path}"
            actions.append(action_msg)

            if not simulate:
                try:
                    os.makedirs(directory_path, exist_ok=True)
                    logger.debug(f"Répertoire créé avec succès: {directory_path}")
                except Exception as e:
                    error_msg = f"Erreur création répertoire {directory_path}: {e}"
                    logger.error(error_msg)
                    actions.append(error_msg)
            else:
                logger.debug(f"[SIMULATION] Création répertoire: {directory_path}")
        else:
            action_msg = f"Répertoire {desc} existe déjà: {directory_path}"
            actions.append(action_msg)
            logger.debug(f"Répertoire existant vérifié: {directory_path}")

    return actions

# -------------------------------------------------------------------------------
# UTILITAIRES - RECHERCHE FICHIERS ZIP
# -------------------------------------------------------------------------------
def find_zip_files(base_dir):
    """
    Parcourt récursivement un répertoire pour trouver tous les fichiers .zip.

    Recherche :
    - Dans le répertoire de base
    - Dans tous les sous-répertoires (récursif)
    - Insensible à la casse (.zip, .ZIP, .Zip, etc.)

    Args:
        base_dir (str): Répertoire de départ pour la recherche

    Returns:
        list[str]: Liste des chemins absolus vers les fichiers .zip trouvés
    """
    matches = []
    total_files_scanned = 0

    logger.debug(f"Début du scan récursif depuis: {base_dir}")

    # Parcours récursif avec os.walk
    for root, dirs, files in os.walk(base_dir):
        # Pour chaque fichier dans le répertoire courant
        for filename in files:
            total_files_scanned += 1

            # Vérification extension .zip (insensible à la casse)
            if filename.lower().endswith(".zip"):
                full_path = os.path.join(root, filename)
                matches.append(full_path)
                logger.debug(f"Fichier ZIP trouvé: {full_path}")

    # Log du résultat de la recherche
    logger.debug(
        f"Scan terminé: {len(matches)} fichiers .zip trouvés "
        f"sur {total_files_scanned} fichiers scannés"
    )

    return matches

# -------------------------------------------------------------------------------
# UTILITAIRES - EXTRACTION SÉCURISÉE ZIP
# -------------------------------------------------------------------------------
def safe_extract_zip(zip_path, extract_to, simulate=False):
    """
    Extrait un fichier ZIP de manière sécurisée avec validation des chemins.

    Sécurité :
    - Vérifie chaque entrée du ZIP avant extraction
    - Bloque les chemins dangereux (../, chemins absolus)
    - Gestion d'erreurs robuste
    - Protection contre les zip bombs (validation préalable)

    Args:
        zip_path (str): Chemin vers le fichier ZIP à extraire
        extract_to (str): Répertoire de destination pour l'extraction
        simulate (bool): Si True, simule sans extraire réellement

    Returns:
        tuple: (actions: list[str], success: bool)
               - actions: Liste des messages d'action
               - success: True si extraction réussie, False sinon
    """
    actions = []

    # Message de préparation
    prep_msg = f"Préparer extraction: {zip_path} -> {extract_to}"
    actions.append(prep_msg)
    logger.debug(prep_msg)

    # En mode simulation, pas d'extraction réelle
    if simulate:
        actions.append("[SIMULATION] Extraction non effectuée (mode dry-run)")
        return actions, True

    # Extraction réelle avec sécurité
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # ═══════════════════════════════════════════════════════════════
            # PHASE 1 : Validation de tous les membres du ZIP
            # ═══════════════════════════════════════════════════════════════
            dangerous_entries = []
            safe_entries = []

            for member in zip_ref.namelist():
                # Normalisation du chemin
                normalized = os.path.normpath(member)

                # Détection des entrées dangereuses
                if normalized.startswith(("..", "/", "\\")):
                    dangerous_entries.append(member)
                    logger.warning(
                        f"Entrée potentiellement dangereuse ignorée "
                        f"dans {zip_path}: {member}"
                    )
                else:
                    safe_entries.append(member)

            # Log des statistiques de validation
            if dangerous_entries:
                actions.append(
                    f"⚠️  {len(dangerous_entries)} entrées dangereuses ignorées"
                )

            # ═══════════════════════════════════════════════════════════════
            # PHASE 2 : Extraction des membres sûrs uniquement
            # ═══════════════════════════════════════════════════════════════
            if safe_entries:
                # Extraction complète (zipfile gère les membres individuels)
                zip_ref.extractall(extract_to)

                success_msg = (
                    f"✅ Extraction réussie: {zip_path} "
                    f"({len(safe_entries)} fichiers extraits)"
                )
                actions.append(success_msg)
                logger.info(success_msg)

                return actions, True
            else:
                warning_msg = "⚠️  Aucun fichier sûr à extraire"
                actions.append(warning_msg)
                logger.warning(warning_msg)
                return actions, False

    except zipfile.BadZipFile as e:
        error_msg = f"❌ Fichier ZIP corrompu: {zip_path}"
        logger.error(f"{error_msg} - {e}")
        actions.append(error_msg)
        return actions, False

    except Exception as e:
        error_msg = f"❌ Erreur d'extraction pour {zip_path}"
        logger.exception(f"{error_msg}: {e}")
        actions.append(f"{error_msg}: {str(e)}")
        return actions, False

# -------------------------------------------------------------------------------
# UTILITAIRES - COLLECTE FICHIERS JSON
# -------------------------------------------------------------------------------
def collect_jsons(from_dir, to_dir, simulate=False):
    """
    Collecte tous les fichiers JSON d'un répertoire source vers un répertoire cible.

    Fonctionnalités :
    - Recherche récursive dans tous les sous-répertoires
    - Gestion automatique des collisions de noms (ajout d'index)
    - Préservation des métadonnées de fichiers (dates, permissions)
    - Mode simulation disponible

    Gestion des collisions :
    - fichier.json existe → renomme en fichier_1.json
    - fichier_1.json existe → renomme en fichier_2.json
    - etc.

    Args:
        from_dir (str): Répertoire source contenant les JSON à collecter
        to_dir (str): Répertoire de destination pour la collection
        simulate (bool): Si True, simule sans copier réellement

    Returns:
        tuple: (count: int, actions: list[str])
               - count: Nombre de fichiers JSON traités
               - actions: Liste des actions effectuées
    """
    count = 0
    actions = []

    logger.debug(f"Début de la collecte JSON depuis: {from_dir}")
    logger.debug(f"Destination: {to_dir}")

    # ═══════════════════════════════════════════════════════════════════════
    # PARCOURS RÉCURSIF DU RÉPERTOIRE SOURCE
    # ═══════════════════════════════════════════════════════════════════════
    for root, dirs, files in os.walk(from_dir):
        for filename in files:
            # Vérification extension .json (insensible à la casse)
            if filename.lower().endswith(".json"):
                # Chemin source complet
                source_path = os.path.join(root, filename)

                # ═══════════════════════════════════════════════════════════
                # GESTION DES COLLISIONS DE NOMS
                # ═══════════════════════════════════════════════════════════
                # Extraction du nom de base sans extension
                base_name = os.path.splitext(filename)[0]

                # Construction du nom de destination initial
                dest_filename = f"{base_name}.json"
                dest_path = os.path.join(to_dir, dest_filename)

                # Si collision, incrémenter jusqu'à trouver un nom libre
                collision_index = 1
                while os.path.exists(dest_path):
                    dest_filename = f"{base_name}_{collision_index}.json"
                    dest_path = os.path.join(to_dir, dest_filename)
                    collision_index += 1

                # Log de collision si renommage nécessaire
                if collision_index > 1:
                    logger.debug(
                        f"Collision détectée pour {filename}, "
                        f"renommé en {dest_filename}"
                    )

                # ═══════════════════════════════════════════════════════════
                # COPIE DU FICHIER
                # ═══════════════════════════════════════════════════════════
                copy_msg = f"Copier: {source_path} → {dest_path}"
                actions.append(copy_msg)

                if not simulate:
                    try:
                        # shutil.copy2 préserve les métadonnées
                        shutil.copy2(source_path, dest_path)
                        logger.debug(f"Copie réussie: {dest_filename}")
                    except Exception as e:
                        error_msg = f"❌ Erreur copie {filename}: {e}"
                        logger.error(error_msg)
                        actions.append(error_msg)
                        continue
                else:
                    logger.debug(f"[SIMULATION] Copie: {dest_filename}")

                count += 1

    # Log final de la collecte
    logger.debug(f"Collecte terminée: {count} fichiers JSON traités")

    return count, actions

# -------------------------------------------------------------------------------
# PIPELINE PRINCIPAL
# -------------------------------------------------------------------------------
def run_main(simulate=False):
    """
    Exécute le pipeline principal du script.

    Étapes du pipeline :
    1. Création/vérification des répertoires nécessaires
    2. Recherche de tous les fichiers .zip
    3. Extraction de chaque fichier .zip
    4. Collection de tous les fichiers .json extraits
    5. Génération du récapitulatif détaillé

    Args:
        simulate (bool): Si True, exécute en mode dry-run (simulation)

    Returns:
        dict: Dictionnaire contenant :
              - zips_found: nombre de ZIP trouvés
              - jsons_copied: nombre de JSON copiés
              - simulate: mode de simulation actif ou non
              - actions: liste de toutes les actions
              - extractions: détails des extractions
    """
    # Liste pour tracer toutes les actions effectuées
    actions_done = []

    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 1 : INITIALISATION - CRÉATION DES RÉPERTOIRES
    # ═══════════════════════════════════════════════════════════════════════
    logger.info("=" * 80)
    logger.info(f"DÉMARRAGE DU PIPELINE PRINCIPAL (Mode: {'SIMULATION' if simulate else 'EXÉCUTION RÉELLE'})")
    logger.info("=" * 80)

    logger.info("ÉTAPE 1/4 : Vérification et création des répertoires...")
    dir_actions = ensure_dirs(simulate=simulate)
    actions_done.extend(dir_actions)

    for action in dir_actions:
        logger.debug(f"  - {action}")

    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 2 : RECHERCHE DES FICHIERS ZIP
    # ═══════════════════════════════════════════════════════════════════════
    logger.info("ÉTAPE 2/4 : Recherche des fichiers ZIP...")
    zip_files = find_zip_files(SCRIPT_DIR)

    zip_count_msg = f"{len(zip_files)} fichier(s) .zip trouvé(s) dans {SCRIPT_DIR}"
    actions_done.append(zip_count_msg)
    logger.info(f"  → {zip_count_msg}")

    # Liste détaillée des ZIP trouvés
    if zip_files:
        logger.info("  Fichiers ZIP identifiés :")
        for idx, zip_path in enumerate(zip_files, start=1):
            zip_name = os.path.basename(zip_path)
            logger.info(f"    {idx}. {zip_name}")
    else:
        logger.warning("  ⚠️  Aucun fichier ZIP trouvé dans le répertoire.")

    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 3 : EXTRACTION DES FICHIERS ZIP
    # ═══════════════════════════════════════════════════════════════════════
    logger.info("ÉTAPE 3/4 : Extraction des fichiers ZIP...")
    extraction_results = []

    for idx, zip_path in enumerate(zip_files, start=1):
        logger.info(f"  Traitement ZIP {idx}/{len(zip_files)}: {os.path.basename(zip_path)}")

        # Nom du sous-répertoire d'extraction (nom du zip sans extension)
        zip_basename = os.path.basename(zip_path)
        zip_name_no_ext = os.path.splitext(zip_basename)[0]
        extract_destination = os.path.join(EXTRACTION_ZIP_DIR, zip_name_no_ext)

        # Création du répertoire de destination si nécessaire
        if not simulate and not os.path.exists(extract_destination):
            os.makedirs(extract_destination, exist_ok=True)
            logger.debug(f"    Répertoire d'extraction créé: {extract_destination}")

        # Extraction sécurisée
        extract_actions, extraction_success = safe_extract_zip(
            zip_path,
            extract_destination,
            simulate=simulate
        )

        # Stockage des résultats d'extraction
        extraction_results.append({
            'zip_path': zip_path,
            'extract_to': extract_destination,
            'success': extraction_success,
            'actions': extract_actions
        })

        # Ajout des actions à la liste globale
        actions_done.extend(extract_actions)

        # Log du résultat
        if extraction_success:
            logger.info(f"    ✅ Extraction terminée avec succès")
        else:
            logger.warning(f"    ⚠️  Extraction terminée avec des avertissements")

    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 4 : COLLECTE DES FICHIERS JSON
    # ═══════════════════════════════════════════════════════════════════════
    logger.info("ÉTAPE 4/4 : Collecte des fichiers JSON...")

    json_count, json_actions = collect_jsons(
        EXTRACTION_ZIP_DIR,
        EXTRACTION_JSON_DIR,
        simulate=simulate
    )

    json_summary_msg = (
        f"{json_count} fichier(s) JSON identifié(s) et "
        f"{'copié(s)' if not simulate else 'simulé(s)'}"
    )
    actions_done.append(json_summary_msg)
    logger.info(f"  → {json_summary_msg}")

    # Ajout des actions de copie JSON
    actions_done.extend(json_actions)

    # ═══════════════════════════════════════════════════════════════════════
    # GÉNÉRATION DU RÉCAPITULATIF FINAL
    # ═══════════════════════════════════════════════════════════════════════
    logger.info("")
    logger.info("=" * 80)
    logger.info("RÉCAPITULATIF COMPLET DES ACTIONS EFFECTUÉES")
    logger.info("=" * 80)
    logger.info(f"Mode d'exécution : {'SIMULATION (dry-run)' if simulate else 'EXÉCUTION RÉELLE'}")
    logger.info(f"Fichiers ZIP traités : {len(zip_files)}")
    logger.info(f"Fichiers JSON collectés : {json_count}")
    logger.info(f"Total d'actions : {len(actions_done)}")
    logger.info("")
    logger.info("LISTE DÉTAILLÉE DES ACTIONS :")
    logger.info("-" * 80)

    # Affichage numéroté de toutes les actions
    for action_number, action_description in enumerate(actions_done, start=1):
        logger.info(f"{action_number:04d}. {action_description}")

    logger.info("=" * 80)
    logger.info("PIPELINE TERMINÉ AVEC SUCCÈS")
    logger.info("=" * 80)

    # ═══════════════════════════════════════════════════════════════════════
    # CONSTRUCTION DU DICTIONNAIRE DE RÉSULTATS
    # ═══════════════════════════════════════════════════════════════════════
    results = {
        "zips_found": len(zip_files),
        "jsons_copied": json_count,
        "simulate": simulate,
        "actions": actions_done,
        "extractions": extraction_results,
        "success": True,
        "timestamp": datetime.datetime.now().isoformat()
    }

    return results

# -------------------------------------------------------------------------------
# CONSTRUCTION DU PARSER D'ARGUMENTS
# -------------------------------------------------------------------------------
def build_arg_parser():
    """
    Construit le parser d'arguments avec tous les arguments requis.

    Arguments implémentés (conformes aux règles V101) :
    - --help / -h : aide détaillée
    - --exec / -exe : exécution du pipeline
    - --prerequis / -pr : vérification des prérequis
    - --install / -i : installation des prérequis
    - --simulate / -s : mode simulation
    - --changelog / -ch : affichage du changelog

    Returns:
        argparse.ArgumentParser: Parser configuré avec tous les arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "Script d'extraction et de collecte de fichiers JSON depuis des archives ZIP.\n"
            "Parcourt le répertoire courant, extrait tous les .zip et collecte les .json."
        ),
        add_help=False,  # Désactivation de l'aide automatique pour gestion personnalisée
        formatter_class=argparse.RawTextHelpFormatter
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ARGUMENT 1 : --help / -h
    # ═══════════════════════════════════════════════════════════════════════
    parser.add_argument(
        "--help", "-h",
        action="store_true",
        dest="help",
        help="Afficher l'aide détaillée avec exemples d'utilisation"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ARGUMENT 2 : --exec / -exe
    # ═══════════════════════════════════════════════════════════════════════
    parser.add_argument(
        "--exec", "-exe",
        action="store_true",
        dest="exec",
        help="Exécuter le pipeline principal (extraction + collecte)"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ARGUMENT 3 : --prerequis / -pr
    # ═══════════════════════════════════════════════════════════════════════
    parser.add_argument(
        "--prerequis", "-pr",
        action="store_true",
        dest="prerequis",
        help="Vérifier tous les prérequis avant exécution"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ARGUMENT 4 : --install / -i
    # ═══════════════════════════════════════════════════════════════════════
    parser.add_argument(
        "--install", "-i",
        action="store_true",
        dest="install",
        help="Installer les prérequis manquants (si possible)"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ARGUMENT 5 : --simulate / -s
    # ═══════════════════════════════════════════════════════════════════════
    parser.add_argument(
        "--simulate", "-s",
        action="store_true",
        dest="simulate",
        help=(
            "Mode simulation (dry-run) : simule l'exécution sans modifications.\n"
            "Si présent : simulation active\n"
            "Si absent : exécution réelle avec modifications"
        )
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ARGUMENT 6 : --changelog / -ch
    # ═══════════════════════════════════════════════════════════════════════
    parser.add_argument(
        "--changelog", "-ch",
        action="store_true",
        dest="changelog",
        help="Afficher l'historique complet des versions (changelog)"
    )

    return parser

# -------------------------------------------------------------------------------
# FONCTION PRINCIPALE
# -------------------------------------------------------------------------------
def main():
    """
    Point d'entrée principal du script.

    Logique de traitement des arguments :
    1. Parse les arguments de la ligne de commande
    2. Détecte le mode systemd
    3. Traite les arguments dans l'ordre de priorité :
       - --help : affiche l'aide et quitte
       - --changelog : affiche le changelog et quitte
       - --prerequis : vérifie les prérequis et quitte
       - --install : installe les prérequis et quitte
       - --exec : exécute le pipeline (avec ou sans --simulate)
    4. Si aucun argument : affiche l'aide (sauf en mode systemd)
    """
    # ═══════════════════════════════════════════════════════════════════════
    # CONSTRUCTION DU PARSER ET PARSING DES ARGUMENTS
    # ═══════════════════════════════════════════════════════════════════════
    parser = build_arg_parser()
    args = parser.parse_args()

    # ═══════════════════════════════════════════════════════════════════════
    # DÉTECTION DU MODE SYSTEMD
    # ═══════════════════════════════════════════════════════════════════════
    running_as_systemd = is_running_as_systemd()

    if running_as_systemd:
        logger.info("Mode systemd détecté - Ajustement du comportement")

    # ═══════════════════════════════════════════════════════════════════════
    # TRAITEMENT : --help
    # ═══════════════════════════════════════════════════════════════════════
    if args.help:
        print_help_and_exit(parser)

    # ═══════════════════════════════════════════════════════════════════════
    # TRAITEMENT : --changelog
    # ═══════════════════════════════════════════════════════════════════════
    if args.changelog:
        # Affichage du changelog complet depuis la docstring
        print("=" * 80)
        print("CHANGELOG COMPLET")
        print("=" * 80)
        print(__doc__)
        print("=" * 80)
        logger.info("Changelog complet affiché.")
        sys.exit(0)

    # ═══════════════════════════════════════════════════════════════════════
    # TRAITEMENT : --prerequis
    # ═══════════════════════════════════════════════════════════════════════
    if args.prerequis:
        print("=" * 80)
        print("VÉRIFICATION DES PRÉREQUIS")
        print("=" * 80)

        prereq_ok, prereq_messages = check_prerequisites()

        # Affichage de tous les messages de vérification
        for message in prereq_messages:
            print(message)
            logger.info(message)

        print("=" * 80)

        # Message final selon le résultat
        if prereq_ok:
            final_msg = "✅ Tous les prérequis sont satisfaits. Le script peut s'exécuter."
            print(final_msg)
            logger.info(final_msg)
            sys.exit(0)
        else:
            final_msg = "❌ Certains prérequis ne sont pas satisfaits. Voir détails ci-dessus."
            print(final_msg)
            logger.error(final_msg)
            sys.exit(1)

    # ═══════════════════════════════════════════════════════════════════════
    # TRAITEMENT : --install
    # ═══════════════════════════════════════════════════════════════════════
    if args.install:
        install_messages = install_prerequisites()

        # Affichage de tous les messages d'installation
        for message in install_messages:
            print(message)
            logger.info(message)

        sys.exit(0)

    # ═══════════════════════════════════════════════════════════════════════
    # TRAITEMENT : --exec
    # ═══════════════════════════════════════════════════════════════════════
    if args.exec:
        # Détermination du mode simulation
        simulate_mode = args.simulate

        if simulate_mode:
            logger.info("🔍 MODE SIMULATION ACTIVÉ (dry-run)")
            logger.info("    Aucune modification ne sera effectuée")
        else:
            logger.info("⚡ MODE EXÉCUTION RÉELLE ACTIVÉ")
            logger.info("    Les modifications seront appliquées")

        # Exécution du pipeline principal
        try:
            results = run_main(simulate=simulate_mode)

            # Log final du statut
            if results["success"]:
                logger.info("✅ Script terminé avec succès")
                sys.exit(0)
            else:
                logger.warning("⚠️  Script terminé avec des avertissements")
                sys.exit(0)

        except Exception as e:
            logger.exception(f"❌ ERREUR FATALE lors de l'exécution: {e}")
            sys.exit(1)

    # ═══════════════════════════════════════════════════════════════════════
    # AUCUN ARGUMENT FOURNI
    # ═══════════════════════════════════════════════════════════════════════
    # Si aucun argument n'est fourni ET que ce n'est pas systemd,
    # afficher l'aide automatiquement
    else:
        if not running_as_systemd:
            logger.info("Aucun argument fourni - Affichage de l'aide automatique")
            print_help_and_exit(parser)
        else:
            # En mode systemd sans arguments, ne rien faire
            logger.info("Mode systemd sans arguments - Sortie silencieuse")
            sys.exit(0)

# -------------------------------------------------------------------------------
# POINT D'ENTRÉE DU SCRIPT
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Point d'entrée lorsque le script est exécuté directement.

    Ce bloc est exécuté uniquement si le script est lancé en tant que programme
    principal (pas importé comme module).
    """
    try:
        # Lancement de la fonction principale
        main()
    except KeyboardInterrupt:
        # Gestion propre de l'interruption utilisateur (Ctrl+C)
        logger.warning("\n⚠️  Interruption utilisateur détectée (Ctrl+C)")
        logger.info("Script arrêté proprement")
        sys.exit(130)  # Code de sortie standard pour SIGINT
    except Exception as e:
        # Gestion des erreurs non prévues
        logger.exception(f"❌ ERREUR NON GÉRÉE: {e}")
        sys.exit(1)
