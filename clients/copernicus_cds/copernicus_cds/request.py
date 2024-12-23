import datetime
from calendar import monthrange
from pathlib import Path
from typing import List, get_args

import cdsapi
from copernicus_cds.schemas import CDS_Request_Variable

DEFAULT_VARIABLES = list(get_args(CDS_Request_Variable))
UK_BOUNDING_BOX = [61, -8, 49.9, 2]


def get_month_days(year: int, month: int) -> List[str]:
    """Get all days in a given month as formatted strings."""
    _, num_days = monthrange(year, month)
    return [f"{day:02d}" for day in range(1, num_days + 1)]


def validate_bounding_box(area):
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


def get_era5_month_request_dict(
    year: int,
    month: int,
    area: list[int] = UK_BOUNDING_BOX,
    variables: list[str] = DEFAULT_VARIABLES,
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
        if variable not in DEFAULT_VARIABLES:
            raise ValueError(f"Variable {variable} is not supported")

    return {
        "product_type": "reanalysis",
        "data_format": "netcdf",
        "download_format": "unarchived",
        "variable": variables,
        "year": year,
        "month": month,
        "day": get_month_days(year, month),
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


def request_era5_montly_files(
    path: Path,
    year: int,
    month: int,
    area: list[int] = UK_BOUNDING_BOX,
    variables: list[str] = DEFAULT_VARIABLES,
) -> None:
    """
    Request ERA5 monthly files from the Copernicus Climate Data Store API
    and save them to the output directory
    """

    c = cdsapi.Client()

    request_dict = get_era5_month_request_dict(year, month, area, variables)
    c.retrieve("reanalysis-era5-single-levels", request_dict, path)


if __name__ == "__main__":
    # Request ERA5 monthly files for the UK for the previous month
    last_month = datetime.date.today().replace(day=1) - datetime.timedelta(1)
    year = last_month.year
    month = last_month.month

    # time the request
    start = datetime.datetime.now()
    request_era5_montly_files(f"uk_{year}_{month}.nc", year, month)
    print("Saved files to disk", f"uk_{year}_{month}.nc")
    print(f"Request took {datetime.datetime.now() - start}")
