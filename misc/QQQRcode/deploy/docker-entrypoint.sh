#!/bin/sh

rm -f /app/docker-entrypoint.sh
socat -v -s TCP4-LISTEN:9999,tcpwrap=script,reuseaddr,fork EXEC:"python3 -u /app/main.py"