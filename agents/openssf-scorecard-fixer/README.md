## Overview

This agent is designed to fix issues in the OpenSSF Scorecard project. It automates the process of updating your GitHub repository settings with the required security hardening and your project's security workflows and other security posture.

## Requirements:

Pre-requisite for running this agent includes:

- GitHub Personal Access Token (PAT) with `repo` scope
- Docker installed and running
- GitHub CLI tool (`gh`) installed
- OpenSSF Scorecard CLI tool installed
- Qodo Command installed globally (`npm install -g @qodo/command`)

## Usage

In the directory with the `agent.yaml` file for the OpenSSF Scorecard fixer agent, run the following command:

```bash
GITHUB_AUTH_TOKEN=1234 qodo openssf-scorecard-fixer --set repo="https://github.com/lirantal/hello-world-js"
```

Replace `1234` with your GitHub PAT (Personal Access Token) and the `repo` value with the URL of your repository.


## Resources

A detailed blog post on how this agent works can be found here: [Automating OpenSSF Scorecard Security issues with Qodo CLI Agentic Workflow](https://lirantal.com/blog/automating-openssf-scorecard-security-issues-with-qodo-cli-agentic-workflow)

