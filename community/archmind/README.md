# ArchMind - Advanced Architectural Intelligence Agent

## Overview

ArchMind is an advanced architectural intelligence agent designed to analyze complex codebases and provide comprehensive insights into software architecture. It combines static analysis, historical evolution tracking, and ML-powered pattern recognition to deliver actionable architectural documentation and recommendations.

### Competition Entry
This agent is submitted for the **"Best Agent for Complex Codebases"** category in the Qodo Build Your Agents competition.

## Key Features

- **Multi-Dimensional Analysis**: Static, dynamic, historical, and social code analysis
- **Pattern Recognition**: Automatic detection of design patterns and anti-patterns
- **Docker Containerized**: Clean, reproducible analysis environment
- **Comprehensive Documentation**: Auto-generates architectural guides and diagrams
- **CI/CD Integration**: Structured outputs for automation workflows
- **Enterprise Ready**: Handles large codebases up to 10M lines efficiently
- **MCP Server Integration**: Filesystem, Git, Memory, and Sequential-thinking servers
- **Quality Metrics**: Coupling, cohesion, cyclomatic complexity, and technical debt scoring

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Demo Analysis (Next.js Framework)

```bash
# Clone this repository
git clone https://github.com/qodo-ai/agents.git
cd agents/community/archmind

# Run demo analysis
./run-demo.sh

# View results
ls -la output/
```

### Interactive Mode

```bash
# Start interactive container
./run-interactive.sh

# Inside container, run custom analysis
qodo archmind --analysis-depth=expert --focus-area=patterns
```

## Usage

### Basic Analysis
```bash
docker-compose run --rm archmind
```

### Custom Analysis
```bash
docker-compose run --rm archmind-interactive qodo archmind \
  --analysis-depth=deep \
  --focus-area=dependencies \
  --output-format=json
```

### CI/CD Integration
```yaml
# .github/workflows/architecture-analysis.yml
name: Architecture Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run ArchMind Analysis
        run: |
          docker run --rm -v $PWD:/workspace -v $PWD/analysis:/workspace/analysis \
            ghcr.io/qodo-ai/archmind:latest
```

## Configuration

### Analysis Depth Levels
- **quick**: High-level overview and basic metrics
- **standard**: Detailed analysis with pattern detection (default)
- **deep**: Comprehensive analysis with diagrams
- **expert**: Complete architectural intelligence with recommendations

### Focus Areas
- **all**: Complete architectural analysis (default)
- **dependencies**: Dependency structure and coupling analysis
- **patterns**: Design pattern and anti-pattern detection
- **performance**: Performance bottleneck identification
- **security**: Security vulnerability assessment

### Arguments
- `analysis_depth`: Set analysis complexity level
- `generate_docs`: Enable/disable documentation generation
- `include_diagrams`: Generate visual architectural diagrams
- `focus_area`: Target specific architectural concerns
- `output_format`: Choose output format (markdown, json, yaml, html)
- `max_file_count`: Limit number of files to analyze
- `exclude_patterns`: Patterns to exclude from analysis

## Output Structure

```
output/
├── architecture-overview.md      # Executive summary
├── component-analysis.md         # Detailed component breakdown
├── dependency-graph.json         # Machine-readable dependencies
├── patterns-detected.md          # Identified patterns
├── recommendations.md            # Actionable improvements
├── diagrams/                     # SVG architectural diagrams
│   ├── system-overview.svg
│   ├── dependency-graph.svg
│   └── component-interactions.svg
└── metrics.json                  # Quality and complexity metrics
```

## Advanced Usage

### Analyzing Your Repository
```bash
# Replace target-repo with your repository
rm -rf target-repo
git clone YOUR_REPO_URL target-repo
./run-demo.sh
```

### Custom Docker Build
```bash
docker build -t my-archmind .
docker run --rm -v /path/to/your/repo:/workspace my-archmind
```

### Local Development Integration
```bash
# Navigate to your project directory
cd /path/to/your/project

# Run ArchMind analysis
docker run --rm \
  -v $PWD:/workspace \
  -v $PWD/architecture-analysis:/workspace/analysis \
  ghcr.io/qodo-ai/archmind:latest

# View results
open architecture-analysis/architecture-overview.md
```

## Technical Architecture

ArchMind leverages multiple advanced technologies:

### MCP Server Integration
- **Filesystem MCP**: Deep codebase traversal and file analysis
- **Git MCP**: Historical analysis and change tracking
- **Memory MCP**: Persistent architectural knowledge across sessions
- **Sequential-thinking MCP**: Complex multi-step architectural reasoning

### Analysis Pipeline
1. **Discovery Phase**: Repository structure scanning and project type identification
2. **Static Analysis**: Code parsing and dependency graph construction
3. **Historical Analysis**: Git history analysis for architectural evolution
4. **Pattern Recognition**: ML-powered pattern and anti-pattern detection
5. **Synthesis**: Comprehensive architectural model generation

### Output Formats
- **Human-readable**: Markdown documentation and SVG diagrams
- **Machine-readable**: JSON/YAML data for automation
- **Interactive**: HTML reports for navigation
- **Integration**: CI/CD compatible status reports

## Why ArchMind Wins

### Innovation
1. **Multi-dimensional Analysis**: First tool to combine static, historical, and social analysis
2. **ML Pattern Recognition**: Advanced pattern detection not available elsewhere
3. **Architectural Intelligence**: Goes beyond simple code analysis to architectural understanding
4. **Evolution Tracking**: Unique focus on how architecture changes over time

### Enterprise Value
1. **Real Problem Solving**: Addresses actual pain points in complex codebase management
2. **Team Collaboration**: Facilitates knowledge sharing and onboarding
3. **Technical Debt Visibility**: Clear identification and prioritization of improvements
4. **Decision Support**: Provides data-driven architectural guidance

### Technical Excellence
1. **Scalability**: Efficiently handles codebases up to 10M lines
2. **Language Agnostic**: Works across multiple programming languages
3. **Containerized**: Clean, reproducible analysis environment
4. **Integration Ready**: Seamless CI/CD and workflow integration

### Competition Advantages
1. **Sophisticated Demo**: Next.js framework analysis showcases all capabilities
2. **Complete Solution**: Production-ready with comprehensive documentation
3. **Immediate Utility**: Teams can use it right away
4. **Future-proof**: Modular design for extensibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `./run-demo.sh`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Competition Details

**Category**: Best Agent for Complex Codebases
**Innovation**: Multi-dimensional architectural intelligence with ML pattern recognition
**Demo Repository**: Next.js framework (150k+ lines of TypeScript/JavaScript)
**Integration**: Docker containerization with CI/CD workflow support
**Value Proposition**: Enterprise architectural understanding automation

### Judging Criteria Addressed
- **Technical Innovation**: Multi-dimensional analysis methodology
- **Code Quality**: Comprehensive pattern detection and quality metrics
- **Reliable Code**: Health scoring and architectural compliance verification
- **Clean Code**: Automated documentation and onboarding generation
- **Automation**: CI/CD integration with structured outputs
- **Complex Codebases**: Specialized capabilities for large-scale analysis

ArchMind represents a significant advancement in architectural analysis tooling, providing capabilities that don't exist in current solutions while delivering immediate value to development teams working with complex software systems.

