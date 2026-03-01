<div align="center">
  <img src="public/logo_dark.png" width="100" alt="Native AI Security Assistant Logo">

  # 🛡️ Native AI Security Assistant for Apple Silicon
  
  *Cisco Foundation-Sec 8B • Bilingual Log Analysis • RAG-Enabled Playbooks • Metal-Accelerated*

  [![English](https://img.shields.io/badge/English-blue?style=for-the-badge)](README.md) [![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md)

  **Maintainer:** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

This project is a multilingual (English/Chinese/Japanese) security analysis smart assistant running on macOS (Apple Silicon M-series chips). By integrating [Chainlit](https://docs.chainlit.io/) to provide a modern interactive interface, and combining multiple Large Language Models (LLMs) with the Qdrant vector database, it achieves professional security log analysis and RAG (Retrieval-Augmented Generation) applications.

## Built With

<div align="center">
  <h3>
    <img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=macos&logoColor=white" height="28" alt="macOS">
    <img src="https://img.shields.io/badge/Apple_Silicon-999999?style=for-the-badge&logo=apple&logoColor=white" height="28" alt="Apple Silicon">
    <img src="https://img.shields.io/badge/Homebrew-F2A900?style=for-the-badge&logo=homebrew&logoColor=white" height="28" alt="Homebrew">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="28" alt="Python">
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" height="28" alt="PyTorch (MPS)">
    <img src="https://img.shields.io/badge/LLaMA_C++-FF7F50?style=for-the-badge&logo=meta&logoColor=white" height="28" alt="LLaMA C++">
    <img src="https://img.shields.io/badge/Chainlit-4A25E1?style=for-the-badge&logo=chainlit&logoColor=white" height="28" alt="Chainlit">
    <img src="https://img.shields.io/badge/Qdrant-1B053A?style=for-the-badge&logo=qdrant&logoColor=white" height="28" alt="Qdrant">
    <img src="https://img.shields.io/badge/FastEmbed-FF4B4B?style=for-the-badge&logo=python&logoColor=white" height="28" alt="FastEmbed">
    <br><br>
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" height="28" alt="Docker">
    <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" height="28" alt="Docker Compose">
    <img src="https://img.shields.io/badge/OrbStack-5645B6?style=for-the-badge&logo=orbstack&logoColor=white" height="28" alt="OrbStack">
    <img src="https://img.shields.io/badge/Podman-892CA0?style=for-the-badge&logo=podman&logoColor=white" height="28" alt="Podman">
    <img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" height="28" alt="Hugging Face">
  </h3>
</div>

## Core Project Components

1. **Frontend Interface**: Uses Chainlit (`main.py`) to build a conversational AI interface, supporting real-time text streaming and chat history.
2. **Multilingual Support**: Handles intent classification, multilingual understanding, and translation through **Llama-3-Taiwan-8B-Instruct**. Optimized for **English**, **Traditional Chinese**, and **Japanese**.
3. **Security Expert**: Performs in-depth system and security log analysis through **Foundation-Sec-8B**, fine-tuned specifically for the cybersecurity domain.
4. **Hardware Acceleration & Fine-tuning**: Integrates macOS Metal (MPS) with `llama-cpp-python`. Supports manual **GPU layer offloading** and **Context Window (KV Cache) adjustment** via `.env` to balance VRAM usage on Mac Pro/Studio (M2/M3).
5. **Vector Retrieval (RAG)**: Uses **Qdrant** (deployed via Docker) to store and retrieve security playbooks. The system features **automatic RAG synchronization** on startup.
6. **Observability & Tracing**: Integrated with **Langfuse** and **Arize Phoenix** for deep trace auditing, AI response quality monitoring, and system-wide **Structlog** logging.
7. **Performance Dashboard & Floating HUD**: Real-time hardware monitoring via ASITOP style HUD (Streamlit) utilizing **GraphQL subscriptions**. Includes floating "PerfMon" and "History" panels.
8. **Refined UI/UX**: Persistent top-center language selector with flag icons for quick switching between EN, ZH, and JA.

## System Requirements

- **Operating System**: macOS (Apple Silicon M1/M2/M3 recommended)
- **Hardware Performance**: At least 16GB of unified memory is recommended (depending on the model size)
- **Prerequisites**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman.io/) (for deploying Qdrant)
  - Internet connection (required for downloading models and dependencies on first launch)

## Project Architecture

```text
.
├── core/                       # Core system logic (LLM, Database, Hardware, Config)
├── models/                     # GGUF model storage (Llama-3 and Foundation-Sec)
├── qdrant_storage/             # Persistent storage directory for Qdrant vector database
├── influxdb3_storage/          # Persistent storage for metrics
├── grafana_storage/            # Grafana dashboard storage
├── public/                     # Custom branding assets (logos, CSS, themes)
├── main.py                     # Main Chainlit application entry point
├── streamlit_app.py            # ASITOP HUD Monitoring interface
├── playbooks.json              # Centralized security SOPs/Playbooks for RAG ingestion
├── .env                        # Environment variables and secrets
├── run.sh                      # Smart execution script (automates setup, skips re-compilation if ready)
└── (Other config files and scripts)
```

## How to Run

Depending on your environment setup, the project provides two ways to run.

### Method 1: One-Click Startup Script (Recommended for First Time)

The project provides a one-click startup script that will automatically install necessary packages, download models, start the Qdrant container, and run the Chainlit service.

1. **Open Terminal**, and navigate to this project directory:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **Grant execution permissions and run the startup script**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **The initial startup process includes**:
   - `./download_models.sh`: Checks for and downloads any missing GGUF language models.
   - `./install_metal.sh`: Automatically installs Homebrew, checks Xcode CLTs, and sets up the Python virtual environment (`ai_env`) with Metal-supported `llama-cpp-python`.
   - **Docker Compose**: Checks for and starts the service named `cisco-foundation-sec-8b-macos-qdrant`.
   - **Automatic RAG Sync**: The application automatically reads `playbooks.json` and updates the Qdrant knowledge base on startup.
   - Starts the `main.py` web service after updating package dependencies.

### Method 2: Manual Startup (Recommended after Initial Setup)

If you have already successfully executed `run.sh` and downloaded all environments and models, you only need to manually start the services going forward:

1. **Ensure Qdrant service is running**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **Activate the virtual environment and start Chainlit**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### Start Chatting

Once the services are up, the terminal will display the local execution info for Chainlit. Typically, you can access the security assistant interface by opening your browser and navigating to `http://localhost:8000`.

## ⚙️ Performance Optimization (Advanced)

To ensure the system stays within resource limits (e.g., < 50% RAM on a 24GB Mac), you can fine-tune the following in your `.env`:

*   `N_GPU_LAYERS_LLAMA3`: GPU layers for the general model (-1 for all, 0 for CPU).
*   `N_GPU_LAYERS_SEC`: GPU layers for the security model.
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: Context size (default 2048). Reducing this saves significant RAM.

## 📊 Observability & Monitoring

The system is equipped with enterprise-grade observability tools:

- **Langfuse**: Trace your LLM calls, costs, and token usage.
- **Arize Phoenix**: Automatic evaluation of RAG responses and tracing.
- **ASITOP HUD**: Floating real-time HUD for GPU/CPU/RAM monitoring.
- **Grafana**: Historical performance dashboards.
## Troubleshooting

- **Qdrant fails to start**: Ensure Docker Desktop or Podman is currently running.
- **`llama-cpp-python` compilation errors**: Usually caused by incomplete installation of Xcode Command Line Tools. Try running `xcode-select --install` manually.
- **Out of memory / Frequent crashes**: Large language models consume significant system resources. Please close unnecessary background applications to reserve enough unified memory for MLX or MPS usage.

## Development and Advanced Features

- **RAG Text Ingestion**: To import new base security documents into the Qdrant knowledge base, execute the document processing script via `ingest_security_docs.py`.
- **Automated Log Translation/Processing**: `translate_logs.py` provides a template for batch processing logs or performing cross-language conversion tests.


## 📄 License

This project is licensed under the **MIT License**. 
See the [LICENSE.md](LICENSE.md) and [LICENSE_ZH.md](LICENSE_ZH.md) files for details. 
