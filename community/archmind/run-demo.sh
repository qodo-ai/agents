#!/bin/bash
set -e

echo "ArchMind Demo - Analyzing Next.js Framework"
echo "==========================================="

# Clone Next.js repository if not exists
if [ ! -d "target-repo" ]; then
    echo "Cloning Next.js repository..."
    git clone --depth 1 https://github.com/vercel/next.js.git target-repo
fi

# Create output directory
mkdir -p output

echo "Starting ArchMind Docker container..."
docker-compose up --build archmind

echo "Analysis complete! Check the output directory for results."
echo "Generated files:"
ls -la output/

echo ""
echo "To run interactive analysis:"
echo "docker-compose run --rm archmind-interactive"
