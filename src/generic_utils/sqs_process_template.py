import json
import os
import logging
from datetime import datetime
import pandas as pd
import boto3

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ssm = boto3.client("ssm")
sqs = boto3.client("sqs", region_name="us-east-1")

try:
    ACCESS_SECRET = ssm.get_parameter(
        Name="/you_secret_parameter_path", WithDecryption=True
    )["Parameter"]["Value"]
    logger.info("Successfully fetched ACCESS_SECRET from SSM.")
except Exception as e:
    logger.error(f"Failed to fetch ACCESS_SECRET from SSM: {e}")
    ACCESS_SECRET = None

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/your_queue_url"


def get_csv_from_s3(bucket_name, file_name):
    try:
        s3_client = boto3.client("s3")
        local_path = "/tmp/csv_tmp"
        s3_client.download_file(bucket_name, file_name, local_path)
        logger.info(
            f"Downloaded CSV file {file_name} from bucket {bucket_name} to {local_path}"
        )
    except Exception as e:
        logger.error(f"Failed to download file from S3: {e}")
        raise


def upload_document_s3_teamplte(
    download_date, object_id, file_path, metadata, content_bucket
):
    try:
        s3 = boto3.resource("s3")
        s3_client = boto3.client("s3")

        content_file = f"{download_date}/{object_id}"
        metadata_file = f"{download_date}/{object_id}"

        s3_client.upload_file(file_path, content_bucket, content_file)
        s3.Object(content_bucket, metadata_file).put(Body=json.dumps(metadata))
        os.remove(file_path)
        logger.info(
            f"Uploaded file {file_path} and metadata to S3 bucket {content_bucket}"
        )
    except Exception as e:
        logger.error(f"Failed to upload file or metadata to S3: {e}")
        raise


def write_values_into_file(line, file_path):
    try:
        with open(file_path, "a") as f:
            if line is not None:
                f.write(line)
        logger.info(f"Successfully wrote line to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write to file {file_path}: {e}")
        raise


def sqs_message_provider(event, _):
    dms_docs = "/tmp/your_temp_file_path"

    try:
        content_df = pd.read_csv(dms_docs, encoding="latin-1")
        logger.info(
            f"Loaded CSV file into DataFrame with columns: {content_df.columns}"
        )
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        return

    # Limit data for testing
    content_df = content_df[:10]
    logger.info(f"Processing {len(content_df)} records.")

    for _, document in content_df.iterrows():
        try:
            object_id = str(document["object_id"])
            attribute_1 = str(document["attribute_1"])
            attribute_2 = str(document["attribute_2"])
            a_time_attribute = (
                datetime.strptime(document["publication_time"], "%Y-%m-%d %H:%M:%S.%f")
                .date()
                .strftime("%Y-%m-%d")
            )

            response = sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageAttributes={
                    "object_id": {"DataType": "String", "StringValue": object_id},
                    "attribute_1": {"DataType": "String", "StringValue": attribute_1},
                    "attribute_2": {"DataType": "String", "StringValue": attribute_2},
                    "a_time_attribute": {
                        "DataType": "String",
                        "StringValue": a_time_attribute,
                    },
                },
                MessageBody=("message_body"),
            )
            logger.info(f"Sent message to SQS with object_id: {object_id}")
        except Exception as e:
            logger.error(
                f"Failed to send message to SQS for object_id {object_id}: {e}"
            )

    return {"Message Status": "Messages processed"}


def sqs_message_handler(event, _):
    try:
        logger.info("Received SQS message event.")
        logger.debug(f"Event content: {json.dumps(event)}")

        properties = event["Records"][0]["body"]
        attribute_1 = event["Records"][0]["messageAttributes"]["attribute_1"][
            "stringValue"
        ]
        attribute_2 = event["Records"][0]["messageAttributes"]["attribute_2"][
            "stringValue"
        ]
        attribute_3 = event["Records"][0]["messageAttributes"]["attribute_3"][
            "stringValue"
        ]

        logger.info("Extracted message attributes successfully.")
        logger.info(f"Properties: {properties}")
        logger.info(f"Attribute 1: {attribute_1}")
        logger.info(f"Attribute 2: {attribute_2}")
        logger.info(f"Attribute 3: {attribute_3}")

    except KeyError as e:
        logger.error(f"KeyError while processing SQS message: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
