from pydantic import BaseModel


class ScreenshotAnalysis(BaseModel):
    filename: str
    confidence: float
