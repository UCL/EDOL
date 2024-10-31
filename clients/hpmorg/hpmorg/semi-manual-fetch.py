#!/usr/bin/env python3
"""
# all users feeds
curl https://heatpumpmonitor.org/system/list/public.json > data/public.json

# retrieve user ids
cat data/public.json | jq '.[].userid' | sort -n > data/user_ids.txt

# all public feeds for users
for i in $(cat data/user_ids.txt); do curl https://heatpumpmonitor.org/timeseries/available?id=$i > data/available/$i.json; sleep 0.25; done

# remove two errors
rm data/available/31.json data/available/351.json

# a file 
for file in data/available/*.json; do
    user_id=$(basename "$file" .json)
    jq -r --arg userid "$user_id" '
        select(.feeds.heatpump_elec != null) |
        [$userid, .feeds.heatpump_elec.start_time, .feeds.heatpump_elec.end_time] | 
        @tsv
    ' "$file"
done > data/heatpump_elec.tsv

"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Iterator, Tuple
import logging
from pathlib import Path
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class HeatPumpDataCollector:
    def __init__(
        self,
        input_file: str,
        base_url: str = "https://heatpumpmonitor.org/timeseries/data",
    ):
        self.base_url = base_url
        self.users_data = pd.read_csv(
            input_file, sep="\s+", names=["user_id", "start_time", "end_time"]
        )

    def generate_date_ranges(
        self, start_timestamp: int, end_timestamp: int
    ) -> Iterator[Tuple[str, str]]:
        """Generate month-by-month date ranges in DD-MM-YYYY format."""
        start_date = datetime.fromtimestamp(start_timestamp)
        end_date = datetime.fromtimestamp(end_timestamp)

        current_date = start_date.replace(day=1)
        while current_date <= end_date:
            # Calculate the end of the current month
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_month = current_date.replace(month=current_date.month + 1)

            # Ensure we don't go past the end date
            period_end = min(next_month - timedelta(days=1), end_date)

            yield (current_date.strftime("%d-%m-%Y"), period_end.strftime("%d-%m-%Y"))

            current_date = next_month

    def fetch_data(self, user_id: int, start_date: str, end_date: str) -> dict:  # type: ignore
        """Fetch data for a specific user and date range."""
        params = {
            "id": user_id,
            "feeds": "heatpump_elec",
            "start": start_date,
            "end": end_date,
            "interval": 1800,  # 30 minutes
            "average": 1,
            "timeformat": "unix",
        }

        logging.info(f"Fetching {user_id} {start_date} - {end_date}")

        response = requests.get(self.base_url, params=params)  # type: ignore
        response.raise_for_status()
        return response.json()  # type: ignore

    def process_and_save_data(self, user_id: int, data: dict, output_dir: str) -> None:  # type: ignore
        """Process the JSON data and save to CSV in the appropriate directory."""
        if not data.get("heatpump_elec"):
            logging.warning(f"No data found for user {user_id}")
            return

        # Convert data to DataFrame
        records = []
        for timestamp, value in data["heatpump_elec"]:
            date = datetime.fromtimestamp(timestamp)
            output_path = (
                Path(output_dir) / f"year={date.year}" / f"month={date.month:02d}"
            )
            output_path.mkdir(parents=True, exist_ok=True)

            records.append({"user_id": user_id, "timestamp": timestamp, "value": value})

        if records:
            df = pd.DataFrame(records)

            # Group by year and month and save to appropriate files
            for (year, month), group in df.groupby(
                [
                    df["timestamp"].apply(lambda x: datetime.fromtimestamp(x).year),
                    df["timestamp"].apply(lambda x: datetime.fromtimestamp(x).month),
                ]
            ):
                output_path = Path(output_dir) / f"year={year}" / f"month={month:02d}"
                output_path.mkdir(parents=True, exist_ok=True)

                output_file = output_path / f"{user_id}.csv"

                # Append if file exists, otherwise create new
                if output_file.exists():
                    group.to_csv(output_file, mode="a", header=False, index=False)
                else:
                    group.to_csv(output_file, index=False)
                logging.info(f"saving to {output_file}")

    def collect_all_data(self, output_dir: str) -> None:
        """Collect data for all users and date ranges."""
        for _, row in self.users_data.iterrows():
            user_id = int(row["user_id"])
            logging.info(f"Processing user {user_id}")

            for start_date, end_date in self.generate_date_ranges(
                int(row["start_time"]), int(row["end_time"])
            ):
                try:
                    logging.info(
                        f"Fetching data for user {user_id} from {start_date} to {end_date}"
                    )
                    data = self.fetch_data(user_id, start_date, end_date)
                    self.process_and_save_data(user_id, data, output_dir)
                    time.sleep(2)  # Be nice to the server
                except Exception as e:
                    logging.error(f"Error processing user {user_id}: {str(e)}")
                    continue


def main() -> None:
    collector = HeatPumpDataCollector(
        "data/heatpump_elec.tsv", "https://heatpumpmonitor.org/timeseries/data"
    )
    collector.collect_all_data("data/hh")


if __name__ == "__main__":
    main()
