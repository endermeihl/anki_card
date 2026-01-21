"""Main entry point for the Anki Card Generator."""

import sys
from typing import List

from config import DEEPSEEK_API_KEY
from processor.file_scanner import scan_input_files, collect_words_by_file
from processor.file_archiver import archive_files_with_words
from api.deepseek import generate_card_data
from generators.learning_csv import LearningCSVWriter
from generators.practice_csv import PracticeCSVWriter


def main() -> int:
    """Run the Anki card generation workflow.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    print("=" * 50)
    print("Anki Card Generator")
    print("=" * 50)

    # Check API key
    if not DEEPSEEK_API_KEY:
        print("\nError: DEEPSEEK_API_KEY not found!")
        print("Please create a .env file with your API key.")
        print("See .env.example for the template.")
        return 1

    # Step 1: Scan input files
    print("\n[1/5] Scanning input directory...")
    input_files = scan_input_files()

    if not input_files:
        print("No .txt files found in input directory.")
        print("Please add word list files to Anki_Auto_Builder/input/")
        return 0

    print(f"Found {len(input_files)} file(s):")
    for f in input_files:
        print(f"  - {f.name}")

    # Step 2: Collect words
    print("\n[2/5] Collecting words...")
    words, words_per_file = collect_words_by_file(input_files)
    print(f"Found {len(words)} unique word(s)")

    if not words:
        print("No words to process.")
        return 0

    # Step 3: Generate card data
    print("\n[3/5] Generating card data via DeepSeek API...")
    learning_writer = LearningCSVWriter()
    practice_writer = PracticeCSVWriter()
    failed_words: List[str] = []

    for i, word in enumerate(words, 1):
        print(f"  Processing [{i}/{len(words)}]: {word}...", end=" ")

        data = generate_card_data(word)

        if data:
            learning_data = data["learning_data"]
            practice_data = data["practice_data"]

            learning_writer.add_card(word, learning_data)
            practice_writer.add_card(
                word,
                learning_data.get("meaning", ""),
                practice_data,
            )
            print("OK")
        else:
            failed_words.append(word)
            print("FAILED")

    # Step 4: Write CSV files
    print("\n[4/5] Writing CSV files...")
    if learning_writer.count() > 0:
        learning_path = learning_writer.write()
        print(f"  Learning cards: {learning_path}")

        practice_path = practice_writer.write()
        print(f"  Practice cards: {practice_path}")
    else:
        print("  No cards to write.")

    # Step 5: Archive processed files (normalized: one word per line)
    print("\n[5/5] Archiving processed files...")
    archived = archive_files_with_words(input_files, words_per_file)
    for path in archived:
        print(f"  Archived: {path.name}")

    # Summary
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    print(f"Total words: {len(words)}")
    print(f"Successful: {learning_writer.count()}")
    print(f"Failed: {len(failed_words)}")

    if failed_words:
        print(f"\nFailed words: {', '.join(failed_words)}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
