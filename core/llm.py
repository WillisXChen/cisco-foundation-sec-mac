import os
from llama_cpp import Llama

class LLMManager:
    """Manages the LLMs (Llama, Foundation-Sec) and intent classification."""
    def __init__(self):
        self.llm_general = None
        self.llm_sec = None
        
        self.sec_system_message = (
            "You are Foundation-Sec, a highly advanced cybersecurity, network, server , devops , docker , kubernetes , webserver and system administration expert.\\n"
            "RULES:\\n"
            "1. Respond directly in English. Do not attempt to translate or use Chinese characters in your output.\\n"
            "2. Provide EXACTLY ONE concise paragraph outlining the analysis, root cause, or concept.\\n"
            "3. Begin your response immediately with the analysis. Do not echo the user's prompt.\\n"
            "4. Do not use markdown headings (#) or numbered lists."
        )
        self.general_system_message = (
            "You are a helpful AI assistant. Answer the user's questions politely and naturally in Traditional Chinese."
        )

    def load_general_model(self, path: str, context_size: int = 4096):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found at {path}")
        self.llm_general = Llama(
            model_path=path,
            n_gpu_layers=-1,
            seed=1337,            
            n_ctx=context_size,   
            verbose=False,        
            chat_format="llama-3" 
        )

    def load_security_model(self, path: str, context_size: int = 4096):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found at {path}")
        self.llm_sec = Llama(
            model_path=path,
            n_gpu_layers=-1,
            seed=1337,            
            n_ctx=context_size,   
            verbose=False,        
            chat_format="llama-3" 
        )

    def classify_intent(self, user_input: str) -> bool:
        """Returns True if intent is security/IT related, False otherwise."""
        classification_messages = [
            {
                "role": "system",
                "content": "You are a specialized technical router. You must classify if the user's input is related to IT, security, programming, system architecture, or operating systems.\\n"
                           "Reply with EXACTLY ONE word: 'YES' or 'NO'. Do NOT provide any explanations, code, or repeat the user's input.\\n"
                           "Reply 'YES' if the input contains ANY of the following: programming questions, tracebacks, errors, code snippets, system architecture design, operating system queries, Apache logs, Nginx logs, PHP errors, permission denied, SQL injection, hacking, bugs, server crashes, security audit, or any raw code/log output.\\n"
                           "Reply 'NO' only if it is a general casual chat like 'Hi', 'How are you', etc."
            },
            {"role": "user", "content": user_input}
        ]
        
        # Fallback keywords
        critical_it_keywords = ["http", "get ", "post ", "error", "exception", "php", "sql", "login", ".bak", "log", "404", "500", "id_rsa", "ssh"]
        user_input_lower = user_input.lower()
        if any(keyword in user_input_lower for keyword in critical_it_keywords):
            return True

        if not self.llm_general:
            return False
            
        try:
            res = self.llm_general.create_chat_completion(
                messages=classification_messages,
                max_tokens=2,
                temperature=0.0
            )
            intent_text = res["choices"][0]["message"]["content"].strip().upper()
            return "YES" in intent_text
        except Exception:
            return False

    def get_active_model(self, is_security: bool):
        return self.llm_sec if is_security else self.llm_general

    def get_active_system_message(self, is_security: bool) -> str:
        return self.sec_system_message if is_security else self.general_system_message
