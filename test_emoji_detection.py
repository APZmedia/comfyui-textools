#!/usr/bin/env python3
"""
Test emoji detection and PNG generation
"""

import re
from utils.apz_emoji_support import EmojiSupport
from utils.apz_emoji_png_renderer import EmojiPNGRenderer

def test_emoji_detection():
    # Test text with emojis
    test_text = "Il freddo giusto per una fioritura perfetta! ❄️🌸"
    
    print(f"Test text: {test_text}")
    print(f"Text length: {len(test_text)}")
    print(f"Characters: {[c for c in test_text]}")
    print(f"Unicode values: {[hex(ord(c)) for c in test_text]}")
    
    # Test emoji support
    es = EmojiSupport()
    print(f"Has emoji: {es.has_emoji(test_text)}")
    
    # Test pattern directly
    pattern = es.unicode_emoji_pattern
    match = pattern.search(test_text)
    print(f"Pattern match: {match}")
    
    # Test split
    parts = es.split_text_by_emoji(test_text)
    print(f"Split parts: {parts}")
    
    # Test PNG renderer
    png_renderer = EmojiPNGRenderer()
    print(f"PNG renderer has emoji: {png_renderer.has_emoji(test_text)}")
    
    # Test individual emojis
    snowflake = "❄️"
    cherry = "🌸"
    print(f"Snowflake: {snowflake}, length: {len(snowflake)}, unicode: {[hex(ord(c)) for c in snowflake]}")
    print(f"Cherry: {cherry}, length: {len(cherry)}, unicode: {[hex(ord(c)) for c in cherry]}")
    
    # Test pattern on individual emojis
    print(f"Snowflake match: {pattern.search(snowflake)}")
    print(f"Cherry match: {pattern.search(cherry)}")

if __name__ == "__main__":
    test_emoji_detection()
