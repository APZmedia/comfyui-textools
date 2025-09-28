#!/usr/bin/env python3
"""
Download sample emoji PNGs for testing.
"""

import os
import requests
from PIL import Image, ImageDraw, ImageFont

def create_sample_emoji_pngs():
    """Create sample emoji PNGs for testing."""
    print("Creating Sample Emoji PNGs")
    print("=" * 50)
    
    # Create emoji directory
    emoji_dir = "fonts/emoji/png"
    os.makedirs(emoji_dir, exist_ok=True)
    
    # Sample emojis to create
    sample_emojis = [
        ("😀", "1f600.png"),  # Grinning face
        ("🎉", "1f389.png"),  # Party popper
        ("🚀", "1f680.png"),  # Rocket
        ("❤️", "2764.png"),   # Heart
        ("⭐", "2b50.png"),   # Star
    ]
    
    for emoji_char, filename in sample_emojis:
        # Create a simple colored square as placeholder
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a colored circle as placeholder
        color = (255, 100, 100)  # Red-ish
        draw.ellipse([8, 8, size-8, size-8], fill=color)
        
        # Add emoji text in the center
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        # Get text size and center it
        bbox = font.getbbox(emoji_char)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), emoji_char, fill=(255, 255, 255), font=font)
        
        # Save the emoji PNG
        filepath = os.path.join(emoji_dir, filename)
        img.save(filepath)
        print(f"✅ Created {filename} for {emoji_char}")
    
    print(f"\n📁 Sample emoji PNGs created in: {emoji_dir}")
    print("🎨 These are placeholder images - replace with real emoji PNGs for best results!")

if __name__ == "__main__":
    create_sample_emoji_pngs()
