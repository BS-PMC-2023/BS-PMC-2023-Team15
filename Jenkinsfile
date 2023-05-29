
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
                //sh 'docker run --rm creativestorage coverage report'


            }
        }


        stage('Metrics 2 - Radon') {
            steps {
                sh 'docker run --rm creativestorage radon cc --show-complexity --total-average main/tests.py'
            }
        }

        stage('Metrics 3 - Bandit') {
            steps {
                sh 'docker run --rm creativestorage bandit -r main/tests.py'
            }
        }

        stage('Metrics 4 - Pylint') {
            steps {
                sh 'docker run --rm creativestorage pylint creativestorage'
            }
        }
    }
}