pipeline {
    agent any

    environment {
        SONAR_HOST_URL = "https://v2code.rtwohealthcare.com"
        SONAR_TOKEN = "sqp_ab4016bc5eef902acdbc5f5dbf8f0d46815f0035"

        DOCKER_REGISTRY = "v2deploy.rtwohealthcare.com"
        DOCKER_REPO     = "test_v4"

        IMAGE_NAME = "test-v4"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install + Test (No Coverage Check)') {
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
                        docker run --rm --network=host \
                            -v ${WORKSPACE}:/src \
                            -w /src \
                            sonarsource/sonar-scanner-cli:5 \
                            sonar-scanner \
                                -Dsonar.projectKey=test_v3 \
                                -Dsonar.sources=backend \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.token=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Skip Quality Gate') {
            steps {
                echo "Skipping Quality Gate for Python project"
            }
        }

        /* ---------------- DOCKER FIXES START ---------------- */

        stage('Docker Build') {
            steps {
                sh """
                    cd backend
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-repo',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} \
                          -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:latest

                        docker logout ${DOCKER_REGISTRY}
                    """
                }
            }
        }

        stage('Verify Pull From Registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-repo',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} \
                          -u "$DOCKER_USER" --password-stdin

                        docker pull ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

                        docker logout ${DOCKER_REGISTRY}

                        echo "Pull test successful."
                    """
                }
            }
        }

        /* ---------------- DOCKER FIXES END ---------------- */
    }
}
