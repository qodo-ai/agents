# GitHub Pages Deploy Agent

This agent automates the deployment of static websites to GitHub Pages, enabling seamless hosting directly from a GitHub repository. It handles repository setup, build detection, deployment branch management, and verification of a successful live site - all in one command.

## Demo

Watch full demo of the deployment workflow in action here👉 [https://vimeo.com/1126271853](https://vimeo.com/1126271853)

## Features

- Initializes a **new Git repository** if one does not exist

- Automatically creates a remote GitHub repository if missing

- Commits and pushes project files to the `main` branch

- Detects and runs **build commands** if applicable (`npm run build`, `next build`, etc.)

- Determines which directory to deploy (auto-detects `build`, `dist`, `out`, or `.next/out`)

- Creates and manages a `gh-pages` branch for static site deployment

- Pushes the deployed content to GitHub Pages

- Confirms the live deployment URL

- Returns structured logs and URLs for both repository and deployed site

## Configuration Options

The agent accepts the following arguments:

| Argument         | Type   | Required | Default                               | Description                                                                                   |
| ---------------- | ------ | -------- | ------------------------------------- | --------------------------------------------------------------------------------------------- |
| `repo`           | string | Yes      | —                                     | GitHub repo in the form `owner/repo`                                                          |
| `build_command`  | string | No       | —                                     | Build command (if applicable). Example: `npm run build` or `next build`                       |
| `source_dir`     | string | No       | *(auto-detect)*                       | Path to built static site directory. If empty, detects `build`, `dist`, `out`, or `.next/out` |
| `commit_message` | string | No       | `Deploy updated site to GitHub Pages` | Commit message for deployment                                                                 |


## Usage

The agent is invoked via the github_pages_deploy command. Below are examples of how to use it.

**Prerequisites**

- `GITHUB_PERSONAL_ACCESS_TOKEN` with `repo` scope
- Qodo Command installed globally (`npm install -g @qodo/command`)
- Git installed and authenticated with GitHub

**Basic Usage**

```bash
qodo github_pages_deploy --set repo=owner/my-static-site
```

**Deploy with a Build Command**

```bash
qodo github_pages_deploy --set repo=owner/my-static-site --set build_command="npm run build"
```

**Specify a Custom Build Directory**

```bash
qodo github_pages_deploy --set repo=owner/my-static-site --set source_dir=./dist
```

**Custom Commit Message**

```bash
qodo github_pages_deploy --set repo=myuser/my-app --set commit_message="Update site with latest changes"
```

## Workflow Steps

1. **Repository Initialization** – Checks for `.git`; initializes if missing.

2. **Remote Repository Verification** – Creates remote repo if it doesn’t exist.

3. **Commit & Push to Main** – Adds, commits, and pushes project files (excluding `node_modules`, `.env`, `build artifacts).

4. **Build Detection** – Runs the build command if specified or auto-detected from package.json.

5. **Deployment Directory Selection** – Uses `source_dir` or auto-detects a suitable build folder.

6. **Temporary Deployment Setup** – Copies deployable files to `.deploy_temp`.

7. **GitHub Pages Branch Preparation** – Checks out or creates `gh-pages` branch, cleans previous content.

8. **Deploy Files** – Copies `.deploy_temp` contents into branch root.

9. **Commit & Push Deployment** – Commits and pushes the updated static content.

10. **Verification** – Confirms live site at `https://<owner>.github.io/<repo>/`.


## Output Schema
After execution, the agent returns a structured output with the following fields:

| Field       | Type             | Description                                          |
| ----------- | ---------------- | ---------------------------------------------------- |
| `success`   | boolean          | Whether deployment succeeded                         |
| `repo_url`  | string           | URL of the GitHub repository                         |
| `pages_url` | string           | URL of the deployed GitHub Pages site                |
| `messages`  | array of strings | Log messages or errors encountered during deployment |


## Troubleshooting Guide

### Common Issues

**Git Not Installed**
- Install Git and ensure it’s available in your PATH. Verify with `git --version`.

**Token Missing**
- Create `.env ` file and add `GITHUB_PERSONAL_ACCESS_TOKEN`

**Missing Build Directory**
- Ensure your project builds correctly before deployment or specify `source_dir` explicitly.

**GitHub Pages Not Updating**
- Ensure the deployment branch is correctly set to `gh-pages` in the repo’s Pages settings. Wait a few minutes for cache updates.

**Invalid Repository Format**
- nsure `repo` argument follows `owner/repo-name` format (e.g., Kiran1689/qodo-deploy).

## Tools Used

- filesystem

- desktop-commander

- github

- git

## License
MIT

