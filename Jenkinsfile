pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t my-django-app .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm my-django-app python manage.py test'
            }
        }
    }
}