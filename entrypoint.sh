#!/bin/bash
set -e

# Wait for database to be ready using Python
echo "Waiting for database..."
python -c "
import sys
import time
import psycopg2
from psycopg2 import OperationalError

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            host='db',
            port=5432,
            user='${POSTGRES_USER:-adbridge}',
            password='${POSTGRES_PASSWORD:-adbridge123}',
            dbname='${POSTGRES_DB:-adbridge}'
        )
        conn.close()
        print('Database is ready!')
        sys.exit(0)
    except OperationalError:
        retry_count += 1
        if retry_count < max_retries:
            time.sleep(1)
        else:
            print('Database connection failed after 30 retries')
            sys.exit(1)
"

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:${PORT:-8000} --timeout 120 --workers 4 --threads 2 "wsgi:app"

