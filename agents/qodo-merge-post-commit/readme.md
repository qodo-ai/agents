This readme will explain how to **automatically** get code suggestion from Qodo Merge after each commit, using a `post-commit` hook.




```

1. **Ensure `pre-commit` is Installed**: :

   ```bash
   pip install pre-commit
   ```

2. **Copy the `.pre-commit-config.yaml` File**: and `.agent.yaml` file from the `agents/qodo-merge-post-commit/` directory to the root of your repository. This file contains the configuration for the pre-commit hooks that will run after each commit.


3. **Install the Post-commit Hooks**: Run the following command in your terminal to install the hooks specified in your configuration file:

   ```bash
   pre-commit install --hook-type post-commit
   ```

   This command sets up the hooks to run automatically before each commit.

4. That's it! Now, every time you make a commit, Qodo Merge will automatically run in the background. 
When it finished (usually takes ~30 seconds), it will generate a file called `diff_review_post_commit.md` in the root of your repository, containing the code suggestions for changes in your current branch not against the main branch.
During the run, another file called `diff_review_post_commit_log.txt` will be created, which contains the logs of the Agent execution. 