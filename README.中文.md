# Cisco Foundation-Sec 8B Native on Apple Mac Silicon (雙語資安助理)

[![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-blue?style=for-the-badge)](README.中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md)

本專案是一個運行在 macOS (Apple Silicon M 系列晶片) 上的雙語 (中文/英文) 資安分析智慧助理。透過整合 [Chainlit](https://docs.chainlit.io/) 提供現代化的互動介面，並結合多個大型語言模型 (LLMs) 與 Qdrant 向量資料庫，實現了專業的資安日誌分析與 RAG (檢索增強生成) 應用。

## 開發工具與技術堆疊

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

## 核心專案元件

1. **前端介面**: 使用 Chainlit (`main.py`) 構建對話式 AI 介面，支援即時文字串流與歷史對話。
2. **多語系支援**: 透過 **Llama-3-Taiwan-8B-Instruct** 處理意圖分類、多語系理解與翻譯，透過 Chainlit 地板語系支援 20+ 種語言。
3. **資安專家**: 透過專為網宇安全領域微調的 **Foundation-Sec-8B**，進行深度的系統與資安日誌分析。
4. **硬體加速**: 整合 macOS Metal (MPS) 與 `llama-cpp-python`，最大化 Apple Silicon 上的推論效能。
5. **向量檢索 (RAG)**: 使用 **Qdrant** (透過 Docker 部署) 儲存並檢索資安 SOP 文件。系統現在支援啟動時**自動 RAG 同步**。
6. **效能監控面板**: 透過 ASITOP 風格的 HUD (Streamlit) 進行硬體即時監控，並利用 InfluxDB v3 + Grafana 追蹤歷史資源消耗趨勢。

## 系統需求

- **作業系統**: macOS (建議使用 Apple Silicon M1/M2/M3)
- **硬體效能**: 建議至少 16GB 的統一記憶體 (取決於模型大小)
- **前置條件**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) 或 [Podman](https://podman.io/) (用於部署 Qdrant)
  - 網際網路連接 (初次啟動時需要下載模型與相依套件)

## 專案架構

```text
.
├── core/                       # 系統核心邏輯 (LLM 管理、資料庫連線、硬體監控、設定檔)
├── models/                     # GGUF 模型儲存目錄 (Llama-3 與 Foundation-Sec)
├── qdrant_storage/             # Qdrant 向量資料庫的持久化儲存目錄
├── influxdb3_storage/          # InfluxDB 指標儲存目錄
├── grafana_storage/            # Grafana 儀表板儲存目錄
├── public/                     # 自定義品牌資源 (Logo、CSS、主題設定)
├── main.py                     # Chainlit 主程式進入點
├── streamlit_app.py            # ASITOP HUD 監控介面 (Streamlit)
├── playbooks.json              # 集中化的資安 SOP/Playbooks，供 RAG 匯入使用
├── .env                        # 環境變數與機敏資訊設定
├── run.sh                      # 智慧化執行腳本 (自動完成設定)
└── (其他設定檔與指令碼)
```

## 如何執行

根據您的環境設定，本專案提供兩種執行方式。

### 方式一：一鍵啟動指令碼 (建議初次使用)

本專案提供了一鍵啟動指令碼，會自動安裝必要套件、下載模型、啟動 Qdrant 容器並執行 Chainlit 服務。

1. **開啟終端機 (Terminal)**，並切換至本專案目錄:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **賦予執行權限並執行啟動指令碼**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **初始啟動過程包含**:
   - `./download_models.sh`: 檢查並下載缺失的 GGUF 語言模型。
   - `./install_metal.sh`: 自動安裝 Homebrew，檢查 Xcode CLTs，並設定支援 Metal 的 `llama-cpp-python` Python 虛擬環境 (`ai_env`)。
   - **Docker Compose**: 檢查並啟動名為 `cisco-foundation-sec-8b-macos-qdrant` 的服務。
   - **自動 RAG 同步**: 應用程式啟動時會自動讀取 `playbooks.json` 並更新 Qdrant 知識庫。
   - 更新套件相依性後，啟動 `main.py` 網頁服務。

### 方式二：手動啟動 (建議完成初始設定後使用)

如果您已經成功執行過 `run.sh` 並下載了所有環境與模型，您後續只需手動啟動服務即可:

1. **確保 Qdrant 服務正在執行**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **啟用虛擬環境並啟動 Chainlit**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### 開始對話

當服務都啟動完畢後，終端機將會顯示 Chainlit 的本地執行資訊。通常您可以開啟瀏覽器並前往 `http://localhost:8000` 來存取資安助理介面。

## 疑難排解

- **Qdrant 啟動失敗**: 確保 Docker Desktop 或 Podman 目前正在執行。
- **`llama-cpp-python` 編譯錯誤**: 通常是 Xcode 命令列工具 (Command Line Tools) 安裝不完整所致。請嘗試手動執行 `xcode-select --install`。
- **記憶體不足 / 頻繁崩潰 (Out of memory / Crashes)**: 大型語言模型會消耗大量系統資源。請關閉不必要的背景應用程式，以為 MLX 或 MPS 保留足夠的統一記憶體。

## 開發與進階功能

- **RAG 文本匯入**: 若要將新的基礎資安文件匯入至 Qdrant 知識庫，透過 `ingest_security_docs.py` 執行文件處理腳本。
- **日誌自動化翻譯 / 處理**: `translate_logs.py` 提供了一個範本，用於批次處理日誌或進行跨語系的轉換測試。