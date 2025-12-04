"""
Hugging Face Spaces entry point.
This file is used for deployment on Hugging Face Spaces.
For local development, use web_app.py instead.
"""
from web_app import demo

if __name__ == "__main__":
    demo.launch()

