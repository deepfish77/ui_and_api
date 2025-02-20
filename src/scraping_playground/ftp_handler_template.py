from ftplib import FTP
import platform
import pysftp
import pandas as pd
from datetime import date, time, timedelta, datetime
import pytz
import calendar
import logging
import boto3

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ssm = boto3.client("ssm")
tz = pytz.timezone("US/Eastern")

try:
    FTP_USER_LOGIN = ssm.get_parameter(Name="/your_ftp_path/", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    FTP_USER_PASSWORD = ssm.get_parameter(
        Name="/your_ftp_path/password", WithDecryption=True
    )["Parameter"]["Value"]
    FTP_USER_NAME = ssm.get_parameter(
        Name="/your_ftp_path/username", WithDecryption=True
    )["Parameter"]["Value"]
    FTP_ENDPOINT = ssm.get_parameter(
        Name="/your_ftp_path/endpoint", WithDecryption=True
    )["Parameter"]["Value"]
    logger.info("Successfully fetched FTP credentials from SSM.")
except Exception as e:
    logger.error(f"Failed to fetch FTP credentials from SSM: {e}")
    raise


def connect_to_sftp_and_return_files():
    logger.info("Connecting to SFTP...")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(
            FTP_ENDPOINT,
            username=FTP_USER_NAME,
            password=FTP_USER_PASSWORD,
            port=22,
            cnopts=cnopts,
        ) as sftp:
            with sftp.cd("Inbox"):
                inbox = sftp.listdir(remotepath=".")
                logger.info(f"SFTP Inbox files: {inbox}")
                return inbox
    except Exception as e:
        logger.error(f"Failed to connect to SFTP or retrieve files: {e}")
        return []


def connect_to_ftp_and_return_files():
    logger.info("Connecting to FTP...")
    files = []
    try:
        with FTP(FTP_ENDPOINT) as ftp:
            ftp.login(user=FTP_USER_LOGIN, passwd=FTP_USER_PASSWORD)
            ftp.cwd("Inbox")
            ftp.retrlines("LIST", files.append)
            logger.info(f"FTP Inbox files: {files}")
    except Exception as e:
        logger.error(f"Failed to connect to FTP or retrieve files: {e}")
        return []
    return files


def get_from_dynamo(dyn_db_table_name, key, query_id):
    logger.info(
        f"Fetching item from DynamoDB table: {dyn_db_table_name} with key: {key}"
    )
    try:
        session = boto3.resource("dynamodb")
        table = session.Table(dyn_db_table_name)
        result = table.get_item(Key={key: query_id})
        logger.info(f"Successfully fetched item: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to fetch item from DynamoDB: {e}")
        return None


def insert_into_dyn_db(dyn_db_table_name, insert_item=None):
    if insert_item is None:
        insert_item = {"example": "val", "example3": "value"}

    logger.info(f"Inserting item into DynamoDB table: {dyn_db_table_name}")
    try:
        session = boto3.resource("dynamodb")
        table = session.Table(dyn_db_table_name)
        table.put_item(Item=insert_item)
        logger.info(f"Successfully inserted item: {insert_item}")
    except Exception as e:
        logger.error(f"Failed to insert item into DynamoDB: {e}")


def connect_to_ftp_debug():
    logger.info("Connecting to FTP in debug mode...")
    files = []
    try:
        with FTP(FTP_ENDPOINT) as ftp:
            ftp.login(user=FTP_USER_LOGIN, passwd=FTP_USER_PASSWORD)
            ftp.cwd("Inbox")
            logger.debug(f"FTP Directory List: {ftp.dir()}")
            ftp.retrlines("LIST", files.append)
            logger.info(f"Files in FTP Inbox: {files}")
    except Exception as e:
        logger.error(f"Failed to connect to FTP in debug mode: {e}")
        return []
    return files
