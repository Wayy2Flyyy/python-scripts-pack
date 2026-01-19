"""Organize files in a directory by extension."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.helpers import pretty_kv_print


def get_extension_category(extension: str) -> str:
    """Map file extension to a category folder."""
    categories = {
        "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
        "documents": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"},
        "videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"},
        "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
        "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
        "code": {".py", ".js", ".java", ".cpp", ".c", ".html", ".css"},
        "spreadsheets": {".xlsx", ".xls", ".csv", ".ods"},
        "presentations": {".ppt", ".pptx", ".odp"},
    }
    ext_lower = extension.lower()
    for category, extensions in categories.items():
        if ext_lower in extensions:
            return category
    return "others"


def organize_directory(source_dir: Path, dry_run: bool = True) -> dict[str, int]:
    """
    Organize files in source_dir into category subdirectories.
    
    Args:
        source_dir: Directory to organize
        dry_run: If True, only report what would be done without moving files
        
    Returns:
        Dictionary mapping category names to file counts
    """
    if not source_dir.exists():
        raise ValueError(f"Directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise ValueError(f"Path is not a directory: {source_dir}")

    stats: dict[str, int] = {}
    
    for item in source_dir.iterdir():
        if not item.is_file():
            continue
        
        # Skip hidden files
        if item.name.startswith("."):
            continue
            
        extension = item.suffix
        if not extension:
            category = "no_extension"
        else:
            category = get_extension_category(extension)
        
        category_dir = source_dir / category
        
        if not dry_run:
            category_dir.mkdir(exist_ok=True)
            destination = category_dir / item.name
            # Handle name conflicts
            counter = 1
            while destination.exists():
                stem = item.stem
                destination = category_dir / f"{stem}_{counter}{extension}"
                counter += 1
            shutil.move(str(item), str(destination))
        
        stats[category] = stats.get(category, 0) + 1
    
    return stats


def main() -> None:
    """Interactive file organizer."""
    print("File Organizer")
    print("=" * 50)
    print()
    
    # Get directory from user
    dir_input = input("Enter directory path to organize (or press Enter for current): ").strip()
    if not dir_input:
        target_dir = Path.cwd()
    else:
        target_dir = Path(dir_input).resolve()
    
    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist")
        return
    
    print(f"\nAnalyzing: {target_dir}")
    print()
    
    # Dry run first
    try:
        stats = organize_directory(target_dir, dry_run=True)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    if not stats:
        print("No files to organize.")
        return
    
    print("Files to organize by category:")
    pretty_kv_print({k: str(v) for k, v in sorted(stats.items())})
    print()
    
    # Confirm action
    response = input("Proceed with organization? (yes/no): ").strip().lower()
    if response not in ("yes", "y"):
        print("Operation cancelled.")
        return
    
    # Actually organize
    organize_directory(target_dir, dry_run=False)
    print("\n✅ Files organized successfully!")


if __name__ == "__main__":
    main()
