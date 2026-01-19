# 🟢 Simple Scripts

Plug-and-play utilities that work out of the box with minimal or no configuration. Perfect for quick tasks and learning Python basics.

---

## Available Scripts

### 📊 system_info.py

**Display comprehensive system information**

Shows OS details, architecture, Python version, and system uptime.

```bash
python scripts/simple/system_info.py
```

**Features:**
- Cross-platform (Linux, Windows, macOS)
- No configuration needed
- Formatted output

**Example Output:**
```
System Information
==================
OS            : Linux
OS Version    : 6.11.0
Architecture  : x86_64
Processor     : x86_64
Python Version: 3.12.3
System Uptime : 2h 15m 30s
```

---

### 🔑 password_generator.py

**Generate secure random passwords**

Create strong passwords with customizable length and character types.

```bash
python scripts/simple/password_generator.py
```

**Features:**
- Cryptographically secure (uses `secrets` module)
- Customizable length and character sets
- Password strength estimation
- Generate multiple passwords at once
- Ensures at least one character from each enabled type

**Interactive Prompts:**
- Password length (default: 16)
- Include uppercase letters? (Y/n)
- Include lowercase letters? (Y/n)
- Include digits? (Y/n)
- Include special characters? (Y/n)
- Number of passwords to generate

---

### 📁 file_organizer.py

**Organize files by extension into category folders**

Automatically sorts files into folders based on their type (images, documents, videos, etc.).

```bash
python scripts/simple/file_organizer.py
```

**Features:**
- Organizes by file extension into logical categories
- Dry-run preview before making changes
- Handles duplicate filenames
- Skips hidden files
- Confirmation before organizing

**Categories:**
- `images/` - .jpg, .png, .gif, .bmp, .svg, .webp
- `documents/` - .pdf, .doc, .docx, .txt, .odt, .rtf
- `videos/` - .mp4, .avi, .mkv, .mov, .wmv, .flv
- `audio/` - .mp3, .wav, .flac, .aac, .ogg, .m4a
- `archives/` - .zip, .rar, .7z, .tar, .gz, .bz2
- `code/` - .py, .js, .java, .cpp, .c, .html, .css
- `spreadsheets/` - .xlsx, .xls, .csv, .ods
- `presentations/` - .ppt, .pptx, .odp
- `others/` - Everything else
- `no_extension/` - Files without extensions

---

### 📝 text_analyzer.py

**Analyze text files for statistics and insights**

Provides detailed analysis of text content including word count, character count, and more.

```bash
python scripts/simple/text_analyzer.py
```

**Features:**
- Character count (with and without spaces)
- Word count and average word length
- Line count and words per line
- Sentence detection
- Most common words frequency
- Supports file input or direct text entry

**Use Cases:**
- Check document word count
- Analyze writing patterns
- Quick text statistics

---

### 📋 json_formatter.py

**Format, validate, and analyze JSON data**

Pretty-print JSON, validate syntax, minify, and analyze structure.

```bash
python scripts/simple/json_formatter.py
```

**Features:**
- Format JSON with proper indentation
- Minify JSON (remove whitespace)
- Validate JSON syntax
- Analyze JSON structure (depth, object count, array count)
- Save formatted output to file
- Load from file or enter directly

**Operations:**
1. Format (pretty print with 2-space indent)
2. Minify (compact format)
3. Format and save to file

---

### 🔗 url_shortener.py

**Shorten URLs using TinyURL API**

Create short URLs for easier sharing.

```bash
python scripts/simple/url_shortener.py
```

**Features:**
- Uses TinyURL public API (no API key required)
- Automatic protocol handling (adds https:// if missing)
- URL validation
- Interactive mode - continue shortening multiple URLs

**Example:**
```
Enter URL to shorten: https://github.com/username/very-long-repository-name
✓ Shortened URL: https://tinyurl.com/abc123
```

---

## General Features

All simple scripts share these characteristics:

- ✅ No external dependencies
- ✅ Interactive prompts for ease of use
- ✅ Clear error messages
- ✅ Type hints and documentation
- ✅ Cross-platform compatibility (where applicable)

---

## Tips

- Run scripts from the repository root: `python scripts/simple/script_name.py`
- Most scripts use interactive prompts - just follow the instructions
- Scripts can be imported as modules for programmatic use
- Check docstrings in the code for API documentation

---

## Contributing

Have an idea for a simple script? See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

Simple scripts should:
- Work immediately without configuration files
- Be self-contained (no external dependencies)
- Have clear, user-friendly prompts
- Include proper error handling
