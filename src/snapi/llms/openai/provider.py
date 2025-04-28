import base64
import unicodedata
from openai import OpenAI, AuthenticationError

from snapi.config import config
from snapi.constants import OPENAI_BASE_URL, OPENAI_DEFAULT_MODEL, PROMPT
from snapi.llms.inference_provider_base import InferenceProvider
from snapi.llms.types import ScreenshotAnalysis


class OpenAIProvider(InferenceProvider):
    def __init__(self):
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set. Try running `snapi --setup`.")

        self.client = OpenAI(base_url=OPENAI_BASE_URL, api_key=config.openai_api_key)
        self.model = config.openai_model or OPENAI_DEFAULT_MODEL

    def encode_image(self, image_path: str) -> str:
        """Encode an image file to base64 string."""
        # Normalize the path to handle Unicode characters
        normalized_path = unicodedata.normalize('NFC', image_path)
        with open(normalized_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def get_options(self, prompt: str, context: str) -> ScreenshotAnalysis | None:
        try:
            assembled_prompt = PROMPT.format(prompt=prompt, context=context)
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[{"role": "user", "content": assembled_prompt}],
                response_format=ScreenshotAnalysis,
            )
            return response.choices[0].message.parsed
        except AuthenticationError:
            print("Error: There was an error with your OpenAI API key. You can change it by running `snapi --setup`.")
            return

    def analyze_image(self, image_path: str, prompt: str = PROMPT) -> str:
        """Analyze an image using GPT-4 Vision."""
        try:
            base64_image = self.encode_image(image_path)
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        ],
                    }
                ],
                response_format=ScreenshotAnalysis,
            )
            return response.choices[0].message.parsed
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return None
