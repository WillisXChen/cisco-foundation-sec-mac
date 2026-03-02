<div align="center">
  <img src="public/logo_dark.png" width="100" alt="Trợ lý Bảo mật AI Logo">

  # 🛡️ Trợ lý Bảo mật AI Nội bộ cho Apple Silicon
  
  *Cisco Foundation-Sec 8B • Phân tích Log Đa ngôn ngữ • Sách hướng dẫn hỗ trợ RAG • Tăng tốc bằng Metal*

  [![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![繁體中文](https://img.shields.io/badge/%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![简体中文](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.简体中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md) [![Español](https://img.shields.io/badge/Espa%C3%B1ol-gray?style=for-the-badge)](README.es.md) [![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-gray?style=for-the-badge)](README.ko.md) [![ไทย](https://img.shields.io/badge/%E0%B9%84%E0%B8%97%E0%B8%A2-gray?style=for-the-badge)](README.th.md) [![Tiếng Việt](https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-blue?style=for-the-badge)](README.vi.md) [![हिन्दी](https://img.shields.io/badge/%E0%A4%B9%E0%A4%BF%E0%A4%A3%E0%A5%8D%E0%A4%A6%E0%A5%80-gray?style=for-the-badge)](README.hi.md)

  **Người duy trì:** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

Dự án này là một trợ lý thông minh phân tích bảo mật đa ngôn ngữ (Anh/Trung/Nhật/Tây Ban Nha/Hàn Quốc/Thái Lan/Việt Nam/Hindi) chạy trên macOS (chip Apple Silicon dòng M). Bằng cách tích hợp [Chainlit](https://docs.chainlit.io/) để cung cấp giao diện tương tác hiện đại và kết hợp nhiều Mô hình Ngôn ngữ Lớn (LLM) với cơ sở dữ liệu vector Qdrant, dự án đạt được khả năng phân tích log bảo mật chuyên nghiệp và các ứng dụng RAG (Retrieval-Augmented Generation).

<div align="center">
  <img src="screenshots/dev-0.0.1/Apple%20Silicon-Prompt-Grasp-PerfPowMon.png" alt="Giám sát hiệu suất" width="800" style="border-radius: 10px; border: 1.2px solid rgba(0, 212, 255, 0.3); box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);">
  <br><br>
  <img src="screenshots/dev-0.0.1/AI-Cisco-Sec-8B.webp" alt="AI-Cisco-Sec-8B" width="800" style="border-radius: 10px; border: 1.2px solid rgba(0, 212, 255, 0.3); box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);">
</div>

## Công nghệ sử dụng

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

## Các thành phần chính

1. **Giao diện Frontend**: Sử dụng Chainlit (`main.py`) để xây dựng giao diện AI đàm thoại, hỗ trợ truyền văn bản thời gian thực và lịch sử trò chuyện.
2. **Hỗ trợ đa ngôn ngữ**: Xử lý phân loại ý định, hiểu đa ngôn ngữ và dịch thuật thông qua **Llama-3-Taiwan-8B-Instruct**. Được tối ưu hóa cho **Tiếng Anh**, **Tiếng Trung Phồn thể**, **Tiếng Nhật**, **Tiếng Tây Ban Nha**, **Tiếng Hàn**, **Tiếng Thái**, **Tiếng Việt** và **Tiếng Hindi**.
3. **Chuyên gia bảo mật**: Thực hiện phân tích chuyên sâu log hệ thống và bảo mật thông qua **Foundation-Sec-8B**, được tinh chỉnh riêng cho lĩnh vực an ninh mạng. Bao gồm logic **Ngắn gọn cấp Doanh nghiệp (Conciseness)** để đưa ra lời khuyên kỹ thuật có cấu trúc, ngắn gọn và có thể hành động.
4. **Tăng tốc phần cứng & Tinh chỉnh**: Tích hợp macOS Metal (MPS) với `llama-cpp-python`. Hỗ trợ **offloading GPU layer thủ công** và **điều chỉnh Context Window (KV Cache)** qua `.env` để cân bằng việc sử dụng VRAM trên Mac Pro/Studio (M2/M3).
5. **Truy xuất vector (RAG)**: Sử dụng **Qdrant** (triển khai qua Docker) để lưu trữ và truy xuất các sách hướng dẫn bảo mật (playbooks). Hệ thống có **tự động đồng bộ RAG** khi khởi động.
6. **Quan sát & Theo dõi**: Tích hợp với **Langfuse** và **Arize Phoenix** để kiểm tra sâu, giám sát chất lượng phản hồi AI và ghi nhật ký **Structlog** toàn hệ thống.
7. **Bảng điều khiển hiệu suất & HUD**: Giám sát phần cứng thời gian thực theo phong cách ASITOP thông qua HUD (Streamlit) sử dụng **GraphQL subscriptions**. Bao gồm các bảng "PerfMon" và "Lịch sử".
8. **UI/UX tinh tế**: Bộ chọn ngôn ngữ cố định ở chính giữa phía trên với các biểu tượng quốc kỳ để chuyển đổi nhanh chóng giữa tất cả ngôn ngữ được hỗ trợ.

## Yêu cầu hệ thống

- **Hệ điều hành**: macOS (Khuyên dùng Apple Silicon M1/M2/M3)
- **Cấu hình phần cứng**: Khuyên dùng ít nhất 16GB bộ nhớ thống nhất (tùy thuộc vào kích thước mô hình)
- **Điều kiện tiên quyết**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) hoặc [Podman](https://podman.io/) (để triển khai Qdrant)
  - Kết nối Internet (cần thiết để tải mô hình và các phụ thuộc trong lần chạy đầu tiên)

## Kiến trúc dự án

```text
.
├── core/                       # Logic hệ thống cốt lõi (LLM, Database, Phần cứng, Config)
├── models/                     # Lưu trữ mô hình GGUF (Llama-3 và Foundation-Sec)
├── locales/                    # Các tệp dịch thuật đa ngôn ngữ (.po/.mo)
├── qdrant_storage/             # Thư mục lưu trữ cố định cho Qdrant vector database
├── influxdb3_storage/          # Lưu trữ cố định cho metrics
├── grafana_storage/            # Lưu trữ dashboard Grafana
├── langfuse_db_storage/        # Lưu trữ cục bộ cho dữ liệu theo dõi Langfuse
├── public/                     # Tài sản thương hiệu tùy chỉnh (logos, CSS, themes)
├── main.py                     # Điểm vào chính của ứng dụng Chainlit
├── api.py                      # GraphQL & Các điểm cuối API tùy chỉnh
├── streamlit_app.py            # Giao diện giám sát ASITOP HUD
├── health_check.py             # Tiện ích kiểm tra sức khỏe hệ sinh thái toàn hệ thống
├── playbooks.json              # Các SOP/Playbooks bảo mật tập trung để nạp vào RAG
├── .env                        # Biến môi trường và bí mật
├── run.sh                      # Script thực thi thông minh (tự động thiết lập)
└── (Các tệp cấu hình và script khác)
```

## Cách thức vận hành

Tùy thuộc vào thiết lập môi trường của bạn, dự án cung cấp hai cách để chạy.

### Cách 1: Script khởi chạy một lần nhấp (Khuyên dùng cho lần đầu)

Dự án cung cấp một script khởi chạy một lần nhấp sẽ tự động cài đặt các thư viện cần thiết, tải mô hình, khởi động container Qdrant và chạy dịch vụ Chainlit.

1. **Mở Terminal**, và di chuyển đến thư mục dự án:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **Cấp quyền thực thi và chạy script**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **Quá trình khởi chạy ban đầu bao gồm**:
   - `./download_models.sh`: Kiểm tra và tải xuống các mô hình GGUF còn thiếu.
   - `./install_metal.sh`: Tự động cài đặt Homebrew, kiểm tra Xcode CLTs, và thiết lập môi trường ảo Python (`ai_env`) với `llama-cpp-python` hỗ trợ Metal.
   - **Docker Compose**: Kiểm tra và khởi động dịch vụ mang tên `cisco-foundation-sec-8b-macos-qdrant`.
   - **Đồng bộ RAG tự động**: Ứng dụng tự động đọc `playbooks.json` và cập nhật cơ sở kiến thức Qdrant khi mở.
   - Khởi động dịch vụ web `main.py` sau khi cập nhật các thư viện phụ thuộc.

### Cách 2: Khởi chạy thủ công (Khuyên dùng sau lần đầu tiên)

Nếu bạn đã thực thi thành công `run.sh` và tải xong môi trường và mô hình, bạn chỉ cần khởi động thủ công các dịch vụ:

1. **Đảm bảo dịch vụ Qdrant đang chạy**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **Kích hoạt môi trường ảo và khởi chạy Chainlit**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### Bắt đầu trò chuyện

Khi các dịch vụ đã sẵn sàng, terminal sẽ hiển thị thông tin thực thi cục bộ cho Chainlit. Thông thường, bạn có thể truy cập giao diện trợ lý bảo mật bằng cách mở trình duyệt và truy cập `http://localhost:8000`.

## ⚙️ Tối ưu hóa hiệu suất (Nâng cao)

Để đảm bảo hệ thống nằm trong giới hạn tài nguyên (ví dụ: < 50% RAM trên Mac 24GB), bạn có thể tinh chỉnh các thông số sau trong tệp `.env`:

*   `N_GPU_LAYERS_LLAMA3`: GPU layers cho mô hình chung (-1 cho tất cả, 0 cho CPU).
*   `N_GPU_LAYERS_SEC`: GPU layers cho mô hình bảo mật.
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: Context size (mặc định 2048). Giảm giá trị này sẽ tiết kiệm RAM đáng kể.

## 📊 Quan sát & Giám sát

Hệ thống được trang bị các công cụ quan sát chuyên nghiệp:

- **Langfuse**: Theo dõi các cuộc gọi LLM, chi phí và mức sử dụng token.
- **Arize Phoenix**: Tự động đánh giá phản hồi RAG và theo dõi dấu vết.
- **ASITOP HUD**: HUD thời gian thực để giám sát GPU/CPU/RAM.
- **Grafana**: Dashboard hiệu suất lịch sử.
- **Kiểm tra sức khỏe hệ thống**: Chạy `python health_check.py` để kiểm tra trạng thái của toàn bộ hệ sinh thái Docker/ML (Qdrant, InfluxDB, Grafana, Langfuse, Phoenix).

## Xử lý sự cố

- **Qdrant không khởi động được**: Đảm bảo Docker Desktop hoặc Podman đang chạy.
- **Lỗi biên dịch `llama-cpp-python`**: Thường do cài đặt thiếu Xcode Command Line Tools. Hãy chạy `xcode-select --install` thủ công.
- **Hết bộ nhớ / Treo máy thường xuyên**: Các mô hình ngôn ngữ lớn tiêu tốn tài nguyên hệ thống đáng kể. Vui lòng đóng các ứng dụng nền không cần thiết.

## Phát triển và các tính năng nâng cao

- **Nạp văn bản RAG**: Để nhập các tài liệu bảo mật mới vào cơ sở kiến thức Qdrant, hãy thực thi script xử lý tài liệu thông qua `ingest_security_docs.py`.
- **Dịch tệp nhật ký/Xử lý tự động**: `translate_logs.py` cung cấp mẫu để xử lý hàng loạt nhật ký hoặc thực hiện các bài kiểm tra chuyển đổi đa ngôn ngữ.

## 📄 Bản quyền

Dự án này được cấp phép theo **Giấy phép MIT**.
Xem tệp [LICENSE.md](LICENSE.md) và [LICENSE_ZH.md](LICENSE_ZH.md) để biết thêm chi tiết.
