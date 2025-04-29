import logging
from pathlib import Path

import dotenv
from rich import print as printr

from cleanshot.config.setup import run_setup
from cleanshot.constants import CONFIG_FILE_NAME
from cleanshot.core.cleanshot import CleanShot
from cleanshot.utils.logging import configure_logging
from cleanshot.utils.utils import create_parser

configure_logging()
logger = logging.getLogger(__name__)


def handle_setup() -> bool:
    config_path = Path.home() / CONFIG_FILE_NAME

    if not config_path.exists():
        logger.info("Starting initial setup")
    else:
        logger.info("Re-running setup to update configuration")

    run_setup()
    logger.info("Setup completed successfully")
    printr("[green]Setup complete.[/green]\n")
    return True


def app() -> None:
    parser = create_parser()
    args = parser.parse_args()

    config_path = Path.home() / CONFIG_FILE_NAME

    if args.setup:
        handle_setup()
        return

    if args.command == "stop":
        if not CleanShot.stop():
            printr("[bold red]CleanShot is not running.[/bold red]")
        else:
            logger.info("CleanShot stopped successfully")
            printr("[bold green]CleanShot stopped.[/bold green]")
        return

    if not config_path.exists():
        handle_setup()

    dotenv.load_dotenv(config_path, override=True)

    if args.daemon:
        app = CleanShot()
        app.run()
        return

    if CleanShot.is_running():
        printr("[bold yellow]CleanShot is already running.[/bold yellow]")
        return

    if CleanShot.run_as_daemon():
        printr(
            "[bold green]CleanShot is now running in the background.[/bold green]\n"
            "[bold yellow]For help run: cleanshot --help[/bold yellow]"
        )
    else:
        printr("[bold red]Failed to start CleanShot.[/bold red]")


if __name__ == "__main__":
    app()
