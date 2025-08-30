# Package Health Reviewer Agent

🔍 **Automated package health assessment using Snyk Advisor data**

Analyze the security, maintenance, and community health of software packages to make informed dependency decisions. This agent fetches real-time data from Snyk Advisor and provides actionable health assessments.

## Features

- **🛡️ Security Analysis**: Identifies vulnerabilities and security risks
- **📊 Popularity Metrics**: Analyzes download statistics and community adoption
- **🔧 Maintenance Assessment**: Evaluates update frequency and maintainer responsiveness
- **👥 Community Health**: Reviews GitHub activity and documentation quality
- **🎯 Smart Scoring**: Returns clear health ratings: "healthy", "sustainable", or "risky"
- **🤖 Bot-Resistant**: Uses Playwright MCP server for reliable web automation
- **📋 Detailed Reports**: Comprehensive metrics and actionable recommendations
- **🚫 No File Creation**: Returns JSON directly without creating files on disk

## Quick Start

```bash
# Analyze a popular package
qodo --agent-file=agent.toml -y --set package_name="express"

# Check a potentially risky package
qodo --agent-file=agent.toml -y --set package_name="request"

# Get minimal output without detailed metrics
qodo --agent-file=agent.toml -y \
  --set package_name="lodash" \
  --set include_details=false
```

## Configuration

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `package_name` | string | ✅ | - | Name of the package to analyze (e.g., 'express', 'lodash') |
| `package_registry` | string | ❌ | `npm` | Package registry to analyze (currently supports: npm) |
| `include_details` | boolean | ❌ | `true` | Include detailed metrics in the output |

### Example Configurations

```bash
# Basic package analysis
qodo --agent-file=agent.toml -y --set package_name="react"

# Analyze with minimal output
qodo --agent-file=agent.toml -y \
  --set package_name="vue" \
  --set include_details=false

# Future: Other registries (when supported)
qodo --agent-file=agent.toml -y \
  --set package_name="requests" \
  --set package_registry="pypi"
```

## Health Score Criteria

### 🟢 Healthy (Score: 90-100)
- **Security**: No critical/high vulnerabilities
- **Popularity**: High download count (>100k weekly)
- **Maintenance**: Recent updates (within 6 months)
- **Community**: Active GitHub repository, good documentation
- **Quality**: High Snyk score, good practices

### 🟡 Sustainable (Score: 60-89)
- **Security**: Some medium vulnerabilities, no critical issues
- **Popularity**: Moderate usage (10k-100k weekly downloads)
- **Maintenance**: Updates within 12 months
- **Community**: Decent GitHub activity
- **Quality**: Acceptable Snyk score

### 🔴 Risky (Score: 0-59)
- **Security**: Critical/high vulnerabilities present
- **Popularity**: Low usage (<10k weekly) or declining
- **Maintenance**: No recent updates (>12 months)
- **Community**: Inactive repository
- **Quality**: Low Snyk score, deprecated status

## Output Schema

The agent returns structured JSON with the following fields:

### Required Fields
```json
{
  "health_score": "healthy|sustainable|risky",
  "package_name": "express",
  "registry": "npm", 
  "overall_score": 95,
  "assessment_date": "2024-01-15T10:30:00Z",
  "analysis_summary": "Express is a healthy package with excellent security posture..."
}
```

### Detailed Fields (when include_details=true)
```json
{
  "security_metrics": {
    "critical": 0,
    "high": 0, 
    "medium": 1,
    "low": 2,
    "total_vulnerabilities": 3
  },
  "popularity_metrics": {
    "weekly_downloads": "2M+",
    "github_stars": 58000,
    "dependents": 15000
  },
  "maintenance_metrics": {
    "last_update": "2024-01-10",
    "update_frequency": "regular",
    "maintainer_response": "excellent"
  },
  "recommendations": [
    "Safe to use in production environments",
    "Keep updated to latest version"
  ],
  "alternatives": [],
  "snyk_url": "https://snyk.io/advisor/npm-package/express"
}
```

## Prerequisites

### System Requirements
- Node.js 18+ and npm
- Playwright MCP server (automatically installed)

