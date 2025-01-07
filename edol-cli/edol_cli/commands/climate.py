import calendar
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from copernicus_cds.netcdf_utils import NetCDFProcessor, ProcessingConfig
from copernicus_cds.request import request_era5_files
from copernicus_cds.schemas import (
    Default_CDS_Request_Variable_List,
    Default_CDS_Request_Variables,
)
from edol_cli.commands.climate_config import config as climate_config

logger = logging.getLogger(__name__)
app = typer.Typer()


def get_days_in_month(date: datetime) -> int:
    """Get the number of days in a month."""
    return calendar.monthrange(date.year, date.month)[1]


@app.command()
def serl_fetch(
    month: Optional[datetime] = typer.Option(
        None,
        "--month",
        "-m",
        formats=["%Y-%m"],
        help="Month to be retrieverd in the format YYYY-MM",
    ),
    cache_dir: Optional[Path] = typer.Option(
        Path("cache") / "serl" / "climate",
        "--cache-dir",
        "-c",
        help="Directory to store downloaded files",
        exists=True,
        file_okay=False,
    ),
) -> None:
    """
    Generate SERL report.
    """
    if month is None:
        # first day of last month
        last_month = datetime.today().replace(day=1) - timedelta(days=1)
        last_month = last_month.replace(day=1)
        month = last_month

    logger.info(f"Generating SERL report for year {month:%Y} month {month:%B}")

    logger.debug(f"Using cache directory {cache_dir}")

    file_name = f"uk_{month:%Y}_{month:%m}.zip"

    request_era5_files(
        path=cache_dir / file_name,
        year=month.year,
        month=month.month,
    )

    logger.info(f"Saved files to disk {cache_dir / file_name}")


@app.command()
def fetch(
    parameters: List[str] = typer.Option(
        ["2m_temperature"],
        "--parameters",
        "-p",
        help=f"List of parameters to retrieve from the CDS API. One of the following: {",".join(Default_CDS_Request_Variables)}. Default is '2m_temperature_K'",
    ),
    bbox: Optional[Tuple[float, float, float, float]] = typer.Option(
        (51.3, -0.8, 51.2, -0.5),
        "--bbox",
        "-b",
        help="Bounding box for the data retrieval in the format 'lon_min,lat_min,lon_max,lat_max'. Default is '51.3,-0.8,51.2,-0.5'",
    ),
    start_date: Optional[datetime] = typer.Option(
        None,
        "--start-date",
        "-s",
        formats=["%Y-%m-%d"],
        help="Start date for the data retrieval in the format YYYY-MM-DD. Default is yesterday",
    ),
    end_date: Optional[datetime] = typer.Option(
        None,
        "--end-date",
        "-e",
        formats=["%Y-%m-%d"],
        help="End date for the data retrieval in the format YYYY-MM-DD. Default is today",
    ),
    cache_dir: Optional[Path] = typer.Option(
        Path("cache") / "serl" / "climate",
        "--cache-dir",
        "-c",
        help="Directory to store downloaded files",
        exists=True,
        file_okay=False,
    ),
) -> None:
    """
    Fetch data from the CDS API.
    """
    logger.info(f"Fetching data for parameters {parameters}")

    if not set(parameters).issubset(Default_CDS_Request_Variables):
        diffed = set(parameters) - set(Default_CDS_Request_Variables)
        logger.error(
            f"Invalid parameters {diffed}. Supported parameters are {Default_CDS_Request_Variables}"
        )
        raise typer.Exit(code=1)

    if start_date is None:
        start_date = date.today() - timedelta(days=1)

    if end_date is None:
        end_date = date.today()

    logger.info(
        f"Fetching {",".join(parameters)} data for period {start_date} to {end_date} for bbox {bbox}"
    )

    # split in months
    months = [
        start_date.replace(day=1),
    ]
    while months[-1] < end_date.replace(day=1):
        months.append((months[-1] + timedelta(days=32)).replace(day=1))

    logger.debug(f"Months to fetch: {months}")

    for i, m in enumerate(months):
        start_day = 1
        end_day = get_days_in_month(m)

        if i == 0:
            start_day = start_date.day

        if i == len(months) - 1:
            end_day = end_date.day

        days = list(range(start_day, end_day + 1))

        logger.info(f"Fetching {i+1}/{len(months)} for {m:%Y-%m}: {days}")

        bbox_str = "_".join(map(str, bbox))

        file_name = (
            f"era5_{bbox_str}_{m:%Y-%m}-{start_day:02d}_to_{m:%Y-%m}-{end_day:02d}.zip"
        )
        logger.debug(f"Saving to {cache_dir / file_name}")

        request_era5_files(
            path=cache_dir / file_name,
            year=m.year,
            month=m.month,
            day=days,
            area=bbox,
            variables=parameters,
        )


@app.command()
def serl_report(
    zip_nc_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path to the zipped netCDF file returned by the CDS API",
    ),
    output_file: Path = typer.Argument(
        None,
        help="Path to the output CSV file",
        writable=True,
        resolve_path=True,
    ),
):
    """
    Generate SERL report.
    """
    logger.info(f"Generating SERL report for file {zip_nc_file}")

    if zip_nc_file.suffix != ".zip":
        logger.error("Only zip files are supported")
        raise typer.Abort("Only zip files are supported")

    if output_file is None:
        output_file = zip_nc_file.with_suffix(".csv")

    try:
        edol_processor_config = ProcessingConfig(
            output_columns=climate_config["output_columns"],
            netcdf_field_mapping=climate_config["netcdf_field_mapping"],
            grid_cells_of_interest=climate_config["grid_cells_of_interest"],
        )
        processor = NetCDFProcessor(edol_processor_config)

        processor.process_zip_file(zip_nc_file, output_file)
        logger.info("Processing completed successfully")

    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise typer.Exit(code=1)
