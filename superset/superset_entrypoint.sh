#!/bin/bash

export $(grep -v '^#' .env | xargs)

export SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI}

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

superset run -h 0.0.0.0 -p 8088
