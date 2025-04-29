import subprocess
from cleanshot.core import ScreenshotManager
import time
import os
import signal
from pathlib import Path
import sys


class CleanShot:
    """Main application class that can run with or without GUI."""

    def __init__(self, use_gui=True):
        self.manager = ScreenshotManager()
        self.monitoring = False
        self.use_gui = use_gui
        self.pid_file = Path.home() / ".cleanshot.pid"

    def _start_monitoring(self):
        try:
            if self.manager.start_monitoring():
                self.monitoring = True
                print(
                    f"Monitoring screenshots in: "
                    f"{self.manager.screenshots_dir}"
                )
            else:
                print("Failed to start monitoring")
        except Exception as e:
            print(f"Error starting monitoring: {e}")

    def open_screenshots_folder(self, _=None):
        """Open the screenshots folder in Finder."""
        subprocess.run(["open", self.manager.screenshots_dir])

    def _save_pid(self):
        """Save the current process ID to a file."""
        with open(self.pid_file, "w") as f:
            f.write(str(os.getpid()))

    def _remove_pid_file(self):
        """Remove the PID file if it exists."""
        if self.pid_file.exists():
            self.pid_file.unlink()
            
    def _is_instance_running(self):
        """Check if another instance of CleanShot is already running."""
        if not self.pid_file.exists():
            return False
            
        try:
            with open(self.pid_file) as f:
                pid = int(f.read().strip())
                
            # Check if the process is still running
            os.kill(pid, 0)  # Send signal 0 to check if process exists
            return True
        except (ProcessLookupError, ValueError, OSError):
            # Process not found or PID file is invalid
            self._remove_pid_file()  # Clean up invalid PID file
            return False

    @classmethod
    def stop(cls):
        """Stop the running CleanShot process."""
        pid_file = Path.home() / ".cleanshot.pid"
        if not pid_file.exists():
            print("No running CleanShot process found")
            return False

        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            pid_file.unlink()
            print("CleanShot process stopped")
            return True
        except (ProcessLookupError, ValueError):
            print("No running CleanShot process found")
            pid_file.unlink()
            return False
        except Exception as e:
            print(f"Error stopping CleanShot: {e}")
            return False

    def run(self):
        # Check if another instance is already running
        if self._is_instance_running():
            print("Another instance of CleanShot is already running.")
            print("To stop it, run: cleanshot stop")
            return
            
        self._start_monitoring()
        
        self._save_pid()
        print("CleanShot is now running in the background.")
        print("To stop it, run: cleanshot stop")
        
        # Keep the process running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.manager.stop_monitoring()
            self._remove_pid_file()
            sys.exit(0)
