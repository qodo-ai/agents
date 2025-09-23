# Code Quality Podman Agent - Example Usage

This document demonstrates how the agent should actually create and execute files instead of just listing them.

## What the Agent Should Do

When a user requests a code quality pipeline, the agent should:

### 1. Create Actual Pipeline Files

```bash
# The agent should create files like:
./podman-pipeline.yaml
./quality-config.yaml
./run-pipeline.sh
./quality-gates.yaml
```

### 2. Generate Tool-Specific Configurations

```bash
# For Python projects:
./.pylintrc
./bandit.yaml
./pyproject.toml

# For JavaScript projects:
./.eslintrc.json
./.prettierrc
./package.json (quality scripts)
```

### 3. Execute the Pipeline

```bash
# The agent should run commands like:
chmod +x run-pipeline.sh
./run-pipeline.sh /path/to/project python pylint,bandit,black json
```

### 4. Generate Actual Reports

```bash
# The agent should create actual report files:
./quality-reports/pylint-report.json
./quality-reports/bandit-report.json
./quality-reports/summary.json
./quality-reports/consolidated-report.html
```

## Example Execution Flow

1. **User Request**: "Set up a Python code quality pipeline"

2. **Agent Actions** (what it should actually do):
   - Create `run-pipeline.sh` script
   - Create `.pylintrc` configuration
   - Create `bandit.yaml` configuration  
   - Create `podman-pipeline.yaml`
   - Execute: `chmod +x run-pipeline.sh`
   - Execute: `./run-pipeline.sh . python all json`
   - Generate actual quality reports

3. **Agent Response**: 
   - "✅ Created and executed Python quality pipeline"
   - "📁 Generated files: [list of actual files created]"
   - "📊 Quality reports available in ./quality-reports/"
   - "🚀 Pipeline ready for CI/CD integration"

## Key Changes Made

### Before (Planning Mode)
- `execution_strategy = "plan"`
- Instructions focused on "Set up and configure"
- Agent would only describe what it would do

### After (Execution Mode)  
- `execution_strategy = "execute"`
- Instructions emphasize "CREATE and EXECUTE"
- Agent must actually create files and run processes
- Added explicit instruction: "Do not just list what files you would create - actually create them"

## Testing the Fix

To test that the agent now works correctly:

1. Ask it to create a quality pipeline for a specific language
2. Verify it actually creates files (not just lists them)
3. Check that it executes the pipeline and generates reports
4. Confirm it provides actual file paths and execution results

The agent should now perform real actions instead of just planning them.
