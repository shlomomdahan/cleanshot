from cleanshot.ui.menu import ScreenshotMonitorApp
from cleanshot.constants import CONFIG_FILE_NAME
from cleanshot.config.setup import run_setup
from pathlib import Path
import dotenv
import sys


def app():
    config_path = Path.home() / CONFIG_FILE_NAME
    args = [arg.strip() for arg in sys.argv[1:]]
    if not config_path.exists():
        run_setup()
        print("Setup complete...\n")
        if len(args) == 1 and args[0] == "--setup":
            return
    elif len(args) == 1 and args[0] == "--setup":
        dotenv.load_dotenv(config_path, override=True)
        run_setup()
        print("Setup complete...\n")
        return

    dotenv.load_dotenv(config_path, override=True)

    app = ScreenshotMonitorApp()
    app.run()


if __name__ == "__main__":
    app()
