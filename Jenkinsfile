pipeline {
    agent any

    tools {
        // Déclaration des outils installés (optionnel mais recommandé)
        maven 'maven-3' // Si vous avez Maven installé dans Jenkins
    }

    environment {
        // Définir les chemins des rapports
        REPORTS_PATH = 'reports'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Cloner le dépôt avec la branche main (la branche par défaut)
                git branch: 'main', 
                    url: 'https://github.com/Elviye/TP-Jenkins-Security.git'
                
                // Afficher le contenu cloné pour vérification
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installer les dépendances Python
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
            post {
                success {
                    echo '✅ Dépendances installées avec succès'
                }
                failure {
                    echo '❌ Échec de l\'installation des dépendances'
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Exécuter les tests unitaires avec pytest
                sh 'pytest test_app.py -v --junitxml=reports/test-results.xml'
            }
            post {
                always {
                    // Publier les résultats des tests dans Jenkins
                    junit 'reports/test-results.xml'
                }
                success {
                    echo '✅ Tous les tests ont réussi'
                }
                failure {
                    echo '❌ Des tests ont échoué'
                }
            }
        }

        stage('SAST Scan - SonarQube') {
            steps {
                // Analyse SAST avec SonarQube
                withSonarQubeEnv('SonarQube') { // Doit correspondre au nom configuré dans Jenkins
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=TP-Jenkins-Security \
                          -Dsonar.projectName="TP Jenkins Security" \
                          -Dsonar.sources=. \
                          -Dsonar.python.version=3 \
                          -Dsonar.sourceEncoding=UTF-8
                    '''
                }
            }
            post {
                success {
                    echo '✅ Analyse SonarQube terminée'
                    echo '📊 Consultez les résultats sur http://localhost:9000'
                }
            }
        }

        stage('SCA Scan - Dependency-Check') {
            steps {
                // Créer le dossier des rapports s'il n'existe pas
                sh 'mkdir -p reports'
                
                // Scanner les dépendances avec seuil CVSS 7
                // Le build échouera si une vulnérabilité avec score >= 7 est trouvée
                sh '''
                    dependency-check.sh \
                      --project "TP-Jenkins-Security" \
                      --scan . \
                      --format HTML \
                      --format XML \
                      --out ./reports \
                      --failOnCVSS 7 \
                      --prettyPrint
                '''
            }
            post {
                always {
                    // Publier le rapport Dependency-Check dans Jenkins
                    dependencyCheckPublisher pattern: 'reports/dependency-check-report.xml'
                    
                    // Archiver les rapports HTML
                    archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
                }
                success {
                    echo '✅ Scan SCA terminé - aucune vulnérabilité critique (CVSS < 7) détectée'
                }
                failure {
                    echo '❌ Scan SCA échoué - une ou plusieurs vulnérabilités critiques (CVSS ≥ 7) ont été détectées'
                }
            }
        }
    }

    post {
        always {
            // Nettoyage (optionnel)
            echo '🏁 Pipeline terminé'
            
            // Afficher le contenu des rapports
            sh 'ls -la reports/ || true'
        }
        success {
            // Actions en cas de succès global
            echo '✅✅✅ Pipeline exécuté avec SUCCÈS ! ✅✅✅'
        }
        failure {
            // Actions en cas d'échec global
            echo '❌❌❌ Le pipeline a ÉCHOUÉ ! ❌❌❌'
        }
        unstable {
            // Actions si le pipeline est instable (ex: tests échoués mais build continue)
            echo '⚠️ Pipeline instable - vérifiez les rapports'
        }
    }
}