"""
Ollama Excel Studio - FastAPI Backend v5.0
Main application entry point
"""
from fastapi import FastAPI, WebSocket, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import asyncio
import logging
from datetime import datetime

# Import our services
from services.ollama import OllamaService
from services.excel import ExcelService
from services.charts import ChartService
from services.templates import TemplateService
from models.requests import (
    ChatRequest,
    ExcelOperationRequest,
    ChartRequest,
    TemplateRequest,
    BatchOperationRequest
)
from models.responses import (
    ChatResponse,
    ExcelOperationResponse,
    FileListResponse,
    ChartResponse,
    OperationHistoryResponse
)
from core.config import get_settings
from core.websocket_manager import WebSocketManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
settings = get_settings()

# Initialize services
ollama_service = OllamaService(settings)
excel_service = ExcelService(settings)
chart_service = ChartService(settings)
template_service = TemplateService(settings)
ws_manager = WebSocketManager()

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    logger.info("🚀 Starting Ollama Excel Studio v5.0")
    
    # Verify Ollama connection on startup
    try:
        await ollama_service.check_connection()
        models = await ollama_service.list_models()
        logger.info(f"✓ Connected to Ollama. Found {len(models)} models")
    except Exception as e:
        logger.warning(f"⚠ Ollama not available: {e}")
        logger.warning("AI features will be limited until Ollama is running")
    
    # Ensure data directories exist
    for directory in [
        settings.excel.directory,
        settings.excel.backup_directory,
        settings.export_directory,
        settings.temp_directory,
        settings.logging.directory
    ]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("✓ Data directories verified")
    
    yield
    
    logger.info("👋 Shutting down Ollama Excel Studio")

# Create FastAPI app
app = FastAPI(
    title="Ollama Excel Studio API",
    description="AI-powered Excel automation with local LLMs",
    version="5.0.0",
    lifespan=lifespan
)

