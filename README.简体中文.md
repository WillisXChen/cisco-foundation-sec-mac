<div align="center">
  <img src="public/logo_dark.png" width="100" alt="Native AI Security Assistant Logo">

  # 🛡️ Native AI Security Assistant for Apple Silicon
  
  *Cisco Foundation-Sec 8B • 多语系日志分析 • RAG 强化手册 • Metal 加速*

  [![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![繁體中文](https://img.shields.io/badge/%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![简体中文](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-blue?style=for-the-badge)](README.简体中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md) [![Español](https://img.shields.io/badge/Espa%C3%B1ol-gray?style=for-the-badge)](README.es.md) [![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-gray?style=for-the-badge)](README.ko.md) [![ไทย](https://img.shields.io/badge/%E0%B9%84%E0%B8%97%E0%B8%A2-gray?style=for-the-badge)](README.th.md) [![Tiếng Việt](https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-gray?style=for-the-badge)](README.vi.md) [![हिन्दी](https://img.shields.io/badge/%E0%A4%B9%E0%A4%BF%E0%A4%A3%E0%A5%8D%E0%A4%A6%E0%A5%80-gray?style=for-the-badge)](README.hi.md)

  **维护者 (Maintainer):** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

本项目是一个运行在 macOS (Apple Silicon M 系列芯片) 上的多语系资安分析智能助手，支持包括中文、英文、日文、西班牙文、韩文、泰文、越南文及印地文等。通过整合 [Chainlit](https://docs.chainlit.io/) 提供现代化的交互界面，并结合多个大型语言模型 (LLMs) 与 Qdrant 向量数据库，实现了专业的资安日志分析与 RAG (检索增强生成) 应用。

<div align="center">
  <img src="screenshots/dev-0.0.1/Apple%20Silicon-Prompt-Grasp-PerfPowMon.png" alt="性能监控" width="800" style="border-radius: 10px; border: 1.2px solid rgba(0, 212, 255, 0.3); box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);">
  <br><br>
  <img src="screenshots/dev-0.0.1/AI-Cisco-Sec-8B.webp" alt="AI-Cisco-Sec-8B" width="800" style="border-radius: 10px; border: 1.2px solid rgba(0, 212, 255, 0.3); box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);">
</div>

## 开发工具与技术堆栈

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

## 核心项目组件

1. **前端界面**: 使用 Chainlit (`main.py`) 构建对话式 AI 界面，支持实时文字流与历史对话。
2. **多语系支持**: 通过 **Llama-3-Taiwan-8B-Instruct** 处理意图分类、多语系理解与翻译，针对**中文、英文、日文、西班牙文、韩文、泰文、越南文与印度文**进行了特别优化。
3. **资安专家**: 通过专为网络安全领域微调的 **Foundation-Sec-8B**，进行深度的系统与资安日志分析。具备**企业级简洁化 (Conciseness)** 逻辑，能提供结构化、精炼且具备行动建议的技术分析。
4. **硬件加速与微调**: 整合 macOS Metal (MPS) 与 `llama-cpp-python`。支持通过 `.env` 手动调校 **GPU 层级卸载 (GPU Layers)** 与 **上下文窗口 (KV Cache)** 大小，以在大容量统一内存 (M2/M3) 上平衡性能与资源占用。
5. **向量检索 (RAG)**: 使用 **Qdrant** (通过 Docker 部署) 存储并检索资安 SOP 文件。系统现在支持启动时**自动 RAG 同步**。
6. **可观测性与追踪 (Observability)**: 整合 **Langfuse** 与 **Arize Phoenix**，提供深入的对话轨迹审计、AI 反应质量监控以及全系统的 **Structlog** 结构化日志。
7. **性能监控与悬浮控制**: 通过 ASITOP 风格的 HUD (Streamlit) 使用 **GraphQL 订阅** 进行硬件实时监控，并利用 InfluxDB v3 + Grafana 追踪历史趋势。整合“PerfMon”与“History”悬浮按钮。
8. **优化使用体验**: 位于画面中央上方的**语系切换器**，支持国旗图标，可快速切换多国语言。

## 系统需求

- **操作系统**: macOS (建议使用 Apple Silicon M1/M2/M3)
- **硬件性能**: 建议至少 16GB 的统一内存 (取决于模型大小)
- **前置条件**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) 或 [Podman](https://podman.io/) (用于部署 Qdrant)
  - 互联网连接 (初次启动时需要下载模型与依赖包)

## 项目架构

```text
.
├── core/                       # 系统核心逻辑 (LLM 管理、数据库连接、硬件监控、配置文件)
├── models/                     # GGUF 模型存储目录 (Llama-3 与 Foundation-Sec)
├── locales/                    # 多语系翻译文本 (.po/.mo)
├── qdrant_storage/             # Qdrant 向量数据库的持久化存储目录
├── influxdb3_storage/          # InfluxDB 指标存储目录
├── grafana_storage/            # Grafana 仪表板存储目录
├── langfuse_db_storage/        # Langfuse 追踪数据的本地存储
├── public/                     # 自定义品牌资源 (Logo、CSS、主题设置)
├── main.py                     # Chainlit 主程序入口点
├── api.py                      # GraphQL 与自定义 API 端点
├── streamlit_app.py            # ASITOP HUD 监控界面 (Streamlit)
├── health_check.py             # 全系统生态系健康检查工具
├── playbooks.json              # 集中化的资安 SOP/Playbooks，供 RAG 导入使用
├── .env                        # 环境变量与机敏信息设置
├── run.sh                      # 智能化执行脚本 (自动完成设置)
└── (其他配置文件与脚本)
```

## 如何执行

根据您的环境设置，本项目提供两种执行方式。

### 方式一：一键启动脚本 (建议初次使用)

本项目提供了一键启动脚本，会自动安装必要包、下载模型、启动 Qdrant 容器并运行 Chainlit 服务。

1. **打开终端 (Terminal)**，并切换至本项目目录:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **赋予执行权限并运行启动脚本**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **初始启动过程包含**:
   - `./download_models.sh`: 检查并下载缺失的 GGUF 语言模型。
   - `./install_metal.sh`: 自动安装 Homebrew，检查 Xcode CLTs，并设置支持 Metal 的 `llama-cpp-python` Python 虚拟环境 (`ai_env`)。
   - **Docker Compose**: 检查并启动名为 `cisco-foundation-sec-8b-macos-qdrant` 的服务。
   - **自动 RAG 同步**: 应用程序启动时会自动读取 `playbooks.json` 并更新 Qdrant 知识库。
   - 更新依赖包后，启动 `main.py` 网页服务。

### 方式二：手动启动 (建议完成初始设置后使用)

如果您已经成功执行过 `run.sh` 并下载了所有环境与模型，您后续只需手动启动服务即可:

1. **确保 Qdrant 服务正在运行**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **激活虚拟环境并启动 Chainlit**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### 开始对话

当服务都启动完毕后，终端将会显示 Chainlit 的本地执行信息。通常您可以打开浏览器并前往 `http://localhost:8000` 来访问资安助手界面。

## ⚙️ 性能优化 (进阶设置)

为了确保系统资源占用（例如在 24GB 的 Mac 上不超过 50% RAM），您可以在 `.env` 中调校以下参数：

*   `N_GPU_LAYERS_LLAMA3`: 通用模型的 GPU 卸载层数 (-1 为全卸载，0 为仅 CPU)。
*   `N_GPU_LAYERS_SEC`: 资安模型的 GPU 卸载层数。
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: 上下文窗口大小 (默认 2048)。缩小此值可显著节省内存。

## 📊 可观测性与监控 (Observability)

本系统配备了企业级的可观测性工具：

- **Langfuse**: 追踪您的 LLM 调用、成本与 Token 使用状况。
- **Arize Phoenix**: 自动评估 RAG 反应质量与追踪 (Evaluation)。
- **ASITOP HUD**: 悬浮实时显示硬件 (GPU/CPU/RAM) 使用状态。
- **Grafana**: 提供系统性能的历史趋势看板。
- **生态系健康检查**: 执行 `python health_check.py` 以验证整个 Docker/ML 生态系（Qdrant, InfluxDB, Grafana, Langfuse, Phoenix）的运行状态。

## 疑难解答

- **Qdrant 启动失败**: 确保 Docker Desktop 或 Podman 目前正在运行。
- **`llama-cpp-python` 编译错误**: 通常是 Xcode 命令行工具 (Command Line Tools) 安装不完整所致。请尝试手动运行 `xcode-select --install`。
- **内存不足 / 频繁崩溃 (Out of memory / Crashes)**: 大型语言模型会消耗大量系统资源。请关闭不必要的后台应用程序，以为 MLX 或 MPS 保留足够的统一内存。

## 开发与进阶功能

- **RAG 文本导入**: 若要将新的基础资安文件导入至 Qdrant 知识库，通过 `ingest_security_docs.py` 执行文件处理脚本。
- **日志自动化翻译 / 处理**: `translate_logs.py` 提供了一个模板，用于批量处理日志或进行跨语系的转换测试。

## 📄 授权条款

本项目采用 **MIT 授权条款**。 
详情请参阅 [LICENSE.md](LICENSE.md) 与 [LICENSE_ZH.md](LICENSE_ZH.md) 档案。
