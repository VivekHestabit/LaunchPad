# Week 5 — Day 1  
## Docker Fundamentals & Linux Internals

---

## Work Done

Explored Docker fundamentals and Linux internals by running a Node.js application inside a container and inspecting the container environment using Linux commands.

---

## Docker Concepts Used

- Images
- Containers
- Volumes
- Networks
- Dockerfile

---

## Container Setup

### Build Docker Image

```bash
docker build -t node-app .


Run Container
docker run -d --name node-container -p 3000:3000 node-app

Accessing the Running Container
docker exec -it node-container /bin/sh

Linux Commands Used Inside Container
File System
ls
ls -lah
ls /

Processes
ps

System Resource Usage
top

Disk Usage
df -h
du -sh /
du -sh /app

Logs
Container Logs (from host)
docker logs node-container

Logs Inside Container
ls /var/log