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

---

## CI/CD and Deployment

### GitHub Actions CI

The repository includes GitHub Actions workflows for:
- **CI**: Automated testing and linting on push/PR
- **Deploy to Hugging Face Spaces**: Automatic deployment of the Gradio app
- **Deploy to GitHub Pages**: Static landing page with app information

### Deploying to Hugging Face Spaces

1. Get a Hugging Face token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Add it as a secret named `HF_TOKEN` in your GitHub repository settings
3. Push to the `main` branch - the workflow will automatically deploy

**Note**: For Hugging Face Spaces, you may need to rename `web_app.py` to `app.py` or create a symlink. Alternatively, create a `app.py` file that imports from `web_app.py`.

### GitHub Pages

GitHub Pages hosts a static landing page (since the Gradio app requires backend processing). The page is automatically deployed when you push to `main`.

To enable GitHub Pages:
1. Go to your repository Settings → Pages
2. Select "GitHub Actions" as the source
3. The workflow will automatically deploy on push to `main`

---

## Usage

1. Upload a video file or provide a video URL
2. Enter comma-separated parasite words (e.g., "um, uh, like, you know")
3. Select a Whisper model (tiny, base, small, or medium)
4. Click "Analyze" to get word counts
