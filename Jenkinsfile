pipeline {
    agent any

    environment {
        REPORTS_PATH = 'reports'
        VENV_DIR = 'venv'
        PATH = "${VENV_DIR}/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Elviye/TP-Jenkins-Security.git'
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "=== Création de l'environnement virtuel ==="
                    rm -rf venv
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    
                    echo "Installation depuis requirements.txt"
                    pip install -r requirements.txt
                    
                    pip install pytest pytest-cov
                    echo "=== Dépendances installées avec succès ==="
                    pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Exécution des tests ==="
                    . venv/bin/activate
                    mkdir -p reports
                    
                    echo "Exécution des tests existants"
                    pytest test_app.py -v --junitxml=reports/test-results.xml --cov=. --cov-report=html:reports/coverage
                    
                    echo "=== Tests terminés ==="
                '''
            }
            post {
                always {
                    // Archiver les rapports sans utiliser junit
                    archiveArtifacts artifacts: 'reports/test-results.xml', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'reports/coverage/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('SAST Scan - SonarQube') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        echo "SonarQube scan - Optionnel"
                        # Si sonar-scanner est installé, décommentez la ligne suivante
                        # sonar-scanner -Dsonar.projectKey=TP-Jenkins-Security -Dsonar.sources=. -Dsonar.python.version=3 || echo "SonarQube non disponible"
                    '''
                }
            }
        }

        stage('SCA Scan - Dependency-Check') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        mkdir -p reports
                        
                        echo "Installation de pip-audit..."
                        pip install pip-audit
                        
                        echo "Analyse des vulnérabilités avec pip-audit..."
                        pip-audit --requirement requirements.txt --format html > reports/pip-audit.html || true
                        
                        echo "Rapport généré dans reports/pip-audit.html"
                        
                        # Vérifier les vulnérabilités critiques - CORRECTION: double échappement
                        if [ -f reports/pip-audit.html ]; then
                            if grep -i "critical\\\\|high" reports/pip-audit.html; then
                                echo "⚠️ ATTENTION: Des vulnérabilités critiques ont été détectées !"
                                # Pour bloquer le build, décommentez la ligne suivante :
                                # exit 1
                            else
                                echo "✅ Aucune vulnérabilité critique détectée"
                            fi
                        fi
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/pip-audit.html', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "=== Nettoyage ==="
            sh 'rm -rf venv || true'
            sh 'rm -rf reports || true'
            echo "Pipeline terminé"
        }
        success {
            echo "✅✅✅ SUCCÈS: Tous les tests sont passés ! ✅✅✅"
        }
        failure {
            echo "❌❌❌ ÉCHEC: Le pipeline a échoué ❌❌❌"
        }
    }
}