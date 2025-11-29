pipeline {
    agent any
    triggers {
        githubPush()
    }
    
    environment {
        REGISTRY_URL = "registry.black-crab.cc"
        IMAGE_NAME   = "greek-encoder"
        FULL_IMAGE   = "${REGISTRY_URL}/${IMAGE_NAME}:latest"
    }

    stages {
        stage('Checkout Source') {
            steps {
                git credentialsId: 'github-creds',
                    url: 'https://github.com/funmicra/scouts-encoder.git',
                    branch: 'master'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }

        stage('Authenticate to Registry') {
             steps {
                 withCredentials([usernamePassword(
                     credentialsId: 'nexus_registry_login',
                      usernameVariable: 'REG_USER',
                       passwordVariable: 'REG_PASS'
                       )]) {
                         sh ''' 
                         echo "$REG_PASS" | docker login ${REGISTRY_URL} -u "$REG_USER" --password-stdin 
                         ''' 
                        } 
                    } 
                }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${FULL_IMAGE}"
            }
        }

        stage('Run Container') {
            steps {
                sh "docker run -d -p 5000:5000 --restart unless-stopped ${FULL_IMAGE}"
            }
        }
    }

    post {
        success { echo "Deployment pipeline executed successfully." }
        failure { echo "Pipeline execution failed. Please review logs." }
    }
}
