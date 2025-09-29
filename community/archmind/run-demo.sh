#!/bin/bash
set -e

echo "ArchMind Demo - Analyzing Next.js Framework"
echo "=============================================="

# Check if API key is set
if [ -z "$QODO_API_KEY" ]; then
    echo ""
    echo "ERROR: Qodo API key required"
    echo "Please set QODO_API_KEY environment variable"
    echo "Get your key from https://qodo.ai"
    echo ""
    echo "Example: export QODO_API_KEY=your_key_here"
    echo ""
    exit 1
fi

# Clone Next.js repository if not exists
if [ ! -d "target-repo" ]; then
    echo "Cloning Next.js repository..."
    git clone --depth 1 https://github.com/vercel/next.js.git target-repo
fi

# Create output directory
mkdir -p output

echo "Starting ArchMind Docker container..."

# Run with explicit agent file specification
docker-compose run --rm archmind qodo archmind \
    --agent-file=/workspace/agent.toml \
    --analysis-depth=deep \
    --generate-docs=true

echo "Analysis complete! Check the output directory for results."
echo "Generated files:"
ls -la output/

echo ""
echo "To run interactive analysis:"
echo "docker-compose run --rm archmind-interactive"