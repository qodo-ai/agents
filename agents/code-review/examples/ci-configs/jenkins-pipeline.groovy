// Jenkins Pipeline for Code Review Agent
pipeline {
    agent any
    
    environment {
        QODO_API_KEY = credentials('qodo-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }
    
    stages {
        stage('Code Review') {
            steps {
                script {
                    def targetBranch = env.CHANGE_TARGET ?: 'main'
                    
                    docker.image('qodoai/command:latest').inside {
                        sh """
                            command \
                              --prompt code-review \
                              --agent-file path/to/agent.toml \
                              --key-value-pairs "target_branch=${targetBranch},severity_threshold=medium,focus_areas=security,performance,include_suggestions=true"
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Archive any generated artifacts
            archiveArtifacts artifacts: '**/*.json', allowEmptyArchive: true
        }
    }
}