# Python License Examples

This directory contains example Python scripts demonstrating different license scenarios for testing the License Compliance Agent.

## Files

- `mit_example.py` - Uses only MIT-licensed dependencies (should PASS)
- `agpl_example.py` - Uses GPL-licensed dependencies (should FAIL/REVIEW_REQUIRED)

## Testing the Agent

Run the license compliance check on this directory:

```bash
qodo --agent-file=qodo-agent.toml -y --set directory=./examples/python
```

## Expected Results

### MIT Example (`mit_example.py`)
- **Dependency**: `pydantic` (MIT license)
- **Expected Status**: PASS ✅
- **Description**: Simple data validation script using Pydantic

### GPL Example (`agpl_example.py`) 
- **Dependency**: `ansible` (GPL-3.0+ license)
- **Expected Status**: FAIL/REVIEW_REQUIRED ❌
- **Description**: Infrastructure automation script using Ansible

## Sample Output

When you run the agent, you should see output similar to:

```json
{
  "compliance_status": "REVIEW_REQUIRED",
  "new_dependencies": [
    {
      "name": "pydantic",
      "license": "MIT",
      "source": "PyPI",
      "status": "allowed"
    },
    {
      "name": "ansible",
      "license": "GPL-3.0+",
      "source": "PyPI",
      "status": "blocked"
    }
  ],
  "license_violations": [
    {
      "type": "blocked_license",
      "severity": "high", 
      "description": "Dependency 'ansible' uses GPL-3.0+ license which is in the blocked list",
      "component": "ansible",
      "recommendation": "Remove this dependency or seek legal approval for GPL usage"
    }
  ],
  "summary": "Found 1 license violation that requires attention",
  "safe_to_merge": false
}
```

## Running Individual Examples

You can also test each file individually by modifying the directory structure or using subdirectories.

### Test Only MIT Example
Create a temporary directory with just the MIT example:
```bash
mkdir temp-mit
cp mit_example.py temp-mit/
qodo --agent-file=qodo-agent.toml -y --set directory=./temp-mit
```

### Test Only GPL Example
Create a temporary directory with just the GPL example:
```bash
mkdir temp-gpl
cp agpl_example.py temp-gpl/
qodo --agent-file=qodo-agent.toml -y --set directory=./temp-gpl
```

## Understanding the Scripts

### UV Script Dependencies
Both examples use uv script format with dependencies declared in comments:

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#     "package-name"
# ]
# ///
```

The agent will automatically detect these dependency declarations and check their licenses.

### Modifying Examples

You can modify these examples to test different scenarios:

1. **Add more dependencies** to the dependency lists
2. **Change license policies** using command arguments:
   ```bash
   qodo --agent-file=qodo-agent.toml -y \
     --set directory=./examples/python \
     --set allowed_licenses="MIT,Apache-2.0" \
     --set blocked_licenses="GPL-3.0,AGPL-3.0,LGPL-3.0"
   ```
3. **Test development dependencies** by setting `ignore_dev_dependencies=false`