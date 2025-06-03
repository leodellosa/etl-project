#!/bin/bash

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Load initial data if DB is empty
if [ ! -f "db.sqlite3" ]; then
  echo "Creating DB and loading initial data..."
  python manage.py migrate --noinput
  python manage.py loaddata initial_data.json
fi

exec "$@"
