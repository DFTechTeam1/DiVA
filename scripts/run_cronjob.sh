#!/bin/sh

# Get the directory of the script
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
CURRENT_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')

BACKUP_CONJOB="$PROJECT_DIR/utils/query/cronjob/backup_image_tag.py"
VENV_PATH="$PROJECT_DIR/.venv/bin/activate"

# Checking OS Environment
echo "Checking OS Environment"
if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
  echo "WSL detected"
  . "$VENV_PATH"
  echo "[$CURRENT_DATETIME] Executing $BACKUP_CONJOB"
  python "$BACKUP_CONJOB"
  echo "[$CURRENT_DATETIME] Task finished."
else
  case "$OSTYPE" in
    linux*)
      echo "Linux based OS detected"
      . "$VENV_PATH"
      echo "[$CURRENT_DATETIME] Executing $BACKUP_CONJOB"
      python "$BACKUP_CONJOB"
      echo "[$CURRENT_DATETIME] Task finished."
      ;;
    cygwin* | msys* | mingw*)
      echo "Windows based OS detected"
      . "$PROJECT_DIR/.venv/Scripts/activate"
      ;;
    *)
      echo "Unsupported OS detected. This feature is not developed yet."
      exit 1
      ;;
  esac
fi
