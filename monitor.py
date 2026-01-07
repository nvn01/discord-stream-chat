"""
Core Discord monitoring logic
Event-driven message capture and image downloading
"""

import discord
from datetime import datetime
from typing import List
from colorama import Fore

from config import config
from utils.logger import get_logger
from utils.downloader import get_downloader
from utils.alerts import alerts

class DiscordMonitor(discord.Client):
    """Discord client for monitoring channels"""
    
    def __init__(self):
        # Initialize Discord client (discord.py-self doesn't use intents)
        super().__init__()
        
        # Initialize utilities
        self.logger = get_logger(config.logs_dir, config.timezone_offset)
        self.downloader = get_downloader(config.downloads_dir)
        self.monitored_channels = set(config.channel_ids)
    
    async def on_ready(self):
        """Called when the bot successfully connects to Discord"""
        print(f"{Fore.GREEN}✓ Logged in as {Fore.WHITE}{self.user}")
        print(f"{Fore.GREEN}✓ User ID: {Fore.WHITE}{self.user.id}")
        
        # Display monitored channels
        print(f"\n{Fore.CYAN}📡 Monitoring {len(self.monitored_channels)} channel(s):")
        for channel_id in self.monitored_channels:
            channel = self.get_channel(channel_id)
            if channel:
                guild_name = channel.guild.name if hasattr(channel, 'guild') else 'DM'
                print(f"{Fore.WHITE}  • #{channel.name} {Fore.CYAN}(in {guild_name})")
            else:
                print(f"{Fore.YELLOW}  ⚠️  Channel {channel_id} not found (might need access)")
        
        alerts.info_startup()
    
    async def on_message(self, message: discord.Message):
        """
        Called when a message is received
        This is event-driven - only fires when a message arrives
        """
        # Ignore messages from self
        if message.author == self.user:
            return
        
        # Only process messages from monitored channels
        if message.channel.id not in self.monitored_channels:
            return
        
        # Get channel name
        channel_name = message.channel.name if hasattr(message.channel, 'name') else 'DM'
        
        # Process attachments (images)
        attachment_data = []
        if message.attachments:
            for attachment in message.attachments:
                # Download the image
                download_result = await self.downloader.download_image(
                    url=attachment.url,
                    message_id=message.id,
                    filename=attachment.filename
                )
                attachment_data.append(download_result)
        
        # Format message data for logging
        message_data = self.logger.format_message(
            message_id=message.id,
            timestamp=message.created_at.isoformat(),
            author_name=str(message.author),
            author_id=message.author.id,
            channel_id=message.channel.id,
            channel_name=channel_name,
            content=message.content,
            attachments=attachment_data
        )
        
        # Log to JSON file
        await self.logger.log_message(message_data)
        
        # Console output
        content_preview = message.content if message.content else "[No text]"
        if message.attachments:
            content_preview += f" [{len(message.attachments)} attachment(s)]"
        
        alerts.info_message_received(
            author=str(message.author),
            channel=channel_name,
            content_preview=content_preview
        )
    
    async def on_disconnect(self):
        """Called when the bot disconnects from Discord"""
        print(f"{Fore.YELLOW}⚠️  Disconnected from Discord")
    
    async def on_error(self, event, *args, **kwargs):
        """Called when an error occurs"""
        import traceback
        print(f"{Fore.RED}❌ Error in {event}:")
        traceback.print_exc()
    
    async def close(self):
        """Clean shutdown"""
        await self.downloader.close()
        await super().close()

def create_monitor() -> DiscordMonitor:
    """Factory function to create a Discord monitor instance"""
    return DiscordMonitor()
