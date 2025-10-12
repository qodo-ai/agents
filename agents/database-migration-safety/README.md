# Database Migration Safety Agent

A comprehensive safety analysis tool for database migrations that prevents catastrophic data loss and production incidents through deterministic SQL parsing, automated risk assessment, dangerous operation detection, and safer alternative recommendations.

## 🎯 Purpose

Database migrations are critical operations that can cause catastrophic data loss, extended downtime, and production incidents if not properly managed. This agent provides automated safety analysis to:

- **Prevent Data Loss**: Detect dangerous operations that could cause data loss
- **Assess Migration Risks**: Evaluate the safety of migration operations
- **Provide Safer Alternatives**: Suggest safer approaches for risky operations
- **Validate Safety Practices**: Check for backup procedures and rollback capabilities
- **Enable Safe Deployment**: Provide clear go/no-go recommendations for CI/CD

## 🚀 Features

### Core Safety Analysis
- **Deterministic SQL Parsing**: Uses reliable tokenization and AST-based analysis for accurate operation detection
- **Dangerous Operation Detection**: Identifies DROP, TRUNCATE, DELETE without WHERE, and other risky operations
- **Data Loss Risk Assessment**: Evaluates potential for data loss and business impact
- **Safety Practice Validation**: Checks for backup procedures, rollback scripts, and best practices
- **Risk Scoring**: Provides quantitative safety scores (0-100) with risk level classification

### Comprehensive Coverage
- **Multiple Database Support**: PostgreSQL, MySQL, SQLite, SQL Server, Oracle
- **Framework Agnostic**: Works with any migration system (Flyway, Liquibase, Rails, etc.)
- **Pattern Recognition**: Detects migration files using common naming conventions
- **Deterministic SQL Analysis**: Uses tokenization and AST-based parsing to identify operation types and risks

### Actionable Recommendations
- **Safer Alternatives**: Provides specific code suggestions for risky operations
- **Rollback Preparation**: Identifies missing rollback scripts and suggests improvements
- **Testing Recommendations**: Suggests testing strategies for migration validation
- **Action Items**: Prioritized list of required actions before deployment

## 📋 Usage

### Basic Usage
```bash
qodo database_migration_safety
```

### Advanced Usage
```bash
# Analyze specific directory
qodo database_migration_safety --migration_directory=./migrations

# Specify database type for better analysis
qodo database_migration_safety --database_type=postgresql

# Set risk threshold
qodo database_migration_safety --risk_threshold=dangerous

# Include rollback validation
qodo database_migration_safety --include_rollback_check=true

# Exclude specific file patterns
qodo database_migration_safety --exclude_patterns="*.backup.sql,*.test.sql"
```

### CI/CD Integration
```bash
# Fail pipeline if migrations are unsafe
qodo database_migration_safety --risk_threshold=caution

# Check for backup requirements
qodo database_migration_safety --check_backup_requirements=true
```

## 🔧 Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `migration_directory` | string | "." | Directory to scan for migration files |
| `database_type` | string | auto-detect | Database type (postgresql, mysql, sqlite, sqlserver, oracle) |
| `risk_threshold` | string | "caution" | Minimum risk level to report (safe, caution, dangerous, critical) |
| `include_rollback_check` | boolean | true | Check for rollback script presence |
| `check_backup_requirements` | boolean | true | Validate backup procedures for destructive operations |
| `suggest_alternatives` | boolean | true | Provide safer alternative suggestions |
| `exclude_patterns` | string | "" | Comma-separated list of file patterns to exclude |

## 📊 Risk Levels

### CRITICAL (90-100)
- Immediate deployment block required
- Operations that will cause data loss
- No rollback capability available

### DANGEROUS (70-89)
- High risk operations requiring immediate attention
- Potential for significant data loss
- Limited rollback capabilities

### CAUTION (40-69)
- Moderate risk operations
- Review recommended before deployment
- Some safety measures missing

### SAFE (0-39)
- Low risk operations
- Proceed with normal deployment process
- Safety measures in place

## 🚨 Dangerous Operations Detected

### Critical Risk Operations
- `DROP TABLE` - Complete table removal
- `DROP DATABASE` - Database deletion
- `TRUNCATE TABLE` - Complete data removal
- `DELETE` without WHERE clause - Mass data deletion
- `DROP COLUMN` - Column removal (potential data loss)
- `ALTER TABLE DROP CONSTRAINT` - Constraint removal

