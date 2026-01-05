# db -> postgres, pgvector
# hosting -> aws
# api -> fastapi
# RAG -> qwen 2 llm, langchain
# misc -> youtube api, ytdlp

# frontend ->
# react, tailwind, vercel
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import asyncio

app = FastAPI()

def lambda_handler(event, context):
    import json
    #from langchain.agents import create_agent
    from fastapi import FastAPI
    pass

#@app.get("/search")
async def search_method():
    from googleapiclient.discovery import build
    import os
    from dotenv import load_dotenv

   # outputs = []
    urls = set()

    load_dotenv()
    yt_api_key= os.getenv("YT_API_KEY")

    # should be replaced with search params
    input_context: dict[str, tuple] = {"artists": ("Prettifun",)}
    youtube = build("youtube", "v3", developerKey=yt_api_key)


    outputs = [search_video(f"royalty free {artist} loop kit", youtube) for artist in input_context["artists"]]
    results = await asyncio.gather(*outputs)
    print(results)

    for video in results[0]:
        url = f"https://youtube.com/watch?v={video['id']['videoId']}"
        urls.add(url)

    print(urls)
    #return results
    return urls

async def search_video(query: str, yt, max_results=1, order="date", videoDuration="short"):

    # include published after maybe
    request = yt.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video",
        order=order,
        videoDuration=videoDuration

    )

    response = await asyncio.to_thread(request.execute)

    return response["items"]



def extract_audio(video_id: str):
    import yt_dlp
    url = f"https://youtube.com/watch?v={video_id}"




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

