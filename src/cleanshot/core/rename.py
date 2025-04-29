from pathlib import Path
import time
from cleanshot.llms.llm import get_inference_provider


def rename_screenshot(file_path: str, max_retries: int = 3, initial_delay: float = 0.5) -> None:
    path = Path(file_path).resolve()
    retry_count = 0
    current_delay = initial_delay

    while retry_count < max_retries:
        try:
            if not path.exists():
                print(
                    f"File not found, retrying in {current_delay} seconds... (attempt {retry_count + 1}/{max_retries})"
                )
                time.sleep(current_delay)
                current_delay *= 2  # Exponential backoff
                retry_count += 1
                continue

            print(f"Renaming screenshot: {file_path}")
            inference_provider = get_inference_provider()
            analysis = inference_provider.analyze_image(str(path))
            print(f"Analysis: {analysis}")

            if analysis:
                new_name = f"{analysis.filename}.png"
                new_path = path.parent / new_name

                if new_path.exists():
                    print(f"Warning: File already exists: {new_path}")
                    return

                path.rename(new_path)
                print(f"Successfully renamed to: {new_name}")
                return
            else:
                print("No analysis results found.")
                return

        except Exception as e:
            print(f"Error renaming screenshot: {e}")
            return

    print(f"Failed to find file after {max_retries} attempts: {file_path}")
