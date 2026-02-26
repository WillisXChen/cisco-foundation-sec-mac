# Cisco Foundation-Sec 8B Native on Apple Mac Silicon (バイリンガル・セキュリティ・アシスタント)

[![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-blue?style=for-the-badge)](README.ja.md)

このプロジェクトは、macOS（Apple Silicon Mシリーズチップ）上で動作するバイリンガル（中国語/英語対応可能）のセキュリティ分析スマートアシスタントです。[Chainlit](https://docs.chainlit.io/)を統合して最新のインタラクティブなUIを提供し、複数の大規模言語モデル（LLMs）とQdrantベクトルデータベースを組み合わせることで、プロフェッショナルなセキュリティログ分析とRAG（検索拡張生成）アプリケーションを実現しています。

## 使用技術

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

## コアコンポーネント

1. **フロントエンドインターフェース**: Chainlit (`cisco_security_chainlit.py`) を使用して会話形式のAIインターフェースを構築し、リアルタイムでのテキストストリーミングとチャット履歴をサポートします。
2. **多言語サポート**: **Llama-3-Taiwan-8B-Instruct**を通じて、意図の分類、多言語理解、および翻訳を処理します。
3. **セキュリティエクスパート**: サイバーセキュリティ領域に特化してファインチューニングされた**Foundation-Sec-8B**により、詳細なシステムおよびセキュリティログ分析を実行します。
4. **ハードウェアアクセラレーション**: macOS Metal (MPS)と`llama-cpp-python`を統合し、Apple Silicon上での推論パフォーマンスを最大化します。
5. **ベクトル検索 (RAG)**: Docker経由でデプロイされた**Qdrant**を使用して、企業内のセキュリティドキュメントを保存・検索することで、言語モデルの分析精度を向上させ、ハルシネーションを低減します。

## システム要件

- **オペレーティングシステム**: macOS (Apple Silicon M1/M2/M3を推奨)
- **ハードウェアパフォーマンス**: 統合メモリ16GB以上を推奨 (モデルサイズに依存)
- **前提条件**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) または [Podman](https://podman.io/) (Qdrantデプロイ用)
  - インターネット接続 (初回起動時のモデルや依存関係のダウンロードに必要)

## プロジェクト構造

```text
.
├── ai_env/                     # Python仮想環境
├── models/                     # GGUFモデルの保存先 (Llama-3 および Foundation-Sec)
├── qdrant_storage/             # Qdrantベクトルデータベースの永続的保存先ディレクトリ
├── cisco_security_chainlit.py  # Chainlitメインアプリケーションファイル
├── download_models.sh          # 必要なHuggingFace GGUFモデルの自動ダウンロード
├── install_metal.sh            # macOS Metal環境、Venvのセットアップ、MPS依存関係のインストール
├── run.sh                      # 統合実行スクリプト (初期セットアップと起動を自動化)
└── (その他の設定ファイルやスクリプト)
```

## 実行方法

環境設定に応じて、プロジェクトには2つの実行方法があります。

### 方法 1: ワンクリック起動スクリプト (初回使用時に推奨)

プロジェクトには、必要なパッケージのインストール、モデルのダウンロード、Qdrantコンテナの開始、およびChainlitサービスの実行を自動的に行うワンクリック起動スクリプトが用意されています。

1. **ターミナルを開き**、本プロジェクトディレクトリに移動します:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **実行権限を付与し、起動スクリプトを実行します**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **初回の起動プロセスには以下が含まれます**:
   - `./download_models.sh`: 不足しているGGUF言語モデルを確認してダウンロードします。
   - `./install_metal.sh`: Homebrewを自動的にインストールし、Xcode CLTsを確認し、Metalをサポートする`llama-cpp-python`を備えたPython仮想環境（`ai_env`）をセットアップします。
   - **Docker Compose**: `cisco-foundation-sec-8b-macos-qdrant`という名前のサービスを確認して起動します。
   - パッケージの依存関係を更新後、`cisco_security_chainlit.py`ウェブサービスを起動します。

### 方法 2: 手動起動 (初回セットアップ完了後に推奨)

すでに`run.sh`を正常に実行し、すべての環境とモデルをダウンロードした場合は、次のようにサービスを手動で起動するだけで済みます:

1. **Qdrantサービスが実行中であることを確認**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **仮想環境を有効化し、Chainlitを起動**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./cisco_security_chainlit.py -w
   ```

### チャットの開始

サービスが起動すると、ターミナルにChainlitのローカル実行情報が表示されます。通常、ブラウザを開き`http://localhost:8000`にアクセスすることで、セキュリティアシスタントのインターフェースにアクセスできます。

## トラブルシューティング

- **Qdrantが起動しない**: Docker Desktop または Podmanが現在実行中であることを確認してください。
- **`llama-cpp-python` のコンパイルエラー**: 通常、Xcode Command Line Tools の不完全なインストールが原因です。`xcode-select --install`を手動で実行してみてください。
- **メモリ不足 / 頻繁なクラッシュ (Out of memory / Crashes)**: 大規模言語モデルはシステムリソースを大量に消費します。MLX または MPS 用に十分な統合メモリを確保するために、不要なバックグラウンドアプリケーションを閉じてください。

## 開発と高度な機能

- **RAG テキストの取り込み**: Qdrantナレッジベースに新しいベースのセキュリティドキュメントを取り込むには、`ingest_security_docs.py`を介してドキュメント処理スクリプトを実行します。
- **ログの自動翻訳 / 処理**: `translate_logs.py`は、ログのバッチ処理や言語間の変換テストを実行するためのテンプレートを提供します。
