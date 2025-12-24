from anthropic import Anthropic
from pydantic import BaseModel
from typing import Literal
import logging

from .base import ModelConfig, ModelProvider

logger = logging.getLogger(__name__) 

class AnthropicClientOptions(BaseModel):
    base_url: str | None = None
    api_key: str | None = None

class AnthropicConfig(ModelConfig):
    provider: Literal["anthropic"] = "anthropic"
    client: AnthropicClientOptions
    max_tokens: int
    model: str


class AnthropicProvider(ModelProvider):
    def __init__(self, config: AnthropicConfig):
        self.config = config
        self.client = Anthropic(
            base_url=config.client.base_url,
            api_key=config.client.api_key,
        )
    
    def generate(self, prompt: str) -> str:
        rsp = self.client.messages.create(
            max_tokens=self.config.max_tokens,
            model=self.config.model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
        )
        logger.debug(rsp)
        assert len(rsp.content) == 1, "Anthropic API unexpectedly returned multiple content blocks"

        return rsp.content[0].text