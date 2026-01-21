# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Anki flashcard generation system for English vocabulary learning. The system processes word lists and uses DeepSeek API to generate structured flashcards with two output types:
- **Learning cards**: Deep vocabulary analysis with etymology, phonetics, memory logic
- **Practice cards**: Three card types per word (cloze, spelling, micro-scenario)

## Architecture

### Directory Structure
```
/Anki_Auto_Builder
    /input          # Drop .txt word files here
    /processed      # Completed files moved here with timestamps
    /output         # Generated CSV files (learning_import.csv, practice_import.csv)
```

### Processing Flow
1. Scan `/input` for .txt files
2. Read words line-by-line (strip, lowercase, deduplicate)
3. Call DeepSeek API for each word
4. Write to two CSV files in `/output`
5. Archive processed files to `/processed`

### API Integration
Uses DeepSeek API with structured JSON response containing:
- `learning_data`: phonetic, meaning, source_code (etymology), assimilation, logic, note, example
- `practice_data`: cloze sentence, spelling definition, scenario context/question

### Output Formats
- `learning_import.csv`: 9 fields for Anki `English_Deep_Learning` note type
- `practice_import.csv`: 7 fields for Anki `English_Practice_Master` note type (generates 3 cards per note)
