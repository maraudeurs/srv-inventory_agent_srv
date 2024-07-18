pipeline {
    agent any

    description('build and push inventory_agent_srv docker image')

    environment {
        DOCKER_REGISTRY = "registry.hub.docker.com"
        DOCKER_IMAGE_NAME = "webdronesas/inventory_agent_srv"
        DOCKER_HUB_CREDENTIAL_ID = "webdrone_dockerhub_token"
        MICROSOFT_TEAMS_WEBHOOK_CREDENTIAL_ID = "infra_cicd_teams_webhook_url"
        GIT_REPO_URL = "https://github.com/maraudeurs/srv-inventory_agent_srv.git"
        GIT_CREDENTIAL_ID = "wddeploy_github_token"
        GIT_BRANCH = "*/main"
        TESTDIRECTORY = "tests"
    }

    options {
        ansiColor('css')
    }

    stages {

        stage('Tag purge') {
            steps {
                // clear local git tags (avoid conflicts when duplicates)
                sh('git tag | xargs git tag -d 2>&1 >/dev/null')
                script {
                    withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIAL_ID}", passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                            sh("git fetch https://${GIT_USERNAME}:${GIT_PASSWORD}@${env.GIT_REPO_URL} --tags 2>&1 >/dev/null")
                        }
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: 'main']],
                    extensions: [[ $class: 'CloneOption', noTags: false, shallow: false, depth: 0, reference: '' ]],
                    userRemoteConfigs: [[credentialsId: "${env.GIT_CREDENTIAL_ID}", url: "https://${env.GIT_REPO_URL}" ]]
                    )
            }
        }

        stage ("Hadolint") {
            agent {
                docker {
                    image('hadolint/hadolint:latest-debian')
                }
            }
            steps {
                sh('hadolint --config .hadolint.yaml Dockerfile')
            }
        }

        stage('Increment Tag') {
            steps {
                script {
                    // get existing tag (from previous commit)
                    def currentTag = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
                    println "Previous tag : ${currentTag}"
                    def version = getVersionFromTag(currentTag)
                    if (version) {
                        INCREMENTEDVERSION = incrementVersion(version)
                        println "New tag : ${INCREMENTEDVERSION}"
                        withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIAL_ID}", passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                            sh("git tag ${INCREMENTEDVERSION}")
                            sh("git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${env.GIT_REPO_URL} ${INCREMENTEDVERSION}")
                        }
                        env.DOCKER_IMAGE_TAG = "${INCREMENTEDVERSION}"
                    } else {
                        error "Invalid tag format: ${currentTag}"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            environment {
                DOCKER_BUILDKIT = 1
            }
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}")
                    sh("docker tag ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} ${env.DOCKER_IMAGE_NAME}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("https://${env.DOCKER_REGISTRY}", "${env.DOCKER_HUB_CREDENTIAL_ID}") {
                        docker.image("${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}").push()
                        docker.image("${env.DOCKER_IMAGE_NAME}:latest").push()
                    }
                }
            }
        }

        stage('Purge docker image') {
            steps{
                //  delete local tag docker image from jenkins
                // sh("docker rmi ${env.DOCKER_IMAGE_NAME}:latest")
                sh("docker rmi ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}")
                //  delete repository tag docker image from jenkins
                sh("docker rmi ${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE_NAME}:latest")
                sh("docker rmi ${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}")
            }
        }

    }
    post {
        success {
            withCredentials([string(credentialsId: "${MICROSOFT_TEAMS_WEBHOOK_CREDENTIAL_ID}", variable: "ms_teams_webhook_url")]) {
                office365ConnectorSend webhookUrl: "${ms_teams_webhook_url}",
                message: "Job : ${env.JOB_NAME}, build : ${BUILD_NUMBER}, result : image ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} successfully build and push",
                status: 'Success'
            }
        }
        failure {
            withCredentials([string(credentialsId: "${MICROSOFT_TEAMS_WEBHOOK_CREDENTIAL_ID}", variable: "ms_teams_webhook_url")]) {
                office365ConnectorSend webhookUrl: "${ms_teams_webhook_url}",
                message: "Job : ${env.JOB_NAME}, build : ${BUILD_NUMBER}, result : image ${env.DOCKER_IMAGE_NAME} failed to build and push",
                status: 'Failure'
            }
        }
    }
}

def getVersionFromTag(tag) {
    // Remove any leading 'v' from the tag
    tag = tag.startsWith('v') ? tag.substring(1) : tag
    // Split the tag by periods
    def parts = tag.split('\\.')
    // Check if the tag has three parts
    if (parts.size() == 3) {
        // Check if each part is a number
        if (parts.every { it.isInteger() }) {
            return tag
        }
    }
    return null
}

def incrementVersion(version) {
    // Split the version string into major, minor, and patch parts
    def parts = version.split('\\.')
    def major = parts[0] as int
    def minor = parts[1] as int
    def patch = parts[2] as int
    // Increment the patch version
    patch++
    // Return the incremented version
    return "${major}.${minor}.${patch}"
}