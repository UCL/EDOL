import os
import logging
from typing import Generator

import boto3
import boto3.s3
from chameleon.generated.chameleon_pb2 import Metadata

DEFAULT_AWS_BUCKET = "edol-chameleon-pilot-bucket"
logger = logging.getLogger(__name__)


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

            if "Contents" not in page:
                logger.info(f"No files found for {prefix}")
                exit()
                continue

            for file in page["Contents"]:
                if file["Key"].endswith(extension):
                    for metadata in self.parse_protobuf(file["Key"]):
                        yield metadata
                else:
                    continue
