# 🤖 MasterMindAI - Unified AI Development Assistant

**One Script. All Agents. Infinite Possibilities.**

MasterMindAI has been completely redesigned as a unified system that integrates all AI agents into one powerful, easy-to-use script. No more managing separate folders and configurations - everything you need is now in one place.

## 🚀 What's New in the Unified System

### ✅ **Single Entry Point**
```bash
# One command to rule them all
./mastermind chunked-generation "enterprise e-commerce platform"
./mastermind code-review --target-branch main
./mastermind documentation --input-file ./src
```

### ✅ **Integrated Configuration**
- All agents defined in one `mastermind_agents.toml` file
- Consistent argument parsing and validation
- Shared global settings and tools

### ✅ **Interactive Mode**
```bash
./mastermind --interactive
# Guided interface for all agents
```

### ✅ **Workflow Automation**
- Predefined workflows combining multiple agents
- Automatic dependency management between agents
- One-command complete development cycles

## 📁 New Project Structure

```
MasterMindAI/
├── mastermind                      # 🆕 Main launcher script
├── mastermind_ai.sh               # 🆕 Unified agent system
├── mastermind_agents.toml         # 🆕 All agent configurations
├── UNIFIED_SYSTEM_README.md       # 🆕 This documentation
├── agents/                        # 📁 Legacy individual agents (kept for reference)
│   ├── chunked-generation/
│   ├── code-review/
│   └── ...
└── generated/                     # Generated projects output
```

## 🎯 Available Agents

| Agent | Description | Usage |
|-------|-------------|-------|
| **chunked-generation** | Generate massive projects (10,000+ lines) | `./mastermind chunked-generation "project idea"` |
| **code-review** | Analyze code changes and provide feedback | `./mastermind code-review --target-branch main` |
| **documentation** | Generate comprehensive documentation | `./mastermind documentation --input-file ./src` |
| **github-issues** | Automatically handle GitHub issues | `./mastermind github-issues --issue-number 123` |
| **test-suite** | Generate comprehensive test suites | `./mastermind test-suite --coverage-threshold 90` |
| **license-compliance** | Check and fix license compliance | `./mastermind license-compliance --scan-path .` |
| **package-health** | Review package health and dependencies | `./mastermind package-health --security-scan` |
| **security-scan** | Comprehensive security analysis | `./mastermind security-scan --scan-type comprehensive` |
| **performance-analysis** | Optimize code performance | `./mastermind performance-analysis --include-profiling` |
| **deployment** | Deploy to cloud platforms | `./mastermind deployment --platform aws` |

## 🚀 Quick Start

### 1. **Basic Usage**
```bash
# List all available agents
./mastermind --list-agents

# Get help for any agent
./mastermind chunked-generation --help

# Generate a massive project
./mastermind chunked-generation "enterprise CRM system" --language python --framework django
```

### 2. **Interactive Mode**
```bash
./mastermind --interactive
# Follow the guided interface to select and configure agents
```

### 3. **Global Options**
```bash
# Set global options for all agents
./mastermind chunked-generation "project" --language javascript --framework react --output-dir ./my-projects --git
```

### 4. **Workflow Examples**
```bash
# Complete development workflow
./mastermind chunked-generation "web application" --language python
./mastermind test-suite --coverage-threshold 85
./mastermind code-review --severity-threshold medium
./mastermind documentation --input-file ./generated
./mastermind security-scan --scan-type comprehensive
```

## 🎮 Interactive Mode Demo

```bash
$ ./mastermind --interactive

🤖 MasterMindAI Interactive Mode
═══════════════════════════════════════════════════════════════

Available agents:
  1. chunked-generation - Generate massive projects with intelligent chunking (10,000+ lines)
  2. code-review - Analyze code changes and provide detailed feedback
  3. documentation - Generate comprehensive README and documentation
  4. github-issues - Automatically handle GitHub issues and create PRs
  5. test-suite - Generate and run comprehensive test suites
  6. license-compliance - Check and fix license compliance issues
  7. package-health - Review and improve package health and dependencies
  8. security-scan - Scan for security vulnerabilities and fixes
  9. performance-analysis - Analyze and optimize code performance
  10. deployment - Deploy applications to cloud platforms
  0. Exit

Select an agent (0-10): 1
🤖 Selected: chunked-generation
Enter project description: enterprise social media platform
Programming language (default: python): python
Framework (optional): django

🚀 Chunked Generation - Massive Project Creation
▶ Project: enterprise social media platform
▶ Language: python
▶ Framework: django
▶ Max chunk size: 2000
▶ Strategy: modular
▶ Quality: standard
...
```

