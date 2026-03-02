<div align="center">
  <img src="public/logo_dark.png" width="100" alt="Native AI Security Assistant Logo">

  # 🛡️ Native AI Security Assistant สำหรับ Apple Silicon
  
  *Cisco Foundation-Sec 8B • การวิเคราะห์บันทึกหลายภาษา • คู่มือการใช้งานที่เปิดใช้งาน RAG • เร่งความเร็วด้วย Metal*

  [![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![繁體中文](https://img.shields.io/badge/%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![简体中文](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.简体中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md) [![Español](https://img.shields.io/badge/Espa%C3%B1ol-gray?style=for-the-badge)](README.es.md) [![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-gray?style=for-the-badge)](README.ko.md) [![ไทย](https://img.shields.io/badge/%E0%B9%84%E0%B8%97%E0%B8%A2-blue?style=for-the-badge)](README.th.md) [![Tiếng Việt](https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-gray?style=for-the-badge)](README.vi.md) [![हिन्दी](https://img.shields.io/badge/%E0%A4%B9%E0%A4%BF%E0%A4%A3%E0%A5%8D%E0%A4%A6%E0%A5%80-gray?style=for-the-badge)](README.hi.md)

  **ผู้ดูแลรักษา:** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

โปรเจกต์นี้เป็นผู้ช่วยอัจฉริยะสำหรับการวิเคราะห์ความปลอดภัยในหลายภาษา (อังกฤษ/จีน/ญี่ปุ่น/สเปน/เกาหลี/ไทย/เวียดนาม/ฮินดี) ที่ทำงานบน macOS (ชิป Apple Silicon ซีรีส์ M) ด้วยการผสานรวม [Chainlit](https://docs.chainlit.io/) เพื่อมอบอินเทอร์เฟซแบบโต้ตอบที่ทันสมัย และการรวมโมเดลภาษาขนาดใหญ่ (LLM) หลายรุ่นเข้ากับฐานข้อมูลเวกเตอร์ Qdrant ทำให้สามารถวิเคราะห์บันทึกความปลอดภัยระดับมืออาชีพและการประยุกต์ใช้ RAG (Retrieval-Augmented Generation) ได้

<div align="center">
  <img src="screenshots/dev-0.0.1/Apple%20Silicon-Prompt-Grasp-PerfPowMon.png" alt="การตรวจสอบประสิทธิภาพ" width="800" style="border-radius: 10px; border: 1.2px solid rgba(0, 212, 255, 0.3); box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);">
  <br><br>
  <img src="screenshots/dev-0.0.1/AI-Cisco-Sec-8B.webp" alt="AI-Cisco-Sec-8B" width="800" style="border-radius: 10px; border: 1.2px solid rgba(0, 212, 255, 0.3); box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);">
</div>

## สร้างด้วย

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

## ส่วนประกอบหลักของโปรเจกต์

1. **อินเทอร์เฟซส่วนหน้า**: ใช้ Chainlit (`main.py`) เพื่อสร้างอินเทอร์เฟซ AI แบบสนทนา รองรับการสตรีมข้อความตามเวลาจริงและประวัติการแชท
2. **การรองรับหลายภาษา**: จัดการการจำแนกเจตนา ความเข้าใจหลายภาษา และการแปลผ่าน **Llama-3-Taiwan-8B-Instruct** ปรับปรุงให้เหมาะสมสำหรับ **ภาษาอังกฤษ**, **ภาษาจีนตัวเต็ม**, **ภาษาญี่ปุ่น**, **ภาษาสเปน**, **ภาษาเกาหลี**, **ภาษาไทย**, **ภาษาเวียดนาม** และ **ภาษาฮินดี**
3. **ผู้เชี่ยวชาญด้านความปลอดภัย**: ดำเนินการวิเคราะห์บันทึกระบบและความปลอดภัยในเชิงลึกผ่าน **Foundation-Sec-8B** ซึ่งได้รับการปรับแต่งมาโดยเฉพาะสำหรับโดเมนความปลอดภัยทางไซเบอร์ มาพร้อมกับตรรกะ **ความกระชับระดับองค์กร (Conciseness)** เพื่อคำแนะนำทางเทคนิคที่มีโครงสร้าง สั้น และนำไปใช้ได้จริง
4. **การเร่งความเร็วฮาร์ดแวร์และการปรับแต่ง**: ผสานรวม macOS Metal (MPS) เข้ากับ `llama-cpp-python` รองรับการ **ปิดโหลดเลเยอร์ GPU ด้วยตนเอง** และ **การปรับหน้าต่างบริบท (KV Cache)** ผ่าน `.env` เพื่อปรับสมดุลการใช้งาน VRAM บน Mac Pro/Studio (M2/M3)
5. **การดึงข้อมูลเวกเตอร์ (RAG)**: ใช้ **Qdrant** (ติดตั้งผ่าน Docker) เพื่อจัดเก็บและดึงข้อมูลคู่มือความปลอดภัย ระบบมี **การซิงค์ RAG อัตโนมัติ** เมื่อเริ่มต้น
6. **ความสามารถในการสังเกตและการติดตาม**: เข้ากับ **Langfuse** และ **Arize Phoenix** สำหรับการตรวจสอบการติดตามเชิงลึก การติดตามคุณภาพการตอบสนองของ AI และการบันทึก **Structlog** ทั่วทั้งระบบ
7. **แดชบอร์ดประสิทธิภาพและ HUD แบบลอยตัว**: การมอนิเตอร์ฮาร์ดแวร์ตามเวลาจริงผ่าน HUD สไตล์ ASITOP (Streamlit) โดยใช้ **การสมัครใช้บริการ GraphQL** รวมถึงพาเนลแบบลอยตัว "PerfMon" และ "ประวัติ"
8. **UI/UX ที่ปรับปรุง**: ตัวเลือกภาษาที่อยู่ตรงกลางด้านบนพร้อมไอคอนธงเพื่อการสลับระหว่างภาษาที่รองรับทั้งหมดได้อย่างรวดเร็ว

## ความต้องการของระบบ

- **ระบบปฏิบัติการ**: macOS (แนะนำให้ใช้ Apple Silicon M1/M2/M3)
- **ประสิทธิภาพฮาร์ดแวร์**: แนะนำให้มีหน่วยความจำรวมอย่างน้อย 16GB (ขึ้นอยู่กับขนาดของโมเดล)
- **ข้อกำหนดเบื้องต้น**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) หรือ [Podman](https://podman.io/) (สำหรับติดตั้ง Qdrant)
  - การเชื่อมต่ออินเทอร์เน็ต (จำเป็นสำหรับการดาวน์โหลดโมเดลและไลบรารีในการเริ่มครั้งแรก)

## สถาปัตยกรรมโปรเจกต์

```text
.
├── core/                       # ตรรกะของระบบหลัก (LLM, ฐานข้อมูล, ฮาร์ดแวร์, การกำหนดค่า)
├── models/                     # พื้นที่เก็บโมเดล GGUF (Llama-3 และ Foundation-Sec)
├── locales/                    # ไฟล์แปลภาษา (.po/.mo)
├── qdrant_storage/             # ไดเรกทอรีจัดเก็บข้อมูลถาวรสำหรับฐานข้อมูลเวกเตอร์ Qdrant
├── influxdb3_storage/          # พื้นที่เก็บข้อมูลถาวรสำหรับเมทริกซ์
├── grafana_storage/            # พื้นที่เก็บข้อมูลแดชบอร์ด Grafana
├── langfuse_db_storage/        # พื้นที่เก็บข้อมูลภายในสำหรับ Langfuse
├── public/                     # สินทรัพย์ตราสินค้าที่กำหนดเอง (โลโก้, CSS, ธีม)
├── main.py                     # จุดเริ่มต้นหลักของแอปพลิเคชัน Chainlit
├── api.py                      # จุดเชื่อมต่อ GraphQL และ API ที่กำหนดเอง
├── streamlit_app.py            # อินเทอร์เฟซมอนิเตอร์ ASITOP HUD
├── health_check.py             # ยูทิลิตี้ตรวจสอบสถานะระบบนิเวศของทั้งระบบ
├── playbooks.json              # SOP ความปลอดภัย/คู่มือการใช้งานส่วนกลางสำหรับการนำเข้า RAG
├── .env                        # ตัวแปรสภาพแวดล้อมและความลับ
├── run.sh                      # สคริปต์การรันอัจฉริยะ (ตั้งค่าอัตโนมัติ)
└── (ไฟล์กำหนดค่าและสคริปต์อื่น ๆ)
```

## วิธีการรัน

ขึ้นอยู่กับการตั้งค่าสภาพแวดล้อมของคุณ โปรเจกต์นี้มีสองวิธีในการรัน

### วิธีที่ 1: สคริปต์เริ่มต้นเพียงคลิกเดียว (แนะนำสำหรับครั้งแรก)

โปรเจกต์มีสคริปต์เริ่มต้นเพียงคลิกเดียวที่จะติดตั้งแพ็กเกจที่จำเป็น ดาวน์โหลดโมเดล เริ่มต้นคอนเทนเนอร์ Qdrant และรันบริการ Chainlit โดยอัตโนมัติ

1. **เปิดเทอร์มินัล** และไปยังไดเรกทอรีโปรเจกต์นี้:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **มอบสิทธิ์การรันและรันสคริปต์เริ่มต้น**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **กระบวนการเริ่มต้นเบื้องต้นประกอบด้วย**:
   - `./download_models.sh`: ตรวจสอบและดาวน์โหลดโมเดลภาษา GGUF ที่ขาดหายไป
   - `./install_metal.sh`: ติดตั้ง Homebrew โดยอัตโนมัติ ตรวจสอบ Xcode CLTs และตั้งค่าสภาพแวดล้อมเสมือนของ Python (`ai_env`) ด้วย `llama-cpp-python` ที่รองรับ Metal
   - **Docker Compose**: ตรวจสอบและเริ่มต้นบริการชื่อ `cisco-foundation-sec-8b-macos-qdrant`
   - **การซิงค์ RAG อัตโนมัติ**: แอปพลิเคชันจะอ่าน `playbooks.json` และอัปเดตฐานความรู้ Qdrant โดยอัตโนมัติเมื่อเริ่มต้น
   - เริ่มต้นบริการเว็บ `main.py` หลังจากอัปเดตไลบรารีแพ็กเกจแล้ว

### วิธีที่ 2: เริ่มต้นด้วยตนเอง (แนะนำหลังจากตั้งค่าเริ่มต้น)

หากคุณรัน `run.sh` สำเร็จแล้วและดาวน์โหลดสภาพแวดล้อมรวมถึงโมเดลทั้งหมดแล้ว คุณเพียงแค่เริ่มต้นบริการด้วยตนเองต่อไปนี้:

1. **ตรวจสอบให้แน่ใจว่าบริการ Qdrant กำลังรันอยู่**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **เปิดใช้งานสภาพแวดล้อมเสมือนและเริ่ม Chainlit**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### เริ่มแชท

เมื่อบริการทำงานแล้ว เทอร์มินัลจะแสดงข้อมูลการรันในเครื่องสำหรับ Chainlit โดยปกติคุณจะสามารถเข้าถึงอินเทอร์เฟซผู้ช่วยความปลอดภัยได้โดยเปิดเบราว์เซอร์แล้วไปยัง `http://localhost:8000`

## ⚙️ การเพิ่มประสิทธิภาพการทำงาน (ขั้นสูง)

เพื่อให้ระบบอยู่ในขีดจำกัดของทรัพยากร (เช่น < 50% RAM บน 24GB Mac) คุณสามารถปรับแต่งสิ่งต่อไปนี้ใน `.env`:

*   `N_GPU_LAYERS_LLAMA3`: GPU เลเยอร์สำหรับโมเดลทั่วไป (-1 สำหรับทั้งหมด, 0 สำหรับ CPU)
*   `N_GPU_LAYERS_SEC`: GPU เลเยอร์สำหรับโมเดลความปลอดภัย
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: ขนาดบริบท (ค่าเริ่มต้น 2048) การลดค่านี้ช่วยประหยัด RAM ได้มาก

## 📊 การสังเกตการณ์และการมอนิเตอร์

ระบบติดตั้งเครื่องมือการสังเกตการณ์ระดับองค์กร:

- **Langfuse**: ติดตามการเรียก LLM ของคุณ ต้นทุน และการใช้โทเค็น
- **Arize Phoenix**: การประเมินคำตอบ RAG อัตโนมัติและการติดตาม
- **ASITOP HUD**: HUD แบบลอยตัวตามเวลาจริงสำหรับการมอนิเตอร์ GPU/CPU/RAM
- **Grafana**: แดชบอร์ดประสิทธิภาพย้อนหลัง
- **การตรวจสอบสถานะระบบ**: รัน `python health_check.py` เพื่อตรวจสอบสถานะของระบบนิเวศ Docker/ML ทั้งหมด (Qdrant, InfluxDB, Grafana, Langfuse, Phoenix)

## การแก้ไขปัญหา

- **Qdrant ไม่สามารถเริ่มทำงานได้**: ตรวจสอบว่า Docker Desktop หรือ Podman กำลังทำงานอยู่
- **ข้อผิดพลาดในการคอมไพล์ `llama-cpp-python`**: มักเกิดจากการติดตั้งเครื่องมือบรรทัดคำสั่ง Xcode ไม่ครบถ้วน ลองรัน `xcode-select --install` ด้วยตนเอง
- **หน่วยความจำไม่เพียงพอ / แครชบ่อยครั้ง**: โมเดลภาษาขนาดใหญ่ใช้ทรัพยากรระบบสูง โปรดปิดแอปพลิเคชันเบื้องหลังที่ไม่จำเป็นเพื่อสำรองหน่วยความจำรวมที่เพียงพอสำหรับการใช้งาน MLX หรือ MPS

## การพัฒนาและคุณสมบัติขั้นสูง

- **การนำเข้าข้อความ RAG**: หากต้องการนำเข้าเอกสารความปลอดภัยพื้นฐานใหม่เข้าสู่ฐานความรู้ Qdrant ให้รันสคริปต์ประมวลผลเอกสารผ่าน `ingest_security_docs.py`
- **การแปล/การประมวลผลบันทึกอัตโนมัติ**: `translate_logs.py` มีเทมเพลตสำหรับการประมวลผลบันทึกเป็นชุดหรือการทดสอบการแปลงข้ามภาษา

## 📄 ใบอนุญาต

โปรเจกต์นี้ได้รับใบอนุญาตภายใต้ **ใบอนุญาต MIT**
ดูไฟล์ [LICENSE.md](LICENSE.md) และ [LICENSE_ZH.md](LICENSE_ZH.md) สำหรับรายละเอียดเพิ่มเติม
