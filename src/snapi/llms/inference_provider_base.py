from snapi.llms.types import ScreenshotAnalysis


class InferenceProvider:
    def __init__(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_options(self, prompt: str, context: str) -> ScreenshotAnalysis | None:
        raise NotImplementedError("Subclasses must implement this method")
