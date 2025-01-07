#!/bin/sh

# Get the directory of the script
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
CURRENT_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')

BACKUP_CONJOB="$PROJECT_DIR/utils/query/cronjob/backup_model_card.py"

# Activate the virtual environment
. "$SCRIPT_DIR/venv.sh"

echo "[$CURRENT_DATETIME] Executing $BACKUP_CONJOB"
python "$BACKUP_CONJOB"
echo "[$CURRENT_DATETIME] Task finished."
