from datetime import datetime, timedelta
from pprint import pprint

from chameleon.db import ChameleonDB
from chameleon.s3 import ChameleonS3Client
from chameleon.generated.chameleon_pb2 import PowerEvent, SensorEvent


def initialize_tables() -> None:

    db = ChameleonDB("chameleon.duckdb", read_only=False)

    db.delete_table("power_events")
    db.delete_table("temperature_events")
    db.delete_table("humidity_events")

    db.create_power_table()
    db.create_temperature_table()
    db.create_humidity_table()


def add_entries(date: str) -> None:

    client = ChameleonS3Client()
    db = ChameleonDB("chameleon.duckdb", read_only=False)

    event_type_counts: dict[str, int] = {}
    cad_counts: dict[str, int] = {}

    try:
        data_files = client.get_data(date)
        next(data_files)
    except KeyError:
        print(f"No data found for {date}")
        return

    for f in data_files:
        power_events: list[PowerEvent] = []
        sensor_events: list[SensorEvent] = []

        for e in f.events:
            event_type = e.WhichOneof("EventType")
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1

            if event_type == "power_event":
                power_event = e.power_event
                cad_id = power_event.cad_id + "_power"
                cad_counts[cad_id] = cad_counts.get(cad_id, 0) + 1
                power_events.append(power_event)
            elif event_type == "sensor_event":
                sensor_event = e.sensor_event
                cad_id = sensor_event.cad_id + "_sensor"
                cad_counts[cad_id] = cad_counts.get(cad_id, 0) + 1
                sensor_events.append(sensor_event)
            else:
                print(f"Unknown event type: {event_type}")
        print(
            f"Inserting {len(power_events)} power events and {len(sensor_events)} sensor events"
        )

        if power_events:
            db.insert_power_events(power_events, refresh_table=False)

        if sensor_events:
            db.insert_sensor_events(sensor_events, refresh_table=False)

    pprint(event_type_counts)
    pprint(cad_counts)


if __name__ == "__main__":
    initialize_tables()

    date_list = [
        (datetime.today() - timedelta(days=i)).strftime("%Y/%m/%d") for i in range(10)
    ]
    date_list.reverse()

    print(date_list)

    for date in date_list:
        add_entries(date)
