#!/bin/sh

# Default host value
HOST="127.0.0.1"

# Check command-line arguments
if [ "$1" = "--prod" ]; then
  echo "Using production environment configuration"
  CURRENT_IP=$(hostname -I | awk '{print $1}')
  if [ -z "$CURRENT_IP" ]; then
    echo "Unable to detect current IP address! Using default host"
  else
    HOST="$CURRENT_IP"
  fi
else
  # Default to local if no argument or if --local is passed
  echo "Using local environment configuration"
fi

sh ./scripts/clean_port.sh --8000
sh ./scripts/venv.sh

echo "Running uvicorn server in debug mode"
uvicorn src.main:app --host "$HOST" --port 8000 --reload --reload-dir=src
