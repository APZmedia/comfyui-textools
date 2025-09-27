# emoji_support.py
import re
import os
import platform
from PIL import ImageFont

class EmojiSupport:
    """
    Enhanced emoji support with font fallback system.
    """
    
    def __init__(self, custom_emoji_font_url=None):
        self.custom_emoji_font_url = custom_emoji_font_url
        self.emoji_fonts = self._get_emoji_font_paths()
        self.emoji_font_cache = {}
        self.unicode_emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]'  # Emoticons
            r'|[\U0001F300-\U0001F5FF]'  # Misc Symbols and Pictographs
            r'|[\U0001F680-\U0001F6FF]'  # Transport and Map
            r'|[\U0001F1E0-\U0001F1FF]'  # Regional indicator symbols
            r'|[\U0001F900-\U0001F9FF]'  # Supplemental Symbols and Pictographs
            r'|[\U00002600-\U000026FF]'  # Miscellaneous symbols
            r'|[\U00002700-\U000027BF]'  # Dingbats
        )
    
    def _get_emoji_font_paths(self):
        """
        Get emoji font paths, prioritizing custom URL fonts, then bundled fonts.
        
        Returns:
            List of potential emoji font paths
        """
        # Get the directory of this script to find bundled fonts
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        bundled_fonts_dir = os.path.join(project_root, "fonts", "emoji")
        
        # Start with custom URL font if provided
        custom_fonts = []
        if self.custom_emoji_font_url:
            try:
                from .apz_url_file_utility import URLFileUtility
                url_utility = URLFileUtility()
                custom_font_path = url_utility.get_local_path(self.custom_emoji_font_url)
                custom_fonts.append(custom_font_path)
                print(f"Using custom emoji font from URL: {self.custom_emoji_font_url}")
            except Exception as e:
                print(f"Warning: Could not load custom emoji font from URL '{self.custom_emoji_font_url}': {e}")
        
        # Prioritize bundled fonts
        bundled_fonts = [
            os.path.join(bundled_fonts_dir, "NotoColorEmoji.ttf"),
            os.path.join(bundled_fonts_dir, "NotoColorEmoji-Regular.ttf"),  # Alternative filename
            os.path.join(bundled_fonts_dir, "Twemoji.woff2"),
        ]
        
        # System-specific emoji fonts as fallback
        system = platform.system()
        system_fonts = []
        
        if system == "Windows":
            system_fonts = [
                "C:/Windows/Fonts/seguiemj.ttf",  # Segoe UI Emoji
                "C:/Windows/Fonts/segmdl2.ttf",    # Segoe MDL2 Assets
                "C:/Windows/Fonts/NotoColorEmoji.ttf",
            ]
        elif system == "Darwin":  # macOS
            system_fonts = [
                "/System/Library/Fonts/Apple Color Emoji.ttc",
                "/System/Library/Fonts/Supplemental/Apple Symbols.ttf",
                "/Library/Fonts/NotoColorEmoji.ttf",
            ]
        else:  # Linux
            system_fonts = [
                "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
                "/usr/share/fonts/truetype/noto/NotoEmoji-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Fallback
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
        
        # Combine custom, bundled, and system fonts
        all_fonts = custom_fonts + bundled_fonts + system_fonts
        
        # Filter to existing fonts
        existing_fonts = []
        for font_path in all_fonts:
            if os.path.exists(font_path):
                existing_fonts.append(font_path)
        
        return existing_fonts
    
    def has_emoji(self, text):
        """
        Check if text contains emoji characters.
        
        Args:
            text: Input text
            
        Returns:
            Boolean indicating if emojis are present
        """
        return bool(self.unicode_emoji_pattern.search(text))
    
    def extract_emojis(self, text):
        """
        Extract all emoji characters from text.
        
        Args:
            text: Input text
            
        Returns:
            List of emoji characters found
        """
        return self.unicode_emoji_pattern.findall(text)
    
    def get_emoji_font(self, font_size):
        """
        Get the best available emoji font for the given size.
        
        Args:
            font_size: Font size to use
            
        Returns:
            PIL ImageFont object or None if no emoji font available
        """
        if (font_size, 'emoji') in self.emoji_font_cache:
            return self.emoji_font_cache[(font_size, 'emoji')]
        
        for font_path in self.emoji_fonts:
            try:
                font = ImageFont.truetype(font_path, font_size)
                self.emoji_font_cache[(font_size, 'emoji')] = font
                print(f"Loaded emoji font: {font_path} at size {font_size}")
                return font
            except (OSError, IOError):
                continue
        
        # Fallback to default font
        try:
            font = ImageFont.load_default()
            self.emoji_font_cache[(font_size, 'emoji')] = font
            print(f"Using default font for emojis at size {font_size}")
            return font
        except:
            return None
    
    def test_emoji_support(self, font, test_emoji="😀"):
        """
        Test if a font supports emoji characters.
        
        Args:
            font: PIL ImageFont object
            test_emoji: Emoji character to test
            
        Returns:
            Boolean indicating if emoji is supported
        """
        try:
            bbox = font.getbbox(test_emoji)
            # If bbox is valid and has reasonable dimensions, emoji is supported
            # Also check if the bbox has non-zero dimensions
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            return width > 0 and height > 0
        except Exception as e:
            print(f"Emoji test error: {e}")
            return False
    
    def get_font_for_text(self, text, regular_font, font_size):
        """
        Get the appropriate font for rendering text (regular or emoji).
        
        Args:
            text: Text to render
            regular_font: Regular font for non-emoji text
            font_size: Font size
            
        Returns:
            PIL ImageFont object
        """
        if self.has_emoji(text):
            emoji_font = self.get_emoji_font(font_size)
            if emoji_font and self.test_emoji_support(emoji_font):
                return emoji_font
        
        return regular_font
    
    def split_text_by_emoji(self, text):
        """
        Split text into emoji and non-emoji parts.
        
        Args:
            text: Input text
            
        Returns:
            List of (text_part, is_emoji) tuples
        """
        parts = []
        current_pos = 0
        
        for match in self.unicode_emoji_pattern.finditer(text):
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

def create_emoji_support(custom_emoji_font_url=None):
    """
    Create and return an EmojiSupport instance.
    
    Args:
        custom_emoji_font_url: Optional URL to custom emoji font
        
    Returns:
        EmojiSupport instance
    """
    return EmojiSupport(custom_emoji_font_url)
