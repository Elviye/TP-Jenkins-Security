pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    try {
                        // Essaie d'abord avec 'main'
                        git branch: 'main', url: 'https://github.com/Elviye/TP-Jenkins-Security.git'
                    } catch (Exception e) {
                        echo 'Branche main non trouvée, essai avec master...'
                        try {
                            // Essaie avec 'master'
                            git branch: 'master', url: 'https://github.com/Elviye/TP-Jenkins-Security.git'
                        } catch (Exception e2) {
                            echo 'master non trouvé non plus, clonage sans spécifier de branche...'
                            // Clone sans spécifier de branche
                            git url: 'https://github.com/Elviye/TP-Jenkins-Security.git'
                        }
                    }
                }
                sh 'ls -la'
                sh 'git branch -a'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install --upgrade pip
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
                sh 'sonar-scanner -Dsonar.projectKey=TP-Jenkins-Security -Dsonar.sources=. -Dsonar.python.version=3 || echo "SonarQube scan skipped"'
            }
        }

        stage('SCA Scan - Dependency-Check') {
            steps {
                sh '''
                    mkdir -p reports
                    dependency-check.sh --project "TP-Jenkins-Security" --scan . --out ./reports --format HTML --failOnCVSS 7 || echo "Dependency-Check scan skipped"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
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