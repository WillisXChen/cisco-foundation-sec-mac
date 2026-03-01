<div align="center">
  <img src="public/logo_dark.png" width="100" alt="Asistente de Seguridad de IA Nativa Logo">

  # 🛡️ Asistente de Seguridad de IA Nativa para Apple Silicon
  
  *Cisco Foundation-Sec 8B • Análisis de Registros Bilingüe • Libros de Jugadas habilitados para RAG • Acelerado por Metal*

  [![English](https://img.shields.io/badge/English-gray?style=for-the-badge)](README.md) [![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-gray?style=for-the-badge)](README.中文.md) [![日本語](https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-gray?style=for-the-badge)](README.ja.md) [![Español](https://img.shields.io/badge/Espa%C3%B1ol-blue?style=for-the-badge)](README.es.md) [![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-gray?style=for-the-badge)](README.ko.md) [![ไทย](https://img.shields.io/badge/%E0%B9%84%E0%B8%97%E0%B8%A2-gray?style=for-the-badge)](README.th.md) [![Tiếng Việt](https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-gray?style=for-the-badge)](README.vi.md) [![हिन्दी](https://img.shields.io/badge/%E0%A4%B9%E0%A4%BF%E0%A4%A3%E0%A5%8D%E0%A4%A6%E0%A5%80-gray?style=for-the-badge)](README.hi.md)

  **Mantenedor:** [Willis Chen](mailto:misweyu2007@gmail.com)
</div>

---

Este proyecto es un asistente inteligente de análisis de seguridad multilingüe (inglés/chino/japonés/español/español/coreano/tailandés/vietnamita/hindi) que se ejecuta en macOS (chips Apple Silicon serie M). Al integrar [Chainlit](https://docs.chainlit.io/) para brindar una interfaz interactiva moderna y combinar múltiples modelos de lenguaje grandes (LLM) con la base de datos vectorial Qdrant, logra un análisis de registros de seguridad profesional y aplicaciones RAG (Retrieval-Augmented Generation).

## Construido con

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

## Componentes principales del proyecto

1. **Interfaz Frontend**: Utiliza Chainlit (`main.py`) para construir una interfaz de IA conversacional, que admite transmisión de texto en tiempo real e historial de chat.
2. **Soporte multilingüe**: Maneja la clasificación de intenciones, la comprensión multilingüe y la traducción a través de **Llama-3-Taiwan-8B-Instruct**. Optimizado para **inglés**, **chino tradicional**, **japonés**, **español**, **coreano**, **tailandés**, **vietnamita** e **hindi**.
3. **Experto en seguridad**: realiza un análisis profundo del sistema y de los registros de seguridad a través de **Foundation-Sec-8B**, ajustado específicamente para el dominio de la ciberseguridad.
4. **Aceleración y ajuste de hardware**: integra macOS Metal (MPS) con `llama-cpp-python`. Admite la **descarga manual de capas de GPU** y el **ajuste de la ventana de contexto (KV Cache)** a través de `.env` para equilibrar el uso de VRAM en Mac Pro/Studio (M2/M3).
5. **Recuperación de vectores (RAG)**: utiliza **Qdrant** (implementado a través de Docker) para almacenar y recuperar libros de jugadas de seguridad. El sistema presenta **sincronización automática de RAG** al iniciarse.
6. **Observabilidad y seguimiento**: integrado con **Langfuse** y **Arize Phoenix** para auditoría profunda de seguimiento, monitoreo de la calidad de respuesta de la IA y registro de **Structlog** en todo el sistema.
7. **Panel de rendimiento y HUD flotante**: monitoreo de hardware en tiempo real a través de HUD estilo ASITOP (Streamlit) utilizando **suscripciones GraphQL**. Incluye paneles flotantes "PerfMon" e "Historial".
8. **UI/UX refinada**: Selector de idioma superior central persistente con iconos de banderas para un cambio rápido entre todos los idiomas admitidos.

## Requisitos del sistema

- **Sistem Operativo**: macOS (Apple Silicon M1/M2/M3 recomendado)
- **Rendimiento de Hardware**: Se recomienda al menos 16 GB de memoria unificada (dependiendo del tamaño del modelo)
- **Requisitos previos**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) o [Podman](https://podman.io/) (para implementar Qdrant)
  - Conexión a Internet (requerida para descargar modelos y dependencias en el primer inicio)

## Arquitectura del proyecto

```text
.
├── core/                       # Lógica central del sistema (LLM, Base de datos, Hardware, Configuración)
├── models/                     # Almacenamiento de modelos GGUF (Llama-3 y Foundation-Sec)
├── qdrant_storage/             # Directorio de almacenamiento persistente para la base de datos vectorial Qdrant
├── influxdb3_storage/          # Almacenamiento persistente para métricas
├── grafana_storage/            # Almacenamiento del tablero de Grafana
├── public/                     # Activos de marca personalizados (logotipos, CSS, temas)
├── main.py                     # Punto de entrada principal de la aplicación Chainlit
├── streamlit_app.py            # Interfaz de monitoreo HUD ASITOP
├── playbooks.json              # SOP de seguridad centralizados/Libros de jugadas para la ingesta de RAG
├── .env                        # Variables de entorno y secretos
├── run.sh                      # Script de ejecución inteligente (automatiza la configuración)
└── (Otros archivos de configuración y scripts)
```

## Cómo ejecutar

Dependiendo de la configuración de su entorno, el proyecto ofrece dos formas de ejecución.

### Método 1: Script de inicio con un clic (recomendado para la primera vez)

El proyecto proporciona un script de inicio de un solo clic que instalará automáticamente los paquetes necesarios, descargará modelos, iniciará el contenedor Qdrant y ejecutará el servicio Chainlit.

1. **Abra la Terminal** y navegue hasta este directorio de proyecto:
   ```bash
   cd /path/to/cisco-foundation-sec-8b-macos
   ```

2. **Otorgue permisos de ejecución y ejecute el script de inicio**:
   ```bash
   chmod +x *.sh
   ./run.sh
   ```

3. **El proceso de inicio inicial incluye**:
   - `./download_models.sh`: Busca y descarga los modelos de lenguaje GGUF que falten.
   - `./install_metal.sh`: Instala automáticamente Homebrew, verifica los CLT de Xcode y configura el entorno virtual de Python (`ai_env`) con `llama-cpp-python` compatible con Metal.
   - **Docker Compose**: Busca e inicia el servicio llamado `cisco-foundation-sec-8b-macos-qdrant`.
   - **Sincronización automática de RAG**: La aplicación lee automáticamente `playbooks.json` y actualiza la base de conocimientos Qdrant al inicio.
   - Inicia el servicio web `main.py` después de actualizar las dependencias del paquete.

### Método 2: Inicio manual (recomendado después de la configuración inicial)

Si ya ejecutó con éxito `run.sh` y descargó todos los entornos y modelos, solo necesita iniciar manualmente los servicios de ahora en adelante:

1. **Asegúrese de que el servicio Qdrant se esté ejecutando**:
   ```bash
   docker compose up -d cisco-foundation-sec-8b-macos-qdrant
   ```

2. **Active el entorno virtual e inicie Chainlit**:
   ```bash
   source ai_env/bin/activate
   chainlit run ./main.py -w
   ```

### Empezar a chatear

Una vez que los servicios estén activos, la terminal mostrará la información de ejecución local para Chainlit. Por lo general, puede acceder a la interfaz del asistente de seguridad abriendo su navegador y navegando a `http://localhost:8000`.

## ⚙️ Optimización del rendimiento (avanzado)

Para garantizar que el sistema se mantenga dentro de los límites de recursos (por ejemplo, < 50% de RAM en una Mac de 24 GB), puede ajustar lo siguiente en su `.env`:

*   `N_GPU_LAYERS_LLAMA3`: Capas de GPU para el modelo general (-1 para todas, 0 para CPU).
*   `N_GPU_LAYERS_SEC`: Capas de GPU para el modelo de seguridad.
*   `N_CTX_LLAMA3` / `N_CTX_SEC`: Tamaño del contexto (predeterminado 2048). Reducir esto ahorra RAM significativa.

## 📊 Observabilidad y Monitoreo

El sistema está equipado con herramientas de observabilidad de nivel empresarial:

- **Langfuse**: Realice un seguimiento de sus llamadas de LLM, costos y uso de tokens.
- **Arize Phoenix**: Evaluación automática de respuestas RAG y seguimiento.
- **ASITOP HUD**: HUD flotante en tiempo real para monitoreo de GPU/CPU/RAM.
- **Grafana**: Tableros de rendimiento histórico.

## Solución de problemas

- **Qdrant no se inicia**: Asegúrese de que Docker Desktop o Podman se estén ejecutando actualmente.
- **Errores de compilación de `llama-cpp-python`**: Generalmente causados por una instalación incompleta de las herramientas de línea de comandos de Xcode. Intente ejecutar `xcode-select --install` manualmente.
- **Sin memoria / Fallos frecuentes**: Los modelos de lenguaje grandes consumen importantes recursos del sistema. Cierre las aplicaciones en segundo plano innecesarias para reservar suficiente memoria unificada para el uso de MLX o MPS.

## Desarrollo y características avanzadas

- **Ingesta de texto RAG**: para importar nuevos documentos de seguridad base a la base de conocimientos Qdrant, ejecute el script de procesamiento de documentos a través de `ingest_security_docs.py`.
- **Procesamiento/Traducción automática de registros**: `translate_logs.py` proporciona una plantilla para registros de procesamiento por lotes o la realización de pruebas de conversión entre idiomas.

## 📄 Licencia

Este proyecto tiene la licencia **MIT License**.
Consulte los archivos [LICENSE.md](LICENSE.md) y [LICENSE_ZH.md](LICENSE_ZH.md) para obtener más detalles.
