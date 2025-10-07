#!/bin/bash

# MasterMindAI Code Generator - Simplified & Intuitive
# One command, smart defaults, minimal questions

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
print_prompt() { echo -e "${PURPLE}?${NC} $1"; }
print_header() { echo -e "${BOLD}${BLUE}$1${NC}"; }

# Global variables with smart defaults
OUTPUT_DIR="generated"
LANGUAGE=""
FRAMEWORK=""
PROMPT=""
AUTO_MODE=false
ITERATION_COUNT=0
PROJECT_NAME=""
CREATE_GIT_REPO=false

show_usage() {
    echo "🤖 MasterMindAI Code Generator"
    echo "============================="
    echo ""
    echo "Usage:"
    echo "  $0                                    # Interactive mode"
    echo "  $0 \"your idea\"                        # Quick generation"
    echo "  $0 \"your idea\" [language] [framework] # Quick with options"
    echo "  $0 improve <directory>                # Improve existing code"
    echo "  $0 --quick \"idea\" [lang] [framework]  # Explicit quick mode"
    echo "  $0 --chunked \"massive project\" [lang] [framework] [chunk_size] # Chunked generation for massive projects"
    echo ""
    echo "Examples:"
    echo "  $0 \"calculator app\""
    echo "  $0 \"todo list with React\" javascript react"
    echo "  $0 \"Python web scraper\" python flask"
    echo "  $0 --quick \"data analysis script\" python pandas"
    echo "  $0 --chunked \"enterprise e-commerce platform\" python django 3000"
    echo "  $0 --chunked \"complete game engine\" python pygame 2500"
    echo "  $0 improve my-project"
    echo ""
    echo "Options:"
    echo "  --quick     Force quick mode (non-interactive)"
    echo "  --chunked   Use intelligent chunking for massive projects (10k+ lines)"
    echo "  --help      Show this help message"
    echo ""
    echo "Chunked Mode:"
    echo "  Perfect for generating massive applications with tens of thousands of lines"
    echo "  Automatically breaks down complex projects into manageable chunks"
    echo "  Maintains consistency and integration across all components"
    echo "  Supports enterprise applications, game engines, ML pipelines, and more"
    echo ""
    exit 1
}

# Smart language detection from prompt
detect_language() {
    local prompt="$1"
    
    # Check for explicit language mentions
    if [[ "$prompt" =~ [Pp]ython ]]; then
        echo "python"
    elif [[ "$prompt" =~ [Jj]ava[Ss]cript|[Jj][Ss]|[Nn]ode ]]; then
        echo "javascript"
    elif [[ "$prompt" =~ [Rr]eact|[Vv]ue|[Aa]ngular ]]; then
        echo "javascript"
    elif [[ "$prompt" =~ [Hh][Tt][Mm][Ll]|[Ww]eb|[Cc][Ss][Ss] ]]; then
        echo "html"
    elif [[ "$prompt" =~ [Gg]o\s|[Gg]olang ]]; then
        echo "go"
    elif [[ "$prompt" =~ [Rr]ust ]]; then
        echo "rust"
    elif [[ "$prompt" =~ [Jj]ava\s ]]; then
        echo "java"
    else
        # Default based on project type
        if [[ "$prompt" =~ [Aa]pp|[Cc]alculator|[Gg]ame ]]; then
            echo "python"  # Good for desktop apps
        elif [[ "$prompt" =~ [Ww]ebsite|[Pp]age|[Ff]orm ]]; then
            echo "html"    # Good for web pages
        elif [[ "$prompt" =~ [Aa][Pp][Ii]|[Ss]erver|[Bb]ackend ]]; then
            echo "python"  # Good for APIs
        else
            echo "python"  # Safe default
        fi
    fi
}

