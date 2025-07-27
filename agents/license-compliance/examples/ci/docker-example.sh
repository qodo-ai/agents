#!/bin/bash
# Docker-based license compliance check
# Usage: ./docker-example.sh /path/to/project

PROJECT_DIR=${1:-$(pwd)}

docker run --rm \
  -v "$PROJECT_DIR:/workspace" \
  -w /workspace \
  ubuntu:latest \
  bash -c "
    apt-get update && apt-get install -y curl jq
    curl -fsSL https://install.qodo.ai | sh
    qodo --agent-file=qodo-agent.toml -y --set directory=./src
  "