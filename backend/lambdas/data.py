from datasets import load_dataset, IterableDataset
from dotenv import load_dotenv
import os
import logging
import asyncio
import requests
import json
import boto3
from botocore.exceptions import ClientError
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
import time
import soundfile as sf



def lambda_handler(event, context):

    # TODO improve error handling within these methods

    secret_name = "YT_API_KEY"
    region_name = "us-east-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-2'
    )


    try:
        get_secret_value_response = client.get_secret_value(
            SecretId='YT_API_KEY'
        )

        secret = get_secret_value_response['SecretString']
        secret_key = json.loads(secret)['YT_API_KEY']

        return {
            'statusCode': 200,
            'body': 'place main method within here ------> asyncio.run(main())'
        }

    except ClientError as e:

        return {
            'statusCode': 500,
            'body': e
        }


"""Upload a file to an S3 bucket

:param file_name: File to upload
:param bucket: Bucket to upload to
:param object_name: S3 object name. If not specified then file_name is used
:return: True if file was uploaded, else False
"""
async def upload_to_s3(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        logging.error(e)
        return False
    
    return True





"""
Downloads a list of urls to the /tmp directory of the lambda function, subsequently pastes the mp3 files into s3. 
The idea is to then send this data to the RAG model
"""
def read_jamendo_max():
    dataset = load_dataset("amaai-lab/JamendoMaxCaps", data_dir="data", split='train', streaming=True)
    return dataset

async def save_mp3_files(dataset, output_dir="mp3_files", epochs = 50):

    try: 
        os.makedirs(output_dir, exist_ok=True)

        dataset_iter = iter(dataset) 
        for epoch in range(epochs):

            data = next(dataset_iter)
            audio = data['audio']['array']


            sample_rate = data['audio']['sampling_rate']
            path = data['audio']['path']
            output_path = os.path.join(output_dir, path)

            if os.path.isfile(output_path):
                sf.write(output_path, audio, sample_rate, format='MP3')
                logging.info(f"Saved file: {output_path}")

            return {
            'statusCode': 200,
            'body': 'success!'
            }
        
    except (StopIteration, StopAsyncIteration, Exception) as e:
        logging.info('an error has occured', e)
        raise e

if __name__ == "__main__":
    dataset = read_jamendo_max()
    asyncio.run(save_mp3_files(dataset))