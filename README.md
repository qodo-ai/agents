# Qodo Agents

This repository contains agents implementations examples, to be used with [Qodo Command](https://github.com/qodo-ai/command), showcasing best practices and common patterns for building AI-powered development workflows.

See [the Qodo Command docs](https://docs.qodo.ai/qodo-documentation/qodo-command/) to learn more about using agents with Qodo Command.

## What are Qodo Agents?

Qodo Agents are configurable AI workflows that combine:
- **Instructions**: Natural language prompts that define the agent's behavior
- **Tools**: MCP servers and external integrations the agent can use
- **Arguments**: Configurable parameters for customization
- **Execution Strategy**: How the agent approaches tasks (plan vs act)
- **Output Schema**: Structured output format for integration
- **Exit Expressions**: Success/failure conditions for CI/CD

---

## Getting Started

### Prerequisites
- [Qodo Command](https://docs.qodo.ai/qodo-documentation/qodo-command) installed
- Node.js 18+ and npm
- Git for version control

## Quickstart

[See the Qodo Command Quickstart and setup documentation](https://docs.qodo.ai/qodo-documentation/qodo-command/getting-started/setup-and-quickstart) to learn how to setup Qodo Command and start using agents.

## How to Use an Existing Agent

All agents in this repository reside in the `agents` folder.

You can specify a custom agent configuration file in two ways: Remote or Local. Both methods allow you to customize agent behavior without modifying core logic.

### Remote Agent File

Use a remote URL to point to an agent configuration file with the flag:

```bash
--agent-file=URL
```

Example:

```bash
my-tool --agent-file=https://example.com/agents/my-agent.toml
```

### Local Agent File

Download or create a local agent `.toml` file and specify its path.

[See the Qodo Command documentation to learn how to write an customized agent `.toml` file.
](https://docs.qodo.ai/qodo-documentation/qodo-command/features/creating-and-managing-agents)

## How to Create an Agent

### Basic Agent Structure

```toml
# agent.toml
version = "1.0"
[commands.my_agent]
description = "Detailed description for users"
instructions = """
Your agent's behavior instructions here.
Be specific about the task and expected outcomes.
"""

# Optional: Define arguments
arguments = [
   { name = "input_file", type = "string", required = true, description = "Input file path" },
   { name = "threshold", type = "number", required = false, default = 0.8, description = "Quality threshold" }
]

# Optional: MCP servers your agent uses
mcpServers = """
{
    "shell": {
      "command": "uvx",
      "args": [
        "mcp-shell-server"
      ],
      "env": {
        "ALLOW_COMMANDS": "..."
      }
    },
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
      "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
}
"""

# Optional: Define available tools
tools = ["filesystem", "git", "shell", "github"]

# Optional: Define execution strategy: "plan" for multi-step, "act" for direct execution
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
qodo my_agent --set input1=0.9 --set input2="test"

# CI/CD integration test
qodo my_agent --ci --set input1=0.9 --set input2="test"
```

---

## Example Agents

These agents demonstrate core patterns and best practices for the Qodo framework.

### Development Workflow Agents
- **[Code Review](agents/code-review/)** - Comprehensive code review with Qodo Merge integration
- **[Diff Test Generation](agents/diff-test-suite/)** - Automated test suite creation and validation of code changes
- **[GitHub Issue Handler](agents/github-issue-handler/)** - Automatically processes GitHub issues by analyzing content, answering questions, implementing fixes, and creating pull requests

## 🤝 Community Agents

Community-contributed agents demonstrating various use cases and integrations.

> **Note:** Community agents are maintained by their respective authors and should be used at your own discretion.

### Development Workflow
- **[ArchMind](community/archmind/)** - Advanced architectural intelligence framework that provides comprehensive analysis, pattern recognition, and documentation generation for complex codebases with Docker containerization and CI/CD integration *(contributed by [@53gf4u1t](https://github.com/53gf4u1t))*
- **[Documentation Writer](agents/documentation-writer/)** - Automatically generates and updates professional README.md files with comprehensive project documentation, including Git hooks for automated updates *(contributed by [@Max77788](https://github.com/Max77788))*

### Security & Compliance
- **[OpenSSF Scorecard Fixer](agents/openssf-scorecard-fixer/)** - Automatically fixes security issues identified by OpenSSF Scorecard to improve repository security posture *(contributed by [@lirantal](https://github.com/lirantal))*
- **[Package Health Reviewer](agents/package-health-reviewer/)** - Automated package health assessment using Snyk Advisor data to analyze security, maintenance, and community metrics of software dependencies *(contributed by [@lirantal](https://github.com/lirantal))*
- **[License Compliance Agent](agents/license-compliance/)** - Automated license compliance checking for multi-language projects with configurable policies and CI/CD integration *(contributed by [@agamm](https://github.com/agamm))*

### Infrastructure & DevOps
- **[AWS Static Deploy](agents/aws-static-deploy/)** - Automates deployment of static websites to AWS S3 and CloudFront with proper configuration, cache invalidation, and deployment validation *(contributed by [@gpavlov2016](https://github.com/gpavlov2016))*


---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. **Reference Agents**: Submit well-documented, tested agents
2. **Community Agents**: Share your specialized use cases
3. **Documentation**: Improve guides and examples
4. **Bug Reports**: Report issues with existing agents

### Contribution Guidelines

- Follow the [Agent Development Guidelines](#agent-development-guidelines)
- Include comprehensive tests and documentation
- Ensure compatibility with latest Qodo Command version
- Add your agent to the appropriate category in this README

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [Qodo Command](https://github.com/qodo-ai/command) - The main Qodo Command framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocol for AI tool integration
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Reference MCP server implementations

## Learn More

[Go to the Qodo Command docs](https://docs.qodo.ai/qodo-documentation/qodo-command/) to learn more about using agents with Qodo Command.

---

**Built with ❤️ by the Qodo community**