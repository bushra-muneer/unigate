
#!/bin/bash

set -euo pipefail

# Generate servers.json with env values
echo "{
    \"Servers\": {
        \"1\": {
            \"Name\": \"unigate\",
            \"Group\": \"Servers\",
            \"Host\": \"${POSTGRES_HOST}\",
            \"Port\": 5432,
            \"MaintenanceDB\": \"${POSTGRES_DB}\",
            \"Username\": \"${POSTGRES_USER}\",
            \"SSLMode\": \"prefer\",
            \"PassFile\": \"/tmp/pgpassfile\"
        }
    }
}" > /tmp/servers.json && chmod 600 /tmp/servers.json

# Create pgpassfile
echo "${POSTGRES_HOST}:5432:*:${POSTGRES_USER}:${POSTGRES_PASSWORD}" > /tmp/pgpassfile && chmod 600 /tmp/pgpassfile

# Copy to PGAdmin config location
mkdir -p /var/lib/pgadmin
cp /tmp/servers.json /var/lib/pgadmin/servers.json
cp /tmp/pgpassfile /var/lib/pgadmin/pgpassfile

# Start pgAdmin
/entrypoint.sh
