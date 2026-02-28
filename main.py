import asyncio
import time
import typing
import engineio
import chainlit as cl
import os
import json
import strawberry
from strawberry.fastapi import GraphQLRouter
from chainlit.server import app as fastapi_app
from collections import deque
import plotly.graph_objects as go

from core.hardware import HardwareMonitor
from core.database import VectorDBManager, MetricsDBManager
from core.llm import LLMManager

engineio.payload.Payload.max_decode_packets = 500000
os.makedirs(".files", exist_ok=True)

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8181")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "apiv3_cisco-super-secret-auth-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "cisco")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "metrics")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

MODEL_SEC_PATH = os.getenv("MODEL_SEC_PATH", "./models/foundation-sec-8b-q4_k_m.gguf")
MODEL_LLAMA3_PATH = os.getenv("MODEL_LLAMA3_PATH", "./models/llama-3-taiwan-8b-instruct-q4_k_m.gguf")

# Global dependencies
hw_monitor = HardwareMonitor()
llm_manager = LLMManager()
vector_db = VectorDBManager(url=QDRANT_URL)
metrics_db = None  # Instantiated in background task to avoid async loop issues

_latest_hw_stats = hw_monitor.get_stats()

import sys
if __name__ not in sys.modules:
    sys.modules[__name__] = sys.modules['__main__']

# GraphQL
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
        while True:
            yield HWStats(**_latest_hw_stats)
            await asyncio.sleep(2)

schema = strawberry.Schema(query=Query, subscription=Subscription)
graphql_app = GraphQLRouter(schema)
fastapi_app.include_router(graphql_app, prefix="/graphql")

async def hardware_monitor_task():
    global _latest_hw_stats, metrics_db
    try:
        metrics_db = MetricsDBManager(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG, bucket=INFLUXDB_BUCKET)
    except Exception as e:
        print(f"InfluxDB Connection error: {e}")
        metrics_db = None

    while True:
        try:
            stats = await asyncio.to_thread(hw_monitor.get_stats)
            _latest_hw_stats = stats
            
            if metrics_db:
                await asyncio.to_thread(metrics_db.write_hardware_stats, stats)
        except Exception as e:
            print(f"Monitor error: {e}")
        await asyncio.sleep(2)

@cl.on_chat_start
async def on_chat_start():
    content = (
        f"### 🚀 ASITOP HUD `{hw_monitor.chip_label}`\n"
        f"<iframe src='http://localhost:8501/?embed=true' width='100%' height='320' frameborder='0' style='border-radius: 8px; border: 1px solid rgba(0, 255, 255, 0.4); background: #0d1117;'></iframe>\n"
    )
    
    actions = [cl.Action(name="view_hw_history", payload={"action": "show"}, description="查看歷史硬體資源與電力消耗數據")]
    stats_msg = cl.Message(content=content, author="H/W Monitor", actions=actions)
    await stats_msg.send()
    
    asyncio.create_task(hardware_monitor_task())

    loading_msg = cl.Message(content="### ⚙️ 系統初始化中... 正在載入 AI 模型，請稍候。")
    await loading_msg.send()

    try:
        if llm_manager.llm_general is None:
            loading_msg.content = "### ⚙️ 載入中 (1/4)：正在載入 Llama3-Taiwan 模型..."
            await loading_msg.update()
            await asyncio.to_thread(llm_manager.load_general_model, MODEL_LLAMA3_PATH)

        if llm_manager.llm_sec is None:
            loading_msg.content = "### ⚙️ 載入中 (2/4)：正在載入 Foundation-Sec 資安模型..."
            await loading_msg.update()
            await asyncio.to_thread(llm_manager.load_security_model, MODEL_SEC_PATH)

        loading_msg.content = "### ⚙️ 載入中 (3/4)：正在連線 Qdrant 向量資料庫..."
        await loading_msg.update()
        await asyncio.to_thread(vector_db.setup_model)

        loading_msg.content = "### ⚙️ 載入中 (4/4)：正在同步資安 SOP 知識庫..."
        await loading_msg.update()
        
        exists = await asyncio.to_thread(vector_db.is_collection_exists)
        if not exists:
            playbooks_path = os.path.join(os.path.dirname(__file__), "playbooks.json")
            await asyncio.to_thread(vector_db.ingest_playbooks, playbooks_path)

        loading_msg.content = "### ✅ 模型載入完成！\n\n🛡️ **歡迎使用 Foundation-Sec-8B Security Assistant!** 🛡️\n\n您可以開始輸入有關資安、程式設計或一般問題。"
        await loading_msg.update()

    except Exception as e:
        loading_msg.content = f"### ❌ 模型載入失敗\n錯誤訊息: `{e}`\n請確認模型路徑是否正確 (預設路徑 `./models/...`)。"
        await loading_msg.update()
        return

    cl.user_session.set("chat_history", [])

