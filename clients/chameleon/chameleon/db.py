from datetime import datetime
from pathlib import Path

import duckdb
from chameleon.generated.chameleon_pb2 import (
    PowerEvent,
    SensorEvent,
    Commodity,
    DataSource,
    Ambient,
    SensorType,
)


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

    def create_power_table(self) -> None:
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS power_events (
                event_id UUID PRIMARY KEY,
                received TIMESTAMP,
                cad_id STRING,
                commodity ENUM('elec', 'gas'),
                reading_timestamp TIMESTAMP,
                source ENUM('cad', 'dcc', 'amr'),
                reading FLOAT,
                ambient ENUM('none', 'red', 'amber', 'green'),
                event_metadata JSON
            )
            """
        )

    def create_temperature_table(self) -> None:
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS temperature_events (
                event_id UUID PRIMARY KEY,
                cloud_received_timestamp TIMESTAMP,
                cad_id STRING,
                meter_update_timestamp TIMESTAMP,
                type ENUM('cad', 'dcc', 'amr'),
                reading FLOAT,
                units STRING,
                event_metadata JSON
            )
            """
        )

    def create_humidity_table(self) -> None:
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS humidity_events (
                event_id UUID PRIMARY KEY,
                cloud_received_timestamp TIMESTAMP,
                cad_id STRING,
                meter_update_timestamp TIMESTAMP,
                type ENUM('cad', 'dcc', 'amr'),
                reading FLOAT,
                units STRING,
                event_metadata JSON
            )
            """
        )

    def insert_power_events(
        self, events: list[PowerEvent], refresh_table: bool
    ) -> None:

        received_timestamp = [datetime.fromtimestamp(e.received / 1000) for e in events]
        reading_timestamp = [
            datetime.fromtimestamp(e.reading_timestamp / 1000) for e in events
        ]

        values: list[
            tuple[str, datetime, str, str, datetime, str, float, float, dict]
        ] = [
            (
                e.event_id,
                received_timestamp[i],
                e.cad_id,
                Commodity.Name(e.source),
                reading_timestamp[i],
                DataSource.Name(e.source),
                e.reading,
                Ambient.Name(e.ambient),
                {},
            )
            for i, e in enumerate(events)
        ]

        if refresh_table:
            self.delete_table("power_events")
            self.create_power_table()

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

    def insert_sensor_events(
        self, events: list[SensorEvent], refresh_table: bool
    ) -> None:

        cloud_received_timestamp = [
            datetime.fromtimestamp(e.cloud_received_timestamp / 1000) for e in events
        ]
        meter_update_timestamp = [
            datetime.fromtimestamp(e.meter_update_timestamp / 1000) for e in events
        ]

        temperature_values: list[
            tuple[str, datetime, str, datetime, str, float, str, str, dict]
        ] = [
            (
                e.event_id,
                cloud_received_timestamp[i],
                e.cad_id,
                meter_update_timestamp[i],
                DataSource.Name(e.source),
                e.reading,
                e.units,
                {},
            )
            for i, e in enumerate(events)
            if SensorType.Name(e.type) == "temp"
        ]

        humidity_values: list[
            tuple[str, datetime, str, datetime, str, float, str, str, dict]
        ] = [
            (
                e.event_id,
                cloud_received_timestamp[i],
                e.cad_id,
                meter_update_timestamp[i],
                DataSource.Name(e.source),
                e.reading,
                e.units,
                {},
            )
            for i, e in enumerate(events)
            if SensorType.Name(e.type) == "humidity"
        ]

        if refresh_table:
            self.delete_table("temperature_events")
            self.create_temperature_table()

            self.delete_table("humidity_events")
            self.create_humidity_table()

        self.insert_temperature_events(temperature_values)
        self.insert_humidity_events(humidity_values)

        pass

    def insert_temperature_events(
        self,
        values: list[tuple[str, int, str, int, str, float, str, str, dict]],
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

    def insert_humidity_events(
        self, values: list[tuple[str, int, str, int, str, float, str, str, dict]]
    ) -> None:

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
