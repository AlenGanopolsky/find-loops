
# from fastapi import FastAPI
# from dotenv import load_dotenv
import asyncio
import boto3
from botocore.exceptions import ClientError

# secrets should live in AWS Secrets Manager


def lambda_handler(event, context):

    secret_name = "YT_API_KEY"
    region_name = "us-east-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        secret = get_secret_value_response['SecretString']
        return {
            'statusCode': 200,
            'body': asyncio.run(search_method({'x': ()}, secret))
        }


    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        return {
            'statusCode': 500,
            'body': e
        }

    
async def search_method(input: dict[str, tuple[str]], api_key: str):
    from googleapiclient.discovery import build
 #   import os
    # from dotenv import load_dotenv
    import logging

    try:

        urls = set()

        yt_api_key = api_key

        # should be replaced with search params that come from the lambda
        input_context: dict[str, tuple] = {"artists": ("Prettifun",)}
        youtube = build("youtube", "v3", developerKey=yt_api_key)


        outputs = [search_video(f"royalty free {artist} loop kit", youtube) for artist in input_context["artists"]]
        results = await asyncio.gather(*outputs)
        logging.info(results)

        for video in results[0]:
            url = f"https://youtube.com/watch?v={video['id']['videoId']}"
            urls.add(url)

        logging.info(urls)
        

        # turn this into a json at some point
        return urls
    
    except Exception as e:
        print('here')
        raise e

async def search_video(query: str, yt, max_results=2, videoDuration="short") -> dict[str]:
    import logging

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

