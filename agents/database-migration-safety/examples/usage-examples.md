# Database Migration Safety Agent - Usage Examples

This document provides comprehensive usage examples for the Database Migration Safety Agent, demonstrating various scenarios and configurations.

## Basic Usage Examples

### 1. Simple Migration Analysis
```bash
# Analyze migrations in current directory
qodo database_migration_safety

# Output: JSON report with safety assessment
```

### 2. Directory-Specific Analysis
```bash
# Analyze migrations in specific directory
qodo database_migration_safety --migration_directory=./db/migrations

# Analyze migrations in multiple directories
qodo database_migration_safety --migration_directory=./src/migrations
```

### 3. Database Type Specification
```bash
# Specify database type for better analysis
qodo database_migration_safety --database_type=postgresql
qodo database_migration_safety --database_type=mysql
qodo database_migration_safety --database_type=sqlite
```

## Risk Threshold Examples

### 1. Conservative Safety Check
```bash
# Only report dangerous and critical operations
qodo database_migration_safety --risk_threshold=dangerous
```

### 2. Comprehensive Safety Check
```bash
# Report all operations including safe ones
qodo database_migration_safety --risk_threshold=safe
```

### 3. Critical Operations Only
```bash
# Only report critical operations that block deployment
qodo database_migration_safety --risk_threshold=critical
```

## Advanced Configuration Examples

### 1. Full Safety Analysis
```bash
qodo database_migration_safety \
  --migration_directory=./migrations \
  --database_type=postgresql \
  --risk_threshold=caution \
  --include_rollback_check=true \
  --check_backup_requirements=true \
  --suggest_alternatives=true
```

### 2. Exclude Test Files
```bash
qodo database_migration_safety \
  --exclude_patterns="*.test.sql,*.backup.sql,test_*.sql"
```

### 3. Minimal Analysis
```bash
qodo database_migration_safety \
  --include_rollback_check=false \
  --check_backup_requirements=false \
  --suggest_alternatives=false
```

## CI/CD Integration Examples

### 1. GitHub Actions - PR Check
```yaml
name: Migration Safety Check
on:
  pull_request:
    paths: ['migrations/**', '**/*.sql']

jobs:
  safety-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install Qodo
        run: npm install -g @qodo/command
      - name: Check Migration Safety
        run: qodo database_migration_safety --risk_threshold=caution
```

### 2. GitLab CI - Pipeline Integration
```yaml
migration_safety:
  stage: test
  script:
    - npm install -g @qodo/command
    - qodo database_migration_safety --risk_threshold=caution
  only:
    changes:
      - migrations/**/*
      - "**/*.sql"
```

### 3. Jenkins - Pipeline Job
```groovy
pipeline {
    agent any
    stages {
        stage('Migration Safety') {
            steps {
                sh 'npm install -g @qodo/command'
                sh 'qodo database_migration_safety --risk_threshold=caution'
            }
        }
    }
}
```

## Real-World Scenarios

### Scenario 1: E-commerce Platform Migration
```bash
# Analyze customer data migration
qodo database_migration_safety \
  --migration_directory=./migrations/customer \
  --database_type=postgresql \
  --risk_threshold=dangerous \
  --check_backup_requirements=true
```

**Expected Output:**
```json
{
  "safety_score": 75,
  "risk_level": "DANGEROUS",
  "dangerous_operations": [
    {
      "file_path": "migrations/customer/V001__remove_old_columns.sql",
      "line_number": 3,
      "operation_type": "DROP COLUMN",
      "risk_level": "DANGEROUS",
      "data_loss_risk": true,
      "description": "Removing customer_old_email column"
    }
  ],
  "safe_to_deploy": false,
  "requires_manual_review": true
}
```

### Scenario 2: Log Cleanup Migration
```bash
# Analyze log cleanup migration
qodo database_migration_safety \
  --migration_directory=./migrations/logs \
  --risk_threshold=critical
```

**Expected Output:**
```json
{
  "safety_score": 95,
  "risk_level": "CRITICAL",
  "dangerous_operations": [
    {
      "file_path": "migrations/logs/V002__cleanup_old_logs.sql",
      "line_number": 1,
      "operation_type": "DELETE",
      "risk_level": "CRITICAL",
      "data_loss_risk": true,
      "description": "Mass deletion without WHERE clause"
    }
  ],
  "safe_to_deploy": false,
  "requires_manual_review": true
}
```

### Scenario 3: Safe Schema Update
```bash
# Analyze safe schema update
qodo database_migration_safety \
  --migration_directory=./migrations/schema \
  --risk_threshold=safe
```

**Expected Output:**
```json
{
  "safety_score": 15,
  "risk_level": "SAFE",
  "dangerous_operations": [],
  "safe_to_deploy": true,
  "requires_manual_review": false
}
```

## Output Interpretation Examples

### 1. Safe Migration Output
```json
{
  "safety_score": 20,
  "risk_level": "SAFE",
  "summary": "Migration contains only safe operations: ADD COLUMN, CREATE INDEX",
  "safe_to_deploy": true,
  "requires_manual_review": false,
  "action_items": [],
  "testing_recommendations": [
    "Test new column functionality",
    "Verify index performance impact"
  ]
}
```

### 2. Dangerous Migration Output
```json
{
  "safety_score": 75,
  "risk_level": "DANGEROUS",
  "summary": "Migration contains dangerous operations that could cause data loss",
  "safe_to_deploy": false,
  "requires_manual_review": true,
  "action_items": [
    {
      "priority": "high",
      "action": "Create backup before DROP COLUMN operation",
      "description": "Ensure data is backed up before removing columns"
    }
  ],
  "safer_alternatives": [
    {
      "original_operation": "DROP COLUMN old_email",
      "alternative_approach": "RENAME COLUMN + phased removal",
      "implementation_steps": [
        "RENAME COLUMN old_email TO old_email_deprecated",
        "Update application code",
        "DROP COLUMN old_email_deprecated in future migration"
      ]
    }
  ]
}
```

