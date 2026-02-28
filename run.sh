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
    MAX_RETRIES=15
    COUNT=0
    while ! curl -s "$INFLUXDB_URL/ping" > /dev/null; do
        sleep 1
        COUNT=$((COUNT+1))
        if [ $COUNT -ge $MAX_RETRIES ]; then
            echo "⚠️  InfluxDB taking longer than expected, continuing anyway..."
            break
        fi
    done
    echo "✅ InfluxDB check complete."
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
        # Check if database exists first or suppress error noise
        docker exec cisco-foundation-sec-8b-macos-influxdb \
            influxdb3 create database metrics \
            --host http://localhost:8181 \
            --token "$INFLUXDB_TOKEN" 2>/dev/null || true

        source ai_env/bin/activate
        
        # Optimization: Only install if requirements changed or marker missing
        if [ ! -f .deps_installed ] || [ requirements.txt -nt .deps_installed ]; then
            echo "Checking dependencies..."
            pip install -q -r requirements.txt
            # Auto-install watchdog for performance if missing
            pip install -q watchdog || true
            touch .deps_installed
            echo "✅ Dependencies verified."
        fi

        echo "================================================="
        echo "🧪 Running Unit Tests..."
        echo "================================================="
        python -m unittest discover tests/
        echo "✅ Unit Tests Passed!"

        echo "Starting ASITOP HUD (Streamlit) in background..."
        streamlit run streamlit_app.py --server.headless=true > streamlit_hud.log 2>&1 &
        
        echo "Launching Chainlit Interface..."
        chainlit run main.py -w
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