"""System information utility."""

from __future__ import annotations

import os
import platform
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.helpers import format_duration, pretty_kv_print
from datetime import timedelta


def get_os_name() -> str:
    return platform.system() or "Unknown"


def get_os_version() -> str:
    return platform.release() or platform.version() or "Unknown"


def get_architecture() -> str:
    return platform.machine() or "Unknown"


def get_processor() -> str:
    return platform.processor() or platform.machine() or "Unknown"


def _uptime_seconds_linux() -> float | None:
    uptime_path = "/proc/uptime"
    if not os.path.isfile(uptime_path):
        return None
    try:
        with open(uptime_path, "r", encoding="utf-8") as handle:
            contents = handle.read().strip().split()
        return float(contents[0]) if contents else None
    except (OSError, ValueError):
        return None


def _uptime_seconds_windows() -> float | None:
    try:
        import ctypes

        get_tick_count64 = ctypes.windll.kernel32.GetTickCount64
        get_tick_count64.restype = ctypes.c_ulonglong
        return get_tick_count64() / 1000.0
    except (AttributeError, OSError):
        return None


def _uptime_seconds_darwin() -> float | None:
    try:
        import subprocess

        result = subprocess.run(
            ["sysctl", "-n", "kern.boottime"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Example output: { sec = 1705246540, usec = 0 } Wed Jan 14 10:15:40 2024
        for part in result.stdout.split("sec ="):
            if "," in part:
                seconds_part = part.split(",", 1)[0].strip()
                boot_seconds = int(seconds_part)
                return max(0.0, time.time() - boot_seconds)
        return None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def get_uptime_seconds() -> float | None:
    system = platform.system().lower()
    if system == "linux":
        return _uptime_seconds_linux()
    if system == "windows":
        return _uptime_seconds_windows()
    if system == "darwin":
        return _uptime_seconds_darwin()
    return None


def format_uptime(seconds: float | None) -> str:
    if seconds is None:
        return "Unknown"
    return format_duration(int(seconds))
    return str(timedelta(seconds=int(seconds)))


def get_python_version() -> str:
    return platform.python_version()


def collect_system_info() -> dict[str, str]:
    return {
        "OS": get_os_name(),
        "OS Version": get_os_version(),
        "Architecture": get_architecture(),
        "Processor": get_processor(),
        "Python Version": get_python_version(),
        "System Uptime": format_uptime(get_uptime_seconds()),
    }


def main() -> None:
    info = collect_system_info()
    title = "System Information"
    print(title)
    print("=" * len(title))
    pretty_kv_print(info)
def render_info(info: dict[str, str]) -> str:
    label_width = max(len(label) for label in info)
    lines = ["System Information", "=" * (label_width + 2)]
    for label, value in info.items():
        lines.append(f"{label.ljust(label_width)}: {value}")
    return "\n".join(lines)


def main() -> None:
    info = collect_system_info()
    print(render_info(info))


if __name__ == "__main__":
    main()
