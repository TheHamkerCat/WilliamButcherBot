#!/bin/sh
set -e

# Only the bind mounts are writable; the root file system is read-only
mkdir -p /wbb/sessions /data
chown -R appuser:appuser /wbb/sessions /data
chmod 700 /wbb/sessions /data

exec gosu appuser /wbb/.venv/bin/python -m wbb
