#!/usr/bin/env bash
# render-build.sh — robust build step for ThaiBridge AI on Render.
#
# Why this exists: `pip freeze` on Windows can capture Windows-only packages
# (pywin32, etc.) and local file-path entries that DO NOT exist on Render's Linux
# build servers, causing "No matching distribution found" failures. This script
# strips those lines into a clean, Linux-safe requirements file before installing,
# and guarantees gunicorn (the production web server) is present.

set -euo pipefail

echo "==> Preparing a Linux-safe requirements file..."

# Packages that only exist on Windows and must never reach a Linux pip install.
WINDOWS_ONLY='pywin32|pypiwin32|pywincffi|winshell|wmi|pywin32-ctypes'

grep -viE "^($WINDOWS_ONLY)([=<>! ]|$)" requirements.txt \
  | grep -v "@ file:///" \
  > requirements.render.txt || true

# Guarantee gunicorn (the production server Render uses) is present.
if ! grep -qiE '^gunicorn([=<>! ]|$)' requirements.render.txt; then
  echo "gunicorn" >> requirements.render.txt
  echo "==> gunicorn was missing; added it."
fi

echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.render.txt

echo "==> Build complete."
