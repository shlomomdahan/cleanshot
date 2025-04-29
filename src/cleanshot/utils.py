import subprocess
import os
from typing import List
from cleanshot.constants import ACCEPTED_ARGS


def validate_args(args: List[str]) -> bool:
    if len(args) != 1:
        return False
    return args[0] in ACCEPTED_ARGS


def get_screenshot_directory() -> str:
    try:
        result = subprocess.run(
            ["defaults", "read", "com.apple.screencapture", "location"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if result.returncode == 0 and result.stdout.strip():
            print(f"Using custom location: {result.stdout.strip()}")
            return result.stdout.strip()

        default_location = os.path.expanduser("~/Desktop")
        if os.path.exists(default_location):
            print(f"Using default location: {default_location}")
            return default_location

    except Exception as e:
        print(f"Error: {e}")
        return os.getcwd()


def is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError):
        return False


def show_help():
    """Display help information about available commands."""
    help_text = """
    [bold cyan]cleanshot CLI Commands:[/bold cyan]
    
    [bold]cleanshot[/bold]              - Start cleanshot in background mode
    [bold]cleanshot stop[/bold]         - Stop a running cleanshot instance
    [bold]cleanshot --setup[/bold]      - Run or re-run the setup process
    [bold]cleanshot --help[/bold]       - Show this help information
    """
    printr(help_text)
