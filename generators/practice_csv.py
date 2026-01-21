"""Practice card CSV generator for Anki import."""

import csv
from pathlib import Path
from typing import List, Tuple

from config import OUTPUT_DIR, PRACTICE_CSV

# CSV fields for English_Practice_Master note type
# This note type generates 3 cards: cloze, spelling, micro-scenario
PRACTICE_FIELDS = [
    "Word",
    "Meaning",
    "Cloze_Text",
    "Cloze_Hint",
    "Spell_Def",
    "Scenario_Context",
    "Scenario_Question",
]


class PracticeCSVWriter:
    """Writer for practice card CSV files."""

    def __init__(self):
        """Initialize the CSV writer."""
        self.rows: List[Tuple] = []

    def add_card(self, word: str, meaning: str, practice_data: dict) -> None:
        """Add a practice card row.

        Args:
            word: The vocabulary word.
            meaning: Word meaning (from learning data).
            practice_data: Dictionary containing practice fields.
        """
        row = (
            word,
            meaning,
            practice_data.get("cloze_text", ""),
            practice_data.get("cloze_hint", ""),
            practice_data.get("spell_def", ""),
            practice_data.get("scenario_context", ""),
            practice_data.get("scenario_question", ""),
        )
        self.rows.append(row)

    def write(self) -> Path:
        """Write all cards to CSV file.

        Returns:
            Path to the written CSV file.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / PRACTICE_CSV

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # No header row for Anki import
            writer.writerows(self.rows)

        return output_path

    def count(self) -> int:
        """Return the number of cards added."""
        return len(self.rows)
