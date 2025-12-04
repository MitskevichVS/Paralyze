import os
import re
import tempfile
from collections import Counter

import gradio as gr
from moviepy.editor import VideoFileClip
import whisper

# Cache Whisper models so they are not reloaded on every request
MODEL_CACHE = {}


def get_model(model_name: str = "small"):
    if model_name not in MODEL_CACHE:
        MODEL_CACHE[model_name] = whisper.load_model(model_name)
    return MODEL_CACHE[model_name]


def extract_audio_from_video(video_path: str, audio_path: str) -> None:
    """Extract audio track from a video file and save as WAV."""
    clip = VideoFileClip(video_path)
    audio = clip.audio
    if audio is None:
        raise ValueError("Video has no audio track.")
    audio.write_audiofile(audio_path, logger=None)
    clip.close()


def transcribe_audio(audio_path: str, model_name: str = "small") -> str:
    """Transcribe audio file to text using Whisper."""
    model = get_model(model_name)
    result = model.transcribe(audio_path)
    return result["text"]


def count_parasite_words(text: str, parasite_words):
    """Count how many times each parasite word appears."""
    text = text.lower()
    tokens = re.findall(r"\b\w+\b", text)
    counts = Counter(tokens)
    parasite_words = [w.lower() for w in parasite_words]
    return {w: counts.get(w, 0) for w in parasite_words}


def process(video, words_str, model_name):
    if video is None:
        return "Please upload a video."

    parasite_words = [w.strip() for w in words_str.split(",") if w.strip()]
    if not parasite_words:
        return "Please provide at least one parasite word, comma separated."

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.wav")

        try:
            extract_audio_from_video(video, audio_path)
        except Exception as e:
            return f"Error while extracting audio: {e}"

        try:
            text = transcribe_audio(audio_path, model_name=model_name)
        except Exception as e:
            return f"Error while transcribing audio: {e}"

        counts = count_parasite_words(text, parasite_words)

    lines = [f"{w}: {counts.get(w.lower(), 0)}" for w in parasite_words]
    total = sum(counts.values())
    lines.append("")
    lines.append(f"Total parasite words: {total}")
    return "\n".join(lines)


demo = gr.Interface(
    fn=process,
    inputs=[
        gr.Video(label="Video file"),
        gr.Textbox(
            label="Parasite words (comma separated)",
            value="um, uh, like",
        ),
        gr.Dropdown(
            ["tiny", "base", "small", "medium"],
            value="small",
            label="Whisper model",
        ),
    ],
    outputs=gr.Textbox(label="Results"),
    title="Paralyze",
    description="Analyze speech and count filler or parasite words.",
)


if __name__ == "__main__":
    # In Codespaces we listen on 0.0.0.0 so the forwarded port works
    demo.launch(server_name="0.0.0.0", server_port=7860)
