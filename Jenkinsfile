pipeline {
    agent any

    stages {
        stage('Install pipenv') {
            steps {
                sh 'apt-get update' // Update package lists
                sh 'apt-get install -y python3-dev python3-pip' // Install Python and pip
                sh 'pip install pipenv' // Install pipenv
            }
        }

        stage('Build') {
            steps {
                sh 'pipenv install -r requirements.txt' // Install dependencies from requirements.txt
                sh 'docker build -t creativestorage .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm creativestorage python manage.py test'
            }
        }

        stage('Metrics 1 - Coverage') {
            steps {
                sh 'docker run --rm creativestorage coverage run manage.py test'
                sh 'docker run --rm creativestorage coverage report'
            }
        }

        stage('Metrics 2 - Code Complexity') {
            steps {
                sh 'docker run --rm creativestorage pip install radon'
                sh 'docker run --rm creativestorage radon cc --show-complexity --total-average'
            }
        }

        stage('Metrics 3 - Maintainability Index') {
            steps {
                sh 'docker run --rm creativestorage pip install radon'
                sh 'docker run --rm creativestorage radon mi'
            }
        }
    }

    post {
        success {
            echo 'Build successful!' // Display success message
        }

        failure {
            echo 'Build failed!' // Display failure message
        }
    }
}
