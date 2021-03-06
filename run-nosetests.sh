#!/bin/sh
#set -x
set -e

export FLASK_APP="clustering_outliers"
export SECRET_KEY="$(dd if=/dev/urandom bs=12 count=1 status=none | base64)"

# Initialize database

flask init-db

# Run

exec nosetests $@