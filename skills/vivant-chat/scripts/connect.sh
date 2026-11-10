#!/usr/bin/env bash
# Quick interactive connection to VIVANT terminal chatroom
HOST="${1:-term.freedom8964.com}"
PORT="${2:-2222}"
USER="${3:-guest}"

echo "Connecting to VIVANT at ${USER}@${HOST}:${PORT}..."
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p "${PORT}" "${USER}@${HOST}"
