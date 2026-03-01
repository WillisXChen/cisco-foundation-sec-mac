from langfuse import Langfuse
import os

# 直接填入您的 Key 進行測試，不依賴環境變數
PUBLIC_KEY = "pk-lf-1234567890"
SECRET_KEY = "sk-lf-1234567890"
HOST = "http://localhost:3001"

print("--- Final Langfuse Test ---")
langfuse = Langfuse(public_key=PUBLIC_KEY, secret_key=SECRET_KEY, host=HOST)

try:
    # 建立一個事件（Event）
    # 在 3.14.5 版本，我們使用底層方法確保資料送出
    print("Creating a manual trace event...")
    langfuse.create_event(
        name="Backend Connectivity Test",
        input="Testing manual event creation",
        output="Successful"
    )
    
    print("Flushing...")
    langfuse.flush()
    print("✅ 資料已送出！")
    print("請到 Langfuse 介面 -> Traces -> 點擊重新整理。")
except Exception as e:
    print(f"❌ 發生錯誤: {e}")
