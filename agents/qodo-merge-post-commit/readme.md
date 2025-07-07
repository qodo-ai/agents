# Qodo Merge Post-Commit Hook

This README explains how to **automatically** receive code suggestions from Qodo Merge after each commit using a `post-commit` hook.

## Setup Instructions

### 1. Setup Qodo Gen CLI

See [here](https://github.com/qodo-ai/qodo-gen-cli?tab=readme-ov-file#installation) for instructions.


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

### 5. Further Enhancements

#### 5.1 Notification In Case of High Severity Issues (MacOS Only)

The post commit hook utilizes MacOS system notifications as well as showing the generated file in Finder, whenever high severity issues are found in the generated file, 
which is turned off by default.
To enable this, simply add the following at the end of the `run_qodo_merge_workflow` function:

```angular2html
    # Show completion notification on macOS, but only if high severity issues found
    if grep -q '<td align=center>High' diff_review_post_commit.md; then
        if is_macos; then
            notify_completion
        fi
    fi
```

Also, in case you want to open the generated file, rather than just show in Finder, you can replace `reveal` in the `notify_completion` function with `open` as follows:
```angular2html
open POSIX file "$file_path"
```
