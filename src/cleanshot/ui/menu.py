import rumps
from cleanshot.core import ScreenshotManager
import os
import subprocess
import threading


class ScreenshotMonitorApp(rumps.App):
    """Main application menu bar interface."""

    def __init__(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "menubar-icon.svg")
        super().__init__("Screenshot Monitor", icon=icon_path)
        self.manager = ScreenshotManager()
        self.monitoring = False

        # Start monitoring in a separate thread
        threading.Thread(target=self._start_monitoring, daemon=True).start()

    def _start_monitoring(self):
        """Start monitoring in a background thread."""
        try:
            if self.manager.start_monitoring():
                self.monitoring = True
                print(f"Monitoring screenshots in: {self.manager.screenshots_dir}")
            else:
                print("Failed to start monitoring")
        except Exception as e:
            print(f"Error starting monitoring: {e}")

    @rumps.clicked("Open Screenshots Folder")
    def open_screenshots_folder(self, _):
        """Open the screenshots directory in Finder."""
        subprocess.run(["open", self.manager.screenshots_dir])
