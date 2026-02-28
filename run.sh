#!/bin/bash
set -e

# Load environment variables from .env if present
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

COMMAND=$1

# Default values if not set in .env
INFLUXDB_URL=${INFLUXDB_URL:-"http://localhost:8181"}
INFLUXDB_TOKEN=${INFLUXDB_TOKEN:-"apiv3_cisco-super-secret-auth-token"}

function wait_for_influx() {
    echo "Waiting for InfluxDB v3 to be ready..."
    MAX_RETRIES=30
    COUNT=0
    while ! curl -s "$INFLUXDB_URL/ping" > /dev/null; do
        sleep 1
        COUNT=$((COUNT+1))
        if [ $COUNT -ge $MAX_RETRIES ]; then
            echo "❌ InfluxDB failed to start in time."
            exit 1
        fi
    done
    echo "✅ InfluxDB is up!"
}

case "$COMMAND" in
    start)
        echo "================================================="
        echo "🚀 Starting Cisco Foundation Sec 8B Ecosystem..."
        echo "================================================="

        ./download_models.sh

        if [ ! -d "ai_env" ]; then
            echo "First-time setup: Creating environment..."
            ./install_metal.sh
        fi

        echo "Starting backing services via Docker Compose..."
        docker compose up -d

        wait_for_influx

        echo "Initializing InfluxDB Database..."
        # Note: Using localhost:8181 here because we are running this on the host
        docker exec cisco-foundation-sec-8b-macos-influxdb \
            influxdb3 create database metrics \
            --host http://localhost:8181 \
            --token "$INFLUXDB_TOKEN" || true

        source ai_env/bin/activate
        
        echo "Verifying dependencies..."
        pip install -q -r requirements.txt

        echo "================================================="
        echo "🧪 Running Unit Tests..."
        echo "================================================="
        python -m unittest discover tests/
        echo "✅ Unit Tests Passed!"

        echo "Starting ASITOP HUD (Streamlit) in background..."
        streamlit run streamlit_app.py --server.headless=true > streamlit_hud.log 2>&1 &
        
        echo "Launching Chainlit Interface..."
        chainlit run ./main.py -w
        ;;

    stop)
        echo "Stopping background processes..."
        pkill -f "streamlit run streamlit_app.py" || true
        pkill -f "chainlit run" || true
        
        echo "Stopping Docker containers..."
        docker compose down
        
        echo "✅ System shut down."
        ;;

    *)
        echo "Usage: ./run.sh [start | stop]"
        exit 1
        ;;
esac