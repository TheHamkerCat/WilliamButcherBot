#!/bin/sh
set -e

mkdir -p /wbb/sessions /data
chown -R appuser:appuser /wbb/sessions /data
chmod 700 /wbb/sessions /data

if [ -f /wbb/config.py ]; then
    chown appuser:appuser /wbb/config.py || true
fi

if [ -f /wbb/config.env ]; then
    chown appuser:appuser /wbb/config.env || true
fi

exec gosu appuser /wbb/.venv/bin/python -m wbb
