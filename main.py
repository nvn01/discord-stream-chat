"""
Discord Stream Monitor - Main Entry Point
Captures real-time messages and images from Discord channels
"""

import sys
import asyncio
import signal
from colorama import Fore, Style

from config import config
from monitor import create_monitor
from utils.alerts import alerts

async def main():
    """Main application entry point"""
    
    # Display configuration
    config.display_config()
    
    # Create Discord monitor
    monitor = create_monitor()
    
    # Handle graceful shutdown
    shutdown_event = asyncio.Event()
    
    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n{Fore.YELLOW}⏸️  Shutting down gracefully...")
        shutdown_event.set()
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start the monitor (this will run until interrupted)
        print(f"{Fore.CYAN}🔌 Connecting to Discord...")
        
        # Run the bot
        async def run_bot():
            try:
                await monitor.start(config.discord_token)
            except discord.errors.LoginFailure:
                alerts.alert_token_invalid()
                sys.exit(1)
            except Exception as e:
                print(f"{Fore.RED}❌ Fatal error: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
        
        # Run bot and wait for shutdown signal
        bot_task = asyncio.create_task(run_bot())
        shutdown_task = asyncio.create_task(shutdown_event.wait())
        
        # Wait for either bot to finish or shutdown signal
        done, pending = await asyncio.wait(
            [bot_task, shutdown_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel pending tasks
        for task in pending:
            task.cancel()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏸️  Interrupted by user")
    
    finally:
        # Clean shutdown
        await monitor.close()
        print(f"{Fore.GREEN}✓ Shutdown complete")
        print(f"{Fore.CYAN}{'='*60}\n")

if __name__ == '__main__':
    # Import discord here to catch import errors
    try:
        import discord
    except ImportError:
        print(f"{Fore.RED}❌ Error: discord.py-self is not installed")
        print(f"{Fore.CYAN}💡 Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the async main function
    asyncio.run(main())
