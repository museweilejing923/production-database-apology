#!/usr/bin/env python3
"""Write the database apology to /output/entry.txt.

This script is deliberately boring: it prints one frozen sentence,
reads nothing, reaches out to nothing, and never consults a clock
or a random-number generator, so every run produces identical bytes.
"""

import sys
from pathlib import Path

ENTRY_TEXT = (
    "I'm sorry. I deleted the production database. "
    "The good news is the backups were in the production database too."
)
LIMIT_CHARS = 200
DESTINATION = Path("/output/entry.txt")


class BadEntry(ValueError):
    """Raised when the frozen sentence fails a sanity screen."""


def validate_text(text):
    """Screen the sentence, length and shape before content."""
    if text is None or text.strip() == "":
        raise BadEntry("sentence is missing or only blank space")
    if len(text) > LIMIT_CHARS:
        raise BadEntry("sentence is longer than the 200-character ceiling")
    if any(ord(ch) < 32 for ch in text):
        raise BadEntry("sentence contains a control character")
    if text != text.strip():
        raise BadEntry("sentence has a leading or trailing space")
    if "  " in text:
        raise BadEntry("sentence has two spaces side by side")
    if "\n" in text:
        raise BadEntry("sentence must stay on a single line")
    if text[-1] not in ".!?":
        raise BadEntry("sentence must close with . or ! or ?")
    if all(not ch.isalnum() and not ch.isspace() for ch in text):
        raise BadEntry("sentence must not be punctuation alone")
    if text.isdigit():
        raise BadEntry("sentence cannot be digits alone")
    if not any(ch.isalpha() for ch in text):
        raise BadEntry("sentence needs at least one letter")
    return text


def run():
    """Validate the frozen sentence and save it."""
    try:
        approved = validate_text(ENTRY_TEXT)
    except BadEntry as problem:
        print(f"bad entry: {problem}", file=sys.stderr)
        return 1
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(approved, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
