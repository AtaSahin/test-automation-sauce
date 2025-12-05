pipeline {
    agent any
    
    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Select browser for test execution'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression', 'login', 'cart', 'checkout'],
            description: 'Select test suite to run'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run tests in headless mode'
        )
    }
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV_DIR = 'venv'
        ALLURE_RESULTS = 'allure-results'
        ALLURE_REPORT = 'allure-report'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code from repository..."
                }
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    echo "Setting up Python virtual environment..."
                }
                bat '''
                    python --version
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Setup Test Configuration') {
            steps {
                script {
                    echo "Configuring test environment..."
                    bat """
                        echo BASE_URL=https://www.saucedemo.com > .env
                        echo BROWSER=${params.BROWSER} >> .env
                        echo HEADLESS=${params.HEADLESS} >> .env
                        echo TIMEOUT=10 >> .env
                        echo SCREENSHOT_ON_FAILURE=true >> .env
                        echo STANDARD_USER=standard_user >> .env
                        echo LOCKED_OUT_USER=locked_out_user >> .env
                        echo PROBLEM_USER=problem_user >> .env
                        echo PERFORMANCE_GLITCH_USER=performance_glitch_user >> .env
                        echo PASSWORD=secret_sauce >> .env
                    """
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo "Running ${params.TEST_SUITE} tests on ${params.BROWSER}..."
                    
                    def testCommand = ''
                    switch(params.TEST_SUITE) {
                        case 'smoke':
                            testCommand = 'pytest -m smoke -v'
                            break
                        case 'regression':
                            testCommand = 'pytest -m regression -v'
                            break
                        case 'login':
                            testCommand = 'pytest tests/test_login.py -v'
                            break
                        case 'cart':
                            testCommand = 'pytest tests/test_cart.py -v'
                            break
                        case 'checkout':
                            testCommand = 'pytest tests/test_checkout.py -v'
                            break
                        default:
                            testCommand = 'pytest -v'
                    }
                    
                    bat """
                        call %VENV_DIR%\\Scripts\\activate.bat
                        ${testCommand}
                    """
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                script {
                    echo "Generating Allure report..."
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: "${ALLURE_RESULTS}"]]
                    ])
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Archiving test results..."
            }
            
            junit allowEmptyResults: true, testResults: 'test-results/*.xml'
            
            archiveArtifacts artifacts: 'test-results/report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
            
            cleanWs(
                deleteDirs: true,
                patterns: [
                    [pattern: "${VENV_DIR}", type: 'INCLUDE'],
                    [pattern: '__pycache__', type: 'INCLUDE'],
                    [pattern: '.pytest_cache', type: 'INCLUDE']
                ]
            )
        }
        
        success {
            script {
                echo "Test execution completed successfully!"
            }
            
            emailext(
                subject: "Jenkins Build #${BUILD_NUMBER} - SUCCESS",
                body: """
                    Test Suite: ${params.TEST_SUITE}
                    Browser: ${params.BROWSER}
                    Status: SUCCESS
                    
                    View results: ${BUILD_URL}
                    View Allure Report: ${BUILD_URL}allure
                """,
                to: 'team@example.com',
                attachLog: true
            )
        }
        
        failure {
            script {
                echo "Test execution failed!"
            }
            
            emailext(
                subject: "Jenkins Build #${BUILD_NUMBER} - FAILED",
                body: """
                    Test Suite: ${params.TEST_SUITE}
                    Browser: ${params.BROWSER}
                    Status: FAILED
                    
                    View results: ${BUILD_URL}
                    View Allure Report: ${BUILD_URL}allure
                """,
                to: 'team@example.com',
                attachLog: true
            )
        }
    }
}

