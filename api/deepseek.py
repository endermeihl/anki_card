"""DeepSeek API client for vocabulary card generation."""

import json
import time
from typing import Optional

import requests

from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_URL,
    DEEPSEEK_MODEL,
    MAX_RETRIES,
    RETRY_DELAY,
)
from api.prompts import build_system_prompt, build_user_prompt


def generate_card_data(word: str) -> Optional[dict]:
    """Generate flashcard data for a word using DeepSeek API.

    Args:
        word: The vocabulary word to process.

    Returns:
        Dictionary containing learning_data and practice_data, or None if failed.
    """
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY not set in environment")
        return None

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(word)},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.7,
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            data = json.loads(content)

            # Validate required fields
            if "learning_data" in data and "practice_data" in data:
                return data

            print(f"Warning: Invalid response structure for '{word}'")

        except requests.exceptions.RequestException as e:
            print(f"API request failed for '{word}' (attempt {attempt + 1}): {e}")
        except json.JSONDecodeError as e:
            print(f"JSON parse error for '{word}' (attempt {attempt + 1}): {e}")
        except (KeyError, IndexError) as e:
            print(f"Response parsing error for '{word}' (attempt {attempt + 1}): {e}")

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)

    print(f"Failed to generate data for '{word}' after {MAX_RETRIES} attempts")
    return None
