pipeline {
    agent any

    environment {
        SONAR_HOST_URL = "https://v2code.rtwohealthcare.com"
        SONAR_TOKEN = "sqp_ab4016bc5eef902acdbc5f5dbf8f0d46815f0035"

        DOCKER_REGISTRY_URL = "v2deploy.rtwohealthcare.com"
        REGISTRY_PATH = "/docker-hosted"
        REGISTRY_HOST = "${DOCKER_REGISTRY_URL}${REGISTRY_PATH}"

        IMAGE_NAME = "test-v4"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install + Test + Coverage') {
            steps {
                sh """
                    docker run --rm \
                        -v $WORKSPACE/backend:/app \
                        -w /app python:3.10-slim \
                        sh -c "
                            pip install -r requirements.txt &&
                            pytest --cov=. --cov-report=xml --disable-warnings --maxfail=1
                        "
                """
            }
        }

        stage('Verify Coverage >= 80%') {
            steps {
                script {
                    def cov = sh(
                        script: "grep '<coverage ' backend/coverage.xml | sed -E 's/.*line-rate=\"([0-9\\.]+)\".*/\\1/'",
                        returnStdout: true
                    ).trim()

                    def percent = (cov.toFloat() * 100).toInteger()
                    echo "Coverage: ${percent}%"

                    if (percent < 80) {
                        error "Coverage below 80%. Failing pipeline."
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        docker run --rm \
                            -v $WORKSPACE:/src \
                            -w /src sonarsource/sonar-scanner-cli:4.6 \
                            sonar-scanner \
                                -Dsonar.projectKey=test_v3 \
                                -Dsonar.sources=backend \
                                -Dsonar.python.coverage.reportPaths=backend/coverage.xml \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.token=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Skip Quality Gate') {
            steps {
                echo "Python project — Quality Gate manually skipped."
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
                sh "docker pull ${REGISTRY_HOST}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}
