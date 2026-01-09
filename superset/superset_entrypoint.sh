#!/bin/bash
set -e

export $(grep -v '^#' .env | xargs)

superset db upgrade

if ! superset fab list-users | grep -q ${SUPERSET_USERNAME}; then
    superset fab create-admin \
        --username ${SUPERSET_USERNAME} \
        --firstname ${SUPERSET_FIRSTNAME} \
        --lastname ${SUPERSET_LASTNAME} \
        --email ${SUPERSET_EMAIL} \
        --password ${SUPERSET_PASSWORD}
fi

superset init

# =============================================================================
# TODO: Import datasets & dashboards
# =============================================================================

superset run -h 0.0.0.0 -p 8088
