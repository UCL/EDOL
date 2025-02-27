import logging

from datetime import datetime, timedelta
from typing import Optional

import typer

from edol_cli.commands.vaillant import (
    default_start_date_option,
    default_end_date_option,
)

from chameleon.db import ChameleonDB
from chameleon.data_collector import collect_data
from chameleon.report_generator import generate_report

logger = logging.getLogger(__name__)
app = typer.Typer()

# name_option = typer.Option(
#     None,
#     "--name",
#     "-n",
#     help="Name to greet.",
# )


# @app.command()
# def hello_world(name: Optional[str] = name_option) -> None:
#     """Prints a greeting."""
#     logger.info(f"Hello, {name}!")


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


@app.command()
def report(
    start_time: Optional[datetime] = default_start_date_option,
    end_time: Optional[datetime] = default_end_date_option,
    interval: str = typer.Option("1 hour", help="Interval to bin data."),
    output_file: str = typer.Option("output.csv", help="Output file."),
    chameleon_db_path: str = typer.Option(
        "chameleon.duckdb", help="Path to Chameleon DB."
    ),
) -> None:
    """Generate a report."""

    chameleon_db = ChameleonDB(chameleon_db_path)

    logger.info("Generating report.")
    generate_report(start_time, end_time, interval, output_file, chameleon_db)
