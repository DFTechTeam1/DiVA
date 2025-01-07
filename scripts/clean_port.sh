#!/bin/bash

# Check if a port number is passed as an argument
if [ -z "$1" ]; then
  echo "Usage: sh clean_port.sh --<port>"
  exit 1
fi

# Extract the port number from the argument (--8000 -> 8000)
PORT=$(echo "$1" | sed 's/--//')

# Validate if the port is a number
if ! echo "$PORT" | grep -qE '^[0-9]+$'; then
  echo "Invalid port number. Please provide a valid port (e.g., --8000)"
  exit 1
fi

# Kill processes running on the specified port
echo "Checking for existing processes on port $PORT"
PIDS=$(lsof -ti :$PORT)

if [ -n "$PIDS" ]; then
  echo "Killing processes on port $PORT"
  kill -9 $PIDS
  echo "Processes on port $PORT have been terminated."
else
  echo "No processes found on port $PORT"
fi
