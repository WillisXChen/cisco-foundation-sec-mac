import asyncio
import time
import typing
import engineio
engineio.payload.Payload.max_decode_packets = 500000

import chainlit as cl
import os
import json

# Ensure internal files directory exists to prevent Chainlit plotting issues
os.makedirs(".files", exist_ok=True)

import psutil
import subprocess
import re
import platform
import pandas as pd
import plotly.graph_objects as go
import strawberry
from strawberry.fastapi import GraphQLRouter
from chainlit.server import app as fastapi_app
from collections import deque
from llama_cpp import Llama
from qdrant_client import QdrantClient
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8181")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "apiv3_cisco-super-secret-auth-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "cisco")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "metrics")

# --- Hardware Monitoring Utils ---
def get_macos_hw_stats():
    """Collect all hardware metrics: CPU, GPU, RAM, power. No sudo required."""
    stats = {
        "e_cpu_pct": 0.0, "p_cpu_pct": 0.0,
        "gpu_pct": 0, "gpu_cores": ST_GPU_CORES,
        "ram_pct": 0.0, "ram_used_gb": 0.0, "ram_total_gb": ST_RAM_TOTAL,
        "e_cores": ST_E_CORES, "p_cores": ST_P_CORES,
        "cpu_power_w": -1, "gpu_power_w": -1, "total_power_w": -1,
        "chip_label": ST_CHIP_LABEL
    }
    try:
        percpu = psutil.cpu_percent(percpu=True)
        stats["e_cpu_pct"] = sum(percpu[:ST_E_CORES]) / ST_E_CORES if ST_E_CORES > 0 else sum(percpu) / len(percpu)
        stats["p_cpu_pct"] = sum(percpu[ST_E_CORES:]) / ST_P_CORES if ST_P_CORES > 0 else stats["e_cpu_pct"]

        mem = psutil.virtual_memory()
        stats["ram_pct"] = mem.percent
        stats["ram_used_gb"] = mem.used / (1024**3)
    except Exception:
        pass

    # Try ASITOP style powermetrics first (requires sudo)
    try:
        import plistlib
        pm_res = subprocess.check_output(
            ['sudo', '-n', 'powermetrics', '-n', '1', '-i', '50', '--samplers', 'cpu_power,gpu_power', '-f', 'plist'],
            stderr=subprocess.DEVNULL, timeout=2
        )
        plist_data = plistlib.loads(pm_res)
        proc_data = plist_data.get('processor', {})
        if 'cpu_energy' in proc_data:
            stats["cpu_power_w"] = round(proc_data['cpu_energy'] / 1000.0, 2)
        if 'gpu_energy' in proc_data:
            stats["gpu_power_w"] = round(proc_data['gpu_energy'] / 1000.0, 2)
        if 'combined_power' in proc_data:
            stats["total_power_w"] = round(proc_data['combined_power'] / 1000.0, 2)
        elif 'processor_energy' in proc_data:
            stats["total_power_w"] = round(proc_data['processor_energy'] / 1000.0, 2)
        elif stats["cpu_power_w"] != -1 and stats["gpu_power_w"] != -1:
            ane_power_w = proc_data.get('ane_energy', 0) / 1000.0
            stats["total_power_w"] = round(stats["cpu_power_w"] + stats["gpu_power_w"] + ane_power_w, 2)
    except Exception:
        pass

    try:
        # GPU utilization via ioreg (no sudo)
        ioreg_res = subprocess.check_output(['ioreg', '-r', '-d', '1', '-c', 'IOAccelerator'],
                                            stderr=subprocess.DEVNULL, timeout=2).decode()
        m = re.search(r'"Device Utilization %"=(\d+)', ioreg_res)
        if m:
            stats["gpu_pct"] = int(m.group(1))
        # Try GPU power from PerformanceStatistics
        m_gpow = re.search(r'"GPU Power"[\s:=]+(\d+\.?\d*)', ioreg_res)
        if m_gpow:
            stats["gpu_power_w"] = float(m_gpow.group(1)) / 1000.0
    except Exception:
        pass
    try:
        # CPU/total power estimate via battery discharge rate (works on MacBooks, no sudo)
        bat = psutil.sensors_battery()
        if bat and not bat.power_plugged:
            # Discharge rate isn't directly available via psutil on macOS easily
            pass
        # Try ioreg AppleSmartBattery for live power
        bat_res = subprocess.check_output(
            ['ioreg', '-r', '-d', '1', '-c', 'AppleSmartBattery'],
            stderr=subprocess.DEVNULL, timeout=2).decode()
        current_m  = re.search(r'"InstantAmperage"=(\d+)', bat_res)
        voltage_m  = re.search(r'"Voltage"=(\d+)', bat_res)
        if current_m and voltage_m:
            amps = int(current_m.group(1))
            # InstantAmperage can be unsigned; treat >0x7fffffff as negative (discharge)
            if amps > 0x7FFFFFFF:
                amps = -(0x100000000 - amps)
            if amps < 0:  # discharging = consuming power
                volts = int(voltage_m.group(1)) / 1000.0  # mV -> V
                total_w = abs(amps) * volts / 1000.0  # mA * V / 1000
                stats["total_power_w"] = round(total_w, 2)
    except Exception:
        pass
    return stats