# Configure CORS
if not settings.server.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ── Health & Status Endpoints ──────────────────────────────────────────

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "app": "Ollama Excel Studio",
        "version": "5.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check Ollama
    try:
        await ollama_service.check_connection()
        models = await ollama_service.list_models()
        health_status["services"]["ollama"] = {
            "status": "up",
            "models_available": len(models)
        }
    except Exception as e:
        health_status["services"]["ollama"] = {
            "status": "down",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check Excel service
    try:
        files = await excel_service.list_files()
        health_status["services"]["excel"] = {
            "status": "up",
            "files_count": len(files)
        }
    except Exception as e:
        health_status["services"]["excel"] = {
            "status": "down",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status

@app.get("/api/status")
async def get_status():
    """Get detailed system status"""
    try:
        models = await ollama_service.list_models()
        current_model = await ollama_service.get_current_model()
        files = await excel_service.list_files()
        
        return {
            "ollama": {
                "connected": True,
                "current_model": current_model,
                "available_models": models,
                "base_url": settings.ollama.base_url
            },
            "excel": {
                "directory": settings.excel.directory,
                "files_count": len(files),
                "backup_enabled": settings.excel.auto_backup,
                "auto_save": settings.excel.auto_save
            },
            "features": {
                "templates": settings.features.enable_templates,
                "batch_ops": settings.features.enable_batch_ops,
                "export": settings.features.enable_export,
                "scheduler": settings.features.enable_scheduler
            },
            "storage": {
                "max_file_size": settings.features.max_file_size,
                "allowed_extensions": settings.features.allowed_extensions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── File Management Endpoints ──────────────────────────────────────────

@app.get("/api/files", response_model=FileListResponse)
async def list_files():
    """List all Excel files"""
    try:
        files = await excel_service.list_files()
        return FileListResponse(success=True, files=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload an Excel file"""
    try:
        # Validate file extension
        if not any(file.filename.endswith(ext) for ext in settings.features.allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {settings.features.allowed_extensions}"
            )
        
        # Validate file size
        contents = await file.read()
        if len(contents) > settings.features.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.features.max_file_size} bytes"
            )
        
        # Save file
        file_path = await excel_service.save_uploaded_file(file.filename, contents)
        
        return {
            "success": True,
            "filename": file.filename,
            "path": str(file_path),
            "size": len(contents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{filename}")
async def get_file_info(filename: str):
    """Get detailed file information"""
    try:
        info = await excel_service.get_file_info(filename)
        return info
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """Delete a file"""
    try:
        await excel_service.delete_file(filename)
        return {"success": True, "message": f"File {filename} deleted"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{filename}/download")
async def download_file(filename: str):
    """Download a file"""
    try:
        file_path = await excel_service.get_file_path(filename)
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Excel Operations Endpoints ─────────────────────────────────────────

@app.post("/api/excel/read", response_model=ExcelOperationResponse)
async def read_excel(request: ExcelOperationRequest):
    """Read data from Excel file"""
    try:
        result = await excel_service.read_sheet(
            request.filename,
            request.sheet_name,
            request.range
        )
        return ExcelOperationResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/excel/write", response_model=ExcelOperationResponse)
async def write_excel(request: ExcelOperationRequest):
    """Write data to Excel file"""
    try:
        result = await excel_service.write_data(
            request.filename,
            request.sheet_name,
            request.data,
            request.start_cell
        )
        
        # Notify connected clients
        await ws_manager.broadcast({
            "type": "file_updated",
            "filename": request.filename,
            "operation": "write"
        })
        
        return ExcelOperationResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/excel/{filename}/sheets")
async def list_sheets(filename: str):
    """List all sheets in a workbook"""
    try:
        sheets = await excel_service.list_sheets(filename)
        return {"success": True, "sheets": sheets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/excel/create-sheet")
async def create_sheet(request: ExcelOperationRequest):
    """Create a new sheet in a workbook"""
    try:
        result = await excel_service.create_sheet(
            request.filename,
            request.sheet_name
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── AI Chat Endpoints ──────────────────────────────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the AI assistant"""
    try:
        response = await ollama_service.chat(
            request.message,
            request.context,
            request.files
        )
        return ChatResponse(success=True, **response)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "chat":
                # Stream response
                async for chunk in ollama_service.chat_stream(
                    data.get("message"),
                    data.get("context")
                ):
                    await websocket.send_json({
                        "type": "chat_chunk",
                        "content": chunk
                    })
            
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        ws_manager.disconnect(websocket)

# ── Visualization Endpoints ────────────────────────────────────────────

@app.post("/api/charts/create", response_model=ChartResponse)
async def create_chart(request: ChartRequest):
    """Create a chart from Excel data"""
    try:
        chart_data = await chart_service.create_chart(
            request.filename,
            request.sheet_name,
            request.chart_type,
            request.data_range,
            request.options
        )
        return ChartResponse(success=True, chart=chart_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/charts/suggestions/{filename}")
async def suggest_charts(filename: str, sheet_name: Optional[str] = None):
    """Get chart suggestions based on data"""
    try:
        suggestions = await chart_service.suggest_charts(filename, sheet_name)
        return {"success": True, "suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/charts/export/{chart_id}")
async def export_chart(chart_id: str, format: str = "png"):
    """Export chart as image"""
    try:
        image_data = await chart_service.export_chart(chart_id, format)
        return StreamingResponse(
            image_data,
            media_type=f"image/{format}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Template Endpoints ─────────────────────────────────────────────────

@app.get("/api/templates")
async def list_templates():
    """List all available templates"""
    try:
        templates = await template_service.list_templates()
        return {"success": True, "templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/templates/apply")
async def apply_template(request: TemplateRequest):
    """Apply a template to create/modify Excel file"""
    try:
        result = await template_service.apply_template(
            request.template_name,
            request.filename,
            request.parameters
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Batch Operations ───────────────────────────────────────────────────

@app.post("/api/batch/execute")
async def execute_batch(request: BatchOperationRequest):
    """Execute batch operations"""
    if not settings.features.enable_batch_ops:
        raise HTTPException(status_code=403, detail="Batch operations disabled")
    
    try:
        results = await excel_service.execute_batch(
            request.operations,
            request.parallel
        )
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── History & Undo Endpoints ───────────────────────────────────────────

@app.get("/api/history/{filename}", response_model=OperationHistoryResponse)
async def get_history(filename: str, limit: int = 50):
    """Get operation history for a file"""
    try:
        history = await excel_service.get_history(filename, limit)
        return OperationHistoryResponse(success=True, history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/history/{filename}/undo")
async def undo_operation(filename: str, operation_id: str):
    """Undo a specific operation"""
    try:
        result = await excel_service.undo_operation(filename, operation_id)
        
        # Notify clients
        await ws_manager.broadcast({
            "type": "file_updated",
            "filename": filename,
            "operation": "undo",
            "operation_id": operation_id
        })
        
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/backups/{filename}")
async def list_backups(filename: str):
    """List all backups for a file"""
    try:
        backups = await excel_service.list_backups(filename)
        return {"success": True, "backups": backups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/backups/{filename}/restore")
async def restore_backup(filename: str, backup_id: str):
    """Restore from a backup"""
    try:
        result = await excel_service.restore_backup(filename, backup_id)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Export Endpoints ───────────────────────────────────────────────────

@app.post("/api/export/pdf")
async def export_pdf(filename: str, sheet_name: Optional[str] = None):
    """Export Excel to PDF"""
    if not settings.features.enable_export:
        raise HTTPException(status_code=403, detail="Export disabled")
    
    try:
        pdf_path = await excel_service.export_to_pdf(filename, sheet_name)
        return FileResponse(
            path=pdf_path,
            filename=f"{filename}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/csv")
async def export_csv(filename: str, sheet_name: str):
    """Export sheet to CSV"""
    try:
        csv_path = await excel_service.export_to_csv(filename, sheet_name)
        return FileResponse(
            path=csv_path,
            filename=f"{sheet_name}.csv",
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Error Handlers ─────────────────────────────────────────────────────

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"detail": "Not found"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal error: {exc}")
    return {"detail": "Internal server error"}

# ── Main Entry Point ───────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.server.host,
        port=settings.server.api_port,
        reload=True,
        log_level="info"
    )
