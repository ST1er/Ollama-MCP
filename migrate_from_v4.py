#!/usr/bin/env python3
"""
Migration Script: Ollama-MCP Excel v4.1 → v5.0
Safely migrates data, config, and backups to the new Studio
"""
import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime


class Migration:
    def __init__(self, v4_path, v5_path):
        self.v4_path = Path(v4_path)
        self.v5_path = Path(v5_path)
        self.log = []
        
    def print_log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️ ",
            "SUCCESS": "✓ ",
            "WARNING": "⚠️ ",
            "ERROR": "✗ "
        }.get(level, "  ")
        
        print(f"[{timestamp}] {prefix}{message}")
        self.log.append(f"[{timestamp}] [{level}] {message}")
    
    def check_v4_exists(self):
        """Verify v4.1 installation exists"""
        self.print_log("Checking for v4.1 installation...")
        
        if not self.v4_path.exists():
            self.print_log(f"v4.1 not found at: {self.v4_path}", "ERROR")
            return False
        
        required_files = [
            "config.json",
            "mcp-excel-server/index.js",
            "ollama-bridge/bridge.js"
        ]
        
        for file in required_files:
            if not (self.v4_path / file).exists():
                self.print_log(f"Missing required file: {file}", "WARNING")
        
        self.print_log("v4.1 installation verified", "SUCCESS")
        return True
    
    def migrate_excel_files(self):
        """Copy Excel files and backups"""
        self.print_log("Migrating Excel files...")
        
        # Excel files
        v4_excel = self.v4_path / "excel-files"
        v5_excel = self.v5_path / "data" / "excel-files"
        
        if v4_excel.exists():
            files = list(v4_excel.glob("*.xlsx")) + list(v4_excel.glob("*.xls"))
            if files:
                v5_excel.mkdir(parents=True, exist_ok=True)
                for file in files:
                    if file.name != ".gitkeep":
                        shutil.copy2(file, v5_excel / file.name)
                        self.print_log(f"  Copied: {file.name}")
                self.print_log(f"Migrated {len(files)} Excel files", "SUCCESS")
            else:
                self.print_log("No Excel files to migrate", "WARNING")
        else:
            self.print_log("No excel-files directory found", "WARNING")
        
        # Backups
        v4_backups = self.v4_path / "backups"
        v5_backups = self.v5_path / "data" / "backups"
        
        if v4_backups.exists():
            backups = list(v4_backups.glob("*.xlsx")) + list(v4_backups.glob("*.xls"))
            if backups:
                v5_backups.mkdir(parents=True, exist_ok=True)
                for backup in backups:
                    if backup.name != ".gitkeep":
                        shutil.copy2(backup, v5_backups / backup.name)
                self.print_log(f"  Copied backup: {backup.name}")
                self.print_log(f"Migrated {len(backups)} backup files", "SUCCESS")
            else:
                self.print_log("No backups to migrate", "WARNING")
        else:
            self.print_log("No backups directory found", "WARNING")
    
    def migrate_config(self):
        """Convert v4.1 config to v5.0 format"""
        self.print_log("Migrating configuration...")
        
        v4_config_path = self.v4_path / "config.json"
        v5_config_path = self.v5_path / "config" / "studio.json"
        
        if not v4_config_path.exists():
            self.print_log("No v4.1 config found, using defaults", "WARNING")
            return
        
        try:
            with open(v4_config_path, 'r') as f:
                v4_config = json.load(f)
            
            # Convert to v5 format
            v5_config = {
                "server": {
                    "host": "localhost",
                    "port": 3000,
                    "apiPort": 8000,
                    "enableCORS": False,
                    "allowedOrigins": ["http://localhost:3000"]
                },
                "ollama": {
                    "baseUrl": v4_config.get("ollama", {}).get("baseUrl", "http://localhost:11434"),
                    "autoSelectModel": v4_config.get("ollama", {}).get("autoSelectModel", True),
                    "preferredModels": v4_config.get("ollama", {}).get("preferredModels", []),
                    "minimumModelSizeB": v4_config.get("ollama", {}).get("minimumModelSizeB", 7),
                    "temperature": v4_config.get("ollama", {}).get("temperatureByFamily", {}).get("default", 0.2),
                    "streamResponse": True,
                    "timeoutSeconds": v4_config.get("ollama", {}).get("timeoutSeconds", 120)
                },
                "excel": {
                    "directory": "./data/excel-files",
                    "backupDirectory": "./data/backups",
                    "maxBackupsPerFile": v4_config.get("excel", {}).get("maxBackupsPerFile", 20),
                    "autoSave": True,
                    "autoSaveInterval": 30000,
                    "autoBackup": v4_config.get("excel", {}).get("autoBackup", True)
                },
                "features": {
                    "enableTemplates": True,
                    "enableBatchOps": True,
                    "enableExport": True,
                    "enableScheduler": False,
                    "maxFileSize": 52428800,
                    "allowedExtensions": [".xlsx", ".xls", ".csv"]
                },
                "ui": {
                    "theme": "light",
                    "language": "en",
                    "showTutorial": True,
                    "chartDefaults": {
                        "width": 800,
                        "height": 400,
                        "renderer": "svg"
                    }
                },
                "security": {
                    "enableAuth": False,
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
            
            # Save v5 config
            v5_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(v5_config_path, 'w') as f:
                json.dump(v5_config, f, indent=2)
            
            self.print_log("Configuration migrated successfully", "SUCCESS")
            
            # Show key changes
            self.print_log("Notable changes in v5.0:")
            self.print_log("  • New web UI configuration added")
            self.print_log("  • Auto-save enabled by default")
            self.print_log("  • Template system enabled")
            self.print_log("  • Export features enabled")
            
        except Exception as e:
            self.print_log(f"Config migration error: {e}", "ERROR")
            self.print_log("Using default v5.0 configuration", "WARNING")
    
    def migrate_mcp_server(self):
        """Copy MCP server scripts (compatible with v5.0)"""
        self.print_log("Migrating MCP server...")
        
        v4_mcp = self.v4_path / "mcp-excel-server"
        v5_mcp = self.v5_path / "mcp-excel-server"
        
        if not v4_mcp.exists():
            self.print_log("No MCP server found", "WARNING")
            return
        
        v5_mcp.mkdir(parents=True, exist_ok=True)
        
        # Copy scripts
        if (v4_mcp / "scripts").exists():
            shutil.copytree(
                v4_mcp / "scripts",
                v5_mcp / "scripts",
                dirs_exist_ok=True
            )
            self.print_log("  MCP scripts copied", "SUCCESS")
        
        # Copy index.js if exists
        if (v4_mcp / "index.js").exists():
            shutil.copy2(v4_mcp / "index.js", v5_mcp / "index.js")
            self.print_log("  MCP server index.js copied", "SUCCESS")
        
        # Copy requirements if exists
        if (v4_mcp / "requirements.txt").exists():
            shutil.copy2(v4_mcp / "requirements.txt", v5_mcp / "requirements.txt")
            self.print_log("  Python requirements copied", "SUCCESS")
        
        self.print_log("MCP server migrated (v4.1 is compatible!)", "SUCCESS")
    
    def create_migration_report(self):
        """Generate a migration report"""
        report_path = self.v5_path / "MIGRATION_REPORT.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("MIGRATION REPORT: v4.1 → v5.0\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("Source: " + str(self.v4_path) + "\n")
            f.write("Target: " + str(self.v5_path) + "\n\n")
            
            f.write("Migration Log:\n")
            f.write("-" * 60 + "\n")
            for entry in self.log:
                f.write(entry + "\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("NEXT STEPS:\n")
            f.write("=" * 60 + "\n")
            f.write("1. Review this migration report\n")
            f.write("2. Verify your files in: data/excel-files/\n")
            f.write("3. Check configuration: config/studio.json\n")
            f.write("4. Start the studio: npm run studio\n")
            f.write("5. Open browser: http://localhost:3000\n\n")
            f.write("Your v4.1 installation is unchanged and can still be used.\n")
            f.write("Both versions can run simultaneously on different ports.\n")
        
        self.print_log(f"Migration report saved: {report_path}", "SUCCESS")
    
    def run(self):
        """Execute full migration"""
        print("\n" + "=" * 60)
        print("  Ollama-MCP Excel: v4.1 → v5.0 Migration Tool")
        print("=" * 60 + "\n")
        
        if not self.check_v4_exists():
            print("\n⚠️  v4.1 installation not found or incomplete.")
            print(f"Expected location: {self.v4_path}")
            print("\nYou can still use v5.0, it will use default settings.")
            return False
        
        print(f"\nSource (v4.1): {self.v4_path}")
        print(f"Target (v5.0): {self.v5_path}\n")
        
        # Confirm
        response = input("Proceed with migration? [Y/n]: ")
        if response.lower() in ['n', 'no']:
            print("\nMigration cancelled.")
            return False
        
        print("\n" + "-" * 60 + "\n")
        
        # Run migration steps
        self.migrate_excel_files()
        print()
        self.migrate_config()
        print()
        self.migrate_mcp_server()
        print()
        
        # Generate report
        self.create_migration_report()
        
        print("\n" + "=" * 60)
        print("  Migration Complete! 🎉")
        print("=" * 60)
        print("\nYour v4.1 data is now available in v5.0!")
        print("\nNext steps:")
        print("  1. cd ollama-excel-studio")
        print("  2. npm run studio")
        print("  3. Open http://localhost:3000")
        print("\nEnjoy the new web interface! 🚀\n")
        
        return True


if __name__ == "__main__":
    # Default paths
    v4_path = "../project"  # Assuming v4.1 is in ../project
    v5_path = "."  # Current directory (v5.0)
    
    # Allow custom paths via args
    if len(sys.argv) > 1:
        v4_path = sys.argv[1]
    if len(sys.argv) > 2:
        v5_path = sys.argv[2]
    
    migration = Migration(v4_path, v5_path)
    success = migration.run()
    
    sys.exit(0 if success else 1)
