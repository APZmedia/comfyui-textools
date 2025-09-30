#!/usr/bin/env python3
"""
Debug the main text renderer emoji logic
"""

from PIL import Image, ImageDraw
from utils.apz_font_manager import FontManager
from utils.apz_emoji_support import EmojiSupport

def debug_main_renderer():
    # Create font manager
    font_manager = FontManager("", "", "", 100)
    
    # Test text
    text = "Il freddo giusto per una fioritura perfetta! ❄️🌸🔥⭐"
    
    print(f"Original text: {text}")
    print(f"Has emoji: {font_manager.emoji_support.has_emoji(text)}")
    
    # Test splitting
    parts = font_manager.emoji_support.split_text_by_emoji(text)
    print(f"Split parts: {parts}")
    
    # Test individual chunks
    test_chunks = ["❄️", "🌸", "🔥", "⭐"]
    
    for chunk in test_chunks:
        print(f"\nTesting chunk: '{chunk}'")
        print(f"  Has emoji: {font_manager.emoji_support.has_emoji(chunk)}")
        
        if font_manager.emoji_support.has_emoji(chunk):
            emoji_parts = font_manager.emoji_support.split_text_by_emoji(chunk)
            print(f"  Split parts: {emoji_parts}")
            
            for emoji_part, is_emoji in emoji_parts:
                print(f"    Part: '{emoji_part}' (is_emoji: {is_emoji})")
                if is_emoji:
                    print(f"      This should be rendered as emoji")
                else:
                    print(f"      This should be rendered as text")

if __name__ == "__main__":
    debug_main_renderer()
