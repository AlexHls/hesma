#!/bin/bash

echo "Shutting down the local cluster..."
docker compose -f production.yml down

echo "Updating the local cluster..."
git fetch origin
git pull origin main

echo "Applying migrations..."
docker compose -f production.yml run django python manage.py migrate

echo "Starting the local cluster..."
docker compose -f production.yml up -d --build

echo "Update complete!"
