#!/usr/bin/env bash

# This runs every time GitHub pushes to main.
PROJECT_NAME=DJANGO_STARTER

set -e

echo "🚀 Deploy started at $(date)"

cd /home/prod_user/$PROJECT_NAME

git pull origin main
git reset --hard origin/main

# Stop and remove existing containers (ignore if none exist)
docker-compose down

# Rebuild and restart containers
docker-compose up -d --build

echo "✅ Deploy complete"
