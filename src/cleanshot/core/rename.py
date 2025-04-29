import logging
import time
from pathlib import Path

from cleanshot.llms.llm import get_inference_provider


class ScreenshotRenamer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def wait_for_file(self, path: Path, delay: float) -> tuple[bool, float]:
        if not path.exists():
            time.sleep(delay)
            return False, delay * 2
        return True, delay

    def get_new_name(self, path: Path) -> str:
        inference_provider = get_inference_provider()
        analysis = inference_provider.analyze_image(str(path))
        self.logger.info(f"Analysis: {analysis}")

        if analysis:
            return f"{analysis.filename}.png"
        return None

    def rename_file(self, path: Path, new_name: str) -> bool:
        new_path = path.parent / new_name

        if new_path.exists():
            self.logger.warning(f"Warning: File already exists: {new_path}")
            return False

        path.rename(new_path)
        self.logger.info(f"Successfully renamed to: {new_name}")
        return True

    def rename_screenshot(self, file_path: str, max_retries: int = 3, initial_delay: float = 0.5) -> None:
        path = Path(file_path).resolve()
        retry_count = 0
        current_delay = initial_delay

        while retry_count < max_retries:
            try:
                file_exists, current_delay = self.wait_for_file(path, current_delay)
                if not file_exists:
                    self.logger.warning(
                        f"File not found, retrying in {current_delay} seconds... (attempt {retry_count + 1}/{max_retries})"
                    )
                    retry_count += 1
                    continue

                self.logger.info(f"Renaming screenshot: {file_path}")

                new_name = self.get_new_name(path)
                if not new_name:
                    self.logger.warning("No analysis results found.")
                    return

                self.rename_file(path, new_name)
                return

            except Exception as e:
                self.logger.error(f"Error renaming screenshot: {e}")
                return

        self.logger.error(f"Failed to find file after {max_retries} attempts: {file_path}")
