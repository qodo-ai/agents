# Contributing to Qodo CLI Agent Reference Implementations

Thank you for your interest in contributing to the Qodo CLI Agent Reference Implementations! This repository serves as a collection of example agents and best practices for building AI-powered coding assistants.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please be respectful, inclusive, and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.8+ or Node.js 16+ (depending on the agent you're working on)
- Git
- Basic understanding of AI/ML concepts and coding assistants

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/qodo-cli-agent-reference-implementations.git
   cd qodo-cli-agent-reference-implementations
   ```
3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://github.com/qodo-dev/qodo-cli-agent-reference-implementations.git
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

1. **New Agent Implementations**
   - Complete agent examples in different programming languages
   - Specialized agents for specific use cases
   - Performance optimizations and improvements

2. **Documentation**
   - Improving existing documentation
   - Adding tutorials and guides
   - Translating documentation

3. **Bug Fixes**
   - Fixing issues in existing agent implementations
   - Correcting documentation errors

4. **Feature Enhancements**
   - Adding new capabilities to existing agents
   - Improving user experience
   - Performance improvements

### Before You Start

1. **Check existing issues** to see if your contribution is already being worked on
2. **Create an issue** to discuss major changes before implementing them
3. **Review the agent guidelines** in the relevant language directory

## Development Guidelines

### Agent Implementation Standards

#### Code Quality
- Write clean, readable, and well-documented code

#### Documentation Requirements
- Include a detailed README for each agent
- Document all configuration options
- Provide usage examples
- Include troubleshooting guides

#### Testing
- Test with various input scenarios
- Ensure compatibility with different environments

### File Structure

When adding a new agent implementation:

```
agents/
├── your-agent-name/
│   ├── README.md                # Agent-specific documentation
│   ├── agent.toml               # Main configuration file
│   ├── agent.yaml               # Alternative YAML configuration (optional)
│   ├── mcp.json                 # MCP server configuration (optional)
```

### Commit Message Guidelines

Use clear and descriptive commit messages:

```
type(scope): brief description

Detailed explanation of the changes made.

- List specific changes
- Reference issues if applicable
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the development guidelines

3. **Test your changes** thoroughly

4. **Update documentation** as needed

5. **Commit your changes** with clear commit messages

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

### Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Documentation**: Note any documentation updates
- **Breaking Changes**: Highlight any breaking changes

### Review Process

1. **Automated checks** will run on your PR
2. **Maintainer review** - at least one maintainer will review your changes
3. **Community feedback** - other contributors may provide feedback
4. **Revisions** - make requested changes if needed
5. **Merge** - once approved, your PR will be merged

## Testing

### Running Tests

```bash
qodo your-agent-name
```

### Test Coverage

Aim for high test coverage, especially for:
- Core agent functionality
- Error handling
- Configuration parsing
- Tool integrations

## Documentation

### Writing Documentation

- Use clear, concise language
- Include examples
- Provide step-by-step instructions
- Keep documentation up to date with code changes

### Documentation Structure

- **README.md**: Overview and quick start
- **docs/**: Detailed documentation
- **examples/**: Working code examples
- **API.md**: API reference (if applicable)

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Discord/Slack**: Real-time community chat (if available)

### Staying Updated

- **Watch the repository** for notifications
- **Follow releases** for new versions
- **Join community channels** for announcements

## Recognition

Contributors will be recognized in:
- The project's README
- Release notes for significant contributions
- Hall of fame for major contributors

## Questions?

If you have questions about contributing, please:
1. Check the existing documentation
2. Search through existing issues
3. Create a new issue with the "question" label
4. Reach out to maintainers

Thank you for contributing to making AI-powered coding assistance more accessible and effective!