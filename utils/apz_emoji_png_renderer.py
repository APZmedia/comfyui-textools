# emoji_png_renderer.py
import os
import re
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class EmojiPNGRenderer:
    """
    Renders emojis using transparent PNG files for perfect color emoji support.
    """
    
    def __init__(self, emoji_dir="fonts/emoji/png"):
        self.emoji_dir = emoji_dir
        self.emoji_cache = {}
        self.emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]'  # Emoticons
            r'|[\U0001F300-\U0001F5FF]'  # Misc Symbols
            r'|[\U0001F680-\U0001F6FF]'  # Transport
            r'|[\U0001F1E0-\U0001F1FF]'  # Regional indicators
            r'|[\U0001F900-\U0001F9FF]'  # Supplemental
            r'|[\U00002600-\U000026FF]'  # Misc symbols
            r'|[\U00002700-\U000027BF]'  # Dingbats
        )
    
    def has_emoji(self, text):
        """Check if text contains emojis."""
        return bool(self.emoji_pattern.search(text))
    
    def get_emoji_png_path(self, emoji_char):
        """Get the PNG file path for an emoji character."""
        # Extract the first emoji from the string if it contains multiple characters
        if len(emoji_char) > 1:
            # Find the first emoji in the string
            emoji_match = self.emoji_pattern.search(emoji_char)
            if emoji_match:
                emoji_char = emoji_match.group()
            else:
                return None
        
        # Convert emoji to filename (e.g., 😀 -> 1f600.png)
        unicode_codepoint = ord(emoji_char)
        filename = f"{unicode_codepoint:x}.png"
        return os.path.join(self.emoji_dir, filename)
    
    def load_emoji_png(self, emoji_char, size):
        """Load and cache emoji PNG at specified size. Generate if not available."""
        cache_key = (emoji_char, size)
        if cache_key in self.emoji_cache:
            return self.emoji_cache[cache_key]
        
        png_path = self.get_emoji_png_path(emoji_char)
        if os.path.exists(png_path):
            try:
                emoji_img = Image.open(png_path)
                # Resize to desired size
                emoji_img = emoji_img.resize((size, size), Image.Resampling.LANCZOS)
                self.emoji_cache[cache_key] = emoji_img
                return emoji_img
            except Exception as e:
                print(f"Failed to load emoji PNG {png_path}: {e}")
                # Fall through to generation
        else:
            print(f"Emoji PNG not found: {png_path}, generating...")
        
        # Generate emoji PNG if not available or failed to load
        emoji_img = self._generate_emoji_png(emoji_char, size)
        if emoji_img:
            self.emoji_cache[cache_key] = emoji_img
            # Save generated PNG for future use
            try:
                os.makedirs(os.path.dirname(png_path), exist_ok=True)
                emoji_img.save(png_path)
                print(f"Generated and saved emoji PNG: {png_path}")
            except Exception as e:
                print(f"Warning: Could not save generated emoji PNG: {e}")
            return emoji_img
        
        return None
    
    def _generate_emoji_png(self, emoji_char, size):
        """Generate emoji PNG using the best available emoji font."""
        try:
            # Try to use the bundled emoji fonts first
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            bundled_fonts_dir = os.path.join(project_root, "fonts", "emoji")
            
            # List of bundled emoji fonts to try
            emoji_font_paths = [
                os.path.join(bundled_fonts_dir, "NotoColorEmoji-Color.ttf"),
                os.path.join(bundled_fonts_dir, "NotoColorEmoji-Regular.ttf"),
                os.path.join(bundled_fonts_dir, "SegoeUIEmoji.ttf"),
            ]
            
            for font_path in emoji_font_paths:
                if os.path.exists(font_path):
                    try:
                        # Try to load at the requested size first
                        font = ImageFont.truetype(font_path, size)
                        return self._render_emoji_to_png(emoji_char, font, size)
                    except OSError:
                        # If it fails, try with a base size and scale
                        try:
                            base_size = 109  # NotoColorEmoji's preferred size
                            font = ImageFont.truetype(font_path, base_size)
                            return self._render_emoji_to_png(emoji_char, font, size, scale_factor=size/base_size)
                        except OSError:
                            continue
            
            # Fallback to system default font
            font = ImageFont.load_default()
            return self._render_emoji_to_png(emoji_char, font, size)
            
        except Exception as e:
            print(f"Failed to generate emoji PNG for {emoji_char}: {e}")
            return None
    
    def _render_emoji_to_png(self, emoji_char, font, size, scale_factor=1.0):
        """Render emoji character to PNG image."""
        try:
            # Create a transparent image
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Get text bounding box to center the emoji
            bbox = font.getbbox(emoji_char)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position to center the emoji
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            # Apply scale factor if needed
            if scale_factor != 1.0:
                # Create a larger image, render, then scale down
                scaled_size = int(size * scale_factor)
                scaled_img = Image.new("RGBA", (scaled_size, scaled_size), (0, 0, 0, 0))
                scaled_draw = ImageDraw.Draw(scaled_img)
                scaled_draw.text((x * scale_factor, y * scale_factor), emoji_char, font=font, embedded_color=True)
                # Scale down to target size
                img = scaled_img.resize((size, size), Image.Resampling.LANCZOS)
            else:
                # Render directly at target size
                try:
                    draw.text((x, y), emoji_char, font=font, embedded_color=True)
                except TypeError:
                    # Fallback if embedded_color not supported
                    draw.text((x, y), emoji_char, font=font, fill=(0, 0, 0, 255))
            
            return img
            
        except Exception as e:
            print(f"Failed to render emoji {emoji_char}: {e}")
            return None
    
    def render_text_with_emoji_pngs(self, draw, text, font, font_size, x, y, color):
        """Render text with emoji PNGs embedded."""
        current_x = x
        current_y = y
        
        # Split text into emoji and non-emoji parts
        parts = self.split_text_and_emojis(text)
        
        for text_part, is_emoji in parts:
            if is_emoji:
                # Render emoji as PNG
                emoji_img = self.load_emoji_png(text_part, font_size)
                if emoji_img:
                    # Paste emoji onto the image
                    draw._image.paste(emoji_img, (int(current_x), int(current_y)), emoji_img)
                    current_x += font_size
                else:
                    # Fallback to text rendering
                    draw.text((current_x, current_y), text_part, fill=color, font=font)
                    bbox = font.getbbox(text_part)
                    current_x += bbox[2] - bbox[0]
            else:
                # Render regular text
                draw.text((current_x, current_y), text_part, fill=color, font=font)
                bbox = font.getbbox(text_part)
                current_x += bbox[2] - bbox[0]
    
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

def create_emoji_png_library():
    """Create a basic emoji PNG library structure."""
    emoji_dir = "fonts/emoji/png"
    os.makedirs(emoji_dir, exist_ok=True)
    
    # Create README for emoji PNG library
    readme_content = """# Emoji PNG Library

This directory should contain transparent PNG files for emojis.

## File Naming Convention:
- Use Unicode codepoint as filename (e.g., 😀 = 1f600.png)
- Files should be transparent PNGs
- Recommended size: 64x64 or 128x128 pixels

## How to Add Emojis:
1. Download emoji PNGs from sources like:
   - https://emojipedia.org/
   - https://github.com/googlefonts/noto-emoji
   - https://twemoji.maxcdn.com/
2. Convert to transparent PNGs
3. Name files using Unicode codepoint
4. Place in this directory

## Example:
- 😀 (U+1F600) → 1f600.png
- 🎉 (U+1F389) → 1f389.png
- 🚀 (U+1F680) → 1f680.png
"""
    
    with open(os.path.join(emoji_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"Created emoji PNG library structure at: {emoji_dir}")
    print("Add transparent PNG emoji files to enable color emoji support!")

if __name__ == "__main__":
    create_emoji_png_library()
