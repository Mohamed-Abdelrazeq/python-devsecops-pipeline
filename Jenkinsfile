pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh '''
                        rm -rf .venv

                        python3 -m venv .venv

                        . .venv/bin/activate

                        python -m pip install --upgrade pip

                        pip install -r requirements.txt
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