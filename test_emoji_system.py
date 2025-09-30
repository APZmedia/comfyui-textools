#!/usr/bin/env python3
"""
Test which emoji system is being used
"""

from utils.apz_emoji_support import EmojiSupport
from utils.apz_twemoji_renderer import TwemojiRenderer
from utils.apz_emoji_png_renderer import EmojiPNGRenderer

def test_emoji_systems():
    text = "Il freddo giusto per una fioritura perfetta! ❄️🌸"
    
    print("=== Testing Emoji Systems ===")
    print(f"Text: {text}")
    
    # Test emoji support
    es = EmojiSupport()
    parts = es.split_text_by_emoji(text)
    print(f"\nSplit parts: {parts}")
    
    # Test Twemoji system
    print("\n=== Twemoji System ===")
    twemoji_renderer = TwemojiRenderer(use_svg=False)
    
    for emoji_part, is_emoji in parts:
        if is_emoji:
            print(f"Testing Twemoji for: '{emoji_part}'")
            img = twemoji_renderer.render_emoji(emoji_part, 72)
            if img:
                print(f"  ✅ Twemoji loaded: {img.size}, Mode: {img.mode}")
            else:
                print(f"  ❌ Twemoji failed")
    
    # Test bundled PNG system
    print("\n=== Bundled PNG System ===")
    png_renderer = EmojiPNGRenderer()
    
    for emoji_part, is_emoji in parts:
        if is_emoji:
            print(f"Testing bundled PNG for: '{emoji_part}'")
            img = png_renderer.load_emoji_png(emoji_part, 72)
            if img:
                print(f"  ✅ Bundled PNG loaded: {img.size}, Mode: {img.mode}")
            else:
                print(f"  ❌ Bundled PNG failed")

if __name__ == "__main__":
    test_emoji_systems()
