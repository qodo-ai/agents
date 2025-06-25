# CI/CD Configuration Examples

This directory contains example configurations for integrating the Code Review Agent with various CI/CD platforms.

## Available Configurations

- **[github-actions.yml](github-actions.yml)** - GitHub Actions workflow for automatic code review on pull requests
- **[gitlab-ci.yml](gitlab-ci.yml)** - GitLab CI/CD pipeline configuration
- **[azure-devops.yml](azure-devops.yml)** - Azure DevOps Pipeline configuration
- **[jenkins-pipeline.groovy](jenkins-pipeline.groovy)** - Jenkins declarative pipeline

## Usage

Choose the configuration file that matches your CI/CD platform and customize it according to your project's needs.

### Required Secrets

All configurations require the following secrets to be set in your CI/CD platform:

- `QODO_API_KEY` - Your Qodo API key (get one at [Qodo](https://qodo.ai))
- Platform-specific tokens:
  - GitHub: `GITHUB_TOKEN` (automatically provided in GitHub Actions)
  - GitLab: `GITLAB_TOKEN` (automatically provided as `CI_JOB_TOKEN`)
  - Azure DevOps: `AZURE_TOKEN` (System.AccessToken)
  - Jenkins: `GITHUB_TOKEN` or relevant SCM token

### Customization

Each configuration can be customized by modifying the `key-value-pairs` section to match your project's requirements:

- `target_branch` - The branch to compare against (default: main)
- `severity_threshold` - Minimum severity to report (low/medium/high/critical)
- `focus_areas` - Comma-separated focus areas (security, performance, maintainability)
- `exclude_files` - File patterns to exclude from review
- `include_suggestions` - Whether to include improvement suggestions

## Platform-Specific Setup

### GitHub Actions
Copy `github-actions.yml` to `.github/workflows/` in your repository.

### GitLab CI
Copy `gitlab-ci.yml` to your repository root as `.gitlab-ci.yml`.

### Azure DevOps
Use `azure-devops.yml` in your Azure DevOps pipeline setup and ensure the `qodo-credentials` variable group is configured.

### Jenkins
Use `jenkins-pipeline.groovy` in your Jenkins pipeline configuration and ensure the required credentials are set up.

## Contributing

If you have configurations for other CI/CD platforms, please contribute them by following our [Contributing Guide](../../../CONTRIBUTING.md).