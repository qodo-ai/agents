# License Compliance Agent

🔐 Automated license compliance checking for your codebase. Prevents license violations before merging code.

## Features

- **Multi-Language Support**: Python, Node.js, Rust, Ruby, Go, Java
- **Smart Detection**: Finds dependencies in manifests, imports, and uv scripts
- **Flexible Policies**: Configurable allowed/blocked license lists
- **CI/CD Ready**: Works with GitHub Actions, GitLab CI, Jenkins, pre-commit

## Quick Start

```bash
# Basic usage
qodo --agent-file=qodo-agent.toml -y --set directory=./src

# Custom policies  
qodo --agent-file=qodo-agent.toml -y \
  --set directory=./src \
  --set allowed_licenses="MIT,Apache-2.0" \
  --set blocked_licenses="GPL-3.0,AGPL-3.0"
```

## Configuration

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `directory` | string | ✅ | - | Directory path to scan for dependencies |
| `allowed_licenses` | string | ❌ | `MIT,BSD-2-Clause,BSD-3-Clause,Apache-2.0,ISC,Unlicense` | Comma-separated list of allowed licenses |
| `blocked_licenses` | string | ❌ | `GPL-3.0,AGPL-3.0,SSPL-1.0` | Comma-separated list of blocked licenses |
| `ignore_dev_dependencies` | boolean | ❌ | `true` | Skip checking development-only dependencies |

## Test with Examples

```bash
qodo --agent-file=qodo-agent.toml -y --set directory=./examples/python
```

Expected: MIT license passes ✅, GPL license fails ❌

## CI/CD Integration

See complete examples in `examples/ci/`:
- GitHub Actions: `github-actions.yml`
- GitLab CI: `gitlab-ci.yml` 
- Jenkins: `Jenkinsfile`
- Pre-commit: `pre-commit-config.yaml`

## Supported Package Managers

| Language | Package Manager | Registry API | License Detection |
|----------|----------------|--------------|-------------------|
| Python | pip/uv | PyPI | ✅ Comprehensive |
| Node.js | npm/yarn | npm Registry | ✅ Comprehensive |
| Rust | cargo | crates.io | ✅ Comprehensive |
| Ruby | gem | RubyGems | ✅ Comprehensive |
| Go | go mod | pkg.go.dev | ⚠️ Limited |
| Java | maven/gradle | Maven Central | ⚠️ Limited |

## Troubleshooting

### Common Issues

**Issue**: `curl: command not found`
```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS
brew install curl

# Alpine
apk add curl
```

**Issue**: `jq: command not found`
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq

# Alpine
apk add jq
```

**Issue**: Package not found in registry
- Verify package name spelling
- Check if package exists in the registry
- Some packages may have different names in different registries

**Issue**: License information unavailable
- The agent will flag these for manual review
- Check the package's GitHub repository for license information
- Contact package maintainers if license is unclear

### Debug Mode

For verbose output, you can modify the agent to include debug information:

```bash
qodo chat qodo-agent.toml
```

Then ask: "Please scan ./src directory with verbose logging enabled"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the provided examples
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📚 [Qodo Documentation](https://docs.qodo.ai/)
- 💬 [Discord Community](https://discord.gg/qodo)
- 🐛 [Report Issues](https://github.com/qodo-ai/agents/issues)