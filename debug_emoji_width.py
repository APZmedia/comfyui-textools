#!/usr/bin/env python3
"""
Debug script to test emoji width calculation and line breaking.
"""

from utils.apz_markdown_parser import parse_markdown
from utils.apz_text_wrapper import wrap_text
from PIL import ImageFont

def debug_emoji_width():
    """Debug emoji width calculation."""
    print("=== Debug Emoji Width Calculation ===")
    
    # Test text with and without emoji
    text_with_emoji = "Hello **World** *This is italic* with #hashtags and 😀 emojis"
    text_without_emoji = "Hello **World** *This is italic* with #hashtags and emojis"
    
    print(f"Text with emoji: '{text_with_emoji}'")
    print(f"Text without emoji: '{text_without_emoji}'")
    
    # Parse both texts
    parsed_with_emoji = parse_markdown(text_with_emoji)
    parsed_without_emoji = parse_markdown(text_without_emoji)
    
    print(f"\nParsed with emoji ({len(parsed_with_emoji)} parts):")
    for i, (text, styles) in enumerate(parsed_with_emoji):
        print(f"  {i}: '{text}' -> {styles}")
    
    print(f"\nParsed without emoji ({len(parsed_without_emoji)} parts):")
    for i, (text, styles) in enumerate(parsed_without_emoji):
        print(f"  {i}: '{text}' -> {styles}")
    
    # Test font loading
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()
    
    # Test width calculation for emoji
    emoji_text = "😀"
    emoji_bbox = font.getbbox(emoji_text)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    print(f"\nEmoji '{emoji_text}' width: {emoji_width}")
    
    # Test width calculation for "emojis"
    word_text = "emojis"
    word_bbox = font.getbbox(word_text)
    word_width = word_bbox[2] - word_bbox[0]
    print(f"Word '{word_text}' width: {word_width}")
    
    # Test line width calculation
    test_line_with_emoji = "and 😀 emojis"
    test_line_without_emoji = "and emojis"
    
    line_bbox_with_emoji = font.getbbox(test_line_with_emoji)
    line_width_with_emoji = line_bbox_with_emoji[2] - line_bbox_with_emoji[0]
    
    line_bbox_without_emoji = font.getbbox(test_line_without_emoji)
    line_width_without_emoji = line_bbox_without_emoji[2] - line_bbox_without_emoji[0]
    
    print(f"\nLine with emoji: '{test_line_with_emoji}' -> width: {line_width_with_emoji}")
    print(f"Line without emoji: '{test_line_without_emoji}' -> width: {line_width_without_emoji}")
    print(f"Width difference: {line_width_with_emoji - line_width_without_emoji}")
    
    # Test wrapping with different max widths
    max_widths = [400, 500, 600, 700, 800]
    
    for max_width in max_widths:
        print(f"\n--- Max width: {max_width} ---")
        
        # Test with emoji
        wrapped_with_emoji, _ = wrap_text(parsed_with_emoji, font, max_width, 60)
        print(f"With emoji: {len(wrapped_with_emoji)} lines")
        for i, (line, parts) in enumerate(wrapped_with_emoji):
            print(f"  Line {i}: '{line}'")
        
        # Test without emoji
        wrapped_without_emoji, _ = wrap_text(parsed_without_emoji, font, max_width, 60)
        print(f"Without emoji: {len(wrapped_without_emoji)} lines")
        for i, (line, parts) in enumerate(wrapped_without_emoji):
            print(f"  Line {i}: '{line}'")

if __name__ == "__main__":
    debug_emoji_width()
