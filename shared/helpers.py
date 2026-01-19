"""Shared utility helpers for scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def format_duration(seconds: int) -> str:
    """Format a duration in seconds into a human-readable string."""
    if seconds < 0:
        seconds = 0
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes:02d}m {secs:02d}s"
    return f"{minutes}m {secs:02d}s"


def format_bytes(bytes_count: int, precision: int = 2) -> str:
    """
    Format byte count into human-readable string.
    
    Args:
        bytes_count: Number of bytes
        precision: Decimal places for display
        
    Returns:
        Formatted string like "1.5 MB" or "3.2 GB"
    """
    if bytes_count < 0:
        bytes_count = 0
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    size = float(bytes_count)
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    if unit_index == 0:  # Bytes - no decimal
        return f"{int(size)} {units[unit_index]}"
    
    return f"{size:.{precision}f} {units[unit_index]}"


def safe_read_json(path: str | Path) -> dict[str, Any]:
    """Read JSON from a file path, raising a clear ValueError on failure."""
    json_path = Path(path)
    try:
        raw = json_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"JSON file not found: {json_path}") from exc
    except OSError as exc:
        raise ValueError(f"Unable to read JSON file: {json_path}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in file: {json_path}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in file: {json_path}")
    return data


def pretty_kv_print(data: dict[str, str], sort_keys: bool = False) -> None:
    """Print aligned key/value pairs."""
    items = sorted(data.items()) if sort_keys else list(data.items())
    if not items:
        return
    key_width = max(len(key) for key, _ in items)
    for key, value in items:
        print(f"{key.ljust(key_width)}: {value}")

