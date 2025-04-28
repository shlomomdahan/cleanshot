from snapi.llms.types import OptionsResponse


class InferenceProvider:
    def __init__(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_options(prompt: str, context: str) -> OptionsResponse | None:
        raise NotImplementedError("Subclasses must implement this method")
