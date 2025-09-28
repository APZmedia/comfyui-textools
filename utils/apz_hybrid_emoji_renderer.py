# hybrid_emoji_renderer.py
import os
import re
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class HybridEmojiRenderer:
    """
    Hybrid emoji renderer that uses PIL for text and system emoji rendering for emojis.
    This approach works around PIL's color emoji limitations.
    """
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        
        # Emoji pattern
        self.emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]'  # Emoticons
            r'|[\U0001F300-\U0001F5FF]'  # Misc Symbols and Pictographs
            r'|[\U0001F680-\U0001F6FF]'  # Transport and Map
            r'|[\U0001F1E0-\U0001F1FF]'  # Regional indicator symbols
            r'|[\U0001F900-\U0001F9FF]'  # Supplemental Symbols and Pictographs
            r'|[\U00002600-\U000026FF]'  # Miscellaneous symbols
            r'|[\U00002700-\U000027BF]'  # Dingbats
        )
    
    def has_emoji(self, text):
        """Check if text contains emojis."""
        return bool(self.emoji_pattern.search(text))
    
    def split_text_and_emojis(self, text):
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
    
    def render_text_with_emojis(self, text, font_family="Arial", font_size=24, 
                              color=(0, 0, 0), x=0, y=0):
        """
        Render text with emoji support.
        
        Args:
            text: Text to render (may contain emojis)
            font_family: Font family for non-emoji text
            font_size: Font size
            color: Text color
            x, y: Position
        """
        if not self.has_emoji(text):
            # No emojis, use regular PIL rendering
            try:
                font = ImageFont.truetype(font_family, font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()
            self.draw.text((x, y), text, fill=color, font=font)
            return
        
        # Split text and emojis
        parts = self.split_text_and_emojis(text)
        current_x = x
        current_y = y
        
        for text_part, is_emoji in parts:
            if is_emoji:
                # Try to render emoji with system fonts
                self._render_emoji(text_part, font_size, color, current_x, current_y)
            else:
                # Render regular text
                try:
                    font = ImageFont.truetype(font_family, font_size)
                except (OSError, IOError):
                    font = ImageFont.load_default()
                self.draw.text((current_x, current_y), text_part, fill=color, font=font)
            
            # Move to next position
            if is_emoji:
                # Estimate emoji width (rough approximation)
                current_x += font_size
            else:
                # Get actual text width
                try:
                    font = ImageFont.truetype(font_family, font_size)
                    bbox = font.getbbox(text_part)
                    current_x += bbox[2] - bbox[0]
                except (OSError, IOError):
                    current_x += len(text_part) * font_size // 2  # Rough estimate
    
    def _render_emoji(self, emoji, font_size, color, x, y):
        """Render a single emoji character."""
        # Try different emoji fonts
        emoji_fonts = [
            "Segoe UI Emoji",  # Windows
            "Apple Color Emoji",  # macOS
            "Noto Color Emoji",  # Cross-platform
            "Arial Unicode MS",  # Fallback
        ]
        
        for font_name in emoji_fonts:
            try:
                font = ImageFont.truetype(font_name, font_size)
                self.draw.text((x, y), emoji, fill=color, font=font)
                return
            except (OSError, IOError):
                continue
        
        # Fallback to default font
        try:
            font = ImageFont.load_default()
            self.draw.text((x, y), emoji, fill=color, font=font)
        except:
            # Last resort - render as text
            font = ImageFont.truetype("Arial", font_size)
            self.draw.text((x, y), emoji, fill=color, font=font)
    
    def render_rich_text(self, text_parts, font_family="Arial", font_size=24,
                        base_color=(0, 0, 0), bold_color=(0, 0, 0),
                        italic_color=(0, 0, 0), hashtag_color=(0, 100, 200),
                        x=0, y=0):
        """
        Render rich text with formatting and emoji support.
        
        Args:
            text_parts: List of (text, styles) tuples
            font_family: Base font family
            font_size: Base font size
            base_color: Default text color
            bold_color: Bold text color
            italic_color: Italic text color
            hashtag_color: Hashtag color
            x, y: Starting position
        """
        current_x = x
        current_y = y
        
        for text_part, styles in text_parts:
            # Determine font weight and style
            font_name = font_family
            if styles.get('b', False):  # Bold
                font_name = f"{font_family} Bold"
            if styles.get('i', False):  # Italic
                font_name = f"{font_family} Italic"
            
            # Determine color
            if styles.get('hashtag', False):
                color = hashtag_color
            elif styles.get('b', False):
                color = bold_color
            elif styles.get('i', False):
                color = italic_color
            else:
                color = base_color
            
            # Render the text part
            self.render_text_with_emojis(
                text_part, font_name, font_size, color, current_x, current_y
            )
            
            # Move to next position
            if self.has_emoji(text_part):
                current_x += font_size  # Rough estimate for emojis
            else:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    bbox = font.getbbox(text_part)
                    current_x += bbox[2] - bbox[0]
                except (OSError, IOError):
                    current_x += len(text_part) * font_size // 2  # Rough estimate
    
    def get_image(self):
        """Get the rendered image."""
        return self.image
    
    def save_to_file(self, filename):
        """Save the image to a file."""
        self.image.save(filename)

def test_hybrid_emoji():
    """Test hybrid emoji rendering."""
    print("Testing Hybrid Emoji Rendering")
    print("=" * 50)
    
    # Create renderer
    renderer = HybridEmojiRenderer(400, 200)
    
    # Test basic emoji rendering
    renderer.render_text_with_emojis(
        "Hello 😀 World 🎉 with 🚀 emojis!",
        font_family="Arial",
        font_size=24,
        color=(0, 0, 0),
        x=20, y=50
    )
    
    # Test rich text with emojis
    text_parts = [
        ("Hello ", {}),
        ("😀", {}),
        (" World ", {}),
        ("🎉", {}),
        (" with ", {}),
        ("#hashtag", {'hashtag': True}),
        (" 🚀", {})
    ]
    
    renderer.render_rich_text(
        text_parts,
        font_family="Arial",
        font_size=24,
        base_color=(0, 0, 0),
        hashtag_color=(0, 100, 200),
        x=20, y=100
    )
    
    # Save test image
    renderer.save_to_file("test_hybrid_emojis.png")
    print("✅ Saved test image: test_hybrid_emojis.png")
    
    return renderer.get_image()

if __name__ == "__main__":
    test_hybrid_emoji()
