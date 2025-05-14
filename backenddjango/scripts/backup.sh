#!/bin/bash

# Exit on error
set -e

# Create backup directory if it doesn't exist
BACKUP_DIR=~/backups
mkdir -p $BACKUP_DIR

# Generate timestamp
TIMESTAMP=$(date +%Y-%m-%d-%H-%M)

# Backup PostgreSQL database
echo "Backing up database..."
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db-$TIMESTAMP.sql

# Backup media files
echo "Backing up media files..."
docker cp $(docker-compose -f docker-compose.prod.yml ps -q web):/app/media $BACKUP_DIR/media-$TIMESTAMP

# Compress backups
echo "Compressing backups..."
tar -czf $BACKUP_DIR/backup-$TIMESTAMP.tar.gz $BACKUP_DIR/db-$TIMESTAMP.sql $BACKUP_DIR/media-$TIMESTAMP

# Remove uncompressed files
rm $BACKUP_DIR/db-$TIMESTAMP.sql
rm -rf $BACKUP_DIR/media-$TIMESTAMP

# Keep only the last 7 backups
echo "Cleaning up old backups..."
ls -tp $BACKUP_DIR/backup-*.tar.gz | grep -v '/$' | tail -n +8 | xargs -I {} rm -- {}

echo "Backup completed: $BACKUP_DIR/backup-$TIMESTAMP.tar.gz"
