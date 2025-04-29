from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from cleanshot.utils import get_screenshot_directory
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

    def on_created(self, event) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        if not event.src_path.endswith(".png") or ".Screenshot" not in event.src_path:
            return

        filename = event.src_path.replace(".Screenshot", "Screenshot")
        print(f"New screenshot detected: {filename}")
        rename_screenshot(filename)

        time.sleep(0.5)