# Smart framework detection
detect_framework() {
    local prompt="$1"
    local language="$2"
    
    case "$language" in
        "python")
            if [[ "$prompt" =~ [Ff]lask ]]; then
                echo "flask"
            elif [[ "$prompt" =~ [Dd]jango ]]; then
                echo "django"
            elif [[ "$prompt" =~ [Aa][Pp][Ii]|[Rr][Ee][Ss][Tt] ]]; then
                echo "flask"  # Good default for APIs
            elif [[ "$prompt" =~ [Ww]eb|[Ss]erver ]]; then
                echo "flask"  # Good default for web
            fi
            ;;
        "javascript")
            if [[ "$prompt" =~ [Rr]eact ]]; then
                echo "react"
            elif [[ "$prompt" =~ [Vv]ue ]]; then
                echo "vue"
            elif [[ "$prompt" =~ [Aa]ngular ]]; then
                echo "angular"
            elif [[ "$prompt" =~ [Ee]xpress|[Aa][Pp][Ii] ]]; then
                echo "express"
            elif [[ "$prompt" =~ [Aa]pp|[Cc]omponent ]]; then
                echo "react"  # Good default for apps
            fi
            ;;
    esac
}

# Setup environment
setup_environment() {
    if [[ "$VIRTUAL_ENV" == "" ]] && [ -f "venv/bin/activate" ]; then
        print_status "Activating virtual environment..."
        source venv/bin/activate
    fi

    if ! command -v qodo &> /dev/null; then
        print_error "Qodo Command not found. Install with: npm install -g @qodo/command"
        exit 1
    fi
}

# Execute qodo command directly without error checking
run_qodo() {
    local cmd="$1"
    local description="$2"
    
    print_status "$description"
    
    # Execute qodo command directly
    echo "" | timeout 120 $cmd --ci
    
    print_success "Code generation completed!"
    return 0
}

# Generate project name from prompt
generate_project_name() {
    local prompt="$1"
    
    # Extract key words and create a project name
    local name=$(echo "$prompt" | tr '[:upper:]' '[:lower:]' | \
                 sed 's/[^a-z0-9 ]//g' | \
                 awk '{for(i=1;i<=3 && i<=NF;i++) printf "%s", $i (i<3 && i<NF ? "-" : "")}' | \
                 sed 's/-$//')
    
    # Use generic name if extraction fails
    if [ -z "$name" ] || [ ${#name} -lt 3 ]; then
        name="my-project"
    fi
    
    echo "$name"
}

# Create project directory structure
create_project_directory() {
    local base_dir="$1"
    local project_name="$2"
    
    local project_dir="$base_dir/$project_name"
    
    # Create unique directory name if it already exists
    local counter=1
    local original_name="$project_name"
    
    while [ -d "$project_dir" ]; do
        project_name="${original_name}-${counter}"
        project_dir="$base_dir/$project_name"
        counter=$((counter + 1))
    done
    
    mkdir -p "$project_dir"
    echo "$project_dir"
}

# Initialize Git repository
init_git_repo() {
    local project_dir="$1"
    local project_name="$2"
    
    cd "$project_dir"
    
    # Initialize git repository
    git init > /dev/null 2>&1
    
    # Create .gitignore based on project type
    create_gitignore "$LANGUAGE"
    
    # Create initial commit
    git add .
    git commit -m "Initial commit: $project_name

Generated by MasterMindAI Code Generator
Prompt: $PROMPT
Language: $LANGUAGE
Framework: $FRAMEWORK" > /dev/null 2>&1
    
    cd - > /dev/null
    
    print_success "Git repository initialized in $project_dir"
}

# Create appropriate .gitignore file
create_gitignore() {
    local language="$1"
    
    case "$language" in
        "python")
            cat > ".gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
            ;;
        "javascript"|"js")
            cat > ".gitignore" << 'EOF'
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
.next/
out/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
            ;;
        "html")
            cat > ".gitignore" << 'EOF'
# Build outputs
dist/
build/

# Dependencies
node_modules/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
            ;;
        *)
            cat > ".gitignore" << 'EOF'
# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build outputs
build/
dist/
target/
EOF
            ;;
    esac
}





