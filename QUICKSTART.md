# ⚡ Quick Start - Ollama Excel Studio v5.0

**Get running in 5 minutes!**

---

## Prerequisites Check ✅

```bash
# 1. Node.js 18+
node --version  # Should be v18.0.0 or higher

# 2. Python 3.9+
python3 --version  # Should be 3.9.0 or higher

# 3. Ollama installed
ollama --version  # Should show version

# 4. Ollama running
curl http://localhost:11434/api/tags  # Should return JSON
```

**Missing something?**
- Node.js: https://nodejs.org
- Python: https://python.org
- Ollama: https://ollama.ai

---

## Installation (One Command!)

```bash
chmod +x install.sh
./install.sh
```

**What it does:**
- ✓ Installs all dependencies
- ✓ Sets up directories
- ✓ Creates configuration
- ✓ Verifies everything

**Takes:** ~2-3 minutes

---

## First Model (if needed)

```bash
# Start Ollama
ollama serve

# Pull recommended model (in new terminal)
ollama pull qwen2.5:14b-instruct

# Verify
ollama list
```

**Recommended models:**
- `qwen2.5:14b-instruct` - Best balance (8.5 GB)
- `llama3.1:8b-instruct` - Good, smaller (4.7 GB)
- `qwen2.5:32b-instruct` - Best quality (19 GB)

---

## Launch the Studio 🚀

```bash
npm run studio
```

**This starts:**
1. Backend API server (port 8000)
2. Frontend web server (port 3000)
3. Auto-opens browser to http://localhost:3000

**You should see:**
```
┌────────────────────────────────────┐
│  Ollama Excel Studio v5.0          │
│  Status: ✓ Ollama Active (3 models)│
│  Files: 0 files                    │
└────────────────────────────────────┘
```

---

## First Steps 🎯

### 1. Upload a File
- Click "Upload Files" or drag-and-drop
- Accepts: .xlsx, .xls, .csv
- File appears in dashboard

### 2. Chat with AI
- Click "AI Assistant" in sidebar
- Type: "What sheets are in my file?"
- AI responds with info

### 3. Try Some Commands

```
"Show me the first 10 rows of Sheet1"
"What's the total of column B?"
"Create a chart of sales over time"
"Add a new row: ['John', 25, 'Active']"
```

### 4. Explore Features
- **Charts**: Auto-generated visualizations
- **Templates**: Pre-built workflows
- **History**: See and undo operations
- **Export**: PDF, CSV, images

---

## Common First-Time Issues 🔧

**"Ollama: Disconnected"**
```bash
ollama serve  # Start Ollama
```

**"No models found"**
```bash
ollama pull qwen2.5:14b-instruct
```

**"Port 3000 in use"**
```bash
PORT=3001 npm run studio
```

**"openpyxl not found"**
```bash
pip3 install openpyxl --break-system-packages
```

---

## Migration from v4.1 📦

**Have v4.1 installed?** Migrate your data:

```bash
python scripts/migrate_from_v4.py /path/to/v4.1
npm run studio
```

**Your v4.1 files and config are now in v5.0!**

---

## Next Steps 📚

1. **Read the User Guide**
   - Full features: `docs/USER_GUIDE.md`
   - API reference: `docs/API.md`

2. **Try Templates**
   - Click "Templates" tab
   - Browse pre-built workflows
   - Apply to your files

3. **Explore Charts**
   - Select a file with data
   - Click "Visualizations"
   - See auto-suggestions

4. **Learn Keyboard Shortcuts**
   - `Ctrl + /` - Quick chat
   - `Ctrl + S` - Save
   - `Ctrl + Z` - Undo

---

## Key Differences from v4.1 🆕

| Feature | v4.1 | v5.0 |
|---------|------|------|
| Interface | CLI only | Web UI ✨ |
| Charts | None | Interactive ✨ |
| Batch ops | None | Built-in ✨ |
| Templates | None | Gallery ✨ |
| Export | CSV only | PDF, CSV, images ✨ |
| History | Backups | Visual timeline ✨ |

**Everything from v4.1 still works!**

---

## Getting Help 💬

**In the app:**
- Click "?" icon
- AI can answer: "How do I...?"

**Documentation:**
- User Guide: `docs/USER_GUIDE.md`
- Troubleshooting: Search guide for error message

**Community:**
- GitHub Issues: Bug reports
- GitHub Discussions: Questions

---

## Status Indicators 🚦

**Status Bar shows:**

✓ **Green** - All systems go
- Ollama: Active (X models)
- Backend: Connected
- Files: Ready

⚠ **Yellow** - Warning
- Ollama disconnected (AI limited)
- Model < 7B (may be unreliable)

✗ **Red** - Error
- Backend unreachable
- File operation failed

---

## Example Workflow 🎬

**Scenario:** Analyze sales data

```
1. Upload sales.xlsx
   → Drag file to dashboard

2. Ask AI: "Summarize this data"
   → AI: "Found 150 rows, 5 columns..."

3. Request: "Show top 10 customers by revenue"
   → AI: Creates filtered view

4. Ask: "Create a bar chart"
   → AI: Generates interactive chart

5. Request: "Export this as PDF report"
   → AI: Creates formatted PDF

6. Done! 🎉
   → Report ready in ./data/exports/
```

**Time:** < 2 minutes

---

## Configuration 🔧

**Edit:** `config/studio.json`

**Common changes:**

```json
{
  "ollama": {
    "preferredModels": ["your-favorite-model"],
    "temperature": 0.2
  },
  "excel": {
    "maxBackupsPerFile": 20,
    "autoSave": true
  },
  "ui": {
    "theme": "dark"  // Coming soon!
  }
}
```

**Changes take effect immediately** (no restart needed for most)

---

## Performance Tips ⚡

**Fast:**
- Use qwen2.5:14b-instruct
- Keep files < 10 MB
- Close other heavy apps

**Faster:**
- Use llama3.1:8b-instruct
- Process files in batches
- Increase Ollama timeout

**Fastest:**
- Use GPU acceleration (Ollama)
- SSD storage
- 16+ GB RAM

---

## That's It! 🎉

You're now ready to use Ollama Excel Studio v5.0!

**Remember:**
- 100% local (no internet needed after setup)
- Your data never leaves your machine
- Automatic backups protect your work
- AI is there to help - just ask!

**Enjoy automating with AI! 🚀**

---

*Questions? See the full User Guide or ask the AI assistant!*
