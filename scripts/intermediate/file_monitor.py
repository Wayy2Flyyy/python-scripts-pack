"""Monitor a directory for file changes."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.helpers import format_duration


@dataclass
class FileSnapshot:
    """Snapshot of a file's state."""
    path: Path
    size: int
    modified_time: float
    
    @classmethod
    def from_path(cls, path: Path) -> FileSnapshot:
        """Create a snapshot from a file path."""
        stat = path.stat()
        return cls(
            path=path,
            size=stat.st_size,
            modified_time=stat.st_mtime,
        )


@dataclass
class ChangeEvent:
    """Represents a file system change."""
    event_type: str  # "created", "modified", "deleted"
    path: Path
    timestamp: datetime
    
    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] {self.event_type.upper()}: {self.path.name}"


class DirectoryMonitor:
    """Monitor a directory for file changes."""
    
    def __init__(self, directory: Path, recursive: bool = False):
        """
        Initialize the monitor.
        
        Args:
            directory: Directory to monitor
            recursive: Whether to monitor subdirectories
        """
        self.directory = directory
        self.recursive = recursive
        self.snapshots: dict[Path, FileSnapshot] = {}
        self._initial_scan()
    
    def _initial_scan(self) -> None:
        """Scan the directory and create initial snapshots."""
        pattern = "**/*" if self.recursive else "*"
        for path in self.directory.glob(pattern):
            if path.is_file():
                self.snapshots[path] = FileSnapshot.from_path(path)
    
    def check_changes(self) -> list[ChangeEvent]:
        """
        Check for changes since last check.
        
        Returns:
            List of change events
        """
        events: list[ChangeEvent] = []
        current_files = set()
        pattern = "**/*" if self.recursive else "*"
        
        # Check for new and modified files
        for path in self.directory.glob(pattern):
            if not path.is_file():
                continue
            
            current_files.add(path)
            current_snapshot = FileSnapshot.from_path(path)
            
            if path not in self.snapshots:
                # New file
                events.append(ChangeEvent("created", path, datetime.now()))
                self.snapshots[path] = current_snapshot
            else:
                # Check if modified
                old_snapshot = self.snapshots[path]
                if (current_snapshot.modified_time != old_snapshot.modified_time or
                    current_snapshot.size != old_snapshot.size):
                    events.append(ChangeEvent("modified", path, datetime.now()))
                    self.snapshots[path] = current_snapshot
        
        # Check for deleted files
        deleted_paths = set(self.snapshots.keys()) - current_files
        for path in deleted_paths:
            events.append(ChangeEvent("deleted", path, datetime.now()))
            del self.snapshots[path]
        
        return events


def main() -> None:
    """Interactive directory monitor."""
    print("Directory Monitor")
    print("=" * 50)
    print()
    
    # Get directory
    dir_input = input("Enter directory to monitor (or press Enter for current): ").strip()
    if not dir_input:
        target_dir = Path.cwd()
    else:
        target_dir = Path(dir_input).resolve()
    
    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist")
        return
    
    if not target_dir.is_dir():
        print(f"Error: '{target_dir}' is not a directory")
        return
    
    # Get monitoring options
    recursive_input = input("Monitor subdirectories? (y/n): ").strip().lower()
    recursive = recursive_input == "y"
    
    # Get check interval
    while True:
        interval_input = input("Check interval in seconds (default 5): ").strip()
        if not interval_input:
            interval = 5
            break
        try:
            interval = int(interval_input)
            if interval < 1:
                print("Interval must be at least 1 second")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    print(f"\nMonitoring: {target_dir}")
    print(f"Recursive: {recursive}")
    print(f"Interval: {interval}s")
    print("\nPress Ctrl+C to stop\n")
    print("-" * 50)
    
    # Start monitoring
    monitor = DirectoryMonitor(target_dir, recursive=recursive)
    start_time = time.monotonic()
    
    try:
        while True:
            time.sleep(interval)
            events = monitor.check_changes()
            
            if events:
                for event in events:
                    print(event)
            else:
                # Show periodic "still watching" message
                elapsed = int(time.monotonic() - start_time)
                if elapsed % 30 == 0:  # Every 30 seconds
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Still monitoring... (uptime: {format_duration(elapsed)})")
    
    except KeyboardInterrupt:
        elapsed = int(time.monotonic() - start_time)
        print("\n")
        print("-" * 50)
        print(f"Monitoring stopped after {format_duration(elapsed)}")


if __name__ == "__main__":
    main()
