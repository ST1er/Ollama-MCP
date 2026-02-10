# 🚀 Ollama Excel Studio v5.0

**The Next Generation: AI-Powered Excel with a Beautiful Web Interface**

Fully local. No cloud. No internet required. Your data never leaves your machine.

---

## 🎯 What's New in v5.0

Built on the rock-solid foundation of v4.1, now with:

- **🌐 Modern Web UI** - Beautiful, responsive interface accessible from any browser
- **📊 Live Visualizations** - Instant charts, graphs, and pivot tables
- **🎨 Drag & Drop** - Upload files, create sheets, manage data visually  
- **🤖 Smart AI Chat** - Conversational interface with suggested actions
- **📋 Operation Templates** - Pre-built workflows for common tasks
- **⏮️ Visual Undo/Redo** - Timeline view of all operations with one-click rollback
- **⚡ Batch Operations** - Process multiple files or operations at once
- **📤 Export Options** - PDF reports, CSV exports, chart images
- **🎯 Quick Actions** - Common tasks accessible with one click
- **📈 Data Analysis** - Auto-detect patterns, suggest insights

All while maintaining **100% local operation** and the **auto-backup safety** you trust.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Web Browser                        │
│                   (React + TypeScript)                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend                           │
│        (Python - handles HTTP, WebSocket, auth)             │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Ollama     │  │ MCP Server   │  │  Charting    │
│   Bridge     │  │ (Excel ops)  │  │  Engine      │
│  (AI Chat)   │  │ (Python)     │  │ (Plotly)     │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  ┌──────────────┐
                  │ Excel Files  │
                  │  + Backups   │
                  └──────────────┘
```

**Key Components:**

1. **Frontend (React)** - Modern SPA with TypeScript, Tailwind CSS
2. **API Server (FastAPI)** - RESTful + WebSocket for real-time updates  
3. **MCP Bridge** - Reuses your existing v4.1 MCP server (no changes!)
4. **Ollama Integration** - Direct integration with local LLM
5. **Visualization Engine** - Plotly for interactive charts
6. **Template System** - Predefined workflows and scripts

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Ollama installed and running
- Your existing v4.1 setup (optional - we include it)

### Installation

```bash
# 1. Clone or extract
cd ollama-excel-studio

# 2. Run the installer (handles everything)
chmod +x install.sh
./install.sh

# 3. Start Ollama with a model
ollama serve
ollama pull qwen2.5:14b-instruct

# 4. Launch the studio
npm run studio

# 5. Open browser
# Auto-opens at http://localhost:3000
```

That's it! 🎉

---

## 📖 Features Deep Dive

### 1️⃣ **Web Interface**

**Dashboard View:**
- File explorer with thumbnails
- Recent operations
- Quick actions panel
- AI chat interface

**Excel Viewer:**
- Spreadsheet grid with editing
- Formula bar
- Sheet tabs
- Formatting controls

**Visualizations:**
- Auto-generated chart suggestions
- Interactive pivot tables
- Custom chart builder
- Export charts as PNG/SVG

### 2️⃣ **AI-Powered Operations**

**Natural Language Processing:**
```
You: "Find all sales over $1000 and highlight them"
AI: ✅ Found 23 rows. Applied yellow highlight.

You: "Create a summary sheet with monthly totals"
AI: ✅ Created "Summary" sheet with pivot table and chart.

You: "Export this as a PDF report"
AI: ✅ Generated report.pdf with charts included.
```

**Smart Suggestions:**
- Detects data patterns
- Suggests visualizations
- Recommends formulas
- Warns about data issues

### 3️⃣ **Templates**

**Pre-built workflows** you can customize:

- 📊 **Sales Report Generator** - Monthly sales with charts
- 📈 **Data Cleaning Wizard** - Remove duplicates, fix formatting
- 💰 **Financial Dashboard** - Income/expense tracking
- 📋 **Inventory Manager** - Stock tracking with alerts
- 📅 **Project Timeline** - Gantt charts from task lists
- 🎯 **KPI Dashboard** - Key metrics with gauges
- 📧 **Mail Merge** - Generate documents from data
- 🔄 **Data Transformation** - Pivot, unpivot, transpose

### 4️⃣ **Batch Operations**

Process multiple files or operations efficiently:

```javascript
// Apply same operation to all files in a folder
Batch.transform({
  files: ["sales_q1.xlsx", "sales_q2.xlsx", "sales_q3.xlsx"],
  operation: "calculate_totals",
  output: "annual_summary.xlsx"
});

