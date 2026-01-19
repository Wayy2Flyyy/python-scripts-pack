"""Simple URL shortener using TinyURL API."""

from __future__ import annotations

import sys
import urllib.parse
import urllib.request
from pathlib import Path


def validate_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def shorten_url(long_url: str) -> str:
    """
    Shorten a URL using TinyURL API.
    
    Args:
        long_url: The URL to shorten
        
    Returns:
        Shortened URL
        
    Raises:
        ValueError: If the URL cannot be shortened
    """
    # Validate URL format
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url
    
    # Use TinyURL API
    api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
    
    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            if response.status == 200:
                short_url = response.read().decode("utf-8").strip()
                # Validate the response is a valid URL
                if not validate_url(short_url):
                    raise ValueError(f"API returned invalid URL: {short_url}")
                return short_url
            else:
                raise ValueError(f"API returned status {response.status}")
    except urllib.error.URLError as e:
        raise ValueError(f"Failed to shorten URL: {e}") from e
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}") from e


def main() -> None:
    """Interactive URL shortener."""
    print("URL Shortener (TinyURL)")
    print("=" * 50)
    print()
    
    while True:
        url_input = input("Enter URL to shorten (or 'quit' to exit): ").strip()
        
        if url_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        
        if not url_input:
            continue
        
        # Add protocol if missing for validation
        check_url = url_input
        if not check_url.startswith(("http://", "https://")):
            check_url = "https://" + check_url
        
        if not validate_url(check_url):
            print("Error: Invalid URL format")
            print()
            continue
        
        try:
            short_url = shorten_url(url_input)
            print(f"✓ Shortened URL: {short_url}")
        except ValueError as e:
            print(f"Error: {e}")
        
        print()


if __name__ == "__main__":
    main()
