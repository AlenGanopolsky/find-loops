
# a microservice that takes the downloaded, parsed yt audio files and places them in s3 -> which is then going to be used by the RAG model in a separate pipeline
# all code for downloading yt videos, parsing them, and sending them to s3 is done here





def upload_file(file_name, bucket, object_name=None):

    import logging
    import aiboto3
    from botocore.exceptions import ClientError
    import os


    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True