pipeline {
    agent any
    triggers {
        githubPush()
    }
    
    environment {
        REGISTRY_URL = "registry.black-crab.cc"
        IMAGE_NAME   = "scouts-encoder"
        FULL_IMAGE   = "${env.REGISTRY_URL}/${env.IMAGE_NAME}:latest"
    }

    stages {
        // Stage to connect to the Github repository
        stage('Connect to Github repo') {
            steps {
                git credentialsId: 'github-creds',
                    url: 'https://github.com/funmicra/scouts-encoder.git',
                    branch: 'master'
            }
        }
        
        // Stage to build the Docker image
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${FULL_IMAGE} .
                    """
                }
            }
        }

        // Stage to authenticate to registry
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

        // Stage to push the Docker image to DockerHub
        stage('Push to Nexus Registry') {
            steps {
                sh """
                docker push ${FULL_IMAGE}
                """
            }
        }

        // Stage to deploy the Docker image to a remote host
        stage('Deploy to Remote Host') {
            steps {
                sshagent(['DEBIANSERVER']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no funmicra@192.168.88.22 '
                        docker pull ${FULL_IMAGE}  &&
                        docker stop Greek-Encoder || true &&
                        docker rm Greek-Encoder || true && 
                        docker run -d -p 5050:5000 --name Greek-Encoder --restart unless-stopped ${FULL_IMAGE}                       
                    '
                    """
                }
            }
        }


    }

    post {
        success { echo "Deployment pipeline executed successfully. \n check here.. http://192.168.88.22:5050/" }
        failure { echo "Pipeline execution failed. Please review logs." }
    }
}
