pipeline {
    agent any

    stages {

       stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh '''
                        python3 -m pip install --upgrade pip
                        pip3 install -r requirements.txt
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