# Screenshot OCR Renamer

This application monitors your macOS Screenshots folder and automatically renames screenshots using OpenAI's OCR capabilities.

## Setup

1. Clone the repository and install the package in development mode:

```bash
git clone <repository-url>
cd screenshot-renamer
pip install -e ".[dev]"
```

2. Create a `.env` file in the project root and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

3. Run the application:

```bash
python -m screenshot_renamer
```

## Features

- Monitors the macOS Screenshots folder for new screenshots
- Uses OpenAI's OCR to extract text from screenshots
- Automatically renames files based on their content
- Preserves original files with a timestamp

## Development

The project includes development dependencies for:

- Testing (pytest)
- Code formatting (black)
- Linting (flake8)
- Type checking (mypy)

### Development Tools

## Requirements

- Python 3.8+
- OpenAI API key
- macOS (for screenshot monitoring)
