#!/bin/sh
set -e

python init_db.py

exec "$@"
