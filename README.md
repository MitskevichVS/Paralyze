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
