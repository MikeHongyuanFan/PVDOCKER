#!/usr/bin/env python

import os
import time
import sys
import psycopg2
from urllib.parse import urlparse

# Parse the DATABASE_URL environment variable
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("DATABASE_URL environment variable not set")
    sys.exit(0)

# Parse the URL
url = urlparse(db_url)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port or 5432

# Wait for the database to be ready
max_tries = 60
tries = 0
while tries < max_tries:
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.close()
        print("Database is ready!")
        sys.exit(0)
    except psycopg2.OperationalError:
        tries += 1
        print(f"Database not ready yet (attempt {tries}/{max_tries}). Waiting...")
        time.sleep(1)

print("Could not connect to database after multiple attempts. Exiting.")
sys.exit(1)
