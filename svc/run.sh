#!/usr/bin/env bash
SVC_ROOT=/opt/svc/bettywhitelist
UDS_PATH="$SVC_ROOT/bettywhitelist.sock"
LOGS_FOLDER="$SVC_ROOT/log"
mkdir -p "$LOGS_FOLDER"
exec "$SVC_ROOT/venv/bin/gunicorn" \
  --bind "unix:$UDS_PATH" \
  --sd-notify \
  --access-logfile "$LOGS_FOLDER/access.log" \
  --error-logfile "$LOGS_FOLDER/errors.log" \
  --workers 3 \
  --umask 007 \
  --chdir "$SVC_ROOT/content" \
  splunge.app:app
