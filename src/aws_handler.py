from res.sharedconstants import *
from res.pgpDecrypt import process_file

import os
import sys
import traceback
from os.path import join, isfile
from urllib import parse
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
S3 = boto3.resource('s3')


def move_on_s3(dest_folder: str, bucket: str, key: str):
    download_filename = trim_path_to_filename(key)
    new_key = join(dest_folder, download_filename)
    logger.info('move original file to ' + new_key)
    S3.Object(bucket, new_key).copy_from(CopySource=f'{bucket}/{key}')
    logger.info('deleting original upload file')
    S3.Object(bucket, key).delete()


def download_file_on_s3(bucket: str, key: str):
    download_filepath = join(DOWNLOAD_DIR, trim_path_to_filename(randomize_filename(key)))
    logger.info(f'downloading s3://{bucket}/{key} to {download_filepath}')
    # try:
    S3.Object(bucket, key).download_file(download_filepath)
    # except ClientError as e:
    #     error_code = int(e.response['Error']['Code'])
    #     if error_code == 404:
    #         exists = False
    #         logger.warning(f'Attempt to download s3://{bucket}/{key} failed, it was not found. \
    #         Most likely file was already processed.')
    #     else:
    #         raise e
    return download_filepath


# download the private encryption key from s3
def download_asc_on_s3():
    logger.info(f'Attempting to download key from s3://{PGP_KEY_LOCATION}/{ASC_REMOTE_KEY}')
    buffer = BytesIO()
    S3.Object(PGP_KEY_LOCATION, ASC_REMOTE_KEY).download_fileobj(buffer)
    buffer.seek(0)
    import_result = gpg.import_keys(buffer.read().decode('UTF-8'))
    length = buffer.tell()
    buffer.seek(0)
    buffer.write(b"\0"*length)
    buffer.close()
    logger.info(f'key import result fingerprint: {", ".join(import_result.fingerprints)}')


def copy_file_on_s3(local_filepath: str, bucket: str, remote_filepath: str):
    logger.info(f'Uploading: {local_filepath} to {bucket}/{remote_filepath}')
    S3.Object(bucket, remote_filepath).upload_file(local_filepath)


# Filepath here is the full path including folders and the filename (and extension) of the remote file
# Store file in error directory
def error_on_s3(bucket: str, filepath: str):
    if ERROR:
        move_on_s3('error/', bucket, filepath)


# Archive and delete the file
def archive_on_s3(bucket: str, filepath: str):
    if ARCHIVE:
        move_on_s3('archive/', bucket, filepath)


def invoke(event, context):
    logger.debug('S3 Event: ' + str(event))
    create_folder_if_not_exists(DOWNLOAD_DIR)
    create_folder_if_not_exists(DECRYPT_DIR)
    create_folder_if_not_exists(LOCAL_UNZIPPED_DIR)
    create_folder_if_not_exists(LOCAL_READY_DIR)
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        remote_filepath = parse.unquote_plus(record['s3']['object']['key'])

        if not remote_filepath.endswith(('.pgp', '.gpg')):
            logger.info(f'File {remote_filepath} is not an encrypted file... Skipping')
            continue

        if ARCHIVE and remote_filepath.startswith('archive/'):
            logger.debug('Archive event triggered... Skipping')
            continue
        elif ERROR and remote_filepath.startswith('error/'):
            logger.debug('Error event triggered... Skipping')
            continue

        try:
            logger.info(f'Begin Processing s3://{bucket}/{remote_filepath}')

            if '.' not in remote_filepath:
                logger.info(f'Skipping processing of folder {remote_filepath}')
                continue
            elif int(record['s3']['object']['size']) == 0:
                logger.info(f'File {remote_filepath} is a placeholder file... Skipping')
                continue

            local_filepath = download_file_on_s3(bucket, remote_filepath)
            download_asc_on_s3()
            local_filepath = process_file(local_filepath)
            # copy ready files to s3 ready bucket
            logger.info('Uploading file')
            dest_remote_filepath = os.path.splitext(remote_filepath)[0]
            copy_file_on_s3(local_filepath, DECRYPTED_DONE_LOCATION, dest_remote_filepath)
            archive_on_s3(bucket, remote_filepath)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            message = f'Unexpected error while processing upload s3://{bucket}/{remote_filepath}, with message "{exc_value}". \
                      The file has been moved to the error folder. Stack trace follows: {"".join("!! " + line for line in lines)}'
            logger.error(message)
            error_on_s3(bucket, remote_filepath)
            return 'failure.'
    return 'success.'
