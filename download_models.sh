#!/bin/sh
set -e

mkdir -p ./models

echo "Installing curl and wget if not present..."
apk add --no-cache wget curl 2>/dev/null || true

echo "Checking and downloading Llama-3-Taiwan-8B-Instruct..."
if [ ! -f ./models/llama-3-taiwan-8b-instruct-q4_k_m.gguf ]; then
  wget -O ./models/llama-3-taiwan-8b-instruct-q4_k_m.gguf \
    https://huggingface.co/phate334/Llama-3-Taiwan-8B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3-taiwan-8b-instruct-q4_k_m.gguf
else
  echo "Llama-3-Taiwan already exists."
fi

echo "Checking and downloading Foundation-Sec-8B..."
if [ -f ./models/foundation-sec-8b-q4_k_m.gguf ]; then
  FILESIZE=$(stat -c%s "/models/foundation-sec-8b-q4_k_m.gguf" 2>/dev/null || stat -f%z "/models/foundation-sec-8b-q4_k_m.gguf" 2>/dev/null || echo 0)
  if [ "$FILESIZE" -lt 1000000000 ]; then
    echo "Existing file is too small (likely a failed download or error page). Redownloading..."
    rm -f /models/foundation-sec-8b-q4_k_m.gguf
  fi
fi

if [ ! -f ./models/foundation-sec-8b-q4_k_m.gguf ]; then
  # Fetching from an ungated HuggingFace repository containing the GGUF model
  wget -O ./models/foundation-sec-8b-q4_k_m.gguf \
    https://huggingface.co/DevQuasar/fdtn-ai.Foundation-Sec-8B-GGUF/resolve/main/fdtn-ai.Foundation-Sec-8B.Q4_K_M.gguf
else
  echo "Foundation-Sec-8B already exists and is valid."
fi

echo "All models downloaded successfully."
