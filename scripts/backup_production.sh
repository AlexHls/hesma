#!/bin/bash

# Backup the postgres database for the production environment

# Load the environment variables, path is specific to the project
source $HOME/hesma/.envs/.production/.postgres

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
docker exec -t hesma-postgres-1 pg_dumpall -c -U $POSTGRES_USER | gzip > $backup_dir/dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql.gz

echo "Backup complete"
