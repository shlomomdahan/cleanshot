from cleanshot.config import config
from cleanshot.constants import LLMProviders
from cleanshot.llms.openai.provider import OpenAIProvider
from cleanshot.llms.inference_provider_base import InferenceProvider


def get_inference_provider() -> InferenceProvider:
    if config.llm_provider == LLMProviders.OPENAI:
        return OpenAIProvider()
    else:
        raise ValueError(f"Invalid LLM provider: {config.llm_provider}")
