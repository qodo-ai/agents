# Local Development with ArchMind

## Analyzing Your Current Project

### Quick Setup
```bash
# Navigate to your project directory
cd /path/to/your/project

# Run ArchMind analysis
docker run --rm \
  -v $PWD:/workspace \
  -v $PWD/architecture-analysis:/workspace/analysis \
  ghcr.io/qodo-ai/archmind:latest

# View results
open architecture-analysis/architecture-overview.md
```

### Detailed Analysis
```bash
# Run comprehensive analysis with custom settings
docker run --rm \
  -v $PWD:/workspace \
  -v $PWD/architecture-analysis:/workspace/analysis \
  ghcr.io/qodo-ai/archmind:latest \
  qodo archmind \
  --analysis-depth=expert \
  --include-diagrams=true \
  --focus-area=all \
  --max-file-count=50000
```

## Interactive Development

### Start Interactive Container
```bash
# Start interactive session
docker run --rm -it \
  -v $PWD:/workspace \
  -v $PWD/architecture-analysis:/workspace/analysis \
  ghcr.io/qodo-ai/archmind:latest /bin/sh

# Inside container, run various analyses
qodo archmind --analysis-depth=quick --focus-area=dependencies
qodo archmind --analysis-depth=deep --focus-area=patterns
qodo archmind --analysis-depth=expert --include-diagrams=true
```

### Multiple Analysis Runs
```bash
# Run different analyses for different purposes
docker run --rm -v $PWD:/workspace ghcr.io/qodo-ai/archmind:latest \
  qodo archmind --analysis-depth=quick --output-format=json > quick-metrics.json

docker run --rm -v $PWD:/workspace ghcr.io/qodo-ai/archmind:latest \
  qodo archmind --focus-area=security --output-format=markdown > security-report.md

docker run --rm -v $PWD:/workspace ghcr.io/qodo-ai/archmind:latest \
  qodo archmind --focus-area=performance --include-diagrams=true
```

## Continuous Analysis

### Git Hook Integration
Add this to your `.git/hooks/post-commit`:

```bash
#!/bin/bash
# Post-commit architectural analysis

echo "Running architectural analysis..."
docker run --rm \
  -v $PWD:/workspace \
  -v $PWD/.architecture:/workspace/analysis \
  ghcr.io/qodo-ai/archmind:latest \
  qodo archmind --analysis-depth=quick --generate-docs=false

# Check for significant architectural changes
if [ -f ".architecture/metrics.json" ]; then
  health_score=$(grep -o '"health_score":[0-9]*' .architecture/metrics.json | cut -d: -f2)
  if [ "$health_score" -lt 6 ]; then
    echo "Warning: Architecture health score dropped to $health_score"
  fi
fi
```

Make it executable:
```bash
chmod +x .git/hooks/post-commit
```

### Pre-push Analysis
Add this to your `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Pre-push architectural validation

echo "Validating architecture before push..."
docker run --rm \
  -v $PWD:/workspace \
  ghcr.io/qodo-ai/archmind:latest \
  qodo archmind --analysis-depth=standard --output-format=json > /tmp/arch-check.json

# Check if architecture meets standards
complexity=$(grep -o '"complexity_score":[0-9]*' /tmp/arch-check.json | cut -d: -f2)
if [ "$complexity" -gt 8 ]; then
  echo "Error: Code complexity too high ($complexity). Consider refactoring."
  exit 1
fi

echo "Architecture validation passed!"
```

## IDE Integration

### VS Code Task
Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "ArchMind Analysis",
      "type": "shell",
      "command": "docker",
      "args": [
        "run", "--rm",
        "-v", "${workspaceFolder}:/workspace",
        "-v", "${workspaceFolder}/architecture:/workspace/analysis",
        "ghcr.io/qodo-ai/archmind:latest"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

### IntelliJ External Tool
1. Go to File → Settings → Tools → External Tools
2. Add new tool:
   - **Name**: ArchMind Analysis
   - **Program**: docker
   - **Arguments**: `run --rm -v $ProjectFileDir$:/workspace ghcr.io/qodo-ai/archmind:latest`
   - **Working Directory**: `$ProjectFileDir$`

## Project-Specific Configuration

### Custom Analysis Configuration
Create `.archmind.toml` in your project root:

```toml
[analysis]
depth = "deep"
focus_areas = ["patterns", "dependencies"]
exclude_patterns = ["vendor/", "node_modules/", "*.test.js"]
max_file_count = 25000

[output]
format = "markdown"
include_diagrams = true
diagram_formats = ["svg", "png"]

[quality_gates]
min_health_score = 7
max_complexity_score = 6
```

### Language-Specific Examples

#### JavaScript/TypeScript Projects
```bash
docker run --rm -v $PWD:/workspace ghcr.io/qodo-ai/archmind:latest \
  qodo archmind \
  --exclude-patterns="node_modules,dist,build,.next" \
  --focus-area=patterns \
  --max-file-count=10000
```

#### Python Projects
```bash
docker run --rm -v $PWD:/workspace ghcr.io/qodo-ai/archmind:latest \
  qodo archmind \
  --exclude-patterns="__pycache__,.venv,venv,*.pyc" \
  --focus-area=dependencies \
  --analysis-depth=deep
```

#### Java Projects
```bash
docker run --rm -v $PWD:/workspace ghcr.io/qodo-ai/archmind:latest \
  qodo archmind \
  --exclude-patterns="target/,*.class,.gradle" \
  --focus-area=all \
  --include-diagrams=true
```

## Troubleshooting

### Common Issues

**Docker Permission Errors**
```bash
# Fix permission issues on Linux
sudo chown -R $USER:$USER architecture-analysis/
```

**Large Repository Analysis**
```bash
# For very large repositories, increase memory and use exclusions
docker run --rm -m 4g \
  -v $PWD:/workspace \
  ghcr.io/qodo-ai/archmind:latest \
  qodo archmind \
  --max-file-count=5000 \
  --exclude-patterns="vendor,node_modules,dist,build"
```

**Network Issues**
```bash
# Use local image if network is limited
docker build -t local-archmind .
docker run --rm -v $PWD:/workspace local-archmind:latest
```

### Performance Optimization

**For Large Codebases (1M+ lines)**
- Use `--analysis-depth=quick` for initial assessment
- Focus on specific areas with `--focus-area`
- Exclude generated files and dependencies
- Consider analyzing subsections separately

**For Frequent Analysis**
- Use Docker layer caching
- Mount analysis directory for result persistence
- Implement incremental analysis workflows
