"""Analyze text files for basic statistics."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.helpers import pretty_kv_print


def analyze_text(text: str) -> dict[str, str]:
    """
    Analyze text and return statistics.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary of statistics
    """
    # Basic counts
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    line_count = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    
    # Word analysis
    words = text.split()
    word_count = len(words)
    
    # Sentence analysis (approximate)
    sentence_endings = text.count(".") + text.count("!") + text.count("?")
    
    # Average calculations
    avg_word_length = (
        round(sum(len(word) for word in words) / word_count, 2)
        if word_count > 0
        else 0.0
    )
    avg_words_per_line = (
        round(word_count / line_count, 2) if line_count > 0 else 0.0
    )
    
    # Most common words
    word_freq = Counter(word.lower().strip(".,!?;:") for word in words if word)
    most_common = word_freq.most_common(5)
    most_common_str = ", ".join(
        f"{word}({count})" for word, count in most_common
    ) if most_common else "N/A"
    
    return {
        "Total Characters": str(char_count),
        "Characters (no spaces)": str(char_count_no_spaces),
        "Total Words": str(word_count),
        "Total Lines": str(line_count),
        "Sentences": str(sentence_endings),
        "Avg Word Length": str(avg_word_length),
        "Avg Words/Line": str(avg_words_per_line),
        "Most Common Words": most_common_str,
    }


def read_file(file_path: Path) -> str:
    """Read text from a file."""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Try with latin-1 as fallback
        return file_path.read_text(encoding="latin-1")


def main() -> None:
    """Interactive text analyzer."""
    print("Text Analyzer")
    print("=" * 50)
    print()
    
    # Get input method
    print("Input method:")
    print("1. Analyze a file")
    print("2. Enter text directly")
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == "1":
        file_input = input("\nEnter file path: ").strip()
        file_path = Path(file_input)
        
        if not file_path.exists():
            print(f"Error: File '{file_path}' does not exist")
            return
        
        if not file_path.is_file():
            print(f"Error: '{file_path}' is not a file")
            return
        
        try:
            text = read_file(file_path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        print(f"\nAnalyzing: {file_path.name}")
    
    elif choice == "2":
        print("\nEnter text (press Ctrl+D or Ctrl+Z to finish):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        text = "\n".join(lines)
    
    else:
        print("Invalid choice")
        return
    
    if not text:
        print("No text to analyze")
        return
    
    # Analyze and display
    print("\nAnalysis Results:")
    print("-" * 50)
    stats = analyze_text(text)
    pretty_kv_print(stats)


if __name__ == "__main__":
    main()