def get_macos_gpu_info():
    """Get GPU core count (used at startup only)."""
    gpu_cores = "N/A"
    if platform.system() != "Darwin":
        return gpu_cores
    try:
        sp = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'],
                                     stderr=subprocess.DEVNULL, timeout=5).decode()
        for line in sp.split('\n'):
            if 'Total Number of Cores' in line:
                gpu_cores = line.strip().split(':')[-1].strip()
                break
    except Exception:
        pass
    return gpu_cores

def get_chip_label():
    """Get Apple chip label (M1/M2/M3...) from system_profiler."""
    try:
        res = subprocess.check_output(['system_profiler', 'SPHardwareDataType'],
                                      stderr=subprocess.DEVNULL, timeout=5).decode()
        for line in res.split('\n'):
            # Match "  Chip: Apple M2" or "  Apple M2" style lines
            if 'Chip:' in line or 'chip:' in line:
                return line.strip().split(':', 1)[-1].strip()
        # Fallback: look for Apple M in any line
        for line in res.split('\n'):
            if 'Apple M' in line:
                # Extract "Apple M2" or similar
                import re as _re
                m = _re.search(r'Apple M\d+\s*\w*', line)
                if m:
                    return m.group(0).strip()
    except Exception:
        pass
    return "Apple M-Series"

# Pre-calculate steady core stats (only once at startup)
ST_CPU_COUNT = psutil.cpu_count()
ST_E_CORES = 4 if ST_CPU_COUNT >= 8 else 0
ST_P_CORES = ST_CPU_COUNT - ST_E_CORES
ST_RAM_TOTAL = round(psutil.virtual_memory().total / (1024**3), 2)
ST_GPU_CORES = get_macos_gpu_info()
ST_CHIP_LABEL = get_chip_label()

# === psutil warmup ===
# cpu_percent() ALWAYS returns 0.0 on the very first call (it needs an interval baseline)
# Call it once now to initialise the internal counter so all subsequent calls return real data.
psutil.cpu_percent(percpu=True)  # discard the zeroed result

# Shared latest stats dict (written by monitor task)
_latest_hw_stats = get_macos_hw_stats()

import sys
if __name__ not in sys.modules:
    sys.modules[__name__] = sys.modules['__main__']

# === GraphQL Real-time Endpoint ===
@strawberry.type
class HWStats:
    e_cpu_pct: float
    p_cpu_pct: float
    gpu_pct: int
    ram_pct: float
    ram_used_gb: float
    ram_total_gb: float
    e_cores: int
    p_cores: int
    gpu_cores: str
    cpu_power_w: float
    gpu_power_w: float
    total_power_w: float
    chip_label: str

@strawberry.type
class Query:
    @strawberry.field
    def current_stats(self) -> HWStats:
        return HWStats(**_latest_hw_stats)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def watch_stats(self) -> typing.AsyncGenerator[HWStats, None]:
        """Real-time subscription that yields hardware stats every 2 seconds."""
        while True:
            yield HWStats(**_latest_hw_stats)
            await asyncio.sleep(2)


