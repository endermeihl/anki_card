"""Processor module for file operations."""

from .file_scanner import scan_input_files, read_words_from_file, collect_words_by_file
from .file_archiver import archive_file, archive_files_with_words

__all__ = [
    "scan_input_files",
    "read_words_from_file",
    "collect_words_by_file",
    "archive_file",
    "archive_files_with_words",
]
