pipeline {
    agent {
        docker {
            image 'python:3'
            args '--shm-size=1g -u root'
        }
    }

    stages {
        stage('install requirements') {
            steps {
                sh "pip3 install -r requirements.txt"
            }
        }

        stage('unit testing') {
            steps {
                sh "pytest tests/unit"
            }
        }

        stage('integration testing') {
            steps {
                sh "pytest tests/integration"
            }
        }
    }
}