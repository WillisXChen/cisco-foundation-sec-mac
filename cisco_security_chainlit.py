import chainlit as cl
import os
from llama_cpp import Llama
from qdrant_client import QdrantClient

# === Configuration ===
# 設定預設的模型路徑，可以透過環境變數覆寫
MODEL_SEC_PATH = os.getenv("MODEL_SEC_PATH", "./models/foundation-sec-8b-q4_k_m.gguf")
MODEL_LLAMA3_PATH = os.getenv("MODEL_LLAMA3_PATH", "./models/llama-3-taiwan-8b-instruct-q4_k_m.gguf")

# === 全域變數 (Global instances) ===
# 只在啟動時載入一次模型，避免每次連線都重新載入消耗記憶體與時間
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
    
    # 傳送載入中的訊息給使用者
    loading_msg = cl.Message(content="### ⚙️ 系統初始化中... 正在載入 AI 模型，請稍候。")
    await loading_msg.send()

    try:
        # 載入模型（若尚未載入）
        if llm_llama3 is None:
            llm_llama3 = load_model(MODEL_LLAMA3_PATH)
        if llm_sec is None:
            llm_sec = load_model(MODEL_SEC_PATH)
        if qdrant_client is None:
            print("Connecting to Qdrant instance...")
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            qdrant_client = QdrantClient(url=qdrant_url)
            print("Setting up embedding model...")
            qdrant_client.set_model("BAAI/bge-small-en-v1.5")
            
        loading_msg.content = "### ✅ 模型載入完成！\n\n🛡️ **歡迎使用 Foundation-Sec-8B Security Assistant!** 🛡️\n\n您可以開始輸入有關資安、程式設計或一般問題。"
        await loading_msg.update()
        
    except Exception as e:
        loading_msg.content = f"### ❌ 模型載入失敗\n錯誤訊息: `{e}`\n請確認模型路徑是否正確 (預設路徑 `./models/...`)。"
        await loading_msg.update()
        return

    # 初始化這個使用者的聊天歷史紀錄
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

    # 僅根據當前問題判斷 Intent，避免歷史對話過長導致分類器（Llama 3）混亂而無法正確輸出 YES/NO
    classification_messages.append({"role": "user", "content": user_input})

    is_security = False
    
    # 建立 IT 關鍵字安全網，防止小型模型對生硬 Log 分類失敗
    critical_it_keywords = ["http", "get ", "post ", "error", "exception", "php", "sql", "login", ".bak", "log", "404", "500", "id_rsa", "ssh"]
    user_input_lower = user_input.lower()
    
    # 如果 Llama3 判斷錯誤，但內容明顯是 IT/Log 相關，強制定義為資安問題
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

    # 根據分類結果決定使用的模型
    active_llm = llm_sec if is_security else llm_llama3
    active_name = "Foundation-Sec" if is_security else "Llama3-Taiwan"
    active_system_msg = sec_system_message if is_security else general_system_message

    # === Main Generation ===
    chat_messages = [{"role": "system", "content": active_system_msg}]
    
    # 無論是一般還是資安問題，都帶入歷史對話紀錄，確保多輪上下文記憶
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

        # 針對資安相關問題，適度提醒回覆英文即可，不要用語氣過於強烈的威脅性字眼，避免 8B 模型引發幻覺崩潰
        enforced_input = f"{context_str}{user_input}\n\n[Action: Please analyze the above input and respond in English only. Base your answer on the Internal System Context if it is relevant.]"
        chat_messages.append({"role": "user", "content": enforced_input})

    # 準備一個明顯的前綴標籤，讓使用者知道是哪個模型在回答
    model_badge = f"### 🧠 由 `{active_name}` 生成回應\n---\n"
    
    # 先發送一個空的 Message (UI 出現載入動畫)，之後會逐步串流 (Stream)
    response_msg = cl.Message(content=model_badge, author=active_name)
    await response_msg.send()

    assistant_response = ""
    
    try:
        stream = active_llm.create_chat_completion(
            messages=chat_messages,
            stream=True,         
            temperature=0.4 if is_security else 0.2,  # 提高自然變化率以取代強壓式的懲罰
            top_p=0.9,
            repeat_penalty=1.05 if is_security else 1.0, # 降到最底線，防止 logits 崩潰成亂碼
            frequency_penalty=0.0, # 全面關閉，這是導致印出奇怪符號的主因
            presence_penalty=0.0,  # 全面關閉
            max_tokens=600 if is_security else 2048,
            stop=["<|eot_id|>", "<|end_of_text|>", "</s>", "[INST]", "User:", "[Foundation-Sec]:", "\n\n", "Your response:"]
        )

        usage_main = None
        for chunk in stream:
            if "usage" in chunk and chunk["usage"]:
                usage_main = chunk["usage"]
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    text_chunk = delta["content"]
                    assistant_response += text_chunk
                    await response_msg.stream_token(text_chunk) # 即時將字串送往前端
                    
        # 計算 Tokens 資訊
        if not usage_main:
            p_tokens = len(active_llm.tokenize(str(chat_messages).encode("utf-8")))
            c_tokens = len(active_llm.tokenize(assistant_response.encode("utf-8")))
            usage_main = {"prompt_tokens": p_tokens, "completion_tokens": c_tokens, "total_tokens": p_tokens + c_tokens}
            
        token_info_main = f"\n\n---\n*⚡ Tokens: {usage_main.get('total_tokens', 0)} (輸入: {usage_main.get('prompt_tokens', 0)} | 輸出: {usage_main.get('completion_tokens', 0)})*"
        await response_msg.stream_token(token_info_main)
        
        await response_msg.update() # 結束 Token 串流

        # === Translation for Security Output ===
        if is_security:
            trans_badge = f"### 🧠 由 `Llama3-Taiwan` 進行翻譯\n---\n"
            trans_msg = cl.Message(content=f"\n\n> 🔄 *正在呼叫 Llama3-Taiwan 翻譯成中文...*\n\n", author="Translator")
            await trans_msg.send()
            
            trans_messages = [
                {"role": "system", "content": "你是資安翻譯專家。請將原文翻譯成繁體中文。請直接輸出翻譯結果，不要加上任何解釋或開場白。"},
                {"role": "user", "content": f"原文：\n{assistant_response}"},
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
                
                # 重設翻譯區塊的內容準備接收新的串流，並加上模型標籤
                trans_msg.content = trans_badge
                await trans_msg.update()

                trans_usage = None
                for chunk in trans_stream:
                    if "usage" in chunk and chunk["usage"]:
                        trans_usage = chunk["usage"]
                    if "choices" in chunk and len(chunk["choices"]) > 0:
                        delta = chunk["choices"][0].get("delta", {})
                        if "content" in delta:
                            text_chunk = delta["content"]
                            chinese_response += text_chunk
                            await trans_msg.stream_token(text_chunk)
                
                # 計算 Tokens 資訊
                if not trans_usage:
                    tp_tokens = len(llm_llama3.tokenize(str(trans_messages).encode("utf-8")))
                    tc_tokens = len(llm_llama3.tokenize(chinese_response.encode("utf-8")))
                    trans_usage = {"prompt_tokens": tp_tokens, "completion_tokens": tc_tokens, "total_tokens": tp_tokens + tc_tokens}
                
                trans_token_info = f"\n\n---\n*⚡ Tokens: {trans_usage.get('total_tokens', 0)} (輸入: {trans_usage.get('prompt_tokens', 0)} | 輸出: {trans_usage.get('completion_tokens', 0)})*"
                await trans_msg.stream_token(trans_token_info)
                
                await trans_msg.update()
                
                # 注意：這裡「不」將中文翻譯結果整併進 assistant_response
                # 這樣才能確保資安模型（只能講英文）在讀取歷史紀錄時，不會看到自己產生中文，避免發生語系幻覺污染
                
            except Exception as e:
                print(f"[Translation Error]: {e}")
                trans_msg.content = "**[中文翻譯失敗]**\n" + str(e)
                await trans_msg.update()

        # Update chat history (只存乾淨的英文或一般對話，不含 Token 資訊與翻譯)
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": assistant_response})
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        error_msg = f"❌ 產生回應時發生錯誤: {e}"
        await cl.Message(content=error_msg, author="System").send()
