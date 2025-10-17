# Clean Code Agent

The Clean Code Agent is an AI-powered tool designed to help developers write more readable, maintainable, and well-structured code. It analyzes your source code and provides actionable feedback based on established clean code principles.

## Key Features

- **Automated Code Refactoring:** Goes beyond simple analysis by providing `diff`-style previews for fixing issues related to naming, complexity, and code smells.
- **Automatic Docstring Generation:** Identifies public functions missing documentation and generates complete docstrings, including parameters and return values.
- **Unit Test Scaffolding:** Creates basic unit test files for your modules, encouraging a test-driven development culture.
- **Linter Integration:** Can run a command-line linter (e.g., ESLint, Pylint) and use its output as a baseline for its own, more context-aware analysis.
- **Customizable Rule Sets:** Allows teams to enforce their own coding standards by providing a custom rules file.
- **CI/CD Integration:** Includes ready-to-use configuration examples for GitHub Actions, GitLab CI, Jenkins, and Azure DevOps to automate code quality checks in your pipeline.
- **Structured Output:** Produces machine-readable JSON output, perfect for integrations and quality gating.

## How to Use

You can run the Clean Code Agent using the `qodo` command-line tool.

### Basic Analysis

```bash
qodo clean_code --set files="path/to/your/code" --set language="your_language"
```

### Generating Docstrings and Tests

```bash
qodo clean_code --set files="src/my_module.py" --set language="python" --set generate_docstrings=true --set generate_tests=true
```

### CI/CD Integration

For examples of how to integrate the agent into your CI/CD pipeline, see the configuration files in the `examples/ci-configs` directory.

## Arguments

- `files` (required): A comma-separated list of file paths or directories to analyze.
- `language` (required): The programming language of the files (e.g., 'python', 'javascript').
- `report_format` (optional): The format for the output report ('markdown' or 'json'). Defaults to 'markdown'.
- `linter_command` (optional): A linter command to run before analysis.
- `rules_file` (optional): A path to a file containing custom analysis rules.
- `complexity_analysis` (optional): Whether to perform and report on cyclomatic complexity. Defaults to `false`.
- `generate_docstrings` (optional): If true, generates missing docstrings for public functions. Defaults to `false`.
- `generate_tests` (optional): If true, generates a scaffold for unit tests. Defaults to `false`.
