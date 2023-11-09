import streamlit as st
from collections import Counter
import requests
import matplotlib.pyplot as plt
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
from textblob import TextBlob
import plotly.express as px
# from config import youtube_api_key, huggingface_api_key
import os

youtube_api_key, huggingface_api_key = st.secrets['youtube_api_key'], st.secrets['huggingface_api_key']
# youtube_api_key, huggingface_api_key = os.getenv('YT_API_KEY'), os.getenv('HF_API_KEY')

# credentials for huggingface
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {huggingface_api_key}"}

# credentials for youtube v3
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = youtube_api_key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# streamlit page config

st.set_page_config(page_title="AnalyzeYT")

# hides footer & header components

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        #GithubIcon {
        visibility: hidden;
        }
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def get_id(url):

    if 'youtu.be' in url:
        videoId = url.split('youtu.be/')[1]
        videoId = videoId.split('?')[0]
    else:
        videoId = url.split('?v=')[1]
        videoId = videoId.split('&')[0]
    
    return videoId

# streamlit components
def get_title(url):
    request = youtube.videos().list(
        part="snippet",
        id=get_id(url)
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']

    # get duration of video
    

def get_summary(url):
    yt_id = get_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(yt_id)
    inputtext = ' '.join([tt['text'] for tt in transcript]).replace('\n', " ")

    output = query({
    "inputs": inputtext,
    })

    return output[0]['summary_text']

def plotly_pie_chart(url):

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=get_id(url),
        maxResults=500
    )
    response = request.execute()

    comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]
    polarities = [TextBlob(comment).sentiment.polarity for comment in comments]
    sentiments = ['Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral' for polarity in polarities]

    df = pd.DataFrame(list(zip(comments, sentiments)), columns=['Comment', 'Sentiment'], index=range(1, len(comments)+1))
    
    sentiment_data = pd.Series(sentiments)

    counter = Counter(sentiment_data)
    labels = list(counter.keys())
    values = list(counter.values())
    fig = px.pie(values=values, names=labels, hole=.3, title='Comment Section Sentiment Analysis:')
    return fig, df

# streamlit main app

st.title('AnalyzeYT')

st.write('Summarizes a YouTube video using its transcript and performs sentiment analysis on the comments.')

url = st.text_input('Enter URL:')

if url:
    if 'youtube.com' and 'youtu.be' not in url:
        st.warning('Please enter a valid YouTube video URL.')
    
    st.markdown(f'**Video Title:**')
    title = get_title(url)
    # st.write(f'{title} (Duration: {duration}')
    st.write(f'{title}')

    st.markdown('**Summary:**')
    try:
        st.write(get_summary(url))         # temporarily removed for avoiding huggingface API call
    except Exception as e:
        st.warning('This video doesn\'t have transcript/subtitles enabled.')
    
    try:
        fig, df = plotly_pie_chart(url)
        st.plotly_chart(fig, use_container_width=True)

        # Use st.expander to create a collapsible section
        with st.expander("See Comments", expanded=False):
            st.dataframe(df)
    except Exception as e:
        st.warning('This video doesn\'t have comments enabled.')