import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# System Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
PLAYBOOKS_PATH = os.path.join(BASE_DIR, "playbooks.json")

# LLM Configuration
MODEL_SEC_PATH = os.getenv("MODEL_SEC_PATH", os.path.join(MODELS_DIR, "foundation-sec-8b-q4_k_m.gguf"))
MODEL_LLAMA3_PATH = os.getenv("MODEL_LLAMA3_PATH", os.path.join(MODELS_DIR, "llama-3-taiwan-8b-instruct-q4_k_m.gguf"))

# GPU Layer Configuration (For model loading optimization)
# Default to -1 for Metal (full offload) unless overridden
N_GPU_LAYERS_LLAMA3 = int(os.getenv("N_GPU_LAYERS_LLAMA3", "-1"))
N_GPU_LAYERS_SEC = int(os.getenv("N_GPU_LAYERS_SEC", "-1"))

# Context Size (KV Cache) - Higher values use more RAM
# 2048 is recommended to keep RAM usage under 12GB for two 8B models
N_CTX_LLAMA3 = int(os.getenv("N_CTX_LLAMA3", "2048"))
N_CTX_SEC = int(os.getenv("N_CTX_SEC", "2048"))

# Database Configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8181")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "apiv3_cisco-super-secret-auth-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "cisco")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "metrics")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = "security_playbooks"

# System Messages
SEC_SYSTEM_MESSAGE = (
    "You are Foundation-Sec, a world-class cybersecurity expert. "
    "Provide CONCISE technical analysis and advice.\\n\\n"
    "GUIDELINES:\\n"
    "1. Respond in English only.\\n"
    "2. **BREVITY IS KEY**. Use minimal tokens.\\n"
    "3. Structure:\\n"
    "   - **Summary**: 1-2 sentence overview.\\n"
    "   - **RCA**: Top 2-3 technical root causes (bullets).\\n"
    "   - **Mitigation**: Top 2-3 critical action items (bullets)."
)

GENERAL_SYSTEM_MESSAGE = (
    "You are a helpful AI assistant. Answer the user's questions politely and naturally in the requested language."
)

TRANSLATION_SYSTEM_MESSAGE = (
    "You are a cybersecurity translation expert. Please translate the following text into {target_lang}. "
    "Output ONLY the translation without any preamble."
)

INTENT_ROUTER_MESSAGE = (
    "You are a specialized technical router. Your task is to determine if the user's input is a technical request "
    "related to security, IT infrastructure, programming, or system administration.\\n\\n"
    "Reply with EXACTLY ONE word: 'YES' or 'NO'.\\n\\n"
    "Reply 'YES' if the input is about:\\n"
    "- Security vulnerabilities (SQLi, XSS, Prompt Injection, etc.)\\n"
    "- Server logs, errors, or system configuration\\n"
    "- Coding, debugging, or technical architecture\\n"
    "- DevOps, Docker, Kubernetes, or Networking queries\\n\\n"
    "Reply 'NO' if it is general conversation, greetings, or non-technical topics."
)

CRITICAL_IT_KEYWORDS = [
    "http", "get ", "post ", "error", "exception", "php", "sql", "login", 
    ".bak", "log", "404", "500", "id_rsa", "ssh", "injection", "attack"
]
