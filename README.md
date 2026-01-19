# 🧩 Python Script Collection

A structured and continuously expanding collection of Python scripts ranging from simple, plug-and-play utilities to more advanced systems that require configuration and technical skill.

All scripts are fully editable, reusable, and permitted for redistribution once downloaded.

---

## 📂 Repository Structure

```
scripts/
├── simple/          # Plug-and-play utilities, minimal setup
├── intermediate/    # Scripts requiring basic configuration
└── advanced/        # Advanced systems for experienced users

shared/              # Reusable helper functions
```

---

## 📦 Available Scripts

### 🟢 Simple Scripts (Ready to Use)

| Script | Description | Usage |
|--------|-------------|-------|
| **system_info.py** | Display detailed system information | `python scripts/simple/system_info.py` |
| **password_generator.py** | Generate secure random passwords | `python scripts/simple/password_generator.py` |
| **file_organizer.py** | Organize files by extension into folders | `python scripts/simple/file_organizer.py` |
| **text_analyzer.py** | Analyze text files for statistics | `python scripts/simple/text_analyzer.py` |
| **json_formatter.py** | Format, validate, and analyze JSON | `python scripts/simple/json_formatter.py` |
| **url_shortener.py** | Shorten URLs using TinyURL API | `python scripts/simple/url_shortener.py` |

### 🟡 Intermediate Scripts (Some Configuration)

| Script | Description | Configuration |
|--------|-------------|---------------|
| **task_timer.py** | Configurable task timer with alerts | Edit `task_timer_config.json` |
| **file_monitor.py** | Monitor directory for file changes | Interactive setup |
| **api_tester.py** | Test REST API endpoints | Interactive requests |

### 🔴 Advanced Scripts (Technical Knowledge Required)

*Coming soon - contributions welcome!*

---

## 🚀 Quick Start

### Run Any Script

```bash
# Clone the repository
git clone https://github.com/Wayy2Flyyy/python-scripts-pack.git
cd python-scripts-pack

# Run a script directly
python scripts/simple/password_generator.py
python scripts/intermediate/task_timer.py
```

### Requirements

- Python 3.10 or higher
- No external dependencies (uses standard library only)

---

## 💡 Usage Examples

### Generate a Secure Password
```bash
python scripts/simple/password_generator.py
# Follow prompts: length, character types, count
```

### Organize Messy Downloads Folder
```bash
python scripts/simple/file_organizer.py
# Enter path: ~/Downloads
# Review categorization plan
# Confirm to organize files
```

### Format JSON Data
```bash
python scripts/simple/json_formatter.py
# Choose input method (file or direct entry)
# Format, minify, or save output
```

### Monitor Project Directory
```bash
python scripts/intermediate/file_monitor.py
# Enter directory path
# Set check interval
# Watch for changes in real-time
```

---

## 🛠️ For Developers

### Project Features

- **Clean Code**: Readable, well-documented Python
- **Type Hints**: Full type annotations using modern Python syntax
- **No Dependencies**: Pure standard library implementations
- **Modular Design**: Shared utilities in `shared/` module
- **Error Handling**: Robust error handling and user feedback

### Shared Utilities

All scripts can leverage shared helper functions:

```python
from shared.helpers import format_duration, safe_read_json, pretty_kv_print
```

See `shared/helpers.py` for available utilities.

---

## 📖 Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributors
- **[scripts/simple/README.md](scripts/simple/README.md)** - Simple script details
- **[scripts/intermediate/README.md](scripts/intermediate/README.md)** - Intermediate script details
- **[scripts/advanced/README.md](scripts/advanced/README.md)** - Advanced script details

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Follow the existing code style and structure
2. Place scripts in the appropriate difficulty folder
3. Include docstrings and type hints
4. Test your scripts before submitting
5. Update documentation as needed

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

All scripts are provided with full access:

- ✅ Modification allowed
- ✅ Personal use allowed  
- ✅ Redistribution allowed

See [LICENSE](LICENSE) for details.

---

## 📌 Status

**Active and Maintained**

This collection is continuously growing. New scripts are added regularly, and improvements to existing scripts are ongoing.

### Planned Additions

- Database utilities
- Image processing tools
- Network utilities
- Automation scripts
- Data analysis tools

---

## 🙏 Credits

**SO PLEASE PLEASE PLEASE MAKE THESE SCRIPTS YOUR OWN AND SEND THEM MY WAY!!!**

We appreciate all contributions and feedback from the community.

