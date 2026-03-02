<div align="center">
  <img src="public/logo_dark.png" width="100" alt="Native AI Security Assistant Logo">

  # 🛡️ Apple Silicon के लिए नेटिव AI सुरक्षा सहायक
  
  *Cisco Foundation-Sec 8B • बहुभाषी लॉग विश्लेषण • RAG-सक्षम प्लेबुक • Metal-त्वरित*

  [![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md) [![Español](https://img.shields.io/badge/Espa%C3%B1ol-gray?style=for-the-badge)](README.es.md) [![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-gray?style=for-the-badge)](README.ko.md) [![ไทย](https://img.shields.io/badge/%E0%B9%84%E0%B8%97%E0%B8%A2-gray?style=for-the-badge)](README.th.md) [![Tiếng Việt](https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-gray?style=for-the-badge)](README.vi.md) [![हिन्दी](https://img.shields.io/badge/%E0%A4%B9%E0%A4%BF%E0%A4%A3%E0%A5%8D%E0%A4%A6%E0%A5%80-blue?style=for-the-badge)](README.hi.md)

  **प्रबंधक:** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

यह प्रोजेक्ट एक बहुभाषी (अंग्रेजी/चीनी/जापानी/स्पेनिश/कोरियाई/थाई/वियतनामी/हिंदी) सुरक्षा विश्लेषण स्मार्ट सहायक है जो macOS (Apple Silicon M-सीरीज चिप्स) पर चलता है। आधुनिक संवादात्मक इंटरफ़ेस प्रदान करने के लिए [Chainlit](https://docs.chainlit.io/) को एकीकृत करके, और कई बड़े भाषा मॉडल (LLMs) को Qdrant वेक्टर डेटाबेस के साथ जोड़कर, यह पेशेवर सुरक्षा लॉग विश्लेषण और RAG (Retrieval-Augmented Generation) अनुप्रयोगों को प्राप्त करता है।

<div align="center">
  <img src="screenshots/dev-0.0.1/AI-Cisco-Sec-8B.webp" alt="AI-Cisco-Sec-8B" width="800">
</div>

## इनके साथ निर्मित

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

## मुख्य प्रोजेक्ट घटक

1. **फ्रंटएंड इंटरफ़ेस**: संवादात्मक AI इंटरफ़ेस बनाने के लिए Chainlit (`main.py`) का उपयोग करता है, जो वास्तविक समय के टेक्स्ट स्ट्रीमिंग और चैट इतिहास का समर्थन करता है।
2. **बहुभाषी समर्थन**: **Llama-3-Taiwan-8B-Instruct** के माध्यम से इरादा वर्गीकरण, बहुभाषी समझ और अनुवाद को संभालता है। **अंग्रेजी**, **पारंपरिक चीनी**, **जापानी**, **स्पेनिश**, **कोरियाई**, **थाई**, **वियतनामी** और **हिंदी** के लिए अनुकूलित।
3. **सुरक्षा विशेषज्ञ**: **Foundation-Sec-8B** के माध्यम से गहन सिस्टम और सुरक्षा लॉग विश्लेषण करता है, जो विशेष रूप से साइबर सुरक्षा डोमेन के लिए तैयार किया गया है।
4. **हार्डवेयर त्वरण और फाइन-ट्यूनिंग**: macOS Metal (MPS) को `llama-cpp-python` के साथ एकीकृत करता है। Mac Pro/Studio (M2/M3) पर VRAM उपयोग को संतुलित करने के लिए `.env` के माध्यम से मैन्युअल **GPU लेयर ऑफलोडिंग** और **संदर्भ विंडो (KV Cache) समायोजन** का समर्थन करता है।
5. **वेक्टर पुनर्प्राप्ति (RAG)**: सुरक्षा प्लेबुक को स्टोर और पुनः प्राप्त करने के लिए **Qdrant** (Docker के माध्यम से तैनात) का उपयोग करता है। सिस्टम स्टार्टअप पर **स्वचालित RAG सिंक** की सुविधा देता है।
6. **अवलोकनीयता और अनुरेखण**: गहन ऑडिटिंग, AI प्रतिक्रिया गुणवत्ता निगरानी और सिस्टम-व्यापी **Structlog** लॉगिंग के लिए **Langfuse** और **Arize Phoenix** के साथ एकीकृत।
7. **प्रदर्शन डैशबोर्ड और फ्लोटिंग HUD**: **GraphQL सब्सक्रिप्शन** का उपयोग करके ASITOP शैली HUD (Streamlit) के माध्यम से वास्तविक समय में हार्डवेयर निगरानी। इसमें फ्लोटिंग "PerfMon" और "इतिहास" पैनल शामिल हैं।
8. **परिष्कृत UI/UX**: सभी समर्थित भाषाओं के बीच त्वरित स्विचिंग के लिए ध्वज चिह्नों के साथ शीर्ष-केंद्र भाषा चयनकर्ता।

## सिस्टम आवश्यकताएँ

- **ऑपरेटिंग सिस्टम**: macOS (Apple Silicon M1/M2/M3 अनुशंसित)
- **हार्डवेयर प्रदर्शन**: कम से कम 16GB यूनिफाइड मेमोरी की सिफारिश की जाती है (मॉडल आकार के आधार पर)
- **पूर्वापेक्षाएँ**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) या [Podman](https://podman.io/) (Qdrant तैनात करने के लिए)
  - इंटरनेट कनेक्शन (पहली बार लॉन्च पर मॉडल और लाइब्रेरी डाउनलोड करने के लिए आवश्यक)

## प्रोजेक्ट आर्किटेक्चर

```text
.
├── core/                       # मुख्य सिस्टम लॉजिक (LLM, डेटाबेस, हार्डवेयर, कॉन्फिगरेशन)
├── models/                     # GGUF मॉडल स्टोरेज (Llama-3 और Foundation-Sec)
├── qdrant_storage/             # Qdrant वेक्टर डेटाबेस के लिए स्टोरेज डायरेक्टरी
├── influxdb3_storage/          # मेट्रिक्स के लिए स्टोरेज
├── grafana_storage/            # ग्रैफाना डैशबोर्ड स्टोरेज
├── public/                     # कस्टम ब्रांडिंग एसेट्स (लोगो, CSS, थीम)
├── main.py                     # मुख्य Chainlit एप्लिकेशन प्रविष्टि बिंदु
├── streamlit_app.py            # ASITOP HUD मॉनिटरिंग इंटरफेस
├── playbooks.json              # RAG अंतर्ग्रहण के लिए केंद्रीकृत सुरक्षा SOPs/प्लेबुक
├── .env                        # पर्यावरण चर और रहस्य
├── run.sh                      # स्मार्ट निष्पादन स्क्रिप्ट (स्वचालित सेटअप)
└── (अन्य कॉन्फिग फाइलें और स्क्रिप्ट)
```

## कैसे चलाएं

आपके वातावरण सेटअप के आधार पर, प्रोजेक्ट चलाने के दो तरीके प्रदान करता है।

### तरीका 1: वन-क्लिक स्टार्टअप स्क्रिप्ट (पहली बार के लिए अनुशंसित)

प्रोजेक्ट एक वन-क्लिक स्टार्टअप स्क्रिप्ट प्रदान करता है जो स्वचालित रूप से आवश्यक पैकेज स्थापित करेगा, मॉडल डाउनलोड करेगा, Qdrant कंटेनर शुरू करेगा और Chainlit सेवा चलाएगा।

1. **टर्मिनल खोलें**, और इस प्रोजेक्ट डायरेक्टरी पर जाएं:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **निष्पादन अनुमति दें और स्टार्टअप स्क्रिप्ट चलाएँ**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **प्रारंभिक स्टार्टअप प्रक्रिया में शामिल हैं**:
   - `./download_models.sh`: लापता GGUF भाषा मॉडल की जाँच करता है और डाउनलोड करता है।
   - `./install_metal.sh`: स्वचालित रूप से Homebrew स्थापित करता है, Xcode CLTs की जाँच करता है, और Metal-समर्थित `llama-cpp-python` के साथ पायथन वर्चुअल वातावरण (`ai_env`) सेट करता है।
   - **Docker Compose**: `cisco-foundation-sec-8b-macos-qdrant` नामक सेवा की जाँच करता है और शुरू करता है।
   - **स्वचालित RAG सिंक**: एप्लिकेशन स्टार्टअप पर स्वतः `playbooks.json` को पढ़ता है और Qdrant ज्ञान आधार को अपडेट करता है।
   - पैकेज लाइब्रेरी को अपडेट करने के बाद `main.py` वेब सेवा शुरू करता है।

### तरीका 2: मैन्युअल स्टार्टअप (प्रारंभिक सेटअप के बाद अनुशंसित)

यदि आप पहले ही सफलतापूर्वक `run.sh` चला चुके हैं और सभी वातावरण और मॉडल डाउनलोड कर चुके हैं, तो आपको आगे केवल मैन्युअल रूप से सेवाएं शुरू करने की आवश्यकता है:

1. **सुनिश्चित करें कि Qdrant सेवा चल रही है**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **वर्चुअल वातावरण सक्रिय करें और Chainlit शुरू करें**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### चैट शुरू करें

सेवाएं शुरू होने के बाद, टर्मिनल Chainlit के लिए स्थानीय निष्पादन जानकारी प्रदर्शित करेगा। आमतौर पर, आप अपने ब्राउज़र को खोलकर और `http://localhost:8000` पर जाकर सुरक्षा सहायक इंटरफ़ेस तक पहुँच सकते हैं।

## ⚙️ प्रदर्शन अनुकूलन (उन्नत)

यह सुनिश्चित करने के लिए कि सिस्टम संसाधन सीमाओं के भीतर रहे (उदाहरण के लिए, 24GB मैक पर < 50% RAM), आप अपने `.env` में निम्नलिखित को फाइन-ट्यून कर सकते हैं:

*   `N_GPU_LAYERS_LLAMA3`: सामान्य मॉडल के लिए GPU लेयर्स (सभी के लिए -1, CPU के लिए 0)।
*   `N_GPU_LAYERS_SEC`: सुरक्षा मॉडल के लिए GPU लेयर्स।
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: संदर्भ आकार (डिफ़ॉल्ट 2048)। इसे कम करने से काफी RAM बचती है।

## 📊 अवलोकनीयता और निगरानी

सिस्टम एंटरप्राइज-ग्रेड अवलोकनीयता टूल से लैस है:

- **Langfuse**: अपने LLM कॉल, लागत और टोकन उपयोग को ट्रेस करें।
- **Arize Phoenix**: RAG प्रतिक्रियाओं का स्वचालित मूल्यांकन और अनुरेขण।
- **ASITOP HUD**: GPU/CPU/RAM निगरानी के लिए वास्तविक समय HUD।
- **Grafana**: ऐतिहासिक प्रदर्शन डैशबोर्ड।

## समस्या निवारण

- **Qdrant शुरू होने में विफल**: सुनिश्चित करें कि Docker Desktop या Podman वर्तमान में चल रहा है।
- **`llama-cpp-python` संकलन त्रुटियाँ**: आमतौर पर Xcode कमांड लाइन टूल्स की अधूरी स्थापना के कारण होती हैं। मैन्युअल रूप से `xcode-select --install` चलाने का प्रयास करें।
- **मेमोरी की कमी / बार-बार क्रैश**: बड़े भाषा मॉडल महत्वपूर्ण सिस्टम संसाधनों का उपभोग करते हैं। MLX या MPS उपयोग के लिए पर्याप्त यूनिफाइड मेमोरी आरक्षित करने के लिए कृपया अनावश्यक बैकग्राउंड एप्लिकेशन बंद करें।

## विकास और उन्नत सुविधाएँ

- **RAG टेक्स्ट इनजेशन**: Qdrant ज्ञान आधार में नए सुरक्षा दस्तावेजों को आयात करने के लिए, `ingest_security_docs.py` के माध्यम से दस्तावेज़ प्रसंस्करण स्क्रिप्ट निष्पादित करें।
- **स्वचालित लॉग अनुवाद/प्रसंस्करण**: `translate_logs.py` लॉग को बैच में संसाधित करने या क्रॉस-भाषा रूपांतरण परीक्षण करने के लिए एक टेम्पलेट प्रदान करता है।

## 📄 लाइसेंस

यह प्रोजेक्ट **MIT लाइसेंस** के तहत लाइसेंस प्राप्त है।
विवरण के लिए [LICENSE.md](LICENSE.md) और [LICENSE_ZH.md](LICENSE_ZH.md) फाइलें देखें।
