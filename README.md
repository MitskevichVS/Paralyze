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

1. **Create a Hugging Face account** (if you don't have one): [https://huggingface.co/join](https://huggingface.co/join)

2. **Create the Space manually** (required first step):
   - Go to [https://huggingface.co/new-space](https://huggingface.co/new-space)
   - Set the **Owner** to your username
   - Set the **Space name** to `paralyze`
   - Select **SDK**: `Gradio`
   - Select **Hardware**: `CPU Basic` (free tier)
   - Click **Create Space**

3. **Get a Hugging Face token**:
   - Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Click **New token**
   - Name it (e.g., "github-actions")
   - Select **Role**: `Write` (important!)
   - Click **Generate a token**
   - Copy the token immediately

4. **Add the token to GitHub**:
   - Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `HF_TOKEN`
   - Value: paste your Hugging Face token
   - Click **Add secret**

5. **Push to deploy**:
   - Push your code to the `main` branch
   - The workflow will automatically deploy your app to the Space

**Note**: The `app.py` file is already set up for Hugging Face Spaces compatibility.

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
