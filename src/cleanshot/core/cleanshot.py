import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from cleanshot.core import ScreenshotManager
from cleanshot.utils.logging import Logger


class CleanShot:
    pid_file = Path.home() / ".cleanshot" / "cleanshot.pid"

    def __init__(self):
        self.manager = ScreenshotManager()
        self.monitoring = False
        self.logger = Logger.get_logger()

    def _start_monitoring(self):
        try:
            if self.manager.start_monitoring():
                self.monitoring = True
                self.logger.info(f"Monitoring screenshots in: {self.manager.screenshots_dir}")
            else:
                self.logger.error("Failed to start monitoring")
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}", exc_info=True)

    def open_screenshots_folder(self, _=None):
        self.logger.debug("Opening screenshots folder")
        subprocess.run(["open", self.manager.screenshots_dir])

    def _save_pid(self):
        try:
            with open(self.pid_file, "w") as f:
                f.write(str(os.getpid()))
            self.logger.debug(f"Saved PID {os.getpid()} to {self.pid_file}")
        except Exception as e:
            self.logger.error(f"Failed to save PID file: {e}", exc_info=True)

    def _remove_pid_file(self):
        if self.pid_file.exists():
            self.pid_file.unlink()
            self.logger.debug("Removed PID file")

    def _is_instance_running(self):
        if not self.pid_file.exists():
            return False

        try:
            with open(self.pid_file) as f:
                pid = int(f.read().strip())

            os.kill(pid, 0)  # Send signal 0 to check if process exists
            self.logger.debug(f"Found running instance with PID {pid}")
            return True
        except (ProcessLookupError, ValueError, OSError):
            self.logger.debug("No running instance found")
            self._remove_pid_file()
            return False

    def run(self):
        if self._is_instance_running():
            self.logger.warning("Another instance is already running")
            return

        self.logger.info("Starting CleanShot")
        self._start_monitoring()
        self._save_pid()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal")
            self.manager.stop_monitoring()
            self._remove_pid_file()
            sys.exit(0)

    @classmethod
    def stop(cls) -> bool:
        logger = Logger.get_logger()

        if not cls.pid_file.exists():
            logger.warning("No PID file found - CleanShot is not running")
            return False

        try:
            with open(cls.pid_file) as f:
                pid = int(f.read().strip())
            logger.info(f"Stopping CleanShot process {pid}")
            os.kill(pid, signal.SIGTERM)
            cls.pid_file.unlink()
            return True
        except (ProcessLookupError, ValueError):
            logger.warning("Process not found or invalid PID")
            cls.pid_file.unlink()
            return False
        except Exception as e:
            logger.error(f"Error stopping CleanShot: {e}", exc_info=True)
            return False

    @classmethod
    def start_background(cls) -> None:
        """Start CleanShot in background mode."""
        logger = Logger.get_logger()

        if cls.pid_file.exists():
            try:
                with open(cls.pid_file) as f:
                    pid = int(f.read().strip())
                os.kill(pid, 0)  # Send signal 0 to check if process exists
                logger.warning("CleanShot is already running")
                return
            except (ProcessLookupError, ValueError):
                cls.pid_file.unlink()
                logger.debug("Removed stale PID file")

        logger.info("Starting CleanShot in background mode")
        subprocess.Popen(
            [sys.executable, "-m", "cleanshot.main", "--background"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        logger.info("CleanShot started successfully in background")
