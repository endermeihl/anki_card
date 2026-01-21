"""File archiving utilities for processed files."""

import os
from datetime import datetime
from pathlib import Path
from typing import List

from config import PROCESSED_DIR


def archive_file(file_path: Path, words: List[str] = None) -> Path:
    """Archive a processed file with normalized format (one word per line).

    Args:
        file_path: Path to the original file.
        words: List of parsed words. If provided, writes normalized content.
               If None, just moves the original file.

    Returns:
        Path to the archived file.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = file_path.stem
    suffix = file_path.suffix
    new_name = f"{stem}_{timestamp}{suffix}"

    dest_path = PROCESSED_DIR / new_name

    if words is not None:
        # Write normalized content (one word per line)
        with open(dest_path, "w", encoding="utf-8") as f:
            for word in words:
                f.write(word + "\n")
        # Remove original file
        os.remove(file_path)
    else:
        # Just move the original file
        import shutil
        shutil.move(str(file_path), str(dest_path))

    return dest_path


def archive_files_with_words(
    files: List[Path], words_per_file: dict[Path, List[str]]
) -> List[Path]:
    """Archive multiple files with their parsed words.

    Args:
        files: List of file paths to archive.
        words_per_file: Dictionary mapping file paths to their parsed words.

    Returns:
        List of paths to archived files.
    """
    archived = []
    for f in files:
        words = words_per_file.get(f)
        archived.append(archive_file(f, words))
    return archived


def archive_files(files: List[Path]) -> List[Path]:
    """Archive multiple files (legacy, just moves files).

    Args:
        files: List of file paths to archive.

    Returns:
        List of paths to archived files.
    """
    return [archive_file(f) for f in files]
