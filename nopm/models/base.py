from abc import ABC, abstractmethod
from pydantic import BaseModel

class ModelConfig(BaseModel):
    provider: str

class ModelProvider(ABC):
    @abstractmethod
    def __init__(self, config: ModelConfig):
        pass
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass