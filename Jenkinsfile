pipeline {
    agent any

    environment {
        PATH = "$PATH:/usr/local/bin"
    }

    stages {
        stage("Deploy Prod") {
            when {
                branch "master"
            }
            steps {
                echo "Stopping previous container..."
                sh "docker-compose down"
                echo "Deploying and Building..."
                sh "docker-compose build"
                sh "docker-compose up -d"
                echo "Deployed!"
            }
        }
    }
//     post {
//         always {
//             echo "Tests"
// //             step([$class: 'JUnitResultArchiver', testResults: 'test_results/*.xml'])
//         }
//     }
}
