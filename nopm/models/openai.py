import openai
from pydantic import BaseModel
from typing import Literal
import logging

from .base import ModelConfig, ModelProvider

logger = logging.getLogger(__name__) 

class OpenAIClientOptions(BaseModel):
    base_url: str | None = None
    api_key: str | None = None

class OpenAIConfig(ModelConfig):
    provider: Literal["openai"] = "openai"
    client: OpenAIClientOptions
    model: str


class OpenAIProvider(ModelProvider):
    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = openai.OpenAI(
            base_url=config.client.base_url,
            api_key=config.client.api_key,
        )
    
    def generate(self, prompt: str) -> str:        
        rsp = self.client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
            model=self.config.model,
        )
        logger.debug(rsp)

        return rsp.choices[0].message.content