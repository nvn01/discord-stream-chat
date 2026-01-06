"""
Configuration loader for Discord Stream Monitor
Loads and validates environment variables from .env file
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.channel_ids = self._parse_channel_ids()
        self.alert_webhook = os.getenv('ALERT_WEBHOOK')
        self.timezone_offset = os.getenv('TIMEZONE_OFFSET', '+07:00')
        
        # Directory paths
        self.base_dir = Path(__file__).parent
        self.logs_dir = self.base_dir / 'logs'
        self.downloads_dir = self.base_dir / 'downloads'
        
        # Create directories if they don't exist
        self.logs_dir.mkdir(exist_ok=True)
        self.downloads_dir.mkdir(exist_ok=True)
        
        # Validate configuration
        self._validate()
    
    def _parse_channel_ids(self):
        """Parse comma-separated channel IDs from environment variable"""
        channel_ids_str = os.getenv('CHANNEL_IDS', '')
        
        if not channel_ids_str:
            return []
        
        # Split by comma and convert to integers
        try:
            return [int(cid.strip()) for cid in channel_ids_str.split(',') if cid.strip()]
        except ValueError:
            print(f"{Fore.RED}❌ Error: CHANNEL_IDS must be comma-separated numbers")
            sys.exit(1)
    
    def _validate(self):
        """Validate required configuration values"""
        errors = []
        
        # Check Discord token
        if not self.discord_token:
            errors.append("DISCORD_TOKEN is required")
        elif self.discord_token == 'your_token_here':
            errors.append("DISCORD_TOKEN must be replaced with your actual token")
        elif self.discord_token.startswith('Bot '):
            errors.append("DISCORD_TOKEN should be a user token, not a bot token (remove 'Bot ' prefix)")
        
        # Check channel IDs
        if not self.channel_ids:
            errors.append("CHANNEL_IDS is required (at least one channel ID)")
        
        # Display errors if any
        if errors:
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{Fore.RED}❌ Configuration Error")
            print(f"{Fore.RED}{'='*60}")
            for error in errors:
                print(f"{Fore.YELLOW}  • {error}")
            print(f"\n{Fore.CYAN}💡 Please check your .env file")
            print(f"{Fore.CYAN}   Copy .env.example to .env and fill in the values")
            print(f"{Fore.RED}{'='*60}\n")
            sys.exit(1)
    
    def display_config(self):
        """Display loaded configuration (for debugging)"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}📋 Discord Stream Monitor Configuration")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}✓ Token: {self.discord_token[:20]}...{self.discord_token[-10:]}")
        print(f"{Fore.GREEN}✓ Monitoring {len(self.channel_ids)} channel(s):")
        for cid in self.channel_ids:
            print(f"{Fore.WHITE}  • {cid}")
        print(f"{Fore.GREEN}✓ Logs directory: {self.logs_dir}")
        print(f"{Fore.GREEN}✓ Downloads directory: {self.downloads_dir}")
        print(f"{Fore.GREEN}✓ Timezone: {self.timezone_offset}")
        print(f"{Fore.CYAN}{'='*60}\n")

# Global config instance
config = Config()
