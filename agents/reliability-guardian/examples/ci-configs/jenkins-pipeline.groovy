// Jenkins Pipeline for Reliability Guardian Agent
pipeline {
    agent any

    environment {
        QODO_API_KEY = credentials('qodo-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Reliability Guardian') {
            steps {
                script {
                    def targetBranch = env.CHANGE_TARGET ?: 'main'

                    docker.image('qodoai/command:latest').inside {
                        sh """
                            command \
                              --prompt reliability_guardian \
                              --agent-file path/to/agent.toml \
                              --key-value-pairs "target_branch=${targetBranch},max_commits=5,mutation_testing=true,fuzz_testing=true"
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