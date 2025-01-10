import datetime
from calendar import monthrange
from pathlib import Path
from typing import List, Tuple, get_args

import cdsapi
from copernicus_cds.schemas import Default_CDS_Request_Variables

UK_BOUNDING_BOX = (61, -8, 49.9, 2)


def get_month_days(year: int, month: int) -> List[str]:
    """Get all days in a given month as formatted strings."""
    _, num_days = monthrange(year, month)
    return [f"{day:02d}" for day in range(1, num_days + 1)]


def validate_bounding_box(area: Tuple[int, int, int, int]):
    if len(area) != 4:
        raise ValueError("Area should be a list of 4 integers")

    if area[0] < -90 or area[0] > 90:
        raise ValueError("Latitude should be between -180 and 180")

    if area[1] < -180 or area[1] > 180:
        raise ValueError("Longitude should be between -180 and 180")

    if area[2] < -90 or area[2] > 90:
        raise ValueError("Latitude should be between -180 and 180")

    if area[3] < -180 or area[3] > 180:
        raise ValueError("Longitude should be between -180 and 180")

    if area[0] < area[2]:
        raise ValueError("Latitude should be in descending order")

    if area[1] > area[3]:
        raise ValueError("Longitude should be in ascending order")


def get_era5_request_dict(
    year: int,
    month: int,
    day: List[str] | int | None = None,
    area: Tuple[float, float, float, float] = UK_BOUNDING_BOX,
    variables: list[str] = Default_CDS_Request_Variables,
) -> dict:
    """
    Returns a dictionary to be used as the request body
    for the Copernicus Climate Data Store API for all days in given month
    """

    # validate yeart and month
    if year < 1940 or year > datetime.datetime.now().year:
        raise ValueError("Year should be between 1940 and current year")

    if month < 1 or month > 12:
        raise ValueError("Month should be between 1 and 12")

    # validate area
    validate_bounding_box(area)

    # validate variables
    for variable in variables:
        if variable not in Default_CDS_Request_Variables:
            raise ValueError(f"Variable {variable} is not supported")

    if day is None:
        # default to all days in the month
        day_list = get_month_days(year, month)
    elif isinstance(day, int):
        # one day
        if day < 1 or day > 31:
            raise ValueError("Day should be between 1 and 31")
        day_list = [f"{day:02d}"]
    elif isinstance(day, list):
        # validate the day list
        for d in day:
            if d < 1 or d > 31:
                raise ValueError("Day should be between 1 and 31")
        day_list = [f"{d:02d}" for d in day]
    else:
        raise ValueError("Day should be an integer or a list of integers or None")

    return {
        "product_type": ["reanalysis"],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "variable": variables,
        "year": year,
        "month": month,
        "day": day_list,
        "time": [
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
        ],
        "area": area,
    }


def request_era5_files(
    path: Path,
    year: int,
    month: int,
    day: List[str] | int | None = None,
    area: Tuple[float, float, float, float] = UK_BOUNDING_BOX,
    variables: list[str] = Default_CDS_Request_Variables,
) -> None:
    """
    Request ERA5 monthly files from the Copernicus Climate Data Store API
    and save them to the output directory

    Args:
    path (Path): Path to save the output files
    year (int): Year to request data for
    month (int): Month to request data for
    day (List[str] | int | None): List of days to request data for. Default is None which means all days in the month
    area (Tuple[float, float, float, float]): Bounding box for the data retrieval in the format 'lon_min,lat_min,lon_max,lat_max'. Default is UK
    variables (list[str]): List of parameters to retrieve from the CDS API. Default is the list of default variables in the copernicus_cds.schemas module
    """

    c = cdsapi.Client()

    request_dict = get_era5_request_dict(
        year=year, month=month, day=day, area=area, variables=variables
    )
    c.retrieve("reanalysis-era5-single-levels", request_dict, path)
