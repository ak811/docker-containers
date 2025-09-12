#!/bin/sh
set -e

# Clean containers/volumes
docker compose down -v || true

# Reset output folder
rm -rf out
mkdir -p out

# Build and run stack
docker compose up --build
