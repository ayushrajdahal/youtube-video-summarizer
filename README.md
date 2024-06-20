# YouTube Video Summarizer

## Author: Ayush Raj Dahal

A TypeScript/Python-based web app that summarizes YouTube videos using their subtitles and performs sentiment analysis on the comments. Aimed to prevent clickbait content and get overall public opinion about videos and creators.

## Installation

```bash
git clone https://github.com/ayushrajdahal/youtube-video-summarizer.git
cd youtube-video-summarizer
pip install -r requirements.txt
cd frontend && npm install
```

## How to run

```bash
python3 app/app.py          # for backend
cd frontend && npm run dev  # for frontend
```

## Features

**What's implemented so far:**

- Text Summarization using the <a href="https://huggingface.co/facebook/bart-large-cnn" target="_blank">BART CNN</a> model.
- Sentiment analysis using <a href="https://textblob.readthedocs.io/en/dev/" target="_blank">TextBlob</a> (soon to be replaced by a custom model).
- Frontend using TypeScript/React.
- Backend using FastAPI.

**Plans for the future:**

- Extend this for the whole channel.
- Use a summarization model with a bigger context length + better underlying architecture, allow users to choose between models for comparison.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://github.com/ayushrajdahal/AnalyzeYT/blob/main/LICENSE)
