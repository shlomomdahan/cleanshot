import logging
import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from cleanshot.utils.utils import get_screenshot_directory

from .rename import ScreenshotRenamer


class ScreenshotMonitor(FileSystemEventHandler):
    def __init__(self):
        self.screenshots_dir = get_screenshot_directory()
        self.observer = None
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        self.renamer = ScreenshotRenamer()

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
            self.logger.info(f"Monitoring screenshots in: {self.screenshots_dir}")
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

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        is_screenshot = event.src_path.endswith(".png") and ".Screenshot" in event.src_path
        if not is_screenshot:
            return

        try:
            filename = event.src_path.replace(".Screenshot", "Screenshot")
            self.logger.info(f"New screenshot detected: {filename}")
            self.renamer.rename_screenshot(filename)
            time.sleep(0.5)  # Small delay to ensure file is fully written
        except Exception as e:
            self.logger.error(f"Error processing screenshot: {e}")
