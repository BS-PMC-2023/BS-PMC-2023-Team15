pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t CreativeStorage .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm CreativeStorage python manage.py test'
            }
        }
    }
}