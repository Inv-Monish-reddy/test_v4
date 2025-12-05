pipeline {
    agent any

    environment {
        SONAR_HOST_URL = "http://10.80.5.127:9070"
        SONAR_TOKEN = "sqp_ab4016bc5eef902acdbc5f5dbf8f0d46815f0035"

        DOCKER_REGISTRY_URL = "v2deploy.rtwohealthcare.com"
        REGISTRY_PATH = "/docker-hosted"
        REGISTRY_HOST = "${DOCKER_REGISTRY_URL}${REGISTRY_PATH}"

        IMAGE_NAME = "test-v4"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install + Test (No coverage check)') {
            steps {
                sh """
                    docker run --rm \
                        -v ${WORKSPACE}/backend:/app \
                        -w /app \
                        python:3.10-slim \
                        sh -c "pip install -r requirements.txt && pytest --disable-warnings --maxfail=1"
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        docker run --rm \
                            -v ${WORKSPACE}:/src \
                            -w /src \
                            sonarsource/sonar-scanner-cli:4.6 \
                            sonar-scanner \
                                -Dsonar.projectKey=test_v4 \
                                -Dsonar.sources=backend \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.login=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Skip Quality Gate') {
            steps {
                echo "⏭️ Skipping Quality Gate for Python project"
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                    cd backend
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY_HOST}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY_HOST}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'nexus-docker-cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh """
                        echo "$PASS" | docker login ${DOCKER_REGISTRY_URL} -u "$USER" --password-stdin
                        docker push ${REGISTRY_HOST}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${REGISTRY_HOST}/${IMAGE_NAME}:latest
                        docker logout ${DOCKER_REGISTRY_URL}
                    """
                }
            }
        }

        stage('Verify Pull From Registry') {
            steps {
                sh """
                    docker pull ${REGISTRY_HOST}/${IMAGE_NAME}:${IMAGE_TAG}
                    echo "Pull test successful."
                """
            }
        }
    }
}
