#!/bin/bash

# Qodo Agent: Changelog Generator - Build Script
set -e

echo "🔨 Building Qodo Agent: Changelog Generator"
echo "============================================="

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local command="$2"
    
    echo -n "Testing: $name... "
    
    if eval "$command" >/dev/null 2>&1; then
        echo "✅ PASS"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo "❌ FAIL"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo
echo "📋 Running validation tests..."

# Test 1: Check Node.js
run_test "Node.js is available" "which node"

# Test 2: Check Qodo CLI
run_test "Qodo CLI is available" "which qodo"

# Test 3: Check configuration files
run_test "TOML configuration exists" "test -f agent.toml"
run_test "YAML configuration exists" "test -f agent.yaml"
run_test "README exists" "test -f README.md"

# Test 4: Check CI configs
run_test "GitHub Actions config exists" "test -f examples/ci-configs/github-actions.yml"
run_test "GitLab CI config exists" "test -f examples/ci-configs/gitlab-ci.yml"

# Test 5: Install dependencies and validate syntax
echo
echo "📦 Installing validation dependencies..."
npm install yaml --no-save --silent >/dev/null 2>&1

run_test "YAML syntax validation" "node -e 'const fs=require(\"fs\"),yaml=require(\"yaml\");yaml.parse(fs.readFileSync(\"agent.yaml\",\"utf8\"))'"

# Test 6: Qodo agent validation
run_test "Qodo recognizes agent" "qodo list-agents | grep -q changelog_generator"

# Cleanup
echo
echo "🧹 Cleaning up..."
rm -rf node_modules package-lock.json 2>/dev/null || true

echo
echo "📊 Build Summary:"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"

if [ $FAILED -eq 0 ]; then
    echo
    echo "🎉 Build successful!"
    echo
    echo "The Qodo Agent: Changelog Generator is ready to use."
    echo
    echo "Usage:"
    echo "  qodo changelog_generator --set repo=owner/repo --set since=v1.0.0"
    exit 0
else
    echo
    echo "❌ Build failed with $FAILED error(s)."
    exit 1
fi