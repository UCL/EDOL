import logging
from pathlib import Path
from typing import Annotated

import typer
from edol_cli.commands import climate, version
from edol_cli.config import Config

APP_NAME = "edol-glowmarkt"
app = typer.Typer()

logger = logging.getLogger(__name__)

app.add_typer(climate.app, name="climate")
app.add_typer(version.app, name="version")


@app.callback()
def main(
    ctx: typer.Context,
    config: Annotated[
        Path | None,
        typer.Option(
            help="Path to the configuration file.",
            show_default="edol-config.toml",
            show_choices=True,
        ),
    ] = None,
    debug: Annotated[
        bool | None,
        typer.Option(
            help="Set logging level higher and print debug information.",
        ),
    ] = None,
) -> None:
    """
    EDOL Glowmarkt CLI tool.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s\t| %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if debug:
        logger.debug("Debug mode enabled.")
    else:
        logger.setLevel(logging.INFO)

    c = Config(config_toml_path=config)

    if isinstance(debug, bool):
        c.debug = debug


if __name__ == "__main__":
    app()
