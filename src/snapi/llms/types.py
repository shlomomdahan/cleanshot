from pydantic import BaseModel
from typing import Optional, List


class ScreenshotAnalysis(BaseModel):
    filename: str
    confidence: float
    tags: List[str]
    app_detected: Optional[str] = None
