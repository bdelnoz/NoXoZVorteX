#!/bin/bash
# =============================================================================
# Script: /home/nox/Documents/ai_export/testapi_lechat.sh
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v2.11 – Date: 2025-10-14
# Target usage: Tester l'API de Le Chat avec création de chat et message personnalisé
# =============================================================================
# Changelog:
# v2.11 – 2025-10-14 – Adaptation des arguments sans "=" et help enrichi
# v2.10 – 2025-10-14 – Ajout de --payload-content pour personnaliser le message (défaut: "Quelle est la date aujourd'hui ?")
# v2.9 – 2025-10-14 – --create-chat <nom> pour créer un chat avec le nom spécifié (défaut: "testing")
# v2.8 – 2025-10-14 – Ajout de --create-chat pour créer un chat "testing" et y envoyer un message
# v2.7 – 2025-10-14 – Correction de l'endpoint par défaut (/chat/completions) et passage en POST avec payload JSON
# v2.6 – 2025-10-14 – Correction définitive du nom du script (testapi_lechat.sh) dans toutes les références
# v2.5 – 2025-10-14 – Correction du nom du script dans l'en-tête et les références
# v2.4 – 2025-10-14 – Réintégration complète du changelog depuis v1.0
# v2.3 – 2025-10-14 – Endpoint `/chat` par défaut pour lister les chats
# v2.2 – 2025-10-14 – Endpoint valide (/models) et gestion des requêtes
# v2.1 – 2025-10-14 – URL de l'API de Le Chat pré-remplie
# v2.0 – 2025-10-14 – Version finale : correction complète, tests validés
# v1.7 – 2025-10-14 – Correction définitive des erreurs de syntaxe dans show_help
# v1.6 – 2025-10-14 – Correction syntaxe parenthèses dans show_help
# v1.5 – 2025-10-14 – Vérification stricte de --url pour --exec
# v1.4 – 2025-10-14 – Token chargé depuis ./ et logs/backups dans le répertoire courant
# v1.3 – 2025-10-14 – Logs et backups dans le répertoire courant
# v1.2 – 2025-10-14 – Adaptation pour exécution depuis ./
# v1.1 – 2025-10-14 – Ajout du chargement automatique du token
# v1.0 – 2025-10-14 – Création initiale
# =============================================================================
# --- Variables globales ---
SCRIPT_NAME="testapi_lechat.sh"
SCRIPT_VERSION="v2.11"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
LOG_FILE="log.${SCRIPT_NAME%.sh}.v${SCRIPT_VERSION}.log"
BACKUP_DIR="backups"
TOKEN_FILE="${SCRIPT_DIR}/.lechat"
API_BASE_URL="https://api.mistral.ai/v1"
API_ENDPOINT="/chat/completions"
API_URL="${API_BASE_URL}${API_ENDPOINT}"
TIMEOUT=30
SIMULATE=true
EXEC=false
DELETE=false
UNDELETE=false
CHECK_PREREQUIS=false
INSTALL_PREREQUIS=false
CREATE_CHAT=false
CHAT_NAME="testing"
PAYLOAD_CONTENT="Quelle est la date aujourd'hui ?"
# --- Chargement du token ---
if [[ ! -f "$TOKEN_FILE" ]]; then
    echo "ERREUR: Fichier de token $TOKEN_FILE introuvable." >&2
    exit 1
