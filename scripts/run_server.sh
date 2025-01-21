#!/bin/sh

# Default value
ENV_FILE="env/.env.development"

# Checking for existing processes on port 8000
echo "Checking for existing processes on port 8000"
PIDS=$(lsof -ti :8000)
if [ -n "$PIDS" ]; then
  echo "Killing existing processes on port 8000"
  kill -9 $PIDS
fi

# Show usage information
show_help() {
  echo "Usage: sh $0 [ --development | --staging | --production | --help ]"
  echo ""
  echo "--development    Run the server on localhost and load the .env.development file"
  echo "--staging        Run the server on the staging IP and load the .env.staging file"
  echo "--production     Run the server on the production IP address and load the .env.production file"
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
    ;;
  --staging)
    echo "Using staging environment configuration"
    ENV_FILE="env/.env.staging"
    ;;
  --production)
    echo "Using production environment configuration"
    ENV_FILE="env/.env.production"
    ;;
  *)
    echo "Invalid option: $1"
    show_help
    exit 1
    ;;
esac

# Load the environment variables
export $(grep -v '^#' $ENV_FILE | xargs)

# Check if SERVER_HOST is defined in the .env file
if [ -z "$SERVER_HOST" ]; then
  echo "SERVER_HOST is not defined in $ENV_FILE. Using default '127.0.0.1'."
  SERVER_HOST="127.0.0.1"
fi

# Activate virtualenv
sh ./scripts/activate.sh

# Start the server
echo "Running uvicorn server with SERVER_HOST=$SERVER_HOST"
uvicorn src.main:app --host "$SERVER_HOST" --port 8000 --reload --log-level debug
