from src.main.res.sharedconstants import *
from src.main.res.emailAlert import send_email

import sys
import traceback
from urllib import parse


def invoke(event, context):
    logger.info('S3 Event: ' + str(event))
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        remote_filepath = parse.unquote_plus(record['s3']['object']['key'])
        size = record['s3']['object']['size']
        md5hash = record['s3']['object']['eTag']
        if '-' in md5hash or len(md5hash) != 32:
            md5hash = "File too large"

        try:
            logger.info(f'Begin Processing s3://{bucket_name}/{remote_filepath}')
            send_email("AWS", bucket_name, remote_filepath, size, md5hash, bucket=bucket_name)
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            message = f'Unexpected error while processing upload s3://{bucket_name}/{remote_filepath}, with message "{exc_value}". \
                      Stack trace follows: {"".join("!! " + line for line in lines)}'
            logger.error(message)
            raise ex
