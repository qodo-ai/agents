#!/bin/bash

# Test script for chunked generation functionality
# Tests the ability to generate massive projects with tens of thousands of lines

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

print_status() { echo -e "${BLUE}▶${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_header() { echo -e "${BOLD}${BLUE}$1${NC}"; }

# Test cases for massive project generation
test_cases=(
    "enterprise e-commerce platform with microservices architecture, user management, product catalog, shopping cart, payment processing, order management, inventory tracking, analytics dashboard, and admin panel|python|django|3000"
    "complete 3D game engine with physics simulation, rendering pipeline, asset management, scripting system, audio engine, networking, and editor tools|python|pygame|2500"
    "comprehensive machine learning platform with data ingestion, preprocessing, model training, hyperparameter optimization, model serving, monitoring, and MLOps pipeline|python|pytorch|4000"
    "full-stack social media application with real-time messaging, content feeds, user profiles, media sharing, notifications, moderation tools, and analytics|javascript|react|3500"
    "enterprise resource planning system with accounting, inventory, human resources, customer relationship management, project management, and reporting modules|python|django|5000"
)

# Function to count lines in a directory
count_lines() {
    local dir="$1"
    if [ -d "$dir" ]; then
        find "$dir" -type f \( -name "*.py" -o -name "*.js" -o -name "*.html" -o -name "*.css" -o -name "*.md" \) -exec wc -l {} + | tail -1 | awk '{print $1}'
    else
        echo "0"
    fi
}

# Function to count files in a directory
count_files() {
    local dir="$1"
    if [ -d "$dir" ]; then
        find "$dir" -type f | wc -l
    else
        echo "0"
    fi
}

# Function to test chunked generation
test_chunked_generation() {
    local test_case="$1"
    local test_num="$2"
    
    IFS='|' read -r prompt language framework chunk_size <<< "$test_case"
    
    print_header "Test $test_num: Chunked Generation"
    print_status "Prompt: $prompt"
    print_status "Language: $language"
    print_status "Framework: $framework"
    print_status "Max chunk size: $chunk_size"
    
    # Generate project name for this test
    local project_name="test-chunked-$test_num"
    
    # Run chunked generation
    print_status "Running chunked generation..."
    
    # Use timeout to prevent hanging
    if timeout 600 ./generate.sh --chunked "$prompt" "$language" "$framework" "$chunk_size"; then
        print_success "Chunked generation completed"
        
        # Find the generated project directory
        local generated_dir=$(find generated/ -name "*$(echo "$prompt" | head -c 20 | tr ' ' '-' | tr '[:upper:]' '[:lower:]')*" -type d | head -1)
        
        if [ -z "$generated_dir" ]; then
            # Fallback: find the most recent directory
            generated_dir=$(find generated/ -type d -name "*" | grep -v "\.git" | sort | tail -1)
        fi
        
        if [ -n "$generated_dir" ] && [ -d "$generated_dir" ]; then
            print_status "Analyzing generated project: $generated_dir"
            
            # Count lines and files
            local total_lines=$(count_lines "$generated_dir")
            local total_files=$(count_files "$generated_dir")
            
            print_status "Total lines generated: $total_lines"
            print_status "Total files generated: $total_files"
            
            # Check if it's a massive project (should be > 5000 lines for chunked generation)
            if [ "$total_lines" -gt 5000 ]; then
                print_success "✓ Massive project generated successfully ($total_lines lines)"
            elif [ "$total_lines" -gt 1000 ]; then
                print_warning "⚠ Large project generated ($total_lines lines) - expected massive project"
            else
                print_warning "⚠ Small project generated ($total_lines lines) - chunking may not have been effective"
            fi
            
            # Check for multiple components/chunks
            local chunk_dirs=$(find "$generated_dir" -mindepth 1 -maxdepth 2 -type d | wc -l)
            if [ "$chunk_dirs" -gt 5 ]; then
                print_success "✓ Multiple components detected ($chunk_dirs directories)"
            else
                print_warning "⚠ Few components detected ($chunk_dirs directories)"
            fi
            
            # Check for documentation
            if find "$generated_dir" -name "README.md" -o -name "ARCHITECTURE.md" | grep -q .; then
                print_success "✓ Documentation generated"
            else
                print_warning "⚠ No documentation found"
            fi
            
            # Check for tests
            if find "$generated_dir" -name "*test*" -type f | grep -q .; then
                print_success "✓ Tests generated"
            else
                print_warning "⚠ No tests found"
            fi
            
            return 0
        else
            print_error "✗ No generated project directory found"
            return 1
        fi
    else
        print_error "✗ Chunked generation failed or timed out"
        return 1
    fi
}

# Function to run all tests
run_all_tests() {
    print_header "🧪 Testing MasterMindAI Chunked Generation"
    print_status "Testing the ability to generate massive projects with intelligent chunking"
    echo ""
    
    local total_tests=${#test_cases[@]}
    local passed_tests=0
    local failed_tests=0
    
    for i in "${!test_cases[@]}"; do
        local test_num=$((i + 1))
        echo ""
        print_header "═══════════════════════════════════════════════════════════════"
        
        if test_chunked_generation "${test_cases[$i]}" "$test_num"; then
            passed_tests=$((passed_tests + 1))
            print_success "Test $test_num PASSED"
        else
            failed_tests=$((failed_tests + 1))
            print_error "Test $test_num FAILED"
        fi
        
        echo ""
        print_status "Progress: $test_num/$total_tests tests completed"
        
        # Add delay between tests to avoid overwhelming the system
        if [ "$test_num" -lt "$total_tests" ]; then
            print_status "Waiting 10 seconds before next test..."
            sleep 10
        fi
    done
    
    # Final summary
    echo ""
    print_header "═══════════════════════════════════════════════════════════════"
    print_header "🎯 Test Results Summary"
    echo ""
    print_status "Total tests: $total_tests"
    print_success "Passed: $passed_tests"
    if [ "$failed_tests" -gt 0 ]; then
        print_error "Failed: $failed_tests"
    else
        print_success "Failed: $failed_tests"
    fi
    
    # Calculate success rate
    local success_rate=$((passed_tests * 100 / total_tests))
    print_status "Success rate: $success_rate%"
    
    if [ "$success_rate" -ge 80 ]; then
        print_success "🎉 Chunked generation is working excellently!"
    elif [ "$success_rate" -ge 60 ]; then
        print_warning "⚠ Chunked generation is working but needs improvement"
    else
        print_error "✗ Chunked generation needs significant fixes"
    fi
    
    # Show generated projects
    echo ""
    print_header "📁 Generated Projects"
    if [ -d "generated" ]; then
        for dir in generated/*/; do
            if [ -d "$dir" ]; then
                local lines=$(count_lines "$dir")
                local files=$(count_files "$dir")
                print_status "$(basename "$dir"): $lines lines, $files files"
            fi
        done
    fi
    
    return $failed_tests
}

# Function to test a single massive project
test_single_massive() {
    local prompt="$1"
    local language="${2:-python}"
    local framework="${3:-django}"
    local chunk_size="${4:-3000}"
    
    print_header "🚀 Testing Single Massive Project"
    print_status "Prompt: $prompt"
    print_status "Language: $language"
    print_status "Framework: $framework"
    print_status "Chunk size: $chunk_size"
    echo ""
    
    test_chunked_generation "$prompt|$language|$framework|$chunk_size" "1"
}

# Main execution
main() {
    # Check if generate.sh exists
    if [ ! -f "generate.sh" ]; then
        print_error "generate.sh not found. Please run this script from the MasterMindAI directory."
        exit 1
    fi
    
    # Make sure generate.sh is executable
    chmod +x generate.sh
    
    # Check command line arguments
    if [ "$1" = "--single" ]; then
        # Test single project
        shift
        test_single_massive "$@"
    elif [ "$1" = "--help" ]; then
        echo "Usage:"
        echo "  $0                    # Run all chunked generation tests"
        echo "  $0 --single \"prompt\" [language] [framework] [chunk_size]"
        echo ""
        echo "Examples:"
        echo "  $0 --single \"enterprise CRM system\" python django 4000"
        echo "  $0 --single \"complete game engine\" python pygame 3000"
        exit 0
    else
        # Run all tests
        run_all_tests
    fi
}

# Run main function with all arguments
main "$@"