@cl.on_message
async def main(message: cl.Message):
    if llm_manager.llm_general is None or llm_manager.llm_sec is None:
        await cl.Message(content="⚠️ 模型尚未載入完成，請重整頁面或確認終端機錯誤訊息。").send()
        return

    user_input = message.content.strip()
    chat_history = cl.user_session.get("chat_history", [])

    is_security = await asyncio.to_thread(llm_manager.classify_intent, user_input)
    
    active_llm = llm_manager.get_active_model(is_security)
    active_name = "Foundation-Sec" if is_security else "Llama3-Taiwan"
    active_system_msg = llm_manager.get_active_system_message(is_security)

    chat_messages = [{"role": "system", "content": active_system_msg}]
    for msg in chat_history:
        chat_messages.append(msg)

    if not is_security:
        chat_messages.append({"role": "user", "content": user_input})
    else:
        context_str = await asyncio.to_thread(vector_db.query_context, user_input)
        enforced_input = f"{context_str}{user_input}\n\n[Action: Please analyze the above input and respond in English only. Base your answer on the Internal System Context if it is relevant.]"
        chat_messages.append({"role": "user", "content": enforced_input})

    model_badge = f"### 🧠 由 `{active_name}` 生成回應\n---\n"
    response_msg = cl.Message(content=model_badge, author=active_name)
    await response_msg.send()

    assistant_response = ""
    try:
        stream = active_llm.create_chat_completion(
            messages=chat_messages,
            stream=True,         
            temperature=0.4 if is_security else 0.2,
            top_p=0.9,
            repeat_penalty=1.05 if is_security else 1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            max_tokens=600 if is_security else 2048,
            stop=["<|eot_id|>", "<|end_of_text|>", "</s>", "[INST]", "User:", "[Foundation-Sec]:", "\n\n", "Your response:"]
        )

        usage_main = None
        gen_start_time = time.time()
        
        while True:
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
                    await response_msg.stream_token(text_chunk)
                    
        gen_elapsed = time.time() - gen_start_time
                    
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
        await response_msg.update()

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
                trans_stream = llm_manager.llm_general.create_chat_completion(
                    messages=trans_messages,
                    stream=True,
                    temperature=0.1,
                    max_tokens=600,
                    stop=["<|eot_id|>", "<|end_of_text|>"]
                )
                
                trans_msg.content = trans_badge
                await trans_msg.update()

                trans_usage = None
                trans_start_time = time.time()
                
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
                            
                trans_elapsed = time.time() - trans_start_time
                
                if not trans_usage:
                    tp_tokens = len(llm_manager.llm_general.tokenize(str(trans_messages).encode("utf-8")))
                    tc_tokens = len(llm_manager.llm_general.tokenize(chinese_response.encode("utf-8")))
                    trans_usage = {"prompt_tokens": tp_tokens, "completion_tokens": tc_tokens, "total_tokens": tp_tokens + tc_tokens}
                
                trans_token_info = (
                    f"*⚡ Tokens: {trans_usage.get('total_tokens', 0)} "
                    f"(輸入: {trans_usage.get('prompt_tokens', 0)} | 輸出: {trans_usage.get('completion_tokens', 0)}) "
                    f"· 🕐 Thought for {trans_elapsed:.1f}s*"
                )
                await trans_msg.stream_token("\n\n---\n")
                await trans_msg.stream_token(trans_token_info)
                await trans_msg.update()
                
            except Exception as e:
                print(f"[Translation Error]: {e}")
                trans_msg.content = "**[中文翻譯失敗]**\n" + str(e)
                await trans_msg.update()

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": assistant_response})
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        error_msg = f"❌ 產生回應時發生錯誤: {e}"
        await cl.Message(content=error_msg, author="System").send()

@cl.action_callback("view_hw_history")
async def on_action_view_hw_history(action: cl.Action):
    await cl.Message(content="📊 正在從 InfluxDB 提取歷史數據...", author="System").send()
    try:
        # Recreate DB manager locally or reuse if possible
        temp_db = MetricsDBManager(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG, bucket=INFLUXDB_BUCKET)
        df = await asyncio.to_thread(temp_db.query_hardware_history_df)

        if df.empty:
            await cl.Message(content="⚠️ 尚未收集到足夠的歷史數據。請稍後再試。", author="System").send()
            return

        from plotly.subplots import make_subplots
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            subplot_titles=("CPU / GPU / RAM 使用率 (%)", "電力消耗 (Watt)"))
        
        if 'e_cpu_pct' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['e_cpu_pct'], name="E-CPU %", mode='lines'), row=1, col=1)
        if 'p_cpu_pct' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['p_cpu_pct'], name="P-CPU %", mode='lines'), row=1, col=1)
        if 'gpu_pct' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['gpu_pct'], name="GPU %", mode='lines'), row=1, col=1)
        if 'ram_pct' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['ram_pct'], name="RAM %", line=dict(dash='dot')), row=1, col=1)

        if 'cpu_power_w' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['cpu_power_w'], name="CPU W", mode='lines'), row=2, col=1)
        if 'gpu_power_w' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['gpu_power_w'], name="GPU W", mode='lines'), row=2, col=1)
        if 'total_power_w' in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df['total_power_w'], name="Total W", mode='lines'), row=2, col=1)

        fig.update_layout(height=600, template="plotly_dark", title_text="最近 15 分鐘硬體資源消耗趨勢")
        
        elements = [cl.Plotly("歷史監控圖表", figure=fig, display="inline")]
        await cl.Message(content="✅ **歷史硬體狀態已生成**", elements=elements, author="H/W Monitor").send()

    except Exception as e:
        await cl.Message(content=f"❌ 讀取 InfluxDB 數據時發生錯誤: {e}", author="System").send()
