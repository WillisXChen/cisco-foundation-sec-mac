#!/bin/bash
set -e

# Ensure models are downloaded
./download_models.sh

# Only run installation if virtual environment is missing
if [ ! -d "ai_env" ]; then
    echo "Environment not found. Starting first-time setup..."
    ./install_metal.sh
else
    echo "Virtual environment detected. Skipping setup."
fi

# Ensure Qdrant service is running
if ! docker ps --format '{{.Names}}' | grep -q "^cisco-foundation-sec-8b-macos-qdrant$"; then
    echo "Qdrant service is not running. Starting via Docker Compose..."
    docker compose up -d cisco-foundation-sec-8b-macos-qdrant
else
    echo "Qdrant service is already active."
fi

# Activating environment and running application
echo "Starting Chainlit application..."
source ai_env/bin/activate
pip install -r requirements.txt
chainlit run ./cisco_security_chainlit.py