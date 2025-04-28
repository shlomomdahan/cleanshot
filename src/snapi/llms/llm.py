from snapi.config import config
from snapi.constants import LLMProviders
from snapi.llms.openai.provider import OpenAIProvider
from snapi.llms.inference_provider_base import InferenceProvider


def get_inference_provider() -> InferenceProvider:
    if config.llm_provider == LLMProviders.OPENAI:
        return OpenAIProvider()
    else:
        raise ValueError(f"Invalid LLM provider: {config.llm_provider}")
