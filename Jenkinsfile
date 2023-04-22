pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y python3-venv'
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