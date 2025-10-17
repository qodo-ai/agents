# Repository Guidelines

## Project Structure & Module Organization

- Root files: README.md, CONTRIBUTING.md, SECURITY.md, LICENSE, AGENTS.md
- Agents are under agents/ with one folder per agent (e.g., agents/api-tester/, agents/package-health-reviewer/). Typical files:
  - agent.toml (or agent.yaml) — Agent configuration and instructions
  - README.md — Agent-specific docs and usage
  - examples/ — CI configs, scripts, or hooks (e.g., examples/ci, examples/ci-configs, examples/hooks)
  - Additional assets as needed (e.g., specs/, express_health_assessment.json)
- Community-contributed agents live under community/ (e.g., community/archmind/)
- CI workflows are under .github/workflows/

## Build, Test, and Development Commands

```bash
# Generate API Test Plan (API Tester)
qodo api_test_plan --set swagger_url="https://petstore.swagger.io/v2/swagger.json"

# Generate API Test Code (API Tester)
qodo api_test_create --set swagger_url="https://petstore.swagger.io/v2/swagger.json"

# Run generated .NET tests (after api_test_create)
cd ApiTests && dotnet restore && dotnet test

# Run Package Health Reviewer locally (from its folder)
qodo --agent-file=agents/package-health-reviewer/agent.toml -y --set package_name="express"
```

## Coding Style & Naming Conventions

