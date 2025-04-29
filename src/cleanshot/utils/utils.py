import argparse
import os
import subprocess


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
