#!/bin/bash

echo "Shutting down the local cluster..."
docker compose -f local.yml down

echo "Updating the local cluster..."
git fetch origin
git pull origin main

echo "Building the local cluster..."
docker compose -f local.yml build

echo "Applying migrations..."
docker compose -f local.yml run django python manage.py migrate

echo "Starting the local cluster..."
docker compose -f local.yml up -d

echo "Update complete!"
