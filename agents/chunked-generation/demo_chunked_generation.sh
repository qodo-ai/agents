#!/bin/bash

# Demo script for MasterMindAI Chunked Generation
# Demonstrates the ability to generate massive projects with tens of thousands of lines

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

# Function to count lines in a directory
count_lines() {
    local dir="$1"
    if [ -d "$dir" ]; then
        find "$dir" -type f \( -name "*.py" -o -name "*.js" -o -name "*.html" -o -name "*.css" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "0"
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

# Demo projects for chunked generation
demo_projects=(
    "enterprise e-commerce platform with microservices|python|django"
    "complete machine learning platform|python|pytorch"
    "full-stack social media application|javascript|react"
    "enterprise resource planning system|python|django"
    "comprehensive game engine|python|pygame"
)

# Function to run a demo
run_demo() {
    local project_info="$1"
    local demo_num="$2"
    
    IFS='|' read -r prompt language framework <<< "$project_info"
    
    print_header "🚀 Demo $demo_num: Chunked Generation"
    print_status "Project: $prompt"
    print_status "Language: $language"
    print_status "Framework: $framework"
    echo ""
    
    # Run chunked generation with timeout
    print_status "Generating massive project..."
    
    local start_time=$(date +%s)
    
    if timeout 300 ./generate.sh --chunked "$prompt" "$language" "$framework" 3000; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        print_success "Generation completed in ${duration}s"
        
        # Find the generated project
        local project_name=$(echo "$prompt" | head -c 20 | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
        local generated_dir=$(find generated/ -name "*$project_name*" -type d | head -1)
        
        if [ -z "$generated_dir" ]; then
            generated_dir=$(find generated/ -type d -name "*" | grep -v "\.git" | sort | tail -1)
        fi
        
        if [ -n "$generated_dir" ] && [ -d "$generated_dir" ]; then
            print_status "Analyzing generated project: $generated_dir"
            
            local total_lines=$(count_lines "$generated_dir")
            local total_files=$(count_files "$generated_dir")
            
            print_status "📊 Results:"
            print_status "  • Total lines: $total_lines"
            print_status "  • Total files: $total_files"
            print_status "  • Generation time: ${duration}s"
            
            # Check if it's a massive project
            if [ "$total_lines" -gt 10000 ]; then
                print_success "🎉 MASSIVE PROJECT GENERATED! ($total_lines lines)"
            elif [ "$total_lines" -gt 5000 ]; then
                print_success "✓ Large project generated ($total_lines lines)"
            elif [ "$total_lines" -gt 1000 ]; then
                print_warning "⚠ Medium project generated ($total_lines lines)"
            else
                print_warning "⚠ Small project generated ($total_lines lines)"
            fi
            
            # Show project structure
            print_status "📁 Project structure:"
            if command -v tree >/dev/null 2>&1; then
                tree "$generated_dir" -L 3 -I "__pycache__|*.pyc|node_modules" | head -20
            else
                find "$generated_dir" -type d | head -10 | sed 's|^|  |'
            fi
            
            return 0
        else
            print_error "No generated project found"
            return 1
        fi
    else
        print_error "Generation failed or timed out"
        return 1
    fi
}

# Main demo function
main() {
    print_header "🤖 MasterMindAI Chunked Generation Demo"
    print_status "Demonstrating the ability to generate massive projects with tens of thousands of lines"
    echo ""
    
    # Check if generate.sh exists
    if [ ! -f "generate.sh" ]; then
        print_error "generate.sh not found. Please run this script from the MasterMindAI directory."
        exit 1
    fi
    
    # Make sure generate.sh is executable
    chmod +x generate.sh
    
    if [ "$1" = "--all" ]; then
        # Run all demos
        local total_demos=${#demo_projects[@]}
        local successful_demos=0
        
        for i in "${!demo_projects[@]}"; do
            local demo_num=$((i + 1))
            echo ""
            print_header "═══════════════════════════════════════════════════════════════"
            
            if run_demo "${demo_projects[$i]}" "$demo_num"; then
                successful_demos=$((successful_demos + 1))
                print_success "Demo $demo_num completed successfully"
            else
                print_error "Demo $demo_num failed"
            fi
            
            echo ""
            print_status "Progress: $demo_num/$total_demos demos completed"
            
            # Wait between demos
            if [ "$demo_num" -lt "$total_demos" ]; then
                print_status "Waiting 30 seconds before next demo..."
                sleep 30
            fi
        done
        
        # Final summary
        echo ""
        print_header "═══════════════════════════════════════════════════════════════"
        print_header "🎯 Demo Results Summary"
        echo ""
        print_status "Total demos: $total_demos"
        print_success "Successful: $successful_demos"
        print_error "Failed: $((total_demos - successful_demos))"
        
        local success_rate=$((successful_demos * 100 / total_demos))
        print_status "Success rate: $success_rate%"
        
        if [ "$success_rate" -ge 80 ]; then
            print_success "🎉 Chunked generation is working excellently!"
        elif [ "$success_rate" -ge 60 ]; then
            print_warning "⚠ Chunked generation is working but could be improved"
        else
            print_error "✗ Chunked generation needs improvement"
        fi
        
    elif [ "$1" = "--quick" ]; then
        # Quick demo with one project
        print_status "Running quick demo with enterprise e-commerce platform..."
        run_demo "${demo_projects[0]}" "1"
        
    elif [ -n "$1" ]; then
        # Custom demo
        local prompt="$1"
        local language="${2:-python}"
        local framework="${3:-django}"
        
        print_status "Running custom demo..."
        run_demo "$prompt|$language|$framework" "Custom"
        
    else
        # Interactive demo
        print_status "Available demo projects:"
        for i in "${!demo_projects[@]}"; do
            local demo_num=$((i + 1))
            IFS='|' read -r prompt language framework <<< "${demo_projects[$i]}"
            print_status "  $demo_num. $prompt ($language + $framework)"
        done
        echo ""
        
        read -p "Select demo number (1-${#demo_projects[@]}) or 'all' for all demos: " choice
        
        if [ "$choice" = "all" ]; then
            exec "$0" --all
        elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#demo_projects[@]}" ]; then
            local selected_index=$((choice - 1))
            run_demo "${demo_projects[$selected_index]}" "$choice"
        else
            print_error "Invalid selection"
            exit 1
        fi
    fi
    
    # Show all generated projects
    echo ""
    print_header "📁 All Generated Projects"
    if [ -d "generated" ]; then
        for dir in generated/*/; do
            if [ -d "$dir" ]; then
                local lines=$(count_lines "$dir")
                local files=$(count_files "$dir")
                local size_indicator=""
                
                if [ "$lines" -gt 10000 ]; then
                    size_indicator="🔥 MASSIVE"
                elif [ "$lines" -gt 5000 ]; then
                    size_indicator="🚀 LARGE"
                elif [ "$lines" -gt 1000 ]; then
                    size_indicator="📦 MEDIUM"
                else
                    size_indicator="📄 SMALL"
                fi
                
                print_status "$size_indicator $(basename "$dir"): $lines lines, $files files"
            fi
        done
    else
        print_warning "No generated projects found"
    fi
}

# Show usage if --help
if [ "$1" = "--help" ]; then
    echo "MasterMindAI Chunked Generation Demo"
    echo ""
    echo "Usage:"
    echo "  $0                    # Interactive demo"
    echo "  $0 --quick           # Quick demo with one project"
    echo "  $0 --all             # Run all demo projects"
    echo "  $0 \"custom prompt\" [language] [framework]  # Custom demo"
    echo ""
    echo "Examples:"
    echo "  $0 --quick"
    echo "  $0 \"enterprise CRM system\" python django"
    echo "  $0 \"complete game engine\" python pygame"
    exit 0
fi

# Run main function
main "$@"