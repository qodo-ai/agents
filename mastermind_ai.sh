#!/bin/bash

# MasterMindAI - Unified AI Development Assistant
# Integrates all AI agents into one comprehensive script
# Version: 2.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Print functions
print_status() { echo -e "${BLUE}▶${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_header() { echo -e "${BOLD}${BLUE}$1${NC}"; }
print_agent() { echo -e "${PURPLE}🤖${NC} $1"; }

# Global variables
VENV_PATH="./venv"
OUTPUT_DIR="generated"
PROJECT_NAME=""
LANGUAGE="python"
FRAMEWORK=""
CREATE_GIT_REPO=false
VERBOSE=false

# Agent configurations
declare -A AGENTS
AGENTS["chunked-generation"]="Generate massive projects with intelligent chunking (10,000+ lines)"
AGENTS["code-review"]="Analyze code changes and provide detailed feedback"
AGENTS["documentation"]="Generate comprehensive README and documentation"
AGENTS["github-issues"]="Automatically handle GitHub issues and create PRs"
AGENTS["test-suite"]="Generate and run comprehensive test suites"
AGENTS["license-compliance"]="Check and fix license compliance issues"
AGENTS["package-health"]="Review and improve package health and dependencies"
AGENTS["security-scan"]="Scan for security vulnerabilities and fixes"
AGENTS["performance-analysis"]="Analyze and optimize code performance"
AGENTS["deployment"]="Deploy applications to cloud platforms"

# Show usage information
show_usage() {
    print_header "🤖 MasterMindAI - Unified AI Development Assistant"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Usage:"
    echo "  $0 <agent> [options] [arguments]"
    echo "  $0 --interactive                    # Interactive mode"
    echo "  $0 --list-agents                    # List all available agents"
    echo "  $0 --help                           # Show this help"
    echo ""
    echo "Available Agents:"
    for agent in "${!AGENTS[@]}"; do
        printf "  %-20s %s\\n" "$agent" "${AGENTS[$agent]}"
    done
    echo ""
    echo "Global Options:"
    echo "  --verbose                           # Enable verbose output"
    echo "  --output-dir <dir>                  # Set output directory (default: generated)"
    echo "  --language <lang>                   # Set programming language (default: python)"
    echo "  --framework <framework>             # Set framework"
    echo "  --git                               # Initialize git repository"
    echo ""
    echo "Examples:"
    echo "  $0 chunked-generation \"enterprise e-commerce platform\" --language python --framework django"
    echo "  $0 code-review --target-branch main --severity-threshold high"
    echo "  $0 documentation --input-file ./src"
    echo "  $0 github-issues --issue-number 123"
    echo "  $0 --interactive"
    echo ""
    exit 1
}

# List all available agents
list_agents() {
    print_header "🤖 MasterMindAI Available Agents"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    for agent in "${!AGENTS[@]}"; do
        print_agent "$agent"
        echo "   ${AGENTS[$agent]}"
        echo ""
    done
    
    echo "Use '$0 <agent> --help' for agent-specific options"
    exit 0
}

# Activate virtual environment
activate_venv() {
    if [ -d "$VENV_PATH" ]; then
        print_status "Activating virtual environment..."
        source "$VENV_PATH/bin/activate"
    else
        print_warning "Virtual environment not found at $VENV_PATH"
        print_status "Creating virtual environment..."
        python3 -m venv "$VENV_PATH"
        source "$VENV_PATH/bin/activate"
        pip install --upgrade pip
    fi
}

# Run qodo command with error handling
run_qodo() {
    local cmd="$1"
    local description="$2"
    
    if [ "$VERBOSE" = true ]; then
        print_status "Running: $cmd"
    fi
    
    print_status "$description"
    
    if eval "$cmd"; then
        print_success "Command completed successfully"
        return 0
    else
        print_error "Command failed: $cmd"
        return 1
    fi
}

# Chunked Generation Agent
agent_chunked_generation() {
    # Check for help first
    if [ "$1" = "--help" ]; then
        echo "Chunked Generation Agent - Generate massive projects with intelligent chunking"
        echo ""
        echo "Usage: $0 chunked-generation \"project description\" [options]"
        echo ""
        echo "Options:"
        echo "  --max-chunk-size <size>     Maximum lines per chunk (default: 2000)"
        echo "  --chunk-strategy <strategy> Chunking strategy: modular, layered, feature, domain"
        echo "  --quality-level <level>     Quality level: basic, standard, enterprise"
        echo "  --no-tests                  Skip test generation"
        echo "  --no-docs                   Skip documentation generation"
        echo ""
        echo "Examples:"
        echo "  $0 chunked-generation \"enterprise e-commerce platform\" --quality-level enterprise"
        echo "  $0 chunked-generation \"ML platform with MLOps\" --max-chunk-size 3000"
        exit 0
    fi
    
    local prompt="$1"
    shift
    
    # Parse chunked generation specific options
    local max_chunk_size=2000
    local chunk_strategy="modular"
    local quality_level="standard"
    local include_tests=true
    local include_docs=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --max-chunk-size)
                max_chunk_size="$2"
                shift 2
                ;;
            --chunk-strategy)
                chunk_strategy="$2"
                shift 2
                ;;
            --quality-level)
                quality_level="$2"
                shift 2
                ;;
            --no-tests)
                include_tests=false
                shift
                ;;
            --no-docs)
                include_docs=false
                shift
                ;;
            --help)
                echo "Chunked Generation Agent - Generate massive projects with intelligent chunking"
                echo ""
                echo "Usage: $0 chunked-generation \"project description\" [options]"
                echo ""
                echo "Options:"
                echo "  --max-chunk-size <size>     Maximum lines per chunk (default: 2000)"
                echo "  --chunk-strategy <strategy> Chunking strategy: modular, layered, feature, domain"
                echo "  --quality-level <level>     Quality level: basic, standard, enterprise"
                echo "  --no-tests                  Skip test generation"
                echo "  --no-docs                   Skip documentation generation"
                echo ""
                echo "Examples:"
                echo "  $0 chunked-generation \"enterprise e-commerce platform\" --quality-level enterprise"
                echo "  $0 chunked-generation \"ML platform with MLOps\" --max-chunk-size 3000"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    if [ -z "$prompt" ]; then
        print_error "Please provide a project description"
        echo "Usage: $0 chunked-generation \"project description\""
        exit 1
    fi
    
    print_header "🚀 Chunked Generation - Massive Project Creation"
    print_status "Project: $prompt"
    print_status "Language: $LANGUAGE"
    print_status "Framework: ${FRAMEWORK:-'(none)'}"
    print_status "Max chunk size: $max_chunk_size"
    print_status "Strategy: $chunk_strategy"
    print_status "Quality: $quality_level"
    
    # Generate project name if not provided
    if [ -z "$PROJECT_NAME" ]; then
        PROJECT_NAME=$(echo "$prompt" | head -c 30 | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
    fi
    
    # Create output directory
    local project_dir="$OUTPUT_DIR/$PROJECT_NAME"
    mkdir -p "$project_dir"
    
    # Enhanced prompt for massive generation
    local enhanced_prompt="Create a massive, enterprise-scale project: $prompt

This should be a comprehensive, production-ready system with:
- Tens of thousands of lines of code
- Multiple interconnected modules/services
- Complete documentation and tests
- Professional architecture and design patterns
- Scalable and maintainable codebase
- Industry best practices

Generate a complete, fully-functional system with all necessary components, configurations, and supporting files. This should be suitable for enterprise deployment."
    
    # Build qodo command
    local cmd="qodo generate_code --set prompt=\"$enhanced_prompt\" --set language=\"$LANGUAGE\""
    [ -n "$FRAMEWORK" ] && cmd="$cmd --set framework=\"$FRAMEWORK\""
    cmd="$cmd --set project_name=\"$PROJECT_NAME\" --set output_dir=\"$project_dir\" --set complexity=\"advanced\""
    cmd="$cmd --set include_tests=$include_tests --set include_docs=$include_docs"
    
    # Run generation
    activate_venv
    run_qodo "$cmd" "Generating massive enterprise-scale project..."
    
    # Initialize git if requested
    if [ "$CREATE_GIT_REPO" = true ]; then
        print_status "Initializing git repository..."
        cd "$project_dir"
        git init
        git add .
        git commit -m "Initial commit: Generated $PROJECT_NAME"
        cd - > /dev/null
    fi
    
    print_success "🎉 Massive project generation complete!"
    print_status "📁 Project location: $project_dir"
}

