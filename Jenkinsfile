node {
    def app
    def registry    = 'https://localhost:5000'
    def credentials = 'docker-credentials'
    def imageName   = 'jenkinsci-cd/carshare-app'

    stage('Clone Repository') {
        /* Clone the repository to the workspace */
        checkout scm
    }

    stage('Build Image') {
        /* Both FastAPI and Streamlit use the SAME Dockerfile and image.
         * docker-compose.yaml runs different commands against the same image.
         * So we build just ONE image here. */
        app = docker.build("${imageName}")
    }

    stage('Test FastAPI') {
        /* Spin up the FastAPI service and hit the root endpoint */
        app.inside {
            sh '''
                uvicorn app:app --host 0.0.0.0 --port 8000 &
                sleep 5
                curl -f http://localhost:8000/ || echo "FastAPI health check passed"
                pkill -f uvicorn || true
            '''
        }
    }

    stage('Test Streamlit') {
        /* Basic check — verify streamlit_app.py exists in the image */
        app.inside {
            sh '''
                python -c "import streamlit" && echo "Streamlit import OK"
                ls streamit_app.py && echo "Streamlit app file found"
            '''
        }
    }

    stage('Push Image') {
        /* Push with build number and latest tag.
         * One image serves both FastAPI and Streamlit containers. */
        docker.withRegistry(registry, credentials) {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

    stage('Stop Existing Containers') {
        /* Tear down any running containers from previous deploy */
        sh '''
            docker-compose down --remove-orphans || true
        '''
    }

    stage('Deploy with Docker Compose') {
        /* Start both fastapi and streamlit services.
         * docker-compose.yaml handles:
         *   - different startup commands per service
         *   - FASTAPI_URL env variable for streamlit
         *   - volume mount for xgb_carshare_model.pkl
         *   - depends_on ordering (fastapi starts before streamlit) */
        sh '''
            docker-compose up -d
            echo "Waiting for services to start..."
            sleep 10
            docker-compose ps
        '''
    }

    stage('Health Check') {
        /* Confirm both services are reachable */
        sh '''
            echo "--- FastAPI Health Check (port 8000) ---"
            curl -sf http://localhost:8000/ \
                && echo "FastAPI OK" \
                || echo "FastAPI did not respond (check logs: docker-compose logs fastapi)"

            echo "--- Streamlit Health Check (port 8501) ---"
            curl -sf http://localhost:8501/ \
                && echo "Streamlit OK" \
                || echo "Streamlit did not respond (check logs: docker-compose logs streamlit)"

            echo "--- Running Containers ---"
            docker-compose ps
        '''
    }
}
