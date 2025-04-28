from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import unicodedata
from snapi.utils import get_screenshot_directory
from .rename import rename_screenshot


class ScreenshotManager(FileSystemEventHandler):
    def __init__(self):
        self.screenshots_dir = get_screenshot_directory()
        self.observer = None

    def start_monitoring(self) -> bool:
        if not self.screenshots_dir:
            print("Error: Failed to get the Screenshots directory path.")
            return False

        self.observer = Observer()
        self.observer.schedule(self, self.screenshots_dir, recursive=False)
        self.observer.start()
        return True

    def stop_monitoring(self) -> None:
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            
    def normalize_filename(self, filename):
        """Apply comprehensive normalization to a filename."""
        normalized_path = unicodedata.normalize('NFC', filename)
        normalized_path = normalized_path.replace('\u202f', ' ').replace('\u00a0', ' ')
        
        directory = os.path.dirname(normalized_path)
        filename = os.path.basename(normalized_path)
        
        if filename.startswith('.'):
            filename = filename[1:]
            normalized_path = os.path.join(directory, filename)
            
            if os.path.exists(event.src_path):
                try:
                    os.rename(event.src_path, normalized_path)
                except Exception as e:
                    print(f"Error removing dot prefix: {e}")
                    return  
                
        if not os.path.exists(normalized_path):
            print(f"Warning: File not found at path: {normalized_path}")
            return
            
        return normalized_path
            
    def on_created(self, event) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        if not event.src_path.endswith(".png"):
            return

        normalized_path = self.normalize_filename(event.src_path)
        
        if normalized_path:
            print(f"New screenshot detected: {normalized_path}")
            rename_screenshot(normalized_path)

        time.sleep(0.5)
