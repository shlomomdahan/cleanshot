import concurrent.futures
import logging
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from cleanshot.core.monitor import ScreenshotMonitor
from cleanshot.utils.utils import find_screenshots


class CleanShot:
    pid_file = Path.home() / ".cleanshot.pid"

    def __init__(self):
        self.manager = ScreenshotMonitor()
        self.monitoring = False
        self.logger = logging.getLogger(__name__)

    def _start_monitoring(self):
        try:
            if self.manager.start_monitoring():
                self.monitoring = True
            else:
                self.logger.error("Failed to start monitoring")
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}", exc_info=True)

    def _save_pid(self):
        try:
            with open(self.pid_file, "w") as f:
                f.write(str(os.getpid()))
            self.logger.debug(f"Saved PID {os.getpid()} to {self.pid_file}")
        except Exception as e:
            self.logger.error(f"Failed to save PID file: {e}", exc_info=True)

    @classmethod
    def is_running(cls) -> bool:
        """Check if CleanShot is already running."""
        if not cls.pid_file.exists():
            return False

        try:
            with open(cls.pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)  # Send signal 0 to check if process exists
            logger = logging.getLogger(__name__)
            logger.debug(f"CleanShot is running with PID {pid}")
            return True
        except (ProcessLookupError, ValueError, OSError):
            # Process doesn't exist, cleanup the pid file
            if cls.pid_file.exists():
                cls.pid_file.unlink()
            return False

    @classmethod
    def run_as_daemon(cls) -> bool:
        """Start CleanShot as a background daemon process."""

        if cls.is_running():
            return False

        try:
            cmd = [sys.executable, "-m", "cleanshot.main", "--daemon"]
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except Exception:
            return False

    def run(self):
        """Run CleanShot in daemon mode."""
        if self.is_running():
            self.logger.warning("Another instance is already running")
            return

        self.logger.info("Starting CleanShot")
        self.manager.start_monitoring()
        self._save_pid()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal")
            self.manager.stop_monitoring()
            self._cleanup_pid_file()
            sys.exit(0)

    @staticmethod
    def _process_screenshot(screenshot: Path) -> Optional[str]:
        """Process a single screenshot file."""
        try:
            from cleanshot.core.rename import ScreenshotRenamer

            renamer = ScreenshotRenamer()
            renamer.rename_screenshot(str(screenshot))
            return f"Successfully processed {screenshot.name}"

        except Exception as e:
            return f"Error processing {screenshot.name}: {e}"

    @classmethod
    def clean(cls, directory: Path) -> None:
        """Clean the screenshots in the given directory using multiple threads."""
        screenshots = find_screenshots(directory)

        if not screenshots:
            print(f"No screenshots found in {directory}")
            return

        print(f"Found {len(screenshots)} screenshots to process")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_screenshot = {
                executor.submit(cls._process_screenshot, screenshot): screenshot for screenshot in screenshots
            }

            for future in concurrent.futures.as_completed(future_to_screenshot):
                screenshot = future_to_screenshot[future]
                try:
                    result = future.result()
                    if result:
                        print(result)
                except Exception as e:
                    print(f"Exception processing {screenshot.name}: {e}")

    @classmethod
    def _cleanup_pid_file(cls) -> None:
        """Clean up the PID file if it exists."""
        if cls.pid_file.exists():
            cls.pid_file.unlink()

    @classmethod
    def stop(cls) -> bool:
        """Stop CleanShot if it's running."""
        logger = logging.getLogger(__name__)

        if not cls.pid_file.exists():
            logger.warning("Attempted to stop CleanShot but it was not running")
            return False

        try:
            with open(cls.pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            cls._cleanup_pid_file()
            return True
        except (ProcessLookupError, ValueError):
            cls._cleanup_pid_file()
            return False
        except Exception:
            return False
