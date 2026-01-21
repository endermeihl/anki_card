"""Learning card CSV generator for Anki import."""

import csv
from pathlib import Path
from typing import List, Tuple

from config import OUTPUT_DIR, LEARNING_CSV

# CSV fields for English_Deep_Learning note type
# Note: Tags is the last column for Anki tag import
LEARNING_FIELDS = [
    "Word",
    "Phonetic",
    "Meaning",
    "SourceCode",
    "Assimilation",
    "Logic",
    "Collocations",  # 搭配差异，不同句式对应不同中文含义
    "Note",
    "Example_En",
    "Example_Cn",
    "Tags",  # 词缀标签，空格分隔
]


class LearningCSVWriter:
    """Writer for learning card CSV files."""

    def __init__(self):
        """Initialize the CSV writer."""
        self.rows: List[Tuple] = []

    def add_card(self, word: str, learning_data: dict) -> None:
        """Add a learning card row.

        Args:
            word: The vocabulary word.
            learning_data: Dictionary containing learning fields.
        """
        row = (
            word,
            learning_data.get("phonetic", ""),
            learning_data.get("meaning", ""),
            learning_data.get("source_code", ""),
            learning_data.get("assimilation", ""),
            learning_data.get("logic", ""),
            learning_data.get("collocations", ""),  # 搭配差异
            learning_data.get("note", ""),
            learning_data.get("example_en", ""),
            learning_data.get("example_cn", ""),
            learning_data.get("tags", ""),  # 词缀标签
        )
        self.rows.append(row)

    def write(self) -> Path:
        """Write all cards to CSV file.

        Returns:
            Path to the written CSV file.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / LEARNING_CSV

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # No header row for Anki import
            writer.writerows(self.rows)

        return output_path

    def count(self) -> int:
        """Return the number of cards added."""
        return len(self.rows)
