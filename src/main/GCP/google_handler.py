from src.main.res.sharedconstants import *
from src.main.res.emailAlert import send_email

import sys
import traceback
from urllib import parse
import base64


def invoke(event, context):
    logger.info('Google Event: ' + str(event))
    bucket_name = event["bucket"]
    remote_filepath = parse.unquote_plus(event["name"])
    md5hash = base64.standard_b64decode(event["md5Hash"].encode('UTF-8')).hex()
    size = event["size"]

    try:
        logger.info(f'Begin Processing gcp://{bucket_name}/{remote_filepath}')
        send_email("GCP", bucket_name, remote_filepath, size, md5hash, bucket=bucket_name)
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = f'Unexpected error while processing upload gcp://{bucket_name}/{remote_filepath}, with message "{exc_value}". \
                  Stack trace follows: {"".join("!! " + line for line in lines)}'
        logger.error(message)
        raise ex
