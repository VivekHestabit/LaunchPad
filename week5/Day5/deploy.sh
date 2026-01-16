#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m' 

echo -e "${GREEN} Starting Deployment for TaskFlow...${NC}"

if [ ! -f ./certs/localhost+1.pem ]; then
    echo " SSL Certificates missing! Run 'mkcert' first."
    exit 1
fi

echo -e "${GREEN} Building and Starting Containers...${NC}"
docker compose -f docker-compose.prod.yml up -d --build

echo -e "${GREEN} Cleaning up old images...${NC}"
docker image prune -f

echo -e "${GREEN} Deployment Complete! checking status...${NC}"
docker compose ps

echo -e "${GREEN} App is live at https://myApp.local${NC}"