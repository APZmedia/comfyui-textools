# url_file_utility.py
import os
import tempfile
import urllib.request
import urllib.parse
import urllib.error
import logging
import hashlib
import time
from pathlib import Path
from typing import Optional, Union

class URLFileUtility:
    """
    Utility class for handling both local file paths and signed URLs.
    Downloads files from URLs to temporary directories and manages cleanup.
    """
    
    def __init__(self, temp_dir: Optional[str] = None, cache_duration: int = 3600):
        """
        Initialize the URL file utility.
        
        Args:
            temp_dir: Custom temporary directory path. If None, uses system temp.
            cache_duration: Cache duration in seconds (default: 1 hour)
        """
        self.logger = logging.getLogger(__name__)
        self.cache_duration = cache_duration
        
        # Set up temporary directory
        if temp_dir:
            self.temp_dir = Path(temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
        else:
            # Use ComfyUI temp directory if available, otherwise system temp
            comfyui_temp = os.path.join(os.path.expanduser("~"), ".comfyui", "temp")
            if os.path.exists(os.path.dirname(comfyui_temp)):
                self.temp_dir = Path(comfyui_temp)
                self.temp_dir.mkdir(parents=True, exist_ok=True)
            else:
                self.temp_dir = Path(tempfile.gettempdir()) / "comfyui_textools"
                self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Track downloaded files for cleanup
        self.downloaded_files = {}
        
        self.logger.info(f"URLFileUtility initialized with temp directory: {self.temp_dir}")
    
    def is_url(self, path: str) -> bool:
        """
        Check if the given path is a URL.
        
        Args:
            path: Path or URL to check
            
        Returns:
            True if path is a URL, False otherwise
        """
        if not path:
            return False
        
        parsed = urllib.parse.urlparse(path)
        return parsed.scheme in ('http', 'https')
    
    def get_file_hash(self, url: str) -> str:
        """
        Generate a hash for the URL to use as filename.
        
        Args:
            url: URL to hash
            
        Returns:
            MD5 hash of the URL
        """
        return hashlib.md5(url.encode('utf-8')).hexdigest()
    
    def get_file_extension(self, url: str, content_type: Optional[str] = None) -> str:
        """
        Determine file extension from URL or content type.
        
        Args:
            url: URL to analyze
            content_type: HTTP content type header
            
        Returns:
            File extension (including the dot)
        """
        # Try to get extension from URL path
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        
        if path and '.' in path:
            return os.path.splitext(path)[1]
        
        # Try to get extension from content type
        if content_type:
            content_type_map = {
                'font/ttf': '.ttf',
                'font/otf': '.otf',
                'font/woff': '.woff',
                'font/woff2': '.woff2',
                'application/font-ttf': '.ttf',
                'application/font-otf': '.otf',
                'application/x-font-ttf': '.ttf',
                'application/x-font-otf': '.otf',
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'image/gif': '.gif',
                'image/webp': '.webp',
                'text/plain': '.txt',
                'application/json': '.json'
            }
            
            for mime_type, ext in content_type_map.items():
                if mime_type in content_type.lower():
                    return ext
        
        # Default to no extension
        return ''
    
    def is_file_cached(self, url: str) -> Optional[str]:
        """
        Check if file is already cached and not expired.
        
        Args:
            url: URL to check
            
        Returns:
            Local file path if cached and valid, None otherwise
        """
        file_hash = self.get_file_hash(url)
        cache_marker = self.temp_dir / f"{file_hash}_cached"
        
        if cache_marker.exists():
            # Check if file is not expired
            file_age = time.time() - cache_marker.stat().st_mtime
            if file_age < self.cache_duration:
                # Look for the actual cached file (without extension first, then with common extensions)
                possible_files = [
                    self.temp_dir / file_hash,  # No extension
                    self.temp_dir / f"{file_hash}.ttf",
                    self.temp_dir / f"{file_hash}.otf",
                    self.temp_dir / f"{file_hash}.woff",
                    self.temp_dir / f"{file_hash}.woff2",
                ]
                
                for cached_file in possible_files:
                    if cached_file.exists():
                        self.logger.debug(f"Using cached file for URL: {url}")
                        return str(cached_file)
                
                # If cache marker exists but no actual file, remove the marker
                try:
                    cache_marker.unlink()
                    self.logger.debug(f"Removed orphaned cache marker: {cache_marker}")
                except OSError as e:
                    self.logger.warning(f"Could not remove orphaned cache marker: {e}")
            else:
                # Remove expired files
                try:
                    cache_marker.unlink()
                    # Also try to remove the actual cached file
                    for cached_file in [self.temp_dir / file_hash, 
                                      self.temp_dir / f"{file_hash}.ttf",
                                      self.temp_dir / f"{file_hash}.otf",
                                      self.temp_dir / f"{file_hash}.woff",
                                      self.temp_dir / f"{file_hash}.woff2"]:
                        if cached_file.exists():
                            cached_file.unlink()
                    self.logger.debug(f"Removed expired cached files for: {url}")
                except OSError as e:
                    self.logger.warning(f"Could not remove expired cached files: {e}")
        
        return None
    
    def download_file(self, url: str, timeout: int = 30) -> str:
        """
        Download file from URL to temporary directory.
        
        Args:
            url: URL to download
            timeout: Request timeout in seconds
            
        Returns:
            Local file path of downloaded file
            
        Raises:
            urllib.error.URLError: If download fails
            OSError: If file operations fail
        """
        # Check cache first
        cached_file = self.is_file_cached(url)
        if cached_file:
            return cached_file
        
        self.logger.info(f"Downloading file from URL: {url}")
        
        try:
            # Create request with proper headers
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'ComfyUI-TextTools/1.0',
                    'Accept': '*/*'
                }
            )
            
            # Download file
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content_type = response.headers.get('Content-Type', '')
                file_extension = self.get_file_extension(url, content_type)
                
                # Generate filename
                file_hash = self.get_file_hash(url)
                filename = f"{file_hash}{file_extension}"
                local_path = self.temp_dir / filename
                
                # Download and save file
                with open(local_path, 'wb') as f:
                    f.write(response.read())
                
                # Create cache marker
                cache_marker = self.temp_dir / f"{file_hash}_cached"
                cache_marker.touch()
                
                # Track downloaded file
                self.downloaded_files[str(local_path)] = {
                    'url': url,
                    'downloaded_at': time.time(),
                    'size': local_path.stat().st_size
                }
                
                self.logger.info(f"Successfully downloaded file to: {local_path}")
                return str(local_path)
                
        except urllib.error.HTTPError as e:
            error_msg = f"HTTP error {e.code} downloading {url}: {e.reason}"
            self.logger.error(error_msg)
            raise urllib.error.URLError(error_msg)
        except urllib.error.URLError as e:
            error_msg = f"URL error downloading {url}: {e.reason}"
            self.logger.error(error_msg)
            raise
        except OSError as e:
            error_msg = f"File system error downloading {url}: {e}"
            self.logger.error(error_msg)
            raise
        except Exception as e:
            error_msg = f"Unexpected error downloading {url}: {e}"
            self.logger.error(error_msg)
            raise urllib.error.URLError(error_msg)
    
    def get_local_path(self, path_or_url: str, timeout: int = 30) -> str:
        """
        Get local file path, downloading from URL if necessary.
        
        Args:
            path_or_url: Local file path or URL
            timeout: Request timeout for URL downloads
            
        Returns:
            Local file path
            
        Raises:
            FileNotFoundError: If local file doesn't exist
            urllib.error.URLError: If URL download fails
        """
        if not path_or_url:
            raise ValueError("Path or URL cannot be empty")
        
        # If it's a URL, download it
        if self.is_url(path_or_url):
            return self.download_file(path_or_url, timeout)
        
        # If it's a local path, verify it exists
        if os.path.exists(path_or_url):
            return path_or_url
        
        # Try relative to ComfyUI directory
        comfyui_path = os.path.join(os.path.expanduser("~"), ".comfyui", path_or_url)
        if os.path.exists(comfyui_path):
            return comfyui_path
        
        # Try relative to current working directory
        cwd_path = os.path.join(os.getcwd(), path_or_url)
        if os.path.exists(cwd_path):
            return cwd_path
        
        raise FileNotFoundError(f"File not found: {path_or_url}")
    
    def cleanup_old_files(self, max_age: int = 86400):
        """
        Clean up old downloaded files.
        
        Args:
            max_age: Maximum age of files in seconds (default: 24 hours)
        """
        current_time = time.time()
        cleaned_count = 0
        
        try:
            for file_path in self.temp_dir.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age:
                        try:
                            file_path.unlink()
                            cleaned_count += 1
                        except OSError as e:
                            self.logger.warning(f"Could not remove old file {file_path}: {e}")
            
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} old files")
                
        except OSError as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def get_download_stats(self) -> dict:
        """
        Get statistics about downloaded files.
        
        Returns:
            Dictionary with download statistics
        """
        total_size = sum(info['size'] for info in self.downloaded_files.values())
        return {
            'downloaded_files': len(self.downloaded_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'temp_directory': str(self.temp_dir)
        }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        # Note: This is not guaranteed to be called, but it's good practice
        try:
            self.cleanup_old_files()
        except:
            pass


# Convenience function for easy use
def get_local_file_path(path_or_url: str, temp_dir: Optional[str] = None, timeout: int = 30) -> str:
    """
    Convenience function to get local file path from path or URL.
    
    Args:
        path_or_url: Local file path or URL
        temp_dir: Custom temporary directory
        timeout: Request timeout for URL downloads
        
    Returns:
        Local file path
    """
    utility = URLFileUtility(temp_dir=temp_dir)
    return utility.get_local_path(path_or_url, timeout)

