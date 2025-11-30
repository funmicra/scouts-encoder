pipeline {
    agent any
    triggers {
        githubPush()
    }
    
    environment {
        REGISTRY_URL = "docker.io/funmicra"
        IMAGE_NAME   = "scouts-encoder"
        FULL_IMAGE   = "${env.REGISTRY_URL}/${env.IMAGE_NAME}:latest"
    }

    stages {

        stage('Connect to Github repo') {
            steps {
                git credentialsId: 'github-creds',
                    url: 'https://github.com/funmicra/scouts-encoder.git',
                    branch: 'master'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${FULL_IMAGE} .
                    """
                }
            }
        }

        stage('Authenticate to Registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DOCKER_HUB',
                    usernameVariable: 'REG_USER',
                    passwordVariable: 'REG_PASS'
                )]) {
                    sh '''
                    echo "$REG_PASS" | docker login ${REGISTRY_URL} -u "$REG_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh """
                docker push ${FULL_IMAGE}
                """
            }
        }


        stage('Deploy to Remote Host') {
            steps {
                sshagent(['DEBIANSERVER']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no funmicra@192.168.88.22 '
                        docker pull funmicra/greek-encoder:latest &&
                        docker stop greek-encoder || true &&
                        docker rm greek-encoder || true &&
                        docker run -d -p 5050:5000 --name Greek-Encoder --restart unless-stopped funmicra/greek-encoder:latest
                    '
                    """
                }
            }
        }
    }

    post {
        success { echo "Deployment pipeline executed successfully." }
        failure { echo "Pipeline execution failed. Please review logs." }
    }
}
