#!/bin/bash

# Ensure celery worker file exists
CELERY_WORKER="$PWD/services/celery/worker.py"

if [ ! -f "$CELERY_WORKER" ]; then
    echo "Worker file not found!"
    exit 1
fi

echo "Celery worker found! Processing request..."
celery --broker=amqp://development:development@localhost:5672// flower -A diva_monitoring \
    --basic_auth=development:development \
    --broker_api=http://development:development@localhost:15672/api/vhost
