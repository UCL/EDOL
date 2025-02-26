from datetime import datetime
from pathlib import Path

from chameleon.db import ChameleonDB


def generate_report(
    start_time: datetime,
    end_time: datetime,
    interval: str,
    output_file: Path,
    chameleon_db: ChameleonDB,
) -> None:

    if start_time > end_time:
        raise ValueError("Start time must be before end time")

    words = interval.split()

    if len(words) != 2:
        raise ValueError(f"Invalid interval... {interval}")

    if words[-1].lower() not in ["minute", "hour", "minutes", "hours"]:
        raise ValueError(
            f"Invalid interval. Must be in minutes or hours, Got {words[-1].lower()}"
        )

    if not interval.split()[-2].isdigit():
        raise ValueError(
            f"Invalid interval... The first part of the interval must be a number. {interval.split()[-2]}"
        )

    with open("binning.sql") as f:
        query = f.read().format(
            start_time=start_time.strftime("%Y-%m-%d"),
            end_time=end_time.strftime("%Y-%m-%d"),
            interval=interval,
            output_file=str(output_file),
        )

    chameleon_db.db.execute(query)


if __name__ == "__main__":

    for interval in [
        "1 minute",
        "5 minutes",
        "15 minutes",
        "30 minutes",
    ]:

        out_file = Path(f"output_{interval}.csv")

        generate_report(
            datetime(2021, 1, 1),
            datetime(2029, 1, 2),
            interval,
            out_file,
            ChameleonDB("chameleon.duckdb"),
        )
