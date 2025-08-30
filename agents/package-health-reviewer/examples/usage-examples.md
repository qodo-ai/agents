# Package Health Reviewer - Usage Examples

This document provides comprehensive examples of using the Package Health Reviewer agent in various scenarios.

## Basic Usage Examples

### 1. Analyze a Popular Package

```bash
qodo --agent-file=agent.toml -y --set package_name="express"
```

**Expected Output:**
```json
{
  "health_score": "healthy",
  "package_name": "express",
  "registry": "npm",
  "overall_score": 95,
  "assessment_date": "2024-01-15T10:30:00Z",
  "security_metrics": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 1,
    "total_vulnerabilities": 1
  },
  "popularity_metrics": {
    "weekly_downloads": "20M+",
    "github_stars": 58000,
    "dependents": 15000
  },
  "maintenance_metrics": {
    "last_update": "2024-01-10",
    "update_frequency": "regular",
    "maintainer_response": "excellent"
  },
  "recommendations": [
    "Safe to use in production environments",
    "Keep updated to latest version",
    "Excellent choice for Node.js web applications"
  ],
  "alternatives": [],
  "snyk_url": "https://snyk.io/advisor/npm-package/express",
  "analysis_summary": "Express is a healthy package with excellent security posture, high popularity, and active maintenance. It's widely adopted and well-maintained, making it a safe choice for production use."
}
```

### 2. Analyze a Risky Package

```bash
qodo --agent-file=agent.toml -y --set package_name="request"
```

**Expected Output:**
```json
{
  "health_score": "risky",
  "package_name": "request",
  "registry": "npm", 
  "overall_score": 25,
  "assessment_date": "2024-01-15T10:35:00Z",
  "security_metrics": {
    "critical": 1,
    "high": 2,
    "medium": 5,
    "low": 3,
    "total_vulnerabilities": 11
  },
  "popularity_metrics": {
    "weekly_downloads": "15M+",
    "github_stars": 25000,
    "dependents": 50000
  },
  "maintenance_metrics": {
    "last_update": "2020-02-11",
    "update_frequency": "none",
    "maintainer_response": "deprecated"
  },
  "recommendations": [
    "⚠️ This package is deprecated and should not be used",
    "Migrate to modern alternatives immediately",
    "Security vulnerabilities will not be fixed"
  ],
  "alternatives": [
    "axios - Modern HTTP client with better security",
    "node-fetch - Lightweight fetch API implementation", 
    "got - Human-friendly HTTP request library"
  ],
  "snyk_url": "https://snyk.io/advisor/npm-package/request",
  "analysis_summary": "Request is a risky package that has been deprecated since 2020. Despite high popularity, it contains multiple security vulnerabilities that will not be fixed. Immediate migration to modern alternatives is strongly recommended."
}
```

### 3. Minimal Output Mode

```bash
qodo --agent-file=agent.toml -y \
  --set package_name="lodash" \
  --set include_details=false
```

**Expected Output:**
```json
{
  "health_score": "sustainable",
  "package_name": "lodash",
  "registry": "npm",
  "overall_score": 78,
  "assessment_date": "2024-01-15T10:40:00Z",
  "analysis_summary": "Lodash is a sustainable package with good popularity but some maintenance concerns. While still widely used, consider modern alternatives for new projects."
}
```

## Advanced Usage Scenarios

### 4. Batch Analysis Script

Create a script to analyze multiple packages:

```bash
#!/bin/bash
# analyze-dependencies.sh

packages=("express" "react" "lodash" "moment" "request" "axios")

echo "Package Health Analysis Report"
echo "=============================="
echo ""

for package in "${packages[@]}"; do
    echo "Analyzing: $package"
    echo "-------------------"
    
    result=$(qodo --agent-file=agent.toml -y --set package_name="$package" --set include_details=false)
    
    # Extract health score and overall score
    health_score=$(echo "$result" | jq -r '.health_score')
    overall_score=$(echo "$result" | jq -r '.overall_score')
    
    echo "Health Score: $health_score ($overall_score/100)"
    echo ""
    
    # Add delay to be respectful
    sleep 2
done
```

### 5. CI/CD Integration Examples

#### GitHub Actions Workflow

```yaml
# .github/workflows/package-health-check.yml
name: Package Health Check

on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          
      - name: Install Playwright
        run: |
          npm install playwright
          npx playwright install chromium
          
      - name: Extract new dependencies
        id: deps
        run: |
          # Extract dependencies from package.json
          NEW_DEPS=$(jq -r '.dependencies | keys[]' package.json)
          echo "dependencies=$NEW_DEPS" >> $GITHUB_OUTPUT
          
      - name: Check package health
        run: |
          echo "Checking health of new dependencies..."
          
          for dep in ${{ steps.deps.outputs.dependencies }}; do
            echo "Analyzing: $dep"
            
            result=$(qodo --agent-file=agents/package-health-reviewer/agent.toml -y \
              --set package_name="$dep" \
              --ci)
            
            health_score=$(echo "$result" | jq -r '.health_score')
            
            if [ "$health_score" = "risky" ]; then
              echo "❌ RISKY package detected: $dep"
              echo "$result" | jq '.recommendations[]'
              exit 1
            elif [ "$health_score" = "sustainable" ]; then
              echo "⚠️ SUSTAINABLE package: $dep (review recommended)"
            else
              echo "✅ HEALTHY package: $dep"
            fi
            
            sleep 1
          done
```

#### GitLab CI Configuration

