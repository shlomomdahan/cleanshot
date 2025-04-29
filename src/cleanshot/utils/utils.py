import argparse
import os
import subprocess
from pathlib import Path


def read_screencapture_location() -> Path | None:
    try:
        loc = subprocess.check_output(
            ["defaults", "read", "com.apple.screencapture", "location"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return Path(loc).expanduser()
    except subprocess.CalledProcessError:
        return None


def get_screenshot_directory() -> Path:
    loc = read_screencapture_location()

    if loc is not None:
        loc = loc.resolve()
        if loc.exists():
            return loc

    desktop = Path.home() / "Desktop"
    desktop.mkdir(exist_ok=True)
    return desktop.resolve()


def is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError):
        return False


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CleanShot - Automatically rename screenshots using OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            cleanshot              Start CleanShot in background mode
            cleanshot stop         Stop a running CleanShot instance
            cleanshot --setup      Run or re-run the setup process (overwrites existing configuration)
        """,
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help=argparse.SUPPRESS,  # Hidden from help output
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run or re-run the setup process (will overwrite existing configuration values)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    subparsers.add_parser("stop", help="Stop a running CleanShot instance")

    return parser
