from cleanshot.config.types import (
    SetupQuestionText,
    SetupQuestionSelect,
    SetupQuestionSelectOption,
)


questions = (
    SetupQuestionText(
        name="OPENAI_API_KEY",
        prompt="Your OPENAI api key:",
        default="",
    ),
    SetupQuestionSelect(
        name="OPENAI_MODEL",
        prompt="Choose which model you would like to default to:",
        options=[
            SetupQuestionSelectOption(
                value="gpt-4o-mini", label="gpt-4o-mini", description="Good performance and speed, and cheaper"
            ),
        ],
    ),
)
