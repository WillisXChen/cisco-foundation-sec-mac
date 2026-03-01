import asyncio
import os
import engineio
import chainlit as cl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from langfuse import observe

# Import our separated modules
from core.config import (
    MODEL_SEC_PATH, MODEL_LLAMA3_PATH, PLAYBOOKS_PATH
)
from core.logger import logger
import core.services as services
# Ensure API routes are loaded
import api

# Performance optimization for Large Payloads
engineio.payload.Payload.max_decode_packets = 500000
os.makedirs(".files", exist_ok=True)

# --- Chainlit Callbacks ---
@cl.on_chat_start
async def on_chat_start():
    actions = [cl.Action(name="view_hw_history", payload={"action": "show"}, description="查看歷史資源趨勢")]
    
    # Start background tasks
    services.start_hardware_monitor()

    loading_msg = cl.Message(content="### ⚙️ 系統初始化中...", actions=actions)
    await loading_msg.send()

    try:
        # Load models if not already loaded
        for step, (name, path, loader) in enumerate([
            ("Llama3-Taiwan", MODEL_LLAMA3_PATH, services.llm_manager.load_general_model),
            ("Foundation-Sec", MODEL_SEC_PATH, services.llm_manager.load_security_model)
        ], 1):
            loading_msg.content = f"### ⚙️ 載入中 ({step}/4)：正在載入 {name}..."
            await loading_msg.update()
            await asyncio.to_thread(loader, path)

        loading_msg.content = "### ⚙️ 載入中 (3/4)：正在初始化向量資料庫..."
        await loading_msg.update()
        await asyncio.to_thread(services.vector_db.setup_model)

        loading_msg.content = "### ⚙️ 載入中 (4/4)：同步知識庫..."
        await loading_msg.update()
        if not await asyncio.to_thread(services.vector_db.is_collection_exists):
            await asyncio.to_thread(services.vector_db.ingest_playbooks, PLAYBOOKS_PATH)

        loading_msg.content = "### ✅ 系統就緒！\n🛡️ **Foundation-Sec-8B Security Assistant** 已啟動。"
        await loading_msg.update()
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        loading_msg.content = f"### ❌ 初始化失敗: `{e}`"
        await loading_msg.update()

    cl.user_session.set("chat_history", [])

@cl.on_message
@observe()
async def main(message: cl.Message):
    chat_history = cl.user_session.get("chat_history", [])
    user_input = message.content.strip()

    # Main Response Generation
    response_msg = cl.Message(content="", author="System")
    assistant_full_text = ""
    is_sec = False

    # Start Phoenix Trace
    with services.tracer.start_as_current_span(f"Chat Generation: {user_input[:20]}..."):
        async for chunk in services.assistant_service.generate_response(user_input, chat_history):
            if chunk["type"] == "meta":
                response_msg.author = chunk["author"]
                response_msg.content = f"### 🧠 由 `{chunk['author']}` 生成回應\n---\n"
                is_sec = chunk["is_security"]
                await response_msg.send()
            elif chunk["type"] == "token":
                assistant_full_text += chunk["content"]
                await response_msg.stream_token(chunk["content"])
            elif chunk["type"] == "final":
                token_info = (
                    f"\n\n---\n*⚡ Tokens: {chunk['tokens']['total']} "
                    f"(進: {chunk['tokens']['prompt']} | 出: {chunk['tokens']['completion']}) "
                    f"· 🕐 {chunk['elapsed']:.1f}s*"
                )
                await response_msg.stream_token(token_info)
                await response_msg.update()

    # Optional Translation
    if is_sec:
        trans_msg = cl.Message(content="\n\n> 🔄 *正在翻譯回中文...*\n\n", author="Translator")
        await trans_msg.send()
        trans_full_text = ""
        
        async for chunk in services.assistant_service.translate_response(assistant_full_text):
            if chunk["type"] == "meta":
                trans_msg.content = f"### 🧠 由 `Llama3-Taiwan` 進行翻譯\n---\n"
                await trans_msg.update()
            elif chunk["type"] == "token":
                trans_full_text += chunk["content"]
                await trans_msg.stream_token(chunk["content"])
            elif chunk["type"] == "final":
                token_info = (
                    f"\n\n---\n*⚡ Tokens: {chunk['tokens']['total']} "
                    f"· 🕐 {chunk['elapsed']:.1f}s*"
                )
                await trans_msg.stream_token(token_info)
                await trans_msg.update()

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": assistant_full_text})
    cl.user_session.set("chat_history", chat_history)

@cl.action_callback("view_hw_history")
async def on_action_view_hw_history(action: cl.Action):
    await cl.Message(content="📊 正在從 InfluxDB 提取歷史數據...", author="System").send()
    
    try:
        if services.metrics_db is None:
            await cl.Message(content="⚠️ 資料庫未連線，請稍後再試。", author="System").send()
            return

        df = await asyncio.to_thread(services.metrics_db.query_hardware_history_df)
        if df.empty:
            await cl.Message(content="⚠️ 尚未收集到足夠的歷史數據。", author="System").send()
            return

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("使用率 (%)", "電力 (Watt)"))
        for col, name in [('e_cpu_pct', 'E-CPU %'), ('p_cpu_pct', 'P-CPU %'), ('gpu_pct', 'GPU %'), ('ram_pct', 'RAM %')]:
            if col in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df[col], name=name), row=1, col=1)
        for col, name in [('cpu_power_w', 'CPU W'), ('gpu_power_w', 'GPU W'), ('total_power_w', 'Total W')]:
            if col in df.columns: fig.add_trace(go.Scatter(x=df['_time'], y=df[col], name=name), row=2, col=1)

        fig.update_layout(
            height=650, 
            template="plotly_dark", 
            title_text="最近 15 分鐘趨勢",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            ),
            margin=dict(b=80)
        )
        await cl.Message(content="✅ **歷史圖表已生成**", elements=[cl.Plotly("歷史監控", figure=fig, display="inline")], author="H/W Monitor").send()
    except Exception as e:
        logger.error(f"Plot error: {e}")
        await cl.Message(content=f"❌ 讀取數據錯誤: {e}", author="System").send()
