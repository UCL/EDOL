import os
from pprint import pprint
from typing import Generator

import boto3
import boto3.s3
from chameleon.generated.chameleon_pb2 import Metadata, PowerEvent, SensorEvent

DEFAULT_AWS_BUCKET = "edol-chameleon-pilot-bucket"


class ChameleonS3Client:
    def __init__(self, bucket: str = os.getenv("AWS_BUCKET", DEFAULT_AWS_BUCKET)):
        self.client = boto3.client("s3", region_name="eu-west-2")
        self.bucket_name = bucket

    def parse_protobuf(self, s3_file_path: str) -> list[Metadata]:
        response = self.client.get_object(Bucket=self.bucket_name, Key=s3_file_path)
        raw_bytes = response["Body"].read()

        messages = []
        while raw_bytes:
            metadata = Metadata()
            try:
                # ParseFromString returns the number of bytes read for this message
                bytes_read = metadata.ParseFromString(raw_bytes)
                messages.append(metadata)
                raw_bytes = raw_bytes[
                    bytes_read:
                ]  # Move to the next message in the buffer
            except Exception as e:
                print(f"Failed to parse protobuf message: {e}")
                break

        return messages

    def get_data(
        self, prefix: str, extension: str = ".pb"
    ) -> Generator[Metadata, None, None]:
        """
        List all files in the bucket with the given prefix and extension. Use empty string as extension to list all files.
        """
        paginator = self.client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
        for page in page_iterator:
            for file in page["Contents"]:
                if file["Key"].endswith(extension):
                    for metadata in self.parse_protobuf(file["Key"]):
                        yield metadata
                else:
                    continue


# Example usage
if __name__ == "__main__":
    from chameleon.db import ChameleonDB

    refresh_power_table = True
    refresh_sensor_table = True

    client = ChameleonS3Client()
    db = ChameleonDB("chameleon.duckdb", read_only=False)

    event_type_counts: dict[str, int] = {}
    cad_counts: dict[str, int] = {}

    for f in client.get_data("2025/02/18/17"):
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
            db.insert_power_events(power_events, refresh_table=refresh_power_table)
            refresh_power_table = False

        if sensor_events:
            db.insert_sensor_events(sensor_events, refresh_table=refresh_sensor_table)
            refresh_sensor_table = False

    pprint(event_type_counts)
    pprint(cad_counts)
