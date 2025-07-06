# Qodo Merge Post-Commit Hook

This README explains how to **automatically** receive code suggestions from Qodo Merge after each commit using a `post-commit` hook.

## Setup Instructions

### 1. Setup Qodo Command

See [here](https://github.com/qodo-ai/command?tab=readme-ov-file#installation) for instructions.


### 2. Copy the `post-commit` Hook

Copy the `post-commit` file from the `agents/qodo-merge-post-commit/` directory to your local `.git/hooks/` directory. 

This file is a git hook that will run automatically after each commit.
(Note that in macOS to see the `.git` directory you need to press `Cmd + Shift + .` )

After copying, ensure the `post-commit` file is executable. You can do this by running the following command in your terminal:

```bash
chmod 755 .git/hooks/post-commit
```

### 3. Copy the agent.toml file

Copy the `agent.toml` file from the `agents/qodo-merge-post-commit/` directory to your local directory. This file contains the prompt to run the Qodo Merge Agent.


### 4. You're All Set!

Now, every time you make a commit, Qodo Merge will automatically run in the background. When it finishes (usually takes ~30 seconds), it will generate a file called `diff_review_post_commit.md` in the root of your repository, containing code suggestions for changes in your current branch compared to the main branch.

![qodo_merge_post_commit](https://codium.ai/images/pr_agent/qodo_merge_post_commit.png)


During the run, another file called `diff_review_post_commit_log.txt` will be created, which contains the logs of the Agent execution.
