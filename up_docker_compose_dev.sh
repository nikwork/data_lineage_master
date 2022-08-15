#! /bin/bash

# Show env vars
echo Show env vars:
echo
grep -v '^#' ./config/.env.dev
echo

export NEO4J_VERSION="latest"

echo Docker-compose UP:
echo
docker-compose --env-file ./config/.env.dev up