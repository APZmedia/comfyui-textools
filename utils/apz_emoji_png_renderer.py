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
        # Handle multi-character emojis by taking the first character
        if len(emoji_char) > 1:
            emoji_char = emoji_char[0]
        
        try:
            unicode_codepoint = ord(emoji_char)
            filename = f"{unicode_codepoint:x}.png"
            return os.path.join(self.emoji_dir, filename)
        except TypeError:
            # If still having issues, return None to fall back to font rendering
            return None
    
    def load_emoji_png(self, emoji_char, size):
        """Load and cache emoji PNG at specified size with smart resolution selection."""
        # Emoji PNG loading logging removed for performance
        cache_key = (emoji_char, size)
        if cache_key in self.emoji_cache:
            # Cached emoji logging removed for performance
            return self.emoji_cache[cache_key]
        
        # Always generate high-quality PNG emojis from fonts
        # This ensures consistent, crisp emoji rendering
        # Emoji generation logging removed for performance
        emoji_img = self._generate_emoji_png(emoji_char, size)
        if emoji_img:
            self.emoji_cache[cache_key] = emoji_img
            # Save high-quality PNG for future use
            try:
                os.makedirs(os.path.dirname(self.get_emoji_png_path(emoji_char)), exist_ok=True)
                # Save at the actual rendered size for maximum quality
                emoji_img.save(self.get_emoji_png_path(emoji_char))
                # Debug logging removed for performance
            except Exception as e:
                # Debug logging removed for performance
                pass
            return emoji_img
        
        return None
    
    def _find_best_resolution_png(self, emoji_char, target_size):
        """Find the best resolution PNG using a ladder approach for optimal quality."""
        # Handle multi-character emojis by taking the first character
        if len(emoji_char) > 1:
            emoji_char = emoji_char[0]
        
        try:
            unicode_codepoint = ord(emoji_char)
            base_filename = f"{unicode_codepoint:x}"
        except TypeError:
            return None
        
        # Define resolution ladder (ordered by size)
        resolution_ladder = [
            ("tiny", 16),      # 16px - smallest
            ("small", 32),     # 32px - small
            ("medium", 64),    # 64px - medium
            ("large", 128),    # 128px - large
            ("xlarge", 256)    # 256px - largest
        ]
        
        # Strategy: Find the best resolution for the target size
        # Prefer downscaling over upscaling for better quality
        best_resolution = None
        best_size = None
        
        # First pass: Look for the largest resolution <= target_size (prefer downscaling)
        for res_name, res_size in reversed(resolution_ladder):
            if res_size <= target_size:
                path = os.path.join(self.emoji_dir, f"{base_filename}_{res_name}.png")
                if os.path.exists(path):
                    best_resolution = res_name
                    best_size = res_size
                    # Debug logging removed for performance
                    break
        
        # If we found a suitable resolution, use it
        if best_resolution:
            return os.path.join(self.emoji_dir, f"{base_filename}_{best_resolution}.png")
        
        # Second pass: If no resolution <= target_size, find the smallest available
        # This handles cases where target_size < 16px
        for res_name, res_size in resolution_ladder:
            path = os.path.join(self.emoji_dir, f"{base_filename}_{res_name}.png")
            if os.path.exists(path):
                # Debug logging removed for performance
                return path
        
        # Fallback to base resolution (no suffix)
        base_path = os.path.join(self.emoji_dir, f"{base_filename}.png")
        if os.path.exists(base_path):
            return base_path
        
        return None
    
    def _generate_emoji_png(self, emoji_char, size):
        """Generate high-quality emoji PNG using super-sampling for crisp rendering."""
        # Generate emoji at 80% of requested size for better text alignment
        target_size = int(size * 0.8)  # 80% of requested size
        # Debug logging removed for performance
        try:
            # Use super-sampling for better quality: render at 2x size, then scale down
            render_size = target_size * 2  # Render at double resolution for crispness
            # Debug logging removed for performance
            
            # Try system emoji fonts first (these work at any size)
            system_fonts = [
                "Segoe UI Emoji",  # Windows
                "Apple Color Emoji",  # macOS
                "Noto Color Emoji",  # Linux
                "Twemoji",  # Alternative
            ]
            
            for font_name in system_fonts:
                try:
                    # Try to load system font at the super-sampled size
                    font = ImageFont.truetype(font_name, render_size)
                    # Debug logging removed for performance
                    # Render at high resolution, then scale down for crispness
                    return self._render_emoji_to_png(emoji_char, font, target_size, scale_factor=2.0)
                except OSError:
                    continue
            
            # Try bundled fonts as fallback
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            bundled_fonts_dir = os.path.join(project_root, "fonts", "emoji")
            
            bundled_font_paths = [
                os.path.join(bundled_fonts_dir, "SegoeUIEmoji.ttf"),
                os.path.join(bundled_fonts_dir, "NotoColorEmoji-Color.ttf"),
                os.path.join(bundled_fonts_dir, "NotoColorEmoji-Regular.ttf"),
            ]
            
            for font_path in bundled_font_paths:
                if os.path.exists(font_path):
                    try:
                        # Try to load at the super-sampled size first
                        font = ImageFont.truetype(font_path, render_size)
                        # Debug logging removed for performance
                        return self._render_emoji_to_png(emoji_char, font, target_size, scale_factor=2.0)
                    except OSError:
                        # If it fails, try with a base size and scale
                        try:
                            base_size = max(109, render_size)  # Use larger base size for quality
                            font = ImageFont.truetype(font_path, base_size)
                            scale_factor = render_size / base_size
                            # Debug logging removed for performance
                            return self._render_emoji_to_png(emoji_char, font, target_size, scale_factor=scale_factor)
                        except OSError:
                            continue
            
            # Final fallback to system default font
            font = ImageFont.load_default()
            return self._render_emoji_to_png(emoji_char, font, target_size)
            
        except Exception as e:
            # Debug logging removed for performance
            return None
    
    def _render_emoji_to_png(self, emoji_char, font, size, scale_factor=1.0):
        """Render high-quality emoji character to PNG image using super-sampling."""
        try:
            # Get text bounding box first to determine proper image size
            bbox = font.getbbox(emoji_char)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Create image exactly the size of the emoji content
            # Use no padding to eliminate extra spacing
            padding = 0  # No padding
            img_width = text_width  # Use actual text width only
            img_height = text_height  # Use actual text height only
            
            # Create a transparent image at the calculated size
            img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
            
            # Apply scale factor for super-sampling
            if scale_factor != 1.0:
                # Create a larger image for super-sampling, render, then scale down
                scaled_size = int(size * scale_factor)
                scaled_img_width = int(text_width * scale_factor)
                scaled_img_height = int(text_height * scale_factor)
                scaled_img = Image.new("RGBA", (scaled_img_width, scaled_img_height), (0, 0, 0, 0))
                scaled_draw = ImageDraw.Draw(scaled_img)
                
                # Calculate proper positioning to prevent cropping
                # The bbox gives us the actual content boundaries
                # We need to position the emoji so its visual content fits properly
                x = -bbox[0]  # Offset by left margin
                y = -bbox[1]  # Offset by top margin
                
                # Debug logging removed for performance
                # Debug logging removed for performance
                
                # Render the emoji at high resolution
                try:
                    scaled_draw.text((x, y), emoji_char, font=font, embedded_color=True)
                except TypeError:
                    # Fallback if embedded_color not supported
                    scaled_draw.text((x, y), emoji_char, font=font, fill=(0, 0, 0, 255))
                
                # Scale down to target size using LANCZOS for maximum quality
                # Scale to the actual content dimensions
                final_width = text_width
                final_height = text_height
                img = scaled_img.resize((final_width, final_height), Image.Resampling.LANCZOS)
                # Debug logging removed for performance
            else:
                # Render directly at target size
                draw = ImageDraw.Draw(img)
                
                # Calculate proper positioning to prevent cropping
                x = -bbox[0]  # Offset by left margin
                y = -bbox[1]  # Offset by top margin
                
                # Debug logging removed for performance
                # Debug logging removed for performance
                
                try:
                    draw.text((x, y), emoji_char, font=font, embedded_color=True)
                except TypeError:
                    # Fallback if embedded_color not supported
                    draw.text((x, y), emoji_char, font=font, fill=(0, 0, 0, 255))
            
            return img
            
        except Exception as e:
            # Debug logging removed for performance
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
        """Split text into emoji and non-emoji parts, handling multiple consecutive emojis."""
        parts = []
        current_pos = 0
        
        for match in self.emoji_pattern.finditer(text):
            start, end = match.span()
            
            # Add non-emoji text before this emoji
            if start > current_pos:
                parts.append((text[current_pos:start], False))
            
            # Add emoji (handle multiple consecutive emojis)
            emoji_text = match.group()
            parts.append((emoji_text, True))
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
    
    # Debug logging removed for performance
    print("Add transparent PNG emoji files to enable color emoji support!")

if __name__ == "__main__":
    create_emoji_png_library()
