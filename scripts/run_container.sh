#!/bin/sh

# Function to show the help message
show_help() {
  echo "Usage: ./run_container.sh [--testing|--production|--development|--help]"
  echo ""
  echo "--testing       Use .env.testing file for environment variables."
  echo "--production    Use .env.production file for environment variables."
  echo "--development   Use .env.development file for environment variables."
  echo "--help          Show this help message."
}

# Default environment file path
ENV_FILE=""

# Parse the command-line arguments
while [ "$#" -gt 0 ]; do
    case $1 in
        --testing)
            echo "Using testing environment configuration"
            ENV_FILE="./env/.env.testing"
            shift
            ;;
        --production)
            echo "Using production environment configuration"
            ENV_FILE="./env/.env.production"
            shift
            ;;
        --development)
            echo "Using development environment configuration"
            ENV_FILE="./env/.env.development"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if the ENV_FILE variable is set
if [ -z "$ENV_FILE" ]; then
    echo "Error: Environment file not specified!"
    show_help
    exit 1
fi

# Check if the specified environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file '$ENV_FILE' not found!"
    exit 1
fi

# Load the selected environment variables
echo "Loading environment variables from $ENV_FILE"
export $(grep -v '^#' $ENV_FILE | xargs)

# Run the Docker container using the appropriate environment settings
echo "Starting container with environment variables from $ENV_FILE..."
docker-compose --env-file $ENV_FILE up -d
