pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "webhook is working"'
            }
        }

        stage('Repository Info') {
            steps {
                sh 'echo "Current directory:"'
                sh 'pwd'

                sh 'echo "Repository files:"'
                sh 'ls -la'
            }
        }

       stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh '''
                        python3 -m venv .venv
                        .venv/bin/pip install --upgrade pip
                        .venv/bin/pip install -r requirements.txt
                    '''
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