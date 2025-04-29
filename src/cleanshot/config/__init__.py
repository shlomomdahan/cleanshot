from pathlib import Path
from dotenv import dotenv_values
from cleanshot.constants import CONFIG_FILE_NAME


class Config:
    def __init__(self):
        self.config_path = Path.home() / CONFIG_FILE_NAME
        self.vals = dotenv_values(self.config_path)

    @property
    def llm_provider(self):
        return self.vals.get("LLM_PROVIDER")

    # OpenAI
    @property
    def openai_api_key(self):
        return self.vals.get("OPENAI_API_KEY")

    @property
    def openai_model(self):
        return self.vals.get("OPENAI_MODEL")


config = Config()