### High Risk Operations
- `ALTER COLUMN` - Column modifications (type changes, nullability)
- `DROP INDEX` - Index removal (performance impact)
- `ALTER TABLE MODIFY` - Column type changes
- `RENAME TABLE/COLUMN` - Structural changes
- `ADD/DROP FOREIGN KEY` - Relationship changes

### Medium Risk Operations
- `CREATE INDEX` - Large index creation (performance impact)
- `ALTER TABLE ADD COLUMN` - New column additions
- `UPDATE` statements - Data modifications
- `INSERT` statements - Data additions

## 📈 Output Schema

The agent returns a comprehensive JSON report with:

```json
{
  "safety_score": 85,
  "risk_level": "DANGEROUS",
  "migration_files_analyzed": [...],
  "dangerous_operations": [...],
  "safety_violations": [...],
  "rollback_assessment": {...},
  "backup_requirements": {...},
  "safer_alternatives": [...],
  "action_items": [...],
  "testing_recommendations": [...],
  "summary": "Migration analysis summary",
  "safe_to_deploy": false,
  "requires_manual_review": true
}
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Database Migration Safety Check
on: [pull_request]
jobs:
  migration-safety:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Migration Safety
        run: |
          npm install -g @qodo/command
          qodo database_migration_safety --risk_threshold=caution
```

### GitLab CI Example
```yaml
migration_safety_check:
  stage: test
  script:
    - npm install -g @qodo/command
    - qodo database_migration_safety --risk_threshold=caution
  only:
    - merge_requests
```

## 🛡️ Safety Best Practices

### Before Running Migrations
1. **Always Backup**: Create full database backups before destructive operations
2. **Test in Staging**: Run migrations in staging environment first
3. **Plan Rollbacks**: Ensure rollback scripts are available and tested
4. **Review Changes**: Manually review high-risk operations
5. **Monitor Performance**: Watch for performance impacts during migration

### Migration Design
1. **Use Transactions**: Wrap migrations in transactions when possible
2. **Make Idempotent**: Ensure migrations can be run multiple times safely
3. **Follow Naming Conventions**: Use consistent, descriptive naming
4. **Document Changes**: Include clear descriptions of what each migration does
5. **Version Control**: Keep all migrations in version control

## 📚 Examples

### Example 1: Safe Migration
```sql
-- V001__add_user_email_column.sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
CREATE INDEX idx_users_email ON users(email);
```

**Analysis Result**: SAFE (Score: 15)
- Low risk operations
- No data loss potential
- Proper indexing for performance

### Example 2: Dangerous Migration
```sql
-- V002__remove_old_columns.sql
ALTER TABLE users DROP COLUMN old_email;
ALTER TABLE users DROP COLUMN temp_data;
```

**Analysis Result**: DANGEROUS (Score: 75)
- High risk operations (DROP COLUMN)
- Potential data loss
- No rollback capability

### Example 3: Critical Migration
```sql
-- V003__cleanup_old_data.sql
DELETE FROM logs WHERE created_at < '2020-01-01';
TRUNCATE TABLE temp_sessions;
```

**Analysis Result**: CRITICAL (Score: 95)
- Mass data deletion operations
- No WHERE clause validation
- High data loss risk

## 🔍 Troubleshooting

### Common Issues

**No migration files found**
- Check the `migration_directory` parameter
- Verify file naming conventions
- Ensure files have `.sql` extension

**Analysis errors**
- Check SQL syntax in migration files
- Verify database type specification
- Review file permissions

**False positives**
- Adjust `risk_threshold` parameter
- Use `exclude_patterns` for test files
- Review migration context and business requirements

## 🤝 Contributing

Contributions are welcome! Please see the main repository for contribution guidelines.

## 📄 License

This agent is part of the Qodo Agents collection. See the main repository for license information.

## 🆘 Support

For issues and questions:
- Create an issue in the main repository
- Check existing documentation
- Review example configurations

---

**Remember**: Database migrations are powerful but dangerous operations. Always prioritize safety over speed, and use this agent as part of a comprehensive migration safety strategy.
