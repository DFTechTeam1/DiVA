#!/bin/sh

# Get the directory of the script
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
CURRENT_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')

IMAGE_TAG_SCRIPT="$PROJECT_DIR/utils/query/cronjob/backup_image_tag.py"
MODEL_CARD_SCRIPT="$PROJECT_DIR/utils/query/cronjob/backup_model_card.py"

show_help() {
    echo "Usage: $0 [--image_tag | --model_card | --help]"
    echo "  --image_tag     Execute backup_image_tag.py"
    echo "  --model_card    Execute backup_model_card.py"
    echo "  --help          Show this help message"
}

# Activate the virtual environment
. "$SCRIPT_DIR/venv.sh"

# Check the argument passed to the script
case "$1" in
    --image_tag)
        echo "[$CURRENT_DATETIME] Executing $IMAGE_TAG_SCRIPT"
        python "$IMAGE_TAG_SCRIPT"
        echo "[$CURRENT_DATETIME] Task finished."
        ;;
    --model_card)
        echo "[$CURRENT_DATETIME] Executing $MODEL_CARD_SCRIPT"
        python "$MODEL_CARD_SCRIPT"
        echo "[$CURRENT_DATETIME] Task finished."
        ;;
    --help | -h)
        show_help
        ;;
    *)
        echo "Invalid option: $1"
        show_help
        exit 1
        ;;
esac
