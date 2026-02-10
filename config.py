"""
Configuration management for Ollama Excel Studio
Uses pydantic-settings for type-safe configuration
"""
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import json
from functools import lru_cache


class ServerConfig(BaseModel):
    """Server configuration"""
    host: str = "localhost"
    port: int = 3000
    api_port: int = 8000
    enable_cors: bool = False
    allowed_origins: List[str] = ["http://localhost:3000"]


class OllamaConfig(BaseModel):
    """Ollama LLM configuration"""
    base_url: str = "http://localhost:11434"
    auto_select_model: bool = True
    preferred_models: List[str] = [
        "qwen2.5:32b-instruct",
        "qwen2.5:14b-instruct",
        "llama3.1:8b-instruct"
    ]
    minimum_model_size_b: int = 7
    temperature: float = 0.2
    stream_response: bool = True
    timeout_seconds: int = 120


class ExcelConfig(BaseModel):
    """Excel file handling configuration"""
    directory: str = "./data/excel-files"
    backup_directory: str = "./data/backups"
    max_backups_per_file: int = 20
    auto_save: bool = True
    auto_save_interval: int = 30000
    auto_backup: bool = True


class FeaturesConfig(BaseModel):
    """Feature flags"""
    enable_templates: bool = True
    enable_batch_ops: bool = True
    enable_export: bool = True
    enable_scheduler: bool = False
    max_file_size: int = 52428800  # 50MB
    allowed_extensions: List[str] = [".xlsx", ".xls", ".csv"]


class UIConfig(BaseModel):
    """UI preferences"""
    theme: str = "light"
    language: str = "en"
    show_tutorial: bool = True
    chart_defaults: dict = {
        "width": 800,
        "height": 400,
        "renderer": "svg"
    }


class SecurityConfig(BaseModel):
    """Security settings"""
    enable_auth: bool = False
    session_timeout: int = 3600
    max_login_attempts: int = 5


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    directory: str = "./logs"
    max_files: int = 10
    max_file_size: int = 10485760  # 10MB


class Settings(BaseSettings):
    """Main application settings"""
    server: ServerConfig = Field(default_factory=ServerConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    excel: ExcelConfig = Field(default_factory=ExcelConfig)
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Additional computed properties
    @property
    def export_directory(self) -> str:
        return "./data/exports"
    
    @property
    def temp_directory(self) -> str:
        return "./data/temp"
    
    @property
    def template_directory(self) -> str:
        return "./templates"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_config_from_file(config_path: str = "./config/studio.json") -> Settings:
    """Load configuration from JSON file"""
    try:
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            return Settings(
                server=ServerConfig(**config_data.get("server", {})),
                ollama=OllamaConfig(**config_data.get("ollama", {})),
                excel=ExcelConfig(**config_data.get("excel", {})),
                features=FeaturesConfig(**config_data.get("features", {})),
                ui=UIConfig(**config_data.get("ui", {})),
                security=SecurityConfig(**config_data.get("security", {})),
                logging=LoggingConfig(**config_data.get("logging", {}))
            )
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        print("Using default configuration")
    
    return Settings()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return load_config_from_file()


def save_config(settings: Settings, config_path: str = "./config/studio.json"):
    """Save configuration to JSON file"""
    config_data = {
        "server": settings.server.model_dump(),
        "ollama": settings.ollama.model_dump(),
        "excel": settings.excel.model_dump(),
        "features": settings.features.model_dump(),
        "ui": settings.ui.model_dump(),
        "security": settings.security.model_dump(),
        "logging": settings.logging.model_dump()
    }
    
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)


# Export for easy imports
__all__ = ['Settings', 'get_settings', 'save_config', 'load_config_from_file']
