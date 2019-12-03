pipeline {
    agent any
    stages {
    stage('Pull code'){
        git 'https://github.com/hansholz/game-bot.git'
    }
    stage('Build Image'){
        app = docker.build("hansholz/game-bot:"+currentBuild.number)
    }
    /*stage('Test image'){
        
        #TEST
        ${env.BUILD_NUMBER}
        app.inside{
            sh 'echo "Test passed"'
        }
        
    }*/
    stage('Push Image'){
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub'){
            app.push()
        }
    }
    stage('Deploy'){
        
        sshPublisher(publishers: [sshPublisherDesc(configName: 'amoremiosa13@server1', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'sudo apt-get update && sudo apt-get install -y docker.io && sudo docker pull hansholz/game-bot:'+currentBuild.number+' && sudo docker run -d hansholz/game-bot:'+currentBuild.number, execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)]) 
        
        }
    }
    post {
        always {
            slackNotifier(currentBuild.currentResult)
            cleanWs()
        }
    }
}