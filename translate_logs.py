import os
import sys
from llama_cpp import Llama

def run_analysis():
    translator_model_path = "./models/llama-3-taiwan-8b-instruct-q4_k_m.gguf"

    english_analysis = """Based on the provided web server logs, there are two distinct attacks attempting to compromise the system:

1. **Directory Traversal (Path Traversal)**: The first log entry shows an attempt to access `/etc/passwd` using `../../`, a common technique to navigate outside the intended directory structure and access sensitive files on Linux systems.

2. **Command Injection**: The second log entry shows an attempt to execute a command (`cmd.exe?/c+dir`) on a Windows system using a directory traversal payload (`..%255c..%255cwinnt/system32/cmd.exe`). This indicates an attacker aims to execute arbitrary commands on the server.

**Implications**: These attacks highlight critical vulnerabilities in the web application's input validation and sanitization. If successful, attackers could gain unauthorized access to sensitive files, execute arbitrary commands, and potentially compromise the entire system."""

    print("Loading Llama-3-Taiwan model...")
    llm_trans = Llama(
        model_path=translator_model_path,
        n_gpu_layers=-1,
        n_ctx=2048,
        verbose=False,
        chat_format="llama-3"
    )

    print("Generating Chinese translation...")
    # Force Chinese output by stating the assistant role
    res_trans = llm_trans.create_chat_completion(
        messages=[
            {"role": "system", "content": "你是一個專業的資安翻譯專家。請將以下原文翻譯成繁體中文 (Traditional Chinese)。"},
            {"role": "user", "content": f"需要翻譯的英文內容：\n{english_analysis}"},
        ],
        max_tokens=800,
        temperature=0.1
    )
    chinese_analysis = res_trans["choices"][0]["message"]["content"].strip()
    
    del llm_trans
    print("---CHINESE_START---")
    print(chinese_analysis)
    print("---CHINESE_END---")

if __name__ == "__main__":
    run_analysis()
