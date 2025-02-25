from datetime import datetime
from pathlib import Path
from typing import Any

import duckdb
from chameleon.generated.chameleon_pb2 import (
    Ambient,
    Commodity,
    DataSource,
    PowerEvent,
    SensorEvent,
    SensorType,
    SensorUnits,
)

type PowerEventRecord = tuple[
    str, datetime, str, str, datetime, str, float, str, dict[str, Any]
]

type TemperatureRecord = tuple[
    str, datetime, str, datetime, str, float, str, str, dict[str, Any]
]

type HumidityRecord = tuple[
    str, datetime, str, datetime, str, float, str, str, dict[str, Any]
]


class ChameleonDB:
    def __init__(self, db_path: str | Path, read_only: bool = False):
        db_path_exists = Path(db_path).exists()

        if read_only and not db_path_exists:
            raise ValueError(
                f"Database file {db_path} does not exist and read_only is True"
            )

        self._db = duckdb.connect(db_path, read_only=read_only)
        if not db_path_exists:
            with open(Path(__file__).parent / "schema.sql") as f:
                self._db.execute(f.read())

    def insert_power_events(self, events: list[PowerEvent]) -> None:

        received_timestamps = [
            datetime.fromtimestamp(e.received / 1000) for e in events
        ]
        reading_timestamps = [
            datetime.fromtimestamp(e.reading_timestamp / 1000) for e in events
        ]

        values: list[PowerEventRecord] = [
            (
                e.event_id,
                received_timestamps[i],
                e.cad_id,
                Commodity.Name(e.source),
                reading_timestamps[i],
                DataSource.Name(e.source),
                e.reading,
                Ambient.Name(e.ambient),
                {},
            )
            for i, e in enumerate(events)
        ]

        self._db.executemany(
            """
            INSERT OR IGNORE INTO power_events (
                event_id,
                received,
                cad_id,
                commodity,
                reading_timestamp,
                source,
                reading,
                ambient,
                event_metadata                       
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            values,
        )

    def insert_temperature_events(
        self,
        values: list[TemperatureRecord],
    ) -> None:

        self._db.executemany(
            """
            INSERT OR IGNORE INTO temperature_events (
                event_id,
                cloud_received_timestamp,
                cad_id,
                meter_update_timestamp,
                type,
                reading,
                units,
                event_metadata                    
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            values,
        )

    def insert_humidity_events(self, values: list[HumidityRecord]) -> None:

        self._db.executemany(
            """
            INSERT OR IGNORE INTO humidity_events (
                event_id,
                cloud_received_timestamp,
                cad_id,
                meter_update_timestamp,
                type,
                reading,
                units,
                event_metadata                    
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            values,
        )

    def insert_sensor_events(self, events: list[SensorEvent]) -> None:

        cloud_received_timestamp = [
            datetime.fromtimestamp(e.cloud_received_timestamp / 1000) for e in events
        ]
        meter_update_timestamp = [
            datetime.fromtimestamp(e.meter_update_timestamp / 1000) for e in events
        ]

        temperature_values: list[TemperatureRecord] = [
            (
                e.event_id,
                cloud_received_timestamp[i],
                e.cad_id,
                meter_update_timestamp[i],
                DataSource.Name(e.source),
                e.reading,
                SensorUnits.Name(e.units),
                SensorType.Name(e.type),
                {},
            )
            for i, e in enumerate(events)
            if SensorType.Name(e.type) == "temp"
        ]

        humidity_values: list[HumidityRecord] = [
            (
                e.event_id,
                cloud_received_timestamp[i],
                e.cad_id,
                meter_update_timestamp[i],
                DataSource.Name(e.source),
                e.reading,
                SensorUnits.Name(e.units),
                SensorType.Name(e.type),
                {},
            )
            for i, e in enumerate(events)
            if SensorType.Name(e.type) == "humidity"
        ]

        self.insert_temperature_events(temperature_values)
        self.insert_humidity_events(humidity_values)
