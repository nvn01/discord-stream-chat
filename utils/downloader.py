"""
Image downloader for Discord attachments
Downloads images with MessageID_Filename naming convention
"""

import aiohttp
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from colorama import Fore, Style

class ImageDownloader:
    """Handles async downloading of Discord image attachments"""
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
    
    def __init__(self, downloads_dir: Path):
        self.downloads_dir = downloads_dir
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _is_image(self, filename: str) -> bool:
        """Check if file is an image based on extension"""
        ext = Path(filename).suffix.lower()
        return ext in self.SUPPORTED_FORMATS
    
    def _generate_filename(self, message_id: int, original_filename: str) -> str:
        """Generate filename in format: MessageID_OriginalFilename"""
        return f"{message_id}_{original_filename}"
    
    async def download_image(
        self,
        url: str,
        message_id: int,
        filename: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Download an image from URL
        
        Args:
            url: Direct URL to the image
            message_id: Discord message ID (for filename)
            filename: Original filename
            max_retries: Number of retry attempts
        
        Returns:
            Dictionary with download status and metadata
        """
        # Check if it's an image
        if not self._is_image(filename):
            return {
                'filename': filename,
                'url': url,
                'size': 0,
                'downloaded': False,
                'error': 'Not an image file'
            }
        
        # Generate destination filename
        dest_filename = self._generate_filename(message_id, filename)
        dest_path = self.downloads_dir / dest_filename
        
        # Try downloading with retries
        for attempt in range(max_retries):
            try:
                session = await self._get_session()
                
                async with session.get(url) as response:
                    if response.status == 200:
                        # Read content
                        content = await response.read()
                        
                        # Save to file
                        dest_path.write_bytes(content)
                        
                        file_size = len(content)
                        print(f"{Fore.GREEN}⬇️  Downloaded: {dest_filename} ({file_size:,} bytes)")
                        
                        return {
                            'filename': filename,
                            'url': url,
                            'size': file_size,
                            'downloaded': True,
                            'local_path': str(dest_path)
                        }
                    else:
                        print(f"{Fore.YELLOW}⚠️  HTTP {response.status} for {filename}")
                        
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"{Fore.YELLOW}⚠️  Retry {attempt + 1}/{max_retries} in {wait_time}s: {filename}")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"{Fore.RED}❌ Failed to download {filename}: {e}")
                    return {
                        'filename': filename,
                        'url': url,
                        'size': 0,
                        'downloaded': False,
                        'error': str(e)
                    }
        
        return {
            'filename': filename,
            'url': url,
            'size': 0,
            'downloaded': False,
            'error': 'Max retries exceeded'
        }
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

# Global downloader instance
_downloader_instance = None

def get_downloader(downloads_dir: Path) -> ImageDownloader:
    """Get or create the global downloader instance"""
    global _downloader_instance
    if _downloader_instance is None:
        _downloader_instance = ImageDownloader(downloads_dir)
    return _downloader_instance
