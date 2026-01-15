# a microservice that takes the downloaded, parsed yt audio files and places them in s3 -> which is then going to be used by the RAG model in a separate pipeline
# all code for downloading yt videos, parsing them, and sending them to s3 is done here

import os
import logging
import json
from pytubefix import YouTube
from pytubefix.cli import on_progress
import asyncio

# TODO increase memory cap for /tmp directory
async def lambda_handler(event, context):
    
    """
    Downloads a list of urls to the /tmp directory of the lambda function, subsequently pastes the mp3 files into s3. 
    The idea is to then send this data to the RAG model
    """
    try:

        # storage size of /tmp directory is 512mb -> can change this later
        url_dir = "/tmp"
        bucket_name = "rag-project-bucket-dev"

        urls = event["urls"]
        for url in urls:
            await asyncio.to_thread(download_file(url))
        
        filenames = [f for f in os.listdir(url_dir) if f.endswith(('.mp3', '.m4a', '.webm'))]

        for filename in filenames:
            upload_file(os.path.join(url_dir, filename), bucket_name) 

        
        return {
         'statusCode': 200,
         'body': json.dumps('Success!')
        }
    
    except Exception as e:
        logging.error(e)


def download_file(url: str, download_dir = "/tmp"):
    try:
        download_dir = r"C:\Users\aleng\test_url"

        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)

        ys = yt.streams.get_audio_only()
        ys.download(output_path=f"{download_dir}")
        print("success!")
    
    except Exception as e:
        raise e



async def upload_file(file_name, bucket, object_name=None):

    import logging
    import boto3
    from botocore.exceptions import ClientError
    import os


    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Process the content as needed
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = await s3_client.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        logging.error(e)
        return False
    
    return True



if __name__ == "__main__":
    download_file("https://youtu.be/3_aRc1NUj0g?si=N8CN0w1whknHmDy2")