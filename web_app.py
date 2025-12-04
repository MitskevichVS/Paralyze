import os
import re
import tempfile
from collections import Counter
from urllib.parse import urlparse
from urllib.request import urlretrieve

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
    """Count how many times each parasite word/phrase appears."""
    text = text.lower()
    parasite_words = [w.lower().strip() for w in parasite_words]
    counts = {}
    
    for word in parasite_words:
        # Escape special regex characters in the word/phrase
        escaped_word = re.escape(word)
        # Use word boundaries for single words, or look for the phrase as-is for multi-word phrases
        if ' ' in word:
            # Multi-word phrase: count occurrences with word boundaries on both sides
            pattern = r'\b' + escaped_word + r'\b'
        else:
            # Single word: use word boundaries
            pattern = r'\b' + escaped_word + r'\b'
        
        matches = re.findall(pattern, text, re.IGNORECASE)
        counts[word] = len(matches)
    
    return counts


def download_video_from_url(url: str, output_path: str) -> None:
    """Download a video from a URL and save it to the output path."""
    try:
        urlretrieve(url, output_path)
    except Exception as e:
        raise ValueError(f"Failed to download video from URL: {e}")


def is_url(text: str) -> bool:
    """Check if the given text is a valid URL."""
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def process(video, video_url, words_str, model_name):
    # Check if we have either a video file or a URL
    if video is None and (video_url is None or not video_url.strip()):
        return "Please upload a video file or provide a video URL."

    parasite_words = [w.strip() for w in words_str.split(",") if w.strip()]
    if not parasite_words:
        return "Please provide at least one parasite word, comma separated."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Handle URL input
        if video is None and video_url and video_url.strip():
            if not is_url(video_url.strip()):
                return "Please provide a valid URL (e.g., https://example.com/video.mp4)."

            video_path = os.path.join(tmpdir, "downloaded_video.mp4")
            try:
                download_video_from_url(video_url.strip(), video_path)
            except Exception as e:
                return f"Error while downloading video: {e}"
        else:
            # Use uploaded video file (Gradio may return a tuple or string)
            if isinstance(video, tuple):
                video_path = video[0]  # Extract file path from tuple
            else:
                video_path = video

        audio_path = os.path.join(tmpdir, "audio.wav")

        try:
            extract_audio_from_video(video_path, audio_path)
        except Exception as e:
            return f"Error while extracting audio: {e}"

        try:
            text = transcribe_audio(audio_path, model_name=model_name)
        except Exception as e:
            return f"Error while transcribing audio: {e}"

        counts = count_parasite_words(text, parasite_words)

    lines = []
    lines.append("PARASITE WORD COUNTS:")
    lines.append("=" * 50)
    # Display counts preserving original word casing
    for w in parasite_words:
        count = counts.get(w.lower().strip(), 0)
        lines.append(f"{w}: {count}")
    total = sum(counts.values())
    lines.append("")
    lines.append(f"Total parasite words: {total}")
    return "\n".join(lines)


with gr.Blocks(title="Paralyze") as demo:
    gr.Markdown("# Paralyze")
    gr.Markdown("Analyze speech and count filler or parasite words. Upload a video file or provide a video URL.")
    
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Video file (optional if URL provided)")
            video_url = gr.Textbox(
                label="Video URL (optional if file uploaded)",
                placeholder="https://example.com/video.mp4",
            )
            words_input = gr.Textbox(
                label="Parasite words (comma separated)",
                value="um, uh, like",
            )
            model_input = gr.Dropdown(
                ["tiny", "base", "small", "medium"],
                value="small",
                label="Whisper model",
            )
            submit_btn = gr.Button("Analyze", variant="primary")
        
        with gr.Column():
            results_output = gr.Textbox(
                label="Results",
                lines=25,
                interactive=False,
            )
    
    submit_btn.click(process, [video_input, video_url, words_input, model_input], results_output)


if __name__ == "__main__":
    import sys
    
    # Check if we should enable auto-reload
    # Set DEV=0 to disable, or pass --no-reload flag
    enable_reload = os.getenv("DEV", "1") == "1" and "--no-reload" not in sys.argv
    
    if enable_reload and "--no-reload" not in sys.argv:
        # Use watchdog to watch for file changes and restart
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        import subprocess
        import time
        
        class ReloadHandler(FileSystemEventHandler):
            def __init__(self, script_path):
                self.script_path = script_path
                self.process = None
                self.last_restart = 0
                self.restart_delay = 1  # Wait 1 second before restarting
            
            def on_modified(self, event):
                if event.src_path.endswith('.py') and not event.is_directory:
                    current_time = time.time()
                    # Debounce: ignore rapid successive changes
                    if current_time - self.last_restart > self.restart_delay:
                        print(f"\n🔄 File changed: {os.path.basename(event.src_path)}")
                        print("🔄 Restarting server...")
                        self.last_restart = current_time
                        if self.process:
                            self.process.terminate()
                            self.process.wait()
                        # Restart the server
                        self.process = subprocess.Popen(
                            [sys.executable, self.script_path, "--no-reload"]
                        )
        
        script_path = os.path.abspath(__file__)
        watch_dir = os.path.dirname(script_path)
        
        event_handler = ReloadHandler(script_path)
        observer = Observer()
        observer.schedule(event_handler, path=watch_dir, recursive=False)
        observer.start()
        
        print("🚀 Starting dev server with auto-reload...")
        print("📝 Watching for file changes in:", watch_dir)
        print("💡 Set DEV=0 or use --no-reload to disable auto-reload")
        
        # Start initial server
        event_handler.process = subprocess.Popen(
            [sys.executable, script_path, "--no-reload"]
        )
        
        try:
            while True:
                time.sleep(1)
                if event_handler.process and event_handler.process.poll() is not None:
                    # Process died, exit
                    break
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            observer.stop()
            if event_handler.process:
                event_handler.process.terminate()
                event_handler.process.wait()
        observer.join()
    else:
        # Normal launch without reload
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            show_error=True,
        )
