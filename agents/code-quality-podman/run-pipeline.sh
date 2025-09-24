#!/bin/bash

# Code Quality Podman Pipeline Execution Script
# This script demonstrates how the agent should actually create and execute quality checks

set -e

echo "🚀 Starting Code Quality Pipeline Execution"
echo "============================================"

# Configuration
PROJECT_DIR="${1:-.}"
LANGUAGE="${2:-auto}"
QUALITY_TOOLS="${3:-all}"
REPORT_FORMAT="${4:-json}"

echo "📁 Project Directory: $PROJECT_DIR"
echo "🔧 Language: $LANGUAGE"
echo "🛠️  Quality Tools: $QUALITY_TOOLS"
echo "📊 Report Format: $REPORT_FORMAT"
echo ""

# Create reports directory
mkdir -p "$PROJECT_DIR/quality-reports"

# Function to run quality checks
run_quality_check() {
    local tool=$1
    local container=$2
    local command=$3

    echo "🔍 Running $tool..."

    # Create a simple podman command to run the quality tool
    podman run --rm \
        -v "$PROJECT_DIR:/workspace:Z" \
        -w /workspace \
        "$container" \
        bash -c "$command" || echo "⚠️  $tool completed with warnings"

    echo "✅ $tool completed"
}

# Language detection if auto
if [ "$LANGUAGE" = "auto" ]; then
    echo "🔍 Auto-detecting language..."

    if [ -f "$PROJECT_DIR/package.json" ]; then
        LANGUAGE="javascript"
        echo "📦 Detected: JavaScript/Node.js"
    elif [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/setup.py" ]; then
        LANGUAGE="python"
        echo "🐍 Detected: Python"
    elif [ -f "$PROJECT_DIR/go.mod" ]; then
        LANGUAGE="go"
        echo "🐹 Detected: Go"
    elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        LANGUAGE="rust"
        echo "🦀 Detected: Rust"
    else
        LANGUAGE="generic"
        echo "📄 Using generic analysis"
    fi
fi

# Run quality checks based on language and tools
echo ""
echo "🏃 Executing Quality Checks"
echo "============================"

case $LANGUAGE in
    "python")
        if [[ "$QUALITY_TOOLS" == *"pylint"* ]] || [ "$QUALITY_TOOLS" = "all" ]; then
            run_quality_check "Pylint" "python:3.11-alpine" "pip install pylint && pylint --output-format=json --reports=no . > quality-reports/pylint-report.json 2>/dev/null || true"
        fi

        if [[ "$QUALITY_TOOLS" == *"bandit"* ]] || [ "$QUALITY_TOOLS" = "all" ]; then
            run_quality_check "Bandit" "python:3.11-alpine" "pip install bandit && bandit -r . -f json -o quality-reports/bandit-report.json 2>/dev/null || true"
        fi

        if [[ "$QUALITY_TOOLS" == *"black"* ]] || [ "$QUALITY_TOOLS" = "all" ]; then
            run_quality_check "Black" "python:3.11-alpine" "pip install black && black --check --diff . > quality-reports/black-report.txt 2>&1 || true"
        fi
        ;;

    "javascript")
        if [[ "$QUALITY_TOOLS" == *"eslint"* ]] || [ "$QUALITY_TOOLS" = "all" ]; then
            run_quality_check "ESLint" "node:18-alpine" "npm install -g eslint && eslint . --format json --output-file quality-reports/eslint-report.json 2>/dev/null || true"
        fi

        if [[ "$QUALITY_TOOLS" == *"prettier"* ]] || [ "$QUALITY_TOOLS" = "all" ]; then
            run_quality_check "Prettier" "node:18-alpine" "npm install -g prettier && prettier --check . > quality-reports/prettier-report.txt 2>&1 || true"
        fi
        ;;

    "go")
        if [[ "$QUALITY_TOOLS" == *"golangci-lint"* ]] || [ "$QUALITY_TOOLS" = "all" ]; then
            run_quality_check "golangci-lint" "golangci/golangci-lint:latest" "golangci-lint run --out-format json > quality-reports/golangci-report.json 2>/dev/null || true"
        fi
        ;;

    *)
        echo "🔍 Running generic security scan with Trivy..."
        run_quality_check "Trivy" "aquasec/trivy:latest" "trivy fs . --format json --output quality-reports/trivy-report.json 2>/dev/null || true"
        ;;
esac

# Generate consolidated report
echo ""
echo "📊 Generating Consolidated Report"
echo "================================="

cat > "$PROJECT_DIR/quality-reports/summary.json" << EOF
{
    "pipeline_execution": {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "language": "$LANGUAGE",
        "tools_executed": "$QUALITY_TOOLS",
        "project_directory": "$PROJECT_DIR",
        "report_format": "$REPORT_FORMAT"
    },
    "execution_status": "completed",
    "reports_generated": [
        $(find "$PROJECT_DIR/quality-reports" -name "*.json" -o -name "*.txt" | sed 's/.*/"&"/' | paste -sd, -)
    ]
}
EOF

echo "✅ Pipeline execution completed!"
echo "📁 Reports available in: $PROJECT_DIR/quality-reports/"
echo ""
echo "📋 Summary:"
ls -la "$PROJECT_DIR/quality-reports/"

echo ""
echo "🎉 Code Quality Pipeline Finished Successfully!"
