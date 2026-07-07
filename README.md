# NexusAI

**A local desktop AI assistant for Windows with direct system control capabilities.**

NexusAI isn't limited to answering questions — it can interact with the operating system through a growing collection of built-in tools.

Creator: [@Greg_ios](https://stardance.hackclub.com/@Greg_ios) — Hack Club Stardance Challenge

---

## 🚀 Features

### 🧠 AI & Memory
- Backend AI logic powered by **Qwen3:4B** and **qwen2.5:3b-instruct** (faster model)
- Memory system (`Memory` class) to retain context across sessions
- Chat history management so the model remembers previous messages
- Refined system prompt for more stable and relevant responses

### 🛠️ System Tools
- **Process management**
- **File management**
- Launching system applications: Calculator, Notepad, File Explorer, Task Manager, Command Prompt
- Opening Chrome
- Opening URLs
- Taking screenshots
- Shutdown, restart, log out

### 📊 System Monitoring
- `get_cpu` — CPU usage percentage
- `get_ram` — RAM usage percentage
- `get_disk_io_counters` — read/write per second
- `get_disk_usage` — disk usage
- `get_network_usage` — sent/received per second

### 🌐 Search & Web
- **YouTube** search
- **GitHub** search
- General **web** search
- Basic web interface

### 🖥️ UI & Backend
- Modern, clean UI
- Backend endpoints via **Flask**
- Structured AI logic on the backend

---

## 📅 Development History (Devlog Highlights)

| Days ago | Feature |
|---|---|
| 14 | Created Flask endpoints & structured the AI logic |
| 14 | Added AI to the backend |
| 13 | Added more system-monitoring tools (CPU, RAM, disk, network) |
| 13 | Added support for tools with arguments — URL opening, screenshots |
| 13 | Added ability to open system applications |
| 13 | Shutdown/restart/log out + model history management |
| 12 | Web search + faster model (qwen2.5:3b-instruct) + basic web interface |
| 12 | Modern, clean UI |
| 11 | File management tools |
| 11 | Process management tools |
| 11 | YouTube & GitHub search + updated AI operating rules |
| 10 | Memory class + memory tool integration, upgraded to Qwen3:4B |
| 10 | Added Memory class (foundation for future tools) |
| 9 | Improved system prompt for more stable responses |
| 1 | Add Main executable file to the binary directory |

---

## 📌 Notes

This README was generated based on the project's devlogs on the Hack Club Stardance Challenge. As the project evolves, consider updating it with:
- Installation instructions (dependencies, Python version, Ollama/models)
- Run instructions (backend + UI)
- Usage examples for commands sent to NexusAI
- License

---

*Made with ❤️ for the Hack Club Stardance Challenge*
