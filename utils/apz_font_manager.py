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
        
        # Log font initialization
        # FontManager initialization logging removed for performance
        
        # Validate and handle font paths
        if not regular_font_path or regular_font_path.strip() == "":
            self.regular_font_path = None  # Will use PIL default font
        elif regular_font_path.startswith(('http://', 'https://')):
            try:
                self.regular_font_path = self.url_utility.get_local_path(regular_font_path)
            except Exception as e:
                self.regular_font_path = None  # Will use PIL default font
        else:
            self.regular_font_path = self._resolve_font_path(regular_font_path)
            if not self.regular_font_path:
                self.regular_font_path = None  # Will use PIL default font
            
        if not italic_font_path or italic_font_path.strip() == "":
            self.italic_font_path = None  # Will use PIL default font
        elif italic_font_path.startswith(('http://', 'https://')):
            try:
                self.italic_font_path = self.url_utility.get_local_path(italic_font_path)
            except Exception as e:
                self.italic_font_path = None  # Will use PIL default font
        else:
            self.italic_font_path = self._resolve_font_path(italic_font_path)
            if not self.italic_font_path:
                self.italic_font_path = None  # Will use PIL default font
            
        if not bold_font_path or bold_font_path.strip() == "":
            self.bold_font_path = None  # Will use PIL default font
        elif bold_font_path.startswith(('http://', 'https://')):
            try:
                self.bold_font_path = self.url_utility.get_local_path(bold_font_path)
            except Exception as e:
                self.bold_font_path = None  # Will use PIL default font
        else:
            self.bold_font_path = self._resolve_font_path(bold_font_path)
            if not self.bold_font_path:
                self.bold_font_path = None  # Will use PIL default font

        # Dictionary to cache loaded fonts
        self.font_cache = {}
        
        # Initialize emoji support
        self.emoji_support = create_emoji_support()

    def _resolve_font_path(self, font_path):
        """
        Resolve font path to absolute path, handling relative paths from project root.
        Supports cross-platform paths for Windows, macOS, and Linux.
        """
        # If it's already an absolute path, check if it exists
        if os.path.isabs(font_path):
            if os.path.exists(font_path):
                return font_path
            else:
                return None
        
        # Get the project root directory (where this file is located)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Try multiple resolution strategies
        potential_paths = []
        
        # Strategy 1: Resolve relative to project root
        project_relative_path = os.path.join(project_root, font_path)
        project_relative_path = os.path.normpath(project_relative_path)
        potential_paths.append(project_relative_path)
        
        # Strategy 2: Try the path as-is (in case it's a system font path)
        potential_paths.append(font_path)
        
        # Strategy 3: Try common system font directories
        import platform
        system = platform.system()
        
        if system == "Windows":
            # Windows system font directories
            system_font_dirs = [
                "C:/Windows/Fonts/",
                "C:/Windows/System32/Fonts/",
                os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts/")
            ]
        elif system == "Darwin":  # macOS
            system_font_dirs = [
                "/System/Library/Fonts/",
                "/Library/Fonts/",
                os.path.expanduser("~/Library/Fonts/"),
                "/System/Library/Fonts/Supplemental/"
            ]
        else:  # Linux
            system_font_dirs = [
                "/usr/share/fonts/",
                "/usr/local/share/fonts/",
                os.path.expanduser("~/.fonts/"),
                os.path.expanduser("~/.local/share/fonts/"),
                "/usr/share/fonts/truetype/",
                "/usr/share/fonts/opentype/"
            ]
        
        # Add system font directory + font_path combinations
        for font_dir in system_font_dirs:
            if os.path.exists(font_dir):
                full_path = os.path.join(font_dir, font_path)
                potential_paths.append(full_path)
                
                # Also try with just the filename if font_path contains directories
                font_filename = os.path.basename(font_path)
                if font_filename != font_path:  # Only if there's a directory component
                    filename_path = os.path.join(font_dir, font_filename)
                    potential_paths.append(filename_path)
        
        # Check all potential paths
        for path in potential_paths:
            if os.path.exists(path):
                return path
        
        return None

    def load_font(self, font_path, font_size):
        # Log font loading attempt
        # Font loading logging removed for performance
        
        # Load font from cache if available
        if (font_path, font_size) not in self.font_cache:
            # Handle None font path (use PIL default font)
            if font_path is None:
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
                            # Fallback font logging removed for performance
                            self.font_cache[(font_path, font_size)] = font
                            return font
                    
                    # If no fallback font found, use default (but it won't scale properly)
                    font = ImageFont.load_default()
                    # Debug logging removed for performance
                    self.font_cache[(font_path, font_size)] = font
                    return font
                except Exception as e:
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            
            # Check if font_path is a URL that needs to be resolved
            actual_font_path = font_path
            if font_path.startswith(('http://', 'https://')):
                try:
                    actual_font_path = self.url_utility.get_local_path(font_path)
                except Exception as e:
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            else:
                # Resolve the font path (handles relative paths)
                actual_font_path = self._resolve_font_path(font_path)
                if actual_font_path is None:
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            
            # Check if the resolved path exists
            if not os.path.exists(actual_font_path):
                font = ImageFont.load_default()
                self.font_cache[(font_path, font_size)] = font
                return font
            
            # Try to load the font
            try:
                font = ImageFont.truetype(actual_font_path, font_size)
                # Font loading success logging removed for performance
                self.font_cache[(font_path, font_size)] = font
                return font
            except Exception as e:
                # Debug logging removed for performance
                font = ImageFont.load_default()
                # Debug logging removed for performance
                self.font_cache[(font_path, font_size)] = font
                return font
        
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
        # Log style selection
        style_type = "bold" if style.get('b', False) else "italic" if style.get('i', False) else "regular"
        # Font retrieval logging removed for performance
        
        # First, get the base font based on style
        if style.get('b', False):
            base_font = self.get_bold_font(font_size)
        elif style.get('i', False):
            base_font = self.get_italic_font(font_size)
        else:
            base_font = self.get_regular_font(font_size)
        
        # Use emoji fonts for emoji text (this is how emojis work in real life)
        if text and self.emoji_support.has_emoji(text):
            # Emoji detection logging removed for performance
            emoji_font = self.emoji_support.get_emoji_font(font_size)
            if emoji_font and self.emoji_support.test_emoji_support(emoji_font):
                # Emoji font usage logging removed for performance
                return emoji_font
            else:
                # Emoji font fallback logging removed for performance
                pass
        
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
