#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."

# The DATABASE_URL is in the environment, we need to parse it for pg_isready
# Example: postgres://user:password@db:5432/the_syndicate_db
# We extract the host 'db' and the port '5432'
DB_HOST=$(echo $DATABASE_URL | sed -E 's/.*@([^:]+):.*/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/.*:([0-9]+)\/.*/\1/')
DB_USER=$(echo $DATABASE_URL | sed -E 's/postgres:\/\/([^:]+):.*/\1/')

while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "PostgreSQL started"

# Run database migrations
# This is a great diagnostic step. If this fails, we know there's a problem.
echo "Running database migrations..."
python manage.py migrate --no-input

# Run the command passed to this script
# This will be 'gunicorn', 'celery worker', or 'celery beat'
exec "$@"