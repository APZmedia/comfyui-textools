# emoji_support.py
import re
import os
import platform
from PIL import ImageFont, Image, ImageDraw

class EmojiSupport:
    """
    Enhanced emoji support with font fallback system.
    """
    
    def __init__(self, custom_emoji_font_url=None):
        self.custom_emoji_font_url = custom_emoji_font_url
        self.emoji_fonts = self._get_emoji_font_paths()
        self.emoji_font_cache = {}
        self.font_metadata = {}
        self._color_font_keywords = (
            "notocoloremoji",
            "color emoji",
            "seguiemj",
            "segoeuemoji",
            "twemoji",
            "apple color emoji",
        )
        self.embedded_color_supported = self._detect_embedded_color_support()
        self._warned_color_without_support = False
        # Comprehensive emoji pattern covering all major Unicode emoji blocks
        # This pattern matches emoji sequences including variation selectors
        self.unicode_emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]'  # Emoticons
            r'|[\U0001F300-\U0001F5FF]'  # Misc Symbols and Pictographs
            r'|[\U0001F680-\U0001F6FF]'  # Transport and Map
            r'|[\U0001F1E0-\U0001F1FF]'  # Regional indicator symbols
            r'|[\U0001F900-\U0001F9FF]'  # Supplemental Symbols and Pictographs
            r'|[\U00002600-\U000026FF]'  # Miscellaneous symbols
            r'|[\U00002700-\U000027BF]'  # Dingbats
            r'|[\U00002744]'  # Snowflake ❄
            r'|[\U0001F338]'  # Cherry blossom 🌸
            r'|[\U00002B50]'  # Star ⭐
            r'|[\U0001F000-\U0001F02F]'  # Mahjong tiles and other symbols
            r'|[\U0001F300-\U0001F5FF]'  # Weather and nature symbols
            r'|[\U0001F400-\U0001F4FF]'  # Animals and objects
            r'|[\U0001F500-\U0001F5FF]'  # Audio and video symbols
            r'|[\U0001F600-\U0001F64F]'  # Face symbols
            r'|[\U0001F680-\U0001F6FF]'  # Transport symbols
            r'|[\U0001F700-\U0001F77F]'  # Alchemical symbols
            r'|[\U0001F780-\U0001F7FF]'  # Geometric shapes extended
            r'|[\U0001F800-\U0001F8FF]'  # Supplemental arrows-C
            r'|[\U0001F900-\U0001F9FF]'  # Supplemental symbols and pictographs
            r'|[\U0001FA00-\U0001FA6F]'  # Chess symbols
            r'|[\U0001FA70-\U0001FAFF]'  # Symbols and pictographs extended-A
            r'|[\U0001FB00-\U0001FBFF]'  # Symbols for legacy computing
            r'|[\U0001FC00-\U0001FCFF]'  # Symbols for legacy computing
            r'|[\U0001FD00-\U0001FDFF]'  # Symbols for legacy computing
            r'|[\U0001FE00-\U0001FEFF]'  # Variation selectors
            r'|[\U0001FF00-\U0001FFFF]'  # Symbols for legacy computing
        )
        
        # Pattern for emoji sequences (emoji + variation selectors)
        self.emoji_sequence_pattern = re.compile(
            r'[\U0001F600-\U0001F64F][\U0000FE00-\U0000FE0F]*'  # Emoticons with selectors
            r'|[\U0001F300-\U0001F5FF][\U0000FE00-\U0000FE0F]*'  # Misc Symbols with selectors
            r'|[\U0001F680-\U0001F6FF][\U0000FE00-\U0000FE0F]*'  # Transport with selectors
            r'|[\U0001F1E0-\U0001F1FF][\U0001F1E0-\U0001F1FF]*'  # Regional indicators
            r'|[\U0001F900-\U0001F9FF][\U0000FE00-\U0000FE0F]*'  # Supplemental with selectors
            r'|[\U00002600-\U000026FF][\U0000FE00-\U0000FE0F]*'  # Misc symbols with selectors
            r'|[\U00002700-\U000027BF][\U0000FE00-\U0000FE0F]*'  # Dingbats with selectors
            r'|[\U00002744][\U0000FE00-\U0000FE0F]*'  # Snowflake with selectors
            r'|[\U0001F338][\U0000FE00-\U0000FE0F]*'  # Cherry blossom with selectors
            r'|[\U00002B50][\U0000FE00-\U0000FE0F]*'  # Star with selectors
        )

    def _detect_embedded_color_support(self):
        """
        Detect whether the current Pillow build supports embedded_color parameter
        for ImageDraw.text. This is required to render glyph palette colors.
        """
        try:
            test_image = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
            test_draw = ImageDraw.Draw(test_image)
            test_font = ImageFont.load_default()
            # Attempt to draw with embedded_color flag. We do not care about output,
            # only that the call succeeds without raising a TypeError.
            test_draw.text((0, 0), " ", font=test_font, embedded_color=True)
            return True
        except TypeError:
            return False
        except Exception:
            return False

    def _is_probable_color_font(self, font_path):
        """
        Heuristic detection for fonts that embed color glyph palettes.
        """
        if not font_path:
            return False
        basename = os.path.basename(font_path).lower()
        return any(keyword in basename for keyword in self._color_font_keywords)

    def _record_font_metadata(self, font_path, font_obj):
        """
        Track metadata about loaded emoji fonts so renderers can decide whether to
        request embedded color glyph rendering.
        """
        if font_obj is None:
            return

        is_color_font = self._is_probable_color_font(font_path)
        self.font_metadata[id(font_obj)] = {
            "path": font_path,
            "is_color_font": is_color_font,
        }

        if is_color_font and not self.embedded_color_supported and not self._warned_color_without_support:
            print(
                "Warning: Emoji font supports color glyphs, but the current Pillow build "
                "does not expose embedded_color. Falling back to monochrome rendering."
            )
            self._warned_color_without_support = True

    def should_use_embedded_color(self, font_obj):
        """
        Determine if the provided font should be rendered with embedded color glyphs.
        """
        if not self.embedded_color_supported or font_obj is None:
            return False

        metadata = self.font_metadata.get(id(font_obj))
        if not metadata:
            return False

        return metadata.get("is_color_font", False)

    def is_color_font(self, font_obj):
        """
        Check if the font was identified as a color emoji font.
        """
        metadata = self.font_metadata.get(id(font_obj))
        if not metadata:
            return False
        return metadata.get("is_color_font", False)
    
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
                # Debug logging removed for performance
            except Exception as e:
                # Debug logging removed for performance
                pass
        
        # Prioritize bundled fonts
        bundled_fonts = [
            os.path.join(bundled_fonts_dir, "NotoColorEmoji-Color.ttf"),  # Color emoji font (with scaling)
            os.path.join(bundled_fonts_dir, "SegoeUIEmoji.ttf"),  # Windows emoji font (monochrome fallback)
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
        
        # Combine custom, bundled, and system fonts (prioritize bundled fonts for serverless)
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
        Handles variable fonts and special cases for color emoji fonts.
        
        Args:
            font_size: Font size to use
            
        Returns:
            PIL ImageFont object or None if no emoji font available
        """
        cache_key = (font_size, "emoji")
        if cache_key in self.emoji_font_cache:
            cached_font = self.emoji_font_cache[cache_key]
            if id(cached_font) not in self.font_metadata:
                self._record_font_metadata(None, cached_font)
            return cached_font
        
        # Try system emoji fonts first (for local development)
        # Note: These may not work in serverless pods
        system_fonts = [
            "Segoe UI Emoji",      # Windows
            "Apple Color Emoji",   # macOS  
            "Noto Color Emoji",    # Linux
            "Twemoji",             # Alternative
        ]
        
        for font_name in system_fonts:
            try:
                font = ImageFont.truetype(font_name, font_size)
                self._record_font_metadata(font_name, font)
                self.emoji_font_cache[cache_key] = font
                # Debug logging removed for performance
                return font
            except OSError:
                continue
        
        # Try bundled fonts (serverless-safe fallback)
        for font_path in self.emoji_fonts:
            try:
                # Try to load the font at the requested size first
                font = ImageFont.truetype(font_path, font_size)
                self._record_font_metadata(font_path, font)
                self.emoji_font_cache[cache_key] = font
                # Debug logging removed for performance
                return font
            except OSError as e:
                # If NotoColorEmoji fails at requested size, try a scaled approach
                if "NotoColorEmoji" in font_path:
                    try:
                        # Try to load at a base size and then scale
                        base_size = 109  # NotoColorEmoji's preferred size
                        font = ImageFont.truetype(font_path, base_size)
                        self._record_font_metadata(font_path, font)
                        # Store the scale factor for later use
                        scale_factor = font_size / base_size
                        font.scale_factor = scale_factor
                        self.emoji_font_cache[cache_key] = font
                        # Debug logging removed for performance
                        return font
                    except OSError:
                        # Debug logging removed for performance
                        continue
                else:
                    # Debug logging removed for performance
                    continue
            except (OSError, IOError) as e:
                # Debug logging removed for performance
                continue
        
        # Fallback to default font
        try:
            font = ImageFont.load_default()
            self._record_font_metadata(None, font)
            self.emoji_font_cache[cache_key] = font
            # Debug logging removed for performance
            return font
        except Exception:
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
            # Debug logging removed for performance
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
    
    def get_emoji_scale_factor(self, font_size):
        """
        Get the scale factor for emoji fonts that require fixed sizes.
        
        Args:
            font_size: Desired font size
            
        Returns:
            Scale factor to apply to emoji rendering
        """
        # Check if we're using NotoColorEmoji at fixed size 109
        # Only apply scaling if the font was actually loaded at size 109
        for font_path in self.emoji_fonts:
            if "NotoColorEmoji" in font_path and os.path.exists(font_path):
                try:
                    # Try to load at requested size first
                    test_font = ImageFont.truetype(font_path, font_size)
                    # If successful, no scaling needed
                    return 1.0
                except OSError:
                    # If it fails, we'll need to use size 109 and scale
                    return font_size / 109.0
        return 1.0
    
    def split_text_by_emoji(self, text):
        """
        Split text into emoji and non-emoji parts.
        Uses emoji sequence pattern to handle variation selectors properly.
        Handles multiple consecutive emojis correctly.
        
        Args:
            text: Input text
            
        Returns:
            List of (text_part, is_emoji) tuples
        """
        parts = []
        current_pos = 0
        
        # First try to match emoji sequences (emoji + variation selectors)
        for match in self.emoji_sequence_pattern.finditer(text):
            start, end = match.span()
            
            # Add non-emoji text before this emoji sequence
            if start > current_pos:
                parts.append((text[current_pos:start], False))
            
            # Add emoji sequence (can contain multiple consecutive emojis)
            emoji_text = match.group()
            parts.append((emoji_text, True))
            current_pos = end
        
        # If no emoji sequences found, fall back to individual emoji matching
        if current_pos == 0:
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
