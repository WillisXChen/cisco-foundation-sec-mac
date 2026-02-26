#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 開始設定 macOS (Apple Silicon / Metal for AI) 環境..."

# 1. 檢查並安裝 Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 正在安裝 Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew 已經安裝。"
fi

# 2. 檢查 Xcode Command Line Tools (編譯 Metal 程式碼所需)
if ! xcode-select -p &> /dev/null; then
    echo "🛠️ 正在安裝 Xcode Command Line Tools..."
    xcode-select --install
    echo "⚠️ 請在安裝完成後，再次執行此腳本！"
    exit 1
else
    echo "✅ Xcode Command Line Tools 已經安裝。"
fi

# 3. 建立並啟用 Python 虛擬環境
echo "🐍 正在建立 Python 虛擬環境 (venv)..."
python3 -m venv ai_env
source ai_env/bin/activate

# 升級 pip
pip install --upgrade pip

# 4. 安裝支援 MPS (Metal Performance Shaders) 的 PyTorch
echo "🔥 正在安裝支援 MPS (Metal) 的 PyTorch..."
pip install torch torchvision torchaudio

# 5. 安裝 Apple 官方的 MLX 框架 (專為 Apple Silicon 最佳化)
echo "🍎 正在安裝 Apple MLX 框架..."
pip install mlx

# 6. 安裝 llama-cpp-python 並啟用 Metal 加速 (GPU)
echo "🦙 正在編譯與安裝具有 Metal 支援的 llama-cpp-python..."
CMAKE_ARGS="-DGGML_METAL=on" pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir

echo "========================================================"
echo "🎉 安裝完成！"
echo "👉 若要開始使用此環境，請執行："
echo "   source ai_env/bin/activate"
echo "========================================================"