- Indentation: spaces; 2-space indentation for TOML/YAML/Markdown; follow language norms in generated code (e.g., C# PascalCase for classes/tests)
- File naming:
  - Agent configs: agent.toml (or agent.yaml) inside each agent directory
  - Documentation: README.md per agent; AGENTS.md at repo root
  - Examples/CI configs: under examples/ci or examples/ci-configs with .yml/.yaml
- Linting/formatting: not centrally enforced; use language-standard tools per agent

## Testing Guidelines

- Frameworks vary by agent; API Tester generates .NET tests (NUnit/xUnit/MSTest)
- Generated artifacts default to ApiTests/
- Run generated tests with:
```bash
cd ApiTests && dotnet restore && dotnet test
```
- Coverage requirements: none specified in this repository

## Commit & Pull Request Guidelines

- Commit style: Conventional Commits commonly used
  - Examples:
    - docs(contributing): fix incorrect upstream URL in contributing guide
    - docs: add Changelog Generator agent to Community Agents section
- PR process (see CONTRIBUTING.md):
  - Create a feature branch (e.g., feature/your-feature-name)
  - Include docs and examples for new/updated agents
  - Ensure agents run with Qodo Command locally or in CI
  - Maintainer review + automated checks
- Branch naming: feature/<name> recommended per CONTRIBUTING.md

---

# Repository Tour

## 🎯 What This Repository Does

Qodo Agents is a collection of agent implementations and reference configurations for Qodo Command, showcasing best practices and patterns for AI-powered development workflows.

Key responsibilities:
- Provide ready-to-use agent configurations (TOML/YAML)
- Demonstrate CI/CD integrations and usage patterns
- Serve as templates for building custom agents

---

## 🏗️ Architecture Overview

This repository comprises self-contained agent configurations. Each agent directory encapsulates instructions, tools/MCP servers, arguments, output schemas, and optional examples. There is no single runtime service; agents are executed by the Qodo Command CLI using agent.toml/agent.yaml.

### System Context
```
Developer → Qodo Command (CLI) → This Repository (agent configs) → External tools/MCP servers
```

### Key Components
- agents/<agent>/agent.toml — Defines instructions, tools, arguments, execution strategy, outputs, and exit expressions
- agents/<agent>/README.md — Agent setup, parameters, and example invocations
- agents/<agent>/examples/** — CI configs, scripts, hooks for usage in pipelines
- .github/workflows/*.yml — Reference CI usage (e.g., README updater workflow)

### Data Flow
1. Developer selects an agent and invokes it with qodo (by command name or --agent-file)
2. Qodo Command loads the agent configuration and starts declared tools/MCP servers
3. The agent executes tasks (analysis, generation, automation) and returns structured output
4. CI workflows may consume outputs or rely on exit_expression for pass/fail

---

## 📁 Project Structure [Partial Directory Tree]

```
./
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── AGENTS.md
├── .github/
│   └── workflows/
│       ├── README.md
│       └── update-readme-for-merged-pr.yml
├── agents/
│   ├── api-tester/
│   │   ├── agent.toml
│   │   ├── README.md
│   │   ├── examples/ci-configs/
│   │   └── specs/
│   ├── package-health-reviewer/
│   │   ├── agent.toml
│   │   ├── README.md
│   │   ├── examples/ci/
│   │   └── examples/scripts/
│   ├── license-compliance/
│   │   └── examples/{ci,python}/
│   ├── documentation-writer/
│   │   └── examples/hooks/
│   ├── diff-test-suite/
│   │   └── examples/ci-configs/
│   ├── code-review/
│   │   └── examples/ci-configs/
│   ├── github-issue-handler/
│   │   └── examples/ci-configs/
│   ├── qodo-cover/
│   │   └── examples/ci/
│   ├── changelog-generator/
│   │   └── examples/ci-configs/
│   ├── aws-static-deploy/
│   ├── openssf-scorecard-fixer/
│   ├── pr-readme-updater/
│   └── qodo-merge-post-commit/
└── community/
    └── archmind/
        └── examples/
```

---

### Key Files to Know

| File | Purpose | When You'd Touch It |
|------|---------|---------------------|
| `README.md` | Repository overview and getting started | Understand repo purpose and usage |
| `CONTRIBUTING.md` | Contributor workflow and standards | Preparing a PR or new agent contribution |
| `agents/<agent>/agent.toml` | Agent definition and instructions | Editing agent behavior, tools, or arguments |
| `agents/<agent>/README.md` | Agent-specific usage and flags | Running or integrating a specific agent |
| `.github/workflows/update-readme-for-merged-pr.yml` | CI to update README via agent | Changing workflow inputs or integration |

---

## 🔧 Technology Stack

### Core Technologies
- Formats: TOML, YAML, JSON, Markdown
- Engine: Qodo Command CLI (Node.js 18+; see README)
- MCP servers/tools: Declared per agent (e.g., filesystem, shell, web_search, playwright)

### Representative Libraries/Integrations
- Playwright MCP (agents/package-health-reviewer)
- RestAssured.Net and .NET test frameworks in generated output (agents/api-tester)

### Development Tools
- Qodo Command — execution engine for agents
- GitHub Actions — example CI integration under .github/workflows

---

## 🌐 External Dependencies

- Varies by agent. Examples:
  - Playwright MCP for browser automation (package-health-reviewer)
  - Swagger/OpenAPI sources via HTTP (api-tester)

---

## 🔄 Common Workflows

- Package Health Review (local):
```bash
qodo --agent-file=agents/package-health-reviewer/agent.toml -y --set package_name="express"
```

- API Test Plan generation:
```bash
qodo api_test_plan --set swagger_url="https://petstore.swagger.io/v2/swagger.json"
```

- API Test code generation (C#/.NET):
```bash
qodo api_test_create --set swagger_url="https://petstore.swagger.io/v2/swagger.json"
```

- Manual CI workflow to update README for a merged PR: see .github/workflows/README.md

---

## 🚨 Things to Be Careful About

### 🔒 Security Considerations
- Do not commit secrets. Some agents require API tokens (e.g., GitHub). Use environment variables and CI secrets
- When using Playwright MCP, ensure system dependencies are installed in CI environments

### Data handling
- Some agents (e.g., package-health-reviewer) instruct not to write files and to return JSON only
- Generated artifacts (like API tests) should be committed thoughtfully and kept up to date


*Update to last commit: 8fbedb21acd9a4f932e645da1546e027f20adf5c*
*Updated at: 2025-10-14*
