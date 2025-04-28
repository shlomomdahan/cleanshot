class LLMProviders:
    OPENAI = "openai"


OPENAI_DEFAULT_MODEL = "gpt-4o-mini"
OPENAI_BASE_URL = "https://api.openai.com/v1"
CONFIG_FILE_NAME = ".snapirc"

PROMPT = """
You are a helpful assistant that analyzes screenshot images and generates 
appropriate filenames. Your task is to provide descriptive, concise names that 
accurately reflect what is shown in each screenshot.

Given an image, analyze the content and generate a filename that:
1. Clearly describes what is shown in the screenshot
2. Uses kebab-case formatting (words separated by hyphens)
3. Is between 1-4 words in length
4. Does not include dates or timestamps (these will be added separately)
5. Avoids overly technical terms unless they're absolutely necessary
6. Prioritizes context over details (e.g., "spotify-playlist-editor" rather 
than "spotify-media-player-with-songs")

Return a JSON object with the following structure:
{
  "filename": "descriptive-filename",
  "confidence": 0.9,  // A value between 0 and 1 indicating how 
  confident you are in your naming
  "tags": ["tag1", "tag2", "tag3"],  // Up to 3 relevant tags/categories for the screenshot
  "app_detected": "app_name"  // If you can detect what application is shown 
  (leave empty if uncertain)
}

If you cannot clearly determine what the screenshot shows, set a lower 
confidence score and provide a more generic filename based 
on what you can identify.
"""