// Chain multiple operations
Batch.chain([
  { op: "clean_data", file: "raw_data.xlsx" },
  { op: "add_formulas", file: "raw_data.xlsx" },
  { op: "create_charts", file: "raw_data.xlsx" },
  { op: "export_pdf", file: "raw_data.xlsx", output: "report.pdf" }
]);
```

### 5️⃣ **Visual History & Undo**

**Timeline View:**
```
12:30 PM - Added row to sales.xlsx
12:28 PM - Updated cell B5 to 1500
12:25 PM - Created sheet "Summary"
12:20 PM - Imported data.csv
```

**One-Click Undo:**
- Each operation is backed up
- Click any point in history to rollback
- Compare before/after states
- Restore from specific backup

### 6️⃣ **Export & Reporting**

**Export Formats:**
- 📄 PDF with embedded charts
- 📊 CSV for data portability
- 🖼️ PNG/SVG chart images
- 📧 HTML email templates
- 📋 Markdown reports

**Scheduled Reports:**
```python
# Auto-generate and export every Monday
Schedule.weekly(
  day="Monday",
  template="sales_report",
  export="pdf",
  email=False  # local only!
)
```

---

## 🎨 Interface Walkthrough

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  Ollama Excel Studio                        [Settings] [?]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📁 Files              🤖 AI Assistant      📊 Quick Actions │
│  ┌──────────────┐     ┌──────────────┐    ┌──────────────┐ │
│  │ sales.xlsx   │     │ How can I    │    │ New File     │ │
│  │ 15 KB | 3 📄 │     │ help you?    │    │ Import CSV   │ │
│  └──────────────┘     │              │    │ Templates    │ │
│  ┌──────────────┐     │ [Type here]  │    │ Batch Ops    │ │
│  │ report.xlsx  │     └──────────────┘    └──────────────┘ │
│  │ 23 KB | 5 📄 │                                           │
│  └──────────────┘     📈 Recent Operations                  │
│                       • Updated sales Q3                    │
│  [+ Upload]           • Created summary chart               │
│                       • Exported monthly report             │
└─────────────────────────────────────────────────────────────┘
```

### Excel Editor
```
┌─────────────────────────────────────────────────────────────┐
│  sales.xlsx                              [Save] [Export]    │
├─────────────────────────────────────────────────────────────┤
│  Sheet1  Sheet2  Summary  [+]                               │
├─────────────────────────────────────────────────────────────┤
│  fx  =SUM(B2:B10)                       [Charts] [Format]   │
├───┬───┬────────┬──────────┬──────────┬────────────────────┤
│   │ A │   B    │    C     │    D     │         E          │
├───┼───┼────────┼──────────┼──────────┼────────────────────┤
│ 1 │   │ Jan    │   Feb    │   Mar    │      Total         │
│ 2 │   │ 1200   │   1500   │   1800   │   =SUM(B2:D2)     │
│ 3 │   │ 900    │   1100   │   1300   │   =SUM(B3:D3)     │
│   │   │        │          │          │                    │
└───┴───┴────────┴──────────┴──────────┴────────────────────┘
```

---

## ⚙️ Configuration

Edit `config/studio.json`:

```json
{
  "server": {
    "host": "localhost",
    "port": 3000,
    "apiPort": 8000,
    "enableCORS": false,
    "allowedOrigins": ["http://localhost:3000"]
  },
  "ollama": {
    "baseUrl": "http://localhost:11434",
    "preferredModels": ["qwen2.5:14b-instruct", "llama3.1:8b-instruct"],
    "temperature": 0.2,
    "streamResponse": true
  },
  "excel": {
    "directory": "./data/excel-files",
    "backupDirectory": "./data/backups",
    "maxBackupsPerFile": 20,
    "autoSave": true,
    "autoSaveInterval": 30000
  },
  "features": {
    "enableTemplates": true,
    "enableBatchOps": true,
    "enableExport": true,
    "enableScheduler": false,
    "maxFileSize": 52428800,
    "allowedExtensions": [".xlsx", ".xls", ".csv"]
  },
  "ui": {
    "theme": "light",
    "language": "en",
    "chartDefaults": {
      "width": 800,
      "height": 400,
      "renderer": "svg"
    }
  }
}
```

