pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t creativestorage .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm creativestorage python manage.py test'
            }
        }
    }
}