## 🔧 Configuration

### Global Settings
Edit `mastermind_agents.toml` to customize:

```toml
[global]
default_language = "python"
default_output_dir = "generated"
venv_path = "./venv"
tools = ["filesystem", "git", "shell", "qodo_merge"]
```

### Agent-Specific Settings
Each agent has its own configuration section:

```toml
[commands.chunked_generation]
description = "Generate massive projects..."
arguments = [
    { name = "prompt", type = "string", required = true },
    { name = "language", type = "string", default = "python" },
    # ... more arguments
]
```

## 🌟 Key Benefits of the Unified System

### 1. **Simplified Usage**
- **Before**: Navigate to different directories, remember different commands
- **After**: One command, consistent interface across all agents

### 2. **Better Integration**
- **Before**: Agents worked in isolation
- **After**: Agents can work together in workflows, share context

### 3. **Easier Maintenance**
- **Before**: Update multiple configuration files
- **After**: Single configuration file for all agents

### 4. **Enhanced User Experience**
- **Before**: Complex setup and usage
- **After**: Interactive mode, helpful error messages, consistent output

### 5. **Workflow Automation**
- **Before**: Manual coordination between agents
- **After**: Predefined workflows for common development tasks

## 📊 Comparison: Before vs After

| Aspect | Before (Separate Agents) | After (Unified System) |
|--------|-------------------------|------------------------|
| **Commands** | `qodo agent1`, `qodo agent2` | `./mastermind agent1`, `./mastermind agent2` |
| **Configuration** | 10+ separate `.toml` files | 1 unified `mastermind_agents.toml` |
| **Setup** | Navigate to each agent directory | Single entry point |
| **Help** | Different help systems | Consistent `--help` across all agents |
| **Integration** | Manual coordination | Automatic workflows |
| **User Experience** | Complex, fragmented | Simple, unified |

## 🎯 Migration from Separate Agents

If you were using the separate agent system:

### Old Way:
```bash
cd agents/chunked-generation
./generate.sh --chunked "project idea"

cd ../code-review  
qodo code_review --target-branch main

cd ../documentation-writer
qodo documentation_writer --input-file ./src
```

### New Way:
```bash
./mastermind chunked-generation "project idea"
./mastermind code-review --target-branch main
./mastermind documentation --input-file ./src
```

## 🔮 Future Enhancements

### Planned Features
- **Workflow Designer**: Visual interface for creating custom workflows
- **Agent Marketplace**: Community-contributed agents
- **Cloud Integration**: Run agents in the cloud for massive projects
- **Real-time Collaboration**: Multi-developer agent sessions

### Extensibility
The unified system is designed for easy extension:

```toml
# Add new agents by extending mastermind_agents.toml
[commands.my_custom_agent]
description = "My custom AI agent"
instructions = "..."
arguments = [...]
```

## 🤝 Contributing

The unified system makes contributing easier:

1. **Add New Agents**: Extend `mastermind_agents.toml`
2. **Improve Workflows**: Add new workflow definitions
3. **Enhance UI**: Improve the interactive mode
4. **Add Integrations**: Connect with new tools and platforms

## 📈 Performance Benefits

- **Faster Startup**: Single process instead of multiple agent processes
- **Shared Resources**: Reuse virtual environment and dependencies
- **Better Caching**: Shared context and caching across agents
- **Reduced Memory**: Single Python process for all operations

## 🎉 Ready to Use

The unified MasterMindAI system is ready for immediate use:

```bash
# Quick start
./mastermind --interactive

# Generate a massive project
./mastermind chunked-generation "your amazing project idea"

# Get help
./mastermind --help
```

**Experience the power of unified AI development assistance!** 🚀

---

**The future of AI-powered development is here - unified, powerful, and incredibly easy to use.**