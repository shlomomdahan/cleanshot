import subprocess
from cleanshot.core import ScreenshotManager
import time
import os
import signal
from pathlib import Path
import sys


class CleanShot:
    def __init__(self):
        self.manager = ScreenshotManager()
        self.monitoring = False
        self.pid_file = Path.home() / ".cleanshot.pid"

    def _start_monitoring(self):
        try:
            if self.manager.start_monitoring():
                self.monitoring = True
                print(f"Monitoring screenshots in: {self.manager.screenshots_dir}")
            else:
                print("Failed to start monitoring")
        except Exception as e:
            print(f"Error starting monitoring: {e}")

    def open_screenshots_folder(self, _=None):
        subprocess.run(["open", self.manager.screenshots_dir])

    def _save_pid(self):
        with open(self.pid_file, "w") as f:
            f.write(str(os.getpid()))

    def _remove_pid_file(self):
        if self.pid_file.exists():
            self.pid_file.unlink()

    def _is_instance_running(self):
        if not self.pid_file.exists():
            return False

        try:
            with open(self.pid_file) as f:
                pid = int(f.read().strip())

            os.kill(pid, 0)  # Send signal 0 to check if process exists
            return True
        except (ProcessLookupError, ValueError, OSError):
            self._remove_pid_file()
            return False

    def run(self):
        if self._is_instance_running():
            return

        self._start_monitoring()
        self._save_pid()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.manager.stop_monitoring()
            self._remove_pid_file()
            sys.exit(0)

    @classmethod
    def stop(cls) -> bool:
        pid_file = Path.home() / ".cleanshot.pid"
        if not pid_file.exists():
            return False
        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            pid_file.unlink()
            return True
        except (ProcessLookupError, ValueError):
            pid_file.unlink()
            return False
        except Exception as e:
            print(f"Error stopping CleanShot: {e}")
            return False
