
# from fastapi import FastAPI
# from dotenv import load_dotenv
import asyncio
import boto3
from botocore.exceptions import ClientError
import json
import logging
from googleapiclient.discovery import build



# input should look like {"artists": (str, str, str..., str)}
def lambda_handler(event, context):

    # need to grab context dict from lambda_handler for using instead of manual
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
            'body': asyncio.run(search_method({"artists": ("Prettifun",)}, secret_key))
        }

    except ClientError as e:

        return {
            'statusCode': 500,
            'body': e
        }

    
async def search_method(input: dict[str, tuple[str]], api_key: str):

    try:

        urls = []
     #   input_context: dict[str, tuple] = {"artists": ("Prettifun",)}


        youtube = build("youtube", "v3", developerKey=api_key)


        outputs = [search_video(f"royalty free {artist} loop kit", youtube) for artist in input["artists"]]
        results = await asyncio.gather(*outputs)
        logging.info(results)

        for video in results[0]:
            url = f"https://youtube.com/watch?v={video['id']['videoId']}"
            urls.append(url)

        logging.info(urls)
        
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": urls,
        }),
        }

    except Exception as e:
        print('here')
        raise e

async def search_video(query: str, yt, max_results=2, videoDuration="short") -> dict[str]:

    try: 
        # include published after maybe
        request = yt.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video",
            videoDuration=videoDuration

        )

        response = await asyncio.to_thread(request.execute)
        print(response)

        return response["items"]
    
    except Exception as e:
        print('here2')
        raise e


















# TECH STACK

# Langchain (Modal), MongoDB, Pinecone, Gemini API for storing credentials and metadata
# React, Tailwind for frontend
# Vercel for deployment
# GitHub Actions, Docker, Terraform (if needed) for CICD

# will be turned into a langchain method, should be async

#####################################################################

# what type of files are we parsing?

