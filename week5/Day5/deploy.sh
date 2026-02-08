#!/bin/bash
GREEN='\033[0;32m' 

echo -e "${GREEN} Starting Deployment for TaskFlow..."

if [ ! -f ./certs/myapp-dev.localhost]; then
    echo " SSL Certificates missing! Run 'mkcert' first."
    exit 1
fi

echo -e "${GREEN} Building and Starting Containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo -e "${GREEN} Cleaning up old images..."
docker image prune -f

echo -e "${GREEN} Deployment Complete! checking status..."
docker compose ps

echo -e "${GREEN} App is live at https://myApp-dev.localhost:8444"