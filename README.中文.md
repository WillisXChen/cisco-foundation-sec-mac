# Cisco Foundation-Sec 8B 原生運行於 Apple Mac 晶片 (雙語資安助手)

此專案是一個運行在 macOS (Apple Silicon M系列晶片) 上的雙語（中/英文）資安分析智慧助手。透過整合 [Chainlit](https://docs.chainlit.io/) 提供現代化的互動介面，並結合多個大型語言模型 (LLMs) 與 Qdrant 向量資料庫，達成專業的資安日誌分析與 RAG (檢索增強生成) 應用。

## 使用技術 (Built With)

<div align="center">
  <h3>
    <img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=macos&logoColor=white" height="24" alt="macOS">
    <img src="https://img.shields.io/badge/Apple_Silicon-999999?style=for-the-badge&logo=apple&logoColor=white" height="24" alt="Apple Silicon">
    <img src="https://img.shields.io/badge/Homebrew-F2A900?style=for-the-badge&logo=homebrew&logoColor=white" height="24" alt="Homebrew">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="24" alt="Python">
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" height="24" alt="PyTorch (MPS)">
    <img src="https://img.shields.io/badge/LLaMA_C++-FF7F50?style=for-the-badge&logo=meta&logoColor=white" height="24" alt="LLaMA C++">
    <img src="https://img.shields.io/badge/Chainlit-4A25E1?style=for-the-badge&logo=chainlit&logoColor=white" height="24" alt="Chainlit">
    <img src="https://img.shields.io/badge/Qdrant-1B053A?style=for-the-badge&logo=qdrant&logoColor=white" height="24" alt="Qdrant">
    <img src="https://img.shields.io/badge/FastEmbed-FF4B4B?style=for-the-badge&logo=python&logoColor=white" height="24" alt="FastEmbed">
    <br><br>
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" height="24" alt="Docker">
    <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" height="24" alt="Docker Compose">
    <img src="https://img.shields.io/badge/OrbStack-5645B6?style=for-the-badge&logo=orbstack&logoColor=white" height="24" alt="OrbStack">
    <img src="https://img.shields.io/badge/Podman-892CA0?style=for-the-badge&logo=podman&logoColor=white" height="24" alt="Podman">
    <img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" height="24" alt="Hugging Face">
  </h3>
</div>

## 專案核心元件

1. **前端介面**: 採用 Chainlit (`cisco_security_chainlit.py`) 建立對話式 AI 介面，支援即時文字串流與歷史對話記錄。
2. **多語言支援**: 透過 **Llama-3-Taiwan-8B-Instruct** 處理意圖分類、多語言理解與翻譯。
3. **資安專欄**: 透過專為資安領域微調的 **Foundation-Sec-8B** 進行深度的系統與安全日誌分析。
4. **硬體加速**: 整合 macOS Metal (MPS) 與 `llama-cpp-python`，最大化 Apple Silicon 上的推理效能。
5. **向量檢索 (RAG)**: 使用 **Qdrant** (Docker 部署) 儲存與檢索企業內部的資安文件，藉此增強語言模型的分析準確度並降低幻覺。

## 系統需求

- **作業系統**: macOS (推薦 Apple Silicon M1/M2/M3)
- **硬體效能**: 建議至少 16GB 以上的記憶體 (依模型大小而定)
- **前置軟體**: 
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) 或 [Podman](https://podman.io/) (用以部署 Qdrant)
  - 網路連線 (初次啟動需下載模型檔及相關套件)

## 專案架構

```text
.
├── ai_env/                     # Python 虛擬環境
├── models/                     # GGUF 模型存放區 (Llama-3 與 Foundation-Sec)
├── qdrant_storage/             # Qdrant 向量資料庫的持久化存儲目錄
├── cisco_security_chainlit.py  # 主從式 Chainlit 應用程式主檔
├── download_models.sh          # 自動下載所需之 HuggingFace GGUF 模型
├── install_metal.sh            # 配置 macOS Metal 環境、Venv 並安裝 MPS 加速相依套件
├── run.sh                      # 整合執行腳本 (自動化初始設定與啟動)
└── (其他設定檔與腳本)
```

## 如何執行 (How to Run)

依據您的需求，專案提供了兩種啟動方式。

### 方式一：使用一鍵整合腳本 (初次使用推薦)

專案中提供了一鍵式啟動腳本，會自動安裝必要套件、下載模型、啟動 Qdrant 容器並運行 Chainlit 服務。

1. **開啟終端機 (Terminal)**，切換至此專案目錄：
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **給予執行權限並執行啟動腳本**：
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **初次啟動流程包含**：
   - `./download_models.sh`: 檢查並下載缺失的 GGUF 語言模型。
   - `./install_metal.sh`: 自動安裝 Homebrew、檢查 Xcode CLTs，並設置 Python 虛擬環境 (`ai_env`) 及支援 Metal 的 `llama-cpp-python`。
   - **Docker Compose**: 檢查並啟動名為 `cisco-foundation-sec-8b-macos-qdrant` 的服務。
   - 更新套件依賴後啟動 `cisco_security_chainlit.py` 網頁服務。

### 方式二：手動啟動 (環境已建置完畢後推薦)

若您已經成功執行過 `run.sh`，且相關環境與模型都已下載設定完成，後續只需手動啟動服務即可：

1. **確認 Qdrant 服務已在運行**：
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **進入虛擬環境並啟動 Chainlit**：
   ```bash
   source ai_env/bin/activate
   chainlit run ./cisco_security_chainlit.py -w
   ```

### 開始對話

當服務啟動後，終端機將會顯示 Chainlit 在本機執行的資訊，通常可以透過打開瀏覽器並前往 `http://localhost:8000` 來存取資安助手介面。

## 疑難排解 (Troubleshooting)

- **Qdrant 啟動失敗**：確保 Docker 或 Podman 桌面版已在運行中。
- **編譯 `llama-cpp-python` 出錯**：通常是由於 Xcode Command Line Tools 未安裝完全，請嘗試手動執行 `xcode-select --install`。
- **缺少記憶體/頻繁當機**：大型語言模型佔用較多系統資源，請盡量關閉非必要的背景程式，保留足夠的統一記憶體供 MLX 或 MPS 使用。

## 開發與進階功能

- **RAG 文本嵌入 (Ingestion)**：若需導入新的基礎資安文件至 Qdrant 知識庫，可透過 `ingest_security_docs.py` 腳本執行文件處理。
- **日誌自動翻譯/處理**：`translate_logs.py` 提供了批次處理日誌或是跨語言轉換測試的範本。