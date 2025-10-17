pipeline {
    agent any
    environment {
        QODO_API_KEY = credentials('qodo-api-key')
    }
    stages {
        stage('Clean Code Check') {
            steps {
                script {
                    sh 'npm install -g @qodo-ai/command'
                    sh 'qodo clean_code --set files="." --set language="python" --set report_format="json"'
                }
            }
        }
    }
}
