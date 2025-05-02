#!/bin/bash

REGION="${REGION:-1}"
EPG_DAYS="${EPG_DAYS:-7}"
REFRESH_HOURS="${REFRESH_HOURS:-6}"
XML_FILE="/app/sky.xml"

cd /app

# Start HTTP server in background
python3 -m http.server 8855 &

function update_epg {
    echo "[INFO] Updating EPG XML for region $REGION with $EPG_DAYS day(s)..."
    python3 sky_epg_grab.py "$XML_FILE"
    echo "[INFO] Done at $(date)"
}

# First run
update_epg

# Repeat every X hours
while true; do
    sleep "${REFRESH_HOURS}h"
    update_epg
done
