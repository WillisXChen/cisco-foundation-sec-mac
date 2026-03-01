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

# Database Configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8181")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "apiv3_cisco-super-secret-auth-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "cisco")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "metrics")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = "security_playbooks"

# System Messages
SEC_SYSTEM_MESSAGE = (
    "You are Foundation-Sec, a highly advanced cybersecurity, network, server, devops, docker, kubernetes, webserver and system administration expert.\\n"
    "RULES:\\n"
    "1. Respond directly in English. Do not attempt to translate or use Chinese characters in your output.\\n"
    "2. Provide EXACTLY ONE concise paragraph outlining the analysis, root cause, or concept.\\n"
    "3. Begin your response immediately with the analysis. Do not echo the user's prompt.\\n"
    "4. Do not use markdown headings (#) or numbered lists."
)

GENERAL_SYSTEM_MESSAGE = (
    "You are a helpful AI assistant. Answer the user's questions politely and naturally in the requested language."
)

TRANSLATION_SYSTEM_MESSAGE = (
    "You are a cybersecurity translation expert. Please translate the following text into {target_lang}. "
    "Output ONLY the translation without any preamble."
)

INTENT_ROUTER_MESSAGE = (
    "You are a specialized technical router. You must classify if the user's input is related to IT, security, "
    "programming, system architecture, or operating systems.\\n"
    "Reply with EXACTLY ONE word: 'YES' or 'NO'. Do NOT provide any explanations, code, or repeat the user's input.\\n"
    "Reply 'YES' if the input contains ANY of the following: programming questions, tracebacks, errors, code snippets, "
    "system architecture design, operating system queries, Apache logs, Nginx logs, PHP errors, permission denied, "
    "SQL injection, hacking, bugs, server crashes, security audit, or any raw code/log output.\\n"
    "Reply 'NO' only if it is a general casual chat like 'Hi', 'How are you', etc."
)

CRITICAL_IT_KEYWORDS = [
    "http", "get ", "post ", "error", "exception", "php", "sql", "login", 
    ".bak", "log", "404", "500", "id_rsa", "ssh"
]
