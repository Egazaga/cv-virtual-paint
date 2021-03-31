pipeline {
    agent {
        docker {
            image 'yaroslaver/cv-virtual-paint'
            args '--shm-size=1g -u root'
        }
    }

    stages {
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

        stage('system testing') {
            steps {
                sh "pytest tests/system"
            }
        }
    }
}