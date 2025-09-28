#!/usr/bin/env python3
"""
Test emoji spacing to see what's happening.
"""

from utils.apz_markdown_parser import parse_markdown

def test_emoji_spacing():
    """Test emoji spacing."""
    print("=== Testing Emoji Spacing ===")
    
    test_cases = [
        "Hello 😀 World",
        "Hello 😀😀 World", 
        "**bold** 😀 text",
        "Hello **bold** 😀 World",
    ]
    
    for test_text in test_cases:
        print(f"\nTest: '{test_text}'")
        
        # Parse markdown
        parsed_parts = parse_markdown(test_text)
        print(f"Parsed parts: {len(parsed_parts)}")
        
        for i, (text_part, styles) in enumerate(parsed_parts):
            print(f"  Part {i}: '{text_part}' (styles: {styles})")
            print(f"    - Length: {len(text_part)}")
            print(f"    - Leading spaces: '{text_part[:len(text_part) - len(text_part.lstrip())]}'")
            print(f"    - Content: '{text_part.strip()}'")
            print(f"    - Trailing spaces: '{text_part[len(text_part.rstrip()):]}'")
            
            # Check if this part contains emojis
            for char in text_part:
                if ord(char) > 127:  # Non-ASCII character (likely emoji)
                    print(f"    - Contains emoji character: '{char}' (ord: {ord(char)})")

if __name__ == "__main__":
    test_emoji_spacing()
