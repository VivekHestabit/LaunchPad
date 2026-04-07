# Ollama Docker Setup — Complete Guide

## Overview

This guide covers the complete setup of Ollama on Docker, copying a local GGUF model into the container, and running it for inference.

---

## Prerequisites

- Docker installed on your Linux machine
- Your model file available at: `/home/viveksingh/Desktop/Launchpad/week8/quantized/model.gguf`

---

## Step 1 — Pull Ollama Docker Image

```bash
docker pull ollama/ollama
```

---

## Step 2 — Run Ollama Container

```bash
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

### Flag Explanation

| Flag | Meaning |
|---|---|
| `-d` | Run in background (detached mode) |
| `-v ollama:/root/.ollama` | Persist models even after container stops |
| `-p 11434:11434` | Expose Ollama's port to your machine |
| `--name ollama` | Name the container "ollama" |

---

## Step 3 — Verify Container is Running

```bash
docker ps
```

You should see the ollama container listed and running ✅

---

## Step 4 — Copy Model into Container

```bash
docker cp /home/viveksingh/Desktop/Launchpad/week8/quantized/model.gguf ollama:/root/.ollama/
````

---

## Step 5 — Go Inside the Container

```bash
docker exec -it ollama bash
```

Your terminal will change to:

```
root@container-id:/#
```

This means you are **inside the container** ✅

---

## Step 6 — Create Modelfile Inside Container

```bash
echo "FROM /root/.ollama/model.gguf" > Modelfile
```

### Verify the Modelfile

```bash
cat Modelfile
```

Expected output:

```
FROM /root/.ollama/model.gguf
```

---

## Step 7 — Create Ollama Model from Modelfile

```bash
ollama create medical-model -f Modelfile
```

---

## Step 8 — Verify Model is Created

```bash
ollama list
```

Expected output:

```
NAME            ID        SIZE    MODIFIED
medical-model   xxxxxxx   x.xGB   x seconds ago
```

---

## Step 9 — Run the Model

```bash
ollama run medical-model
```

You can now chat with your model directly in the terminal 🎉

---

## Step 10 — Exit the Container

```bash
exit
```

---

## Step 11 — Test via curl from Outside Container

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "medical-model",
    "messages": [
      {"role": "user", "content": "What is diabetes?"}
    ]
  }'
```

---

## Quick Command Summary

```
docker pull ollama/ollama          → Get Ollama image
docker run ...                     → Start container
docker ps                          → Verify running
docker cp model.gguf ollama:/...   → Copy model into container
docker exec -it ollama bash        → Go inside container
echo "FROM ..." > Modelfile        → Create Modelfile
ollama create medical-model ...    → Create model
ollama list                        → Verify model
ollama run medical-model           → Run and chat
exit                               → Exit container
curl http://localhost:11434/...    → Test from outside
```

---

## Useful Container Management Commands

| Command | Purpose |
|---|---|
| `docker start ollama` | Restart stopped container |
| `docker stop ollama` | Stop running container |
| `docker logs ollama` | Check container logs |
| `docker ps` | List running containers |
| `docker stats ollama` | Check RAM and CPU usage |

---

## Notes

- Model **persists** across restarts because of the `-v ollama:/root/.ollama` volume flag
- Port `11434` is Ollama's default port
- Use `host.docker.internal:11434` to connect from other Docker containers like Open WebUI