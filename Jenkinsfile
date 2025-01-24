pipeline {
    agent {
        label 'builder'
    }

    options {
        timestamps()
    }

    environment {
        BRANCH_NAME = 'system-manager'
        IMAGE_NAME = "etherfurnace/${BRANCH_NAME}"
        IMAGE_TAG='latest'
    }

    stages {
        stage('构建前通知'){
           steps {
                sh """
                    curl '${env.NOTIFICATION_URL}' \
                    -H 'Content-Type: application/json' \
                    -d '{
                        "msgtype": "text",
                        "text": {
                            "content": "[${BRANCH_NAME}]: 🚀 开始构建"
                        }
                    }'
                """
           }
        }

        stage('克隆代码仓库') {
            steps {
                git url: 'https://github.com/WeOps-Lab/rewind', branch: BRANCH_NAME
            }
       }

       stage('构建镜像') {
            steps {
                script {
                    sh "sudo docker build -f ./support-files/docker/Dockerfile -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
       }

       stage('推送镜像'){
            steps {
                script {
                    sh "sudo docker push  ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
       }

       stage('更新云环境'){
            steps {
                script {
                    sh """
                        cd ${env.KUBE_DIR}/system-manager/overlays/cwoa/ && \
                            sudo kubectl delete -k . || true &&\
                            sudo kubectl apply -k .
                    """
                }
            }
       }

       stage('更新环境'){
            agent { 
                label 'docker' 
            }
            options {
                skipDefaultCheckout true
            }
            steps {
                script {
                    sh """
                    docker pull ${IMAGE_NAME}:${IMAGE_TAG}
                    docker stop system-manager || true
                    docker rm system-manager || true
                    docker run -itd --name system-manager --restart always \
                        -v /root/codes/conf/system-manager/.env:/apps/.env \
                        --network lite \
                        etherfurnace/system-manager
                    """
                }
            }
       }
    }

    post {
        success {
            sh """
                curl '${env.NOTIFICATION_URL}' \
                -H 'Content-Type: application/json' \
                -d '{
                    "msgtype": "text",
                    "text": {
                        "content": "[${BRANCH_NAME}]: 🎉 构建成功"
                    }
                }'
            """
        }
        failure {
            sh """
                curl '${env.NOTIFICATION_URL}' \
                -H 'Content-Type: application/json' \
                -d '{
                    "msgtype": "text",
                    "text": {
                        "content": "[${BRANCH_NAME}]: ❌ 构建失败"
                    }
                }'
            """
        }
    }
}