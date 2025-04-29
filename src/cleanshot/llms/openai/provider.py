import base64
import unicodedata
from openai import OpenAI

from cleanshot.config import config
from cleanshot.constants import OPENAI_BASE_URL, OPENAI_DEFAULT_MODEL, PROMPT
from cleanshot.llms.inference_provider_base import InferenceProvider
from cleanshot.llms.types import ScreenshotAnalysis


class OpenAIProvider(InferenceProvider):
    def __init__(self):
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set. Try running `cleanshot --setup`.")

        self.client = OpenAI(base_url=OPENAI_BASE_URL, api_key=config.openai_api_key)
        self.model = config.openai_model or OPENAI_DEFAULT_MODEL

    def encode_image(self, image_path: str) -> str:
        """Encode an image file to base64 string."""
        # Normalize the path to handle Unicode characters
        normalized_path = unicodedata.normalize("NFC", image_path)
        with open(normalized_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def analyze_image(self, image_path: str, prompt: str = PROMPT) -> str:
        """Analyze an image using GPT-4 Vision."""
        try:
            response = self.client.responses.parse(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {
                                "type": "input_image",
                                "image_url": f"data:image/png;base64,{self.encode_image(image_path)}",
                            },
                        ],
                    }
                ],
                text_format=ScreenshotAnalysis,
            )
            return response.output_parsed
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return None
