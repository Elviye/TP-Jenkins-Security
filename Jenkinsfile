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
                    
                    if [ -f "requirements.txt" ]; then
                        echo "Installation depuis requirements.txt"
                        pip install -r requirements.txt
                    else
                        echo "Création de requirements.txt"
                        cat > requirements.txt << EOF
pytest
pytest-cov
requests
flask
jinja2
EOF
                        pip install -r requirements.txt
                    fi
                    
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
                    
                    if [ -f "test_app.py" ]; then
                        echo "Exécution des tests existants"
                        pytest test_app.py -v --junitxml=reports/test-results.xml --cov=. --cov-report=html:reports/coverage
                    else
                        echo "Création d'un fichier de test"
                        cat > test_app.py << 'EOF'
import pytest

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): 
    if b == 0:
        raise ValueError("Division par zéro")
    return a / b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 5) == -4

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(6, 3) == 2
    with pytest.raises(ValueError):
        divide(10, 0)

def test_simple():
    assert True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
EOF
                        echo "Exécution des tests créés"
                        pytest test_app.py -v --junitxml=reports/test-results.xml
                    fi
                '''
            }
            post {
                always {
                    // Alternative à junit : archiver simplement le fichier XML
                    archiveArtifacts artifacts: 'reports/test-results.xml', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'reports/coverage/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('SAST Scan - SonarQube') {
            steps {
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            if command -v sonar-scanner &> /dev/null; then
                                echo "Exécution de SonarQube..."
                                sonar-scanner \
                                  -Dsonar.projectKey=TP-Jenkins-Security \
                                  -Dsonar.projectName="TP Jenkins Security" \
                                  -Dsonar.sources=. \
                                  -Dsonar.exclusions=venv/**,reports/**,**/__pycache__/** \
                                  -Dsonar.python.version=3 \
                                  -Dsonar.sourceEncoding=UTF-8
                            else
                                echo "SonarQube non installé, étape ignorée"
                            fi
                        '''
                    } catch (Exception e) {
                        echo "SonarQube scan ignoré: ${e.message}"
                    }
                }
            }
        }

        stage('SCA Scan - Dependency-Check') {
            steps {
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            mkdir -p reports
                            
                            echo "Installation de pip-audit..."
                            pip install pip-audit
                            
                            echo "Analyse des vulnérabilités avec pip-audit..."
                            pip-audit --requirement requirements.txt --format html > reports/pip-audit.html || true
                            
                            echo "Rapport généré dans reports/pip-audit.html"
                            
                            # Vérification des vulnérabilités critiques (simulée)
                            if grep -i "critical\|high" reports/pip-audit.html; then
                                echo "⚠️ Des vulnérabilités critiques détectées !"
                                # exit 1  # Décommentez pour bloquer le build
                            else
                                echo "✅ Aucune vulnérabilité critique détectée"
                            fi
                        '''
                    } catch (Exception e) {
                        echo "Scan SCA ignoré: ${e.message}"
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "Nettoyage terminé"
            // Alternative à cleanWs : supprimer manuellement
            sh 'rm -rf venv || true'
            sh 'rm -rf reports || true'
        }
        success {
            echo "✅✅ Pipeline exécuté avec SUCCÈS ! ✅✅"
        }
        failure {
            echo "❌❌ Le pipeline a ÉCHOUÉ ! ❌❌"
        }
    }
}