import asyncio
import time
import typing
from core.llm import LLMManager
from core.database import VectorDBManager
from core.config import TRANSLATION_SYSTEM_MESSAGE
from core.logger import logger
from langfuse import observe

class AssistantService:
    """Orchestrates LLM calls, RAG context, and translation logic."""
    def __init__(self, llm_manager: LLMManager, vector_db: VectorDBManager):
        self.llm = llm_manager
        self.vector_db = vector_db

    @observe(as_type="generation")
    async def generate_response(self, user_input: str, chat_history: list, target_lang: str = "Traditional Chinese") -> typing.AsyncGenerator[dict, None]:
        """Classifies intent, fetches context, and streams main response."""
        
        # 1. Classify Intent
        is_security = await asyncio.to_thread(self.llm.classify_intent, user_input)
        active_llm = self.llm.get_active_model(is_security)
        active_name = "Foundation-Sec" if is_security else "Llama3-Taiwan"
        active_system_msg = self.llm.get_active_system_message(is_security)

        # 2. Build Messages
        chat_messages = [{"role": "system", "content": active_system_msg}]
        chat_messages.extend(chat_history)

        if is_security:
            context_str = await asyncio.to_thread(self.vector_db.query_context, user_input)
            enforced_input = (
                f"{context_str}{user_input}\n\n"
                f"[Action: Please analyze the above input and respond in English only. "
                f"Base your answer on the Internal System Context if it is relevant.]"
            )
            chat_messages.append({"role": "user", "content": enforced_input})
        else:
            if target_lang != "Traditional Chinese":
                enforced_input = f"{user_input}\n\n[Action: Please respond in {target_lang} only.]"
                chat_messages.append({"role": "user", "content": enforced_input})
            else:
                chat_messages.append({"role": "user", "content": user_input})

        # 3. Stream Main Response
        temperature = 0.4 if is_security else 0.2
        max_tokens = 600 if is_security else 2048
        
        logger.info(f"Generating response using {active_name}...")
        stream = active_llm.create_chat_completion(
            messages=chat_messages,
            stream=True,
            temperature=temperature,
            top_p=0.9,
            max_tokens=max_tokens,
            stop=["<|eot_id|>", "<|end_of_text|>", "</s>", "[INST]", "User:", "[Foundation-Sec]:", "\n\n", "Your response:"]
        )

        assistant_response = ""
        gen_start_time = time.time()
        
        yield {"type": "meta", "author": active_name, "is_security": is_security}

        while True:
            chunk = await asyncio.to_thread(next, stream, None)
            if chunk is None:
                break
            
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    text_chunk = delta["content"]
                    assistant_response += text_chunk
                    yield {"type": "token", "content": text_chunk}

        gen_elapsed = time.time() - gen_start_time
        
        # Simple token count estimation if not provided by llama-cpp
        p_tokens = len(active_llm.tokenize(str(chat_messages).encode("utf-8")))
        c_tokens = len(active_llm.tokenize(assistant_response.encode("utf-8")))
        
        yield {
            "type": "final",
            "full_content": assistant_response,
            "elapsed": gen_elapsed,
            "tokens": {"total": p_tokens + c_tokens, "prompt": p_tokens, "completion": c_tokens}
        }
        
        # TODO: manual trace update logic needs mapping to the new API if possible, for now simplify by letting the decorator handle it

    @observe(as_type="generation")
    async def translate_response(self, text: str, target_lang: str) -> typing.AsyncGenerator[dict, None]:
        """Translates English response to target layout using the general model."""
        if not self.llm.llm_general:
            return

        logger.info(f"Translating response to {target_lang}...")
        trans_messages = [
            {"role": "system", "content": TRANSLATION_SYSTEM_MESSAGE.format(target_lang=target_lang)},
            {"role": "user", "content": f"Text to translate:\n{text}"},
        ]

        trans_stream = self.llm.llm_general.create_chat_completion(
            messages=trans_messages,
            stream=True,
            temperature=0.1,
            max_tokens=600,
            stop=["<|eot_id|>", "<|end_of_text|>"]
        )

        chinese_response = ""
        trans_start_time = time.time()

        yield {"type": "meta", "author": "Translator"}

        while True:
            chunk = await asyncio.to_thread(next, trans_stream, None)
            if chunk is None:
                break
            
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    text_chunk = delta["content"]
                    chinese_response += text_chunk
                    yield {"type": "token", "content": text_chunk}

        trans_elapsed = time.time() - trans_start_time
        tp_tokens = len(self.llm.llm_general.tokenize(str(trans_messages).encode("utf-8")))
        tc_tokens = len(self.llm.llm_general.tokenize(chinese_response.encode("utf-8")))

        yield {
            "type": "final",
            "full_content": chinese_response,
            "elapsed": trans_elapsed,
            "tokens": {"total": tp_tokens + tc_tokens, "prompt": tp_tokens, "completion": tc_tokens}
        }
        
        # TODO: manual trace update logic needs mapping to the new API if possible
