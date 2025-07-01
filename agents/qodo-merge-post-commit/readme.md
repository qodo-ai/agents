# Qodo Merge Post-Commit Hook

This README explains how to **automatically** receive code suggestions from Qodo Merge after each commit using a `post-commit` hook.

## Setup Instructions

### 1. Ensure `pre-commit` is Installed

Install `pre-commit` if you haven't already:

```bash
pip install pre-commit
```

### 2. Copy Configuration Files

Copy the `.pre-commit-config.yaml` and `agent.yaml` files from the `agents/qodo-merge-post-commit/` directory to the root of your repository. These files contain the configuration for the pre-commit hooks that will run after each commit.

### 3. Install the Post-Commit Hooks

Run the following command in your terminal to install the hooks specified in your configuration file:

```bash
pre-commit install --hook-type post-commit
```

This command sets up the hooks to run automatically after each commit.

### 4. You're All Set!

Now, every time you make a commit, Qodo Merge will automatically run in the background. When it finishes (usually takes ~30 seconds), it will generate a file called `diff_review_post_commit.md` in the root of your repository, containing code suggestions for changes in your current branch compared to the main branch.

![qodo_merge_post_commit](https://codium.ai/images/pr_agent/qodo_merge_post_commit.png){width=512}


During the run, another file called `diff_review_post_commit_log.txt` will be created, which contains the logs of the Agent execution.