#!/usr/bin/env python3
"""
Debug script to test emoji word splitting in text wrapper.
"""

from utils.apz_markdown_parser import parse_markdown
from PIL import ImageFont

def debug_emoji_word_splitting():
    """Debug emoji word splitting."""
    print("=== Debug Emoji Word Splitting ===")
    
    # Test text
    text = "Hello **World** *This is italic* with #hashtags and 😀 emojis"
    
    # Parse markdown
    parsed_parts = parse_markdown(text)
    
    print("Parsed parts:")
    for i, (text_part, styles) in enumerate(parsed_parts):
        print(f"  {i}: '{text_part}' -> {styles}")
        
        # Split by spaces to see how words are handled
        words = text_part.split(' ')
        print(f"    Words: {words}")
        
        # Test font loading
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            font = ImageFont.load_default()
        
        # Test width calculation for each word
        for j, word in enumerate(words):
            if word:  # Skip empty words
                bbox = font.getbbox(word)
                width = bbox[2] - bbox[0]
                print(f"      Word {j}: '{word}' -> width: {width}px")
                
                # Check if this word contains emoji
                if '😀' in word:
                    print(f"        *** EMOJI DETECTED IN WORD: '{word}' ***")
                    print(f"        Word length: {len(word)}")
                    print(f"        Word characters: {[c for c in word]}")
                    print(f"        Word bytes: {word.encode('utf-8')}")

if __name__ == "__main__":
    debug_emoji_word_splitting()
