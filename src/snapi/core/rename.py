import os
from snapi.llms.llm import get_inference_provider


def rename_screenshot(file_path: str) -> None:
    try:
        # Ensure the file exists and is accessible
        if not os.path.exists(file_path):
            print(f"Error: File not found at path: {file_path}")
            return

        # Get the directory and ensure we have write permissions
        directory = os.path.dirname(file_path)
        if not os.access(directory, os.W_OK):
            print(f"Error: No write permission in directory: {directory}")
            return

        inference_provider = get_inference_provider()
        analysis = inference_provider.analyze_image(file_path)
        
        if analysis:
            new_name = f"{analysis.filename}.png"
            new_path = os.path.join(directory, new_name)
            
            # Check if destination file already exists
            if os.path.exists(new_path):
                print(f"Warning: File already exists: {new_path}")
                return
                
            os.rename(file_path, new_path)
            print(f"Successfully renamed to: {new_name}")
        else:
            print("No analysis results found.")

    except Exception as e:
        print(f"Error renaming screenshot: {e}")
