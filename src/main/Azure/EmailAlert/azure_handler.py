from res.sharedconstants import *
from res.emailAlert import send_email

import sys
import traceback
from urllib import parse
from hashlib import md5

import azure.functions
import azure.storage.blob


def invoke(event: azure.functions.InputStream):
    logger.info(f"New event: {event}")
    url = event.uri
    url = parse.unquote_plus(url)
    size = event.length
    hashhex = md5(event.read()).hexdigest()
    blob_obj = azure.storage.blob.BlobClient.from_blob_url(url)
    account_name = blob_obj.account_name
    container_name = blob_obj.container_name
    remote_filepath = blob_obj.blob_name
    logger.info(f'Azure Event: {container_name}/{remote_filepath} was uploaded')
    try:
        logger.info(f'Begin Processing {url}')
        send_email("Azure", f"{account_name}/{container_name}", remote_filepath, size, hashhex)
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = f'Unexpected error while processing upload {container_name}/{remote_filepath}, with message \"{exc_value}\". \
                  Stack trace follows: {"".join("!! " + line for line in lines)}'
        logger.error(message)
        raise ex
