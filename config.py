"""Configuration settings for the Anki Card Generator."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Working directories
ANKI_DIR = BASE_DIR / "Anki_Auto_Builder"
INPUT_DIR = ANKI_DIR / "input"
OUTPUT_DIR = ANKI_DIR / "output"
PROCESSED_DIR = ANKI_DIR / "processed"

# Output file names
LEARNING_CSV = "learning_import.csv"
PRACTICE_CSV = "practice_import.csv"

# API settings
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
