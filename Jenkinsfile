pipeline {
    agent any

    environment {
        FLASK_HOST = "10.0.1.20"
        FLASK_PUBLIC_IP = "135.225.34.112"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/python-devsecops-pipeline"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        // TODO: REPLACE WITH TruffleHog LATER
        stage('Secret Scan - Gitleaks') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        mkdir -p reports
                        printf '[]\n' > reports/gitleaks-report.json
                        /usr/local/bin/gitleaks version
                        /usr/local/bin/gitleaks detect \
                            --source . \
                            --config secret-scanning/gitleaks.toml \
                            --report-format json \
                            --report-path reports/gitleaks-report.json \
                            --no-banner
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/gitleaks-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Create Virtual Environment') {
            steps {
                dir('app') {
                    sh '''
                        rm -rf .venv
                        python3 -m venv .venv
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh '''
                        .venv/bin/python -m pip install --upgrade pip
                        .venv/bin/pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('SCA - Safety') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    withCredentials([string(credentialsId: 'safety-api-key', variable: 'SAFETY_API_KEY')]) {
                        sh '''
                            mkdir -p reports
                            PYTHONWARNINGS="ignore" app/.venv/bin/python -m safety \
                                --stage cicd \
                                --key "$SAFETY_API_KEY" \
                                scan \
                                --target app \
                                --output json > reports/safety-report.json
                        '''
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/safety-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'app/.venv/bin/python -m pytest app/tests -v'
            }
        }
        
        stage('SAST - Bandit Scan') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        mkdir -p reports
                        app/.venv/bin/python -m bandit -r app \
                            -c sast/.bandit \
                            -x app/.venv,app/tests,app/uploads,app/__pycache__ \
                            -f json \
                            -o reports/bandit-report.json
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/bandit-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t python-devsecops-pipeline:${BUILD_NUMBER} \
                        -t python-devsecops-pipeline:latest \
                        .
                '''
            }
        }

        stage('Container Security - Trivy') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        mkdir -p reports

                        trivy image \
                            --format json \
                            --output reports/trivy-report.json \
                            python-devsecops-pipeline:${BUILD_NUMBER}
                    '''
                }
            }

            post {
                always {
                    archiveArtifacts artifacts: 'reports/trivy-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        docker tag \
                            python-devsecops-pipeline:${BUILD_NUMBER} \
                            ${DOCKER_USERNAME}/python-devsecops-pipeline:${BUILD_NUMBER}

                        docker tag \
                            python-devsecops-pipeline:latest \
                            ${DOCKER_USERNAME}/python-devsecops-pipeline:latest
                    '''
                }
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            --username "$DOCKER_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        docker push ${DOCKER_USERNAME}/python-devsecops-pipeline:${BUILD_NUMBER}

                        docker push ${DOCKER_USERNAME}/python-devsecops-pipeline:latest
                    '''
                }
            }
        }

        stage('Deploy to Flask VM') {
            steps {
                sshagent(credentials: ['flask-vm-ssh']) {

                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub-creds',
                            usernameVariable: 'DOCKERHUB_USERNAME',
                            passwordVariable: 'DOCKERHUB_PASSWORD'
                        )
                    ]) {

                        sh """
                        ssh -o StrictHostKeyChecking=no azureuser@${FLASK_HOST} <<EOF
                        set -e

                        echo "Pulling image..."
                        docker pull ${DOCKERHUB_USERNAME}/python-devsecops-pipeline:${BUILD_NUMBER}

                        echo "Removing previous deployment (if any)..."
                        docker rm -f flask-app 2>/dev/null || true

                        echo "Starting new container..."
                        docker run -d \
                            --name flask-app \
                            --restart unless-stopped \
                            -p 5000:5000 \
                            ${DOCKERHUB_USERNAME}/python-devsecops-pipeline:${BUILD_NUMBER}

                        echo "Deployment completed successfully."
EOF
                        """
                    }
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    echo "Waiting for application to start..."
                    sleep 10

                    echo "Running smoke test..."
                    curl --fail --silent --show-error http://$FLASK_HOST:5000/ > /dev/null

                    echo "Smoke test passed."
                '''
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        mkdir -p reports

                        docker run --rm \
                            -v "$(pwd)/reports:/zap/wrk" \
                            ghcr.io/zaproxy/zaproxy:stable \
                            zap-baseline.py \
                            -t http://${FLASK_HOST}:5000 \
                            -J zap-report.json \
                            -r zap-report.html \
                            -I
                    '''
                }
            }

            post {
                always {
                    archiveArtifacts artifacts: 'reports/zap-report.json', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'reports/zap-report.html', allowEmptyArchive: true
                }
            }
        }
    }    

    post {
        always {
            sh 'docker logout || true'
            echo 'Pipeline finished.'
        }

        success {
            echo 'Build succeeded!'
        }

        failure {
            echo 'Build failed!'
        }
    }
}
