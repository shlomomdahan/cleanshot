from pathlib import Path
from cleanshot.llms.llm import get_inference_provider


def rename_screenshot(file_path: str) -> None:
    try:
        print(f"Renaming screenshot: {file_path}")
        path = Path(file_path).resolve()

        if not path.exists():
            print(f"Error: File not found at path: {path}")
            return

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
        else:
            print("No analysis results found.")

    except Exception as e:
        print(f"Error renaming screenshot: {e}")
