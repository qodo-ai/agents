# CI/CD Integration Configurations

This directory contains separate configuration files for different CI/CD platforms, split from the original `ci-integration.yml` file for better organization and easier maintenance.

## Available Configurations

### 1. GitHub Actions (`github-actions.yml`)
- Complete workflow for GitHub Actions
- Includes code review job and security review job
- Features PR commenting, artifact uploading, and status checks
- Supports conditional security reviews based on labels

### 2. GitLab CI (`gitlab-ci.yml`)
- GitLab CI/CD pipeline configuration
- Multi-stage pipeline with review and security stages
- Includes artifact management and conditional execution
- Supports merge request events and file change detection

### 3. Jenkins Pipeline (`jenkins-pipeline.groovy`)
- Declarative Jenkins pipeline
- Includes setup, code review, and security check stages
- Features HTML report publishing and email notifications
- Supports conditional security checks based on file changes

### 4. Azure DevOps (`azure-devops.yml`)
- Azure DevOps Pipeline configuration
- Supports both CI triggers and PR validation
- Includes test result publishing and variable groups
- Features Node.js setup and Qodo CLI integration

## Usage

Choose the appropriate configuration file for your CI/CD platform:

- **GitHub**: Copy `github-actions.yml` to `.github/workflows/` in your repository
- **GitLab**: Copy `gitlab-ci.yml` to your repository root as `.gitlab-ci.yml`
- **Jenkins**: Use `jenkins-pipeline.groovy` in your Jenkins pipeline configuration
- **Azure DevOps**: Use `azure-devops.yml` in your Azure DevOps pipeline setup

## Common Features

All configurations include:
- Qodo CLI installation and setup
- Code review execution with configurable parameters
- Result artifact management
- Security-focused reviews for sensitive changes
- Conditional execution based on branch/PR context

## Customization

Each configuration can be customized by modifying:
- Severity thresholds
- Focus areas (security, performance, etc.)
- File exclusion patterns
- Target branches
- Notification settings