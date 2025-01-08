#!/bin/sh

# Default host value
HOST="127.0.0.1"
ENV_FILE="env/.env.development"  # Default to development environment

# Show usage information
show_help() {
  echo "Usage: $0 [--development | --production | --test | --help]"
  echo ""
  echo "--development    Run the server on localhost and load the .env.development file"
  echo "--production     Run the server on the current machine IP address and load the .env.production file"
  echo "--testing        Run the server on localhost and load the .env.testing file"
  echo "--help           Show this help message"
}

# Check command-line arguments
if [ "$1" = "--help" ]; then
  show_help
  exit 0
fi

# Parse arguments
case "$1" in
  --development)
    echo "Using development environment configuration"
    ENV_FILE="env/.env.development"
    HOST="127.0.0.1"
    ;;
  --production)
    echo "Using production environment configuration"
    CURRENT_IP=$(hostname -I | awk '{print $1}')
    if [ -z "$CURRENT_IP" ]; then
      echo "Unable to detect current IP address! Using default host"
    else
      HOST="$CURRENT_IP"
    fi
    ENV_FILE="env/.env.production"
    ;;
  --testing)
    echo "Using testing environment configuration"
    ENV_FILE="env/.env.testing"
    HOST="127.0.0.1"
    ;;
  *)
    echo "Invalid option: $1"
    show_help
    exit 1
    ;;
esac

# Load the environment variables from the selected .env file
echo "Loading environment variables from $ENV_FILE"
export $(grep -v '^#' $ENV_FILE | xargs)

# Call your clean and venv scripts
sh ./scripts/clean_port.sh --8000
sh ./scripts/venv.sh

# Ensure the environment file is passed to secret.py (dynamically load environment variables)
echo "Loading environment variables in secret.py"
python -c "from utils.helper import load_env_file; load_env_file('$ENV_FILE')"

echo "Running uvicorn server in debug mode"
uvicorn src.main:app --host "$HOST" --port 8000 --reload --reload-dir=src