### 3. Critical Migration Output
```json
{
  "safety_score": 95,
  "risk_level": "CRITICAL",
  "summary": "Migration contains critical operations that will cause data loss",
  "safe_to_deploy": false,
  "requires_manual_review": true,
  "action_items": [
    {
      "priority": "critical",
      "action": "STOP: Do not deploy this migration",
      "description": "Migration will cause irreversible data loss"
    }
  ],
  "backup_requirements": {
    "backup_required": true,
    "backup_procedures_documented": false,
    "backup_recommendations": [
      "Create full database backup",
      "Export affected tables",
      "Test rollback procedures"
    ]
  }
}
```

## Troubleshooting Examples

### 1. No Migration Files Found
```bash
# Check if migration directory exists
ls -la ./migrations/

# Use absolute path
qodo database_migration_safety --migration_directory=/absolute/path/to/migrations
```

### 2. SQL Parsing Errors
```bash
# Check SQL syntax
qodo database_migration_safety --migration_directory=./migrations --database_type=postgresql

# Common fixes:
# - Ensure proper SQL syntax
# - Check for missing semicolons
# - Verify database-specific syntax
```

### 3. Performance Issues with Large Migrations
```bash
# Exclude large backup files
qodo database_migration_safety --exclude_patterns="*.backup.sql,*.dump.sql"

# Focus on specific migration files
qodo database_migration_safety --migration_directory=./migrations/V001*
```

## Best Practices Examples

### 1. Pre-deployment Safety Check
```bash
#!/bin/bash
# pre-deploy-safety-check.sh

echo "🔍 Running pre-deployment migration safety check..."

# Run safety analysis
qodo database_migration_safety \
  --migration_directory=./migrations \
  --risk_threshold=caution \
  --check_backup_requirements=true

# Check exit code
if [ $? -eq 0 ]; then
  echo "✅ Migration safety check passed"
  exit 0
else
  echo "❌ Migration safety check failed"
  exit 1
fi
```

### 2. Automated Rollback Preparation
```bash
#!/bin/bash
# prepare-rollback.sh

echo "🔄 Preparing rollback procedures..."

# Analyze migrations for rollback requirements
qodo database_migration_safety \
  --migration_directory=./migrations \
  --include_rollback_check=true \
  --suggest_alternatives=true

# Generate rollback scripts based on analysis
# (Implementation depends on specific requirements)
```

### 3. Integration with Deployment Pipeline
```bash
#!/bin/bash
# deploy-with-safety-check.sh

set -e  # Exit on any error

echo "🚀 Starting deployment with safety checks..."

# Step 1: Safety check
echo "Step 1: Migration safety analysis"
qodo database_migration_safety --risk_threshold=caution

# Step 2: Backup (if required)
echo "Step 2: Creating backup"
# Backup logic here

# Step 3: Deploy
echo "Step 3: Deploying migrations"
# Deployment logic here

# Step 4: Verify
echo "Step 4: Verifying deployment"
# Verification logic here

echo "✅ Deployment completed successfully"
```

## Monitoring and Alerting Examples

### 1. Slack Notification
```bash
#!/bin/bash
# slack-notification.sh

# Run safety check
qodo database_migration_safety --risk_threshold=caution > results.json

# Parse results
SAFETY_SCORE=$(jq -r '.safety_score' results.json)
RISK_LEVEL=$(jq -r '.risk_level' results.json)
SAFE_TO_DEPLOY=$(jq -r '.safe_to_deploy' results.json)

# Send Slack notification
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"Migration Safety Check: Score $SAFETY_SCORE, Risk $RISK_LEVEL, Safe: $SAFE_TO_DEPLOY\"}" \
  $SLACK_WEBHOOK_URL
```

### 2. Email Alert
```bash
#!/bin/bash
# email-alert.sh

# Run safety check
qodo database_migration_safety --risk_threshold=caution > results.json

# Check if unsafe
SAFE_TO_DEPLOY=$(jq -r '.safe_to_deploy' results.json)

if [ "$SAFE_TO_DEPLOY" = "false" ]; then
  # Send email alert
  echo "Migration safety check failed. Please review." | mail -s "Migration Safety Alert" devops@company.com
fi
```

## Custom Integration Examples

### 1. Custom Risk Threshold
```bash
#!/bin/bash
# custom-risk-check.sh

# Define custom risk levels
CUSTOM_RISK_THRESHOLD="caution"

# Run analysis
qodo database_migration_safety --risk_threshold=$CUSTOM_RISK_THRESHOLD

# Custom processing based on results
# (Implementation depends on specific requirements)
```

### 2. Multi-Environment Safety Check
```bash
#!/bin/bash
# multi-env-safety-check.sh

ENVIRONMENTS=("development" "staging" "production")

for env in "${ENVIRONMENTS[@]}"; do
  echo "🔍 Checking migrations for $env environment..."
  
  qodo database_migration_safety \
    --migration_directory=./migrations/$env \
    --risk_threshold=caution
    
  if [ $? -ne 0 ]; then
    echo "❌ Safety check failed for $env"
    exit 1
  fi
done

echo "✅ All environment safety checks passed"
```

This comprehensive set of examples demonstrates the flexibility and power of the Database Migration Safety Agent across various use cases and integration scenarios.
