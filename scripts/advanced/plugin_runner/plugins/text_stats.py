"""Text statistics plugin."""

from __future__ import annotations


def run(config: dict) -> dict:
    input_text = str(config["input_text"])
    lines = input_text.splitlines() or [""]
    words = input_text.split()
    return {
        "chars": len(input_text),
        "words": len(words),
        "lines": len(lines),
    }
