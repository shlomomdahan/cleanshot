from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from snapi.utils import get_screenshot_directory


class ScreenshotManager:
    def __init__(self):
        self.screenshots_dir = get_screenshot_directory()
        self.screenshot_count = 0
        self.observer = None
        self.event_handler = None

    def start_monitoring(self) -> bool:
        if not self.screenshots_dir:
            print("Error: Failed to get the Screenshots directory path.")
            return False

        self.event_handler = ScreenshotHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.screenshots_dir, recursive=False)
        self.observer.start()
        return True

    def stop_monitoring(self) -> None:
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

    def increment_counter(self) -> int:
        self.screenshot_count += 1
        return self.screenshot_count


class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, manager: ScreenshotManager):
        self.manager = manager

    def on_created(self, event) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        if not event.src_path.endswith(".png"):
            return

        print(f"New screenshot detected: {event.src_path}")
        self.manager.increment_counter()

        # Wait a brief moment to ensure the file is completely written
        time.sleep(0.5)
