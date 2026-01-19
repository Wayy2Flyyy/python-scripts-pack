"""Test REST API endpoints with configurable requests."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.helpers import pretty_kv_print


# Configuration
MAX_RESPONSE_DISPLAY_LENGTH = 2000  # Maximum characters to display in response body


@dataclass
class APIResponse:
    """Represents an API response."""
    status_code: int
    headers: dict[str, str]
    body: str
    response_time_ms: int
    
    def is_success(self) -> bool:
        """Check if response indicates success."""
        return 200 <= self.status_code < 300


def make_request(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: str | None = None,
    timeout: int = 30,
) -> APIResponse:
    """
    Make an HTTP request and return the response.
    
    Args:
        url: Target URL
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        headers: Request headers
        body: Request body (for POST/PUT)
        timeout: Request timeout in seconds
        
    Returns:
        APIResponse object
        
    Raises:
        ValueError: If the request fails
    """
    headers = headers or {}
    
    # Prepare request
    data = body.encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    
    # Make request and measure time
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_time_ms = int((time.time() - start_time) * 1000)
            response_body = response.read().decode("utf-8")
            response_headers = dict(response.headers)
            
            return APIResponse(
                status_code=response.status,
                headers=response_headers,
                body=response_body,
                response_time_ms=response_time_ms,
            )
    
    except urllib.error.HTTPError as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_body = e.read().decode("utf-8") if e.fp else ""
        response_headers = dict(e.headers) if e.headers else {}
        
        return APIResponse(
            status_code=e.code,
            headers=response_headers,
            body=error_body,
            response_time_ms=response_time_ms,
        )
    
    except urllib.error.URLError as e:
        raise ValueError(f"Request failed: {e}") from e
    
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}") from e


def format_json_body(body: str) -> str:
    """Try to format body as JSON, return as-is if not JSON."""
    try:
        data = json.loads(body)
        return json.dumps(data, indent=2)
    except (json.JSONDecodeError, ValueError):
        return body


def print_response(response: APIResponse, show_headers: bool = False) -> None:
    """Print formatted response information."""
    # Status line
    status_emoji = "✓" if response.is_success() else "✗"
    print(f"\n{status_emoji} Status: {response.status_code}")
    print(f"Response Time: {response.response_time_ms}ms")
    
    # Headers
    if show_headers and response.headers:
        print("\nHeaders:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
    
    # Body
    print("\nBody:")
    print("-" * 50)
    formatted_body = format_json_body(response.body)
    # Truncate very long responses
    if len(formatted_body) > MAX_RESPONSE_DISPLAY_LENGTH:
        print(formatted_body[:MAX_RESPONSE_DISPLAY_LENGTH])
        print(f"\n... (truncated, {len(formatted_body)} total chars)")
    else:
        print(formatted_body)


def main() -> None:
    """Interactive API tester."""
    print("REST API Tester")
    print("=" * 50)
    print()
    
    while True:
        # Get URL
        url = input("Enter API URL (or 'quit' to exit): ").strip()
        
        if url.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        
        if not url:
            continue
        
        # Get method
        method = input("HTTP Method (default GET): ").strip().upper()
        if not method:
            method = "GET"
        
        # Get headers
        headers = {}
        print("Headers (enter key:value pairs, empty line to finish):")
        while True:
            header_input = input("  ").strip()
            if not header_input:
                break
            if ":" in header_input:
                key, value = header_input.split(":", 1)
                headers[key.strip()] = value.strip()
        
        # Get body for POST/PUT
        body = None
        if method in ("POST", "PUT", "PATCH"):
            print("Request body (enter JSON or text, empty line to skip):")
            body_lines = []
            while True:
                line = input("  ").strip()
                if not line and not body_lines:
                    break
                if not line and body_lines:
                    break
                body_lines.append(line)
            if body_lines:
                body = "\n".join(body_lines)
        
        # Show headers option
        show_headers_input = input("Show response headers? (y/n): ").strip().lower()
        show_headers = show_headers_input == "y"
        
        print("\nSending request...")
        
        try:
            response = make_request(
                url=url,
                method=method,
                headers=headers,
                body=body,
            )
            print_response(response, show_headers=show_headers)
        
        except ValueError as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
