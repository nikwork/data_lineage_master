#! /bin/bash

export NEO4J_VERSION="latest"
docker-compose --env-file ./config/.env.dev up