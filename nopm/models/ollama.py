from datetime import timedelta
import ollama
from typing import Literal
import logging

from pydantic_core.core_schema import str_schema

from .base import ModelConfig, ModelProvider

logger = logging.getLogger(__name__) 

class OllamaConfig(ModelConfig):
    provider: Literal["ollama"] = "ollama"
    model: str
    method: Literal["chat", "generate"] = "generate"


class OllamaProvider(ModelProvider):
    def __init__(self, config: OllamaConfig):
        self.config = config
    
    def generate(self, prompt: str) -> str:  
        # https://docs.ollama.com/api/chat
        if self.config.method == "chat":
            return self._chat(prompt)
        elif self.config.method == "generate":
            return self._generate(prompt)
        
        raise ValueError(f"Unknown method: {self.config.method}")
    
    def _generate(self, prompt: str) -> str:
        # https://docs.ollama.com/api/generate
        response = ollama.generate(
            model=self.config.model,
            prompt=prompt,
        )

        logger.debug(response)
        self._stat(response)

        return response.response
    
    def _chat(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.config.model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt 
                }
            ]
        )

        logger.debug(response)
        self._stat(response)

        return response['message']['content']
    
    def _stat(self, rsp: ollama.ChatResponse | ollama.GenerateResponse):
        def _or_na(duration: float | None):
            if duration is None:
                return "N/A"
            td = timedelta(milliseconds=duration // 1000)
            return str(td)

        info = {
            "total_duration": _or_na(rsp.total_duration),
            "load_duration": _or_na(rsp.load_duration),
            "prompt_eval_duration": _or_na(rsp.prompt_eval_duration),
            "eval_duration": _or_na(rsp.eval_duration),
        }

        logger.info("Generation statistics:")
        for key, value in info.items():
            logger.info(f" {key}: {value}")