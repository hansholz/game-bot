node{
    def app

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
            sshPublisher(
                publishers: [sshPublisherDesc(configName: 'amoremiosa13@server1', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'bash deploy.sh '+currentBuild.number, execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
        }

        stage('Post-Build actions'){
            /*Send notifications to Slack*/
            slackSend channel: 'humeniuk-ci-cd-notification', message: 'Hi! Build number: '+currentBuild.number+' is '+currentBuild.currentResult

            /*Clean Workspace*/
            cleanWs()
        }
    }
