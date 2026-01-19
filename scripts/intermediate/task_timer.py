"""Simple configurable task timer."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.helpers import format_duration, safe_read_json


@dataclass(frozen=True)
class TaskConfig:
    task_name: str
    duration_minutes: int
    alert_on_complete: bool
    update_interval_seconds: int


CONFIG_FILE = Path(__file__).with_name("task_timer_config.json")


def load_config() -> TaskConfig:
    raw = safe_read_json(CONFIG_FILE)

    task_name = str(raw.get("task_name", "Task"))
    duration_minutes = int(raw.get("duration_minutes", 1))
    alert_on_complete = bool(raw.get("alert_on_complete", True))
    update_interval_seconds = int(raw.get("update_interval_seconds", 60))

    if duration_minutes < 1:
        duration_minutes = 1
    if update_interval_seconds < 1:
        update_interval_seconds = 1

    return TaskConfig(
        task_name=task_name,
        duration_minutes=duration_minutes,
        alert_on_complete=alert_on_complete,
        update_interval_seconds=update_interval_seconds,
    )


def format_remaining(seconds_remaining: int) -> str:
    return format_duration(seconds_remaining)


def run_timer(config: TaskConfig) -> None:
    total_seconds = config.duration_minutes * 60
    end_time = time.monotonic() + total_seconds
    next_update = time.monotonic()

    print(f"Starting '{config.task_name}' for {config.duration_minutes} minutes.")

    while True:
        now = time.monotonic()
        remaining = max(0, int(end_time - now))
        if now >= next_update or remaining == 0:
            print(f"Remaining: {format_remaining(remaining)}")
            next_update = now + config.update_interval_seconds
        if remaining == 0:
            break
        time.sleep(1)


def notify_complete(config: TaskConfig) -> None:
    if config.alert_on_complete:
        print(f"'{config.task_name}' complete! ✅")
    else:
        print(f"'{config.task_name}' complete.")


def main() -> None:
    config = load_config()
    run_timer(config)
    notify_complete(config)


if __name__ == "__main__":
    main()
