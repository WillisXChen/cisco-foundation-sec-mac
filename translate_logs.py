import os
import sys
from llama_cpp import Llama

def run_analysis():
    # Use absolute path for robustness
    base_dir = os.path.dirname(os.path.abspath(__file__))
    translator_model_path = os.path.join(base_dir, "models", "llama-3-taiwan-8b-instruct-q4_k_m.gguf")

    english_analysis = """Based on the provided web server logs, there are two distinct attacks attempting to compromise the system:

1. **Directory Traversal (Path Traversal)**: The first log entry shows an attempt to access `/etc/passwd` using `../../`, a common technique to navigate outside the intended directory structure and access sensitive files on Linux systems.

2. **Command Injection**: The second log entry shows an attempt to execute a command (`cmd.exe?/c+dir`) on a Windows system using a directory traversal payload (`..%255c..%255cwinnt/system32/cmd.exe`). This indicates an attacker aims to execute arbitrary commands on the server.

**Implications**: These attacks highlight critical vulnerabilities in the web application's input validation and sanitization. If successful, attackers could gain unauthorized access to sensitive files, execute arbitrary commands, and potentially compromise the entire system."""

    print("Loading Llama-3-Taiwan model...")
    if not os.path.exists(translator_model_path):
        print(f"Error: Model not found at {translator_model_path}")
        return

    llm_trans = Llama(
        model_path=translator_model_path,
        n_gpu_layers=-1,
        n_ctx=2048,
        verbose=False,
        chat_format="llama-3"
    )

    print("Generating Chinese translation...")
    # Force Chinese output by stating the assistant role in the prompt
    res_trans = llm_trans.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a professional cybersecurity translation expert. Please translate the following English content into Traditional Chinese. Output ONLY the translation."},
            {"role": "user", "content": f"English content to translate:\n{english_analysis}"},
        ],
        max_tokens=800,
        temperature=0.1
    )
    chinese_analysis = res_trans["choices"][0]["message"]["content"].strip()
    
    del llm_trans
    print("---CHINESE_TRANSLATION_START---")
    print(chinese_analysis)
    print("---CHINESE_TRANSLATION_END---")

if __name__ == "__main__":
    run_analysis()
