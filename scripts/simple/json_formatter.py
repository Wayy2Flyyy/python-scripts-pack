"""Format and validate JSON files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def format_json(json_str: str, indent: int = 2, sort_keys: bool = False) -> str:
    """
    Format JSON string with proper indentation.
    
    Args:
        json_str: JSON string to format
        indent: Number of spaces for indentation
        sort_keys: Whether to sort object keys alphabetically
        
    Returns:
        Formatted JSON string
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        data = json.loads(json_str)
        return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


def minify_json(json_str: str) -> str:
    """
    Minify JSON by removing whitespace.
    
    Args:
        json_str: JSON string to minify
        
    Returns:
        Minified JSON string
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        data = json.loads(json_str)
        return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


def validate_json(json_str: str) -> tuple[bool, str]:
    """
    Validate JSON and return result.
    
    Args:
        json_str: JSON string to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        json.loads(json_str)
        return True, "Valid JSON ✓"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def analyze_json(json_str: str) -> dict[str, str]:
    """
    Analyze JSON structure.
    
    Args:
        json_str: JSON string to analyze
        
    Returns:
        Dictionary of statistics
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"Error": str(e)}
    
    def count_elements(obj: object, depth: int = 0) -> dict[str, int]:
        """Recursively count JSON elements."""
        counts = {"objects": 0, "arrays": 0, "max_depth": depth}
        
        if isinstance(obj, dict):
            counts["objects"] += 1
            for value in obj.values():
                child_counts = count_elements(value, depth + 1)
                counts["objects"] += child_counts["objects"]
                counts["arrays"] += child_counts["arrays"]
                counts["max_depth"] = max(counts["max_depth"], child_counts["max_depth"])
        
        elif isinstance(obj, list):
            counts["arrays"] += 1
            for item in obj:
                child_counts = count_elements(item, depth + 1)
                counts["objects"] += child_counts["objects"]
                counts["arrays"] += child_counts["arrays"]
                counts["max_depth"] = max(counts["max_depth"], child_counts["max_depth"])
        
        return counts
    
    counts = count_elements(data)
    
    return {
        "Type": type(data).__name__,
        "Objects": str(counts["objects"]),
        "Arrays": str(counts["arrays"]),
        "Max Depth": str(counts["max_depth"]),
        "Size (chars)": str(len(json_str)),
        "Size (formatted)": str(len(json.dumps(data, indent=2))),
    }


def main() -> None:
    """Interactive JSON formatter."""
    print("JSON Formatter & Validator")
    print("=" * 50)
    print()
    
    # Get input method
    print("Input method:")
    print("1. Load from file")
    print("2. Enter JSON directly")
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == "1":
        file_input = input("\nEnter file path: ").strip()
        file_path = Path(file_input)
        
        if not file_path.exists():
            print(f"Error: File '{file_path}' does not exist")
            return
        
        try:
            json_str = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    
    elif choice == "2":
        print("\nEnter JSON (press Ctrl+D or Ctrl+Z on a new line to finish):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        json_str = "\n".join(lines)
    
    else:
        print("Invalid choice")
        return
    
    if not json_str.strip():
        print("No JSON to process")
        return
    
    # Validate
    is_valid, message = validate_json(json_str)
    print(f"\n{message}")
    
    if not is_valid:
        return
    
    # Show statistics
    print("\nJSON Statistics:")
    print("-" * 50)
    stats = analyze_json(json_str)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Operation choice
    print("\nOperation:")
    print("1. Format (pretty print)")
    print("2. Minify")
    print("3. Format and save to file")
    op_choice = input("Choose (1, 2, or 3): ").strip()
    
    try:
        if op_choice == "1":
            formatted = format_json(json_str, indent=2, sort_keys=False)
            print("\nFormatted JSON:")
            print("-" * 50)
            print(formatted)
        
        elif op_choice == "2":
            minified = minify_json(json_str)
            print("\nMinified JSON:")
            print("-" * 50)
            print(minified)
        
        elif op_choice == "3":
            output_file = input("\nEnter output file path: ").strip()
            formatted = format_json(json_str, indent=2, sort_keys=False)
            Path(output_file).write_text(formatted, encoding="utf-8")
            print(f"✓ Saved to: {output_file}")
        
        else:
            print("Invalid choice")
    
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
