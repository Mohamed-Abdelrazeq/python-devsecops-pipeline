pipeline {
    agent any

    stages {

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
                sh '.venv/bin/python -m pytest app/tests -v'
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