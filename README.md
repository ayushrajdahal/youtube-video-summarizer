# AnalyzeYT

## Author: Ayush Raj Dahal

A python-based web app that summarizes YouTube videos using their subtitles and performs sentiment analysis on the comments. Aimed to prevent clickbait content and get overall public opinion about videos and creators.

## Installation

```bash
git clone https://github.com/ayushrajdahal/AnalyzeYT.git
cd AnalyzeYT
pip install -r requirements.txt
```

## How to run

```bash
python3 app/app.py
```

## File Structure

```bash
.
├── app
│   └── app.py          # main app
└── requirements.txt    # dependencies
```

## Features

**What's implemented so far:**

- Text Summarization using the <a href="https://huggingface.co/facebook/bart-large-cnn" target="_blank">BART CNN</a> model.
- Sentiment analysis using <a href="https://textblob.readthedocs.io/en/dev/" target="_blank">TextBlob</a> (soon to be replaced by a custom model).
- Backend using FastAPI.

**Plans for the future:**

- Extend this for the whole channel.
- Use a summarization model with a bigger context length + better underlying architecture, allow users to choose between models for comparison.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://github.com/ayushrajdahal/AnalyzeYT/blob/main/LICENSE)
