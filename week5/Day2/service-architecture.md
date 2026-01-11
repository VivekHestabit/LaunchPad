# Service Architecture — Docker Compose Multi-Container Application

## Overview
This project demonstrates a **multi-container application architecture** using Docker Compose.  
The application consists of three independent services:

- Client (React)
- Server (Node.js)
- Database (MongoDB)

Each service runs inside its own Docker container and is orchestrated using a single `docker-compose.yml` file.

The entire application stack is started using one command:

docker compose up -d