fi
API_KEY=$(tr -d '\n' < "$TOKEN_FILE")
# --- Fonction: Afficher l'aide ---
show_help() {
    cat <<EOF
Usage: ./$(basename "$0") [OPTIONS]
Options:
  --help               Afficher cette aide
  --exec               Exécuter le script
  --endpoint <PATH>    Changer l'endpoint (défaut: $API_ENDPOINT)
  --create-chat <NOM>  Créer un chat avec le nom spécifié (défaut: "testing")
  --payload-content "<message>"  Message à envoyer (défaut: "$PAYLOAD_CONTENT")
  --remove             Supprimer les logs
  --delete             Supprimer tous les fichiers générés
  --undelete           Restaurer depuis le dernier backup
  --prerequis          Vérifier les prérequis
  --install            Installer les prérequis manquants
  --simulate true|false  Mode simulation (défaut: true)
  --changelog          Afficher le changelog complet

Exemples:
  # Envoie une requête de chat standard
  ./$(basename "$0") --exec --simulate false

  # Crée un chat "testing" et demande la date
  ./$(basename "$0") --exec --create-chat testing --simulate false

  # Crée un chat "mon_chat" et envoie un message personnalisé
  ./$(basename "$0") --exec --create-chat mon_chat --payload-content "Bonjour, comment ça va ?" --simulate false

  # Crée un chat "urgent" et envoie un message avec des guillemets
  ./$(basename "$0") --exec --create-chat urgent --payload-content '"Quelle heure est-il ?"' --simulate false

  # Liste les modèles disponibles
  ./$(basename "$0") --exec --endpoint /models --simulate false

  # Vérifie les prérequis
  ./$(basename "$0") --prerequis

  # Installe les prérequis manquants
  ./$(basename "$0") --install

  # Supprime les logs (mode simulation)
  ./$(basename "$0") --delete --simulate true
EOF
}
# --- Fonction: Afficher le changelog ---
show_changelog() {
    cat <<EOF
# Changelog complet
## v2.11 – 2025-10-14
- Arguments sans "=" : --create-chat <nom>, --payload-content "<message>"
- Help enrichi avec plus d'exemples
## v2.10 – 2025-10-14
- Ajout de --payload-content pour personnaliser le message (défaut: "$PAYLOAD_CONTENT")
## v2.9 – 2025-10-14
- --create-chat <nom> pour créer un chat avec le nom spécifié (défaut: "testing")
## v2.8 – 2025-10-14
- Ajout de --create-chat pour créer un chat "testing" et y envoyer un message
## v2.7 – 2025-10-14
- Correction de l'endpoint par défaut (\`/chat/completions\`) et passage en POST avec payload JSON
## v2.6 – 2025-10-14
- Correction définitive du nom du script (\`testapi_lechat.sh\`) dans toutes les références
## v2.5 – 2025-10-14
- Correction du nom du script dans l'en-tête et les références
## v2.4 – 2025-10-14
- Réintégration complète du changelog depuis v1.0
## v2.3 – 2025-10-14
- Endpoint \`/chat\` par défaut pour lister les chats
## v2.2 – 2025-10-14
- Endpoint valide (\`/models\`) et gestion des requêtes
## v2.1 – 2025-10-14
- URL de l'API de Le Chat pré-remplie (\`https://api.mistral.ai/v1/\`)
## v2.0 – 2025-10-14
- Version finale : correction complète, tests validés
## v1.7 – 2025-10-14
- Correction définitive des erreurs de syntaxe dans show_help
## v1.6 – 2025-10-14
- Correction syntaxe parenthèses dans show_help
## v1.5 – 2025-10-14
- Vérification stricte de --url pour --exec
## v1.4 – 2025-10-14
- Token chargé depuis le répertoire du script, logs/backups dans le répertoire courant
## v1.3 – 2025-10-14
- Logs et backups dans le répertoire courant
## v1.2 – 2025-10-14
- Adaptation pour exécution depuis ./
## v1.1 – 2025-10-14
- Ajout du chargement automatique du token depuis ./.lechat
## v1.0 – 2025-10-14
- Création initiale
EOF
}
# --- Fonction: Vérifier les prérequis ---
check_prerequis() {
    echo "=== Vérification des prérequis ===" | tee -a "$LOG_FILE"
    if ! command -v curl &> /dev/null; then
        echo "ERREUR: curl n'est pas installé." | tee -a "$LOG_FILE"
        return 1
    fi
    if ! command -v jq &> /dev/null; then
        echo "AVERTISSEMENT: jq non installé (réponses JSON non formatées)." | tee -a "$LOG_FILE"
    fi
    echo "OK: Prérequis vérifiés." | tee -a "$LOG_FILE"
    return 0
}
# --- Fonction: Installer les prérequis ---
install_prerequis() {
    echo "=== Installation des prérequis ===" | tee -a "$LOG_FILE"
    sudo apt-get update > /dev/null 2>&1
    sudo apt-get install -y curl jq >> "$LOG_FILE" 2>&1
    echo "OK: Prérequis installés." | tee -a "$LOG_FILE"
}
# --- Fonction: Tester l'API ---
test_api() {
    echo "=== Test API de Le Chat ===" | tee -a "$LOG_FILE"
    echo "URL: $API_URL" | tee -a "$LOG_FILE"
    if [[ "$SIMULATE" == "true" ]]; then
        echo "[SIMULATION] Requête POST vers $API_URL" | tee -a "$LOG_FILE"
        return 0
    fi
    local payload
    if [[ "$CREATE_CHAT" == true ]]; then
        payload='{
            "model": "mistral-tiny",
            "messages": [
                {"role": "user", "content": "'"${PAYLOAD_CONTENT}"'"}
            ]
        }'
        echo "[PAYLOAD] Création du chat '"$CHAT_NAME"' et envoi du message : '"${PAYLOAD_CONTENT}"'" | tee -a "$LOG_FILE"
    else
        payload='{
            "model": "mistral-tiny",
            "messages": [
                {"role": "user", "content": "Bonjour !"}
            ]
        }'
    fi
    local response
    response=$(curl -s -X POST "$API_URL" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        --max-time "$TIMEOUT" 2>&1)
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "$payload")
    echo "Code HTTP: $http_code" | tee -a "$LOG_FILE"
    if command -v jq &> /dev/null; then
        echo "$response" | jq . | tee -a "$LOG_FILE"
    else
        echo "$response" | tee -a "$LOG_FILE"
    fi
}
# --- Fonction: Supprimer proprement ---
delete_all() {
    echo "=== Suppression ===" | tee -a "$LOG_FILE"
    if [[ "$SIMULATE" == "true" ]]; then
        echo "[SIMULATION] Suppression de $LOG_FILE" | tee -a "$LOG_FILE"
        return 0
    fi
    mkdir -p "$BACKUP_DIR"
    local backup_file="${BACKUP_DIR}/backup_${SCRIPT_NAME%.sh}.v${SCRIPT_VERSION}_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czf "$backup_file" "$LOG_FILE" 2>/dev/null && \
    rm -f "$LOG_FILE" && \
    echo "Backup créé: $backup_file" | tee -a "$LOG_FILE"
}
# --- Fonction: Restaurer depuis backup ---
undelete() {
    echo "=== Restauration ===" | tee -a "$LOG_FILE"
    local last_backup
    last_backup=$(ls -t "${BACKUP_DIR}"/backup_*"${SCRIPT_NAME%.sh}"*.tar.gz 2>/dev/null | head -1)
    if [[ -z "$last_backup" ]]; then
        echo "ERREUR: Aucun backup trouvé." | tee -a "$LOG_FILE"
        return 1
    fi
    tar -xzf "$last_backup" && \
    echo "Restauration depuis $last_backup" | tee -a "$LOG_FILE"
}
# --- Gestion des arguments ---
main() {
    if (( $# == 0 )); then
        show_help
        exit 0
    fi
    while (( $# > 0 )); do
        case "$1" in
            --help) show_help; exit 0 ;;
            --exec) EXEC=true ;;
            --endpoint) API_ENDPOINT="$2"; API_URL="${API_BASE_URL}${API_ENDPOINT}"; shift ;;
            --create-chat) CREATE_CHAT=true; CHAT_NAME="$2"; shift ;;
            --payload-content)
                shift
                PAYLOAD_CONTENT="$1"
                PAYLOAD_CONTENT="${PAYLOAD_CONTENT//\"}"
                ;;
            --remove) REMOVE=true ;;
            --delete) DELETE=true ;;
            --undelete) UNDELETE=true ;;
            --prerequis) CHECK_PREREQUIS=true ;;
            --install) INSTALL_PREREQUIS=true ;;
            --simulate) SIMULATE="$2"; shift ;;
            --changelog) show_changelog; exit 0 ;;
            *) echo "Option invalide: $1" | tee -a "$LOG_FILE"; show_help; exit 1 ;;
        esac
        shift
    done
    mkdir -p "$BACKUP_DIR"
    touch "$LOG_FILE"
    echo "=== Démarrage $(basename "$0") v$SCRIPT_VERSION ===" >> "$LOG_FILE"
    if [[ "$CHECK_PREREQUIS" == true ]]; then
        check_prerequis || exit 1
    fi
    if [[ "$INSTALL_PREREQUIS" == true ]]; then
        install_prerequis
    fi
    if [[ "$DELETE" == true ]]; then
        delete_all
    fi
    if [[ "$UNDELETE" == true ]]; then
        undelete
    fi
    if [[ "$EXEC" == true ]]; then
        test_api
    fi
}
main "$@"
