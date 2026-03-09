pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Elviye/TP-Jenkins-Security.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest test_app.py -v'
            }
        }

        stage('SAST Scan - SonarQube') {
            steps {
                sh 'sonar-scanner -Dsonar.projectKey=TP-Jenkins-Security -Dsonar.sources=. -Dsonar.python.version=3'
            }
        }

        stage('SCA Scan - Dependency-Check') {
            steps {
                sh '''
                    mkdir -p reports
                    dependency-check.sh --project "TP-Jenkins-Security" --scan . --out ./reports --format HTML --failOnCVSS 7
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/*.html'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline exécuté avec succès!'
        }
        failure {
            echo 'Le pipeline a échoué!'
        }
    }
}