pipeline {
    agent {
        label 'builder'
    }

    options {
        timestamps()
    }

    environment {
        BRANCH_NAME = 'main'
    }

    stages {
        stage('克隆代码仓库') {
            steps {
                git url: 'https://github.com/WeOps-Lab/rewind', branch: BRANCH_NAME
            }
       }

       stage('代码扫描') {
            steps {
                script {
                    sh """
                    sudo docker run \
                        --rm \
                        -e SONAR_HOST_URL="${env.SONARQUBE_URL}"  \
                        -e SONAR_TOKEN="${env.SONARQUBE_TOKEN}" \
                        -v "${WORKSPACE}:/usr/src" \
                        sonarsource/sonar-scanner-cli
                    """
                }
            }
       }
    }
}