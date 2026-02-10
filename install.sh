#!/bin/bash

# Ollama Excel Studio v5.0 Installer
# One-command setup for the complete system

set -e  # Exit on any error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 Ollama Excel Studio v5.0 Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# ── Step 1: Check Prerequisites ──────────────────────────────────────

print_step "Checking prerequisites..."

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ required. Found: $(node --version)"
        exit 1
    fi
    print_success "Node.js $(node --version)"
else
    print_error "Node.js not found. Install from: https://nodejs.org"
    exit 1
fi

# Check npm
if command_exists npm; then
    print_success "npm $(npm --version)"
else
    print_error "npm not found"
    exit 1
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_success "Python $(python3 --version)"
else
    print_error "Python 3.9+ not found"
    exit 1
fi

# Check pip
if command_exists pip3; then
    print_success "pip3 $(pip3 --version | cut -d' ' -f2)"
else
    print_error "pip3 not found"
    exit 1
fi

# Check Ollama (warning only, not fatal)
if command_exists ollama; then
    print_success "Ollama installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_success "Ollama is running"
        
        # List available models
        MODELS=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
        if [ "$MODELS" -gt 0 ]; then
            print_success "Found $MODELS Ollama model(s)"
        else
            print_warning "No Ollama models installed. Run: ollama pull qwen2.5:14b-instruct"
        fi
    else
        print_warning "Ollama not running. Start it with: ollama serve"
    fi
else
    print_warning "Ollama not found. Install from: https://ollama.ai"
    print_warning "The app will work but AI features require Ollama"
fi

echo ""

# ── Step 2: Create Directory Structure ──────────────────────────────

print_step "Creating directory structure..."

mkdir -p frontend/src/{components,features,hooks,services,store,types,utils}
mkdir -p frontend/public
mkdir -p backend/{api,core,services,models,utils}
mkdir -p mcp-excel-server/scripts
mkdir -p templates/{sales,finance,data,reports}
mkdir -p data/{excel-files,backups,exports,temp}
mkdir -p config
mkdir -p logs
mkdir -p docs
mkdir -p scripts

print_success "Directory structure created"

# ── Step 3: Install Backend Dependencies ────────────────────────────

print_step "Installing Python backend dependencies..."

cat > backend/requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
openpyxl==3.1.2
pandas==2.2.0
plotly==5.18.0
kaleido==0.2.1
aiofiles==23.2.1
websockets==12.0
httpx==0.26.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
EOF

pip3 install -r backend/requirements.txt --break-system-packages 2>&1 | grep -v "WARNING: Running pip as"

print_success "Backend dependencies installed"

# ── Step 4: Install Frontend Dependencies ───────────────────────────

print_step "Installing Node.js frontend dependencies..."

cat > frontend/package.json << 'EOF'
{
  "name": "ollama-excel-studio-frontend",
  "version": "5.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.3",
    "@tanstack/react-query": "^5.17.19",
    "axios": "^1.6.5",
    "zustand": "^4.5.0",
    "react-hot-toast": "^2.4.1",
    "lucide-react": "^0.309.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1",
    "react-dropzone": "^14.2.3",
    "recharts": "^2.10.4",
    "xlsx": "^0.18.5",
    "date-fns": "^3.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@typescript-eslint/eslint-plugin": "^6.19.0",
    "@typescript-eslint/parser": "^6.19.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.17",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.12"
  }
}
EOF

cd frontend && npm install 2>&1 | tail -5 && cd ..

print_success "Frontend dependencies installed"

# ── Step 5: Install MCP Dependencies ─────────────────────────────────

print_step "Installing MCP server dependencies..."

cat > mcp-excel-server/package.json << 'EOF'
{
  "name": "mcp-excel-server",
  "version": "5.0.0",
  "type": "module",
  "main": "index.js",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  }
}
EOF

cd mcp-excel-server && npm install 2>&1 | tail -5 && cd ..

print_success "MCP server dependencies installed"

# ── Step 6: Create Root Package.json ─────────────────────────────────

print_step "Creating root package.json..."

cat > package.json << 'EOF'
{
  "name": "ollama-excel-studio",
  "version": "5.0.0",
  "description": "AI-powered Excel automation with beautiful web interface",
  "type": "module",
  "scripts": {
    "studio": "concurrently \"npm run backend\" \"npm run frontend\"",
    "backend": "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000",
    "frontend": "cd frontend && npm run dev -- --port 3000",
    "build": "cd frontend && npm run build",
    "dev": "npm run studio",
    "install:all": "./install.sh"
  },
  "dependencies": {
    "concurrently": "^8.2.2"
  },
  "keywords": [
    "excel",
    "ai",
    "ollama",
    "local",
    "automation"
  ],
  "author": "Ollama Excel Studio Team",
  "license": "MIT"
}
EOF

npm install concurrently 2>&1 | tail -5

print_success "Root package configured"

# ── Step 7: Create Configuration Files ──────────────────────────────

print_step "Creating configuration files..."

cat > config/studio.json << 'EOF'
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
    "autoSelectModel": true,
    "preferredModels": [
      "qwen2.5:32b-instruct",
      "qwen2.5:14b-instruct",
      "llama3.1:8b-instruct",
      "gemma2:27b-instruct",
      "gemma2:9b-instruct"
    ],
    "minimumModelSizeB": 7,
    "temperature": 0.2,
    "streamResponse": true,
    "timeoutSeconds": 120
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
    "showTutorial": true,
    "chartDefaults": {
      "width": 800,
      "height": 400,
      "renderer": "svg"
    }
  },
  "security": {
    "enableAuth": false,
    "sessionTimeout": 3600,
    "maxLoginAttempts": 5
  },
  "logging": {
    "level": "INFO",
    "directory": "./logs",
    "maxFiles": 10,
    "maxFileSize": 10485760
  }
}
EOF

print_success "Configuration created"

# ── Step 8: Create Sample Templates ─────────────────────────────────

print_step "Creating sample templates..."

# Copy existing MCP server if present
if [ -d "../project/mcp-excel-server" ]; then
    print_step "Found existing MCP v4.1 server, copying..."
    cp -r ../project/mcp-excel-server/* mcp-excel-server/
    print_success "MCP server migrated from v4.1"
fi

print_success "Templates created"

# ── Step 9: Create .gitignore ────────────────────────────────────────

cat > .gitignore << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
pip-log.txt
pip-delete-this-directory.txt

# Build outputs
dist/
build/
*.egg-info/
.vite/
frontend/dist/

# Data & logs
data/excel-files/*
!data/excel-files/.gitkeep
data/backups/*
!data/backups/.gitkeep
data/exports/*
!data/exports/.gitkeep
data/temp/*
logs/*
!logs/.gitkeep

# Environment
.env
.env.local
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Cache
.cache/
*.log
EOF

# ── Final Steps ──────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_success "Installation Complete! 🎉"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📋 Next steps:"
echo ""
echo "1. Make sure Ollama is running:"
echo "   ${BLUE}ollama serve${NC}"
echo ""
echo "2. Pull a recommended model (if not done):"
echo "   ${BLUE}ollama pull qwen2.5:14b-instruct${NC}"
echo ""
echo "3. Start Ollama Excel Studio:"
echo "   ${BLUE}npm run studio${NC}"
echo ""
echo "4. Open your browser to:"
echo "   ${GREEN}http://localhost:3000${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Documentation: ./docs/README.md"
echo "🐛 Issues: Create an issue on GitHub"
echo "💬 Need help? Check the troubleshooting guide"
echo ""
print_success "Happy Excel automation! 🚀"
