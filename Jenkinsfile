
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
         //coverage run manage.py test
         //coverage report
        stage('Metrics 1 - Coverage') {
            steps {
                sh 'docker run --rm creativestorage coverage run manage.py test'
                sh 'docker run --rm creativestorage coverage report'

            }
        }
    }
}