### Installation
The Playwright MCP server is automatically configured and installed when you run the agent. No manual installation is required.

```bash
# The agent will automatically install the Playwright MCP server:
# npx @playwright/mcp@latest
```

## Examples

### Test with Known Packages

```bash
# Test with a healthy package (Express)
qodo --agent-file=agent.toml -y --set package_name="express"
# Expected: "healthy" score with high metrics

# Test with a risky package (Request - deprecated)
qodo --agent-file=agent.toml -y --set package_name="request"  
# Expected: "risky" score with deprecation warnings

# Test with a sustainable package
qodo --agent-file=agent.toml -y --set package_name="moment"
# Expected: "sustainable" score (popular but has maintenance concerns)
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Package Health Check
on: [pull_request]

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install Playwright
        run: |
          npm install playwright
          npx playwright install chromium
      - name: Check package health
        run: |
          qodo --agent-file=agents/package-health-reviewer/agent.toml -y \
            --set package_name="${{ matrix.package }}" \
            --ci
        env:
          PACKAGE_NAME: ${{ matrix.package }}
    strategy:
      matrix:
        package: [express, lodash, axios]
```

## Troubleshooting

### Common Issues

**Issue**: `Could not initialize the server playwright`
```bash
# The Playwright MCP server should install automatically
# If you encounter issues, you can manually install it:
npx @playwright/mcp@latest --help

# Or check if Node.js is available:
node --version
npm --version
```

**Issue**: `Browser launch failed`
```bash
# The Playwright MCP server handles browser installation automatically
# If you encounter issues, the agent can use the browser_install tool
# to install required browsers

# For system dependencies (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install -y \
  libnss3 \
  libatk-bridge2.0-0 \
  libdrm2 \
  libxkbcommon0 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  libgbm1 \
  libxss1 \
  libasound2
```

**Issue**: `Package not found on Snyk Advisor`
- Verify the package name is correct
- Check if the package exists on npm registry
- Some packages may not be indexed by Snyk yet
- Try alternative package names or spellings

**Issue**: `Rate limiting or blocked requests`
- The agent uses Playwright with realistic browser headers
- If issues persist, try running with delays between requests
- Check your network connection and proxy settings

### Debug Mode

For verbose output and debugging:

```bash
# Run in interactive mode for debugging
qodo chat agent.toml

# Then ask: "Please analyze the package 'express' with verbose logging"
```

## Supported Registries

| Registry | Status | Package URL Format |
|----------|--------|-------------------|
| npm | ✅ Supported | `https://snyk.io/advisor/npm-package/{name}` |
| PyPI | 🚧 Planned | `https://snyk.io/advisor/pypi-package/{name}` |
| Maven | 🚧 Planned | `https://snyk.io/advisor/maven-package/{group}/{artifact}` |
| RubyGems | 🚧 Planned | `https://snyk.io/advisor/rubygems-package/{name}` |

## Limitations

- Currently supports npm packages only
- Requires internet connection to fetch Snyk Advisor data
- Analysis accuracy depends on Snyk's data freshness
- Some packages may not be indexed by Snyk Advisor
- Rate limiting may apply for bulk analysis

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-registry`)
3. Make your changes
4. Test with the provided examples
5. Submit a pull request

### Adding New Registry Support

To add support for a new package registry:

1. Update the `package_registry` argument options
2. Modify the URL construction logic in the instructions
3. Add registry-specific parsing logic
4. Update documentation and examples
5. Add test cases for the new registry

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📚 [Qodo Documentation](https://docs.qodo.ai/)
- 💬 [Discord Community](https://discord.gg/qodo)
- 🐛 [Report Issues](https://github.com/qodo-ai/agents/issues)
- 🔍 [Snyk Advisor](https://snyk.io/advisor/) - Data source for package analysis

## Related Tools

- [Snyk CLI](https://docs.snyk.io/snyk-cli) - Direct security scanning
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) - Built-in npm security audit
- [Dependabot](https://github.com/dependabot) - Automated dependency updates
- [Socket Security](https://socket.dev/) - Alternative package security analysis