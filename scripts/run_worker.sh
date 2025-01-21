#!/bin/sh

# Ensure celery worker file exists
CELERY_WORKER="$PWD/services/celery/worker.py"

if [ ! -f "$CELERY_WORKER" ]; then
    echo "Worker file not found!"
    exit 1
fi


sh ./scripts/venv.sh

echo "Celery worker found! Processing request..."
celery -A services.celery.worker worker --loglevel=INFO
