# Usage Examples

This document provides comprehensive examples of how to use the License Compliance Agent in different scenarios.

## Basic Usage

### Check a single directory
```bash
qodo --agent-file=qodo-agent.toml -y --set directory=./src
```

### Check with custom policies
```bash
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set allowed_licenses="MIT,BSD-3-Clause,Apache-2.0" \
  --set blocked_licenses="GPL-3.0,AGPL-3.0,SSPL-1.0"
```

### Include development dependencies
```bash
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set ignore_dev_dependencies=false
```

## Project-Specific Examples

### Python Project
```bash
# Check Python project with typical dependencies
qodo --agent-file=qodo-agent.toml -y --set directory=./src

# Strict policy for commercial software
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set allowed_licenses="MIT,BSD-2-Clause,BSD-3-Clause,Apache-2.0" \
  --set blocked_licenses="GPL-2.0,GPL-3.0,LGPL-2.1,LGPL-3.0,AGPL-3.0"
```

### Node.js Project
```bash
# Check npm dependencies
qodo --agent-file=qodo-agent.toml -y --set directory=./src

# Allow common Node.js licenses
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set allowed_licenses="MIT,ISC,BSD-3-Clause,Apache-2.0,Unlicense"
```

### Multi-language Project
```bash
# Check entire project
qodo --agent-file=qodo-agent.toml -y --set directory=.

# Check specific subdirectories
qodo --agent-file=qodo-agent.toml -y --set directory=./backend
qodo --agent-file=qodo-agent.toml -y --set directory=./frontend
```

## CI/CD Integration Examples

### GitHub Actions (Complete Workflow)
```yaml
name: License Compliance

on:
  pull_request:
  push:
    branches: [main]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Qodo
      run: curl -fsSL https://install.qodo.ai | sh
    
    - name: Install jq
      run: sudo apt-get update && sudo apt-get install -y jq
    
    - name: License Compliance Check
      id: license-check
      run: |
        qodo --agent-file=qodo-agent.toml -y --set directory=./src > license-result.json
        echo "result=$(cat license-result.json | jq -r '.safe_to_merge')" >> $GITHUB_OUTPUT
    
    - name: Fail if unsafe
      if: steps.license-check.outputs.result == 'false'
      run: |
        echo "License compliance check failed!"
        cat license-result.json | jq '.'
        exit 1
```

### Pre-commit Hook (Detailed)
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running license compliance check..."

# Check if qodo is installed
if ! command -v qodo &> /dev/null; then
    echo "Error: qodo command not found. Please install Qodo CLI."
    exit 1
fi

# Run license check
if ! qodo --agent-file=qodo-agent.toml -y --set directory=./src; then
    echo "❌ License compliance check failed!"
    echo "Please resolve license issues before committing."
    exit 1
fi

echo "✅ License compliance check passed!"
```

### Makefile Integration
```makefile
.PHONY: license-check license-strict license-report

license-check:
	qodo --agent-file=qodo-agent.toml -y --set directory=./src

license-strict:
	qodo --agent-file=qodo-agent.toml -y \
		--set directory=./src \
		--set allowed_licenses="MIT,BSD-3-Clause,Apache-2.0" \
		--set blocked_licenses="GPL-2.0,GPL-3.0,LGPL-2.1,LGPL-3.0,AGPL-3.0"

license-report:
	qodo --agent-file=qodo-agent.toml -y --set directory=./src > license-report.json
	@echo "License report generated: license-report.json"

ci-check: license-strict
	@echo "CI license check completed"
```

## Advanced Scenarios

### Enterprise Policy
```bash
# Very strict enterprise policy
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set allowed_licenses="MIT,BSD-2-Clause,BSD-3-Clause,Apache-2.0" \
  --set blocked_licenses="GPL-2.0,GPL-3.0,LGPL-2.1,LGPL-3.0,AGPL-3.0,SSPL-1.0,WTFPL" \
  --set ignore_dev_dependencies=true
```

### Open Source Project
```bash
# More permissive for open source
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set allowed_licenses="MIT,BSD-2-Clause,BSD-3-Clause,Apache-2.0,ISC,Unlicense,GPL-3.0" \
  --set blocked_licenses="SSPL-1.0" \
  --set ignore_dev_dependencies=true
```

### Development Environment
```bash
# Include dev dependencies for thorough check
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set ignore_dev_dependencies=false
```

## Batch Processing

### Check Multiple Directories
```bash
#!/bin/bash
# check-all-projects.sh

PROJECTS=("./backend" "./frontend" "./shared" "./tools")

for project in "${PROJECTS[@]}"; do
    echo "Checking $project..."
    if ! qodo --agent-file=qodo-agent.toml -y --set directory="$project"; then
        echo "❌ License check failed for $project"
        exit 1
    fi
    echo "✅ $project passed"
done

echo "🎉 All projects passed license compliance!"
```

### Generate Reports for All Projects
```bash
#!/bin/bash
# generate-reports.sh

PROJECTS=("./backend" "./frontend" "./shared")

for project in "${PROJECTS[@]}"; do
    project_name=$(basename "$project")
    echo "Generating report for $project_name..."
    qodo --agent-file=qodo-agent.toml -y --set directory="$project" > "license-report-$project_name.json"
done

echo "Reports generated for all projects"
```

## Troubleshooting Commands

### Debug Mode
```bash
# Use interactive mode for debugging
qodo chat qodo-agent.toml

# Then ask: "Please check ./src with verbose output and explain any issues found"
```

### Manual Package Check
```bash
# Check specific Python package
curl -s https://pypi.org/pypi/requests/json | jq -r '
  .info.license                                  
  //                                             
  (.info.classifiers[]                           
    | select(test("^License ::"))                
    | sub("^License ::[[:space:]]*"; ""))'

# Check specific npm package
curl -s https://registry.npmjs.org/express | jq -r '.license'
```

### Validate Configuration
```bash
# Test with examples
qodo --agent-file=qodo-agent.toml -y --set directory=./examples/python

# Should output compliance report with detected licenses
```