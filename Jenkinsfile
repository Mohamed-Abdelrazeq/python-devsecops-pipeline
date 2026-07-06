pipeline {
    agent any

    stages {

        stage('Secret Scan - Gitleaks') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        mkdir -p reports
                        gitleaks detect \
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

        stage('Run Tests') {
            steps {
                sh 'app/.venv/bin/python -m pytest app/tests -v'
            }
        }
        
        stage('SAST - Bandit Scan') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
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

    }

    post {
        always {
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
