import streamlit as st
from collections import Counter
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
from textblob import TextBlob
import plotly.express as px
from htbuilder import HtmlElement, div, hr, a, p, img, styles
from htbuilder.units import percent, px as ht_px
from  pytube.extract import video_id

youtube_api_key, huggingface_api_key = st.secrets['youtube_api_key'], st.secrets['huggingface_api_key']

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


# streamlit components
def get_title(yt_id):
    request = youtube.videos().list(
        part="snippet",
        id=yt_id
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']

    # get duration of video
    

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
    polarities = [TextBlob(comment).sentiment.polarity for comment in comments]
    sentiments = ['Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral' for polarity in polarities]

    df = pd.DataFrame(list(zip(comments, sentiments)), columns=['Comment', 'Sentiment'], index=range(1, len(comments)+1))
    
    sentiment_data = pd.Series(sentiments)

    counter = Counter(sentiment_data)
    labels = list(counter.keys())
    values = list(counter.values())
    fig = px.pie(values=values, names=labels, hole=.3, title='Comment Section Sentiment Analysis:')
    return fig, df

# app title

# st.markdown("<h1 style='text-align: center;'>AnalyzeYT</h1>", unsafe_allow_html=True)
st.title('AnalyzeYT')

st.write('Summarizes YouTube videos using their subtitles and performs sentiment analysis on the comments.')


# footer stuff

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=ht_px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="auto",
    )

    style_hr = styles(
        display="block",
        margin=ht_px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=ht_px(0)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made with ❤️ by ",
        link("https://ayushraj.com.np/", "Ayush Raj Dahal"),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()


# main app

url = st.text_input('Enter video URL:')

if url:
    try:
        yt_id = video_id(url)
    except Exception as e:
        st.warning('Please enter a valid YouTube video URL.')
        st.stop()
    
    st.markdown(f'**Video Title:**')
    with st.spinner('Getting video title...'):
        title = get_title(yt_id)
    # st.write(f'{title} (Duration: {duration}')
    st.write(f'{title}')

    st.markdown('**Summary:**')
    try:
        with st.spinner('Summarizing the video...'):
            st.write(get_summary(yt_id))         # temporarily removed for avoiding huggingface API call
    except Exception as e:
        st.warning('This video doesn\'t have transcript/subtitles enabled.')
    
    try:
        with st.spinner('Loading` comment section sentiment analysis...'):
            fig, df = plotly_pie_chart(yt_id)
            st.plotly_chart(fig, use_container_width=True)

            # Use st.expander to create a collapsible section
            with st.expander("See Comments", expanded=False):
                st.dataframe(df)
    except Exception as e:
        st.warning('This video doesn\'t have comments enabled.')