schema = strawberry.Schema(query=Query, subscription=Subscription)
graphql_app = GraphQLRouter(schema)
fastapi_app.include_router(graphql_app, prefix="/graphql")

# History for charts (kept server-side for the monitor task text update)
MAX_HISTORY = 30
history_ecpu = deque([0]*MAX_HISTORY, maxlen=MAX_HISTORY)
history_pcpu = deque([0]*MAX_HISTORY, maxlen=MAX_HISTORY)
history_gpu = deque([0]*MAX_HISTORY, maxlen=MAX_HISTORY)
history_ram = deque([0]*MAX_HISTORY, maxlen=MAX_HISTORY)

async def hardware_monitor_task():
    """Background task: update global stats dict for GraphQL every 2s, and write to InfluxDB."""
    global _latest_hw_stats
    
    # Initialize InfluxDB Client
    try:
        influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    except Exception as e:
        print(f"InfluxDB Connection error: {e}")
        write_api = None

    while True:
        try:
            stats = await asyncio.to_thread(get_macos_hw_stats)
            _latest_hw_stats = stats
            
            if write_api:
                # Create a Point and write to InfluxDB
                p = Point("hardware_monitor") \
                    .tag("host", "mac_server") \
                    .tag("chip", stats["chip_label"]) \
                    .field("e_cpu_pct", float(stats.get("e_cpu_pct", 0))) \
                    .field("p_cpu_pct", float(stats.get("p_cpu_pct", 0))) \
                    .field("gpu_pct", float(stats.get("gpu_pct", 0))) \
                    .field("ram_pct", float(stats.get("ram_pct", 0))) \
                    .field("ram_used_gb", float(stats.get("ram_used_gb", 0))) \
                    .field("cpu_power_w", float(stats.get("cpu_power_w", 0))) \
                    .field("gpu_power_w", float(stats.get("gpu_power_w", 0))) \
                    .field("total_power_w", float(stats.get("total_power_w", 0)))
                # Await writing to avoid blocking event loop
                await asyncio.to_thread(write_api.write, bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=p)

        except Exception as e:
            print(f"Monitor error: {e}")
        await asyncio.sleep(2)

# === Configuration ===
# Set default model paths, can be overridden via environment variables
MODEL_SEC_PATH = os.getenv("MODEL_SEC_PATH", "./models/foundation-sec-8b-q4_k_m.gguf")
MODEL_LLAMA3_PATH = os.getenv("MODEL_LLAMA3_PATH", "./models/llama-3-taiwan-8b-instruct-q4_k_m.gguf")

# === Global instances ===
# Load models only once at startup to avoid memory and time overhead on every connection
llm_llama3 = None
llm_sec = None
qdrant_client = None

# === System Messages ===
sec_system_message = (
    "You are Foundation-Sec, a highly advanced cybersecurity, network, server , devops , docker , kubernetes , webserver and system administration expert.\n"
    "RULES:\n"
    "1. Respond directly in English. Do not attempt to translate or use Chinese characters in your output.\n"
    "2. Provide EXACTLY ONE concise paragraph outlining the analysis, root cause, or concept.\n"
    "3. Begin your response immediately with the analysis. Do not echo the user's prompt.\n"
    "4. Do not use markdown headings (#) or numbered lists."
)

general_system_message = (
    "You are a helpful AI assistant. Answer the user's questions politely and naturally in Traditional Chinese."
)

