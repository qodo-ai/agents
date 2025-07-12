# Qodo Agent: Static Site Deployment

This agent automates the deployment of static websites (such as Webflow exports) to AWS S3 and CloudFront. It streamlines the process of hosting static content on AWS, ensuring proper configuration, cache invalidation, and deployment validation. The agent is defined in `agent.toml` and uses the desktop-commander mcp server.

---

## Demo

Watch a demo of the deployment workflow in action:

[![Watch the demo](https://img.youtube.com/vi/5QaXuSn2XGs/hqdefault.jpg)](https://youtu.be/5QaXuSn2XGs)


---

## Features
- Validates AWS CLI installation and configuration
- Selects or prompts for AWS CLI profile
- Creates and configures S3 bucket for static hosting
- Syncs local static files to S3
- Creates or updates a CloudFront distribution with secure access (OAI/OAC)
- Invalidates CloudFront cache for updated files
- Provides deployment summary and validation steps

---

## Configuration Options
The agent accepts the following arguments (as defined in `deploy-static.yaml`):

| Argument   | Type    | Required | Description                                                                                 |
|------------|---------|----------|---------------------------------------------------------------------------------------------|
| `folder`   | string  | Yes      | Directory containing the Webflow-exported static files to deploy.                            |
| `bucket`   | string  | No      | Name of the target S3 bucket for hosting the static site.                                    |
| `profile`  | string  | No       | AWS CLI profile to use. If omitted, uses `AWS_PROFILE` environment variable or default.      |

---

## Usage
The agent is invoked via the `deploy-static` command. Below are example usages for different scenarios.

### Prerequisites

- AWS CLI installed and configured (see [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- AWS credentials configured and authenticated
- [Desktop Commander MCP server](https://github.com/wonderwhy-er/DesktopCommanderMCP) installed
- [Qodo CLI](https://docs.qodo.ai/qodo-documentation/qodo-command/getting-started/setup-and-quickstart) installed (`npm install -g @qodo/command`)

### Basic Usage
```
qodo deploy-static --set folder=./webflow-export
```

### Specify S3 Bucket
```
qodo deploy-static --set folder=./webflow-export --set bucket=my-static-site-bucket
```

### Specify AWS Profile
```
qodo deploy-static --set folder=./webflow-export --set profile=my-aws-profile
```

### Full Example
```
qodo deploy-static --set folder=./webflow-export --set bucket=my-static-site-bucket --set profile=my-aws-profile
```

---

## Workflow Steps
1. **AWS CLI Validation**: Checks for AWS CLI installation and configuration.
2. **Profile Selection**: Lists available AWS CLI profiles and selects the one to use.
3. **S3 Bucket Setup**: Creates the S3 bucket if it does not exist and configures it for static hosting.
4. **File Sync**: Uploads and syncs local static files to the S3 bucket.
5. **CloudFront Distribution**: Creates or updates a CloudFront distribution with secure access (OAI/OAC).
6. **Cache Invalidation**: Invalidates CloudFront cache for updated files to ensure changes are live.
7. **Deployment Validation**: Outputs the CloudFront distribution domain for testing.

---

## Output Schema
After execution, the agent returns a summary object with the following fields:
- `profileInUse`: The AWS CLI profile used for deployment.
- `bucket`: The S3 bucket name.
- `distributionId`: The CloudFront distribution ID.
- `distributionDomain`: The CloudFront distribution domain name.
- `invalidatedPaths`: List of paths invalidated in CloudFront.
- `syncSummary`: Summary of the file sync operation.

---

## Troubleshooting Guide

### AWS CLI Not Installed or Not Found
- **Symptom:** The agent fails with an error about AWS CLI not being found.
- **Solution:** Install the AWS CLI and ensure it is in your system PATH. Verify with `aws --version`.

### AWS CLI Not Logged In
- **Symptom:** The agent fails with an error about AWS CLI not being logged in.
- **Solution:** Run `aws configure sso` to log in to the AWS CLI.

### AWS Profile Not Configured
- **Symptom:** The agent cannot find or use the specified AWS profile.
- **Solution:** Run `aws configure --profile <profile-name>` to set up the profile, or use the default profile.

### S3 Bucket Already Exists (Ownership Error)
- **Symptom:** Error about S3 bucket already existing but not owned by you.
- **Solution:** Choose a unique bucket name or ensure you have access to the existing bucket.

### CloudFront Distribution Issues
- **Symptom:** CloudFront distribution is not created or updated as expected.
- **Solution:** Check AWS permissions for CloudFront, and ensure the agent has the necessary IAM rights.

### Files Not Updating (Cache Not Invalidated)
- **Symptom:** Changes are not visible after deployment.
- **Solution:** Ensure cache invalidation step completes. Check `invalidatedPaths` in the output. Manually invalidate if needed via AWS Console.

### Permission Denied Errors
- **Symptom:** Access denied when syncing files or updating CloudFront.
- **Solution:** Verify your AWS credentials and permissions for S3 and CloudFront.

---

## Tools Used
- `filesystem`
- `desktop-commander`

---

## License
See LICENSE file for details.
