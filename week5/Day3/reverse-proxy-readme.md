# NGINX Reverse Proxy & Load Balancing (Docker)

## Objective
The goal of this task is to demonstrate how **NGINX can be used as a reverse proxy and load balancer**
to route incoming client requests to multiple backend service instances running inside Docker containers.

---

## Architecture Overview

Client  
↓  
NGINX (Reverse Proxy + Load Balancer)  
↓  
Backend Service Replicas (Node.js)

NGINX acts as a single entry point for clients and distributes traffic across multiple backend instances using **round-robin load balancing**.

---

## Components Used

- **NGINX**
  - Acts as a reverse proxy
  - Routes `/api` requests to backend services
  - Performs round-robin load balancing

- **Backend Service**
  - Node.js HTTP server
  - Runs on port `3000`
  - Two identical instances (`backend1`, `backend2`)

- **Docker & Docker Compose**
  - Containerizes all services
  - Provides internal networking and DNS-based service discovery

---

## Request Flow

1. Client sends a request to `/api`
2. Request reaches the NGINX container
3. NGINX forwards the request to one of the backend containers
4. Backend responds with its instance identifier
5. NGINX sends the response back to the client

---

## Load Balancing Strategy

- **Round-robin** (default in NGINX)
- Requests are distributed sequentially:
  - Request 1 → backend1
  - Request 2 → backend2
  - Request 3 → backend1

This ensures even distribution of traffic across backend services.

---

## Why Reverse Proxy is Used

- Backend services are not exposed directly to clients
- Centralized traffic management
- Improved security and scalability
- Easier backend scaling without client-side changes

---

## Docker Networking

- Docker Compose creates a private bridge network
- Containers can communicate using service names
- NGINX resolves `backend1` and `backend2` via Docker’s internal DNS

---

## How to Run the Project

```bash
docker-compose up --build