```yaml
# .gitlab-ci.yml
stages:
  - health-check

package-health-check:
  stage: health-check
  image: node:18
  
  before_script:
    - npm install playwright
    - npx playwright install chromium
    
  script:
    - |
      # Check specific packages
      packages=("express" "lodash" "axios")
      
      for package in "${packages[@]}"; do
        echo "Checking health of: $package"
        
        result=$(qodo --agent-file=agents/package-health-reviewer/agent.toml -y \
          --set package_name="$package" \
          --ci)
        
        health_score=$(echo "$result" | jq -r '.health_score')
        
        if [ "$health_score" = "risky" ]; then
          echo "RISKY package detected: $package"
          exit 1
        fi
      done
      
  only:
    changes:
      - package.json
      - package-lock.json
```

### 6. Pre-commit Hook Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: package-health-check
        name: Package Health Check
        entry: bash -c 'qodo --agent-file=agents/package-health-reviewer/agent.toml -y --set package_name="$1" --ci'
        language: system
        files: package\.json$
        pass_filenames: false
```

### 7. Custom Scoring Thresholds

For organizations with specific security requirements:

```bash
# High-security environment (only allow healthy packages)
qodo --agent-file=agent.toml -y --set package_name="some-package"

# Check exit code for CI/CD
if [ $? -ne 0 ]; then
    echo "Package failed health check - blocking deployment"
    exit 1
fi
```

### 8. Integration with Package Managers

#### npm Integration

```bash
# Check before installing
check_and_install() {
    local package=$1
    
    echo "Checking health of: $package"
    result=$(qodo --agent-file=agent.toml -y --set package_name="$package")
    health_score=$(echo "$result" | jq -r '.health_score')
    
    case $health_score in
        "healthy")
            echo "✅ Installing healthy package: $package"
            npm install "$package"
            ;;
        "sustainable") 
            echo "⚠️ Installing sustainable package: $package (review recommended)"
            npm install "$package"
            ;;
        "risky")
            echo "❌ Risky package detected: $package"
            echo "Alternatives:"
            echo "$result" | jq -r '.alternatives[]'
            echo "Install anyway? (y/N)"
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                npm install "$package"
            fi
            ;;
    esac
}

# Usage
check_and_install "express"
check_and_install "request"
```

## Testing Examples

### 9. Test Suite for Different Package Types

```bash
#!/bin/bash
# test-package-health.sh

echo "Running Package Health Test Suite"
echo "================================="

# Test cases with expected outcomes
declare -A test_cases=(
    ["express"]="healthy"
    ["react"]="healthy" 
    ["lodash"]="sustainable"
    ["moment"]="sustainable"
    ["request"]="risky"
    ["colors"]="risky"
)

passed=0
failed=0

for package in "${!test_cases[@]}"; do
    expected="${test_cases[$package]}"
    
    echo "Testing: $package (expected: $expected)"
    
    result=$(qodo --agent-file=agent.toml -y \
      --set package_name="$package" \
      --set include_details=false)
    
    actual=$(echo "$result" | jq -r '.health_score')
    
    if [ "$actual" = "$expected" ]; then
        echo "✅ PASS: $package -> $actual"
        ((passed++))
    else
        echo "❌ FAIL: $package -> expected: $expected, got: $actual"
        ((failed++))
    fi
    
    echo ""
    sleep 1
done

echo "Test Results:"
echo "Passed: $passed"
echo "Failed: $failed"

if [ $failed -gt 0 ]; then
    exit 1
fi
```

### 10. Performance Testing

```bash
#!/bin/bash
# performance-test.sh

packages=("express" "react" "vue" "angular" "lodash")

echo "Performance Test - Package Health Analysis"
echo "=========================================="

total_time=0

for package in "${packages[@]}"; do
    echo "Analyzing: $package"
    
    start_time=$(date +%s.%N)
    
    qodo --agent-file=agent.toml -y \
      --set package_name="$package" \
      --set include_details=false > /dev/null
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    total_time=$(echo "$total_time + $duration" | bc)
    
    echo "Time: ${duration}s"
    echo ""
done

average_time=$(echo "scale=2; $total_time / ${#packages[@]}" | bc)
echo "Average analysis time: ${average_time}s"
echo "Total time: ${total_time}s"
```

## Error Handling Examples

### 11. Handling Non-existent Packages

```bash
qodo --agent-file=agent.toml -y --set package_name="this-package-does-not-exist-12345"
```

**Expected Error Response:**
```json
{
  "error": "Package not found",
  "package_name": "this-package-does-not-exist-12345",
  "registry": "npm",
  "message": "Package 'this-package-does-not-exist-12345' was not found on npm registry or Snyk Advisor",
  "suggestions": [
    "Check package name spelling",
    "Verify package exists on npm registry",
    "Try searching for similar package names"
  ]
}
```

### 12. Network Error Handling

```bash
# Simulate network issues (disconnect internet)
qodo --agent-file=agent.toml -y --set package_name="express"
```

**Expected Error Response:**
```json
{
  "error": "Network error",
  "package_name": "express", 
  "registry": "npm",
  "message": "Failed to fetch data from Snyk Advisor due to network issues",
  "retry_suggestions": [
    "Check internet connection",
    "Verify firewall settings",
    "Try again in a few minutes"
  ]
}
```

## Best Practices

### 13. Recommended Usage Patterns

```bash
# 1. Always check critical dependencies
critical_packages=("express" "react" "axios")
for pkg in "${critical_packages[@]}"; do
    qodo --agent-file=agent.toml -y --set package_name="$pkg"
done

# 2. Use in dependency review process
echo "New dependency: $NEW_PACKAGE"
qodo --agent-file=agent.toml -y --set package_name="$NEW_PACKAGE"

# 3. Regular health audits
qodo --agent-file=agent.toml -y --set package_name="$pkg" | \
  jq '.health_score, .overall_score, .recommendations[]'
```

These examples demonstrate the versatility and power of the Package Health Reviewer agent across different use cases and environments.