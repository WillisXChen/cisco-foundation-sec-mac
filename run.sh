#!/bin/bash
./download_models.sh
./install_metal.sh
# 檢查 qdrant-db 容器是否正在運行
if ! docker ps --format '{{.Names}}' | grep -q "^cisco-foundation-sec-8b-macos-qdrant$"; then
    echo "Qdrant 服務尚未執行，正在啟動 docker compose..."
    docker compose up -d cisco-foundation-sec-8b-macos-qdrant
else
    echo "Qdrant 服務已經在運行中。"
fi
./ai_env/bin/pip install -r requirements.txt
./ai_env/bin/chainlit run ./cisco_security_chainlit.py 