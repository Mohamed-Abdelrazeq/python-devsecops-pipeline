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

        stage('Debug Tests') {
            steps {
                dir('app') {
                    sh '''
                        echo "Current directory:"
                        pwd

                        echo
                        echo "Repository tree:"
                        find .

                        echo
                        echo "Tests directory:"
                        ls -la tests || true

                        echo
                        echo "Contents of test_app.py:"
                        cat tests/test_app.py || true
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('app') {
                    sh '.venv/bin/pytest -v'
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