#!/usr/bin/env python3
"""
Script to regenerate corrupted emoji PNG files.
This will regenerate the multi-resolution PNG library using the current (correct) logic.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def regenerate_emoji_png(emoji_char, emoji_dir="fonts/emoji/png"):
    """Regenerate all resolution versions of an emoji PNG."""
    print(f"Regenerating emoji: {emoji_char}")
    
    # Get Unicode codepoint
    try:
        unicode_codepoint = ord(emoji_char)
        base_filename = f"{unicode_codepoint:x}"
    except TypeError:
        print(f"Invalid emoji character: {emoji_char}")
        return False
    
    # Define resolution ladder
    resolution_ladder = [
        ("tiny", 16),
        ("small", 32), 
        ("medium", 64),
        ("large", 128),
        ("xlarge", 256)
    ]
    
    # Try to use bundled emoji fonts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_fonts_dir = os.path.join(script_dir, "fonts", "emoji")
    
    emoji_font_paths = [
        os.path.join(bundled_fonts_dir, "NotoColorEmoji-Color.ttf"),
        os.path.join(bundled_fonts_dir, "NotoColorEmoji-Regular.ttf"),
        os.path.join(bundled_fonts_dir, "SegoeUIEmoji.ttf"),
    ]
    
    # Find available font
    emoji_font_path = None
    for font_path in emoji_font_paths:
        if os.path.exists(font_path):
            emoji_font_path = font_path
            break
    
    if not emoji_font_path:
        print("No emoji font found!")
        return False
    
    print(f"Using font: {emoji_font_path}")
    
    # Generate each resolution
    for res_name, res_size in resolution_ladder:
        try:
            # Try to load font at the target size first
            try:
                font = ImageFont.truetype(emoji_font_path, res_size)
                scale_factor = 1.0
            except OSError:
                # If it fails, use base size and scale
                base_size = 109  # NotoColorEmoji's preferred size
                font = ImageFont.truetype(emoji_font_path, base_size)
                scale_factor = res_size / base_size
            
            # Create transparent image
            img = Image.new("RGBA", (res_size, res_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Get text bounding box to center the emoji
            bbox = font.getbbox(emoji_char)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position to center the emoji
            x = (res_size - text_width) // 2
            y = (res_size - text_height) // 2
            
            # Apply scale factor if needed
            if scale_factor != 1.0:
                # Create a larger image, render, then scale down
                scaled_size = int(res_size * scale_factor)
                scaled_img = Image.new("RGBA", (scaled_size, scaled_size), (0, 0, 0, 0))
                scaled_draw = ImageDraw.Draw(scaled_img)
                try:
                    scaled_draw.text((x * scale_factor, y * scale_factor), emoji_char, font=font, embedded_color=True)
                except TypeError:
                    scaled_draw.text((x * scale_factor, y * scale_factor), emoji_char, font=font, fill=(0, 0, 0, 255))
                # Scale down to target size
                img = scaled_img.resize((res_size, res_size), Image.Resampling.LANCZOS)
            else:
                # Render directly at target size
                try:
                    draw.text((x, y), emoji_char, font=font, embedded_color=True)
                except TypeError:
                    # Fallback if embedded_color not supported
                    draw.text((x, y), emoji_char, font=font, fill=(0, 0, 0, 255))
            
            # Save PNG
            if res_name == "large":
                # Save base resolution (no suffix)
                base_path = os.path.join(emoji_dir, f"{base_filename}.png")
                img.save(base_path)
                print(f"Saved: {base_path}")
            
            # Save resolution-specific file
            res_path = os.path.join(emoji_dir, f"{base_filename}_{res_name}.png")
            img.save(res_path)
            print(f"Saved: {res_path}")
            
        except Exception as e:
            print(f"Error generating {res_name} ({res_size}px): {e}")
            return False
    
    return True

def main():
    """Regenerate specific problematic emojis."""
    # Test with the problematic emoji
    test_emojis = ["💫"]  # 1f4a0
    
    for emoji in test_emojis:
        success = regenerate_emoji_png(emoji)
        if success:
            print(f"✅ Successfully regenerated {emoji}")
        else:
            print(f"❌ Failed to regenerate {emoji}")

if __name__ == "__main__":
    main()
