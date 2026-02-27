import asyncio
import time
import chainlit as cl
import os
import json
from llama_cpp import Llama
from qdrant_client import QdrantClient

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

    # Send loading message to user (Show before model starts loading to inform them to wait)
    # Note: During on_chat_start execution, Chainlit automatically locks the input field,
    #       until this function completes fully, ensuring input unlocks only when models are ready.
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
        # Check if collection exists or has documents (Simplified: just attempt to ingest)
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
        for chunk in stream:
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
                for chunk in trans_stream:
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
