pipeline {
    agent any
    
    parameters {
        string(name: 'MIGRATION_DIRECTORY', defaultValue: './migrations', description: 'Directory containing migration files')
        choice(name: 'RISK_THRESHOLD', choices: ['safe', 'caution', 'dangerous', 'critical'], description: 'Minimum risk level to report')
        booleanParam(name: 'INCLUDE_ROLLBACK_CHECK', defaultValue: true, description: 'Check for rollback script presence')
        booleanParam(name: 'CHECK_BACKUP_REQUIREMENTS', defaultValue: true, description: 'Validate backup procedures')
        booleanParam(name: 'SUGGEST_ALTERNATIVES', defaultValue: true, description: 'Provide safer alternative suggestions')
    }
    
    triggers {
        // Trigger on changes to migration files
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'node --version'
                sh 'npm --version'
                sh 'npm install -g @qodo/command'
            }
        }
        
        stage('Migration Safety Check') {
            steps {
                script {
                    echo "🔍 Analyzing database migrations for safety..."
                    
                    def command = """
                        qodo database_migration_safety \
                            --migration_directory=${params.MIGRATION_DIRECTORY} \
                            --risk_threshold=${params.RISK_THRESHOLD} \
                            --include_rollback_check=${params.INCLUDE_ROLLBACK_CHECK} \
                            --check_backup_requirements=${params.CHECK_BACKUP_REQUIREMENTS} \
                            --suggest_alternatives=${params.SUGGEST_ALTERNATIVES} \
                            --output_file=migration-safety-results.json
                    """
                    
                    sh command
                }
            }
        }
        
        stage('Validate Results') {
            steps {
                script {
                    if (fileExists('migration-safety-results.json')) {
                        def results = readJSON file: 'migration-safety-results.json'
                        
                        echo "📊 Migration Safety Results:"
                        echo "Safety Score: ${results.safety_score}/100"
                        echo "Risk Level: ${results.risk_level}"
                        echo "Safe to Deploy: ${results.safe_to_deploy}"
                        echo "Requires Manual Review: ${results.requires_manual_review}"
                        
                        if (results.dangerous_operations.size() > 0) {
                            echo "⚠️ Dangerous Operations Found:"
                            results.dangerous_operations.each { op ->
                                echo "  - ${op.operation_type} in ${op.file_path}:${op.line_number} (${op.risk_level})"
                            }
                        }
                        
                        if (results.action_items.size() > 0) {
                            echo "📋 Action Items:"
                            results.action_items.each { item ->
                                echo "  - ${item.priority.toUpperCase()}: ${item.action}"
                            }
                        }
                        
                        if (!results.safe_to_deploy) {
                            error "❌ Migrations are not safe to deploy! Risk Level: ${results.risk_level}"
                        } else {
                            echo "✅ Migrations are safe to deploy"
                        }
                    } else {
                        error "⚠️ No migration safety results found"
                    }
                }
            }
        }
        
        stage('Security Review') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    if (fileExists('migration-safety-results.json')) {
                        def results = readJSON file: 'migration-safety-results.json'
                        
                        if (results.risk_level == 'CRITICAL' || results.risk_level == 'DANGEROUS') {
                            echo "⚠️ High-risk migration detected: ${results.risk_level}"
                            echo "Manual approval required before deployment"
                            
                            // Add manual approval step
                            input message: 'Please review the migration safety analysis and approve if safe to deploy', 
                                  ok: 'Approve', 
                                  parameters: [text(name: 'Approval_Notes', description: 'Add any notes about the approval')]
                        } else {
                            echo "✅ Migration risk level acceptable: ${results.risk_level}"
                        }
                    }
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'migration-safety-results.json', fingerprint: true
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'migration-safety-results.json',
                    reportName: 'Migration Safety Report'
                ])
            }
        }
    }
    
    post {
        always {
            echo "Migration safety check completed"
        }
        
        success {
            echo "✅ Migration safety check passed"
        }
        
        failure {
            echo "❌ Migration safety check failed"
            emailext (
                subject: "Migration Safety Check Failed - ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "The migration safety check has failed. Please review the results and address any issues.",
                to: "${env.CHANGE_AUTHOR_EMAIL ?: 'devops@company.com'}"
            )
        }
        
        unstable {
            echo "⚠️ Migration safety check unstable"
        }
    }
}
