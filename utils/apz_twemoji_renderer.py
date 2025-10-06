#!/usr/bin/env python3
"""
Twemoji-based emoji renderer for serverless environments.
Downloads and caches emoji SVGs/PNGs from Twitter's Twemoji CDN.
"""

import os
import re
import requests
from PIL import Image, ImageDraw
import io
import hashlib

class TwemojiRenderer:
    """
    Renders emojis using Twitter's Twemoji library.
    Downloads and caches emoji assets from CDN for serverless compatibility.
    """
    
    def __init__(self, emoji_dir="fonts/emoji/twemoji", use_svg=False):
        self.emoji_dir = emoji_dir
        self.use_svg = use_svg
        self.emoji_cache = {}
        self.session = requests.Session()
        
        # Create emoji directory
        os.makedirs(self.emoji_dir, exist_ok=True)
        
        # Twemoji CDN base URL
        self.cdn_base = "https://twemoji.maxcdn.com/v/latest"
        
        # Emoji pattern for detection
        self.emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]'  # Emoticons
            r'|[\U0001F300-\U0001F5FF]'  # Misc Symbols and Pictographs
            r'|[\U0001F680-\U0001F6FF]'  # Transport and Map
            r'|[\U0001F1E0-\U0001F1FF]'  # Regional indicator symbols
            r'|[\U0001F900-\U0001F9FF]'  # Supplemental Symbols and Pictographs
            r'|[\U00002600-\U000026FF]'  # Miscellaneous symbols
            r'|[\U00002700-\U000027BF]'  # Dingbats
            r'|[\U00002744]'  # Snowflake ❄
            r'|[\U0001F338]'  # Cherry blossom 🌸
        )
    
    def has_emoji(self, text):
        """Check if text contains emojis."""
        return bool(self.emoji_pattern.search(text))
    
    def get_emoji_unicode(self, emoji_char):
        """Get Unicode codepoint for emoji character."""
        if len(emoji_char) > 1:
            emoji_char = emoji_char[0]
        
        try:
            return f"{ord(emoji_char):x}"
        except TypeError:
            return None
    
    def get_emoji_url(self, emoji_char, size=72):
        """Get Twemoji CDN URL for emoji."""
        unicode_codepoint = self.get_emoji_unicode(emoji_char)
        if not unicode_codepoint:
            return None
        
        if self.use_svg:
            return f"{self.cdn_base}/svg/{unicode_codepoint}.svg"
        else:
            # Twemoji uses format: {size}x{size}/{unicode}.png
            return f"{self.cdn_base}/{size}x{size}/{unicode_codepoint}.png"
    
    def get_emoji_path(self, emoji_char, size=72):
        """Get local file path for emoji."""
        unicode_codepoint = self.get_emoji_unicode(emoji_char)
        if not unicode_codepoint:
            return None
        
        if self.use_svg:
            return os.path.join(self.emoji_dir, f"{unicode_codepoint}.svg")
        else:
            return os.path.join(self.emoji_dir, f"{unicode_codepoint}_{size}.png")
    
    def download_emoji(self, emoji_char, size=72):
        """Download emoji from Twemoji CDN."""
        url = self.get_emoji_url(emoji_char, size)
        if not url:
            return None
        
        try:
            # Debug logging removed for performance
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            # Debug logging removed for performance
            return None
    
    def load_emoji(self, emoji_char, size=72):
        """Load emoji image, downloading if necessary."""
        cache_key = (emoji_char, size)
        if cache_key in self.emoji_cache:
            return self.emoji_cache[cache_key]
        
        # Check if local file exists
        local_path = self.get_emoji_path(emoji_char, size)
        if local_path and os.path.exists(local_path):
            try:
                if self.use_svg:
                    # For SVG, we need to convert to PNG
                    img = self._svg_to_png(local_path, size)
                else:
                    img = Image.open(local_path)
                    
                    # Convert palette mode to RGBA for better compatibility
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                
                if img:
                    self.emoji_cache[cache_key] = img
                    return img
            except Exception as e:
                # Debug logging removed for performance
                pass
        
        # Download from CDN
        emoji_data = self.download_emoji(emoji_char, size)
        if emoji_data:
            try:
                if self.use_svg:
                    # Save SVG and convert to PNG
                    with open(local_path, 'wb') as f:
                        f.write(emoji_data)
                    img = self._svg_to_png(local_path, size)
                else:
                    # Save PNG directly
                    with open(local_path, 'wb') as f:
                        f.write(emoji_data)
                    img = Image.open(io.BytesIO(emoji_data))
                    
                    # Convert palette mode to RGBA for better compatibility
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                
                if img:
                    self.emoji_cache[cache_key] = img
                    return img
            except Exception as e:
                # Debug logging removed for performance
                pass
        
        return None
    
    def _svg_to_png(self, svg_path, size):
        """Convert SVG to PNG using PIL (basic implementation)."""
        try:
            # For SVG support, we'd need cairosvg or similar
            # For now, we'll use PNG mode which is more reliable
            # Debug logging removed for performance
            return None
        except Exception as e:
            # Debug logging removed for performance
            return None
    
    def render_emoji(self, emoji_char, size=72):
        """Render emoji at specified size."""
        img = self.load_emoji(emoji_char, size)
        if img and img.size != (size, size):
            # Use better scaling algorithm based on whether we're upscaling or downscaling
            original_size = max(img.size)
            if size > original_size:
                # Upscaling - use BICUBIC for smooth scaling
                img = img.resize((size, size), Image.Resampling.BICUBIC)
            else:
                # Downscaling - use LANCZOS for better quality
                img = img.resize((size, size), Image.Resampling.LANCZOS)
        return img
    
    def split_text_by_emoji(self, text):
        """Split text into emoji and non-emoji parts."""
        parts = []
        current_pos = 0
        
        for match in self.emoji_pattern.finditer(text):
            start, end = match.span()
            
            # Add non-emoji text before this emoji
            if start > current_pos:
                parts.append((text[current_pos:start], False))
            
            # Add emoji
            parts.append((match.group(), True))
            current_pos = end
        
        # Add remaining non-emoji text
        if current_pos < len(text):
            parts.append((text[current_pos:], False))
        
        return parts

def test_twemoji():
    """Test the Twemoji renderer."""
    renderer = TwemojiRenderer()
    
    # Test emoji detection
    text = "Hello ❄️🌸 World!"
    # Debug logging removed for performance
    # Debug logging removed for performance
    
    # Test splitting
    parts = renderer.split_text_by_emoji(text)
    # Debug logging removed for performance
    
    # Test individual emoji loading
    for emoji_part, is_emoji in parts:
        if is_emoji:
            # Debug logging removed for performance
            img = renderer.load_emoji(emoji_part, 72)
            if img:
                # Debug logging removed for performance
                pass
            else:
                # Debug logging removed for performance
                pass

if __name__ == "__main__":
    test_twemoji()
