#!/bin/bash
set -euo pipefail

echo "Running create-databases.sh..."

psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE ${UNIGATE_DB};"
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE ${AUTH_DB};"
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE ${UNIVERSITY_DB};"

echo "Databases created: $UNIGATE_DB, $AUTH_DB, $UNIVERSITY_DB"


