"""File scanning utilities for reading word lists."""

from pathlib import Path
from typing import List, Set

from config import INPUT_DIR


def scan_input_files() -> List[Path]:
    """Scan the input directory for .txt files.

    Returns:
        List of Path objects for each .txt file found.
    """
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    return list(INPUT_DIR.glob("*.txt"))


def read_words_from_file(file_path: Path) -> List[str]:
    """Read words from a file.

    Supports multiple formats:
    - One word per line
    - Space-separated words on a single line
    - Tab-separated words
    - Comma-separated words
    - Any combination of the above

    Args:
        file_path: Path to the text file.

    Returns:
        List of unique words, stripped and lowercased.
    """
    import re

    words: List[str] = []
    seen: Set[str] = set()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Split by whitespace, commas, or semicolons
            tokens = re.split(r'[\s,;]+', line.strip())
            for token in tokens:
                # Clean up the token: remove punctuation at edges, keep hyphens
                word = token.strip().lower()
                # Skip empty strings and pure numbers
                # Allow words with hyphens (e.g., "ex-boyfriend")
                if word and _is_valid_word(word) and word not in seen:
                    words.append(word)
                    seen.add(word)

    return words


def _is_valid_word(word: str) -> bool:
    """Check if a string is a valid English word.

    Args:
        word: The string to check.

    Returns:
        True if it's a valid word (letters and optional hyphens).
    """
    if not word:
        return False
    # Allow letters and hyphens, but not starting/ending with hyphen
    if word.startswith('-') or word.endswith('-'):
        return False
    # Must contain at least one letter
    has_letter = any(c.isalpha() for c in word)
    # Only allow letters and hyphens
    valid_chars = all(c.isalpha() or c == '-' for c in word)
    return has_letter and valid_chars


def collect_all_words(files: List[Path]) -> List[str]:
    """Collect unique words from all input files.

    Args:
        files: List of file paths to process.

    Returns:
        List of unique words across all files.
    """
    all_words: List[str] = []
    seen: Set[str] = set()

    for file_path in files:
        words = read_words_from_file(file_path)
        for word in words:
            if word not in seen:
                all_words.append(word)
                seen.add(word)

    return all_words


def collect_words_by_file(files: List[Path]) -> tuple[List[str], dict[Path, List[str]]]:
    """Collect unique words from all input files, tracking source files.

    Args:
        files: List of file paths to process.

    Returns:
        Tuple of:
        - List of unique words across all files
        - Dictionary mapping each file to its parsed words
    """
    all_words: List[str] = []
    seen: Set[str] = set()
    words_per_file: dict[Path, List[str]] = {}

    for file_path in files:
        words = read_words_from_file(file_path)
        words_per_file[file_path] = words
        for word in words:
            if word not in seen:
                all_words.append(word)
                seen.add(word)

    return all_words, words_per_file