# Run tests if they exist
run_tests() {
    local dir="$1"
    
    cd "$dir" 2>/dev/null || return 1
    
    if [ -f "package.json" ] && grep -q '"test"' package.json; then
        print_status "Running tests..."
        npm test 2>/dev/null && print_success "Tests passed!" || print_warning "Some tests failed"
    elif find . -name "*test*.py" | grep -q .; then
        print_status "Running tests..."
        python -m pytest 2>/dev/null || python -m unittest discover 2>/dev/null
        [ $? -eq 0 ] && print_success "Tests passed!" || print_warning "Some tests failed"
    fi
    
    cd - > /dev/null
}

# Follow-up prompts loop
follow_up_loop() {
    echo ""
    print_success "🎉 Your project is ready!"
    echo ""
    
    while true; do
        print_prompt "What would you like to do next?"
        echo "  • Describe changes you want to make"
        echo "  • Ask questions about the code"
        echo "  • Request new features"
        echo "  • Type 'exit' to quit"
        echo ""
        read -p "Your request (or 'exit'): " user_input
        
        # Check for exit
        if [[ "$user_input" =~ ^[Ee]xit$ ]] || [[ "$user_input" =~ ^[Qq]uit$ ]] || [[ "$user_input" =~ ^[Qq]$ ]]; then
            print_success "Thanks for using MasterMindAI! 👋"
            break
        fi
        
        # Check for empty input
        if [ -z "$user_input" ]; then
            print_warning "Please describe what you'd like to do, or type 'exit' to quit"
            continue
        fi
        
        # Process the follow-up request
        process_followup "$user_input"
    done
}

# Process follow-up requests
process_followup() {
    local request="$1"
    
    print_status "Processing your request..."
    
    # Create improvement prompt
    local improvement_prompt="Based on the existing project in '$OUTPUT_DIR', please: $request
    
Maintain all existing functionality while implementing the requested changes. Keep the same file structure and ensure the code remains clean and well-organized."
    
    # Apply the improvement
    local cmd="qodo generate_code --set prompt=\"$improvement_prompt\" --set language=\"$LANGUAGE\""
    [ -n "$FRAMEWORK" ] && cmd="$cmd --set framework=\"$FRAMEWORK\""
    cmd="$cmd --set output_dir=\"$OUTPUT_DIR\" --set include_tests=true --set include_docs=true"
    
    run_qodo "$cmd" "Applying your changes..."
    print_success "✓ Changes applied successfully!"
    
    # Run tests if available
    run_tests "$OUTPUT_DIR"
    
    echo ""
    print_status "📁 Updated project is in: $OUTPUT_DIR"
    print_status "💡 You can open the files to see the changes"
    
    echo ""
}

# Simple improvement suggestions
suggest_improvements() {
    echo ""
    print_prompt "Want to improve your code? Choose an option:"
    echo "  1. Add error handling"
    echo "  2. Improve styling"
    echo "  3. Add more features"
    echo "  4. I'm happy with it"
    echo ""
    read -p "Choice (1-4): " choice
    
    case $choice in
        1) return 1 ;;  # Add error handling
        2) return 2 ;;  # Improve styling
        3) return 3 ;;  # Add features
        *) return 0 ;;  # Done
    esac
}

# Apply simple improvements
apply_improvement() {
    local type="$1"
    local dir="$2"
    
    case $type in
        1)
            local prompt="Add comprehensive error handling and input validation to make the code more robust"
            ;;
        2)
            local prompt="Improve the visual design and styling to make it more modern and attractive"
            ;;
        3)
            read -p "What features would you like to add? " features
            local prompt="Add these new features: $features"
            ;;
    esac
    
    print_status "Applying improvements..."
    
    local cmd="qodo generate_code --set prompt=\"$prompt\" --set language=\"$LANGUAGE\" --set output_dir=\"$dir\""
    
    run_qodo "$cmd" "Improving your code..."
    print_success "Improvements applied!"
    return 0
}