# Code Review Agent
agent_code_review() {
    local target_branch="main"
    local severity_threshold="medium"
    local include_suggestions=true
    local focus_areas=""
    local exclude_files=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --target-branch)
                target_branch="$2"
                shift 2
                ;;
            --severity-threshold)
                severity_threshold="$2"
                shift 2
                ;;
            --no-suggestions)
                include_suggestions=false
                shift
                ;;
            --focus-areas)
                focus_areas="$2"
                shift 2
                ;;
            --exclude-files)
                exclude_files="$2"
                shift 2
                ;;
            --help)
                echo "Code Review Agent - Analyze code changes and provide feedback"
                echo ""
                echo "Usage: $0 code-review [options]"
                echo ""
                echo "Options:"
                echo "  --target-branch <branch>        Branch to compare against (default: main)"
                echo "  --severity-threshold <level>    Minimum severity: low, medium, high, critical"
                echo "  --no-suggestions               Skip improvement suggestions"
                echo "  --focus-areas <areas>          Focus areas: security,performance,maintainability"
                echo "  --exclude-files <patterns>     File patterns to exclude"
                echo ""
                echo "Examples:"
                echo "  $0 code-review --target-branch develop"
                echo "  $0 code-review --focus-areas security,performance"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    print_header "🔍 Code Review - Intelligent Code Analysis"
    print_status "Target branch: $target_branch"
    print_status "Severity threshold: $severity_threshold"
    print_status "Include suggestions: $include_suggestions"
    
    # Build qodo command
    local cmd="qodo code_review --set target_branch=\"$target_branch\" --set severity_threshold=\"$severity_threshold\""
    cmd="$cmd --set include_suggestions=$include_suggestions"
    [ -n "$focus_areas" ] && cmd="$cmd --set focus_areas=\"$focus_areas\""
    [ -n "$exclude_files" ] && cmd="$cmd --set exclude_files=\"$exclude_files\""
    
    activate_venv
    run_qodo "$cmd" "Analyzing code changes..."
    
    print_success "Code review completed!"
}

