"""
Alert system for critical events
Currently uses console alerts; future: webhook support
"""

from colorama import Fore, Style
from datetime import datetime

class AlertSystem:
    """Handles alerts for critical events"""
    
    @staticmethod
    def alert_token_invalid():
        """Alert when Discord token is invalid or expired"""
        print(f"\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}❌ ALERT: Invalid or Expired Token")
        print(f"{Fore.RED}{'='*60}")
        print(f"{Fore.YELLOW}Your Discord token may be invalid or expired.")
        print(f"{Fore.YELLOW}Please update the DISCORD_TOKEN in your .env file.")
        print(f"\n{Fore.CYAN}To get a new token:")
        print(f"{Fore.CYAN}1. Open Discord in browser")
        print(f"{Fore.CYAN}2. Press F12 → Network tab")
        print(f"{Fore.CYAN}3. Refresh page and find 'authorization' header")
        print(f"{Fore.RED}{'='*60}\n")
    
    @staticmethod
    def alert_connection_lost(retry_count: int, max_retries: int):
        """Alert when connection is lost"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{Fore.YELLOW}⚠️  [{timestamp}] Connection lost!")
        print(f"{Fore.YELLOW}   Retry {retry_count}/{max_retries}...")
    
    @staticmethod
    def alert_connection_restored():
        """Alert when connection is restored"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{Fore.GREEN}✅ [{timestamp}] Connection restored!")
    
    @staticmethod
    def alert_max_retries_exceeded():
        """Alert when max reconnection attempts exceeded"""
        print(f"\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}❌ ALERT: Connection Failed")
        print(f"{Fore.RED}{'='*60}")
        print(f"{Fore.YELLOW}Could not reconnect after multiple attempts.")
        print(f"{Fore.YELLOW}Please check your internet connection.")
        print(f"{Fore.RED}{'='*60}\n")
    
    @staticmethod
    def info_message_received(author: str, channel: str, content_preview: str):
        """Info log for received message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        preview = content_preview[:50] + '...' if len(content_preview) > 50 else content_preview
        print(f"{Fore.CYAN}💬 [{timestamp}] {Fore.WHITE}{author} {Fore.CYAN}in {Fore.WHITE}#{channel}")
        if preview:
            print(f"{Fore.WHITE}   {preview}")
    
    @staticmethod
    def info_startup():
        """Info log for successful startup"""
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}🚀 Discord Stream Monitor Started")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.CYAN}Listening for messages...")
        print(f"{Fore.CYAN}Press Ctrl+C to stop")
        print(f"{Fore.GREEN}{'='*60}\n")

# Global alert system instance
alerts = AlertSystem()
