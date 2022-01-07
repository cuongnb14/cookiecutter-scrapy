#!/usr/bin/env bash
set -e

cron
rm twistd.pid || echo "ignore"

exec scrapyd