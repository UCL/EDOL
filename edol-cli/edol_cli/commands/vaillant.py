import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Literal, Optional

import typer
from vaillant.api import VaillantApi, VaillantApiConfig

logger = logging.getLogger(__name__)
app = typer.Typer()

# Common default parameters
default_serials_argument = typer.Argument(
    None,
    help="Serial numbers of the systems. If not provided, uses VAILLANT_TEST_SERIALS env var.",
)

default_scale_option = typer.Option(
    "hourly",
    "--scale",
    "-s",
    help="Time scale for consumption data. One of: hourly (default), daily or monthly",
)

default_start_date_option = typer.Option(
    (datetime.now() - timedelta(days=1)),
    "--start-date",
    "-s",
    formats=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"],
    help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)",
)

default_end_date_option = typer.Option(
    datetime.now(),
    "--end-date",
    "-e",
    formats=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"],
    help="End date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)",
)


def get_vaillant_client(ctx: typer.Context, serials: List[str]) -> VaillantApi:
    """Helper function to create VaillantApi client using context configuration."""
    config = (
        ctx.obj.get("config.vaillant", VaillantApiConfig())
        if ctx.obj
        else VaillantApiConfig()
    )

    if not serials:
        # Fallback to environment variable if no serials provided
        env_serials = os.getenv("VAILLANT_TEST_SERIALS", "").split(",")
        if not env_serials or env_serials == [""]:
            raise typer.BadParameter(
                "No serial numbers provided. Either pass serials as arguments or set VAILLANT_TEST_SERIALS environment variable."
            )
        serials = env_serials

    return VaillantApi(config=config, serials=serials)


@app.command()
def get_consumption(
    ctx: typer.Context,
    serials: List[str] = default_serials_argument,
    scale: str = default_scale_option,
    start_date: datetime = default_start_date_option,
    end_date: datetime = default_end_date_option,
) -> None:
    """Get consumption data for specific systems."""
    client = get_vaillant_client(ctx, serials)

    for serial in client._serials:
        try:
            logger.info(f"Getting consumption data for system {serial}")
            client.get_single_consumption(
                serial=serial,
                scale=scale,
                from_datetime=start_date,
                to_datetime=end_date,
            )
            logger.info(f"Consumption data saved to cache/single_cons_{serial}.json")
        except Exception as e:
            logger.error(f"Failed to get consumption data for {serial}: {e}")


@app.command()
def get_component_consumption(
    ctx: typer.Context,
    serials: List[str] = default_serials_argument,
    scale: str = default_scale_option,
    start_date: datetime = default_start_date_option,
    end_date: datetime = default_end_date_option,
) -> None:
    """Get component-level consumption data for specific systems."""
    client = get_vaillant_client(ctx, serials)

    for serial in client._serials:
        try:
            logger.info(f"Getting component consumption data for system {serial}")
            client.get_components_consumption(
                serial=serial,
                scale=scale,
                from_datetime=start_date,
                to_datetime=end_date,
            )
            logger.info(
                f"Component consumption data saved to cache/sys_cons_{serial}.json"
            )
        except Exception as e:
            logger.error(f"Failed to get component consumption data for {serial}: {e}")


@app.command()
def get_settings(
    ctx: typer.Context,
    serials: List[str] = default_serials_argument,
    include_metadata: bool = typer.Option(
        True, "--include-metadata/--no-metadata", help="Include metadata in response"
    ),
) -> None:
    """Get system settings for specific systems."""
    client = get_vaillant_client(ctx, serials)

    for system_id in client._serials:
        try:
            logger.info(f"Getting settings for system {system_id}")
            client.get_system_settings(
                system_id=system_id,
                include_metadata=include_metadata,
            )
            logger.info(f"System settings saved to cache/sys_set_{system_id}.json")
        except Exception as e:
            logger.error(f"Failed to get system settings for {system_id}: {e}")


@app.command()
def get_topology(
    ctx: typer.Context,
    serials: List[str] = default_serials_argument,
) -> None:
    """Get system topology for specific systems."""
    client = get_vaillant_client(ctx, serials)

    for serial in client._serials:
        try:
            logger.info(f"Getting topology for system {serial}")
            client.get_topology(serial=serial)
            logger.info(f"System topology saved to cache/topology_{serial}.json")
        except Exception as e:
            logger.error(f"Failed to get system topology for {serial}: {e}")


@app.command()
def get_contract_systems(
    ctx: typer.Context,
) -> None:
    """Get all systems under the contract."""
    client = get_vaillant_client(ctx, [])
    try:
        client.get_contract_systems()
        contract_number = client._config.contract_number
        logger.info(
            f"Contract systems saved to cache/contract_systems_{contract_number}.json"
        )
    except Exception as e:
        logger.error(f"Failed to get contract systems: {e}")


@app.command()
def register_client(
    ctx: typer.Context,
    serials: List[str] = default_serials_argument,
    email: str = typer.Argument(..., help="Email address for registration"),
    country: str = typer.Option("GB", "--country", help="Country code (default: GB)"),
) -> None:
    """Register new client systems."""
    client = get_vaillant_client(ctx, serials)

    for serial in client._serials:
        try:
            logger.info(f"Registering system {serial}")
            client.register_client(
                serial=serial,
                email=email,
                country=country,
            )
            logger.info(
                f"Client registration response saved to register_client_*_{serial}.json"
            )
        except Exception as e:
            logger.error(f"Failed to register client for {serial}: {e}")


if __name__ == "__main__":
    app()
