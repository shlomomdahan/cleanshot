from cleanshot.core import CleanShot
from cleanshot.constants import CONFIG_FILE_NAME
from cleanshot.config.setup import run_setup
from pathlib import Path
import dotenv
import sys
import subprocess
from cleanshot.utils import is_process_running, validate_args
from rich import print as printr


def app():
    config_path = Path.home() / CONFIG_FILE_NAME
    args = [arg.strip() for arg in sys.argv[1:]]
    
    if len(args) > 0:
        if not validate_args(args):
            printr("[bold red]Invalid argument[/bold red]")
            printr("[yellow]Try running [bold]--help[/bold] for more information[/yellow]")
            return
    
    if not config_path.exists():
        run_setup()
        printr("[green]Setup complete.[/green]\n")
        if len(args) == 1 and args[0] == "--setup":
            return
    elif len(args) == 1 and args[0] == "--setup":
        dotenv.load_dotenv(config_path, override=True)
        run_setup()
        printr("[green]Setup complete.[/green]\n")
        return
    
    if len(args) == 1 and args[0] == "--help":
        # TODO: Implement help
        # show_help()
        printr("[cyan]Help is not implemented yet.[/cyan]")
        return

    if len(args) == 1 and args[0] == "stop":
        if not CleanShot.stop():
            printr("[bold red]CleanShot is not running.[/bold red]")
        else:
            printr("[bold green]CleanShot stopped.[/bold green]")
        return

    dotenv.load_dotenv(config_path, override=True)

    if len(args) == 0:
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
            start_new_session=True
        )
        printr(
            "[bold green]CleanShot is now running in the background.[/bold green]\n"
            "[bold yellow]for help run: cleanshot --help[/bold yellow]"
        )
        return

    app = CleanShot()
    app.run()


if __name__ == "__main__":
    app()
