<div align="center">
  <img src="public/logo_dark.png" width="100" alt="네이티브 AI 보안 비서 로고">

  # 🛡️ Apple Silicon 전용 네이티브 AI 보안 비서
  
  *Cisco Foundation-Sec 8B • 이중 언어 로그 분석 • RAG 활성화 플레이북 • Metal 가속*

  [![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md) [![Español](https://img.shields.io/badge/Espa%C3%B1ol-gray?style=for-the-badge)](README.es.md) [![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-blue?style=for-the-badge)](README.ko.md) [![ไทย](https://img.shields.io/badge/%E0%B9%84%E0%B8%97%E0%B8%A2-gray?style=for-the-badge)](README.th.md) [![Tiếng Việt](https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-gray?style=for-the-badge)](README.vi.md) [![हिन्दी](https://img.shields.io/badge/%E0%A4%B9%E0%A4%BF%E0%A4%A3%E0%A5%8D%E0%A4%A6%E0%A5%80-gray?style=for-the-badge)](README.hi.md)

  **유지관리자:** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

이 프로젝트는 macOS(Apple Silicon M-series 칩)에서 실행되는 다국어(영어/중국어/일본어/스페인어/한국어/태국어/베트남어/힌디어) 보안 분석 스마트 비서입니다. [Chainlit](https://docs.chainlit.io/)을 통합하여 현대적인 인터랙티브 인터페이스를 제공하고, 여러 대규모 언어 모델(LLM)과 Qdrant 벡터 데이터베이스를 결합하여 전문적인 보안 로그 분석 및 RAG(검색 증강 생성) 애플리케이션을 구현합니다.

## 기술 스택

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

## 핵심 프로젝트 구성 요소

1. **프론트엔드 인터페이스**: Chainlit(`main.py`)을 사용하여 대화형 AI 인터페이스를 구축하며, 실시간 텍스트 스트리밍과 채팅 기록을 지원합니다.
2. **다국어 지원**: **Llama-3-Taiwan-8B-Instruct**를 통해 의도 분류, 다국어 이해 및 번역을 처리합니다. **영어**, **번체 중국어**, **일본어**, **스페인어**, **한국어**, **태국어**, **베트남어**, **힌디어**에 최적화되어 있습니다.
3. **보안 전문가**: 사이버 보안 도메인에 특화되어 미세 조정된 **Foundation-Sec-8B**를 통해 심층적인 시스템 및 보안 로그 분석을 수행합니다.
4. **하도웨어 가속 및 미세 조정**: macOS Metal(MPS)을 `llama-cpp-python`과 통합합니다. Mac Pro/Studio (M2/M3)에서 VRAM 사용량의 균형을 맞추기 위해 `.env`를 통한 **수동 GPU 레이어 오프로딩** 및 **컨텍스트 윈도우(KV 캐시) 조정**을 지원합니다.
5. **벡터 검색 (RAG)**: 보안 플레이북을 저장하고 검색하기 위해 **Qdrant**(Docker를 통해 배포)를 사용합니다. 시작 시 **자동 RAG 동기화** 기능을 제공합니다.
6. **관측 가능성 및 추적**: 심층 추적 감사, AI 응답 품질 모니터링 및 시스템 전반의 **Structlog** 로깅을 위해 **Langfuse** 및 **Arize Phoenix**와 통합되었습니다.
7. **성능 대시보드 및 플로팅 HUD**: **GraphQL 구독**을 활용하여 ASITOP 스타일 HUD(Streamlit)를 통한 실시간 하드웨어 모니터링을 제공합니다. "PerfMon" 및 "History" 플로팅 패널이 포함되어 있습니다.
8. **정제된 UI/UX**: 모든 지원되는 언어 간에 빠르게 전환할 수 있는 국기 아이콘이 있는 상단 중앙의 고정 언어 선택기.

## 시스템 요구 사항

- **운영 체제**: macOS (Apple Silicon M1/M2/M3 권장)
- **하드웨어 사양**: 최소 16GB 통합 메모리 권장 (모델 크기에 따라 다름)
- **사전 요구 사항**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) 또는 [Podman](https://podman.io/) (Qdrant 배포용)
  - 인터넷 연결 (최초 실행 시 모델 및 종속성 다운로드에 필요)

## 프로젝트 아키텍처

```text
.
├── core/                       # 핵심 시스템 로직 (LLM, 데이터베이스, 하드웨어, 설정)
├── models/                     # GGUF 모델 저장소 (Llama-3 및 Foundation-Sec)
├── qdrant_storage/             # Qdrant 벡터 데이터베이스용 영구 저장소 디렉토리
├── influxdb3_storage/          # 메트릭용 영구 저장소
├── grafana_storage/            # Grafana 대시보드 저장소
├── public/                     # 맞춤형 브랜드 자산 (로고, CSS, 테마)
├── main.py                     # 메인 Chainlit 애플리케이션 진입점
├── streamlit_app.py            # ASITOP HUD 모니터링 인터페이스
├── playbooks.json              # RAG 인제션을 위한 중앙 집중식 보안 SOP/플레이북
├── .env                        # 환경 변수 및 비밀 키
├── run.sh                      # 스마트 실행 스크립트 (설정 자동화)
└── (기타 설정 파일 및 스크립트)
```

## 실행 방법

환경 설정에 따라 두 가지 방법으로 실행할 수 있습니다.

### 방법 1: 원클릭 시작 스크립트 (최초 실행 시 권장)

이 프로젝트는 필요한 패키지를 자동으로 설치하고, 모델을 다운로드하고, Qdrant 컨테이너를 시작하고, Chainlit 서비스를 실행하는 원클릭 시작 스크립트를 제공합니다.

1. **터미널을 열고** 이 프로젝트 디렉토리로 이동합니다.
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **실행 권한을 부여하고 시작 스크립트를 실행합니다**.
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **초기 시작 프로세스에는 다음이 포함됩니다**:
   - `./download_models.sh`: 누락된 GGUF 언어 모델을 확인하고 다운로드합니다.
   - `./install_metal.sh`: Homebrew를 자동으로 설치하고, Xcode CLT를 확인하고, Metal을 지원하는 `llama-cpp-python`으로 Python 가상 환경(`ai_env`)을 설정합니다.
   - **Docker Compose**: `cisco-foundation-sec-8b-macos-qdrant`라는 서비스를 확인하고 시작합니다.
   - **자동 RAG 동기화**: 애플리케이션이 시작 시 `playbooks.json`을 자동으로 읽고 Qdrant 지식 베이스를 업데이트합니다.
   - 패키지 종속성 업데이트 후 `main.py` 웹 서비스를 시작합니다.

### 방법 2: 수동 시작 (초기 설정 후 권장)

`run.sh`를 성공적으로 실행하고 모든 환경과 모델을 다운로드했다면, 이후에는 수동으로 서비스만 시작하면 됩니다.

1. **Qdrant 서비스가 실행 중인지 확인합니다**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **가상 환경을 활성화하고 Chainlit을 시작합니다**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### 채팅 시작하기

서비스가 시작되면 터미널에 Chainlit의 로컬 실행 정보가 표시됩니다. 일반적으로 브라우저를 열고 `http://localhost:8000`으로 이동하여 보안 비서 인터페이스에 액세스할 수 있습니다.

## ⚙️ 성능 최적화 (고급)

시스템이 리소스 제한 내에서 유지되도록 하려면(예: 24GB Mac에서 RAM 50% 미만) `.env`에서 다음을 미세 조정할 수 있습니다.

*   `N_GPU_LAYERS_LLAMA3`: 일반 모델의 GPU 레이어 (모두 -1, CPU는 0).
*   `N_GPU_LAYERS_SEC`: 보안 모델의 GPU 레이어.
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: 컨텍스트 크기 (기본값 2048). 이를 줄이면 상당한 RAM이 절약됩니다.

## 📊 관측 가능성 및 모니터링

이 시스템은 엔터프라이즈급 관측 가능성 도구를 갖추고 있습니다.

- **Langfuse**: LLM 호출, 비용 및 토큰 사용량을 추적합니다.
- **Arize Phoenix**: RAG 응답의 자동 평가 및 추적.
- **ASITOP HUD**: GPU/CPU/RAM 모니터링을 위한 실시간 플로팅 HUD.
- **Grafana**: 기록 성능 대시보드.

## 문제 해결

- **Qdrant 시작 실패**: Docker Desktop 또는 Podman이 현재 실행 중인지 확인하세요.
- **`llama-cpp-python` 컴파일 오류**: 일반적으로 Xcode 커맨드 라인 도구 설치가 불완전하여 발생합니다. `xcode-select --install`을 수동으로 실행해 보세요.
- **메모리 부족 / 빈번한 충돌**: 대규모 언어 모델은 상당한 시스템 리소스를 소비합니다. MLX 또는 MPS 사용을 위해 충분한 통합 메모리를 확보할 수 있도록 불필요한 백그라운드 애플리케이션을 종료하세요.

## 개발 및 고급 기능

- **RAG 텍스트 인제션**: 새로운 기본 보안 문서를 Qdrant 지식 베이스로 가져오려면 `ingest_security_docs.py`를 통해 문서 처리 스크립트를 실행하세요.
- **자동 로그 번역/처리**: `translate_logs.py`는 로그를 일괄 처리하거나 언어 간 변환 테스트를 수행하기 위한 템플릿을 제공합니다.

## 📄 라이선스

이 프로젝트는 **MIT 라이선스**에 따라 라이선스가 부여됩니다.
자세한 내용은 [LICENSE.md](LICENSE.md) 및 [LICENSE_ZH.md](LICENSE_ZH.md) 파일을 참조하세요.
