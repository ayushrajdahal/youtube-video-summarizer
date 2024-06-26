import os, re, json
from fastapi import FastAPI
from collections import Counter
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from textblob import TextBlob
from pytube.extract import video_id
import googleapiclient.discovery
import googleapiclient.errors


app = FastAPI()


# credentials for huggingface
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
huggingface_api_key = os.environ['HF_API_KEY']
headers = {"Authorization": f"Bearer {huggingface_api_key}"}


# credentials for youtube v3
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ['YT_API_KEY']


youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


@app.get("/")
def read_root():
    return {"message": "Welcome to AnalyzeYT API!"}


@app.get("/video/{video_id}")
def get_video_info(video_id: str):
    try:
        title = get_title(video_id)
        summary = get_summary(video_id)
        fig, df = plotly_pie_chart(video_id)
        return {
            "title": title,
            "summary": summary,
            "chart": fig.to_json(),
            "comments": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}


def get_title(yt_id):
    request = youtube.videos().list(
        part="snippet",
        id=yt_id
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']


def get_summary(yt_id):
    transcript = YouTubeTranscriptApi.get_transcript(yt_id)
    inputtext = ' '.join([tt['text'] for tt in transcript]).replace('\n', " ")

    output = query({
        "inputs": inputtext,
    })

    return output[0]['summary_text']


def plotly_pie_chart(yt_id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=yt_id,
        maxResults=500
    )
    response = request.execute()

    comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]
    comments = list(map(lambda x: re.sub(r'<.*?>', '', x), comments))  # Remove content enclosed in <>
    comments = [comment.replace("&#39;", "'").replace("&quot;", '"') for comment in comments]  # Replace &#39; with ' and &quot; with "
    
    polarities = [TextBlob(comment).sentiment.polarity for comment in comments]
    sentiments = ['Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral' for polarity in polarities]

    table_json = json.dumps(list(zip(comments, sentiments)), columns=['Comment', 'Sentiment'], index=range(1, len(comments) + 1))
    
    return table_json