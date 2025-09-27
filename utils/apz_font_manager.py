# font_manager.py
from PIL import ImageFont 
from .apz_url_file_utility import URLFileUtility
from .apz_emoji_support import create_emoji_support

class FontManager:
    def __init__(self, regular_font_path, italic_font_path, bold_font_path, max_font_size):
        self.max_font_size = max_font_size
        
        # Initialize URL file utility for handling URLs
        self.url_utility = URLFileUtility()
        
        # Convert paths/URLs to local paths
        try:
            self.regular_font_path = self.url_utility.get_local_path(regular_font_path)
        except Exception as e:
            print(f"Warning: Could not resolve regular font path '{regular_font_path}': {e}")
            self.regular_font_path = regular_font_path
            
        try:
            self.italic_font_path = self.url_utility.get_local_path(italic_font_path)
        except Exception as e:
            print(f"Warning: Could not resolve italic font path '{italic_font_path}': {e}")
            self.italic_font_path = italic_font_path
            
        try:
            self.bold_font_path = self.url_utility.get_local_path(bold_font_path)
        except Exception as e:
            print(f"Warning: Could not resolve bold font path '{bold_font_path}': {e}")
            self.bold_font_path = bold_font_path

        # Print statements to confirm paths
        print(f"Initialized FontManager with Regular Font: {self.regular_font_path}")
        print(f"Italic Font: {self.italic_font_path}")
        print(f"Bold Font: {self.bold_font_path}")

        # Dictionary to cache loaded fonts
        self.font_cache = {}
        
        # Initialize emoji support
        self.emoji_support = create_emoji_support()

        

    def load_font(self, font_path, font_size):
        # Load font from cache if available
        if (font_path, font_size) not in self.font_cache:
            print(f"Loading font from path: {font_path} with size: {font_size}")
            font = ImageFont.truetype(font_path, font_size)
            self.font_cache[(font_path, font_size)] = font
        return self.font_cache[(font_path, font_size)]
    

    def get_regular_font(self, font_size):
        return self.load_font(self.regular_font_path, font_size)

    def get_italic_font(self, font_size):
        return self.load_font(self.italic_font_path, font_size)

    def get_bold_font(self, font_size):
        return self.load_font(self.bold_font_path, font_size)

    def get_font_for_style(self, style, font_size, text=""):
        """
        Get the appropriate font for a given style and text.
        Now supports emoji font fallback.
        
        Args:
            style: Style dictionary
            font_size: Font size
            text: Text to render (for emoji detection)
            
        Returns:
            PIL ImageFont object
        """
        # First, get the base font based on style
        if style.get('b', False):
            base_font = self.get_bold_font(font_size)
        elif style.get('i', False):
            base_font = self.get_italic_font(font_size)
        else:
            base_font = self.get_regular_font(font_size)
        
        # Check if text contains emojis and get appropriate font
        if text and self.emoji_support.has_emoji(text):
            emoji_font = self.emoji_support.get_emoji_font(font_size)
            if emoji_font and self.emoji_support.test_emoji_support(emoji_font):
                return emoji_font
        
        return base_font
    
    def get_font_for_text(self, text, font_size):
        """
        Get the best font for rendering text (with emoji support).
        
        Args:
            text: Text to render
            font_size: Font size
            
        Returns:
            PIL ImageFont object
        """
        if self.emoji_support.has_emoji(text):
            emoji_font = self.emoji_support.get_emoji_font(font_size)
            if emoji_font and self.emoji_support.test_emoji_support(emoji_font):
                return emoji_font
        
        return self.get_regular_font(font_size)
