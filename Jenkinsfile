pipeline {
    agent any

    stages {

        stage('TEST') {
            steps {
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
                        if [ ! -d ".venv" ]; then
                            python3 -m venv .venv
                        fi

                        . .venv/bin/activate
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