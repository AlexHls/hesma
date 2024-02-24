#!/bin/bash

echo "Create database backup? (y/n)"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    echo "Creating database backup..."
    # Load the environment variables
    source .envs/.production/.postgres

    # Check if POSTGRES_BACKUP_DIR env var is set
    if [ -z "$POSTGRES_BACKUP_DIR" ]; then
        echo "POSTGRES_BACKUP_DIR is not set. Defaulting to ./backups"
        backup_dir="./backups"
    else
        echo "POSTGRES_BACKUP_DIR is set to $POSTGRES_BACKUP_DIR"
        backup_dir=$POSTGRES_BACKUP_DIR
    fi

    # Create the backup directory if it doesn't exist
    if [ ! -d "$backup_dir" ]; then
        mkdir -p $backup_dir
    fi

    # Backup the database
    docker exec -t hesma_production_postgres pg_dumpall -c -U $POSTGRES_USER | gzip > $backup_dir/dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql.gz

    echo "Backup complete"
fi

echo "Shutting down the local cluster..."
docker compose -f production.yml down

echo "Updating the local cluster..."
git fetch origin
git pull origin main

echo "Building the local cluster..."
docker compose -f production.yml build

echo "Applying migrations..."
docker compose -f production.yml run django python manage.py migrate

echo "Starting the local cluster..."
docker compose -f production.yml up -d

echo "Update complete!"
