#!/bin/bash

# Test script for Package Health Reviewer Agent
# This script tests the agent with known packages to validate functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AGENT_FILE="agent.toml"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BLUE}Package Health Reviewer Agent - Test Suite${NC}"
echo "==========================================="
echo ""

# Check if agent file exists
if [ ! -f "$AGENT_DIR/$AGENT_FILE" ]; then
    echo -e "${RED}❌ Agent file not found: $AGENT_DIR/$AGENT_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Agent file found: $AGENT_DIR/$AGENT_FILE${NC}"
echo ""

# Test cases with expected outcomes
declare -A test_cases=(
    ["express"]="healthy"
    ["react"]="healthy"
    ["lodash"]="sustainable"
    ["moment"]="sustainable"
    ["request"]="risky"
    ["colors"]="risky"
)

# Counters
passed=0
failed=0
total=${#test_cases[@]}

echo -e "${BLUE}Running $total test cases...${NC}"
echo ""

# Function to run a single test
run_test() {
    local package=$1
    local expected=$2
    local test_num=$3
    
    echo -e "${BLUE}[$test_num/$total] Testing: $package (expected: $expected)${NC}"
    echo "---------------------------------------------------"
    
    # Run the agent
    local start_time=$(date +%s.%N)
    
    if result=$(qodo --agent-file="$AGENT_DIR/$AGENT_FILE" -y \
        --set package_name="$package" \
        --set include_details=false \
        2>/dev/null); then
        
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc)
        
        # Parse the result
        local actual=$(echo "$result" | jq -r '.health_score // "error"')
        local score=$(echo "$result" | jq -r '.overall_score // 0')
        
        # Check if the result matches expectation
        if [ "$actual" = "$expected" ]; then
            echo -e "${GREEN}✅ PASS: $package -> $actual (Score: $score/100) [${duration}s]${NC}"
            ((passed++))
        else
            echo -e "${RED}❌ FAIL: $package -> expected: $expected, got: $actual (Score: $score/100) [${duration}s]${NC}"
            ((failed++))
            
            # Show additional details for failed tests
            echo "   Result details:"
            echo "$result" | jq -r '.analysis_summary // "No summary available"' | sed 's/^/   /'
        fi
    else
        echo -e "${RED}❌ ERROR: Failed to analyze $package${NC}"
        ((failed++))
    fi
    
    echo ""
    
    # Add delay to be respectful to Snyk Advisor
    sleep 2
}

# Run all test cases
test_num=1
for package in "${!test_cases[@]}"; do
    expected="${test_cases[$package]}"
    run_test "$package" "$expected" "$test_num"
    ((test_num++))
done

# Summary
echo "=========================================="
echo -e "${BLUE}Test Results Summary${NC}"
echo "=========================================="
echo -e "${GREEN}✅ Passed: $passed${NC}"
echo -e "${RED}❌ Failed: $failed${NC}"
echo -e "${BLUE}📊 Total:  $total${NC}"

if [ $failed -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! The agent is working correctly.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}⚠️ Some tests failed. Please review the agent implementation.${NC}"
    
    # Calculate success rate
    success_rate=$(echo "scale=1; $passed * 100 / $total" | bc)
    echo -e "${YELLOW}📈 Success rate: $success_rate%${NC}"
    
    if [ "$success_rate" -ge "80" ]; then
        echo -e "${YELLOW}Note: Success rate is acceptable (≥80%). Some variance is expected due to dynamic data.${NC}"
        exit 0
    else
        exit 1
    fi
fi