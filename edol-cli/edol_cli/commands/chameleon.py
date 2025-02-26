import logging

from datetime import datetime, timedelta
from typing import Optional

import typer

from edol_cli.commands.vaillant import (
    default_start_date_option,
    default_end_date_option,
)

from chameleon.data_collector import collect_data

logger = logging.getLogger(__name__)
app = typer.Typer()

name_option = typer.Option(
    None,
    "--name",
    "-n",
    help="Name to greet.",
)


@app.command()
def hello_world(name: Optional[str] = name_option) -> None:
    """Prints a greeting."""
    logger.info(f"Hello, {name}!")


@app.command()
def fetch(
    start_date: Optional[datetime] = default_start_date_option,
    end_date: Optional[datetime] = default_end_date_option,
) -> None:
    """Fetch data."""
    logger.info("Fetching data.")

    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    if start_date is None:
        start_date = yesterday

    if end_date is None:
        end_date = yesterday

    collect_data(start_date, end_date)


@app.callback()
def report() -> None:
    """EDOL CLI tool."""
    pass
