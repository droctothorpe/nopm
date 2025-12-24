import importlib.util
import yaml

from nopm.models.base import ModelProvider

# Check for openai sdk
if importlib.util.find_spec("openai"):
    OPENAI_AVAILABLE = True

    from .openai import OpenAIProvider, OpenAIConfig
else:
    OPENAI_AVAILABLE = False
# Check for ollama sdk
if importlib.util.find_spec("ollama"):
    OLLAMA_AVAILABLE = True
    from .ollama import OllamaProvider, OllamaConfig
else:
    OLLAMA_AVAILABLE = False
# Check for anthropic sdk
if importlib.util.find_spec("anthropic"):
    ANTHROPIC_AVAILABLE = True
    from .anthropic import AnthropicProvider, AnthropicConfig
else:
    ANTHROPIC_AVAILABLE = False

def provider_from_config_path(config_path: str) -> ModelProvider:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    return provider_from_config_data(config)

def provider_from_config_data(config_data: dict) -> ModelProvider:
    # Peak at provider type
    provider_type = config_data['provider'].lower()

    if provider_type == "openai":
        if not OPENAI_AVAILABLE:
            raise RuntimeError("Config specified OpenAI as the provider but it is not installed, use `python -m pip install openai` to install it.")
        
        config = OpenAIConfig.model_validate(config_data)
        return OpenAIProvider(config)
    elif provider_type == "ollama":
        if not OLLAMA_AVAILABLE:
            raise RuntimeError("Config specified Ollama as the provider but it is not installed, use `python -m pip install ollama` to install it.")
        
        config = OllamaConfig.model_validate(config_data)
        return OllamaProvider(config)
    elif provider_type == "anthropic":
        if not ANTHROPIC_AVAILABLE:
            raise RuntimeError("Config specified Anthropic as the provider but it is not installed, use `python -m pip install anthropic` to install it.")
        
        config = AnthropicConfig.model_validate(config_data)
        return AnthropicProvider(config)
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")