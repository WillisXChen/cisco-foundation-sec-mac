#!/bin/bash
set -e

COMMAND=$1

case "$COMMAND" in
    start)
        echo "================================================="
        echo "🚀 Starting Cisco Security Assistant Ecosystem..."
        echo "================================================="

        # Ensure models are downloaded
        ./download_models.sh

        # Only run installation if virtual environment is missing
        if [ ! -d "ai_env" ]; then
            echo "Environment not found. Starting first-time setup..."
            ./install_metal.sh
        else
            echo "Virtual environment detected. Skipping setup."
        fi

        # Ensure all Docker services (Qdrant, InfluxDB, Grafana) are running
        echo "Starting backing services (Qdrant, InfluxDB v3, Grafana) via Docker Compose..."
        docker compose up -d

        echo "Initializing InfluxDB v3 Core Database..."
        # Wait a few seconds for InfluxDB v3 API to be ready
        sleep 5
        docker exec cisco-foundation-sec-8b-macos-influxdb influxdb3 create database metrics --host http://localhost:8181 --token apiv3_cisco-super-secret-auth-token || true

        echo "Activating environment..."
        source ai_env/bin/activate
        
        # Ensure latest requirements are installed (like influxdb-client)
        pip install -r requirements.txt

        echo "Starting ASITOP HUD (Streamlit)..."
        # Start Streamlit in the background, suppressing its output and detaching it
        streamlit run streamlit_app.py --server.headless=true > streamlit_hud.log 2>&1 &
        STREAMLIT_PID=$!
        echo "ASITOP HUD Started in background (PID: $STREAMLIT_PID)"

        echo "Starting Chainlit application (Main Interface & Background Worker)..."
        # Run chainlit in the foreground so the user can interact and see logs
        chainlit run ./cisco_security_chainlit.py -w
        ;;

    stop)
        echo "================================================="
        echo "🛑 Stopping Cisco Security Assistant Ecosystem..."
        echo "================================================="
        
        # Stop background Streamlit HUDs
        echo "Stopping Streamlit instances..."
        pkill -f "streamlit run streamlit_app.py" || echo "No Streamlit process found."
        
        # Stop Chainlit instances (in case they were running in bg)
        echo "Stopping Chainlit instances..."
        pkill -f "chainlit run" || echo "No Chainlit process found."

        # Stop Docker composition
        echo "Stopping backing services (Qdrant, InfluxDB v3, Grafana)..."
        docker compose down
        
        echo "✅ All services successfully shut down."
        ;;

    *)
        echo "Usage: ./run.sh [start | stop]"
        echo "  start : Download models, start Docker backing services (Qdrant/InfluxDB),"
        echo "          start Streamlit HUD in the background, and launch Chainlit App/Worker."
        echo "  stop  : Shut down all background Python processes and stop Docker containers."
        exit 1
        ;;
esac