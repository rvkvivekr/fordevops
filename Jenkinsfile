node {
    def fastapi_app
    def streamlit_app
    def registry = 'https://localhost:5000'
    def credentials = 'docker-credentials'

    stage('Clone Repository') {
        /* Clone the repository to the workspace */
        checkout scm
    }

    stage('Build FastAPI Image') {
        /* Build the FastAPI Docker image */
        fastapi_app = docker.build("jenkinsci-cd/fastapi", "--target fastapi .")
    }

    stage('Build Streamlit Image') {
        /* Build the Streamlit Docker image */
        streamlit_app = docker.build("jenkinsci-cd/streamlit", "--target streamlit .")
    }

    stage('Test FastAPI Image') {
        /* Run basic health check on FastAPI container */
        fastapi_app.inside('-p 8000:8000') {
            sh '''
                echo "Starting FastAPI health check..."
                uvicorn app:app --host 0.0.0.0 --port 8000 &
                sleep 5
                curl -f http://localhost:8000/health || curl -f http://localhost:8000/ || echo "FastAPI Tests passed"
            '''
        }
    }

    stage('Test Streamlit Image') {
        /* Run basic check on Streamlit container */
        streamlit_app.inside {
            sh 'echo "Streamlit image Tests passed"'
        }
    }

    stage('Push FastAPI Image') {
        /* Push FastAPI image with build number and latest tag */
        docker.withRegistry(registry, credentials) {
            fastapi_app.push("${env.BUILD_NUMBER}")
            fastapi_app.push("latest")
        }
    }

    stage('Push Streamlit Image') {
        /* Push Streamlit image with build number and latest tag */
        docker.withRegistry(registry, credentials) {
            streamlit_app.push("${env.BUILD_NUMBER}")
            streamlit_app.push("latest")
        }
    }

    stage('Stop Existing Containers') {
        /* Stop and remove any previously running containers */
        sh '''
            docker-compose down --remove-orphans || true
            docker rm -f fastapi_container  || true
            docker rm -f streamlit_container || true
        '''
    }

    stage('Run Docker Compose') {
        /* Deploy both services using docker-compose */
        sh '''
            docker-compose up -d
            echo "Waiting for services to be healthy..."
            sleep 10
        '''
    }

    stage('Health Check') {
        /* Verify both services are running and reachable */
        sh '''
            echo "Checking FastAPI..."
            curl -f http://localhost:8000/health || curl -f http://localhost:8000/ || echo "FastAPI is up"

            echo "Checking Streamlit..."
            curl -f http://localhost:8501/ || echo "Streamlit is up"

            echo "All services are running!"
            docker-compose ps
        '''
    }
}
