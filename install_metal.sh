#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting macOS (Apple Silicon / Metal for AI) environment setup..."

# 1. Check and install Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew is already installed."
fi

# 2. Check Xcode Command Line Tools (required to compile Metal code)
if ! xcode-select -p &> /dev/null; then
    echo "🛠️ Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "⚠️ Please re-run this script once the installation is complete!"
    exit 1
else
    echo "✅ Xcode Command Line Tools is already installed."
fi

# 3. Create and activate Python virtual environment
echo "🐍 Creating Python virtual environment (venv)..."
python3 -m venv ai_env
source ai_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# 4. Install PyTorch with MPS (Metal Performance Shaders) support
echo "🔥 Installing PyTorch with MPS (Metal) support..."
pip install torch torchvision torchaudio

# 5. Install Apple's official MLX framework (Optimized for Apple Silicon)
echo "🍎 Installing Apple MLX framework..."
pip install mlx

# 6. Install llama-cpp-python and enable Metal Acceleration (GPU)
echo "🦙 Compiling and installing llama-cpp-python with Metal support..."
CMAKE_ARGS="-DGGML_METAL=on" pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir

echo "========================================================"
echo "🎉 Installation complete!"
echo "👉 To start using this environment, run:"
echo "   source ai_env/bin/activate"
echo "========================================================"
