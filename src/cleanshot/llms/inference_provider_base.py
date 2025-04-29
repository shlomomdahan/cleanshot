from cleanshot.llms.types import ScreenshotAnalysis


class InferenceProvider:
    def __init__(self):
        raise NotImplementedError("Subclasses must implement this method")

    def analyze_image(self, image_path: str) -> ScreenshotAnalysis | None:
        raise NotImplementedError("Subclasses must implement this method")
