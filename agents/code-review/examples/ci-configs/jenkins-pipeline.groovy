// Jenkins Pipeline for Code Review Agent
pipeline {
    agent any
    
    environment {
        QODO_API_KEY = credentials('qodo-api-key')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g @qodo/gen'
            }
        }
        
        stage('Code Review') {
            steps {
                script {
                    def reviewResult = sh(
                        script: '''
                            qodo -q --ci code_review \
                                --target_branch=${CHANGE_TARGET} \
                                --severity_threshold=medium \
                                --include_suggestions=true \
                                > review-results.json
                            cat review-results.json
                        ''',
                        returnStdout: true
                    )
                    
                    def results = readJSON file: 'review-results.json'
                    
                    if (!results.approved) {
                        currentBuild.result = 'UNSTABLE'
                        error("Code review failed: ${results.summary.total_issues} issues found")
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'review-results.json'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'review-results.json',
                        reportName: 'Code Review Report'
                    ])
                }
            }
        }
        
        stage('Security Check') {
            when {
                anyOf {
                    changeset "src/auth/**"
                    changeset "src/security/**"
                    changeset "src/api/**"
                }
            }
            steps {
                sh '''
                    qodo -q --ci code_review \
                        --focus_areas=security \
                        --severity_threshold=high \
                        > security-results.json
                '''
                script {
                    def securityResults = readJSON file: 'security-results.json'
                    if (securityResults.summary.security_issues > 0) {
                        error("Security issues found!")
                    }
                }
            }
        }
    }
    
    post {
        failure {
            emailext (
                subject: "Code Review Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Code review failed for ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}