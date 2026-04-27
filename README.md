# 📺 YouTube Playlist Tracker

A Streamlit app that calculates the total duration of any YouTube playlist and tracks your progress through it.

## Project Structure

```
youtube-playlist-tracker/
├── app.py               # Streamlit UI
├── requirements.txt     # Python dependencies
├── README.md
└── utils/
    ├── __init__.py      # Public re-exports
    └── youtube.py       # Core logic (fetching, duration math, helpers)
```

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

## Features

- **Total playlist duration** — instantly see how long a playlist is
- **Progress tracking** — enter which video you're on and your timestamp
- **Flexible completion mode** — count the current video as fully watched or only up to your timestamp
- **Clean dark UI** — minimal, readable interface

## Usage

1. Paste a YouTube playlist URL
2. Optionally enter your current video index (1-based) and timestamp (`mm:ss`)
3. Choose whether to count the full current video as completed
4. Click **Calculate →**
