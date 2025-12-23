pipeline {
    agent any

    environment {
        // -------- SONAR --------
        SONAR_HOST_URL = "https://v2code.rtwohealthcare.com"

        // -------- DOCKER / NEXUS --------
        DOCKER_REGISTRY = "v2deploy.rtwohealthcare.com"
        DOCKER_REPO     = "test_v4"

        IMAGE_NAME = "test-v4"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install + Test (Python)') {
            steps {
                sh '''
                    docker run --rm \
                      -v ${WORKSPACE}/backend:/app \
                      -w /app \
                      python:3.10-slim \
                      sh -c "pip install -r requirements.txt && pytest --disable-warnings --maxfail=1"
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                            docker run --rm --network=host \
                              -v ${WORKSPACE}:/src \
                              -w /src \
                              sonarsource/sonar-scanner-cli:5 \
                              sonar-scanner \
                                -Dsonar.projectKey=test_v4 \
                                -Dsonar.sources=backend \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.token=${SONAR_TOKEN}
                        '''
                    }
                }
            }
        }

        stage('Skip Quality Gate') {
            steps {
                echo "Skipping Quality Gate for Python project"
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    cd backend

                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-repo',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} \
                          -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:latest

                        docker logout ${DOCKER_REGISTRY}
                    '''
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
                    sh '''
                        echo "$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} \
                          -u "$DOCKER_USER" --password-stdin

                        docker pull ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

                        docker logout ${DOCKER_REGISTRY}

                        echo "Pull test successful."
                    '''
                }
            }
        }
    }
}
