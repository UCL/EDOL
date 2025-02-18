import os
from pprint import pprint
from typing import Generator

import boto3
import boto3.s3
from generated.chameleon_pb2 import Metadata

DEFAULT_AWS_BUCKET = "edol-chameleon-pilot-bucket"


class ChameleonS3Client:
    def __init__(self, bucket: str = os.getenv("AWS_BUCKET", DEFAULT_AWS_BUCKET)):
        self.client = boto3.client("s3", region_name="eu-west-2")
        self.bucket_name = bucket

    def parse_prorobuf(self, s3_file_path: str) -> Metadata:
        response = self.client.get_object(Bucket=self.bucket_name, Key=s3_file_path)

        obj = response["Body"].read()

        metadata = Metadata()
        metadata.ParseFromString(obj)

        return metadata

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
                    yield self.parse_prorobuf(file["Key"])
                else:
                    continue


# Example usage
if __name__ == "__main__":
    event_type_counts: dict[str, int] = {}
    cad_counts: dict[str, int] = {}

    client = ChameleonS3Client()
    for f in client.get_data("2025/02/18/11"):
        for e in f.events:
            event_type = e.WhichOneof("EventType")
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1

            if event_type == "power_event":
                power_event = e.power_event
                cad_id = power_event.cad_id
                cad_counts[cad_id] = cad_counts.get(cad_id, 0) + 1
            elif event_type == "sensor_event":
                sensor_event = e.sensor_event
                cad_id = sensor_event.cad_id
                cad_counts[cad_id] = cad_counts.get(cad_id, 0) + 1
            else:
                print(f"Unknown event type: {event_type}")

    pprint(event_type_counts)
    pprint(cad_counts)
