#!/bin/sh

# Get the directory of the script
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
CURRENT_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')

IMAGE_TAG_SCRIPT="$PROJECT_DIR/utils/query/cronjob/backup_image_tag.py"
MODEL_CARD_SCRIPT="$PROJECT_DIR/utils/query/cronjob/backup_model_card.py"

ENV_FILE=""
JOB_SCRIPT=""

show_help() {
    echo "Usage: $0 [ --development | --staging | --production ] [ --image_tag | --model_card | --help ]"
    echo ""
    echo "Environment Options:"
    echo "  --development    Set the environment to development."
    echo "  --staging        Set the environment to staging."
    echo "  --production     Set the environment to production."
    echo ""
    echo "Job Options:"
    echo "  --image_tag      Execute backup_image_tag.py"
    echo "  --model_card     Execute backup_model_card.py"
    echo ""
    echo "  --help           Show this help message."
}

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --development)
            ENV_FILE="$PROJECT_DIR/env/.env.development"
            ;;
        --staging)
            ENV_FILE="$PROJECT_DIR/env/.env.staging"
            ;;
        --production)
            ENV_FILE="$PROJECT_DIR/env/.env.production"
            ;;
        --image_tag)
            JOB_SCRIPT="$IMAGE_TAG_SCRIPT"
            ;;
        --model_card)
            JOB_SCRIPT="$MODEL_CARD_SCRIPT"
            ;;
        --help | -h)
            show_help
            exit 0
            ;;
        *)
            echo "Invalid option: $1"
            show_help
            exit 1
            ;;
    esac
    shift
done

# Validate inputs
if [ -z "$ENV_FILE" ]; then
    echo "Error: No environment specified. Please provide one of --development, --staging, or --production."
    show_help
    exit 1
fi

if [ -z "$JOB_SCRIPT" ]; then
    echo "Error: No job type specified. Please provide one of --image_tag or --model_card."
    show_help
    exit 1
fi

#Load the environment variables using the external script
export $(grep -v '^#' $ENV_FILE | xargs)
sh ./scripts/load_env.sh

# Activate virtualenv
sh ./scripts/activate.sh

# Execute the job script
echo "[$CURRENT_DATETIME] Executing $JOB_SCRIPT in $ENV_FILE environment"
if ! python3 "$JOB_SCRIPT"; then
    echo "[$CURRENT_DATETIME] Task failed!"
    exit 1
fi

echo "[$CURRENT_DATETIME] Task finished successfully."
