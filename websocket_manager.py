"""
WebSocket Manager for real-time updates
Handles client connections and broadcasting messages
"""
from fastapi import WebSocket
from typing import List, Dict, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections and broadcasting"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_info: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_info[websocket] = {
            "connected_at": datetime.utcnow(),
            "messages_sent": 0,
            "messages_received": 0
        }
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
        
        # Send welcome message
        await websocket.send_json({
            "type": "connection_established",
            "message": "Connected to Ollama Excel Studio",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            info = self.connection_info.pop(websocket, {})
            logger.info(
                f"WebSocket disconnected. "
                f"Sent: {info.get('messages_sent', 0)}, "
                f"Received: {info.get('messages_received', 0)}. "
                f"Remaining: {len(self.active_connections)}"
            )
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific client"""
        try:
            await websocket.send_json(message)
            if websocket in self.connection_info:
                self.connection_info[websocket]["messages_sent"] += 1
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any], exclude: WebSocket = None):
        """Broadcast a message to all connected clients"""
        disconnected = []
        
        for connection in self.active_connections:
            if connection == exclude:
                continue
            
            try:
                await connection.send_json(message)
                if connection in self.connection_info:
                    self.connection_info[connection]["messages_sent"] += 1
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_file_update(self, filename: str, operation: str, data: Any = None):
        """Broadcast file update notification"""
        await self.broadcast({
            "type": "file_updated",
            "filename": filename,
            "operation": operation,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def broadcast_operation_progress(
        self,
        operation_id: str,
        progress: float,
        message: str = None
    ):
        """Broadcast operation progress"""
        await self.broadcast({
            "type": "operation_progress",
            "operation_id": operation_id,
            "progress": progress,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def broadcast_error(self, error: str, details: Any = None):
        """Broadcast error notification"""
        await self.broadcast({
            "type": "error",
            "error": error,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about connections"""
        total_sent = sum(
            info.get("messages_sent", 0)
            for info in self.connection_info.values()
        )
        total_received = sum(
            info.get("messages_received", 0)
            for info in self.connection_info.values()
        )
        
        return {
            "active_connections": len(self.active_connections),
            "total_messages_sent": total_sent,
            "total_messages_received": total_received
        }