def load_model(model_path: str, context_size: int = 4096):
    """
    Load a Llama-3 based model using llama.cpp with Metal (MPS) support.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    print(f"Loading model from {model_path}...")
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=-1,      # Metal (GPU) Acceleration on Mac
        seed=1337,            
        n_ctx=context_size,   
        verbose=False,        
        chat_format="llama-3" 
    )
    return llm

@cl.on_chat_start
async def on_chat_start():
    global llm_llama3, llm_sec, qdrant_client
    
    # 1. Initialize Top-Bar HUD with iframe (sent ONCE, Streamlit handles its own refresh inside the iframe)
    content = (
        f"### 🚀 ASITOP HUD `{ST_CHIP_LABEL}`\n"
        f"<iframe src='http://localhost:8501/?embed=true' width='100%' height='320' frameborder='0' style='border-radius: 8px; border: 1px solid rgba(0, 255, 255, 0.4); background: #0d1117;'></iframe>\n"
    )
    
    actions = [
        cl.Action(name="view_hw_history", payload={"action": "show"}, description="查看歷史硬體資源與電力消耗數據")
    ]
    stats_msg = cl.Message(content=content, author="H/W Monitor", actions=actions)
    await stats_msg.send()
    
    # 2. Start background task to fetch metrics for GraphQL
    asyncio.create_task(hardware_monitor_task())

    loading_msg = cl.Message(content="### ⚙️ 系統初始化中... 正在載入 AI 模型，請稍候。")
    await loading_msg.send()

    try:
        # Use asyncio.to_thread() to offload synchronous load_model to Thread Pool,
        # preventing event loop blockage, allowing Chainlit to refresh UI status in real-time.
        if llm_llama3 is None:
            loading_msg.content = "### ⚙️ 載入中 (1/4)：正在載入 Llama3-Taiwan 模型..."
            await loading_msg.update()
            llm_llama3 = await asyncio.to_thread(load_model, MODEL_LLAMA3_PATH)

        if llm_sec is None:
            loading_msg.content = "### ⚙️ 載入中 (2/4)：正在載入 Foundation-Sec 資安模型..."
            await loading_msg.update()
            llm_sec = await asyncio.to_thread(load_model, MODEL_SEC_PATH)

        if qdrant_client is None:
            loading_msg.content = "### ⚙️ 載入中 (3/4)：正在連線 Qdrant 向量資料庫..."
            await loading_msg.update()
            print("Connecting to Qdrant instance...")
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            qdrant_client = QdrantClient(url=qdrant_url)
            print("Setting up embedding model...")
            await asyncio.to_thread(qdrant_client.set_model, "BAAI/bge-small-en-v1.5")

        # Automatically ingest playbooks from playbooks.json if collection is empty
        loading_msg.content = "### ⚙️ 載入中 (4/4)：正在同步資安 SOP 知識庫..."
        await loading_msg.update()
        
        collection_name = "security_playbooks"
        
        # Check if collection exists to avoid 409 Conflict (Collection already exists)
        # We use a synchronous check within to_thread or check list_collections
        collections = await asyncio.to_thread(qdrant_client.get_collections)
        exists = any(c.name == collection_name for c in collections.collections)
        
        if not exists:
            playbooks_path = os.path.join(os.path.dirname(__file__), "playbooks.json")
            if os.path.exists(playbooks_path):
                with open(playbooks_path, "r", encoding="utf-8") as f:
                    docs_data = json.load(f)
                    docs = [d["content"] for d in docs_data]
                    metadatas = [{"title": d["title"]} for d in docs_data]
                    ids = [d["id"] for d in docs_data]
                    await asyncio.to_thread(
                        qdrant_client.add,
                        collection_name=collection_name,
                        documents=docs,
                        metadata=metadatas,
                        ids=ids
                    )

        loading_msg.content = "### ✅ 模型載入完成！\n\n🛡️ **歡迎使用 Foundation-Sec-8B Security Assistant!** 🛡️\n\n您可以開始輸入有關資安、程式設計或一般問題。"
        await loading_msg.update()

    except Exception as e:
        loading_msg.content = f"### ❌ 模型載入失敗\n錯誤訊息: `{e}`\n請確認模型路徑是否正確 (預設路徑 `./models/...`)。"
        await loading_msg.update()
        return

    # Initialize chat history for this user session
    cl.user_session.set("chat_history", [])

@cl.on_message
async def main(message: cl.Message):
    global llm_llama3, llm_sec, qdrant_client
    
    if llm_llama3 is None or llm_sec is None or qdrant_client is None:
        await cl.Message(content="⚠️ 模型尚未載入完成，請重整頁面或確認終端機錯誤訊息。").send()
        return

    user_input = message.content.strip()
    chat_history = cl.user_session.get("chat_history", [])

    # === Intent Classification with Llama3 ===
    classification_messages = [
        {
            "role": "system",
            "content": "You are a specialized technical router. You must classify if the user's input is related to IT, security, programming, system architecture, or operating systems.\n"
                       "Reply with EXACTLY ONE word: 'YES' or 'NO'. Do NOT provide any explanations, code, or repeat the user's input.\n"
                       "Reply 'YES' if the input contains ANY of the following: programming questions, tracebacks, errors, code snippets, system architecture design, operating system queries, Apache logs, Nginx logs, PHP errors, permission denied, SQL injection, hacking, bugs, server crashes, security audit, or any raw code/log output.\n"
                       "Reply 'NO' only if it is a general casual chat like 'Hi', 'How are you', etc."
        }
    ]

    # Only determine intent based on current question to prevent Llama 3 classifier confusion over long history context
    classification_messages.append({"role": "user", "content": user_input})

    is_security = False
    
    # Fallback keyword safety net, preventing small models from failing to classify stark logs
    critical_it_keywords = ["http", "get ", "post ", "error", "exception", "php", "sql", "login", ".bak", "log", "404", "500", "id_rsa", "ssh"]
    user_input_lower = user_input.lower()
    
    # If Llama3 misjudged but contents are ostensibly IT/Log related, force assign to security intent
    if any(keyword in user_input_lower for keyword in critical_it_keywords):
        is_security = True
        print("[DEBUG] Intent forced to YES by Keyword Matching")
    else:
        try:
            res = llm_llama3.create_chat_completion(
                messages=classification_messages,
                max_tokens=2,
                temperature=0.0
            )
            intent_text = res["choices"][0]["message"]["content"].strip().upper()
            intent_usage = res.get("usage", {})
            print(f"[DEBUG] Intent Classification = {intent_text} | Tokens: {intent_usage}")
            is_security = "YES" in intent_text
        except Exception as e:
            print(f"[Classification Error]: {e}")
            is_security = False

    # Choose model to use based on classification result
    active_llm = llm_sec if is_security else llm_llama3
    active_name = "Foundation-Sec" if is_security else "Llama3-Taiwan"
    active_system_msg = sec_system_message if is_security else general_system_message

    # === Main Generation ===
    chat_messages = [{"role": "system", "content": active_system_msg}]
    
    # Prepend chat history for context memory regardless of general or security question
    for msg in chat_history:
        chat_messages.append(msg)

    if not is_security:
        chat_messages.append({"role": "user", "content": user_input})
    else:
        # === Qdrant RAG Context Retrieval ===
        context_str = ""
        try:
            search_result = qdrant_client.query(
                collection_name="security_playbooks",
                query_text=user_input,
                limit=1
            )
            if search_result:
                best_match = search_result[0]
                print(f"[RAG] Found context: {best_match.metadata.get('title')} (score: {best_match.score:.2f})")
                context_str = f"[Internal System Context]\n{best_match.document}\n\n"
        except Exception as e:
            print(f"[RAG Error] {e}")

        # Enforce English-only output for security questions implicitly without overly heavy threatening tones, preventing hallucinations from the 8B model
        enforced_input = f"{context_str}{user_input}\n\n[Action: Please analyze the above input and respond in English only. Base your answer on the Internal System Context if it is relevant.]"
        chat_messages.append({"role": "user", "content": enforced_input})

    # Output visible prefix badge so users know which model generated responses
    model_badge = f"### 🧠 由 `{active_name}` 生成回應\n---\n"
    
    # Send empty Message first (triggering UI loading animation), then we stream out progressively
    response_msg = cl.Message(content=model_badge, author=active_name)
    await response_msg.send()

    assistant_response = ""
    
    try:
        stream = active_llm.create_chat_completion(
            messages=chat_messages,
            stream=True,         
            temperature=0.4 if is_security else 0.2,  # Boost natural variation rate as an alternative to harsh penalties
            top_p=0.9,
            repeat_penalty=1.05 if is_security else 1.0, # Drop to bottom baseline to prevent logit collapse into gibberish
            frequency_penalty=0.0, # Completely disabled, as this was the main reason for strange symbol outputs
            presence_penalty=0.0,  # Completely disabled
            max_tokens=600 if is_security else 2048,
            stop=["<|eot_id|>", "<|end_of_text|>", "</s>", "[INST]", "User:", "[Foundation-Sec]:", "\n\n", "Your response:"]
        )

        usage_main = None
        gen_start_time = time.time()  # ⏱️ Start timing
        
        while True:
            # Yield control back to event loop, fetching Llama chunk safely from a background thread!
            chunk = await asyncio.to_thread(next, stream, None)
            if chunk is None:
                break
                
            if "usage" in chunk and chunk["usage"]:
                usage_main = chunk["usage"]
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    text_chunk = delta["content"]
                    assistant_response += text_chunk
                    await response_msg.stream_token(text_chunk) # Yield real-time string over to frontend
        gen_elapsed = time.time() - gen_start_time  # ⏱️ End timing
                    
        # Calculate Tokens metadata
        if not usage_main:
            p_tokens = len(active_llm.tokenize(str(chat_messages).encode("utf-8")))
            c_tokens = len(active_llm.tokenize(assistant_response.encode("utf-8")))
            usage_main = {"prompt_tokens": p_tokens, "completion_tokens": c_tokens, "total_tokens": p_tokens + c_tokens}
            
        token_info_main = (
            f"*⚡ Tokens: {usage_main.get('total_tokens', 0)} "
            f"(輸入: {usage_main.get('prompt_tokens', 0)} | 輸出: {usage_main.get('completion_tokens', 0)}) "
            f"· 🕐 Thought for {gen_elapsed:.1f}s*"
        )
        await response_msg.stream_token("\n\n---\n")
        await response_msg.stream_token(token_info_main)
        
        await response_msg.update() # Finish Token streaming

        # === Translation for Security Output ===
        if is_security:
            trans_badge = f"### 🧠 由 `Llama3-Taiwan` 進行翻譯\n---\n"
            trans_msg = cl.Message(content=f"\n\n> 🔄 *正在呼叫 Llama3-Taiwan 翻譯成中文...*\n\n", author="Translator")
            await trans_msg.send()
            
            trans_messages = [
                {"role": "system", "content": "You are a cybersecurity translation expert. Please translate the following text into Traditional Chinese. Output ONLY the translation without any preamble."},
                {"role": "user", "content": f"Text to translate:\n{assistant_response}"},
            ]
            
            chinese_response = ""
            try:
                trans_stream = llm_llama3.create_chat_completion(
                    messages=trans_messages,
                    stream=True,
                    temperature=0.1,
                    max_tokens=600,
                    stop=["<|eot_id|>", "<|end_of_text|>"]
                )
                
                # Reset translation chunk to prepare for new streams, alongside the model badge
                trans_msg.content = trans_badge
                await trans_msg.update()

                trans_usage = None
                trans_start_time = time.time()  # ⏱️ Start translation timing
                
                while True:
                    chunk = await asyncio.to_thread(next, trans_stream, None)
                    if chunk is None:
                        break
                        
                    if "usage" in chunk and chunk["usage"]:
                        trans_usage = chunk["usage"]
                    if "choices" in chunk and len(chunk["choices"]) > 0:
                        delta = chunk["choices"][0].get("delta", {})
                        if "content" in delta:
                            text_chunk = delta["content"]
                            chinese_response += text_chunk
                            await trans_msg.stream_token(text_chunk)
                trans_elapsed = time.time() - trans_start_time  # ⏱️ End translation timing
                
                # Calculate Tokens metadata
                if not trans_usage:
                    tp_tokens = len(llm_llama3.tokenize(str(trans_messages).encode("utf-8")))
                    tc_tokens = len(llm_llama3.tokenize(chinese_response.encode("utf-8")))
                    trans_usage = {"prompt_tokens": tp_tokens, "completion_tokens": tc_tokens, "total_tokens": tp_tokens + tc_tokens}
                
                trans_token_info = (
                    f"*⚡ Tokens: {trans_usage.get('total_tokens', 0)} "
                    f"(輸入: {trans_usage.get('prompt_tokens', 0)} | 輸出: {trans_usage.get('completion_tokens', 0)}) "
                    f"· 🕐 Thought for {trans_elapsed:.1f}s*"
                )
                await trans_msg.stream_token("\n\n---\n")
                await trans_msg.stream_token(trans_token_info)
                
                await trans_msg.update()
                
                # Note: We do "not" integrate the translated Chinese response into assistant_response here!
                # This guarantees that the security model (English-only domain) does not see generated Chinese inside history, avoiding localization hallucinations.
                
            except Exception as e:
                print(f"[Translation Error]: {e}")
                trans_msg.content = "**[中文翻譯失敗]**\n" + str(e)
                await trans_msg.update()

        # Update chat history (only storing clean English or general chats, no token info or nested translations)
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": assistant_response})
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        error_msg = f"❌ 產生回應時發生錯誤: {e}"
        await cl.Message(content=error_msg, author="System").send()

@cl.action_callback("view_hw_history")
async def on_action_view_hw_history(action: cl.Action):
    """Query InfluxDB and plot historical statistics."""
    await cl.Message(content="📊 正在從 InfluxDB 提取歷史數據...", author="System").send()
    try:
        # InfluxDB v3 Core drops Flux support (/api/v2/query returns 404). 
        # We must use InfluxQL via the /query endpoint (compatible with v1/v3)
        import requests
        headers = {
            "Authorization": f"Token {INFLUXDB_TOKEN}"
        }
        params = {
            "db": INFLUXDB_BUCKET,
            "q": "SELECT * FROM hardware_monitor WHERE time >= now() - 15m"
        }
        res = await asyncio.to_thread(requests.get, f"{INFLUXDB_URL}/query", headers=headers, params=params)
        res_json = res.json()
        
        results = res_json.get("results", [])
        if not results or "series" not in results[0]:
            await cl.Message(content="⚠️ 尚未收集到足夠的歷史數據。請稍後再試。", author="System").send()
            return

        series = results[0]["series"][0]
        columns = series["columns"]
        values = series["values"]
        df = pd.DataFrame(values, columns=columns)

        # Ensure _time is datetime
        if 'time' in df.columns:
            df['_time'] = pd.to_datetime(df['time'])

        # Create Plotly figure
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            subplot_titles=("CPU / GPU / RAM 使用率 (%)", "電力消耗 (Watt)"))
        
        if 'e_cpu_pct' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['e_cpu_pct'], name="E-CPU %", mode='lines'), row=1, col=1)
        if 'p_cpu_pct' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['p_cpu_pct'], name="P-CPU %", mode='lines'), row=1, col=1)
        if 'gpu_pct' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['gpu_pct'], name="GPU %", mode='lines'), row=1, col=1)
        if 'ram_pct' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['ram_pct'], name="RAM %", line=dict(dash='dot')), row=1, col=1)

        if 'cpu_power_w' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['cpu_power_w'], name="CPU W", mode='lines'), row=2, col=1)
        if 'gpu_power_w' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['gpu_power_w'], name="GPU W", mode='lines'), row=2, col=1)
        if 'total_power_w' in df.columns:
            fig.add_trace(go.Scatter(x=df['_time'], y=df['total_power_w'], name="Total W", mode='lines'), row=2, col=1)

        fig.update_layout(height=600, template="plotly_dark", title_text="最近 15 分鐘硬體資源消耗趨勢")
        
        # Send chart directly in Chainlit
        elements = [
            cl.Plotly("歷史監控圖表", figure=fig, display="inline")
        ]
        await cl.Message(content="✅ **歷史硬體狀態已生成**", elements=elements, author="H/W Monitor").send()

    except Exception as e:
        await cl.Message(content=f"❌ 讀取 InfluxDB 數據時發生錯誤: {e}", author="System").send()
