---
title: Paralyze
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Paralyze

Paralyze is a tiny web app that analyzes your speech, detects parasite or filler words, and helps you clean up your communication.

Upload a video, select your parasite words, and get instant stats.

---

## Features

- Upload a video file
- Automatic speech to text using Whisper
- Custom list of parasite or filler words
- Simple web UI powered by Gradio
- Works locally or on a server

---

## Tech stack

- Python 3.11+
- [Gradio](https://gradio.app) for the web UI
- [MoviePy](https://zulko.github.io/moviepy/) for audio extraction
- [OpenAI Whisper](https://github.com/openai/whisper) for transcription
- PyTorch as the backend for Whisper

You also need `ffmpeg` installed on the system.

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/<your-user>/paralyze.git
cd paralyze
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python web_app.py
```

The app will be available at `http://127.0.0.1:7860`

## Usage

1. Upload a video file or provide a video URL
2. Enter comma-separated parasite words (e.g., "um, uh, like, you know")
3. Select a Whisper model (tiny, base, small, or medium)
4. Click "Analyze" to get word counts
