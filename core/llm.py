import os
from llama_cpp import Llama
from core.config import (
    SEC_SYSTEM_MESSAGE, 
    GENERAL_SYSTEM_MESSAGE, 
    INTENT_ROUTER_MESSAGE, 
    CRITICAL_IT_KEYWORDS
)
from core.logger import logger

class LLMManager:
    """Manages the LLMs (Llama, Foundation-Sec) and intent classification."""
    def __init__(self):
        self.llm_general = None
        self.llm_sec = None

    def _load_model(self, path: str, context_size: int = 4096) -> Llama:
        if not os.path.exists(path):
            logger.error(f"Model file not found at {path}")
            raise FileNotFoundError(f"Model file not found at {path}")
        
        logger.info(f"Loading model from {path}...")
        return Llama(
            model_path=path,
            n_gpu_layers=-1,
            seed=1337,            
            n_ctx=context_size,   
            verbose=False,        
            chat_format="llama-3" 
        )

    def load_general_model(self, path: str, context_size: int = 4096):
        if self.llm_general is not None:
            logger.info("General model already loaded, skipping.")
            return
        self.llm_general = self._load_model(path, context_size)

    def load_security_model(self, path: str, context_size: int = 4096):
        if self.llm_sec is not None:
            logger.info("Security model already loaded, skipping.")
            return
        self.llm_sec = self._load_model(path, context_size)

    def classify_intent(self, user_input: str) -> bool:
        """Returns True if intent is security/IT related, False otherwise."""
        user_input_lower = user_input.lower()
        if any(keyword in user_input_lower for keyword in CRITICAL_IT_KEYWORDS):
            logger.info("Intent classified as 'Security' via keyword match.")
            return True

        if not self.llm_general:
            return False
            
        classification_messages = [
            {"role": "system", "content": INTENT_ROUTER_MESSAGE},
            {"role": "user", "content": user_input}
        ]
        
        try:
            res = self.llm_general.create_chat_completion(
                messages=classification_messages,
                max_tokens=2,
                temperature=0.0
            )
            intent_text = res["choices"][0]["message"]["content"].strip().upper()
            is_sec = "YES" in intent_text
            logger.info(f"Intent classified by LLM: {'Security' if is_sec else 'General'}")
            return is_sec
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return False

    def get_active_model(self, is_security: bool):
        return self.llm_sec if is_security else self.llm_general

    def get_active_system_message(self, is_security: bool) -> str:
        return SEC_SYSTEM_MESSAGE if is_security else GENERAL_SYSTEM_MESSAGE
