from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from cleanshot.utils import get_screenshot_directory
from .rename import rename_screenshot
import logging


class ScreenshotManager(FileSystemEventHandler):
    def __init__(self):
        self.screenshots_dir = get_screenshot_directory()
        self.observer = None
        self.is_running = False
        self.logger = logging.getLogger(__name__)

    def start_monitoring(self) -> bool:
        """Start monitoring the screenshots directory."""
        if not self.screenshots_dir:
            self.logger.error("Failed to get the Screenshots directory path.")
            return False

        if self.is_running:
            self.logger.warning("Monitoring is already running.")
            return True

        try:
            self.observer = Observer()
            self.observer.schedule(self, self.screenshots_dir, recursive=False)
            self.observer.start()
            self.is_running = True
            self.logger.info(f"Started monitoring: {self.screenshots_dir}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            return False

    def stop_monitoring(self) -> None:
        """Stop monitoring the screenshots directory."""
        if not self.is_running:
            return

        try:
            if self.observer:
                self.observer.stop()
                self.observer.join()
                self.observer = None
            self.is_running = False
            self.logger.info("Stopped monitoring screenshots directory")
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")

    def on_created(self, event) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        is_screenshot = event.src_path.endswith(".png") and ".Screenshot" in event.src_path
        if not is_screenshot:
            return

        try:
            filename = event.src_path.replace(".Screenshot", "Screenshot")
            self.logger.info(f"New screenshot detected: {filename}")
            rename_screenshot(filename)
            time.sleep(0.5)  # Small delay to ensure file is fully written
        except Exception as e:
            self.logger.error(f"Error processing screenshot: {e}")

    @property
    def status(self) -> dict:
        """Get the current status of the screenshot manager."""
        return {
            "is_running": self.is_running,
            "screenshots_dir": self.screenshots_dir,
            "observer_active": self.observer is not None,
        }
