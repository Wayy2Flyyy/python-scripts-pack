# 🟡 Intermediate Scripts

Scripts that require some configuration or basic technical understanding. More flexible and powerful than simple scripts, with customizable behavior.

---

## Available Scripts

### ⏱️ task_timer.py

**Configurable task timer with progress updates**

A flexible timer for focused work sessions, pomodoro technique, or any timed tasks.

```bash
python scripts/intermediate/task_timer.py
```

**Configuration:**

Edit `task_timer_config.json` to customize:

```json
{
  "task_name": "Focus session",
  "duration_minutes": 25,
  "alert_on_complete": true,
  "update_interval_seconds": 60
}
```

**Configuration Options:**
- `task_name` - Display name for the task
- `duration_minutes` - Timer duration (minimum 1 minute)
- `alert_on_complete` - Show completion message with emoji
- `update_interval_seconds` - How often to print remaining time

**Example Output:**
```
Starting 'Deep Work' for 25 minutes.
Remaining: 24m 00s
Remaining: 23m 00s
...
Remaining: 0m 00s
'Deep Work' complete! ✅
```

**Use Cases:**
- Pomodoro timer (25-minute work sessions)
- Meeting timers
- Study sessions
- Workout intervals

---

### 📂 file_monitor.py

**Monitor a directory for file changes in real-time**

Watch a directory and get notified when files are created, modified, or deleted.

```bash
python scripts/intermediate/file_monitor.py
```

**Features:**
- Real-time file system monitoring
- Detects file creation, modification, and deletion
- Optional recursive monitoring (subdirectories)
- Configurable check interval
- Timestamps for all events
- Uptime tracking

**Interactive Setup:**
- Directory to monitor (default: current directory)
- Monitor subdirectories? (y/n)
- Check interval in seconds (default: 5)

**Example Output:**
```
Monitoring: /home/user/projects/myapp
Recursive: True
Interval: 5s

Press Ctrl+C to stop
--------------------------------------------------
[14:23:15] CREATED: new_file.py
[14:23:42] MODIFIED: config.json
[14:24:01] DELETED: old_backup.txt
[14:24:30] Still monitoring... (uptime: 1m 15s)
```

**Use Cases:**
- Development workflow monitoring
- Log file watching
- Backup verification
- Directory synchronization debugging
- File system change auditing

---

### 🌐 api_tester.py

**Test REST API endpoints with custom requests**

Interactive HTTP client for testing and debugging REST APIs.

```bash
python scripts/intermediate/api_tester.py
```

**Features:**
- Support for all HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.)
- Custom headers
- Request body for POST/PUT/PATCH
- Response time measurement
- JSON formatting for responses
- Optional header display
- Status code indication (✓ for success, ✗ for errors)

**Interactive Workflow:**
1. Enter API URL
2. Select HTTP method (default: GET)
3. Add custom headers (key:value pairs)
4. Add request body (for POST/PUT/PATCH)
5. Choose to show/hide response headers
6. View formatted response

**Example Session:**
```
Enter API URL: https://api.github.com/users/octocat
HTTP Method (default GET): 
Headers (enter key:value pairs, empty line to finish):
  User-Agent: MyAPITester/1.0

Show response headers? (y/n): n

Sending request...

✓ Status: 200
Response Time: 342ms

Body:
--------------------------------------------------
{
  "login": "octocat",
  "id": 1,
  "name": "The Octocat",
  ...
}
```

**Use Cases:**
- API endpoint testing
- Debugging API responses
- Checking API availability
- Testing authentication headers
- Validating API payloads

---

## General Features

Intermediate scripts typically:

- 📝 Require configuration files or setup
- 🔧 Offer customizable behavior
- 💪 More powerful than simple scripts
- 🎯 Targeted at specific workflows
- 📚 May require basic technical knowledge

---

## Configuration Tips

### task_timer.py

- Keep duration_minutes reasonable (1-120)
- Set update_interval_seconds based on duration (longer timers = less frequent updates)
- Use meaningful task names for better tracking

### file_monitor.py

- Start with non-recursive mode for focused monitoring
- Use shorter intervals (1-5s) for real-time needs
- Use longer intervals (10-30s) for low-priority monitoring
- Monitor specific directories, not entire drives

### api_tester.py

- Add `Content-Type: application/json` header for JSON APIs
- Add `Accept: application/json` header for JSON responses
- Use `Authorization: Bearer <token>` for authenticated endpoints
- Test error cases by intentionally sending bad requests

---

## Extending Scripts

All intermediate scripts are designed to be extended:

- Modify configuration formats
- Add new features
- Integrate with other tools
- Use as modules in larger projects

See the source code for implementation details and extension points.

---

## Contributing

Have an idea for an intermediate script? See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

Intermediate scripts should:
- Use configuration files or interactive setup
- Provide meaningful customization options
- Include clear documentation
- Be more flexible than simple scripts
