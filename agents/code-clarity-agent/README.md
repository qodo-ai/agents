# Universal Code Clarity Agent

**Don't just detect code quality issues—FIX them automatically with AI, for *any* language.**

This Qodo agent analyzes source code in any language (Python, JavaScript, Java, Rust, and more) for common clarity and quality problems, generates language-specific AI-powered fixes, and provides a quantifiable score to prove the improvement.

---
Competition Category
Best Agent for Clean Code Description


## Quick Start

To analyze and automatically refactor a file, run:

```bash
qodo code-clarity --set file_path=path/to/your/code.js --set language=javascript
```

```bash
qodo code-clarity --set file_path=path/to/your/code.py --set language=python
```

---

## Core Features

-   ✅ **Detects 5 Types of Issues**: Finds missing docstrings, magic numbers, poor variable names, overly complex functions, and redundant comments.
-   ✅ **Generates AI-Powered Fixes**: Automatically generates high-quality docstrings, extracts magic numbers into named constants, and suggests better variable names.
-   ✅ **Quantifiable Scoring**: Calculates a "Clarity Score" (0-100) before and after the fixes, so you can see the concrete improvement.
-   ✅ **Before/After Comparison**: The agent's output includes the original and the refactored code, making it easy to review the changes.

---

## Core Philosophy: From Detection to Solution

Many code quality tools are excellent at **detecting** problems. They generate a list of issues, leaving the developer with the manual task of fixing them.

This agent is built on a different philosophy: **it provides a solution, not just a report.**

By leveraging AI, the Universal Code Clarity Agent moves beyond simple analysis to offer automated, language-aware refactoring. Its core value is in saving developer time and cognitive load by not just identifying what's wrong, but by actively fixing it.

### Key Differentiators
*   **Automated Refactoring:** Instead of just flagging missing docstrings or magic numbers, the agent generates high-quality, language-specific fixes and applies them.
*   **Quantifiable Improvement:** The Clarity Score (0-100) provides a concrete metric to demonstrate the value of the changes, showing a clear "before and after" state.
*   **Multi-Language by Design:** The agent is built to be language-agnostic, applying the appropriate documentation standards (JSDoc, Google-style docstrings, etc.) based on the user's input.

---

## Example Workflow

1.  **You run the agent on a file:**
    `qodo code-clarity --set file_path=examples/bad_code.py`

2.  **The agent analyzes the code and finds:**
    *   2 missing docstrings
    *   1 magic number
    *   2 poor variable names
    *   **Initial Score: 45/100**

3.  **The agent automatically applies fixes:**
    *   Generates two complete, Google-style docstrings.
    *   Extracts `0.15` into a constant named `THRESHOLD`.
    *   Suggests renaming `calc` to `calculate_value` and `x` to `base_value`.

4.  **The agent displays the results:**
    *   **Final Score: 90/100**
    *   **Improvement: +100%**
    *   A clear, side-by-side view of the original and refactored code.

---

## Value Proposition

The Universal Code Clarity Agent transforms code quality analysis from a manual, time-consuming chore into a fast, automated workflow. By using AI to generate fixes and providing a clear scoring system, it allows developers to improve their codebase's readability and maintainability in seconds, not hours. This means less time spent on tedious refactoring and more time focused on building features.

---

## Requirements

-   **Qodo CLI:** Requires a standard installation and login (`qodo login`).
-   **No Special API Keys:** Unlike other agents that may require a `QODO_API_KEY` for premium services, our agent uses the core AI model and local tools, making it accessible to anyone with a basic Qodo account.
