#!/usr/bin/env python3
"""
Test the PNG emoji approach.
"""

from PIL import Image, ImageDraw
from utils.apz_emoji_png_renderer import EmojiPNGRenderer

def test_png_emoji_approach():
    """Test the PNG emoji rendering approach."""
    print("Testing PNG Emoji Approach")
    print("=" * 50)
    
    # Create test image
    img = Image.new('RGBA', (400, 200), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Create emoji PNG renderer
    emoji_renderer = EmojiPNGRenderer()
    
    # Test text with emojis
    test_text = "Hello 😀 World 🎉 with 🚀 emojis!"
    
    print(f"Testing text: {test_text}")
    print(f"Has emojis: {emoji_renderer.has_emoji(test_text)}")
    
    # Split text into parts
    parts = emoji_renderer.split_text_and_emojis(test_text)
    print(f"Text parts: {parts}")
    
    # Try to load emoji PNGs
    for text_part, is_emoji in parts:
        if is_emoji:
            png_path = emoji_renderer.get_emoji_png_path(text_part)
            print(f"Emoji {text_part}: {png_path}")
            print(f"  File exists: {os.path.exists(png_path)}")
    
    # Save test image
    img.save("test_png_emoji_approach.png")
    print("💾 Saved test image: test_png_emoji_approach.png")
    
    print("\n📝 To enable color emojis:")
    print("1. Download transparent PNG emojis")
    print("2. Name them using Unicode codepoint (e.g., 1f600.png for 😀)")
    print("3. Place them in fonts/emoji/png/ directory")
    print("4. Restart ComfyUI")

if __name__ == "__main__":
    import os
    test_png_emoji_approach()
