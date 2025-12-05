pipeline {
    agent any

    environment {
        SONAR_HOST_URL = "https://v2code.rtwohealthcare.com"   // FIXED
        SONAR_TOKEN    = "sqp_ab4016bc5eef902acdbc5f5dbf8f0d46815f0035"

        DOCKER_REGISTRY_URL = "v2deploy.rtwohealthcare.com"
        IMAGE_NAME = "test-v4"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Test Python Code') {
            steps {
                sh """
                    docker run --rm \
                        -v \$PWD/backend:/app \
                        -w /app python:3.10-slim sh -c "
                            pip install -r requirements.txt &&
                            pytest --cov=. --cov-report=term --disable-warnings --maxfail=1
                        "
                """
            }
        }

        stage('Verify Coverage >= 80%') {
            steps {
                script {
                    def cov = sh(
                        script: "docker run --rm -v \$PWD/backend:/app -w /app python:3.10-slim \
                                 sh -c \"pytest --cov=. --cov-report=term 2>&1 | grep 'TOTAL' | awk '{print \$4}'\"",
                        returnStdout: true
                    ).trim().replace('%','')

                    cov = cov as Integer

                    if (cov < 80) {
                        error "❌ Code coverage is ${cov}% — BELOW required 80%"
                    } else {
                        echo "✅ Coverage OK: ${cov}%"
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("SonarQube") {
                    sh """
                        docker run --rm \
                           -v \$PWD:/src \
                           -w /src sonarsource/sonar-scanner-cli:4.6 \
                           sonar-scanner \
                               -Dsonar.projectKey=test_v3 \
                               -Dsonar.sources=backend \
                               -Dsonar.host.url=${SONAR_HOST_URL} \
                               -Dsonar.login=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Skip Quality Gate') {
            steps {
                echo "⏭️ Skipping QG intentionally for Python project."
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                    cd backend
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY_URL}/${IMAGE_NAME}:latest
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

                        docker push ${DOCKER_REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKER_REGISTRY_URL}/${IMAGE_NAME}:latest

                        docker logout ${DOCKER_REGISTRY_URL}
                    """
                }
            }
        }

        stage('Verify Pull From Registry') {
            steps {
                sh """
                    docker pull ${DOCKER_REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }

    post {
        failure {
            echo "❌ Pipeline FAILED — Fix errors."
        }
        success {
            echo "✅ Pipeline SUCCESS — All steps passed."
