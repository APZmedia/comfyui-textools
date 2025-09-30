# font_manager.py
import os
from PIL import ImageFont 
from .apz_url_file_utility import URLFileUtility
from .apz_emoji_support import create_emoji_support

class FontManager:
    def __init__(self, regular_font_path, italic_font_path, bold_font_path, max_font_size):
        print("=" * 60)
        print("FONT MANAGER INITIALIZATION")
        print("=" * 60)
        print(f"Input paths received:")
        print(f"  Regular: '{regular_font_path}'")
        print(f"  Italic:  '{italic_font_path}'")
        print(f"  Bold:    '{bold_font_path}'")
        print(f"  Max size: {max_font_size}")
        
        self.max_font_size = max_font_size
        
        # Initialize URL file utility for handling URLs
        self.url_utility = URLFileUtility()
        
        # Validate and handle font paths
        print("\nProcessing Regular Font Path:")
        if not regular_font_path or regular_font_path.strip() == "":
            print("  → Empty path detected, will use default system font")
            self.regular_font_path = None  # Will use PIL default font
        elif regular_font_path.startswith(('http://', 'https://')):
            print(f"  → URL detected: {regular_font_path}")
            try:
                self.regular_font_path = self.url_utility.get_local_path(regular_font_path)
                print(f"  → URL resolved to: {self.regular_font_path}")
            except Exception as e:
                print(f"  → URL resolution failed: {e}")
                print("  → Will use default system font")
                self.regular_font_path = None  # Will use PIL default font
        else:
            print(f"  → Local path detected, resolving...")
            self.regular_font_path = self._resolve_font_path(regular_font_path)
            if self.regular_font_path:
                print(f"  → Resolved to: {self.regular_font_path}")
            else:
                print("  → Resolution failed, will use default system font")
            
        print("\nProcessing Italic Font Path:")
        if not italic_font_path or italic_font_path.strip() == "":
            print("  → Empty path detected, will use default system font")
            self.italic_font_path = None  # Will use PIL default font
        elif italic_font_path.startswith(('http://', 'https://')):
            print(f"  → URL detected: {italic_font_path}")
            try:
                self.italic_font_path = self.url_utility.get_local_path(italic_font_path)
                print(f"  → URL resolved to: {self.italic_font_path}")
            except Exception as e:
                print(f"  → URL resolution failed: {e}")
                print("  → Will use default system font")
                self.italic_font_path = None  # Will use PIL default font
        else:
            print(f"  → Local path detected, resolving...")
            self.italic_font_path = self._resolve_font_path(italic_font_path)
            if self.italic_font_path:
                print(f"  → Resolved to: {self.italic_font_path}")
            else:
                print("  → Resolution failed, will use default system font")
            
        print("\nProcessing Bold Font Path:")
        if not bold_font_path or bold_font_path.strip() == "":
            print("  → Empty path detected, will use default system font")
            self.bold_font_path = None  # Will use PIL default font
        elif bold_font_path.startswith(('http://', 'https://')):
            print(f"  → URL detected: {bold_font_path}")
            try:
                self.bold_font_path = self.url_utility.get_local_path(bold_font_path)
                print(f"  → URL resolved to: {self.bold_font_path}")
            except Exception as e:
                print(f"  → URL resolution failed: {e}")
                print("  → Will use default system font")
                self.bold_font_path = None  # Will use PIL default font
        else:
            print(f"  → Local path detected, resolving...")
            self.bold_font_path = self._resolve_font_path(bold_font_path)
            if self.bold_font_path:
                print(f"  → Resolved to: {self.bold_font_path}")
            else:
                print("  → Resolution failed, will use default system font")

        # Print final resolved paths
        print("\n" + "=" * 60)
        print("FINAL FONT PATHS")
        print("=" * 60)
        print(f"Regular Font: {self.regular_font_path}")
        print(f"Italic Font:  {self.italic_font_path}")
        print(f"Bold Font:    {self.bold_font_path}")
        print("=" * 60)

        # Dictionary to cache loaded fonts
        self.font_cache = {}
        
        # Initialize emoji support
        self.emoji_support = create_emoji_support()

    def _resolve_font_path(self, font_path):
        """
        Resolve font path to absolute path, handling relative paths from project root.
        Supports cross-platform paths for Windows, macOS, and Linux.
        """
        print(f"    Resolving font path: '{font_path}'")
        
        # If it's already an absolute path, check if it exists
        if os.path.isabs(font_path):
            print(f"    → Absolute path detected")
            if os.path.exists(font_path):
                print(f"    → Path exists: {font_path}")
                return font_path
            else:
                print(f"    → Path does not exist: {font_path}")
                return None
        
        print(f"    → Relative path detected, trying multiple strategies...")
        
        # Get the project root directory (where this file is located)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"    → Project root: {project_root}")
        
        # Try multiple resolution strategies
        potential_paths = []
        
        # Strategy 1: Resolve relative to project root
        project_relative_path = os.path.join(project_root, font_path)
        project_relative_path = os.path.normpath(project_relative_path)
        potential_paths.append(project_relative_path)
        print(f"    → Strategy 1 - Project relative: {project_relative_path}")
        
        # Strategy 2: Try the path as-is (in case it's a system font path)
        potential_paths.append(font_path)
        print(f"    → Strategy 2 - As-is: {font_path}")
        
        # Strategy 3: Try common system font directories
        import platform
        system = platform.system()
        print(f"    → Detected system: {system}")
        
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
        
        print(f"    → Strategy 3 - System font directories:")
        # Add system font directory + font_path combinations
        for i, font_dir in enumerate(system_font_dirs):
            if os.path.exists(font_dir):
                full_path = os.path.join(font_dir, font_path)
                potential_paths.append(full_path)
                print(f"      {i+1}. {full_path}")
                
                # Also try with just the filename if font_path contains directories
                font_filename = os.path.basename(font_path)
                if font_filename != font_path:  # Only if there's a directory component
                    filename_path = os.path.join(font_dir, font_filename)
                    potential_paths.append(filename_path)
                    print(f"      {i+1}b. {filename_path} (filename only)")
            else:
                print(f"      {i+1}. {font_dir} (directory not found)")
        
        print(f"    → Total paths to check: {len(potential_paths)}")
        
        # Check all potential paths
        for i, path in enumerate(potential_paths, 1):
            print(f"    → Checking path {i}/{len(potential_paths)}: {path}")
            if os.path.exists(path):
                print(f"    → ✅ FOUND: {path}")
                return path
            else:
                print(f"    → ❌ Not found: {path}")
        
        # If no path found, print helpful debug information
        print(f"    → ❌ No valid path found for '{font_path}'")
        print(f"    → Searched {len(potential_paths)} potential paths")
        
        return None

    def load_font(self, font_path, font_size):
        print(f"\n--- LOADING FONT ---")
        print(f"Requested: '{font_path}' at size {font_size}")
        
        # Load font from cache if available
        if (font_path, font_size) not in self.font_cache:
            print(f"Font not in cache, loading...")
            
            # Handle None font path (use PIL default font)
            if font_path is None:
                print("→ None font path detected, using fallback system fonts")
                # PIL default font doesn't scale, so we need to use a scalable fallback
                try:
                    # Try to use a system font that supports scaling
                    import platform
                    system = platform.system()
                    print(f"→ Detected system: {system}")
                    
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
                    
                    print(f"→ Trying {len(fallback_fonts)} fallback fonts...")
                    for i, fallback_font in enumerate(fallback_fonts, 1):
                        print(f"  {i}. Checking: {fallback_font}")
                        if os.path.exists(fallback_font):
                            print(f"  → ✅ Found fallback: {fallback_font}")
                            font = ImageFont.truetype(fallback_font, font_size)
                            self.font_cache[(font_path, font_size)] = font
                            print(f"  → Font loaded successfully")
                            return font
                        else:
                            print(f"  → ❌ Not found: {fallback_font}")
                    
                    # If no fallback font found, use default (but it won't scale properly)
                    print("→ No fallback fonts found, using PIL default")
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
                except Exception as e:
                    print(f"→ Error loading fallback fonts: {e}")
                    print("→ Using PIL default font")
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            
            # Check if font_path is a URL that needs to be resolved
            actual_font_path = font_path
            if font_path.startswith(('http://', 'https://')):
                print(f"→ URL detected: {font_path}")
                try:
                    actual_font_path = self.url_utility.get_local_path(font_path)
                    print(f"→ URL resolved to: {actual_font_path}")
                except Exception as e:
                    print(f"→ URL resolution failed: {e}")
                    print("→ Falling back to PIL default font")
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
            else:
                print(f"→ Local path detected, resolving...")
                # Resolve the font path (handles relative paths)
                actual_font_path = self._resolve_font_path(font_path)
                if actual_font_path is None:
                    print(f"→ Path resolution failed for: '{font_path}'")
                    print("→ Falling back to PIL default font")
                    font = ImageFont.load_default()
                    self.font_cache[(font_path, font_size)] = font
                    return font
                else:
                    print(f"→ Path resolved to: {actual_font_path}")
            
            # Check if the resolved path exists
            print(f"→ Checking if resolved path exists...")
            if not os.path.exists(actual_font_path):
                print(f"→ ❌ Resolved path does not exist: {actual_font_path}")
                print(f"→ Original path was: {font_path}")
                print("→ Falling back to PIL default font")
                font = ImageFont.load_default()
                self.font_cache[(font_path, font_size)] = font
                return font
            else:
                print(f"→ ✅ Resolved path exists: {actual_font_path}")
            
            # Try to load the font
            print(f"→ Attempting to load font from: {actual_font_path}")
            try:
                font = ImageFont.truetype(actual_font_path, font_size)
                self.font_cache[(font_path, font_size)] = font
                print(f"→ ✅ Font loaded successfully!")
                return font
            except Exception as e:
                print(f"→ ❌ Failed to load font: {e}")
                print("→ Falling back to PIL default font")
                font = ImageFont.load_default()
                self.font_cache[(font_path, font_size)] = font
                return font
        else:
            print(f"→ Font found in cache")
        
        print(f"--- FONT LOADING COMPLETE ---\n")
        return self.font_cache[(font_path, font_size)]
    

    def get_regular_font(self, font_size):
        print(f"Getting regular font (size {font_size}) from: {self.regular_font_path}")
        return self.load_font(self.regular_font_path, font_size)

    def get_italic_font(self, font_size):
        print(f"Getting italic font (size {font_size}) from: {self.italic_font_path}")
        return self.load_font(self.italic_font_path, font_size)

    def get_bold_font(self, font_size):
        print(f"Getting bold font (size {font_size}) from: {self.bold_font_path}")
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
        
        # Use emoji fonts for emoji text (this is how emojis work in real life)
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
