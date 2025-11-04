pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'weather-dashboard'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        AWS_DEFAULT_REGION = 'us-east-1'
        EC2_INSTANCE_IP = '' // Will be set during deployment
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh """
                        docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -m pytest tests/
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh """
                        echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Deploy Infrastructure') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    dir('terraform') {
                        sh """
                            terraform init
                            terraform apply -auto-approve
                        """
                        script {
                            // Get EC2 instance IP from Terraform output
                            EC2_INSTANCE_IP = sh(
                                script: 'terraform output -raw instance_public_ip',
                                returnStdout: true
                            ).trim()
                        }
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ec2-user@${EC2_INSTANCE_IP} '
                            docker pull ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker stop weather-app || true
                            docker rm weather-app || true
                            docker run -d --name weather-app -p 80:5000 ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful! Application is running at http://${EC2_INSTANCE_IP}"
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
        always {
            sh 'docker logout'
        }
    }
}