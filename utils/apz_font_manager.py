# font_manager.py
import os
from PIL import ImageFont 
from .apz_url_file_utility import URLFileUtility
from .apz_emoji_support import create_emoji_support

class FontManager:
    def __init__(self, regular_font_path, italic_font_path, bold_font_path, max_font_size):
        self.max_font_size = max_font_size
        
        # Initialize URL file utility for handling URLs
        self.url_utility = URLFileUtility()
        
        # Validate and handle font paths
        if not regular_font_path or regular_font_path.strip() == "":
            print("Warning: Regular font path is empty, using default system font")
            self.regular_font_path = None  # Will use PIL default font
        elif regular_font_path.startswith(('http://', 'https://')):
            try:
                self.regular_font_path = self.url_utility.get_local_path(regular_font_path)
            except Exception as e:
                print(f"Warning: Could not resolve regular font URL '{regular_font_path}': {e}")
                self.regular_font_path = None  # Will use PIL default font
        else:
            self.regular_font_path = self._resolve_font_path(regular_font_path)
            
        if not italic_font_path or italic_font_path.strip() == "":
            print("Warning: Italic font path is empty, using default system font")
            self.italic_font_path = None  # Will use PIL default font
        elif italic_font_path.startswith(('http://', 'https://')):
            try:
                self.italic_font_path = self.url_utility.get_local_path(italic_font_path)
            except Exception as e:
                print(f"Warning: Could not resolve italic font URL '{italic_font_path}': {e}")
                self.italic_font_path = None  # Will use PIL default font
        else:
            self.italic_font_path = self._resolve_font_path(italic_font_path)
            
        if not bold_font_path or bold_font_path.strip() == "":
            print("Warning: Bold font path is empty, using default system font")
            self.bold_font_path = None  # Will use PIL default font
        elif bold_font_path.startswith(('http://', 'https://')):
            try:
                self.bold_font_path = self.url_utility.get_local_path(bold_font_path)
            except Exception as e:
                print(f"Warning: Could not resolve bold font URL '{bold_font_path}': {e}")
                self.bold_font_path = None  # Will use PIL default font
        else:
            self.bold_font_path = self._resolve_font_path(bold_font_path)

        # Print statements to confirm paths
        print(f"Initialized FontManager with Regular Font: {self.regular_font_path}")
        print(f"Italic Font: {self.italic_font_path}")
        print(f"Bold Font: {self.bold_font_path}")

        # Dictionary to cache loaded fonts
        self.font_cache = {}
        
        # Initialize emoji support
        self.emoji_support = create_emoji_support()

    def _resolve_font_path(self, font_path):
        """
        Resolve font path to absolute path, handling relative paths from project root.
        Only resolves paths that start with 'fonts/' to use bundled fonts.
        """
        # If it's already an absolute path, return as is
        if os.path.isabs(font_path):
            return font_path
        
        # Only resolve relative paths that start with 'fonts/' (bundled fonts)
        if font_path.startswith('fonts/'):
            # Get the project root directory (where this file is located)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Resolve relative path from project root
            resolved_path = os.path.join(project_root, font_path)
            resolved_path = os.path.normpath(resolved_path)
            
            # Check if the resolved path exists
            if os.path.exists(resolved_path):
                return resolved_path
            else:
                print(f"Warning: Bundled font file not found at resolved path: {resolved_path}")
                return None
        else:
            # For other relative paths, return as-is (let the system handle them)
            return font_path

    def load_font(self, font_path, font_size):
        # Load font from cache if available
        if (font_path, font_size) not in self.font_cache:
            print(f"Loading font from path: {font_path} with size: {font_size}")
            
            # Handle None font path (use PIL default font)
            if font_path is None:
                print("Using PIL default font")
                # PIL default font doesn't scale, so we need to use a scalable fallback
                try:
                    # Try to use a system font that supports scaling
                    import platform
                    system = platform.system()
                    if system == "Windows":
                        fallback_fonts = [
                            "C:/Windows/Fonts/arial.ttf",
                            "C:/Windows/Fonts/calibri.ttf",
                            "C:/Windows/Fonts/tahoma.ttf"
                        ]
                    elif system == "Darwin":  # macOS
                        fallback_fonts = [
                            "/System/Library/Fonts/Arial.ttf",
                            "/System/Library/Fonts/Helvetica.ttc"
                        ]
                    else:  # Linux
                        fallback_fonts = [
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
                        ]
                    
                    for fallback_font in fallback_fonts:
                        if os.path.exists(fallback_font):
                            font = ImageFont.truetype(fallback_font, font_size)
                            self.font_cache[(font_path, font_size)] = font
                            print(f"Using fallback font: {fallback_font}")
                            return font
                    
                    # If no fallback font found, use default (but it won't scale properly)
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
                except Exception as e:
                    print(f"Warning: Could not load fallback font: {e}")
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            
            # Check if font_path is a URL that needs to be resolved
            actual_font_path = font_path
            if font_path.startswith(('http://', 'https://')):
                try:
                    actual_font_path = self.url_utility.get_local_path(font_path)
                    print(f"Resolved URL to local path: {actual_font_path}")
                except Exception as e:
                    print(f"Warning: Could not resolve font URL '{font_path}': {e}")
                    # Fall back to default font
                    print("Falling back to PIL default font")
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            
            # Check if the resolved path exists
            if not os.path.exists(actual_font_path):
                print(f"Warning: Font file does not exist: {actual_font_path}")
                print("Falling back to PIL default font")
                font = ImageFont.load_default()
                self.font_cache[(font_path, font_size)] = font
                return font
            
            try:
                font = ImageFont.truetype(actual_font_path, font_size)
                self.font_cache[(font_path, font_size)] = font
            except Exception as e:
                print(f"Warning: Could not load font from '{actual_font_path}': {e}")
                print("Falling back to PIL default font")
                font = ImageFont.load_default()
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
        
        # Skip font-based emoji rendering when using PNG system
        # The PNG system handles emoji rendering separately
        # if text and self.emoji_support.has_emoji(text):
        #     emoji_font = self.emoji_support.get_emoji_font(font_size)
        #     if emoji_font and self.emoji_support.test_emoji_support(emoji_font):
        #         return emoji_font
        
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
    
    def should_use_embedded_color(self, font):
        """
        Determine whether the provided font should be rendered using embedded color glyphs.
        """
        return self.emoji_support.should_use_embedded_color(font)
    
    def is_color_font(self, font):
        """
        Check if the provided font was identified as a color emoji font.
        """
        return self.emoji_support.is_color_font(font)
