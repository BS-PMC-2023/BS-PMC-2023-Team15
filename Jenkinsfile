pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'apt-get update'
                sh 'apt-get install -y python3-venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python manage.py test'
            }
        }
    }
}