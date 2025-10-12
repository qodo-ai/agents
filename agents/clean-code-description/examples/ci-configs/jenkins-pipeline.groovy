// Jenkins Pipeline for Clean Code Description Agent
pipeline {
    agent any

    environment {
        QODO_API_KEY = credentials('qodo-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Clean Code Review') {
            steps {
                script {
                    def targetBranch = env.CHANGE_TARGET ?: 'main'

                    docker.image('qodoai/command:latest').inside {
                        sh """
                            command \
                              --prompt clean_code_description \
                              --agent-file path/to/agent.toml \
                              --key-value-pairs "target_branch=${targetBranch},severity_threshold=medium,focus_areas=docstrings,comments,naming,include_suggestions=true"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.json', allowEmptyArchive: true
        }
    }
}