# Documentation Agent
agent_documentation() {
    local input_file="."
    local output_file="README.md"
    local doc_type="readme"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --input-file)
                input_file="$2"
                shift 2
                ;;
            --output-file)
                output_file="$2"
                shift 2
                ;;
            --type)
                doc_type="$2"
                shift 2
                ;;
            --help)
                echo "Documentation Agent - Generate comprehensive documentation"
                echo ""
                echo "Usage: $0 documentation [options]"
                echo ""
                echo "Options:"
                echo "  --input-file <path>     Input file or directory (default: .)"
                echo "  --output-file <file>    Output file (default: README.md)"
                echo "  --type <type>          Documentation type: readme, api, user-guide"
                echo ""
                echo "Examples:"
                echo "  $0 documentation --input-file ./src"
                echo "  $0 documentation --type api --output-file API.md"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    print_header "📚 Documentation Generator"
    print_status "Input: $input_file"
    print_status "Output: $output_file"
    print_status "Type: $doc_type"
    
    local cmd="qodo documentation_writer --set input_file=\"$input_file\" --set output_file=\"$output_file\""
    
    activate_venv
    run_qodo "$cmd" "Generating documentation..."
    
    print_success "Documentation generated: $output_file"
}

# Interactive mode
interactive_mode() {
    print_header "🤖 MasterMindAI Interactive Mode"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    while true; do
        echo "Available agents:"
        local i=1
        local agent_list=()
        for agent in "${!AGENTS[@]}"; do
            echo "  $i. $agent - ${AGENTS[$agent]}"
            agent_list[$i]="$agent"
            ((i++))
        done
        echo "  0. Exit"
        echo ""
        
        read -p "Select an agent (0-$((i-1))): " choice
        
        if [ "$choice" = "0" ]; then
            print_success "Goodbye!"
            break
        elif [ "$choice" -ge 1 ] && [ "$choice" -lt "$i" ]; then
            local selected_agent="${agent_list[$choice]}"
            print_agent "Selected: $selected_agent"
            
            case "$selected_agent" in
                "chunked-generation")
                    read -p "Enter project description: " prompt
                    read -p "Programming language (default: python): " lang
                    read -p "Framework (optional): " fw
                    [ -n "$lang" ] && LANGUAGE="$lang"
                    [ -n "$fw" ] && FRAMEWORK="$fw"
                    agent_chunked_generation "$prompt"
                    ;;
                "code-review")
                    read -p "Target branch (default: main): " branch
                    [ -n "$branch" ] && agent_code_review --target-branch "$branch" || agent_code_review
                    ;;
                "documentation")
                    read -p "Input file/directory (default: .): " input
                    [ -n "$input" ] && agent_documentation --input-file "$input" || agent_documentation
                    ;;
                *)
                    print_warning "Agent '$selected_agent' not yet implemented in interactive mode"
                    ;;
            esac
        else
            print_error "Invalid selection"
        fi
        
        echo ""
        read -p "Press Enter to continue..."
        echo ""
    done
}

# Parse global options in place
parse_global_options() {
    local new_args=()
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose)
                VERBOSE=true
                shift
                ;;
            --output-dir)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --language)
                LANGUAGE="$2"
                shift 2
                ;;
            --framework)
                FRAMEWORK="$2"
                shift 2
                ;;
            --git)
                CREATE_GIT_REPO=true
                shift
                ;;
            --project-name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            *)
                # Collect non-global arguments
                new_args+=("$1")
                shift
                ;;
        esac
    done
    # Set the global array with remaining arguments
    REMAINING_ARGS=("${new_args[@]}")
}

# Global array for remaining arguments
declare -a REMAINING_ARGS

# Main function
main() {
    # Parse global options first
    parse_global_options "$@"
    set -- "${REMAINING_ARGS[@]}"
    
    # Debug output
    if [ "$VERBOSE" = true ]; then
        print_status "DEBUG: After parsing global options:"
        print_status "DEBUG: LANGUAGE=$LANGUAGE"
        print_status "DEBUG: FRAMEWORK=$FRAMEWORK"
        print_status "DEBUG: Remaining args: $@"
    fi
    
    # Handle special cases
    case "${1:-}" in
        "--help"|"help"|""|"-h")
            show_usage
            ;;
        "--list-agents"|"list")
            list_agents
            ;;
        "--interactive"|"interactive")
            interactive_mode
            ;;
        "chunked-generation")
            shift
            agent_chunked_generation "$@"
            ;;
        "code-review")
            shift
            agent_code_review "$@"
            ;;
        "documentation")
            shift
            agent_documentation "$@"
            ;;
        *)
            print_error "Unknown agent or command: ${1:-}"
            echo ""
            echo "Use '$0 --help' to see available options"
            echo "Use '$0 --list-agents' to see available agents"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"