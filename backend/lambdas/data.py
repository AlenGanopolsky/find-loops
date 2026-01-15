from datasets import load_dataset, IterableDataset
import os
import logging
import asyncio
import json
import boto3
from botocore.exceptions import ClientError
import soundfile as sf
import aioboto3



# initializes secret manager
region = 'us-east-2'
api_key = 'HF_API_KEY'

session = boto3.session.Session()
client = session.client(
        service_name='secretsmanager',
        region_name=f'{region}'
)

get_secret_value_response = client.get_secret_value(
            SecretId=f'api_key'
)

secret = get_secret_value_response['SecretString']
secret_key = json.loads(secret)[f'api_key']
s3_client = boto3.client('s3', region_name=region)


def lambda_handler(event, context):


    # TODO improve error handling within these methods

    try:

        asyncio.run(main())

        return {
            'statusCode': 200,
            'body': 'lambda has ran successfully!'
        }

    except ClientError as e:

        return {
            'statusCode': 500,
            'body': e
        }
    
async def main():
    try:

        dataset = read_jamendo_max()
        paths = save_mp3_files(dataset, s3_client)['body']

        tasks = [asyncio.create_task(upload_to_s3(path)) for path in paths]
        await asyncio.gather(*tasks)


    except Exception as e:
        logging.error(e)
        raise e



# """Upload a file to an S3 bucket

# :param file_name: File to upload
# :param bucket: Bucket to upload to
# :param object_name: S3 object name. If not specified then file_name is used
# :return: True if file was uploaded, else False
# """
async def upload_to_s3(file_name, bucket="rag-project-bucket-dev", object_name=None):

    session = aioboto3.Session()
    try:

        async with session.client('s3', region_name=region) as s3_client:
            await s3_client.upload_file(file_name, bucket, object_name)

        return {
            'statusCode': 200,
            'body': 'success!'
        }


    except ClientError as e:
        logging.error(e)
        raise e
    
    
"""
Downloads a list of urls to the /tmp directory of the lambda function, subsequently pastes the mp3 files into s3. 
The idea is to then send this data to the RAG model
"""
def read_jamendo_max():

    # TODO use token = secret_key
    dataset = load_dataset("amaai-lab/JamendoMaxCaps", data_dir="data", split='train', streaming=True)
    return dataset



async def save_mp3_files(dataset, output_dir="mp3_files", epochs = 50):

    paths = []

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
                paths.append(output_path)
                logging.info(f"Saved file: {output_path}")

            return {
            'statusCode': 200,
            'body': f'{paths}'
            }
        
    except Exception as e:
        logging.info('an error has occured', e)
        raise e



if __name__ == "__main__":
    dataset = read_jamendo_max()
    asyncio.run(save_mp3_files(dataset))