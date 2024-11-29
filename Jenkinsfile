pipeline {
    agent {
        label 'builder'
    }

    options {
        timestamps()
    }

    environment {
        BRANCH_NAME = 'user-manager'
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
                    sh """
                    go mod tidy && \
                    go mod vendor &&\
                    cd incubation/user-manager && \
                    go mod tidy && \
                    go mod vendor &&\
                    /home/umaru/go/bin/swag init --parseDependency && \
                    go build && \
                    sudo docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    """
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

       stage('更新环境'){
            steps {
                script {
                    sh """
                    echo 'upgrade'
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