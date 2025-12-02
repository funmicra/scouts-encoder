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

        // Stage to authenticate to DockerHub registry
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

        // Stage to push the Docker image to DockerHub
        stage('Push to DockerHub') {
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
                        docker pull funmicra/greek-encoder:latest &&
                        docker stop greek-encoder || true &&
                        docker rm greek-encoder || true && 
                        docker run -d --name greek-encoder -p 5050:5050 funmicra/greek-encoder:latest                       
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
