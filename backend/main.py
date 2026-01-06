# db -> postgres, pgvector
# hosting -> aws
# api -> fastapi
# RAG -> qwen 2 llm, langchain
# misc -> youtube api, ytdlp

# frontend ->
# react, tailwind, vercel
from fastapi import FastAPI
from dotenv import load_dotenv
import asyncio



def lambda_handler(event, context):
    return asyncio.run(search_method())
    

#@app.get("/search")
async def search_method():
    from googleapiclient.discovery import build
    import os
    from dotenv import load_dotenv
    import logging
    import json

    try:

    # outputs = []
        urls = set()

        load_dotenv()
        yt_api_key= os.getenv("YT_API_KEY")

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

        return urls
    
    except Exception as e:
        print('here')
        logging.error(e)

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
        logging.info(response)

        return response["items"]
    
    except Exception as e:
        print('here2')
        logging.error(e)



if __name__ == "__main__":
    result = asyncio.run(search_method())
    print(f"Returned result: {result}")


















# TECH STACK

# Langchain (Modal), MongoDB, Pinecone, Gemini API for storing credentials and metadata
# React, Tailwind for frontend
# Vercel for deployment
# GitHub Actions, Docker, Terraform (if needed) for CICD

# will be turned into a langchain method, should be async

#####################################################################

# what type of files are we parsing?

