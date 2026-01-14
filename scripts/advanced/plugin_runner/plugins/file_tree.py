"""File tree plugin."""

from __future__ import annotations

from pathlib import Path


def _walk_tree(root: Path, max_depth: int, include_files: bool) -> list[str]:
    items: list[str] = []
    root_depth = len(root.parts)

    for path in sorted(root.rglob("*")):
        depth = len(path.parts) - root_depth
        if depth > max_depth:
            continue
        if path.is_file() and not include_files:
            continue
        indent = "  " * depth
        label = f"{path.name}/" if path.is_dir() else path.name
        items.append(f"{indent}{label}")

    return items


def run(config: dict) -> dict:
    root_path = Path(str(config["root_path"]))
    max_depth = int(config.get("max_depth", 2))
    include_files = bool(config.get("include_files", True))

    if not root_path.exists():
        raise ValueError(f"root_path does not exist: {root_path}")
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    return {
        "root": str(root_path.resolve()),
        "items": _walk_tree(root_path, max_depth, include_files),
    }
