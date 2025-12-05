pipeline {
    agent any

    stages {
        
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Python Script') {
            steps {
                sh """
                    docker run --rm \
                        -v ${WORKSPACE}/backend:/app \
                        -w /app python:3.10-slim \
                        python app.py
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline Finished"
        }
    }
}
