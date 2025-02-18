from pathlib import Path

import duckdb
from chameleon.generated.chameleon_pb2 import PowerEvent, SensorEvent


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
        # FIXME: This doesn't work because of timestamp. I would like to use
        # native formats as much as possible, to benefit from functions, conversions, etc.
        # so we need to find out if the event comes with milliseconds timestamp, or just seconds
        # and convert it to a proper timestamp using duckdb's TO_TIMESTAMP family of functions.
        values: list[tuple[str, int, str, str, int, str, float, float, dict]] = [
            (
                e.event_id,
                e.received,
                e.cad_id,
                e.commodity,
                e.reading_timestamp,
                e.source,
                e.reading,
                e.ambient,
                {},
            )
            for e in events
        ]

        self._db.executemany(
            """
            INSERT INTO power_events (
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
            VALUES (?, TO_TIMESTAMP(?), ?, ?, TO_TIMESTAMP(?), ?, ?, ?, ?)""",
            values,
        )

    def insert_sensor_events(self, events: list[SensorEvent]) -> None:
        values: list[tuple[str, int, str, int, str, float, str, str, dict]] = [
            (
                e.event_id,
                e.cloud_received_timestamp,
                e.cad_id,
                e.meter_update_timestamp,
                e.type,
                e.reading,
                e.source,
                e.units,
                {},
            )
            for e in events
        ]

        self._db.executemany(
            """
            INSERT INTO sensor_events (
                event_id,
                cloud_received_timestamp,
                cad_id,
                meter_update_timestamp,
                type,
                reading,
                source,
                units,
                event_metadata,                     
            )
            VALUES (?, TO_TIMESTAMP(?), ?, TO_TIMESTAMP(?), ?, ?, ?, ?, ?)""",
            values,
        )