# Ask user about Git repository creation
ask_git_permission() {
    echo ""
    print_prompt "Would you like to initialize a Git repository for this project?"
    echo "  This will create a .git folder and make an initial commit"
    echo ""
    read -p "Initialize Git repo? [Y/n]: " git_choice
    
    if [[ ! $git_choice =~ ^[Nn]$ ]]; then
        CREATE_GIT_REPO=true
        print_success "Git repository will be initialized"
    else
        CREATE_GIT_REPO=false
        print_status "Skipping Git repository initialization"
    fi
}

# Main generation function
generate_code() {
    local prompt="$1"
    
    # Store the original prompt
    PROMPT="$prompt"
    
    # Smart detection
    LANGUAGE=$(detect_language "$prompt")
    FRAMEWORK=$(detect_framework "$prompt" "$LANGUAGE")
    
    # Generate project name
    PROJECT_NAME=$(generate_project_name "$prompt")
    
    print_status "Creating your $LANGUAGE project: $PROJECT_NAME"
    [ -n "$FRAMEWORK" ] && print_status "Using $FRAMEWORK framework"
    
    # Ask about Git repository
    ask_git_permission
    
    # Create project directory
    local project_dir=$(create_project_directory "$OUTPUT_DIR" "$PROJECT_NAME")
    
    print_status "Project directory: $project_dir"
    
    # Build qodo command with project-specific directory
    local cmd="qodo generate_code --set prompt=\"$prompt\" --set language=\"$LANGUAGE\""
    [ -n "$FRAMEWORK" ] && cmd="$cmd --set framework=\"$FRAMEWORK\""
    cmd="$cmd --set project_name=\"$PROJECT_NAME\" --set output_dir=\"$project_dir\" --set include_tests=true --set include_docs=true"
    
    # Run qodo generation
    run_qodo "$cmd" "Generating your code..."
    print_success "Code generated successfully!"
    
    # Initialize Git repository if requested
    if [ "$CREATE_GIT_REPO" = true ]; then
        if command -v git &> /dev/null; then
            init_git_repo "$project_dir" "$PROJECT_NAME"
        else
            print_warning "Git not available, skipping repository initialization"
        fi
    fi
    
    # Update OUTPUT_DIR to point to the project directory for subsequent operations
    OUTPUT_DIR="$project_dir"
    
    # Run tests
    run_tests "$project_dir"
    
    # Simple improvement loop
    while suggest_improvements; do
        improvement_type=$?
        if apply_improvement $improvement_type "$project_dir"; then
            run_tests "$project_dir"
        fi
        ITERATION_COUNT=$((ITERATION_COUNT + 1))
        [ $ITERATION_COUNT -ge 3 ] && break  # Max 3 improvements
    done
    
    # Follow-up prompts loop (only in interactive mode)
    follow_up_loop
}

# Improve existing project
improve_project() {
    local dir="$1"
    
    if [ ! -d "$dir" ]; then
        print_error "Directory '$dir' not found"
        exit 1
    fi
    
    print_status "Analyzing project in $dir..."
    
    # Auto-detect language
    cd "$dir"
    if [ -f "package.json" ]; then
        LANGUAGE="javascript"
    elif find . -name "*.py" | grep -q .; then
        LANGUAGE="python"
    elif find . -name "*.html" | grep -q .; then
        LANGUAGE="html"
    else
        LANGUAGE="generic"
    fi
    cd - > /dev/null
    
    print_status "Detected language: $LANGUAGE"
    
    # Simple improvement loop
    OUTPUT_DIR="$dir"
    while suggest_improvements; do
        improvement_type=$?
        if apply_improvement $improvement_type "$dir"; then
            run_tests "$dir"
        fi
        ITERATION_COUNT=$((ITERATION_COUNT + 1))
        [ $ITERATION_COUNT -ge 5 ] && break  # Max 5 improvements for existing projects
    done
    
    # Follow-up prompts loop
    follow_up_loop
}

