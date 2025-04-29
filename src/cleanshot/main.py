from pathlib import Path

import dotenv
from rich import print as printr

from cleanshot.config.setup import run_setup
from cleanshot.constants import CONFIG_FILE_NAME
from cleanshot.core import CleanShot
from cleanshot.utils.logging import Logger
from cleanshot.utils.utils import create_parser

logger = Logger.get_logger()


def handle_setup() -> bool:
    config_path = Path.home() / CONFIG_FILE_NAME

    if not config_path.exists():
        logger.info("Starting initial setup")
        run_setup()
        logger.info("Setup completed successfully")
        printr("[green]Setup complete.[/green]\n")
        return True
    return False


def app() -> None:
    parser = create_parser()
    args = parser.parse_args()

    config_path = Path.home() / CONFIG_FILE_NAME

    if args.setup:
        handle_setup()
        return

    # Handle stop command
    if args.command == "stop":
        if not CleanShot.stop():
            logger.warning("Attempted to stop CleanShot but it was not running")
            printr("[bold red]CleanShot is not running.[/bold red]")
        else:
            logger.info("CleanShot stopped successfully")
            printr("[bold green]CleanShot stopped.[/bold green]")
        return

    if args.background:
        logger.info("Starting CleanShot in background mode")
        dotenv.load_dotenv(config_path, override=True)
        app = CleanShot()
        app.run()
        return

    if not config_path.exists():
        handle_setup()
    else:
        dotenv.load_dotenv(config_path, override=True)
        CleanShot.start_background()
        printr(
            "[bold green]CleanShot is now running in the background.[/bold green]\n"
            "[bold yellow]For help run: cleanshot --help[/bold yellow]"
        )


if __name__ == "__main__":
    app()
