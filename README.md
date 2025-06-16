# Qodo Agent Reference Implementations

A curated collection of reference agent implementations for the [Qodo CLI](https://github.com/qodo-ai/qodo-gen-cli) framework, showcasing best practices and common patterns for building AI-powered development workflows.

## What are Qodo Agents?

Qodo Agents are configurable AI workflows that combine:
- **Instructions**: Natural language prompts that define the agent's behavior
- **Tools**: MCP servers and external integrations the agent can use
- **Arguments**: Configurable parameters for customization
- **Execution Strategy**: How the agent approaches tasks (plan vs act)
- **Output Schema**: Structured output format for integration
- **Exit Expressions**: Success/failure conditions for CI/CD

## 🌟 Reference Agents

These agents demonstrate core patterns and best practices for the Qodo framework.

### Development Workflow Agents
- **[Code Review](agents/code-review/)** - Comprehensive code review with Qodo Merge integration
- **[Test Generation](agents/test-generation/)** - Automated test suite creation and validation
- **[Documentation](agents/documentation/)** - Generate and maintain project documentation
- **[Refactoring](agents/refactoring/)** - Safe code refactoring with validation
- **[Security Audit](agents/security-audit/)** - Security vulnerability scanning and remediation

### CI/CD Integration Agents
- **[Pre-commit Validation](agents/pre-commit/)** - Pre-commit hook validation and fixes
- **[Release Notes](agents/release-notes/)** - Automated release note generation
- **[Deployment Validation](agents/deployment/)** - Post-deployment health checks
- **[Performance Analysis](agents/performance/)** - Performance regression detection

### Project Management Agents
- **[Issue Triage](agents/issue-triage/)** - Automated issue classification and routing
- **[Sprint Planning](agents/sprint-planning/)** - Sprint planning assistance
- **[Technical Debt](agents/tech-debt/)** - Technical debt identification and prioritization

### Data & Analytics Agents
- **[Data Pipeline](agents/data-pipeline/)** - Data pipeline monitoring and validation
- **[Report Generation](agents/reports/)** - Automated report generation
- **[Metrics Analysis](agents/metrics/)** - Performance metrics analysis

## 🤝 Community Agents

Community-contributed agents demonstrating various use cases and integrations.

> **Note:** Community agents are maintained by their respective authors and should be used at your own discretion.

### Language-Specific Agents
- **[Python Linting](community/python-linting/)** - Python-specific code quality checks
- **[JavaScript Testing](community/js-testing/)** - JavaScript/TypeScript testing workflows
- **[Go Optimization](community/go-optimization/)** - Go performance optimization
- **[Rust Safety](community/rust-safety/)** - Rust memory safety validation

### Framework-Specific Agents
- **[React Component](community/react-component/)** - React component analysis and optimization
- **[Django Migration](community/django-migration/)** - Django database migration validation
- **[FastAPI Documentation](community/fastapi-docs/)** - FastAPI documentation generation

### Integration Agents
- **[GitHub Actions](community/github-actions/)** - GitHub Actions workflow optimization
- **[Docker Security](community/docker-security/)** - Docker container security scanning
- **[Kubernetes Health](community/k8s-health/)** - Kubernetes cluster health monitoring

## 📚 Agent Categories

### By Execution Strategy
- **Planning Agents** - Multi-step strategic approaches
- **Action Agents** - Direct execution patterns
- **Hybrid Agents** - Adaptive strategy selection

### By Integration Type
- **MCP-Based** - Leveraging Model Context Protocol servers
- **API-Based** - Direct API integrations
- **Tool-Based** - Command-line tool integrations

### By Output Type
- **Structured Data** - JSON/YAML output for automation
- **Reports** - Human-readable analysis
- **Actions** - Direct system modifications

## 🚀 Getting Started

### Prerequisites
- [Qodo CLI](https://github.com/qodo-ai/qodo-gen-cli) installed
- Node.js 18+ and npm
- Git for version control

### Quick Start

1. **Clone this repository:**
   ```bash
   git clone https://github.com/qodo-ai/agent-reference-implementations.git
   cd agent-reference-implementations
   ```

2. **Choose an agent:**
   ```bash
   # Copy a reference agent to your project
   cp -r src/code-review/ /path/to/your/project/agents/
   ```

3. **Configure the agent:**
   ```bash
   # Edit the agent configuration
   vim /path/to/your/project/agents/code-review/agent.toml
   ```

4. **Run the agent:**
   ```bash
   cd /path/to/your/project
   qodo code-review --agent-file=agents/code-review/agent.toml
   ```

### Using Reference Agents

Each reference agent includes:
- **Configuration file** (`agent.toml` or `agent.yaml`)
- **README** with usage instructions and examples
- **Test cases** demonstrating expected behavior
- **Integration examples** for common scenarios

## 🛠️ Creating Your Own Agent

### Basic Agent Structure

```toml
# agent.toml
version = "1.0"
description = "Brief description of what your agent does"

[commands.my_agent]
description = "Detailed description for users"
instructions = """
Your agent's behavior instructions here.
Be specific about the task and expected outcomes.
"""

arguments = [
    { name = "input_file", type = "string", required = true, description = "Input file path" },
    { name = "threshold", type = "number", required = false, default = 0.8, description = "Quality threshold" }
]

# MCP servers your agent uses
mcpServers = """
{
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "git": {
        "command": "uvx",
        "args": ["mcp-server-git"]
    }
}
"""

available_tools = ["filesystem", "git"]
execution_strategy = "act"

# Optional: Define expected output structure
output_schema = """
{
    "properties": {
        "success": {"type": "boolean"},
        "results": {"type": "array", "items": {"type": "string"}},
        "score": {"type": "number"}
    }
}
"""

# Optional: Success condition for CI/CD
exit_expression = "success"
```

### Agent Development Guidelines

1. **Clear Instructions**: Write specific, actionable instructions
2. **Proper Tool Selection**: Choose appropriate MCP servers and tools
3. **Error Handling**: Include error scenarios in instructions
4. **Testing**: Provide test cases and expected outputs
5. **Documentation**: Include comprehensive README and examples

### Testing Your Agent

```bash
# Test with sample data
qodo my_agent --input_file=test/sample.txt --threshold=0.9

# Validate output schema
qodo my_agent --input_file=test/sample.txt | jq '.success'

# CI/CD integration test
qodo my_agent --ci --input_file=test/sample.txt
```

## 📖 Documentation

### Agent Configuration Reference
- [Configuration Schema](docs/configuration-schema.md)
- [MCP Server Integration](docs/mcp-integration.md)
- [Output Schema Design](docs/output-schema.md)
- [CI/CD Integration](docs/ci-cd-integration.md)

### Best Practices
- [Agent Design Patterns](docs/design-patterns.md)
- [Error Handling](docs/error-handling.md)
- [Performance Optimization](docs/performance.md)
- [Security Considerations](docs/security.md)

### Examples
- [Basic Agent Tutorial](docs/tutorials/basic-agent.md)
- [MCP Integration Tutorial](docs/tutorials/mcp-integration.md)
- [CI/CD Setup Tutorial](docs/tutorials/ci-cd-setup.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. **Reference Agents**: Submit well-documented, tested agents
2. **Community Agents**: Share your specialized use cases
3. **Documentation**: Improve guides and examples
4. **Bug Reports**: Report issues with existing agents

### Contribution Guidelines

- Follow the [Agent Development Guidelines](#agent-development-guidelines)
- Include comprehensive tests and documentation
- Ensure compatibility with latest Qodo CLI version
- Add your agent to the appropriate category in this README

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Qodo CLI](https://github.com/qodo-ai/qodo-gen-cli) - The main Qodo CLI framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocol for AI tool integration
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Reference MCP server implementations

## 💬 Community

- [GitHub Discussions](https://github.com/qodo-ai/agent-reference-implementations/discussions)
- [Discord Server](https://discord.gg/qodo-ai)
- [Documentation](https://docs.qodo.ai)

## ⭐ Support

If you find these agent implementations useful, please consider:
- Starring this repository
- Contributing your own agents
- Sharing feedback and suggestions
- Helping improve documentation

---

**Built with ❤️ by the Qodo community**