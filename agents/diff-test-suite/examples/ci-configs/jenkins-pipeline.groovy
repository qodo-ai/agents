// Jenkins Pipeline for Diff Test Suite Agent
pipeline {
    agent any
    
    environment {
        QODO_API_KEY = credentials('qodo-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }
    
    stages {
        stage('Generate Tests') {
            steps {
                script {
                    def baseBranch = env.CHANGE_TARGET ?: 'main'
                    
                    docker.image('qodoai/command:latest').inside {
                        sh """
                            command \
                              --prompt diff-test-suite \
                              --agent-file path/to/agent.toml \
                              --key-value-pairs "base_branch=${baseBranch},files_to_ignore=package-lock.json,*.md,run_tests=true"
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Archive any generated test files and results
            archiveArtifacts artifacts: 'tests/**/*,**/*.json', allowEmptyArchive: true
        }
    }
}