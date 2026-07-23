# GameLLM-DataForge
A distributed data processing pipeline for LLM pre-training, focusing on code data, general web text, and game-domain text.

The project simulates the critical steps in industry-standard pre-training data processing:

- Data schema standardization
- Rule-based text & HTML cleaning
- AST-based code cleaning & validation
- Rule-based quality scoring
- Rejected sample tracking
- Cleaned JSONL export & Data quality reporting

## Why this project?

Large language models rely heavily on high-quality pre-training data. This project aims to demonstrate how noisy multi-source data can be cleaned, filtered, scored, and transformed into structured JSONL formats suitable for downstream LLM training.

## Current Phase

**Phase 1 & 2**: Dummy data generation and local basic pipeline testing.

## Data Types

This pipeline currently supports three types of samples:
1. `general_text`: General web-style text
2. `game_text`: Game-domain text (e.g., reviews, mechanics, character lore)
3. `code`: Programming code snippets (Python, Lua, etc.)

## Unified JSONL Schema

Each sample flows through the pipeline using this unified format. After processing, tracking fields are automatically appended:

```json
{
  "id": "sample_001",
  "type": "game_text",
  "source": "steam_reviews",
  "language": "en",
  "content": "The combat system encourages team synergy...",
  "meta": {
    "game_genre": "RPG"
  },
  "processing_result": {
    "is_rejected": false,
    "quality_score": 0.95,
    "rejected_reason": null
  }
}