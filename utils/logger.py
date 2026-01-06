"""
Daily JSON logger for Discord messages
Creates a new JSON file each day with format: YYYY-MM-DD.json
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from colorama import Fore, Style

class DailyLogger:
    """Handles daily JSON logging of Discord messages"""
    
    def __init__(self, logs_dir: Path, timezone_offset: str = '+07:00'):
        self.logs_dir = logs_dir
        self.timezone_offset = timezone_offset
        self.current_file = None
        self.current_date = None
        self._lock = asyncio.Lock()
    
    def _get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format"""
        # For simplicity, using local time
        # In production, you'd want to use pytz for proper timezone handling
        return datetime.now().strftime('%Y-%m-%d')
    
    def _get_log_file_path(self, date_str: str) -> Path:
        """Get the log file path for a specific date"""
        return self.logs_dir / f"{date_str}.json"
    
    async def _ensure_file(self) -> Path:
        """Ensure the current day's log file exists"""
        current_date = self._get_current_date()
        
        # Check if we need to rotate to a new file
        if current_date != self.current_date:
            self.current_date = current_date
            self.current_file = self._get_log_file_path(current_date)
            
            # Create file if it doesn't exist
            if not self.current_file.exists():
                self.current_file.write_text('[]', encoding='utf-8')
                print(f"{Fore.GREEN}📄 Created new log file: {self.current_file.name}")
        
        return self.current_file
    
    async def log_message(self, message_data: Dict[str, Any]):
        """
        Log a message to the current day's JSON file
        
        Args:
            message_data: Dictionary containing message information
        """
        async with self._lock:
            try:
                # Ensure we have the right file
                log_file = await self._ensure_file()
                
                # Read existing data
                existing_data = json.loads(log_file.read_text(encoding='utf-8'))
                
                # Append new message
                existing_data.append(message_data)
                
                # Write back to file (pretty-printed for readability)
                log_file.write_text(
                    json.dumps(existing_data, indent=2, ensure_ascii=False),
                    encoding='utf-8'
                )
                
            except Exception as e:
                print(f"{Fore.RED}❌ Error logging message: {e}")
    
    def format_message(
        self,
        message_id: int,
        timestamp: str,
        author_name: str,
        author_id: int,
        channel_id: int,
        channel_name: str,
        content: str,
        attachments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Format message data for logging
        
        Returns:
            Dictionary with structured message data
        """
        return {
            "message_id": str(message_id),
            "timestamp": timestamp,
            "author": author_name,
            "author_id": str(author_id),
            "channel_id": str(channel_id),
            "channel_name": channel_name,
            "content": content,
            "attachments": attachments
        }

# Global logger instance
_logger_instance = None

def get_logger(logs_dir: Path, timezone_offset: str = '+07:00') -> DailyLogger:
    """Get or create the global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = DailyLogger(logs_dir, timezone_offset)
    return _logger_instance