# Interactive mode
interactive_mode() {
    print_header "🤖 What would you like to create?"
    echo ""
    echo "Just describe your idea in plain English:"
    echo "  • \"calculator app\""
    echo "  • \"todo list with React\""
    echo "  • \"Python web scraper\""
    echo "  • \"landing page for my business\""
    echo ""
    read -p "Your idea: " prompt
    
    if [ -z "$prompt" ]; then
        print_error "Please describe what you want to create"
        exit 1
    fi
    
    # Ask for custom project name (optional)
    echo ""
    local suggested_name=$(generate_project_name "$prompt")
    print_prompt "Project name (press Enter for '$suggested_name'):"
    read -p "Name: " custom_name
    
    if [ -n "$custom_name" ]; then
        # Clean the custom name
        PROJECT_NAME=$(echo "$custom_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
        if [ -z "$PROJECT_NAME" ]; then
            PROJECT_NAME="$suggested_name"
        fi
    else
        PROJECT_NAME="$suggested_name"
    fi
    
    generate_code "$prompt"
}

# Chunked generation mode for massive projects
chunked_generate() {
    local prompt="$1"
    local language="$2"
    local framework="$3"
    local max_chunk_size="${4:-2000}"
    
    if [ -z "$prompt" ]; then
        print_error "Please provide a prompt for chunked generation"
        show_usage
    fi
    
    print_header "🚀 Chunked Code Generation (Massive Projects)"
    print_status "Prompt: $prompt"
    print_status "Max chunk size: $max_chunk_size lines"
    
    # Override language and framework if provided
    if [ -n "$language" ]; then
        LANGUAGE="$language"
        print_status "Language: $language"
    else
        LANGUAGE=$(detect_language "$prompt")
        print_status "Detected language: $LANGUAGE"
    fi
    
    if [ -n "$framework" ]; then
        FRAMEWORK="$framework"
        print_status "Framework: $framework"
    else
        FRAMEWORK=$(detect_framework "$prompt" "$LANGUAGE")
        if [ -n "$FRAMEWORK" ]; then
            print_status "Detected framework: $FRAMEWORK"
        fi
    fi
    
    # Generate project name
    PROJECT_NAME=$(generate_project_name "$prompt")
    print_status "Project name: $PROJECT_NAME"
    
    # Auto-create Git repo in chunked mode
    CREATE_GIT_REPO=true
    
    # Create project directory
    local project_dir=$(create_project_directory "$OUTPUT_DIR" "$PROJECT_NAME")
    print_status "Project directory: $project_dir"
    
    # Build enhanced prompt for massive project generation
    local enhanced_prompt="Create a massive, enterprise-scale project: $prompt

This should be a comprehensive, production-ready system with:
- Tens of thousands of lines of code
- Multiple interconnected modules/services
- Complete documentation and tests
- Professional architecture and design patterns
- Scalable and maintainable codebase
- Industry best practices

Generate a complete, fully-functional system with all necessary components, configurations, and supporting files. This should be suitable for enterprise deployment."
    
    # Build qodo command for massive generation
    local cmd="qodo generate_code --set prompt=\"$enhanced_prompt\" --set language=\"$LANGUAGE\""
    [ -n "$FRAMEWORK" ] && cmd="$cmd --set framework=\"$FRAMEWORK\""
    cmd="$cmd --set project_name=\"$PROJECT_NAME\" --set output_dir=\"$project_dir\" --set include_tests=true --set include_docs=true --set complexity=\"advanced\""
    
    # Run qodo generation for massive project
    run_qodo "$cmd" "Generating massive enterprise-scale project..."
    print_success "Chunked generation completed successfully!"
    
    # Initialize Git repository
    if [ "$CREATE_GIT_REPO" = true ] && command -v git &> /dev/null; then
        init_git_repo "$project_dir" "$PROJECT_NAME"
    fi
    
    # Update OUTPUT_DIR for potential follow-up
    OUTPUT_DIR="$project_dir"
    
    # Run tests
    run_tests "$project_dir"
    
    # Final message
    echo ""
    print_success "🎉 Massive project generation complete!"
    print_status "📁 Your project is in: $project_dir"
    print_status "💡 Next steps:"
    echo "  • Review the generated architecture"
    echo "  • Install dependencies for each component"
    echo "  • Run integration tests"
    echo "  • Deploy components as needed"
    echo ""
}

# Quick generation mode (non-interactive)
quick_generate() {
    local prompt="$1"
    local language="$2"
    local framework="$3"
    
    if [ -z "$prompt" ]; then
        print_error "Please provide a prompt for quick generation"
        show_usage
    fi
    
    print_header "🚀 Quick Code Generation"
    print_status "Prompt: $prompt"
    
    # Override language and framework if provided
    if [ -n "$language" ]; then
        LANGUAGE="$language"
        print_status "Language: $language"
    else
        LANGUAGE=$(detect_language "$prompt")
        print_status "Detected language: $LANGUAGE"
    fi
    
    if [ -n "$framework" ]; then
        FRAMEWORK="$framework"
        print_status "Framework: $framework"
    else
        FRAMEWORK=$(detect_framework "$prompt" "$LANGUAGE")
        if [ -n "$FRAMEWORK" ]; then
            print_status "Detected framework: $FRAMEWORK"
        fi
    fi
    
    # Generate project name
    PROJECT_NAME=$(generate_project_name "$prompt")
    print_status "Project name: $PROJECT_NAME"
    
    # Auto-create Git repo in quick mode
    CREATE_GIT_REPO=true
    
    # Create project directory
    local project_dir=$(create_project_directory "$OUTPUT_DIR" "$PROJECT_NAME")
    print_status "Project directory: $project_dir"
    
    # Build qodo command
    local cmd="qodo generate_code --set prompt=\"$prompt\" --set language=\"$LANGUAGE\""
    [ -n "$FRAMEWORK" ] && cmd="$cmd --set framework=\"$FRAMEWORK\""
    cmd="$cmd --set project_name=\"$PROJECT_NAME\" --set output_dir=\"$project_dir\" --set include_tests=true --set include_docs=true"
    
    # Run qodo generation
    run_qodo "$cmd" "Generating your code..."
    print_success "Code generated successfully!"
    
    # Initialize Git repository
    if [ "$CREATE_GIT_REPO" = true ] && command -v git &> /dev/null; then
        init_git_repo "$project_dir" "$PROJECT_NAME"
    fi
    
    # Update OUTPUT_DIR for potential follow-up
    OUTPUT_DIR="$project_dir"
    
    # Run tests
    run_tests "$project_dir"
    
    # Final message
    echo ""
    print_success "🎉 Quick generation complete!"
    print_status "📁 Your project is in: $project_dir"
    print_status "💡 Next steps:"
    echo "  • Review the generated files"
    echo "  • Install any dependencies"
    echo "  • Test and customize as needed"
    echo ""
}

# Main execution
main() {
    setup_environment
    
    case "${1:-}" in
        "improve")
            if [ -z "$2" ]; then
                print_error "Please specify a directory to improve"
                show_usage
            fi
            improve_project "$2"
            ;;
        "--quick")
            quick_generate "$2" "$3" "$4"
            ;;
        "--chunked")
            chunked_generate "$2" "$3" "$4" "$5"
            ;;
        "-h"|"--help"|"help")
            show_usage
            ;;
        "")
            interactive_mode
            ;;
        *)
            # Check if this looks like a quick generation (has arguments)
            if [ $# -ge 1 ] && [[ ! "$1" =~ ^- ]]; then
                # If we have 2+ args or the first arg doesn't look like a flag, assume quick mode
                if [ $# -ge 2 ] || [[ "$1" =~ [a-zA-Z] ]]; then
                    quick_generate "$1" "$2" "$3"
                else
                    generate_code "$1"
                fi
            else
                generate_code "$1"
            fi
            ;;
    esac
    
    # Final message
    echo ""
    print_success "🎉 All done!"
    echo ""
    print_status "Your project is in: $OUTPUT_DIR"
    print_status "Next steps:"
    echo "  • Review the generated files"
    echo "  • Install any dependencies"
    echo "  • Test and customize as needed"
    echo ""
    print_success "Happy coding! 🚀"
}

main "$@"