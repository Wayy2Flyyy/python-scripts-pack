"""Hash utility plugin."""

from __future__ import annotations

import hashlib


def run(config: dict) -> dict:
    input_text = config["input_text"]
    algorithm = config.get("algorithm", "sha256")

    if algorithm not in {"sha256", "md5"}:
        raise ValueError("algorithm must be 'sha256' or 'md5'")

    hasher = hashlib.new(algorithm)
    hasher.update(str(input_text).encode("utf-8"))
    return {"algorithm": algorithm, "hash": hasher.hexdigest()}