---

## 🔧 Development

```bash
# Frontend development
cd frontend
npm install
npm run dev

# Backend development  
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Run both (production)
npm run studio

# Build for distribution
npm run build
```

---

## 📁 Project Structure

```
ollama-excel-studio/
├── frontend/                   # React app
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── features/          # Feature modules
│   │   ├── hooks/             # React hooks
│   │   ├── services/          # API clients
│   │   ├── store/             # State management
│   │   ├── types/             # TypeScript types
│   │   └── utils/             # Helpers
│   ├── public/
│   └── package.json
│
├── backend/                    # FastAPI server
│   ├── api/                   # API endpoints
│   ├── core/                  # Core logic
│   ├── services/              # Business logic
│   │   ├── ollama.py         # LLM integration
│   │   ├── excel.py          # Excel operations
│   │   ├── charts.py         # Visualization
│   │   └── templates.py      # Template system
│   ├── models/                # Data models
│   ├── utils/                 # Utilities
│   └── main.py
│
├── mcp-excel-server/          # Original MCP server (reused!)
├── templates/                 # Operation templates
├── data/                      # User data
│   ├── excel-files/
│   ├── backups/
│   └── exports/
├── config/
│   └── studio.json
├── install.sh
├── package.json
└── README.md
```

---

## 🚦 Roadmap

### ✅ Phase 1: Foundation (v5.0) - Current
- Web UI with file management
- Excel viewer/editor
- AI chat integration
- Basic visualizations
- Template system

### 🔄 Phase 2: Advanced Features (v5.1)
- Collaborative editing (local network)
- Advanced charts (Gantt, waterfall, etc.)
- Custom formula builder
- Data validation rules
- Conditional formatting

### 📋 Phase 3: Pro Features (v5.2)
- Python script editor for custom operations
- Plugin system for extensions
- Advanced data analysis (ML predictions)
- Multi-file projects
- Version control integration

### 🌟 Phase 4: Enterprise (v6.0)
- Multi-user support (local network)
- Role-based access control
- Audit logs and compliance
- Advanced scheduling
- Integration with other local tools

---

## 🤝 Upgrading from v4.1

Your existing v4.1 installation works perfectly with v5.0:

```bash
# Keep your v4.1 data
cp -r ../ollama-mcp-excel-v4/excel-files ./data/
cp -r ../ollama-mcp-excel-v4/backups ./data/

# Migrate config
python scripts/migrate_config.py ../ollama-mcp-excel-v4/config.json

# Start using v5.0
npm run studio
```

---

## 🐛 Troubleshooting

**"Port 3000 already in use"**
```bash
# Change port in config/studio.json or
PORT=3001 npm run studio
```

**"Cannot connect to Ollama"**
```bash
# Verify Ollama is running
ollama serve

# Check models
ollama list

# Test connection
curl http://localhost:11434/api/tags
```

**"Python dependencies missing"**
```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

**"Charts not displaying"**
```bash
# Install Plotly
pip install plotly kaleido
```

---

## 📜 License

MIT License - same as v4.1

---

## 🙏 Credits

Built on the excellent foundation of:
- **Ollama-MCP Excel v4.1** by the original team
- **Ollama** for local LLM inference
- **MCP Protocol** by Anthropic
- **React** & **FastAPI** communities
- **openpyxl** for Excel manipulation
- **Plotly** for visualizations

---

## 💬 Support & Community

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions  
- **Docs**: Full documentation at `/docs`
- **Examples**: Check `/examples` folder

---

**Build the open-source future of AI-powered productivity! 🚀**

No cloud. No subscriptions. Just pure local power.
