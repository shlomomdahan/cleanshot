import argparse
import os
import re
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import requests


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


def find_screenshots(directory: Path) -> list[Path]:
    screenshot_pattern = re.compile(r"^Screenshot.*\.png$", re.IGNORECASE)
    all_files = directory.glob("Screenshot*.png")
    return [f for f in all_files if screenshot_pattern.match(f.name)]


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
cleanshot --version    Show the current version of CleanShot
cleanshot clean <dir>  Rename all screenshots in the specified directory (e.g., '~/Desktop' or '.')
        """,
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run or re-run the setup process (will overwrite existing configuration values)",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help=argparse.SUPPRESS,  # Hidden from help output
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Cleanshot v{get_version()}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    subparsers.add_parser("stop", help="Stop a running CleanShot instance")

    clean_parser = subparsers.add_parser(
        "clean",
        help="Rename all screenshots in the specified directory (e.g., '~/Desktop' or '.')",
        description="Processes and renames screenshot files in the given directory using",
        usage="cleanshot clean <dir>",
    )
    clean_parser.add_argument("directory", help="Provide directory to cleanup")

    return parser


def get_version() -> str:
    try:
        return version("cleanshot")
    except PackageNotFoundError:
        return "unknown"


def check_latest_version(package_name: str = "cleanshot") -> str | None:
    """Check the latest version of the package on PyPI. Returns the latest version string if newer, else None."""
    try:
        resp = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=2)
        if resp.status_code == 200:
            latest = resp.json()["info"]["version"]
            if latest != get_version():
                return latest
    except Exception:
        pass
    return None
