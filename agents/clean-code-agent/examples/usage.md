# Clean Code Agent Usage Examples

This document provides a set of examples for using the Clean Code Agent.

## Example 1: Basic Analysis of a Single File

This example shows how to run the agent on a single Python file and get the report in Markdown format.

**Command:**

```bash
qodo clean_code --set files="src/my_module.py" --set language="python"
```

**Expected Output:**

A Markdown report printed to the console, listing any clean code issues found in `src/my_module.py`.

## Example 2: Analyzing an Entire Directory with JSON Output

This example analyzes all JavaScript files in the `src` directory and outputs the results in JSON format, which can be piped to other tools.

**Command:**

```bash
qodo clean_code --set files="src/" --set language="javascript" --set report_format="json" > report.json
```

**Expected Output:**

A `report.json` file containing a structured list of all the issues found.

## Example 3: Using a Linter and Complexity Analysis

This example demonstrates how to use the agent with a linter and enable cyclomatic complexity analysis.

**Command:**

```bash
qodo clean_code --set files="." --set language="javascript" --set linter_command="eslint ." --set complexity_analysis=true
```

**Expected Output:**

A report that includes both the AI's analysis and the linter's findings, with cyclomatic complexity scores for relevant functions.

## Example 4: Applying Custom Rules

This example shows how to use a custom rules file to guide the agent's analysis.

**Command:**

```bash
qodo clean_code --set files="app/" --set language="ruby" --set rules_file=".codify/clean_code_rules.txt"
```

**Expected Output:**

A report where the issues are prioritized and analyzed based on the rules defined in `.codify/clean_code_rules.txt`.

## Example 5: Generating Docstrings and Unit Tests

This example demonstrates how to use the agent's code generation capabilities. It will analyze the specified file, generate a missing docstring, and create a new unit test file.

**Command:**

```bash
qodo clean_code --set files="src/utils.py" --set language="python" --set generate_docstrings=true --set generate_tests=true
```

**Expected Output:**

- A `diff` suggestion in the output to add the new docstring to `src/utils.py`.
- A new file created at `src/test_utils.py` with a basic test structure.
- A summary in the output indicating that 1 docstring was generated and 1 test file was created.
