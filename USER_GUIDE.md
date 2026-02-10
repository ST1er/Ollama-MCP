# 📚 Ollama Excel Studio - Complete User Guide

**Version 5.0 | February 2026**

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Interface Overview](#interface-overview)
3. [Working with Files](#working-with-files)
4. [AI Assistant Usage](#ai-assistant-usage)
5. [Creating Visualizations](#creating-visualizations)
6. [Using Templates](#using-templates)
7. [Batch Operations](#batch-operations)
8. [History & Undo](#history--undo)
9. [Export Options](#export-options)
10. [Keyboard Shortcuts](#keyboard-shortcuts)
11. [Tips & Best Practices](#tips--best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 🚀 First Time Setup (5 minutes)

1. **Install & Start Ollama**
   ```bash
   # Download from: https://ollama.ai
   ollama serve
   
   # Pull a recommended model
   ollama pull qwen2.5:14b-instruct
   ```

2. **Launch the Studio**
   ```bash
   cd ollama-excel-studio
   npm run studio
   ```

3. **Open Your Browser**
   - Automatically opens at http://localhost:3000
   - Or manually navigate there

4. **Upload Your First File**
   - Click "Upload Files" or drag & drop
   - Try asking the AI: "What's in this file?"

### ✨ Your First AI Interaction

```
You: What sheets are in sales.xlsx?
AI: Found 3 sheets: Q1, Q2, Q3

You: Show me all rows where revenue is over 50000
AI: Found 12 matching rows. Would you like me to create a summary?

You: Yes, create a summary sheet with totals
AI: ✓ Created "Summary" sheet with monthly totals and a chart
```

---

## Interface Overview

### Main Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] Ollama Excel Studio v5.0        Status    [Settings]│
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│ Sidebar  │              Main Content Area                   │
│          │                                                   │
│ • Dash   │   Displays: Files, Editor, Chat, Charts, etc.   │
│ • Editor │                                                   │
│ • Chat   │                                                   │
│ • Charts │                                                   │
│ • Temps  │                                                   │
│ • Hist   │                                                   │
│          │                                                   │
└──────────┴──────────────────────────────────────────────────┘
```

### Status Bar (Top Right)

Shows real-time information:
- **Ollama**: ✓ Active (3 models) or ⚠ Disconnected
- **Files**: Number of Excel files in your workspace
- **Model**: Currently selected AI model
- **Auto-save**: Status indicator

---

## Working with Files

### Uploading Files

**Method 1: Drag & Drop**
- Drag .xlsx, .xls, or .csv files anywhere on the dashboard
- Files appear instantly in the file list

**Method 2: Upload Button**
- Click "Upload Files" button
- Select single or multiple files
- Maximum size: 50 MB per file (configurable)

**Method 3: Import CSV**
- Use "Import CSV" quick action
- Automatically converts to .xlsx format
- Preserves formatting and data types

### File Operations

**View File Info**
- Click on any file to see:
  - Sheet count
  - Row/column counts
  - File size
  - Last modified
  - Number of backups

**Download File**
- Click the download icon
- Downloads current version
- Includes all recent changes

**Delete File**
- Click trash icon
- Requires confirmation
- Creates final backup before deletion

### File Organization

Files are stored in: `./data/excel-files/`
Backups are saved in: `./data/backups/`

**Naming Convention:**
```
sales.xlsx                    → Original file
sales.backup-20260210-143055.xlsx → Auto backup
sales.backup-20260210-150230.xlsx → Another backup
```

---

## AI Assistant Usage

### Starting a Conversation

1. Click "AI Assistant" in sidebar
2. Type your question or request
3. AI responds with actions and results

### Natural Language Examples

**Reading Data:**
```
"What's in cell B5 of sales.xlsx?"
"Show me the first 10 rows of the Q1 sheet"
"List all unique values in column C"
"How many rows are in this file?"
```

**Writing Data:**
```
"Set B5 to 1500"
"Add a new row: ['John', 25, 'Active']"
"Update all values in column D to 0"
"Fill cells A1 to A10 with sequential numbers"
```

**Analysis:**
```
"Find all rows where sales > 1000"
"Calculate the average of column B"
"What's the total revenue for Q3?"
"Which month had the highest sales?"
```

**Formatting & Structure:**
```
"Create a new sheet called Summary"
"Delete the Temp sheet"
"Sort by column A ascending"
"Add a header row with: Name, Age, Status"
```

**Advanced Operations:**
```
"Create a pivot table showing sales by region"
"Generate a monthly summary with charts"
"Find and remove duplicate rows"
"Highlight all cells where value < 100"
```

### AI Response Types

The AI can:
1. **Execute operations** and show results
2. **Ask clarifying questions** if needed
3. **Suggest next steps** based on your data
4. **Warn about potential issues** before making changes
5. **Explain what it's doing** in simple terms

### Context Awareness

The AI remembers:
- Your current file selection
- Recent operations (last 10 turns)
- Sheet names and structure
- Previous questions in the conversation

**Example of context:**
```
You: Open sales.xlsx
AI: ✓ Loaded sales.xlsx (3 sheets, 150 rows)

You: What's in the Q1 sheet?        [AI knows you mean sales.xlsx]
AI: Q1 has 45 rows with columns: Date, Product, Revenue...

You: Show me rows where revenue > 5000   [AI knows Q1 sheet]
AI: Found 12 matching rows...

You: Create a chart                 [AI knows the filtered data]
AI: Created bar chart of high-revenue products
```

---

## Creating Visualizations

### Auto-Suggested Charts

When viewing data, the AI automatically suggests charts:

```
AI: I notice you have time-series data. 
    Suggested charts:
    📈 Line chart (trend over time)
    📊 Bar chart (compare periods)
    🥧 Pie chart (proportion breakdown)
```

### Manual Chart Creation

1. **From the Charts Tab:**
   - Select your data file
   - Choose chart type
   - Configure options
   - Generate chart

2. **Via AI Assistant:**
   ```
   "Create a line chart of sales over time"
   "Make a pie chart showing market share"
   "Generate a bar chart comparing Q1, Q2, Q3"
   ```

### Supported Chart Types

| Type | Best For | Example Request |
|------|----------|----------------|
| **Line** | Trends over time | "Show sales trend for 2025" |
| **Bar** | Comparing categories | "Compare revenue by region" |
| **Pie** | Proportions/percentages | "Show expense breakdown" |
| **Scatter** | Correlation analysis | "Plot price vs. demand" |
| **Area** | Cumulative data | "Show stacked revenue streams" |
| **Heatmap** | Matrix data | "Visualize sales by day/hour" |
| **Box** | Statistical distribution | "Show price distribution" |

### Chart Customization

**Interactive Features:**
- Zoom and pan
- Hover for details
- Click to filter
- Export as PNG/SVG
- Embed in Excel sheet

**Styling Options:**
- Color schemes
- Axis labels
- Legend position
- Grid lines
- Annotations

### Exporting Charts

```
You: Export this chart as PNG
AI: ✓ Saved to ./data/exports/sales_chart_20260210.png

You: Add this chart to the Summary sheet
AI: ✓ Chart embedded in Summary sheet at cell A1
```

---

## Using Templates

### Template Categories

**📊 Sales & Marketing**
- Monthly Sales Report
- Sales Forecast Dashboard
- Customer Segmentation Analysis
- Marketing ROI Tracker

**💰 Finance & Accounting**
- Budget Tracker
- Expense Report
- Cash Flow Statement
- Financial Dashboard

**📦 Operations & Inventory**
- Inventory Management
- Order Tracking System
- Project Timeline (Gantt)
- Resource Allocation

**📈 Analytics & Reporting**
- KPI Dashboard
- Data Cleaning Wizard
- Pivot Table Generator
- Executive Summary

### Applying Templates

**Method 1: Template Gallery**
1. Click "Templates" in sidebar
2. Browse categories
3. Click "Use Template"
4. Configure parameters
5. Generate file

**Method 2: AI Command**
```
You: Apply the sales report template to Q1_data.xlsx
AI: Which template?
    1. Basic Sales Report
    2. Advanced Sales Dashboard
    3. Sales Forecast Model
    
You: Option 2
AI: ✓ Generated sales dashboard with:
    - Summary sheet
    - Monthly breakdown
    - Trend charts
    - Top performers table
```

### Custom Templates

**Create Your Own:**

1. Design your template file
2. Save in `./templates/custom/`
3. Add configuration in JSON:

```json
{
  "name": "My Template",
  "category": "custom",
  "description": "Does X, Y, Z",
  "parameters": {
    "date_column": "string",
    "metric_column": "string",
    "grouping": "string"
  },
  "script": "my_template.py"
}
```

4. Template appears in gallery

---

## Batch Operations

### What Are Batch Operations?

Process multiple files or apply multiple operations at once.

### Use Cases

**Scenario 1: Process Monthly Reports**
```javascript
Apply same calculation to Jan.xlsx, Feb.xlsx, Mar.xlsx
→ Add totals row
→ Calculate percentages
→ Format as currency
→ Generate summary
```

**Scenario 2: Data Consolidation**
```javascript
Combine multiple files into one:
→ Read all sheets from 5 files
→ Merge into master file
→ Remove duplicates
→ Sort by date
```

**Scenario 3: Automated Reports**
```javascript
For each file in folder:
→ Clean data
→ Add formulas
→ Create charts
→ Export as PDF
```

### Running Batch Operations

**Via Web Interface:**
1. Go to Dashboard
2. Click "Batch Ops"
3. Select operation type
4. Choose files
5. Configure settings
6. Click "Execute"
7. Monitor progress

**Via AI:**
```
You: For all files in the folder, calculate column B total
AI: Found 5 files. This will:
    1. Add totals for column B in each file
    2. Create backups before modifying
    3. Save results
    
    Continue? [Yes] [No]

You: Yes
AI: Processing...
    ✓ file1.xlsx (Total: 15,230)
    ✓ file2.xlsx (Total: 22,105)
    ✓ file3.xlsx (Total: 18,940)
    ✓ file4.xlsx (Total: 21,550)
    ✓ file5.xlsx (Total: 19,875)
    
    All done! Total processed: 97,700
```

### Batch Safety Features

- **Preview mode**: See what will change before applying
- **Auto-backup**: Every file backed up before modification
- **Error handling**: Failed operations don't affect other files
- **Progress tracking**: Real-time updates
- **Undo all**: Revert entire batch with one click

---

## History & Undo

### Operation Timeline

Every change is recorded:
- **What** changed
- **When** it happened
- **Who/what** made the change (AI or manual)
- **Before/after** states

### Viewing History

**Timeline View:**
```
Today 2:45 PM  - Updated cell B5 to 1500 (sales.xlsx)
Today 2:30 PM  - Created Summary sheet (sales.xlsx)
Today 2:15 PM  - Imported data from CSV
Today 1:50 PM  - Deleted Temp sheet (report.xlsx)
Yesterday      - Applied sales template
```

**Filter Options:**
- By file
- By operation type
- By date range
- By AI vs manual edits

### Undoing Operations

**Method 1: Click to Undo**
- Click any operation in timeline
- Confirms: "Restore to this point?"
- Reverts all changes after that point

**Method 2: AI Command**
```
You: Undo the last change
AI: ✓ Reverted update to cell B5

You: Undo all changes today
AI: This will undo 7 operations. Continue?
You: Yes
AI: ✓ Restored to yesterday's state
```

**Method 3: Manual Backup Restore**
```bash
# List backups
You: Show me all backups for sales.xlsx

AI: Found 8 backups:
    1. 10:30 AM today (before AI edits)
    2. 9:15 AM today (original upload)
    3. Yesterday 5:00 PM
    ...

# Restore specific backup
You: Restore backup #2
AI: ✓ Restored sales.xlsx to 9:15 AM state
```

### Compare States

```
You: Compare current sales.xlsx with version from 2 hours ago

AI: Changes detected:
    ✓ Cell B5: 1200 → 1500
    ✓ New sheet: Summary
    ✓ Row 45: Added
    ✓ Column D: Formula changed
    
    [Restore Old] [Keep Current] [View Details]
```

---

## Export Options

### PDF Reports

**Quick Export:**
```
You: Export sales.xlsx as PDF
AI: ✓ Generated sales_20260210.pdf
    Includes:
    - All sheets
    - Charts embedded
    - Formatted tables
    
    [Download] [Email] [Print]
```

**Custom PDF:**
- Select specific sheets
- Include/exclude charts
- Add header/footer
- Set page layout
- Add cover page

### CSV Export

```
You: Export Q1 sheet as CSV
AI: ✓ Saved Q1.csv (UTF-8 encoding)
```

**Options:**
- Delimiter: comma, tab, semicolon
- Encoding: UTF-8, UTF-16, ASCII
- Include headers: yes/no
- Quote strings: always, auto, never

### Chart Images

```
You: Export all charts as PNG
AI: ✓ Exported 3 charts:
    - sales_trend.png (800x400)
    - revenue_breakdown.png (800x400)
    - monthly_comparison.png (800x400)
```

**Formats:**
- PNG (recommended)
- SVG (vector)
- PDF (print-ready)

### Scheduled Exports

```python
# Export every Monday morning
Schedule:
  - Frequency: Weekly
  - Day: Monday
  - Time: 08:00
  - Template: Sales Report
  - Export: PDF
  - Destination: ./data/exports/weekly/
```

---

## Keyboard Shortcuts

### Global

| Shortcut | Action |
|----------|--------|
| `Ctrl + /` | Open AI chat |
| `Ctrl + O` | Open file |
| `Ctrl + S` | Save current file |
| `Ctrl + Z` | Undo last operation |
| `Ctrl + Shift + Z` | Redo |
| `Ctrl + F` | Find in current sheet |
| `Ctrl + H` | Find and replace |
| `Escape` | Close dialog/panel |

### Excel Editor

| Shortcut | Action |
|----------|--------|
| `Arrow Keys` | Navigate cells |
| `Enter` | Edit cell / Move down |
| `Tab` | Move to next cell |
| `Shift + Enter` | Move up |
| `Ctrl + Home` | Go to A1 |
| `Ctrl + End` | Go to last cell |
| `Ctrl + C` | Copy |
| `Ctrl + V` | Paste |
| `Delete` | Clear cell |

### Charts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Alt + C` | Create chart |
| `Ctrl + E` | Export chart |
| `+` / `-` | Zoom in/out |

---

## Tips & Best Practices

### 🎯 General Tips

1. **Start Small**
   - Test AI commands on sample data first
   - Verify results before batch operations

2. **Use Descriptive Names**
   - Good: `sales_q1_2026.xlsx`
   - Bad: `untitled_1.xlsx`

3. **Leverage Auto-Backup**
   - Don't disable it
   - Backups saved you from mistakes

4. **Organize with Sheets**
   - Raw data → one sheet
   - Calculations → another sheet
   - Summary → final sheet

5. **Ask AI for Help**
   - Not sure how? Just ask!
   - "How do I calculate monthly average?"
   - "What's the best way to visualize this?"

### 📊 Data Management

1. **Keep Raw Data Separate**
   ```
   Sheet1: "Raw Data" (never modified)
   Sheet2: "Cleaned" (processed version)
   Sheet3: "Analysis" (calculations)
   ```

2. **Use Consistent Formatting**
   - Date format: YYYY-MM-DD
   - Currency: Always include symbol
   - Numbers: Same decimal places

3. **Add Headers**
   - Every column should have a clear header
   - Helps AI understand your data

### 🤖 AI Best Practices

1. **Be Specific**
   - ❌ "Update the numbers"
   - ✓ "Set all values in column B to 0"

2. **Confirm Important Changes**
   - AI will ask before deleting/overwriting
   - Always review batch operation previews

3. **Use Context**
   - Reference previous messages
   - "Use the same format as before"
   - "Apply this to all similar cells"

4. **Break Down Complex Tasks**
   - Instead of: "Create complete financial dashboard"
   - Try: 
     1. "Calculate monthly totals"
     2. "Add percentage change column"
     3. "Create trend chart"
     4. "Format as currency"

### 🚀 Performance

1. **File Size**
   - Keep files under 10 MB when possible
   - Large files (50 MB+) may be slow

2. **Batch Operations**
   - Process 10-20 files at a time
   - For more, split into multiple batches

3. **Charts**
   - Limit data points for smooth interaction
   - Use data sampling for huge datasets

---

## Troubleshooting

### Ollama Connection Issues

**Problem:** "Ollama: Disconnected" in status bar

**Solutions:**
```bash
# 1. Check if Ollama is running
curl http://localhost:11434/api/tags

# 2. Start Ollama
ollama serve

# 3. Verify models are installed
ollama list

# 4. Pull a model if needed
ollama pull qwen2.5:14b-instruct
```

**Still not working?**
- Check firewall settings
- Verify port 11434 is not blocked
- Restart both Ollama and the studio

### File Upload Failures

**Problem:** "Failed to upload file"

**Common causes:**
1. File too large (>50 MB)
   - Solution: Split into smaller files or increase limit in config

2. Invalid file format
   - Solution: Convert to .xlsx first

3. File is open in Excel
   - Solution: Close Excel before uploading

4. Disk space full
   - Solution: Free up space or change data directory

### AI Not Responding

**Problem:** AI doesn't respond to messages

**Checklist:**
- [ ] Ollama is running
- [ ] A model is pulled
- [ ] Model size > 7B (smaller models unreliable)
- [ ] Check backend logs: `./logs/`

**Quick fix:**
```bash
# Restart backend
cd ollama-excel-studio
npm run studio
```

### Slow Performance

**Problem:** Operations take too long

**Optimizations:**
1. **Use a faster model**
   - Switch from 32B to 14B model
   - Smaller = faster (but less capable)

2. **Reduce file size**
   - Remove unnecessary sheets
   - Delete old data
   - Use CSV for large datasets

3. **Close other apps**
   - Ollama uses GPU/CPU intensively
   - Free up resources

4. **Increase timeout**
   - Edit `config/studio.json`
   - Increase `ollama.timeoutSeconds`

### Charts Not Displaying

**Problem:** Charts show as blank or error

**Solutions:**
```bash
# 1. Check Plotly installation
pip install plotly kaleido --break-system-packages

# 2. Clear browser cache
# Ctrl + Shift + R (hard refresh)

# 3. Check browser console
# F12 → Console → Look for errors
```

### Backup/Restore Issues

**Problem:** "Backup failed" error

**Causes:**
1. Insufficient disk space
2. Backup directory doesn't exist
3. File permissions

**Fix:**
```bash
# Create backup directory
mkdir -p data/backups
chmod 755 data/backups

# Check disk space
df -h

# Check file permissions
ls -la data/
```

### Common Error Messages

**"Model too small"**
- Your model is < 7B parameters
- Use: `ollama pull qwen2.5:14b-instruct`

**"Sheet not found"**
- Sheet name typo
- Sheet was deleted
- Use `list_sheets` to see available sheets

**"Cell reference invalid"**
- Format should be: A1, B5, AA100
- Not: A-1, B.5, 1A

**"Permission denied"**
- File is read-only
- File is locked by another program
- Check file permissions

### Getting Help

**Resources:**
1. This guide (you're reading it!)
2. GitHub Issues: Report bugs
3. Discussions: Ask questions
4. Logs: `./logs/` for detailed errors

**Before asking for help, provide:**
- Error message (full text)
- What you were trying to do
- Ollama version: `ollama --version`
- Studio version: v5.0
- System: Windows/Mac/Linux

---

## Advanced Topics

### Custom Scripts

Want to add your own Excel operations? See `docs/CUSTOM_SCRIPTS.md`

### API Reference

Build integrations with the Studio? See `docs/API.md`

### Configuration Guide

Detailed config options: See `docs/CONFIGURATION.md`

### Performance Tuning

Optimize for your system: See `docs/PERFORMANCE.md`

---

**Questions?** Ask the AI assistant: "How do I...?"

**Found a bug?** Create an issue on GitHub

**Love the Studio?** Star us on GitHub! ⭐

---

*Made with ❤️ by the Ollama Excel Studio team*  
*MIT License | 100% Local | 100% Free*
