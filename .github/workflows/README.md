# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automating various tasks in the agents repository.

## Available Workflows

### 📝 Update README for Merged PR

**File**: `update-readme-for-merged-pr.yml`

**Purpose**: Automatically updates the README Community Agents section when a new agent is added via a merged pull request.

**Trigger**: Manual (workflow_dispatch)

**How to Use**:

1. **Navigate to Actions Tab**:
   - Go to the repository's Actions tab
   - Find "Update README for Merged PR" workflow

2. **Click "Run workflow"**:
   - Select the branch (usually `main`)
   - Fill in the required parameters

3. **Required Parameters**:
   - **PR Number**: The number of the merged PR that added a new agent (e.g., `10`)

4. **Optional Parameters**:
   - **Repository Owner**: Default is `qodo-ai`
   - **Repository Name**: Default is `agents`
   - **Base Branch**: Default is `main`
   - **Branch Prefix**: Default is `docs/update-readme`

**Example Usage**:
```
PR Number: 10
Repository Owner: qodo-ai (default)
Repository Name: agents (default)
Base Branch: main (default)
Branch Prefix: docs/update-readme (default)
```

**What It Does**:

1. **Analyzes the Merged PR**:
   - Fetches PR #10 details
   - Identifies new agents added
   - Extracts contributor information

2. **Updates README**:
   - Parses existing Community Agents section
   - Determines appropriate category (or creates new one if needed)
   - Adds new agent entry with proper attribution

3. **Creates Documentation PR**:
   - Creates new branch: `docs/update-readme-pr-10`
   - Commits README changes
   - Opens pull request with comprehensive description
   - Links back to original PR

**Permissions Required**:
- `contents: write` - To create branches and commit changes
- `pull-requests: write` - To create pull requests
- `issues: read` - To read PR information

**Dependencies**:
- Node.js 18+ (for Qodo Command)
- Python 3.11+ (for MCP servers)
- Git configuration for commits

## Workflow Features

### 🔒 Security
- Uses `GITHUB_TOKEN` for authentication
- Minimal required permissions
- Secure environment variable handling

### 🚀 Performance
- Caches Node.js dependencies
- Uses latest stable versions
- Efficient checkout with minimal fetch depth

### 📊 Monitoring
- Comprehensive step summaries
- Clear error reporting
- Detailed logging for debugging

### 🔄 Flexibility
- Configurable parameters
- Support for different repositories
- Customizable branch naming

## Usage Examples

### Example 1: Standard Agent Addition
When PR #15 adds a new security agent:
```
PR Number: 15
(all other defaults)
```

Result: Creates `docs/update-readme-pr-15` branch with README update

### Example 2: Different Repository
For a fork or different repository:
```
PR Number: 8
Repository Owner: myorg
Repository Name: my-agents
```

### Example 3: Custom Branch Naming
For specific branch naming convention:
```
PR Number: 22
Branch Prefix: feature/docs-update
```

Result: Creates `feature/docs-update-pr-22` branch

## Troubleshooting

### Common Issues

**1. PR Not Found**
- Verify the PR number exists
- Ensure the PR is merged
- Check repository owner/name are correct

**2. No Agent Files Detected**
- Confirm the PR actually adds agent files
- Check that files are in `agents/` directory
- Verify agent has proper structure

**3. Permission Errors**
- Ensure `GITHUB_TOKEN` has required permissions
- Check repository settings allow Actions to create PRs

**4. MCP Server Issues**
- Check Python/Node.js versions are compatible
- Verify MCP dependencies are installed correctly

### Getting Help

1. Check the workflow run logs in Actions tab
2. Look for specific error messages in failed steps
3. Verify all input parameters are correct
4. Ensure the original PR contains valid agent files

## Future Enhancements

Potential improvements for this workflow:

- **Automatic Triggering**: Trigger on PR merge events
- **Multi-Agent Support**: Handle PRs with multiple agents
- **Validation**: Pre-validate agent structure before processing
- **Notifications**: Slack/Discord notifications on completion
- **Rollback**: Ability to revert README changes if needed

---

**Note**: This workflow is designed to work with the PR README Updater agent located in `agents/pr-readme-updater/`. Ensure that agent is properly configured before running this workflow.