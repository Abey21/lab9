pipeline {
    agent any

    environment {
        PYTHON_HOME = '/usr/bin/python3'  // Adjust this if needed
    }

    triggers {
        // Trigger the job on each code push to GitHub
        githubPush()
    }

    stages {
        stage('Stage 1: Setup Virtual Environment and Install Packages') {
            steps {
                echo 'Setting up virtual environment and installing required packages...'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install ncclient pandas netaddr prettytable pylint napalm'
            }
        }

        stage('Stage 2: Checking and Fixing Violations') {
            steps {
                echo 'Running pylint to check for PEP8 violations...'
                script {
                    def pylint = sh(script: '. venv/bin/activate && pylint --fail-under=5 /var/lib/jenkins/workspace/Lab9/netman_netconf_obj2.py', returnStatus: true)
                    if (pylint != 0) {
                        error 'Pylint score <5. Please fix the code style issues before proceeding.'
                    }
                }
            }
        }

        stage('Stage 3: Running the Application') {
            steps {
                echo 'Running the application...'
                sh '. venv/bin/activate && python3 /var/lib/jenkins/workspace/Lab9/netman_netconf_obj2.py'
            }
        }

        stage('Stage 4: Unit Test') {
            steps {
                echo 'Running unit tests...'
                sh '. venv/bin/activate && python3 /var/lib/jenkins/workspace/Lab9/unitTest.py'
            }
        }
    }

    post {
	always {
		emailext body: '$DEFAULT_CONTENT', 
		recipientProviders: [
		    [$class: 'CulpritsRecipientProvider'],
		    [$class: 'DevelopersRecipientProvider'],
		    [$class: 'RequesterRecipientProvider']
		], 
		replyTo: '$DEFAULT_REPLYTO', 
		subject: '$DEFAULT_SUBJECT',
		to: '$DEFAULT_RECIPIENTS'
	}
    }
}
