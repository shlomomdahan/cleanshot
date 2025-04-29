from pathlib import Path
import sys
import subprocess
import dotenv
from rich import print as printr

from cleanshot.core import CleanShot
from cleanshot.constants import CONFIG_FILE_NAME
from cleanshot.config.setup import run_setup
from cleanshot.utils import is_process_running, validate_args, show_help


def handle_setup(force=False):
    config_path = Path.home() / CONFIG_FILE_NAME

    if not config_path.exists() or force:
        run_setup()
        printr("[green]Setup complete.[/green]\n")
        return True
    return False


def start_background_process():
    pid_file = Path.home() / ".cleanshot.pid"

    if pid_file.exists():
        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
            if is_process_running(pid):
                printr("[bold yellow]CleanShot is already running.[/bold yellow]")
                return
            else:
                pid_file.unlink()
        except (ValueError, ProcessLookupError):
            pid_file.unlink()

    subprocess.Popen(
        [sys.executable, "-m", "cleanshot.main", "--background"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    printr(
        "[bold green]CleanShot is now running in the background.[/bold green]\n"
        "[bold yellow]For help run: cleanshot --help[/bold yellow]"
    )


def app():
    config_path = Path.home() / CONFIG_FILE_NAME
    args = [arg.strip() for arg in sys.argv[1:]]

    if args and not validate_args(args):
        printr("[bold red]Invalid argument[/bold red]")
        printr("[yellow]Try running [bold]--help[/bold] for more information[/yellow]")
        return

    if not args:
        if not config_path.exists():
            handle_setup()
        else:
            dotenv.load_dotenv(config_path, override=True)
            start_background_process()
        return

    if len(args) == 1:
        command = args[0]

        if command == "--background":
            dotenv.load_dotenv(config_path, override=True)
            app = CleanShot()
            app.run()

        if command == "--help":
            show_help()
            return

        if command == "--setup":
            handle_setup(force=True)
            return

        if command == "stop":
            if not CleanShot.stop():
                printr("[bold red]CleanShot is not running.[/bold red]")
            else:
                printr("[bold green]CleanShot stopped.[/bold green]")
            return


if __name__ == "__main__":
    app()
